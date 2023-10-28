"""
# project: 将mysql中是报纸模板添加到es中
# author: Neil
# date: 2021/1/12 10:11
# update: 
"""

import elasticsearch
from lib.common_utils.llog import LLog


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
            "query": {"match": {"platformName": "福建日报"}},
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
                return source
        except Exception as e:
            raise ValueError(e)



if __name__ == '__main__':
    log = LLog("Test", only_console=True, logger_level="DEBUG").logger
    DealWithTemplates(log).get_data_from_es()
