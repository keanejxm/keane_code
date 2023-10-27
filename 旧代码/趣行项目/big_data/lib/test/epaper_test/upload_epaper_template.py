# -*- coding:utf-8 -*-
"""
# project:上传报纸模版到数据库
# author: Neil
# date: 2020/10/28

"""
import pymysql
import json


def con_mysql():
    """
    连接数据库
    """
    conmysql = pymysql.connect(
        "192.168.32.18",
        "root",
        "moR7tzWCv$ZYBe*$",
        "big_data_platform")
    cursor = conmysql.cursor()
    return conmysql, cursor


def xpath_rule():
    """
    返回数据体的最新一条。
    """
    temps = [
        {
            "platformName": "广信报",
            "sourceProvince": "江西",
            "sourceCity": "",
            # 1：国家级，2：省级，3：市级，0：商业类网站。
            "sourceLevel": 3,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # %Y-%m/%d，{proxies}。
            "start_url": "http://www.cnepaper.com/srxb/html/%Y-%m/%d/node_74348.htm",
            "cookiestr": "",
            # 版面url。
            "layout_url_xpath": ["//td[@class='default'][@align='left']/a/@href"],
            # 下一版链接
            "layout_next_xpath": ['//a[@class="preart"][@id="ed_next"]/@href'],
            # 版面名称
            "layout_title_xpath": ['//td[@align="left"]/strong/text()'],
            # 版面标签
            "layout_map_xpath": ["//map[@name='PagePicMap']"],
            # 版面图链接
            "layout_map_image_xpath": ["//img[@usemap='#PagePicMap']/@src"],
            "layout_large_image_xpath": [],
            # 版面图链接pdf链接
            "layout_pdf_xpath": ['//td[@align="right"][@valign="center"]/a/@href'],
            # 稿件详情。
            "detail_url_xpath": ["//map[@name='PagePicMap']/area/@href"],
            # 预标题
            "detail_pre_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][1]/td/text()'],
            # 主标题
            "detail_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][2]/td//text()'],
            # 子标题
            "detail_sub_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][3]/td/text()'],
            # 作者
            "detail_author_xpath": [],
            # 正文内容
            "detail_content_xpath": ['//table[@id="newspic"]//table//td | //div[@id="ozoom"]'],
            # 提交时间
            "detail_pubTime_xpath": [],

        },
        # 菏泽日报
        {
            "platformName": "菏泽日报",
            "sourceProvince": "山东",
            "sourceCity": "菏泽",
            "sourceLevel": 3,
            "sourceClassify": 1,
            "sourceImportance": 0,
            "mainMedia": 0,
            "start_url": "http://www.heze.cn/hzrb/pc/layout/%Y%m/%d/node_A1.html",
            "cookiestr": "",
            "layout_url_xpath": ["//ul[@id=\"layoutlist\"]/li/a/@href"],

            "layout_next_xpath": ['//a[@class="nextArt"]/@href'],

            "layout_title_xpath": ['//span[@id="layout"]//text()'],

            "layout_map_xpath": ['//map[@name="PagePicMap"]'],

            "layout_map_image_xpath": ['//img[@usemap="#PagePicMap"]/@src'],
            "layout_large_image_xpath": [],

            "layout_pdf_xpath": ['//div[@class="pull-right"]/a/@href'],

            "detail_url_xpath": ['//map[@name="PagePicMap"]/area/@href'],

            "detail_pre_title_xpath": ['//p[@id="PreTitle"]/text()'],

            "detail_title_xpath": ['//h2[@id="Title"]/text()'],

            "detail_sub_title_xpath": ['//p[@id="SubTitle"]/text()'],

            "detail_author_xpath": [],

            "detail_content_xpath": ['//div[@class="attachment"] | //div[@id="ozoom"]'],
            "detail_pubTime_xpath": [],
        },

        # 10个报纸模板
        # 青州通讯
        {
            "platformName": "青州通讯",
            "sourceProvince": "山东",
            "sourceCity": "青州",
            # 1：国家级，2：省级，3：市级，0：商业类网站。
            "sourceLevel": 3,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # %Y-%m/%d，{proxies}。
            "start_url": "http://epaper.qzxww.com/html/%Y-%m/%d/node_43725.htm",
            "cookiestr": "",
            # 版面url。
            "layout_url_xpath": ['//a[@class="rigth_bmdh_href"]/@href'],
            # 下一版链接
            "layout_next_xpath": ['//a[@id="ed_next"]/@href'],
            # 版面名称
            "layout_title_xpath": ['//td[@id="currentBM"]/strong/text()'],
            # 版面标签
            "layout_map_xpath": ['//div[@id="main-ed-map"]/map'],
            # 版面图链接
            "layout_map_image_xpath": ["//img[@usemap='#PagePicMap']/@src"],
            "layout_large_image_xpath": [],
            # 版面图链接pdf链接
            "layout_pdf_xpath": ['//a[@id="bigbmshowpdf"]/@href'],
            # 稿件详情。
            "detail_url_xpath": ['//div[@id="main-ed-map"]/map/area/@href'],
            # 预标题
            "detail_pre_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][1]/td/text()'],
            # 主标题
            "detail_title_xpath": ['//p[@class="BSHARE_TEXT"]/text()'],
            # 子标题
            "detail_sub_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][3]/td/text()'],
            # 作者
            "detail_author_xpath": [],
            # 正文内容
            "detail_content_xpath": ['//table[@id="newspic"]//table//td | //div[@id="ozoom"]'],
            # 提交时间
            "detail_pubTime_xpath": [],
        },
        # 沂蒙晚报
        {
            "platformName": "沂蒙晚报",
            "sourceProvince": "山东",
            "sourceCity": "",
            # 1：国家级，2：省级，3：市级，0：商业类网站。
            "sourceLevel": 3,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # %Y%m/%d，{proxies}。
            "start_url": "http://ymwb.langya.cn/paper/pc/layout/%Y%m/%d/node_01.html",
            "cookiestr": "",
            # 版面url。
            "layout_url_xpath": ['//div[@class="Therestlist"]//li/a[2]/@href'],
            # 下一版链接
            "layout_next_xpath": ['//div[@class="newsnext"]/a/@href'],
            # 版面名称
            "layout_title_xpath": ['//div[@class="newslisttit"]/em/text()'],
            # 版面标签
            "layout_map_xpath": ['//map[@name="PagePicMap"]'],
            # 版面图链接
            "layout_map_image_xpath": ["//img[@usemap='#PagePicMap']/@src"],
            "layout_large_image_xpath": [],
            # 版面图链接pdf链接
            "layout_pdf_xpath": [],
            # 稿件详情。
            "detail_url_xpath": ['//map[@name="PagePicMap"]/area/@href'],
            # 预标题
            "detail_pre_title_xpath": ['//div[@class="intro"]/text()'],
            # 主标题
            "detail_title_xpath": ['//div[@class="newsdetatit"]/h3/text()'],
            # 子标题
            "detail_sub_title_xpath": ['//div[@class="sub"]/text()'],
            # 作者
            "detail_author_xpath": [],
            # 正文内容
            "detail_content_xpath": ['//div[@class="newsdetatext"]'],
            # 提交时间
            "detail_pubTime_xpath": [],

        },
        # 鲁南商报
        {
            "platformName": "鲁南商报",
            "sourceProvince": "山东",
            "sourceCity": "鲁南",
            # 1：国家级，2：省级，3：市级，0：商业类网站。
            "sourceLevel": 3,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 3,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # %Y%m/%d，{proxies}。
            "start_url": "http://lnsb.langya.cn/paper/pc/layout/%Y%m/%d/node_01.html",
            "cookiestr": "",
            # 版面url。
            "layout_url_xpath": ['//div[@class="Therestlist"]//li/a[2]/@href'],
            # 下一版链接
            "layout_next_xpath": ['//div[@class="newsnext"]/a/@href'],
            # 版面名称
            "layout_title_xpath": ['//div[@class="newslisttit"]/em/text()'],
            # 版面标签
            "layout_map_xpath": ['//map[@name="PagePicMap"]'],
            # 版面图链接
            "layout_map_image_xpath": ["//img[@usemap='#PagePicMap']/@src"],
            "layout_large_image_xpath": [],
            # 版面图链接pdf链接
            "layout_pdf_xpath": [],
            # 稿件详情。
            "detail_url_xpath": ['//map[@name="PagePicMap"]/area/@href'],
            # 预标题
            "detail_pre_title_xpath": ['//div[@class="intro"]/text()'],
            # 主标题
            "detail_title_xpath": ['//div[@class="newsdetatit"]/h3/text()'],
            # 子标题
            "detail_sub_title_xpath": ['//div[@class="sub"]/text()'],
            # 作者
            "detail_author_xpath": [],
            # 正文内容
            "detail_content_xpath": ['//div[@class="newsdetatext"]'],
            # 提交时间
            "detail_pubTime_xpath": ['//p[@align="center"]/text()'],

        },
        # 枣庄晚报
        {
            "platformName": "枣庄晚报",
            "sourceProvince": "山东",
            "sourceCity": "枣庄",
            # 1：国家级，2：省级，3：市级，0：商业类网站。
            "sourceLevel": 3,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # %Y%m/%d，{proxies}。
            "start_url": "http://www.zzrbw.com/zzwbPaper/PC/layout/%Y%m/%d/node_01.html",
            "cookiestr": "",
            # 版面url。
            "layout_url_xpath": ['//div[@class="Therestlist"]//li/a[2]/@href'],
            # 下一版链接
            "layout_next_xpath": ['//div[@class="newsnext"]/a/@href'],
            # 版面名称
            "layout_title_xpath": ['//div[@class="newslisttit"]/em/text()'],
            # 版面标签
            "layout_map_xpath": ['//map[@name="PagePicMap"]'],
            # 版面图链接
            "layout_map_image_xpath": ["//img[@usemap='#PagePicMap']/@src"],
            "layout_large_image_xpath": [],
            # 版面图链接pdf链接
            "layout_pdf_xpath": [],
            # 稿件详情。
            "detail_url_xpath": ['//map[@name="PagePicMap"]/area/@href'],
            # 预标题
            "detail_pre_title_xpath": ['//div[@class="intro"]/text()'],
            # 主标题
            "detail_title_xpath": ['//div[@class="newsdetatit"]/h3/text()'],
            # 子标题
            "detail_sub_title_xpath": ['//div[@class="sub"]/text()'],
            # 作者
            "detail_author_xpath": [],
            # 正文内容
            "detail_content_xpath": ['//div[@class="newsdetatext"]'],
            # 提交时间
            "detail_pubTime_xpath": ['//p[@align="center"]/text()'],

        },
        # 牡丹晚报
        {
            "platformName": "牡丹晚报",
            "sourceProvince": "山东",
            "sourceCity": "菏泽",
            "sourceLevel": 3,
            "sourceClassify": 1,
            "sourceImportance": 0,
            "mainMedia": 0,
            "start_url": "http://www.heze.cn/hzrb/pc/layout/%Y%m/%d/node_A1.html",
            "cookiestr": "",
            "layout_url_xpath": ["//ul[@id=\"layoutlist\"]/li/a/@href"],

            "layout_next_xpath": ['//a[@class="nextArt"]/@href'],

            "layout_title_xpath": ['//span[@id="layout"]//text()'],

            "layout_map_xpath": ['//map[@name="PagePicMap"]'],

            "layout_map_image_xpath": ['//img[@usemap="#PagePicMap"]/@src'],
            "layout_large_image_xpath": [],

            "layout_pdf_xpath": ['//div[@class="pull-right"]/a/@href'],

            "detail_url_xpath": ['//map[@name="PagePicMap"]/area/@href'],

            "detail_pre_title_xpath": ['//p[@id="PreTitle"]/text()'],

            "detail_title_xpath": ['//h2[@id="Title"]/text()'],

            "detail_sub_title_xpath": ['//p[@id="SubTitle"]/text()'],

            "detail_author_xpath": [],

            "detail_content_xpath": ['//div[@class="attachment"] | //div[@id="ozoom"]'],
            "detail_pubTime_xpath": [],
        },
        # 寿光日报
        {
            "platformName": "寿光日报",
            "sourceProvince": "山东",
            "sourceCity": "潍坊",
            "sourceLevel": 3,
            "sourceClassify": 1,
            "sourceImportance": 0,
            "mainMedia": 0,
            "start_url": "http://szb.sgnet.cc/sgrb/sgrb/pc/layout/%Y%m/%d/node_A01.html",
            "cookiestr": "",
            "layout_url_xpath": ["//ul[@id=\"layoutlist\"]/li/a/@href"],

            "layout_next_xpath": ['//a[@class="nextArt"]/@href'],

            "layout_title_xpath": ['//span[@id="layout"]//text()'],

            "layout_map_xpath": ['//map[@name="PagePicMap"]'],

            "layout_map_image_xpath": ['//img[@usemap="#PagePicMap"]/@src'],
            "layout_large_image_xpath": [],

            "layout_pdf_xpath": ['//div[@class="pull-right"]/a/@href'],

            "detail_url_xpath": ['//map[@name="PagePicMap"]/area/@href'],

            "detail_pre_title_xpath": ['//p[@id="PreTitle"]/text()'],

            "detail_title_xpath": ['//h2[@id="Title"]/text()'],

            "detail_sub_title_xpath": ['//p[@id="SubTitle"]/text()'],

            "detail_author_xpath": [],

            "detail_content_xpath": ['//div[@class="attachment"] | //div[@id="ozoom"]'],
            "detail_pubTime_xpath": [],
        },
        # 北方蔬菜报
        {
            "platformName": "北方蔬菜报",
            "sourceProvince": "山东",
            "sourceCity": "",
            "sourceLevel": 3,
            "sourceClassify": 3,
            "sourceImportance": 0,
            "mainMedia": 0,
            # %Y%m/%d，{proxies}。
            "start_url": "http://szb.sgnet.cc/sgrb/bfscb/pc/layout/%Y%m/%d/node_JSA01.html",
            "cookiestr": "",
            "layout_url_xpath": ["//ul[@id=\"layoutlist\"]/li/a/@href"],

            "layout_next_xpath": ['//a[@class="nextArt"]/@href'],

            "layout_title_xpath": ['//span[@id="layout"]//text()'],

            "layout_map_xpath": ['//map[@name="PagePicMap"]'],

            "layout_map_image_xpath": ['//img[@usemap="#PagePicMap"]/@src'],
            "layout_large_image_xpath": [],

            "layout_pdf_xpath": ['//div[@class="pull-right"]/a/@href'],

            "detail_url_xpath": ['//map[@name="PagePicMap"]/area/@href'],

            "detail_pre_title_xpath": ['//p[@id="PreTitle"]/text()'],

            "detail_title_xpath": ['//h2[@id="Title"]/text()'],

            "detail_sub_title_xpath": ['//p[@id="SubTitle"]/text()'],

            "detail_author_xpath": [],

            "detail_content_xpath": ['//div[@class="attachment"] | //div[@id="ozoom"]'],
            "detail_pubTime_xpath": [],
        },
        # 东方烟草报
        {
            "platformName": "东方烟草报",
            "sourceProvince": "山东",
            "sourceCity": "济南",
            # 1：国家级，2：省级，3：市级，0：商业类网站。
            "sourceLevel": 3,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 3,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # %Y-%m/%d，{proxies}。
            "start_url": "https://paper.eastobacco.com/html/%Y-%m/%d/node_1.htm",
            "cookiestr": "",
            # 版面url。
            "layout_url_xpath": ['//td[@class="default"]/a[@id="pageLink2"]/@href'],
            # 下一版链接
            "layout_next_xpath": ['//td[@align="right"]/a[@id="ed_next"]/@href'],
            # 版面名称
            "layout_title_xpath": ['//a[@id="ed_next"]/@href'],
            # 版面标签
            "layout_map_xpath": ["//map[@name='PagePicMap']"],
            # 版面图链接
            "layout_map_image_xpath": ["//img[@usemap='#PagePicMap']/@src"],
            "layout_large_image_xpath": [],
            # 版面图链接pdf链接
            "layout_pdf_xpath": ['//td[@valign="center"]/a/@href'],
            # 稿件详情。
            "detail_url_xpath": ["//map[@name='PagePicMap']/area/@href"],
            # 预标题
            "detail_pre_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][1]/td/text()'],
            # 主标题
            "detail_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][2]/td//text()'],
            # 子标题
            "detail_sub_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][3]/td/text()'],
            # 作者
            "detail_author_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][4]/td/founder-author//text()'],
            # 正文内容
            "detail_content_xpath": ['//table[@id="newspic"]//table//td | //div[@id="ozoom"]'],
            # 提交时间
            "detail_pubTime_xpath": [],

        },
        # 淄川工作报
        {
            "platformName": "淄川工作报",
            "sourceProvince": "山东",
            "sourceCity": "淄博市",
            # 1：国家级，2：省级，3：市级，0：商业类网站。
            "sourceLevel": 3,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # %Y-%m/%d，{proxies}。
            "start_url": "http://www.cnepaper.com/zcgz/html/%Y-%m/%d/node_103186.htm",
            "cookiestr": "",
            # 版面url。
            "layout_url_xpath": ['//td[@class="default"]/a[@id="pageLink"]/@href'],
            # 下一版链接
            "layout_next_xpath": ['//a[@id="ed_next"]/@href'],
            # 版面名称
            "layout_title_xpath": ['//td[@align="left"]/strong/text()'],
            # 版面标签
            "layout_map_xpath": ["//map[@name='PagePicMap']"],
            # 版面图链接
            "layout_map_image_xpath": ["//img[@usemap='#PagePicMap']/@src"],
            "layout_large_image_xpath": [],
            # 版面图链接pdf链接
            "layout_pdf_xpath": ['//td[@valign="center"]/a/@href'],
            # 稿件详情。
            "detail_url_xpath": ["//map[@name='PagePicMap']/area/@href"],
            # 预标题
            "detail_pre_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][1]/td/text()'],
            # 主标题
            "detail_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][2]/td//text()'],
            # 子标题
            "detail_sub_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][3]/td/text()'],
            # 作者
            "detail_author_xpath": [],
            # 正文内容
            "detail_content_xpath": ['//table[@id="newspic"]//table//td | //div[@id="ozoom"]'],
            # 提交时间
            "detail_pubTime_xpath": [],

        },
        # 今日章丘
        {
            "platformName": "今日章丘",
            "sourceProvince": "山东",
            "sourceCity": "济南市",
            # 1：国家级，2：省级，3：市级，0：商业类网站。
            "sourceLevel": 3,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # %Y-%m/%d，{proxies}。
            "start_url": "http://115.236.76.50/jrzq/html/%Y-%m/%d/node_57343.htm",
            "cookiestr": "",
            # 版面url。
            "layout_url_xpath": ['//td[@class="default"]/a[@id="pageLink"]/@href'],
            # 下一版链接
            "layout_next_xpath": ['//a[@id="ed_next"]/@href'],
            # 版面名称
            "layout_title_xpath": ['//td[@align="left"]/strong/text()'],
            # 版面标签
            "layout_map_xpath": ["//map[@name='PagePicMap']"],
            # 版面图链接
            "layout_map_image_xpath": ["//img[@usemap='#PagePicMap']/@src"],
            "layout_large_image_xpath": [],
            # 版面图链接pdf链接
            "layout_pdf_xpath": ['//td[@valign="center"]/a/@href'],
            # 稿件详情。
            "detail_url_xpath": ["//map[@name='PagePicMap']/area/@href"],
            # 预标题
            "detail_pre_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][1]/td/text()'],
            # 主标题
            "detail_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][2]/td//text()'],
            # 子标题
            "detail_sub_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][3]/td/text()'],
            # 作者
            "detail_author_xpath": [],
            # 正文内容
            "detail_content_xpath": ['//table[@id="newspic"]//table//td | //div[@id="ozoom"]'],
            # 提交时间
            "detail_pubTime_xpath": [],

        },

        # fred
        # 怒江报
        {
            "platformName": "怒江日报",
            "sourceProvince": "云南省",
            "sourceCity": "",
            # 1：国家级，2：省级，3：市级，0：商业类网站。
            "sourceLevel": 3,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # %Y-%m-%d，{proxies}。
            # 起始url
            "start_url": "http://zwb.nujiang.cn/Html/%Y-%m-%d/Qpaper.html",
            "cookiestr": "",
            # 版面url。多个
            "layout_url_xpath": ['//div[@id="bancilist"]//li/a/@href'],
            # 下一版链接
            "layout_next_xpath": [],
            # 版面名称 //1个结果
            "layout_title_xpath": ['//span[@class="banming2"]/text()'],
            # 版面标签
            "layout_map_xpath": ['//div[@class="paper_rect"]/map'],
            # 版面图链接 //图片地址
            "layout_map_image_xpath": ['//img[@id="mappaper"]/@src'],
            "layout_large_image_xpath": [],
            # 版面图链接pdf（大图）链接
            "layout_pdf_xpath": ['//a[@class="button fl"]/@href'],
            # 稿件详情。
            # 从版面图的map标签中获取详情页链接
            "detail_url_xpath": ['//div[@class="paper_rect"]/map/area/@href'],
            # 预标题
            "detail_pre_title_xpath": ['//div[@id="yinti"]/text()'],
            # 主标题
            "detail_title_xpath": ['//div[@id="doctitle"]/text()'],
            # 子标题
            "detail_sub_title_xpath": ['//div[@id="subdoctitle"]/text()'],
            # 作者
            "detail_author_xpath": [],
            # 正文内容
            "detail_content_xpath": ['//div[@id="doccontent"]'],
            # 提交时间
            "detail_pubTime_xpath": [],
        },
        # 今日兴义
        {
            "platformName": "今日兴义",
            "sourceProvince": "贵州省",
            "sourceCity": "",
            # 1：国家级，2：省级，3：市级，0：商业类网站。
            "sourceLevel": 3,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # %Y-%m/%d，{proxies}。
            # 起始url
            "start_url": "http://115.236.76.50/xyb/html/%Y-%m/%d/node_56600.htm",
            "cookiestr": "",
            # 版面url。多个
            "layout_url_xpath": ['//td[@class="default"]/a[@id="pageLink"]/@href'],
            # 下一版链接
            "layout_next_xpath": ['//td[@align="right"]/a[@id="ed_next"]/@href'],
            # 版面名称 //1个结果
            "layout_title_xpath": ['//td[@align="left"]/strong/text()'],
            # 版面标签
            "layout_map_xpath": ['//map[@name="PagePicMap"]'],
            # 版面图链接 //图片地址
            "layout_map_image_xpath": ['//img[@usemap="#PagePicMap"]/@src'],
            "layout_large_image_xpath": [],
            # 版面图链接pdf（大图）链接
            "layout_pdf_xpath": [],
            # 稿件详情。
            # 从版面图的map标签中获取详情页链接
            "detail_url_xpath": ['//map[@name="PagePicMap"]/area/@href'],
            # 预标题
            "detail_pre_title_xpath": ['//tr[@valign="top"][1]/td[@class="font02"][@align="center"]/text()'],
            # 主标题
            "detail_title_xpath": ['//p[@class="BSHARE_TEXT"]'],
            # 子标题
            "detail_sub_title_xpath": ['//tr[@valign="top"][3]/td[@class="font02"][@align="center"]/text()'],
            # 作者
            "detail_author_xpath": [],
            # 正文内容
            "detail_content_xpath": ['//table[@id="newspic"] | //div[@id="ozoom"]'],
            # 提交时间
            "detail_pubTime_xpath": [],
        },
        # 大方报
        {
            "platformName": "大方报",
            "sourceProvince": "贵州省",
            "sourceCity": "",
            # 1：国家级，2：省级，3：市级，0：商业类网站。
            "sourceLevel": 3,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # %Y-%m/%d，{proxies}。
            # 起始url
            "start_url": "http://115.236.76.50/dfb/html/%Y-%m/%d/node_114196.htm",
            "cookiestr": "",
            # 版面url。多个
            "layout_url_xpath": ['//a[@class="rigth_bmdh_href"]/@href'],
            # 下一版链接
            "layout_next_xpath": ['//a[@id="ed_next"]/@href'],
            # 版面名称 //1个结果
            "layout_title_xpath": ['//td[@id="currentBM"]//text()'],
            # 版面标签
            "layout_map_xpath": ['//map[@name="PagePicMap"]'],
            # 版面图链接 //图片地址
            "layout_map_image_xpath": ['//img[@usemap="#PagePicMap"]/@src'],
            "layout_large_image_xpath": [],
            # 版面图链接pdf（大图）链接
            "layout_pdf_xpath": ['//a[@id="bigbmshowpdf"]/@href'],
            # 稿件详情。
            # 从版面图的map标签中获取详情页链接
            "detail_url_xpath": ['//map[@name="PagePicMap"]/area/@href'],
            # 预标题
            "detail_pre_title_xpath": ['//tr[@valign="top"][1]/td[@class="font02"][@align="center"]/text()'],
            # 主标题
            "detail_title_xpath": ['//p[@class="BSHARE_TEXT"]'],
            # 子标题
            "detail_sub_title_xpath": ['//tr[@valign="top"][3]/td[@class="font02"][@align="center"]/text()'],
            # 作者
            "detail_author_xpath": [],
            # 正文内容
            "detail_content_xpath": ['//table[@id="newspic"] | //div[@id="ozoom"]'],
            # 提交时间
            "detail_pubTime_xpath": [],
        },
        # 黔中早报
        {
            "platformName": "黔中早报",
            "sourceProvince": "贵州省",
            "sourceCity": "",
            # 1：国家级，2：省级，3：市级，0：商业类网站。
            "sourceLevel": 3,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # %Y-%m/%d，{proxies}。
            # 起始url
            "start_url": "http://www.asrbs.net/site1/qzzb/html/%Y-%m/%d/node_22.htm",
            "cookiestr": "",
            # 版面url。多个
            "layout_url_xpath": ['//td[@class="tits"]/a/@href'],
            # 下一版链接
            "layout_next_xpath": ['//div[@id="layer33"]/a/@href'],
            # 版面名称 //1个结果
            "layout_title_xpath": ['//div[@class="fl mt5"]//text()'],
            # 版面标签
            "layout_map_xpath": ['//map[@name="pagepicmap"]'],
            # 版面图链接 //图片地址
            "layout_map_image_xpath": ['//img[@usemap="#PagePicMap"]/@src'],
            "layout_large_image_xpath": [],
            # 版面图链接pdf（大图）链接
            "layout_pdf_xpath": ['//div[@class="fr mt3"]/a/@href'],
            # 稿件详情。
            # 从版面图的map标签中获取详情页链接
            "detail_url_xpath": ['//map[@name="pagepicmap"]/area/@href'],
            # 预标题
            "detail_pre_title_xpath": ['//tr[@valign="top"][1]//td[@class="bt2"]/text()'],
            # 主标题
            "detail_title_xpath": ['//td[@class="bt1"]/text()'],
            # 子标题
            "detail_sub_title_xpath": ['//tr[@valign="top"][3]//td[@class="bt2"]/text()'],
            # 作者
            "detail_author_xpath": [],
            # 正文内容
            "detail_content_xpath": ['//div[@class="M_m_cont"]'],
            # 提交时间
            "detail_pubTime_xpath": [],

        },
        # 黔东南日报
        {
            "platformName": "黔东南日报",
            "sourceProvince": "贵州省",
            "sourceCity": "凯里市",
            # 1：国家级，2：省级，3：市级，0：商业类网站。
            "sourceLevel": 3,
            # 1：媒体类，2：政务类，3：商业类。
            "sourceClassify": 1,
            # 是否重点渠道。
            "sourceImportance": 0,
            # 是否主流媒体。
            "mainMedia": 0,
            # %Y%m/%d，{proxies}。
            # 起始url
            "start_url": "http://dzb.qdnrbs.cn/szb/pc/%Y%m/%d/l01.html",
            "cookiestr": "",
            # 版面url。
            "layout_url_xpath": ['//div[@class="nav-list"]//li/a[1]/@href'],
            # 下一版链接
            "layout_next_xpath": ['//a[@class="b-btn"]/@href'],
            # 版面名称
            "layout_title_xpath": ['//div[@class="tabs"]/h3/text()'],
            # 版面标签
            "layout_map_xpath": ['//map[@name="PagePicMap"]'],
            # 版面图链接
            "layout_map_image_xpath": ['//img[@usemap="#PagePicMap"]/@src'],
            "layout_large_image_xpath": [],
            # 版面图链接pdf（大图）链接
            "layout_pdf_xpath": ['//a[@class="pdf"]/@href'],
            # 稿件详情。
            # 从版面图的map标签中获取详情页链接
            "detail_url_xpath": ['//map[@name="PagePicMap"]/area/@href'],
            # 预标题
            "detail_pre_title_xpath": ['//p[@id="PreTitle"]/text()'],
            # 主标题
            "detail_title_xpath": ['//h2[@id="Title"]/text()'],
            # 子标题
            "detail_sub_title_xpath": ['//p[@id="SubTitle"]/text()'],
            # 作者
            "detail_author_xpath": [],
            # 正文内容
            "detail_content_xpath": ['//div[@class="attachment"] | //div[@id="ozoom"]'],
            # 提交时间
            "detail_pubTime_xpath": [],

        },

    ]
    return temps


def upload():
    """
    上传模版信息
    """
    conmysql, cursor = con_mysql()
    for paper_template in xpath_rule():
        name = paper_template["platformName"]
        paper_template["platformType"] = 6
        source_level = paper_template["sourceLevel"]
        source_classify = paper_template["sourceClassify"]
        source_importance = paper_template["sourceImportance"]
        media = paper_template['mainMedia']
        paper_template = json.dumps(paper_template)
        print(paper_template)
        # 先查询是否存在
        sql = f"select platformName from epaper_template where platformName='{name}';"
        try:
            cursor.execute(sql)
        except Exception as e:
            raise Exception(e)
        mysql_result = cursor.fetchall()
        if mysql_result:
            print(f"该'{name}'已存在")
            continue
        else:
            # 将数据写入到数据库
            sql = 'insert into epaper_template (platformName, platformType,sourceLevel,sourceClassify,sourceImportance, ' \
                  'mainMedia, epaperTemplate) values (%s,6,%s,%s,%s,%s,%s)'
            data = (name, source_level, source_classify, source_importance, media, paper_template)
            cursor.execute(sql, data)
            conmysql.commit()
            print(f'{name}添加成功')
    cursor.close()
    conmysql.close()


upload()




