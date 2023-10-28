# -*- coding:utf-8 -*-
"""
# project:
# author: Neil
# date: 2020/12/25
# update: 2020/12/25
"""
import hashlib
import json
import logging
import time
import traceback
import elasticsearch
from lib.common_utils.llog import LLog


def md5(unicode_str, charset="UTF-8"):
    """
    字符串转md5格式。
    :return:
    """
    _md5 = hashlib.md5()
    _md5.update(unicode_str.encode(charset))
    return _md5.hexdigest()


class SaveEpaperTemplateToES:

    def __init__(self, logger):
        # 日志对象。
        assert isinstance(logger, logging.Logger), "Error param, logger."
        self._logger = logger
        # 链接ES。
        self._es_conn = elasticsearch.Elasticsearch([{"host": "180.76.161.67", "port": 9200}])

        # 报纸模板导入。
        self._discover_epaper_template_index = "dc_source_spider_templates"
        self.default_epaper_template_fields = {
            "status": 1,
            "name": "",
            "describe": "",
            "value": "",
            "platformID": "",
            "platformName": "",
            "platformType": 5,
            "channelID": "",
            "channelName": "",
            "accountID": "",
            "accountName": "",
            "topicID": "",
            "topicTitle": "",
            "worksID": "",
            "worksTitle": "",
            "createTime": 0,
            "updateTime": 0,
        }

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

    def _es_create_new_template(self, index_name, field_id, fields):
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
        fields = dict(self.default_epaper_template_fields, **temp_fields)
        now = int(time.time() * 1000)
        fields["createTime"] = fields["updateTime"] = int(now)
        return self._es_conn.index(index=index_name, doc_type="_doc", body=fields, id=field_id)

    def save_epaper_template_to_es(self, epaper):
        """
        将版面信息存入ES。
        :param epaper: 电子报。
        :return:
        """

        # 参数验证。
        assert epaper and isinstance(epaper, (dict, list)), "Error param, layouts."

        # 统计数据。
        create_num = update_num = 0
        # 索引名。
        index_name = self._discover_epaper_template_index

        # 分为列表处理方式和字典处理方式。
        if isinstance(epaper, list):
            for fields in epaper:
                try:
                    if fields:
                        field_id = fields.pop("_id")
                        if self._es_conn.exists(index=index_name, doc_type="_doc", id=field_id):
                            continue
                        else:
                            # 执行新增。
                            res = self._es_create_new_template(index_name, field_id, fields)
                            create_num += 1
                        self._logger.info(f'{index_name} {field_id}, {res["result"]}')
                except Exception as e:
                    self._logger.warning(f"{e}\n{traceback.format_exc()}")
        elif isinstance(epaper, dict):
            fields = epaper
            if fields:
                field_id = fields.pop("_id")
                if self._es_conn.exists(index=index_name, doc_type="_doc", id=field_id):
                    # 执行更新。
                    res = self._es_update_platform(index_name, field_id, fields)
                    update_num += 1
                else:
                    # 执行新增。
                    res = self._es_create_new_template(index_name, field_id, fields)
                    create_num += 1
                self._logger.info(f'{index_name} {field_id}, {res["result"]}')
        else:
            pass

        # 记录数据。
        self._logger.info(f"{index_name} total: {create_num + update_num}, create: {create_num}, update: {update_num}.")


if __name__ == '__main__':
    log = LLog("Test", only_console=True, logger_level="DEBUG").logger
    res = {
        "_id": md5(f"{'05afba94ef0925418e4bf275d96cf1ff'}{''}{''}{''}"),
        "value": json.dumps(
            {
                "platformName": "人民网",
                "sourceProvince": "北京市",
                "sourceCity": "北京市",
                "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 1,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://www.people.com.cn/",
                # cookie
                "cookie": "wdcid=45baebdfbd94ce92; ALLYESID4=149BAB0F3E2EA038; sso_c=0; sfr=1; _"
                          "ma_tk=zgpicq5vf4yyqiqva52wj8llfb5c4mre; wdses=27fb1ccdb7c29320; _"
                          "people_ip_new_code=050000; _ma_is_new_u=0; _ma_starttm=1608694197317; wdlast=1608694396",
                # 首页头条新闻
                "headline_news": ["//div[@id='rmw_topline']//a"],
                # 轮播信息
                "banner_news": ["//ul[@class='people-container']/li/a"],
                # 轮播旁边新闻
                "banner_news_side": ["//div[@class='main ml35']/h2/a | //div[@class='main ml35']/ul/li/a |"
                                     " //div[@class='box fl ml35 news_center']/ul/li//a"],
                # 频道信息
                "channel_info_xpath": ["//nav/div[@class='w1000']/span/a"],
                # 详情链接。
                "doc_links": [
                    r"http://[\w\-\.]+\.people\.com\.cn/n1/\d{4,}/\d{4}/c\d+-\d+\.html$",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//div[@class='clearfix w1000_320 text_title']/h1/text()", },
                        {"xpath": "//div[@class='title']/h1/text()", },
                        {"xpath": "//div[@class='title']/h2/text()", },
                        {"xpath": "//h1[@class='article-title']/text()", },
                    ],
                    "content": [
                        {"xpath": "//div[@id='rwb_zw']", },
                        {"xpath": "//div[@id='picG'] | //div[@class='content clear clearfix']", },
                        {"xpath": "//div[@class='box_con']", },
                        {"xpath": "//div[@class='artDet']", },
                        {"xpath": "//div[@class='player']", },
                    ],
                    "pubSource": [
                        {
                            "describe": "http://tw.people.com.cn/n1/2020/0113/c14657-31545303.html",
                            "xpath": "//div[@class='box01']/div[@class='fl']/a/text()",
                        },
                        {
                            "describe": "http://pic.people.com.cn/n1/2020/0113/c426981-31546571.html",
                            "xpath": "//div[@class='page_c' and @style]/a/text()",
                        },
                        {
                            "xpath": "//div[@class='data']/text()",
                            "regex": r"来源[: ：](\w+)$",
                        }

                    ],
                    "pubTime": [
                        {"xpath": "//div[@class='box01']/div[@class='fl']/text()", },
                        {"xpath": "//div[@class='page_c' and @style]/text()[2]", },
                        {
                            "xpath": "//div[@class='data']/text()",
                            "regex": r"发布日期[: ：](\w+).*",
                        }
                    ],
                    "channel": [
                        {"xpath": "//span[@id='rwb_navpath']/a[@class='clink'][2]/text()"},
                        {"xpath": "//div[@class='fl']/a[@class='clink'][2]/text()"},
                    ],
                    "authors": [],
                    "summary": [],
                }
            })
    }
    SaveEpaperTemplateToES(log).save_epaper_template_to_es(res)
