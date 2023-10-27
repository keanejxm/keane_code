# -*- coding:utf-8 -*-
"""
ES工具。
# author: Trico
# date: 2021/1/4
# update: 2021/1/4
"""

import time
import logging
import traceback
import elasticsearch

from api.config import es_config


class ESUtils(object):

    def __init__(self, logger):
        # 日志对象。
        assert isinstance(logger, logging.Logger), "Error param, logger."
        self._logger = logger
        # 链接ES。
        self._es_conn = elasticsearch.Elasticsearch(**es_config)

        # 作品索引。
        self._dc_discover_works_index = "dc_works"
        self.default_works_fields = {
            "status": 1,
            "platformID": "",
            "platformName": "",
            "platformType": -1,
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
            "updateParams": "",
            "sentiment": -1,
            "sentimentPositiveProb": -1,
            "sentimentRawInfo": "",
            "tags": [],
            "tagsLength": 0,
            "personNames": [],
            "regionNames": [],
            "organizationNames": [],
            "keywords": [],
            "segmentWordsRawInfo": [],
            "wordFrequency": [],
            "wordFrequencyLength": 0,
            "hasDiscovery": -1,
            "hasSpread": -1,
            "hasSimilarWorks": -1,
            "hasSimilarOriginalWorks": -1,
            "reprintNum": 0,
            "reprintMediaNum": 0,
            "spreadHI": 0.0,
            "interactiveHI": 0.0,
            "pubTime": 0,
            "createTime": 0,
            "updateTime": 0,
        }

    def _es_update_account(self, index_name, field_id, fields):
        """
        更新账号信息。
        :return:
        """

        new_fields = dict()
        for key, value in fields.items():
            # None值不更新。
            if value is not None:
                # 过滤掉不需要更新的字段。
                if key not in (
                        "workNum", "readNum", "playNum", "likeNum",
                        "commentNum", "forwardNum", "wxLookNum", "wangYiJoinNum",
                        "createTime", "createDateTime"):
                    # 过滤掉为0的更新数。
                    if key.endswith("Num") or key.endswith("Count"):
                        if value != 0:
                            new_fields[key] = value
                    else:
                        new_fields[key] = value
        # 更新时间。
        now = int(time.time() * 1000)
        new_fields["updateTime"] = int(now / 1000)
        new_fields["updateDateTime"] = now
        new_fields = dict(doc=new_fields)
        # 执行更新。
        return self._es_conn.update(index=index_name, doc_type="_doc", body=new_fields, id=field_id)

    def _es_create_new_account(self, index_name, field_id, fields):
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
        fields = dict(self.default_accounts_fields, **temp_fields)
        now = int(time.time() * 1000)
        fields["createTime"] = fields["updateTime"] = int(now / 1000)
        fields["createDateTime"] = fields["updateDateTime"] = now
        return self._es_conn.index(index=index_name, doc_type="_doc", body=fields, id=field_id)

    def _es_update_works(self, index_name, field_id, fields):
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
        new_fields["updateTime"] = int(now / 1000)
        new_fields["updateDateTime"] = now

        # 不再更新列表图链接，因为第一次采集时已经上传BOS且做了链接替换。
        # 更新时不再清除covers字段。
        # if "covers" in new_fields:
        #     new_fields.pop("covers")

        # 上传列表图（封面图）至BOS，只在新增数据的时候才做。
        try:
            if "covers" in fields and fields["covers"]:
                new_fields["covers"] = self.upload_links_to_bos(fields["covers"])
        except Exception as e:
            self._logger.warning(f"{e}\n{traceback.format_exc()}")

        # 计算热度。
        try:
            new_fields["HI"] = self.compute_hi_for_update(field_id, new_fields)
        except Exception as e:
            self._logger.warning(f"{e}\n{traceback.format_exc()}")
            new_fields["HI"] = 0.0

        # 更新。
        new_fields = dict(doc=new_fields)
        return self._es_conn.update(index=index_name, doc_type="_doc", body=new_fields, id=field_id)

    def _es_create_new_works(self, index_name, field_id, fields, hi_account):
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
        fields["createTime"] = fields["updateTime"] = int(now / 1000)
        fields["createDateTime"] = fields["updateDateTime"] = now

        # 上传列表图（封面图）至BOS，只在新增数据的时候才做。
        try:
            if "covers" in fields and fields["covers"]:
                fields["covers"] = self.upload_links_to_bos(fields["covers"])
        except Exception as e:
            self._logger.warning(f"{e}\n{traceback.format_exc()}")

        # 计算热度。
        try:
            if hi_account and fields["accountType"] in (1, 2):
                fields["HI"] = self.compute_hi(fields["mediaType"], dict(hi_account, **fields))
        except Exception as e:
            self._logger.warning(f"{e}\n{traceback.format_exc()}")
            fields["HI"] = 0.0

        # 新增。
        return self._es_conn.index(index=index_name, doc_type="_doc", body=fields, id=field_id)

    def es_save_accounts_and_works(self, data):
        """
        保存采集结果。
        :return:
        """

        if "account" in data and data["account"]:
            try:
                self.es_save_accounts(data["account"])
            except Exception as e:
                self._logger.warning(f"{e}\n{traceback.format_exc()}")
        if "works" in data and data["works"]:
            try:
                if "account" in data and data["account"] and isinstance(data["account"], dict):
                    # 计算热度。
                    self.es_save_works(data["works"], account=data["account"])
                else:
                    self.es_save_works(data["works"])
            except Exception as e:
                self._logger.warning(f"{e}\n{traceback.format_exc()}")

    def es_save_accounts(self, accounts):
        """
        将账号信息存入ES。
        :param accounts: 账号信息。
        :return:
        """

        # 参数验证。
        assert accounts and isinstance(accounts, (dict, list)), "Error param, accounts."

        # 统计数据。
        create_num = update_num = 0
        # 索引名。
        index_name = self._yym_discover_accounts_index

        # 分为列表处理方式和字典处理方式。
        if isinstance(accounts, list):
            for fields in accounts:
                try:
                    if fields:
                        field_id = fields.pop("_id")
                        if self._es_conn.exists(index=index_name, doc_type="_doc", id=field_id):
                            # 执行更新。
                            res = self._es_update_account(index_name, field_id, fields)
                            update_num += 1
                        else:
                            # 执行新增。
                            res = self._es_create_new_account(index_name, field_id, fields)
                            create_num += 1
                        self._logger.info(f'{index_name} {field_id}, {res["result"]}')
                except Exception as e:
                    self._logger.warning(f"{e}\n{traceback.format_exc()}")
        elif isinstance(accounts, dict):
            fields = accounts
            if fields:
                field_id = fields.pop("_id")
                if self._es_conn.exists(index=index_name, doc_type="_doc", id=field_id):
                    # 执行更新。
                    res = self._es_update_account(index_name, field_id, fields)
                    update_num += 1
                else:
                    # 执行新增。
                    res = self._es_create_new_account(index_name, field_id, fields)
                    create_num += 1
                self._logger.info(f'{index_name} {field_id}, {res["result"]}')
        else:
            pass

        # 记录数据。
        self._logger.info(f"{index_name} total: {create_num + update_num}, create: {create_num}, update: {update_num}.")

    def es_save_works(self, works, account=None):
        """
        将作品信息存入ES。
        :param works: 作品信息。
        :param account: 账号信息。
        :return:
        """

        # 参数验证。
        assert works and isinstance(works, (dict, list)), "Error param, works."

        # 整理账号信息，用于计算热度。
        hi_account = dict()
        if account and isinstance(account, dict):
            account = dict(self.default_accounts_fields, **account)
            hi_account["fanNum"] = account["fanNum"]
            hi_account["workNum"] = account["workNum"]

        # 统计数据。
        create_num = update_num = 0
        # 索引名。
        index_name = self._yym_discover_works_index

        # 分为列表处理方式和字典处理方式。
        if isinstance(works, list):
            for fields in works:
                try:
                    if fields:
                        field_id = fields.pop("_id")
                        if self._es_conn.exists(index=index_name, doc_type="_doc", id=field_id):
                            # 更新作品。
                            res = self._es_update_works(index_name, field_id, fields)
                            update_num += 1
                        else:
                            # 新增作品。
                            res = self._es_create_new_works(index_name, field_id, fields, hi_account)
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
                    res = self._es_update_works(index_name, field_id, fields)
                    update_num += 1
                else:
                    # 新增作品。
                    res = self._es_create_new_works(index_name, field_id, fields, hi_account)
                    create_num += 1
                self._logger.info(f'{index_name} {field_id}, {res["result"]}')

        # 记录数据。
        self._logger.info(
            f"{index_name} total: {create_num + update_num}, create: {create_num}, update: {update_num}.")
