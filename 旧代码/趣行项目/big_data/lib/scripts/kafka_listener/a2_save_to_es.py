# -*- coding:utf-8 -*-
"""
监听器，存储至ES。
# author: Trico
# date: 2021/1/15
# update: 2021/1/15
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
from common_utils.upload_bos import bos_upload_image_by_url_and_compute_hash


class KafkaListenerA2FromFlowComputedToES(object):
    """
    监听Kafka，监听流计算结果，存储至ES中。
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
        self._src_topic = kafka_topics["flowComputed"]

        # ES连接。
        self._es_conn = elasticsearch.Elasticsearch(**es_config)

    def deal_with_platforms(self, i_data):
        """
        处理平台数据，一般只做部分字段更新。
        :return:
        """

        # 索引名。
        index_name = "dc_platforms"
        doc_type = "_doc"
        # 平台索引可更新的字段。
        # update_fields = []
        # _id。
        field_id = i_data.pop("_id")
        # 根据ES中是否存在区分不同逻辑。
        if not self._es_conn.exists(index=index_name, doc_type=doc_type, id=field_id):
            # 平台必须存在。
            raise ValueError(f"不存在的平台ID（理应是存在的），{field_id}")
        else:
            # 更新。
            fields = dict()
            # 更新时间。
            fields["updateTime"] = int(time.time() * 1000)

            try:
                # 单独处理扩展字段，防止采集旧数据时，覆盖掉这个字段。
                if "extendData" in i_data:
                    # 先设置默认值。
                    fields["extendData"] = i_data["extendData"]
                    # 从ES中获取当前数据。
                    res = self._es_conn.get(
                        index=index_name, doc_type=doc_type, id=field_id, _source=["extendData", "type"]
                    )
                    # 旧数据体。
                    platform_type = res["_source"].get("type")
                    if platform_type == 5:
                        old_extend_data_str = res["_source"].get("extendData")
                        old_extend_data = json.loads(old_extend_data_str)
                        # 新数据体。
                        new_extend_data_str = i_data["extendData"]
                        new_extend_data = json.loads(new_extend_data_str)
                        # 比较新旧数据的时间，保留新的。
                        if new_extend_data and old_extend_data:
                            new_latest_paper_time = int(new_extend_data.get("latestPaperTime"))
                            old_latest_paper_time = int(old_extend_data.get("latestPaperTime"))
                            if old_latest_paper_time >= new_latest_paper_time:
                                fields.pop("extendData")
            except Exception as e:
                self._logger.debug(f"{e}\n{traceback.format_exc()}")

            update_fields = dict(doc=fields)
            # 执行更新。
            return self._es_conn.update(index=index_name, doc_type=doc_type, body=update_fields, id=field_id)

    def deal_with_accounts(self, i_data):
        """
        处理账号数据，一般只做部分字段更新。
        :return:
        """

        # 索引名。
        index_name = "dc_accounts"
        doc_type = "_doc"
        # 账号索引可更新的字段。
        update_fields = [
            "name", "introduction", "avatar", "qrcode", "gender", "mobilePhoneNumber", "email", "identityCode",
            "certificationTye", "url", "platformFansNum", "platformFollowsNum", "platformReadsNum", "platformLikesNum",
            "platformCommentsNum", "platformForwardsNum", "extendData",
        ]
        # _id。
        field_id = i_data.pop("_id")
        # 根据ES中是否存在区分不同逻辑。
        if not self._es_conn.exists(index=index_name, doc_type=doc_type, id=field_id):
            # 账号必须存在。
            raise ValueError(f"不存在的账号ID（理应是存在的），{field_id}")
        else:
            # 更新。
            fields = dict()
            for field in update_fields:
                if field in i_data:
                    fields[field] = i_data[field]
            # 更新时间。
            fields["updateTime"] = int(time.time() * 1000)
            update_fields = dict(doc=fields)
            # 执行更新。
            return self._es_conn.update(index=index_name, doc_type=doc_type, body=update_fields, id=field_id)

    def deal_with_epaper_layouts(self, i_data):
        """
        处理报纸版面数据。
        :return:
        """

        # 索引名。
        index_name = "dc_epaper_layouts"
        doc_type = "_doc"
        # 报纸版面索引。
        # http://showdoc.hbrbdata.cn/showdoc/web/#/56?page_id=1848
        default_fields = {
            "status": 1,
            "platformID": None,
            "platformName": None,
            "url": "",
            "layoutTitle": "",
            "layoutSeq": -1,
            "layoutNum": -1,
            "layoutMapAreas": None,
            "layoutMapAreasLength": 0,
            "mapImage": "",
            "mapImageLocal": "",
            "largeImage": "",
            "largeImageLocal": "",
            "pdf": "",
            "pdfLocal": "",
            "pubTime": None,
            "createTime": None,
            "updateTime": None,
        }
        necessary_fields = ["platformID", "platformName", "pubTime"]
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

    def deal_with_topics(self, i_data):
        """
        处理专题数据，采集而来。
        :return:
        """

        # 索引名。
        index_name = "dc_topics"
        doc_type = "_doc"
        # 频道索引。
        # http://showdoc.hbrbdata.cn/showdoc/web/#/56?page_id=1868
        default_fields = {
            "status": 1,
            "topicID": None,
            "platformID": None,
            "platformName": None,
            "platformType": None,
            "url": "",
            "title": "",
            "digest": "",
            "topicCovers": "",
            "platformReadsNum": 0,
            "platformLikesNum": 0,
            "platformCommentsNum": 0,
            "platformForwardsNum": 0,
            "worksNum": 0,
            "pubTime": None,
            "createTime": None,
            "updateTime": None,
        }
        necessary_fields = ["topicID", "platformID", "platformName", "platformType", "pubTime"]
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

    def deal_with_channels(self, i_data):
        """
        处理频道数据。
        :return:
        """

        # 索引名。
        index_name = "dc_channels"
        doc_type = "_doc"
        # 频道索引。
        # http://showdoc.hbrbdata.cn/showdoc/web/#/56?page_id=1847
        default_fields = {
            "status": 1,
            "platformID": None,
            "platformName": None,
            "platformType": None,
            "name": "",
            "url": "",
            "region": [],
            "types": [],
            "selfTypesIDs": [],
            "createTime": None,
            "updateTime": None,
        }
        necessary_fields = ["platformID", "platformName", "platformType", "name"]
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

    def deal_with_works(self, i_data):
        """
        处理作品数据。
        :return:
        """

        # 索引名。
        index_name = "dc_works"
        doc_type = "_doc"
        # 作品索引。
        # http://showdoc.hbrbdata.cn/showdoc/web/#/56?page_id=1843
        default_fields = {
            "status": 1,
            "platformWorksID": None,
            "platformID": None,
            "platformName": None,
            "platformType": None,
            "channelID": "",
            "channelName": "",
            "accountID": "",
            "accountName": "",
            "topicID": "",
            "topicTitle": "",
            "epaperLayoutID": "",
            "url": "",
            "authors": [],
            "editors": [],
            "hbrbAuthors": [],
            "preTitle": "",
            "subTitle": "",
            "title": "",
            "titleWordsNum": 0,
            "content": "",
            "contentWordsNum": 0,
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
            "wxLookNum": 0,
            "wangYiJoinNum": 0,
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
            # 封面图。
            covers = fields.get("covers")
            if covers:
                new_covers = list()
                for cover in covers:
                    # noinspection PyBroadException
                    try:
                        # 上传bos，并获取图片哈希值。
                        pic_url, _ = bos_upload_image_by_url_and_compute_hash(cover)
                        # 更新封面图链接。
                        new_covers.append(pic_url)
                    except Exception:
                        continue
                if new_covers:
                    fields["covers"] = new_covers

            # 内容图。
            image_hash_list = list()
            images = fields.get("images")
            if images:
                new_images = list()
                for image in images:
                    # noinspection PyBroadException
                    try:
                        # 上传bos，并获取图片哈希值。
                        pic_url, pic_hash = bos_upload_image_by_url_and_compute_hash(image)
                        # 保存图片哈希值。
                        image_hash_list.append(dict(url=pic_url, hash=pic_hash))
                        # 更新内容图链接。
                        new_images.append(pic_url)
                        # 将正文中的图片链接替换为新链接。
                        fields["content"].replace(image, pic_url)
                    except Exception:
                        continue
                if new_images:
                    fields["images"] = new_images
            # 更新图片哈希值字段。
            fields["imageHash"] = image_hash_list
            fields["imageHashLength"] = len(fields["imageHash"])

            # 计算热度。

            # 执行新增。
            return self._es_conn.index(index=index_name, doc_type=doc_type, body=fields, id=field_id)
        else:
            # 更新。
            fields = dict()
            # 部分数据是不可以更新的。
            for key, value in i_data.items():
                # None值不更新。
                if value and value not in (-1, "{}", "[]"):
                    if key not in ("createTime", "createDateTime"):
                        # 过滤掉为0的更新数。
                        if key.endswith("Num"):
                            if value != 0:
                                fields[key] = value
                        elif key == "isPush":
                            if value == 1:
                                fields[key] = value
                        else:
                            # 其它字段都更新。
                            fields[key] = value
            # 更新时间。
            fields["updateTime"] = int(time.time() * 1000)

            # 计算热度。

            # 执行更新。
            update_fields = dict(doc=fields)
            # todo: 还需要优化，不是所有的字段都需要更新。
            return self._es_conn.update(index=index_name, doc_type=doc_type, body=update_fields, id=field_id)

    def deal_with_top_queries(self, i_data):
        """
        处理热搜数据。
        :return:
        """

        # 索引名。
        index_name = "dc_top_queries"
        doc_type = "_doc"
        # 报纸版面索引。
        # http://showdoc.hbrbdata.cn/showdoc/web/#/56?page_id=1854
        default_fields = {
            "status": 1,
            "queryPlatform": None,
            "topQueries": '[]',
            "createTime": None,
            "updateTime": None,
        }
        necessary_fields = ["queryPlatform"]
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

    def deal_with_msg(self, i_name, i_data):
        """
        处理数据。
        :param i_name: 结构名。
        :param i_data: 结构数据体。
        :return:
        """

        if i_name == "works":
            # 作品。
            resp = self.deal_with_works(i_data)
            self._logger.debug(f"{resp}")
        elif i_name == "epaperLayout":
            # 报纸版面。
            resp = self.deal_with_epaper_layouts(i_data)
            self._logger.debug(f"{resp}")
        elif i_name == "platform":
            # 平台，一般只做部分字段更新。
            resp = self.deal_with_platforms(i_data)
            self._logger.debug(f"{resp}")
        elif i_name == "account":
            # 账号，一般只做部分字段更新。
            resp = self.deal_with_accounts(i_data)
            self._logger.debug(f"{resp}")
        elif i_name == "channel":
            # 频道。
            resp = self.deal_with_channels(i_data)
            self._logger.debug(f"{resp}")
        elif i_name == "topQuery":
            # 频道。
            resp = self.deal_with_top_queries(i_data)
            self._logger.debug(f"{resp}")
        elif i_name == "topic":
            # 频道。
            resp = self.deal_with_topics(i_data)
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


def listener_subprocess(seq, logger_prefix="a2"):
    """
    子进程。
    :return:
    """

    my_log_path = f"{log_path}/kafka_listener/{logger_prefix}"
    logger = LLog(f"{logger_prefix}_{seq}", log_path=my_log_path, logger_level="DEBUG").logger
    KafkaListenerA2FromFlowComputedToES(logger).listen()


def run(listener_num=1, logger_prefix="a2"):
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
