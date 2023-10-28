# -*- coding:utf-8 -*-
"""
监听器，流计算逻辑。
# author: Trico
# date: 2021/1/4
# update: 2021/1/4
"""

import json
import logging
import requests
import traceback
import elasticsearch
import multiprocessing

from lib_conf.config import api_host, kafka_topics, log_path, es_config
from common_utils.llog import LLog
from common_utils.kafka.kafka_utils import dc_kafka_consumer, dc_kafka_producer
from common_utils.get_public_params import get_baidu_tags_to_classifications_map, get_data_plural_singular_map


class KafkaListenerA1FromOriginToFlowCompute(object):
    """
    监听Kafka，监听爬虫一手数据。
    批数据会被切分为流数据。
    """

    def __init__(self, logger):
        # 日志对象。
        assert isinstance(logger, logging.Logger), "Error param, logger."
        self._logger = logger

        # kafka主题。
        self._src_topic = kafka_topics["origin"]
        self._dst_topic = kafka_topics["flowComputed"]

        # 接口地址。
        self._api_url_flow_compute_baidu_api_nlp = f"{api_host}/dc/flow_compute/baidu_api/nlp/"
        self._api_url_flow_compute_simhash = f"{api_host}/dc/flow_compute/common/get_simhash_value/"
        # 接口超时时间。
        self._api_timeout = 60

        # 公共参数，百度作品分类和作品归类的映射。
        self._baidu_tags_to_classifications_map = get_baidu_tags_to_classifications_map()

        # 复数与单数映射。
        self._plural_singular_map = get_data_plural_singular_map(map_direction="p_s")
        # 单数与复数映射。
        self._singular_plural_map = get_data_plural_singular_map(map_direction="s_p")

        # ES连接。
        self._es_conn = elasticsearch.Elasticsearch(**es_config)
        # 作品索引，检查数据是否已存在于该索引中，如果存在则不再进行流计算，直接返回。
        self._index_dc_works = "dc_works"
        self._doc_type_dc_works = "_doc"

    def flow_compute_simhash(self, works):
        """
        计算simhash值，用于匹配相似文章。
        :return:
        """

        # 经流计算接口完成数据补充。
        try:
            content = works.get("content", "")
            if content:
                post_data = {"content": content, "need_cleaning": "need"}
                resp = requests.post(
                    self._api_url_flow_compute_simhash,
                    json=post_data,
                    timeout=self._api_timeout
                )
                if resp.status_code == requests.codes.ok:
                    if resp.content:
                        resp = json.loads(resp.content)
                        if "data" in resp and resp["data"]:
                            works["simhash"] = resp["data"]
                    else:
                        raise ValueError(f"接口请求失败，{resp.reason}，{self._api_url_flow_compute_simhash}")
                else:
                    raise ValueError(f"接口请求失败，{resp.status_code}，{self._api_url_flow_compute_simhash}")
        except Exception as e:
            self._logger.warning(f"{e}\n{traceback.format_exc()}")
        finally:
            return works

    def flow_compute_baidu_api_nlp(
            self, works,
            # nlp_functions=("emotion", "label", "participles", "abstract", "classified", "frequency")
            # 只保留分词和词频，2021年1月26日。
            nlp_functions=("classified", "frequency", "participles")
    ):
        """
        百度自然语言分析接口。
        :return:
        """

        # 经流计算接口完成数据补充。
        try:
            title = works.get("title", "")
            content = works.get("content", "")
            # 计算选项。
            nlp_functions = list(nlp_functions)
            if title and content:
                post_data = {"title": title, "content": content, "nlp_function": nlp_functions}
                resp = requests.post(
                    self._api_url_flow_compute_baidu_api_nlp,
                    json=post_data,
                    timeout=self._api_timeout
                )
                if resp.status_code == requests.codes.ok:
                    if resp.content:
                        nlp_result = json.loads(resp.content)
                        if "data" in nlp_result and nlp_result["data"]:
                            nlp_res_data = nlp_result["data"]

                            # 词频。
                            # noinspection PyBroadException
                            try:
                                word_frequency = nlp_res_data["计算词频"]
                                works["wordFrequency"] = [dict(word=x[0], times=x[1]) for x in word_frequency]
                                works["wordFrequencyLength"] = len(word_frequency)
                            except Exception:
                                works["wordFrequency"] = None
                                works["wordFrequencyLength"] = 0

                            # 文章归类。
                            # noinspection PyBroadException
                            try:
                                tags_info = nlp_res_data["文章归类"]
                                if tags_info:
                                    # 百度的归类信息。
                                    tags = list()
                                    # 前端需要的归类信息ID列表。
                                    classifications = works.get("classifications", list())
                                    # 逐级遍历，多级结构调整为单级结构存储。
                                    for tag_info in tags_info:
                                        for key in ("lv1_tag_list", "lv2_tag_list"):
                                            tag_level_list = tag_info.get(key, [])
                                            for tag in tag_level_list:
                                                try:
                                                    # 归类信息。
                                                    tags.append(dict(tag=tag["tag"], score=tag["score"]))
                                                    # 前端需要的归类信息ID。
                                                    class_item = self._baidu_tags_to_classifications_map.get(
                                                        tag["tag"])
                                                    if class_item is not None:
                                                        classifications.append(class_item["id"])
                                                except Exception as e:
                                                    self._logger.debug(f"{e}\n{traceback.format_exc()}")
                                    works["tags"] = tags
                                    works["tagsLength"] = len(tags)
                                    works["hasDiscovery"] = 1
                                    works["classifications"] = classifications
                                else:
                                    raise ValueError("没有解析出文章归类")
                            except Exception:
                                works["tags"] = None
                                works["tagsLength"] = 0
                                works["hasDiscovery"] = -1
                                works["classifications"] = works.get("classifications", list())

                            # 全文分词。
                            # noinspection PyBroadException
                            try:
                                # segment_words_raw_info = nlp_res_data["全文分词"]["raw_data"]
                                # works["segmentWordsRawInfo"] = json.dumps(
                                #     segment_words_raw_info, separators=(",", ":"))
                                works["segmentWordsRawInfo"] = "[]"
                                works["personNames"] = list(nlp_res_data["全文分词"]["人名"])
                                works["regionNames"] = list(nlp_res_data["全文分词"]["地名"])
                                works["organizationNames"] = list(nlp_res_data["全文分词"]["组织"])
                                keywords = nlp_res_data["全文分词"]["关键词"]
                                works["keywords"] = [keyword["word"] for keyword in keywords]
                            except Exception:
                                works["segmentWordsRawInfo"] = "[]"
                                works["personNames"] = []
                                works["regionNames"] = []
                                works["organizationNames"] = []
                                works["keywords"] = []

                            # 文章标签。
                            # noinspection PyBroadException
                            try:
                                labels = nlp_res_data["文章标签"]
                                works["labels"] = [label["tag"] for label in labels]
                            except Exception:
                                works["labels"] = []

                            # 情感分析。
                            # noinspection PyBroadException
                            try:
                                sentiment_data = nlp_res_data["情感分析"][-1]["items"][0]
                                works["sentiment"] = sentiment_data["sentiment"]
                                works["sentimentPositiveProb"] = sentiment_data["positive_prob"]
                                # works["sentimentRawInfo"] = json.dumps(nlp_res_data["情感分析"], separators=(",", ":"))
                                works["sentimentRawInfo"] = "[]"
                            except Exception:
                                works["sentiment"] = -1
                                works["sentimentPositiveProb"] = -1
                                works["sentimentRawInfo"] = "[]"

                            # 文章摘要。
                            # noinspection PyBroadException
                            try:
                                works["digestCompute"] = nlp_res_data["文章摘要"][0]["summary"]
                            except Exception:
                                works["digestCompute"] = ""
                    else:
                        raise ValueError(f"接口请求失败，{resp.reason}，{self._api_url_flow_compute_baidu_api_nlp}")
                else:
                    raise ValueError(f"接口请求失败，{resp.status_code}，{self._api_url_flow_compute_baidu_api_nlp}")
            else:
                self._logger.debug(f"标题或正文为空，不做百度NLP分析，"
                                   f"{works.get('platformName')}，{works.get('platformType')}")
        except Exception as e:
            self._logger.warning(f"{e}\n{traceback.format_exc()}")
        finally:
            return works

    def flow_compute(self, works):
        """
        解析作品。
        :param works: 作品详情。
        :return:
        """

        try:
            # 获取作品的唯一ID。
            field_id = works.get("_id")
            if field_id:
                # 去ES里检查一下是否已经存在，如果不存在再做流计算。
                if not self._es_conn.exists(
                        index=self._index_dc_works, doc_type=self._doc_type_dc_works, id=field_id
                ):
                    # 执行流计算。
                    for method in (
                            self.flow_compute_baidu_api_nlp,
                            self.flow_compute_simhash
                    ):
                        try:
                            works = method(works)
                        except Exception as e:
                            self._logger.warning(f"{e}\n{traceback.format_exc()}")
                else:
                    # 如果已经存在，则只保留一些需要更新的字段。
                    update_fields = ["_id", "readNum", "likeNum", "commentNum", "forwardNum", "collectNum", "wxLookNum", "wangYiJoinNum"]
                    new_works = dict(_id=field_id)
                    for update_field in update_fields:
                        if update_field in works and works[update_field]:
                            new_works[update_field] = works[update_field]
                    works = new_works
            else:
                raise ValueError(f"works中缺少_id，{works.get('platformType')}，{works.get('platformName')}")
        finally:
            return works

    def send_to_kafka(self, producer, i_name, data):
        """
        发送至kafka中。
        :return:
        """

        # 保存至下一步Kakfa主题中。
        assert isinstance(i_name, str), f"参数错误，i_name：{i_name}"

        # 将复数单词改为单数单词。
        if i_name in self._plural_singular_map:
            i_name = self._plural_singular_map[i_name]
        elif i_name in self._singular_plural_map:
            pass
        else:
            self._logger.warning(f"不熟悉的结构名称：{i_name}")

        # 导入Kafka。
        msg = dict(code=1, msg="ok", data={i_name: data})
        msg = json.dumps(msg, separators=(",", ":")).encode("utf-8")
        resp = producer.send(topic=self._dst_topic, value=msg)
        if resp.failed():
            raise resp.exception
        else:
            self._logger.info(f"{self._dst_topic}，{i_name}，{len(msg) / 1024:.2f} KB")

    def listen(self):
        """
        开始监听并处理。
        :return:
        """

        # 连接Kafka。
        consumer = dc_kafka_consumer(topic=self._src_topic)
        producer = dc_kafka_producer()
        # 监听新数据。
        for msg in consumer:
            try:
                msg = json.loads(msg.value)
                data = msg["data"]
                for i_name, i_data in data.items():
                    try:
                        if i_data:
                            # 临时取消论坛数据参与流计算。
                            # if i_name in ("worksList", "forumDetails"):
                            if i_name in ("worksList", ):
                                # 处理作品列表。
                                if isinstance(i_data, (list, tuple)):
                                    for i in range(len(i_data)):
                                        try:
                                            if i_data[i]:
                                                works = self.flow_compute(i_data[i])
                                                self.send_to_kafka(producer, i_name, works)
                                        except Exception as e:
                                            self._logger.warning(f"{e}\n{traceback.format_exc()}")
                            # 临时取消论坛数据参与流计算。
                            # elif i_name in ("works", "forumDetail"):
                            elif i_name in ("works", ):
                                # 处理作品。
                                if isinstance(i_data, dict):
                                    works = self.flow_compute(i_data)
                                    self.send_to_kafka(producer, i_name, works)
                            else:
                                # 处理其它数据。
                                if isinstance(i_data, (list, tuple)):
                                    try:
                                        # 处理列表型数据。
                                        for i_data_child in i_data:
                                            self.send_to_kafka(producer, i_name, i_data_child)
                                    except Exception as e:
                                        self._logger.warning(f"{e}\n{traceback.format_exc()}")
                                elif isinstance(i_data, dict):
                                    # 处理字典型数据。
                                    self.send_to_kafka(producer, i_name, i_data)
                                else:
                                    self._logger.warning(f"未知数据体类型，{i_name}，{type(i_data)}")
                    except Exception as e:
                        self._logger.warning(f"{e}\n{traceback.format_exc()}")
            except Exception as e:
                self._logger.error(f"{e}\n{traceback.format_exc()}")


def listener_subprocess(seq, logger_prefix="a1"):
    """
    子进程。
    :return:
    """

    my_log_path = f"{log_path}/kafka_listener/{logger_prefix}"
    logger = LLog(f"{logger_prefix}_{seq}", log_path=my_log_path, logger_level="DEBUG").logger
    KafkaListenerA1FromOriginToFlowCompute(logger).listen()


def run(listener_num=1, logger_prefix="a1"):
    # 测试。
    listener_num = int(listener_num)
    assert listener_num > 0, f"参数错误，listener_num：{listener_num}"

    # 注册子进程。
    pool = multiprocessing.Pool(processes=listener_num)
    for i in range(listener_num):
        pool.apply_async(listener_subprocess, (i, logger_prefix))
    pool.close()
    pool.join()


if __name__ == "__main__":
    run()
