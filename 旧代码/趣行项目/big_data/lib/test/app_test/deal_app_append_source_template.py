#!/usr/bin/env python3
# -*- coding:utf-8
# Author Keane
# coding=utf-8
# @Time    : 2021/1/18 17:01
# @File    : deal_app_append_source_template.py
# @Software: PyCharm

import json
# from lib_conf.config import mysql_config
# from lib_conf.config import mysql_config
# from common_utils.mysql_utils import MySQLUtils
import pymysql
# from test.epaper_test.save_template_ES import SaveEpaperTemplateToES
import elasticsearch
from common_utils.llog import LLog
import hashlib


def md5(unicode_str, charset="UTF-8"):
    """
    字符串转md5格式。
    :return:
    """
    _md5 = hashlib.md5()
    _md5.update(unicode_str.encode(charset))
    return _md5.hexdigest()


class DealWithTemplates(object):

    def __init__(self):
        self.es = elasticsearch.Elasticsearch([{"host": "180.76.161.67", "port": 9200}])
        self.index_work_name = "dc_platforms"

    def get_data_from_es(self, name):

        """
        查询es
        """
        query_body = {
            "query": {"match": {"name": name}},
        }

        try:
            response = self.es.search(
                index=self.index_work_name,
                doc_type="_doc",
                body=query_body,
            )
            platform_id = ""
            if response:
                for res_data in response["hits"]["hits"]:
                    platform_id = res_data["_id"]
                return platform_id
            else:
                return []
        except Exception as e:
            raise ValueError(e)

    def intergration_data_save_to_es(self):
        """
        整合数据并存入es
        """
        mysql_config = {
            "host": "180.76.96.208",
            "port": 3306,
            "user": "debugger",
            "passwd": "903976",
            "db": "data_center",
            "charset": "utf8mb4",
            "cursorclass": pymysql.cursors.DictCursor
        }
        conmysql = pymysql.connect(**mysql_config)
        cursor = conmysql.cursor()
        sql = "select * from app_template"
        cursor.execute(sql)
        results = cursor.fetchall()
        num = 0
        for result in results:
            num += 1
            name = result["platformName"]
            if name in ["人民日报客户端","环球Time移动端"]:
                targetType =2
            else:
                targetType = 1
            app_data = {"pyName": result["app_template"],"selfTypeIDs":result["selftypeID"]}
            platform_id = self.get_data_from_es(name)
            result = {
                "platformID": platform_id,
                "_id": md5(f"{platform_id}{''}{''}{''}"),
                "platformName": name,
                "value": json.dumps(app_data),
                "platformType":4,
                "status":1,
                "targetType":targetType
            }
            res_id = result.pop("_id")
            res = self.es.index(index = "dc_source_spider_templates", doc_type = "_doc", body = result, id = res_id)
            print(res)
            print(num)
        else:
            raise ValueError("error")


if __name__ == '__main__':
    log = LLog("Test", only_console=True, logger_level="DEBUG").logger
    DealWithTemplates().intergration_data_save_to_es()
