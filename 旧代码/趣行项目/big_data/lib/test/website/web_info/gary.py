res = [
    # 1/13 5 85
    # 河北工信厅(90)
    {
        "platformName": "河北工信厅",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://gxt.hebei.gov.cn/hbgyhxxht/index/index.html",
        "cookie": "UM_distinctid=176fa65bf817d7-046e1009073f6e-c791039-1fa400-176fa65bf82713; CNZZDATA1277589853=2122265070-1610518962-%7C1610518962",
        # 首页头条新闻
        "headline_news": [""],
        # 轮播信息
        "banner_news": ["//div[@id='KinSlideshow_content']//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='portlet']//ul[@class='newsList']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav-gong']//ul//a"],
        # 详情链接。
        "doc_links": [
            # http://gxt.hebei.gov.cn/hbgyhxxht/xwzx32/tzgg83/767693/index.html
            r"http?://[\w\-\.]+/\w+/\w+\d+/\w+\d+/\d+/index.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='gxt-xilan-con clear']//h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='gxt-xilan-con clear']//div[@class='gxt-xilan-content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='gxt-xilan-con clear']//div[@class='gxt-xilan-date']/span[2]/text()",
                    "regex": r"\s*?来源[: ：]\s*?(\w+)$",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='gxt-xilan-con clear']//div[@class='gxt-xilan-date']/span[1]/text()",
                    "regex": r"发布时间[: ：]\s*?(.*)$",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 河北司法厅(90)
    {
        "platformName": "河北司法厅",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://sft.hebei.gov.cn/",
        "cookie": "UM_distinctid=176fa65bf817d7-046e1009073f6e-c791039-1fa400-176fa65bf82713; _gscu_429604091=1052131452e9yw61; _gscbrs_429604091=1; _gscs_429604091=1052131406vu1261|pv:1",
        # 首页头条新闻
        "headline_news": ["//div[@class='toutiao']//ul//li/a"],
        # 轮播信息
        "banner_news": ["//div[@class='news']//div[@class='hiSlider-wrap']//ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='newslist']//ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav_bg']//div[@class='nav']//ul/li/a"],
        # 详情链接。
        "doc_links": [
            # http://sft.hebei.gov.cn/system/2021/01/11/030071058.shtml
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\d+.html",
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\d+.shtml",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='myContent']//div[@class='main_title']/span/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='myContent']//div[@class='main_ct']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='main_top']//div[@class='top_itme']/span[2]/text()",
                    "regex": r"\s*?来源[: ：]\s*?(\w+)$",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='main_top']//div[@class='top_itme']/span[1]/text()",
                    "regex": r"日期[: ：]\s*?(.*)$",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 河北国土资源厅(95)
    {
        "platformName": "河北国土资源厅",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://zrzy.hebei.gov.cn/",
        "cookie": "UM_distinctid=176fa65bf817d7-046e1009073f6e-c791039-1fa400-176fa65bf82713; Secure; _idx_count=1",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='news_lunhuan']/div/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='index-list']//ul//li//a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@id='siteMenu']//li//a"],
        # 详情链接。
        "doc_links": [
            # http://zrzy.hebei.gov.cn/heb/xinwen/gwyw/10540862736508542976.html
            r"http?://[\w\-\.]+/\w+/\w+/\w+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//*[@id='yanse']/div[@class='p_nei']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='BodyLabel']", },
            ],
            "pubSource": [
                {
                    "xpath": "//*[@id='yanse']/div[@class='p_nei']/h4/span[2]/text()",
                    "regex": r"信息来源[: ：]\s*?(.*)$",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//*[@id='yanse']/div[@class='p_nei']/h4/span[1]/text()",
                    "regex": r"发布日期[: ：]\s*?(.*)$",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 河北环保厅(90)
    {
        "platformName": "河北环保厅",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://hbepb.hebei.gov.cn/",
        "cookie": "UM_distinctid=176fa65bf817d7-046e1009073f6e-c791039-1fa400-176fa65bf82713; __FT10000005=2021-1-13-16-6-45; __NRU10000005=1610525205692; __RT10000005=2021-1-13-16-6-45; CNZZDATA1275921890=493337421-1610522091-%7C1610522091",
        # 首页头条新闻
        "headline_news": ["//div[@class='toutiao']/h1/a"],
        # 轮播信息
        "banner_news": ["//div[@class='m_lunbo']//div[@class='swiper-slide']//a"],
        # 轮播旁边新闻
        "banner_news_side": [
            "//div[@class='newlistcenter']/ul[@class='newlist02']/li/a|//div[@class='newlistcenter']/ul[@class='newlist02 height300']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']/div[@class='menubox01']//a"],
        # 详情链接。
        "doc_links": [
            # http://hbepb.hebei.gov.cn/xwzx/stdt/202012/t20201231_107463.html
            r"http?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='erjibigbox']//div[@class='consanji']/h2/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='congczt']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@id='laiyuan']/text()",
                    "regex": r"发布单位[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//p[@class='lytlesj']/span[1]/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                }

            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='consanji']//p[@class='lytlesj']//span[2]/text()",
                    "regex": r"时间[: ：]\s*?(.*)$",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 河北交通厅(90)
    {
        "platformName": "河北交通厅",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://jtt.hebei.gov.cn/",
        "cookie": "UM_distinctid=176fa65bf817d7-046e1009073f6e-c791039-1fa400-176fa65bf82713; __jsluid_h=4c1d729f91616c8e99123198cadbe9d9; _idx_count=1; CNZZDATA1275910339=2033724877-1610526308-%7C1610526308",
        # 首页头条新闻
        "headline_news": ["//div[@class='headlines']/div[@class='headlines_right']/h1/a"],
        # 轮播信息
        "banner_news": ["//div[@class='News_img']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": [
            "//div[@class='News_list']//div[@class='newInfo toggle_tab index1']/ul/li/a|//div[@class='News_list']//div[@class='newInfo toggle_tab index1']//div[@class='bt']//a|//div[@class='News_list']//div[@class='newInfo toggle_tab index2']/ul/li/a|//div[@class='News_list']//div[@class='newInfo toggle_tab index3']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='siteMenu']/a"],
        # 详情链接。
        "doc_links": [
            # http://jtt.hebei.gov.cn/jtyst/jtzx/tpxw/101608897847615.html
            r"http?://[\w\-\.]+/\w+/\w+/\w+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='p_nei']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='BodyLabel']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='p_nei']/h4/span[2]/text()",
                    "regex": r"信息来源[: ：]\s*?(.*)$",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='p_nei']/h4/span[1]/text()",
                    "regex": r"发布日期[: ：]\s*?(.*)$",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },

    # 1/14 11 (90)
    # 北京周报
    {
        "platformName": "北京周报",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://www.beijingreview.com.cn/",
        "cookie": "wdcid=3cb36185ccf5e210; wdses=4701ac13290a97b0; wdlast=1610594441",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["/html/body/div[4]/div[1]/div[@class='fr']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div/ul/li/div/table//a"],
        # 导航信息
        "channel_info_xpath": ["//table[@id='nav_m']//a"],
        # 详情链接。
        "doc_links": [
            # http://www.beijingreview.com.cn/shishi/202101/t20210113_800232487.html
            r"http?://[\w\-\.]+/\w+/\d+/\w\d+_\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h4[@id='TRS_Editor_title']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='TRS_Editor']/p ", },
            ],
            "pubSource": [
                {
                    'xpath': "//td[@class='bian5 ly3']/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                }
            ],
            "pubTime": [],
            "authors": [],
            "summary": [],
        }
    },
    # 京城在线
    {
        "platformName": "京城在线",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://www.jingchengw.cn/",
        "cookie": "__51cke__=; __tins__2484241=%7B%22sid%22%3A%201610605281679%2C%20%22vd%22%3A%202%2C%20%22expires%22%3A%201610607096306%7D; __51laig__=2",
        # 首页头条新闻
        "headline_news": ["//div[@class='focus']//h3//a[1]"],
        # 轮播信息
        "banner_news": ["//div[@class='index_banner']/div//ul//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='zx']//div[2]//a[2]|//div[@class='zx']//div[2]//h3//a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='mainNav_in']//div//a"],
        # 详情链接。
        "doc_links": [
            # http://www.jingchengw.cn/news/hot/20160125/17913.htm
            r"http?://[\w\-\.]+/\w+/\w+/\d+/\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='wenbenleft_list']//h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='wenbenleft_list']//div[@id='news_content']", },
            ],
            "pubSource": [
                {
                    'xpath': "//*[@id='jyzdy_q']/p[1]/a/text()",
                }
            ],
            "pubTime": [],
            "authors": [],
            "summary": [],
        }
    },
    # 北京商报网1
    {
        "platformName": "北京商报网",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "https://www.bbtnews.com.cn/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='head_news']/a"],
        # 轮播信息
        "banner_news": ["//div[@id='carouse']/ul/li/a[1]"],
        # 轮播旁边新闻
        "banner_news_side": [
            "//div[@id='news-container']//ul/div//div[@class='detail_cont textMoreTwo']//a|//div[@id='news-container']//div[@class='text_cont textMoreTwo']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='BJ_nav']/div[@class='wrap']/ul//a"],
        # 详情链接。
        "doc_links": [
            # https://www.bbtnews.com.cn/2021/0114/383041.shtml
            r"https?://[\w\-\.]+/\d+/\d+/\d+.shtml",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='con-box con-box-top article-box']/div[@class='article-hd']//h3/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='con-box con-box-top article-box']/div[@id='pageContent']", },
            ],
            "pubSource": [
                {
                    'xpath': "//div[@class='con-box con-box-top article-box']//div[@class='assist clearfix']//span[1]/text()",
                    "regex": r"出处[: ：]\s*?(.*)$",
                }
            ],
            "pubTime": [
                {
                    'xpath': "//div[@class='con-box con-box-top article-box']//div[@class='assist clearfix']//span[4]/text()",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 辽宁省政府网
    {
        "platformName": "辽宁省政府网",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://www.ln.gov.cn/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//table[@class='head_new_table2']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='jrgz_table1']/div[1]/table//div[@id='bimg']/div//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='jrgz_table1']/div[2]/table//tr[2]//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='sy_nav']/dl/dt/a"],
        # 详情链接。
        "doc_links": [
            # http: // www.ln.gov.cn / ywdt / zymtkln / 202101 / t20210108_4067640.html
            # http: // www.ln.gov.cn / ywdt / jrln / tpxw / 202101 / t20210111_4068340.html
            r"http?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.html",
            r"http?://[\w\-\.]+/\w+/\w+/.*/\d+/\w\d+_\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='dlist_title']/text()", },
                {"xpath": "/html/body/table//tr[4]/td/table[1]//tr[1]/td/p[1]/span", },
            ],
            "content": [
                {"xpath": "//div[@class='dlist_con']//div[@class='TRS_Editor']//p", },
                {"xpath": '//*[@id="Zoom"]/div/p'}
            ],
            "pubSource": [
                {
                    'xpath': "//div[@class='dlist_time']/text()",
                    "regex": r"信息来源[: ：]\s*?(.*)$",
                }
            ],
            "pubTime": [

                {
                    'xpath': "//div[@class='dlist_time']/text()",
                    "regex": r"发布时间[: ：]\s*?(.*)信息.*",
                }],
            "authors": [],
            "summary": [],
        }
    },
    # 辽宁人大网
    {
        "platformName": "辽宁人大网",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://www.lnrd.gov.cn/",
        "cookie": "Hm_lvt_60432665b095e9008669009faf6aed25=1610609550; Hm_lpvt_60432665b095e9008669009faf6aed25=1610609550",
        # 首页头条新闻
        "headline_news": ["//div[@class='gg02']//div[@class='tt_bt']/a"],
        # 轮播信息
        "banner_news": ["//ul[@class='rotaion_list']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='new_nr']//div[@class='new_nr_tit']/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='headnav']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.lnrd.gov.cn/contents/5/56574.html
            r"http?://[\w\-\.]+/\w+/\d/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='bg-wrap']/div[@class='meta']/h2/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='bg-wrap']/div[@class='entry']", },
            ],
            "pubSource": [
                {
                    'xpath': "//div[@class='news_lyzz']/text()",
                    "regex": r"来源[: ：]\s*?(.*)作者.*",
                }
            ],
            "pubTime": [
                {
                    'xpath': "//div[@class='bg-wrap']//div[@class='info']/span[1]/text()"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 辽宁卫健委1
    {
        "platformName": "辽宁卫健委",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://wsjk.ln.gov.cn/index.html",
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='owl-wrapper']/div//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='meiti']/div[@class='mod-body1']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='menu']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            # http://wsjk.ln.gov.cn/wst_tpxw/202008/t20200822_3937260.html
            r"http?://[\w\-\.]+/\w+_\w+/\d+/\w\d+_\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='news-content-main']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@id=\"ContTextSize\"]", },
            ],
            "pubSource": [
                {
                    'xpath': "//div[@class='news-content-main']//div[@class='news-info']/text()",
                    "regex": r"来源[: ：]\s*?(.*)发布时间.*",
                }
            ],
            "pubTime": [
                {
                    'xpath': "//div[@class='news-content-main']//div[@class='news-info']/text()",
                    "regex": r"发布时间[: ：]\s*?(.*)",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 辽宁省委党校
    {
        "platformName": "辽宁省委党校",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://www.lnswdx.cn/",
        "cookie": "UqZBpD3n3iXPAw1X9E/skHKTXuAT45wOI//XvMyf/0LM=v10nPrsgSDEZc; _gscu_415543273=10613620irbap866; _gscbrs_415543273=1; _gscs_415543273=10613620oizx0866|pv:1",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='index_sleft']//div[@class='bd']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='yao_nfra1 g_r_news_cent']//div[@class='yao_line']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='g_head_nav_cont']//ul/li//a"],
        # 详情链接。
        "doc_links": [
            # http://www.lnswdx.cn/tpxw/202011/t20201118_4016836.html
            # http://www.lnswdx.cn/xwzx/szyw/202101/t20210114_4069982.html
            r"http?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.html",
            r"http?://[\w\-\.]+/\w+/\d+/\w\d+_\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='g_news_info']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='g_news_info']//div[@class='TRS_Editor']/div", },
                {"xpath": "//div[@class='g_news_info']//div[@class='TRS_Editor']/div/p", },
                {"xpath": "//div[@class='g_news_info']//div[@class='g_news_info_text']", },
            ],
            "pubSource": [
                {
                    'xpath': "//div[@class='g_news_info']//div[@class='l-xl-bg']/span[1]/text()",
                    "regex": r"文章来源[: ：]\s*?(.*)",
                }
            ],
            "pubTime": [
                {
                    'xpath': "//div[@class='g_news_info']//div[@class='l-xl-bg']/span[3]/text()",
                    "regex": r"发布时间[: ：]\s*?(.*)",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 东北新闻网1
    {
        "platformName": "东北新闻网",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://www.nen.com.cn/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='hotest']/a"],
        # 轮播信息
        "banner_news": ["//div[@id='KSS_contentClone']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='fst']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='navBox']/a"],
        # 详情链接。
        "doc_links": [
            # http://news.nen.com.cn/system/2021/01/14/021083771.shtml
            r"http?://[\w\-\.]+/\w+/\d+/\d+/\d+/\d+.shtml",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='content']//div[@class='clearfix w1000_320 text_title fl']/h1/text()", },
                {"xpath": "//div[@class='contentt']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='content']//div[@id='rwb_zw']/span/p", },
                {"xpath": "//div[@class='box_con']/ul", },
            ],
            "pubSource": [
                {
                    'xpath': "//div[@class='content']//div[@class='box01']/div/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                }
            ],
            "pubTime": [{
                'xpath': "//div[@class='content']//div[@class='box01']/div/text()",
                "regex": r"(.*)来源.*",
            }],
            "authors": [],
            "summary": [],
        }
    },
    # 北国网
    {
        "platformName": "北国网",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://www.lnd.com.cn/",
        "cookie": "uid=1610616483198_9072739322; Hm_lvt_04eeba0e2919689a35c4d021788b2d63=1610616483; Hm_lpvt_04eeba0e2919689a35c4d021788b2d63=1610616483",
        # 首页头条新闻
        "headline_news": ["//div[@class='toutiao']/h2/a"],
        # 轮播信息
        "banner_news": ["//span[@class='cms_block_span']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//span[@class='cms_block_span']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='w1000 bgwdh']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            # http://cpc.people.com.cn/n1/2021/0114/c164113-31999749.html
            # http://news.lnd.com.cn/system/2021/01/14/030166097.shtml
            r"http?://[\w\-\.]+/\w\d/\d+/\d+/\w\d+-\d+.html",
            r"http?://[\w\-\.]+/\w+/\d+/\d+/\d+/\d+.shtml",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='float_left main_l']/p/text()", },
                {"xpath": "//div[@class='text_c']/h1/text()"}
            ],
            "content": [
                {"xpath": "//div[@class='float_left main_l']/div[@class='news']", },
                {"xpath": "//div[@class='show_text']", },
            ],
            "pubSource": [
                {
                    "xpath": "//a[@class='grey']/text()"
                },
                {
                    "xpath": "//p[@class='sou']/a/text()"
                }
            ],
            "pubTime": [
                {
                    'xpath': "//div[@class='newsly']/div[@class='float_left']/span[2]/text()",
                },
                {
                    'xpath': "//p[@class='sou']/text()",
                    "regex": r"\s*?(.*)来源：",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 沈阳在线
    {
        "platformName": "沈阳在线",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://www.syol.net/",
        "cookie": "PHPSESSID=9oq93tod4k9tshm53iv3vv5up4; __tins__292361=%7B%22sid%22%3A%201610617942061%2C%20%22vd%22%3A%201%2C%20%22expires%22%3A%201610619742061%7D; __51cke__=; __51laig__=1",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@id='index_jdt']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": [
            "//div[@class='index_focus_list c_g_6']/ul/li/a|//div[@class='index_img_list1']/ul/li//h2//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='wh_class_nav']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.syol.net/dushi/20201227/116156-1
            r"http?://[\w\-\.]+/\w+/\d+/.*",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@id='news_title']/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='news_content']/p", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@id='news_from']/text()",
                    "regex": r"来源[: ：]\s*?(.*)作者.*",
                },
            ],
            "pubTime": [
                {
                    'xpath': "//div[@id='news_author']/text()",
                    "regex": r"\s*?(.*) | ",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 沈阳网1
    {
        "platformName": "沈阳网",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://www.syd.com.cn/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='topNews']/a"],
        # 轮播信息
        "banner_news": ["//div[@class='scrollNews']/div/div[1]//div[@class='title']//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='center']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='channelNav']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            # http://news.syd.com.cn/system/2021/01/14/011896554.shtml
            r"http?://[\w\-\.]+/\w+/\d+/\d+/\d+/\d+.shtml",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='contentBody']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='contentBody']/div[@class='article']", },
            ],
            "pubSource": [{
                'xpath': "//div[@class='extInfo']/a/text()",
            }],
            "pubTime": [
                {
                    'xpath': "//div[@class='extInfo']/text()",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },

    # 1/15 14 95
    # 盛京文化网1
    {
        "platformName": "盛京文化网",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://wenhua.syd.com.cn/",
        "cookie": "Hm_lvt_bb21a16a9ce4b5929f9ce6095786458c=1610674715; bdshare_firstime=1610674730494; Hm_lpvt_bb21a16a9ce4b5929f9ce6095786458c=1610674765",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//ul[@id='focusImage-content']/li/div//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='newsList']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='nav']//div[@class='text']/a"],
        # 详情链接。
        "doc_links": [
            # http://wenhua.syd.com.cn/system/2020/12/30/011893243.shtml
            r"http?://[\w\-\.]+/\w+/\d+/\d+/\d+/\d+.shtml",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='news_list']/div[@class='new_title']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='news_list']/div[@class='new_content']", },
            ],
            "pubSource": [
                {"xpath": "//div[@class='news_list']/div[@class='new_sour']/a/text()"}
            ],
            "pubTime": [
                {
                    'xpath': "//div[@class='news_list']/div[@class='new_sour']/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 沈阳文明网
    {
        "platformName": "沈阳文明网",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://sy.wenming.cn/",
        "cookie": "wdcid=0163af0cf3747c40; wdlast=1610676859",
        # 首页头条新闻
        "headline_news": ["//div[@class='top_lefttp2 right']//h4//a|//div[@class='top_lefttp2 right']/a"],
        # 轮播信息
        "banner_news": ["//div[@class='focusNav']//ul//li/a[2]"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='stitle']/ul/li//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='top_dh_left']/li//a"],
        # 详情链接。
        "doc_links": [
            # http://sy.wenming.cn/gdtp/202101/t20210105_6892806.html
            # http://www.wenming.cn/ldhd/xjp/zyjh/202101/t20210109_5910258.shtml
            r"http?://[\w\-\.]+/\w+/\d+/\w\d+_\d+.html",
            r"http?://[\w\-\.]+/\w+/\w+/\w+/\d+/\w\d+_\d+.shtml",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='title_tex']/text()", },
                {"xpath": "//div[@class='content_news']/h4/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='tex']", },
                {"xpath": "//div[@class='content_news']/ul"}
            ],
            "pubSource": [
                {
                    "xpath": "//div[@id='time_tex']/text()",
                    "regex": r"\?(\d{4}-\d{1,2}-\d{1,2})",
                },
                {
                    "xpath": "//div[@class='content_news']/h5/text()",
                    "regex": r"来源[:：](.*)[|].*",
                }
            ],
            "pubTime": [
                {
                    'xpath': "//div[@id='time_tex']/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2})",
                },
                {
                    "xpath": "//div[@class='content_news']/h5/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2})",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 千华网
    {
        "platformName": "千华网",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://www.qianhuaweb.com/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='headlines']/h1/a"],
        # 轮播信息
        "banner_news": ["//div[@id='featured']/div/div/h3/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='focusnews']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav_main']//a"],
        # 详情链接。
        "doc_links": [
            # http://www.qianhuaweb.com/2021/0114/4166794.shtml
            r"http?://[\w\-\.]+/\d+/\d+/\d+.shtml",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//article[@class='article-main']//h1/text()", },
            ],
            "content": [
                {"xpath": "//article[@class='article-main']//div[@class='article-content fontSizeSmall BSHARE_POP']", },
            ],
            "pubSource": [
                {
                    'xpath': "//article[@class='article-main']//span[@class='source']/text()",
                }
            ],
            "pubTime": [
                {
                    'xpath': "//article[@class='article-main']//span[@class='date']/text()",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 抚顺传媒网1
    {
        "platformName": "抚顺传媒网",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://www.0245.net.cn/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='slick-track']//div[@class='news-title']/a"],
        # 轮播旁边新闻
        "banner_news_side": [
            "//div[@class='content-mod']//div[@class='news-title']/a|//div[@class='content-mod']//p[@class='news-title']/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='index_nav']/ul/li//a"],
        # 详情链接。
        "doc_links": [
            # http://www.0245.net.cn/news/content/2021-01/15/content_231082.html
            r"http?://[\w\-\.]+/\w+/\w+/\d+-\d+/\d+/\w+_\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='fs-article']/div[@class='article-hd']//h1/text()", },
                {"xpath": "//div[@class='fs-article']/div[@class='article-hd']/h1[2]/text()", },
                {"xpath": "//div[@class='fs-article']/div[@class='article-hd']/h1[3]/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='text_content']", },
                {"xpath": "//div[@class='fs-article']/div[@class='content']", },
            ],
            "pubSource": [
                {
                    'xpath': "//div[@class='fs-article']//div[@class='article-time-source']/span[2]/a/text()",
                }
            ],
            "pubTime": [
                {
                    'xpath': "//div[@class='fs-article']//div[@class='article-time-source']/span[1]/text()",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 丹东市政府网
    {
        "platformName": "丹东市政府网",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://www.dandong.gov.cn/",
        "cookie": "_d_id=7ef9387f0268be7e71091c7c7f0370; UM_distinctid=17704bef153d3-0dbc9e539f8db5-c791039-1fa400-17704bef1543a4; CNZZDATA1259683168=479791320-1610690281-%7C1610690281; _gscu_1618879470=10692358ixz7m218; _gscbrs_1618879470=1; _gscs_1618879470=10692358hddwtp18|pv:1",
        # 首页头条新闻
        "headline_news": ["//ul[@id='xsw-newsList-844']/li/a"],
        # 轮播信息
        "banner_news": ["//div[@id='carousel-example-generic']/div//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='tab-content']//ul[@class='xsw-newsList']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='dhbox1 nav nav-pills']/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.dandong.gov.cn/html/18/20211/a92222ae842903c5.html
            # http://www.xinhuanet.com/2020-06/01/c_1126060621.htm
            r"http?://[\w\-\.]+/\w+/\d+/\d+/.*",
            r"http?://[\w\-\.]+/\d+-\d+/\d+/\w_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//article/div[@class='arTitle']/h2/text()", },
                {"xpath": "//div[@class='h-title']/text()"}
            ],
            "content": [
                {"xpath": "//article/div[@class='arBd']", },
                {"xpath": "//div[@id='p-detail']"}
            ],
            "pubSource": [
                {
                    'xpath': "//article/div[@class='arMeta']/small/text()",
                    "regex": r"来源[: ：]\s*?(.*)浏览.*",
                },
                {
                    "xpath": "//div[@class='h-info']/span[2]",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    'xpath': "//article/div[@class='arMeta']/small/text()",
                    "regex": r"发布时间[: ：]\s*?(.*)来源.*",
                },
                {
                    "xpath": "//div[@class='h-info']/span[@class='h-time']"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 锦州市政府网
    {
        "platformName": "锦州市政府网",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://www.jz.gov.cn/",
        "cookie": "_gscu_262868561=10694186fhiown19; _gscbrs_262868561=1; _gscs_262868561=10694186oap4fz19|pv:1",
        # 首页头条新闻
        "headline_news": ["//div[@class='bd']//div[@class='tempWrap']/ul/li/a"],
        # 轮播信息
        "banner_news": ["//div[@class='focusBox']//div[@class='txt']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='news-list']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='menuc']/a"],
        # 详情链接。
        "doc_links": [
            # http://www.jz.gov.cn/info/1012/75518.htm
            r"http?://[\w\-\.]+/\w+/\d+/\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//form/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='vsb_content']", },
            ],
            "pubSource": [
                {
                    'xpath': "//form/h2/text()",
                    "regex": r"信息来源[: ：]\s*?(.*)责任编辑.*",
                },
            ],
            "pubTime": [
                {
                    'xpath': "//form/h2/text()",
                    "regex": r"发布时间[: ：]\s*?(.*)信息来源.*",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 阜新新闻网1
    {
        "platformName": "阜新新闻网",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://www.fxrbs.cn/",
        "cookie": "LWBg_2132_saltkey=dE57Y19k; LWBg_2132_lastvisit=1610691858; LWBg_2132_sid=x1M11g; LWBg_2132_lastact=1610695458%09home.php%09misc; LWBg_2132_sendmail=1; zycna=BO4RVd4pgNYBAWpxBwyeL8PS",
        # 首页头条新闻
        "headline_news": ["//div[@id='framehdF7En_left']//div[@class='dxb_bc']//a"],
        # 轮播信息
        "banner_news": ["//div[@id='hdp1']//ul//li//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@id='youliebiao']//li//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='wrap NavMCon']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.fxrbs.cn/portal.php?spm=zm5038-001.0.0.1.v43DDI&mod=view&aid=203196
            # http://www.xinhuanet.com/2021-01/13/c_1126979705.htm
            r"http?://[\w\-\.]+/\w+.php?.*",
            r"http?://[\w\-\.]+/\d+-\d+/\d+/\w_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='mn']//h1/text()", },
                {"xpath": "//div[@class='header domPC']//h1//span[@class='title']/text()", },
            ],
            "content": [
                {"xpath": "//td[@id='article_content']", },
                {"xpath": "//div[@id='detail']", },
            ],
            "pubSource": [
                {
                    'xpath': "//div[@class='source']/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
                {
                    'xpath': "//div[@class='h hm']/p[@class='xg1']/text()",
                    "regex": r"来自[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    'xpath': "//div[@class='header-time left']/text()",
                },
                {
                    'xpath': "//div[@class='h hm']/p[@class='xg1']/text()",
                    "regex": r"\s*?(.*)发布者.*",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 阜新市政府网
    {
        "platformName": "阜新市政府网",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://www.fuxin.gov.cn/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='containter_inner']/div[1]//a"],
        # 轮播信息
        "banner_news": ["//div[@id='carousel']//ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@id='tabs_p']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='headNav']/ul/li/div/a"],
        # 详情链接。
        "doc_links": [
            # http://www.fuxin.gov.cn/newsdetail.jsp?id=461307
            r"http?://[\w\-\.]+/\w+.jsp?.*",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='news_inner']/div[@class='DetailcontentTile']/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='Detailcontent']", },
            ],
            "pubSource": [
                {
                    'xpath': "//div[@class='news_inner']/p[@class='DetailcontentTime']/span[3]/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    'xpath': "//div[@class='news_inner']/p[@class='DetailcontentTime']/span[3]/text()",
                    "regex": r"日期[: ：]\s*?(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 辽阳市政府网
    {
        "platformName": "辽阳市政府网",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://www.liaoyang.gov.cn/",
        "cookie": "JSESSIONID=2A07979474CAB0016CCB5F2E668A826F; zh_choose=s",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@id='img-play']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='zf_newk']/div[@class='neik1']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='base_nav']/a"],
        # 详情链接。
        "doc_links": [
            # http://www.liaoyang.gov.cn/html/LY/202101/161058237571631.html
            r"http?://[\w\-\.]+/.*",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='neik']/div[@class='bt']/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='zoom']/p", },
            ],
            "pubSource": [
                {
                    'xpath': "//div[@class='neik']/div[@class='time']/div[@class='fl']/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    'xpath': "//div[@class='neik']/div[@class='time']/div[@class='fl']/text()",
                    "regex": r"发布时间[: ：]\s*?(.*)来源",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 盘锦市政府网
    {
        "platformName": "盘锦市政府网",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://www.panjin.gov.cn/",
        "cookie": "sftms_P8SESSION=c0e423e217f97f4d; zh_choose_undefined=s",
        # 首页头条新闻
        "headline_news": ["//div[@class='index_m1']//a"],
        # 轮播信息
        "banner_news": ["//div[@id='D1pic1']/div/span/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='news_list']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav_list fl']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.panjin.gov.cn/html/1738/2021-01-13/content-87612.html
            r"http?://[\w\-\.]+/\w+/\d+/\d+-\d+-\d+/\w+-\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='ny_mb_inner_box ny_mb_inner_box1']/p/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='ny_mb_inner_box ny_mb_inner_box1']/div[@class='xwnr_txt']", },
            ],
            "pubSource": [
                {
                    'xpath': "//div[@class='ny_mb_inner_box ny_mb_inner_box1']/div[@class='source']/span/text()",
                    "regex": r"信息来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    'xpath': "//div[@class='ny_mb_inner_box ny_mb_inner_box1']/div[@class='fbsj_llcs_box']/span[1]/text()",
                    "regex": r"发布时间[: ：]\s*?(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中国铁岭
    {
        "platformName": "中国铁岭",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://www.tielingcn.com/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='ind_toutiao_box']//h1/a"],
        # 轮播信息
        "banner_news": ["//div[@id='slideBox']//ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='ind_news']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='gnavi']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.tielingcn.com/lnnews/content/2021-01/07/content_7625.html
            r"http?://[\w\-\.]+/\w+/\w+/\d+-\d+/\d+/\w+_\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='article']//h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='arcont']", },
            ],
            "pubSource": [
                {
                    'xpath': "//div[@class='article']//p[@class='browse']/span[2]/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    'xpath': "//div[@class='article']//p[@class='browse']/span[1]/text()",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 铁岭广播电视台1
    {
        "platformName": "铁岭广播电视台",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://www.tielingtv.com/",
        "cookie": "UM_distinctid=177055cb6a93b8-0932e6a9406189-c791039-1fa400-177055cb6aa784; CNZZDATA1258844690=27544342-1610699155-%7C1610699155",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@id='slider']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='yaowen']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='menua']//a"],
        # 详情链接。
        "doc_links": [
            # http://www.tielingtv.com/html/news/tl/2021/0111/10510.html
            r"http?://[\w\-\.]+/\w+/\w+/\w+/\d+/\d+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='l']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='l']/div[@class='icontent']", },
            ],
            "pubSource": [
                {
                    'xpath': "//div[@class='l']//div[@class='il']/span[1]/a/text()",
                },
            ],
            "pubTime": [
                {
                    'xpath': "//div[@class='l']//div[@class='il']/span[2]/text()",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 铁岭市政府网
    {
        "platformName": "铁岭市政府网",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://www.tieling.gov.cn/",
        "cookie": "Hm_lvt_3d25fcdd6d1a225248857d05d9982585=1610703131; Hm_lpvt_3d25fcdd6d1a225248857d05d9982585=1610703131; UM_distinctid=17705635208155-0d10b31cd34b3a-c791039-1fa400-17705635209c7; CNZZDATA1271190300=1547046220-1610703132-%7C1610703132",
        # 首页头条新闻
        "headline_news": ["//div[@id='taotiao']//a[2]"],
        # 轮播信息
        "banner_news": ["//div[@class='txt']//ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='product-wrap']//ul/li//a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='Tl_top2']/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.tieling.gov.cn/tieling/xwzx/bmdt/1366950/index.html
            r"http?://[\w\-\.]+/\w+/\w+/\w+/\d+/index.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='content']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='content_con']", },
            ],
            "pubSource": [
                {
                    'xpath': "//div[@class='content']//div[@class='content_source']/span[1]/text()",
                    "regex": r"文章来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    'xpath': "//div[@class='content']//div[@class='content_source']/span[2]/text()",
                    "regex": r"添加时间[: ：]\s*?(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 朝阳新闻网1
    {
        "platformName": "朝阳新闻网",
        # "sourceProvince": "北京市",
        # "sourceCity": "北京市",
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
        "start_url": "http://www.cynews.com.cn/",
        "cookie": "ASP.NET_SessionId=mflzcwk235fs50undeantkbw; SSCSum=1; Hm_lvt_c6966c14fc8295df361c89dbe0030bd9=1610703731; Hm_lpvt_c6966c14fc8295df361c89dbe0030bd9=1610703731; wdcid=3914c75e080a4f0a; wdlast=1610703731",
        # 首页头条新闻
        "headline_news": ["//div[@class='Hotnews left']//div/a"],
        # 轮播信息
        "banner_news": ["//div[@class='txt']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='news_list news_list_lh34']/li//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='mainwidth daohang']/ul/li//a"],
        # 详情链接。
        "doc_links": [
            # http://www.cynews.com.cn/chaoyangyaowen/39033.aspx
            # http://www.cynews.com.cn/html/xinwentoutiao/39034.html
            r"http?://[\w\-\.]+/\w+/\d+.aspx",
            r"http?://[\w\-\.]+/\w+/\w+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='title_tex']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='Custom_UnionStyle']", },
            ],
            "pubSource": [],
            "pubTime": [
                {
                    'xpath': "//div[@id='time_tex']/text()",
                    "regex": r"(\d{4}/\d{1,2}/\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },

    # 1.16 12
    # 葫芦岛市政府网
    {
        "platformName": "葫芦岛市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.hld.gov.cn/",
        # 首页头条新闻
        "headline_news": ["//ul[@class='infoList']/li/h3//a"],
        # 轮播信息
        "banner_news": ["//div[@class='txt']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='homelist1']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.hld.gov.cn/xwdt/zwyw/202012/t20201224_1014204.html
            r"http?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='content-hd']/h1/text()"},
                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                # {"xpath": '/html/body/div[2]/div[1]/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": "//div[@class='TRS_Editor']", },
                # {"xpath": '/html/body/div[2]/div[3]/div[2]', },
            ],

            "pubSource": [
                {
                    "xpath": "//div[@class='attr-l']/span[2]/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='attr-l']/span[1]/text()",
                    "regex": r"时间[: ：]\s*?(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 吉林广播网(首页无数据，修改)
    {
        "platformName": "吉林广播网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.jlradio.cn/",
        "cookie": "Hm_lvt_80207cbeadeb28733834edeb49d71f71=1610774348; Hm_lpvt_80207cbeadeb28733834edeb49d71f71=1610774348; Qs_lvt_337602=1610774347; Qs_pv_337602=2984102851639028700",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@id='w-slider-aabl']//div[@class='slidesjs-slide sliderimgLoaded']/a[2]"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='widget-main']/span/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@id='nav']/li//a"],
        # 详情链接。
        "doc_links": [
            # http://www.jlradio.cn/html/2908/2021/1/15/426398.html
            r"http?://[\w\-\.]+/\w+/\d+/\d+/\d/\d+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='content_page']/h1/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='content_page']/div[@class='txt']/p", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='info1']/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='info2 phone2']/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",
                },
                {
                    "xpath": "//div[@class='content_page']/h4/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 吉视网
    {
        "platformName": "吉视网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.jlntv.cn/newpc/",
        "cookie": "UM_distinctid=17709b548ce607-0bca95d56e68ed-c791039-1fa400-17709b548cf5fc; CNZZDATA4639130=cnzz_eid%3D1250037412-1610774891-%26ntime%3D1610774891",
        # 首页头条新闻
        "headline_news": ["//div[@class='headline mt20']//a"],
        # 轮播信息
        "banner_news": ["//ul[@class='slide-content']//li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='fl w420 mr15']//ul//li/a[2]|//div[@class='pdrdcon']//ul//li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='fl navList']/div/p/a"],
        # 详情链接。
        "doc_links": [
            # http://www.jlntv.cn/newpc/jx/thnews/folder2857/2020-11-17/1410357.html
            r"http?://[\w\-\.]+/\w+/\w+/\w+/\w+\d+/\d+-\d+-\d+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='article-title pull-left']/h1/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='article-main']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='origin']/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class='time']/text()",
                    "regex": r"时间[: ：]\s*?(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 吉林在线1
    {
        "platformName": "吉林在线",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.jl852.com/",
        "cookie": "PHPSESSID=us097p5l0fbuqe29mn2o99v8v5",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//ul[@id='textBall']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='con']//ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='nav']/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.jl852.com/qsiyyi/n_16650.html
            r"http?://[\w\-\.]+/\w+/\w_\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='article_left_bor']//h1/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='article_body']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='article2_left']/p[2]/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='article2_left']/p[1]/text()",
                    "regex": r"更新时间[: ：]\s*?(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 吉网
    {
        "platformName": "吉网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cnjiwang.com/",
        "cookie": "_trs_uv=kjzbkvxz_1009_4v7; _trs_ua_s_1=kjzbkvxz_1009_c9a1; UM_distinctid=17709d866933ef-0d80f052f00058-c791039-1fa400-17709d866947cc; CNZZDATA1261550231=2038477887-1610775280-%7C1610775280; Hm_lvt_920cb63e2f2de0c677b3c42aad2f9559=1610777913; Hm_lpvt_920cb63e2f2de0c677b3c42aad2f9559=1610777913",
        # 首页头条新闻
        "headline_news": ["//div[@class='news']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='part9']//ul//li//div[@class='text']//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='part10 left']//ul//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav-bar w1230 clearfix']//ul//a"],
        # 详情链接。
        "doc_links": [
            # http://news.cnjiwang.com/jwyc/202101/3298177.html
            # http://news.cnjiwang.com/jlxwdt/sn/202101/3299152.html
            r"http?://[\w\-\.]+/\w+/\d+/\d+.html",
            r"http?://[\w\-\.]+/\w+/\w+/\d+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "/html/body/div[6]/div/h1/span/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='content']/div", },
                {"xpath": "//div[@class='content']/p", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='zxdata mt20']/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
                {
                    "xpath": "//div[@class='zxdata mt20']/a/text()",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='zxdata mt20']/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 吉林融媒
    {
        "platformName": "吉林融媒",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.jlntv.cn/folder3454/",
        "cookie": "UM_distinctid=17709b548ce607-0bca95d56e68ed-c791039-1fa400-17709b548cf5fc; CNZZDATA4639130=cnzz_eid%3D1250037412-1610774891-%26ntime%3D1610780294",
        # 首页头条新闻
        "headline_news": ["//div[@class='headline mt20']//a"],
        # 轮播信息
        "banner_news": ["//ul[@class='slide-content']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='fl w420 mr15']//ul/li//a[2]"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='fl navList']/div/p/a"],
        # 详情链接。
        "doc_links": [
            # http://www.jlntv.cn/newpc/jx/folder510/2020-01-20/1106602.html
            r"http?://[\w\-\.]+/.*html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[2]/div[2]/div[4]/div/div[1]/h1/text()'},
            ],
            "content": [
                {"xpath": "//div[@class='article-main']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='origin']/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class='time']/text()",
                    "regex": r"时间[: ：]\s*?(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 长春新闻网(新闻频道数据少)
    {
        "platformName": "长春新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.changchunews.com/",
        "cookie": "Hm_lvt_3364f120bcf2d9731db3ebf4d9234ba8=1610785131; Hm_lpvt_3364f120bcf2d9731db3ebf4d9234ba8=1610785131",
        # 首页头条新闻
        "headline_news": ["//div[@class='hd']/a"],
        # 轮播信息
        "banner_news": ["//div[@class='am-slider am-slider-c2 am-no-layout']//ul[@class='am-slides']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='m-g am-fl']//ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.jlntv.cn/newpc/jx/folder510/2020-01-20/1106602.html
            r"http?://[\w\-\.]+/\w+/\w+/.*html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class='am-article-hd am-text-xl']"},
            ],
            "content": [
                {"xpath": "//div[@class='am-article-bd']", },
            ],
            "pubSource": [
                {
                    "xpath": "//p[@class='am-article-meta']/text()",
                    "regex": r"来源[: ：]\s*?(.*)时间.*",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//p[@class='am-article-meta']/text()",
                    "regex": r"时间[: ：]\s*?(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 长春广播网
    {
        "platformName": "长春广播网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.ccradio.cn/",
        "cookie": "Hm_lvt_fa3aeb7679794913c141f79b5557353c=1610785803; Hm_lpvt_fa3aeb7679794913c141f79b5557353c=1610785803; Hm_lvt_bc212b3cd3135514ccb6f4aa24c0b484=1610785803; Hm_lpvt_bc212b3cd3135514ccb6f4aa24c0b484=1610785803",
        # 首页头条新闻
        "headline_news": ["//div[@class='jrtt']//a"],
        # 轮播信息
        "banner_news": [],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='g_box1 fl']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']//a"],
        # 详情链接。
        "doc_links": [
            # http://www.ccradio.cn/zonghe/20210113/118635.html
            r"http?://[\w\-\.]+/\w+/\d+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='g_con']/h1"},
            ],
            "content": [
                {"xpath": "//div[@class='con']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='info']/span[1]/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='info']/span[3]/text()",
                    "regex": r"时间[: ：]\s*?(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 长春市政府网
    {
        "platformName": "长春市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.changchun.gov.cn/",
        "cookie": "_gscu_2032267129=10786250ch2s8x18; _gscbrs_2032267129=1; _gscs_2032267129=10786250n87juc18|pv:1; _trs_uv=kjzgjlxr_1008_75g; _trs_ua_s_1=kjzgjlxr_1008_6hky",
        # 首页头条新闻
        "headline_news": ["//div[@class='main_content']//a"],
        # 轮播信息
        "banner_news": ["//ul[@id='pic-box']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='xw_left_ywdt index_news_left']/div//ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav_xll']//ul/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.changchun.gov.cn/zw_33994/tpxx/202012/t20201215_2656437.html
            # http://www.gov.cn/premier/2021-01/16/content_5580402.htm
            r"http?://[\w\-\.]+/\w+_\d+/\w+/\d+/\w\d+_\d+.html",
            r"http?://[\w\-\.]+/.*htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "/html/body/div[3]/div/div[1]/div[2]/h2/text()"},
                {"xpath": "/html/body/div[3]/div[2]/div[1]/div[2]/h1/text()"}
            ],
            "content": [
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '//*[@id="Zoom"]', },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='font']/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class='font']/text()",
                    "regex": r"时间[: ：]\s*?(.*)来源.*",
                },
                {
                    "xpath": "//div[@class='pages-date']/text()"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 松花江网1
    {
        "platformName": "松花江网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.shjnet.cn/",
        "cookie": "security_session_verify=20111e789dbf0820d80d051a8a7252a1; Hm_lvt_8fc630ab6ae06b474758ddcb74206b15=1610787739; Hm_lpvt_8fc630ab6ae06b474758ddcb74206b15=1610787739",
        # 首页头条新闻
        "headline_news": ["/html/body/div[2]/section/div[1]/div/div[2]//a"],
        # 轮播信息
        "banner_news": ["//div[@id='news-carousel']//div[@class='carousel-inner']//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@id='rtion']//ul[@id='font16']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='navbar-collapse collapse']/ul//a"],
        # 详情链接。
        "doc_links": [
            # http://www.shjnet.cn/xw/txsl/gnxw/202101/t20210116_526754.html
            r"http?://[\w\-\.]+/\w+/\w+/.*html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='hght']/h2/text()"},
            ],
            "content": [
                {"xpath": "//div[@id='essay']", },
            ],
            "pubSource": [
                # {
                #     "xpath": "//div[@class='t_left']/span[2]/text()",
                #     "regex": r"来源[: ：]\s*?(.*)",
                #  },
            ],
            "pubTime": [
                {
                    "xpath": "//*[@id='hght']/div[1]/span/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 延边新闻网1
    {
        "platformName": "延边新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.ybrbnews.cn/",
        "cookie": "_gscu_498304974=10788980u19rqt57; _gscbrs_498304974=1; _gscs_498304974=10788980ejac0j57|pv:1; UM_distinctid=1770a81473c427-0061917b94ed0d-c791039-1fa400-1770a81473d49a; CNZZDATA1278299154=2082035602-1610787959-%7C1610787959",
        # 首页头条新闻
        "headline_news": ["//div[@id='taotiao']//a"],
        # 轮播信息
        "banner_news": ["//div[@id='slidercontent']/ul/li/div[@class='txt']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='text']/li//a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@id='titmenu']/li//a"],
        # 详情链接。
        "doc_links": [
            # http://www.ybrbnews.cn/ynews/content/2021-01/14/142_466607.html
            r"http?://[\w\-\.]+/\w+/\w+/.*html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='content']/h1/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='maincontent']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='taow']/span/a/text()",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='taow']/span[1]/text()",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 四平政府网
    {
        "platformName": "四平市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.siping.gov.cn/",
        "cookie": "_trs_uv=kjzihxur_79_1239; _trs_ua_s_1=kjzihxur_79_xlr; _gscu_2042815902=10789532y0o1gb10; _gscbrs_2042815902=1; _gscs_2042815902=107895328fjv6u10|pv:1; UM_distinctid=1770a89b50c17f-0ab5a2d67d7113-c791039-1fa400-1770a89b50d3f8; CNZZDATA1272818459=632357794-1610788740-%7C1610788740; bgm=1",
        # 首页头条新闻
        "headline_news": ["//div[@class='import_notice']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='my-slider']//h2//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='index_bg index_left']/div/ul//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='header_nav_box']/ul//a"],
        # 详情链接。
        "doc_links": [
            # http://www.siping.gov.cn/szf/lshd/202101/t20210115_552259.html
            r"http?://[\w\-\.]+/\w+/\w+/.*html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='newscont']/h2[1]/text()"},
            ],
            "content": [
                {"xpath": "//div[@id='content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='newstop left']/span[3]/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "///div[@class='newstop left']/span[2]/text()",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },

    # 1.19
    # 通化新闻网
    {
        "platformName": "通化新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.thnews.net/",
        "cookie": "security_session_verify=c563de04c6185006e93bcad153819d7d; UM_distinctid=17714145e5e590-0e8b87fec2e529-c791039-1fa400-17714145e5f5e7; CNZZDATA1278973663=1411483041-1610947728-%7C1610947728; flashSet=ture",
        # 首页头条新闻
        "headline_news": ["//div[@class='section']//h3/a"],
        # 轮播信息
        "banner_news": ["//ul[@class='slide-cont']/li/div//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='side-txt-list']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav-box']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.thnews.net/news/show-35008.html
            r"http?://[\w\-\.]+/\w+/\w+-\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='bg-wrap']/div[@class='meta']/h2/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='entry']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='info']/span[2]/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='info']/span[1]/text()",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 白城新闻网1
    {
        "platformName": "白城新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.bcxww.com/",
        "cookie": "Hm_lvt_411490693c9fa55a43e96882d9600957=1611026193; Hm_lpvt_411490693c9fa55a43e96882d9600957=1611026193",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": [],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='w_nr3']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='zm-wrap zm-subnav']//a"],
        # 详情链接。
        "doc_links": [
            # http://xw.bcxww.com/bcxw/2021/0119/63694.html
            r"http?://[\w\-\.]+/\w+/\d+/\d+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='title']/h2[1]/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='info']/a/text()",
                    # "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='info']/text()",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 辽源市政府网
    {
        "platformName": "辽源市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.liaoyuan.gov.cn/wzsy/",
        "cookie": "_trs_uv=kk3kqop4_1358_3aa; _trs_ua_s_1=kk3kqop4_1358_1cpz",
        # 首页头条新闻
        "headline_news": ["//div[@id='wrap']/div/div/a"],
        # 轮播信息
        "banner_news": ["//div[@id='fsD1']/div/div/span/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='tab']/p/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='navigation-v3 navtaba']/ul/li//a"],
        # 详情链接。
        "doc_links": [
            # http://www.liaoyuan.gov.cn/xxgk/dtxw/zwlb/zwyw/202101/t20210119_538277.html
            r"http?://[\w\-\.]+/\w+/\w+/\w+/.*html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='sycon_leftwh news_cont']/h2/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='TRS_Editor']/p", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='sywzy_xbt wxx_neirong_timecent']/span[2]/text()",
                    "regex": r"信息来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='sywzy_xbt wxx_neirong_timecent']/span[1]/text()",
                    "regex": r"发布时间[: ：]\s*?(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 松源新闻网
    {
        "platformName": "松原新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.qhdcy.cn/",
        "cookie": "__tins__20322621=%7B%22sid%22%3A%201611035874025%2C%20%22vd%22%3A%201%2C%20%22expires%22%3A%201611037674025%7D; __51cke__=; __51laig__=1",
        # 首页头条新闻
        "headline_news": ["//div[@class='news-main-cont-detail']/ul/li/a"],
        # 轮播信息
        "banner_news": ["//div[@id='slider-main']/ul/li/a[2]"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='article-newslist']//h3/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='head-nav']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.qhdcy.cn/techan/2315.html
            r"http?://[\w\-\.]+/\w+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='article-detail-bigtit']/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='article-detail-cont']", },
            ],
            "pubSource": [
                # {
                #     "xpath": "//div[@class='sywzy_xbt wxx_neirong_timecent']/span[2]/text()",
                #     "regex": r"信息来源[: ：]\s*?(.*)",
                #  },
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class='article-detail-share']/text()",
                    "regex": r"时间[: ：]\s*?(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 松原市政府网
    {
        "platformName": "松原市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.jlsy.gov.cn/",
        "cookie": "_trs_uv=kk3lx2sz_84_1nef; _trs_ua_s_1=kk3lx2sz_84_8jdp",
        # 首页头条新闻
        "headline_news": ["//div[@class='line_tt']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='line01_bd']//ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='line01_yw fr']//ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//dd[@class='nav fr']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.jlsy.gov.cn/xwzx/ywdt/202101/t20210115_421383.html
            r"http?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h3[@class='news_tit_lj']/text()"},
                {"xpath": "//h3[@class='news_tit_lj']/p/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='TRS_Editor']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='news_source_lj']/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class='news_date_lj']/text()",
                    "regex": r"发布时间[: ：]\s*?(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 长白山新闻网1
    {
        "platformName": "长白山新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cbsrb.com/",
        "cookie": "ASP.NET_SessionId=hfsljf452fqalo2pcjn4ho45; bdshare_firstime=1611037904511",
        # 首页头条新闻
        "headline_news": ["//div[@class='headNews mb20']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='focPicNews clearfix mb20']//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='scrollNewsList']/li//div[@class='title']//a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@id='mainNav']/li//a"],
        # 详情链接。
        "doc_links": [
            # http://www.cbsrb.com/Item/38757.aspx
            r"http?://[\w\-\.]+/\w+/\d+.aspx",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h2[@class='articleTitle']/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='conTxt']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='property']/span[2]/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                # {
                #     "xpath": "//span[@class='news_date_lj']/text()",
                #     "regex": r"发布时间[: ：]\s*?(.*)",
                # },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 新华报业网1
    {
        "platformName": "新华报业网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.xhby.net/",
        "cookie": "_trs_uv=kk3ot7r3_3064_6fcd; _trs_ua_s_1=kk3ot7r3_3064_2mkl",
        # 首页头条新闻
        "headline_news": ["//div[@class='HotContent']/a"],
        # 轮播信息
        "banner_news": ["//div[@id='select_btn']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='type_content_card']/div/a[2]"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='Nav']/div//a"],
        # 详情链接。
        "doc_links": [
            # http://news.xhby.net/zt/zyq/202101/t20210119_6952151.shtml
            r"http?://[\w\-\.]+/\w+/.*shtml",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='title']/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='TRS_Editor']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@id='source_baidu']/a/text()",
                    # "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//span[@id='pubtime_baidu']/text()",
                    # "regex": r"发布日期[: ：]\s*?(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中国江苏网
    {
        "platformName": "中国江苏网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.jschina.com.cn/",
        "cookie": "__jsluid_h=af02173867979a1ad93c170358951d0c; Hm_lvt_7e2676118a96afc7e3f09188211f7a18=1611042601; Hm_lpvt_7e2676118a96afc7e3f09188211f7a18=1611042601; wdcid=61315f947156ea56; wdlast=1611042601",
        # 首页头条新闻
        "headline_news": ["//div[@class='bigbiaot']//div/ul/li[2]//a"],
        # 轮播信息
        "banner_news": [
            "//div[@class='swiper-container s1 swiper-container-horizontal']/div[@class='swiper-wrapper']/div/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='box']/div[@class='right']/div/ul//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='top']/div/div/a"],
        # 详情链接。
        "doc_links": [
            # http://news.jschina.com.cn/scroll/xxjxs/gj/202101/t20210119_2713025.shtml
            r"http?://[\w\-\.]+/\w+/.*shtml",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='title']/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='TRS_Editor']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@id='source_baidu']/a/text()",
                    # "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//span[@id='pubtime_baidu']/text()",
                    # "regex": r"发布日期[: ：]\s*?(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 江苏之窗1(已修改)
    {
        "platformName": "江苏之窗",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.jiangszc.com/",
        "cookie": "Hm_lvt_80a59052b996bd55bb03c9d8f276cfd0=1611045789; Hm_lpvt_80a59052b996bd55bb03c9d8f276cfd0=1611045789",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": [],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='box2']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='middle']/div/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.jiangszc.com/zixun/20210111/139622.html
            r"http?://[\w\-\.]+/\w+/\d+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//article/h1/text()"},
                {"xpath": "//div[@class=\"art-min\"]/h1/text()"},
            ],
            "content": [
                {"xpath": "//article/div[@class='neirong']", },
                {"xpath": "//article[@class=\"neirong\"]", },
            ],
            "pubSource": [
                # {
                #     "xpath": "//article/div[@class='laiyuan']/text()",
                #     # "regex": r"来源[: ：]\s*?(.*)",
                #  },
            ],
            "pubTime": [
                {
                    "xpath": "//article/div[@class='laiyuan']/text()",
                    # "regex": r"时间[: ：]\s*?(.*)",
                },
                {
                    "xpath": "//div[@class='laiyuan']/text()[4]",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 现代快报
    {
        "platformName": "现代快报",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.xdkb.net/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='title']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='slider-slides event-attached']/div/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='new-list']/div/div[@class='item-right']/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='navbar Semilight']//a|//div[@class='logo logo-index']/a"],
        # 详情链接。
        "doc_links": [
            # http://www.xdkb.net/p1/150044.html
            r"http?://[\w\-\.]+/.*html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='big-title bold']/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='context']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='message overflow Semilight']/ul/li[1]/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='message overflow Semilight']/ul/li[3]/text()",
                    "regex": r"时间[: ：]\s*?(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 江苏工人报
    {
        "platformName": "江苏工人报",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.jsgrb.com/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//a[@class='font-blue']"],
        # 轮播信息
        "banner_news": ["//div[@class='swiper-wrapper']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='list-firstRight vertical_top']//ul//li//a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='navbar-inner']/li//a"],
        # 详情链接。
        "doc_links": [
            # http://www.jsgrb.com/article/content?key=5d3505e24da8d555338b456c&parentkey=
            r"http?://[\w\-\.]+/\w+/\w+?.*",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='list-body']/h2/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='view_item']", },
            ],
            "pubSource": [
                # {
                #     "xpath": "//div[@class='message overflow Semilight']/ul/li[1]/text()",
                #     "regex": r"来源[: ：]\s*?(.*)",
                #  },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='list-txt']/span[2]/text()",
                    # "regex": r"时间[: ：]\s*?(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 我苏网1
    {
        "platformName": "我苏网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.ourjiangsu.com/",
        "cookie": "sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217719fb22965cb-01f850733b977a-c791039-2073600-17719fb22974ac%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2217719fb22965cb-01f850733b977a-c791039-2073600-17719fb22974ac%22%7D; Hm_lvt_c324388b3a7e79cbcf0c10d6e0fd3948=1611048625; Hm_lpvt_c324388b3a7e79cbcf0c10d6e0fd3948=1611048641",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//ul[@id='imgs_cont1']/li/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='contmain_r']/div//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='navigation']//ul/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.ourjiangsu.com/a/20210119/1611015895966.shtml
            r"http?://[\w\-\.]+/\w/\d+/\d+.shtml",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='article']/h1/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='source']/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class='time']/text()",
                    # "regex": r"时间[: ：]\s*?(.*)",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 江苏省政府网
    {
        "platformName": "江苏省政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.jiangsu.gov.cn/",
        "cookie": "__jsluid_h=6072a540e91d7fcab2426630fc70170b; zh_choose_1=s; yunsuo_session_verify=fa390e4a14fd214cc0733db9c0a1ec0f",
        # 首页头条新闻
        "headline_news": ["//div[@id='Marquee']//li[@class='valChoose']/a"],
        # 轮播信息
        "banner_news": ["//div[@class='tempWrap']//ul/li/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//li[@class='valChoose']//a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='cf nav']/li/a"],
        # 详情链接。
        "doc_links": [
            # http://www.jiangsu.gov.cn/art/2021/1/19/art_37384_9647053.html
            r"http?://[\w\-\.]+/\w+/\d+/\d/\d+/.*html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='sp_title']/text()"},
                {"xpath": "//div[@class=\"article oneColumn pub_border\"]/h1/text()"},
            ],
            "content": [
                {"xpath": "//div[@id='zoom']", },
                {"xpath": "//div[@id=\"UCAP-CONTENT\"]", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='sp_time']/font[2]/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
                {
                    "xpath": "//span[@class=\"font\"]/text()",
                    "regex": r"来源[: ：]\s*?(.*)",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='sp_time']/font[1]/text()",
                    "regex": r"发布日期[: ：]\s*?(.*)",
                },
                {
                    "xpath": "//div[@class=\"pages-date\"]/text()",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },

    #1.20
    #龙虎网
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
            #http://news.longhoo.net/2021/renshi_0119/462754.html
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
    #南报网
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
            #http://www.njdaily.cn/news/2021/0120/3078036004133663390.html
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
    #南京广播网(广播网本就数据少)
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
            #http://www.njgb.com/2021/0116/64515.shtml
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
    #金陵热线
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
            #http://edu.jlonilne.com/jiaoyu/jiaoyuredian/2017/0905/49.html
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
    #无锡新传媒
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
        "banner_news_side": ["//div[@class='tabN w100 clearfix']/div[2]//ul/li/a|//div[@class='tabN w100 clearfix']/div[3]//ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav w100 clearfix']/div/ul/li/a"],
        # 详情链接。
        "doc_links": [
            #http://www.wxrb.com/doc/2021/01/20/61084.shtml
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
    #无锡市政府网
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
            #http://www.wuxi.gov.cn/doc/2021/01/20/3170112.shtml
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
    #太湖明珠网
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
            #http://news.thmz.com/col50/2021-01-19/1275317.html
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
    #淮海网
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
            #http://www.huaihai.tv/folder7147/folder7248/2021-01-20/HEtWwT6vgz0qrwsb.html
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
    #武进新闻网
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
            #http://zt3.cz001.com.cn/2020-12/03/content_3871935.htm
            #http://www.wj001.com/news/jinriyaowen/2021-01-20/27281.html
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
    #中吴网
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
            #http://www.zhong5.cn/article-486293-1.html
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
    #常州在线
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
            #http://www.cz001.com.cn/index.php?c=Web&m=detail&id=2524
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
    #苏州新闻网
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
            #http://www.subaonet.com/2021/xwzt/2021szlh/2021szlh_ywdt/0120/148080.shtml
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
