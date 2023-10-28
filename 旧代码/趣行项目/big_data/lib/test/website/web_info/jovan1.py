configs = [

    # 2021年1月13日-3个
    # 中国文明网河北(95)
    {
        "platformName": "中国文明网河北",
        "sourceProvince": "河北省",
        "sourceCity": "河北省",
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
        "start_url": "http://hb.wenming.cn/",
        "cookie": "wdcid=33a2f2ff053e1ad9; wdlast=1610514822",
        # 首页头条新闻
        "headline_news": ["//div[@class='Hotnews11']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='ccw_focusImage-content']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//table[@width='435' and @border='0' and @cellspacing='0' and @cellspacing='0']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='dhl-a']//a"],
        # 详情链接。
        "doc_links": [
            # r"https?://[\w\-\.]+/\w+/\d{6,}/\w\d{6,}_\d+.html$",
            r"https?://[\w\-\.]+/\w+/\d+/\w\d+_\d+.html$",
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
                    # "regex": r".*来源：(.*)$",
                }
            ],
            "pubTime": [{"xpath": "//div[@id='time_tex']/text()[1]", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 河北省政协(95)
    {
        "platformName": "河北省政协",
        "sourceProvince": "河北省",
        "sourceCity": "河北省",
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
        "start_url": "http://www.hebzx.gov.cn/",
        "cookie": "wdcid=33a2f2ff053e1ad9; wdlast=1610514822",
        # 首页头条新闻
        "headline_news": ["//div[@class='div1200 toutiao']//a[@title]"],
        # 轮播信息
        "banner_news": ["//div[@class='hiSlider-wrap']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='columnlist newslist']/div[@class='list_bd']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']//a"],
        # 详情链接。
        "doc_links": [
            # r"https?://[\w\-\.]+/\w+/\d{6,}/\w\d{6,}_\d+.html$",
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\d+.shtml$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='title']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='m_ct_txt']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='info']/span[@class='ly']/text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                }
            ],
            "pubTime": [{"xpath": "//div[@class='info']/span[@class='date']", }, ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 河北青年报(95)
    {
        "platformName": "河北青年报",
        "sourceProvince": "河北省",
        "sourceCity": "河北省",
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
        "start_url": "http://www.hbqnb.com/index.html",
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["/html/body/div[@class='jrtt']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='slider']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='lhzl-t mb20']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='menu']//a"],
        # 详情链接。
        "doc_links": [
            # r"https?://[\w\-\.]+/\w+/\d{6,}/\w\d{6,}_\d+.html$",
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='title']//text()", },
            ],
            "content": [
                {"xpath": "//div[@class='content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='resource']/text()[1]",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='resource']/text()[2]",
                    "regex": r".*?发布时间[: ：]\s*?(.*)$",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },

    # 2021年1月14日-15个 90
    # 唐山市政府网
    {
        "platformName": "唐山市政府网",
        "sourceProvince": "河北省",
        "sourceCity": "唐山市",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.tangshan.gov.cn/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='toutiaotuijian']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='ln-cen1-left-pic left']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class=' xwdt_tab_bottom bd']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\d+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//p[@id='biaoti']/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='conN']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='main_div_title_time']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class='main_div_title_time']/text()",
                    "regex": r".*?发布时间[: ：]\s*?(.*)$",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 秦皇岛市政府网
    {
        "platformName": "秦皇岛市政府网",
        "sourceProvince": "河北省",
        "sourceCity": "秦皇岛市",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.qhd.gov.cn/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='ttnewN']/a"],
        # 轮播信息
        "banner_news": ["//div[@id='fsD1']/div[@id='D1pic1']//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='tabnrN']//ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']//li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+.do[?]uuid=",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='thirdtitle']/text()", },
                {"xpath": "//div[@class='article oneColumn pub_border']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='thirdtext']", },
                {"xpath": "//div[@id='CuPlayer']", },
                {"xpath": "//div[@class='pages_content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='thirdgnsty fl'][2]/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='pages-date']/span[@class='font']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='thirdgnsty fl'][1]/text()",
                    "regex": r".*?时间[: ：]\s*?(.*)$",
                },
                {
                    "//div[@class='pages-date'][1]/text()",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 秦皇岛新闻网1
    {
        "platformName": "秦皇岛新闻网",
        "sourceProvince": "河北省",
        "sourceCity": "秦皇岛市",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.qhdnews.com/",
        "cookie": "SF_cookie_1=41077003; __jsluid_h=1e534b360501674698672276f843145f; Hm_lvt_df4d3f66e0283d616d01a9241335f145=1610596929; Hm_lpvt_df4d3f66e0283d616d01a9241335f145=1610597688",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='focusBox']/ul[@class='pic']//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='main']/div[@class='main-col-01']/div[@class='sidebar_text']/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='nav']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/home/details[?]+.*",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='title']/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='detail']", },
                {"xpath": "//div[@id='body']/p", },
                {"xpath": "//div[@id='body']/div[not(contains(@class,'bottom'))]", },
                {"xpath": "//section[@data-role='outer']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='aticle-src']/text()",
                }
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
    # 邯郸市政府网
    {
        "platformName": "邯郸市政府网",
        "sourceProvince": "河北省",
        "sourceCity": "邯郸市",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.hd.gov.cn/",
        "cookie": "_gscu_318669530=10603445pk8vm155; _gscbrs_318669530=1; _gscs_318669530=10603445ab7i2755|pv:1; Hm_lvt_da5e30b702f3552b05284d4a2dd0d239=1610603445; Hm_lpvt_da5e30b702f3552b05284d4a2dd0d239=1610603445",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='bannerANDxw']/div[@class='lbt']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='ywgg_b']/div[@class='bl']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav clearfix']//ul[@id]/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d{6,}_\d+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='zzy_wz clearfix']/h4/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='TRS_Editor']", },
            ],
            "pubSource": [

            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='rq']/text()",
                    "regex": r".*?发布时间[: ：]\s*?(.*)$",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 邯郸新闻网
    {
        "platformName": "邯郸新闻网",
        "sourceProvince": "河北省",
        "sourceCity": "邯郸市",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.handannews.com.cn/",
        "cookie": "Hm_lvt_b3bb66284d3d39eb68af82075309f71e=1610605083; Hm_lpvt_b3bb66284d3d39eb68af82075309f71e=1610605083",
        # 首页头条新闻
        "headline_news": ["//div[@class='topnews']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='rolling']//ul[@class='rotaion_list']/li/a[1]"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='focus']//ul[@class='list1']/li/strong/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='navarea']//ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/content+/content_\d+.html$",
            r"https?://[\w\-\.]+/\w+/content+/\d{4,}-\d{2,}/\d{2}/content_\d+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class='main-title']/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='artibody']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='date-source']/a[@class='source ent-source']/text()",
                    # "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='date-source']/span[@class='date']/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 邢台市政府网(数据不多)
    {
        "platformName": "邢台市政府网",
        "sourceProvince": "河北省",
        "sourceCity": "邢台市",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.xingtai.gov.cn/",
        "cookie": "security_session_verify=13fa462559bbd96abcd2661308e85d8d",
        # 首页头条新闻
        "headline_news": ["//div[@class='toutiao']//a"],
        # 轮播信息
        "banner_news": ["//div[@id='tabSlide']/div[1]//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='cont']//ul[@class='swt']//li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='navbar']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\d+/t\d+_\d+.html$",
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/content_\d+.htm$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='article oneColumn pub_border']/h1/text()", },
                {"xpath": "//div[@class='divyykug']/div[@class='my_conbox']/h1", },
            ],
            "content": [
                {"xpath": "//div[@class='TRS_Editor']", },
                {"xpath": "//div[@class='pages_content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='pages-date']/span[@class='font']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//p[@class='sjly13s']/span[1]/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='pages-date']/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//p[@class='sjly13s']/span[2]/text()",
                    "regex": r".*?时间[: ：]\s*?(.*)$",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 邢台网
    {
        "platformName": "邢台网",
        "sourceProvince": "河北省",
        "sourceCity": "邢台市",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.xtrb.cn/",
        "cookie": "_D_SID=A18F8F2EDBDC95B5EC791D7E81A895B8",
        # 首页头条新闻
        "headline_news": ["//div[@class='NewsHot fl']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='banner']//p[@class='slide-title']/a"],
        # 轮播旁边新闻banner_new_side
        "banner_news_side": ["//div[@class='news_left']/div[@class='news']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='rmw_nav']/nav/div[@class='w1000']//span/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/content_\d+.htm$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "/html/body/div[@class='clearfix w1000 text_title']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='rwb_zw']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='clearfix w1000 text_title']/div[@class='box01']/div[@class='fl']/a/text()",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='clearfix w1000 text_title']/div[@class='box01']/div[@class='fl']/text()",
                    "regex": r".*?(.*)星期.*",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 保定市体育局
    {
        "platformName": "保定市体育局",
        "sourceProvince": "河北省",
        "sourceCity": "保定市",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://tyj.baoding.gov.cn/",
        "cookie": "_gscu_1086629998=1061438011x2ro44; JSESSIONID=090753C97A66FCBFE29E1EE3847BD6CC; _gscbrs_1086629998=1; _gscs_1086629998=10614380j6ni7g44|pv:8",
        # 首页头条新闻
        "headline_news": ["//table[@class='main_notice_title4']//a"],
        # 轮播信息
        "banner_news": [],  # flash的banner
        # 轮播旁边新闻banner_new_side
        "banner_news_side": ["//div[@class='right']/div[@id='xwzxcontainer']/div[@id='xwzxcon']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav_bg']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/content-\d+-\d+.html$",
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/content_\d+.htm$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='sj_nrbr']/table[@class='sj_bt']//td/text()", },
                {"xpath": "//div[@class='article oneColumn pub_border']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='sj_nrbr']//table[@class='sj_nr']", },
                {"xpath": "//div[@class='pages_content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='sj_nrbr']/table[@class='sj_zy']//td[1]//td/text()",
                    "regex": r".*?信息发布人[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='pages-date']/span[@class='font']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='sj_nrbr']/table[@class='sj_zy']//td[1]//td/text()",
                    "regex": r"发布时间[: ：]\s*?(.*)信息发布人.*",
                },
                {
                    "xpath": "//div[@class='pages-date']/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 保定市政府网1
    {
        "platformName": "保定市政府网",
        "sourceProvince": "河北省",
        "sourceCity": "保定市",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.baoding.gov.cn/",
        "cookie": "_gscu_1086629998=1061438011x2ro44; JSESSIONID=090753C97A66FCBFE29E1EE3847BD6CC; _gscbrs_1086629998=1; _gscs_1086629998=10614380j6ni7g44|pv:8",
        # 首页头条新闻
        "headline_news": ["//table[@class=\"sy_zdgzwz\"]//a"],
        # 轮播信息
        "banner_news": [],  # flash的banner
        # 轮播旁边新闻banner_new_side
        "banner_news_side": ["//div[@id=\"tab01\"]/ul/table[1]//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='zx_nav']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/content-\d+-\d+.html$",
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/content_\d+.htm$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='sj_nrbr']/table[@class='sj_bt']//td/text()", },
                {"xpath": "//div[@class='article oneColumn pub_border']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='sj_nrbr']//table[@class='sj_nr']", },
                {"xpath": "//div[@class='pages_content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='sj_nrbr']/table[@class='sj_zy']//td/text()",
                    "regex": r".*?信息发布人[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='pages-date']/span[@class='font']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='sj_nrbr']/table[@class='sj_zy']//td/text()",
                    "regex": r"发布时间[: ：]\s*?(.*)信息发布人.*",
                },
                {
                    "xpath": "//div[@class='pages-date']/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 张家口大境门网
    {
        "platformName": "张家口大境门网",
        "sourceProvince": "河北省",
        "sourceCity": "张家口市",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://zjkdjm.hebei.com.cn/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='dtt_title']/a"],
        # 轮播信息
        "banner_news": ["//div[@id='tabSlide']//p/a"],
        # 轮播旁边新闻banner_new_side
        "banner_news_side": ["//div[@class='sld_box']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='tou_lm']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d{4,}/\d{2,}/\d{2}/\d+.shtml$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='g_width content']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='text']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='post_source yh']/text()[1]",
                    # "regex": r".*?信息发布人[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='post_source yh']/text()[2]",
                    # "regex": r"发布时间[: ：]\s*?(.*)信息发布人.*",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 张家口市政府网
    {
        "platformName": "张家口市政府网",
        "sourceProvince": "河北省",
        "sourceCity": "张家口市",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.zjk.gov.cn/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='toutiao phone-hide']/a[@class='title']"],
        # 轮播信息
        "banner_news": ["//div[@class='phone-box carousel-box']/ul/li/p[@class='title']/a"],
        # 轮播旁边新闻banner_new_side
        "banner_news_side": ["//div[@class='col-c']/div[@class='con']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/content+/\d+/\d+.html$",
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/content_\d+.htm$",
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\d+/index.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='detail-box']/h1/text()", },
                {"xpath": "//div[@class='article oneColumn pub_border']/h1/text()", },
                {"xpath": "//h2[@class='cont_title']/text()", },
                {"xpath": "//div[@class='content']/div[@class='top-info']/h1[@class='t-type2']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='detail-box']/div[@class='detail']", },
                {"xpath": "//div[@class='pages_content']", },
                {"xpath": "//div[@id='zoom']", },
                {"xpath": "//div[@class='content']//div[@id='content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='info']/span[@class='fl']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='pages-date']/span[@class='font']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='content']//div[@class='info']/text()",
                    "regex": r"发布机构[: ：]\s*?(.*)浏览次数.*",
                },

            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='info']/span[@class='fl']/text()",
                    "regex": r".*?(.*)来源.*",
                },
                {
                    "xpath": "//div[@class='pages-date']/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//li[@class='xl_shijian']",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='content']//div[@class='info']/text()",
                    "regex": r"发布时间[: ：]\s*?(.*)发布机构.*",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 崇礼新闻网1
    {
        "platformName": "崇礼新闻网",
        "sourceProvince": "河北省",
        "sourceCity": "张家口市",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.clxxww.com/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='cl-headline']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='slider']//ul/li//a"],
        # 轮播旁边新闻banner_new_side
        "banner_news_side": ["//div[@class='cl-focuslist']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='cl-menu']/div/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/index.php[?]m=content&c=index&a=show&catid=+\d+&id=+.*",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//p[@class='news-government-title']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='news-government-con']/div[1]", },
            ],
            "pubSource": [

            ],
            "pubTime": [
                {
                    "xpath": "//p[@class='news-government-copy']/span[1]/text()",
                    "regex": r".*?时间[: ：]\s*?(.*)$",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 张家口市康保县政府网
    {
        "platformName": "张家口市康保县政府网",
        "sourceProvince": "河北省",
        "sourceCity": "张家口市",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.zjkkb.gov.cn/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": [],  # flash的banner
        # 轮播旁边新闻banner_new_side
        "banner_news_side": ["//div[@class='conxwr']/div[@id='tab01']/ul/table[@class='l_xwzxlist1']/tbody/tr/td[1]/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='zx_nav']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/content-\d+-\d+.html$",
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/content_\d+.htm$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='sj_nrbr']/table[@class='sj_bt']//td/text()", },
                {"xpath": "//div[@class='article oneColumn pub_border']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='sj_nrbr']//table[@class='sj_nr']", },
                {"xpath": "//div[@class='pages_content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='sj_nrbr']/table[@class='sj_zy']//td/text()",
                    "regex": r".*?信息发布人[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='pages-date']/span[@class='font']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='sj_nrbr']/table[@class='sj_zy']//td/text()",
                    "regex": r"发布时间[: ：]\s*?(.*)信息发布人.*",
                },
                {
                    "xpath": "//div[@class='pages-date']/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 张家口市怀来县政府网
    {
        "platformName": "张家口市怀来县政府网",
        "sourceProvince": "河北省",
        "sourceCity": "张家口市",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.huailai.gov.cn/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='toutiao']//a[@class='title']"],
        # 轮播信息
        "banner_news": ["//div[@class='carousel-box fl mt20']/ul/li/a"],
        # 轮播旁边新闻banner_new_side
        "banner_news_side": ["//div[@id='switch1']/div[@class='col-con']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav-box']/div[@class='container']/div[@class='nav fl']/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/content+/\d+/\d+.html$",
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/content_\d+.htm$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='container']/div[@class='detail-box']/h1/text()", },
                {"xpath": "//div[@class='article oneColumn pub_border']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='detail-box']/div[@class='detail']", },
                {"xpath": "//div[@class='pages_content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='info']/span[@class='fl']/text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='pages-date']/span[@class='font']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='info']/span[@class='fl']/text()",
                    "regex": r"发布日期[: ：]\s*?(.*)来源.*",
                },
                {
                    "xpath": "//div[@class='pages-date']/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                }
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 山西省政府网1
    {
        "platformName": "山西省政府网",
        "sourceProvince": "山西省",
        "sourceCity": "",
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
        "start_url": "http://www.shanxi.gov.cn/",
        "cookie": "insert_cookie=21719132; _trs_uv=kjwujtx2_695_wed; _trs_ua_s_1=kjwujtx2_695_yyl; JSESSIONID=E97108122C87A54AAAAF242618AC1B5F",
        # 首页头条新闻
        "headline_news": ["//div[@class='headline oflow-hd circular-bl box-shadow-com']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='shxidx-wrapper']/div/a"],
        # 轮播旁边新闻banner_new_side
        "banner_news_side": ["//div[@class='mt10 oflow-hd'][1]/div[@class='tab-flag-construck']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='main-nav-box mg-ltrb-center position-relative']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+/t\d+_\d+.shtml$",
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\d+/t\d+_\d+.shtml$",
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\w+/\d+/t\d+_\d+.shtml$",
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/content_\d+.htm$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='detail-article-title oflow-hd']//text()", },
                {"xpath": "//div[@class='article oneColumn pub_border']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='TRS_Editor']", },
                {"xpath": "//div[@class='pages_content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//ul[@class='detail-article-infos oflow-hd']/li[@class='article-infos-source left']/span[2]/text()",
                    # "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='pages-date']/span[@class='font']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//ul[@class='detail-article-infos oflow-hd']/li[@class='article-infos-source left']/span[1]/text()",
                    # "regex": r"发布日期[: ：]\s*?(.*)来源.*",
                },
                {
                    "xpath": "//div[@class='pages-date']/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                }
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },

    # 2021年1月15日-15个 90
    # 山西卫计委
    {
        "platformName": "山西卫计委",
        "sourceProvince": "山西省",
        "sourceCity": "",
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
        "start_url": "http://wjw.shanxi.gov.cn/",
        "cookie": "_trs_uv=kjwujtx2_695_wed",
        # 首页头条新闻
        "headline_news": ["//div[@class='news_No1']/div[@class='news_title']/a"],
        # 轮播信息
        "banner_news": ["//div[@class='slidePic']/div[@id='slide-holder']/div[@id='slide-runner']/a"],
        # 轮播旁边新闻banner_new_side
        "banner_news_side": ["//div[@class='news']/div[@class='news_box']//ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']/ul/li/a[@class='link']"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+.hrh$",
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/content_\d+.htm$",  # 中国政府网
            # r"https?://[\w\-\.]+/static/tpl/datailpage/dzpage.html[?]itemId=.*$",  # 全国党媒平台-ifrme
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='boxC']/h3/text()", },
                {"xpath": "//div[@class='article oneColumn pub_border']/h1/text()", },  # 中国政府网
            ],
            "content": [
                {"xpath": "//div[@class='boxC']/div[@class='ze-art']", },
                {"xpath": "//div[@class='pages_content']", },  # 中国政府网
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='boxC']/div[@class='artxx']/text()",
                    "regex": r"文章来源[: ：]\s*?(.*)浏览.*",
                },
                {  # 中国政府网
                    "xpath": "//div[@class='pages-date']/span[@class='font']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='boxC']/div[@class='artxx']/text()",
                    "regex": r"发布时间[: ：]\s*?(.*)发布人.*",
                },
                {  # 中国政府网
                    "xpath": "//div[@class='pages-date']/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                }
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 山西新闻出版广电局1
    {
        "platformName": "山西新闻出版广电局",
        "sourceProvince": "山西省",
        "sourceCity": "",
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
        "start_url": "http://gdj.shanxi.gov.cn/",
        "cookie": "_trs_uv=kjwujtx2_695_wed; _gscu_216566774=106775814lj0lr39; _gscbrs_216566774=1; _gscs_216566774=10677581rmzteg39|pv:1",
        # 首页头条新闻
        "headline_news": [
            "//div[@class='header-line']/dl[@class='header-line-news']//a[not(contains(@class,'header-more'))]"],
        # 轮播信息
        "banner_news": ["//div[@class='shxidx-wrapper']/div[@class='content-imgs-slide-item']/a[@class='sxrta-item']"],
        # 轮播旁边新闻banner_new_side
        "banner_news_side": [
            "//dd[@class='tab-flag-construck']/div[contains(@class,'slide-news-tabox common-tab-content-box')]//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav-box']/div[@class='nav-inner']/ul[@class='nav-list']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+/t\d+_\d+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='detail-article-title oflow-hd']//text()", },
            ],
            "content": [
                {"xpath": "//div[@class='TRS_Editor']", },
            ],
            "pubSource": [
                {
                    "xpath": "//li[@class='article-infos-source left']/span[2]/text()",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//li[@class='article-infos-source left']/span[1]/text()",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 山西信息港
    {
        "platformName": "山西信息港",
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
        "start_url": "http://www.zmgov.com/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": [],
        # 轮播旁边新闻banner_new_side
        "banner_news_side": [],
        # 导航信息
        "channel_info_xpath": ["//div[@class='leader']/div[@class='pull_down']/div[@class='leadertext-box']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/detail/id+/.*$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='article']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='article']/div[@class='d_content']/p", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='article']/div[@class='d_time']/span/text()",
                    "regex": r"[\u4E00-\u9FA5\s]+",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='article']/div[@class='d_time']/span/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 太原晚报网
    {
        "platformName": "太原晚报网",
        "sourceProvince": "山西省",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.tywbw.com/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@id='KinSlideshow']//div[@id='KSS_content']/a"],
        # 轮播旁边新闻banner_new_side
        "banner_news_side": ["//div[@id='news']/div[not(contains(@id,'top'))]//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='nav']/div[@id='nav1']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/c/\d{4,}-\d{2,}/\d{2}/content_\d+.htm$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='container padding-big-top'][2]/h1/text()", },
                {"xpath": "//div[@id='lside']/div[@id='clist']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='detail']", },
                {"xpath": "//div[@id='clist']/div[@id='ct']", },
            ],
            "pubSource": [
                {
                    "xpath": "//p[@class='ly']/span[1]/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                }, {
                    "xpath": "//div[@id='clist']/div[@id='dt']/p/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//p[@class='ly']/span[2]/text()",
                },
                {
                    "xpath": "//div[@id='clist']/div[@id='dt']/p/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})",
                },

            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 太原市政府网
    {
        "platformName": "太原市政府网",
        "sourceProvince": "山西省",
        "sourceCity": "",
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
        "start_url": "http://www.taiyuan.gov.cn/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='headline oflow-hd circular-bl box-shadow-com']/div[@class='headline-big']/a"],
        # 轮播信息
        "banner_news": ["//div[@class='bd']/div[@class='tempWrap']/ul/li/div/a"],
        # 轮播旁边新闻banner_new_side
        "banner_news_side": ["//div[contains(@id,'con_clicka')]//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav fr']/ul[@class='ul01']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d{4,}/\d{2,}/\d{2}/\d+.shtml$",
            r"https?://[\w\-\.]+/\w+/\w+/\d+/t\d+_\d+.shtml$",
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\d+/t\d+_\d+.shtml$",
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\w+/\d+/t\d+_\d+.shtml$",
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/content_\d+.htm$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='pd20 news_con']/h3[contains(@class,'text-center yahei')][1]/text()", },
                {"xpath": "//div[@class='detail-article-title oflow-hd']//text()", },
                {"xpath": "//div[@class='article oneColumn pub_border']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='zoom']", },
                {"xpath": "//div[@class='TRS_Editor']", },
                {"xpath": "//div[@class='pages_content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//p[@class='date font12 mgt20 grey text-center']/text()",
                    "regex": r"发布机构[: ：]\s*?(.*)更新时间.*",

                },
                {
                    "xpath": "//ul[@class='detail-article-infos oflow-hd']/li[@class='article-infos-source left']/span[2]/text()",
                    # "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='pages-date']/span[@class='font']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//p[@class='date font12 mgt20 grey text-center']/text()",
                    "regex": r"更新时间[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//ul[@class='detail-article-infos oflow-hd']/li[@class='article-infos-source left']/span[1]/text()",
                    # "regex": r"发布日期[: ：]\s*?(.*)来源.*",
                },
                {
                    "xpath": "//div[@class='pages-date']/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                }
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 大同新闻网1
    {
        "platformName": "大同新闻网",
        "sourceProvince": "山西省",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.dtnews.cn/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//ul[@class='items']/li/a"],
        # 轮播旁边新闻banner_new_side
        "banner_news_side": ["//div[@class='today']/div[@class='td_text']//a[not(contains(@class,'td_news'))]"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/\d+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='text']/dl/dt/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='news_cont']//p", },
            ],
            "pubSource": [

            ],
            "pubTime": [

            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 大同市政府网
    {
        "platformName": "大同市政府网",
        "sourceProvince": "山西省",
        "sourceCity": "",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.dt.gov.cn/dtzww/index.shtml",
        "cookie": "UM_distinctid=17704df17478f-02ad401fbb40c3-59442e11-100200-17704df1748316; CNZZDATA5636633=cnzz_eid%3D1923978641-1610692759-%26ntime%3D1610692759; _gscu_824660600=10694465my54w110; _gscbrs_824660600=1; _gscs_824660600=10694465jxn2ng10|pv:6",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='slides_container']/div[@class='slides_control']/div/a"],
        # 轮播旁边新闻banner_new_side
        "banner_news_side": ["//div[@class='pjjy_middle_center cl']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='tabs']/div[@class='snap-box']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d{6,}/\w+.shtml$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='conbox']//ucaptitle/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='content']//ucapcontent", },
            ],
            "pubSource": [
                {"xpath": "//div[@class='source']/div[@class='sdiv'][2]//ucapsource/text()", },
            ],
            "pubTime": [
                {"xpath": "//div[@class='source']/div[@class='sdiv'][1]//publishtime/text()", },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 朔州市政府网
    {
        "platformName": "朔州市政府网",
        "sourceProvince": "山西省",
        "sourceCity": "",
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
        "start_url": "http://www.shuozhou.gov.cn/",
        "cookie": "BIGipServerMHWZ-WEB_all=2516587180.0.0000; _trs_uv=kjxyovct_348_6afm; _trs_ua_s_1=kjxyovct_348_1sp2",
        # 首页头条新闻
        "headline_news": ["//div[@class='main'][1]/div[2]/a"],
        # 轮播信息
        "banner_news": ["//div[@class='jdt']/div[@id='idTransformView2']/ul[@id='idSlider2']/li/a"],
        # 轮播旁边新闻banner_new_side
        "banner_news_side": [
            "//div[@class='xw']/div[@class='xwb fr']/div[@class='jrsz']/div[@id='tab1']/div[@class='bd']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']/ul/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d{6,}/t\d+_\d+.html$",
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/content_\d+.htm$",  # 中国政府网
            # r"https?://[\w\-\.]+/static/tpl/datailpage/dzpage.html[?]itemId=.*$",  # 全国党媒平台-ifrme
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='bt']/text()", },
                {"xpath": "//div[@class='detail-article-title oflow-hd']//text()", },
                {"xpath": "//div[@class='article oneColumn pub_border']/h1/text()", },  # 中国政府网
            ],
            "content": [
                {"xpath": "//div[@class='TRS_Editor']", },
                {"xpath": "//div[@class='pages_content']", },  # 中国政府网
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='fbxx']/span[2]/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//ul[@class='detail-article-infos oflow-hd']/li[@class='article-infos-source left']/span[2]/text()",
                    # "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {  # 中国政府网
                    "xpath": "//div[@class='pages-date']/span[@class='font']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='fbxx']/span[1]/text()",
                },
                {
                    "xpath": "//ul[@class='detail-article-infos oflow-hd']/li[@class='article-infos-source left']/span[1]/text()",
                    # "regex": r"发布日期[: ：]\s*?(.*)来源.*",
                },
                {  # 中国政府网
                    "xpath": "//div[@class='pages-date']/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                }
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 朔州新闻网
    {
        "platformName": "朔州新闻网",
        "sourceProvince": "山西省",
        "sourceCity": "",
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
        "start_url": "http://www.sxsznews.com/",
        "cookie": "newsznews_P8SESSION=b3d755b5c5b19ef5; Hm_lvt_3fb27c0473ccf4f73fc919ecca3b1abc=1610698031; yunsuo_session_verify=e93ec29f0c708f5540656af861efe05b; Hm_lpvt_3fb27c0473ccf4f73fc919ecca3b1abc=1610698036; zycna=BRWNVYA0XHcBAWpyUTfKFwFN",
        # 首页头条新闻
        "headline_news": ["//ul[@class='label_headline10']/li/a"],
        # 轮播信息
        "banner_news": ["//div[@class='focuspic']//div[@class='pic']/a"],
        # 轮播旁边新闻banner_new_side
        "banner_news_side": ["//div[@class='slideTxtBox']//div[@class='newlist']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='navigation winner']/div[@class='navbar clearfix']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/html+/\d+/content-\d+.shtml$",
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/c_\d+.htm$",  # 新华社
            r"https?://[\w\-\.]+/\w+/\w+/\d{4,}-\d{2,}/\d{2}/c_\d+.htm$",  # 新华社
            # r"https?://[\w\-\.]+/static/tpl/datailpage/dzpage.html[?]itemId=.*$",  # 全国党媒平台-ifrme
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='actitle']//text()", },
                {"xpath": "//div[@class='conTit']/h2[@class='title']/text()", },  # 新华社
                {"xpath": "//div[@class='h-title']/text()", },  # 新华社
            ],
            "content": [
                {"xpath": "//div[@id='content']", },
                {"xpath": "//div[@class='xlcontent']", },  # 新华社
                {"xpath": "//div[@id='p-detail']/div[@class='main-aticle']", },  # 新华社
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='ac_date']/div[@class='ac_fl']/span[1]/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
                {  # 新华社
                    "xpath": "//div[@class='h-info']/span[@class='sub-src']/span[@class='aticle-src']/text()",
                    # "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {  # 新华社
                    "xpath": "//div[@class='info']/text()[2]",
                    # "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='ac_date']/div[@class='ac_fl']/span/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})",
                },
                {  # 新华社
                    "xpath": "//div[@class='h-info']/span[@class='sub-time']/span[@class='h-time']//text()",
                    # "regex": r"发布日期[: ：]\s*?(.*)来源.*",
                },
                {  # 新华社
                    "xpath": "//div[@class='info']/text()[1]",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                }
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 忻州在线1
    {
        "platformName": "忻州在线",
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
        "start_url": "http://www.xzrbw.com/",
        "cookie": "JSESSIONID=AF98B3A644FEB7857B90347DF15FD2DF",
        # 首页头条新闻
        "headline_news": ["//div[@class='toutiao']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='mkeFocus']/div[@class='mkeUl']//a"],
        # 轮播旁边新闻banner_new_side
        "banner_news_side": ["//div[@class='xinwen']/ul[contains(@class,'wenzhang')]//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/info/\d+/\d+.htm$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//td[@class='titlestyle42947']", },
            ],
            "content": [
                {"xpath": "//td[@class='contentstyle42947']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='authorstyle42947']/text()",
                }
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class='timestyle42947']/text()",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 忻州网
    {
        "platformName": "忻州网",
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
        "start_url": "http://news.xinzhou.org/",
        "cookie": "__tins__370812=%7B%22sid%22%3A%201610700268936%2C%20%22vd%22%3A%201%2C%20%22expires%22%3A%201610702068936%7D; __51cke__=; __51laig__=1",
        # 首页头条新闻
        "headline_news": [
            "//div[@align='center' and @style='width:1180px; margin:0px auto 0px auto; height:auto']/div[@style='background-color:#FFFFFF;padding-top:15px;']//a"],
        # 轮播信息
        "banner_news": ["//div[@id='myFocus']/div[@class='txt']/ul/li/a"],
        # 轮播旁边新闻banner_new_side
        "banner_news_side": ["/html/body/div[4]/div[2]/div[2]/div/div//a"],
        # 导航信息
        "channel_info_xpath": ["//td/a[@class='white14_24a']"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/html+/\d+/\w+_\d+/\d+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='Article']/h1[1]/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='Article']//div[@class='content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@id='Article']/h1[2]/span[1]//text()",
                    "regex": r"来源[: ：]\s*?(.*)作者.*",
                },

            ],
            "pubTime": [
                {
                    "xpath": "//div[@id='Article']/h1[2]/span[1]//text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 忻州市政府网
    {
        "platformName": "忻州市政府网",
        "sourceProvince": "山西省",
        "sourceCity": "",
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
        "start_url": "https://www.sxxz.gov.cn/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='txtMarquee-left']//ul[@class='infoList']/a"],
        # 轮播信息
        "banner_news": ["//div[@id='slideBox']/div[@class='bd2']/ul/li/a[@class='title']"],
        # 轮播旁边新闻banner_new_side
        "banner_news_side": ["//div[@class='subject-left1']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav oflow-hd']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+/t\d+_\d+.shtml$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class='article-title']/text()", },
                {"xpath": "//h2[@class='article-title']/text()", },
                {"xpath": "//h3[@class='article-title']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='TRS_Editor']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='article-filed']//text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },

            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='article-filed']//text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 阳泉市政府网
    {
        "platformName": "阳泉市政府网",
        "sourceProvince": "山西省",
        "sourceCity": "",
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
        "start_url": "http://www.yq.gov.cn/",
        "cookie": "_trs_uv=kjy35jd2_1325_eo9m; _trs_ua_s_1=kjy35jd2_1325_27ps",
        # 首页头条新闻
        "headline_news": ["//div[@class='notice left']/h3/a"],
        # 轮播信息
        "banner_news": ["//div[@class='yx-rotaion-content left']/div[@class='yx-rotaion']/ul[@class='txt']/li/a"],
        # 轮播旁边新闻banner_new_side
        "banner_news_side": ["//div[contains(@id,'con_two_')]/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']/ul/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+/t\d+_\d+.shtml$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='article-font-zoom']/h2/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='TRS_Editor']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@id='article-font-zoom']/h3/span[2]/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },

            ],
            "pubTime": [
                {
                    "xpath": "//div[@id='article-font-zoom']/h3/text()",
                    # "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 吕梁新闻网1
    {
        "platformName": "吕梁新闻网",
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
        "start_url": "http://www.sxllnews.cn/",
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='headlines']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='Rolling']//div[@class='pic']/a"],
        # 轮播旁边新闻banner_new_side
        "banner_news_side": ["//div[@class='Rolling-left']/ul[@class='ul']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='navs']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/content+/\d{4,}-\d{2,}/\d+/\d+_\d+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='text']/h1/text()", },
                {"xpath": "//div[@class='largeImages-main']/h1/text()", },
                {"xpath": "//div[@class='player']/h3/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='text']/div[@class='content-main']", },
                {"xpath": "//div[@class='largeImages-main']/div[@class='largeImages-info']/following-sibling::*", },
                {"xpath": "//div[@id='flashContent']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='text']/div[1]//text()",
                    "regex": r".*?编辑[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='largeImages-main']/div[@class='largeImages-info']/span//text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='player']/div[@class='source']//text()",
                    "regex": r".*?文章来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='text']/div[1]/i[1]/text()",
                    # "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",
                },
                {
                    "xpath": "//div[@class='largeImages-main']/div[@class='largeImages-info']/span[1]/text()",
                    # "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",
                },
                {
                    "xpath": "//div[@class='player']/div[@class='source']/i[1]/text()",
                    "regex": r".*?发布时间[: ：]\s*?(.*)$",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 吕梁网
    {
        "platformName": "吕梁网",
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
        "start_url": "http://www.ll.gov.cn/",
        "cookie": "Hm_lvt_f1cb683695270755708f191e8500c82c=1610706294; Hm_lpvt_f1cb683695270755708f191e8500c82c=1610706294",
        # 首页头条新闻
        "headline_news": ["//div[@class='NavLink']/ul/marquee/a"],
        # 轮播信息-flash
        "banner_news": [],
        # 轮播旁边新闻banner_new_side
        "banner_news_side": ["//div[@class='news_toutiao']/div/a[@class='STYLEtoutiao']"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='subNav']/ul[@class='sub1']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d{6,}/\d+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='content']/div[@id='artName']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='artCon']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@id='infoCon']/span[2]//text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@id='infoCon']/span[1]/text()",
                    # "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },

    # 2021年1月20日-12个
    # 长治新闻网
    {
        "platformName": "长治新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.changzhinews.com/",
        # 首页头条新闻
        "headline_news": ["//div[@class='tt']//a"],
        # 轮播信息-flash,抓不到
        "banner_news": [],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='wx' or @class='wx_tt']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='menu']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}-\d{2}/\d+.html$",
            r"https?://[\w\-\.]+/\w+/\w+/\d{4,}-\d{2,}-\d{2}/\d+.html$",
            r"https?://[\w\-\.]+/\d{4,}/\d{2,}/\d{2}/\w+.shtml$",  # 央视网新闻
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//p[@class='fywztitle']/text()"},
                {"xpath": "//div[@class='cnt_bd']/h1/text()"},
                {"xpath": "//div[@id='title_area']/h1/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='fymain']/div[@id='kzzt']"},
                {"xpath": "//div[@class='cnt_bd']/p"},
                {"xpath": "//div[@id='text_area']"},
            ],
            # 来源：央视新闻客户端 2021年01月17日 12:55
            "pubSource": [
                {
                    "xpath": "//table[@class='fywzzz']//td[1]/a/text()",
                },
                {
                    "xpath": "//span[@class='info']/i/text()",
                    "regex": r"来源[: ：]\s*?(.*)20.*",
                },
                {
                    "xpath": "//div[@id='title_area']/div[@class='info']/text()",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//table[@class='fywzzz']//td[1]/text()[1]",
                    "regex": r".*?(.*)来源.*",
                },
                {
                    "xpath": "//span[@class='info']/i/text()",
                    "regex": r"(\d{4}年\d{1,2}月\d{1,2}日\s\d{1,2}:\d{1,2})",

                },
                {
                    "xpath": "//div[@id='title_area']/div[@class='info']/span/text()",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # i长治网
    {
        "platformName": "i长治网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.ichangzhi.com.cn/",
        # 首页头条新闻
        "headline_news": ["//table[1]//tr/td/table[6]//tr/td[3]/a"],
        # 轮播信息
        "banner_news": ["//div[@id='bd1lfimg']/div/dl/dd//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//td[@class='listxwtt']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d{4,}-\d{2,}-\d{2}/\d+.html",
            r"https?://[\w\-\.]+/\w+/\w+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//td[@class='icznr']//text()"},
            ],
            "content": [
                {"xpath": "//td[@class='iczcontent']"},
            ],
            # 来源：央视新闻客户端 2021年01月17日 12:55
            "pubSource": [
                {
                    "xpath": "//div[@class='lmly']/ul/li[1]/a/text()",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='lmly']/ul/li[2]/text()",
                    "regex": r".*?发布时间[: ：]\s*?(.*)$",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 晋城新闻网
    {
        "platformName": "晋城新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.jcnews.com.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='toutiao']/a"],
        # 轮播信息
        "banner_news": ["//ul[@class='rotaion_list']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='jdxw']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='logo']/div[@class='jz logo1']/div/table//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d{6,}/t\d+_\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='article']/h1[@id='title']/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='TRS_Editor']"},
            ],
            # 来源：央视新闻客户端 2021年01月17日 12:55
            "pubSource": [
                {
                    "xpath": "//div[@class='source']/span[2]/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='source']/span[@class='time']/text()",
                    # "regex": r".*?发布时间[: ：]\s*?(.*)$",
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 临汾新闻网
    {
        "platformName": "临汾新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.lfxww.com/",
        # 首页头条新闻
        "headline_news": ["//div[@class='topnews-strong t-news']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='swiper-hd']//div[@class='hd-title']//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='n-c-Focus']/ul[@class='list-light-gray']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='menu']//div[@class='m-l-content fl']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+.html",
            r"https?://[\w\-\.]+/\w+/\w+/\d+.html",
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\d+.html",
            r"https?://[\w\-\.]+/\d{4,}/\d{2,}/\d{2}/\w+.shtml$",  # 央视网新闻
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h2[@class='h2 text-center xb-h2']/text()"},
                {"xpath": "//div[@class='piccontext']/h2/text()"},
                {"xpath": "//div[@class='cnt_bd']/h1/text()"},
                {"xpath": "//div[@id='title_area']/h1/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='col-md-12 nry jcontent']"},
                {"xpath": "//div[@class='picshow']"},
                {"xpath": "//div[@class='cnt_bd']/p"},
                {"xpath": "//div[@id='text_area']"},
            ],
            # 来源：央视新闻客户端 2021年01月17日 12:55
            "pubSource": [
                {
                    "xpath": "//div[@class='col-md-8 xb-left']/h3[@class='h4 text-center xb-h4']/text()",
                    "regex": r"来源[: ：]\s*?(.*)浏览次数.*",
                },
                {
                    "xpath": "//span[@class='info']/i/text()",
                    "regex": r"来源[: ：]\s*?(.*)20.*",
                },
                {
                    "xpath": "//div[@id='title_area']/div[@class='info']/text()",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='col-md-8 xb-left']/h3[@class='h4 text-center xb-h4']/text()",
                    "regex": r".*?(.*)来源.*",
                },
                {
                    "xpath": "//div[@class='source_left']/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})",

                },
                {
                    "xpath": "//span[@class='info']/i/text()",
                    "regex": r"(\d{4}年\d{1,2}月\d{1,2}日\s\d{1,2}:\d{1,2})",

                },
                {
                    "xpath": "//div[@id='title_area']/div[@class='info']/span/text()",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 临汾市政府网
    {
        "platformName": "临汾市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://linfen.gov.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='headline oflow-hd circular-bl box-shadow-com']//a"],
        # 轮播信息
        "banner_news": [
            "//div[@class='shxidx-wrapper']/div[@class='content-imgs-slide-item']/a[@class='content-imgs-slide-item']"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='subject-left1']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='main-nav left']//a"],
        # 详情链接。
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/contents+/\d+/\d+.html$",
            r"https?://[\w\-\.]+/\w+/\w+/\d+/t\d+_\d+.shtml$",  # 山西省政府网
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\d+/t\d+_\d+.shtml$",  # 山西省政府网
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\w+/\d+/t\d+_\d+.shtml$",  # 山西省政府网
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/content_\d+.htm$",  # 中国政府网
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='cont w']/h1//text()", },
                {"xpath": "//div[@class='detail-article-title oflow-hd']//text()", },  # 山西省政府网
                {"xpath": "//div[@class='article oneColumn pub_border']/h1/text()", },  # 中国政府网
            ],
            "content": [
                {"xpath": "//div[@id='UCAP-CONTENT']", },
                {"xpath": "//div[@class='TRS_Editor']", },  # 山西省政府网
                {"xpath": "//div[@class='pages_content']", },  # 中国政府网
            ],
            "pubSource": [
                {  # 山西省政府网
                    "xpath": "//ul[@class='detail-article-infos oflow-hd']/li[@class='article-infos-source left']/span[2]/text()",
                    # "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {  # 中国政府网
                    "xpath": "//div[@class='pages-date']/span[@class='font']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='pages-date']/text()[1]",
                    # "regex": r"发布日期[: ：]\s*?(.*)来源.*",
                },
                {  # 山西省政府网
                    "xpath": "//ul[@class='detail-article-infos oflow-hd']/li[@class='article-infos-source left']/span[1]/text()",
                    # "regex": r"发布日期[: ：]\s*?(.*)来源.*",
                },
                {  # 中国政府网
                    "xpath": "//div[@class='pages-date']/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                }
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 运城市政府网
    {
        "platformName": "运城市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.yuncheng.gov.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='news_top_one']/a"],
        # 轮播信息
        "banner_news": ["//div[@class='tempWrap']/ul/li/h2/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='home_common_newslist home_newslist']/ul[@class='list']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='hd1 mainnav']/ul/li/a"],
        # 详情链接。
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/doc+/\d{4,}/\d{2,}/\d{2,}/\d+.shtml$",
            r"https?://[\w\-\.]+/\w+/\w+/\d+/t\d+_\d+.shtml$",  # 山西省政府网
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\d+/t\d+_\d+.shtml$",  # 山西省政府网
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\w+/\d+/t\d+_\d+.shtml$",  # 山西省政府网
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/content_\d+.htm$",  # 中国政府网
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='info_title']/text()", },
                {"xpath": "//div[@class='detail-article-title oflow-hd']//text()", },  # 山西省政府网
                {"xpath": "//div[@class='article oneColumn pub_border']/h1/text()", },  # 中国政府网
            ],
            "content": [
                {"xpath": "//div[@id='info_content']", },
                {"xpath": "//div[@class='TRS_Editor']", },  # 山西省政府网
                {"xpath": "//div[@class='pages_content']", },  # 中国政府网
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='attribute']/span[@class='info_source']/text()",
                    # "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {  # 山西省政府网
                    "xpath": "//ul[@class='detail-article-infos oflow-hd']/li[@class='article-infos-source left']/span[2]/text()",
                    # "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {  # 中国政府网
                    "xpath": "//div[@class='pages-date']/span[@class='font']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='attribute']/span[@class='infoe_time']/text()",
                    # "regex": r"发布日期[: ：]\s*?(.*)来源.*",
                },
                {  # 山西省政府网
                    "xpath": "//ul[@class='detail-article-infos oflow-hd']/li[@class='article-infos-source left']/span[1]/text()",
                    # "regex": r"发布日期[: ：]\s*?(.*)来源.*",
                },
                {  # 中国政府网
                    "xpath": "//div[@class='pages-date']/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                }
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 运城新闻网
    {
        "platformName": "运城新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.sxycrb.com/",
        # 首页头条新闻
        "headline_news": ["//div[@class='lead-news']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='tempWrap']/ul[@class='picList']/li/i/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='news-center']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav clearfix']//a"],
        # 详情链接。
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d{4,}-\d{2,}/\d{2,}/content_\d+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='detail-h']/h1//text()", },
                {"xpath": "//div[@class='largeImages-main']/h1//text()", },
            ],
            "content": [
                {"xpath": "//div[@class='detail-d']", },
                {"xpath": "//ul[@class='largeImages']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='detail-h']/p/span[1]/text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='largeImages-info']/span[4]/i/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='detail-h']/p/span[3]/text()",
                    "regex": r".*?时间[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='largeImages-info']/span[1]/text()",
                    # "regex": r"发布日期[: ：]\s*?(.*)来源.*",
                },

            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 安徽新广网
    {
        "platformName": "安徽新广网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://gdj.ah.gov.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='ind_tt_list']//a"],
        # 轮播信息
        "banner_news": ["//div[@id='myFocus01']/div[@class='txt']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='fr ls-newsbox']/div[@class='ls-newslist']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='navbar']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='ls-content-con']/h1[@class='newstitle']/text()", },
                {"xpath": "//div[@class='con_main']/h1[@class='gk_title']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='wzcon j-fontContent clearfix']", },
                {"xpath": "//div[@class='j-fontContent gkwz_contnet']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='newsinfo']/span[@class='wz_res']/i/text()",
                    # "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//span[@class='wz_res']/text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='newsinfo']/span[@class='wz_date']/i/text()",
                    # "regex": r"发布日期[: ：]\s*?(.*)来源.*",
                },
                {
                    "xpath": "//span[@class='wz_date']/text()",
                    "regex": r"\s*?发布时间[: ：]\s*?(.*)$",
                },

            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 安徽网
    {
        "platformName": "安徽网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.ahwang.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='headline mar-t-15 f-r']//a"],
        # 轮播信息
        "banner_news": ["//div[@id='headslide']/ul[@class='slides clearfix']/li/h2/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='nxw f-r m-t-15']/ul[@class='f-l']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='navigation']/nav//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d{4,}\d{2,}\d{2,}/\d+.html$",
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2,}/content_\d+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//article[@class='article-main']/h1/text()", },
                {"xpath": "//div[@class='article-main']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='article-content mar-t-20']", },
                {"xpath": "//div[@class='news_txt fontSizeBig clearfix']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='source']//text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//span[@class='source']/a/text()",
                    # "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='article-infos']/span[@class='date']/text()",
                    "regex": r"\s*?发布时间[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//span[@class='release-date']/text()",
                },

            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 安青网
    {
        "platformName": "安青网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.ahyouth.com/",
        # 首页头条新闻
        "headline_news": ["//div[@class='section1-title']/div[@class='section1-title-content']/h1/a"],
        # 轮播信息
        "banner_news": ["//div[@class='swiper-wrapper']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='scrollnews']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='mainnav']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/news+/\d{4,}\d{2,}\d{2,}/\d+.shtml$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='acrticle-title']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='acrticle-content']/div[@class='acrticle-p']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='acrticle-title-small-title']/text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='acrticle-title-small-title']/span[1]/text()",
                },

            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 皖工网
    {
        "platformName": "皖工网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.ahgrrb.com/",
        # 首页头条新闻
        "headline_news": ["//div[@class='headline']/span[@class='headline-title']//a"],
        # 轮播信息
        "banner_news": ["//div[@id='slider-wrap']/ul[@id='slider']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='recommend']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='page-top']/div[@class='page_header_category']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/html/detail+/\d{4,}\d{2,}\d{2,}/\d+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='cont-item1']/h2/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='cont-item2']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='item1-from']/text()",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class='item1-time']/text()",
                },

            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 江淮新闻网
    {
        "platformName": "江淮新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.jhxww.net/",
        # 首页头条新闻
        "headline_news": ["//div[@class='NewsTop']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='PicNews']//div[@class='item']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='HomeNews']/div[@class='NewsBox']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='Nav']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/cn/\w+/info_\d+.aspx[?]itemid=.*",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='ActiveContent']/div[@class='Atit']/h2/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='ActiveContent']/div[@class='ContentAbout']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='ins']/a/text()",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='ins']/text()[2]",
                },

            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 2021年1月21日-12个
    # 马鞍山市政府网
    {
        "platformName": "马鞍山市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.mas.gov.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='ind_dbt']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='ind_flash']//div[@class='txt']//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='list']//li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='navbar']/ul[@class='nav navbar-nav']/li/a"],
        # 详情链接。
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+.html$",
            r"https?://[\w\-\.]+/openness/detail/content+/\w+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class='newstitle']/text()", },
                {"xpath": "//h1[@class='u-dttit']/text()", },
                {"xpath": "//div[@class='interview-title']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='wzcon j-fontContent']", },
                {"xpath": "//div[@class='m-detailcont']/div[@id='zoom']", },
                {"xpath": "//div[@class='desc']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='wzfbxx clearfix']/text()[3]",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {  # 山西省政府网
                    "xpath": "//div[@class='wzfbxx clearfix']/text()[2]",
                    "regex": r".*?发布时间[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//li[@class='col-md-6 f-clearfix'][5]/div/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='in-info']/p[@class='p1']/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                }
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 淮北新闻网
    {
        "platformName": "淮北新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.hbnews.net/",
        # 首页头条新闻
        "headline_news": ["//p[@class='onenewstxt']/a"],
        # 轮播信息-flash,抓不到
        "banner_news": ["//div[@class='scroll_txt']//h2/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='w1lst lst f-r']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='menu']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}-\d{2,}/\w+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='title']/p/text()"},
            ],
            "content": [
                {"xpath": "//div[@class='mian']"},
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='soure']//text()",
                    "regex": r".*来源：(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class='time']/text()",
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 淮北市政府网
    {
        "platformName": "淮北市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.huaibei.gov.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='ttnews']/div[@class='tt_title']/a"],
        # 轮播信息
        "banner_news": ["//div[@id='myFocus01']/div[@class='txt']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='news_list']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='navbar']/ul[@class='nav navbar-nav']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+.html$",
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\d+.html$",
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/content_\d+.htm$",  # 中国政府网
            # r"https?://[\w\-\.]+/static/tpl/datailpage/dzpage.html[?]itemId=.*$",  # 全国党媒平台-ifrme
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class='newstitle']/text()", },
                {"xpath": "//div[@class='wenzhang']/h1[@class='wztit']/text()", },
                {"xpath": "//div[@class='article oneColumn pub_border']/h1/text()", },  # 中国政府网
            ],
            "content": [
                {"xpath": "//div[@id='zoom']", },
                {"xpath": "//div[@class='wzcon j-fontContent']", },
                {"xpath": "//div[@class='pages_content']", },  # 中国政府网
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='newsinfo newsinfo2']//text()",
                    "regex": r"信息来源[: ：]\s*?(.*)发布时间.*",
                },
                {
                    "xpath": "//span[@class='fbxx']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
                {  # 中国政府网
                    "xpath": "//div[@class='pages-date']/span[@class='font']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='newsinfo newsinfo2']//text()",
                    "regex": r".*?发布时间[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//span[@class='fbxx']/text()",
                    "regex": r".*?(.*)来源.*",
                },
                {  # 中国政府网
                    "xpath": "//div[@class='pages-date']/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                }
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 铜陵市政府网
    {
        "platformName": "铜陵市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.tl.gov.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='first_news']/a"],
        # 轮播信息
        "banner_news": ["//div[@class='focus_box']//ul[@class='listA']/li[@class='sub_li']/p/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='focus_box']/div[@class='f_right']/div[@class='four_down']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='h_down']/ul[@class='btnB btn']/li//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\d{6,}/t\d{6,}_\d+.html$",
            r"https?://[\w\-\.]+/\w+/\w+/\d+.html$",
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\d+.html$",
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/content_\d+.htm$",  # 中国政府网
            # r"https?://[\w\-\.]+/static/tpl/datailpage/dzpage.html[?]itemId=.*$",  # 全国党媒平台-ifrme
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='detail_title']/text()", },
                {"xpath": "//h1[@class='newstitle']/text()", },
                {"xpath": "//div[@class='wenzhang']/h1[@class='wztit']/text()", },
                {"xpath": "//div[@class='article oneColumn pub_border']/h1/text()", },  # 中国政府网
            ],
            "content": [
                {"xpath": "//div[@id='con']", },
                {"xpath": "//div[@id='zoom']", },
                {"xpath": "//div[@class='wzcon j-fontContent']", },
                {"xpath": "//div[@class='pages_content']", },  # 中国政府网
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='d_time']/span[2]/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='newsinfo newsinfo2']//text()",
                    "regex": r"信息来源[: ：]\s*?(.*)发布时间.*",
                },
                {
                    "xpath": "//span[@class='fbxx']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
                {  # 中国政府网
                    "xpath": "//div[@class='pages-date']/span[@class='font']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='d_time']/span[1]/text()",
                    # "regex": r".*?发布时间[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='newsinfo newsinfo2']//text()",
                    "regex": r".*?发布时间[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//span[@class='fbxx']/text()",
                    "regex": r".*?(.*)来源.*",
                },
                {  # 中国政府网
                    "xpath": "//div[@class='pages-date']/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                }
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 铜陵新闻网
    {
        "platformName": "铜陵新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.tlnews.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='tlnewstt']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='www51buycom']/ul[@class='51buypic']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='area_right']/div[@class='news' or @class='news2']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='tlmenu']/ul[@class='ul1']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d{4,}-\d{2,}/\d{2,}/content_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\w+/\d{4,}-\d{2,}/\d{2,}/content_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/c_\d+.htm$",  # 新华社
            r"https?://[\w\-\.]+/\w+/\w+/\d{4,}-\d{2,}/\d{2}/c_\d+.htm$",  # 新华社
            # r"https?://[\w\-\.]+/static/tpl/datailpage/dzpage.html[?]itemId=.*$",  # 全国党媒平台-ifrme
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='art']/h1[@id='spm_title']//text()", },
                {"xpath": "//div[@class='art']/h1/text()", },
                {"xpath": "//div[@class='conTit']/h2[@class='title']/text()", },  # 新华社
                {"xpath": "//div[@class='h-title']/text()", },  # 新华社
            ],
            "content": [
                {"xpath": "//div[@id='spm_content']", },
                {"xpath": "//div[@class='xlcontent']", },  # 新华社
                {"xpath": "//div[@id='p-detail']/div[@class='main-aticle']", },  # 新华社
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='art']/h2//text()",
                    "regex": r"来源[: ：]\s*?(.*)编辑.*",
                },
                {  # 新华社
                    "xpath": "//div[@class='h-info']/span[@class='sub-src']/span[@class='aticle-src']/text()",
                    # "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {  # 新华社
                    "xpath": "//div[@class='info']/text()[2]",
                    # "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//span[@id='spm_pubTime ']/text()",
                    # "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})",
                },
                {  # 新华社
                    "xpath": "//div[@class='h-info']/span[@class='sub-time']/span[@class='h-time']//text()",
                    # "regex": r"发布日期[: ：]\s*?(.*)来源.*",
                },
                {  # 新华社
                    "xpath": "//div[@class='info']/text()[1]",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                }
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 铜陵网络台
    {
        "platformName": "铜陵网络台",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.tlbts.com/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@id='slider']/div[@class='carousel-inner']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='content']/article[@class='excerpt excerpt-one']/header/h2/a"],
        # 导航信息
        "channel_info_xpath": ["//header[@class='header']/ul[@class='nav']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/[?]p=.*",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class='article-title']//text()", },
            ],
            "content": [
                {"xpath": "//article[@class='article-content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//ul[@class='article-meta']/li[3]/text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//ul[@class='article-meta']/li[1]/text()",
                    "regex": r"\s*?发布于\s*?(.*)$",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 桐城网
    {
        "platformName": "桐城网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.itongcheng.cc/",
        # 首页头条新闻
        "headline_news": ["//div[@class='top1']/div[@class='top_tit']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='index_foucs']/div[@class='index_foucs_show']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='m']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='yb_twonav']/div[@class='yb_twonm2']/span/p/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d{4,}_\d{2,}/\d{2,}_\d+.html",
            r"https?://[\w\-\.]+/\w+/\d{4,}_\d{4,}_\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class='show_title']/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='news_con']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='content_line']/span[2]/text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='content_line']/span[1]/text()",
                    # "regex": r"\s*?发布于\s*?(.*)$",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 安庆新闻网
    {
        "platformName": "安庆新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.aqnews.com.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='row2']//a"],
        # 轮播信息
        "banner_news": ["//div[@id='head_swiper']//a[@class='swiper-slide-link']"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='head-news-list']/li[@class='list-item']/h3[@class='list-item-title']/a"],
        # 导航信息
        "channel_info_xpath": ["//nav[@class='navbar font-22']//li[@class='nav-item']/a[@class='nav-item-link']"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d{4,}/\d{2,}/\d{2,}/\w+.html$",
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/c_\d+.htm$",  # 新华社
            r"https?://[\w\-\.]+/\w+/\w+/\d{4,}-\d{2,}/\d{2}/c_\d+.htm$",  # 新华社
            r"https?://[\w\-\.]+/\d{4,}/\d{2,}/\d{2}/\w+.shtml$",  # 央视网新闻
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='article']/h2[contains(@class,'article-title')]/text()", },
                {"xpath": "//div[@class='conTit']/h2[@class='title']/text()", },  # 新华社
                {"xpath": "//div[@class='h-title']/text()", },  # 新华社
                {"xpath": "//div[@class='cnt_bd']/h1/text()"},  # 央视网新闻
                {"xpath": "//div[@id='title_area']/h1/text()"},  # 央视网新闻

            ],
            "content": [
                {"xpath": "//div[@class='article']/div[contains(@class,'article-main')]", },
                {"xpath": "//div[@class='xlcontent']", },  # 新华社
                {"xpath": "//div[@id='p-detail']/div[@class='main-aticle']", },  # 新华社
                {"xpath": "//div[@class='cnt_bd']/p"},  # 央视网新闻
                {"xpath": "//div[@id='text_area']"},  # 央视网新闻
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='article-resource'][2]/text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {  # 新华社
                    "xpath": "//div[@class='h-info']/span[@class='sub-src']/span[@class='aticle-src']/text()",
                    # "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {  # 新华社
                    "xpath": "//div[@class='info']/text()[2]",
                    # "regex": r".*?来源[: ：]\s*?(.*)$",
                },
                {  # 央视网新闻
                    "xpath": "//span[@class='info']/i/text()",
                    "regex": r"来源[: ：]\s*?(.*)20.*",
                },
                {  # 央视网新闻
                    "xpath": "//div[@id='title_area']/div[@class='info']/text()",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class='article-publish-date']/text()",
                    "regex": r".*?发布时间[: ：]\s*?(.*)$",
                    # "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})",
                },
                {  # 新华社
                    "xpath": "//div[@class='h-info']/span[@class='sub-time']/span[@class='h-time']//text()",
                    # "regex": r"发布日期[: ：]\s*?(.*)来源.*",
                },
                {  # 新华社
                    "xpath": "//div[@class='info']/text()[1]",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                },
                {  # 央视网新闻
                    "xpath": "//span[@class='info']/i/text()",
                    "regex": r"(\d{4}年\d{1,2}月\d{1,2}日\s\d{1,2}:\d{1,2})",

                },
                {  # 央视网新闻
                    "xpath": "//div[@id='title_area']/div[@class='info']/span/text()",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 安庆市政府网
    {
        "platformName": "安庆市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.anqing.gov.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='toutiao xw_toptitle']//a"],
        # 轮播信息
        # 轮播信息
        "banner_news": ["//div[@id='myFocus01']/div[@class='txt']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='ywnews_wz']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='navbar']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+.html$",
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\w+/\d+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class='newstitle']/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='J_content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='newsinfo']/text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='newsinfo']/text()",
                    "regex": r"发布日期[: ：]\s*?(.*)来源.*",
                },

            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 安庆长安网
    {
        "platformName": "安庆长安网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.aqzfw.gov.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@id='index_toutiao']//a"],
        # 轮播信息
        "banner_news": ["//div[@id='row1']/div[@class='box']/div[@class='box-1']//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='TabContent']//div[@class='index_news']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='nav']/div[@class='m']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/html/default/news+/\d+/\d+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='content_main']/h1/text()", },
                {"xpath": "//div[@class='title']/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='zoom']", },
                {"xpath": "//div[@class='content_main']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='show-info']/ul/li[2]/text()",
                    # "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='source']/span[2]/text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='show-info']/ul/li[3]/text()",
                },
                {
                    "xpath": "//div[@class='source']/span[1]/text()",
                    "regex": r"\s*?时间[: ：]\s*?(.*)$",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 黄山市政府网
    {
        "platformName": "黄山市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.huangshan.gov.cn/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        # 轮播信息
        "banner_news": ["//div[@id='myFocus01']/div[@class='txt']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='xwcon']/div/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='navbar']/ul[@class='nav navbar-nav']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='wenzhang']/h1[@class='wztit']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='wzcon j-fontContent clearfix']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='res']/text()",
                    "regex": r"\s*?信息来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class='fbsj']/text()",
                    "regex": r"\s*?发布时间[: ：]\s*?(.*)$",
                },

            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 黄山长安网
    {
        "platformName": "黄山长安网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.hscaw.com/",
        # 首页头条新闻
        "headline_news": ["//div[@class='headline']/h1[@class='tc']/a"],
        # 轮播信息
        "banner_news": ["//div[@id='D1pic1']/div[@class='fcon']/strong/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='toutiao left'][1]/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='daoh']/div[@class='nav1']/span/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d{4,}-\d{2,}-\d{2,}/\d+.html",
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\d{4,}-\d{2,}-\d{2,}/\d+.html",
            r"https?://[\w\-\.]+/\w+/\w+/\w+/content_\d+.shtml",
            r"https?://[\w\-\.]+/chinapeace/c\d+/\d{4,}-\d{2,}/\d{2,}/content_\d+.shtml",  # 中国长安网
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='GcDetail']/div[@id='ScDetailTitle']/text()", },
                {"xpath": "//div[@class='content']/h3/text()", },
                {"xpath": "//div[@class='title']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='content_info']", },
                {"xpath": "//div[@class='content']/div[@class='player']", },
                {"xpath": "//div[@class='content']//div[@id='TIDE_PLAYER_0']", },
                {"xpath": "//div[@class='content_main']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='desc'][2]/text()",
                    "regex": r"来源[: ：]\s*?(.*)作者.*",
                },
                {
                    "xpath": "//span[@class='time'][2]/text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='source']/span[2]/text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='desc'][2]/text()",
                    "regex": r"时间[: ：]\s*?(.*)来源.*",

                },
                {
                    "xpath": "//span[@class='time'][1]/text()",
                    # "regex": r"\s*?时间[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='source']/span[1]/text()",
                    "regex": r"\s*?时间[: ：]\s*?(.*)$",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 2021年1月22日-12个
    # 黄山在线
    {
        "platformName": "黄山在线",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.huangshannews.cn/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='contmain_l fL']//a[@class='t1']"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='contmain_r']/div/div[@class='hd clearfix ']/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='navlist']/div[@class='navlist-right']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\w+/content_\d+.shtml",
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\w+/content_\d+.shtml",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='content-wrap']/h3/text()", },

            ],
            "content": [
                {"xpath": "//div[@class='text-center content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='source'][2]/text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class='time']/text()",
                    # "regex": r"发布日期[: ：]\s*?(.*)来源.*",
                    # "regex": r"(\d{4}年\d{1,2}月\d{1,2}日\s\d{1,2}:\d{1,2})",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 黄山新闻网
    {
        "platformName": "黄山新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.hsnewsnet.com/",
        # 首页头条新闻
        "headline_news": ["//section[@class='con-title']//a[not(contains(@class,'title-advert'))]"],
        # 轮播信息
        "banner_news": ["//div[@id='news-slide']/ul[@id='slide-list']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='main-right']/div[@class='news-list']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='navs']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\w+/content_\d+.shtml",
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\w+/pc_content_\d+.shtml",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='content']/h3/text()", },

            ],
            "content": [
                {"xpath": "//div[@class='content_center']", },
                {"xpath": "//div[@class='player']/div | //div[@class='content_center']", },
                # {"xpath": "//div[@class='player' or @class='content_center']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='time'][2]/text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class='time'][1]/text()",
                    # "regex": r"发布日期[: ：]\s*?(.*)来源.*",
                    # "regex": r"(\d{4}年\d{1,2}月\d{1,2}日\s\d{1,2}:\d{1,2})",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 阜阳新闻网
    {
        "platformName": "阜阳新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.fynews.net/",
        # 首页头条新闻
        "headline_news": ["//div[@class='box_top_z']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='box_slide']//div[@class='title slideother']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='box_tnews']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='nv']/div[@class='wp ftzt']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/article+-\d+-\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='h hm']/h1[@class='ph']/text()", },

            ],
            "content": [
                {"xpath": "//td[@id='article_content']", },
            ],
            "pubSource": [
                # {
                #     "xpath": "//span[@class='time'][2]/text()",
                #     "regex": r"\s*?来源[: ：]\s*?(.*)$",
                # },
            ],
            "pubTime": [
                {
                    "xpath": "//p[@class='xg1 xs2']/text()[1]",
                    # "regex": r"发布日期[: ：]\s*?(.*)来源.*",
                    # "regex": r"(\d{4}年\d{1,2}月\d{1,2}日\s\d{1,2}:\d{1,2})",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 阜阳市政府网
    {
        "platformName": "阜阳市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.fy.gov.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='m-hot']//a"],
        # 轮播信息
        "banner_news": [
            "//div[@class='m-list1'][1]/div[@class='m-flash']/div[@class='bd']/div[@class='tempWrap']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='m-fyyw']/div[@class='bd m-list']//ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='new-nav']/div[@class='new-container']//a[@class='dropdown-toggle']"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/content/detail+/\w+.html",
            r"https?://[\w\-\.]+/openness/detail/content+/\w+.html$",
            r"https?://[\w\-\.]+/\w+/\w+/\d+.html$",  # 安徽政府网
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/content_\d+.htm$",  # 中国政府网
            # r"https?://[\w\-\.]+/static/tpl/datailpage/dzpage.html[?]itemId=.*$",  # 全国党媒平台-ifrme
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='m-body']/h1/text()", },
                {"xpath": "//div[@class='m-zw j-fontContent row']/h1/text()", },
                {
                    "xpath": "//div[@class='wenzhang']/h2[@class='wzsbt']|//div[@class='wenzhang']/h1[@class='wztit']|//div[@class='wenzhang']/h2[@class='wzfbt']", },
                {"xpath": "//div[@class='detail-article-title oflow-hd']//text()", },
                {"xpath": "//div[@class='article oneColumn pub_border']/h1/text()", },  # 中国政府网
            ],
            "content": [
                {"xpath": "//div[@id='zoom']", },
                {"xpath": "//div[@class='wenzhang']/div[@class='wzcon j-fontContent']", },
                {"xpath": "//div[@class='pages_content']", },  # 中国政府网
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='u-funs']/span[3]/text()",
                    "regex": r".*?信息来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='m-syh']//tr[4]/td[4]/text()",
                },
                {
                    "xpath": "//div[@class='wenzhang']/div[@class='wzfbxx']/span[@class='fbxx']/text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {  # 中国政府网
                    "xpath": "//div[@class='pages-date']/span[@class='font']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='u-funs']/span[4]/text()",
                    "regex": r".*?发布时间[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='m-syh']//tr[3]/td[4]/text()",
                },
                {
                    "xpath": "//div[@class='wenzhang']/div[@class='wzfbxx']/span[@class='fbxx']/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",
                },
                {  # 中国政府网
                    "xpath": "//div[@class='pages-date']/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                }
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 宿州新闻网
    {
        "platformName": "宿州新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.ahsz.tv/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='fl slide']/div[@class='TB-focus']/div[@class='bd']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='fl r_news1 ml25']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav-bar']/map/ul[@class='nav-site']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/p/\d+.html$",
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/c_\d+.htm$",  # 新华社
            r"https?://[\w\-\.]+/\w+/\w+/\d{4,}-\d{2,}/\d{2}/c_\d+.htm$",  # 新华社
            r"https?://[\w\-\.]+/vh+\d+/share/\d+[?]channel=.*",  # 新华社
            r"https?://[\w\-\.]+/\d{4,}/\d{2,}/\d{2}/\w+.shtml$",  # 央视网新闻
            r"https?://[\w\-\.]+/article+/\d+/.*",  # 人民日报
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='Article']/h1/text()", },
                {"xpath": "//div[@class='conTit']/h2[@class='title']/text()", },  # 新华社
                {"xpath": "//div[@class='h-title']/text()", },  # 新华社
                {"xpath": "//div[@class='head-line clearfix']/h1/span[@class='title']/text()", },  # 新华社
                {"xpath": "//header[@class='news-basic']/h1/text()", },  # 新华社
                {"xpath": "//div[@class='cnt_bd']/h1/text()"},  # 央视网新闻
                {"xpath": "//div[@id='title_area']/h1/text()"},  # 央视网新闻
                {"xpath": "//div[@class='header']/h1[@class='title']|//div[@class='header']/h2[@class='sub-title']"},
                # 人民日报

            ],
            "content": [
                {"xpath": "//div[@id='Article']/div[@class='content']/p", },
                {"xpath": "//div[@class='xlcontent']", },  # 新华社
                {"xpath": "//div[@id='p-detail']/div[@class='main-aticle']", },  # 新华社
                {"xpath": "//div[@id='detail']", },  # 新华社
                {"xpath": "//section[@class='main-text-container']", },  # 新华社
                {"xpath": "//div[@class='cnt_bd']/p"},  # 央视网新闻
                {"xpath": "//div[@id='text_area']"},  # 央视网新闻
                {"xpath": "//div[@class='article article-detail']"},  # 人民日报
            ],
            "pubSource": [
                {
                    "xpath": "//div[@id='Article']/h1/span/text()[1]",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {  # 新华社
                    "xpath": "//div[@class='h-info']/span[@class='sub-src']/span[@class='aticle-src']/text()",
                    # "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {  # 新华社
                    "xpath": "//div[@class='info']/text()[2]",
                    # "regex": r".*?来源[: ：]\s*?(.*)$",
                },
                {  # 新华社
                    "xpath": "//div[@class='source']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
                {  # 新华社
                    "xpath": "//p[@class='hender-info-source-v7']/span/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
                {  # 央视网新闻
                    "xpath": "//span[@class='info']/i/text()",
                    "regex": r"来源[: ：]\s*?(.*)20.*",
                },
                {  # 央视网新闻
                    "xpath": "//div[@id='title_area']/div[@class='info']/text()",
                },
                {  # 人民日报
                    "xpath": "//span[@class='pr10 head-info-copyfrom']/text()",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@id='Article']/h1/span/text()[1]",
                    # "regex": r".*?发布时间[: ：]\s*?(.*)$",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",
                },
                {  # 新华社
                    "xpath": "//div[@class='h-info']/span[@class='sub-time']/span[@class='h-time']//text()",
                    # "regex": r"发布日期[: ：]\s*?(.*)来源.*",
                },
                {  # 新华社
                    "xpath": "//div[@class='info']/text()[1]",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                },
                {  # 新华社
                    "xpath": "//div[@class='header-time left']//text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                },
                {  # 新华社
                    "xpath": "//span[@class='hender-info-over']/span[1]/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                },
                {  # 央视网新闻
                    "xpath": "//span[@class='info']/i/text()",
                    "regex": r"(\d{4}年\d{1,2}月\d{1,2}日\s\d{1,2}:\d{1,2})",

                },
                {  # 央视网新闻
                    "xpath": "//div[@id='title_area']/div[@class='info']/span/text()",
                },
                {  # 人民日报
                    "xpath": "//span[@class='pr10'][2]/text()",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 拂晓新闻网
    {
        "platformName": "拂晓新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.zgfxnews.com/",
        # 首页头条新闻
        "headline_news": ["//div[@class='topline']//a"],
        # 轮播信息
        "banner_news": ["//div[@id='focusimg']/div/h3/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='newslist']//ul/li//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='menu']/div[@class='mainnav']/div[@class='navInner']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/content+/\d{4,}-\d{2,}/\d{2}/content_\d+.htm$",
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/c_\d+.htm$",  # 新华社
            r"https?://[\w\-\.]+/\w+/\w+/\d{4,}-\d{2,}/\d{2}/c_\d+.htm$",  # 新华社
            # r"https?://[\w\-\.]+/vh+\d+/share/\d+[?]channel=.*",  # 新华社
            r"https?://[\w\-\.]+/\d{4,}/\d{2,}/\d{2}/\w+.shtml$",  # 央视网新闻
            r"https?://[\w\-\.]+/article+/\d+/.*",  # 人民日报
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='Articletit_m']/h1/text()", },
                {"xpath": "//div[@class='conTit']/h2[@class='title']/text()", },  # 新华社
                {"xpath": "//div[@class='h-title']/text()", },  # 新华社
                {"xpath": "//div[@class='head-line clearfix']/h1/span[@class='title']/text()", },  # 新华社
                {"xpath": "//header[@class='news-basic']/h1/text()", },  # 新华社
                {"xpath": "//div[@class='cnt_bd']/h1/text()"},  # 央视网新闻
                {"xpath": "//div[@id='title_area']/h1/text()"},  # 央视网新闻
                {"xpath": "//div[@class='header']/h1[@class='title']|//div[@class='header']/h2[@class='sub-title']"},
                # 人民日报

            ],
            "content": [
                {"xpath": "//div[@class='Articletit']", },
                {"xpath": "//div[@class='xlcontent']", },  # 新华社
                {"xpath": "//div[@id='p-detail']/div[@class='main-aticle']", },  # 新华社
                {"xpath": "//div[@id='detail']", },  # 新华社
                {"xpath": "//section[@class='main-text-container']", },  # 新华社
                {"xpath": "//div[@class='cnt_bd']/p"},  # 央视网新闻
                {"xpath": "//div[@id='text_area']"},  # 央视网新闻
                {"xpath": "//div[@class='article article-detail']"},  # 人民日报
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='source']/text()",
                    # "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {  # 新华社
                    "xpath": "//div[@class='h-info']/span[@class='sub-src']/span[@class='aticle-src']/text()",
                    # "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {  # 新华社
                    "xpath": "//div[@class='info']/text()[2]",
                    # "regex": r".*?来源[: ：]\s*?(.*)$",
                },
                {  # 新华社
                    "xpath": "//div[@class='source']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
                {  # 新华社
                    "xpath": "//p[@class='hender-info-source-v7']/span/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
                {  # 央视网新闻
                    "xpath": "//span[@class='info']/i/text()",
                    "regex": r"来源[: ：]\s*?(.*)20.*",
                },
                {  # 央视网新闻
                    "xpath": "//div[@id='title_area']/div[@class='info']/text()",
                },
                {  # 人民日报
                    "xpath": "//span[@class='pr10 head-info-copyfrom']/text()",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class='info']/text()[2]",
                    # "regex": r".*?发布时间[: ：]\s*?(.*)$",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",
                },
                {  # 新华社
                    "xpath": "//div[@class='h-info']/span[@class='sub-time']/span[@class='h-time']//text()",
                    # "regex": r"发布日期[: ：]\s*?(.*)来源.*",
                },
                {  # 新华社
                    "xpath": "//div[@class='info']/text()[1]",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                },
                {  # 新华社
                    "xpath": "//div[@class='header-time left']//text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                },
                {  # 新华社
                    "xpath": "//span[@class='hender-info-over']/span[1]/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                },
                {  # 央视网新闻
                    "xpath": "//span[@class='info']/i/text()",
                    "regex": r"(\d{4}年\d{1,2}月\d{1,2}日\s\d{1,2}:\d{1,2})",

                },
                {  # 央视网新闻
                    "xpath": "//div[@id='title_area']/div[@class='info']/span/text()",
                },
                {  # 人民日报
                    "xpath": "//span[@class='pr10'][2]/text()",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 宿州长安网
    {
        "platformName": "宿州长安网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.szcaw.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='toutiao']/div[@class='title']/a"],
        # 轮播信息
        "banner_news": ["//div[@id='focus']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='zfhy_wz']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='navbar']/ul[@class='nav navbar-nav navbar-index']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/html+/\d+/\d+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='con_main']/h1[@class='newstitle']/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='zoom']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='newsinfo']/div[@class='fl newsinfoleft']/span[1]/text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='newsinfo']/div[@class='fl newsinfoleft']/span[2]/text()",
                    "regex": r"\s*?发表时间[: ：]\s*?(.*)$",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 宿州市政府网
    {
        "platformName": "宿州市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.ahsz.gov.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='toutiao']/div[@class='title']/a"],
        # 轮播信息
        "banner_news": ["//div[@id='myFocus01']/div[@class='txt']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='xw_wz']/ul/li/a[@class='left']|//div[@class='zyzz_con']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='navbar']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+.html$",
            r"https?://[\w\-\.]+/\w+/\w+/\d+.html$",  # 安徽政府网
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/content_\d+.htm$",  # 中国政府网
            # r"https?://[\w\-\.]+/static/tpl/datailpage/dzpage.html[?]itemId=.*$",  # 全国党媒平台-ifrme
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='con_main']/h1[@class='newstitle']/text()", },
                {"xpath": "//h1[@class='newstitle']/text()", },
                {
                    "xpath": "//div[@class='wenzhang']/h2[@class='wzsbt']|//div[@class='wenzhang']/h1[@class='wztit']|//div[@class='wenzhang']/h2[@class='wzfbt']", },
                {"xpath": "//div[@class='detail-article-title oflow-hd']//text()", },
                {"xpath": "//div[@class='article oneColumn pub_border']/h1/text()", },  # 中国政府网
            ],
            "content": [
                {"xpath": "//div[@class='j-fontContent newscontnet minh500 clearfix']", },
                {"xpath": "//div[@class='j-fontContent clearfix']", },
                {"xpath": "//div[@class='wenzhang']/div[@class='wzcon j-fontContent']", },
                {"xpath": "//div[@class='pages_content']", },  # 中国政府网
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='fl newsinfoleft']/span[1]/text()",
                    "regex": r".*?文章来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='div_table_suoyin']//tr[2]/td[@class='pmingcheng'][2]/text()",
                },
                {
                    "xpath": "//div[@class='wenzhang']/div[@class='wzfbxx']/span[@class='fbxx']/text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {  # 中国政府网
                    "xpath": "//div[@class='pages-date']/span[@class='font']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='fl newsinfoleft']/span[3]/text()",
                    "regex": r".*?发表时间[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class='div_table_suoyin']//tr[3]/td[@class='pmingcheng'][2]/text()",
                },
                {
                    "xpath": "//div[@class='wenzhang']/div[@class='wzfbxx']/span[@class='fbxx']/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",
                },
                {  # 中国政府网
                    "xpath": "//div[@class='pages-date']/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                }
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 滁州市政府网
    {
        "platformName": "滁州市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.chuzhou.gov.cn/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='mF_tbhuabao_wrap']/div[@id='syflash']/div[@class='txt']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='fr nr_rbox clearfix']//div[@class='list1']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='qqmylist fl']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+.html$",
            r"https?://[\w\-\.]+/\w+/\w+/\d+.html$",  # 安徽政府网
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/content_\d+.htm$",  # 中国政府网
            # r"https?://[\w\-\.]+/static/tpl/datailpage/dzpage.html[?]itemId=.*$",  # 全国党媒平台-ifrme
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class='newstitle']/text()", },
                {
                    "xpath": "//div[@class='wenzhang']/h2[@class='wzsbt']|//div[@class='wenzhang']/h1[@class='wztit']|//div[@class='wenzhang']/h2[@class='wzfbt']", },
                {"xpath": "//div[@class='detail-article-title oflow-hd']//text()", },
                {"xpath": "//div[@class='article oneColumn pub_border']/h1/text()", },  # 中国政府网
            ],
            "content": [
                {"xpath": "//div[@class='newscontnet j-fontContent']", },
                {"xpath": "//div[@class='gkwz_contnet j-fontContent xxgk_contnetleft']", },
                {"xpath": "//div[@class='clearfix xxgkcontent minh500']", },
                {"xpath": "//div[@class='wenzhang']/div[@class='wzcon j-fontContent']", },
                {"xpath": "//div[@class='pages_content']", },  # 中国政府网
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='newsinfo']/span[4]/text()",
                },
                {
                    "xpath": "//div[@class='wenzhang']/div[@class='wzfbxx']/span[@class='fbxx']/text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                },
                {  # 中国政府网
                    "xpath": "//div[@class='pages-date']/span[@class='font']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='newsinfo']/span[3]/text()",
                },
                {
                    "xpath": "//div[@class='wenzhang']/div[@class='wzfbxx']/span[@class='fbxx']/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",
                },
                {  # 中国政府网
                    "xpath": "//div[@class='pages-date']/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                }
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 上海市人社局
    {
        "platformName": "上海市人社局",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://rsj.sh.gov.cn/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": [
            "//div[@class='normal-slider pic-slider owl-carousel Slider-one owl-theme owl-loaded']//div[@class='owl-item cloned']/div[@class='item']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='tab-content']/div[@id='tab2-1' or @id='tab2-2']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@id='tablist']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+_\d+/\d{8,}/t\d+_\d+.html$",
            r"https?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2}/content_\d+.htm$",  # 中国政府网
            # r"https?://[\w\-\.]+/static/tpl/datailpage/dzpage.html[?]itemId=.*$",  # 全国党媒平台-ifrme
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h2[@id='ivs_title']/text()", },
                {"xpath": "//div[@class='article oneColumn pub_border']/h1/text()", },  # 中国政府网
            ],
            "content": [
                {"xpath": "//div[@class='TRS_Editor']", },
                {"xpath": "//div[@class='pages_content']", },  # 中国政府网
            ],
            "pubSource": [
                {  # 中国政府网
                    "xpath": "//div[@class='pages-date']/span[@class='font']/text()",
                    "regex": r".*?来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//small[@id='ivs_date']/span[@class='inline-block']/text()",
                    "regex": r".*?发布时间[: ：]\s*?(.*)$",
                },
                {  # 中国政府网
                    "xpath": "//div[@class='pages-date']/text()",
                    # "regex": r".*?时间[: ：]\s*?(.*)$",
                }
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 上海发改委
    {
        "platformName": "上海发改委",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://fgw.sh.gov.cn/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='hp-news-item clearFix blur']//ul[@class='slides']/li/p/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='tab-content']/div/ul[@class='pageList']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@id='mainNav']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d{6,}/\w+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='ivs_title']//text()", },
            ],
            "content": [
                {"xpath": "//div[@id='ivs_content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='xwzx_time'][1]/text()",
                    "regex": r"\s*?信息来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='xwzx_time'][1]/text()",
                    "regex": r"发布时间[: ：]\s*?(.*)信息来源.*",
                },
                {
                    "xpath": "//div[@class='xwzx_time1']/ul/li[2]/text()",
                    "regex": r"\s*?发布日期[: ：]\s*?(.*)$",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 上海基层党建
    {
        "platformName": "上海基层党建",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.shjcdj.cn/djWeb/djweb/web/djweb/index/index.action",
        # 首页头条新闻
        "headline_news": ["//div[@class='topnews cl']/a|//div[@class='toptitle']/a"],
        # 轮播信息
        "banner_news": ["//div[@class='focus']//div[@class='tempWrap']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='ywcon']/ul[@class='ywlist']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='nav']/ul[@class='menu']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/djWeb/djweb/web/djweb/index/index!info.action[?]articleid=.*",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='artbox']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='artcon']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='artinfo']/text()",
                    "regex": r"来源[: ：]\s*?(.*)发布时间.*",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='artinfo']/text()",
                    "regex": r"\s*?发布时间[: ：]\s*?(.*)$",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 2021年1月23日-12个
    # 上海海事局
    {
        "platformName": "上海海事局",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.sh.msa.gov.cn/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@id='lunbo']/div[@class='carousel-inner']/div/div[@class='carousel-caption']/h3/a"],
        # 轮播旁边新闻
        "banner_news_side": [
            "//div[@class='pull-right yaowen']/ul[@class='list-unstyled tab-content']/li/a[@class='ellipsis']"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='sidebar']/ul[@class='list-unstyled']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+.jhtml$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//p[@class='contentTitle']/text()", },
                {"xpath": "//div[@class='commonTitle']/span[@class='titleText']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='interviewTextWrap']", },
                {"xpath": "//div[@class='tableWrap']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='subTitle']/span[2]/text()",
                    # "regex": r"来源[: ：]\s*?(.*)发布时间.*",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='subTitle']/span[6]/text()",
                    # "regex": r"\s*?发布时间[: ：]\s*?(.*)$",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 上海市高级人民法院
    {
        "platformName": "上海市高级人民法院",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.hshfy.sh.cn/shfy/web/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": [
            "//div[@class='news']/div[@class='txt']/ul/li[@class='txt_content']/div[@class='inside-content']/a"],
        # 轮播旁边新闻
        "banner_news_side": [
            "//div[@class='dt_con']/div/ul[@class='dt_nr_item']/li[@class='dt_li']/a[@class='dt_li_a']"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']/li[@class='nav_a nav_a_xt']/a"],
        # 详情链接。
        "doc_links": [
            # r"https?://[\w\-\.]+/\w+.jsp[?]pa=.*",
            r"https?://[\w\-\.]+/shfy/web+/\w+.jsp[?]pa=.*&zd=.*$",
            # r"https?://[\w\-\.]+/shfy/web+/\w+.jsp+.*",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='wby']/text()", },
                {"xpath": "//div[@class='new_text']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='nrtxt']", },
            ],
            "pubSource": [],
            "pubTime": [
                {
                    "xpath": "//div[@class='wby']/font/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2})",
                },
                {
                    "xpath": "//div[@class='text_bq']/text()",
                    "regex": r"(\d{4}-\d{1,2}-\d{1,2})",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 上海市公安局
    {
        "platformName": "上海市公安局",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://gaj.sh.gov.cn/shga",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='cons-lefting']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": [],
        # 导航信息
        "channel_info_xpath": ["//div[@class='one-navs']/ul[@id='mainNav']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/detail[?]pa=.*",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='main']/h2/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='content']", },
            ],
            "pubSource": [],
            "pubTime": [
                {
                    "xpath": "//p[@id='ftitle_id']/text()",
                    "regex": r"\s*?时间[: ：]\s*?(.*)$",
                    # "regex": r"发布时间[: ：]\s*?(.*)信息来源.*",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 上海市国税局
    {
        "platformName": "上海市国税局",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://shanghai.chinatax.gov.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='notice']/a"],
        # 轮播信息
        "banner_news": ["//div[@class='swiper-banner swiper-container js_banner']/div[@class='swiper-wrapper']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='import o_u']/div[@class='content']/ul//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='mainNav']/div[@class='warp']/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d{6,}/t\d+.html$",
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\d{6,}/t\d+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='ivs_title']//text()", },
            ],
            "content": [
                {"xpath": "//div[@class='TRS_Editor']", },
                {"xpath": "//div[@id='ivs_content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@class='source']/text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                    # "regex": r"发布时间[: ：]\s*?(.*)信息来源.*",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//span[@class='time js_time']//text()",
                    "regex": r"\s*?发布时间[: ：]\s*?(.*)$",
                    # "regex": r"发布时间[: ：]\s*?(.*)信息来源.*",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 上海科技
    {
        "platformName": "上海科技",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://stcsm.sh.gov.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@id='leftSidebar']/ul/li/a"],
        # 轮播信息
        "banner_news": ["//div[@class='sy_left']/ul[@class='sytx_wenzi']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@id='zxgk_right']/div[@class='sy_zxgkContent']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='content']/h2/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d{6,}/\w+.html$",
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\d{6,}/\w+.html$",
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\w+/\d{6,}/\w+.html$",
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\w+/\w+/\d{6,}/\w+.html$",
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\w+/\w+/\w+/\d{6,}/\w+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='ivs_title']//text()", },
            ],
            "content": [
                {"xpath": "//div[@id='ivs_content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='xxgk_content_time']/span[2]/text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                    # "regex": r"发布时间[: ：]\s*?(.*)信息来源.*",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='xxgk_content_time']/span[1]/text()",
                    "regex": r"\s*?发布日期[: ：]\s*?(.*)$",
                    # "regex": r"发布时间[: ：]\s*?(.*)信息来源.*",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 上海市民宗委
    {
        "platformName": "上海市民宗委",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://mzzj.sh.gov.cn/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='newsPic']/div[@id='newsPic']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='hd_newfont']/div[@id='leftTab01']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='mainNav']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d{6,}/\w+.html$",
            r"https?://[\w\-\.]+/\w+/\d{6,}/\d+-\d+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='ivs_title']//text()", },
            ],
            "content": [
                {"xpath": "//div[@id='ivs_content']", },
            ],
            "pubSource": [],
            "pubTime": [
                {
                    "xpath": "//div[@class='fbrq']/text()",
                    "regex": r"\s*?发布日期[: ：]\s*?(.*)$",
                    # "regex": r"发布时间[: ：]\s*?(.*)信息来源.*",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 上海市国资委
    {
        "platformName": "上海市国资委",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.gzw.sh.gov.cn/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": [
            "//div[@class='owl-stage-outer']/div[@class='owl-stage']/div[@class='owl-item']/div[@class='item']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='tr']/div[@class='news']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d{8,}/\w+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='ivs_title']//text()", },
            ],
            "content": [
                {"xpath": "//div[@id='ivs_content']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='gqzc_cont']/span[2]/b/text()",
                    "regex": r"\s*?信息来源[: ：]\s*?(.*)$",
                    # "regex": r"发布时间[: ：]\s*?(.*)信息来源.*",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='gqzc_cont']/span[1]/b/text()",
                    "regex": r"\s*?发布日期[: ：]\s*?(.*)$",
                    # "regex": r"发布时间[: ：]\s*?(.*)信息来源.*",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 上海市公务员局
    {
        "platformName": "上海市公务员局",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.shacs.gov.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='headlines']/div[@class='headlines-llist']/ul/li/a"],
        # 轮播信息
        "banner_news": ["//div[@id='myCarousel']/div[@class='carousel-inner']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='lineTab']/div[@class='tab-content']/div/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='navbar']/ul[@class='nav navbar-nav']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/CivilServants/CivilServantsDetail+/.*$",
            r"https?://[\w\-\.]+/Government/MechanismDetail+/.*$",
            r"https?://[\w\-\.]+/Home/NewsDetail+/.*$",
            r"https?://[\w\-\.]+/Dynamic/DynamicDetail+/.*$",
            r"https?://[\w\-\.]+/\w+/\d{6,}/t\d{8,}_\d+.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='news_title text-center']/h3/text()", },
                {"xpath": "//div[@class='san_main']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='text-center']/div[@id='news_con']", },
                {"xpath": "//div[@id='news_con']", },
            ],
            "pubSource": [],
            "pubTime": [
                {
                    "xpath": "//div[@class='news_title text-center']/span[@class='date']/text()",
                    # "regex": r"\s*?发布日期[: ：]\s*?(.*)$",
                    # "regex": r"发布时间[: ：]\s*?(.*)信息来源.*",
                },
                {
                    "xpath": "//div[@class='san_main']/h5/a/text()",
                    # "regex": r"\s*?发布日期[: ：]\s*?(.*)$",
                    # "regex": r"发布时间[: ：]\s*?(.*)信息来源.*",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 上海市政府征兵办-这个拿不到其他频道，未找到原因
    {
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
    },
    # 张江国家自主创新示范区
    {
        "platformName": "张江国家自主创新示范区",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://kcb.sh.gov.cn/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='index-c1-l']/div[@class='index-c1-bd']/div[@class='tempWrap']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='index-c1-r']/div[@class='news-c']/div[1]/dl//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='head jz']/div[@class='head-r']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/html/1+/\d+/\d+/\d+.html$",
            r"https?://[\w\-\.]+/html/1+/\d+/\d+/\d+/\d+.html$",
            r"https?://[\w\-\.]+/html/1+/\d+/\d+/\d+/\d+/\d+.html$",

        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='xq-c jz']/h3[@class='xq-t']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='xq-c jz']/div[@class='xq-nr']", },
            ],
            "pubSource": [
                {
                    "xpath": "//dl[@class='xq-c2']/dd/h4[@id='xqSource']/text()",
                    "regex": r"\s*?来源[: ：]\s*?(.*)$",
                    # "regex": r"作者[: ：]\s*?(.*)发布时间.*",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//dl[@class='xq-c2']/dd/span/text()",
                    "regex": r"\s*?发布时间[: ：]\s*?(.*)$",
                    # "regex": r"发布时间[: ：]\s*?(.*)信息来源.*",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 上海共青团
    {
        "platformName": "上海共青团",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.shyouth.net/",
        # 首页头条新闻
        "headline_news": ["//div[@id='Headline']/h1/a"],
        # 轮播信息
        "banner_news": ["//div[@class='fpic']/div[@class='pic']/div[@class='pic_box']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='work_box']/div[@class='work_content'][2]/div/ul//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='header_nav_bar']/div[@class='nav_bar fl']//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/html/1+//\w+/\w+/\d+.html$",
            # r"https?://[\w\-\.]+/html/1+/\d+/\d+/\d+/\d+.html$",
            # r"https?://[\w\-\.]+/html/1+/\d+/\d+/\d+/\d+/\d+.html$",

        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//td[@class='title']//text()", },
            ],
            "content": [
                {"xpath": "//td[@id='content_box']", },
            ],
            "pubSource": [
                {
                    "xpath": "//td[@class='con_nav_bar']/div/text()",
                    # "regex": r"\s*?来源[: ：]\s*?(.*)$",
                    "regex": r"来源[: ：]\s*?(.*)时间.*",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//td[@class='con_nav_bar']/div/text()",
                    "regex": r"时间[: ：]\s*?(.*)点击量.*",
                    # "regex": r"发布时间[: ：]\s*?(.*)信息来源.*",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 上海消防网
    {
        "platformName": "上海消防网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 2,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://sh.119.gov.cn/infoplat/platformData/infoplat/pub/xiaofang_2542/shouye_7602/index.html",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息=flash
        "banner_news": [],
        # 轮播旁边新闻
        "banner_news_side": [
            "//div[@class='navleft']//td[@class='index_sj1']//a|//div[@class='navright']//td[@class='index_sj1']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='menu']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/infoplat/platformData/infoplat/pub/xiaofang_2542/docs+/\d{6,}/d_\d+.html$",
            # r"https?://[\w\-\.]+/html/1+/\d+/\d+/\d+/\d+.html$",
            # r"https?://[\w\-\.]+/html/1+/\d+/\d+/\d+/\d+/\d+.html$",

        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='WordSection1']/p[@class='MsoNormal'][1]/b[1]/span/text()", },
            ],
            "content": [
                {
                    "xpath": "//div[@class='listnei'][1]/div/div|//div[@class='WordSection1']/p[@class='MsoNormal'][position()>2]", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='mainnei']/div[@id='div2']/table//td[1]/text()",
                    # "regex": r"\s*?来源[: ：]\s*?(.*)$",
                    "regex": r"作者[: ：]\s*?(.*)发布时间.*",
                },
            ],
            "pubTime": [
                {
                    "xpath": "//div[@class='mainnei']/div[@id='div2']/table//td[1]/text()",
                    "regex": r"\s*?发布时间[: ：]\s*?(.*)$",
                    # "regex": r"发布时间[: ：]\s*?(.*)信息来源.*",
                },
            ],
            # "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
]
