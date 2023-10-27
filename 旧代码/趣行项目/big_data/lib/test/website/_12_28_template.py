# -*- coding:utf-8 -*-
"""
# project: 未进行更新网站
# author: Neil
# date: 2020/12/28
# update: 2020/12/28
"""

a_list = [
    # 28
    # 中国铁路总公司
    {
        "platformName": "中国铁路总公司",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.china-railway.com.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//ul[@class=\"swiper_text\"]/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class=\"reports_lists\"]/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class=\"nav_menu clearfix\"]/li//a "],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\w+/\d+/t\d+_\d+\.html$",
            r"https?://[\w\-\.]+?/\w+\d{4,}/\w+/\d{4,}-\d{2,}/\d{2,}/\w+_\d+\.htm$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//strong[@class=\"title\"]/text()", },
                {"xpath": "//div[@class=\"article_title\"]/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@id=\"zoomCon\"]", },
                {"xpath": "//div[@class=\"TRS_Editor\"]", },
            ],
            "pubSource": [],
            "pubTime": [{"xpath": "//div[@class=\"source\"]/p/span[1]/text()", "regex": r"发布时间：(.*)", }, ],
            "channel": [],
            "authors": [],
            "summary": [],
        }
    },
    # 国务院新闻办
    {
        "platformName": "国务院新闻办",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.scio.gov.cn/index.htm",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class=\"tttp\"]//li/a"],
        # 轮播信息
        "banner_news": ["//div[@class=\"mabd2 mabd1\"]/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//li[@class=\"yao_wen\"]//li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"nav\"]/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\w+/\w+/\d+/\d+\.htm$",
            r"https?://[\w\-\.]+?/\w+/\w+/\d+/\d+/\w+/\d+/\d+\.htm$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"tc A_title\"]/text()", },

            ],
            "content": [
                {"xpath": "//div[@id=\"content\"]", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class=\"tc A_t1 f12 pr\"]/div[1]/text()",
                    "regex": r"来源：(.*)",
                },
            ],
            "pubTime": [],
            "channel": [],
            "authors": [],
            "summary": [],
        }
    },
    # 中国气象台
    {
        "platformName": "中国气象台",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.weather.com.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class=\"focusImg\"]/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"mainContent\"]//a | //div[@class=\"newsList\"]/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"nav_addr\"]/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\w+/\d+\.shtml$",
            r"https?://\w.[\w\-\.]+?/\d{4,}/\d{2,}/\d+\.shtml$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//p[@class=\"articleTittle\"]/text()", },

            ],
            "content": [
                {"xpath": "//div[@class=\"articleBody\"]", },
            ],
            "pubSource": [{"xpath": "//div[@class=\"articleTimeSizeleft\"]/span/a/text()", }, ],
            "pubTime": [{"xpath": "//div[@class=\"articleTimeSizeleft\"]/span[1]/text()", }, ],
            "channel": [],
            "authors": [],
            "summary": [],
        }
    },
    # 中国政府采购网
    {
        "platformName": "中国政府采购网",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.ccgp.gov.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//ul[@class=\"slides\"]/li/div[2]/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"txtnews\"]/div//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"v4incheadertop_nav\"]/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\d+/t\d+_\d+\.htm$",
            r"https?://[\w\-\.]+?/\w+/\w+/\d+/t\d+_\d+\.htm$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h2[@class=\"tc\"]/text()", },

            ],
            "content": [
                {"xpath": "//div[@class=\"vF_detail_content\"]", },
            ],
            "pubSource": [{"xpath": "//span[@id=\"sourceName\"]/text()", }, ],
            "pubTime": [{"xpath": "//span[@id=\"pubTime\"]/text()", }, ],
            "channel": [],
            "authors": [],
            "summary": [],
        }
    },
    # 国家质检总局
    {
        "platformName": "国家质检总局",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.samr.gov.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class=\"newbanner01\"]/a"],
        # 轮播信息
        "banner_news": ["//div[@class=\"box01\"]/div/div[1]//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"sama-box sama-box2\"]/div/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"navigation-v3\"]/ul/li/a | //div[@class=\"navigation-down\"]//ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\w+/\d{4,}-\d{2,}/\d{2,}/c_\d+\.htm$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"h-title\"]/text()", },

            ],
            "content": [
                {"xpath": "//div[@class=\"main-aticle\"]", },
            ],
            "pubSource": [{"xpath": "//span[@class=\"aticle-src\"]/text()", }, ],
            "pubTime": [{"xpath": "//span[@class=\"h-time\"]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 中国国家卫生健康委员会
    {
        "platformName": "中国国家卫生健康委员会",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.nhc.gov.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class=\"txt\"]/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class=\"inLists\"]/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class=\"intabnav fl\"]/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\w\d+/\d+/[A-z0-9]+\.shtml$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"tit\"]/text()", },

            ],
            "content": [
                {"xpath": "//div[@id=\"xw_box\"]", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class=\"mr\"]/text()",
                    "regex": r".*来源:(.*)",
                },

            ],
            "pubTime": [
                {
                    "xpath": "//div[@class=\"source\"]/span[1]/text()",
                    "regex": r".*发布时间：(.*)",
                },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中国生态环境部
    {
        "platformName": "中国生态环境部",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.mee.gov.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class=\"bd\"]/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"indexBXxgkANavBox\"]/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class=\"yaowenlunboUl\"]/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\w+/\d+/t\d+_\d+\.shtml$",
            r"https?://[\w\-\.]+?/\w+\d+/\w+/\w+\d+/\d+/t\d+_\d+\.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h2[@class=\"neiright_Title\"]/text()", },

            ],
            "content": [
                {"xpath": "//div[@class=\"neiright_JPZ_GK_CP\"]", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class=\"xqLyPc\"]/text()",
                    "regex": r".*来源：(.*)",
                },
            ],
            "pubTime": [{"xpath": "//span[@class=\"xqLyPc time\"]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 中国水利部
    {
        "platformName": "中国水利部",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.mwr.gov.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@id=\"area_tpxw\"]/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@id=\"demo_Two\"]//td/a | "
                             "//div[@class=\"js_qh_parent hp_news_right shadow bg_fff fl\"]/div//ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id=\"area_nav\"]/ul/li//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\w+/\d+/t\d+_\d+\.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id=\"slywxl2\"]/h1/text()", },

            ],
            "content": [
                {"xpath": "//div[@class=\"TRS_Editor\"]", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class=\"fl\"]/text()",
                    "regex": r".*来源：(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class=\"fl\"]/text()",
                    "regex": r"(.*)来源：.*",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 国家体育总局
    {
        "platformName": "国家体育总局",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.sport.gov.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@id=\"KSS_contentClone\"]/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"ml_con_one_r fr\"]/ul/li/a | //div[@id=\"con_zxa1_1\"]/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"nav center relative\"]//ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+\d+/\w+\d+/\w+\.html$",
            r"https?://[\w\-\.]+?/\w+\d+/\w+\d+/\w+\d+/\w+\.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"wz_title\"]/text()", },

            ],
            "content": [
                {"xpath": "//div[@class=\"wz_con\"]", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class=\"wz_info\"]/span[2]/text()",
                    "regex": r"来源：(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class=\"wz_info\"]/span[1]/text()",
                    "regex": r"发布时间：(.*)",
                },
            ],
            "authors": [
                {
                    "xpath": "//div[@class=\"wz_info\"]/span[3]/text()",
                    "regex": r"作者：(.*)",
                },
            ],
            "summary": [],
        }
    },
    # 国家机关事务管理局
    {
        "platformName": "国家机关事务管理局",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.ggj.gov.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//dt[@class=\"bd\"]/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class=\"txtbox a_width1\"]/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"menubox\"]/p/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\w+/\d+/t\d+_\d+\.htm$",
            r"https?://[\w\-\.]+?/\w+/\w+/\d{4,}-\d{2,}/\d{2,}/\w_\d+\.htm$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"h-title\"]/text()", },
                {"xpath": "//h1[@class=\"titlebox boxcenter\"]/text()", }

            ],
            "content": [
                {"xpath": "//div[@class=\"TRS_Editor\"]", },
                {"xpath": "//div[@class=\"main-aticle\"]", },

            ],
            "pubSource": [
                {"xpath": "//span[@class=\"aticle-src\"]/text()", },
                {
                    "xpath": "//dt[@class=\"fl\"]/span[4]/text()",
                    "regex": r"来源：(.*)",
                },
            ],
            "pubTime": [
                {"xpath": "//dt[@class=\"fl\"]/span[3]/text()", },
                {"xpath": "//span[@class=\"h-time\"]/text()", },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中国林业网
    {
        "platformName": "中国林业网",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.forestry.gov.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class=\"main-title\"]/a"],
        # 轮播信息
        "banner_news": ["//div[@class=\"floor-1 clearfix\"]//div[@id=\"index-pic\"]/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class=\"list-ul\"]/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"nav\"]/div//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\d+/\d+/\d+\.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//span[@id=\"forestry_title\"]/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"con\"]", },
            ],
            "pubSource": [
                {"xpath": "//span[@id=\"forestry_datasource\"]/text()", },
            ],
            "pubTime": [
                {"xpath": "//span[@class=\"date\"]/text()", },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 港澳办
    {
        "platformName": "港澳办",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.hmo.gov.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class=\"bd\"]/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"tabItemCon\"]//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"nav\"]/ul/li//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\w+/\d+/t\d+_\d+\.html$",
            r"https?://[\w\-\.]+?/\w+/\w+/\w+/\w+/\d+/t\d+_\d+\.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"pageHead\"]/h2/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"detailCon\"]/div[1]", },
            ],
            "pubSource": [
                {"xpath": "//div[@class=\"pageHead\"]/h3/span[2]/text()", },
            ],
            "pubTime": [
                {"xpath": "//div[@class=\"pageHead\"]/h3/span[1]/text()", },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中国民航局
    {
        "platformName": "中国民航局",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.caac.gov.cn/index.html",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//h3[@class=\"tit\"]/a"],
        # 轮播信息
        "banner_news": ["//div[@class=\"n_pic\"]/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@id=\"div001\"]/div/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"nav\"]/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\d+/t\d+_\d+\.html$",
            r"https?://[\w\-\.]+?/\w+/\w+/\d+/t\d+_\d+\.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"content_t\"]/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"TRS_Editor\"]", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@id=\"source\"]/text()",
                    "regex": r"来源：(.*)"
                },
            ],
            "pubTime": [
                {"xpath": "//span[@class=\"p_r10\"][2]/text()", },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中国社科院
    {
        "platformName": "中国社科院",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://cass.cssn.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class=\"toutiao\"]//a"],
        # 轮播信息
        "banner_news": ["//div[@id=\"hwslider\"]/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"home-tzgg\"]/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"menu-box\"]/dl//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+\d+/\w+/\d+/t\d+_\d+\.shtml$",
            r"https?://[\w\-\.]+?/\w+/\d+/t\d+_\d+\.shtml$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"ywXqMCenter\"]/h5/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"TRS_Editor\"]", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class=\"ywXqLy\"]/text()",
                    "regex": r"来源：(.*)",
                },
            ],
            "pubTime": [
                {"xpath": "//span[@class=\"ywXqTime\"]/text()", },
            ],
            "authors": [
                {
                    "xpath": "//span[@class=\"ywXqZz\"]/text()",
                    "regex": r"作者：(.*)",

                },
            ],
            "summary": [],
        }
    },
    # 国家地震局
    {
        "platformName": "国家地震局",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.cea.gov.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class=\"zyyw_list\"]/p/a"],
        # 轮播信息
        "banner_news": ["//div[@class=\"bd\"]/ul/li//p/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"portlet\"]//dd/a | //ul[@class=\"dzj_yw_list1 ztli\"]/li/a |"
                             " //ul[@class=\"dzj_yw_list\"]/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"sy2_inside\"]//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\d{4,}-\d{2,}/\d{2,}/\w+_\d+\.htm$",
            r"https?://[\w\-\.]+?/\w+/\w+/\d+/\d+/\w+\.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@id=\"title\"]/text()", },
                {"xpath": "//div[@class=\"article oneColumn pub_border\"]/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@id=\"news_content\"]", },
                {"xpath": "//div[@class=\"pages_content\"]", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class=\"font\"]/text()",
                    "regex": r"来源：(.*)"
                },
                {"xpath": "//span[@id=\"replace\"]/text()", },
            ],
            "pubTime": [
                {"xpath": "//div[@class=\"pages-date\"]/text()", },
                {
                    "xpath": "//span[@class=\"span1\"]/text()",
                    "regex": r"发布时间：(.*)"
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 国务院侨办
    {
        "platformName": "国务院侨办",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.gqb.gov.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class=\"banner_info\"]/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@id=\"myTabhd_qs_Content0\"]//div//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"qiaowu_daohang_text\"]/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\d+/\d+/\d+\.shtml$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"caijingt_wztop\"]/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@id=\"fontzoom\"]", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class=\"caijingt_wztop\"]/p/a/text()",
                    "regex": r"来源：(.*)"
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class=\"caijingt_wztop\"]/p/text()",
                    "regex": r"(.*)来源：.*"
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 国家信访局
    {
        "platformName": "国家信访局",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.gjxfj.gov.cn/gjxfj/index.htm",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class=\"part\"]/h1/a"],
        # 轮播信息
        "banner_news": ["//div[@class=\"swiper-wrapper\"]/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"tab-cont\"]/div/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@id=\"navUl\"]/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\d{4,}-\d{2,}/\d{2,}/\w+_\d+\.htm$",
            r"https?://[\w\-\.]+?/\d{4,}-\d{2,}/\d{2,}/\w+_\d+\.htm$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"article oneColumn pub_border\"]/h1/text()", },
                {"xpath": "//h3[@id=\"title_tex\"]/text()", },
            ],
            "content": [
                {"xpath": "//div[@id=\"BodyLabel\"]", },
                {"xpath": "//div[@class=\"pages_content\"]", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class=\"font\"]/text()",
                    "regex": r"来源：(.*)",
                },
                {
                    "xpath": "//h4[@id=\"time_tex\"]/text()",
                    "regex": r"来源：(.*)",
                },
            ],
            "pubTime": [
                {"xpath": "//div[@class=\"pages-date\"]/text()", },
                {
                    "xpath": "//h4[@id=\"time_tex\"]/text()",
                    "regex": r"日期：(.*)来源：.*",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易
    {
        "platformName": "网易",
        "sourceProvince": "北京",
        "sourceCity": "",
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
        "start_url": "https://www.163.com/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class=\"focus_body\"]//li//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"yaowen_news\"]//ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"bd\"]/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\d+/\d+/\d+/[A-Z0-9]+\.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id=\"epContentLeft\"]/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@id=\"endText\"]", },
            ],
            "pubTime": [
                {"xpath": "//div[@class=\"post_time_source\"]/text()", },
            ],
            "pubSource": [
                {"xpath": "//a[@id=\"ne_article_source\"]/text()", },
            ],

            "authors": [],
            "summary": [],
        }
    },
    # 中新网河北频道
    {
        "platformName": "中新网河北频道",
        "sourceProvince": "河北省",
        "sourceCity": "石家庄市",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.heb.chinanews.com/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class=\"topNews\"]/a"],
        # 轮播信息
        "banner_news": ["//div[@id=\"newsSlide\"]/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"newsList\"]/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"menu1\"]/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\d+\.shtml$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@id=\"tit\"]/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"article13hui15\"]", },
            ],
            "pubTime": [
                {"xpath": "//div[@class=\"left-t\"]/span[1]/text()", },
            ],
            "pubSource": [
                {"xpath": "//div[@class=\"left-t\"]/span[3]/text()", },
            ],

            "authors": [],
            "summary": [],
        }
    },
    # 人民网河北频道
    {
        "platformName": "人民网河北频道",
        "sourceProvince": "河北省",
        "sourceCity": "石家庄市",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://he.people.com.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class=\"title mt15 clear clearfix\"]/h1/a"],
        # 轮播信息
        "banner_news": ["//div[@id=\"focus_list\"]/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"news_box\"]//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"pd_nav w1000 white clear clearfix\"]/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w\d/\d{4,}/\d{4,}/\w\d+-\d+\.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"clearfix w1000_320 text_title\"]/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"fl text_con_left\"]", },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class=\"box01\"]/div/text()",
                    "regex": r"(.*)来源：.*",
                },
            ],
            "pubSource": [
                {"xpath": "//div[@class=\"box01\"]/div/a/text()", },
            ],

            "authors": [],
            "summary": [],
        }
    },

    # 29
    # 国务院参事室
    {
        "platformName": "国务院参事室",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.counsellor.gov.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class=\"swiper-wrapper\"]//p[@class=\"name\"]/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"tab_cont\"]/div//a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class=\"nav_list\"]/li//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\d{4,}-\d{2,}/\d{2,}/\w_\d+\.htm$",
            r"https?://[\w\-\.]+?/\w+/\d{4,}-\d{2,}/\d{2,}/\w_\d+\.htm$",

        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"h-title\"]/text()", },
                {"xpath": "//h2[@class=\"title\"]/text()", },
            ],
            "content": [
                {"xpath": "//div[@id=\"p-detail\"]", },
                {"xpath": "//div[@class=\"text\"]", },
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class=\"h-time\"]/text()",
                },
                {
                    "xpath": "//div[@class=\"time\"]/text()",
                },
            ],
            "pubSource": [
                {"xpath": "//div[@class=\"h-info\"]/span[2]/text()",
                 "regex": r"来源：(.*)"},
                {"xpath": "//div[@class=\"source\"]/text()",
                 "regex": r"来源：(.*)"},
            ],

            "authors": [
                {"xpath": "//div[@class=\"author\"]/text()",
                 "regex": r"作者：(.*)"}, ],
            "summary": [],
        }
    },
    # 法制网
    {
        "platformName": "法制网",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.legaldaily.com.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class=\"div1000\"]/a"],
        # 轮播信息
        "banner_news": ["//div[@class=\"bd\"]/ul/li/div[@class=\"title\"]/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"tt\"]/div/a | //ul[@class=\"imp-news\"]/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"nav20200928\"]/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+_\w+/\w+/\d{4,}-\d{2,}/\d{2,}/\w+_\d+\.htm$",
            r"https?://[\w\-\.]+?/\w+/\w+/\d{4,}-\d{2,}/\d{2,}/\w+_\d+\.htm#.*$",

        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id=\"CONTENT\"]/h1/text()", },
                {"xpath": "//dd[@class=\"dd640wz\"]/dl/dd[2]/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"ad-image-wrapper\"] | //div[@id=\"CONTENT-MAIN\"]", },
                {"xpath": "//dd[@class=\"dd640wz\"]/dl/dd[@id=\"CONTENT\"]", },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@id=\"CONTENT-INFO\"]/span[1]/text()",
                    "regex": r"发布时间：(.*)"
                },
                {
                    "xpath": "//dd[@class=\"f12 balck02 yh\"]/text()",
                    "regex": r"发布时间：(.*).*"
                },
            ],
            "pubSource": [
                {"xpath": "//div[@id=\"CONTENT-INFO\"]/span[2]/text()",
                 "regex": r"来源：(.*)"},

                {"xpath": "//dd[@class=\"f12 black02\"]/text()",
                 "regex": r"来源：(.*)"},
            ],

            "authors": [],
            "summary": [],
        }
    },
    # 中青在线
    {
        "platformName": "中青在线",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cyol.com/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class=\"yw-left\"]/dl//a"],
        # 轮播信息
        "banner_news": ["//div[@class=\"box\"]/div[@class=\"txt\"]/h3/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//dl[@id=\"ticker-1\"]/dd/a | //ul[@class=\"yw-list\"]/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class=\"navList1\"]/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\d{4,}-\d{2,}/\d{2,}/\w+_\d+\.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class=\"title\"]/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"content\"]", },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class=\"year\"]//text() | //div[@class=\"month\"]/text() |"
                             " //div[@class=\"oclock\"]/text()",
                },
                {
                    "xpath": "//dd[@class=\"f12 balck02 yh\"]/text()",
                    "regex": r"发布时间：(.*).*"
                },
            ],
            "pubSource": [
                {"xpath": "//div[@class=\"author\"]/text()",
                 "regex": r"来源：(.*)"},

            ],

            "authors": [
                {"xpath": "//div[@class=\"author\"]/text()",
                 "regex": r"作者：(.*)来源：.*"}, ],
            "summary": [],
        }
    },
    # 中国国家航天局
    {
        "platformName": "中国国家航天局",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cnsa.gov.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@id=\"KSS_content\"]/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"left fl\"]/a | //div[@class=\"right fr\"]/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"nav clearfix\"]/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w\d+/\w\d+/\w+\.htm",
            r"https?://[\w\-\.]+?/\w\d+/\w\d+/\w\d+/\w+\.htm"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"wrap1130\"]/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"conText\"]", },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class=\"information\"]/span[1]/text()",
                    "regex": r"发布日期：(.*)"
                },
            ],
            "pubSource": [

                {"xpath": "//div[@class=\"information\"]/span[2]/text()",
                 "regex": r"来源: (.*)"},

            ],

            "authors": [],
            "summary": [],
        }
    },
    # 自然资源部
    {
        "platformName": "自然资源部",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.mnr.gov.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class=\"new_right_top\"]/ul/li/a"],
        # 轮播信息
        "banner_news": ["//div[@class=\"tempWrap\"]/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"parBd\"]//ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"nav_nei clearfix\"]/ul/li//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\w+/\d+/\w\d+_\d+\.html$",
            r"https?://[\w\-\.]+?/\w+/\d{4,}-\d{2,}/\d{2,}/\w+_\d+\.htm$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h2[@id=\"doctitle\"]/text()", },
                {"xpath": "//div[@class=\"article oneColumn pub_border\"]/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"TRS_Editor\"]", },
                {"xpath": "//div[@id=\"UCAP-CONTENT\"]", },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class=\"fl clearfix ky_fx\"]/span[1]/text()",
                },
                {
                    "xpath": "//div[@class=\"pages-date\"]/text()",
                },
            ],
            "pubSource": [

                {"xpath": "//div[@class=\"fl clearfix ky_fx\"]/span[2]/text()",
                 "regex": r"来源：(.*)"},

                {"xpath": "//span[@class=\"font\"]/text()",
                 "regex": r"来源：(.*)"},

            ],

            "authors": [],
            "summary": [],
        }
    },
    # 国家行政学院
    {
        "platformName": "国家行政学院",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.naea.edu.cn/gjjyxzxy/index/index.html",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class=\"picbox\"]/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"sym-body clearfix\"]//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"listNav\"]/div[2]//li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\d+/\d+/\w+\.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"xl-tit\"]/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"xl-con\"]", },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class=\"xl-info\"]/text()",
                    "regex": r"发布时间：(.*).*浏览.*"
                },

            ],
            "pubSource": [],

            "authors": [],
            "summary": [],
        }
    },
    # 全国残联
    {
        "platformName": "全国残联",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cdpf.org.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@id=\"scrollimg\"]/dl/dd/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class=\"publist1\"]/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id=\"mainnav\"]//a | //ul[@id=\"main_subnav\"]/li/a"],
        # 详情链接。
        "doc_links": [

            r"https?://[\w\-\.]+?/\w+/\d+/\w\d+_\d+\.shtml$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h3[@id=\"content_h3\"]//text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"TRS_Editor\"]", },
            ],
            "pubTime": [
                {
                    "xpath": "//ul[@id=\"top_gj\"]/li[1]/text()",
                },

            ],
            "pubSource": [],
            "authors": [],
            "summary": [],
        }
    },
    # 国家邮政局
    {
        "platformName": "国家邮政局",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.spb.gov.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class=\"tp-box\"]//div[@class=\"bd\"]/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"dt-box\"]//div[@class=\"inBox\"]/div[1]//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"nav-box\"]/ul/li/h3/a"],
        # 详情链接。
        "doc_links": [

            r"https?://[\w\-\.]+?/\w+/\w+_\d+/\d+/\w\d+_\d+\.html$"
            r"https?://[\w\-\.]+?/\w+/\d{4,}-\d{2,}/\d{2,}/\w+_\d+\.htm$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"title1\"]/text()", },
                {"xpath": "//div[@class=\"article oneColumn pub_border\"]/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"content\"]", },
                {"xpath": "//div[@id=\"UCAP-CONTENT\"]", },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class=\"time\"]/a[1]/text()",
                },
                {
                    "xpath": "//div[@class=\"pages-date\"]/text()",
                },

            ],
            "pubSource": [
                {
                    "xpath": "//div[@class=\"time\"]/a[2]/text()",
                },
                {
                    "xpath": "//span[@class=\"font\"]/text()",
                    "regex": r"来源：(.*)"
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中国退役军人事务部
    {
        "platformName": "中国退役军人事务部",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.mva.gov.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class=\"container\"]/h2/a"],
        # 轮播信息
        "banner_news": ["//div[@class=\"txt\"]/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//h3[@class=\"subhot\"]//a | //div[@class=\"bd\"]/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class=\"nav-bar\"]/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\d{4,}-\d{2,}/\d{2,}/\w+_\d+\.htm$",
            r"https?://[\w\-\.]+?/\w+/\w+/\w+/\d+/\w\d+_\d+\.html$",
            r"https?://[\w\-\.]+?/\w+/\w+/\d+/\w\d+_\d+\.html$"

        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"details_page\"]/h2/p/text()", },

                {"xpath": "//div[@class=\"article oneColumn pub_border\"]/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@id=\"div_zhengwen\"]", },

                {"xpath": "//div[@id=\"UCAP-CONTENT\"]", },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class=\"article-info\"]/text()",
                    "regex": r"时间：(.*)来源.*"
                },
                {
                    "xpath": "//div[@class=\"pages-date\"]/text()",
                },

            ],
            "pubSource": [
                {
                    "xpath": "//div[@class=\"article-info\"]/text()",
                    "regex": r"来源：(.*)"
                },
                {
                    "xpath": "//span[@class=\"font\"]/text()",
                    "regex": r"来源：(.*)"
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中共中央文献研究室
    {
        "platformName": "中共中央文献研究室",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.dswxyjy.org.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class=\"topnews\"]/p//a"],
        # 轮播信息
        "banner_news": ["//div[@class=\"p2_left\"]//div[@class=\"swiper-wrapper\"]/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"p2_right more\"]/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"nav_li clearfix\"]/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w\d/\d{4,}/\d+/\w\d+-\d+\.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"text_title\"]/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"art_text\"]", },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class=\"ptime\"]/text()",
                    "regex": r"发布时间：(.*)来源.*"
                },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class=\"ptime\"]/a/text()",
                },
            ],
            "authors": [
                {
                    "xpath": "//div[@class=\"ptime\"]/text()",
                    "regex": r"作者：(.*)发布时间.*"
                },
            ],
            "summary": [],
        }
    },
    # 中国互联网联合辟谣平台
    {
        "platformName": "中国互联网联合辟谣平台",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.piyao.org.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class=\"jryw_right\"]/div[@class=\"tit\"]/a"],
        # 轮播信息
        "banner_news": ["//div[@class=\"jryw_left\"]//div[@class=\"swiper-wrapper\"]/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"jjrt_nr\"]//a | //div[@class=\"tit_small\"]/a | "
                             "//ul[@class=\"list_jryw\"]/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class=\"nav_list\"]/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\w+/\d{4,}-\d{2,}/\d+/\w_\d+\.htm$",
            r"https?://[\w\-\.]+?/\d{4,}-\d{2,}/\d+/\w_\d+\.htm$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"h-title\"]/text()", },
                {"xpath": "//div[@class=\"con_tit\"]/h2/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"main-aticle\"]", },
                {"xpath": "//div[@class=\"con_txt\"]", },
            ],
            "pubTime": [
                {"xpath": "//span[@class=\"h-time\"]/text()", },
                {"xpath": "//div[@class=\"con_tit\"]/p/span/text()", "regex": r"时间：(.*)", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class=\"aticle-src\"]/text()",
                },
                {
                    "xpath": "//div[@class=\"con_tit\"]/p/text()",
                    "regex": r"来源：(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中国社会科学院
    {
        "platformName": "中国社会科学院",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://cass.cssn.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class=\"toutiao\"]//a"],
        # 轮播信息
        "banner_news": ["//div[@id=\"hwslider\"]/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class=\"tzgg-tab-box\"]/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"menu\"]//dl/dt/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+\d+/\w+/\d+/\w\d+_\d+\.shtml$",
            r"https?://[\w\-\.]+?/\w+/\d+/\w\d+_\d+\.shtml$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"ywXqMCenter\"]/h5/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"TRS_Editor\"]", },
            ],
            "pubTime": [
                {"xpath": "//span[@class=\"ywXqTime\"]/text()", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class=\"ywXqLy\"]/text()",
                    "regex": r"来源：(.*)",

                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 国家医疗保障局
    {
        "platformName": "国家医疗保障局",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.nhsa.gov.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@id=\"slideBox\"]/div[@class=\"title\"]/ul/li/a"],
        # 轮播信息
        "banner_news": ["//div[@id=\"slideBox1\"]/div[@class=\"title\"]/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"sf-xz-r\"]/ul/li//a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class=\"clearfix\"]/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\d{4,}-\d{2,}/\d{2,}/\w+_\d+\.htm$",
            r"https?://[\w\-\.]+?/\w+/\d{4,}/\d+/\d+/\w+_\d+_\d+\.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"article oneColumn pub_border\"]/h1/text()", },
                {"xpath": "//div[@class=\"atricle-title\"]/text()", },
            ],
            "content": [
                {"xpath": "//div[@id=\"UCAP-CONTENT\"]", },
                {"xpath": "//div[@id=\"zoom\"]", },
            ],
            "pubTime": [
                {"xpath": "//div[@class=\"pages-date\"]/text()", },
                {"xpath": "//span[@class=\"wzy-rq\"]/text()", "regex": r"日期：(.*)", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class=\"font\"]/text()",
                    "regex": r"来源：(.*)",

                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 国家移民管理局
    {
        "platformName": "国家移民管理局",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.nia.gov.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class=\"toutiao\"]//p/a"],
        # 轮播信息
        "banner_news": ["//div[@class=\"topnews\"]//div[@class=\"swiper-wrapper\"]/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@id=\"con_newBtn_1\"]//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"nav ctop3a\"]//li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\d{4,}-\d{2,}/\d+/\w+_\d+\.htm$",
            r"https?://[\w\-\.]+?/\w\d+/\w\d+/\w+\.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"article oneColumn pub_border\"]/h1/text()", },
                {"xpath": "//p[@class=\"sv_texth1\"]/text()", },
            ],
            "content": [
                {"xpath": "//div[@id=\"UCAP-CONTENT\"]", },
                {"xpath": "//li[@id=\"content\"]", },
            ],
            "pubTime": [
                {"xpath": "//div[@class=\"pages-date\"]/text()", },
                {"xpath": "//span[@class=\"zuo1_day\"]/text()", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class=\"font\"]/text()",
                    "regex": r"来源：(.*)",
                },
                {
                    "xpath": "//span[@class=\"zuo1_laiyuan\"]/text()",
                    "regex": r"来源：(.*)",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 国家核安全局
    {
        "platformName": "国家核安全局",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://nnsa.mee.gov.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class=\"bd\"]/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"indexBXxgkANavBox\"]/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class=\"yaowenlunboUl\"]/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\d+/\w\d+_\d+\.html$",
            r"https?://[\w\-\.]+?/\w+/\w+/\d+/\w\d+_\d+\.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h2[@class=\"neiright_Title\"]/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"TRS_Editor\"]", },
            ],
            "pubTime": [
                {"xpath": "//span[@class=\"bgtTimeSpan\"]/text()", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class=\"xqLyPc\"]/text()",
                    "regex": r"来源：(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中国银保监会
    {
        "platformName": "中国银保监会",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cbirc.gov.cn/cn/view/pages/index/index.html",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class=\"jgdt-brief-title\"]/a"],
        # 轮播信息
        "banner_news": ["//div[@class=\"bd\"]/div/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"col-lg-6\"]//div[@class=\"panel active\"]/div/span/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"nav ng-scope\"]/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"http://www.cbirc.gov.cn/cn/view/pages/ItemDetail.html.*"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"wenzhang-title ng-binding\"]/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"Section0\"]", },
            ],
            "pubTime": [
                {"xpath": "//div[@class=\"col-lg-6 pages-date\"]/span[@class=\"ng-binding\"]/text()",
                 "regex": r"发布时间：(.*)", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class=\"col-lg-6 pages-date\"]/span[@class=\"pages-date-laiyuan ng-binding\"]"
                             "/text()",
                    "regex": r"来源：(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 应急管理部消防救援局
    {
        "platformName": "应急管理部消防救援局",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.119.gov.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class=\"tong1_Con_top\"]/a"],
        # 轮播信息
        "banner_news": ["//ul[@class=\"focus_list\"]/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"firstCon-r\"]/div/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"wrapNav\"]//div/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/[A-z0-9]+$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"t-container-title\"]/h3/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"b-container\"]", },
            ],
            "pubTime": [
                {"xpath": "//span[@class=\"time\"]/text", }
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class=\"source\"]/text",
                    "regex": r"来源：(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 国家天文台
    {
        "platformName": "国家天文台",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.bao.ac.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class=\"carousel-inner\"]/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"col-md-4 column-topnews-R\"]/ul//a | "
                             "//ul[@class=\"col-md-8 col-sm-8 hidden-xs\"]/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class=\"nav navbar-nav\"]/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\w+/\d+/\w\d+_\d+\.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h2[@class=\"pt15\"]/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"TRS_Editor\"]", },
            ],
            "pubTime": [
                {"xpath": "//div[@class=\"temp02-info-article\"]/span[1]/text()", }
            ],
            "pubSource": [],
            "authors": [],
            "summary": [],
        }
    },
    # 国家档案局
    {
        "platformName": "国家档案局",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.saac.gov.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class=\"sytpxw fl\"]//div[@class=\"swiper-wrapper\"]/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"yw_lmcon\"]/div/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"nav\"]/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w+/\w+/\d+/[a-z0-9]+\.shtml$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"title\"]/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"pages_content\"]", },
            ],
            "pubTime": [
                {"xpath": "//span[@class=\"font\"][1]/text()", }
            ],
            "pubSource": [],
            "authors": [],
            "summary": [],
        }
    },
    # 中国福彩网
    {
        "platformName": "中国福彩网",
        "sourceProvince": "北京",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cwl.gov.cn/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class=\"touTiao\"]/a"],
        # 轮播信息
        "banner_news": ["//div[@class=\"slideShow\"]//div[@class=\"hdwk\"]/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=\"touxiaoC\"]/span/a | //div[@class=\"sqN\"]/div/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"containerHome\"]/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?/\w/\d{4,}-\d{2,}-\d{2,}/\d+\.shtml$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class=\"col-lg-8 col-md-8 col-sm-8 col-xs-12 text_content\"]/h4/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"article col-lg-12 col-md-12 col-sm-12 col-xs-12\"]", },
            ],
            "pubTime": [
                {"xpath": "//small[@class=\"sj-zh\"]/text()", }
            ],
            "pubSource": [
                {"xpath": "//div[@class=\"col-lg-8 col-md-8 col-sm-8 col-xs-12 text_content\"]/small[1]/span/text()", }
            ],
            "authors": [],
            "summary": [],
        }
    },

]
