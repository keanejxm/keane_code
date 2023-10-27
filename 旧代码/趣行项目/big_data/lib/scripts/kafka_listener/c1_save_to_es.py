# -*- coding:utf-8 -*-
"""
Kafka监听器，存储至ES。
监听dc-forum主题，即论坛数据，该主题下的数据直接入库，便于前端快速查看。
# author: Trico
# date: 2021/1/26
# update: 2021/1/26
"""

import json
import time
import logging
import traceback
import elasticsearch
import multiprocessing

from lib_conf.config import es_config, kafka_topics, log_path
from common_utils.kafka.kafka_utils import dc_kafka_consumer
from common_utils.llog import LLog


class KafkaListenerC1FromOriginalToES(object):
    """
    监听Kafka，监听流计算结果，存储至ES中。
    监听dc-forum主题，即论坛数据，该主题下的数据直接入库，便于前端快速查看。
    """

    def __init__(self, logger):
        """
        初始化ES链接，ES默认字段值等。
        :param logger: 日志对象。
        """

        # 日志对象。
        assert isinstance(logger, logging.Logger), "Error param, logger."
        self._logger = logger

        # kafka主题。
        self._src_topic = kafka_topics["forum"]

        # ES连接。
        self._es_conn = elasticsearch.Elasticsearch(**es_config)

    def deal_with_forums(self, i_data):
        """
        处理论坛分类数据。
        :return:
        """

        # 索引名。
        index_name = "dc_forum"
        doc_type = "_doc"
        # 频道索引。
        # http://showdoc.hbrbdata.cn/showdoc/web/#/56?page_id=1847
        default_fields = {
            "status": 1,
            "sourceTypesName": "",
            "platformID": "",
            "platformName": "",
            "parentID": "",
            "parentName": "",
            "name": "",
            "forumId": "",
            "introduction": "",
            "logo": "",
            "url": "",
            "region": [],
            "type": 6,
            "levelNumber": 0,
            "followsNum": 0,
            "worksNum": 0,
            "createTime": None,
            "updateTime": None,
        }
        necessary_fields = []
        # _id。
        field_id = i_data.pop("_id")
        # 根据ES中是否存在区分不同逻辑。
        if not self._es_conn.exists(index=index_name, doc_type=doc_type, id=field_id):
            # 判断必要字段是否齐全。
            for necessary_field in necessary_fields:
                if necessary_field not in i_data:
                    raise ValueError(f"{index_name}，{field_id}，数据中缺少必要字段：{necessary_field}")
            # 新增。
            temp_fields = dict()
            for key, value in i_data.items():
                # None值不处理。
                if value is not None:
                    temp_fields[key] = value
            fields = dict(default_fields, **temp_fields)
            fields["createTime"] = fields["updateTime"] = int(time.time() * 1000)

            # 执行新增。
            return self._es_conn.index(index=index_name, doc_type=doc_type, body=fields, id=field_id)
        else:
            # 更新时间。
            update_fields = dict(doc=dict(updateTime=int(time.time() * 1000)))
            # 执行更新。
            return self._es_conn.update(index=index_name, doc_type=doc_type, body=update_fields, id=field_id)

    def deal_with_forum_details(self, i_data):
        """
        处理论坛详情数据。
        :return:
        """

        # 索引名。
        index_name = "dc_forum_details"
        doc_type = "_doc"
        # 论坛详情索引。
        # http://showdoc.hbrbdata.cn/showdoc/web/#/56?page_id=1889
        default_fields = {
            "status": 1,
            "sourceTypesName": None,
            "platformWorksID": None,
            "platformID": None,
            "platformName": None,
            "platformType": None,
            "parentID": "",
            "parentName": "",
            "accountID": "",
            "accountUrl": "",
            "accountName": "",
            "url": "",
            "authors": [],
            "title": "",
            "titleWordsNum": 0,
            "content": "",
            "contentWordsNum": 0,
            "question": "",
            "oneAnswer": "",
            "answer": "",
            "html": "",
            "simhash": "",
            "contentType": -1,
            "digest": "",
            "digestOriginal": "",
            "digestCompute": "",
            "source": "",
            "isOriginal": -1,
            "isOriginalCompute": -1,
            "isTop": -1,
            "isPush": -1,
            "classifications": [],
            "images": [],
            "topics": [],
            "covers": [],
            "videos": [],
            "audios": [],
            "readNum": 0,
            "likeNum": 0,
            "commentNum": 0,
            "forwardNum": 0,
            "collectNum": 0,
            "updateParams": "{}",
            "sentiment": -1,
            "sentimentPositiveProb": -1,
            "sentimentRawInfo": "[]",
            "labels": [],
            "tags": None,
            "tagsLength": 0,
            "personNames": [],
            "regionNames": [],
            "organizationNames": [],
            "keywords": [],
            "segmentWordsRawInfo": "[]",
            "wordFrequency": None,
            "wordFrequencyLength": 0,
            "hasDiscovery": -1,
            "hasSpread": -1,
            "hasSimilarWorks": -1,
            "hasSimilarOriginalWorks": -1,
            "reprintNum": 0,
            "reprintMediaNum": 0,
            "HI": 0,
            "spreadHI": 0,
            "interactiveHI": 0,
            "spreadHIIncreasement": 0,
            "pubTime": None,
            "createTime": None,
            "updateTime": None,
        }
        necessary_fields = ["platformWorksID", "platformID", "platformName", "platformType", "pubTime"]
        # _id。
        field_id = i_data.pop("_id")
        # 根据ES中是否存在区分不同逻辑。
        if not self._es_conn.exists(index=index_name, doc_type=doc_type, id=field_id):
            # 判断必要字段是否齐全。
            for necessary_field in necessary_fields:
                if necessary_field not in i_data:
                    raise ValueError(f"{index_name}，{field_id}，数据中缺少必要字段：{necessary_field}")
            # 新增。
            temp_fields = dict()
            for key, value in i_data.items():
                # None值不处理。
                if value is not None:
                    temp_fields[key] = value
            fields = dict(default_fields, **temp_fields)
            fields["createTime"] = fields["updateTime"] = int(time.time() * 1000)

            # 上传列表图（封面图）至BOS，只在新增数据的时候才做。

            # 计算热度。

            # 执行新增。
            return self._es_conn.index(index=index_name, doc_type=doc_type, body=fields, id=field_id)
        else:
            # 更新。
            fields = dict()
            # 部分数据是不可以更新的。
            for key, value in i_data.items():
                # None值不更新。
                if value is not None:
                    if key not in ("createTime", "createDateTime"):
                        # 过滤掉为0的更新数。
                        if key.endswith("Num"):
                            if value != 0:
                                fields[key] = value
                        else:
                            fields[key] = value
            # 更新时间。
            fields["updateTime"] = int(time.time() * 1000)

            # 计算热度。

            # 执行更新。
            update_fields = dict(doc=fields)
            # todo: 还需要优化，不是所有的字段都需要更新。
            return self._es_conn.update(index=index_name, doc_type=doc_type, body=update_fields, id=field_id)

    def deal_with_msg(self, i_name, i_data):
        """
        处理数据。
        :param i_name: 结构名。
        :param i_data: 结构数据体。
        :return:
        """

        if i_name == "forum":
            # 频道。
            resp = self.deal_with_forums(i_data)
            self._logger.debug(f"{resp}")
        elif i_name == "forumDetail":
            # 频道。
            resp = self.deal_with_forum_details(i_data)
            self._logger.debug(f"{resp}")
        else:
            raise ValueError(f"未知数据体，{i_name}")

    def listen(self):
        """
        开始监听并处理。
        :return:
        """

        # 连接Kafka。
        consumer = dc_kafka_consumer(topic=self._src_topic)
        # 监听新数据。
        for msg in consumer:
            try:
                msg = json.loads(msg.value)
                data = msg["data"]
                for i_name, i_data in data.items():
                    try:
                        self.deal_with_msg(i_name, i_data)
                    except Exception as e:
                        self._logger.error(
                            f"平台类型：{i_data.get('platformType', i_data.get('type', '未知'))}，"
                            f"平台名称：{i_data.get('platformName', i_data.get('name', '未知'))}，"
                            f"{e}\n{traceback.format_exc()}")
            except Exception as e:
                self._logger.error(f"{e}\n{traceback.format_exc()}")


def listener_subprocess(seq, logger_prefix="c1"):
    """
    子进程。
    :return:
    """

    my_log_path = f"{log_path}/kafka_listener/{logger_prefix}"
    logger = LLog(f"{logger_prefix}_{seq}", log_path=my_log_path, logger_level="DEBUG").logger
    KafkaListenerC1FromOriginalToES(logger).listen()


def run(listener_num=1, logger_prefix="c1"):
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
