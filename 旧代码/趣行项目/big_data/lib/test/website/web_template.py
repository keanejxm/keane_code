# -*- coding:utf-8 -*-
"""
# project:
# author: Neil
# date: 2020/12/15
# update: 2020/12/15
"""

a = [
    ##########################################################################3
    # 国家级
    # 光明网(已更新)
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
        # 起始地址。
        "start_url": "http://www.gmw.cn/",
        # cookie
        "cookie": "ga=GA1.2.1814703408.1607671291; __auc=a90c036517650ad1f302bcb0b08; wdcid=1edb014370588150; "
                  "wdlast=1608174859; _gid=GA1.2.626919831.1608706526; _gat=1; __asc=05dde9871768e986bc5915755f9",
        # 首页头条新闻
        "headline_news": ["//div[@class='m_imgTitleWrap']/a | //div[@class='m_zy']/span/a"],
        # 轮播信息
        "banner_news": ["//div[@class='bd']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='m_title']/strong/a | //ul[@class='m_ulList']/li/a"],
        # 频道信息
        "channel_info_xpath": ["//div[@class='g_navs u_bgColor']/div/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+?\.gmw.cn/\d{4,}-\d{2}/\d{2}/content_\d+\.htm$",
            r"https?://[\w\-\.]+?\.gmw.cn/\w+/\d{4,}-\d{2}/\d{2}/content_\d+\.htm$"
        ],
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
        },
    },
    # 澎湃新闻(省级)(已更新)
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
        # 起始地址
        "start_url": "https://www.thepaper.cn/",
        # cookie
        "cookie": "UM_distinctid=1765085e65d39c-013f7c22972075-c791039-240000-1765085e65e4be; "
                  "Hm_lvt_94a1e06bbce219d29285cee2e37d1d26=1607668721,1608019316,1608175554,1608716891; "
                  "p_h5_u=EFC5791A-75C0-46C2-89F8-E6C2C6AC80E1; CNZZDATA1261102524=1002803912-1607664163-%7C1608714620",
        # 首页头条新闻
        "headline_news": ["//div[@class='headline_txt']/a"],
        # 轮播信息
        "banner_news": ["//div[@class='swiper-wrapper']/div/div[1]/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='newsbox']//div[@class='news_tu']/a"],
        # 频道信息
        "channel_info_xpath": ["//div[@class='head_banner']/div/a | //ul[@class='clearfix']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://www\.thepaper\.cn/newsDetail_forward_\d+$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [{"xpath": "//h1[@class='news_title']/text()", },
                      {"xpath": "//div[@class='cnt_bd']/h1/text()", }],

            "content": [{"xpath": "//div[@class='news_txt']", }, ],
            "pubSource": [
                {
                    "describe": "https://www.thepaper.cn/newsDetail_forward_5504339",
                    "xpath": "//div[@class='news_about']/p/span/text()",
                    "regex": r"\s*?来源:(\w+)$",
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
    },
    # 环球网(已更新)
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
        # 起始地址。
        "start_url": "https://www.huanqiu.com/",
        "cookie": "REPORT_UID_=I14TVVXCkP2Y6GwvUkapAqbWbkgFa6iW; Hm_lvt_1fc983b4c305d209e7e05d96e713939f=1610187751;"
                  " Hm_lpvt_1fc983b4c305d209e7e05d96e713939f=1610187751; "
                  "UM_distinctid=176e6ab402ac2-0db0c07f6add6f-4353760-144000-176e6ab402ba78; "
                  "CNZZDATA1000010102=2036155356-1610185827-%7C1610185827; _ma_tk=476k9yo28fcgylqnv9getjvpknutz7ku; "
                  "_ma_is_new_u=1; _ma_starttm=1610187751591",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//ul[@id='imgCon']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@data-ati-block-key='blockW6ZOA40e8k1bviuj']/dl//a"],
        # 频道信息
        "channel_info_xpath": ["//div[@class='rTxt']/a"],
        # 详情链接。
        "doc_links": [r"https?://[\w\-\.]+?\.huanqiu\.com/article/\w+$", ],
        # 目标采集字段
        "fields": {
            "title": [{"xpath": "//div[@class='t-container-title']/h3/text()", }, ],
            "content": [{"xpath": "//article//p", }, ],
            "pubSource": [
                {
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
    },
    # 新华网(已更新)
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
        # 起始地址。
        "start_url": "http://www.xinhuanet.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="headline"]/h1/a'],
        # 轮播信息
        "banner_news": ['//*[@id="focusMediaScroll1"]/div[4]/div[1]/div/div[1]/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="mCSB_1"]/div[1]/ul/li/span/a'],
        # 频道信息
        "channel_info_xpath": ['//div[@class="top-nav"]/div//a'],
        # 详情链接。
        "doc_links": [r"https?://[\w\-\.]+?/\w+/\d{4,}-\d{2}/\d{2}/c_\d+\.htm$", ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//div[@class="head-line clearfix"]//span[@class="title"]/text()', },
                {"xpath": '//div[@class="h-title"]/text()', },
                {"xpath": '//div[@class="b-title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="detail"]', },
                {"xpath": '//div[@class="main"]', },
                {"xpath": '/html/body/div[7]/div[3]', },
            ],
            "pubSource": [
                {
                    # "describe": "http://www.xinhuanet.com/renshi/2020-01/07/c_1125432025.htm",
                    "xpath": "/html/body/div[5]/div[2]/div[2]/text()",
                    "regex": r"源[:：](.*)",
                },
                {
                    "xpath": '//*[@id="source"]/text()',
                },
                {
                    "xpath": '/html/body/div[7]/div[2]/text()',
                    "regex": r"源[:：](.*)\|",
                }
            ],
            "pubTime": [
                {"xpath": "string(/html/body/div[5]/div[2]/div[1])", },
                {"xpath": '//span[@class="h-time"]/text()', },
                {"xpath": '/html/body/div[7]/div[2]/text()',
                 "regex": r"时间[:：](\d+.*\d+)",
                 },
            ],
            "channel": [],
            "authors": [],
            "summary": [],
        },
    },
    # 人民网(已更新)
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
                    "regex": r".*\s*? 来源：\s*?(\w+)$",
                }

            ],
            "pubTime": [
                {"xpath": "//div[@class='box01']/div[@class='fl']/text()", },
                {"xpath": "//div[@class='page_c' and @style]/text()[2]", },
                {
                    "xpath": "//div[@class='data']/text()",
                    "regex": r"发布日期：\s*?(\w+)\s.*",
                }
            ],
            "channel": [
                {"xpath": "//span[@id='rwb_navpath']/a[@class='clink'][2]/text()"},
                {"xpath": "//div[@class='fl']/a[@class='clink'][2]/text()"},
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 5
    # 12/16
    # 中国网(已更新)
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
        # 起始地址。
        "start_url": "http://www.china.com.cn/",
        # cookie
        "cookie": "wdcid=23dc44febc26d351; wdlast=1610173199",
        # 首页头条新闻
        "headline_news": ["//div[@class='topTxt w728 fl']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='rightPic w660 fr']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='leftNews w325 fl']/div/p/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='subNav w1000 wauto hauto']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+\.china\.com\.cn/\d{4,}-\d{2}/\d{2}/content_\d+\.htm$",
            r"https?://[\w\-\.]+\.china\.com\.cn/\w+/detail\d_\d{4,}_\d{2}/\d{2}/\d+\.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class='articleTitle']/text()", },
                {"xpath": "//h1[@class='artTitle']/text()", },
                {"xpath": "//h1[contains(@class, 'artiTitle')]/text()", },
                {"xpath": "//div[@id='menucontainer0_10']/div/dl/dt/text()", },
                {"xpath": "//div[@class='title']/h1/text()", },
                {"xpath": "//div[@class='wrap c top']/h1/text()", },
                {"xpath": "//div[@class='bigpic']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='articleBody']", },
                {"xpath": "//div[@id='artbody']", },
                {"xpath": "//div[@id='artiContent']", },
                {"xpath": "//div[@id='menucontainer0_10']/div/p", },
                {"xpath": "//div[@class='content']", },
                {"xpath": "//div[@id='fontzoom']", },
            ],
            "pubSource": [
                {
                    "xpath": "//span[@id='source_baidu']//text()",
                    "regex": r"\s*?来源[: ：]\s*?(\w+)$",
                },
                {
                    "xpath": "//div[@id='menucontainer0_10']/div/dl/dd/span/text()",
                    "regex": r"\s*?来源[: ：]\s*?(\w+)$",
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
                    "regex": r"\s*?作者[: ：](\w+)$",
                }
            ],
            "summary": [],
        },
    },
    # 海外网
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
        # 起始地址。
        "start_url": "http://www.haiwainet.cn/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@id='focus']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='l']/ul/li//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav publicIndex marginLRAuto']/div/a | "
                               "//div[@class='nav-s1']/a | //div[@class='publicNavBox']/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+\.haiwainet\.cn/n/\d{4,}/\d{4}/c\d+-\d+\.html$",
        ],
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
    },
    # 中新网(已更新)
    {
        "platformName": "中国新闻网",
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
        "start_url": "http://www.chinanews.com/",
        "cookie": "cnsuuid=f05695a4-5fc9-b7f4-2ec7-c9334b0fbc0b2267.102397822924_1610177698910",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='banner_info']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='xwzxdd-dbt']/h1/a | //div[@class='xwzxdd-xbt']/div/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='nav']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+\.chinanews\.com/\w+/\d{4,}/\d{2}-\d{2}/\d+\.shtml$",
            r"https?://[\w\-\.]+\.chinanews\.com/\w+/\d+.shtml$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='content']/h1[1]/text()", },
                {"xpath": "//h1[@id='tit']/text()", },
                {"xpath": "//div[@class='left']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='left_zw']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='left-time']/div[@class='left-t']/a[@class='source']/text()",
                },
                {
                    "xpath": "//div[@class='left-time']/div[@class='left-t']/"
                             "span[contains(text(), '来源：')]/text()",
                    "regex": r"来源[: ：](\w+)$",
                },
                {
                    "xpath": "//div[@class='left-t'][contains(text(), '来源：')]/text()",
                    "regex": r"来源[: ：](\w+)$",
                },
            ],
            "pubTime": [
                {"xpath": "//div[@class='left-time']/div[@class='left-t']/text()[1]", },
                {"xpath": "//div[@class='left-time']/div[@class='left-t']/span[1]/text()", },
            ],
            "authors": [
                {"xpath": "//div[@class='author-info']/"
                          "a[@data-author and contains(@class, 'author-name')]/text()", },
            ],
            "summary": [],
        },
    },
    # 央视网(已更新)
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
        # 起始地址。
        "start_url": "http://www.cctv.com/",
        "cookie": "country_code=CN; Fingerprint=3DE811BAE3D276BD85F876F263565007; "
                  "cna=j2WAGCJrbVICAXvEgSKYg/EQ; sca=353333a5; atpsida=617339745ea2701565327db7_1610186433_42",
        # 首页头条新闻
        "headline_news": ["//div[@class='head_tit']/a | //div[@class='bottom_tit']/a"],
        # 轮播信息
        "banner_news": ["//div[@class='title']//div[@class='txt']/a"],
        # 轮播旁边新闻
        "banner_news_side": [],
        # 导航信息
        "channel_info_xpath": ["//span[@class='nav_tit']/a"],
        # 模板内容。
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+\.cctv\.com/\d{4,}/\d{2}/\d{2}/\w+\.shtml$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@id='title_area']/h1/text()", },
                {"xpath": "//div[@class='cnt_bd']/h1/text()", },
                {"xpath": "//div[@class='cnt_nav']/h3/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='text_area']", },
                {"xpath": "//div[@class='cnt_bd']/p", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='info']/a/text()",
                },
                {
                    "xpath": "//span[@class='info']/i/a[1]/text()",
                },
                {
                    "xpath": "//span[@class='info']/em/a/text()",
                },
                {
                    "xpath": "//span[@class='info']/i//text()",
                    "regex": r"来源[: ：](\w+)|.*",
                },
            ],
            "pubTime": [
                {"xpath": "//span[@class='info']/i/text()", },
                {"xpath": "//div[@class='info']/span/text()", },
                {"xpath": "//div[@class='info']/text()", },
            ],
            "authors": [],
            "summary": [],
        },
    },
    # 参考消息(已更新)
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
        # 起始地址。
        "start_url": "http://www.cankaoxiaoxi.com/",
        # cookie
        "cookie": "Hm_lvt_308b87570281daa02f0d31c085c39163=1608182539,1608636263,1608685792,1608709200; "
                  "acw_tc=1b80d68816087095707938426ef3eba99066c73eec8f0e41f456856236; "
                  "Hm_lpvt_308b87570281daa02f0d31c085c39163=1608709927",
        # 首页头条新闻
        "headline_news": ["//div[@class='f-l w-839']/h2/a | //div[@class='f-l w-839']/p/a"],
        # 轮播信息
        "banner_news": ["//ul[@id='slide_pictures']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='new-slider']/li/a | //div[@class='yaowen YH']/p/a | "
                             "//div[@class='allcontent mar-t-15']/div/p/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='navWrap column']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"http://www.cankaoxiaoxi.com/\w+/\d+/\d+\.shtml$",
            r"https?://[\w\-\.]+\.cankaoxiaoxi\.com/\d{4,}/\d{4}/\d+\.shtml$",
            r"https?://[\w\-\.]+\.cankaoxiaoxi\.com/\w+/\d{4,}/\d{4}/\d+\.shtml$",
        ],
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
    },
    # 10
    # 央广网(已更新)
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
        # 起始地址。
        "start_url": "http://www.cnr.cn/",
        "cookie": "wdcid=01c4f8fac27f5cf7; wdses=2e3473f3f8e155db; wdlast=1610187148; "
                  "cna=j2WAGCJrbVICAXvEgSKYg/EQ; Secure; COLLCK=2878231424",
        # 首页头条新闻
        "headline_news": ["//div[@class='header']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='tabs']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='col_w373']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav_list']/div/span[@class='nav_tit']/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+\.cnr\.cn/[\w/]+/\d{4,}\d{4}/t\d{4,}\d{4}_\d+\.shtml$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='article-header']/h1/text()", },
                {"xpath": "//div[@id='title_area']/h1/text()", },
                {"xpath": "//div[@class='wh610 left']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='article-body']", },
                {"xpath": "//div[@id='content_area']", },
                {"xpath": "//div[@class='TRS_Editor']", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='source']/span[contains(text(), '来源：')]/text()",
                    "regex": r"\s*?来源[: ：]\s*?(\w+)$",
                }
            ],
            "pubTime": [{"xpath": "//div[@class='source']/span[1]/text()", }, ],
            "channel": [{"xpath": "//ol/li/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 华夏时报网
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
        # 起始地址。
        "start_url": "http://www.chinatimes.net.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='hottags']/ul/li/a"],
        # 轮播信息
        "banner_news": [],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='item']/h2/a | //div[@class='item']/p/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='hd_block']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://www\.chinatimes\.net\.cn/article/\d+\.html$",
        ],
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
    },
    # 中国经济网
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
        # 起始地址。
        "start_url": "http://www.ce.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='hot_news clearfix']//h1/a | //div[@class='hot_news clearfix']//span/a"],
        # 轮播信息
        "banner_news": ["//div[@class='img_list']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='hotnews']/div/ul/li/a"],
        # 模板内容。
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav_con']/div/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+\.ce\.cn/[\w/]+/\d{6,}/\d{2}/t\d{8,}_\d+\.shtml$",
        ],
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
    },
    # 中国军网
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
        # 起始地址。
        "start_url": "http://www.81.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='articles']/h2/a"],
        # 轮播信息
        "banner_news": ["//div[@class='touchslider-viewport']/div/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='tab-body']/ul/li/div/a"],
        # 模板内容。
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav-inner clearfix']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+\.81\.cn/\w+/\d{4,}-\d{2}/\d{2}/content_\d+\.htm$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='article-header']/h1/text()", },
                {"xpath": "//div[@class='container artichle-info']/h2/text()", },
                {"xpath": "//div[@class='video-header']/h2/text()", },
            ],
            "content": [
                {"xpath": "//div[@id='article-content']", },
                {"xpath": "//div[@id='cmplayer']", },  # 视频
            ],
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
    },
    # 中工网
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
        # 起始地址。
        "start_url": "http://www.workercn.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='container tt']//a"],
        # 轮播信息
        "banner_news": ["//ul[@id='tptt']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='list']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav1']/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+\.workercn\.cn/\d+/\d{6,}/\d{2}/\d+\.shtml$",
        ],
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
    },
    # 15
    # 中国农网
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
        # 起始地址。
        "start_url": "http://www.farmer.com.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='section headline']//a"],
        # 轮播信息
        "banner_news": ["//div[@id='main_swiper']/div/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='today-topic-aside fl']/ul/li/a"],
        # 模板内容。
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']/div/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://www\.farmer\.com\.cn/\d{4,}/\d{2}/\d{2}/\d+\.html$",
        ],
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
    },
    # 中国青年网
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
        # 起始地址。
        "start_url": "http://www.youth.cn",
        # 首页头条新闻
        "headline_news": ["//div[@class='TRS_Editor']/h1//a"],
        # 轮播信息
        "banner_news": ["//div[@class='slidImgDiv']/ul[@class='magicp']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='new-list']/div[@class='TRS_Editor']/li/a"],
        # 模板内容。
        # 导航信息
        "channel_info_xpath": ["//div[@class='menu-con']/ul/li//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+\.youth\.cn/\w+/\d{6,}/t\d{8,}_\d+\.htm$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//p[@class='pbt']/text()", },
                {"xpath": "//div[@class='page_title']/h1/text()", },
            ],
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
    },
    # 中国日报网(已更新)
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
        # 起始地址。
        "start_url": "http://cn.chinadaily.com.cn/",
        "cookie": "HMF_CI=12667dd61fe93041ee8c82ce53aac965ff0928095abcef7d6e70e88984a531a4c3; "
                  "HMY_JC=7f71120772ceed882574bd9ea0af696546f75c3df19c3f0bcd0c0b34762ac2ba0a,2370; "
                  "wdcid=0a25acac60aa7f80; wdlast=1610188582; wdses=1812abe2724300f7; "
                  "UM_distinctid=176e6b7eb9e77b-065b44a985a9fa-4353760-144000-176e6b7eb9f448; "
                  "CNZZDATA1975683=cnzz_eid%3D1035344945-1610185739-%26ntime%3D1610185739; "
                  "pt_37a49e8b=uid=tILTtIcYP7WuyHcIAaUOcw&nid=1&vid=I9tW1nj-G2r79Rvpg1RwXA&vn=1&pvn=1&"
                  "sact=1610188583596&to_flag=0&pl=t4NrgYqSK5M357L2nGEQCw*pt*1610188583596; "
                  "pt_s_37a49e8b=vt=1610188583596&cad=",
        # 首页头条新闻
        "headline_news": ["//div[@id='xi']//a"],
        # 轮播信息
        "banner_news": ["//div[@id='D1pic1']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='yaowen-xinwen']/h2/a | //div[@class='yaowen-xinwen']/h3/a |"
                             " //div[@class='right-lei']/ul[1]/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='header']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+\.chinadaily\.com\.cn/a/\d{6,}/\d{2}/\w+\.html$",
        ],
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
                    "regex": r"\s*?来源[: ：]\s*?(\w+)$",
                }
            ],
            "pubTime": [
                {"xpath": "//div[@class='fenx']/div[@class='xinf-le'][2]//text()", },
                {"xpath": "//p[@class='main_title3']/text()", },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中华工商网
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
        # 起始地址。
        "start_url": "http://www.cbt.com.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='topline']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='tempWrap']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='mod-txt'][1]/div[@class='bd']/div[@class='txt']/ul/li/a"],
        # 模板内容。
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']/ul/li/a | //div[@class='subnav']/div/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://www\.cbt\.com\.cn/[\w/]+/\d{6,}/t\d{8,}_\d+\.html$",
        ],
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
    },
    # 中国企业网
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
        # 起始地址。
        "start_url": "http://www.zqcn.com.cn/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='tempWrap']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//p[@class='t']/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='navbox']/ul/li/a | //div[@class='menu']/div/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+\.zqcn\.com\.cn/[\w/]+/\d{6,}/\d{2}/c?\d+\.html",
            r"https?://[\w\-\.]+\.zqcn\.com\.cn/[\w/]+/\d{8,}/c?\d+\.html$",
            r"https?://[\w\-\.]+\.zqcn\.com\.cn/[\w/]+/content/c?\d+\.html$",
        ],
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
    },
    # 20
    # 中国经济导报网
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
        # 起始地址。
        "start_url": "http://www.ceh.com.cn/",
        # 首页头条新闻
        "headline_news": ["//td[@class='title_m1']/a"],
        # 轮播信息
        "banner_news": [],
        # 轮播旁边新闻
        "banner_news_side": ["//td[@class='jryw_list']/a"],
        # 导航信息
        "channel_info_xpath": ["//td[@class='dh dh_unsel']/a"],
        # 详情链接。
        "doc_links": [
            r"https?://www\.ceh\.com\.cn/\w+/\d{4,}/\d+\.shtml$",
            r"https?://www\.ceh\.com\.cn/\w+/\d+\.shtml$",
        ],
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
        },
    },
    # 中国妇女网
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
        # 起始地址。
        "start_url": "http://www.cnwomen.com.cn/",
        # 首页头条新闻
        "headline_news": ["//h3[@class='tab_title']/a"],
        # 轮播信息
        "banner_news": ["//ul[@id='bannerList']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='tab_sub_items']/li/span/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav_main']/ul/li//span/a"],
        # 详情链接。
        "doc_links": [
            r"https?://www\.cnwomen\.com\.cn/\d{4,}/\d{2}/\d{2}/\d+\.html$",
        ],
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
    },
    # 中国科技网
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
        # 起始地址。
        "start_url": "http://www.stdaily.com/",
        # 首页头条新闻
        "headline_news": ["//div[@class='mainNav']/ul/li/a"],
        # 轮播信息
        "banner_news": ["//div[@class='swiper-wrapper']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='m_hotnews_left']//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav_main']/ul/li//span/a"],
        # 详情链接。
        "doc_links": [
            r"https?://www\.stdaily\.com/[\w/]+/\d{4,}-\d{2}/\d{2}/content_\d+\.shtml$",
        ],
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
    },
    # 界面新闻
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
        # 起始地址。
        "start_url": "https://www.jiemian.com/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//ul[@class='slider-body']/li//h3/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='news-msg-list']/div//h3/a |  //h3[@class='title']/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='jiemian-nav']/li/div/a"],
        # 模板内容。
        # 详情链接。
        "doc_links": [r"https?://www\.jiemian.com/article/\d+.html$", ],
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
    },
    # 云南网
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
        # 起始地址。
        "start_url": "http://www.yunnan.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='ar-t fr']/h1/a"],
        # 轮播信息
        "banner_news": ["//div[@id='sl1']/div[@class='wrapper']/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='n_yw nn xjp']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='main clearfix']/ul/li/a"],
        # 模板内容。
        # 详情链接。
        "doc_links": [
            r"http://[\w\-\.]+\.yunnan\.cn/system/\d{4,}/\d{2}/\d{2}/\d+.shtml$",
        ],
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
    },
    # 25
    # 河北新闻网(已更新)
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
        # 起始地址。
        "start_url": "http://www.hebnews.cn/",
        # cookie
        "cookie": "Cookie: zycna=RaUngjlqosUBAd7f1SJVm0RP; 2wop_93a6_saltkey=jP8TTEDT; 2wop_93a6_lastvisit=1608195093;"
                  " 2wop_93a6_visitedfid=383; Hm_lvt_fc19c432c6dd37e78d6593b2756fb674=1607493845,1608198201,1608198678,"
                  "1608712773; Hm_lpvt_fc19c432c6dd37e78d6593b2756fb674=1608712773",
        # 首页头条新闻
        "headline_news": ["//div[@class='zj2018-headline']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='yx-rotaion']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='tdn']//div/ul/li/a | //div[@class='list-gov']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav-ul']/ul/li/a | //li[@class='nav-more']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+\.hebnews\.cn/\d{4,}-\d{2}/\d{2}/content_\d+\.htm$",
            # 影像河北
            # r"https?://[\w\-\.]+\.hebnews\.cn/[\w]+-\d+-\d-\d\.html"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='g_width content']/h1/text()", },
                # 影视河北
                # {"xpath": "//span[@id='thread_subject']/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='text']", },
                {"xpath": "//div[@class='t_fsz']//td", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class='post_source']/text()",
                    "regex": r".*来源:\s*?(\w+)$",
                }
            ],
            "pubTime": [{"xpath": "//div[@class='post_source']/text()", }, ],
            "channel": [{"xpath": "//div[@class='bc_main']/a[1]/text()", }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 四川新闻网
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
        # 起始地址。
        "start_url": "http://www.newssc.org/",
        # 首页头条新闻
        "headline_news": ["//div[@class='zj2018-headline']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='yx-rotaion']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@id='tbc_11']/div//li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav-ul']/ul/li/a"],
        # 模板内容。
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
    },
    # 封面新闻
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
        # 起始地址。
        "start_url": "http://www.thecover.cn/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='bigView-list']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": [],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='top-nav']/li/a | //div[@class='more-wrapper']/a"],
        # 详情链接。
        "doc_links": [
            r"https?://www\.thecover\.cn/news/\d+$",
        ],
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
    },
    # 台海网
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
        # 起始地址。
        "start_url": "http://www.taihainet.com/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='owl-wrapper']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='news-l fl']/div/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='w1200']/a"],
        # 模板内容。
        # 详情链接。
        "doc_links": [
            r"https?://www\.taihainet\.com/(\w+/){2,3}\d{4,}-\d{2}-\d{2}/\d+.html$",
        ],
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
    },
    # 东南网
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
        # 起始地址。
        "start_url": "http://www.fjsen.com/",
        # 首页头条新闻
        "headline_news": ["//div[@class='ct tt']//a"],
        # 轮播信息
        "banner_news": [],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='lsa']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='ct']/div/a"],
        # 模板内容。
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+\.fjsen\.com/\d{4,}-\d{2}/\d{2}/content_\d+\.htm$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='cont_head']/h1/text()", },
                {"xpath": "//div[@class='biaoti']/text()", },
                {"xpath": "//div[@class='big_title']/h1/text()", },
            ],
            "content": [
                {"xpath": "//td[@id='new_message_id']", },
                {"xpath": "//div[@id='zoom']", },
                {"xpath": "//td[@id='new_message_id']", },
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
    },
    # 30
    # 闽南网
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
        # 起始地址。
        "start_url": "http://www.mnw.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='mnw_top']//a"],
        # 轮播信息
        "banner_news": ["//div[@id='KSS_content']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='mnw_now']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav_link_line']/div/a"],
        # 模板内容。
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+\.mnw\.cn/[\w/]+/\d+\.html$",
        ],
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
    },
    # 四川在线
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
        # 起始地址。
        "start_url": "https://www.scol.com.cn/",
        # 首页头条新闻
        "headline_news": ["//ul[@class='a1']/a | //ul[@class='a2']/li[2]//a"],
        # 轮播信息
        "banner_news": ["//ul[@class='hd']/ol/h1/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//li[@class='xw_txt']/dt/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='scol_nav']/ul/li/a"],
        # 模板内容。
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+\.scol\.com\.cn/\w+/\d{6,}/\d+.html$",
        ],
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
    },
    # 广西新闻网(需要修改)
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
        # 起始地址。
        "start_url": "http://www.gxnews.com.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='model-title']/ul/li//a"],
        # 轮播信息
        "banner_news": ["//div[@id='focus_conau_21360']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='day-list']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav']/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+\.gxnews\.com\.cn/staticpages/\d{8,}/newgx\w+-\d+\.shtml$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='article']/h1/text()", },
                {"xpath": "//td[@class='title']/text()", },
                {"xpath": "//td[@class='title']/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='article-content']", },
                {"xpath": "//td[@id='artContent']", },
                {"xpath": "//td[@class='artContent article-content']", },
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
    },
    # 大江网
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
        # 起始地址。
        "start_url": "http://www.jxnews.com.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='xdd_bigtit']/h1/a | //ul[@class='xdd_lb']//li/a"],
        # 轮播信息
        "banner_news": [],
        # 轮播旁边新闻
        "banner_news_side": ["//td[@class='ywli']/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='con']/ul[@class='topmenu']/li/a"],
        # 模板内容。
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+\.jxnews\.com\.cn/system/\d{4,}/\d{2}/\d{2}/\d+\.shtml$",
        ],
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
    },
    # 京报网
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
        # 起始地址。
        "start_url": "http://www.bjd.com.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='xdd_bigtit']/h1/a | //ul[@class='xdd_lb']//li/a"],
        # 轮播信息
        "banner_news": [],
        # 轮播旁边新闻
        "banner_news_side": ["//td[@class='ywli']/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='con']/ul[@class='topmenu']/li/a"],
        # 模板内容。
        # 详情链接。
        "doc_links": [
            r"https?://www\.bjd\.com\.cn/a/\d{6,}/\d{2}/\w+\.html$",
        ],
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
    },
    # 35
    # 新京报网
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
        # 起始地址。
        "start_url": "http://www.bjnews.com.cn/",
        # 首页头条新闻
        "headline_news": ["//a[@class='outsideLink']"],
        # 轮播信息
        "banner_news": ["//div[@class='swiper-wrapper']/div/div[1]/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//h3/a[@class='link']"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='menu_inner']/span/a"],
        # 模板内容。
        # 详情链接。
        "doc_links": [
            r"https?://www\.bjnews\.com\.cn/\w+/\d{4,}/\d{2}/\d{2}/\d+\.html$",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//div[@class='title']/h1/text()", },
                {"xpath": "//div[@class='bodyTitle']/div/h1/text()", },
            ],
            "content": [
                {"xpath": "//div[@class='content']", },
                {"xpath": "//div[@class='article-text']", },
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
    },
    # 新民网
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
        # 起始地址。
        "start_url": "http://www.xinmin.cn/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": [],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='item']/h1/a | //div[@class='HotContent']/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='MainNav']/a"],
        # 模板内容。
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+\.xinmin\.cn/\w+/\d{4,}/\d{2}/\d{2}/\d+\.html$",
        ],
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
    },
    # 中国政府网
    {
        "platformName": "中国政府网",
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
        # 起始地址。
        "start_url": "http://www.gov.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='column1']/div/a"],
        # 轮播信息
        "banner_news": ["//div[@class='slidesjs-control']/div//h6/a"],
        # 轮播旁边新闻
        "banner_news_side": [],
        # 导航信息
        "channel_info_xpath": ["//div[@id='menu']/ul[@id='nav']/li/ul/li/a"],
        # 详情链接。
        "doc_links": ["http://www.gov.cn/[a-z]+/\\\\d{4}-\\\\d{2}/\\\\d{2}/content_\\\\d+.htm"],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [{"xpath": "//h1/text()"}],
            "content": [{"xpath": "//div[@class=\'pages_content\']"}],
            "pubSource": [{"describe": "http://www.gov.cn/xinwen/2020-01/14/content_5468786.htm",
                           "xpath": "//span[@class=\'font\']/text()",
                           "regex": "\\u6765\\u6e90\\uff1a\\\\s+([\\\\S]+)"}],
            "pubTime": [{"xpath": "//div[@class=\'pages-date\']/text()"}],
            "channel": [{"xpath": "//div[@class=\'BreadcrumbNav\']/a[2]/text()"}],
            "authors": [{"xpath": ""}],
            "summary": [{"xpath": ""}],
        }
    },
    # 共产党员网
    {
        "platformName": "共产党员网",
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
        # 起始地址。
        "start_url": "http://www.12371.cn/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='swiper-container20190916']/div[@class='swiper-wrapper']/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='dyw820_text_List']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='dyw947_nav']/li/a"],
        # 详情链接。
        "doc_links": ["http://www.12371.cn/\\\\d{4}/\\\\d{2}/\\\\d{2}/[A-Z0-9]+.shtml",
                      "http://tougao.12371.cn/gaojian.php?tid=\\\\d+"],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [{"xpath": "//h1[@class=\'big_title\']/text()"}],
            "content": [{"xpath": "//div[@class=\'con\']"}],
            "pubSource": [
                {"describe": "http://www.12371.cn/2018/10/22/ARTI1540177872459953.shtml",
                 "xpath": "//i[@class=\'time\']/text()", "regex": "\\u6765\\u6e90\\uff1a([\\\\S]+)"}],
            "pubTime": [{"xpath": "//i[@class=\'time\']/text()"}],
            "channel": [{"xpath": "//div[@id=\'path\']/a[last()]/@title"}],
            "authors": [{"xpath": ""}],
            "summary": [{"xpath": ""}],
        }
    },
    # 北青网
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
        # 起始地址。
        "start_url": "http://www.ynet.com/index.html",
        # 首页头条新闻
        "headline_news": ["//div[@class='bq_event w1200']/h1/a"],
        # 轮播信息
        "banner_news": ["//div[@id='tu_da']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='fRight bq_kuaixun']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@id='navBar']/ul/li/a"],
        # 模板内容。
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+\.ynet\.com/\d{4,}/\d{2}/\d{2}/\w+.html$",
        ],
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
    },
    # 40
    # 中华网
    {
        "platformName": "中华网",
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
        "start_url": "https://www.china.com/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='focusCon']/div//a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='spotCon']/ul//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='con clearfix']/div/div//a"],
        # 详情链接。
        "doc_links": ["https://[a-z]+.china.com/[a-z/]+/\\\\d+/\\\\d{8}/\\\\d+.html"],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [{"xpath": "//h1/text()"}],
            "content": [{"xpath": "//div[@id=\'chan_newsDetail\']"}],
            "pubSource": [{"describe": "https://news.china.com/zw/news/13000776/20200114/37704846.html",
                           "xpath": "//div[@class=\'chan_newsInfo_source\']/span[@class=\'source\']/a/text()"}],
            "pubTime": [{"xpath": "//div[@class=\'chan_newsInfo_source\']/span[@class=\'time\']/text()"}],
            "channel": [{"xpath": "//div[@id=\'chan_breadcrumbs\']/a[last()]/text()"}],
            "authors": [{"xpath": ""}],
            "summary": [{"xpath": ""}]
        }
    },
    # 第一财经
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
        # 起始地址。
        "start_url": "https://www.yicai.com/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//div[@class='textlist']/a | //div[@class='owl-stage']/div//a"],
        # 轮播旁边新闻
        "banner_news_side": [],
        # 导航信息
        "channel_info_xpath": ["//div[@class='m-menu']/ul/li/a"],
        # 模板内容。
        # 详情链接。
        "doc_links": [
            r"https?://www\.yicai\.com/news/\d+\.html$",
        ],
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
    },
    # 湖南在线
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
        # 起始地址。
        "start_url": "http://hunan.voc.com.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='dbt_l']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='bjt']//h4/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='font2']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav_in']/p/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+\.voc\.com\.cn/article/\d{6,}/\d+\.html$",
        ],
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
    },
    # 中国文明网
    {
        "platformName": "中国文明网",
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
        # 起始地址。
        "start_url": "http://www.wenming.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='Hotnews']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='swiper-wrapper']/div//p/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='news_list news_list_lh34']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//nav//div[@class='nav_bottom-C']/ul/li/a"],
        # 详情链接。
        "doc_links": ["http://www.wenming.cn/[a-z\\\\/]+\\\\d{6}/t\\\\d{8}_\\\\d+.shtml"],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [{"xpath": "//div[@id=\'title_tex\']/text()"}],
            "content": [{"xpath": "//div[@class=\'TRS_Editor\']"}],
            "pubSource": [{"describe": "http://www.gov.cn/xinwen/2020-01/14/content_5468786.htm",
                           "xpath": "//div[@id=\'time_tex\']/text()", "regex": "\\\\d+-\\\\d+-\\\\d+([\\\\S]+)"}],
            "pubTime": [{"xpath": "//div[@id=\'time_tex\']/text()"}],
            "channel": [{"xpath": "//div[@class=\'title\']/a[last()-1]/text()"}],
            "authors": [{"xpath": ""}],
            "summary": [{"xpath": ""}],
        }
    },
    # 未来网
    {
        "platformName": "未来网",
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
        "start_url": "http://www.k618.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='hd d_cap']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='ptC']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='u u_dot']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='t_nav']/li/a"],
        # 详情链接。
        "doc_links": ["http://news.k618.cn/[a-z]+/\\\\d{6}/t\\\\d{8}_\\\\d+.html"],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [{"xpath": "//h1/text()"}],
            "content": [{"xpath": "//div[@class=\'TRS_Editor\']"}],
            "pubSource": [{"describe": "http://www.gov.cn/xinwen/2020-01/14/content_5468786.htm",
                           "xpath": "//div[@class=\'news_time_source\']/span/text()", "regex": "\\\\t([\\\\S]+)"}],
            "pubTime": [{"xpath": "//div[@class=\'news_time_source\']/text()"}],
            "channel": [{"xpath": "//div[@class=\'news_crumb\']/p/a[last()]/text()"}],
            "authors": [{"xpath": ""}],
            "summary": [{"xpath": ""}],
        }
    },
    # 45
    # 中国警察网
    {
        "platformName": "中国警察网",
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
        # 起始地址。
        "start_url": "http://www.cpd.com.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@id='top_5']/h1/a"],
        # 轮播信息
        "banner_news": ["//ul[@id='sb-slider']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@id='c1_left']/div//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='t3_1']/div//li//a"],
        # 详情链接。
        "doc_links": ["http://[a-z]+.cpd.com.cn/n\\\\d+/\\\\d{6}/t\\\\d{8}_\\\\d+.html"],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [{"xpath": "//gettitle/text()"}],
            "content": [{"xpath": "//div[@class=\'TRS_Editor\']/div[@class=\'TRS_Editor\']"}],
            "pubSource": [{"describe": "https://news.dahe.cn/2020/01-14/578827.html",
                           "xpath": "//span[@id=\'source_report\']/text()"}],
            "pubTime": [{"xpath": "//span[@id=\'pub_time_report\']/text()"}],
            "channel": [{"xpath": "//div[@id=\'path\']/a[last()]/@title"}],
            "authors": [{"xpath": "//div[@class=\'newsattr z12\']/span[@id=\'author_report\']/text()"}],
            "summary": [{"xpath": ""}],
        }
    },
    # 经济观察网
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
        # 起始地址。
        "start_url": "http://www.eeo.com.cn/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ["//ul[@class='w_bannerPic']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='xd-div']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='xd-list-shangye']/li/a"],
        # 详情链接。
        "doc_links": ["https?://www\\\\.eeo\\\\.com\\\\.cn/\\\\d{4,}/\\\\d{4}/\\\\d+\\\\.shtml$"],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [{"xpath": "//div[@class=\'xd-b-b\']/h1/text()"}],
            "content": [{"xpath": "//div[@class=\'xd-nr\']/*[@class=\'xd-xd-xd-newsimg\' or @class=\'xx_boxsing\']"}],
            "pubSource": [],
            "pubTime": [{"xpath": "//div[@class=\'xd-b-b\']/p/span[1]/text()"}],
            "channel": [{"xpath": ""}],
            "authors": [{"xpath": "//div[@class=\'xd-b-b\']/p/text()[1]"}],
            "summary": [{"xpath": ""}],
        }
    },
    # 三秦网
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
        # 起始地址。
        "start_url": "http://www.sanqin.com/",
        # 首页头条新闻
        "headline_news": ["//div[@class='headLineBox']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='swiper-wrapper']//div[@class='focus-con']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='hotNewsLine']/li/h3/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='nav']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://www\.sanqin\.com/\d{4,}-\d{2}/\d{2}/content_\d+\.html$",
        ],
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
    },
    # 老友网
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
        # 起始地址。
        "start_url": "http://www.nntv.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='headline']/h2/a"],
        # 轮播信息
        "banner_news": ["//div[@class='swiper-container swiper-container-horizontal']/div/div/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='txtList list_gdxw']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='navBar']/div/ul/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://www\.nntv\.cn/[\w/]+/\d{4,}-\d{1,2}-\d{1,2}/\d+\.shtml$",
        ],
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
    },
    # 半月谈网
    {
        "platformName": "半月谈网",
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
        "start_url": "http://www.banyuetan.org/",
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class='hot_tt']/h3/a"],
        # 轮播信息
        "banner_news": ["//div[@class='event-item']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@class='byt_jd clearFix']/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='more_list']/ul/li/a"],
        # 详情链接。
        "doc_links": ["http://www.banyuetan.org/[a-z]+/detail/\\\\d{8}/\\\\d+_1.html"],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [{"xpath": "//h1/text()"}],
            "content": [
                {"xpath": "//div[@class=\'detail_content\']"}],
            "pubSource": [{
                "describe": "http://www.banyuetan.org/pl/detail/20200114/1000200033135041578880530986392036_1.html",
                "xpath": "//div[@class=\'detail_tit_source\']/text()",
                "regex": "\\u6765\\u6e90\\uff1a([\\\\S]+)"}],
            "pubTime": [{
                "xpath": "//div[@class=\'detail_tit_time\']/text()"}],
            "channel": [{"xpath": "", }, ],
            "authors": [],
            "summary": [
                {
                    "xpath": "",
                },
            ],
        }
    },
    #############################################################################
    # 50

    # 潇湘晨报网
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
        # 起始地址。
        "start_url": "http://www.xxcb.cn/",
        # 首页头条新闻
        "headline_news": ["//div[@class='headLineBox']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='swiper-wrapper']//div[@class='focus-con']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='hotNewsLine']/li/h3/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='nav']/li/a"],
        # 详情链接。
        "doc_links": [
            r"https?://www\.xxcb\.cn/\w+/\w+/\d{4,}-\d{2}-\d{2}/\d+\.html$",
        ],
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
    },
    # 深圳新闻网
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
        # 起始地址。
        "start_url": "http://www.sznews.com/",
        # 首页头条新闻
        "headline_news": ["//div[@class='headLineBox']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='swiper-wrapper']//div[@class='focus-con']/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='hotNewsLine']/li/h3/a"],
        # 导航信息
        "channel_info_xpath": ["//ul[@class='nav']/li/a"],
        # 详情链接。
        "doc_links": [
            "https?://[\\\\w\\\\-\\\\.]+\\\\.sznews\\\\.com/[\\\\w/]*?content/\\\\d{4,}-\\\\d{2}/\\\\d{2}/content_\\\\d+\\\\.htm$"],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [{"xpath": "//h1[@class=\'h1-news\']/text()"}, {"xpath": "//h1[@class=\'con_title\']/text()"}],
            "content": [{"xpath": "//div[contains(@class, \'article-content\')]/*[not(@id=\'qrcodeWrap\')]"}, {
                "xpath": "//div[@id=\'con_arc_content\']/*[not(@id=\'qrcodeWrap\') and not(@class=\'pages\')]"}],
            "pubSource": [{"describe": "http://www.sznews.com/news/content/2020-01/17/content_22784754.htm",
                           "xpath": "//span[@class=\'ml10\']/text()",
                           "regex": "\\\\s*?\\u6765\\u6e90\\uff1a\\\\s*?(\\\\w+)$"}],
            "pubTime": [{"xpath": "//div[@class=\'fs18 share-date l\']/text()"},
                        {"xpath": "//div[@class=\'fs18 r share-date\']/text()"},
                        {"xpath": "//div[@class=\'bigPhoto-date yahei fs18 r\']/text()"}],
            "channel": [{"xpath": "//div[@class=\'crumbs yahei\']/a[2]/text()"},
                        {"xpath": "//div[@class=\'crumbs cf\']/a[2]/text()"}],
            "authors": [],
            "summary": [{"xpath": "//h2[@class=\'article-title\']/text()"}],
        }
    },
    # 华西都市网
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
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.huaxi100.com/",
        # 首页头条新闻
        "headline_news": ["//div[@id='top_5']/h1/a"],
        # 轮播信息
        "banner_news": ["//ul[@id='sb-slider']/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//div[@id='c1_left']/div//a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='t3_1']/div//li//a"],
        # 详情链接。
        "doc_links": ["https?://www\\\\.huaxi100\\\\.com/a/\\\\w+$",
                      "https?://news\\\\.huaxi100\\\\.com/show-[\\\\d\\\\-]+\\\\.html$"],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [{"xpath": "//h5[@class=\'title\']/text()"}, {"xpath": "//h1[@class=\'details_title\']/text()"}],
            "content": [{"xpath": "//section[@class=\'sec-content\']/*[not(@data-tools)]"},
                        {"xpath": "//div[@class=\'summary\']"}],
            "pubSource": [{"xpath": "//div[@class=\'details_info\']/text()", "regex": ".*?\\u6765\\u6e90: (\\\\w+)$"}],
            "pubTime": [{"xpath": "//div[@class=\'details_info\']/text()"}],
            "channel": [{"xpath": "//span[@class=\'nrNow\'][1]/a/text()"}],
            "authors": [{"xpath": ""}],
            "summary": [{"xpath": "//p[@class=\'pad-bt\']/text()"}],
        }
    },
    # 广东广播电视台
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
    # 21世纪经济报道
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

    # 南方周末
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
    # 福建网络广播电视台
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
        # 起始地址。
        "start_url": "http://www.fjtv.net/",
        # 首页头条新闻
        "headline_news": ["//div[@class='dbt_l']//a"],
        # 轮播信息
        "banner_news": ["//div[@class='bjt']//h4/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class='font2']/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class='nav_in']/p/a"],
        # 模板内容。
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+\.fjtv.net/folder\d+/\d{4,}-\d{2}-\d{2}/\d+\.html$",
        ],
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
    },
    # 宁夏广播电视台
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
    # 青海羚网
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
    # 广西广播电视台
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
    # 黑龙江网络广播电视台
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
    # 四川广播电视台
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

    # 1/11
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
    # 1/15

    # 淮南网
    {
        "platformName": "淮南网",
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
        "cookie": "__cfduid=d7fec309fe686f2bc3d17bd33122736701610625537; membercenterjsessionid=ZTRkNDYzMjgtOGQ3MC00NDA1LTk3ZWEtYWVjNzA0ODdlNjNi; hn_gova_SHIROJSESSIONID=a96f8258-b678-465e-9c5a-d4a2dedd1b9f",
        # 首页头条新闻
        "headline_news": ["//h1[@class=\"dbt\"]/a | //ul[@class=\"zt clearfix\"]/li/a"],
        # 轮播信息
        "banner_news": ["//*[@id=\"myFocus011\"]/div[1]/ul/li/a"],
        # 轮播旁边新闻
        "banner_news_side": [
            "//div[@class=\"ind_xwlist\"]/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"menubox\"]/dl/dd/div[1]/a"],
        # 详情链接。
        "doc_links": [
            r"http?://[\w\-\.]+/\w+/\w+/\d+.html",
            r"http?://[\w\-\.]+/\w+/\d{4,}-\d{2,}/\d{2,}/\w+_\d+.htm",
            r"http?://[\w\-\.]+/\w+/\d+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class=\"newstitle\"]/text()", },
                {"xpath": "//div[@class=\"article oneColumn pub_border\"]/h1/text()", },
                {"xpath": "//h1[@class=\"wztit xxgk_wztit\"]/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"wzcon j-fontContent clearfix\"]", },
                {"xpath": "//div[@id=\"UCAP-CONTENT\"]/p[position()>1]", },
                {"xpath": "//div[@class=\"wzcon j-fontContent\"]", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class=\"fl\"]/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class=\"pages-date\"]/span/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//span[@class=\"fbxx\"]/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {"xpath": "//div[@class=\"fl\"]/text()", "regex": r"(.*)点击.*", },
                {"xpath": "//div[@class=\"pages-date\"]/text()", },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易
    {
        "platformName": "网易",
        # "sourceProvince": "安徽省",
        # "sourceCity": "",
        # "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 0,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.163.com/",
        "cookie": "__root_domain_v=.163.com; _qddaz=QD.hgrr5b.c9otyz.kchpu6qj; _ntes_nnid=6eeab83b4796aee032e6670f889dd93e,1596855361285; _ntes_nuid=6eeab83b4796aee032e6670f889dd93e; mail_psc_fingerprint=ec22c0cfd16f2e323e9e1c670de4176b; UM_distinctid=173fca2fb2218c-0ea36d67ae1885-4353760-144000-173fca2fb23605; NTES_CMT_USER_INFO=306445309%7C%E6%9C%89%E6%80%81%E5%BA%A6%E7%BD%91%E5%8F%8B0ig-LZ%7Chttp%3A%2F%2Fcms-bucket.nosdn.127.net%2F2018%2F08%2F13%2F078ea9f65d954410b62a52ac773875a1.jpeg%7Cfalse%7CengxODkzMjk5QDE2My5jb20%3D; nteslogger_exit_time=1601115521462; nts_mail_user=ciyhnb@163.com:-1:1; P_INFO=zx1893299@163.com|1610172364|0|mail163|00&99|tij&1610172354&carddav#bej&null#10#0#0|&0|mailmaster_ios|zx1893299@163.com; _antanalysis_s_id=1611120776182; NTES_hp_textlink1=old; CNZZDATA1254828714=22731690-1602910188-https%253A%252F%252Fnews.163.com%252F%7C1611120556; ne_analysis_trace_id=1611122402110; s_n_f_l_n3=00091e913c1675381611122402117; UserProvince=%u5168%u56FD; vinfo_n_f_l_n3=00091e913c167538.1.10.1597671403757.1602912823459.1611122427219",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": [],
        # 轮播旁边新闻
        "banner_news_side": [
            "//div[@id=\"tab-news-01\"]/ul/li/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"nav-mod cf\"]//a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/[A-z0-9]+/[A-z0-9]+.html"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//h1[@class=\"newstitle\"]/text()", },
                {"xpath": "//div[@class=\"article oneColumn pub_border\"]/h1/text()", },
                {"xpath": "//h1[@class=\"wztit xxgk_wztit\"]/text()", },
            ],
            "content": [
                {"xpath": "//div[@class=\"wzcon j-fontContent clearfix\"]", },
                {"xpath": "//div[@id=\"UCAP-CONTENT\"]/p[position()>1]", },
                {"xpath": "//div[@class=\"wzcon j-fontContent\"]", },
            ],
            "pubSource": [
                {
                    "xpath": "//div[@class=\"fl\"]/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//div[@class=\"pages-date\"]/span/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//span[@class=\"fbxx\"]/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                },
            ],
            "pubTime": [
                {"xpath": "//div[@class=\"fl\"]/text()", "regex": r"(.*)点击.*", },
                {"xpath": "//div[@class=\"pages-date\"]/text()", },
            ],
            "authors": [],
            "summary": [],
        }
    },

]
