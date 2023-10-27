list = [
    # 1/13 3 85
    # 河北省人社局(90,我已修改)
    {
        "platformName": "河北省人社局",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://rst.hebei.gov.cn/index.html",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@id='myjQueryContent']/div/a | //div[@id='jQueryVideoContent']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": [
            "//div[@id='con_news_1']//a | //div[@id='con_news_2']/ul/li/a | //div[@id='con_news_3']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='hbrswnavx']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            # https://rst.hebei.gov.cn/a/news/tupian/2021/0112/9929.html
            r"https?://[\w\-\.]+/\w/\w+/\w+/\d{4,}/\d{4,}/\d+.html$",
            r"https?://[\w\-\.]+/\w/\w+/\w+/\d{4,}/\d{2,}/\d{2,}/\d+.shtml$",
            r"https?://[\w\-\.]+/\w/\w+/\d{4,}/\d{2,}/\d{2,}/\d+.shtml$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='title']/h1/text()", },
                {"xpath": "//div[@id='title_area']/h1/text()", },
                {"xpath": "//div[@class='wh610 left']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='body']", },
                {"xpath": "//div[@id='content_area']", },
                {"xpath": "//div[@class='TRS_Editor']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='info']/span[contains(text(), '来源')]/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                }
            ],
            "pubTime": [
                {"xpath": "//div[@class='info']/span[contains(text(), '时间')]/text()", "regex": r"时间[: ：]\s*?(.*)$"},
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 河北共产党员网(90,已修改)
    {
        "platformName": "河北共产党员网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.hebgcdy.com/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@id='dytt']/a"],
        # 轮播信息
        "banner_news": ["//div[@class='banner_0_top']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//table[@class='secondary-table']//a[@class='bglb1'][@target='_blank']"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav0']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d{4,}/\d{2,}/\d{2,}/\d+.shtml$",
        ],
        # 目标采集字段
        "fields": {
            "title": [
                {"xpath": "//div[@class='page_main']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='content_text0']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@id='laiyuan']/text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                }
            ],
            "pubTime": [
                {"xpath": "//span[@id='fbsj']/text()", "regex": r"发布时间[: ：]\s*?(.*)$", },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 今日渤海网(重做)
    # Fred:已修改
    {
        "platformName": "今日渤海网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.bohaitoday.cn/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='news_title']/a"],
        # 轮播信息
        "banner_news": ["//div[@id='photoDotSwitch319']/div[@class='switchGroup']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@id='newsList433']/div[@ topclassname ='top1']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='itemCenter navItem']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/.*",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class='title']/text()", },
                {"xpath": "//div[@class='g_width content']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='jz_fix_ue_img']", },
                {"xpath": "//div[@class='text']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='leftInfo']/span[contains(text(), '来源')]/text()",
                    "regex": r"来源[: ：]\s*?(.*)"
                },

            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='leftInfo']/span[contains(text(), '发表时间')]/text()",
                    "regex": r"发表时间[: ：]\s*?(.*)"
                },
            ],
            "authors": [],
            "summary": [],
        }
    },

    # 1/14 5 90
    # 廊坊市政府网
    {
        "platformName": "廊坊市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.lf.gov.cn/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='hotHead']/p/a"],
        # 轮播信息
        "banner_news": ["//div[@class='bd']/ul/li/div/a"],
        # 轮播旁边新闻
        "banner_news_side": [
            "//div[@class='bd J_tabContent']/ul[@class='infoList infoListB']/li/a | //div[@class='bd J_tabContent']/ul[@class='infoList infoListB hide']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='siteWidth']/dl/dd/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+.aspx$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='titleBar']/h2/text()", },
                {"xpath": "//div[@class='titleBar']//span/text()"}
            ],
            "content": [
                {"xpath": "//div[@id='fontzoom']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='property']/span[2]/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                }
            ],
            "pubTime": [{"xpath": "//div[@class='property']/span[1]/text()", }, ],
            "authors": [{"xpath": "//div[@class='property']/span[3]/text()",
                         "regex": r"作者[: ：]\s*?(.*)", }, ],
            "summary": [],
        }
    },
    # 环京津新闻网
    {
        "platformName": "环京津新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.010lf.com/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='toutiao']//a"],
        # 轮播信息
        "banner_news": [
            "//div[@id='hotpic']/div[@class='swiper-wrapper']/div[@class='swiper-slide']/a | //div[@id='hotpic']/div[@class='swiper-wrapper']/div[@class='swiper-slide swiper-slide-visible swiper-slide-active']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='teletext']/div/h2/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='menu']/ul/li//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\d+.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='article pt10']/h3/text()", },

            ],
            "content": [
                {"xpath": "//div[@class='aritclecontent']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='time']/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                },

            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='time']/text()",
                    "regex": r"\s*?(.*) | "}
            ],

            "authors": [{"xpath": "//div[@class='editor']/a/text()"}],
            "summary": [],
        }
    },
    # 廊坊新闻网
    {
        "platformName": "廊坊新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.lfnews.cn/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@id='portal_block_3_content']//a"],
        # 轮播信息
        "banner_news": [
            "//div[@class='swiper-wrapper']/div[@class='swiper-slide']/a | //div[@class='swiper-wrapper']/div[@class='swiper-slide swiper-slide-visible swiper-slide-active']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='klp_swplist001']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='daohang']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+.php.*"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//header[@class='atc_header']/h1/text()", },

            ],
            "content": [
                {"xpath": "//td[@id='article_content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='atc_meta atc_pcmeta']/span[3]/text()",
                },
            ],
            "pubTime": [{"xpath": "//div[@class='atc_meta atc_pcmeta']/span[@class='item'][2]", },
                        {"xpath": "//div[@class='atc_meta atc_pcmeta']/span[2]/text()"}],

            "authors": [{"xpath": "//div[@class='atc_meta atc_pcmeta']/span[1]/text()"}],
            "summary": [{"xpath": "//div[@class='view_con']/p/text()"}],
        }
    },
    # 和合承德网(可删)
    {
        "platformName": "和合承德网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.hehechengde.cn/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": ['//div[@class="block-head-news"]//a'],
        # 轮播信息
        "banner_news": ["//div[@class='slider has-dots']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ['//div[@class="col-top-right"]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ["//div[@class='main-nav']/div/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\d+/\d+.html$",
            r"https?://[\w\-\.]+/\w+/\w+/\d{4,}-\d{2,}-\d{2,}/\d+.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='section-title mt20']/h1/text()", },

            ],
            "content": [
                {"xpath": "//div[@id='text']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='info mt10']/span/a/text()",
                },
                {
                    "xpath": "//div[@class='info mt10']/span[contains(text(), '来源：')]/text()",
                    "regex": r"来源[: ：]\s*?(.*)$"

                }
            ],
            "pubTime": [{"xpath": "//div[@class='info mt10']/span/em/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 廊坊日报
    {
        "platformName": "廊坊日报",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://lfrbs.gov.010lf.com/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='swiper-wrapper']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='newslist-1']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='w1000 clearfix']/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.].*",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='hd']/h1/text()", },

            ],
            "content": [
                {"xpath": "//div[@class='bd']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='source fl']/text()",
                    "regex": r"来源[: ：]\s*?(.*)$"
                },

            ],
            "pubTime": [{"xpath": "//div[@class='date fl']/span/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 廊坊传媒网
    {
        "platformName": "廊坊传媒网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.lfcmw.com/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='auto tl']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='bd']/ul/li/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='ul fd']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']/div[@class='auto']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2,}/\w+_\d+.html$",
            r"https?://[\w\-\.]+/\w+/\w+/\d{4,}-\d{2,}/\d{2,}/\w+_\d+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='detail-h']/h1/text() | //div[@class='detail-h']/h2/text()", },

            ],
            "content": [
                {"xpath": "//div[@class='detail-d']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='detail-h']/p/span[1]/text()",
                    "regex": r"来源[: ：]\s*?(.*)"
                },

            ],
            "pubTime": [{"xpath": "//div[@class='detail-h']/p/span[2]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },

    # 1/15 13 90
    # 衡水市政府网1
    {
        "platformName": "衡水市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.hengshui.gov.cn/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='index_new_all_top']/a"],
        # 轮播信息
        "banner_news": ["//ul[@class='pic']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='action_nav2']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='hd']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w{3,}/\d{4,}/\d+/\d{2,}/\w{3,}_\d{2,}_\d{2,}.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='nr']/h2/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='nr_P']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='nr_center']/span[contains(text(), '来源')]/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='nr_center']/span[contains(text(), '发布日期')]/text()",
                    "regex": r"发布日期[: ：]\s*?(.*)$",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 衡水新闻网1
    {
        "platformName": "衡水新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.hsrb.com.cn/a/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='intou']/li/a"],
        # 轮播信息
        "banner_news": ["//ul[@id='slides']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@id='zy_obj0']/li/a | //div[@id='zy_obj1']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//table[@class='ttt']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w{4,}/\w{4,}/\d{4,}/\d{4,}/\d{6,}.html$",
            r"https?://[\w\-\.]+/\w+/\w{4,}/\w{4,}/\d{6,}.html$",
            r"https?://[\w\-\.]+/\w+/\w{4,}/\d+/\d{4,}/\d{4,}/\d{6,}.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@align='center']/h2/text()", },

            ],
            "content": [
                {"xpath": "//td[@class='a14-25']/cms-content", },
                {"xpath": "//td[@class='a14-25']/p", },
                {"xpath": "//td[@class='a14-25']/div[@style='text-align: center;']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='info']/text()[3]",
                },

            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='info']/text()[2]"
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 衡水广播电视网
    {
        "platformName": "衡水广播电视网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.hsrtv.cn/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],  # 无
        # 轮播信息
        "banner_news": [],  # js
        # 轮播旁边新闻
        "banner_news_side": ["//div[@id='MODBLK_1677']/div[1]/div[1]/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='navigation']/li/span/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.].*"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='artview_title']/text()", },

            ],
            "content": [
                {"xpath": "//div[@id='artview_content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='artview_info']/text()[3]",
                    "regex": r"来源[: ：]\s*?(.*)发布时间."
                },

            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='artview_info']/text()[3]",
                    "regex": r"发布时间[: ：]\s*?(.*)"
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 千龙网
    {
        "platformName": "千龙网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.qianlong.com/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='headline']/div/div/a"],
        # 轮播信息
        "banner_news": ["//a[@class='carousel-tit']"],
        # ["//div[@class='swiper-container top_swiper swiper-container-initialized swiper-container-horizontal']/div/div[@class='swiper-slide']/a | //div[@class='swiper-container top_swiper swiper-container-initialized swiper-container-horizontal']/div/div[@class='swiper-slide swiper-slide-prev']/a | //div[@class='swiper-container top_swiper swiper-container-initialized swiper-container-horizontal']/div/div[@class='swiper-slide swiper-slide-active']/a | //div[@class='swiper-container top_swiper swiper-container-initialized swiper-container-horizontal']/div/div[@class='swiper-slide swiper-slide-next']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='recommend hidden-desktop visible-lg']/div/a"],  # 无
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav_main']/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d{4,}/\d{4,}/\d{7,}.shtml$",
            r"https?://[\w\-\.]+thread-.*html"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1/text()", },
                {"xpath": "//div[@class='title']/text()"},

            ],
            "content": [
                {"xpath": "//div[@class='z_cen_box f_size_2 article-content']", },
                {"xpath": "//div[@class='article-content']"}
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='row']/a/text()",
                },
                {
                    "xpath": "//span[@class='source']"
                }

            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='row']/span/text()",
                },
                {
                    "xpath": "//span[@class='pubDate']/text()"
                },
                {
                    "xpath": "//span[@class='mr10']/text()"
                }
            ],
            "authors": [
                {
                    "xpath": "//div[@class='z_cen_bj']/span[contains(text(), '作者')]/text()",
                    "regex": r"作者[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='z_cen_bj']/span[contains(text(), '责任编辑')]/text()",
                    "regex": r"责任编辑[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//p[@class='editor'][contains(text(), '责任编辑：')]/span/text()"
                }
            ],
            "summary": [],
        }
    },
    # 北晚新视觉
    {
        "platformName": "北晚新视觉",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.takefoto.cn/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],  # 无
        # 轮播信息
        "banner_news": ["//div[@id='slider']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='reporter']/li/a[2]"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/viewnews-\d{7,}.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class='arc_title page_w mb20']/text()", },
                {"xpath": "//h2[@class='viewTitle']/text()"}
            ],
            "content": [
                {"xpath": "//div[@id='post']", },

            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='time-source']/span/a/text()",
                },
                {
                    "xpath": "//div[@class='content']/h4/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='time-source']/span[1]/text()",
                },
                {
                    "xpath": "//p[@class='time_source']/span/text()",
                    "regex": r"发布日期[: ：]\s*?(.*)$",
                }
            ],
            "authors": [
                {
                    "xpath": "//div[@class='time-source']/span[contains(text(), '编辑')]/text()",
                    "regex": r"编辑[: ：]\s*?(.*)$",
                },
            ],
            "summary": [{"xpath": "//p[@class='arc_lead']/text()"}],
        }
    },
    # 北京网1(使用代理访问比较慢)
    {
        "platformName": "北京网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.ibjw.cn/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='bj_img']/a"],
        # 轮播信息
        "banner_news": ["//div[@id='focus']/ul/li/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='bjcon']/div[@class='bj_con'][1]/div[@class='bj_con_c']/ul/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='bj_hend']/ul/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/news/\d{6}.htm$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='con_title']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='con_con']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='con_time']/text()",
                    "regex": r"来源[: ：]\s*?(.*)更新时间.",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='con_time']/text()",
                    "regex": r"更新时间[: ：]\s*?(.*)\s*?阅读.*",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中国文明网北京
    {
        "platformName": "中国文明网北京",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://bj.wenming.cn/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='hLine_Cont fl']//a"],
        # 轮播信息
        "banner_news": ["//ul[@class='new_S_ul new_S_ul_id1 clearfix']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='new_I_list']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='headMenu_bg comWidth clearfix']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w{2,}/\w{2,}/\d{6}/t\d{8}_\d{7,}.shtml$",
            r"https?://[\w\-\.]+/\w{2,}/\d{6}/t\d{8}_\d{7,}.shtml$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='title_tex']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='TRS_Editor']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@id='time_tex']/text()[2]",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@id='time_tex']/text()[1]",
                },
            ],
            "authors": [
                {
                    "xpath": "//div[@class='editor_tex']/text()",
                },
            ],
            "summary": [],
        }
    },
    # 新农村商报网
    {
        "platformName": "新农村商报网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.xncsb.cn/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@id='toutiao']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='pics']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@id='rowlwft-news']/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='xnc-nav']/div/div[@class='nav1']/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/newsf/\d{6}.htm$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@id='newstitle']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='zw']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@id='newsinfo']/span[2]/text()",
                    "regex": r"来 源[: ：]\s*?(.*)$",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//div[@id='newsinfo']/span[1]/text()",
                    "regex": r"时间[: ：]\s*?(.*)$",
                }
            ],
            "authors": [
                {
                    "xpath": "//div[@class='bianji'][1]/p/text()",
                    "regex": r"责编[: ：]\s*?(.*)]$",
                }
            ],
            "summary": [],
        }
    },
    # 天津市政府网
    {
        "platformName": "天津市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.tj.gov.cn/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@id='headNews']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='box_img']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='tab-details']/div/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav-box']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w{2,}/\w{4,}/\d{6}/t\d{8,}_\d{7}.html$",
            r"https?://[\w\-\.]+/\w{4}/\w{6,}/\d{4}\w{5}/\d{6}/t\d{8,}_\d{7}.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='qt-title']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='xw-txt']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='p-title']/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class='p-title p-fbsj']/text()",
                    "regex": r"发布时间[: ：]\s*?(.*)$",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 天津市卫生健康委1
    {
        "platformName": "天津市卫生健康委",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://wsjk.tj.gov.cn/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],  # 无
        # 轮播信息
        "banner_news": ["//div[@class='bd']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='tab-details']/div/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='zxxx']/div/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w{2,}\d{4}/\w{4,}\d{4,}/\d{6}/t\d{8}_\d{7}.html$",
            r"https?://[\w\-\.]+/ZTZL1/ZTZL750.*.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='pages']/h3/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='page_content Clear']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='page_date Clear']/div[2]/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='page_date Clear']/div[1]//text()",
                    "regex": r"发布日期[: ：]\s*?(.*)$",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 津滨网
    {
        "platformName": "津滨网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.tjbh.com/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='row']/div[@class='col-md-11']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='carousel-inner']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@id='myTabContent']/div[@id='home']/div[@class='list-group-items']/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='col-md-12 bgblue']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/c/\d{4}-\d{2}-\d{2}/\d{6}.shtml$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class='text-center']/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='cons']", },
                {"xpath": "//div[@class='item active']"},
                {"xpath": "//div[@class='m-lg']"}
            ],
            "pubSource": [
                {
                    "xpath": "//p[@class='text-center']/text()",
                    "regex": r"稿源[: ：]\s*?(.*)编辑.",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//p[@class='text-center']/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",
                }
            ],
            "authors": [
            ],
            "summary": [],
        }
    },
    # 天津广播电视台
    {
        "platformName": "天津广播电视台",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://tjtv.enorth.com.cn/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],  # 无
        # 轮播信息
        "banner_news": ["//div[@id='fc']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//td[@class='zi14 hanggao30']//a"],
        # 导航信息
        "channel_info_xpath": ["//td[@class='p12']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/system/\d{4}/\d{2}/\d{2}/\d{9}.shtml$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//td[@class='hei201']/text()", },
                {"xpath": "//h2[@class='col-sm-12']/text()", },
                {"xpath": "//div[@align='center']/h1/text()", },

            ],
            "content": [
                {"xpath": "//td[@class='zi14 hanggao30']", },
                {"xpath": "//div[@class='content']"},
                {"xpath": "//td[@class='p14']"}
            ],
            "pubSource": [
                {
                    "xpath": "//td[@class='yansehui jiacu']/text()",
                    "regex": r"\s*?稿源[: ：]\s*?(\w+)$",
                },
                {
                    "xpath": "//p[@class='col-sm-6 info']/span[contains(text(), '来源：')]/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//font[@class='p12']//text()",
                    "regex": r"稿源[: ：]\s*?(.*)编辑.",
                }

            ],
            "pubTime": [
                {
                    "xpath": "//div[@align='center']/font[@class='p12']/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",
                },
                {
                    "xpath": "//td[@class='yansehui jiacu']/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",
                },
                {
                    "xpath": "//p[@class='col-sm-6 info']/span/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})",
                },
                {
                    "xpath": "//font[@class='p12']//text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",
                }
            ],
            "authors": [
                {
                    "xpath": "//p[@class='col-sm-6 info']/span[contains(text(), '作者：')]/text()",
                    "regex": r"作者[: ：]\s*(.*)$",
                },
            ],
            "summary": [],
        }
    },
    # 上海市新闻办1
    {
        "platformName": "上海市新闻办",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.shio.gov.cn/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],  # 无
        # 轮播信息
        "banner_news": ["//div[@id='D1pic1']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@id='tabbox2']//a | //div[@id='tabbox1']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/sh/xwb/.*.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='ivs_title']/text()", },
            ],

            "content": [
                {"xpath": "//div[@id='ivs_content'] | //div[@id='ivs_player']", },
            ],

            "pubSource": [
                {
                    "xpath": "//p[@class='ly']/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                },
            ],

            "pubTime": [
                {
                    "xpath": "//p[@class='info']/text()",
                },
            ],

            "authors": [
            ],
            "summary": [],
        }
    },

    # 1/16 14 90
    # 黑龙江政府网
    {
        "platformName": "黑龙江政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.hlj.gov.cn/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],  # 无
        # 轮播信息
        "banner_news": [
            "//div[@id='swiper-container-p2']/div/div[@class='swiper-slide']/a | //div[@id='swiper-container-p2']/div/div[@class='swiper-slide swiper-slide-visible swiper-slide-active']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@id='list2']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='w1000 nav white clearfix']/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/n200/\d{4}/\d{4}/c\d{2,}-\d{8}.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='clearfix w1000 text_title']/h1/text()", },
            ],

            "content": [
                {"xpath": "//div[@class='box_con']", },
            ],

            "pubSource": [
                {
                    "xpath": "//div[@class='box01']//text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                },
            ],

            "pubTime": [
                {
                    "xpath": "//div[@class='box01']//text()",
                    "regex": r"(\d{4}年\d{1,2}月\d{1,2}日\d{1,2}:\d{1,2})"
                },
            ],

            "authors": [
            ],
            "summary": [],
        }
    },
    # 黑龙江网络广播电视台
    {
        "platformName": "黑龙江网络广播电视台",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.hljtv.com/",
        # 可无
        "cookie": "Hm_lvt_3fb9c5ab2bdc88d8a2e0980e99bee01d=1610713302; UM_distinctid=17705fe831b9da-0d70620ab932d8-171d4b58-fa000-17705fe831c6d0; zycna=BgNW2dnzRXcBAXf4cBE9UwWp; Hm_lpvt_3fb9c5ab2bdc88d8a2e0980e99bee01d=1610846972; CNZZDATA1265765445=271378681-1610710058-%7C1610844778",
        # 首页头条新闻
        "headline_news": ["//p[@class='ptd-title']/a"],
        # 轮播信息
        "banner_news": ["//div[@class='cell_6078_ clearfix']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//p[@class='ptd-title']/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='cell_6070_']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w{4,}/\w{6,}\d+/\d{4}-\d{2,}-\d{2}/\d{6,}.shtml$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1/text()", },
            ],

            "content": [
                {"xpath": "//div[@class='article-main']", },
                {"xpath": "//div[@class='gallery-main clearfix']"}
            ],

            "pubSource": [
                {
                    "xpath": "//span[@class='origin']/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                },
            ],

            "pubTime": [
                {
                    "xpath": "//span[@class='time']/text()",
                },
            ],

            "authors": [
            ],
            "summary": [],
        }
    },
    # 哈尔滨新闻网
    {
        "platformName": "哈尔滨新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://news.my399.com/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],  # 无
        # 轮播信息
        "banner_news": ["//div[@id='cnu_focus']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='s32']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='t5']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w{4,}/content/\d{4}-\d{2}/\d{2}/content_\d{7,}.htm$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//span[@class='n8']/text()", },
            ],

            "content": [
                {"xpath": "//div[@id='newscontent']", },
            ],

            "pubSource": [
                {
                    "xpath": "//span[@class='n10']/text()",
                },
            ],

            "pubTime": [
                {
                    "xpath": "//span[@class='n10']/span/text()",
                },
            ],

            "authors": [
            ],
            "summary": [],
        }
    },
    # 齐齐哈尔新闻网
    {
        "platformName": "齐齐哈尔新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.qqhrnews.com/",
        # 可无
        "cookie": "__tins__18973979=%7B%22sid%22%3A%201610765080990%2C%20%22vd%22%3A%201%2C%20%22expires%22%3A%201610766880990%7D; __51cke__=; __51laig__=1; Hm_lvt_f8809d1838401514fc88eaa5623b4d92=1610765081; Hm_lpvt_f8809d1838401514fc88eaa5623b4d92=1610765081",
        # 首页头条新闻
        "headline_news": ["//ul[@class='list-group m0 gundong']/li/a"],
        # 轮播信息
        "banner_news": [],  # js
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='col-lg-6 jnribikan']/ul[@class='list-group']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='z-nav row cl']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/bendixinwen/.*.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@name='title']/text()", },
                {"xpath": "//div[@class='piccontext']/h2/text()"}
            ],

            "content": [
                {"xpath": "//div[@class='TRS_Editor']/span"},
                {"xpath": "//div[@class='TRS_Editor']", },
            ],

            "pubSource": [
                {
                    "xpath": "//span[@id='ilaiyuan']/text()",
                },
            ],

            "pubTime": [
                {
                    "xpath": "//span[@id='idate']/text()",
                },
            ],

            "authors": [
            ],
            "summary": [],
        }
    },
    # 佳木斯日报新闻网
    {
        "platformName": "佳木斯日报新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.jmsxww.com/",
        # 可无
        "cookie": "zycna=CLcSj2fzHuIBAXf4cBHGllhH; lc=ABA8018EC729082A538A2C42F9721B29",
        # 首页头条新闻
        "headline_news": ["//div[@class='tout']/div[@class='con']/div[@class='left']/a"],
        # 轮播信息
        "banner_news": ["//div[@class='right']//div[@class='swiper-wrapper']//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='list-img']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='bottom1']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/index.php\?m=content&c=index&a=show&catid=.*"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='Article']/h1/text()", },
            ],

            "content": [
                {"xpath": "//div[@class='content']", },
                {"xpath": "//div[@class='cont']"}
            ],

            "pubSource": [
                {
                    "xpath": "//div[@class='time']/span[2]/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                },
            ],

            "pubTime": [
                {
                    "xpath": "//div[@class='time']/span[1]/text()",
                },
            ],

            "authors": [],
            "summary": [],
        }
    },

    # 佳木斯市政府网
    {
        "platformName": "佳木斯市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.jms.gov.cn/html/index/index.html",
        # 可无
        "cookie": "JSESSIONID=8B4856E4129250BB99CB59113D1BABEB; _gscu_527698695=108528932vvny660; _gscbrs_527698695=1; _gscs_527698695=10852893aqfl7w60|pv:1",
        # 首页头条新闻
        "headline_news": ["//div[@class='jms_newstitle']/a"],
        # 轮播信息
        "banner_news": ["//div[@id='fc']//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@id='tagaContent0']//a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='jms_navul']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/html/.*.html$",
            # r"https?://[\w\-\.]+/zwgk/html/.*.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='jms_contentT']/h1/text()", },

            ],

            "content": [
                {"xpath": "//div[@id='zoom']", },
            ],

            "pubSource": [
                {
                    "xpath": "//ul[@class='jms_contentUL']/li/text()",
                    "regex": r"来源\s*?(.*)$",
                },
            ],

            "pubTime": [
                {
                    "xpath": "//ul[@class='jms_contentUL']/li/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})"
                },
            ],

            "authors": [
            ],
            "summary": [],
        }
    },

    # 大庆日报
    {
        "platformName": "大庆日报",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.dqdaily.com/",
        # 可无
        "cookie": "Qs_lvt_52062=1610854660; _ga=GA1.2.1025554506.1610854661; _gid=GA1.2.403214475.1610854661; Hm_lvt_094102ec75c9a49b0e3a764b9ec1c875=1610854661; SSCSum=4; Qs_pv_52062=1023737578732775400%2C861308115458984300; Hm_lvt_fc36ca611428cc148cf2ee1da05c1b56=1610854844; zycna=Dm5Epm6OWsUBAXf4cBEg6b6r; Hm_lpvt_094102ec75c9a49b0e3a764b9ec1c875=1610864923; Hm_lpvt_fc36ca611428cc148cf2ee1da05c1b56=1610864925",
        # 首页头条新闻
        "headline_news": ["//div[@class='a1 overflow']//a"],
        # 轮播信息
        "banner_news": ["//div[@id='slide_x']/div[@class='box']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='nr1']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav f14px overflow cWhite']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d{4}-\d{2}/\d{2}/content_\d{7}.htm$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class='cBlack']/text()", },
            ],

            "content": [
                {"xpath": "//div[@class='overflow cCGray zhengwen']", },
            ],

            "pubSource": [
                {
                    "xpath": "//div[@class='f12px cTGray margin10']/text()",
                    "regex": r"来源[: ：]\s*?(.*)编辑.",
                },
            ],

            "pubTime": [
                {
                    "xpath": "//div[@class='f12px cTGray margin10']/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})"
                },
            ],

            "authors": [
                {
                    "xpath": "//div[@class='f12px cTGray margin10']/text()",
                    "regex": r"编辑[: ：]\s*?(.*)$",
                },
            ],
            "summary": [],
        }
    },

    # 鸡西新闻网
    {
        "platformName": "鸡西新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://jixi.dbw.cn/",
        # 可无
        "cookie": "wdcid=2a7619e4324f8871; wdlast=1610868139; zycna=DzkkH/W8XbEBAXf4cBGhY1dG",
        # 首页头条新闻
        "headline_news": ["//th[@class='title_sl_16h30']/span[@class='title_sl_14h24']//a"],
        # 轮播信息
        "banner_news": [],
        # 轮播旁边新闻
        "banner_news_side": ["//td[@class='title_sl_16h24']//td[@class='title_sl_14h24']//a"],
        # 导航信息
        "channel_info_xpath": ["//td[@class='title_sl_14h24']/table//table//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/system/\d{4}/\d{2}/\d{2}/\d{9}.shtml$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//span[@class='title_sl_16h30']//text()", },
                {"xpath": "//div[@class='title_sl_16h18']//text()"},
                {"xpath": "//th[@class='title_sl_40h60']/text()"}
            ],

            "content": [
                {"xpath": "//span[@class='title_sl_15h24']", },
            ],

            "pubSource": [
                {
                    "xpath": "//span[@class='style16']//text()",
                    "regex": r"来源[: ：]\s*?(.*)作者.",
                },
            ],

            "pubTime": [
                {
                    "xpath": "//span[@class='style11']/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2})"
                },
            ],

            "authors": [
                {
                    "xpath": "//span[@class='style16']/text()",
                    "regex": r"作者[: ：]\s*?(.*)$",
                },
            ],
            "summary": [],
        }
    },

    # 双鸭山新闻网
    {
        "platformName": "双鸭山新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://shuangyashan.dbw.cn/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='w1 hot_h11']//a"],
        # 轮播信息
        "banner_news": ["//ul[@class='bigUl']//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='r_h4']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav1 w1']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/system/\d{4}/\d{2}/\d{2}/\d{9}.shtml$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//table[@class='black14']//tr/td/div/font//text()", },
            ],

            "content": [
                {"xpath": "//table[@class='black14']", },  # 标题，正文，来源作者都在一个table里，区分不开
            ],

            "pubSource": [
                {
                    "xpath": "//span[@class='black12']/text()",
                    "regex": r"来源[: ：]\s*?(.*)编辑.",
                },
            ],

            "pubTime": [
                {
                    "xpath": "//table[@class='black14']//tr/td/div//text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})"
                },
            ],

            "authors": [
                {
                    "xpath": "//span[@class='black12']/text()",
                    "regex": r"作者[: ：]\s*?(.*)来源.",
                },
            ],
            "summary": [],
        }
    },

    # 双鸭山市政府网
    {
        "platformName": "双鸭山市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.shuangyashan.gov.cn/",
        # 可无
        "cookie": "JSESSIONID=AB81634055939A4E211BC24F253E15FD",
        # 首页头条新闻
        "headline_news": ["//div[@class='headlines']//a"],
        # 轮播信息
        "banner_news": ["//div[@id='D1pic1']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='fr']/div/ul[@class='newslist']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='mainNav']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/NewCMS/index/html/.*",
            r"https?://[\w\-\.]+/index/html/.*"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class='article_title']/text()", },
                {"xpath": "//h1[@class='rightTextTitle']/text()", },
                {"xpath": "//div[@class='container-bg col-12 padding']/h3/text()", },
                {"xpath": "//h3[@class='text-c pb-15 mb-20']/text()"}
            ],

            "content": [
                {"xpath": "//div[@class='article']/*[not(name()='h1') and not(name()='h2')]", },
                {"xpath": "//div[@class='container-bg col-12 padding']/span"},
            ],

            "pubSource": [
                {
                    "xpath": "//h2[@class='article_title2']/span/text()",
                    "regex": r"来源[: ：]\s*?(.*)时间.",
                },
            ],

            "pubTime": [
                {
                    "xpath": "//h2[@class='article_title2']/span/text()",
                    "regex": r"时间[: ：]\s*?(.*).0",
                },
            ],

            "authors": [
            ],
            "summary": [],
        }
    },

    # 伊春市政府网
    {
        "platformName": "伊春市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.yc.gov.cn/",
        # 可无
        "cookie": "wdcid=07625bb254e2d1eb; wdses=071a3fd2663b6a53; UM_distinctid=1770fb4be63483-0deb857856fbf8-171d4b58-fa000-1770fb4be64232; JSESSIONID=18958E7A6F0FE41F8674CE3E2D343481.web; CNZZDATA1255855019=1819066282-1610873829-%7C1610873829; wdlast=1610877353",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//ul[@class='focus-bar']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='newtabe']/div//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w{4}/\w{4}/\d{4}/\d{2}/\d{6}.html$",
            r"https?://[\w\-\.]+/\w{4}/\w{4,}/\w{3,}/\d{4}/\d{2}/\d{6}.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1/text()", },
            ],

            "content": [
                {"xpath": "//div[@class='con']", },
            ],

            "pubSource": [
                {
                    "xpath": "//div[@class='source']/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                },
            ],

            "pubTime": [
                {
                    "xpath": "//div[@class='source']/text()",
                    "regex": r"(\d{4}.\d{1,2}.\d{1,2})"
                },
            ],

            "authors": [
            ],
            "summary": [],
        }
    },

    # 伊春新闻网
    {
        "platformName": "伊春新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://yichun.dbw.cn/",
        # 可无
        "cookie": "wdcid=2a7619e4324f8871; zycna=DzkkH/W8XbEBAXf4cBGhY1dG; Hm_lvt_4cb6b42a89afc77bded7bd5076f69fa9=1610870898; Hm_lpvt_4cb6b42a89afc77bded7bd5076f69fa9=1610876189",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@id='ifocus_piclist']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='yw_r l f14_black']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='mainnav']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/system/\d{4}/\d{2}/\d{2}/\d{9}.shtml$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1/text()", },
                {"xpath": "//span[@class='f14_black']/text()"}
            ],

            "content": [
                {"xpath": "//span[@class='f14_black']", },
                {"xpath": "//div[@class='box']/span[@class='f14_black']"}
            ],

            "pubSource": [
                {
                    "xpath": "//div[@class='box10']/span[@class='f12_red']/text()",
                    "regex": r"来源[: ：]\s*?(.*)编辑.",
                },
                {
                    "xpath": "//div[@class='box']//span[@class='f12_red']/text()",
                    "regex": r"来源[: ：]\s*?(.*)编辑.",
                }
            ],

            "pubTime": [
                {
                    "xpath": "//div[@class='temarea_linebox textc']//text()",
                    "regex": r"(\d{4}年\d{1,2}月\d{1,2}日\s\d{1,2}:\d{1,2}:\d{1,2})"
                },
                {
                    "xpath": "//div[@class='textc f12_red']//text()",
                    "regex": r"(\d{4}年\d{1,2}月\d{1,2}日\s\d{1,2}:\d{1,2}:\d{1,2})"

                }
            ],

            "authors": [
                {
                    "xpath": "//div[@class='box10']/span[@class='f12_red']/text()",
                    "regex": r"作者[: ：]\s*?(.*)来源.",
                },
                {
                    "xpath": "//div[@class='box']//span[@class='f12_red']/text()",
                    "regex": r"作者[: ：]\s*?(.*)来源.",
                }
            ],
            "summary": [],
        }
    },

    # 七台河市政府网
    {
        "platformName": "七台河市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.qth.gov.cn/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='bd']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='top']/table[3]//div[@id='szyw1']/table//tr[2]/td/table//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='navigation-v3 navtaba']/ul/li//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w{4,}/\w{4,}/\d{6}/t\d{8}_\d{3,}.htm$",
            r"https?://[\w\-\.]+/\w{4,}/\w{4,}/\w{3,}/\d{6}/t\d{8}_\d{3,}.htm$",
            r"https?://[\w\-\.]+/\w{4,}_\d{5,}/\w{4,}/\w{3,}/\d{6}/t\d{8}_\d{3,}.htm$",
            r"https?://[\w\-\.]+/\w{4,}_\d{5,}/\w{4,}/\d{6}/t\d{8}_\d{3,}.htm$",
            r"https?://[\w\-\.]+/\w{4,}/\w{4,}/\w{4,}/\d{4}/\d{2}/\d{6,}.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1/text()", },
                {"xpath": "//div[@class='dbt']/text()"},
            ],

            "content": [
                {"xpath": "//div[@class='Custom_UnionStyle']", },
                {"xpath": "//div[@class='TRS_Editor']//*[not(name()='style')]"}
            ],

            "pubSource": [
                {
                    "xpath": "/html//table[2]//tr[3]/td/table//tr[1]/td[1]//text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='jzsj']/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                }
            ],

            "pubTime": [
                {
                    "xpath": "/html//table[2]//tr[3]/td/table//tr[1]/td[1]//text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2})"
                },
                {
                    "xpath": "//div[@class='jzsj']/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2})",
                }
            ],

            "authors": [
            ],
            "summary": [],
        }
    },

    # 鹤岗新闻网
    {
        "platformName": "鹤岗新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://hegangnews.dbw.cn/",
        # 可无
        "cookie": "wdcid=2a7619e4324f8871; zycna=DzkkH/W8XbEBAXf4cBGhY1dG; Hm_lvt_4cb6b42a89afc77bded7bd5076f69fa9=1610870898; _gscu_1681584908=108865006exz9n75; _gscbrs_1681584908=1; Hm_lpvt_4cb6b42a89afc77bded7bd5076f69fa9=1610886522; _gscs_1681584908=1088650062sd5875|pv:2; wdlast=1610886522",
        # 首页头条新闻
        "headline_news": ["//div[@id='demo1']//a"],
        # 轮播信息
        "banner_news": ["//div[@id='focus']/div[@class='pic']//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='list']/ul//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='nav']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/system/\d{4}/\d{2}/\d{2}/\d{9}.shtml$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1/text()", },
            ],

            "content": [
                {"xpath": "//div[@class='news']", },
            ],

            "pubSource": [
                {
                    "xpath": "//h6/text()",
                    "regex": r"来源[: ：]\s*?(.*)编辑.",
                },
            ],

            "pubTime": [
                {
                    "xpath": "//div[@class='tem_wwwbox txtc gray']/text()",
                    "regex": r"(\d{4}年\d{1,2}月\d{1,2}日\s\d{1,2}:\d{1,2}:\d{1,2})"
                },
            ],

            "authors": [
                {
                    "xpath": "//h6/text()",
                    "regex": r"编辑[: ：]\s*?(.*)$",
                },
            ],
            "summary": [],
        }
    },

    # 1/20 9
    # 七台河新闻网(不要)
    {
        "platformName": "七台河新闻网",
        "sourceProvince": "黑龙江省",
        "sourceCity": "七台河市",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.qthnews.org.cn/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//td[@class='STYLE91']/a"],
        # 轮播信息
        "banner_news": ["//ul[@id='conScroll_100004767']/div/div[1]/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//span[@class='STYLE94']/a"],
        # 导航信息
        "channel_info_xpath": ["//td[@class='STYLE13']/table//tr/td/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w{4,}/system/\d{4}/\d{2}/\d{2}/\d{9}.shtml$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//td[@class='heiti20 STYLE112 zi12 STYLE114']/text()", },
                {"xpath": "//td[@class='heiti20 STYLE112 zi12 zi12 zi12 STYLE114']//text()"},
                {"xpath": "//div[@class='STYLE59 zhuti']//text()"},
                {"xpath": "//div[@class='heiti20 STYLE59']/text() | //div[@class='zi18']/text()"}
            ],

            "content": [
                {"xpath": "//td[@class='zi14']", },
                {"xpath": "//td[@class='zi16']"},
            ],

            "pubSource": [
                # {
                #     #稿源：七台河新闻网　作者：李凤茹 李想　2018/05/30　编辑：陈荣娣
                #     #稿源：七台河新闻网 2018/05/30　编辑：陈荣娣
                # 两种情况，取稿源不安全
                #     "xpath": "//span[@class='STYLE112']/text()",
                #     "regex": r"稿源[: ：]\s*?(.*?)",
                # },
                {
                    "xpath": "//span[@id='source_baidu'][1]/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                }
            ],

            "pubTime": [
                {
                    "xpath": "//span[@class='STYLE112']/text()",
                    "regex": r"(\d{4}/\d{1,2}/\d{1,2})"
                },
                {
                    "xpath": "//span[@id='pubtime_baidu']/text()"
                }
            ],
            "channel": [{"xpath": "//span[@class='cms_block_span']/a[2]/text()", }, ],
            "authors": [
                {
                    "xpath": "//span[@class='STYLE112']/text()",
                    "regex": r"编辑[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//span[@id='editor_baidu']/text()",
                    "regex": r"编辑[: ：]\s*?(.*)$",
                }
            ],
            "summary": [],
        }
    },

    # 中国文明网黑龙江
    {
        "platformName": "中国文明网黑龙江",
        "sourceProvince": "黑龙江省",
        "sourceCity": "黑龙江省",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://hlj.wenming.cn/",
        # 可无
        "cookie": "UM_distinctid=17704b5a0f89c-03a7890b899265-171d4b58-fa000-17704b5a0f97d3; wdcid=40756524da03987d; Hm_lvt_3bdce7455c04dfb8cf1a26c3ac808bea=1610710707; Hm_lpvt_3bdce7455c04dfb8cf1a26c3ac808bea=1610710707",
        # 首页头条新闻
        "headline_news": ["/html/body/table[3]//tr[1]/td[2]/table//tr//a"],
        # 轮播信息
        "banner_news": ["//div[@id='focus']//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='ywlist']//a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='navli']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w{4,}\d+/\d{6}/t\d{8}_\d{7}.htm$",
            r"https?://[\w\-\.]+/\w{4,}/\d{6}/t\d{8}_\d{7}.htm$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//span[@class='newsh']//text()", },
            ],

            "content": [
                {"xpath": "//div[@class='TRS_Editor']/div/div[@class='TRS_Editor']", },
            ],

            "pubSource": [
                {
                    "xpath": "/html//table[3]//tr[2]/td/table//tr[2]//text()",
                    "regex": r"稿件来源[: ：]\s*?(.*)$",
                },
            ],

            "pubTime": [
                {
                    "xpath": "/html//table[3]//tr[2]/td/table//tr[2]//text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2})",
                },
            ],
            "channel": [{"xpath": "/html/body/table[3]//tr[1]/td//a[2]/text()", }, ],
            "authors": [
                {
                    "xpath": "//td[@class=' xwnr']//td/text()",
                    "regex": r"责任编辑[: ：]\s*?(.*)$",

                }
            ],
            "summary": [],
        }
    },

    # 黑河市政府网
    {
        "platformName": "黑河市政府网",
        "sourceProvince": "黑龙江省",
        "sourceCity": "黑河市",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.heihe.gov.cn/",
        # 可无
        "cookie": "JSESSIONID=D2FD57763EB89EC2AC2E45997C89B65E",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@id='KSS_content']//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='news-con']/ul[@class='gg-list']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='nav-menu']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/info/\d{4}/\d{6}.htm$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='content-title']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='vsb_content_2']", },
                {"xpath": "//div[@id='vsb_content']"},
                {"xpath": "//div[@id='vsb_content_6']"},
                {"xpath": "//div[@id='vsb_content_1001']"}
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='date']/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='date']/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})"
                },
            ],
            "channel": [{"xpath": "//div[@class='position']/h5/a[2]/text()", }, ],
            "authors": [
            ],
            "summary": [],
        }
    },

    # 绥化新闻网
    {
        "platformName": "绥化新闻网",
        "sourceProvince": "黑龙江省",
        "sourceCity": "绥化市",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://suihua.dbw.cn/",
        # 可无
        "cookie": "wdcid=2a7619e4324f8871; zycna=DzkkH/W8XbEBAXf4cBGhY1dG; Hm_lvt_4cb6b42a89afc77bded7bd5076f69fa9=1610870898",
        # 首页头条新闻
        "headline_news": ["//div[@class='fu-toutiao']//a"],
        # 轮播信息
        "banner_news": ["//div[@id='D1pic1']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='news-right']/div/ul//a"],
        # 导航信息
        "channel_info_xpath": ["//table[@class='top2']//tr/td/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/system/\d{4}/\d{2}/\d{2}/\d{9}.shtml$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1/text()", },
                {"xpath": "//div[@class='tit']/text()"}
            ],
            "content": [
                {"xpath": "//div[@id='zoom']", },
                {"xpath": "//td[@class='black14']"}
            ],

            "pubSource": [
                {
                    "xpath": "//div[@class='post_source']/text()",
                    "regex": r"来源[: ：]\s*?(.*)\d{4,}.*",
                },
                {
                    "xpath": "//td[@class='blue12']/text()",
                    "regex": r"来源[: ：]\s*?(.*)编辑",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='post_source']/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})"
                },
                {
                    "xpath": "//div[@class='blue12']/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})"
                }
            ],
            "channel": [{"xpath": "//div[@class='bc_main']/a[last()]/text()", }, ],
            "authors": [
                {
                    "xpath": "//div[@class='editor']/text()",
                    "regex": r"编辑[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//td[@class='blue12']/text()",
                    "regex": r"编辑[: ：]\s*?(.*)$",
                }
            ],
            "summary": [],
        }
    },

    # 大兴安岭日报
    {
        "platformName": "大兴安岭日报",
        "sourceProvince": "黑龙江省",
        "sourceCity": "大兴安岭地区",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.dxalrb.org.cn/",
        # 可无
        "cookie": "PHPSESSID=atbqot10shgl0jbs452vkaucp7; _gscu_1813631601=11121585h33l7e17; _gscbrs_1813631601=1; Hm_lvt_10ae61601bc47db6fdd13323f396a728=1611121586; zycna=HlRuULJ6ECABAXf4cBEH9bv4; _gscs_1813631601=11121585lnj78z17|pv:4; Hm_lpvt_10ae61601bc47db6fdd13323f396a728=1611121639",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='home_topics']/ul/li/div[@class='pic']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='loop']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/show/\d{5}.html.*"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='news_show']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='intro']", },
            ],

            "pubSource": [],  # 无
            "pubTime": [
                {
                    "xpath": "//div[@class='info']/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2})"
                },
            ],
            "channel": [{"xpath": "//ol/li[2]//text()", }, ],
            "authors": [],
            "summary": [],
        }
    },

    # 大兴安岭政府网
    {
        "platformName": "大兴安岭政府网",
        "sourceProvince": "黑龙江省",
        "sourceCity": "大兴安岭地区",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 2,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.dxal.gov.cn/",
        # 可无
        "cookie": "__RequestVerificationToken=qwk9UphHHfSJjkrj_1Hb9PyacvPj9JGNgV19HRRr5bTTOq56vQHp8Km4zGeflf8zfA08aUyP7yTQUcukK9emZS5P6SC-VlD875F82n1yN_Q1; ASP.NET_SessionId=eri3a2fqumqnfjlzqjxgpjrf; PowerLeaveSitePrompts=NoShow; PowerUniqueVisitor=43a2246f-1856-45e4-b438-65eae9d02b0e_2021%2F1%2F20%200%3A00%3A00; showGuide=true",
        # 首页头条新闻
        "headline_news": ["//div[@class='con']/div/a"],
        # 轮播信息
        "banner_news": ["//div[@id='focusHome']/div/div/ul/li/div[@class='pic']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='infoList']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@id='mainNav']/li/h3/a"],
        # 详情链接。
        "doc_links": [
            # r"https?://[\w\-\.]+/\w{4}/\w{4}/content_\d{5}",
            r"https?://[\w\-\.]+/.*/content_\d{5}",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h2[@class='title']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='conTxt']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='property']//text()",
                    "regex": r"来源[: ：]\s*?(.*)发布时间",
                },
            ],

            "pubTime": [
                {
                    "xpath": "//div[@class='property']//text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",
                },
            ],
            "channel": [{"xpath": "//div[@class='path1']/a[2]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },

    # 中国民委
    {
        "platformName": "中国民委",
        "sourceProvince": "",
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
        "start_url": "https://www.neac.gov.cn/",
        "cookie": "zh_choose=s; yfx_c_g_u_id_10005996=_ck21012016355112131485843331031; yfx_f_l_v_t_10005996=f_t_1611131751211__r_t_1611131751211__v_t_1611131751211__r_c_0",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": [
            "//div[@class='slidesjs-control']/div[@class='item slidesjs-slide']/div[@class='pannel-image']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='mwyw']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav w1200']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/seac/\w{4,}/\d{6}/\d{7}.shtml$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//p[@class='p1 wzxsbt']/text()", },
                {"xpath": "//p[@class='p1']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='p3']", },
            ],
            "pubSource": [
                {
                    "xpath": "//p[@class='p2']//text()",
                    "regex": r"来源[: ：]\s*?(.*)字号.",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//p[@class='p2']//text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2})"
                },
                {
                    "xpath": "//p[@class='p2']//text()",
                    "regex": r"(\d{4}/\d{1,2}/\d{1,2})"
                },
            ],
            "channel": [{"xpath": "//div[@class='BreadcrumbNav']/p/a[2]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },

    # 中国铁路总公司
    {
        "platformName": "中国铁路总公司",
        "sourceProvince": "",
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
        "start_url": "http://www.china-railway.com.cn/",
        "cookie": "zh_choose=n",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//ul[@class='swiper_menu clearfix']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='reports_lists']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='nav_menu clearfix']/li[1]/a | //ul[@class='nav_menu clearfix']/li/ul//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w{4,}/\w{4,}/\d{6}/t\d{8}_\d{6}.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='article_title']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='TRS_Editor']", },
            ],
            "pubSource": [],
            "pubTime": [
                {
                    "xpath": "//div[@class='source']//text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2})"
                },
            ],
            "channel": [{"xpath": "//div[@class='position1']/span/a[2]//text()", }, ],
            "authors": [],
            "summary": [],
        }
    },

    # 中国水利部
    {
        "platformName": "中国水利部",
        "sourceProvince": "",
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
        "start_url": "http://www.mwr.gov.cn/",
        "cookie": "zhuzhan=44186949; uid=user; __FT10000001=2021-1-20-17-20-29; __NRU10000001=1611134429461; __RT10000001=2021-1-20-17-20-29",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@id='area_tpxw']/ul[@class='clearfix']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@id='area_szyw']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w{2,}/\w{4,}/\d{6}/t\d{8}_\d{7}.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='TRS_Editor']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='fl']/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class='fl']/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2})"
                },
            ],
            "channel": [{"xpath": "//div[@class='nav_layered']/span/a[2]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },

    # 中央政府驻港联络办
    {
        "platformName": "中央政府驻港联络办",
        "sourceProvince": "",
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
        "start_url": "http://www.locpg.gov.cn/",
        "cookie": "wdcid=18bf72c0ebcc3194; wdlast=1611146270",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='swiper-wrapper']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='jj_right_list']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@id='topnav']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/jsdt/\d{4}-\d{2}/\d{2}/c_\d{10}.htm$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='info domPC']/text()",
                    "regex": r"来源[: ：]\s*?(.*)发布时间.",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='info domPC']/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2})"
                },
            ],
            "channel": [{"xpath": "//div[@class='domPC']/a/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    
    
    #1/21 15
    #中国载人航天
    {
        "platformName": "中国载人航天",
        "sourceProvince": "",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cmse.gov.cn/",
        # 可无
        "cookie": "__FT10000001=2021-1-21-8-24-34; __NRU10000001=1611188674590; __RT10000001=2021-1-21-8-24-34",
        # 首页头条新闻
        "headline_news": ["//ul[@class='indexXwzxBox']/li/a"],
        # 轮播信息
        "banner_news": ["//div[@class='bd']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='zhxwUl']/li//a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@id='daohang1']/li//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w{4}/\w{4}/\d{6}/t\d{8}_\d{5}.html$",
            r"https?://[\w\-\.]+/\w{4}/\d{6}/t\d{8}_\d{5}.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='title']/text()", },
                {"xpath": "//h2[@class='hdjl_zbxq_bt_title']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='TRS_Editor']", },
                {"xpath": "//div[@class='content']"}
            ],

            "pubSource": [
                {
                    "xpath": "//div[@class='source']//text()",
                    "regex": r"信息来源[: ：]\s*?(.*)$",
                },
            ],

            "pubTime": [
                {
                    "xpath": "//div[@class='pubDate']//text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2})",
                },
            ],
            "channel": [{"xpath": "//div[@class='mbx pc_none']/div[@class='mbxBox']/a[2]/text()", }, ],
            "authors": [
            ],
            "summary": [],
        }
    },
    #中国侨网
    {
        "platformName": "中国侨网",
        "sourceProvince": "",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.chinaqw.com/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@id='gdt']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@id='myTabhd_dd_Content0']/div[@class='new_top_p']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='qw_nav']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w{2,}/\d{4}/\d{2}-\d{2}/\d{6}.shtml$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1//text()", },
                {"xpath": "//div[@id='mian']/div/i[@class='title']/text()"}
            ],
            "content": [
                {"xpath": "//div[@class='left_ph'] | //div[@class='left_pt'] | //div[@class='left_zw']", },
                {"xpath": "//div[@id='cont_show']/div[@class='zxians']"}
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='left-t']/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='left-time']/div[@class='left-t']/a[1]/text()",
                }
            ],

            "pubTime": [
                {
                    "xpath": "//div[@class='left-t']/text()",
                    "regex": r"(\d{4}年\d{1,2}月\d{1,2}日\s\d{1,2}:\d{1,2})"
                },
            ],
            "channel": [
                {"xpath": "//div[@class='qw_listmbx']/a[last()]/text()", },
            ],
            "authors": [
            ],
            "summary": [],
        }
    },
    #正义网
    {
        "platformName": "正义网",
        "sourceProvince": "",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.jcrb.com/",
        # 可无
        "cookie": "_trs_uv=kk69711z_539_hj2e; _trs_ua_s_1=kk69711y_539_cfge; Hm_lvt_f90fd9516b719f9d87860fd9946f3c44=1611197170; Hm_lpvt_f90fd9516b719f9d87860fd9946f3c44=1611197170; wdcid=782649934abec360; wdlast=1611197170; wdses=3ee86187c8142506",
        # 首页头条新闻
        "headline_news": ["//div[@class='tout']/div[@class='TRS_Editor']//a"],
        # 轮播信息
        "banner_news": ["//div[@id='D1pic1']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='jjL']/div[@class='TRS_Editor']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+.*/t\d{8}_\d{7}.shtml$",
            r"https?://[\w\-\.]+.*/t\d{8}_\d{7}.html"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1/text()", },
                {"xpath": "//td[@class='wzbt']/text()"},
                {"xpath": "//div[@class='artile']/text()"}
            ],
            "content": [
                {"xpath": "//div[@id='fontzoom']", },
                {"xpath": "//video[@class='cj_shipingkuan']"},
                {"xpath": "//div[@class='TRS_Editor']"}
            ],
            "pubSource": [
                {
                    "xpath": "//span[@id='source_baidu']/text()",
                    "regex": r"新闻来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//td[@class='w14']//text()",
                    "regex": r"新闻来源[: ：]\s*?(.*)$",
                },
            ],

            "pubTime": [
                {
                    "xpath": "//span[@id='pubtime_baidu']/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})"
                },
                {
                    "xpath": "//td[@class='w14']//text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})"
                },
            ],
            "channel": [
                {"xpath": "//div[@class='curpage']/a[last()-1]/text()", },
            ],
            "authors": [
            ],
            "summary": [],
        }
    },
    #人民论坛网
    {
        "platformName": "人民论坛网",
        "sourceProvince": "",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.rmlt.com.cn/",
        # 可无
        "cookie": "Hm_lvt_321c97f9d02ec221cbdca88b0717bc77=1611205550; Hm_lpvt_321c97f9d02ec221cbdca88b0717bc77=1611205550",
        # 首页头条新闻
        "headline_news": ["//div[@class='gdtt-tit']//a"],
        # 轮播信息
        "banner_news": ["//ul[@class='imgs']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='bd']/ul/li/h3/a"],
        # 导航信息
        "channel_info_xpath": ["//nav[@class='column']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d{4}/\d{4}/\d{6}.shtml$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1/text()", },
                {"xpath": "//h2/text()"}
            ],
            "content": [
                {"xpath": "//p[@class='describe'] | //div[@class='addon-video mod-video'] | //div[@class='article-content fontSizeSmall BSHARE_POP']", },
                {"xpath": "//video[@id='cmstop_video_']"}
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='source']//text()",
                },
                {
                    "xpath": "//span[@class='editors f-l']/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class='date']/text()",
                },
                {
                    "xpath": "//span[@class='date f-l']/text()"
                }
            ],
            "channel": [
                {
                    "xpath": "//div[@class='crumb column mar-t-10']/a[2]/text()",
                },
                {
                    "xpath": "//div[@class='crumb column mar-t-10']/a[2]/text()"
                }
            ],
            "authors": [
                {
                    "xpath": "//span[@class='editors']/text()",
                },
                {
                    "xpath": "//span[@class='editors f-r']/text()",
                    "regex": r"责任编辑[: ：]\s*?(.*)$",
                }
            ],
            "summary": [],
        }
    },
    #理论网
    {
        "platformName": "理论网",
        "sourceProvince": "",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cntheory.com/",
        # 可无
        "cookie": "ASP.NET_SessionId=ywhqr5uten2pymfuwietyx55; UM_distinctid=177237490f53e3-03fd7d05b335eb-6915227c-fa000-177237490f66aa; CNZZDATA5156191=cnzz_eid%3D915267240-1611207107-%26ntime%3D1611207107",
        # 首页头条新闻
        "headline_news": ["//td[@class='font_50']/a | //td[@class='font_22']/a"],
        # 轮播信息
        "banner_news": ["//div[@id='imgplayer']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='font_24 icon7']/a | //div[@class='gray1']/div/a"],
        # 导航信息
        "channel_info_xpath": ["//table[@class='font_18 white b']//tr/td[1]/a | //td[@class='xian_gray']/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/zydx/\d{4}-\d{2}/.*.html$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='font_36']//text()", },
            ],
            "content": [
                {"xpath": "//div[@class='font_16']", },
            ],
            "pubSource": [
                {
                    "xpath": "//table[@class='ke-zeroborder'][1]//table[@class='ke-zeroborder'][2]//tr/td/table//tr/td[1]/text()",
                    "regex": r"来源[: ：]\s*?(.*)作者.",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//table[@class='ke-zeroborder'][1]//table[@class='ke-zeroborder'][2]//tr/td/table//tr/td[1]/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})"
                },
            ],
            "channel": [
                {
                    "xpath": "//td[@class='icon15 gray font_16']/a[2]/text()",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    #理论中国网
    {
        "platformName": "理论中国网",
        "sourceProvince": "",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.theorychina.org/",
        # 可无
        "cookie": "route=0a2e7c5af5ea9f492cc64f2d2834e0d2; 170_vq=1; UM_distinctid=177239b4ff49c-07401518b006c9-6915227c-fa000-177239b4ff524d; CNZZDATA4378561=cnzz_eid%3D777455720-1611205828-%26ntime%3D1611205828",
        # 首页头条新闻
        "headline_news": ["//div[@class='toutiao']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='swiper-wrapper']/div[@class='swiper-slide']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='focus_right']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='p1_nav']/ul/li//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/c/\d{4}-\d{2}-\d{2}/\d{7}.shtml$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='body']", },
            ],
            "pubSource": [
                {
                    "xpath": "//p[@class='art_info']/text()",
                    "regex": r"来源[: ：]\s*?(.*)\d{4,}.*",
                },
                {
                    "xpath": "//p[@class='art_info']/text()",
                    "regex": r"来源[: ：]\s*?(.*)|.",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//p[@class='art_info']/text()",
                    "regex": r"发布时间[: ：]\s*?(.*)|.",
                },
            ],
            "channel": [
                {
                    "xpath": "//div[@class='bread']/a[2]/text()",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    #中国领导网
    {
        "platformName": "中国领导网",
        "sourceProvince": "",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cnleaders.net/",
        # 可无
        "cookie": "UM_distinctid=17723c4807b2c3-0639418fc48306-6915227c-fa000-17723c4807c9c5; CNZZDATA1274023526=1160471010-1611209885-%7C1611209885",
        # 首页头条新闻
        "headline_news": ["//div[@class='today-hot wrapper']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='slideTxtBox clearfix']/div[@class='bd ']/div[@class='tempWrap']/ul[@class='clearfix']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='news-items']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='menu-%e8%8f%9c%e5%8d%95-container']/ul[@class='menu']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d{8}/\d{5}.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='article-title']/h2/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='article-txt']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='article-about']/span[2]/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='article-about']/span[1]/text()",
                    "regex": r"(\d{4}年\d{1,2}月\d{1,2}日\s\d{1,2}:\d{1,2})"
                },
            ],
            "channel": [],
            "authors": [],
            "summary": [],
        }
    },
    #中国社会新闻调查中心
    {
        "platformName": "中国社会新闻调查中心",
        "sourceProvince": "",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cnsnrc.com/",
        # 可无
        "cookie": "security_session_verify=d705a628e00188ff8ff81d2452997891",
        # 首页头条新闻
        "headline_news": ["//div[@class='headlines']//a"],
        # 轮播信息
        "banner_news": ["//div[@id='D1pic1']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='list14']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='layout_nav']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w{3,}/\w{4,}/\d{4}-\d{2}-\d{2}/\d{5}.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='bc']", },
                {"xpath": "//span[@id='zoom']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='lei']/div[1]//text()",
                    "regex": r"文章来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//p[@class='p3']//text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                },

            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='lei']/div[4]//text()",
                    "regex": r"发布时间[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//p[@class='p2']/text()",
                },
            ],
            "channel": [],
            "authors": [],
            "summary": [],
        }
    },
    #中国城市网
    {
        "platformName": "中国城市网",
        "sourceProvince": "",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.zgcsb.com/",
        # 可无
        "cookie": "Hm_lvt_6e33622d92353af0d6a1c322e4dd6b08=1611216090; Hm_lpvt_6e33622d92353af0d6a1c322e4dd6b08=1611216090; Hm_lvt_f5ed875547d72068304a52fea338456a=1611216090; Hm_lpvt_f5ed875547d72068304a52fea338456a=1611216090",
        # 首页头条新闻
        "headline_news": ["//div[@class='auto tl']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='bd']/ul/li/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='lx-lft']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='auto']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w{4,}/\d{4}-\d{2}/\d{2}/content_\d{6}.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='ft-tu']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='wznr clearfix']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='ft-tu']/span[2]//text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='ft-tu']/span[1]//text()",
                }
            ],
            "channel": [
                {
                    "xpath": "//div[@class='dht']/a[2]/text()",
                }
            ],
            "authors": [
                {
                    "xpath": "//div[@class='ft-tu']/span[3]//text()",
                    "regex": r"作者[: ：]\s*?(.*)$",
                }
            ],
            "summary": [],
        }
    },
    #人民铁道网
    {
        "platformName": "人民铁道网",
        "sourceProvince": "",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.peoplerail.com/rail/",
        # 可无
        "cookie": "UM_distinctid=17724090822149-0dbce2f917127f-6915227c-fa000-1772409082382b; CNZZDATA4695361=cnzz_eid%3D911335837-1611214998-%26ntime%3D1611214998; _ma_tk=z90qgu9mmafff94aqppx6udsct5hbp9o; _ma_is_new_u=1; _ma_starttm=1611217308452",
        # 首页头条新闻
        "headline_news": ["//div[@class='zt']/p/a"],
        # 轮播信息
        "banner_news": ["//ul[@id='slider']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='i-news fr']/div/ul//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='top w']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/rail/show-\d{4}-\d{6}-1.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='details-xq tc']/h2/text()", },
                {"xpath": "//div[@class='m_nr']/h3/text()", },
                {"xpath": "//div[@class='zwbt']/a/text()", },
                # {"xpath": "//div[@class='title']/p[@class='p p_s']/text()"}
            ],
            "content": [
                {"xpath": "//div[@class='details-xq tc']/*[not(name()='h2') and not(@class='shij')]", },
                {"xpath": "//div[@class='m_nr']/*[not(name()='h3') and not(@class='p_first')]", },
                {"xpath": "//div[@class='content1']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='shij']/span[2]//text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//p[@class='p_first']/span[2]/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='zwbt']/span[3]//text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='shij']/span[1]//text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})"
                },
                {
                    "xpath": "//p[@class='p_first']/span[1]//text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})"
                },
                {
                    "xpath": "//div[@class='zwbt']/span[1]//text()",
                }

            ],
            "channel": [
                {
                    "xpath": "//ul[@class='breadcrumb']/li[2]/a[1]/text()",
                },
                {
                    "xpath": "//ul[@class='breadcrumb fl']/li[2]/a[1]/text()",
                },
                {
                    "xpath": "//div[@class='xdh']/a[1]/text()",
                }
            ],
            "authors": [
                {
                    "xpath": "//div[@class='shij']/span[3]//text()",
                    "regex": r"作者[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//p[@class='p_first']/span[3]//text()",
                    "regex": r"作者[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='zwbt']/span[5]/text()",
                    "regex": r"编辑[: ：]\s*?(.*)$",
                },
            ],
            "summary": [],
        }
    },
    #中国劳动保障新闻网
    {
        "platformName": "中国劳动保障新闻网",
        "sourceProvince": "",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.clssn.com/html1/folder/0/1-1.htm",
        # 可无
        "cookie": "community=Home; Hm_lvt_ce46604a2bdbc2e1cc54f6d8a5acdf4e=1611220012; __utma=134973347.34852410.1611220012.1611220012.1611220012.1; __utmc=134973347; __utmz=134973347.1611220012.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; status=0; Hm_lpvt_ce46604a2bdbc2e1cc54f6d8a5acdf4e=1611220041; __utmb=134973347.3.10.1611220012",
        # 首页头条新闻
        "headline_news": ["//div[@class='top']//span[@id='VenuesIDPicture']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='FocusChart']/div[@id='NEWS_DIV']//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='position']/div//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='right']//td[@class='td01']/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/html1/report/\d{2}/\d{4}-1.htm$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='top']/span[@id='ReportIDname']/text()", },
            ],
            "content": [
                {"xpath": "//span[@id='ReportIDtext']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@id='ReportIDMediaName']/text()",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//span[@id='ReportIDIssueTime']/text()",
                },
            ],
            "channel": [
                {
                    "xpath": "//span[@id='PathID2']/a/text()",
                },
            ],
            "authors": [
                {
                    "xpath": "//span[@id='ReportIDeditmember']/text()",
                },
            ],
            "summary": [
                {"xpath": "//div[@id='daodu']"}
            ],
        }
    },
    #九三学社中央委员会
    {
        "platformName": "九三学社中央委员会",
        "sourceProvince": "",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.93.gov.cn/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='swiper-wrapper']/div/div[@class='img']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='news-tabCont']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='wrap flex-item navtitle']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w{4,}-\w{4,}/\d{6}.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='pageTitle text-center']/h2/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='text']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='pageTitle text-center']/ul/li[2]/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='pageTitle text-center']/ul/li[1]/text()",
                    "regex": r"发布日期[: ：]\s*?(.*)$",
                },
            ],
            "channel": [
                {
                    "xpath": "//div[@class='subNav wrap']/p/a[2]/text()",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    #中央联络部
    {
        "platformName": "中央联络部",
        "sourceProvince": "",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.idcpc.org.cn/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='content']/ul/li/a"],
        # 轮播信息
        "banner_news": ["//div[@class='swiper-container lunbox']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='top_list']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='zlb-nav']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+.*/\d{6}/t\d{6,}_\d{6,}.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='flag_div xl_div']/h3[@class='xl_h3']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='TRS_Editor']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='flag_div xl_div']/div[@class='flag_Div'][3]/span[2]/text()"
                }
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='flag_div xl_div']/div[@class='flag_Div'][1]/span[2]/text()",
                },
            ],
            "channel": [
                {
                    "xpath": "//ol[@class='breadcrumb baiBread hidden-sm hidden-xs']/li/a[4]/text()",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    #人民代表网
    {
        "platformName": "人民代表网",
        "sourceProvince": "",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.rmdbw.gov.cn/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//ul[@class='items']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='list']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='crjwz']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/html/\d{4}-\d{2}/\d{2}/content_\d{4,}.htm$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='title-p']/h2/text()",
                    "regex": r"来源[: ：]\s*?(.*)\d{4,}.*"
                }
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='title-p']/h2/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})"
                },
            ],
            "channel": [

            ],
            "authors": [],
            "summary": [],
        }
    },
    #人民中国
    {
        "platformName": "人民中国",
        "sourceProvince": "",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.peoplechina.com.cn/",
        # 可无
        "cookie": "wdcid=62f55c44342d28c5; wdses=3298ecbda335493f; wdlast=1611229739",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//ul[@class='slideshow']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='right_channel_content']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@id='nav']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+.*/\d{6}/t\d{8}_\d{9}.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='content_title']/h2//text()", },
                {"xpath": "//td[@class='m22b_655236']//text()"}
            ],
            "content": [
                {"xpath": "//div[@class='TRS_Editor']", },
            ],
            "pubSource": [
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='content_time']//text()",
                },
            ],
            "channel": [
                {
                    "xpath": "//div[@class='cur_page']/a[last()]//text()"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },

    #1.22  17
    #凤凰网天津
    {
        "platformName": "凤凰网天津",
        "sourceProvince": "天津市",
        "sourceCity": "天津市",
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
        "start_url": "http://tj.ifeng.com/",
        "cookie": "adb_isBlock=0; prov=cn0311; city=0311; weather_city=hb_sjz; region_ip=119.248.112.x; region_ver=1.2; userid=1611275859623_mfr5qk1347",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//ul[@class='picZA']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='yaowen']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='index_nav_box']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/c/.*",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {
                    "xpath": "//h1/text()",
                },
            ],
            "content": [
                {
                    "xpath": "//div[@class='text-3w2e3DBc']",
                },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='source-3w6NRfBZ']//text()",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//p[@class='time-1tZsY6dU']/span[1]/text()",
                },
            ],
            "channel": [
                {
                    "xpath": "//div[@class='breadcrumbs-1nBD5-4_']/span[2]/a/text()"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },

    #凤凰网河北
    {
        "platformName": "凤凰网河北",
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
        "start_url": "https://hebei.ifeng.com/",
        "cookie": "userid=1611275859623_mfr5qk1347; TEMP_USER_ID=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI2MDBhMjQ2NmE2NDQzIiwidGltZSI6MTYxMTI3NzQxNH0.wNIw5UpR28ZMd9yO1ezDAgpl6skXk_PWgKOMF3IqlnU; prov=cn0311; city=0311; weather_city=hb_sjz; region_ip=119.248.112.17; region_ver=1.30; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22%24device_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; vjuids=357311199.17727a427ac.0.7154cbce90398; vjlast=1611277805.1611277805.30; adb_isBlock=0",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@id='tabSlide']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='Firleft']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='col_nav']/ul[@class='clearfix']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/c/.*",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {
                    "xpath": "//h1/text()",
                },
            ],
            "content": [
                {
                    "xpath": "//div[@class='text-3w2e3DBc']",
                },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='source-3w6NRfBZ']//text()",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//p[@class='time-1tZsY6dU']/span[1]/text()",
                },
            ],
            "channel": [
                {
                    "xpath": "//div[@class='breadcrumbs-1nBD5-4_']/span[2]/a/text()"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },

    #凤凰网辽宁
    {
            "platformName": "凤凰网辽宁",
            "sourceProvince": "辽宁省",
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
            "start_url": "http://ln.ifeng.com/",
            "cookie": "userid=1611275859623_mfr5qk1347; TEMP_USER_ID=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI2MDBhMjQ2NmE2NDQzIiwidGltZSI6MTYxMTI3NzQxNH0.wNIw5UpR28ZMd9yO1ezDAgpl6skXk_PWgKOMF3IqlnU; prov=cn0311; city=0311; weather_city=hb_sjz; region_ip=119.248.112.17; region_ver=1.30; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22%24device_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; vjuids=357311199.17727a427ac.0.7154cbce90398; vjlast=1611277805.1611277805.30; adb_isBlock=0; prov=cn0311; city=0311; weather_city=hb_sjz; region_ip=119.248.112.x; region_ver=1.2",
            # 首页头条新闻
            "headline_news": [],
            # 轮播信息
            "banner_news": ["//ul[@class='picZA']/li/a"],
            # 轮播旁边新闻
            "banner_news_side": ["//ul[@class='yaowen']/li/a"],
            # 导航信息
            "channel_info_xpath": ["//div[@class='index_nav_box']/ul/li/a"],
            # 详情链接。
            "doc_links": [
                r"https?://[\w\-\.]+/c/.*",
            ],
            # 目标采集字段，成功时忽略后续模板。
            "fields": {
                "title": [
                    {
                        "xpath": "//h1/text()",
                    },
                ],
                "content": [
                    {
                        "xpath": "//div[@class='text-3w2e3DBc']",
                    },
                ],
                "pubSource": [
                    {
                        "xpath": "//span[@class='source-3w6NRfBZ']//text()",
                    }
                ],
                "pubTime": [
                    {
                        "xpath": "//p[@class='time-1tZsY6dU']/span[1]/text()",
                    },
                ],
                "channel": [
                    {
                        "xpath": "//div[@class='breadcrumbs-1nBD5-4_']/span[2]/a/text()"
                    }
                ],
                "authors": [],
                "summary": [],
            }
        },

    #凤凰网吉林
    {
                "platformName": "凤凰网吉林",
                "sourceProvince": "吉林省",
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
                "start_url": "http://jl.ifeng.com/",
                "cookie": "userid=1611275859623_mfr5qk1347; TEMP_USER_ID=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI2MDBhMjQ2NmE2NDQzIiwidGltZSI6MTYxMTI3NzQxNH0.wNIw5UpR28ZMd9yO1ezDAgpl6skXk_PWgKOMF3IqlnU; prov=cn0311; city=0311; weather_city=hb_sjz; region_ip=119.248.112.17; region_ver=1.30; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22%24device_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; vjuids=357311199.17727a427ac.0.7154cbce90398; vjlast=1611277805.1611277805.30; UM_distinctid=17727cafef3481-044a7f584d68ca-6915227c-fa000-17727cafef461e; CNZZDATA1257491987=1512320077-1611279230-%7C1611279230; adb_isBlock=0; prov=cn0311; city=0311; weather_city=hb_sjz; region_ip=119.248.112.x; region_ver=1.2",
                # 首页头条新闻
                "headline_news": [],
                # 轮播信息
                "banner_news": ["//div[@id='topPicMove']/ul[@class='picList']/li/a"],
                # 轮播旁边新闻
                "banner_news_side": ["//div[@class='box_01']/div//a"],
                # 导航信息
                "channel_info_xpath": ["//ul[@class='m_nav_list']/li/a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/c/.*",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {
                            "xpath": "//h1/text()",
                        },
                    ],
                    "content": [
                        {
                            "xpath": "//div[@class='text-3w2e3DBc']",
                        },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//span[@class='source-3w6NRfBZ']//text()",
                        }
                    ],
                    "pubTime": [
                        {
                            "xpath": "//p[@class='time-1tZsY6dU']/span[1]/text()",
                        },
                    ],
                    "channel": [
                        {
                            "xpath": "//div[@class='breadcrumbs-1nBD5-4_']/span[2]/a/text()"
                        }
                    ],
                    "authors": [],
                    "summary": [],
                }
            },

    #凤凰网江苏
    {
        "platformName": "凤凰网江苏",
        "sourceProvince": "江苏省",
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
        "start_url": "http://js.ifeng.com/",
        "cookie": "userid=1611275859623_mfr5qk1347; TEMP_USER_ID=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI2MDBhMjQ2NmE2NDQzIiwidGltZSI6MTYxMTI3NzQxNH0.wNIw5UpR28ZMd9yO1ezDAgpl6skXk_PWgKOMF3IqlnU; prov=cn0311; city=0311; weather_city=hb_sjz; region_ip=119.248.112.17; region_ver=1.30; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22%24device_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; vjuids=357311199.17727a427ac.0.7154cbce90398; vjlast=1611277805.1611277805.30; UM_distinctid=17727cafef3481-044a7f584d68ca-6915227c-fa000-17727cafef461e",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='ppt1_ul']/div/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='left_c f_l m_30']/div//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav_c m_0']/h2/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/a/\d{8}/\d{8}_0.shtml$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {
                    "xpath": "//h1/text()",
                },
            ],
            "content": [
                {
                    "xpath": "//div[@id='main_content']",
                },
                {
                    "xpath": "//div[@class='js_selection_area']"
                }
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='ss03']//text()",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class='ss01']//text()",
                },
            ],
            "channel": [
                {
                    "xpath": "//div[@class='theCurrent cDGray js_crumb']/a[2]/text()"
                }
            ],
            "authors": [
                {
                    "xpath": "//p[@class='iphone_none']/text()",
                    "regex": r"责任编辑[: ：]\s*?(.*)]$",
                }
            ],
            "summary": [],
        }
    },

    #凤凰网浙江
    {
                "platformName": "凤凰网浙江",
                "sourceProvince": "浙江省",
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
                "start_url": "http://zj.ifeng.com/",
                "cookie": "userid=1611275859623_mfr5qk1347; TEMP_USER_ID=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI2MDBhMjQ2NmE2NDQzIiwidGltZSI6MTYxMTI3NzQxNH0.wNIw5UpR28ZMd9yO1ezDAgpl6skXk_PWgKOMF3IqlnU; prov=cn0311; city=0311; weather_city=hb_sjz; region_ip=119.248.112.17; region_ver=1.30; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22%24device_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; vjuids=357311199.17727a427ac.0.7154cbce90398; vjlast=1611277805.1611277805.30; UM_distinctid=17727cafef3481-044a7f584d68ca-6915227c-fa000-17727cafef461e; adb_isBlock=0",
                # 首页头条新闻
                "headline_news": [],
                # 轮播信息
                "banner_news": ["//div[@id='main-footer-banner-boxs']/a"],
                # 轮播旁边新闻
                "banner_news_side": ["//div[@class='box_hots']//a"],
                # 导航信息
                "channel_info_xpath": ["//ul[@class='nav clearfix cg']/li/a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/c/.*",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {
                            "xpath": "//h1/text()",
                        },
                    ],
                    "content": [
                        {
                            "xpath": "//div[@class='text-3w2e3DBc']",
                        },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//span[@class='source-3w6NRfBZ']/a/text()",
                        }
                    ],
                    "pubTime": [
                        {
                            "xpath": "//p[@class='time-1tZsY6dU']/span[1]/text()",
                        },
                    ],
                    "channel": [
                        {
                            "xpath": "//div[@class='breadcrumbs-1nBD5-4_']/span[2]/a/text()"
                        }
                    ],
                    "authors": [],
                    "summary": [],
                }
            },

    #凤凰网安徽
    {
            "platformName": "凤凰网安徽",
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
            "start_url": "https://ah.ifeng.com/",
            "cookie": "userid=1611275859623_mfr5qk1347; TEMP_USER_ID=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI2MDBhMjQ2NmE2NDQzIiwidGltZSI6MTYxMTI3NzQxNH0.wNIw5UpR28ZMd9yO1ezDAgpl6skXk_PWgKOMF3IqlnU; prov=cn0311; city=0311; weather_city=hb_sjz; region_ip=119.248.112.17; region_ver=1.30; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22%24device_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; vjuids=357311199.17727a427ac.0.7154cbce90398; vjlast=1611277805.1611277805.30; UM_distinctid=17727cafef3481-044a7f584d68ca-6915227c-fa000-17727cafef461e; CNZZDATA1254680111=1775227485-1611279335-%7C1611279335; CNZZDATA1279403376=1144910924-1611281870-%7C1611281870; Hm_lvt_c1e42373bb9c6d135d90edf29b8fac65=1611282425; Hm_lpvt_c1e42373bb9c6d135d90edf29b8fac65=1611282425; adb_isBlock=0; prov=cn0311; city=0311; weather_city=hb_sjz; region_ip=119.248.112.x; region_ver=1.2",
            # 首页头条新闻
            "headline_news": ["//div[@class='toutiao']//a"],
            # 轮播信息
            "banner_news": ["//div[@id='mb-iboxs']/ul/li/a"],
            # 轮播旁边新闻
            "banner_news_side": ["//div[@class='list_tdnews']//a"],
            # 导航信息
            "channel_info_xpath": ["//div[@class='col_nav']/ul[@class='clearfix']/li/a"],
            # 详情链接。
            "doc_links": [
                r"https?://[\w\-\.]+/c/.*",
            ],
            # 目标采集字段，成功时忽略后续模板。
            "fields": {
                "title": [
                    {
                        "xpath": "//h1/text()",
                    },
                ],
                "content": [
                    {
                        "xpath": "//div[@class='text-3w2e3DBc']",
                    },
                ],
                "pubSource": [
                    {
                        "xpath": "//span[@class='source-3w6NRfBZ']/a/text()",
                    }
                ],
                "pubTime": [
                    {
                        "xpath": "//p[@class='time-1tZsY6dU']/span[1]/text()",
                    },
                ],
                "channel": [
                    {
                        "xpath": "//div[@class='breadcrumbs-1nBD5-4_']/span[2]/a/text()"
                    }
                ],
                "authors": [],
                "summary": [],
            }
        },

    #凤凰网江西
    {
            "platformName": "凤凰网江西",
            "sourceProvince": "江西省",
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
            "start_url": "https://jx.ifeng.com/",
            "cookie": "userid=1611275859623_mfr5qk1347; TEMP_USER_ID=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI2MDBhMjQ2NmE2NDQzIiwidGltZSI6MTYxMTI3NzQxNH0.wNIw5UpR28ZMd9yO1ezDAgpl6skXk_PWgKOMF3IqlnU; prov=cn0311; city=0311; weather_city=hb_sjz; region_ip=119.248.112.17; region_ver=1.30; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22%24device_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; vjuids=357311199.17727a427ac.0.7154cbce90398; vjlast=1611277805.1611277805.30; UM_distinctid=17727cafef3481-044a7f584d68ca-6915227c-fa000-17727cafef461e; Hm_lvt_c1e42373bb9c6d135d90edf29b8fac65=1611282425; Hm_lpvt_c1e42373bb9c6d135d90edf29b8fac65=1611282452; __gads=ID=fafdd603faa71ce5-222b6215cbc5001e:T=1611282834:RT=1611282834:S=ALNI_MbpoaGklu_XYIGwyUkTDp2KqKR04A; adb_isBlock=0; prov=cn0311; city=0311; weather_city=hb_sjz; region_ip=119.248.112.x; region_ver=1.2",
            # 首页头条新闻
            "headline_news": ["//div[@class='col_w1000 mt01 clearfix'][1]/div[@class='col_l']//a"],
            # 轮播信息
            "banner_news": ["//div[@class='fpic']/div/a"],
            # 轮播旁边新闻
            "banner_news_side": ["//div[@class='left_c3 left_c0 left_c1']/div[@class='box_hots']//a"],
            # 导航信息
            "channel_info_xpath": ["//div[@class='col_nav']/ul[@class='clearfix']/li/a"],
            # 详情链接。
            "doc_links": [
                r"https?://[\w\-\.]+/c/.*",
            ],
            # 目标采集字段，成功时忽略后续模板。
            "fields": {
                "title": [
                    {
                        "xpath": "//h1/text()",
                    },
                ],
                "content": [
                    {
                        "xpath": "//div[@class='text-3w2e3DBc']",
                    },
                    {
                        "xpath": "//table[@class='swiper_wrapper-GaGfr-O2']"
                    }
                ],
                "pubSource": [
                    {
                        "xpath": "//span[@class='source-3w6NRfBZ']/a/text()",
                    }
                ],
                "pubTime": [
                    {
                        "xpath": "//p[@class='time-1tZsY6dU']/span[1]/text()",
                    },
                ],
                "channel": [
                    {
                        "xpath": "//div[@class='breadcrumbs-1nBD5-4_']/span[2]/a/text()"
                    }
                ],
                "authors": [],
                "summary": [],
            }
        },

    #凤凰网山东
    {
            "platformName": "凤凰网山东",
            "sourceProvince": "山东省",
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
            "start_url": "https://sd.ifeng.com/",
            "cookie": "userid=1611275859623_mfr5qk1347; TEMP_USER_ID=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI2MDBhMjQ2NmE2NDQzIiwidGltZSI6MTYxMTI3NzQxNH0.wNIw5UpR28ZMd9yO1ezDAgpl6skXk_PWgKOMF3IqlnU; prov=cn0311; city=0311; weather_city=hb_sjz; region_ip=119.248.112.17; region_ver=1.30; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22%24device_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; vjuids=357311199.17727a427ac.0.7154cbce90398; vjlast=1611277805.1611277805.30; UM_distinctid=17727cafef3481-044a7f584d68ca-6915227c-fa000-17727cafef461e; Hm_lvt_c1e42373bb9c6d135d90edf29b8fac65=1611282425; Hm_lpvt_c1e42373bb9c6d135d90edf29b8fac65=1611282452; __gads=ID=fafdd603faa71ce5-222b6215cbc5001e:T=1611282834:RT=1611282834:S=ALNI_MbpoaGklu_XYIGwyUkTDp2KqKR04A; adb_isBlock=0",
            # 首页头条新闻
            "headline_news": [],
            # 轮播信息
            "banner_news": [],#iframe
            # 轮播旁边新闻
            "banner_news_side": ["//div[@class='col_l']/div[@class='box_01']/div[@class='box_hots']//a"],
            # 导航信息
            "channel_info_xpath": ["//div[@class='col_nav']/ul/li//a"],
            # 详情链接。
            "doc_links": [
                r"https?://[\w\-\.]+/c/.*",
            ],
            # 目标采集字段，成功时忽略后续模板。
            "fields": {
                "title": [
                    {
                        "xpath": "//h1/text()",
                    },
                ],
                "content": [
                    {
                        "xpath": "//div[@class='text-3w2e3DBc']",
                    },
                ],
                "pubSource": [
                    {
                        "xpath": "//span[@class='source-3w6NRfBZ']/a/text()",
                    }
                ],
                "pubTime": [
                    {
                        "xpath": "//p[@class='time-1tZsY6dU']/span[1]/text()",
                    },
                ],
                "channel": [
                    {
                        "xpath": "//div[@class='breadcrumbs-1nBD5-4_']/span[2]/a/text()"
                    }
                ],
                "authors": [],
                "summary": [],
            }
        },

    #凤凰网河南(首页内容js,不要)
    {
        "platformName": "凤凰网河南",
        "sourceProvince": "河南省",
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
        "start_url": "http://hn.ifeng.com/",
        "cookie": "userid=1611275859623_mfr5qk1347; TEMP_USER_ID=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI2MDBhMjQ2NmE2NDQzIiwidGltZSI6MTYxMTI3NzQxNH0.wNIw5UpR28ZMd9yO1ezDAgpl6skXk_PWgKOMF3IqlnU; prov=cn0311; city=0311; weather_city=hb_sjz; region_ip=119.248.112.17; region_ver=1.30; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22%24device_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; vjuids=357311199.17727a427ac.0.7154cbce90398; vjlast=1611277805.1611277805.30; UM_distinctid=17727cafef3481-044a7f584d68ca-6915227c-fa000-17727cafef461e; Hm_lvt_c1e42373bb9c6d135d90edf29b8fac65=1611282425; Hm_lpvt_c1e42373bb9c6d135d90edf29b8fac65=1611282452; __gads=ID=fafdd603faa71ce5-222b6215cbc5001e:T=1611282834:RT=1611282834:S=ALNI_MbpoaGklu_XYIGwyUkTDp2KqKR04A; prov=cn0311; city=0311; weather_city=hb_sjz; region_ver=1.2; CNZZDATA5636592=cnzz_eid%3D719624890-1611286385-%26ntime%3D1611286385; Hm_lvt_3cbccceddb735fe74dd8c771e1514568=1611287661; Hm_lpvt_3cbccceddb735fe74dd8c771e1514568=1611287661; region_ip=101.24.17.x; adb_isBlock=0",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": [
            "//div[@class='swiper-container']/div/div[@class='swiper-slide css_jdimg']/a | //div[@class='swiper-wrapper']/div[@class='swiper-slide css_jdimg swiper-slide-visible swiper-slide-active']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@id='cont_yaowen']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav-four']/ul[@class='nav-four-ul']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/c/.*",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {
                    "xpath": "//h1/text()",
                },
            ],
            "content": [
                {
                    "xpath": "//div[@class='text-3w2e3DBc']",
                },
                {
                    "xpath": "//div[@id='forAd']"
                }
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='source-3w6NRfBZ']/a/text()",
                },
                {
                    "xpath": "//div[@class='titL-36mV2OzS']/p/a/text()"
                },
                {
                    "xpath": "//div[@class='titL-1ZkkRt8v']/p/a/text()"
                },
                {
                    "xpath": "//span[@class='source-qK4Su0--']/a/text()"
                }

            ],
            "pubTime": [
                {
                    "xpath": "//p[@class='time-1tZsY6dU']/span[1]/text()",
                },
                {
                    "xpath": "//div[@class='titL-36mV2OzS']/p/span/text()"
                },
                {
                    "xpath": "//div[@class='titL-1ZkkRt8v']/p/span/text()"
                },
                {
                    "xpath": "//p[@class='time-1Mgp9W-1']/span[1]/text()"
                }
            ],
            "channel": [
                {
                    "xpath": "//div[@class='breadcrumbs-1nBD5-4_']/span[2]/a/text()"
                },
                {
                    "xpath": "//div[@class='speNav-O3KXDmLK']/span[2]/a/text()"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },

    #凤凰网湖北
    {
                "platformName": "凤凰网湖北",
                "sourceProvince": "湖北省",
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
                "start_url": "https://hb.ifeng.com/",
                "cookie": "userid=1611275859623_mfr5qk1347; TEMP_USER_ID=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI2MDBhMjQ2NmE2NDQzIiwidGltZSI6MTYxMTI3NzQxNH0.wNIw5UpR28ZMd9yO1ezDAgpl6skXk_PWgKOMF3IqlnU; prov=cn0311; city=0311; weather_city=hb_sjz; region_ip=119.248.112.17; region_ver=1.30; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22%24device_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; vjuids=357311199.17727a427ac.0.7154cbce90398; vjlast=1611277805.1611277805.30; UM_distinctid=17727cafef3481-044a7f584d68ca-6915227c-fa000-17727cafef461e; Hm_lvt_c1e42373bb9c6d135d90edf29b8fac65=1611282425; Hm_lpvt_c1e42373bb9c6d135d90edf29b8fac65=1611282452; __gads=ID=fafdd603faa71ce5-222b6215cbc5001e:T=1611282834:RT=1611282834:S=ALNI_MbpoaGklu_XYIGwyUkTDp2KqKR04A; Hm_lvt_d775ebc569d609e63f2a70e787932cd7=1611294058; Hm_lpvt_d775ebc569d609e63f2a70e787932cd7=1611294058; adb_isBlock=0; prov=cn0311; city=0311; weather_city=hb_sjz; region_ip=101.24.17.x; region_ver=1.2",
                # 首页头条新闻
                "headline_news": [],
                # 轮播信息
                "banner_news": ["//div[@id='mb-iboxs']/ul/li/a"],
                # 轮播旁边新闻
                "banner_news_side": ["//div[@class='box_01']/div//a"],
                # 导航信息
                "channel_info_xpath": ["//div[@class='col_nav']/ul[@class='clearfix']/li/a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/c/.*",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {
                            "xpath": "//h1/text()",
                        },
                        {
                            "xpath": "//div[@class='titlebox']/h3/text()"
                        }
                    ],
                    "content": [
                        {
                            "xpath": "//div[@class='text-3w2e3DBc']",
                        },
                        {
                            "xpath": "//div[@id='forAd']"
                        },
                        {
                            "xpath": "//div[@class='content']"
                        },
                        {
                            "xpath": "//div[@class='area1']"
                        }
                    ],
                    "pubSource": [
                        {
                            "xpath": "//span[@class='source-3w6NRfBZ']/a/text()",
                        },
                    ],
                    "pubTime": [
                        {
                            "xpath": "//p[@class='time-1tZsY6dU']/span[1]/text()",
                        },
                    ],
                    "channel": [
                        {
                            "xpath": "//div[@class='breadcrumbs-1nBD5-4_']/span[2]/a/text()"
                        },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },

    #凤凰网广东
    {
                "platformName": "凤凰网广东",
                "sourceProvince": "广东省",
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
                "start_url": "http://gd.ifeng.com/",
                "cookie": "userid=1611275859623_mfr5qk1347; TEMP_USER_ID=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI2MDBhMjQ2NmE2NDQzIiwidGltZSI6MTYxMTI3NzQxNH0.wNIw5UpR28ZMd9yO1ezDAgpl6skXk_PWgKOMF3IqlnU; prov=cn0311; city=0311; weather_city=hb_sjz; region_ip=119.248.112.17; region_ver=1.30; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22%24device_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; vjuids=357311199.17727a427ac.0.7154cbce90398; vjlast=1611277805.1611277805.30; UM_distinctid=17727cafef3481-044a7f584d68ca-6915227c-fa000-17727cafef461e; Hm_lvt_c1e42373bb9c6d135d90edf29b8fac65=1611282425; Hm_lpvt_c1e42373bb9c6d135d90edf29b8fac65=1611282452; __gads=ID=fafdd603faa71ce5-222b6215cbc5001e:T=1611282834:RT=1611282834:S=ALNI_MbpoaGklu_XYIGwyUkTDp2KqKR04A; adb_isBlock=0; prov=cn0311; city=0311; weather_city=hb_sjz; region_ip=101.24.17.x; region_ver=1.2",
                # 首页头条新闻
                "headline_news": [],
                # 轮播信息
                "banner_news": ["//div[@class='owl-wrapper']/div/a"],
                # 轮播旁边新闻
                "banner_news_side": ["//div[@id='headLineGuangdong']//a"],
                # 导航信息
                "channel_info_xpath": ["//ul[@class='clearfix']/li/a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/c/.*",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {
                            "xpath": "//h1/text()",
                        },
                        {
                            "xpath": "//h2[@class='title-14yWv8ay']/text()"
                        }
                    ],
                    "content": [
                        {
                            "xpath": "//div[@class='text-3w2e3DBc']",
                        },
                        {
                          "xpath": "//div[@id='forAd']"
                        },
                        {
                            "xpath": "//div[@class='smallFont-Z_OfA44W text-20BABGxP']"
                        },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//span[@class='source-3w6NRfBZ']/a/text()",
                        },
                        {
                            "xpath": "//span[@class='source-qK4Su0--']/a/text()"
                        }
                    ],
                    "pubTime": [
                        {
                            "xpath": "//p[@class='time-1tZsY6dU']/span[1]/text()",
                        },
                        {
                            "xpath": "//p[@class='time-1Mgp9W-1']/span[1]/text()"
                        },
                        {
                            "xpath": "//time[@class='time-M6w87NaQ']/text()"
                        }
                    ],
                    "channel": [
                        {
                            "xpath": "//div[@class='breadcrumbs-1nBD5-4_']/span[2]/a/text()"
                        },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },

    #凤凰网海南
    {
            "platformName": "凤凰网海南",
            "sourceProvince": "海南省",
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
            "start_url": "https://hainan.ifeng.com/",
            "cookie": "userid=1611275859623_mfr5qk1347; TEMP_USER_ID=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI2MDBhMjQ2NmE2NDQzIiwidGltZSI6MTYxMTI3NzQxNH0.wNIw5UpR28ZMd9yO1ezDAgpl6skXk_PWgKOMF3IqlnU; prov=cn0311; city=0311; weather_city=hb_sjz; region_ip=119.248.112.17; region_ver=1.30; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22%24device_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; vjuids=357311199.17727a427ac.0.7154cbce90398; vjlast=1611277805.1611277805.30; UM_distinctid=17727cafef3481-044a7f584d68ca-6915227c-fa000-17727cafef461e; Hm_lvt_c1e42373bb9c6d135d90edf29b8fac65=1611282425; Hm_lpvt_c1e42373bb9c6d135d90edf29b8fac65=1611282452; __gads=ID=fafdd603faa71ce5-222b6215cbc5001e:T=1611282834:RT=1611282834:S=ALNI_MbpoaGklu_XYIGwyUkTDp2KqKR04A; Hm_lvt_77aee6b00788fbf80395ebfa5f620f86=1611296961; Hm_lpvt_77aee6b00788fbf80395ebfa5f620f86=1611296961; CNZZDATA1254987826=1707077158-1611291636-%7C1611291636; adb_isBlock=0",
            # 首页头条新闻
            "headline_news": [],
            # 轮播信息
            "banner_news": ["//div[@id='mb-iboxs']/ul/li/a"],
            # 轮播旁边新闻
            "banner_news_side": ["//div[@class='box_01']/div[@class='box_hots']/h2/a | //div[@class='box_01']/div[@class='box_hots']/h3/a"],
            # 导航信息
            "channel_info_xpath": ["//ul[@class='clearfix']/li/a"],
            # 详情链接。
            "doc_links": [
                r"https?://[\w\-\.]+/c/.*",
            ],
            # 目标采集字段，成功时忽略后续模板。
            "fields": {
                "title": [
                    {
                        "xpath": "//h1/text()",
                    },
                ],
                "content": [
                    {
                        "xpath": "//div[@class='text-3w2e3DBc']",
                    },
                    {
                      "xpath": "//div[@id='forAd']"
                    },
                ],
                "pubSource": [
                    {
                        "xpath": "//span[@class='source-3w6NRfBZ']/a/text()",
                    },
                ],
                "pubTime": [
                    {
                        "xpath": "//p[@class='time-1tZsY6dU']/span[1]/text()",
                    },
                ],
                "channel": [
                    {
                        "xpath": "//div[@class='breadcrumbs-1nBD5-4_']/span[2]/a/text()"
                    },
                ],
                "authors": [],
                "summary": [],
            }
        },

    #凤凰网重庆
    {
                "platformName": "凤凰网重庆",
                "sourceProvince": "重庆省",
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
                "start_url": "https://cq.ifeng.com/",
                "cookie": "userid=1611275859623_mfr5qk1347; TEMP_USER_ID=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI2MDBhMjQ2NmE2NDQzIiwidGltZSI6MTYxMTI3NzQxNH0.wNIw5UpR28ZMd9yO1ezDAgpl6skXk_PWgKOMF3IqlnU; prov=cn0311; city=0311; weather_city=hb_sjz; region_ip=119.248.112.17; region_ver=1.30; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22%24device_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; vjuids=357311199.17727a427ac.0.7154cbce90398; vjlast=1611277805.1611277805.30; UM_distinctid=17727cafef3481-044a7f584d68ca-6915227c-fa000-17727cafef461e; Hm_lvt_c1e42373bb9c6d135d90edf29b8fac65=1611282425; Hm_lpvt_c1e42373bb9c6d135d90edf29b8fac65=1611282452; __gads=ID=fafdd603faa71ce5-222b6215cbc5001e:T=1611282834:RT=1611282834:S=ALNI_MbpoaGklu_XYIGwyUkTDp2KqKR04A; adb_isBlock=0",
                # 首页头条新闻
                "headline_news": [],
                # 轮播信息
                "banner_news": ["//div[@id='main-footer-banner-boxs']/a"],
                # 轮播旁边新闻
                "banner_news_side": ["//div[@class='box_01']/div[@class='box_hots']/h2/a | //div[@class='box_01']/div[@class='box_hots']/h3/a"],
                # 导航信息
                "channel_info_xpath": ["//ul[@class='clearfix']/li/a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/c/.*",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {
                            "xpath": "//h1/text()",
                        },
                    ],
                    "content": [
                        {
                            "xpath": "//div[@class='text-3w2e3DBc']",
                        },
                        {
                          "xpath": "//div[@id='forAd']"
                        },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//span[@class='source-3w6NRfBZ']/a/text()",
                        },
                    ],
                    "pubTime": [
                        {
                            "xpath": "//p[@class='time-1tZsY6dU']/span[1]/text()",
                        },
                    ],
                    "channel": [
                        {
                            "xpath": "//div[@class='breadcrumbs-1nBD5-4_']/span[2]/a/text()"
                        },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },

    #凤凰网陕西
    {
                "platformName": "凤凰网陕西",
                "sourceProvince": "陕西省",
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
                "start_url": "https://sn.ifeng.com/",
                "cookie": "userid=1611275859623_mfr5qk1347; TEMP_USER_ID=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI2MDBhMjQ2NmE2NDQzIiwidGltZSI6MTYxMTI3NzQxNH0.wNIw5UpR28ZMd9yO1ezDAgpl6skXk_PWgKOMF3IqlnU; prov=cn0311; city=0311; weather_city=hb_sjz; region_ip=119.248.112.17; region_ver=1.30; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22%24device_id%22%3A%22177279e370e35-03adc31fe01a29-6915227c-1024000-177279e370f186%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; vjuids=357311199.17727a427ac.0.7154cbce90398; vjlast=1611277805.1611277805.30; UM_distinctid=17727cafef3481-044a7f584d68ca-6915227c-fa000-17727cafef461e; Hm_lvt_c1e42373bb9c6d135d90edf29b8fac65=1611282425; Hm_lpvt_c1e42373bb9c6d135d90edf29b8fac65=1611282452; __gads=ID=fafdd603faa71ce5-222b6215cbc5001e:T=1611282834:RT=1611282834:S=ALNI_MbpoaGklu_XYIGwyUkTDp2KqKR04A; adb_isBlock=0; prov=cn0311; city=0311; weather_city=hb_sjz; region_ip=101.24.17.x; region_ver=1.2",
                # 首页头条新闻
                "headline_news": [],
                # 轮播信息
                "banner_news": ["//div[@class='swiper-wrapper']/div/a"],
                # 轮播旁边新闻
                "banner_news_side": ["//ul[@id='newslist']/li/a"],
                # 导航信息
                "channel_info_xpath": ["//ul[@class='clearfix']/li/a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/c/.*",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {
                            "xpath": "//h1/text()",
                        },
                    ],
                    "content": [
                        {
                            "xpath": "//div[@class='text-3w2e3DBc']",
                        },
                        {
                          "xpath": "//div[@id='forAd']"
                        },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//span[@class='source-3w6NRfBZ']/a/text()",
                        },
                    ],
                    "pubTime": [
                        {
                            "xpath": "//p[@class='time-1tZsY6dU']/span[1]/text()",
                        },
                    ],
                    "channel": [
                        {
                            "xpath": "//div[@class='breadcrumbs-1nBD5-4_']/span[2]/a/text()"
                        },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },

    #中国政府采购网
    {
                "platformName": "中国政府采购网",
                "sourceProvince": "",
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
                "start_url": "http://www.ccgp.gov.cn/",
                "cookie": "Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1611299685; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1611299685",
                # 首页头条新闻
                "headline_news": [],
                # 轮播信息
                "banner_news": ["//ul[@class='slides']/li//a"],
                # 轮播旁边新闻
                "banner_news_side": ["//div[@class='txtnews_list_contianer']/ul/li/a"],
                # 导航信息
                "channel_info_xpath": ["//ul[@class='v4incheadertop_nav_ls']/li/a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+.*/\d{6}/t\d{8}_\d{7,}.htm",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {
                            "xpath": "//h2[@class='tc']//text()",
                        },
                    ],
                    "content": [
                        {
                            "xpath": "//div[@class='vF_detail_content']",
                        },
                        {
                          "xpath": "//div[@class='rh_info']"
                        },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//span[@id='sourceName']/text()",
                        },
                    ],
                    "pubTime": [
                        {
                            "xpath": "//span[@id='pubTime']/text()",
                        },
                    ],
                    "channel": [
                        {
                            "xpath": "//div[@class='vF_deail_currentloc mt10']/p/a[2]/text()"
                        },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },

    #全国哲学社会科学规划办公室
    {
                "platformName": "全国哲学社会科学规划办公室",
                "sourceProvince": "",
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
                "start_url": "http://www.nopss.gov.cn/",
                "cookie": "wdcid=5bda367f30e54832; wdlast=1611302150; wdses=1315fc8216d5ee03",
                # 首页头条新闻
                "headline_news": ["//div[@class='w1000 p1']/h1/a | //div[@class='w1000 p1']/marquee/ul/li/a"],
                # 轮播信息
                "banner_news": ["//div[@class='swiper-wrapper']/div/a"],
                # 轮播旁边新闻
                "banner_news_side": ["//div[@class='p1-right-main']//a"],
                # 导航信息
                "channel_info_xpath": ["//ul[@class='w1000 clearfix nav_h']/li/a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/.*/\d{4}/\d{4}/c\d{6}-\d{8}.html$",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {
                            "xpath": "//h1//text()",
                        },
                    ],
                    "content": [
                        {
                            "xpath": "//div[@class='text_con clearfix ']",
                        },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//p[@class='author']/em[3]/a/text()",
                        },
                    ],
                    "pubTime": [
                        {
                            "xpath": "//p[@class='author']/em[2]/text()",
                        },
                    ],
                    "channel": [
                        {
                            "xpath": "//div[@class='clearfix path']/a[2]/text()"
                        },
                    ],
                    "authors": [
                        {
                            "xpath": "//div[@class='edit clearfix']/text()",
                            "regex": r"责编[: ：]\s*?(.*)\)$",
                        }
                    ],
                    "summary": [],
                }
            },

    #中科清研科学技术研究院（无发布时间）
    {
                "platformName": "中科清研科学技术研究院",
                "sourceProvince": "",
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
                "start_url": "http://www.cnian.org/",
                "cookie": 'attrAid=13484116; attrSiteId=0; attrSiteType=1; attrIsMobile=false; _jz_w_c="aid":13484116,"siteid":0,"siteType":1,"mobile":false; _cliid=fPlTXz6UFw-lhcP5; _lastEnterDay=2021-01-22; _siteStatId=1d12e1eb-6ebc-474e-9efd-5f4de5731e6f; _siteStatDay=20210122; _siteStatRedirectUv=redirectUv_13484116; _siteStatVisitorType=visitorType_13484116; _siteStatVisit=visit_13484116; _siteStatVisitTime=1611304621140; _checkSiteLvBrowser=true',
                # 首页头条新闻
                "headline_news": ["//div[@id='noticeMarquee373']//a"],
                # 轮播信息
                "banner_news": ["//a[@class='carousel-img']"],
                # 轮播旁边新闻
                "banner_news_side": ["//div[@class='formMiddleContent formMiddleContent341']//div[@topclassname='top1']//a"],
                # 导航信息
                "channel_info_xpath": ["//div[@class='itemContainer']/table//a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/h-nd-.*",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {
                            "xpath": "//h1//text()",
                        },
                    ],
                    "content": [
                        {
                            "xpath": "//div[@class='richContent richContent3']",
                        },
                        {
                            "xpath": "//div[@class='richContent  richContent3']",
                        },
                    ],
                    "pubSource": [

                    ],
                    "pubTime": [

                    ],
                    "channel": [

                    ],
                    "authors": [

                    ],
                    "summary": [],
                }
            },

    #1.23 9
    #中国文化和旅游部
    {
                    "platformName": "中国文化和旅游部",
                    "sourceProvince": "",
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
                    "start_url": "https://www.mct.gov.cn/",
                    "cookie": "",
                    # 首页头条新闻
                    "headline_news": [],
                    # 轮播信息
                    "banner_news": ["//div[@class='imgnew_img_list']/div//a"],
                    # 轮播旁边新闻
                    "banner_news_side": ["//ul[@class='govpushinfo150203']/li/a"],
                    # 导航信息
                    "channel_info_xpath": ["//ul[@class='nav']/li/a"],
                    # 详情链接。
                    "doc_links": [
                        r"https?://[\w\-\.]+/\w{4,}/\w{4,}/\d{6}/t\d{8}_\d{6}.htm$",
                        r"https?://[\w\-\.]+/\w{2,}/\w{2,}/\w{4,}/\d{6}/t\d{8}_\d{6}.html$"
                    ],
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {
                                "xpath": "//div[@class='sp_title']//text()",
                            },
                            {
                                "xpath": "//td[@class='title']/text()",
                            },
                            {
                                "xpath": "//div[@class='article oneColumn pub_border']/h1//text()",
                            },
                            {
                                "xpath": "//div[@class='ctitle']/h2//text()"
                            },
                            {
                                "xpath": "//div[@class='spbf-first-bt']/text()"
                            }
                        ],
                        "content": [
                            {
                                "xpath": "//div[@id='zoom']",
                            },
                            {
                                "xpath": "//div[@id='UCAP-CONTENT']",
                            },
                            {
                                "xpath": "//div[@class='gsj_htmlcon_bot']",
                            },
                            {
                                "xpath": "//div[@class='spbf-first-left']",
                            },
                        ],
                        "pubSource": [
                            {
                                "xpath": "//div[@class='sp_time']/font[2]/text()",
                                "regex": r"来源[: ：]\s*?(.*)$",
                            },
                            {
                                "xpath": "//div[@class='pages-date']/span/text()",
                                "regex": r"来源[: ：]\s*?(.*)$",
                            },
                        ],
                        "pubTime": [
                            {
                                "xpath": "//div[@class='sp_time']/font[1]/text()",
                                "regex": r"发布时间[: ：]\s*?(.*)$",
                            },
                            {
                                "xpath": "//div[@class='pages-date']/text()",
                                "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",
                            },
                            {
                                "xpath": "//p[@class='pubtime']/text()",
                                "regex": r"(\d{4}年\d{1,2}月\d{1,2}日)",
                            },
                            {
                                "xpath": "//div[@class='spbf-first-right-mc2']/text()",
                                "regex":  r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})"
                            }
                        ],
                        "channel": [
                            {
                                "xpath": "//div[@class='bt-position']/a[2]/text()"
                            },
                            {
                                "xpath": "//div[@class='BreadcrumbNav']/a[2]/text()"
                            },
                            {
                                "xpath": "//div[@class='mbx']/a[3]/text()"
                            },
                        ],
                        "authors": [
                            {
                                "xpath": "//div[@class='sp_time']/font[3]/text()",
                                "regex": r"编辑[: ：]\s*?(.*)$",
                            },
                        ],
                        "summary": [],
                    }
                },

    #中国民用航空西北地区管理局(总局详情js加载拿不到，分局没问题)
    {
                "platformName": "中国民用航空西北地区管理局",
                "sourceProvince": "",
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
                "start_url": "http://xb.caac.gov.cn/",
                "cookie": "__FT10000025=2021-1-23-9-56-50; __NRU10000025=1611367010901; __RT10000025=2021-1-23-9-56-50; Hm_lvt_ac569fd8898150f7fb87982e2d373611=1611367011; Hm_lpvt_ac569fd8898150f7fb87982e2d373611=1611367037",
                # 首页头条新闻
                "headline_news": [],
                # 轮播信息
                "banner_news": ["//div[@class='n_pic']/ul/li/a"],
                # 轮播旁边新闻
                "banner_news_side": ["//div[@id='sys_box2']/div//a"],
                # 导航信息
                "channel_info_xpath": ["//div[@class='nav']/ul//a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+/\w{2,}_\w{4,}/\w{2,}_\w{4,}/\d{6}/t\d{8}_\d{6}.html$",
                    r"https?://[\w\-\.]+/\w{4,}/\w{4,}/\d{6}/t\d{8}_\d{6}.html$"
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {
                            "xpath": "//div[@class='content_t']/text()",
                        },
                    ],
                    "content": [
                        {
                            "xpath": "//div[@class='TRS_Editor']",
                        },
                    ],
                    "pubSource": [
                        {
                            "xpath": "//span[@id='source']/text()",
                            "regex": r"来源[: ：]\s*?(.*)$",
                        },
                    ],
                    "pubTime": [
                        {
                            "xpath": "//div[@class='content_info']/span[2]/text()",
                        },
                    ],
                    "channel": [
                        {
                            "xpath": "//div[@class='path_bar']/a[2]/text()"
                        },
                    ],
                    "authors": [],
                    "summary": [],
                }
            },

    #国家市场监督管理局
    {
                    "platformName": "国家市场监督管理局",
                    "sourceProvince": "",
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
                    "start_url": "http://www.samr.gov.cn/",
                    "cookie": "wwwcookie=18205800; __jsluid_h=51bcf358c92802a4a14558066b017d92; UM_distinctid=1772d18f3b158a-0ab90779cb95df-6915227c-fa000-1772d18f3b2684; CNZZDATA1276383350=428143456-1611368110-%7C1611368110; yfx_c_g_u_id_10008476=_ck21012310354616337937467533361; yfx_f_l_v_t_10008476=f_t_1611369346575__r_t_1611369346575__v_t_1611369346575__r_c_0",
                    # 首页头条新闻
                    "headline_news": ["//div[@class='newbanner01']/a | //div[@class='samr-banner-text']//a"],
                    # 轮播信息
                    "banner_news": ["//div[@class='box01']/div/a"],
                    # 轮播旁边新闻
                    "banner_news_side": ["//div[@id='contentLeft-sy-gwy9_content']/ul//a"],
                    # 导航信息
                    "channel_info_xpath": ["//div[@class='navigation-v3']/ul/li/a"],
                    # 详情链接。
                    "doc_links": [
                        r"https?://[\w\-\.]+/\w{2,}/\w{2,}/\d{6}/t\d{8}_\d{6}.html$",
                        r"https?://[\w\-\.]+/wsbs/.*",
                    ],
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {
                                "xpath": "//li[@class='Three_xilan_03']//text()",
                            },
                            {
                                "xpath": "//div[@class='h-title']//text()"
                            },
                            {
                                "xpath": "//td[@colspan='2']/ul[@class='dw']/li[@class='Three_xilan01_02 Three_xilan01_0201']/text()"
                            }
                        ],
                        "content": [
                            {
                                "xpath": "//div[@class='TRS_Editor']",
                            },
                            {
                                "xpath": "//div[@id='detail']"
                            },
                            {
                                "xpath": "//div[@class='Three_xilan_07']"
                            }
                        ],
                        "pubSource": [
                            {
                                "xpath": "//li[@class='Three_xilan_04']/text()",
                                "regex": r"信息来源[: ：]\s*?(.*)$",
                            },
                            {
                                "xpath": "//span[@class='aticle-src']/text()",
                            },
                        ],
                        "pubTime": [
                            {
                                "xpath": "//li[@class='Three_xilan_04']/text()",
                                "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})"
                            },
                            {
                                "xpath": "//span[@class='h-time']/text()"
                            },
                            {
                                "xpath": "//div[@id='Three_xxgk_0203_content']/div[@id='printcont']/div[@class='Three_xilan_01']/div[@class='Three_xilan01_01']/table//tr[4]/td[2]/ul[@class='dw']/li[@class='Three_xilan01_02 Three_xilan01_0201']/text()"
                            }
                        ],
                        "channel": [
                            {
                                "xpath": "//div[@class='Second_banner']/ul/li/a[2]/text()"
                            },
                            {
                                "xpath": "//div[@class='news-position']/a[2]/text()"
                            }
                        ],
                        "authors": [],
                        "summary": [],
                    }
                },

    #台湾民主自治同盟
    {
                    "platformName": "台湾民主自治同盟",
                    "sourceProvince": "",
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
                    "start_url": "http://www.taimeng.org.cn/",
                    "cookie": "__jsluid_h=ecd4f3664216ce6bffdceec96edc816b; __jsluid_s=aa48d2e1f8f1c7aae800206f76ab4c71",
                    # 首页头条新闻
                    "headline_news": [],
                    # 轮播信息
                    "banner_news": ["//ul[@class='pic']/li/a"],
                    # 轮播旁边新闻
                    "banner_news_side": ["//ul[@class='tab']/li/a"],
                    # 导航信息
                    "channel_info_xpath": ["//ul[@class='menu']/li/div/a"],
                    # 详情链接。
                    "doc_links": [
                        r"https?://[\w\-\.]+.*/\d{6}/t\d{8}_\d{6}.htm$",
                    ],
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {
                                "xpath": "//h1[@class='title']/text()",
                            },
                            {
                                "xpath": "//td[@class='font14']/strong/text()"
                            }
                        ],
                        "content": [
                            {
                                "xpath": "//div[@id='font_size']",
                            },
                            {
                                "xpath": "//td[@id='div_zhengwen']",
                            },
                        ],
                        "pubSource": [
                            {
                                "xpath": "//div[@class='info']/span[1]/text()",
                                "regex": r"来源[: ：]\s*?(.*)$",
                            },
                        ],
                        "pubTime": [
                            {
                                "xpath": "//div[@class='info']/span[2]/text()",
                                "regex": r"日期[: ：]\s*?(.*)$",
                            },
                            {
                                "xpath": "//div[@class='bgbox']/div[@id='maincontent']/table//tr/td/table[2]//tr[2]/td/text()",
                                "regex": r"日期[: ：]\s*?(.*)$",
                            }
                        ],
                        "channel": [
                            {
                                "xpath": "//div[@class='crumbs']/a[2]/text()"
                            },
                            {
                                "xpath": "//td[@class='font14']/a[2]/text()"
                            },
                        ],
                        "authors": [],
                        "summary": [],
                    }
                },

    #中华全国工商业联合会
    {
                    "platformName": "中华全国工商业联合会",
                    "sourceProvince": "",
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
                    "start_url": "http://www.acfic.org.cn/",
                    "cookie": "",
                    # 首页头条新闻
                    "headline_news": ["//div[@class='main_top_tit'][1]/table//tr/td/h2/a"],
                    # 轮播信息
                    "banner_news": ["//div[@class='slideBox fl']/div[@class='bd']/ul/li/a"],
                    # 轮播旁边新闻
                    "banner_news_side": ["//ol[@class='tab_c tab_cjs']/li/div//a"],
                    # 导航信息
                    "channel_info_xpath": ["//div[@class='nav']/a"],
                    # 详情链接。
                    "doc_links": [
                        r"https?://[\w\-\.]+.*/\d{6}/t\d{8}_\d{6}.html$",
                        r"https?://[\w\-\.]+/ydyl/.*.html$"
                    ],
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {
                                "xpath": "//div[@class='ldzcDetail']/h2/text()",
                            },
                            {
                                "xpath": "//div[@class='center_context_a']/text()"
                            }
                        ],
                        "content": [
                            {
                                "xpath": "//div[@class='TRS_Editor']",
                            },
                            {
                                "xpath": "//div[@class='center_context_c']",
                            },
                        ],
                        "pubSource": [
                            {
                                "xpath": "//div[@class='ldzcDetail']/h3/span[2]/text()",
                            },
                            {
                                "xpath": "//em[@id='ly']/text()"
                            }
                        ],
                        "pubTime": [
                            {
                                "xpath": "//div[@class='ldzcDetail']/h3/span[1]/text()",
                            },
                            {
                                "xpath": "//div[@class='l']/span[1]/text()",
                                "regex": r"发布日期[: ：]\s*?(.*)$",
                            }
                        ],
                        "channel": [
                            {
                                "xpath": "//div[@class='location']/a[2]/text()"
                            },
                            {
                                "xpath": "//div[@class='center_context_map w']/span/a[2]/text()"
                            },
                        ],
                        "authors": [],
                        "summary": [],
                    }
                },

    #国家宗教事务局
    {
                    "platformName": "国家宗教事务局",
                    "sourceProvince": "",
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
                    "start_url": "http://www.sara.gov.cn/gjzjswjhtml/index.html",
                    "cookie": "__jsluid_h=f6f19248951eb728deeb432be8271098",
                    # 首页头条新闻
                    "headline_news": ["//div[@class='focusNews text-center']/h1/a"],
                    # 轮播信息
                    "banner_news": ["//div[@class='swiper-wrapper']/div/div/a"],
                    # 轮播旁边新闻
                    "banner_news_side": ["//ul[@class='new-ul']/li/a"],
                    # 导航信息
                    "channel_info_xpath": ["//ul[@class='menu-ul clearfix']/li/a"],
                    # 详情链接。
                    "doc_links": [
                        r"https?://[\w\-\.]+/\w{4}/\d{6}.jhtml$",
                    ],
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {
                                "xpath": "//div[@class='article']/h2//text()",
                            },
                        ],
                        "content": [
                            {
                                "xpath": "//div[@class='article-con']",
                            },
                        ],
                        "pubSource": [
                            {
                                "xpath": "//div[@class='pull-left']/a/text()",
                            },
                        ],
                        "pubTime": [
                            {
                                "xpath": "//div[@class='pull-right']/text()",
                            },
                        ],
                        "channel": [
                            {
                                "xpath": "//ol[@class='breadcrumb']//li[4]/a/text()"
                            }
                        ],
                        "authors": [],
                        "summary": [],
                    }
                },

    #中国国防动员网
    {
                    "platformName": "中国国防动员网",
                    "sourceProvince": "",
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
                    "start_url": "http://www.gfdy.gov.cn/",
                    "cookie": "wdcid=17020b19f52c4143; wdlast=1611384365; wdses=135934bb854bea64",
                    # 首页头条新闻
                    "headline_news": ["//div[@class='bg']/h2/a"],
                    # 轮播信息
                    "banner_news": ["//div[@class='touchslider-viewport']/div/div/a"],
                    # 轮播旁边新闻
                    "banner_news_side": ["//ul[@class='branch-list']/li/a"],
                    # 导航信息
                    "channel_info_xpath": ["//div[@class='clearfix channel hidden-md-down navbar-nav']/div/div/a"],
                    # 详情链接。
                    "doc_links": [
                        r"https?://[\w\-\.]+.*/\d{4}-\d{2}/\d{2}/content_\d{7}.htm$",
                    ],
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {
                                "xpath": "//div[@class='information']/h2/text()",
                            },
                        ],
                        "content": [
                            {
                                "xpath": "//div[@class='article-content']",
                            },
                            {
                                "xpath": "//div[@class='article-content p-t']"
                            },
                        ],
                        "pubSource": [
                            {
                                "xpath": "//div[@class='down']/span[1]//text()",
                                "regex": r"来源[: ：]\s*?(.*)$",
                            },
                        ],
                        "pubTime": [
                            {
                                "xpath": "//span[@class='infor-time']/text()",
                            },
                        ],
                        "channel": [],
                        "authors": [
                            {
                                "xpath": "//span[@class='infor-editor']/text()",
                                "regex": r"作者[: ：]\s*?(.*)$",
                            }
                        ],
                        "summary": [],
                    }
                },

    #中国国防科工局
    {
                "platformName": "中国国防科工局",
                "sourceProvince": "",
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
                "start_url": "http://www.sastind.gov.cn/",
                "cookie": "HttpOnly; bg5=4|AF2MX",
                # 首页头条新闻
                "headline_news": ["//div[@id='demo1']/a"],
                # 轮播信息
                "banner_news": [],
                # 轮播旁边新闻
                "banner_news_side": ["//td[@class='sv_black14_30']/a"],
                # 导航信息
                "channel_info_xpath": ["/html/body/table[@class='sv_center']//tr/td[2]/table[1]//tr/td[2]/table//tr[2]/td/table//tr//a"],
                # 详情链接。
                "doc_links": [
                    r"https?://[\w\-\.]+.*/content.html$",
                ],
                # 目标采集字段，成功时忽略后续模板。
                "fields": {
                    "title": [
                        {
                            "xpath": "//div[@id='con_title']/text()",
                        },
                        {
                            "xpath": "//td[@class='blue20_30']/text()"
                        },
                        {
                            "xpath": "//td[@class='ercontent']/table[2]//tr[1]/td//text()"
                        }
                    ],
                    "content": [
                        {
                            "xpath": "//div[@id='con_con']",
                        },
                        {
                            "xpath": "//td[@class='black12_24']"
                        },
                        {
                            "xpath": "//div[@id='news_content66']"
                        }

                    ],
                    "pubSource": [
                        {
                            "xpath": "//td[@class='sv_brown']/text()",
                            "regex": r"信息来源[: ：]\s*?(.*)].",
                        },
                    ],
                    "pubTime": [
                        {
                            "xpath": "//span[@id='con_time']/text()",
                            "regex":  r"(\d{4}-\d{1,2}-\d{1,2})"
                        },
                        {
                            "xpath": "//td[@class='font_hs']/text()",
                            "regex": r"(\d{4}年\d{1,2}月\d{1,2}日)"
                        },
                        {
                            "xpath": "/html/body/table[3]//tr/td/table[2]//tr[2]/td/table//tr/td[1]/text()",
                            "regex": r"(\d{4}-\d{1,2}-\d{1,2})"
                        }
                    ],
                    "channel": [],
                    "authors": [],
                    "summary": [],
                }
            },

    #中华全国归国华侨联合会
    {
                    "platformName": "中华全国归国华侨联合会",
                    "sourceProvince": "",
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
                    "start_url": "http://www.chinaql.org/",
                    "cookie": "wdcid=3bd1de75ad86f9a0; wdlast=1611390853; wdses=41ee736d76842992",
                    # 首页头条新闻
                    "headline_news": [],
                    # 轮播信息
                    "banner_news": ["//div[@class='swiper-container-focus']/div[@class='swiper-wrapper']/div[@class='swiper-slide']/div/a | //div[@class='swiper-container-focus']/div[@class='swiper-wrapper']/div[@class='swiper-slide swiper-slide-visible swiper-slide-active']/div/a"],
                    # 轮播旁边新闻
                    "banner_news_side": ["//div[@class='content-right-list']/div//a"],
                    # 导航信息
                    "channel_info_xpath": ["//ul[@class='navlist']/li/a"],
                    # 详情链接。
                    "doc_links": [
                        r"https?://[\w\-\.]+/n1/\d{4}/\d{4}/c\d{6}-\d{8}.html$",
                    ],
                    # 目标采集字段，成功时忽略后续模板。
                    "fields": {
                        "title": [
                            {
                                "xpath": "//div[@class='detail-title']/text()",
                            },
                        ],
                        "content": [
                            {
                                "xpath": "//div[@class='art_txt']",
                            },
                        ],
                        "pubSource": [
                            {
                                "xpath": "//div[@class='pdate']/a/text()",
                            },
                        ],
                        "pubTime": [
                            {
                                "xpath": "//div[@class='pdate']/text()",
                                "regex":  r"(\d{4}年\d{1,2}月\d{1,2}日\d{1,2}:\d{1,2})"
                            },
                        ],
                        "channel": [
                            {
                                "xpath": "//div[@class='text']/a[2]/text()"
                            },
                        ],
                        "authors": [
                            {
                                "xpath": "//div[@class='editer clearfix']/text()",
                                "regex": r"责编[: ：]\s*?(.*)\)$",
                            }
                        ],
                        "summary": [],
                    }
                },

]
