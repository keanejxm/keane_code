# -*- coding:utf-8 -*-
"""
上传网站采集模板。
# author: Trico
# date: 2020.1.13
# update: 2020.1.13
"""

import os
import json
import time
import gzip
import requests
import traceback


def row():
    """
    返回数据体的最新一条。
    :return:
    """

    return [
        {
            "platformName": "澎湃新闻",
            "sourceProvince": "上海市",
            "sourceCity": "上海市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "https://www.thepaper.cn/",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.thepaper\.cn/channel_\d+$",
                                r"https?://www\.thepaper\.cn/list_\d+$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [r"https?://www\.thepaper\.cn/asktopic_detail_\d+$", ],
                            "target": [r"https?://www\.thepaper\.cn/newsDetail_forward_\d+$", ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//h1[@class='news_title']/text()", }, ],
                        "content": [{"xpath": "//div[@class='news_txt']", }, ],
                        "pubSource": [
                            {
                                "describe": "https://www.thepaper.cn/newsDetail_forward_5504339",
                                "xpath": "//div[@class='news_about']/p/span/text()",
                                "regex": r"\s*?来源：(\w+)$",
                            },
                            {
                                "describe": "https://www.thepaper.cn/newsDetail_forward_5504451",
                                "xpath": "//div[@class='news_about']/p[1]/text()",
                                "regex": r"[^/]*?/(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//div[@class='news_about']/p[2]/text()", }, ],
                        "channel": [{"xpath": "//div[@class='news_path']/a[2]/text()", }, ],
                        "authors": [{
                            "xpath": "//div[@class='news_about']/p[1]/text()",
                            "regex": r"澎湃新闻记者 (\w+)+?",
                        }, ],
                    }
                }
            ]
        },
        {
            "platformName": "光明网",
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
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.gmw.cn/",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+?\.gmw\.cn/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [r"https?://[\w\-\.]+?\.gmw.cn/\d{4,}-\d{2}/\d{2}/content_\d+\.htm$", ],
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//h1[@class='u-title']/text()", }, ],
                        "content": [{"xpath": "//div[@class='u-mainText']", }, ],
                        "pubSource": [
                            {
                                "describe": "http://politics.gmw.cn/2020-01/13/content_33475863.htm",
                                "xpath": "//span[@class='m-con-source']/a/text()",
                            }
                        ],
                        "pubTime": [{"xpath": "//span[@class='m-con-time']/text()", }, ],
                        "channel": [{"xpath": "//div[@class='g-crumbs']/a[3]/text()", }, ],
                        "authors": [],
                    }
                }
            ]
        },
        {
            "platformName": "环球网",
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
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "https://www.huanqiu.com/",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+?\.huanqiu\.com/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [r"https?://[\w\-\.]+?\.huanqiu\.com/article/\w+$", ],
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//div[@class='t-container-title']/h3/text()", }, ],
                        "content": [{"xpath": "//article//p", }, ],
                        "pubSource": [
                            {
                                "describe": "https://opinion.huanqiu.com/article/9CaKrnKoP8w",
                                "xpath": "//span[@class='source']/span/text()",
                            }
                        ],
                        "pubTime": [{"xpath": "//p[@class='time']/text()", }, ],
                        "channel": [{"xpath": "//div[@class='nav-section-submenu']/a[1]/text()", }, ],
                        "authors": [
                            {
                                "xpath": "//span[@class='author']/span/text()",
                                "regex": r"作者：(\w+)+?",
                            }
                        ],
                    }
                }
            ]
        },
        {
            "platformName": "界面新闻",
            "sourceProvince": "上海市",
            "sourceCity": "上海市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {
                "proxy": 1,
            },
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "https://www.jiemian.com/",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www.jiemian.com/lists/\d+.html$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [r"https?://www\.jiemian.com/article/\d+.html$", ],
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//div[@class='article-header']/h1/text()", }, ],
                        "content": [{"xpath": "//div[@class='article-main']/div[not(@id='ad_content')]", }, ],
                        "pubSource": [
                            {
                                "describe": "https://www.jiemian.com/article/3850351.html",
                                "xpath": "//div[@class='article-info']//*[contains(text(), '来源：')]/text()",
                                "regex": r"\s*?来源：(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//div[@class='article-info']/p/span[2]/text()", }, ],
                        "channel": [],
                        "authors": [{"xpath": "//div[@class='article-info']//span[@class='author']/a/text()", }, ],
                        "summary": [{"xpath": "//div[@class='article-header']/p/text()", }, ],
                    }
                }
            ]
        },
        {
            "platformName": "新华网",
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
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.xinhuanet.com/",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.xinhuanet\.com/\w+/index\.htm$",
                                r"https?://www\.xinhuanet\.com/\w+/\w+\.htm$",
                                r"https?://www\.xinhuanet\.com/\w+/$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.xinhuanet\.com/\w+/\d{4,}-\d{2}/\d{2}/c_\d+\.htm$",
                            ],
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//div[@class='h-title']/text()", },
                            {"xpath": "//h1[@id='title']/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@id='p-detail']/*[not(@class='tadd') "
                                      "and not(@class='p-tags') and not(@class='zan-wap')]", },
                            {"xpath": "//div[@class='article']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://www.xinhuanet.com/renshi/2020-01/07/c_1125432025.htm",
                                "xpath": "//div[@class='h-info']/span[2][contains(text(), '来源：')]/text()",
                                "regex": r"\s*?来源：\s*?(\w+)$",
                            },
                            {
                                "describe": "http://www.xinhuanet.com/xhsld/2019-11/18/c_1125243700.htm",
                                "xpath": "//em[@id='source']/text()",
                            }
                        ],
                        "pubTime": [
                            {"xpath": "//span[@class='h-time']/text()", },
                            {"xpath": "//span[@class='time']/text()", },
                        ],
                        "channel": [],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "华尔街见闻",
            "sourceProvince": "上海市",
            "sourceCity": "上海市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 0,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 3,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.myzaker.com/",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.myzaker\.com/channel/\d+$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.myzaker\.com/article/\w+/$",
                            ],
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//h1[@class='article-title']/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@id='content']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://www.myzaker.com/article/5e1d07198e9f097af57a2c01/",
                                "xpath": "//a[@class='article-auther']/text()",
                            }
                        ],
                        "pubTime": [
                            {"xpath": "//span[@class='time']/text()", },
                        ],
                        "channel": [
                            {"xpath": "//div[@class='breadcrumb']/a[2]/@title"},
                        ],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
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
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.people.com.cn/",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.people\.com\.cn/$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"http://[\w\-\.]+\.people\.com\.cn/n1/\d{4,}/\d{4}/c\d+-\d+\.html$",
                            ],
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//div[@class='clearfix w1000_320 text_title']/h1/text()", },
                            {"xpath": "//div[@class='title']/h1/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@id='rwb_zw']", },
                            {"xpath": "//div[@id='picG'] | //div[@class='content clear clearfix']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://tw.people.com.cn/n1/2020/0113/c14657-31545303.html",
                                "xpath": "//div[@class='box01']/div[@class='fl']/a/text()",
                            },
                            {
                                "describe": "http://pic.people.com.cn/n1/2020/0113/c426981-31546571.html",
                                "xpath": "//div[@class='page_c' and @style]/a/text()",
                            }
                        ],
                        "pubTime": [
                            {"xpath": "//div[@class='box01']/div[@class='fl']/text()", },
                            {"xpath": "//div[@class='page_c' and @style]/text()[2]", },
                        ],
                        "channel": [
                            {"xpath": "//span[@id='rwb_navpath']/a[@class='clink'][2]/text()"},
                            {"xpath": "//div[@class='fl']/a[@class='clink'][2]/text()"},
                        ],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "云南网",
            "sourceProvince": "云南省",
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
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.yunnan.cn/",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.yunnan\.cn/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"http://[\w\-\.]+\.yunnan\.cn/system/\d{4,}/\d{2}/\d{2}/\d+.shtml$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//span[@id='layer213']/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@id='layer216']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://news.yunnan.cn/system/2020/01/14/030568196.shtml",
                                "xpath": "//span[@class='xt2 yh fl']/span[2]/text()",
                            },
                        ],
                        "pubTime": [
                            {"xpath": "//span[@class='xt2 yh fl']/span[1]/text()", },
                        ],
                        "channel": [
                            {"xpath": "//span[@class='cms_block_span']/a[2]/text()"},
                        ],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "中国网",
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
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.china.com.cn/",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.china\.com\.cn/?$",
                                r"https?://[\w\-\.]+\.china\.com\.cn/\w+/node_\d+\.htm$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.china\.com\.cn/\d{4,}-\d{2}/\d{2}/content_\d+\.htm$",
                                r"https?://[\w\-\.]+\.china\.com\.cn/\w+/detail\d_\d{4,}_\d{2}/\d{2}/\d+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//h1[@class='articleTitle']/text()", },
                            {"xpath": "//h1[@class='artTitle']/text()", },
                            {"xpath": "//h1[contains(@class, 'artiTitle')]/text()", },
                            {"xpath": "//div[@id='menucontainer0_10']/div/dl/dt/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@id='articleBody']", },
                            {"xpath": "//div[@id='artbody']", },
                            {"xpath": "//div[@id='artiContent']", },
                            {"xpath": "//div[@id='menucontainer0_10']/div/p", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://guoqing.china.com.cn/2020-01/14/content_75611917.htm",
                                "xpath": "//span[@id='source_baidu']//text()",
                                "regex": r"\s*?来源：\s*?(\w+)$",
                            },
                            {
                                "describe": "http://sports.china.com.cn/zuqiu/detail2_2020_01/14/1675042.html",
                                "xpath": "//div[@id='menucontainer0_10']/div/dl/dd/span/text()",
                                "regex": r"\s*?来源：\s*?(\w+)$",
                            },
                        ],
                        "pubTime": [
                            {"xpath": "//span[@id='pubtime_baidu']/text()", },
                            {"xpath": "//div[@id='menucontainer0_10']/div/dl/dd/text()", },
                        ],
                        "channel": [],
                        "authors": [
                            {
                                "xpath": "//span[@id='author_baidu']/text()",
                                "regex": r"\s*?作者：(\w+)$",
                            }
                        ],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "台海网",
            "sourceProvince": "福建省",
            "sourceCity": "厦门市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.taihainet.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.taihainet\.com/?$",
                                r"https?://www\.taihainet\.com/\w+/?$",
                                r"https?://www\.taihainet\.com/\w+/\w+/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.taihainet\.com/(\w+/){2,3}\d{4,}-\d{2}-\d{2}/\d+.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//hgroup[@class='wrapper']/h1/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@class='article-content']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://guoqing.china.com.cn/2020-01/14/content_75611917.htm",
                                "xpath": "//span[@class='source_baidu']//text()",
                            }
                        ],
                        "pubTime": [
                            {"xpath": "//time/text()", },
                        ],
                        "channel": [
                            {"xpath": "//div[@class='list-path wrapper ovv']/a[2]/text()", }
                        ],
                        "authors": [
                            {"xpath": "//span[@class='editors']//text()", }
                        ],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "海外网",
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
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.haiwainet.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.haiwainet\.cn/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.haiwainet\.cn/n/\d{4,}/\d{4}/c\d+-\d+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//h1[@class='show_wholetitle']/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@class='contentMain']/p", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://opinion.haiwainet.cn/n/2017/0607/c353596-30954815.html",
                                "xpath": "//div[@class='contentExtra']/span[contains(text(), '来源：')]//text()",
                                "regex": r"\s*?来源：\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [
                            {"xpath": "//div[@class='contentExtra']/span[@class='first']/text()", },
                        ],
                        "channel": [
                            {"xpath": "//div[@class='fl'][2]/a[1]/text()", }
                        ],
                        "authors": [],
                        "summary": [
                            {
                                "describe": "http://opinion.haiwainet.cn/n/2017/0607/c353596-30954815.html",
                                "xpath": "//div[@class='summary']/text()",
                                "regex": r"\s*?摘要：\s*?(\w+)$",
                            }
                        ],
                    }
                }
            ]
        },
        {
            "platformName": "猎云网",
            "sourceProvince": "北京市",
            "sourceCity": "北京市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 0,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 3,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "https://www.lieyunwang.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.lieyunwang\.com/archives/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.lieyunwang\.com/archives/\d+$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//h1[@class='lyw-article-title']/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@class='main-text']/*[last()]/preceding-sibling::*", },
                        ],
                        "pubSource": [],
                        "pubTime": [
                            {"xpath": "//span[@class='time']/text()", },
                        ],
                        "channel": [],
                        "authors": [
                            {"xpath": "//div[@class='author-info']/"
                                      "a[@data-author and contains(@class, 'author-name')]/text()", },
                        ],
                        "summary": [
                            {
                                "describe": "https://www.lieyunwang.com/archives/462608",
                                "xpath": "//div[contains(@class, 'article-digest mb20')]/text()",
                            }
                        ],
                    }
                }
            ]
        },
        {
            "platformName": "中新网",
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
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.chinanews.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.chinanews\.com/\w+/?$",
                                r"https?://www\.chinanews\.com/scroll-news/news1\.html",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.chinanews\.com/\w+/\d{4,}/\d{2}-\d{2}/\d+\.shtml$",
                                r"https?://[\w\-\.]+\.chinanews\.com/\w+/\d+.shtml$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//div[@class='content']/h1[1]/text()", },
                            {"xpath": "//h1[@id='tit']/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@class='left_zw']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://www.chinanews.com/gn/2020/01-16/9061311.shtml",
                                "xpath": "//div[@class='left-time']/div[@class='left-t']/a[@class='source']/text()",
                            },
                            {
                                "describe": "http://www.heb.chinanews.com/zxjzkhb/20200113404024.shtml",
                                "xpath": "//div[@class='left-time']/div[@class='left-t']/"
                                         "span[contains(text(), '来源：')]/text()",
                                "regex": r"\s*?来源：\s*?(\w+)$",
                            },
                        ],
                        "pubTime": [
                            {"xpath": "//div[@class='left-time']/div[@class='left-t']/text()[1]", },
                            {"xpath": "//div[@class='left-time']/div[@class='left-t']/span[1]/text()", },
                        ],
                        "channel": [
                            {"xpath": "//div[@id='nav_div']/div[@id='nav']/a[2]/text()", },
                        ],
                        "authors": [
                            {"xpath": "//div[@class='author-info']/"
                                      "a[@data-author and contains(@class, 'author-name')]/text()", },
                        ],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "央视网",
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
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.cctv.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.cctv\.com/?(index.shtml)?$",
                                r"https?://[\w\-\.]+\.cctv\.com/\w+/?(index.shtml)?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [
                                r"https?://v\.cctv\.com/\d{4,}/\d{2}/\d{2}/\w+\.shtml",
                                r"https?://tv\.cctv\.com/\d{4,}/\d{2}/\d{2}/\w+\.shtml",
                            ],
                            "target": [
                                r"https?://[\w\-\.]+\.cctv\.com/\d{4,}/\d{2}/\d{2}/\w+\.shtml$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//div[@id='title_area']/h1/text()", },
                            {"xpath": "//div[@class='cnt_bd']/h1/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@class='text_area']", },
                            {"xpath": "//div[@class='cnt_bd']/p", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://news.cctv.com/2020/01/14/ARTIyv150b2we1eCdQ7b0gGY200114.shtml",
                                "xpath": "//div[@class='info']/text()[1]",
                            },
                            {
                                "describe": "http://news.cctv.com/2020/01/16/ARTIFmhAbm11R99bhx579rE2200116.shtml",
                                "xpath": "//span[@class='info']/i/a[1]/text()",
                            },
                            {
                                "describe": "http://jingji.cctv.com/2020/01/14/ARTImIRGQeFBrkz0KsyBrkNb200114.shtml",
                                "xpath": "//span[@class='info']/i//text()",
                                "regex": r"\s*?来源：\s*?(\w+)\s?",
                            },
                        ],
                        "pubTime": [
                            {"xpath": "//span[@class='info']/i/text()", },
                            {"xpath": "//div[@class='info']/span/text()", },
                            {"xpath": "//div[@class='info']/text()", },
                        ],
                        "channel": [
                            {"xpath": "//span[@class='info']/em/a/text()", },
                        ],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "东莞时间网",
            "sourceProvince": "广东省",
            "sourceCity": "东莞市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 3,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.timedg.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [
                                r"https?://[\w\-\.]+\.timedg\.com/previewp"
                                r"https?://[\w\-\.]+\.timedg\.com/prep"
                            ],
                            "target": [
                                r"https?://[\w\-\.]+\.timedg\.com/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.timedg\.com/\d{4,}-\d{2}/\d{2}/\d+\.shtml",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//div[@id='content']/h1/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@class='mainContent article-content']", },
                            {"xpath": "//div[@class='mainContent video-content']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://news.timedg.com/2020-01/15/21006362.shtml",
                                "xpath": "//span[@id='source_baidu']/text()",
                                "regex": r"\s*?来源：\s*?(\w+)",
                            },
                        ],
                        "pubTime": [
                            {"xpath": "//span[@id='pubtime_baidu']/text()", },
                        ],
                        "channel": [
                            {"xpath": "//div[@class='breadCrumbs']/a[1]/text()", },
                        ],
                        "authors": [
                            {
                                "describe": "http://www.timedg.com/2020-01/08/20998952.shtml",
                                "xpath": "//span[@id='author_baidu']/text()",
                                "regex": r"\s*?记者：\s*?(\w+)",
                            },
                        ],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "参考消息",
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
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.cankaoxiaoxi.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.cankaoxiaoxi\.com/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.cankaoxiaoxi\.com/\d{4,}/\d{4}/\d+\.shtml$",
                                r"https?://[\w\-\.]+\.cankaoxiaoxi\.com/\w+/\d{4,}/\d{4}/\d+\.shtml$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//h1[@class='articleHead']/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@class='articleText']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://ihl.cankaoxiaoxi.com/2020/0110/2399828.shtml",
                                "xpath": "//span[@id='source_baidu']/text()",
                                "regex": r"\s*?来源：\s*?(\w+)$",
                            },
                        ],
                        "pubTime": [
                            {"xpath": "//span[@id='pubtime_baidu']/text()", },
                        ],
                        "channel": [
                            {"xpath": "//div[@class='indexList']/a[2]/text()", },
                        ],
                        "authors": [
                            {
                                "describe": "http://ihl.cankaoxiaoxi.com/2020/0110/2399828.shtml",
                                "xpath": "//span[@id='author_baidu']/text()",
                                "regex": r"\s*?作者：\s*?(\w+)",
                            },
                        ],
                        "summary": [
                            {
                                "describe": "http://ihl.cankaoxiaoxi.com/2020/0110/2399828.shtml",
                                "xpath": "//div[@class='articleAbs']/span/text()",
                                "regex": r"\s*?核心提示：\s*?([^\s]+)",
                            },
                        ],
                    }
                }
            ]
        },
        {
            "platformName": "爱范儿",
            "sourceProvince": "广东省",
            "sourceCity": "广州市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 0,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 3,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "https://www.ifanr.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.ifanr\.com/category/[%\w]+$",
                                r"https?://www\.ifanr\.com/video/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.ifanr\.com/\d+",
                                r"https?://www\.ifanr\.com/video/\d+$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//h1[@class='c-single-normal__title']/text()", },
                        ],
                        "content": [
                            {"xpath": "//article", },
                        ],
                        "pubSource": [],
                        "pubTime": [
                            {
                                "xpath": "//p[@class='c-article-header-meta__time']/@data-timestamp",
                                "just_target": True,
                            },
                        ],
                        "channel": [
                            {"xpath": "//p[@class='c-article-header-meta__category']/text()", },
                        ],
                        "authors": [
                            {
                                "describe": "https://www.ifanr.com/1292861",
                                "xpath": "//p[@class='c-card-author__name']/text()",
                            },
                        ],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "央广网",
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
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.cnr.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.cnr\.cn/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.cnr\.cn/[\w/]+/\d{4,}\d{4}/t\d{4,}\d{4}_\d+\.shtml$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//div[@class='article-header']/h1/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@class='article-body']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://finance.cnr.cn/gundong/20200116/t20200116_524940252.shtml",
                                "xpath": "//div[@class='source']/span[contains(text(), '来源：')]/text()",
                                "regex": r"\s*?来源：\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//div[@class='source']/span[1]/text()", }, ],
                        "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "东南网",
            "sourceProvince": "福建省",
            "sourceCity": "福州市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.fjsen.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.fjsen\.com/?(\w+\.htm)?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.fjsen\.com/\d{4,}-\d{2}/\d{2}/content_\d+\.htm$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//div[@class='cont_head']/h1/text()", },
                            {"xpath": "//div[@class='biaoti']/text()", },
                        ],
                        "content": [
                            {"xpath": "//td[@id='new_message_id']", },
                            {"xpath": "//div[@id='zoom']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://xm.fjsen.com/2020-01/16/content_30134589.htm",
                                "xpath": "//span[@id='source_baidu']/text()",
                                "regex": r"\s*?来源：\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//span[@id='pubtime_baidu']/text()", }, ],
                        "channel": [{"xpath": "//a[@class='daohang'][1]/text()", }, ],
                        "authors": [
                            {
                                "xpath": "//span[@id='author_baidu']/text()",
                                "regex": r"\s*?作者：\s*?(\w+)$",
                            },
                        ],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "闽南网",
            "sourceProvince": "福建省",
            "sourceCity": "泉州市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.mnw.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.mnw\.cn/?(\w+)?/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.mnw\.cn/[\w/]+/\d+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//div[@class='l']/h1/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@class='icontent']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://www.mnw.cn/quanzhou/news/2242018.html",
                                "xpath": "//div[@class='il']/span[contains(text(), '来源:')]/text()",
                                "regex": r"\s*?来源:\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//div[@class='il']/span[2]/text()", }, ],
                        "channel": [{"xpath": "//div[@class='p']/a[2]/text()", }, ],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "四川在线",
            "sourceProvince": "四川省",
            "sourceCity": "成都市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "https://www.scol.com.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.scol\.com\.cn/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.scol\.com\.cn/\w+/\d{6,}/\d+.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//span[@class='w_title']/h1/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@class='con_text']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "https://sichuan.scol.com.cn/ggxw/201912/57407665.html",
                                "xpath": "//span[@class='w_source']//text()",
                                "regex": r"\s*?来源：\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//span[@class='w_pubtime']/text()", }, ],
                        "channel": [{"xpath": "//li[@class='nav']/a[1]/text()", }, ],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "深圳新闻网",
            "sourceProvince": "广东省",
            "sourceCity": "深圳市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 3,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.sznews.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.sznews\.com/?(node_\d+\.htm)?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.sznews\.com/[\w/]*?content/\d{4,}-\d{2}/\d{2}/content_\d+\.htm$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//h1[@class='h1-news']/text()", },
                            {"xpath": "//h1[@class='con_title']/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[contains(@class, 'article-content')]/*[not(@id='qrcodeWrap')]", },
                            {"xpath": "//div[@id='con_arc_content']/"
                                      "*[not(@id='qrcodeWrap') and not(@class='pages')]", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://www.sznews.com/news/content/2020-01/17/content_22784754.htm",
                                "xpath": "//span[@class='ml10']/text()",
                                "regex": r"\s*?来源：\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [
                            {"xpath": "//div[@class='fs18 share-date l']/text()", },
                            {"xpath": "//div[@class='fs18 r share-date']/text()", },
                            {"xpath": "//div[@class='bigPhoto-date yahei fs18 r']/text()", },
                        ],
                        "channel": [
                            {"xpath": "//div[@class='crumbs yahei']/a[2]/text()", },
                            {"xpath": "//div[@class='crumbs cf']/a[2]/text()", },
                        ],
                        "authors": [],
                        "summary": [{"xpath": "//h2[@class='article-title']/text()", }, ],
                    }
                }
            ]
        },
        {
            "platformName": "i黑马网",
            "sourceProvince": "北京市",
            "sourceCity": "北京市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 0,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 3,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.iheima.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.iheima\.com/scope/\d+$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.iheima\.com/article-\d+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//div[@class='main-content']/div[@class='title']/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@class='main-content']/p", },
                        ],
                        "pubSource": [
                            {"xpath": "//div[@class='fl ad']/text()", },
                        ],
                        "pubTime": [
                            {"xpath": "//div[@class='author']/span[@class='time fl']/text()", },
                        ],
                        "channel": [
                            {"xpath": "//div[@class='author']/span[@class='time fr']/text()", },
                        ],
                        "authors": [],
                        "summary": [{"xpath": "//div[@class='outline']//text()", }, ],
                    }
                }
            ]
        },
        {
            "platformName": "四川新闻网",
            "sourceProvince": "四川省",
            "sourceCity": "成都市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.newssc.org/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.newssc\.org/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.newssc\.org/system/\d{8,}/\d+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//div[@class='col-xs-12 left']/h1/text()", },
                            {"xpath": "//div[@class='bsbt']//text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@class='content']", },
                            {"xpath": "//div[@class='txt_zw #000']//td[@class='#000']/p", },
                            {"xpath": "//td[@class='qzbs']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://local.newssc.org/system/20200116/002836359.htm",
                                "xpath": "//span[@id='source_baidu ']//text()",
                                "regex": r"\s*?来源：\s*?(\w+)$",
                            },
                            {
                                "describe": "http://local.newssc.org/system/20200116/002836359.htm",
                                "xpath": "//span[@id='source_baidu']/a/text()",
                            },
                        ],
                        "pubTime": [
                            {"xpath": "//span[@id='pubtime_baidu ']/text()", },
                            {"xpath": "//span[@id='pubtime_baidu']/text()", },
                        ],
                        "channel": [
                            {"xpath": "//div[@class and contains(text(), '您当前的位置')]/a[1]/text()", },
                            {"xpath": "//span[@class='txt_12px' and contains(text(), '您当前的位置')]/a[1]/text()", },
                        ],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "海南在线",
            "sourceProvince": "海南省",
            "sourceCity": "海口市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 0,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 3,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.hainan.net/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://news\.hainan\.net/\w+/list_1\.shtml$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://news\.hainan\.net/[\w/]+/?\d{4,}/\d{2}/\d{2}/\d+\.shtml$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//*[@id='subject']/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@class='content']/p", },
                            {"xpath": "//div[@class='article_slider_bigPic_box cf']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://news.hainan.net/shehui/shehuiliebiao/2020/01/17/4160321.shtml",
                                "xpath": "//div[@class='info_le']/a[1]/text()",
                            },
                            {
                                "describe": "http://news.hainan.net/photo/guoneiguoji/xiaotu/2020/01/17/4160309.shtml",
                                "xpath": "//div[@class='picTip cf']/ul/li[1]/text()",
                            }
                        ],
                        "pubTime": [
                            {"xpath": "//div[@class='info_le']/text()", },
                            {"xpath": "//div[@class='picTip cf']/ul/li[3]/text()", },
                        ],
                        "channel": [
                            {"xpath": "//li[@class='l1']/a/text()", },
                        ],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "合肥在线",
            "sourceProvince": "安徽省",
            "sourceCity": "合肥市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 3,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.hf365.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.hf365\.com/[\w/]+/$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.hf365\.com/\d{4,}/\d{4}/\d+\.shtml$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//div[contains(@class, 'article-main')]/h1/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[contains(@class, 'article-content')]", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://www.hf365.com/2020/0116/1265349.shtml",
                                "xpath": "//span[@class='source']//text()",
                                "regex": r"\s*?稿源：\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [
                            {"xpath": "//span[@class='date']/text()", },
                        ],
                        "channel": [],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "广西新闻网",
            "sourceProvince": "广西省",
            "sourceCity": "南宁市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.gxnews.com.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.gxnews\.com\.cn/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.gxnews\.com\.cn/staticpages/\d{8,}/newgx\w+-\d+\.shtml$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//div[@class='article']/h1/text()", },
                            {"xpath": "//td[@class='title']/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@class='article-content']", },
                            {"xpath": "//td[@id='artContent']", },
                        ],
                        "pubSource": [
                            {
                                "xpath": "//div[@class='article-info']/span[1]/text()",
                                "regex": r".+?来源：(\w+)",
                            },
                            {
                                "xpath": "//td[@class='fs12']/text()",
                                "regex": r".+?来源：(\w+)",
                            }
                        ],
                        "pubTime": [
                            {"xpath": "//div[@class='article-info']/span[1]/text()", },
                            {"xpath": "//td[@class='fs12']/text()", },
                        ],
                        "channel": [
                            {"xpath": "//div[@class='more-title']/span/a[3]/text()", },
                        ],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "南方周末",
            "sourceProvince": "广东省",
            "sourceCity": "广州市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.infzm.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.infzm\.com/topics/t\d+.html$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.infzm\.com/contents/\d+$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//div[@class='nfzm-content__title']/h1/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@class='nfzm-content__fulltext']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://www.infzm.com/contents/174738",
                                "xpath": "//p[@class='nfzm-content__author']/span/text()",
                                "regex": r"\s*?作者：(\w+)",
                            },
                        ],
                        "pubTime": [
                            {"xpath": "//span[@class='nfzm-content__publish']/@data-time", },
                        ],
                        "channel": [
                            {"xpath": "//span[@class='nfzm-content__term']/text()", },
                        ],
                        "authors": [],
                        "summary": [{"xpath": "//blockquote[@class='nfzm-bq']/text()", }, ],
                    }
                }
            ]
        },
        {
            "platformName": "大江网",
            "sourceProvince": "江西省",
            "sourceCity": "南昌市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.jxnews.com.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.jxnews\.com\.cn/\w+/$",
                                r"https?://[\w\-\.]+\.jxnews\.com\.cn/index\.shtml$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.jxnews\.com\.cn/system/\d{4,}/\d{2}/\d{2}/\d+\.shtml$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//div[@data-toggle='title']/text()", },
                            {"xpath": "//div[@class='title']/text()", },
                        ],
                        "content": [
                            {"xpath": "//font[@id='Zoom']", },
                            {"xpath": "//div[@data-toggle='content']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://www.infzm.com/contents/174738",
                                "xpath": "//span[@id='source_baidu']//text()",
                                "regex": r"\s*?来源：\s*?(\w+)",
                            },
                        ],
                        "pubTime": [
                            {"xpath": "//span[@id='pubtime_baidu']/text()", },
                        ],
                        "channel": [
                            {"xpath": "//div[@class='position']/a[3]/text()", },
                        ],
                        "authors": [
                            {
                                "xpath": "//span[@id='author_baidu']/text()",
                                "regex": r"\s*?作者：\s*?([\w\s]+)",
                            },
                        ],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "新京报网",
            "sourceProvince": "北京市",
            "sourceCity": "北京市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.bjnews.com.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.bjnews\.com\.cn/?(\w+)?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.bjnews\.com\.cn/\w+/\d{4,}/\d{2}/\d{2}/\d+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//div[@class='title']/h1/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@class='content']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://www.bjnews.com.cn/wevideo/2018/11/01/516776.html",
                                "xpath": "//div[@class='fl ntit_l']/span[@class='author']/text()",
                                "regex": r"(\w+) ?·?[记作]者：",
                            },
                            {
                                "describe": "http://www.bjnews.com.cn/ent/2018/10/12/510454.html",
                                "xpath": "//div[@class='fl ntit_l']/span[@class='author']/text()",
                            }
                        ],
                        "pubTime": [
                            {"xpath": "//div[@class='fl ntit_l']/span[@class='date']/text()", },
                        ],
                        "channel": [
                            {"xpath": "//div[@id='logo']/h3/text()", },
                        ],
                        "authors": [
                            {
                                "xpath": "//div[@class='fl ntit_l']/span[@class='author']/text()",
                                "regex": r".*?[记作]者：(\w+)",
                            },
                        ],
                        "summary": [{"xpath": "//p[@id='daoy']/text()"}],
                    }
                }
            ]
        },
        {
            "platformName": "大洋网",
            "sourceProvince": "广东省",
            "sourceCity": "广州市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 3,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.dayoo.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://news\.dayoo\.com/\w+/\d+\.shtml$",
                                r"https?://[\w\-\.]+\.dayoo\.com/\w+/index\.shtml$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.dayoo\.com/\w+/\d{6,}/\d{2}/\d+_\d+.htm$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//div[@class='article-hd']/h1/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@class='content']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://news.dayoo.com/guangzhou/202001/17/139995_53034396.htm",
                                "xpath": "//span[@class='source']/text()",
                                "regex": r"\s*?来源:(\w+)$",
                            }
                        ],
                        "pubTime": [
                            {"xpath": "//span[@class='time']/text()", },
                        ],
                        "channel": [
                            {"xpath": "//div[@class='crumbs']/a[2]/text()", },
                        ],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "新民网",
            "sourceProvince": "上海市",
            "sourceCity": "上海市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.xinmin.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.xinmin\.cn/\w+/?$",
                                r"https?://[\w\-\.]+\.xinmin\.cn/\w+/pc/index\.htm$",
                                r"https?://[\w\-\.]+\.xinmin\.cn/\w+/index\.htm$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.xinmin\.cn/\w+/\d{4,}/\d{2}/\d{2}/\d+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//h1[@class='a_title']/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@class='a_content']/*[not(@class='copyright')]", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://shanghai.xinmin.cn/tfbd/2019/10/31/31604482.html",
                                "xpath": "//div[@class='info']/span[1]//text()",
                                "regex": r"\s*?来源：(\w+)$",
                            }
                        ],
                        "pubTime": [
                            {"xpath": "//div[@class='info']/span[contains(text(), ':')]//text()", },
                        ],
                        "channel": [
                            {
                                "xpath": "//div[@class='Mbx']/text()",
                                "regex": r"您现在的位置：首页 > (\w+)",
                            },
                        ],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "证券时报网",
            "sourceProvince": "广东省",
            "sourceCity": "深圳市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 0,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 3,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.stcn.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.stcn\.com/\w+/?$",
                                r"https?://[\w\-\.]+\.stcn\.com/\w+/index\.shtml$",
                                r"https?://[\w\-\.]+\.stcn\.com/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.stcn\.com/\d{4,}/\d{4}/\d+\.shtml$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//div[@class='intal_tit']/h2/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@id='ctrlfscont']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://news.stcn.com/2020/0117/15604150.shtml",
                                "xpath": "//div[@class='info']/span[1]/text()",
                                "regex": r"\s*?来源：(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//div[@class='info']/text()", }, ],
                        "channel": [{"xpath": "//div[@class='website']/a[3]/text()", }, ],
                        "authors": [
                            {
                                "xpath": "//div[@class='info']/span/text()",
                                "regex": r".*?作者：(\w+)$",
                            }
                        ],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "潇湘晨报网",
            "sourceProvince": "湖南省",
            "sourceCity": "长沙市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.xxcb.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.xxcb\.cn/\w+/\w+/$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.xxcb\.cn/\w+/\w+/\d{4,}-\d{2}-\d{2}/\d+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//h1[@id='comment-subject']/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@id='endPc']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://www.xxcb.cn/opinion/xjpl/2017-08-03/9069778.html",
                                "xpath": "//span[@id='source_baidu']/text()",
                                "regex": r"\s*?来源：(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//span[@id='comment-time']/text()", }, ],
                        "channel": [{"xpath": "//span[@class='menu_At']/a[2]/text()", }, ],
                        "authors": [
                            {
                                "xpath": "//span[@id='author_baidu']/text()",
                                "regex": r"\s*?作者：(\w+)$",
                            }
                        ],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "京报网",
            "sourceProvince": "北京市",
            "sourceCity": "北京市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {
                "interval": 0.5,
            },
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.bjd.com.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.bjd\.com\.cn/\w+/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.bjd\.com\.cn/a/\d{6,}/\d{2}/\w+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//span[@class='span1']/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@class='contentnews21']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://www.bjd.com.cn/a/202001/16/WS5e206115e4b0e6e58393919b.html",
                                "xpath": "//span[@class='span32']/text()",
                                "regex": r"\s*?来源:\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//span[@class='span31']/text()", }, ],
                        "channel": [
                            {
                                "xpath": "//span[@id='columnId']/text()",
                                "regex": r"(\w+)＞$",
                            },
                        ],
                        "authors": [
                            {
                                "xpath": "//span[@class='span33'][1]/text()",
                                "regex": r"\s*?作者:\s*?(\w+)$",
                            }
                        ],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "经济观察网",
            "sourceProvince": "北京市",
            "sourceCity": "北京市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 0,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.eeo.com.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.eeo\.com\.cn/\w+/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.eeo\.com\.cn/\d{4,}/\d{4}/\d+\.shtml$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//div[@class='xd-b-b']/h1/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@class='xd-nr']/*[@class='xd-xd-xd-newsimg' or @class='xx_boxsing']", },
                        ],
                        "pubSource": [],
                        "pubTime": [{"xpath": "//div[@class='xd-b-b']/p/span[1]/text()", }, ],
                        "channel": [],
                        "authors": [{"xpath": "//div[@class='xd-b-b']/p/text()[1]", }, ],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "华夏时报网",
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
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.chinatimes.net.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.chinatimes\.net\.cn/\w+/\w+/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.chinatimes\.net\.cn/article/\d+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//div[@class='title']/h1/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@class='infoMain']/p", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://www.chinatimes.net.cn/article/93650.html",
                                "xpath": "//p[@id='source_baidu']//text()",
                                "regex": r"\s*?来源：\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//p[@id='pubtime_baidu']/text()", }, ],
                        "channel": [{"xpath": "//div[@class='contentpart']/p/a[2]/text()", }, ],
                        "authors": [
                            {
                                "xpath": "//p[@id='author_baidu']//text()",
                                "regex": r"\s*?作者：(\w+)$",
                            }
                        ],
                        "summary": [
                            {
                                "xpath": "//div[@class='abstract']/text()",
                                "regex": r"\s*?摘要：(.+)$",
                            }
                        ],
                    }
                }
            ]
        },
        {
            "platformName": "华西都市网",
            "sourceProvince": "四川省",
            "sourceCity": "成都市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 3,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.huaxi100.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.huaxi100\.com/portal\.php\?mod=\w+$",
                                r"https?://news\.huaxi100\.com/list-[\d\-]+\.html",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.huaxi100\.com/a/\w+$",
                                r"https?://news\.huaxi100\.com/show-[\d\-]+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//h5[@class='title']/text()", },
                            {"xpath": "//h1[@class='details_title']/text()", },
                        ],
                        "content": [
                            {"xpath": "//section[@class='sec-content']/*[not(@data-tools)]", },
                            {"xpath": "//div[@class='summary']", },
                        ],
                        "pubSource": [
                            {
                                "xpath": "//div[@class='details_info']/text()",
                                "regex": r".*?来源: (\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//div[@class='details_info']/text()", }, ],
                        "channel": [{"xpath": "//span[@class='nrNow'][1]/a/text()", }, ],
                        "authors": [],
                        "summary": [{"xpath": "//p[@class='pad-bt']/text()", }, ],
                    }
                }
            ]
        },
        {
            "platformName": "北青网",
            "sourceProvince": "北京市",
            "sourceCity": "北京市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.ynet.com/index.html",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.ynet\.com/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.ynet\.com/\d{4,}/\d{2}/\d{2}/\w+.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//div[@class='articleTitle']/h1/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@id='articleBox']/*[not(div)]", },
                        ],
                        "pubSource": [{"xpath": "//span[@class='sourceMsg']/text()", }, ],
                        "pubTime": [{"xpath": "//span[@class='yearMsg']/text()", }, ],
                        "channel": [{"xpath": "//dl[@class='cfix fLeft']/dd/a[2]/text()", }, ],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "半岛网",
            "sourceProvince": "山东省",
            "sourceCity": "青岛市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 3,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.bandao.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.bandao\.cn/?$",
                                r"https?://[\w\-\.]+\.bandao\.cn/c/\w+\.html$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.bandao\.cn/a/\d+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//div[@class='content-main ']/h1/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@id='content']//p", },
                        ],
                        "pubSource": [{"xpath": "//div[@class='time']/span[1]/text()", }],
                        "pubTime": [{"xpath": "//div[@class='time']/text()", }, ],
                        "channel": [{"xpath": "//div[@class='nav']/a[2]/text()", }, ],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "金羊网",
            "sourceProvince": "广东省",
            "sourceCity": "广州市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 3,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.ycwb.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.ycwb\.com/?$",
                                r"https?://[\w\-\.]+\.ycwb\.com/\w+\.htm$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.ycwb\.com/\d{4,}-\d{2}/\d{2}/content_\d+\.htm$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//h1[@id='tiwj']/text()", }, ],
                        "content": [{"xpath": "//div[@class='main_article']", }, ],
                        "pubSource": [
                            {
                                "xpath": "//span[@id='source_baidu']/text()",
                                "regex": r"\s*?来源：\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//span[@id='pubtime_baidu']/text()", }, ],
                        "channel": [{"xpath": "//div[@class='path']/a[1]/text()", }, ],
                        "authors": [
                            {
                                "xpath": "//span[@id='author_baidu']/text()",
                                "regex": r"\s*?作者：\s*?(\w+)、?(\w+)?、?(\w+)?、?(\w+)?$",
                            }
                        ],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "三秦网",
            "sourceProvince": "陕西省",
            "sourceCity": "西安市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.sanqin.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.sanqin\.com/node_\d+\.html$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.sanqin\.com/\d{4,}-\d{2}/\d{2}/content_\d+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//h1[@class='showtitle']/text()", }, ],
                        "content": [{"xpath": "//div[@class='article-content']", }, ],
                        "pubSource": [{"xpath": "//span[@class='source']/text()", }, ],
                        "pubTime": [{"xpath": "//div[@class='col-xs-18 showinfo']/span[last()]/text()", }, ],
                        "channel": [{"xpath": "//div[@class='col-xs-18 showinfo']/span[1]/a/text()", }, ],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "中国经济网",
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
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.ce.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.ce\.cn/?$",
                                r"https?://[\w\-\.]+\.ce\.cn/[\w/]+/?(index\.shtml)?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.ce\.cn/[\w/]+/\d{6,}/\d{2}/t\d{8,}_\d+\.shtml$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//h1[@id='articleTitle']/text()", }, ],
                        "content": [{"xpath": "//div[@id='articleText']", }, ],
                        "pubSource": [
                            {
                                "xpath": "//span[@id='articleSource']/text()",
                                "regex": r"\s*?来源：\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//span[@id='articleTime']/text()", }, ],
                        "channel": [{"xpath": "//a[@class='CurrChnlCls'][2]/text()", }, ],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "第一财经",
            "sourceProvince": "上海市",
            "sourceCity": "上海市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "https://www.yicai.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.yicai\.com/\w+/?(\w+)?/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.yicai\.com/news/\d+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//div[contains(@class, 'title')]/h1/text()", }, ],
                        "content": [{"xpath": "//div[@class='m-txt']/*[not(@class='statement')]", }, ],
                        "pubSource": [{"xpath": "//div[@class='title f-pr']/p/span[1]/text()", }, ],
                        "pubTime": [{"xpath": "//div[@class='title f-pr']/p/em/text()", }, ],
                        "channel": [{"xpath": "//span[@class='z-crt']/text()", }, ],
                        "authors": [{"xpath": "//div[@class='person f-cb']/ul/a/li/p/text()", }, ],
                        "summary": [{"xpath": "//div[@class='intro']/text()", }, ],
                    }
                }
            ]
        },
        {
            "platformName": "河北新闻网",
            "sourceProvince": "河北省",
            "sourceCity": "石家庄市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.hebnews.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.hebnews\.cn/?(node_\d+\.htm)?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.hebnews\.cn/\d{4,}-\d{2}/\d{2}/content_\d+\.htm$",
                                # 阳光理政。
                                # r"https?://yglz\.tousu\.hebnews\.cn/s-\d+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//div[@class='g_width content']/h1/text()", }, ],
                        "content": [{"xpath": "//div[@class='text']", }, ],
                        "pubSource": [
                            {
                                "xpath": "//div[@class='post_source']/text()",
                                "regex": r".*?来源：\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//div[@class='post_source']/text()", }, ],
                        "channel": [{"xpath": "//div[@class='bc_main']/a[1]/text()", }, ],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "湖南在线",
            "sourceProvince": "湖南省",
            "sourceCity": "长沙市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://hunan.voc.com.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.voc\.com\.cn/?$",
                                r"https?://[\w\-\.]+\.voc\.com\.cn/class/\d+\.html$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.voc\.com\.cn/article/\d{6,}/\d+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//div[@class='main_l']/h1/text()", }, ],
                        "content": [{"xpath": "//div[@id='content']", }, ],
                        "pubSource": [
                            {
                                "xpath": "//span[@id='source_baidu']//text()",
                                "regex": r".*?来源:\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//span[@id='pubtime_baidu']/text()", }, ],
                        "channel": [
                            {
                                "xpath": "//a[@class='nav_link'][3]/text()",
                            }
                        ],
                        "authors": [
                            {
                                "xpath": "//span[@id='author_baidu']//text()",
                                "regex": r".*?作者:\s*?(\w+)\s?(\w+)?\s?(\w+)?$",
                            }
                        ],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "中国军网",
            "sourceProvince": "北京市",
            "sourceCity": "北京市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 1,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 2,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {
                "interval": 0.2,
            },
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.81.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.81\.cn/?(\w+)?/?((index\.htm)|(node_\d+\.htm))?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.81\.cn/\w+/\d{4,}-\d{2}/\d{2}/content_\d+\.htm$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//div[@class='article-header']/h1/text()", },
                            {"xpath": "//div[@class='container artichle-info']/h2/text()", },
                        ],
                        "content": [{"xpath": "//div[@id='article-content']", }, ],
                        "pubSource": [
                            {
                                "xpath": "//div[@class='info']/span[1]//text()",
                                "regex": r".*?来源：\s*?(\w+)$",
                            },
                            {
                                "xpath": "//div[@class='container artichle-info']/p/span[1]//text()",
                                "regex": r".*?来源：\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [
                            {"xpath": "//i[@class='time']/text()", },
                            {"xpath": "//div[@class='container artichle-info']/p/span[3]/text()", },
                        ],
                        "channel": [{"xpath": "//ol[@class='breadcrumb hidden-print']/a[1]/text()", }, ],
                        "authors": [
                            {
                                "xpath": "//div[@class='info']/span[contains(text(), '作者：')]/text()",
                                "regex": r".*?作者：\s*?(\w+)\s?等?\s?(\w+)?\s?等?\s?(\w+)?\s?等?$",
                            },
                            {
                                "xpath": "//span[@id='author-info']/text()",
                                "regex": r".*?作者：\s*?(\w+)、?\s?等?(\w+)?、?\s?等?(\w+)?\s?等?$",
                            }
                        ],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "中工网",
            "sourceProvince": "北京市",
            "sourceCity": "北京市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 1,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 2,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.workercn.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.workercn\.cn/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.workercn\.cn/\d+/\d{6,}/\d{2}/\d+\.shtml$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//h1[@class='ctitle']/text()", }, ],
                        "content": [{"xpath": "//div[@class='ccontent']", }, ],
                        "pubSource": [{"xpath": "//div[@class='signdate']/span[2]/text()", }, ],
                        "pubTime": [{"xpath": "//div[@class='signdate']/span[1]/text()", }, ],
                        "channel": [{"xpath": "//h2[@class='sub']/a/text()", }],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "中国农网",
            "sourceProvince": "北京市",
            "sourceCity": "北京市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 1,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 2,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.farmer.com.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.farmer\.com\.cn/[\w/]+/list\.shtml$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.farmer\.com\.cn/\d{4,}/\d{2}/\d{2}/\d+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//h1[@class='article-title']/text()", }, ],
                        "content": [{"xpath": "//div[@id='article_main']", }, ],
                        "pubSource": [{"xpath": "//span[@class='tag-text tag-text-source']/text()", }, ],
                        "pubTime": [{"xpath": "//span[@class='article-meta-time']/text()", }, ],
                        "channel": [{"xpath": "//a[@class='breadcrumb-item is-active']/text()", }],
                        "authors": [
                            {
                                "xpath": "//div[@class='article-meta-left fl']/span[@class='tag-text']/text()",
                                "regex": r".*?作者：\s*?(\w+)\s?(\w+)?\s?(\w+)?$",
                            }
                        ],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "中国青年网",
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
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.youth.cn",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.youth\.cn/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.youth\.cn/\w+/\d{6,}/t\d{8,}_\d+\.htm$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//p[@class='pbt']/text()", }, ],
                        "content": [{"xpath": "//div[@class='TRS_Editor']", }, ],
                        "pubSource": [
                            {
                                "xpath": "//p[@class='pwz']//text()",
                                "regex": r".*?来源：\s*?(\w+)$",
                            },
                        ],
                        "pubTime": [{"xpath": "//p[@class='pwz']/text()", }, ],
                        "channel": [{"xpath": "//span[@class='lm_mc']/a[2]/@title", }],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "中国日报网",
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
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {
                "allowRedirects": 1
            },
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://cn.chinadaily.com.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.chinadaily\.com\.cn/\w+/?(\w+)?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.chinadaily\.com\.cn/a/\d{6,}/\d{2}/\w+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//h1[@class='dabiaoti']/text()", },
                            {"xpath": "//span[@class='main_title1']/text()", },
                        ],
                        "content": [{"xpath": "//div[@id='Content']", }, ],
                        "pubSource": [
                            {
                                "xpath": "//div[@class='fenx']/div[@class='xinf-le'][1]//text()",
                                "regex": r"\s*?来源：\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [
                            {"xpath": "//div[@class='fenx']/div[@class='xinf-le'][2]//text()", },
                            {"xpath": "//p[@class='main_title3']/text()", },
                        ],
                        "channel": [{"xpath": "//div[@class='dingtou']/div[@class='da-bre']/a[1]/text()", }],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "中华工商网",
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
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.cbt.com.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.cbt\.com\.cn/\w{2,3}/\w+/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.cbt\.com\.cn/[\w/]+/\d{6,}/t\d{8,}_\d+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//div[@class='con-title']/h1/text()", }, ],
                        "content": [
                            {"xpath": "//div[@class='article-detail']", },
                            {"xpath": "//div[@class='video-detail']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://www.cbt.com.cn/rw/xylj/202001/t20200115_151307.html",
                                "xpath": "//div[@class='time']/span[2]/text()",
                                "regex": r"\s*?来源：\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//div[@class='time']/span[1]/text()", }, ],
                        "channel": [{"xpath": "//a[@class='CurrChnlCls'][2]/@title", }],
                        "authors": [
                            {
                                "describe": "http://www.cbt.com.cn/rw/xylj/202001/t20200115_151307.html",
                                "xpath": "//div[@class='time']/span[3]/text()",
                                "regex": r"\s*?作者：\s*?(\w+)\s*?(\w+)?\s*?(\w+)?$",
                            }
                        ],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "中国企业网",
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
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.zqcn.com.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.zqcn\.com\.cn/?$",
                                r"https?://[\w\-\.]+\.zqcn\.com\.cn/[\w/]+/node\d+\.html$",
                                r"https?://[\w\-\.]+\.zqcn\.com\.cn/[\w/]+/col\d+\.html$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.zqcn\.com\.cn/[\w/]+/\d{6,}/\d{2}/c?\d+\.html",
                                r"https?://[\w\-\.]+\.zqcn\.com\.cn/[\w/]+/\d{8,}/c?\d+\.html$",
                                r"https?://[\w\-\.]+\.zqcn\.com\.cn/[\w/]+/content/c?\d+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {"xpath": "//h2[@class='t']/text()", },
                            {"xpath": "//div[@id='title']/h1/text()", },
                        ],
                        "content": [
                            {"xpath": "//div[@class='ctbox']/*[not(@class='fenge') and not(@class='fanye')]", },
                            {"xpath": "//div[@class='content']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://www.zqcn.com.cn/yuanqu/202001/15/c518011.html",
                                "xpath": "//div[@class='tag']/span[1]/text()",
                                "regex": r"\s*?来源：\s*?([\w－]+)$",
                            },
                            {
                                "describe": "https://finance.zqcn.com.cn/html/stock/20200107/104212.html",
                                "xpath": "//div[@class='info']/span[2]/text()",
                                "regex": r"(\w+)$",
                            },
                        ],
                        "pubTime": [
                            {"xpath": "//div[@class='tag']/span[2]/text()", },
                            {"xpath": "//div[@class='info']/span[1]/text()", },
                        ],
                        "channel": [
                            {"xpath": "//span[@class='cmb']/a[2]/text()", },
                            {"xpath": "//div[@class='current_p']/a[2]/text()", },
                        ],
                        "authors": [
                            {
                                "describe": "http://www.zqcn.com.cn/hongguan/202001/20/c518098.html",
                                "xpath": "//div[@class='tag']/a[1]/text()",
                                "regex": r"(\w+)\s?(\w+)?\s?(\w+)?\s?(\w+)?$",
                            }
                        ],
                        "summary": [{"xpath": "//div[@class='des']/text()"}],
                    }
                }
            ]
        },
        {
            "platformName": "中国经济导报网",
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
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.ceh.com.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.ceh\.com\.cn/\w+/index\.shtml$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.ceh\.com\.cn/\w+/\d{4,}/\d+\.shtml$",
                                r"https?://www\.ceh\.com\.cn/\w+/\d+\.shtml$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//td[@class='title_content']/text()", }, ],
                        "content": [{"xpath": "//td[@class='content3']/p", }, ],
                        "pubSource": [
                            {
                                "describe": "http://www.zqcn.com.cn/yuanqu/202001/15/c518011.html",
                                "xpath": "//td[@class='date_content']/text()",
                                "regex": r"[\d\:\-\s]+?\s+(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//td[@class='date_content']/text()", }, ],
                        "channel": [{"xpath": "//td[@class='dqwz']/a[2]/text()", }, ],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "中国妇女网",
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
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.cnwomen.com.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.cnwomen\.com\.cn/cnwomen/\w+/index\.shtml$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.cnwomen\.com\.cn/\d{4,}/\d{2}/\d{2}/\d+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//p[@class='f_container_title']/text()", }, ],
                        "content": [{"xpath": "//div[@class='f_navigation_bars']/"
                                              "p[@class='f_container_source']/following-sibling::p", }, ],
                        "pubSource": [
                            {
                                "describe": "http://www.cnwomen.com.cn/2019/12/30/99186995.html",
                                "xpath": "//p[@class='f_container_source']/span[2]/text()",
                                "regex": r"\s*?来源：\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//ul[@class='f_container_ul']/li[2]/text()", }, ],
                        "channel": [{"xpath": "//div[@class='f_navigation_bars']/p/a[last()]/span/text()", }, ],
                        "authors": [
                            {
                                "describe": "http://www.cnwomen.com.cn/2020/01/20/99189089.html",
                                "xpath": "//p[@class='f_container_source']/span[3]/text()",
                                "regex": r"\s*?作者：\s*?本?报?实?习?记?者?\s?(\w+)\s?(\w+)?\s?(\w+)?$",
                            }
                        ],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "中国科技网",
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
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.stdaily.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.stdaily\.com/\w+/?$",
                                r"https?://www\.stdaily\.com/\w+/index\.shtml?$",
                                r"https?://www\.stdaily\.com/[\w/]+/\w+\.shtml$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.stdaily\.com/[\w/]+/\d{4,}-\d{2}/\d{2}/content_\d+\.shtml$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//div[@class='aticleHead']/h1/text()", }, ],
                        "content": [{"xpath": "//div[@class='content']", }, ],
                        "pubSource": [
                            {
                                "describe": "http://www.stdaily.com/cxzg80/guonei/2019-12/31/content_849425.shtml",
                                "xpath": "//span[@class='f_source']/text()",
                            }
                        ],
                        "pubTime": [{"xpath": "//div[@class='time ']/text()", }, ],
                        "channel": [{"xpath": "//ol[@class='breadcrumb']/a[2]/span/text()", }, ],
                        "authors": [{"xpath": "//span[@class='f_author']/text()", }, ],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "福建网络广播电视台",
            "sourceProvince": "福建省",
            "sourceCity": "福州市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.fjtv.net/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.fjtv\.net/?\w*?/?\w*?/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.fjtv.net/folder\d+/\d{4,}-\d{2}-\d{2}/\d+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//div[@class='article-title']/h1/text()", }, ],
                        "content": [
                            {"xpath": "//div[@class='article-brief'] | //div[@class='article-main']", },
                        ],
                        "pubSource": [
                            {
                                "describe": "http://headline.fjtv.net/folder476/2020-01-20/2154263.html",
                                "xpath": "//span[@class='origin']/text()",
                                "regex": r"\s*?来源:\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//span[@class='time']/text()", }, ],
                        "channel": [],
                        "authors": [
                            {
                                "xpath": "//span[@class='author']/text()",
                                "regex": r"\s*?作者:\s*?(\w+)$",
                            },
                        ],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "宁夏广播电视台",
            "sourceProvince": "宁夏回族自治区",
            "sourceCity": "银川市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.nxtv.com.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.nxtv\.com\.cn/?\w*?/?\w*?/?$",
                                r"https?://[\w\-\.]+\.nxtv\.com\.cn/\w+/folder\d+/\d{4,}-\d{2}-\d{2}/\d+\.html$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.nxtv\.com\.cn/\w+/\d{4,}-\d{2}-\d{2}/\d+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//div[@class='article-title']/h1/text()", }, ],
                        "content": [{"xpath": "//div[@class='article-brief'] | //div[@class='article-main']", }, ],
                        "pubSource": [
                            {
                                "describe": "http://news.nxtv.com.cn/life/2020-01-20/508046.html",
                                "xpath": "//span[@class='origin']//text()",
                                "regex": r"\s*?来源:\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//span[@class='time']/text()", }, ],
                        "channel": [{"xpath": "//ul[@class='cell_8700_ clearfix']/li[3]/a/@title", }, ],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "青海羚网",
            "sourceProvince": "青海省",
            "sourceCity": "西宁市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "https://www.qhlingwang.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.qhlingwang\.com/?\w*?/?\w*?/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.qhlingwang\.com/\w+/\w+/\d{4,}-\d{2}-\d{2}/\d+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//h2[@class='article-title']/text()", }, ],
                        "content": [{"xpath": "//div[@class='article-entry']", }, ],
                        "pubSource": [
                            {
                                "describe": "https://www.qhlingwang.com/xinwen/qinghai/2020-01-20/308824.html",
                                "xpath": "//span[@class='laiyuan']//text()",
                                "regex": r"\s*?来源:\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//time[@class='date updated']/text()", }, ],
                        "channel": [{"xpath": "//nav[@id='breadcrumb']/p/a[3]/text()", }, ],
                        "authors": [
                            {
                                "xpath": "//span[@class='author']//text()",
                                "regex": r"\s*?作者:\s*?(\w+)$",
                            }
                        ],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "老友网",
            "sourceProvince": "广西壮族自治区",
            "sourceCity": "南宁市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.nntv.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.nntv\.cn/[\w/]+/$",
                                r"https?://www\.nntv\.cn/[\w/]+/list\.shtml$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.nntv\.cn/[\w/]+/\d{4,}-\d{1,2}-\d{1,2}/\d+\.shtml$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//div[@class='subject']/h1/text()", }, ],
                        "content": [{"xpath": "//div[@class='content']", }, ],
                        "pubSource": [
                            {
                                "describe": "http://www.nntv.cn/news/m/2020-1-20/1579491713326.shtml",
                                "xpath": "//div[@class='source']/span[2]/text()",
                                "regex": r"\s*?来源：\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//span[@class='time']/text()", }, ],
                        "channel": [{"xpath": "//nav[@id='breadcrumb']/p/a[3]/text()", }, ],
                        "authors": [],
                        "summary": [
                            {
                                "xpath": "//div[@class='summary']/p/text()",
                                "regex": "[^此][^节][^目][^暂][^时][^还][^未][^添][^加][^摘][^要](.+)$",
                            },
                        ],
                    }
                }
            ]
        },
        {
            "platformName": "广西广播电视台",
            "sourceProvince": "广西壮族自治区",
            "sourceCity": "南宁市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 状态，是否开启采集。
            "status": 0,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "https://www.gxtv.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [
                                r"https?://tv\.gxtv\.cn/?"
                            ],
                            "target": [
                                r"https?://[\w\-\.]+\.gxtv\.cn/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://[\w\-\.]+\.gxtv\.cn/article/detail_\w+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//h1[@id='title']/text()", }, ],
                        "content": [{"xpath": "//div[@id='news_con']", }, ],
                        "pubSource": [
                            {
                                "describe": "https://news.gxtv.cn/article/detail_9ae9b5f3ecd5420ab18bd6cedbcc0653.html",
                                "xpath": "//span[@class='news_from']//text()",
                                "regex": r"\s*?来源：\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//span[@class='news_time']/text()", }, ],
                        "channel": [{"xpath": "//span[@class='capname']/a[2]/text()", }, ],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "黑龙江网络广播电视台",
            "sourceProvince": "黑龙江省",
            "sourceCity": "哈尔滨市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 状态，是否开启采集。
            "status": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.hljtv.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.hljtv\.com/\w+/$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.hljtv\.com/news/folder\d+/\d{4,}-\d{2}-\d{2}/\d+\.shtml$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//div[@class='article-title pull-left']/h1/text()", }, ],
                        "content": [{"xpath": "//div[@class='article-main']", }, ],
                        "pubSource": [
                            {
                                "describe": "http://www.hljtv.com/news/folder9/2020-01-19/738760.shtml",
                                "xpath": "//span[@class='origin']//text()",
                                "regex": r"\s*?来源：\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//span[@class='time']//text()", }, ],
                        "channel": [{"xpath": "//ul[@class='cell_1096_ clearfix']/li[3]/a/@title", }, ],
                        "authors": [],
                        "summary": [
                            {
                                "xpath": "//div[@class='brief']/text()",
                                "regex": r"\s*?[摘要]\s*?(\w+)$",
                            },
                        ],
                    }
                }
            ]
        },
        {
            "platformName": "四川广播电视台",
            "sourceProvince": "四川省",
            "sourceCity": "成都市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 状态，是否开启采集。
            "status": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.sctv.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [
                                r"https?://www\.sctv\.com/live/?",
                            ],
                            "target": [
                                r"https?://www\.sctv\.com/\w+/$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [
                                r"https?://www\.sctv\.com/live/?",
                            ],
                            "target": [
                                r"https?://www\.sctv\.com/[\w/]+/\d{6,}/t\d{8,}_\d+\.shtml$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//h1[@class='ep-h1']/text()", }, ],
                        "content": [{"xpath": "//div[@id='end-text']", }, ],
                        "pubSource": [
                            {
                                "describe": "http://www.sctv.com/news/gn/202001/t20200120_4329331.shtml",
                                "xpath": "//div[@class='ep-source']//text()",
                                "regex": r"\s*?来源:\s*?(\w+)$",
                            }
                        ],
                        "pubTime": [{"xpath": "//div[@class='ep-time']//text()", }, ],
                        "channel": [{"xpath": "//div[@class='ep-crumb']/a[3]/@title", }, ],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "广东广播电视台",
            "sourceProvince": "广东省",
            "sourceCity": "广州市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 状态，是否开启采集。
            "status": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {
                "depth": 2,
            },
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.gdtv.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [
                                r"https?://v\.gdtv\.cn/?",
                            ],
                            "target": [
                                r"https?://www\.gdtv\.cn/\w+/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [
                                r"https?://v\.gdtv\.cn/?",
                            ],
                            "target": [
                                r"https?://www\.gdtv\.cn/[\w/]+/\d{4,}-\d{2}-\d{2}/\d+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//div[@class='article-title pull-left']/h1/text()", }, ],
                        "content": [{"xpath": "//div[@class='article-main']", }, ],
                        "pubSource": [
                            {
                                "describe": "http://www.gdtv.cn/local/2019-12-30/2246114.html",
                                "xpath": "//span[@class='origin']/text()",
                            }
                        ],
                        "pubTime": [{"xpath": "//span[@class='datetime']/text()", }, ],
                        "channel": [{"xpath": "//div[@class='mbx overflow']/ul[@class='clearfix']/li[2]/a/@title", }, ],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "封面新闻",
            "sourceProvince": "四川省",
            "sourceCity": "成都市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 状态，是否开启采集。
            "status": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.thecover.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.thecover\.cn/channel_\d+/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.thecover\.cn/news/\d+$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//article/header/h1/text()", }, ],
                        "content": [{"xpath": "//section[@class='article-content']/"
                                              "*[not(./strong[starts-with(text(), '【如果您有新闻线索，')])]", }, ],
                        "pubSource": [
                            {
                                "describe": "http://www.thecover.cn/news/3420095",
                                "xpath": "//p[@class='props-of-title']/a/span/text()",
                            }
                        ],
                        "pubTime": [{"xpath": "//p[@class='props-of-title']/span[1]/text()", }, ],
                        "channel": [],
                        "authors": [],
                        "summary": [],
                    }
                }
            ]
        },
        {
            "platformName": "21世纪经济报道",
            "sourceProvince": "广东省",
            "sourceCity": "广州市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 2,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 1,
            # 是否主流媒体。
            "mainMedia": 1,
            # 状态，是否开启采集。
            "status": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.21jingji.com/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.21jingji\.com/channel/\w+/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.21jingji\.com/\d{4,}/\d{1,2}-\d{1,2}/\w+\.html$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//h2[@class='titl']/text()", }, ],
                        "content": [{"xpath": "//div[@class='detailCont']", }, ],
                        "pubSource": [{"xpath": "//span[@class='baodao']/text()", }, ],
                        "pubTime": [{"xpath": "//p[@class='Wh']/span/text()", }, ],
                        "channel": [{"xpath": "//p[@class='colorGreen detailF']/a[2]/@title", }, ],
                        "authors": [
                            {
                                "describe": "http://www.21jingji.com/2020/1-17/3OMDEzODFfMTUyNzE3OA.html",
                                "xpath": "//span[@class='Wh1']/text()",
                                "regex": r"(\w+),?(\w+)?,?(\w+)?$",
                            },
                        ],
                        "summary": [{"xpath": "//p[@class='abstract backg']/text()", }, ],
                    }
                }
            ]
        },
        {
            "platformName": "TECHWEB",
            "sourceProvince": "北京市",
            "sourceCity": "北京市",
            "sourceCounty": "",
            # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
            "sourceLevel": 0,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 3,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # 状态，是否开启采集。
            "status": 1,
            # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
            "params": {},
            # 模板内容。
            "templates": [
                {
                    # 起始地址。
                    "start_url": "http://www.techweb.com.cn/",
                    "start_url_name": "首页",
                    # 导航链接。
                    "navi_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.techweb\.com\.cn/\w+/?$",
                            ]
                        }
                    },
                    # 详情链接。
                    "doc_links": {
                        "regex": {
                            "ignore": [],
                            "target": [
                                r"https?://www\.techweb\.com\.cn/\w+/\d{4,}-\d{2}-\d{2}/\d+\.shtml$",
                            ]
                        }
                    },
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [{"xpath": "//div[@class='main_c']/h1/text()", }, ],
                        "content": [{"xpath": "//div[@id='content']", }, ],
                        "pubSource": [
                            {
                                "describe": "http://www.techweb.com.cn/it/2020-01-21/2774671.shtml",
                                "xpath": "//span[@class='from']//text()",
                                "regex": r"\s*?来源:\s*?(\w+)\s*?$",
                            },
                        ],
                        "pubTime": [{"xpath": "//span[@class='time']/text()", }, ],
                        "channel": [{"xpath": "//div[@class='breadnav']/a[2]/text()", }, ],
                        "authors": [
                            {
                                "xpath": "//span[@class='author']//text()",
                                "regex": r"\s*?作者:\s*?(\w+)$",
                            },
                        ],
                        "summary": [],
                    }
                }
            ]
        },


    ][-1]


def post(url, use_gzip=False, batch_size=10):
    """
    发送请求。
    :return:
    """

    t = time.time()
    one_row = row()
    one_row["batchSize"] = batch_size
    response = requests.post(url, data=json.dumps(one_row).encode('utf-8'))
    if response.status_code == requests.codes.ok:
        # noinspection PyBroadException
        try:
            if not use_gzip:
                response = json.loads(response.content.decode("utf-8"))
            else:
                response = json.loads(gzip.decompress(response.content).decode("utf-8"))
            print(json.dumps(response, indent=4, ensure_ascii=False))
        except Exception:
            print(traceback.format_exc())
    else:
        print("Failed {}.".format(response.status_code))
    print("[{}.{}] Time used: {}.".format(os.getppid(), os.getpid(), time.time() - t))


def upload_template():
    """
    上传电子报xpath。
    :return:
    """

    post("http://192.168.32.18:6091/website/template/check", use_gzip=True, batch_size=15)
    # post("http://192.168.32.18:6090/website/template/create")
    # post("http://192.168.32.18:6090/website/template/update")


if __name__ == '__main__':
    upload_template()
