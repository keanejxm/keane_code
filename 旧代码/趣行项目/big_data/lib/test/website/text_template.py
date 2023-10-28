"""
# project: 
# author: Neil
# date: 2021/1/20 11:23
# update: 
"""


from test.website.new_web_spider import WebSpider
from api_common_utils.llog import LLog

# log = LLog("lucio", log_path="./data_log", only_console=False, logger_level="DEBUG").logger
# log = LLog("jovan", log_path="./data_log", only_console=False, logger_level="DEBUG").logger
# log = LLog("fred", log_path="./data_log", only_console=False, logger_level="DEBUG").logger
log = LLog("gary", log_path="./data_log", only_console=False, logger_level="DEBUG").logger

paper_templates = [
    # 龙虎网
    {
        "platformName": "龙虎网",
        # 1：国家级，2：省 级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.longhoo.net/",
        "cookie": "Hm_lvt_83caa016a0e742556c562a659491ecc8=1611112447; __jsluid_h=ec07887d30d41167c8c932ecc1e78cdb; Hm_lpvt_83caa016a0e742556c562a659491ecc8=1611112991",
        # 首页头条新闻
        "headline_news": ["//dl[@class='bigBiao']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='lantern']/ul/li/a[2]"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='listDotBlack mrgt18']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']//a"],
        # 详情链接。
        "doc_links": [
            # http://news.longhoo.net/2021/renshi_0119/462754.html
            r"http?://[\w\-\.]+/\d+/.*html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class='title']/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='articalCont']", },
            ],
            "pubSource": [
                {
                    "xpath": "//p[@class='articalWrite']/text()",
                    "regex": r"来源[: ：]\s*?(.*)编辑.*",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='message']/text()",
                    # "regex": r"发布时间[: ：]\s*?(.*)来源.*",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 南报网
    {
        "platformName": "南报网",
        # 1：国家级，2：省 级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.njdaily.cn/",
        "cookie": "__cfduid=dd260ef984cae3e57b28da2150a2e089c1610174463; __yjs_duid=1_dc163014dd20dd426e5db83ed02d6b401611114318860; acw_tc=76b20f4416111143189223104e0dc75ba9b675d780431f682333793a01df63; SERVERID=6993a94bd2899446ee97cf236c6bc8aa|1611114319|1611114318; Hm_lvt_7f32aed534f2da344768184078540b91=1611114318; Hm_lpvt_7f32aed534f2da344768184078540b91=1611114318",
        # 首页头条新闻
        "headline_news": ["//div[@class='header-title']//a|//div[@class='header-title header-title-2']//a"],
        # 轮播信息
        "banner_news": ["//div[@id='big-swiper']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='content-main-mod1']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='header-nav clearfix']//a"],
        # 详情链接。
        "doc_links": [
            # http://www.njdaily.cn/news/2021/0120/3078036004133663390.html
            r"http?://[\w\-\.]+/\w+/\d+/\d+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='news-title']/h1/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='news-ctx']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='news-title']/span[3]/text()",
                    "regex": r"图文来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='news-title']/span[1]/text()",
                    # "regex": r"发布时间[: ：]\s*?(.*)来源.*",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 南京广播网
    {
        "platformName": "南京广播网",
        # 1：国家级，2：省 级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.njgb.com/",
        "cookie": "SF_cookie_18=26891593; Hm_lvt_ada660d870053bc973518f02c3f501dd=1611120564; _ga=GA1.2.725764888.1611120564; _gid=GA1.2.1935888839.1611120564; Hm_lpvt_ada660d870053bc973518f02c3f501dd=1611120589; bdshare_firstime=1611120588590",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": [],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='e-visit']/ul/li/p/a|//ul[@class='visit-list']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='head2015']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.njgb.com/2021/0116/64515.shtml
            r"http?://[\w\-\.]+/\d+/\d+/\d+.shtml",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class='arttitle']/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='artconzw']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='artsjgy']/text()",
                    "regex": r"稿源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='artsjgy']/text()",
                    "regex": r"\s*?(.*)稿源.*",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 金陵热线
    {
        "platformName": "金陵热线",
        # 1：国家级，2：省 级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.jlonilne.com/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='toutiao clearfix']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='fcon']/span/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='gg']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='m-hd']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            # http://edu.jlonilne.com/jiaoyu/jiaoyuredian/2017/0905/49.html
            r"http?://[\w\-\.]+/\w+/\w+/\d+/\d+/.*html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='title']/h1/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='content showp']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='info']/span[1]/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='info']/span[2]/text()",
                    "regex": r"时间[: ：]\s*?(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 无锡新传媒
    {
        "platformName": "无锡新传媒",
        # 1：国家级，2：省 级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.wxrb.com/",
        "cookie": "safedog-flow-item=; __jsluid_h=33647cd872e4ed73dfefdbef48fb4872",
        # 首页头条新闻
        "headline_news": ["//dl[@class='news_wuxi fl']/dd/a"],
        # 轮播信息
        "banner_news": ["//div[@class='slide01 w100']/div/div/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": [
            "//div[@class='tabN w100 clearfix']/div[2]//ul/li/a|//div[@class='tabN w100 clearfix']/div[3]//ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav w100 clearfix']/div/ul/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.wxrb.com/doc/2021/01/20/61084.shtml
            r"http?://[\w\-\.]+/\w+/\d+/\d+/\d+/.*shtml",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1/strong/text()"},
            ],
            "content": [
                {"xpath": "//div[@id='zoom']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='ldate fl mgt40 font20']/p[5]/text()/text()",
                    # "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='ldate fl mgt40 font20']/p[1]/span/text()|//div[@class='ldate fl mgt40 font20']/p[2]/text()|//div[@class='ldate fl mgt40 font20']/p[3]/text()",
                    # "regex": r"发布时间[: ：]\s*?(.*)文字大小.*",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 无锡市政府网
    {
        "platformName": "无锡市政府网",
        # 1：国家级，2：省 级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.wuxi.gov.cn/",
        "cookie": "jstideAnalyticsUID=ab5900fe1d49d8eea027c910482419ba; Hm_lvt_5d9e966f155ffa33c223ddb76d31091c=1611122482; _gscu_1195712177=1112248221t71k21; _gscbrs_1195712177=1; Hm_lvt_1502c72f84cb43c26ef7d14759c8e5eb=1611122482; Hm_lpvt_5d9e966f155ffa33c223ddb76d31091c=1611122517; _gscs_1195712177=1112248200mg3m21|pv:4; Hm_lpvt_1502c72f84cb43c26ef7d14759c8e5eb=1611122517",
        # 首页头条新闻
        "headline_news": ["//div[@class='top_n fl']/h1/a"],
        # 轮播信息
        "banner_news": ["//div[@class='slideBox disInBlk']//ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='yaowen fl']//ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']//ul[@class='navbox1 fl font20']/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.wuxi.gov.cn/doc/2021/01/20/3170112.shtml
            r"http?://[\w\-\.]+/\w+/\d+/\d+/\d+/.*shtml",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class='text-center font24']/text()"},
            ],
            "content": [
                {"xpath": "//div[@id='Zoom']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='w100 text-right pdb20']/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='funcArea text-center']/text()",
                    "regex": r"发布时间[: ：]\s*?(.*)文字大小.*",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 太湖明珠网
    {
        "platformName": "太湖明珠网",
        # 1：国家级，2：省 级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.thmz.com/",
        "cookie": "__jsluid_h=9a9dac87512cd96eef51d865badd7dcd; UM_distinctid=1771e98e297197-06743531bb1df3-c791039-1fa400-1771e98e298162; CNZZDATA168843=cnzz_eid%3D772789603-1611125377-%26ntime%3D1611125377; Hm_lvt_c7287493abfe02f63ab225fc70e74bf8=1611126072; Hm_lpvt_c7287493abfe02f63ab225fc70e74bf8=1611126072",
        # 首页头条新闻
        "headline_news": ["//div[@class='topnewscon']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='swiper-wrapper']/div/div[@class='text']/h2/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='list right']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//nav/ul/li/a"],
        # 详情链接。
        "doc_links": [
            # http://news.thmz.com/col50/2021-01-19/1275317.html
            r"http?://[\w\-\.]+/\w+\d+/.*html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='title border-bottom']/h3/text()"},
                {"xpath": "//div[@class='article-title']/h1/text()"}
            ],
            "content": [
                {"xpath": "//div[@class='newscon']/article", },
                {"xpath": "//div[@class='article-main']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='subtime']/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
                {
                    "xpath": "//span[@class='origin']/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='float-left']/span[1]/text()",
                    # "regex": r"发布时间[: ：]\s*?(.*)文字大小.*",
                },
                {
                    "xpath": "//span[@class='time']/text()",
                    # "regex": r"发布时间[: ：]\s*?(.*)文字大小.*",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 淮海网
    {
        "platformName": "淮海网",
        # 1：国家级，2：省 级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.huaihai.tv/",
        "cookie": "Hm_lvt_79e5332dc050875ba76473dbc12d7860=1611191843; Hm_lpvt_79e5332dc050875ba76473dbc12d7860=1611191843; UM_distinctid=1772284777136b-08ae637c3c815a-c791039-1fa400-1772284777386b; CNZZDATA137675=cnzz_eid%3D167103633-1611189026-%26ntime%3D1611189026",
        # 首页头条新闻
        "headline_news": ["//li[@class='content_toutiao']/div[2]/ul/li/a"],
        # 轮播信息
        "banner_news": ["//li[@class='xiao_lb']//ul[@class='am-slides']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='am-list am-list-static am-list-border am-u-sm-4']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='am-nav am-nav-pills am-topbar-nav']/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.huaihai.tv/folder7147/folder7248/2021-01-20/HEtWwT6vgz0qrwsb.html
            r"http?://[\w\-\.]+/.*html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class='article_nr_title']/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='article_nr_content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='am_list_author']/a/span[1]/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//article//div[@class='am_list_author']//span[@class='am_news_time']/time/text()",
                    # "regex": r"发布时间[: ：]\s*?(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 武进新闻网
    {
        "platformName": "武进新闻网",
        # 1：国家级，2：省 级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.wj001.com/",
        "cookie": "ad_play_index=28",
        # 首页头条新闻
        "headline_news": ["//div[@class='leftwide']/div/h1/a|//div[@class='leftwide']/div/div/div/a"],
        # 轮播信息
        "banner_news": ["//div[@id='D1pic1']/div/span/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='wjnewsbomright']/div/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='navtable']/div/a"],
        # 详情链接。
        "doc_links": [
            # http://zt3.cz001.com.cn/2020-12/03/content_3871935.htm
            # http://www.wj001.com/news/jinriyaowen/2021-01-20/27281.html
            r"http?://[\w\-\.]+/\d+-\d+/\d+/.*htm",
            r"http?://[\w\-\.]+/\w+/\w+/.*html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class='title']/text()"},
                {"xpath": "//div[@class='heading']/text()"},
            ],
            "content": [
                {"xpath": "//div[@id='zoom']", },
                {"xpath": "//div[@id='Zoom']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='source']/span[1]/text()",
                    "regex": r"来源[: ：]\s*?(.*)作者.*",
                },
                {
                    "xpath": "//div[@class='author']/a/text()",
                    # "regex": r"来源[: ：]\s*?(.*)作者.*",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='source']/span[1]/text()",
                    "regex": r"日期[: ：]\s*?(.*)",
                },
                {
                    "xpath": "//div[@class='author']/text()[1]",
                    # "regex": r"来源[: ：]\s*?(.*)作者.*",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中吴网
    {
        "platformName": "中吴网",
        # 1：国家级，2：省 级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.zhong5.cn/",
        "cookie": "acw_tc=2f624a6f16111945823418408e22136e1c26bc99e6149ad3391f660269a30d; lTUZ_eb82_saltkey=B8i977Is; lTUZ_eb82_lastvisit=1611190982; lTUZ_eb82_sid=QJ1MCR; lTUZ_eb82_lastact=1611194582%09home.php%09misc; lTUZ_eb82_sendmail=1; Hm_lvt_e7ff8cdc0b91be594688384fd2795b09=1611194581; Hm_lpvt_e7ff8cdc0b91be594688384fd2795b09=1611194581",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='focusShow']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='newspart-al-list']/div//ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='categoryNavigation']/div//ul/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.zhong5.cn/article-486293-1.html
            r"http?://[\w\-\.]+/.*html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class='ph']/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='d']/table", },
            ],
            "pubSource": [
                {
                    "xpath": "//p[@class='xg1']/text()[2]",
                    "regex": r"来自[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//p[@class='xg1']/text()[1]",
                    # "regex": r"日期[: ：]\s*?(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 常州在线
    {
        "platformName": "常州在线",
        # 1：国家级，2：省 级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cz001.com.cn/",
        "cookie": "acw_tc=2f624a6f16111945823418408e22136e1c26bc99e6149ad3391f660269a30d; lTUZ_eb82_saltkey=B8i977Is; lTUZ_eb82_lastvisit=1611190982; lTUZ_eb82_sid=QJ1MCR; lTUZ_eb82_lastact=1611194582%09home.php%09misc; lTUZ_eb82_sendmail=1; Hm_lvt_e7ff8cdc0b91be594688384fd2795b09=1611194581; Hm_lpvt_e7ff8cdc0b91be594688384fd2795b09=1611194581",
        # 首页头条新闻
        "headline_news": ["//div[@class='ui-xi-main']/div/h3/a[1]|//div[@class='ui-xi-main']/div/div/h3/a[1]"],
        # 轮播信息
        "banner_news": ["//div[@id='yb_banner_scroll']//div[@class='yb_scroll_group']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='article-li']/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='ui_head_menu']/a"],
        # 详情链接。
        "doc_links": [
            # http://www.cz001.com.cn/index.php?c=Web&m=detail&id=2524
            r"http?://[\w\-\.]+/index.php?.*",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@id='detail_title']/text()"},
            ],
            "content": [
                {"xpath": "//div[@id='detail_content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@id='detail_meta']//span[1]/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@id='detail_meta']//span[2]/text()",
                    # "regex": r"日期[: ：]\s*?(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 苏州新闻网
    {
        "platformName": "苏州新闻网",
        # 1：国家级，2：省 级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.subaonet.com/",
        "cookie": "UM_distinctid=17722c359382c4-02ced14fafdad4-c791039-1fa400-17722c35939312; CNZZDATA1598574=cnzz_eid%3D1757267120-1611195328-%26ntime%3D1611195328; CNZZDATA1598650=cnzz_eid%3D1370649996-1611193478-%26ntime%3D1611193478",
        # 首页头条新闻
        "headline_news": ["//div[@class='toutiao_t_r']/a"],
        # 轮播信息
        "banner_news": ["//div[@id='focus-title']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='xxpt_wen']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='screen Navigation']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.subaonet.com/2021/xwzt/2021szlh/2021szlh_ywdt/0120/148080.shtml
            r"http?://[\w\-\.]+/\d+/\w+/.*shtml",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//span[@class='top_wen']/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='list_neiA fontSizeSmall BSHARE_POP article-content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='NavigationB_r_r_l']/text()",
                    "regex": r"来源[: ：]\s*?(.*)责任编辑.*",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class='NavigationB_r_r_l']/text()",
                    "regex": r"\s*?(.*)来源.*",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
]
paper_templatess = [{
        "platformName": "上海市政府征兵办",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://zbb.sh.gov.cn",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@id='fsD1']/div[@id='D1pic1']/div[@class='fcon']/span[@class='shadow']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='padding_20 in_news']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='layui-main m_t_20']/div[@class='in_kuan in_menu clearfix']/ol/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d{6,}/\w+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='detail-title']/h2/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='wen']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='detail-info']/text()",
                    "regex": r"作者[: ：]\s*?(.*)发布时间.*",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='detail-info']/text()",
                    "regex": r"\s*?发布时间[: ：]\s*?(.*)$",
                    # "regex": r"发布时间[: ：]\s*?(.*)信息来源.*",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    }]

for paper_template in paper_templatess:
    try:
        WebSpider(paper_template=paper_template, logger=log).fetch_yield()
    except Exception as e:
        log.debug("falid to fetch()".format(e))
        continue
