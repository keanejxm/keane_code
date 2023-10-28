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
        # 网站模板
        res = [
            # 山西法制网
            {
                "platformName": "山西法制网",
                "sourceProvince": "山西省",
                "sourceCity": "",
                "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://www.sxfzb.com/",
                "cookie": "ci_session=13qsaed0mnd3mg2fs3gg5vgh70dsjc06; Hm_lvt_bee79f8ca758e151eadd747e948013b3=1610335789; Hm_lvt_b393d153aeb26b46e9431fabaf0f6190=1610335790; Hm_lpvt_bee79f8ca758e151eadd747e948013b3=1610335813; Hm_lpvt_b393d153aeb26b46e9431fabaf0f6190=1610335813",
                # 首页头条新闻
                "headline_news": ["//div[@class=\"main toutiao\"]//a"],
                # 轮播信息
                "banner_news": ["//div[@class=\"yw_l\"]/div/div[@class=\"bd\"]/ul/li/a"],
                # 轮播旁边新闻
                "banner_news_side": ["//div[@class=\"yw_r\"]/div/div[@class=\"bd\"]/ul/li/a"],
                # 导航信息
                "channel_info_xpath": ["//div[@class=\"nav\"]/ul/li/a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/index.php/\w+/\w+/\d+",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//div[@class=\"title\"]/text()", },
                    ],
                    "content": [{"xpath": "//div[@id=\"Content \"]", }, ],
                    "pubSource": [
                        {
                            "xpath": "//div[@class=\"box_info\"]/p/text()",
                            "regex": r"来源[: ：](\w+)$",

                        }
                    ],
                    "pubTime": [
                        {
                            "xpath": "//div[@class=\"box_info\"]/p/text()",
                            "regex": r"发布时间[: ：](.*)阅读.*$",
                        },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },
            # 太原新闻网
            {
                "platformName": "太原新闻网",
                "sourceProvince": "山西省",
                "sourceCity": "",
                "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://www.tynews.com.cn/",
                "cookie": "UM_distinctid=176ef8cb5439d2-0d7c2a956a87ae-4353760-144000-176ef8cb544b15; CNZZDATA1253696506=1676426552-1610332246-%7C1610332246; zycna=74y3rUV0N/ABAXvEgSLir0+j",
                # 首页头条新闻
                "headline_news": ["//div[@class=\"headlines\"]/span/a | //div[@class=\"headmore\"]/p/a"],
                # 轮播信息
                "banner_news": ["//div[@id=\"focus\"]//ul[@class=\"slides\"]/li/a"],
                # 轮播旁边新闻
                "banner_news_side": ["//div[@id=\"newsFocus\"]/div/ul/li/a"],
                # 导航信息
                "channel_info_xpath": ["//div[@id=\"pcHeader\"]/div/div/a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/system/\d{4,}/\d{2,}/\d{2,}/\d+.shtml$",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//h1[@class=\"title\"]/text()", },
                    ],
                    "content": [{"xpath": "//div[@id=\"article\"]", }, ],
                    "pubSource": [
                        {
                            "xpath": "//div[@class=\"info clearfix\"]/span[1]/a/text()",
                        }
                    ],
                    "pubTime": [
                        {
                            "xpath": "//div[@class=\"info clearfix\"]/span[3]/text()",
                        },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },
            # 安徽新闻网
            {
                "platformName": "安徽新闻网",
                "sourceProvince": "安徽省",
                "sourceCity": "",
                "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://www.ahnews.com.cn/",
                "cookie": "UM_distinctid=176efcf504770c-0551bc1963a2e8-4353760-144000-176efcf5048a52; CNZZDATA1275212582=108674766-1610338056-%7C1610338056",
                # 首页头条新闻
                "headline_news": ["//div[@id=\"headLine\"]/div/div/a"],
                # 轮播信息
                "banner_news": ["//div[@id=\"rmw_focus\"]/div/ul/li/a"],
                # 轮播旁边新闻
                "banner_news_side": [
                    "//div[@class=\"hots\"]/p/a | //div[@id=\"hpart2L\"]/h3/a | //div[@id=\"hpart2L\"]/ul/li/a"],
                # 导航信息
                "channel_info_xpath": ["//div[@id=\"navBody\"]/div/ul/li/a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/[a-z0-9]+/\w+/\w+/\d{4,}-\d{2,}/\d{2,}/\d+_\d+.html$",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//div[@class=\"h-title\"]/text()", },
                    ],
                    "content": [{"xpath": "//div[@id=\"p-detail\"]", }, ],
                    "pubSource": [
                        {
                            "xpath": "//div[@class=\"h-info\"]/span[1]/text()",
                            "regex": r"来源[: ：]\s*?(.*)$",
                        }
                    ],
                    "pubTime": [
                        {
                            "xpath": "//span[@class=\"h-time\"]/text()",
                        },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },
            # 法治安徽网
            {
                "platformName": "法治安徽网",
                "sourceProvince": "安徽省",
                "sourceCity": "",
                "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://www.fzahw.com/",
                "cookie": "",
                # 首页头条新闻
                "headline_news": ["//div[@class=\"fl news\"]/h3/a"],
                # 轮播信息
                "banner_news": ["//div[@class=\"index-4 clr\"]//div[@class=\"swiper-wrapper\"]/div/div[1]/a"],
                # 轮播旁边新闻
                "banner_news_side": [
                    "//div[@class=\"index-4-rt clr fr\"]//a"],
                # 导航信息
                "channel_info_xpath": ["//div[@class=\"nav clr\"]/div/ul/li/a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/index.php.*",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//div[@class=\"wd1150 clr\"]/h1[2]/text()", },
                    ],
                    "content": [{"xpath": "//div[@id=\"content\"]", }, ],
                    "pubSource": [
                        {
                            "xpath": "//div[@class=\"time\"]/text()",
                            "regex": r"稿源[: ：]\s*?(.*)]$",
                        }
                    ],
                    "pubTime": [
                        {
                            "xpath": "//div[@class=\"time\"]/text()",
                            "regex": r"时间[: ：]\s*?(.*)稿源.*$",
                        },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },
            # 安徽经济新闻网
            {
                "platformName": "安徽经济新闻网",
                "sourceProvince": "安徽省",
                "sourceCity": "",
                "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://www.ahenews.com.cn/",
                "cookie": "",
                # 首页头条新闻
                "headline_news": ["//div[@class=\"content\"]//a"],
                # 轮播信息
                "banner_news": ["//div[@id=\"swiper-1\"]/div/div/a"],
                # 轮播旁边新闻
                "banner_news_side": [
                    "//div[@class=\"fl text click-tabbar\"]/ul/li/a"],
                # 导航信息
                "channel_info_xpath": ["//div[@class=\"column fc\"]/a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/\w+/\w+/\d{4,}-\d{2,}-\d{2,}/\d+.html",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//h3[@class=\"title\"]/text()", },
                    ],
                    "content": [{"xpath": "//div[@class=\"body\"]", }, ],
                    "pubSource": [
                    ],
                    "pubTime": [
                        {
                            "xpath": "//span[@class=\"d\"]/text()",
                        },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },
            # 黄河新闻网
            {
                "platformName": "黄河新闻网",
                "sourceProvince": "山西省",
                "sourceCity": "",
                "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://www.sxgov.cn/",
                "cookie": "",
                # 首页头条新闻
                "headline_news": ["//div[@id=\"toutiao\"]/h1/a | //div[@id=\"toutiao\"]/h2/a"],
                # 轮播信息
                "banner_news": [],
                # 轮播旁边新闻
                "banner_news_side": [
                    "//div[@id=\"con1righta\"]/ul/li/a"],
                # 导航信息
                "channel_info_xpath": ["//div[@id=\"menulefta\"]/a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2,}/\w+_\d+.htm",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//div[@class=\"dahei\"]/text()", },
                    ],
                    "content": [{"xpath": "//div[@class=\"Newsfont\"]", }, ],
                    "pubSource": [
                        {
                            "xpath": "//span[@id=\"source_baidu\"]/text()",
                            "regex": r"来源[: ：]\s*?(.*)$",
                        }
                    ],
                    "pubTime": [
                        {
                            "xpath": "//span[@id=\"pubtime_baidu\"]/text()",
                        },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },
            # 河北经济网
            {
                "platformName": "河北经济网",
                "sourceProvince": "河北省",
                "sourceCity": "",
                "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://www.hbjjrb.com/",
                "cookie": "",
                # 首页头条新闻
                "headline_news": ["//div[@id=\"news_rolling\"]/ul/li/a"],
                # 轮播信息
                "banner_news": ["//div[@id=\"lhdxw_tabSlide\"]/div/div/a"],
                # 轮播旁边新闻
                "banner_news_side": [
                    "//div[@class=\"tt_left\"]/ul/li/a"],
                # 导航信息
                "channel_info_xpath": ["//div[@class=\"navblue\"]/div/ul/li/a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/\w+/\d{4,}/\d{2,}/\d{2,}/\d+.shtml",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//div[@class=\"g_width content\"]/h1/text()", },
                    ],
                    "content": [{"xpath": "//div[@class=\"main_left\"]", }, ],
                    "pubSource": [
                        {
                            "xpath": "//div[@class=\"post_source\"]/text()",
                            "regex": r"来源[: ：]\s*?(.*)\d{4,}.*",
                        }
                    ],
                    "pubTime": [
                    ],
                    "authors": [],
                    "summary": [],
                }
            },
            # 长城网
            {
                "platformName": "长城网",
                "sourceProvince": "河北省",
                "sourceCity": "",
                "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://www.hebei.com.cn/",
                "cookie": "Hm_lvt_92396e74c684f3350d1339e0cfa20423=1610351060; Hm_lpvt_92396e74c684f3350d1339e0cfa20423=1610351060; Hm_lvt_9f14d979332fd6e91cb6fbbfc0a6a211=1610351060; Hm_lpvt_9f14d979332fd6e91cb6fbbfc0a6a211=1610351060; UM_distinctid=176f067255f2ab-0656d0225373a4-4353760-144000-176f0672560afb; CNZZDATA1273191674=1641680346-1610350221-%7C1610350221; uid=1610351061094_6523821532",
                # 首页头条新闻
                "headline_news": ["//div[@id=\"news_rolling\"]/ul/li/a | //div[@class=\"xjpdttxg\"]/a"],
                # 轮播信息
                "banner_news": ["//div[@id=\"tabSlide\"]/div/div/a"],
                # 轮播旁边新闻
                "banner_news_side": [
                    "//div[@class=\"news_left\"]/ul/li/a"],
                # 导航信息
                "channel_info_xpath": ["//div[@class=\"navred\"]/div//div[1]/li/a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/\w+/\d{4,}/\d{2,}/\d{2,}/\d+.shtml",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//div[@class=\"g_width content\"]/h1/text()", },
                    ],
                    "content": [{"xpath": "//div[@class=\"main_left\"]", }, ],
                    "pubSource": [
                        {
                            "xpath": "//div[@class=\"post_source\"]/text()",
                            "regex": r"来源[: ：]\s*?(.*)\d{4,}.*",
                        }
                    ],
                    "pubTime": [
                    ],
                    "authors": [],
                    "summary": [],
                }
            },
            # 河北法制网
            {
                "platformName": "河北法制网",
                "sourceProvince": "河北省",
                "sourceCity": "",
                "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "https://www.hbfzb.com/",
                "cookie": "UM_distinctid=176f07d5e8d247-0473faa1f3b54e-4353760-144000-176f07d5e8e946; CNZZDATA2489726=cnzz_eid%3D750772888-1610347806-%26ntime%3D1610347806",
                # 首页头条新闻
                "headline_news": ["//div[@class=\"conA_lft_tit\"]//a"],
                # 轮播信息
                "banner_news": ["//div[@id=\"KSS_content\"]/a"],
                # 轮播旁边新闻
                "banner_news_side": [
                    "//div[@class=\"fzhb_con\"]/ul/li/a"],
                # 导航信息
                "channel_info_xpath": ["//div[@class=\"nav\"]/ul/li/a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/\w+/\d{4,}/fazhihebei_\d+/\d+.html",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//div[@class=\"wzyA_tit\"]/h3/text()", },
                    ],
                    "content": [{"xpath": "//div[@class=\"wzyA_con\"]", }, ],
                    "pubSource": [
                        {
                            "xpath": "//div[@class=\"wzyA_tit_a\"]/span[2]/a/text()",
                        }
                    ],
                    "pubTime": [
                        {"xpath": "//div[@class=\"wzyA_tit_a\"]/span[1]/text()"}

                    ],
                    "authors": [],
                    "summary": [],
                }
            },
            # 石家庄新闻网
            {
                "platformName": "石家庄新闻网",
                "sourceProvince": "河北省",
                "sourceCity": "",
                "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://www.sjzdaily.com.cn/",
                "cookie": "",
                # 首页头条新闻
                "headline_news": ["//div[@class=\"hl_1\"]/h1/a | //div[@class=\"hl1m_right\"]/ul/li/a"],
                # 轮播信息
                "banner_news": ["//div[@class=\"boxImage\"]/div/div/a"],
                # 轮播旁边新闻
                "banner_news_side": [
                    "//div[@class=\"w1100-w1200\"]//a | //ul[@class=\"font_inner\"]/li//a"],
                # 导航信息
                "channel_info_xpath": ["//div[@class=\"m_navs page_header\"]/ul/li/a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/\d{4,}/\d{2,}/\d{2,}/\d+.html",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//h1[@class=\"news_title\"]/text()", },
                        {"xpath": "//div[@class=\"title clearfix\"]/h1/text()", },
                    ],
                    "content": [
                        {"xpath": "//div[@class=\"news_txt\"]", },
                        {"xpath": "//div[@class=\"content\"]", },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//div[@class=\"news_about\"]/p[2]/span/text()",
                            "regex": r"来源[: ：]\s*?(.*)",
                        }
                    ],
                    "pubTime": [
                        {"xpath": "//div[@class=\"news_about\"]/p[2]/text()"},
                        {"xpath": "//span[@id=\"pubtime\"]/text()"}

                    ],
                    "authors": [],
                    "summary": [],
                }
            },
            # 张家口新闻网
            {
                "platformName": "张家口新闻网",
                "sourceProvince": "河北省",
                "sourceCity": "",
                "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://www.zjknews.com/",
                "cookie": "Hm_lvt_0a8bd715bbdb8052327b7c58dcb4fe38=1610355092; Hm_lpvt_0a8bd715bbdb8052327b7c58dcb4fe38=1610355092",
                # 首页头条新闻
                "headline_news": ["//div[@class=\"pro-title\"]/a"],
                # 轮播信息
                "banner_news": ["//div[@class=\"swiper-wrapper\"]/div/a"],
                # 轮播旁边新闻
                "banner_news_side": [
                    "//ul[@class=\"hotnews\"]/li/a"],
                # 导航信息
                "channel_info_xpath": ["//div[@class=\"maincenter clearfix\"]/div/ul/li/a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/\w+/\w+/\d{4,}\d{2,}/\d{2,}/\d+.html",
                    r"https?://[\w\-\.]+/\w+/\w+/\w+/\d{4,}\d{2,}/\d{2,}/\d+.html"
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//h1[@class=\"w1 hot_h1\"]//text()", },
                    ],
                    "content": [
                        {"xpath": "//div[@class=\"i_left fl\"]", },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//span[@class=\"key_word\"]/a/text()",
                        }
                    ],
                    "pubTime": [
                        {"xpath": "//span[@class=\"key_word\"]/text()",
                         "regex": r"(.*)来源.*", },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },
            # 京华网
            {
                "platformName": "京华网",
                "sourceProvince": "北京",
                "sourceCity": "",
                "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://www.jinghva.com/",
                "cookie": "Hm_lvt_a082710d86f8a8f8959ba4f51fb0365a=1610356473; Hm_lpvt_a082710d86f8a8f8959ba4f51fb0365a=1610356491",
                # 首页头条新闻
                "headline_news": [],
                # 轮播信息
                "banner_news": ["//div[@id=\"banner_silider\"]/a"],
                # 轮播旁边新闻
                "banner_news_side": [
                    "//div[@id=\"J_hot_news\"]/div//a"],
                # 导航信息
                "channel_info_xpath": ["//div[@id=\"nav_cnt\"]/ul/li/a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/\w+/\d+.html",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//div[@class=\"J-title_detail title_detail\"]/h1/span/text()", },
                    ],
                    "content": [
                        {"xpath": "//div[@class=\"J-contain_detail_cnt contain_detail_cnt\"]", },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//div[@class=\"share_cnt_p\"]/i[2]/text()",
                        }
                    ],
                    "pubTime": [
                        {"xpath": "//div[@class=\"share_cnt_p\"]/i[1]/text()", },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },
            # 法制期刊网
            {
                "platformName": "法制期刊网",
                "sourceProvince": "北京",
                "sourceCity": "",
                "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://www.fzqkw.com/",
                "cookie": "",
                # 首页头条新闻
                "headline_news": ["//h1[@class=\"fontwr\"]/a"],
                # 轮播信息
                "banner_news": ["//div[@class=\"flashlist\"]/div/a"],
                # 轮播旁边新闻
                "banner_news_side": [
                    "//ul[@class=\"groom\"]/li//a"],
                # 导航信息
                "channel_info_xpath": ["//div[@class=\"mainnav\"]/div/a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/\w+/\w+/\d+/\d+/\d+.html",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//div[@class=\"left1_a\"]/h1/text()", },
                    ],
                    "content": [
                        {"xpath": "//div[@class=\"left1_d\"]", },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//div[@class=\"left1_b\"]/span[2]/text()",
                            "regex": r"来源[: ：]\s*?(.*)点击.*",
                        }
                    ],
                    "pubTime": [
                        {"xpath": "//div[@class=\"left1_b\"]/span[1]/text()", },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },
            # 合肥网
            {
                "platformName": "合肥网",
                "sourceProvince": "安徽省",
                "sourceCity": "",
                "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://www.wehefei.com/",
                "cookie": "UM_distinctid=176f168804026-0a47fd804e620e-4353760-144000-176f1688041a93; CNZZDATA2516558=cnzz_eid%3D472082583-1610365873-%26ntime%3D1610365873; CNZZDATA3509894=cnzz_eid%3D1508588521-1610367926-%26ntime%3D1610367926",
                # 首页头条新闻
                "headline_news": ["//div[@class=\"left\"]/div/a | //div[@class=\"p2 p\"]/a"],
                # 轮播信息
                "banner_news": [],
                # 轮播旁边新闻
                "banner_news_side": [
                    "//div[@class=\"p9 p\"]/ul/li/a | //div[@class=\"p4 p\"]/div/ul/li/a"],
                # 导航信息
                "channel_info_xpath": ["//div[@class=\"links\"]/span/a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/\w+/\d{4,}/\d{2,}/\d{2,}/\w_\d+.htm",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//div[@id=\"title\"]/text()", },
                    ],
                    "content": [
                        {"xpath": "//div[@class=\"left\"]", },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//div[@class=\"info p\"]/span[1]/text()",
                            "regex": r".*来源[: ：]\s*?(.*)$",
                        },
                    ],
                    "pubTime": [
                        {"xpath": "//span[@class=\"pub-time\"]/text()", },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },

            # 1/14
            # 合肥市先锋网
            {
                "platformName": "合肥市先锋网",
                # "sourceProvince": "安徽省",
                # "sourceCity": "",
                # "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://www.hfxf.gov.cn/",
                "cookie": "__jsluid_h=6ec00f90dd10d65ba4edca8673a0598c; hefei_gove_SHIROJSESSIONID=9eaa8e06-fd3b-44d1-9527-e0689054e12e",
                # 首页头条新闻
                "headline_news": ["//div[@class=\"newstext\"]/div/p/a"],
                # 轮播信息
                "banner_news": ["//div[@class=\"box\"]/ul/li/a"],
                # 轮播旁边新闻
                "banner_news_side": [
                    "//div[@class=\"section\"]/div/div[2]/ul/li/a"],
                # 导航信息
                "channel_info_xpath": ["//div[@class=\"menu1\"]/ul/li/a"],
                # 详情链接。
                "doc_links": [
                    r"http?://[\w\-\.]+/\w+/\d+.html",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//h1[@class=\"newstitlee\"]/text()", },
                    ],
                    "content": [
                        {"xpath": "//div[@class=\"j-fontContent datail_content\"]", },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//div[@class=\"showxx\"]/b[2]/text()",
                            "regex": r"发布者[: ：]\s*?(.*)$",
                        },
                    ],
                    "pubTime": [
                        {"xpath": "//div[@class=\"showxx\"]/b[3]/text()",
                         "regex": r"发布日期[: ：]\s*?(.*)$", },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },
            # 芜湖市政府网
            {
                "platformName": "芜湖市政府网",
                # "sourceProvince": "安徽省",
                # "sourceCity": "",
                # "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://www.wuhu.gov.cn/",
                "cookie": "SHIROJSESSIONID=e3f08a9c-e356-44f9-80f0-845c93eeaaf0",
                # 首页头条新闻
                "headline_news": ["//h2[@class=\"title\"]/a"],
                # 轮播信息
                "banner_news": ["//div[@class=\"pic\"]/ul/li/a"],
                # 轮播旁边新闻
                "banner_news_side": [
                    "//div[@class=\"xwcon\"]/div/ul/li/a"],
                # 导航信息
                "channel_info_xpath": ["//ul[@class=\"nav navbar-nav\"]/li/a"],
                # 详情链接。
                "doc_links": [
                    r"http?://[\w\-\.]+/\w+/\w+/\d+.html",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//h1[@class=\"wztit\"]/text()", },
                    ],
                    "content": [
                        {"xpath": "//div[@class=\"wzcon j-fontContent clearfix\"]", },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//span[@class=\"res\"]/text()",
                            "regex": r"信息来源[: ：]\s*?(.*)$",
                        },
                    ],
                    "pubTime": [
                        {"xpath": "//span[@class=\"fbsj\"]/text()",
                         "regex": r"发布时间[: ：]\s*?(.*)", },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },
            # 芜湖长安网
            {
                "platformName": "芜湖长安网",
                # "sourceProvince": "安徽省",
                # "sourceCity": "",
                # "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://whcaw.wh.cn/",
                "cookie": "SHIROJSESSIONID=2743eab5-512f-46e8-9ba9-302edd84ec4e",
                # 首页头条新闻
                "headline_news": [],
                # 轮播信息
                "banner_news": ["//div[@class=\"pic\"]/ul/li/a"],
                # 轮播旁边新闻
                "banner_news_side": [
                    "//div[@class=\"fl ind_newsbox\"]/div[@class=\"xw_list\"]/ul/li/a"],
                # 导航信息
                "channel_info_xpath": ["//div[@class=\"menubox\"]/ul/li/a"],
                # 详情链接。
                "doc_links": [
                    r"http?://[\w\-\.]+/\w+/\w+/\d+.html",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//h1[@class=\"newstitle\"]/text()", },
                    ],
                    "content": [
                        {"xpath": "//div[@class=\"wzcon j-fontContent\"]", },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//span[@class=\"wz_res\"]/text()",
                            "regex": r"来源[: ：]\s*?(.*)$",
                        },
                    ],
                    "pubTime": [
                        {"xpath": "//span[@class=\"wz_date\"]/text()",
                         "regex": r"发布时间[: ：]\s*?(.*)", },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },
            # 芜湖新闻网
            {
                "platformName": "芜湖新闻网",
                # "sourceProvince": "安徽省",
                # "sourceCity": "",
                # "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://www.wuhunews.cn/",
                "cookie": "SHIROJSESSIONID=2743eab5-512f-46e8-9ba9-302edd84ec4e",
                # 首页头条新闻
                "headline_news": [
                    "//div[@class=\"topnews hd\"]//h1/a | //div[@class=\"topnews hd\"]//div[1]/a |//div[@class=\"topnews\"]/h1/a"],
                # 轮播信息
                "banner_news": ["//div[@class=\"topnews\"]//div[@class=\"swiper-wrapper\"]/div/a"],
                # 轮播旁边新闻
                "banner_news_side": [
                    "//div[@class=\"topnews\"]/div[@class=\"news-list\"]/ul/li/a"],
                # 导航信息
                "channel_info_xpath": ["//ul[@class=\"wrap\"]/li//a"],
                # 详情链接。
                "doc_links": [
                    r"http?://[\w\-\.]+/\w+/\w/\d+.html",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//h1[@class=\"title\"]/text()", },
                        {"xpath": "//article[@class=\"article-content\"]/h1/text()", },
                    ],
                    "content": [
                        {"xpath": "//div[@class=\"article-content\"]", },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//span[@class=\"source\"]/a/text()",
                        },
                    ],
                    "pubTime": [
                        {"xpath": "//time[@class=\"date\"]/text()", },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },
            # 芜湖网
            {
                "platformName": "芜湖网",
                # "sourceProvince": "安徽省",
                # "sourceCity": "",
                # "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://www.wewuhu.com/",
                "cookie": "UM_distinctid=176ffe023ecadc-05c6c23be40eb1-4353760-144000-176ffe023ed6e3; Hm_lvt_8d97d01ebdcfd50d8236fd3eb9f1641f=1610610650; CNZZDATA1260616684=961364525-1610605416-%7C1610611440; Hm_lpvt_8d97d01ebdcfd50d8236fd3eb9f1641f=1610614982",
                # 首页头条新闻
                "headline_news": [
                    "//div[@class=\"headlines\"]//a"],
                # 轮播信息
                "banner_news": ["//div[@id=\"focus\"]/ul[@class=\"pp\"]/li/a"],
                # 轮播旁边新闻
                "banner_news_side": [
                    "//div[@class=\"four_headlines fr\"]//a"],
                # 导航信息
                "channel_info_xpath": ["//div[@class=\"nav\"]/div/dl//a"],
                # 详情链接。
                "doc_links": [
                    r"http?://[\w\-\.]+/\w+/\d+/\d+.html",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//div[@class=\"main_news_l fl\"]/h1/text()", },

                    ],
                    "content": [
                        {"xpath": "//div[@class=\"artical\"]", },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//em[@class=\"form\"]/a/text()",
                        },
                    ],
                    "pubTime": [
                        {"xpath": "//em[@class=\"time\"]/text()",
                         "regex": r"时间[: ：]\s*?(.*)", },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },
            # 蚌埠市政府网
            {
                "platformName": "蚌埠市政府网",
                # "sourceProvince": "安徽省",
                # "sourceCity": "",
                # "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://www.bengbu.gov.cn/",
                "cookie": "__jsluid_h=ef0ec13b85e2bf562aaa3739c3de2733; membercenterjsessionid=ODYwOWY0NWEtNGIxMi00NmMzLWJmZDAtYjE1ZWRhMGRiNWFk; SHIROJSESSIONID=bca3b1ae-d07a-41b4-8adb-9fa83ce134e1",
                # 首页头条新闻
                "headline_news": [
                    "//ul[@class=\"list1\"]/h2/a"],
                # 轮播信息
                "banner_news": ["//*[@id=\"myFocus01\"]/div[1]/ul/li/a"],
                # 轮播旁边新闻
                "banner_news_side": [
                    "//*[@id=\"container\"]/div[2]/div/div[3]/div[2]/div[2]/ul/li/a"],
                # 导航信息
                "channel_info_xpath": ["//ul[@class=\"nav navbar-nav\"]/li/a"],
                # 详情链接。
                "doc_links": [
                    r"http?://[\w\-\.]+/\w+/\w+/\d+.html",
                    r"http?://[\w\-\.]+/\w+/\d+/\d+.html",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//h1[@class=\"newstitle\"]/text()", },
                        {"xpath": "//h1[@class=\"wztit xxgk_wztit\"]/text()", },

                    ],
                    "content": [
                        {"xpath": "//div[@class=\"j-fontContent newscontnet minh300\"]", },
                        {"xpath": "//div[@class=\"wzcon j-fontContent\"]", },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//*[@id=\"color_printsssss\"]/div[1]/span[2]/text()",
                            "regex": r"信息来源[: ：]\s*?(.*)",
                        },
                        {
                            "xpath": "//span[@class=\"fbxx\"]/text()",
                            "regex": r"来源[: ：]\s*?(.*)",
                        },
                    ],
                    "pubTime": [
                        {"xpath": "//*[@id=\"color_printsssss\"]/div[1]/span[1]/text()",
                         "regex": r"发布日期[: ：]\s*?(.*)", },
                        {"xpath": "//*[@id=\"zcjdDiv\"]/table/tbody/tr[3]/td[2]/text()",
                         },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },
            # 蚌埠长安网
            {
                "platformName": "蚌埠长安网",
                # "sourceProvince": "安徽省",
                # "sourceCity": "",
                # "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://swzfw.bb.ah.cn/",
                "cookie": "__jsluid_h=2567dcde6f0a927e20d6f1a530a37a25; SHIROJSESSIONID=186d4d7a-b17f-42a6-9089-c807524482ae",
                # 首页头条新闻
                "headline_news": [],
                # 轮播信息
                "banner_news": ["//*[@id=\"myFocus02\"]/div[1]/ul/li/a"],
                # 轮播旁边新闻
                "banner_news_side": [
                    "/html/body/div[2]/div[1]/div[2]/div[2]//a"],
                # 导航信息
                "channel_info_xpath": ["//div[@class=\"header_nav\"]/ul/li/a"],
                # 详情链接。
                "doc_links": [
                    r"http?://[\w\-\.]+/\w+/\d+.html",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//h1[@class=\"newstitle\"]/text()", },
                    ],
                    "content": [
                        {"xpath": "//div[@class=\"j-fontContent newscontnet minh300\"]", },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//*[@id=\"color_printsssss\"]/div[1]/span[2]/text()",
                            "regex": r"信息来源[: ：]\s*?(.*)",
                        },
                    ],
                    "pubTime": [
                        {"xpath": "//*[@id=\"color_printsssss\"]/div[1]/span[1]/text()",
                         "regex": r"发布日期[: ：]\s*?(.*)", },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },
            # 蚌埠新闻网
            {
                "platformName": "蚌埠新闻网",
                # "sourceProvince": "安徽省",
                # "sourceCity": "",
                # "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://www.bbnews.cn/",
                "cookie": "PASSPORTID=uam9lfgsso4b3792qr7g6lgbg4; Users_CtmediaSetting=%7B%22id%22%3A%221%22%2C%22siteid%22%3A%2210001%22%2C%22platform_name%22%3A%22%22%2C%22platform_thumb%22%3A%22%22%2C%22fans_num%22%3A%220%22%2C%22subscribe_num%22%3A%220%22%2C%22is_pv%22%3A%221%22%2C%22isday_num%22%3A%220%22%2C%22day_num%22%3A%2210%22%2C%22agreement_title%22%3A%22%22%2C%22tips%22%3A%22%22%2C%22istips%22%3A%220%22%7D; zycna=AKROZg9vPHwBAXvEgSIQa2tE",
                # 首页头条新闻
                "headline_news": ["//div[@class=\"content_one_p1\"]/div/p/a | //div[@class=\"fl\"]/p/a"],
                # 轮播信息
                "banner_news": [],
                # 轮播旁边新闻
                "banner_news_side": [
                    "//div[@class=\"content_two\"]/div/dl//a"],
                # 导航信息
                "channel_info_xpath": ["//div[@class=\"nav\"]/ul/li/a"],
                # 详情链接。
                "doc_links": [
                    r"http?://[\w\-\.]+/[a-z0-9]+/p/\d+.html.*",
                    r"http?://[\w\-\.]+/\w+/\w+/\d{4,}-\d{2,}/\d{2,}/c_\d+.htm.*",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//div[@class=\"header_details_tit\"]/h1/text()", },
                        {"xpath": "//div[@class=\"h-title\"]/text()", },
                    ],
                    "content": [
                        {"xpath": "//div[@class=\"Rich_text\"]", },
                        {"xpath": "//div[@id=\"detail\"]", },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//div[@class=\"header_details_tit_tip\"]/span[2]/text()",
                        },
                        {
                            "xpath": "//span[@class=\"aticle-src\"]/text()",
                        },
                    ],
                    "pubTime": [
                        {"xpath": "//div[@class=\"header_details_tit_tip\"]/span[1]/text()", },
                        {"xpath": "//span[@class=\"h-time\"]/text()", },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },
            # 淮南市政府网
            {
                "platformName": "淮南市政府网",
                # "sourceProvince": "安徽省",
                # "sourceCity": "",
                # "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://www.huainan.gov.cn/",
                "cookie": "__cfduid=d7fec309fe686f2bc3d17bd33122736701610625537; membercenterjsessionid=N2U0M2RiMzktM2Q3Zi00ZjdmLWFiNjUtZmQyODQ5YzdmYTg3; hn_gova_SHIROJSESSIONID=be614537-fb56-46eb-acbf-b24ad7f79bd2",
                # 首页头条新闻
                "headline_news": ["//h1[@class=\"dbt\"]/a | //ul[@class=\"zt clearfix\"]/li/a"],
                # 轮播信息
                "banner_news": ["//*[@id=\"myFocus011\"]/div[1]/ul/li/a"],
                # 轮播旁边新闻
                "banner_news_side": [
                    "//div[@class=\"ind_xwlist\"]/ul/li/a"],
                # 导航信息
                "channel_info_xpath": ["/html/body/div[1]/div[1]/div[3]/div/dl/dd/div[1]/a"],
                # 详情链接。
                "doc_links": [
                    r"http?://[\w\-\.]+/\w+/\w+/\d+.html$",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//h1[@class=\"newstitle\"]/text()", },
                        {"xpath": "//h1[@class=\"wztit\"]/text()", },
                    ],
                    "content": [
                        {"xpath": "//div[@class=\"wzcon j-fontContent clearfix\"]", },
                        {"xpath": "//div[@id=\"leftShow\"]", },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//div[@class=\"fl\"]/text()",
                            "regex": r"来源[: ：]\s*?(.*)",
                        },
                        {
                            "xpath": "//*[@id=\"wenzhang\"]/div[1]/table/tbody/tr[3]/td[1]/text()",
                        },
                    ],
                    "pubTime": [
                        {"xpath": "//div[@class=\"fl\"]/text()", "regex": r"(.*)点击数.*", },
                        {"xpath": "//*[@id=\"wenzhang\"]/div[1]/table/tbody/tr[2]/td[2]/text()", },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },
            # 淮南长安网
            {
                "platformName": "淮南长安网",
                # "sourceProvince": "安徽省",
                # "sourceCity": "",
                # "sourceCounty": "",
                # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
                "sourceLevel": 2,
                # 1：媒体类，2：政务类，3：商业类。
                "sourceClassify": 1,
                # 是否重点渠道。
                "sourceImportance": 1,
                # 是否主流媒体。
                "mainMedia": 1,
                # 起始地址。
                "start_url": "http://www.hnzzb.gov.cn/",
                "cookie": "SHIROJSESSIONID=3cef968f-394f-4b39-a911-af70007e9121",
                # 首页头条新闻
                "headline_news": ["//h2[@class=\"title\"]/a"],
                # 轮播信息
                "banner_news": ["//*[@id=\"myfocus01\"]/div[1]/ul/li/a"],
                # 轮播旁边新闻
                "banner_news_side": [
                    "//div[@class=\"fr ind_newsbox\"]/div[2]/ul/li/a"],
                # 导航信息
                "channel_info_xpath": ["//div[@class=\"container\"]/ul/li/a"],
                # 详情链接。
                "doc_links": [
                    r"http?://[\w\-\.]+/\w+/\w+/\d+.html$",
                    r"http?://[\w\-\.]+/\w+/\d+.html$"
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {"xpath": "//h1[@class=\"newstitle\"]/text()", },
                        {"xpath": "//div[@class=\"title\"]/text()", },
                    ],
                    "content": [
                        {"xpath": "//div[@class=\"wzcon j-fontContent\"]", },
                        {"xpath": "//div[@class=\"content_main\"]", },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//div[@class=\"wzbjxx\"]/text()",
                            "regex": r"来源[: ：]\s*?(.*)点击数.*",
                        },
                        {
                            "xpath": "//div[@class=\"source\"]/span[2]/text()",
                            "regex": r"来源[: ：]\s*?(.*)$",
                        },
                    ],
                    "pubTime": [
                        {"xpath": "//div[@class=\"wzbjxx\"]/text()", "regex": r"(.*)来源.*", },
                        {"xpath": "//div[@class=\"source\"]/span[1]/text()", "regex": r"时间[: ：](.*)", },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },
        ]
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
                    "platformType": 3,
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
