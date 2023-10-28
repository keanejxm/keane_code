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
        self.index_work_name = "dc_platforms"
        self._logger = log

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
            types = []
            if response:
                for res_data in response["hits"]["hits"]:
                    platform_id = res_data["_id"]
                    types = res_data["_source"]["types"]
                return platform_id, types
            else:
                return []
        except Exception as e:
            raise ValueError(e)

    def intergration_data_save_to_es(self):
        """
        整合数据并存入es
        """
        # conmysql = MySQLUtils(**mysql_config)
        # sql = f"select epaperTemplate from epaper_template where platformName='福建日报';"
        # res = conmysql.search(sql)
        res = [{
        "platformName": "潍坊日报",
        "sourceProvince": "山东",
        "sourceCity": "",
        # 1：国家级，2：省级，3：市级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 0,
        # 是否主流媒体。
        "mainMedia": 0,
        # %Y%m%d，{proxies}。
        "start_url": "http://wfrb.wfnews.com.cn/content/%Y%m%d/Page01JQ.htm",
        "cookiestr": "",
        # 版面url。
        "layout_url_xpath": ["//td[@class='default' and @align='left']/a/@href"],
        # 下一版链接
        "layout_next_xpath": [],
        # 版面名称
        "layout_title_xpath": ['//td[@align="left" ]/strong/..//text()'],
        # 版面标签
        "layout_map_xpath": [],
        # 版面图链接
        "layout_map_image_xpath": ["//img[@usemap='#PageMap']/@src"],
        "layout_large_image_xpath": [],
        # 版面图链接pdf链接
        "layout_pdf_xpath": [],
        # 稿件详情。
        "detail_url_xpath": ["//div[@id='mylink']/a/@href"],
        # 预标题
        "detail_pre_title_xpath": ["//*[@id='suptitle']/text()"],
        # 主标题
        "detail_title_xpath": ['//*[@id="title"]/text()'],
        # 子标题
        "detail_sub_title_xpath": ['//*[@id="subtitle"]/text()'],
        # 正文内容
        "detail_content_xpath": ['//td[@class="font6"]/table//td[@align="middle"]/table//table//tr/td | //div[@id="ozoom"]'],
        # 提交时间
        "detail_pubTime_xpath": [],

    }]
        if res:
            for epaper_data in res:
                # epaper_data = json.loads(epaper_data["epaperTemplate"])
                # 修改值
                # # %Y-%m/%d，
                dum = json.dumps(epaper_data, ensure_ascii=False)
                name = epaper_data["platformName"]
                platform_id, types = self.get_data_from_es(name)
                result = {
                    "platformID": platform_id,
                    "_id": md5(f"{platform_id}{''}{''}{''}"),
                    "platformName": name,
                    "platformType": 5,
                    "value": dum,
                    "types": types,
                }
                SaveEpaperTemplateToES(log).save_epaper_template_to_es(result)
                self._logger.info(f"{name}保存成功")
        else:
            raise ValueError("error")


if __name__ == '__main__':
    log = LLog("Test", only_console=True, logger_level="DEBUG").logger
    DealWithTemplates(log).intergration_data_save_to_es()
