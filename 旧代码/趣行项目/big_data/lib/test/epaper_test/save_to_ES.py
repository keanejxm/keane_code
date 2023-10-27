# -*- coding:utf-8 -*-
"""
# project:
# author: Neil
# date: 2020/12/21
# update: 2020/12/21
"""

import logging
import time
import traceback

import elasticsearch

from lib.common_utils.llog import LLog


class LayoutsCrawlerESUtils(object):

    def __init__(self, logger):

        # 日志对象。
        assert isinstance(logger, logging.Logger), "Error param, logger."
        self._logger = logger
        # 链接ES。
        self._es_conn = elasticsearch.Elasticsearch([{"host": "180.76.161.67", "port": 9200}])

        # 版面索引。
        self._discover_layouts_index = "dc_epaper_layouts"
        self.default_layouts_fields = {
            "status": 1,
            "platformID": "",
            "platformName": "",
            "url": "",
            "layoutTitle": "",
            "layoutSeq": 0,
            "layoutNum": 0,
            "layoutMapAreas": [],
            "layoutMapAreasLength": 0,
            "mapImage": "",
            "mapImageLocal": "",
            "largeImage": "",
            "largeImageLocal": "",
            "pdf": "",
            "pdfLocal": "",
            "pubTime": 0,
            "createTime": 0,
            "updateTime": 0,
        }

        # 频道索引
        self._discover_channels_index = "dc_channels"
        self.default_channels_fields = {
            "status": 1,
            "platformID": "",
            "platformName": "",
            "platformType": 3,
            "name": "",
            "url": "",
            "region": [],
            "types": [],
            "selfTypesIDs": [],
            "createTime": 0,
            "updateTime": 0,
        }

        # 作品索引。
        self._discover_works_index = "dc_works"
        self.default_works_fields = {
            "status": 1,
            "platformWorksID": "",
            "platformID": "",
            "platformName": "",
            "platformType": 0,
            "channelID": "",
            "channelName": "",
            "accountID": "",
            "accountName": "",
            "topicID": "",
            "epaperLayoutID": "",
            "url": "",
            "authors": [],
            "editors": list(),
            "hbrbAuthors": list(),
            "preTitle": "",
            "subTitle": "",
            "title": "",
            "labels": [],
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
            "isOriginal": 1,
            "isOriginalCompute": -1,
            "isTop": -1,
            "isPush": -1,
            "classifications": list(),
            "images": list(),
            "covers": list(),
            "topics": list(),
            "videos": list(),
            "audios": list(),
            "readNum": 0,
            "commentNum": 0,
            "likeNum": 0,
            "collectNum": 0,
            "forwardNum": 0,
            "wxLookNum": 0,
            "wangYiJoinNum": 0,
            "updateParams": "{}",
            "sentiment": -1,
            "sentimentRawInfo": "",
            "sentimentPositiveProb": -1,
            "tags": [],
            "tagsLength": 0,
            "personNames": list(),
            "regionNames": list(),
            "organizationNames": list(),
            "keywords": list(),
            "segmentWordsRawInfo": "",
            "wordFrequency": [],
            "wordFrequencyLength": 0,
            "hasDiscovery": -1,
            "hasSpread": -1,
            "hasSimilarWorks": -1,
            "hasSimilarOriginalWorks": -1,
            "reprintNum": 0,
            "reprintMediaNum": 0,
            "spreadHI": 0,
            "interactiveHI": 0,
            "pubTime": 0,
            "createTime": 0,
            "updateTime": 0,
        }

        # 平台索引
        self._discover_platforms_index = "dc_platforms"
        self.default_platforms_fields = {
            "status": 1,
            "name": "",
            "introduction": "",
            "logo": "",
            "weMediaName": "",
            "url": 0,
            "type": 0,
            "types": [],
            "selfTypesIDs": 0,
            "region": "",
            "extendData": "",
            "worksNum": "",
            "createTime": 0,
            "updateTime": 0,
            "latestWorksTime": "",
        }

    def es_save_layout_and_works(self, data):
        """
        保存采集结果。
        :return:
        """

        if "epaperLayout" in data and data["epaperLayout"]:
            try:
                self.es_save_layout(data["epaperLayout"])
            except Exception as e:
                self._logger.warning(f"{e}\n{traceback.format_exc()}")
        if "worksList" in data and data["worksList"]:
            try:
                self.es_save_works(data["worksList"])
            except Exception as e:
                self._logger.warning(f"{e}\n{traceback.format_exc()}")

    def es_save_channel_and_works(self, data):
        """
        保存采集结果。
        :return:
        """

        if "channel" in data and data["channel"]:
            try:
                self.es_save_channel(data["channel"])
            except Exception as e:
                self._logger.warning(f"{e}\n{traceback.format_exc()}")
        if "article" in data and data["article"]:
            try:
                self.es_save_works(data["article"])
            except Exception as e:
                self._logger.warning(f"{e}\n{traceback.format_exc()}")

    def _es_create_new_works(self, index_name, field_id, fields):
        """
        新增作品。
        :return:
        """
        # 过滤掉None值字段。
        temp_fields = dict()
        for key, value in fields.items():
            # None值不更新。
            if value is not None:
                temp_fields[key] = value
        fields = dict(self.default_works_fields, **temp_fields)
        now = int(time.time() * 1000)
        fields["createTime"] = fields["updateTime"] = int(now)

        # 新增。
        return self._es_conn.index(index=index_name, doc_type="_doc", body=fields, id=field_id)

    def _es_create_new_layout(self, index_name, field_id, fields):
        """
        新增账号信息。
        :return:
        """

        # 过滤掉None值字段。
        temp_fields = dict()
        for key, value in fields.items():
            # None值不更新。
            if value is not None:
                temp_fields[key] = value
        fields = dict(self.default_layouts_fields, **temp_fields)
        now = int(time.time() * 1000)
        fields["createTime"] = fields["updateTime"] = int(now)
        return self._es_conn.index(index=index_name, doc_type="_doc", body=fields, id=field_id)

    def _es_create_new_channle(self, index_name, field_id, fields):
        """
        新增账号信息。
        :return:
        """

        # 过滤掉None值字段。
        temp_fields = dict()
        for key, value in fields.items():
            # None值不更新。
            if value is not None:
                temp_fields[key] = value
        fields = dict(self.default_channels_fields, **temp_fields)
        now = int(time.time() * 1000)
        fields["createTime"] = fields["updateTime"] = int(now)
        return self._es_conn.index(index=index_name, doc_type="_doc", body=fields, id=field_id)

    def es_save_layout(self, layouts):
        """
        将版面信息存入ES。
        :param layouts: 账号信息。
        :return:
        """

        # 参数验证。
        assert layouts and isinstance(layouts, (dict, list)), "Error param, layouts."

        # 统计数据。
        create_num = update_num = 0
        # 索引名。
        index_name = self._discover_layouts_index

        # 分为列表处理方式和字典处理方式。
        if isinstance(layouts, list):
            for fields in layouts:
                try:
                    if fields:
                        field_id = fields.pop("_id")
                        if self._es_conn.exists(index=index_name, doc_type="_doc", id=field_id):
                            self._logger.info("已存在")
                            continue
                        else:
                            # 执行新增。
                            res = self._es_create_new_layout(index_name, field_id, fields)
                            create_num += 1
                        self._logger.info(f'{index_name} {field_id}, {res["result"]}')
                except Exception as e:
                    self._logger.warning(f"{e}\n{traceback.format_exc()}")
        elif isinstance(layouts, dict):
            fields = layouts
            if fields:
                field_id = fields.pop("_id")
                if self._es_conn.exists(index=index_name, doc_type="_doc", id=field_id):
                    # 执行更新。
                    res = self._es_create_new_layout(index_name, field_id, fields)
                else:
                    # 执行新增。
                    res = self._es_create_new_layout(index_name, field_id, fields)
                    create_num += 1
                print(f'{index_name} {field_id}, {res["result"]}')
        else:
            pass

        # 记录数据。
        self._logger.info(f"{index_name} total: {create_num + update_num}, create: {create_num}, update: {update_num}.")

    def es_save_channel(self, channels):
        """
        将频道信息存入ES。
        :param channels: 账号信息。
        :return:
        """

        # 参数验证。
        assert channels and isinstance(channels, (dict, list)), "Error param, layouts."

        # 统计数据。
        create_num = update_num = 0
        # 索引名。
        index_name = self._discover_channels_index

        # 分为列表处理方式和字典处理方式。
        if isinstance(channels, list):
            for fields in channels:
                try:
                    if fields:
                        field_id = fields.pop("_id")
                        if self._es_conn.exists(index=index_name, doc_type="_doc", id=field_id):
                            self._logger.info("已存在")
                            continue
                        else:
                            # 执行新增。
                            res = self._es_create_new_layout(index_name, field_id, fields)
                            create_num += 1
                        self._logger.info(f'{index_name} {field_id}, {res["result"]}')
                except Exception as e:
                    self._logger.warning(f"{e}\n{traceback.format_exc()}")

        elif isinstance(channels, dict):
            fields = channels
            if fields:
                field_id = fields.pop("_id")
                if self._es_conn.exists(index=index_name, doc_type="_doc", id=field_id):
                    # 执行更新。
                    res = self._es_create_new_channle(index_name, field_id, fields)
                else:
                    # 执行新增。
                    res = self._es_create_new_channle(index_name, field_id, fields)
                    create_num += 1
                self._logger.info(f'{index_name} {field_id}, {res["result"]}')
        else:
            pass

        # 记录数据。
        self._logger.info(f"{index_name} total: {create_num + update_num}, create: {create_num}, update: {update_num}.")

    def es_save_works(self, works):
        """
        将作品信息存入ES。
        :param works: 作品信息。
        :return:
        """

        # 参数验证。
        assert works and isinstance(works, (dict, list)), "Error param, works."

        # 统计数据。
        create_num = update_num = 0
        # 索引名。
        index_name = self._discover_works_index

        # 分为列表处理方式和字典处理方式。
        if isinstance(works, list):
            for fields in works:
                try:
                    if fields:
                        field_id = fields.pop("_id")
                        if self._es_conn.exists(index=index_name, doc_type="_doc", id=field_id):
                            # 新增作品。
                            res = self._es_create_new_works(index_name, field_id, fields)
                            create_num += 1
                        else:
                            # 新增作品。
                            res = self._es_create_new_works(index_name, field_id, fields)
                            create_num += 1
                        print(f'{index_name} {field_id}, {res["result"]}')
                except Exception as e:
                    self._logger.warning(f'{e}\n{traceback.format_exc()}')
        elif isinstance(works, dict):
            fields = works
            if fields:
                field_id = fields.pop("_id")
                if self._es_conn.exists(index=index_name, doc_type="_doc", id=field_id):
                    # 新增作品。
                    res = self._es_create_new_works(index_name, field_id, fields)
                    create_num += 1
                else:
                    # 新增作品。
                    res = self._es_create_new_works(index_name, field_id, fields)
                    create_num += 1
                self._logger.info(f'{index_name} {field_id}, {res["result"]}')

        # 记录数据。
        self._logger.info(
            f"{index_name} total: {create_num + update_num}, create: {create_num}, update: {update_num}.")

    def _es_update_platform(self, index_name, field_id, fields):
        """
        更新作品信息。
        :return:
        """

        # 新数据体。
        new_fields = dict()
        for key, value in fields.items():
            # None值不更新。
            if value is not None:
                if key not in ("createTime", "createDateTime"):
                    # 过滤掉为0的更新数。
                    if key.endswith("Num") or key.endswith("Count"):
                        if value != 0:
                            new_fields[key] = value
                    else:
                        new_fields[key] = value

        # 更新时间。
        now = int(time.time() * 1000)
        new_fields["updateTime"] = int(now)
        new_fields["createTime"] = int(now)

        # 更新。
        new_fields = dict(doc=new_fields)
        return self._es_conn.update(index=index_name, doc_type="_doc", body=new_fields, id=field_id)

    def save_to_platform(self, works):
        """
        将头版信息存入ES。
        :param works: 作品信息。
        :return:
        """

        # 参数验证。
        assert works and isinstance(works, (dict, list)), "Error param, works."

        # 统计数据。
        create_num = update_num = 0
        # 索引名。
        index_name = self._discover_platforms_index

        # 分为列表处理方式和字典处理方式。
        if isinstance(works, list):
            for fields in works:
                try:
                    if fields:
                        field_id = fields.pop("_id")
                        if self._es_conn.exists(index=index_name, doc_type="_doc", id=field_id):
                            # 新增作品。
                            res = self._es_create_new_works(index_name, field_id, fields)
                            create_num += 1
                        else:
                            # 新增作品。
                            res = self._es_create_new_works(index_name, field_id, fields)
                            create_num += 1
                        self._logger.info(f'{index_name} {field_id}, {res["result"]}')
                except Exception as e:
                    self._logger.warning(f'{e}\n{traceback.format_exc()}')
        elif isinstance(works, dict):
            fields = works
            if fields:
                field_id = fields.pop("_id")
                if self._es_conn.exists(index=index_name, doc_type="_doc", id=field_id):
                    # 更新作品。
                    res = self._es_update_platform(index_name, field_id, fields)
                    update_num += 1
                else:
                    # 新增作品。
                    res = self._es_create_new_works(index_name, field_id, fields)
                    create_num += 1
                self._logger.info(f'{index_name} {field_id}, {res["result"]}')

        # 记录数据。
        self._logger.info(
            f"{index_name} total: {create_num + update_num}, create: {create_num}, update: {update_num}.")


if __name__ == '__main__':
    log = LLog("Test", only_console=True, logger_level="DEBUG").logger
    res = {
        "data": {'code': 1, 'msg': '成功', 'channel': {'_id': '598c66fe1ae79fcd83866a99e4ada551', 'platformID': '3_4_5_2',
                                                     'platformName': '参考消息-中国频道',
                                                     'url': 'http://china.cankaoxiaoxi.com/', 'name': '中国'},
                 'article': [
                     {'url': 'http://www.cankaoxiaoxi.com/china/20201218/2427432.shtml', 'title': '中欧经贸往来疫情中逆势而上',
                      'pubSource': '', 'pubTime': 1608256670, 'channel': '中国频道', 'authors': [], 'summary': ''},
                     {'url': 'http://www.cankaoxiaoxi.com/china/20201216/2427290.shtml', 'title': '英媒:中美航天科研势头正在逆转',
                      'pubSource': '', 'pubTime': 1608110487, 'channel': '中国频道', 'authors': [], 'summary': ''}]}
    }
    LayoutsCrawlerESUtils(log).es_save_channel(res["data"]["channel"])
