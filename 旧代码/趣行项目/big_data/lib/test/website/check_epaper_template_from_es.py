"""
# project: 
# author: Neil
# date: 2021/1/21 19:16
# update: 
"""
import elasticsearch
from lib.common_utils.llog import LLog
from common_utils.es.scroll_search_es import scroll_search_es


class DealWithTemplates:

    def __init__(self, log):
        self.es = elasticsearch.Elasticsearch([{"host": "180.76.161.67", "port": 9200}])
        self.index_work_name = "dc_source_spider_templates"
        self._logger = log

    def get_data_from_es(self):

        """
        查询es
        """
        result_ = list()

        query_body = {
            "query": {"bool": {"must": [
                {"term": {"platformName": "中国新闻网"}},
            ]}}
        }
        hits = None
        try:
            for i, hits in enumerate(scroll_search_es(self.es, self.index_work_name, query_body, limit=1 * 10 ** 7),
                                     1):
                # noinspection PyBroadException
                try:
                    hits = hits
                except Exception as e:
                   raise ValueError(e)
            return hits
        except Exception as e:
            raise ValueError(e)


if __name__ == '__main__':
    log = LLog("Test", only_console=True, logger_level="DEBUG").logger
    res = DealWithTemplates(log).get_data_from_es()
    print(res)
