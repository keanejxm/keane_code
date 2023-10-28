paper_templates = [
    # 1/13
    # 河北省监察厅(90)
    {
        "platformName": "河北省监察厅",
        # "sourceProvince": "河北省",
        # "sourceCity": "",
        # "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.hebcdi.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//div[@class="tdn"]/div/ul//a'],
        # 轮播信息
        "banner_news": ['//*[@id="KSS_content"]/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[2]/div[2]/div[2]/div/div[1]//a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[1]//a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+\-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "string(/html/body/div[3]/div[1]/div[2]/div[2]/div[1]/div[1])", },
                {"xpath": "/html/body/div[2]/div/div[2]/div[1]/div[1]/h1/text()", },
                {"xpath": "/html/body/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/text()", },
            ],
            "content": [
                {"xpath": "/html/body/div[3]/div[1]/div[2]/div[1]/div[2]", },
                {"xpath": "/html/body/div[3]/div[1]/div[2]/div[2]/div[2]", },
            ],
            "pubSource": [
                {"xpath": "/html/head/meta[16]/@content",
                 }
            ],
            "pubTime": [{
                "xpath": "/html/head/meta[15]/@content",
            }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 河北旅游局(非新闻类网站，可以忽略)
    {
        "platformName": "河北旅游局",
        "sourceProvince": "河北省",
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
        "start_url": "http://www.hebeitour.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//*[@id="tbc_0"]/ul//a'],
        # 轮播信息
        "banner_news": ['/html/body/div[6]/div[1]/div//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="tbc_2"]/ul//a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[3]/div/ul/li/a'],
        # 详情链接。
        "doc_links": [
            r".*ArticleDetail\?id=\d+",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "string(/html/body/div[4]/div[1]/div[2]/h1/text())", },
                {"xpath": '//*[@id="Tow_page"]/div[2]/div[2]/h1/text()', },
                # {"xpath": "/html/body/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]", },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                # {"xpath": "/html/body/div[3]/div[1]/div[2]/div[2]/div[2]", },
            ],
            "pubSource": [
                {"xpath": "/html/body/div[4]/div[1]/div[2]/div[1]/text()",
                 "regex": r"来源[: ：].*?(\w+)$"}
            ],
            "pubTime": [{
                "xpath": "/html/body/div[4]/div[1]/div[2]/div[1]/text()",
                "regex": r"(.*)文章来源.*$"
            }, ],
            "authors": [],
            "summary": [],
        }
    },
    # 河北体育局(90)
    {
        "platformName": "河北体育局",
        "sourceProvince": "河北省",
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
        "start_url": "http://www.hebsport.gov.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[5]/div[1]/div[2]/a'],
        # 轮播信息
        "banner_news": ['/html/body/div[5]/div[2]/div/div/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="indexNews"]/li/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[3]/div/ul/li//a'],
        # 详情链接。
        "doc_links": [
            r".*\w+/\d+/\d+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//*[@id="title"]/text()', },
                {"xpath": '//*[@id="Tow_page"]/div[2]/div[2]/h1/text()', },
                # {"xpath": "ml/body/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]", },
            ],
            "content": [
                {"xpath": '/html/body/div[4]/div/div[1]/article/div[2]', },
                # {"xpath": "ml/body/div[3]/div[1]/div[2]/div[2]/div[2]", },
            ],
            "pubSource": [
                {"xpath": "/html/body/div[4]/div/div[1]/article/div[1]/p/text()",
                 "regex": r"来源[: ：](.*).*时间.*"
                 },
            ],
            "pubTime": [
                {
                    "xpath": "/html/body/div[4]/div/div[1]/article/div[1]/p/text()",
                    "regex": r"时间[: ：](.*)"
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 河北人社厅(90)
    {
        "platformName": "河北人社厅",
        "sourceProvince": "河北省",
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
        "start_url": "https://rst.hebei.gov.cn/index.html",
        # 首页头条新闻
        "headline_news": ['//*[@id="con_news_1"]/ul/li/a'],
        # 轮播信息
        "banner_news": ['//*[@id="myjQueryContent"]/div/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="con_news_2"]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[1]/div/div[3]/ul/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\d+/\d+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[2]/div[1]/div[2]/div[1]/h1/text()', },
                {"xpath": '//*[@id="xxgknr"]/div/div[1]/h1/text()', },
                # {"xpath": "/html/body/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]", },
            ],
            "content": [
                {"xpath": '/html/body/div[2]/div[1]/div[2]/div[3]', },
                {"xpath": '//*[@id="xxgknr"]/div/div[3]', },
            ],
            "pubSource": [
                {"xpath": "/html/body/div[2]/div[1]/div[2]/div[2]/span[1]/text()",
                 "regex": r"来源[: ：].*?(.*)"}
            ],
            "pubTime": [{"xpath": "/html/body/div[2]/div[1]/div[2]/div[2]/span[2]/text()",
                         "regex": r"时间[: ：](.*)"},
                        ],
            "authors": [],
            "summary": [],
        }
    },
    # 河北公安厅(90)
    {
        "platformName": "河北公安厅",
        "sourceProvince": "河北省",
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
        "start_url": "http://gat.hebei.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//*[@id="s1668427_content"]/div/div/ul/li/a'],
        # 轮播信息
        "banner_news": ['//*[@id="slideBox"]/div[2]/ul/li[2]/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="s47083212_content"]/table//tr/td/span[1]/span/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="s19851677_content"]/table/tbody/tr/td/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+.*?detail&tid=\d+",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//*[@id="s3636946_content"]/div/table[1]//tr[1]/td/text()', },
                # {"xpath": '//*[@id="xxgknr"]/div/div[1]/h1', },
                # {"xpath": "/html/body/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]", },
            ],
            "content": [
                {"xpath": '//*[@id="s3636946_content"]/div/table[1]//tr[3]', },
                # {"xpath": '//*[@id="xxgknr"]/div/div[3]', },
            ],
            "pubSource": [
                {"xpath": 'string(//*[@id="s3636946_content"]/div/table[1]/tbody/tr[2]/td/table//tr//td[1])',
                 "regex": r"来源[: ：].*?(\w+)"}
            ],
            "pubTime": [{"xpath": 'string(//*[@id="s3636946_content"]/div/table[1]/tbody/tr[2]/td/table//tr/td[3])',
                         "regex": r"时间[: ：](.*)"},
                        ],
            "authors": [],
            "summary": [],
        }
    },
    # 1/14
    # 东方网
    {
        "platformName": "东方网",
        # "sourceProvince": "河北省",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://eastday.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="cpc19"]/h1/a'],
        # 轮播信息
        "banner_news": [],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="indexyw"]/div[3]//li/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="dh1"]//p/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\wnews/\d+",
            r"https?://[\w\-\.]+/\wnews/\w+\d+",
            r'https?://[\w\-\.]+/\w+\d+/\w+/\w+\d+/\d+/\w+\d+.html'
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//div[@class="article"]/h1/text()'},
                {"xpath": '/html/body/div[3]/div[3]/h1/text()', },
                {"xpath": '//h2[@class="dabiao7 ma"]/text()', },
                # {"xpath": "/html/body/div[3]/div[1]/div[2]/h1/text()", },
            ],
            "content": [
                {"xpath": '//div[@class="detail"]', },
                {"xpath": '//div[@class="para ma"]', },
            ],
            "pubSource": [
                {"xpath": '//div[@class="article"]//span[@class="source"]/a/text()  ',
                 }, {"xpath": 'string(//p[@class="time"][2])  ',
                     "regex": r"来源[: ：](.*?)\s"
                     },

            ],
            "pubTime": [
                {
                    "xpath": '//div[@class="article"]//span[@class="date"]/text()',
                    # "regex": r"\d+.*?:\d+"
                }, {
                    "xpath": '//p[@class="time"][1]/text()',
                    # "regex": r"\d+.*?:\d+"
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 上海在线1
    {
        "platformName": "上海在线",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.shzxmh.com/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[2]/div[1]/div[3]/div[1]/div/h3/a'],
        # 轮播信息
        "banner_news": ['/html/body/div[2]/div[1]/div[2]/div[1]/ul[1]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[2]/div[1]/div[2]/div[2]/div[@class="hotbox"]/h3/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[1]/div/ul/li//a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[2]/div[1]/div/div[2]/div[1]/h3/text()'},
                # {"xpath": '/html/body/div[3]/div[3]/h1/text()', },
                # {"xpath": '//h2[@class="dabiao7 ma"]/text()', },
                # {"xpath": "/html/body/div[3]/div[1]/div[2]/h1/text()", },
            ],
            "content": [
                {"xpath": '/html/body/div[2]/div[1]/div/div[3]', },
            ],
            # 上海在线没有来源
            "pubSource": [
                {"xpath": '//div[@class="article"]//span[@class="source"]/a/text()  ',
                 }

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[2]/div[1]/div/div[2]/div[1]/p/span[2]/text()',
                    # "regex": r"\d+.*?:\d+"
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 新民周刊
    {
        "platformName": "新民周刊",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.xinminweekly.com.cn/",
        # 首页头条新闻
        "headline_news": [],
        # 轮播信息
        "banner_news": ['//*[@id="content01"]/div[2]/div/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="content01"]/div[1]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="logo_menu"]/div[2]/ul/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//*[@id="pege_content2"]/div[2]/div/h1/text()'},
                # {"xpath": '/html/body/div[3]/div[3]/h1/text()', },
                # {"xpath": '//h2[@class="dabiao7 ma"]/text()', },
                # {"xpath": "/html/body/div[3]/div[1]/div[2]/h1/text()", },
            ],
            "content": [
                {"xpath": '//*[@id="ctrlfscont"]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="pege_content2"]/div[2]/div/div[1]/text()',
                 "regex": r"来源.*?[: ：].*?(.*)\s"
                 }

            ],
            "pubTime": [
                {
                    "xpath": '//*[@id="pege_content2"]/div[2]/div/div[1]/text()',
                    "regex": r"日期[: ：](\d+.*\d+)"
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 新民晚报
    {
        "platformName": "新民晚报",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.xinmin.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[5]/div/div[1]/div[4]/div[2]/div[1]/div[1]/div/div/a[1]'],
        # 轮播信息
        "banner_news": ['//*[@id="SiderBarBcroll2_slidexinminpic"]/div/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[5]/div/div[1]/div[1]/div[2]/div/div//h1/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="MainNav"]/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[5]/div/div[1]/div[2]/h1/text()'},
                {"xpath": '/html/body/div[3]/div[1]/div[2]/h1/text()', },
                {"xpath": '/html/body/div[3]/div[1]/div[1]/h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[5]/div/div[1]/div[2]/div[2]', },
                {"xpath": '/html/body/div[3]/div[1]/div[2]/div[3]', },
                {"xpath": '/html/body/div[3]/div[1]/div[1]/div[3]', },
            ],

            "pubSource": [
                {"xpath": '/html/body/div[5]/div/div[1]/div[2]/div[1]/span[1]/a/text()',
                 # "regex":  r"来源.*?[: ：].*?(.*)\s"
                 }

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[5]/div/div[1]/div[2]/div[1]/span[3]/text()',
                    # "regex": r"日期[: ：](\d+.*\d+)"
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆市政府网
    {
        "platformName": "重庆市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cq.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//*[@id="gwyinfo"]/li/a'],
        # 轮播信息
        "banner_news": ['/html/body/div[2]/div[1]/div[1]/div[1]/ul[1]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[2]/div[1]/div[1]/div[2]/div[2]/ul[2]/li/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[2]/div[1]/div[1]/div[2]/div[1]/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\w+/\d+/.*?.html",
            r"https?://[\w\-\.]+/\w+/\w+/\d+/.*?.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()'},
                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                # {"xpath": '/html/body/div[3]/div[1]/div[1]/h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]', },
                # {"xpath": '/html/body/div[3]/div[1]/div[2]/div[3]', },
                # {"xpath": '/html/body/div[3]/div[1]/div[1]/div[3]', },
            ],

            "pubSource": [
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                 "regex": r"来源[: ：](.*)"
                 }

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                    "regex": r"时间[: ：](\d+.*\d+)"
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 七一网
    {
        "platformName": "七一网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.12371.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//*[@id="content"]/ul[2]/ul[5]/li[1]/a'],
        # 轮播信息
        "banner_news": ['//*[@id="focusNews"]/div[1]/ul/li/div/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="content"]/ul[2]/div[3]/ul/li//a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="liID114"]//h4/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+.aspx",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/.*?.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//*[@id="detailBox"]/div[2]/div/h2/text()'},
                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                # {"xpath": '/html/body/div[3]/div[1]/div[1]/h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="detailBox"]/div[2]/div/div[2]', },
                # {"xpath": '/html/body/div[3]/div[1]/div[2]/div[3]', },
                # {"xpath": '/html/body/div[3]/div[1]/div[1]/div[3]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="detailBox"]/div[2]/div/div[1]/span[1]/text()',
                 "regex": r"来源[: ：](.*)"
                 }

            ],
            "pubTime": [
                {
                    "xpath": '//*[@id="detailBox"]/div[2]/div/div[1]/span[3]/text()',
                    "regex": r"时间[: ：](\d+.*\d+)"
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 阳光重庆
    {
        "platformName": "阳光重庆",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.ygcq.com.cn/",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": [''],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[2]/div[1]/div//h1/a'],
        # 导航信息
        "channel_info_xpath": [''],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\w+_\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/.*?.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[5]/div[1]/text()'},
                {"xpath": '//*[@id="activity-name"]/text()', },
                # {"xpath": '/html/body/div[3]/div[1]/div[1]/h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[5]/div[2]', },
                {"xpath": '//*[@id="js_content"]/section[1]', },
                # {"xpath": '/html/body/div[3]/div[1]/div[1]/div[3]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="js_name"]/text()',
                 # "regex":  r"(.*？)\s"
                 },
                {"xpath": '/html/body/div[5]/div[1]/span/text()',
                 "regex": r"(\w+)\s"},

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[5]/div[1]/span/text()',
                    "regex": r"时间[: ：](\d+年\d+月d+日)"
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆新闻社1
    {
        "platformName": "重庆新闻社",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cqxws.com/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[5]/div[2]/ul/li/a'],
        # 轮播信息
        "banner_news": ['/html/body/div[3]/div[1]/div/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[3]/div[2]/div/dl/dd/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="nav"]/ul/li/p/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\d+/\d+.html",
            r"https?://[\w\-\.]+/\w+/\w+/\d+.html",
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[3]/div[2]/div[1]/p[1]/text()'},
                # {"xpath": '//*[@id="activity-name"]/text()', },
                # {"xpath": '/html/body/div[3]/div[1]/div[1]/h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[3]/div[2]/div[2]', },
                # {"xpath": '//*[@id="js_content"]/section[1]', },
                # {"xpath": '/html/body/div[3]/div[1]/div[1]/div[3]', },
            ],

            "pubSource": [
                {"xpath": '/html/body/div[3]/div[2]/div[1]/p[2]/text()',
                 "regex": r"来源[:：](\w+)\s"},

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[3]/div[2]/div[1]/p[2]/text()',
                    "regex": r"时间[：:](\d+.*\d+)\s"
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 视界网
    {
        "platformName": "视界网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.cbg.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[2]/div[2]/div[1]/a'],
        # 轮播信息
        "banner_news": ['/html/body/div[2]/div[2]/dl/dd/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[2]/div[2]/div[2]/div/div/dl/dd/div[2]/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[2]/div[1]/div/div[1]/ul[1]/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+-\d+.html",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+.html",
            # r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/section[1]/div[1]/article/div[1]/h1/text()'},
                {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[2]/text()/text()', },
                {"xpath": '/html/body/div[3]/div/div[2]/h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/section[1]/div[1]/article/div[7]', },
                {"xpath": '//*[@id="detail"]', },
                {"xpath": '//*[@id="J_video_player"]', },
            ],

            "pubSource": [
                {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[2]/span/text()',
                 },
                {"xpath": '/html/body/section[1]/div[1]/article/div[2]/span[2]/text()',
                 "regex": r"来源[:：](\w+)"},

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/section[1]/div[1]/article/div[2]/span[1]/text()',
                    "regex": r"时间[：:](\d+.*\d+)"
                }, {
                    "xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[1]/span/text()',
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 华龙网
    {
        "platformName": "华龙网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cqnews.net/",
        # 首页头条新闻
        "headline_news": ['//*[@id="pc_toutiao1"]/a'],
        # 轮播信息
        "banner_news": ['//*[@id="pc_jdtp"]/div/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="pc_toutiao2"]/li/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="BtBody"]/div[4]/div[2]/ul/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.html",
            r"https?://[\w\-\.]+/\w+/\w+/\d+-\d+/\d+/\w+_\d+.html",
            # r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '//div[@class="sp_box"]/h2/text()', },
                # {"xpath": '//h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="main_text"]', },
                {"xpath": '//*[@id="_cont"]', },
                {"xpath": '/html/body/div[5]/div[2]/div[1]/div[4]', },
            ],

            "pubSource": [
                {"xpath": '//div[@class="sousuo2_lwz"]/a/text()',
                 },
                {"xpath": '//div[@class="pl"]/span[2]//text()',
                 "regex": r"来源.*?>(.*?)</a>"
                 },
                {"xpath": '//div[@class="pl"]/span[2]/text()',
                 "regex": r"来源.*?= '(.*?)'"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '//div[@class="pl"]/span[1]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
            ],
            "authors": [],
            "summary": [],
        }
    },

    # 1/15
    # 三峡传媒网
    {
        "platformName": "三峡传媒网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.sxcm.net/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[10]/div/div[2]/h1/a'],
        # 轮播信息
        "banner_news": ['/html/body/div[11]/div/div[1]/div[2]/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[11]/div/div[2]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[3]/div/div/ul/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/.*\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+-\d+/\d+/\w+_\d+.html",
            # r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[2]/div[2]/div[1]/div[4]/text()'},
                # {"xpath": '//div[@class="sp_box"]/h2/text()', },
                # {"xpath": '//h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="zoom main_text"]', },
                # {"xpath": '//*[@id="_cont"]', },
                # {"xpath": '/html/body/div[5]/div[2]/div[1]/div[4]', },
            ],

            "pubSource": [
                # {"xpath": '//div[@class="sousuo2_lwz"]/a/text()',
                #  },
                {"xpath": '/html/body/div[2]/div[2]/div[1]/div[7]/div[2]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                # {"xpath": '//div[@class="pl"]/span[2]/text()',
                #  "regex": r"来源.*?= '(.*?)'"
                #  },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[2]/div[2]/div[1]/div[7]/div[1]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆渝中政府网
    {
        "platformName": "重庆市渝中区政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cqyz.gov.cn/",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": ['/html/body/div[2]/div[1]/div[2]/div[1]/div[1]/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[2]/div[1]/div[2]/div[2]/div/div[1]/div/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+_\d+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[2]/div/div/div[1]/p/text()'},
                {"xpath": '//h1/text()', },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[2]/div/div/div[2]', },
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]', },
            ],

            "pubSource": [

                {"xpath": '/html/body/div[2]/div/div/div[1]/div/span[4]/text()',
                 # "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[2]/div/div/div[1]/div/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                }, {
                    "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                    "regex": r"时间[：:](\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 涪陵网
    {
        "platformName": "涪陵网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.fulingwx.com/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[4]/div[2]/div[2]/ul/li[2]/a'],
        # 轮播信息
        "banner_news": ['/html/body/div[4]/div[2]/div[2]/div[1]/div/div/div/ul[1]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="incon"]/ul[1]/li/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[2]/ul/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+-\d+-\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[4]/div[2]/div[1]/div[1]/p[1]/text()'},
                # {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[4]/div[2]/div[1]/div[1]/div', },
                # {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]', },
            ],

            "pubSource": [

                # {"xpath": '/html/body/div[2]/div/div/div[1]/div/span[4]/text()',
                #  # "regex": r"来源[:：](.*)"
                #  },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },
                {"xpath": '/html/body/div[4]/div[2]/div[1]/div[1]/p[2]/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                # {
                #     "xpath": '/html/body/div[2]/div/div/div[1]/div/span[2]/text()',
                #     # "regex": r"时间[：:](\d+.*\d+)"
                # },
                # {
                #     "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #     # "regex": r"时间[：:](\d+.*\d+)"
                # },
                {
                    "xpath": '/html/body/div[4]/div[2]/div[1]/div[1]/p[2]/text()',
                    "regex": r"(\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆市涪陵区政府网
    {
        "platformName": "重庆市涪陵区政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.fl.gov.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div/div[3]/div/div[2]/div/a'],
        # 轮播信息
        "banner_news": ['/html/body/div/div[3]/div/div[3]/div[1]/div/div[1]/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="gwyinfo"]/li/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div/div[3]/div/div[5]/div[1]/h3/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            r"https?://[\w\-\.]+/\w+_\d+/\w+/\d+/\w\d+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[3]/div/div/div/div[1]/p/text()'},
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '/html/body/div[3]/div/div/div/div[2]', },
                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]', },
            ],

            "pubSource": [

                {"xpath": '/html/body/div[3]/div/div/div/div[1]/div/span[4]/text()',
                 #  # "regex": r"来源[:：](.*)"
                 },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[3]/div/div/div/div[1]/div/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                # {
                #     "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #     # "regex": r"时间[：:](\d+.*\d+)"
                # },
                {
                    "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                    "regex": r"(\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 大渡口网
    {
        "platformName": "大渡口网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.ddknews.gov.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[8]/div[2]/div[2]/div[1]/div[1]/ul/li[1]/h1/a'],
        # 轮播信息
        "banner_news": ['/html/body/div[8]/div[2]/div[1]/div[1]/div[2]/ul/li/div[2]/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[8]/div[2]/div[2]/div[1]/div[2]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['//div[@class="bgbox2"]/div//div[@class="rink"]/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+.htm",
            r"https?://[\w\-\.]+/\w+_\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[3]/div/div/div[2]/text()'},
                {"xpath": '//*[@id="detail"]/div[1]/text()', },
                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[3]/div/div/div[4]', },
                {"xpath": '//*[@id="detail"]/div[4]', },
                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]', },
            ],

            "pubSource": [

                {"xpath": '//*[@id="detail"]/div[2]/span[1]/text()',
                 #  # "regex": r"来源[:：](.*)"
                 },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {
                    "xpath": '//*[@id="detail"]/div[2]/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                # {
                #     "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #     # "regex": r"时间[：:](\d+.*\d+)"
                # },
                {
                    "xpath": '/html/body/div[3]/div/div/div[3]/text()',
                    "regex": r"(\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆市大渡口区政府网
    {
        "platformName": "重庆市大渡口区政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.ddk.gov.cn/",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": ['//div[@class="fade-img"]/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['//div[@class="i1-w556-top"]/span/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+_\d+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]', },
                {"xpath": '/html/body/div[4]/div/div/div/div[2]/div[2]/div', },
            ],

            "pubSource": [

                {"xpath": '/html/body/div[4]/div/div/div/div[1]/div/span[4]/text()',
                 #  # "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[4]/div/div/div/div[1]/div/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                    "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                    "regex": r"(\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆市江北区政府网
    {
        "platformName": "重庆市江北区政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cqjb.gov.cn/",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": ['//div[@class="fade-img"]/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['//div[@class="i1-w556-top"]/span/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+_\d+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]', },
                {"xpath": '/html/body/div[4]/div/div/div/div[2]/div[2]/div', },
            ],

            "pubSource": [

                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="zwxl-bar"]/span[4]/text()',
                 #  # "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[4]/div/div/div/div[1]/div/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                    "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                    "regex": r"(\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 江北新闻网
    {
        "platformName": "江北新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://jbxww.cnnb.com.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/center/table[2]/tbody/tr/td/table[5]/tbody/tr/td/a'],
        # 轮播信息
        "banner_news": [''],
        # 轮播旁边新闻
        "banner_news_side": [
            '/html/body/center/table[2]//tr/td/table[7]//tr/td[3]/table//tr[1]/td/table//tr[2]/td/table//tr//a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/center/table[2]//tr/td/table[4]//tr/td[1]/table//tr/td[2]/span/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\d+.shtm",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//*[@id="Zoom"]/table[1]//tr[2]/td'},
                {"xpath": '/html/body/div[8]/div[1]/div/h1/text()', },
                {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[2]/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="Zoom"]/table[3]//tr[5]/td', },
                {"xpath": '/html/body/div[8]/div[1]/div/div[2]', },
                {"xpath": '//*[@id="detail"]', },
            ],

            "pubSource": [

                {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[2]/span/text()',
                 #  "regex": r"来源[:：](.*)"
                 },
                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },
                {"xpath": '//*[@id="Zoom"]/table[3]//tr[6]/td[1]/div/font[4]/text()',
                 #  # "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[8]/div[1]/div/p[2]/text()',
                    "regex": r"(\d+.*\d+)"
                },
                # {
                #     "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                #     "regex": r"时间[：:](\d+.*\d+)"
                # },
                {
                    "xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[1]/span/text()',
                    # "regex": r"(\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆市沙坪坝区政府网
    {
        "platformName": "重庆市沙坪坝区政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cqspb.gov.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[4]/div/div[1]/a'],
        # 轮播信息
        "banner_news": ['//*[@id="SmallPics"]/span/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[4]/div/div[3]/div[1]/div[1]/div/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                {"xpath": '/html/body/div[2]/div[1]/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]', },
                {"xpath": '/html/body/div[2]/div[3]/div[2]', },
            ],

            "pubSource": [

                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": 'string(//div[@class="infobar"])',
                 "regex": r"来源[:：](.*)<"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                    "regex": r"时间[：:](\d.*\d)"
                },
                {
                    "xpath": 'string(//div[@class="infobar"])',
                    "regex": r"日期[：:](\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 全搜九龙网
    {
        "platformName": "全搜九龙网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cqjlp.com.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[4]/div[1]/div/ul/li/a'],
        # 轮播信息
        "banner_news": ['/html/body/div[5]/div[1]/div[2]/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[5]/div[2]/div[3]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[3]/div/ul/li[3]/ul/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+.shtm",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                # {"xpath": '/html/body/div[2]/div[1]/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[7]/article', },
                {"xpath": '/html/body/div[7]/div[3]', },
                # {"xpath": '/html/body/div[2]/div[3]/div[2]', },
            ],

            "pubSource": [

                {"xpath": '/html/body/div[7]/article/div[1]/a/text()',
                 # "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[7]/div[3]/div[1]/div/span[1]/i/text()',
                 "regex": r"来源[:：](.*?)\d"
                 },
                # {"xpath": 'string(//div[@class="infobar"])',
                #   "regex": r"来源[:：](.*)<"
                #  },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[7]/article/div[1]/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                    "regex": r"(\d.*\d)"
                },
                # {
                # "xpath": 'string(//div[@class="infobar"])',
                # "regex": r"日期[：:](\d+.*\d+)"
                # }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 南岸网
    {
        "platformName": "南岸网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cqna.com.cn/",
        # 首页头条新闻
        "headline_news": ['//*[@id="headLine"]/a'],
        # 轮播信息
        "banner_news": ['//*[@id="slideBoxPic"]/div[1]/div/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['//*[@id="swtTitle"]/ul/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+_\w+\d+/\d+-\d+/\d+/\w+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\w+/\d+-\d+/\d+/\w_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\d+/\d+",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                # {"xpath": '/html/body/div[4]/div[1]/div[1]/text()', },
                {"xpath": '//div[@class="newsTitle cl"]/text()', },
                {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[2]/text()', },
            ],
            "content": [
                {"xpath": '//div[@class="content fl mt20"]', },
                {"xpath": '//*[@id="app"]/div[1]/div[3]/div[1]', },
                {"xpath": '//*[@id="detail"]', },
            ],

            "pubSource": [

                {"xpath": '//*[@id="newsSources"]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//*[@id="app"]/div[1]/div[2]/div/div/span[1]/text()',
                 # "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[2]/span/text()',
                 # "regex": r"来源[:：](.*)<"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '//*[@id="newsDate"]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '//*[@id="app"]/div[1]/div[2]/div/div/span[3]/text()',
                    # "regex": r"时间[：:](\d.*\d)"
                },
                {
                    "xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[1]/span/text()',
                    # "regex": r"日期[：:](\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆市南岸区政府网
    {
        "platformName": "重庆市南岸区政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cqna.gov.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[3]/div[1]/div/div[1]/div/div/h1/a'],
        # 轮播信息
        "banner_news": ['/html/body/div[3]/div[1]/div/div[2]/div[1]/ul[1]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[3]/div[1]/div/div[2]/div[2]/div[1]/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+_\d+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
                {"xpath": '/html/body/div[3]/div/div/div/div[1]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]', },
                {"xpath": '/html/body/div[4]/div/div/div/div[2]/div[2]/div', },
                {"xpath": '/html/body/div[3]/div/div/div/div[2]', },
            ],

            "pubSource": [

                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="zwxl-bar"]/span[4]/text()',
                 #  # "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[4]/div/div/div/div[1]/div/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[3]/div/div/div/div[1]/div/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                    "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                    "regex": r"(\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆市北碚区政府网
    {
        "platformName": "重庆市北碚区政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.beibei.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//div[@class="index-headline-tab"]/div/h1/a'],
        # 轮播信息
        "banner_news": ['/html/body/div[3]/div[1]/div/div[2]/div[1]/ul[1]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[3]/div[1]/div/div[2]/div[2]/div[1]/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+_\d+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
                {"xpath": '/html/body/div[3]/div/div/div/div[1]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]', },
                {"xpath": '/html/body/div[4]/div/div/div/div[2]/div[2]/div', },
                {"xpath": '/html/body/div[3]/div/div/div/div[2]', },
            ],

            "pubSource": [

                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="zwxl-bar"]/span[4]/text()',
                 #  # "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[4]/div/div/div/div[1]/div/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[3]/div/div/div/div[1]/div/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                    "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                    "regex": r"(\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆市北碚长安网
    {
        "platformName": "重庆市北碚长安网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://caw.beibei.gov.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[2]/div[1]/div[2]/a/div[1]'],
        # 轮播信息
        "banner_news": ['/html/body/div[2]/div[3]/div[2]/div[1]/div/div/div/div/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[1]/div[3]/div[1]/ul/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+-\d+-\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[2]/div[1]/div[2]/div[2]/div/div[1]/div/text()'},
                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="news_conent_two_text"]', },
                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[2]/div[2]/div', },
                # {"xpath": '/html/body/div[3]/div/div/div/div[2]', },
            ],

            "pubSource": [

                {"xpath": '/html/body/div[2]/div[1]/div[2]/div[2]/div/div[3]/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },

                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },
                # {"xpath": '//div[@class="zwxl-bar"]/span[4]/text()',
                # "regex": r"来源[:：](.*)"
                # },
                #
            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[2]/div[1]/div[2]/div[2]/div/div[3]/span[4]/text()',
                    "regex": r"日期[：:](\d+.*\d+)"
                },
                # {
                #     "xpath": '/html/body/div[3]/div/div/div/div[1]/div/span[2]/text()',
                #     "regex": r"时间[：:](\d+.*\d+)"
                # },
                # {
                #     "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                #     "regex": r"时间[：:](\d+.*\d+)"
                # },
                # {
                #     "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #     "regex": r"(\d+.*\d+)"
                # }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆綦江网
    {
        "platformName": "重庆綦江网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.cqqjnews.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[3]/div[9]/div[1]/a'],
        # 轮播信息
        "banner_news": ['/html/body/div[4]/div[1]/div/div/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[6]/div[1]/div[1]/div/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="top_menu_2"]/ul/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+_\w+/.*?/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/table[2]//tr[2]/td[1]/table[1]//tr[2]/td/div[1]/strong/text()'},
                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
            ],
            "content": [
                {"xpath": '/html/body/table[2]//tr[2]/td[1]/table[1]//tr[2]/td', },
                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[2]/div[2]/div', },
                # {"xpath": '/html/body/div[3]/div/div/div/div[2]', },
            ],

            "pubSource": [

                {"xpath": '/html/body/table[2]//tr[2]/td[1]/table[1]//tr[2]/td/div[2]/text()',
                 "regex": r"来源[:：](.*?)编辑"
                 },

                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },
                # {"xpath": '//div[@class="zwxl-bar"]/span[4]/text()',
                # "regex": r"来源[:：](.*)"
                # },
                #
            ],
            "pubTime": [
                {
                    "xpath": '/html/body/table[2]//tr[2]/td[1]/table[1]//tr[2]/td/div[2]/text()',
                    "regex": r"(\d+.*\d+)"
                },
                # {
                #     "xpath": '/html/body/div[3]/div/div/div/div[1]/div/span[2]/text()',
                #     "regex": r"时间[：:](\d+.*\d+)"
                # },
                # {
                #     "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                #     "regex": r"时间[：:](\d+.*\d+)"
                # },
                # {
                #     "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #     "regex": r"(\d+.*\d+)"
                # }
            ],
            "authors": [],
            "summary": [],
        }
    },

    # 1/16 17 90
    # 重庆市綦江区政府网
    {
        "platformName": "重庆市綦江区政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cqqj.gov.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[3]/div[1]/div/div[1]/div/div/h1/a'],
        # 轮播信息
        "banner_news": ['/html/body/div[3]/div[1]/div/div[2]/div[1]/ul[1]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[3]/div[1]/div/div[2]/div[2]/div[1]/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+_\d+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
                {"xpath": '/html/body/div[3]/div/div/div/div[1]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]', },
                {"xpath": '/html/body/div[4]/div/div/div/div[2]/div[2]/div', },
                {"xpath": '/html/body/div[3]/div/div/div/div[2]', },
            ],

            "pubSource": [
                {"xpath": '/html/head/meta[@name="ContentSource"]/@content',
                 #  # "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[4]/div/div/div/div[1]/div/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[3]/div/div/div/div[1]/div/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                    "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                    "regex": r"(\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆市大足区政府网
    {
        "platformName": "重庆市大足区政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.dazu.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//div[@class="index-headline-item"]/h1/a'],
        # 轮播信息
        "banner_news": ['//div[@class="index-newspic"]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="tab-list-bool clearfix"]/li/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\w+_\d+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
                {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]', },
                {"xpath": '/html/body/div[4]/div/div/div/div[2]/div[2]/div', },
                {"xpath": '/html/body/div[2]/div/div/div[2]', },
            ],

            "pubSource": [
                {"xpath": '/html/head/meta[@name="ContentSource"]/@content',
                 #  # "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[2]/div/div/div[1]/div/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/head/meta[@name="PubDate"]/@content',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                    "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                    "regex": r"(\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 黔江广电传媒网
    {
        "platformName": "黔江广电传媒网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://cqjtv.com/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[4]/a'],
        # 轮播信息
        "banner_news": ['//*[@id="D1pic1"]/div/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[5]/div[2]/div[2]/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="nav"]/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/.*?&.*?&.*?&.*?&.*?id=\d+",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                # {"xpath": '/html/body/div[3]/div[1]/div[1]/text()'},
                {"xpath": '//h1/text()', },
                # {"xpath": '//*[@id="activity-name"]/text()', },
                # {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[5]/div[1]/div[2]', },
                {"xpath": '/html/body/div[5]/div[2]', },
                # {"xpath": '/html/body/section/div/div/div/div/div[1]/div[1]/div', },
                # {"xpath": '/html/body/div[1]/div[2]/div/div/div[2]', },
            ],

            "pubSource": [
                # {"xpath": '/html/body/div[3]/div[1]/div[2]/div[1]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },
                {"xpath": '/html/body/div[5]/div[1]/div[1]/span[1]/a/text()',
                 # "regex": r"来源[:：](.*)"
                 },

                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                # {
                # "xpath": '/html/body/div[3]/div[1]/div[2]/div[1]/text()',
                # "regex": r"(\d+.*\d+)"
                # },
                {
                    "xpath": '/html/body/div[5]/div[1]/div[1]/span[3]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },

                # {
                #     "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #     "regex": r"(\d+.*\d+)"
                # }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆市渝北区政府网1
    {
        "platformName": "重庆市渝北区政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.ybq.gov.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div/div[4]/div[1]/a'],
        # 轮播信息
        "banner_news": ['/html/body/div/div[4]/div[2]/div[1]/div[1]/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['/html/body/div/div[4]/div[2]/div[2]/div[1]/ul/li/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\w+_\d+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
                {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]', },
                {"xpath": '/html/body/div[4]/div/div/div/div[2]/div[2]/div', },
                {"xpath": '/html/body/div/div[4]/div[1]/div/div[2]/div[2]', },
            ],

            "pubSource": [
                {"xpath": '/html/head/meta[@name="ContentSource"]/@content',
                 #  # "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[2]/div/div/div[1]/div/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/head/meta[@name="PubDate"]/@content',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                    "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                    "regex": r"(\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 永川网
    {
        "platformName": "永川网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.ycw.gov.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[13]/div[2]/h1/a'],
        # 轮播信息
        "banner_news": ['/html/body/div[14]/div[1]/div/div/ul[1]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//div[@class="jdtnews"]//a'],
        # 导航信息
        "channel_info_xpath": ['//div[@class="center"]/div[@class="newslm"]/em/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[4]/div[1]/div[1]/text()', },
                {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[2]/text()', },
                # {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="detail"]', },
                {"xpath": '/html/body/section/div/div/div/div/div[1]', },
                {"xpath": '//*[@id="main"]/div[1]/div[2]/div', },
            ],

            "pubSource": [
                {"xpath": '/html/body/div[4]/div[1]/div[2]/div[1]/text()',
                 "regex": r"来源[:：](.*?)\d"
                 },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[2]/span/text()',
                # "regex": r"来源[:：](.*)"
                # },

                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[4]/div[1]/div[2]/div[1]/text()',
                    "regex": r"(\d+.*\d+)"
                },
                # {
                #     "xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[1]/span/text()',
                # "regex": r"时间[：:](\d+.*\d+)"
                # },

                # {
                #     "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #     "regex": r"(\d+.*\d+)"
                # }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆市巴南区政府网
    {
        "platformName": "重庆市巴南区政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cqbn.gov.cn/",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": ['/html/body/div/div[2]/div/div[1]/div[1]/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['/html/body/div/div[2]/div/div[2]/div[1]/ul/li/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\w+_\d+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
                {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]', },
                {"xpath": '/html/body/div[4]/div/div/div/div[2]/div[2]/div', },
                {"xpath": '/html/body/div[1]/div[2]/div/div/div[2]', },
            ],

            "pubSource": [
                {"xpath": '/html/head/meta[@name="ContentSource"]/@content',
                 #  # "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[2]/div/div/div[1]/div/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/head/meta[@name="PubDate"]/@content',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                    "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                    "regex": r"(\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 黔江新闻网1
    {
        "platformName": "黔江新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.wldsb.com/index.htm",
        # 首页头条新闻
        "headline_news": ['//div[@class="hotnewsm"]//h1/a'],
        # 轮播信息
        "banner_news": ['//div[@class="slideBox"]/div[@class="bd"]/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//div[@class="right"]/ol/li/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="n1"]/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\w+_\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[3]/div[1]/div[1]/text()'},
                {"xpath": '//h1/text()', },
                {"xpath": '//*[@id="activity-name"]/text()', },
                # {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="text_area"]', },
                {"xpath": '/html/body/section/div/div/div/div/div[1]/div[1]/div', },
                # {"xpath": '/html/body/div[1]/div[2]/div/div/div[2]', },
            ],

            "pubSource": [
                {"xpath": '/html/body/div[3]/div[1]/div[2]/div[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//*[@id="title_area"]/div/text()',
                 # "regex": r"来源[:：](.*)"
                 },

                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[3]/div[1]/div[2]/div[1]/text()',
                    "regex": r"(\d+.*\d+)"
                },
                {
                    "xpath": '//*[@id="title_area"]/div/span/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },

                # {
                #     "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #     "regex": r"(\d+.*\d+)"
                # }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆市长寿区政府网
    {
        "platformName": "重庆市长寿区政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cqcs.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//div[@class="index-headline-item"]/h1/a'],
        # 轮播信息
        "banner_news": ['//div[@class="index-newspic"]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="tab-list-bool clearfix"]/li/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\w+_\d+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
                {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[2]/div[2]/div', },
                {"xpath": '/html/body/div[1]/div[3]/div/div/div[2]/div[2]', },
            ],

            "pubSource": [
                {"xpath": '/html/head/meta[@name="ContentSource"]/@content',
                 #  # "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[2]/div/div/div[1]/div/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/head/meta[@name="PubDate"]/@content',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                    "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                    "regex": r"(\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 长寿新闻网 1
    {
        "platformName": "长寿新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.ccs.cn/index/",
        # 首页头条新闻
        "headline_news": ['//*[@id="titlenewspic"]/a'],
        # 轮播信息
        "banner_news": ['//*[@id="focusBox1197"]/dt[2]/ul/li/dd[1]/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="docs1"]/ol[1]/table//tr/td/div/div/ul/ul/li/div[1]/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="nav"]/ul/li[2]/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+-\d+/\d+_\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//*[@id="detail"]/div[1]/text()'},
                {"xpath": '//*[@id="newstitle"]/text()', },
                # {"xpath": '//*[@id="activity-name"]/text()', },
                # {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="docc"]//tr/td/table[3]//tr/td', },
                {"xpath": '//*[@id="detail"]/div[5]', },
                # {"xpath": '/html/body/section/div/div/div/div/div[1]/div[1]/div', },
                # {"xpath": '/html/body/div[1]/div[2]/div/div/div[2]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="detail"]/div[2]/span[1]/text()',
                 #  "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//*[@id="sitetitle"]/text()',
                 # "regex": r"来源[:：](.*)"
                 },

                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {
                    "xpath": '//*[@id="detail"]/div[2]/span[2]/text()',
                    # "regex": r"(\d+.*\d+)"
                },
                {
                    "xpath": '//*[@id="newsdate"]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },

                # {
                #     "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #     "regex": r"(\d+.*\d+)"
                # }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆市江津区政府网
    {
        "platformName": "重庆市江津区政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.jiangjin.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//div[@class="i1-news-cont"]/a'],
        # 轮播信息
        "banner_news": ['//div[@class="fade-img"]/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['//div[@class="i1-w556-top"]/span/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\w+_\d+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
                {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[2]/div[2]/div', },
                {"xpath": '/html/body/div[3]/div/div/div[2]/div[2]', },
            ],

            "pubSource": [
                {"xpath": '/html/head/meta[@name="ContentSource"]/@content',
                 #  # "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[2]/div/div/div[1]/div/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/head/meta[@name="PubDate"]/@content',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                    "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                    "regex": r"(\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 江津网
    {
        "platformName": "江津网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cqjjnet.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="toutiao"]/a'],
        # 轮播信息
        "banner_news": ['//*[@id="myfocus"]/div[1]/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div/div[8]/div[9]/div[4]//a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="meun"]//a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[2]/text()', },
                # {"xpath": '//*[@id="activity-name"]/text()', },
                # {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[6]/div[2]/div[1]/div[3]', },
                {"xpath": '//*[@id="text_area"]', },
                {"xpath": '/html/body/div[6]/div[2]/div[4]/div/div[2]', },
                # {"xpath": '/html/body/div[1]/div[2]/div/div/div[2]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="source"]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[2]/span/text()',
                 # "regex": r"来源[:：](.*)"
                 },

                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {
                    "xpath": '//*[@id="source"]/text()',
                    "regex": r"(\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[1]/span/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },

                # {
                #     "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #     "regex": r"(\d+.*\d+)"
                # }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆市永川区政府网
    {
        "platformName": "重庆市永川区政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://yc.cq.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//div[@class="main_info"]/a'],
        # 轮播信息
        "banner_news": ['//div[@class="fade-img"]/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="tab-list-bool clearfix"]/li/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\w+_\d+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
                {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[2]/div[2]/div', },
                {"xpath": '/html/body/div[1]/div[2]/div/div/div[2]', },
            ],

            "pubSource": [
                {"xpath": '/html/head/meta[@name="ContentSource"]/@content',
                 #  # "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[2]/div/div/div[1]/div/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/head/meta[@name="PubDate"]/@content',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                    "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                    "regex": r"(\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 今日合川
    {
        "platformName": "今日合川",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.jrhcw.com/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[2]/div[1]/div[1]/div/div[4]/div/div[1]/h1/a'],
        # 轮播信息
        "banner_news": ['//ul[@class="pgwSlider"]//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//div[@class="zw"]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['//div[@class="hcxw"]/div/a[1]'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[7]/div[3]/div[1]/h1/text()', },
                {"xpath": '//*[@id="activity-name"]/text()', },
                # {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[2]/div[1]/div[6]', },
                {"xpath": '/html/body/div[7]/div[3]/div[1]', },
                {"xpath": '//*[@id="js_content"]', },
                # {"xpath": '/html/body/div[1]/div[2]/div/div/div[2]', },
            ],

            "pubSource": [
                {"xpath": '/html/body/div[2]/div[1]/div[4]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[2]/span/text()',
                # "regex": r"来源[:：](.*)"
                # },

                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[2]/div[1]/div[4]/text()',
                    "regex": r"(\d+.*\d+)"
                },
                # {
                #     "xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[1]/span/text()',
                # "regex": r"时间[：:](\d+.*\d+)"
                # },

                # {
                #     "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #     "regex": r"(\d+.*\d+)"
                # }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 永川新闻网1
    {
        "platformName": "永川新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://news.yongchuan.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[5]/div[2]/div[1]/h2/a'],
        # 轮播信息
        "banner_news": [''],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[5]/div[2]/div[2]/div[1]/ul/li//a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[4]/div/div/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/newsshow-\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[7]/div[3]/div[1]/h1/text()', },
                {"xpath": '//*[@id="detail"]/div[1]/text()', },
                # {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//div[@class="conter_show"]', },
                {"xpath": '/html/body/div[7]/div[3]/div[1]', },
                {"xpath": '//*[@id="detail"]/div[4]', },
                # {"xpath": '//*[@id="main"]/div[1]/div[2]/div', },
            ],

            "pubSource": [
                # {"xpath": '/html/body/div[4]/div[1]/div[2]/div[1]/text()',
                #  "regex": r"来源[:：](.*?)\d"
                #  },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[2]/span/text()',
                # "regex": r"来源[:：](.*)"
                # },

                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {
                    "xpath": '//div[@class="Title_h1"]/div/text()',
                    "regex": r"(\d+.*\d+)"
                },
                # {
                #     "xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[1]/span/text()',
                # "regex": r"时间[：:](\d+.*\d+)"
                # },

                # {
                #     "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #     "regex": r"(\d+.*\d+)"
                # }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 南川网1
    {
        "platformName": "南川网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cqncnews.com/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[4]/div[6]/div[2]/div/a'],
        # 轮播信息
        "banner_news": ['//*[@id="select_btn"]/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[4]/div[8]/div[2]/div/li/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[3]/ul/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/\w+_\d+/\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[4]/div[5]/div[1]/div[1]/div/span/text()'},
                {"xpath": '//h1/text()', },
                {"xpath": '/html/body/div[4]/div[2]/div[3]/h1/span[1]/text()', },
                # {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[4]/div[5]/div[1]/div[2]/div', },
                {"xpath": '//*[@id="Area"]/div[6]/div/div[6]', },
                {"xpath": '//*[@id="text_area"]', },
                {"xpath": '//*[@id="detail"]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="source_baidu"]/a/text()',
                 # "regex": r"来源[:：](.*?)\d"
                 },
                {"xpath": '//*[@id="title_area"]/div/text()',
                 # "regex": r"来源[:：](.*)"
                 },

                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[4]/div[5]/div[1]/div[1]/span/text()',
                    "regex": r"(\d+.*\d+)\s"
                },
                {
                    "xpath": '//*[@id="pubtime_baidu"]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },

                {
                    "xpath": '//*[@id="title_area"]/div/span/text()',
                    "regex": r"(\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆市南川区政府网
    {
        "platformName": "重庆市南川区政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cqnc.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//div[@class="index-headline-item"]/h1/a'],
        # 轮播信息
        "banner_news": ['//div[@class="index-newspic"]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="tab-list-bool clearfix"]/li/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\w+_\d+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
                {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[2]/div[2]/div', },
                {"xpath": '/html/body/div[1]/div[2]/div/div/div[2]', },
            ],

            "pubSource": [
                {"xpath": '/html/head/meta[@name="ContentSource"]/@content',
                 #  # "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[2]/div/div/div[1]/div/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/head/meta[@name="PubDate"]/@content',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                    "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                    "regex": r"(\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆市璧山区政府网
    {
        "platformName": "重庆市璧山区政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.bishan.gov.cn//",
        # 首页头条新闻
        "headline_news": ['//div[@class="index-headline-tab"]/div/h1/a'],
        # 轮播信息
        "banner_news": ['//div[@class="index-newspic"]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="tab-list-bool clearfix"]/li/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\w+_\d+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
                {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[2]/div[2]/div', },
                {"xpath": '/html/body/div[1]/div[2]/div/div/div[2]', },
            ],

            "pubSource": [
                {"xpath": '/html/head/meta[@name="ContentSource"]/@content',
                 #  # "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[2]/div/div/div[1]/div/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/head/meta[@name="PubDate"]/@content',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                    "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                    "regex": r"(\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },

    # 1/18
    # 璧山网
    {
        "platformName": "璧山网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.bswxw.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="tt_big_word"]/a'],
        # 轮播信息
        "banner_news": ['//*[@id="focusNews"]/div[1]/div/ul/li/div[@class="pic"]/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div/table[7]//tr/td[3]/table//tr/td[1]/table//tr[2]/td/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\w+/\w+_\d+",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//td[@class="bleak2"]/text()'},
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
                # {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div/table[11]//tr/td[1]/table[4]//tr/td/font/div', },
                {"xpath": '/html/body/div[7]/div[3]', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[2]/div[2]/div', },
                # {"xpath": '/html/body/div[1]/div[2]/div/div/div[2]', },
            ],

            "pubSource": [
                {"xpath": '/html/body/div[7]/div[3]/div[1]/div/span[1]/i/text()',
                 "regex": r"来源[:：](.*)\d"
                 },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div/table[11]//tr/td[1]/table[2]//tr/td/text()',
                    "regex": r"(\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[7]/div[3]/div[1]/div/span[1]/i/text()',
                    "regex": r"(\d+.*\d+)"
                },
                # {
                #     "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                #     "regex": r"时间[：:](\d+.*\d+)"
                # }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 铜梁网
    {
        "platformName": "铜梁网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://113.207.122.7/",
        # 首页头条新闻
        "headline_news": ['//*[@id="BannerZoneAD_Div31"]/a'],
        # 轮播信息
        "banner_news": ['//*[@id="slideBox3"]/div[2]/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[6]/div[7]/div[1]/div[2]//a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[5]/div/ul/li[1]//a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\d\-\.]+/\w+/.*?ArticleID=\d+",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//*[@id="N_left"]/div[1]//text()'},
                {"xpath": '//h1/text()', },
                {"xpath": '//*[@id="activity-name"]/text()', },
                # {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="zoom"]', },
                {"xpath": '/html/body/section/div[2]', },
                {"xpath": '//*[@id="js_content"]', },
                # {"xpath": '/html/body/div[1]/div[2]/div/div/div[2]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="N_left"]/div[2]/ul/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/section/div[2]/div[1]/div/text()',
                 "regex": r"来源[:：](.*)\s"
                 },

                {"xpath": '//*[@id="profileBt"]//text()',
                 # "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '//*[@id="N_left"]/div[2]/ul/text()',
                    "regex": r"(\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/section/div[2]/div[1]/div/span/text()',
                    #     "regex": r"(\d+.*\d+)"
                },
                {
                    "xpath": '//*[@id="publish_time"]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 铜梁市政府网
    {
        "platformName": "重庆市铜梁区政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.cqstl.gov.cn//",
        # 首页头条新闻
        "headline_news": ['//div[@class="main_info underlines"]/a'],
        # 轮播信息
        "banner_news": ['//div[@class="fade-img"]/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="tab-list-bool clearfix"]/li/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\w+_\d+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
                {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[2]/div[2]/div', },
                {"xpath": '/html/body/div[1]/div[3]/div/div/div[2]', },
            ],

            "pubSource": [
                {"xpath": '/html/head/meta[@name="ContentSource"]/@content',
                 #  # "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[2]/div/div/div[1]/div/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/head/meta[@name="PubDate"]/@content',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                    "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                    "regex": r"(\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 潼南网
    {
        "platformName": "潼南网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cqtn.com/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[2]/div[14]/table//tr/td[1]/table//tr/td/table//tr/td[2]/table//tr[1]/td/a'],
        # 轮播信息
        "banner_news": ['//*[@id="Focus_01"]/div/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[2]/div[17]/table//tr/td/table//tr/td[1]/table//tr[4]/td/a'],
        # 导航信息
        "channel_info_xpath": ['//td[@class="zitt06"]/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//*[@id="MainBody"]/div[2]/div[1]/div[1]/h1/text()'},
                {"xpath": '//td[@class="p04 t06"]/text()', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
                # {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//td[@class="p04 t01"]', },
                {"xpath": '//*[@id="MainBody"]/div[2]/div[1]', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[2]/div[2]/div', },
                # {"xpath": '/html/body/div[1]/div[2]/div/div/div[2]', },
            ],

            "pubSource": [
                # {"xpath": '/html/head/meta[@name="ContentSource"]/@content',
                #  #  # "regex": r"来源[:：](.*)"
                #  },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

                {"xpath": 'string(/html/body/table[1]//tr[3]/td/table//tr/td/table//tr[2]/td/table//tr/td[1])',
                 "regex": r"\d+.*?([\u4E00-\u9FA5]+)"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/table[1]//tr[3]/td/table//tr/td/table//tr[2]/td/table//tr/td[1]/text()',
                    "regex": r"(\d+.*\d+)"
                },
                # {
                #     "xpath": '/html/head/meta[@name="PubDate"]/@content',
                #     # "regex": r"时间[：:](\d+.*\d+)"
                # },
                # {
                #     "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                #     "regex": r"时间[：:](\d+.*\d+)"
                # },
                # {
                #     "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #     "regex": r"(\d+.*\d+)"
                # }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆市潼南区政府网
    {
        "platformName": "重庆市潼南区政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cqtn.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//div[@class="index-headline-item"]//a'],
        # 轮播信息
        "banner_news": ['//div[@class="index-newspic"]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="tab-list-bool clearfix"]/li/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\w+_\d+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
                {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[2]/div[2]/div', },
                {"xpath": '/html/body/div[1]/div[3]/div/div/div[2]', },
            ],

            "pubSource": [
                {"xpath": '/html/head/meta[@name="ContentSource"]/@content',
                 #  # "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[2]/div/div/div[1]/div/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/head/meta[@name="PubDate"]/@content',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                    "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                    "regex": r"(\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆晚报
    {
        "platformName": "重庆晚报",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.cqwb.com.cn/",
        # 首页头条新闻
        "headline_news": ['//*[@id="title1"]/div[1]/a'],
        # 轮播信息
        "banner_news": [''],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="dataload"]/li//a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="header"]/div/div/ul/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/.*\d+.htm",
            r"https?://[\w\-\.]+/\d+/\d+/\d+/\w+\d+.shtml",
            r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[5]/div[2]/div[3]/h1/span[1]/text()'},
                # {"xpath": '/html/body/div[12]/div[1]/div[1]/h1/text()', },
                {"xpath": '//text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="detail"]', },
                {"xpath": '/html/body/div[12]/div[1]/div[1]', },
                {"xpath": '//*[@id="article_inbox"]/div[6]', },
                {"xpath": '//*[@id="cont"]', },
                {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '/html/body/div[5]/div[2]/div[2]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//*[@id="c_left"]/div[3]/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '/html/body/div[12]/div[1]/div[1]/div/span[1]',
                 "regex": r"\d+.*\d+"
                 },
                {"xpath": '//*[@id="c_left"]/div[3]',
                 "regex": r"\d+.*\d+"
                 },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 巴渝传媒网
    {
        "platformName": "巴渝传媒网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.bycmw.com/",
        # 首页头条新闻
        "headline_news": ['//div[@class="to"]/h1/a'],
        # 轮播信息
        "banner_news": ['//*[@id="KSS_content"]/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//ul[@class="alt"]/li/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[3]/ul[1]/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+-\d+.html",
            r"/\w+/\w+-\d+.html",
            # r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[2]/text()'},
                {"xpath": '/html/body/div[5]/div/div[2]/h3', },
                {"xpath": '//h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//div[@class="conter_show"]', },
                {"xpath": '/html/body/div[7]', },
                # {"xpath": '/html/body/div[5]/div[2]/div[1]/div[4]', },
            ],

            "pubSource": [
                {"xpath": '//div[@class="Title_h1"]/div/text()',
                 "regex": r"来源[:：](.*?)\d"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="Title_h1"]/div/text()',
                 "regex": r"(\d+.*\d+)"
                 },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆市荣昌区政府网
    {
        "platformName": "重庆市荣昌区政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.rongchang.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//div[@class="lb-tt-item"]/a'],
        # 轮播信息
        "banner_news": ['//div[@class="fade-img"]/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="tab-list-bool clearfix"]/li/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\w+_\d+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
                {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[2]', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[2]/div[2]/div', },
                {"xpath": '/html/body/div[1]/div[3]/div/div/div[2]', },
            ],

            "pubSource": [
                {"xpath": '/html/head/meta[@name="ContentSource"]/@content',
                 #  # "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[2]/div/div/div[1]/div/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/head/meta[@name="PubDate"]/@content',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                    "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                    "regex": r"(\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 荣昌新闻网
    {
        "platformName": "荣昌新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.cqrc.org.cn/",
        # 首页头条新闻
        "headline_news": ['//div[@class="big_headlines_box"]/a'],
        # 轮播信息
        "banner_news": ['//div[@class="swiper-wrapper"]/div/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//ul[@class="new_list_1_content"]/li/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="nav_ul"]/li/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[2]/div[3]/div/div[2]/text()', },
                {"xpath": '/html/body/div[7]/div[3]/div[1]/h1/text()', },
                # {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//div[@class="l02"]', },
                {"xpath": '/html/body/div[7]/div[3]/div[1]', },
                {"xpath": '//*[@id="text_area"]', },
                # {"xpath": '/html/body/div[1]/div[3]/div/div/div[2]', },
            ],

            "pubSource": [
                # {"xpath": '/html/head/meta[@name="ContentSource"]/@content',
                #  # "regex": r"来源[:：](.*)"
                # },
                {"xpath": '/html/body/div[7]/div[3]/div[1]/div/span[1]/i/text()',
                 "regex": r"来源[:：](.*?)\d"
                 },

                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                # {
                #     "xpath": '/html/body/div[2]/div/div/div[1]/div/span[2]/text()',
                # "regex": r"时间[：:](\d+.*\d+)"
                # },
                {
                    "xpath": '/html/body/div[7]/div[3]/div[1]/div/span[1]/i/text()',
                    "regex": r"(\d+.*\d+)"
                },
                {
                    "xpath": '//div[@class="t"]/text()',
                    "regex": r"(\d+.*\d+)"
                },
                # {
                # "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                # "regex": r"(\d+.*\d+)"
                # }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 开州之窗
    {
        "platformName": "开州之窗",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.kxzc.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[3]/div[10]/div[1]/a'],
        # 轮播信息
        "banner_news": ['//*[@id="section-focus-pic"]/div[1]/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[3]/div[11]/div[2]/div[2]//a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[2]/div/div[4]/div/div/ul/li/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\d+/\d+/\d+.shtm",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[3]/div[2]/div[2]/div[1]/text()'},
                {"xpath": '/html/body/div[5]/div[3]/div[3]/div[1]/text()', },
                {"xpath": '//h1/text()', },
                # {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[3]/div[2]/div[2]/article', },
                {"xpath": '/html/body/div[5]/article', },
                {"xpath": '//*[@id="text_area"]', },
                # {"xpath": '/html/body/div[1]/div[3]/div/div/div[2]', },
            ],

            "pubSource": [
                # {"xpath": '/html/head/meta[@name="ContentSource"]/@content',
                #  # "regex": r"来源[:：](.*)"
                # },
                {"xpath": '/html/body/div[3]/div[2]/div[2]/div[2]/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },

                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                # {
                #     "xpath": '/html/body/div[2]/div/div/div[1]/div/span[2]/text()',
                # "regex": r"时间[：:](\d+.*\d+)"
                # },
                {
                    "xpath": '/html/body/div[3]/div[2]/div[2]/div[2]/text()',
                    # "regex": r"(\d+.*\d+)"
                },
                # {
                #     "xpath": '//div[@class="t"]/text()',
                #     "regex": r"(\d+.*\d+)"
                # },
                # {
                # "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                # "regex": r"(\d+.*\d+)"
                # }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 重庆市两江新区政府网
    {
        "platformName": "重庆市两江新区政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.liangjiang.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//div[@class="toutiao"]/a'],
        # 轮播信息
        "banner_news": ['//ul[@class="pic"]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//div[@class="news"]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['//div[@class="menu"]/ul/li[1]/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[5]/div[1]/div[1]/text()'},
                # {"xpath": '/html/body/div[5]/div[3]/div[3]/div[1]/text()', },
                {"xpath": '//h1/text()', },
                # {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '/html/body/div[7]/div[1]/div/div', },
                {"xpath": '/html/body/div[6]/div[2]', },
                # {"xpath": '/html/body/div[1]/div[3]/div/div/div[2]', },
            ],

            "pubSource": [
                # {"xpath": '/html/head/meta[@name="ContentSource"]/@content',
                #  # "regex": r"来源[:：](.*)"
                # },
                {"xpath": '/html/body/div[5]/div[1]/div[2]/div[1]/text()',
                 "regex": r"\d(.*?)阅读量"
                 },

                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                # {
                #     "xpath": '/html/body/div[2]/div/div/div[1]/div/span[2]/text()',
                # "regex": r"时间[：:](\d+.*\d+)"
                # },
                {
                    "xpath": '/html/body/div[5]/div[1]/div[2]/div[1]/text()',
                    "regex": r"(\d+.*\d+)"
                },
                # {
                #     "xpath": '//div[@class="t"]/text()',
                #     "regex": r"(\d+.*\d+)"
                # },
                # {
                # "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                # "regex": r"(\d+.*\d+)"
                # }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 澎湃
    {
        "platformName": "澎湃",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.thepaper.cn/",
        # 首页头条新闻
        "headline_news": ['//div[@class="headline_txt"]/a'],
        # 轮播信息
        "banner_news": ['//div[@class="swiper-wrapper"]/div/div/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="masonryContent"]/div/h2/a'],
        # 导航信息
        "channel_info_xpath": ['//div[@class="head_banner"]/div/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\w+_\w+_\d+",
            # r"https?://[\w\-\.]+/\w+/\w+/\d+/\w\d+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                # {"xpath": '/html/body/div[5]/div[1]/div[1]/text()'},
                {"xpath": '//div[@class="video_txt_t"]/h2/text()', },
                {"xpath": '//h1/text()', },
                # {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//div[@class="news_txt"]', },
                {"xpath": '/html/body/div[3]', },
                # {"xpath": '/html/body/div[6]/div[2]', },
                # {"xpath": '/html/body/div[1]/div[3]/div/div/div[2]', },
            ],

            "pubSource": [
                # {"xpath": '/html/head/meta[@name="ContentSource"]/@content',
                #  # "regex": r"来源[:：](.*)"
                # },
                {"xpath": '//div[@class="news_about"]/p[1]/text()',
                 # "regex": r"\d(.*?)阅读量"
                 },

                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                # {
                #     "xpath": '/html/body/div[2]/div/div/div[1]/div/span[2]/text()',
                # "regex": r"时间[：:](\d+.*\d+)"
                # },
                {
                    "xpath": '//div[@class="news_about"]/p[2]/text()',
                    # "regex": r"(\d+.*\d+)"
                },
                # {
                #     "xpath": '//div[@class="t"]/text()',
                #     "regex": r"(\d+.*\d+)"
                # },
                # {
                # "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                # "regex": r"(\d+.*\d+)"
                # }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 观察者网
    {
        "platformName": "观察者网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "https://www.guancha.cn/",
        # 首页头条新闻
        "headline_news": ['//div[@class="content-headline"]/h3/a'],
        # 轮播信息
        "banner_news": ['/html/body/div[3]/div/div[1]/div/div[1]/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//ul[@class="img-List"]/li/h4/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[1]/div/div[1]/div/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\w+/\d+_\d+_\d+_\d+.shtml",
            r"https?://[\w\-\.]+/\w+/\w+/\w+.html\?id=\d+",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                # {"xpath": '/html/body/div[5]/div[1]/div[1]/text()'},
                {"xpath": '/html/body/div[1]/div[3]/ul/li[1]/h3/text()', },
                # {"xpath": '//h1/text()', },
                {"xpath": '//*[@id="content"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[1]/div[3]/ul/li[1]/div[3]', },
                # {"xpath": '/html/body/div[3]', },
                {"xpath": '//*[@id="player-container-id"]', },
                # {"xpath": '/html/body/div[1]/div[3]/div/div/div[2]', },
            ],

            "pubSource": [
                # {"xpath": '/html/head/meta[@name="ContentSource"]/@content',
                #  # "regex": r"来源[:：](.*)"
                # },
                {"xpath": '/html/body/div[1]/div[3]/ul/li[1]/div[2]/span[3]/text()',
                 "regex": r"来源[:：](.*)"
                 },

                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                # {
                #     "xpath": '/html/body/div[2]/div/div/div[1]/div/span[2]/text()',
                # "regex": r"时间[：:](\d+.*\d+)"
                # },
                {
                    "xpath": '/html/body/div[1]/div[3]/ul/li[1]/div[2]/span[1]/text()',
                    # "regex": r"(\d+.*\d+)"
                },
                # {
                #     "xpath": '//div[@class="t"]/text()',
                #     "regex": r"(\d+.*\d+)"
                # },
                # {
                # "xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                # "regex": r"(\d+.*\d+)"
                # }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 河北省自然资源厅
    {
        "platformName": "河北省自然资源厅",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://zrzy.hebei.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//div[@class="tt"]/h1/a'],
        # 轮播信息
        "banner_news": ['//*[@id="J_bg_ban2"]/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/div/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\w+_\d+/\w+/\d+/\w\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\w+/\d+.html",
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '/html/body/div[2]/div[2]/div/div/div/h2/text()', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
                {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '//*[@id="BodyLabel"]', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[2]/div[2]/div', },
                {"xpath": '/html/body/div[1]/div[3]/div/div/div[2]', },
            ],

            "pubSource": [
                {"xpath": '/html/head/meta[@name="ContentSource"]/@content',
                 #  # "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

                {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[2]/div/div/div[1]/div/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/head/meta[@name="PubDate"]/@content',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                    "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '//*[@id="yanse"]/div[2]/h4/span[1]/text()',
                    "regex": r"(\d+.*\d+)"
                }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 河北人大
    {
        "platformName": "河北人大",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.hbrd.net/",
        # 首页头条新闻
        "headline_news": ['//li[@class="bt28"]/a'],
        # 轮播信息
        "banner_news": ['/html/body/div[3]/div/div[2]/div[1]/div/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[3]/div/div[2]/div[2]/div[2]/ul[1]/li/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top"]/li/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\w+/\w+/\w+/\d+.html",
            # r"https?://[\w\-\.]+/\w+/\w+/\w+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                # {"xpath": '//h1/text()'},
                {"xpath": '//div[@class="title"]/text()', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
                # {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[3]/div/div/div[2]/div[5]', },
                # {"xpath": '//*[@id="BodyLabel"]', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[2]/div[2]/div', },
                # {"xpath": '/html/body/div[1]/div[3]/div/div/div[2]', },
            ],

            "pubSource": [
                # {"xpath": '/html/head/meta[@name="ContentSource"]/@content',
                #  # "regex": r"来源[:：](.*)"
                # },
                {"xpath": '/html/body/div[3]/div/div/div[2]/div[3]/div[1]/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },

                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {
                    "xpath": '/html/body/div[3]/div/div/div[2]/div[3]/div[1]/span[2]/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                # {
                #     "xpath": '/html/head/meta[@name="PubDate"]/@content',
                #     # "regex": r"时间[：:](\d+.*\d+)"
                # },
                # {
                #     "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                #     "regex": r"时间[：:](\d+.*\d+)"
                # },
                # {
                #     "xpath": '//*[@id="yanse"]/div[2]/h4/span[1]/text()',
                #     "regex": r"(\d+.*\d+)"
                # }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 河北广播网
    {
        "platformName": "河北广播网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.hebradio.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="contant"]/div[4]/div[2]/div[3]/ul/li/a'],
        # 轮播信息
        "banner_news": ['//*[@id="divimginfog_imgPlayer"]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="contant"]/div[12]/div[3]/div[2]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="header"]/div[4]/div[1]/ul/li//a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\w+/\w+/\w+/\d+.html",
            # r"https?://[\w\-\.]+/\w+/\w+/\w+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()'},
                {"xpath": '//*[@id="tv_video_bofang_t"]/div/text()', },
                # {"xpath": '/html/body/div[4]/div/div/div/div[1]/p/text()', },
                # {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="layout_inner"]/div[1]/div[2]/section/article/div[1]', },
                {"xpath": '//*[@id="gallery"]/div[2]', },
                {"xpath": '//*[@id="tv_video_bofang_m"]/div/div[1]', },
                # {"xpath": '/html/body/div[1]/div[3]/div/div/div[2]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="photo_detitle_main"]/section/div/header/div/span[2]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//*[@id="layout_inner"]/div[1]/div[2]/div[2]/p[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },

                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {
                    "xpath": '//*[@id="layout_inner"]/div[1]/div[2]/div[2]/p[1]/text()',
                    "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '//*[@id="photo_detitle_main"]/section/div/header/div/span[1]/text()',
                    "regex": r"时间[：:](\d+.*\d+)"
                },
                # {
                #     "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                #     "regex": r"时间[：:](\d+.*\d+)"
                # },
                # {
                #     "xpath": '//*[@id="yanse"]/div[2]/h4/span[1]/text()',
                #     "regex": r"(\d+.*\d+)"
                # }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 河北网络电视台
    {
        "platformName": "河北网络电视台",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.hebtv.com/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[2]/div[5]/div/h5/a'],
        # 轮播信息
        "banner_news": ['/html/body/div[2]/div[9]/div[1]/div[2]/div/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[2]/div[9]/div[2]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[2]/div[2]/div/ul/li[1]/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\d+-\d+-\d+/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\w+/\w+/\w+/\d+.html",
            # r"https?://[\w\-\.]+/\w+/\w+/\w+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                # {"xpath": '//h1/text()'},
                {"xpath": '//*[@id="news_contents"]/div[1]/h5/text()', },
                {"xpath": '/html/body/div[3]/div[2]/p/text()', },
                # {"xpath": '//div[@class="zwxl-title"]/p/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="news_contents"]/div[2]', },
                {"xpath": '/html/body/div[3]/div[1]', },
                # {"xpath": '//*[@id="tv_video_bofang_m"]/div/div[1]', },
                # {"xpath": '/html/body/div[1]/div[3]/div/div/div[2]', },
            ],

            "pubSource": [
                # {"xpath": '/html/head/meta[@name="ContentSource"]/@content',
                #  # "regex": r"来源[:：](.*)"
                # },
                {"xpath": '//*[@id="news_contents"]/div[1]/div/div[1]/p[1]/span/text()',
                 # "regex": r"来源[:：](.*)"
                 },

                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {
                    "xpath": '//*[@id="news_contents"]/div[1]/div/div[1]/p[3]/span/text()',
                    # "regex": r"时间[：:](\d+.*\d+)"
                },
                {
                    "xpath": '/html/body/div[3]/div[2]/span/text()',
                    #     # "regex": r"时间[：:](\d+.*\d+)"
                },
                # {
                #     "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                #     "regex": r"时间[：:](\d+.*\d+)"
                # },
                # {
                #     "xpath": '//*[@id="yanse"]/div[2]/h4/span[1]/text()',
                #     "regex": r"(\d+.*\d+)"
                # }
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 河北广电网
    {
        "platformName": "河北广电网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.hbgd.net/",
        # 首页头条新闻
        "headline_news": ['//*[@id="title30"]/a'],
        # 轮播信息
        "banner_news": ['/html/body/div[3]/div[2]/div[1]/section/div[1]/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="content16-left"]/div/ul[1]/li/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="channel"]/li/a'],
        # 详情链接。
        "doc_links": [
            ''
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\d+.html",
            # r"https?://[\w\-\.]+/\w+/\w+/\w+/\w+/\d+.html",
            # r"https?://[\w\-\.]+/\w+/\w+/\w+/\d+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                # {"xpath": '//h1/text()'},
                {"xpath": '//*[@id="content"]/div[2]/h2/text()', },
                {"xpath": '//*[@id="header"]/div[2]/div[2]/div[1]/div[1]/div/div[1]/text()', },
                # {"xpath": '//div[@class="zwxl-title"]/p/text()',  },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]/div[2]/div[2]', },
                {"xpath": '//*[@id="header"]/div[2]/div[2]/div[1]/div[1]', },
                # {"xpath": '//*[@id="tv_video_bofang_m"]/div/div[1]', },
                # {"xpath": '/html/body/div[1]/div[3]/div/div/div[2]', },
            ],

            "pubSource": [
                # {"xpath": '/html/head/meta[@name="ContentSource"]/@content',
                #  # "regex": r"来源[:：](.*)"
                # },
                {"xpath": '//*[@id="content"]/div[2]/div[1]/a/text()',
                 # "regex": r"来源[:：](.*)"
                 },

                # {"xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[1]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {
                    "xpath": '//*[@id="content"]/div[2]/div[1]/text()',
                    "regex": r"(\d+.*\d+)"
                },
                # {
                # "xpath": '/html/body/div[3]/div[2]/span/text()',
                #     # "regex": r"时间[：:](\d+.*\d+)"
                # },
                # {
                #     "xpath": '/html/body/div[2]/div[2]/div/div/div/div[1]/span/span[2]/text()',
                #     "regex": r"时间[：:](\d+.*\d+)"
                # },
                # {
                #     "xpath": '//*[@id="yanse"]/div[2]/h4/span[1]/text()',
                #     "regex": r"(\d+.*\d+)"
                # }
            ],
            "authors": [],
            "summary": [],
        }
    },

    # 1/19 ——2/23任务
    # 1/19  10个上周未完成 本周任务8个
    # 六安新闻网
    {
        "platformName": "六安新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ma_tk=ccmx4w3d7b9b2lrkrd7oj7a364egn4vl; _ma_starttm=1611020845560; UM_distinctid=1771853420a1df-0ed29455fe000d-31346d-144000-1771853420bb2e; CNZZDATA1278877383=839932181-1611015944-%7C1611015944; Hm_lvt_6e24f4b69ca1d7558baf15af1d094b53=1611020846; PowerLeaveSitePrompts=NoShow; PowerUniqueVisitor=6e718d9c-ac52-4741-8139-5fb4e6ce2052_01%2F19%2F2021%2000%3A00%3A00; _ma_is_new_u=0; Hm_lpvt_6e24f4b69ca1d7558baf15af1d094b53=1611021334; __RequestVerificationToken=8BmR7BoR6Cxp3VS4N1cfBSF3dynadllfQM2h4qnPFQeXAaUWn3T_XLv5JbRNWsqs84If5Gy72_UKxr6mJCt1ytNv_DLKQ4uzWc1EfitSd_41; security_session_verify=59dc7b52701822fcf0a4c8b519ba7dc9',
        # 起始地址。
        "start_url": "https://www.luaninfo.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="topnews"]/dd/div/ul/li/div//a'],
        # 轮播信息
        "banner_news": ['//*[@id="pageSlide"]/div[1]/div/ul/li/div[1]//a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[1]/div[3]/div[6]/div[1]/div[1]/div[2]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="nav"]/div/ul/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\w+_\d+",
            # r"https?://[\w\-\.]+/\d+/\d+/\d+/\w+\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h2[@class="title"]/text()'},
                # {"xpath": '/html/body/div[12]/div[1]/div[1]/h1/text()', },
                {"xpath": '//h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="main"]/div[1]/div[2]/div', },
                # {"xpath": '//*[@id="article_inbox"]/div[6]', },
                # {"xpath": '//*[@id="cont"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="content"]/div/article/div[1]/div[1]/span[2]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//*[@id="main"]/div[1]/div[1]/div/span[2]/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//*[@id="content"]/div/article/div[1]/div[1]/span[3]/text()',
                 "regex": r"时间[：:](\d+.*\d+)"
                 },
                {"xpath": '//*[@id="main"]/div[1]/div[1]/div/span[1]/text()',
                 #  "regex": r"\d+.*\d+"
                 },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 六安网
    {
        "platformName": "六安网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'UM_distinctid=1771867dca8435-0caa4b8e61f014-31346d-144000-1771867dca9b49; CNZZDATA2866606=cnzz_eid%3D1441445532-1611020606-http%253A%252F%252Fwww.wxrb.com.cn%252F%26ntime%3D1611020606',
        # 起始地址。
        "start_url": "http://www.wxrb.com.cn/news/",
        # 首页头条新闻
        "headline_news": ['//ul[@class="news black font12"]/li/a'],
        # 轮播信息
        "banner_news": ['//td[@class="font12 black"]/table//tr[1]//a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['/html/body/table[2]//tr/td[2]/table//tr/td[1]/table//tr/td[2]/table//tr//a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\d+/\d+/\d+/\w+\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/table[4]//tr/td[1]/table[2]//tr[1]/td/text()'},
                # {"xpath": '/html/body/div[12]/div[1]/div[1]/h1/text()', },
                # {"xpath": '//h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//td[@class="contenta"]', },
                # {"xpath": '//*[@id="main"]/div[1]/div[2]/div', },
                # {"xpath": '//*[@id="article_inbox"]/div[6]', },
                # {"xpath": '//*[@id="cont"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//td[@class="sourcea"]/text()',
                 "regex": r"来源[:：](.*)编辑"
                 },
                # {"xpath": '//*[@id="main"]/div[1]/div[1]/div/span[2]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '//td[@class="sourcea"]/text()',
                 "regex": r"时间[：:](\d+.*\d+分)"
                 },
                # {"xpath": '//*[@id="main"]/div[1]/div[1]/div/span[1]/text()',
                #  "regex": r"\d+.*\d+"
                # },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 六安广播电视网
    {
        "platformName": "六安广播电视网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '',
        # 起始地址。
        "start_url": "http://www.china-latv.com/",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": ['//ul[@class="trigger"]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//ul[@class="clearfix cell_2888_"]/li/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[4]/div[1]/div/ul/li[2]/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+-\d+-\d+/\d+.html",
            # r"https?://[\w\-\.]+/\d+/\d+/\d+/\w+\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                # {"xpath": '/html/body/table[4]//tr/td[1]/table[2]//tr[1]/td/text()'},
                # {"xpath": '/html/body/div[12]/div[1]/div[1]/h1/text()', },
                {"xpath": '//h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[2]/div[2]/div[3]/div/div[2]', },
                # {"xpath": '//*[@id="main"]/div[1]/div[2]/div', },
                # {"xpath": '//*[@id="article_inbox"]/div[6]', },
                # {"xpath": '//*[@id="cont"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//span[@class="origin"]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                # {"xpath": '//*[@id="main"]/div[1]/div[1]/div/span[2]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '//span[@class="publish-time"]/text()',
                 # "regex": r"时间[：:](\d+.*\d+分)"
                 },
                # {"xpath": '//*[@id="main"]/div[1]/div[1]/div/span[1]/text()',
                #  "regex": r"\d+.*\d+"
                # },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 六安政府网
    {
        "platformName": "六安政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '__jsluid_h=738c3b0a78f06eea5243312c4f3cf695; UM_distinctid=1771891547acb4-0ebe346e8d920f-31346d-144000-1771891547bb5b; CNZZDATA1279628549=781300556-1611020839-%7C1611027442; luan_gova_SHIROJSESSIONID=84fa090a-9991-43ff-9499-ef76798cdd50',
        # 起始地址。
        "start_url": "http://www.luan.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//*[@id="myFocus02"]/div[1]/ul/li[1]/a'],
        # 轮播信息
        "banner_news": ['//*[@id="myFocus01"]/div[1]/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="1tab1"]/div[2]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="tab1"]/div[2]/div[2]/ul/li[3]/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\d+.html",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                # {"xpath": '/html/body/table[4]//tr/td[1]/table[2]//tr[1]/td/text()'},
                # {"xpath": '/html/body/div[12]/div[1]/div[1]/h1/text()', },
                {"xpath": '//h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="zoom"]', },
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@id="article_inbox"]/div[6]', },
                # {"xpath": '//*[@id="cont"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//td[@class="is-leftinfo"]/span[2]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//td[@class="is-leftinfo"]/span[3]/text()',
                 "regex": r"时间[：:](\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                 "regex": r"\d+.*\d+"
                 },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 六安长安网
    {
        "platformName": "六安长安网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'bdshare_firstime=1611028057053; PHPSESSID=tkpodek1mac4uaioh1c58n0pn0; security_session_verify=50b04458f9ab993143eeac3e5bb1a8ca',
        # 起始地址。
        "start_url": "http://www.lashgl.gov.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[2]/div[2]/div[3]/div[2]/a'],
        # 轮播信息
        "banner_news": ['//*[@id="contentList"]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="dtE_0"]/li/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="nav_54c1c3179a05c2e24f5ab70e"]'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/detail/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                # {"xpath": '/html/body/table[4]//tr/td[1]/table[2]//tr[1]/td/text()'},
                # {"xpath": '/html/body/div[12]/div[1]/div[1]/h1/text()', },
                {"xpath": '//div[@class="is-newstitle"]/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//div[@class="is-newscontnet"]', },
                # {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@id="article_inbox"]/div[6]', },
                # {"xpath": '//*[@id="cont"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//td[@class="is-leftinfo"]//text()',
                 "regex": r"来源[:：](.*)发布"
                 },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '//td[@class="is-leftinfo"]//text()',
                 "regex": r"时间[：:](\d+.*\d+)"
                 },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #   "regex": r"\d+.*\d+"
                #  },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 宣城新闻网
    {
        "platformName": "宣城新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '',
        # 起始地址。
        "start_url": "http://www.newsxc.com/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[6]/div[12]/div/div/ul/li/a'],
        # 轮播信息
        "banner_news": ['/html/body/div[6]/div[18]/div[2]/ul[1]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//div[@class="xcxw"]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="nava"]/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+-\d+-\d+-\d+.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                # {"xpath": '/html/body/table[4]//tr/td[1]/table[2]//tr[1]/td/text()'},
                # {"xpath": '/html/body/div[12]/div[1]/div[1]/h1/text()', },
                {"xpath": '//div[@class="dabiaoti"]/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//div[@class="article-main"]', },
                # {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@id="article_inbox"]/div[6]', },
                # {"xpath": '//*[@id="cont"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//span[@class="origin"]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '//span[@class="time"]//text()',
                 "regex": r"时间[：:](\d+.*\d+)"
                 },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #   "regex": r"\d+.*\d+"
                #  },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 宣城市政府网
    {
        "platformName": "宣城市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'UM_distinctid=17719251c4d91d-0305510d1a67b8-31346d-144000-17719251c4e425; CNZZDATA1262697769=747890967-1611030730-%7C1611030730; Hm_lvt_96da6bb9c6240d1fcc3e26827fb60319=1611034599; Hm_lpvt_96da6bb9c6240d1fcc3e26827fb60319=1611034599',
        # 起始地址。
        "start_url": "http://www.xuancheng.gov.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[2]/div/div[2]/a'],
        # 轮播信息
        "banner_news": ['//*[@id="j-flash"]/div[1]/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="news_index"]/div[5]/ul[1]/li/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="news_index"]/div[1]/ul/li[1]/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+.html",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                # {"xpath": '/html/body/table[4]//tr/td[1]/table[2]//tr[1]/td/text()'},
                # {"xpath": '/html/body/div[12]/div[1]/div[1]/h1/text()', },
                {"xpath": '//h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="zoom"]', },
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@id="article_inbox"]/div[6]', },
                # {"xpath": '//*[@id="cont"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '/html/body/div[2]/div/div[2]/div[1]/div[1]/span[2]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '/html/body/div[2]/div/div[2]/div[1]/div[1]/span[1]/text()',
                 "regex": r"时间[：:](\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                 "regex": r"\d+.*\d+"
                 },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 宣城长安网
    {
        "platformName": "宣城长安网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'ASPSESSIONIDCAABCRSQ=HCPLKGNCFLBAJLAABGCMJFAN',
        # 起始地址。
        "start_url": "http://www.xccaw.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//td[@class="ttfont"]/a'],
        # 轮播信息
        "banner_news": ['//div[@class="slidesjs-control"]/div/div[1]/a'],
        # 轮播旁边新闻
        "banner_news_side": [
            '/html/body/table[4]//tr/td/table[1]//tr/td/table[4]//tr/td[2]/table//tr/td/table[5]//tr//a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="navMenu"]/ul/li[3]/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//td[@class="f22 b black"]/text()'},
                {"xpath": '/html/body/div[4]/div/div[2]/div[1]/div/div[1]/text()', },
                {"xpath": '//h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="div1400"]/div[2]/div[6]/div/table//tr[3]/td/article/div', },
                {"xpath": '/html/body/div[4]/div/div[2]/div[1]/div/div[3]', },
                {"xpath": '/html/body/div/div/div[2]/div[2]', },
                # {"xpath": '//*[@id="cont"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//td[@class="f12 black"]//tr[1]/td[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[4]/div/div[2]/div[1]/div/div[2]/span[2]/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//td[@class="f12 black"]//tr[1]/td[2]/text()',
                 "regex": r"时间[：:](\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[4]/div/div[2]/div[1]/div/div[2]/span[1]/text()',
                 "regex": r"\d+.*\d+"
                 },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 池州新闻网
    {
        "platformName": "池州新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'UM_distinctid=177195f65cf6c-0681409e6e8f7b-31346d-144000-177195f65d0ae8; CNZZDATA182204=cnzz_eid%3D75441137-1611034985-%26ntime%3D1611034985; bdshare_firstime=1611038418506; JSESSIONID=201299959B7A8AD6C5216569617CB734',
        # 起始地址。
        "start_url": "http://www.chiznews.com/",
        # 首页头条新闻
        "headline_news": ['//div[@class="headlines"]/a'],
        # 轮播信息
        "banner_news": ['//div[@class="news-banner fr"]/div[1]/div[1]/div//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//div[@class="news-list fl"]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="navl"]/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[3]/div/div/div/div[2]/div[1]/div[1]/form/div[2]/text()'},
                # {"xpath": '/html/body/div[4]/div/div[2]/div[1]/div/div[1]/text()', },
                # {"xpath": '//h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[3]/div/div/div/div[2]/div[1]/div[1]/form/div[5]', },
                # {"xpath": '/html/body/div[4]/div/div[2]/div[1]/div/div[3]', },
                # {"xpath": '/html/body/div/div/div[2]/div[2]', },
                # {"xpath": '//*[@id="cont"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//div[@class="contshi"]/text()',
                 "regex": r"来源[:：](.*?)\s"
                 },
                # {"xpath": '/html/body/div[4]/div/div[2]/div[1]/div/div[2]/span[2]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                # {"xpath": '//td[@class="f12 black"]//tr[1]/td[2]/text()',
                #  "regex": r"时间[：:](\d+.*\d+)"
                #  },
                {"xpath": '//div[@class="contshi"]/text()',
                 "regex": r"日期[：:](\d+.*\d+)"
                 },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 浙江新闻网
    {
        "platformName": "浙江新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_trs_uv=kjxxordk_181_8npv; aliyungf_tc=AQAAAFzeyE508QoAq1YztirHaaQLLop6; acw_tc=76b20fe816110402157213679e4c18de838cb581ea0698c2135f35d64a5c70; SERVERID=5de59201df01420c28800476b9e3838f|1611040215|1611040215; Hm_lvt_2a5004732122e2825309d75bc37bf43f=1610694113,1610694794,1611040216; Hm_lpvt_2a5004732122e2825309d75bc37bf43f=1611040216; _trs_ua_s_1=kk3nqycg_181_5t02',
        # 起始地址。
        "start_url": "https://zj.zjol.com.cn/",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": ['//div[@class="swiper-wrapper"]/div/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[3]/div/div[2]/div[1]/ul/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[2]/div[2]/div/div/ul/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/news.html\?id=\d+",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                # {"xpath": '/html/body/div[3]/div/div/div/div[2]/div[1]/div[1]/form/div[2]/text()'},
                # {"xpath": '/html/body/div[4]/div/div[2]/div[1]/div/div[1]/text()', },
                {"xpath": '//h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[3]/div/div[2]/div/div[1]/div', },
                # {"xpath": '/html/body/div[4]/div/div[2]/div[1]/div/div[3]', },
                # {"xpath": '/html/body/div/div/div[2]/div[2]', },
                # {"xpath": '//*[@id="cont"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": 'string(//p[@class="news_info"])',
                 "regex": r"\|(.*)\|"
                 },
                {"xpath": 'string(//p[@class="news_info"])',
                 "regex": r"\|(.*)"
                 },
                # {"xpath": '/html/body/div[4]/div/div[2]/div[1]/div/div[2]/span[2]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                # {"xpath": '//td[@class="f12 black"]//tr[1]/td[2]/text()',
                #  "regex": r"时间[：:](\d+.*\d+)"
                #  },
                {"xpath": '//p[@class="news_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 浙江省政府网
    {
        "platformName": "浙江省政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'zh_choose_undefined=s; SERVERID=e741bbf83b6f24e79f118d965207c05f|1611041493|1611041329',
        # 起始地址。
        "start_url": "http://www.zj.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//div[@class="swiper-wrapper headLines-wrapper"]/div/a'],
        # 轮播信息
        "banner_news": ['//ul[@class="gwyxx"]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="barrierfree_container"]/div[4]/div/div[2]/div[2]/div[2]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": [''],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\w+_\d+_\d+.html",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                # {"xpath": '/html/body/div[3]/div/div/div/div[2]/div[1]/div[1]/form/div[2]/text()'},
                {"xpath": '//*[@id="c"]//tr[1]/td/text()', },
                {"xpath": '//h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//td[@class="bt_content"]', },
                {"xpath": '/html/body/div[4]/div/div[2]/div[1]/div/div[3]', },
                # {"xpath": '/html/body/div/div/div[2]/div[2]', },
                # {"xpath": '//*[@id="cont"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[3]/text()',
                 "regex": r"来源[:：](.*)"
                 },

                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 浙江在线
    {
        "platformName": "浙江在线",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_trs_uv=kjxxordk_181_8npv; aliyungf_tc=AQAAAMgrMXS2EQgAq1YztsjNbSzvdHA1; _trs_ua_s_1=kk3oyret_1_fn2q',
        # 起始地址。
        "start_url": "https://www.zjol.com.cn/",
        # 首页头条新闻
        "headline_news": ['//*[@id="widget13648"]/h3/a'],
        # 轮播信息
        "banner_news": ['//*[@id="widget13576"]/div[1]/div/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="widget14153"]/ul[1]/li/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="navUl firstNavUl"]/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/.*?\d+/t\d+_\d+.shtml",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//div[@class="contTit"]//text()', },
                {"xpath": '//*[@id="container"]/div[2]/div[1]/div[2]/div[1]/text()', },
                # {"xpath": '//h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//div[@class="contTxt"]', },
                {"xpath": '//*[@id="container"]/div[2]/div[1]/div[2]/div[3]', },
                # {"xpath": '/html/body/div/div/div[2]/div[2]', },
                # {"xpath": '//*[@id="cont"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="source_baidu"]/text()',
                 "regex": r"来源[:：](.*)"
                 },

                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '//*[@id="pubtime_baidu"]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 浙江新闻网
    {
        "platformName": "浙江新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'Hm_lvt_9fee1f84162c409c49a75e539132a5d8=1611045438; Hm_lpvt_9fee1f84162c409c49a75e539132a5d8=1611045438',
        # 起始地址。
        "start_url": "https://news.zj.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="top_title"]/a'],
        # 轮播信息
        "banner_news": ['//*[@id="Main"]/div[1]/div/h2/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="Main"]/div[1]/div/h2/a'],
        # 导航信息
        "channel_info_xpath": ['//div[@class="nav"]/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\d+.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//*[@id="Naver"]/div[3]/div[1]/text()', },
                # {"xpath": '//*[@id="container"]/div[2]/div[1]/div[2]/div[1]/text()', },
                # {"xpath": '//h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="Naver"]/div[3]/div[3]', },
                # {"xpath": '//*[@id="container"]/div[2]/div[1]/div[2]/div[3]', },
                # {"xpath": '/html/body/div/div/div[2]/div[2]', },
                # {"xpath": '//*[@id="cont"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                # {"xpath": '//*[@id="source_baidu"]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '//*[@id="Naver"]/div[3]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 浙江之声网
    {
        "platformName": "浙江之声网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'acw_tc=76b20fe316110458352374768e35764f49446c84bad094bd1754d0bd10bcc6; Hm_lvt_5c3d520d131f79b2e027c95704f603d6=1611045837; Hm_lpvt_5c3d520d131f79b2e027c95704f603d6=1611045837; br-resp-key="g:202101191643_5145ffbb-416e-450f-4f42-7ccd22e34022',
        # 起始地址。
        "start_url": "http://www.am810.net/",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": [''],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div/div[1]/div[3]/div[2]/div[1]/div[1]/div[2]/a'],
        # 导航信息
        "channel_info_xpath": ['//div[@class="nav"]/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\d+.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div/div[1]/div[3]/div[1]/div[1]/text()', },
                # {"xpath": '//*[@id="container"]/div[2]/div[1]/div[2]/div[1]/text()', },
                # {"xpath": '//h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div/div[1]/div[3]/div[1]/div[3]', },
                # {"xpath": '//*[@id="container"]/div[2]/div[1]/div[2]/div[3]', },
                # {"xpath": '/html/body/div/div/div[2]/div[2]', },
                # {"xpath": '//*[@id="cont"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                # {"xpath": '//*[@id="source_baidu"]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '/html/body/div/div[1]/div[3]/div[1]/div[2]/span[1]/text()',
                 # "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 浙江工人日报网
    {
        "platformName": "浙江工人日报网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'aHm_lvt_08c75675b4ae51e9127dfd7400b5c4f7=1611045998; Hm_lpvt_08c75675b4ae51e9127dfd7400b5c4f7=1611045998',
        # 起始地址。
        "start_url": "http://www.zjgrrb.com/",
        # 首页头条新闻
        "headline_news": ['/html/body/table[6]//tr/td/table//tr/td[3]/table//tr/td/a'],
        # 轮播信息
        "banner_news": ['/html/body/table[8]//tr/td[5]/table//tr/td/table[1]//tr[2]/td/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="demo1"]/div/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/table[4]//tr/td/table[3]//tr/td/table//tr/td/strong/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/table[4]//tr/td/table[1]//tr[1]/td/div[2]/h2/text()', },
                # {"xpath": '//*[@id="container"]/div[2]/div[1]/div[2]/div[1]/text()', },
                # {"xpath": '//h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/table[4]//tr/td/table[1]//tr[3]/td', },
                # {"xpath": '//*[@id="container"]/div[2]/div[1]/div[2]/div[3]', },
                # {"xpath": '/html/body/div/div/div[2]/div[2]', },
                # {"xpath": '//*[@id="cont"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '/html/body/table[4]//tr/td/table[1]//tr[1]/td/div[4]//text()',
                 "regex": r"来源[:：](.*?)作者"
                 },

                {"xpath": '/html/body/table[4]//tr/td/table[1]//tr[1]/td/div[4]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '/html/body/table[4]//tr/td/table[1]//tr[1]/td/div[4]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 浙江在线杭州频道
    {
        "platformName": "浙江在线杭州频道",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_trs_uv=kjxxordk_181_8npv; zycna=GaRcvsRuTyIBAbYzVquEHsyK; UM_distinctid=17719a4712ccc9-0077244564bac8-31346d-144000-17719a4712dba8; aliyungf_tc=AQAAABWL/BRmsQ0AmkbsfJDk64fk1OZD; CNZZDATA1259786647=1977782027-1611046573-%7C1611046573',
        # 起始地址。
        "start_url": "http://hangzhou.zjol.com.cn/",
        # 首页头条新闻
        "headline_news": ['//*[@id="widget11245"]/a'],
        # 轮播信息
        "banner_news": ['//*[@id="slidesImgs"]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="main0"]/ul/li/ol/li//a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="page"]/div[1]/div[1]/ul/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+/t\d+_\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//*[@id="artibodytitle"]/text()', },
                # {"xpath": '//*[@id="container"]/div[2]/div[1]/div[2]/div[1]/text()', },
                # {"xpath": '//h1/text()', },
                # {"xpath": '//*[@id="MP_title"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="ArticleCnt"]', },
                # {"xpath": '//*[@id="container"]/div[2]/div[1]/div[2]/div[3]', },
                # {"xpath": '/html/body/div/div/div[2]/div[2]', },
                # {"xpath": '//*[@id="cont"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="oZoom"]/div[4]/a/text()',
                 # "regex": r"来源[:：](.*?)记者"
                 },

                # {"xpath": '/html/body/table[4]//tr/td/table[1]//tr[1]/td/div[4]//text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '//*[@id="oZoom"]/div[4]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 杭州网
    {
        "platformName": "杭州网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'Hm_lvt_08261419fd973f118d693f2d1ce6e02b=1611048506; Hm_lpvt_08261419fd973f118d693f2d1ce6e02b=1611048506; wdcid=50c087dd99df6d9c; wdlast=1611048507; wdses=17e78edc3ff2c6be',
        # 起始地址。
        "start_url": "https://www.hangzhou.com.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[15]/div[2]/h1/a'],
        # 轮播信息
        "banner_news": ['//*[@id="picshow_img"]/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[18]/div[2]/div[1]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[2]/div/div[2]/div[1]/div/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[1]/div[5]/div[2]/div[1]/span/text()', },
                {"xpath": '/html/body/div[5]/div[2]/div[1]/div[3]/div[1]/span/text()', },
                {"xpath": '//h1/text()', },
                {"xpath": '/html/body/div[3]/div[1]/div/div/div[2]/div[1]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[1]/div[5]/div[2]/div[3]', },
                {"xpath": '/html/body/div[5]/div/div[1]/div[2]', },
                {"xpath": '/html/body/div[5]/div[2]/div[1]/div[3]/div[3]', },
                {"xpath": '/html/body/div[3]/div[1]/div/div/div[2]/div[4]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '/html/body/div[1]/div[5]/div[2]/div[2]/a/text()',
                 # "regex": r"来源[:：](.*?)记者"
                 },

                {"xpath": '/html/body/div[3]/div[1]/div/div/div[2]/div[2]/a/text()',
                 # "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '/html/body/div[1]/div[5]/div[2]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[3]/div[1]/div/div/div[2]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 宁波在线
    {
        "platformName": "宁波在线",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '2RRb_2132_saltkey=LgIPoSIi; 2RRb_2132_lastvisit=1611045803; PHPSESSID=84kl3hha3fo7j8kenc9dgnvtm1; UM_distinctid=1771a0705ba696-096e33ad5c0d82-31346d-144000-1771a0705bbb43; CNZZDATA1278523226=290065747-1611049404-%7C1611049404; 2RRb_2132_sid=n229C6; 2RRb_2132_lastact=1611049481%09plugin.php%09',
        # 起始地址。
        "start_url": "https://www.nb114.net/index.html",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": [''],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[7]/div[2]/div[1]/div[2]/a'],
        # 导航信息
        "channel_info_xpath": [''],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+-\d+-\d+.html",
            # r"https?://[\w\-\.]+/plugin.php\?id=tom_tctoutiao&site=1&mod=info&aid=\d+",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[3]/div[1]/div/div[1]/div[1]/text()', },
                # {"xpath": '/html/body/section[2]/div[1]/text()', },
                # {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div[1]/div/div/div[2]/div[1]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[3]/div[1]/div/div[2]', },
                # {"xpath": '/html/body/section[2]/div[3]', },
                # {"xpath": '/html/body/div[5]/div[2]/div[1]/div[3]/div[3]', },
                # {"xpath": '/html/body/div[3]/div[1]/div/div/div[2]/div[4]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '/html/body/div[3]/div[1]/div/div[1]/div[2]/text()',
                 "regex": r"来源[:：](.*)"
                 },

                # {"xpath": '/html/body/div[3]/div[1]/div/div/div[2]/div[2]/a/text()',
                # "regex": r"来源[:：](.*)"
                # },

            ],
            "pubTime": [
                {"xpath": '/html/body/div[3]/div[1]/div/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '/html/body/div[3]/div[1]/div/div/div[2]/div[2]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
            ],
            "authors": [],
            "summary": [],
        }
    },

    # 1/20   完成16个
    # 新华网
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
    # 人民网
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
        # 首页头条新闻
        "headline_news": ['//*[@id="rm_topline"]/a'],
        # 轮播信息
        "banner_news": ['//*[@id="rm_focus"]/div/div[2]/div[1]/div/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="rm_bq"]/div[2]//a'],
        # 频道信息
        "channel_info_xpath": ['//*[@id="rm_topnav"]/div/div[1]/ul/li//a'],
        # 详情链接。
        "doc_links": [r"http://[\w\-\.]+\.people\.com\.cn/n\d+/\d{4,}/\d{4}/c\d+-\d+\.html$", ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                {"xpath": '/html/body/div[1]/div[7]/div[1]/h1/text()', },
                {"xpath": '/html/body/div/div[4]/div/div/div[1]/div[2]/div[1]/div[1]/h2/text()', },
            ],
            "content": [
                {"xpath": '//div[@class="box_con"]', },
                {"xpath": '/html/body/div[1]/div[7]/div[1]/div[3]', },
                {"xpath": '/html/body/div[8]/div[1]/div/div[2]', },
            ],
            "pubSource": [
                {
                    # "describe": "http://www.xinhuanet.com/renshi/2020-01/07/c_1125432025.htm",
                    "xpath": "/html/body/div[1]/div[7]/div[1]/div[2]/div[1]//text()",
                    "regex": r"源[:：](.*)",
                },
                {
                    "xpath": '/html/body/div[8]/div[1]/div/p[2]//text()',
                    "regex": r"源[:：](.*)",
                },
                {
                    "xpath": '/html/body/div[5]/div/div[1]//text()',
                    "regex": r"源[:：](.*)",
                },
                # {
                #     "xpath": '/html/body/div[7]/div[2]/text()',
                #     "regex": r"源[:：](.*)\|",
                # }
            ],
            "pubTime": [

                {"xpath": '/html/body/div[1]/div[7]/div[1]/div[2]/div[1]//text()',
                 "regex": r"(\d+.*\d+)",
                 },
                {"xpath": '/html/body/div[8]/div[1]/div/p[2]//text()',
                 "regex": r"(\d+.*\d+)",
                 },
                {"xpath": '/html/body/div[5]/div/div[1]//text()',
                 "regex": r"(\d+.*\d+)",
                 },
            ],
            "channel": [],
            "authors": [],
            "summary": [],
        },
    },
    # 中国宁波网
    {
        "platformName": "中国宁波网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'wdcid=33cd8dc9fbbde138',
        # 起始地址。
        "start_url": "http://www.cnnb.com.cn/",
        # 首页头条新闻
        "headline_news": ['//*[@id="slidesHot"]/li/div[1]/a'],
        # 轮播信息
        "banner_news": ['//*[@id="slides"]/div/div/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="four"]/div[2]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="one-up"]/ul[1]/li//a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//div[@class="heading"]/text()', },
                {"xpath": '//*[@id="wrapper"]/div/div[1]/table//tr[2]/td/table//tr[2]/td/text()', },
                # {"xpath": '/html/body/div[3]/div[1]/div/div/div[2]/div[1]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="pc"]/div[3]/div[1]/div[2]/div/div[1]', },
                {"xpath": '//*[@id="content14"]', },
                # {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="pc"]/div[3]/div[1]/div[1]/div[4]/span[2]/text()',
                 "regex": r"源[:：](.*)"
                 },

                # {"xpath": '//div[@class="sub-title"]/span[3]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '//*[@id="pc"]/div[3]/div[1]/div[1]/div[4]/span[1]/text()',
                 # "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//div[@class="sub-title"]/span[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
                # {"xpath": '/html/body/div[3]/div[1]/div/div/div[2]/div[2]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 宁波广电网
    {
        "platformName": "宁波广电网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '73_vq=1',
        # 起始地址。
        "start_url": "http://www.nbtv.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[2]/div[6]/div/div/div/ul/li/a'],
        # 轮播信息
        "banner_news": ['/html/body/div[2]/div[7]/div[1]/div[1]/ul[1]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//div[@class="new_text"]//a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[2]/div[3]/div[1]//a'],
        # 详情链接。
        "doc_links": [
            r"http://[\w\-\.]+/\w+/\w+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[3]/div[2]/div/div[1]/div[1]/h2/text()', },
                # {"xpath": '//*[@id="wrapper"]/div/div[1]/table//tr[2]/td/table//tr[2]/td/text()', },
                # {"xpath": '/html/body/div[3]/div[1]/div/div/div[2]/div[1]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="editWrap"]', },
                # {"xpath": '//*[@id="content14"]', },
                # {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="pc"]/div[3]/div[1]/div[1]/div[4]/span[2]/text()',
                 "regex": r"源[:：](.*)"
                 },

                # {"xpath": '//div[@class="sub-title"]/span[3]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '/html/body/div[3]/div[2]/div/div[1]/div[1]/h5/span[1]/text()',
                 # "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//div[@class="sub-title"]/span[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
                # {"xpath": '/html/body/div[3]/div[1]/div/div/div[2]/div[2]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 温州市政府网
    {
        "platformName": "温州市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'zh_choose=n; SERVERID=bc6beea6e995cecb42c7a1341ba3517f|1611115618|1611115576',
        # 起始地址。
        "start_url": "http://www.wenzhou.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//*[@id="barrierfree_container"]/div[2]/div[1]/div[1]/p/a'],
        # 轮播信息
        "banner_news": ['//*[@id="slideBox"]/div/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="clearfix bt-left tt"]/li//a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\w+_\d+_\d+.html",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//*[@id="c"]//tr[1]/td/text()', },
                {"xpath": '//h1/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="zoom"]', },
                {"xpath": '//*[@id="c"]//tr[4]/td', },
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="c"]//tr[2]/td/table//tr/td[3]/text()',
                 "regex": r"源[:：](.*)"
                 },
                #
                {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[3]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//*[@id="c"]//tr[2]/td/table//tr/td[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 温州新闻网
    {
        "platformName": "温州新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '',
        # 起始地址。
        "start_url": "http://www.66wz.com/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[3]/div[2]/div[2]/div[1]/a'],
        # 轮播信息
        "banner_news": ['//*[@id="banner"]/div[2]/div/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[3]/div[3]/div[2]/div[2]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="nav_news"]/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                # {"xpath": '//*[@id="c"]//tr[1]/td/text()', },
                {"xpath": '//h1/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="artibody"]', },
                # {"xpath": '//*[@id="c"]//tr[4]/td', },
                # {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="source_baidu"]/text()',
                 # "regex": r"源[:：](.*)"
                 },
                #
                # {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[3]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '//*[@id="pubtime_baidu"]/text()',
                 # "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 绍兴市政府
    {
        "platformName": "绍兴市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'zh_choose=n; SERVERID=bc6beea6e995cecb42c7a1341ba3517f|1611115618|1611115576',
        # 起始地址。
        "start_url": "http://www.sx.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//ul[@id="StateCouncil"]/li/a'],
        # 轮播信息
        "banner_news": ['//ul[@class="sideshow clearfix"]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="con_first_3"]/div[2]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": [''],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\w+_\d+_\d+.html",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//div[@class="art_title"]/h2/text()', },
                {"xpath": '//h1/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="zoom"]', },
                {"xpath": '//*[@id="c"]//tr[4]/td', },
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                # {"xpath": '//div[@class="fz_xx"]/span[1]/text()',
                #  "regex": r"源[:：](.*)"
                #  },
                #
                {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[3]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="fz_xx"]/span[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 绍兴网
    {
        "platformName": "绍兴网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '',
        # 起始地址。
        "start_url": "http://www.shaoxing.com.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[3]/div/div[7]/div[1]/h2/a'],
        # 轮播信息
        "banner_news": ['//*[@id="swiper3"]/div[1]/div/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[3]/div/div[8]/div[1]/div[1]//a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="red-nav"]/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//div[@class="detail-contant"]/h2/text()', },
                {"xpath": '//div[@class="a-title"]/h1/text()', },
                {"xpath": '//div[@class="vid-contant"]/p/text()', },
            ],
            "content": [
                {"xpath": '//div[@class="detail-contant-main"]', },
                {"xpath": '//div[@class="video-content"]', },
                # {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                # {"xpath": '//div[@class="fz_xx"]/span[1]/text()',
                #  "regex": r"源[:：](.*)"
                #  },
                #
                {"xpath": '//div[@class="detail-contant"]/span/a/text()',
                 # "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="detail-contant"]/p/text()',
                 # "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//span[@class="date"]/text()',
                 # "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 湖州市政府网
    {
        "platformName": "湖州市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'SERVERID=b2ba659a0bf802d127f2ffc5234eeeba|1611126844|1611126790',
        # 起始地址。
        "start_url": "http://www.huzhou.gov.cn/?404",
        # 首页头条新闻
        "headline_news": ['//*[@id="barrierfree_container"]/div[1]/div[4]/div/div[1]/div[2]/div[1]/a'],
        # 轮播信息
        "banner_news": ['//*[@id="cxslide_id"]/div/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="barrierfree_container"]/div[1]/div[4]/div/div[1]/div[2]/div[2]/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="barrierfree_container"]/div[1]/div[4]/div/div[1]/div[2]/ul/a[5]'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\w+_\d+_\d+.html",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//*[@id="barrierfree_container"]/div[3]/div/div/div/div[2]/div[1]/text()', },
                {"xpath": '//h1/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="zoom"]', },
                {"xpath": '//*[@id="c"]//tr[4]/td', },
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                # {"xpath": '//div[@class="fz_xx"]/span[1]/text()',
                #  "regex": r"源[:：](.*)"
                #  },
                #
                {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[3]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//*[@id="barrierfree_container"]/div[3]/div/div/div/div[2]/div[2]/span[1]/text()',
                 # "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 今日湖州
    {
        "platformName": "今日湖州",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '',
        # 起始地址。
        "start_url": "http://www.hugd.com/jrhz/list.shtml",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": [''],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="content"]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": [''],
        # 详情链接。
        "doc_links": [
            # r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\w+_\d+_\d+.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//*[@id="wrapper"]/div/div/div[2]/div[2]/div/div[1]/span/text()', },
                # {"xpath": '//h1/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="wrapper"]/div/div/div[2]/div[2]', },
                # {"xpath": '//*[@id="c"]//tr[4]/td', },
                # {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                # {"xpath": '//div[@class="fz_xx"]/span[1]/text()',
                #  "regex": r"源[:：](.*)"
                #  },
                #
                {"xpath": 'string(//*[@id="llcount"])',
                 "regex": r"来源[:：](.*?)\d"
                 },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": 'string(//*[@id="llcount"])',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 嘉兴市政府网
    {
        "platformName": "嘉兴市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_gscu_443420073=1112837796nt5717; _gscbrs_443420073=1; _gscs_443420073=111283773tpsn117|pv:4; SERVERID=a6d2b4ba439275d89aa9b072a5b72803|1611128412|1611128376',
        # 起始地址。
        "start_url": "http://www.jiaxing.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//*[@id="con_ifo_1"]/ul/li/a'],
        # 轮播信息
        "banner_news": ['//*[@id="bt-jq-TX-010108"]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="con_ifo_2"]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": [''],
        # 详情链接。
        "doc_links": [
            # r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\w+_\d+_\d+.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h2/text()', },
                # {"xpath": '//h1/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="zoom"]', },
                # {"xpath": '//*[@id="c"]//tr[4]/td', },
                # {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                # {"xpath": '//div[@class="fz_xx"]/span[1]/text()',
                #  "regex": r"源[:：](.*)"
                #  },
                #
                {"xpath": '//div[@class="fz_xx"]/span[2]/text()',
                 "regex": r"来源[:：](.*?)\d"
                 },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '//div[@class="fz_xx"]/span[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 嘉兴在线
    {
        "platformName": "嘉兴在线",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '__utma=28760046.823477338.1611129460.1611129460.1611129460.1; __utmc=28760046; __utmz=28760046.1611129460.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=28760046.1.10.1611129460',
        # 起始地址。
        "start_url": "https://www.cnjxol.com/",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": ['//div[@id="jscroll"]/ul[@id="jscroll_img"]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//div[@class="fr"]/div[@class="item mr"]/div[@class="main"]/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="sub"]/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/t\d+_\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//*[@id="main"]/div[1]/div[3]/text()', },
                # {"xpath": '//h1/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="main"]/div[1]/div[6]', },
                # {"xpath": '//*[@id="c"]//tr[4]/td', },
                # {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                # {"xpath": '//div[@class="fz_xx"]/span[1]/text()',
                #  "regex": r"源[:：](.*)"
                #  },
                #
                # {"xpath": '//div[@class="fz_xx"]/span[2]/text()',
                #  "regex": r"来源[:：](.*?)\d"
                #  },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '//*[@id="main"]/div[1]/div[5]/span/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 金华新闻网
    {
        "platformName": "金华新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'UM_distinctid=1771edaaa112f6-09314889f1554d-31346d-144000-1771edaaa1274c; CNZZDATA1279010528=282746784-1611130174-%7C1611130174; _trs_uv=kk55fksq_3485_a0bl; _trs_ua_s_1=kk55fksq_3485_5h0h; mbdInit=Initialized',
        # 起始地址。
        "start_url": "https://www.jhnews.com.cn/",
        # 首页头条新闻
        "headline_news": ['//*[@id="widget314"]/h3/a'],
        # 轮播信息
        "banner_news": ['//*[@id="swiper1"]/div[1]/div/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="widget315"]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[4]/div/ul/li/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/t\d+_\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                # {"xpath": '//*[@id="main"]/div[1]/div[3]/text()', },
                {"xpath": '//h1/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[6]/div/div[2]/div[2]', },
                # {"xpath": '//*[@id="c"]//tr[4]/td', },
                # {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '/html/body/div[6]/div/div[2]/div[1]/p[2]/text()',
                 "regex": r"源[:：](.*)"
                 },
                #
                # {"xpath": '//div[@class="fz_xx"]/span[2]/text()',
                #  "regex": r"来源[:：](.*?)\d"
                #  },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '/html/body/div[6]/div/div[2]/div[1]/p[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 衢州传媒网
    {
        "platformName": "衢州传媒网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '',
        # 起始地址。
        "start_url": "http://www.qz123.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="topWrap"]/div/div[3]/div[1]/p/a'],
        # 轮播信息
        "banner_news": ['//*[@id="topWrap"]/div/div[4]/div[1]/div/div[1]/div/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="topWrap"]/div/div[4]/div[2]/ul//a'],
        # 导航信息
        "channel_info_xpath": ['//div[@class="dhcont"]/div[1]/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\w+_\w+_\d+.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                # {"xpath": '//*[@id="main"]/div[1]/div[3]/text()', },
                {"xpath": '/html/body/div[5]/div/div/div/div[1]/p[1]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[5]/div/div/div/div[1]/div[2]', },
                # {"xpath": '//*[@id="c"]//tr[4]/td', },
                # {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                # {"xpath": '/html/body/div[6]/div/div[2]/div[1]/p[2]/text()',
                #  "regex": r"源[:：](.*)"
                #  },
                #
                # {"xpath": '//div[@class="fz_xx"]/span[2]/text()',
                #  "regex": r"来源[:：](.*?)\d"
                #  },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '/html/body/div[5]/div/div/div/div[1]/div[1]/div/span[3]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 台州在线
    {
        "platformName": "台州在线",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '',
        # 起始地址。
        "start_url": "http://www.576tv.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="content"]/div[2]/div[1]/div[1]/div[1]/ul/li/a'],
        # 轮播信息
        "banner_news": ['//*[@id="content"]/div[2]/div[1]/div[1]/div[2]/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="content"]/div[2]/div[1]/div[1]/div[3]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="header"]/div[2]/div/ul/li[2]/div/ul[1]/li//a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/Program/\d+.html",
            # r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '//div[@class="art_title"]/h2/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="playerBox"]', },
                {"xpath": '///*[@id="content"]/div[3]/div[3]', },
                # {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="content"]/div[1]/div[2]/div/a/text()',
                 # "regex": r"源[:：](.*)浏览"
                 },
                #
                # {"xpath": '//div[@class="fz_xx"]/span[2]/text()',
                #  "regex": r"来源[:：](.*?)\d"
                #  },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '//*[@id="content"]/div[1]/div[2]/div/text()',
                 "regex": r"时间[:：](\d+.*\d+)\s"
                 },
                # {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中国台州网
    {
        "platformName": "中国台州网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '',
        # 起始地址。
        "start_url": "http://www.taizhou.com.cn/index.htm",
        # 首页头条新闻
        "headline_news": ['//*[@id="content"]/div[2]/div[1]/div[1]/div[1]/ul/li/a'],
        # 轮播信息
        "banner_news": ['//*[@id="turn"]/ul[1]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div/div[9]/div[1]/div//a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div/div[6]//a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/.*?\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                {"xpath": '//td[@class="black30"]/text()', },
                {"xpath": '//h1[@class="black30 title"]//text()', },
            ],
            "content": [
                {"xpath": '//div[@class="article-content"]', },
                {"xpath": '//td[@class="black14"]', },
                # {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": 'string(//*[@id="source_baidu"])',
                 "regex": r"源[:：](.*)"
                 },
                #
                # {"xpath": '//div[@class="fz_xx"]/span[2]/text()',
                #  "regex": r"来源[:：](.*?)\d"
                #  },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '//*[@id="pubtime_baidu"]/text()',
                 # "regex": r"时间[:：](\d+.*\d+)\s"
                 },
                # {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },

    # 1/21    完成20个
    # 宁波市政府网
    {
        "platformName": "宁波市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'zh_choose=n; SERVERID=e741bbf83b6f24e79f118d965207c05f|1611049932|1611049868',
        # 起始地址。
        "start_url": "http://www.ningbo.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//p[@class="big"]/a'],
        # 轮播信息
        "banner_news": ['//div[@class="bx-viewport"]/div/div/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['//div[@class="first_right fr"]/div[@class="tit2 cf"]/p/a'],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\w+_\d+_\d+.html",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//*[@id="c"]//tr[1]/td/text()', },
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div[1]/div/div/div[2]/div[1]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="c"]//tr[4]', },
                {"xpath": '//div[@class="zoom"]', },
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//ul[@class="list"]/li[3]/text()',
                 "regex": r"来源[:：](.*)"
                 },

                {"xpath": '//div[@class="sub-title"]/span[3]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//ul[@class="list"]/li[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//div[@class="sub-title"]/span[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '/html/body/div[3]/div[1]/div/div/div[2]/div[2]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
            ],
            "authors": [],
            "summary": [],
        }
    },
    # 丽水门户
    {
        "platformName": "丽水门户",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '',
        # 起始地址。
        "start_url": "http://www.lishui.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//*[@id="zfzxlist1"]/li/a'],
        # 轮播信息
        "banner_news": ['//*[@id="barrierfree_container"]/div[5]/div[2]/div[1]/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="zfzxlist2"]/li/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="zfzx5"]/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\w+_\d+_\d+.html",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//div[@class="xl_title"]/text()', },
                {"xpath": '//h1/text()', },
            ],
            "content": [
                {"xpath": '//div[@class="TRS_Editor"]', },
                {"xpath": '//*[@id="c"]//tr[4]/td', },
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//div[@class="xl_doc"]/span[2]/text()',
                 "regex": r"源[:：](.*)"
                 },

                {"xpath": '//*[@id="c"]//tr[3]/td/ul/li[3]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="fz_xx"]/span[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//div[@class="xl_doc"]/span[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },

            ],
            "authors": [],
            "summary": [],

        }
    },
    # 丽水网
    {
        "platformName": "丽水网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_trs_uv=kk68a0no_284_hhkf; _trs_ua_s_1=kk68a0no_284_5goj',
        # 起始地址。
        "start_url": "http://www.lsnews.com.cn/",
        # 首页头条新闻
        "headline_news": ['//*[@id="widget402"]/li/a'],
        # 轮播信息
        "banner_news": ['//*[@id="splx__"]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="widget71"]/li/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="mainNewsMain"]/div/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/t\d+_\d+.shtm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//*[@id="newsTitle"]/text()', },
                {"xpath": '/html/body/table[4]//tr/td/table//tr[1]/td/div/text()', },
            ],
            "content": [
                {"xpath": '//td[@class="content"]', },
                {"xpath": '//td[@class="wzwz"]', },
                # {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '/html/body/table[4]//tr/td[1]/table//tr[4]/td/div/span[1]/text()',
                 "regex": r"源[:：](.*)"
                 },
                #
                {"xpath": '/html/body/table[4]//tr/td/table//tr[2]/td/div/text()',
                 "regex": r"来源[:：](.*)"
                 },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '/html/body/table[4]//tr/td[1]/table//tr[4]/td/div/span[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '/html/body/table[4]//tr/td/table//tr[2]/td/div/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],

        }
    },
    # 舟山市政府网
    {
        "platformName": "舟山市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_trs_uv=kk69oias_47_doiu; _trs_ua_s_1=kk69oias_47_e2s; _gscu_10725743=11197989rvyixi29; _gscbrs_10725743=1; SERVERID=e741bbf83b6f24e79f118d965207c05f|1611198560|1611197984; _gscs_10725743=11197989y0v9p229|pv:8',
        # 起始地址。
        "start_url": "http://www.zhoushan.gov.cn/col/col1275904/index.html",
        # 首页头条新闻
        "headline_news": ['//*[@id="con-one-1"]/div/ul/li//a'],
        # 轮播信息
        "banner_news": ['/html/body/div[4]/div/div[1]/div[1]/div/div/ul[1]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="con-two-2"]/div/ul/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="two1"]/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/\d+/\d+/\w+_\d+_\d+.html",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//div[@class="sp_title"]/text()', },
                {"xpath": '//h1/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="zoom"]', },
                {"xpath": '//*[@id="c"]//tr[4]/td', },
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="barrierfree_container"]/div[5]/div/div[2]/font[2]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="pages-date"]/span/text()',
                 "regex": r"源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//*[@id="barrierfree_container"]/div[5]/div/div[2]/font[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//div[@class="pages-date"]/text()',
                 "regex": r"(\d+.*\d+)"
                 },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 舟山网
    {
        "platformName": "舟山网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '',
        # 起始地址。
        "start_url": "http://www.zhoushan.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[8]/div/div[1]/h2/a'],
        # 轮播信息
        "banner_news": ['/html/body/div[9]/div[1]/div[1]/dl/dd[2]/div/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[9]/div[1]/div[2]/dl/dd/ul[1]/li/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[4]/div/ul/li[1]/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+/t\d+_\d+.shtm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[4]/div/div/div[1]/div[2]/div[1]/h3/text()', },
                {"xpath": '/html/body/div[3]/div/h3/text()', },
                {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[4]/div/div/div[1]/div[2]/div[2]', },
                {"xpath": '//*[@id="video-container"]', },
                {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="srcname"]/text()',
                 # "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//*[@id="docreltime"]/text()',
                 "regex": r"源[:：](.*)发布"
                 },

            ],
            "pubTime": [
                {"xpath": '/html/body/div[4]/div/div/div[1]/div[2]/div[1]/div/span[1]/text()',
                 # "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[3]/div/div/span[3]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="docreltime"]/text()',
                 "regex": r"(\d+.*\d+)"
                 },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 无限舟山
    {
        "platformName": "无线舟山",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '',
        # 起始地址。
        "start_url": "https://www.wifizs.cn/",
        # 首页头条新闻
        "headline_news": ['//*[@id="body_wrapper"]/div[2]/div[1]/div[1]/div[2]/div[2]//a'],
        # 轮播信息
        "banner_news": [''],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="body_wrapper"]/div[2]/div[1]/div[2]/div[3]/ul//a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="head_wrapper"]/div[3]/div/div[1]/ul/li[2]/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+\d+/\d+-\d+-\d+/\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="body_wrapper"]/div/div[1]/div[2]/div/div[2]', },
                {"xpath": '//*[@id="body_wrapper"]/div/div[2]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="body_wrapper"]/div/div[1]/div[2]/div/div[1]/div/span[1]/span[1]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"源[:：](.*)发布"
                #  },

            ],
            "pubTime": [
                {"xpath": '//*[@id="body_wrapper"]/div/div[1]/div[2]/div/div[1]/div/span[1]/span[3]/text()',
                 # "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '/html/body/div[3]/div/div/span[3]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易黑龙江
    {
        "platformName": "网易黑龙江",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://hlj.news.163.com",
        # 首页头条新闻
        "headline_news": ['//*[@id="ne_wrap"]/body/div[3]/div[7]/div[2]//a'],
        # 轮播信息
        "banner_news": ['//*[@id="ne_wrap"]/body/div[3]/div[7]/div[1]/ul[1]/li/div/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="ne_wrap"]/body/div[3]/div[8]/div[2]/ul/li[7]/div/div/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="ne_wrap"]/body/div[3]/div[6]/div[2]/ul/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                # {"xpath": '//*[@id="body_wrapper"]/div/div[2]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="container"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"源[:：](.*)发布"
                #  },

            ],
            "pubTime": [
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '/html/body/div[3]/div/div/span[3]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易海南
    {
        "platformName": "网易海南",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://hn.news.163.com/",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": ['//*[@id="ne_wrap"]/body/div[7]/div/ul[1]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="ne_wrap"]/body/div[8]/div[2]/ul/li[2]/div/div/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="ne_wrap"]/body/div[6]/div[2]/ul/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                # {"xpath": '//*[@id="body_wrapper"]/div/div[2]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]//text()',
                 "regex": r"源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易陕西
    {
        "platformName": "网易陕西",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://shanxi.news.163.com/",
        # 首页头条新闻
        "headline_news": ['//ul[@class="hotNews-list2"]/li/a'],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//ul[@class="newsdata_list noloading"]/li/div/div/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                # {"xpath": '//*[@id="body_wrapper"]/div/div[2]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]//text()',
                 "regex": r"源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易甘肃
    {
        "platformName": "网易甘肃",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://gs.news.163.com/",
        # 首页头条新闻
        "headline_news": ['//ul[@class="hotNews-list2"]//a'],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="test_temple"]/div/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                # {"xpath": '//*[@id="body_wrapper"]/div/div[2]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]//text()',
                 "regex": r"源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易云南
    {
        "platformName": "网易云南",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://yn.news.163.com/",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//ul[@class="newsdata_list noloading"]/li/div/div/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                # {"xpath": '//*[@id="body_wrapper"]/div/div[2]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]//text()',
                 "regex": r"源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易贵州
    {
        "platformName": "网易贵州",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://gz.news.163.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="ne_wrap"]/body/div[6]/div[3]/ul[2]/li/a'],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="test_temple"]/div/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="caozhi_wrap"]/div[2]/div[2]/div[2]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)举报"
                 },
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易内蒙古
    {
        "platformName": "网易内蒙古",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://hhht.news.163.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="ne_wrap"]/body/div[6]/div[3]/ul[1]/li/a'],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="test_temple"]/div/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="caozhi_wrap"]/div[2]/div[2]/div[2]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)举报"
                 },
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易广西
    {
        "platformName": "网易广西",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "http://gx.news.163.com",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//ul[@class="newsdata_list noloading bgloading"]/li/div/div/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="caozhi_wrap"]/div[2]/div[2]/div[2]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)举报"
                 },
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易新疆
    {
        "platformName": "网易新疆",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "http://xj.news.163.com",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="test_temple"]/div/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="caozhi_wrap"]/div[2]/div[2]/div[2]', },
                {"xpath": '//*[@id="endText"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)举报"
                 },
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易江苏
    {
        "platformName": "网易江苏",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://js.news.163.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="ne_wrap"]/body/div[5]/div[3]/ul[2]/li/a'],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="ne_wrap"]/body/div[5]/div[2]/ul/li/div/div/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="caozhi_wrap"]/div[2]/div[2]/div[2]', },
                {"xpath": '/html/body/div[3]/div[2]/div[1]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)举报"
                 },
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[3]/div[1]/div[2]/span/text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易河南
    {
        "platformName": "网易河南",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "http://henan.163.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="ne_wrap"]/body/div[4]/div[4]/div[4]/div[2]/div//a'],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="ne_wrap"]/body/div[4]/div[4]/div[5]/div[1]/div[2]/ul[1]/li/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="caozhi_wrap"]/div[2]/div[2]/div[2]', },
                {"xpath": '//*[@id="endText"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)举报"
                 },
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易浙江
    {
        "platformName": "网易浙江",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "http://henan.163.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="ne_wrap"]/body/div[5]/div[3]/ul[2]/li/a'],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="test_temple"]/div/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="caozhi_wrap"]/div[2]/div[2]/div[2]', },
                {"xpath": '//*[@id="endText"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)举报"
                 },
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易广东
    {
        "platformName": "网易广东",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://gd.news.163.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="ne_wrap"]/body/div[5]/div//a'],
        # 轮播信息
        "banner_news": ['//*[@id="ne_wrap"]/body/div[5]/div[1]/ul[1]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="ne_wrap"]/body/div[6]/div[1]/div[2]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="caozhi_wrap"]/div[2]/div[2]/div[2]', },
                {"xpath": '//*[@id="endText"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)举报"
                 },
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易福建
    {
        "platformName": "网易福建",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://fj.news.163.com",
        # 首页头条新闻
        "headline_news": ['//*[@id="ne_wrap"]/body/div[3]/div[8]/div[3]/ul[2]/li/a'],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="ne_wrap"]/body/div[3]/div[8]/div[2]/ul/li/div/div/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="caozhi_wrap"]/div[2]/div[2]/div[2]', },
                {"xpath": '//*[@id="endText"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)举报"
                 },
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },

    # 1/22
    # 网易北京
    {
        "platformName": "网易北京",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://bj.news.163.com",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="test_temple"]/div/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="caozhi_wrap"]/div[2]/div[2]/div[2]', },
                {"xpath": '//*[@id="endText"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)举报"
                 },
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易安徽
    {
        "platformName": "网易安徽",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://ah.news.163.com/",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="test_temple"]/div/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="caozhi_wrap"]/div[2]/div[2]/div[2]', },
                {"xpath": '//*[@id="endText"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)举报"
                 },
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易宁夏
    {
        "platformName": "网易宁夏",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://ningxia.news.163.com/",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="ne_wrap"]/body/div[5]/div[2]/ul/li/div/div/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="caozhi_wrap"]/div[2]/div[2]/div[2]', },
                {"xpath": '//*[@id="endText"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)举报"
                 },
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易大连
    {
        "platformName": "网易大连",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://dl.news.163.com",
        # 首页头条新闻
        "headline_news": ['//ul[@class="hotNews-list2"]/li/a'],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="test_temple"]/div/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="caozhi_wrap"]/div[2]/div[2]/div[2]', },
                {"xpath": '//*[@id="endText"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)举报"
                 },
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易湖南
    {
        "platformName": "网易湖南",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://hunan.news.163.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="ne_wrap"]/body/div[5]/div[2]//a'],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="ne_wrap"]/body/div[6]/div[2]/ul/li/div/div/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="caozhi_wrap"]/div[2]/div[2]/div[2]', },
                {"xpath": '//*[@id="endText"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)举报"
                 },
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易四川
    {
        "platformName": "网易四川",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://sc.news.163.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="ne_wrap"]/body/div[5]/div[2]//a'],
        # 轮播信息
        "banner_news": ['//*[@id="ne_wrap"]/body/div[5]/div[1]/ul[1]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//ul[@class="new-text"]/li/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="caozhi_wrap"]/div[2]/div[2]/div[2]', },
                {"xpath": '//*[@id="endText"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)举报"
                 },
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易重庆
    {
        "platformName": "网易重庆",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://chongqing.163.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="ne_wrap"]/body/div[6]/div[3]/ul[2]/li/a'],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="test_temple"]/div/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="caozhi_wrap"]/div[2]/div[2]/div[2]', },
                {"xpath": '//*[@id="endText"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)举报"
                 },
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易湖北
    {
        "platformName": "网易湖北",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://hb.news.163.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="ne_wrap"]/body/div[5]/div[2]//a'],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="ne_wrap"]/body/div[6]/div[2]/ul/li/div/div/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="caozhi_wrap"]/div[2]/div[2]/div[2]', },
                {"xpath": '//*[@id="endText"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)举报"
                 },
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易上海
    {
        "platformName": "网易上海",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://sh.news.163.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="ne_wrap"]/body/div[6]/div[3]/ul[2]/li/a'],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="test_temple"]/div/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="caozhi_wrap"]/div[2]/div[2]/div[2]', },
                {"xpath": '//*[@id="endText"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)举报"
                 },
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易山西
    {
        "platformName": "网易山西",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://sx.news.163.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="ne_wrap"]/body/div[3]/div[3]/div[2]/div[8]/div[3]/div[1]/div/ul/li/a'],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="test_temple"]/div/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="caozhi_wrap"]/div[2]/div[2]/div[2]', },
                {"xpath": '//*[@id="endText"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)举报"
                 },
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易吉林
    {
        "platformName": "网易吉林",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://jl.news.163.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="ne_wrap"]/body/div[5]/div[2]/div/div/a'],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="test_temple"]/div/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="caozhi_wrap"]/div[2]/div[2]/div[2]', },
                {"xpath": '//*[@id="endText"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)举报"
                 },
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易江西
    {
        "platformName": "网易江西",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://jx.news.163.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="ne_wrap"]/body/div[7]/div[3]/ul[2]/li/a'],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="test_temple"]/div/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="caozhi_wrap"]/div[2]/div[2]/div[2]', },
                {"xpath": '//*[@id="endText"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)举报"
                 },
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 网易山东
    {
        "platformName": "网易山东",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '_ntes_nnid=19b338322130572dcc7be7e17691024f,1611122151692; UM_distinctid=1771e5d1298ab0-0e282251161051-31346d-144000-1771e5d1299ca1; ne_analysis_trace_id=1611208006982; s_n_f_l_n3=b80c4c22d74c8d1e1611208006984; _ntes_nuid=19b338322130572dcc7be7e17691024f; vinfo_n_f_l_n3=b80c4c22d74c8d1e.1.0.1611208006984.0.1611208063996',
        # 起始地址。
        "start_url": "https://sd.news.163.com/",
        # 首页头条新闻
        "headline_news": ['//*[@id="ne_wrap"]/body/div[7]/div[2]//a'],
        # 轮播信息
        "banner_news": ['//ul[@class="focus-ul"]/li//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="ne_wrap"]/body/div[8]/div[2]/ul/li/div/div/a'],
        # 导航信息
        "channel_info_xpath": ['//ul[@class="top-nav"]/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\d+/\d+/\d+/.*?.htm",
            r"https?://[\w\-\.]+/dy/article/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '/html/body/div[3]/div/h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="caozhi_wrap"]/div[2]/div[2]/div[2]', },
                {"xpath": '//*[@id="endText"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)举报"
                 },
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"源[:：](.*)"
                 },
                {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//div[@class="post_info"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '//div[@class="post_time_source"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中国发展网
    {
        "platformName": "中国发展网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '__51cke__=; UM_distinctid=17728c124008e5-0c898323fe9dde-31346d-144000-17728c12401b46; Hm_lvt_903b0137299475a075386b5d6719d33d=1611296492; bdshare_firstime=1611296492570; CNZZDATA1260924627=71246949-1611291514-%7C1611296917; __tins__15133790=%7B%22sid%22%3A%201611299365652%2C%20%22vd%22%3A%202%2C%20%22expires%22%3A%201611301183243%7D; __51laig__=5; Hm_lpvt_903b0137299475a075386b5d6719d33d=1611299385; sid=160219323.95160290.1611299386720.1611299428254',
        # 起始地址。
        "start_url": "http://www.chinadevelopment.com.cn/",
        # 首页头条新闻
        "headline_news": ['//div[@class="toutiao1"]/h1/a'],
        # 轮播信息
        "banner_news": ['//div[@class="slider-wrapper"]/div/div//h2/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="fgwsf1"]/ul[2]/li/dl/dt/a'],
        # 导航信息
        "channel_info_xpath": ['//div[@class="nav"]/ul[@class="menu_con"]//a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/[a-zA-Z]+/\w+/\d+/\d+/\d+.shtml",
            r"https?://[\w\-\.]+/[a-zA-Z]+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                {"xpath": '//h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//div[@class="article-detail-inner article-relevance w660 ov"]', },
                {"xpath": '//div[@class="content article-content"]', },
                {"xpath": '//div[@class="content-article"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//span[@class="source fl-l"]/text()',
                 # "regex": r"源[:：](.*)举报"
                 },
                # {"xpath": '//div[@class="post_info"]//text()',
                #  "regex": r"源[:：](.*)"
                #  },
                # {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                #  "regex": r"来源[:：](.*)"
                #  },
                # {"xpath": '//div[@class="post_time_source"]//text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '//span[@class="date fl-l"]/text()',
                 # "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
                # {"xpath": '//div[@class="post_time_source"]//text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中国工信部
    {
        "platformName": "中国工信部",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'SF_cookie_1=31501425',
        # 起始地址。
        "start_url": "https://www.miit.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//*[@id="barrierfree_container"]/div[4]/div/div[2]/div[2]/ul[1]/li/a'],
        # 轮播信息
        "banner_news": ['//*[@id="slideBox"]/div[2]/div[1]/div/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="barrierfree_container"]/div[4]/div/div[2]/div[2]/ul[2]/li/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="new_nav"]/a[3]'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\d+/\w+_.*?.html",
            # r"https?://[\w\-\.]+/[a-zA-Z]+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                {"xpath": '//h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="con_con"]', },
                # {"xpath": '//div[@class="content article-content"]', },
                # {"xpath": '//div[@class="content-article"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="cinfo center"]/span[2]/text()',
                 "regex": r"源[:：](.*)"
                 },
                # {"xpath": '//div[@class="post_info"]//text()',
                #  "regex": r"源[:：](.*)"
                #  },
                # {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                #  "regex": r"来源[:：](.*)"
                #  },
                # {"xpath": '//div[@class="post_time_source"]//text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '//*[@id="con_time"]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
                # {"xpath": '//div[@class="post_time_source"]//text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中国监证会
    {
        "platformName": "中国监证会",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'acw_tc=ca8f643616113014061182039edb496628a36e0a679bca88d6f19dfd32',
        # 起始地址。
        "start_url": "http://www.csrc.gov.cn/pub/newsite/",
        # 首页头条新闻
        "headline_news": ['//*[@id="con_1_1"]/div[1]/a'],
        # 轮播信息
        "banner_news": ['//*[@id="YNews"]/dl//a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="con_1_1"]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div/div/div[4]/div[2]/div[1]/div[2]/div[1]/ul/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\w+/\d+/t\d+_\d+.html",
            # r"https?://[\w\-\.]+/[a-zA-Z]+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//div[@class="title"]/text()', },
                # {"xpath": '//h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//div[@class="content"]/div[3]', },
                # {"xpath": '//div[@class="content article-content"]', },
                # {"xpath": '//div[@class="content-article"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="content"]/div[2]/span[3]/text()',
                 "regex": r"源[:：](.*)"
                 },
                # {"xpath": '//div[@class="post_info"]//text()',
                #  "regex": r"源[:：](.*)"
                #  },
                # {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                #  "regex": r"来源[:：](.*)"
                #  },
                # {"xpath": '//div[@class="post_time_source"]//text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '//div[@class="content"]/div[2]/span[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
                # {"xpath": '//div[@class="post_time_source"]//text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }},

    # 1/23 15 
    # 中国就业网
    {
        "platformName": "中国就业网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'route=22e0e571b222aca3f31ab6d5d01784f1; 1_vq=2',
        # 起始地址。
        "start_url": "http://chinajob.mohrss.gov.cn/",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": ['/html/body/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/div/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[1]/div[2]/div[2]/ul/li[2]/ul/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/c/\d+-\d+-\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/[a-zA-Z]+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//div[@class="detail_con"]/h4/text()', },
                # {"xpath": '//h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//div[@class="detail_article"]', },
                # {"xpath": '//div[@class="content article-content"]', },
                # {"xpath": '//div[@class="content-article"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="fl link"]/text()',
                 # "regex": r"源[:：](.*)"
                 },
                # {"xpath": '//div[@class="post_info"]//text()',
                #  "regex": r"源[:：](.*)"
                #  },
                # {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                #  "regex": r"来源[:：](.*)"
                #  },
                # {"xpath": '//div[@class="post_time_source"]//text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '//div[@class="fl date"]/text()',
                 # "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
                # {"xpath": '//div[@class="post_time_source"]//text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中国教育部
    {
        "platformName": "中国教育部",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'wdcid=7e76e0d5abeeec31; wdlast=1611302840',
        # 起始地址。
        "start_url": "http://www.moe.gov.cn/",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": ['//*[@id="jyb_index_focus"]/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="eight_con2"]/div[1]/div/ul/li//a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="one_con2"]/dd/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+_\w+/\w+_\w+/\w+/\d+/t\d+_\d+.html",
            r"https?://[\w\-\.]+/\w+_\w+/\w+/\d+/t\d+_\d+.html",
            # r"https?://[\w\-\.]+/[a-zA-Z]+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//h1/text()', },
                # {"xpath": '//h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//div[@class="TRS_Editor"]', },
                # {"xpath": '//div[@class="content article-content"]', },
                # {"xpath": '//div[@class="content-article"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//*[@id="moe-detail-box"]/div[1]/text()',
                 "regex": r"源[:：](.*)"
                 },
                # {"xpath": '//div[@class="post_info"]//text()',
                #  "regex": r"源[:：](.*)"
                #  },
                # {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                #  "regex": r"来源[:：](.*)"
                #  },
                # {"xpath": '//div[@class="post_time_source"]//text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '//*[@id="moe-detail-box"]/div[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
                # {"xpath": '//div[@class="post_time_source"]//text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 吕梁市政府网
    {
        "platformName": "吕梁市政府网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'web_m2o_dtradio_com_cn=eyJpdiI6IlBUQ050U1RuXC8zcjRSVks3N1ZlRzFnPT0iLCJ2YWx1ZSI6InFuTGMweCtZdXQ1WWpHUlJhNCtsXC9kQ01OVHpWTUU3QTd2RUJSSjV0UkNFWjJEXC9xVXBPTWVFZnI4T1cwSDFnOVlsSERsNlpqazhDSXpmekpYNmFYeHc9PSIsIm1hYyI6ImM2NDQ2ODdjYjcyNGNiYzA5YzNiNTQ3YjZlMzBiZWQ0ZWY4ZmUxY2ZhOGFlMzNkODMxYmE3MDhhNDRhMDQ2YTkifQ%3D%3D',
        # 起始地址。
        "start_url": "http://www.lvliang.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//*[@id="container"]/div[4]/div/div[3]/ul/li[1]/ul/li/a'],
        # 轮播信息
        "banner_news": ['//*[@id="container"]/div[4]/div/div[1]/div[1]/div/ul[1]/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="container"]/div[4]/div/div[1]/div[2]/div[2]/div[1]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": [''],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+/t\d+_\d+.s?html",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/[a-zA-Z]+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//*[@id="container"]/div[3]/div/div[2]/div[2]/div[1]/h2/text()', },
                {"xpath": '//h1//text()', },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[2]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="container"]/div[3]/div/div[2]/div[2]/div[2]', },
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@id="detail"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//p[@class="x"]//text()',
                 "regex": r"来源[:：](.*)更新"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*?)\d"
                 },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[2]/span/text()',
                # "regex": r"来源[:：](.*)"
                # },

            ],
            "pubTime": [
                {"xpath": '//p[@class="x"]//text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[1]/span/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中国人社部
    {
        "platformName": "中国人社部",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'UM_distinctid=177291dae7b8c1-0aef3a5611d889-31346d-144000-177291dae7cb91; CNZZDATA1279432962=2137114698-1611300096-%7C1611300096; Hm_lvt_64e46e3f389bd47c0981fa5e4b9f2405=1611302547; __FTabceffgh=2021-1-22-16-2-27; __NRUabceffgh=1611302547197; __RTabceffgh=2021-1-22-16-2-27; Hm_lpvt_64e46e3f389bd47c0981fa5e4b9f2405=1611303717',
        # 起始地址。
        "start_url": "http://www.mohrss.gov.cn/",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": ['/html/body/div[2]/div[1]/div[3]/div[1]/div[1]/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[2]/div[1]/div[3]/div[1]/div[2]/div/div[1]/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\d+/t\d+_\d+.html",
            # r"https?://[\w\-\.]+/\w+_\w+/\w+/\d+/t\d+_\d+.html",
            # r"https?://[\w\-\.]+/[a-zA-Z]+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//div[@class="insMainConTitle_b"]/text()', },
                # {"xpath": '//h3/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//div[@class="insMainConTxt"]', },
                # {"xpath": '//div[@class="content article-content"]', },
                # {"xpath": '//div[@class="content-article"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '/html/head/meta[22]/@content',
                 },
                # {"xpath": '//*[@id="contain"]/div[1]/div[2]//text()',
                #  "regex": r"来源[:：](.*)"
                #  },
                # {"xpath": '//div[@class="post_time_source"]//text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '//*[@id="div1"]/div[1]/div[1]/div[2]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//*[@id="container"]/div[1]/div[2]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
                # {"xpath": '//div[@class="post_time_source"]//text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中国国家旅游局
    {
        "platformName": "中国国家旅游局",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'yfx_c_g_u_id_10001331=_ck21012216340718757930767397042; yfx_f_l_v_t_10001331=f_t_1611304447868__r_t_1611304447868__v_t_1611304447868__r_c_0; _trs_uv=kk812d1s_4419_efui; _trs_ua_s_1=kk812d1s_4419_aacr',
        # 起始地址。
        "start_url": "https://www.mct.gov.cn/",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": ['//*[@id="part1"]/div[1]/div/div[1]/div/a'],
        # 轮播旁边新闻
        "banner_news_side": [''],
        # 导航信息
        "channel_info_xpath": ['//*[@id="part1"]/div[2]/ul/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+/t\d+_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/[a-zA-Z]+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[4]/div/div[1]/text()', },
                {"xpath": '//h1/text()', },
                # {"xpath": '//*[@id="doctitle"]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="zoom"]', },
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//div[@class="content-article"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '/html/body/div[4]/div/div[3]/font[2]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },
                # {"xpath": '//div[@class="post_time_source"]//text()',
                #  "regex": r"来源[:：](.*)"
                #  },

            ],
            "pubTime": [
                {"xpath": '/html/body/div[4]/div/div[3]/font[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '//div[@class="post_time_source"]//text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 国家广播电视总局
    {
        "platformName": "国家广播电视总局",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'BIGipServersarft-web=174368960.20480.0000',
        # 起始地址。
        "start_url": "http://www.nrta.gov.cn/col/col111/index.html",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": ['//*[@id="all"]/div/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="con_two_1"]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['//div[@class="onelist left"]/div[@class="hdlefttit"]/ul/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/c_\d+.htm",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/[a-zA-Z]+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//td[@class="title"]/text()', },
                {"xpath": '//h1/text()', },
                {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[2]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="c"]', },
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '//*[@id="detail"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//*[@id="c"]//tr[2]/td/table//tr/td[2]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[2]/span/text()',
                 # "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//*[@id="c"]//tr[2]/td/table//tr/td[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[1]/span/text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中国住建部
    {

        "platformName": "中国住建部",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '',
        # 起始地址。
        "start_url": "http://www.mohurd.gov.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/table//tr[3]/td[1]/table//tr[1]/td[3]/table[3]//tr[2]/td/table//tr//a'],
        # 轮播信息
        "banner_news": [''],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="ulNews"]/tbody/tr//a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/table//tr[3]/td[1]/table//tr[1]/td[3]/table[3]//tr[5]/td/table//tr/td[2]/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/t\d+_\d+.htm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/[a-zA-Z]+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/table//tr[2]/td/table[2]//tr[2]/td/table//tr[1]/td/text()', },
                {"xpath": '//h1//text()', },
                {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[2]/text()', },
            ],
            "content": [
                {"xpath": '//div[@class="union"]', },
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                {"xpath": '//*[@id="detail"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//*[@id="c"]//tr[2]/td/table//tr/td[2]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[2]/span/text()',
                 # "regex": r"来源[:：](.*)"
                 },

            ],
            "pubTime": [
                {"xpath": '//*[@id="c"]//tr[2]/td/table//tr/td[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[1]/span/text()',
                 "regex": r"(\d+.*\d+)"
                 },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中央统战部
    {
        "platformName": "中央统战部",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '',
        # 起始地址。
        "start_url": "http://www.zytzb.gov.cn/html/index.html",
        # 首页头条新闻
        "headline_news": ['/html/body/div[2]/div/div[1]/h1/a'],
        # 轮播信息
        "banner_news": ['//*[@id="slideBox"]/div[2]/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[2]/div/div[2]/div[2]/ul[1]/li/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="header_pub"]/div[2]/div/ul/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+.jhtm",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/[a-zA-Z]+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//div[@class="detail_title"]//text()', },
                # {"xpath": '//h1//text()', },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[2]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@id="detail"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '//div[@class="laiyuan fl"]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[2]/span/text()',
                # "regex": r"来源[:：](.*)"
                # },

            ],
            "pubTime": [
                {"xpath": '//div[@class="date fl"]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[1]/span/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 国务院发展研究中心
    {
        "platformName": "国务院发展研究中心",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '',
        # 起始地址。
        "start_url": "https://www.drc.gov.cn/default.aspx",
        # 首页头条新闻
        "headline_news": ['//*[@id="body"]/div[3]/div/div[1]/ul/li[1]/a'],
        # 轮播信息
        "banner_news": ['//*[@id="D1pic1"]/div/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="dtbox_current_2"]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": [''],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/DocView.aspx\?chnid=\d+&leafid=\d+&docid=\d+",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/[a-zA-Z]+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '//*[@id="MainContent_docSubject"]/text()', },
                # {"xpath": '//h1//text()', },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[2]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="MainContent_docContent"]', },
                # {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@id="detail"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                # {"xpath": '//div[@class="laiyuan fl"]/text()',
                #  "regex": r"来源[:：](.*)"
                #  },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[2]/span/text()',
                # "regex": r"来源[:：](.*)"
                # },

            ],
            "pubTime": [
                {"xpath": '//*[@id="MainContent_docAuthor"]/text()',
                 # "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[1]/span/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中国司法部
    {
        "platformName": "中国司法部",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '',
        # 起始地址。
        "start_url": "http://www.moj.gov.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[7]/h1/a'],
        # 轮播信息
        "banner_news": ['/html/body/div[8]/div/div[1]/div[1]/div/ul/li/a'],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[8]/div/div[1]/div[2]/div/div[2]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": [''],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+-\d+/\d+/\w+_\d+.html",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/[a-zA-Z]+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[4]/div[2]/div[2]/div[2]/text()', },
                {"xpath": '//h1//text()', },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[2]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="content"]', },
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@id="detail"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '/html/body/div[4]/div[2]/div[2]/div[4]/div[1]/span[2]/text()',
                 # "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[2]/span/text()',
                # "regex": r"来源[:：](.*)"
                # },

            ],
            "pubTime": [
                {"xpath": '/html/body/div[4]/div[2]/div[2]/div[4]/div[1]/span[1]/text()',
                 # "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[1]/span/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 国家铁路局
    {
        "platformName": "国家铁路局",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": '',
        # 起始地址。
        "start_url": "http://www.nra.gov.cn/",
        # 首页头条新闻
        "headline_news": ['//*[@id="s1"]/ul/li[1]/a'],
        # 轮播信息
        "banner_news": ['//*[@id="D1pic1"]/div/a'],
        # 轮播旁边新闻
        "banner_news_side": ['//*[@id="div1"]/li/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[1]/div[2]/ul/li[3]/div/dl/dd/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\w+/\d+/t\d+_\d+.shtml",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/[a-zA-Z]+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[4]/div[2]/div[2]/div[2]/text()', },
                {"xpath": '//h1//text()', },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[2]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="Zoom1"]', },
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@id="detail"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '/html/body/div[3]/div/div[1]/span[2]/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[2]/span/text()',
                # "regex": r"来源[:：](.*)"
                # },

            ],
            "pubTime": [
                {"xpath": '/html/body/div[3]/div/div[1]/span[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[1]/span/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 唐山广电网
    {
        "platformName": "唐山广电网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'UM_distinctid=1772d023bdfa77-04ac58285fb6f-31346d-144000-1772d023be010b; CNZZDATA1277739694=1034488468-1611366628-%7C1611366628',
        # 起始地址。
        "start_url": "http://www.tsr.he.cn/",
        # 首页头条新闻
        "headline_news": [''],
        # 轮播信息
        "banner_news": [''],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[3]/div[1]/div/div[2]/div/a'],
        # 导航信息
        "channel_info_xpath": ['//*[@id="Z_Box"]/div[3]/table//tr/td/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/.*?.shtml",
            r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/[a-zA-Z]+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[2]/div/div[1]/div[1]/h4/text()', },
                {"xpath": '//h1//text()', },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[2]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/div[2]/div/div[1]/div[1]/div[2]', },
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@id="detail"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '/html/body/div[2]/div/div[1]/div[1]/div[1]/p//text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                 "regex": r"来源[:：](.*)"
                 },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[2]/span/text()',
                # "regex": r"来源[:：](.*)"
                # },

            ],
            "pubTime": [
                {"xpath": '/html/body/div[2]/div/div[1]/div[1]/div[1]/p/span[1]/text()',
                 # "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[1]/span/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 中国日报网山西记者站
    {
        "platformName": "中国日报网山西记者站",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'USR=okkkoafs%090%091611368580%09http%3A%2F%2Fwww.zjkgdcs.com%2Fdo%2Fhack.php%3Fhack%3Dlogin%26styletype%3Dzjk%26iframeID%3Dhead_loginer; UM_distinctid=1772d0d4366293-02bf440335ea34-31346d-144000-1772d0d43677d2; CNZZDATA1255643442=2102874582-1611364984-%7C1611364984',
        # 起始地址。
        "start_url": "https://sx.chinadaily.com.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[4]/div[1]/div[2]/div[1]/div[2]/h3/a'],
        # 轮播信息
        "banner_news": [''],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[4]/div[1]/div[2]/div/div[1]/div/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[4]/div[1]/div[2]/div[11]/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/\d+/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/[a-zA-Z]+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[2]/div/div[1]/div[1]/h4/text()', },
                {"xpath": '//h1//text()', },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[2]/text()', },
            ],
            "content": [
                {"xpath": '//*[@id="Content"]', },
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@id="detail"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '/html/body/div[5]/div[1]/div[1]/div[1]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[2]/span/text()',
                # "regex": r"来源[:：](.*)"
                # },

            ],
            "pubTime": [
                {"xpath": '/html/body/div[5]/div[1]/div[1]/div[2]/text()',
                 # "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[1]/span/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 大同广播在线
    {

        "platformName": "大同广播在线",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'web_m2o_dtradio_com_cn=eyJpdiI6IlBUQ050U1RuXC8zcjRSVks3N1ZlRzFnPT0iLCJ2YWx1ZSI6InFuTGMweCtZdXQ1WWpHUlJhNCtsXC9kQ01OVHpWTUU3QTd2RUJSSjV0UkNFWjJEXC9xVXBPTWVFZnI4T1cwSDFnOVlsSERsNlpqazhDSXpmekpYNmFYeHc9PSIsIm1hYyI6ImM2NDQ2ODdjYjcyNGNiYzA5YzNiNTQ3YjZlMzBiZWQ0ZWY4ZmUxY2ZhOGFlMzNkODMxYmE3MDhhNDRhMDQ2YTkifQ%3D%3D',
        # 起始地址。
        "start_url": "http://www.dtradio.com.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/div[4]/div[5]/div[2]/p/a'],
        # 轮播信息
        "banner_news": [''],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/div[4]/div[7]/div[1]/div[2]/ul[1]/li/div[1]/div[1]/ul/li/a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/div[3]/div[2]/div/div[3]/ul/li/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\w+/\d+-\d+-\d+/.*?.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/[a-zA-Z]+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/div[2]/div/div[2]/p/text()', },
                {"xpath": '//h1//text()', },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[2]/text()', },
            ],
            "content": [
                {"xpath": '//div[@class="articleContent"]', },
                {"xpath": '//*[@id="UCAP-CONTENT"]', },
                # {"xpath": '//*[@id="detail"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '/html/body/div[5]/div[1]/div[1]/div[1]//text()',
                 "regex": r"来源[:：](.*)"
                 },
                # {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/span/text()',
                #  "regex": r"来源[:：](.*)"
                #  },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[2]/span/text()',
                # "regex": r"来源[:：](.*)"
                # },

            ],
            "pubTime": [
                {"xpath": '/html/body/div[2]/div/div[2]/div/div/span[1]/text()',
                 # "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[1]/span/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },
    # 阳泉新闻网
    {
        "platformName": "阳泉新闻网",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 1,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。
        "sourceImportance": 1,
        # 是否主流媒体。
        "mainMedia": 1,
        "cookie": 'web_m2o_dtradio_com_cn=eyJpdiI6IlBUQ050U1RuXC8zcjRSVks3N1ZlRzFnPT0iLCJ2YWx1ZSI6InFuTGMweCtZdXQ1WWpHUlJhNCtsXC9kQ01OVHpWTUU3QTd2RUJSSjV0UkNFWjJEXC9xVXBPTWVFZnI4T1cwSDFnOVlsSERsNlpqazhDSXpmekpYNmFYeHc9PSIsIm1hYyI6ImM2NDQ2ODdjYjcyNGNiYzA5YzNiNTQ3YjZlMzBiZWQ0ZWY4ZmUxY2ZhOGFlMzNkODMxYmE3MDhhNDRhMDQ2YTkifQ%3D%3D',
        # 起始地址。
        "start_url": "http://www.yqnews.com.cn/",
        # 首页头条新闻
        "headline_news": ['/html/body/table[5]//tr[1]/td[1]/table//tr/td/a'],
        # 轮播信息
        "banner_news": [''],
        # 轮播旁边新闻
        "banner_news_side": ['/html/body/table[6]//tr/td[1]/table[2]//tr/td/table//tr[1]//a'],
        # 导航信息
        "channel_info_xpath": ['/html/body/table[4]//tr/td/table//tr/td/a'],

        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w+/\d+/t\d+_\d+.html",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+/\d+/\w+_\d+.htm",
            # r"https?://[\w\-\.]+/[a-zA-Z]+/\d+/\d+/\d+.shtml",
            # r"https?://[\w\-\.]+/\w+/\d+-\d+-\d+/\d+_\w+.html",
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": '/html/body/table[3]//tr[2]/td/table//tr[2]/td/text()', },
                {"xpath": '//h1//text()', },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[2]/text()', },
            ],
            "content": [
                {"xpath": '/html/body/table[5]//tr[1]/td/table//tr[2]/td', },
                {"xpath": '//div[@class="content_18313"]', },
                # {"xpath": '//*[@id="detail"]', },
                # {"xpath": '/html/body/div[5]', },
                # {"xpath": '//*[@class="content"]', },
            ],

            "pubSource": [

                {"xpath": '/html/body/table[3]//tr[5]/td[2]/table//tr/td/text()',
                 "regex": r"来源[:：](.*)"
                 },
                {"xpath": '/html/body/div[7]/div[3]/div[1]/div[1]/span[1]/i/text()',
                 "regex": r"来源[:：](.*?)\d"
                 },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[2]/span/text()',
                # "regex": r"来源[:：](.*)"
                # },

            ],
            "pubTime": [
                {"xpath": '/html/body/table[3]//tr[5]/td[1]/table//tr/td/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                {"xpath": '/html/body/div[7]/div[3]/div[1]/div[1]/span[1]/i/text()',
                 "regex": r"(\d+.*\d+)"
                 },
                # {"xpath": '/html/body/div[6]/div[2]/div[3]/div[2]/div/div[3]/span[1]/span/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

                # {"xpath": '//*[@id="docreltime"]/text()',
                #  "regex": r"(\d+.*\d+)"
                #  },

            ],
            "authors": [],
            "summary": [],
        }
    },

]
