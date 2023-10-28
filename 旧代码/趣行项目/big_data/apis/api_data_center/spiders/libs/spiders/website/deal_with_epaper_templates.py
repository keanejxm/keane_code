"""
# project: 将mysql中是报纸模板添加到es中
# author: Neil
# date: 2021/1/12 10:11
# update: 
"""

import json
from api.config import mysql_config
from common_utils.mysql_utils import MySQLUtils
from test.epaper_test.save_template_ES import SaveEpaperTemplateToES
import elasticsearch
from lib.common_utils.llog import LLog
import hashlib


def md5(unicode_str, charset="UTF-8"):
    """
    字符串转md5格式。
    :return:
    """
    _md5 = hashlib.md5()
    _md5.update(unicode_str.encode(charset))
    return _md5.hexdigest()


class DealWithTemplates:

    def __init__(self, log):
        self.es = elasticsearch.Elasticsearch([{"host": "180.76.161.67", "port": 9200}])
        self.index_work_name = "dc_source_spider_templates"
        self._logger = log

    def get_data_from_es(self):

        """
        查询es
        """
        query_body = {
            "query": {"match": {"platformName": "张家口市怀来县政府网"}},
        }

        try:
            response = self.es.search(
                index=self.index_work_name,
                doc_type="_doc",
                body=query_body,
            )
            source = ""
            if response:
                for res_data in response["hits"]["hits"]:
                    source = res_data["_source"]
                return source
            else:
                return []
        except Exception as e:
            raise ValueError(e)



if __name__ == '__main__':
    log = LLog("Test", only_console=True, logger_level="DEBUG").logger
    DealWithTemplates(log).get_data_from_es()
