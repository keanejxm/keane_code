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
        # for name in [
        #     # "人民日报",
        #     # "光明日报",
        #     "新华每日电讯",
        #     # "解放军报",
        #     # "工人日报",
        #     # "农民日报",
        #     # "经济日报",
        #     # "学习时报",
        #     # "科技日报",
        #     # "人民政协报",
        #     "中国纪检监察报",
        #     # "中国青年报",
        #     # "中国妇女报",
        #     # "人民日报海外版"
        #     # "河北日报",
        #     # "山西日报",
        #     # "辽宁日报",
        #     # "吉林日报",
        #     # "浙江日报",
        #     # "安徽日报",
        #     # "福建日报",
        #     # "江西日报",
        #     # "河南日报",
        #     # "湖北日报",
        #     # "湖南日报",
        #     # "海南日报",
        #     # "四川日报",
        #     # "贵州日报",
        #     # "云南日报",
        #     # "陕西日报",
        #     # "青海日报",
        #     ]:
        name = "潍坊日报"
        query_body = {
            "query": {"bool": {"must": [
                {"term": {"platformName": name}},
            ]}}
        }

        try:
            for i, hits in enumerate(scroll_search_es(self.es, self.index_work_name, query_body, limit=1 * 10 ** 7),
                                     1):
                # noinspection PyBroadException
                try:
                    hits = hits
                    # result_.append(hits)
                    print(hits)
                    return hits
                except Exception as e:
                    print(f"{name}模板不存在")

        except Exception as e:
            print(f"{name}模板不存在")



if __name__ == '__main__':
    log = LLog("Test", only_console=True, logger_level="DEBUG").logger
    res = DealWithTemplates(log).get_data_from_es()
    print(res)
