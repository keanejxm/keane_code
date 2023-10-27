# -*- coding:utf-8 -*-
"""
# project:
# author: Neil
# date: xxxx/xx/xx

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
        "big_data")
    cursor = conmysql.cursor(pymysql.cursors.DictCursor)
    sql = f"select * from dxwz where platformType = 5"
    try:
        cursor.execute(sql)
    except Exception as e:
        raise Exception('query error')
    mysql_result = cursor.fetchall()
    cursor.close()
    conmysql.close()
    return mysql_result


update_web = list()

for i in con_mysql()[:20]:
    web_dict = {
        "platformName": i["platformName"],
        "sourceProvince": i["sourceProvince"],
        "sourceCity": i["sourceCity"],
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": i["sourceLevel"],
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": i["sourceClassify"],
        # 是否重点渠道。
        "sourceImportance": i["sourceImportance"],
        # 是否主流媒体。
        "mainMedia": i["mainMedia"],
        # 起始地址。
        "start_url": i["start_url"],
    }

    update_web.append(web_dict)
print({"data": update_web})


def integrate_data():
    """
    整合数据库中的数据
    :return:
    """
    data_list = list()
    result = con_mysql()
    for r in result:
        body = dict()
        body["platformName"] = r["platformName"]
        body["sourceProvince"] = r["sourceProvince"]
        body["sourceCity"] = r["sourceCity"]
        body["sourceLevel"] = r["sourceLevel"]
        body["sourceClassify"] = r["sourceClassify"]
        body["sourceImportance"] = r["sourceImportance"]
        body["mainMedia"] = r["mainMedia"]
        body["start_url"] = r["start_url"]
        body["cookiestr"] = r["cookiestr"]
        layout_info = eval(r["layout_info_xpath"])
        if 'layout_useful_day' in layout_info:
            continue
        body["layout_url_xpath"] = layout_info["layout_url_xpath"]
        body["layout_next_xpath"] = layout_info["layout_next_xpath"]
        body["layout_title_xpath"] = layout_info["layout_title_xpath"]
        body["layout_map_xpath"] = layout_info["layout_map_xpath"]
        body["layout_map_image_xpath"] = layout_info["layout_map_image_xpath"]
        if "layout_large_image_xpath" in layout_info:
            body["layout_large_image_xpath"] = layout_info["layout_large_image_xpath"]
        else:
            body["layout_large_image_xpath"] = []
            print(f'{r["platformName"]}large_img有错误，添加成功')
        if "layout_pdf_xpath" in layout_info:
            body["layout_pdf_xpath"] = layout_info["layout_pdf_xpath"]
        else:
            body["layout_pdf_xpath"] = []
            print(f'{r["platformName"]}pdf有错误,添加成功')
        body["detail_url_xpath"] = r["detail_url_xpath"]
        body["detail_pre_title_xpath"] = r["detail_pre_title_xpath"]
        body["detail_title_xpath"] = r["detail_title_xpath"]
        body["detail_sub_title_xpath"] = r["detail_sub_title_xpath"]
        body["detail_content_xpath"] = r["detail_content_xpath"]
        body["detail_pubTime_xpath"] = r["detail_pubTime_xpath"]
        data_list.append(body)
    return data_list

# def update():
#     """
#     更新模版信息
#     """
#     conmysql, cursor = conn_mysql()
#     # list = [
#     #     # 中国绿色时报·花草园林周刊
#     #     {
#     #         "platformName": "中国绿色时报·花草园林周刊",
#     #         "sourceProvince": "北京",
#     #         "sourceCity": "",
#     #         # 1：国家级，2：省级，3：市级，0：商业类网站。
#     #         "sourceLevel": 0,
#     #         # 1：媒体类，2：政务类，3：商业类。
#     #         "sourceClassify": 3,
#     #         # 是否重点渠道。
#     #         "sourceImportance": 0,
#     #         # 是否主流媒体。
#     #         "mainMedia": 0,
#     #         # %Y-%m-%d，{proxies}。
#     #         "start_url": "http://www.greentimes.com/hcyl/html/%Y-%m/%d/node_12.htm",
#     #         "cookiestr": "",
#     #         # 版面url。
#     #         "layout_url_xpath": ["//a[@id='pageLink']/@href"],
#     #         # 下一版链接
#     #         "layout_next_xpath": ['//a[@class="preart"]/@href'],
#     #         # 版面名称
#     #         "layout_title_xpath": ['//div[@class="paperinfo fl"]/text()'],
#     #         # 版面标签
#     #         "layout_map_xpath": ['//map[@name="pagepicmap"]'],
#     #         # 版面图链接
#     #         "layout_map_image_xpath": ['//img[@usemap="#PagePicMap"]/@src'],
#     #         "layout_large_image_xpath": [],
#     #         # 版面图链接pdf（大图）链接
#     #         "layout_pdf_xpath": [],
#     #         # 稿件详情。
#     #         # 从版面图的map标签中获取详情页链接
#     #         "detail_url_xpath": ['//map[@name="pagepicmap"]/area/@href'],
#     #         # 预标题
#     #         "detail_pre_title_xpath": ['//div[@class="content fl"]/h3/text()'],
#     #         # 主标题
#     #         "detail_title_xpath": ['//div[@class="content fl"]/h2/text()'],
#     #         # 子标题
#     #         "detail_sub_title_xpath": ['//div[@class="content fl"]/h4/text()'],
#     #         # 作者
#     #         "detail_author_xpath": [],
#     #         # 正文内容
#     #         "detail_content_xpath": ['//div[@class="cont"]/table//table//td | //div[@id="ozoom"]'],
#     #         # 提交时间
#     #         "detail_pubTime_xpath": [],
#     #
#     #     },
#     #     # 中国绿色时报·绿色产业周刊
#     #     {
#     #         "platformName": "中国绿色时报·绿色产业周刊",
#     #         "sourceProvince": "北京",
#     #         "sourceCity": "",
#     #         # 1：国家级，2：省级，3：市级，0：商业类网站。
#     #         "sourceLevel": 0,
#     #         # 1：媒体类，2：政务类，3：商业类。
#     #         "sourceClassify": 3,
#     #         # 是否重点渠道。
#     #         "sourceImportance": 0,
#     #         # 是否主流媒体。
#     #         "mainMedia": 0,
#     #         # %Y-%m/%d，{proxies}。
#     #         "start_url": "http://www.greentimes.com/lscy/html/%Y-%m/%d/node_20.htm",
#     #         "cookiestr": "",
#     #         # 版面url。
#     #         "layout_url_xpath": ["//a[@id='pageLink']/@href"],
#     #         # 下一版链接
#     #         "layout_next_xpath": ['//a[@class="preart"]/@href'],
#     #         # 版面名称
#     #         "layout_title_xpath": ['//div[@class="paperinfo fl"]/text()'],
#     #         # 版面标签
#     #         "layout_map_xpath": ['//map[@name="pagepicmap"]'],
#     #         # 版面图链接
#     #         "layout_map_image_xpath": ['//img[@usemap="#PagePicMap"]/@src'],
#     #         "layout_large_image_xpath": [],
#     #         # 版面图链接pdf（大图）链接
#     #         "layout_pdf_xpath": [],
#     #         # 稿件详情。
#     #         # 从版面图的map标签中获取详情页链接
#     #         "detail_url_xpath": ['//map[@name="pagepicmap"]/area/@href'],
#     #         # 预标题
#     #         "detail_pre_title_xpath": ['//div[@class="content fl"]/h3/text()'],
#     #         # 主标题
#     #         "detail_title_xpath": ['//div[@class="content fl"]/h2/text()'],
#     #         # 子标题
#     #         "detail_sub_title_xpath": ['//div[@class="content fl"]/h4/text()'],
#     #         # 作者
#     #         "detail_author_xpath": [],
#     #         # 正文内容
#     #         "detail_content_xpath": ['//div[@class="cont"]/table//table//td | //div[@id="ozoom"]'],
#     #         # 提交时间
#     #         "detail_pubTime_xpath": [],
#     #
#     #     },
#     #     # 中国政府采购报
#     #     {
#     #         "platformName": "中国政府采购报",
#     #         "sourceProvince": "北京",
#     #         "sourceCity": "",
#     #         # 1：国家级，2：省级，3：市级，0：商业类网站。
#     #         "sourceLevel": 1,
#     #         # 1：媒体类，2：政务类，3：商业类。
#     #         "sourceClassify": 2,
#     #         # 是否重点渠道。
#     #         "sourceImportance": 0,
#     #         # 是否主流媒体。
#     #         "mainMedia": 0,
#     #         # %Y-%m-%d，{proxies}。
#     #         "start_url": "http://www.cgpnews.cn/epapers?period=1&period_date=%Y-%m-%d",
#     #         "cookiestr": "",
#     #         # 版面url。
#     #         "layout_url_xpath": ['//div[@id="pageList"]//li//a/@href'],
#     #         # 下一版链接
#     #         "layout_next_xpath": ['//div[@class="B_01_2"]/a[2]/@href'],
#     #         # 版面名称
#     #         "layout_title_xpath": ['//div[@class="left B_02_1"]/div/text()'],
#     #         # 版面标签
#     #         "layout_map_xpath": [],
#     #         # 版面图链接
#     #         "layout_map_image_xpath": ['//img[@usemap="#hotarea"]/@src'],
#     #         "layout_large_image_xpath": [],
#     #         # 版面图链接pdf（大图）链接
#     #         "layout_pdf_xpath": [],
#     #         # 稿件详情。
#     #         # 从版面图的map标签中获取详情页链接
#     #         "detail_url_xpath": ['//div[@id="titleList"]//li//a/@href'],
#     #         # 预标题
#     #         "detail_pre_title_xpath": [],
#     #         # 主标题
#     #         "detail_title_xpath": ['//h1[@class="title"]/text()'],
#     #         # 子标题
#     #         "detail_sub_title_xpath": [],
#     #         # 作者
#     #         "detail_author_xpath": [],
#     #         # 正文内容
#     #         "detail_content_xpath": ['//div[@id="articleText"]'],
#     #         # 提交时间
#     #         "detail_pubTime_xpath": [],
#     #
#     #     },
#     #     # 重庆日报农村版
#     #     {
#     #         "platformName": "重庆日报农村版",
#     #         "sourceProvince": "重庆",
#     #         "sourceCity": "",
#     #         # 1：国家级，2：省级，3：市级，0：商业类网站。
#     #         "sourceLevel": 2,
#     #         # 1：媒体类，2：政务类，3：商业类。
#     #         "sourceClassify": 1,
#     #         # 是否重点渠道。
#     #         "sourceImportance": 0,
#     #         # 是否主流媒体。
#     #         "mainMedia": 0,
#     #         # %Y-%m/%d，{proxies}。
#     #         "start_url": "https://epaper.cqrb.cn/html/ncb/%Y-%m/%d/001/node.htm",
#     #         "cookiestr": "",
#     #         # 版面url。
#     #         "layout_url_xpath": ["//tbody/tr/td[@class='default'][@align='left']/a/@href"],
#     #         # 下一版链接
#     #         "layout_next_xpath": ["//td[@align='right']//td[@class='px12']/a/@href"],
#     #         # 版面名称
#     #         "layout_title_xpath": ["//td[@class='px12'][1]//text()"],
#     #         # 版面标签
#     #         "layout_map_xpath": ["//map[@name='PagePicMap']"],
#     #         # 版面图链接
#     #         "layout_map_image_xpath": ["//img[@usemap='#PagePicMap']/@src"],
#     #         "layout_large_image_xpath": [],
#     #         # 版面图链接pdf链接
#     #         "layout_pdf_xpath": ["//td[@class='px12'][@valign='center']/a/@href"],
#     #         # 稿件详情。
#     #         "detail_url_xpath": ["//map[@name='PagePicMap']/area/@href"],
#     #         # 预标题
#     #         "detail_pre_title_xpath": ["//table[@cellpadding='5']/tbody/tr[2]//span[1]/text()"],
#     #         # 主标题
#     #         "detail_title_xpath": ["//tr/td[@align='center']/strong/text()"],
#     #         # 子标题
#     #         "detail_sub_title_xpath": ["//table[@cellpadding='5']/tbody/tr[2]//span[2]/text()"],
#     #         # 作者
#     #         "detail_author_xpath": ["//tbody/tr[1]/td[2]/table[3]/tbody/tr[2]//span/text()"],
#     #         # 正文内容
#     #         "detail_content_xpath": ["//div[@id='ozoom']"],
#     #         # 提交时间
#     #         "detail_pubTime_xpath": [],
#     #
#     #     },
#     #     # 武陵都市报
#     #     {
#     #         "platformName": "武陵都市报",
#     #         "sourceProvince": "重庆",
#     #         "sourceCity": "武陵",
#     #         # 1：国家级，2：省级，3：市级，0：商业类网站。
#     #         "sourceLevel": 3,
#     #         # 1：媒体类，2：政务类，3：商业类。
#     #         "sourceClassify": 1,
#     #         # 是否重点渠道。
#     #         "sourceImportance": 0,
#     #         # 是否主流媒体。
#     #         "mainMedia": 0,
#     #         # %Y-%m/%d，{proxies}。
#     #         "start_url": "http://115.236.76.50/wldsb/html/%Y-%m/%d/node_37749.htm",
#     #         "cookiestr": "",
#     #         # 版面url。
#     #         "layout_url_xpath": ['//td[@class="default"]/a[@id="pageLink"]/@href'],
#     #         # 下一版链接
#     #         "layout_next_xpath": ['//td[@align="right"]/a[@id="ed_next"]/@href'],
#     #         # 版面名称
#     #         "layout_title_xpath": ['//td[@align="left"]/strong/text()'],
#     #         # 版面标签
#     #         "layout_map_xpath": ["//map[@name='PagePicMap']"],
#     #         # 版面图链接
#     #         "layout_map_image_xpath": ["//img[@usemap='#PagePicMap']/@src"],
#     #         "layout_large_image_xpath": [],
#     #         # 版面图链接pdf链接
#     #         "layout_pdf_xpath": ['//td[@valign="center"]/a/@href'],
#     #         # 稿件详情。
#     #         "detail_url_xpath": ["//map[@name='PagePicMap']/area/@href"],
#     #         # 预标题
#     #         "detail_pre_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][1]/td/text()'],
#     #         # 主标题
#     #         "detail_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][2]/td//text()'],
#     #         # 子标题
#     #         "detail_sub_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][3]/td/text()'],
#     #         # 作者
#     #         "detail_author_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][4]/td/text()'],
#     #         # 正文内容
#     #         "detail_content_xpath": ['//table[@id="newspic"]//table//td | //div[@id="ozoom"]'],
#     #         # 提交时间
#     #         "detail_pubTime_xpath": [],
#     #
#     #     },
#     #     # 天津工人报
#     #     {
#     #         "platformName": "天津工人报",
#     #         "sourceProvince": "天津",
#     #         "sourceCity": "",
#     #         # 1：国家级，2：省级，3：市级，0：商业类网站。
#     #         "sourceLevel": 3,
#     #         # 1：媒体类，2：政务类，3：商业类。
#     #         "sourceClassify": 1,
#     #         # 是否重点渠道。
#     #         "sourceImportance": 0,
#     #         # 是否主流媒体。
#     #         "mainMedia": 0,
#     #         # %Y-%m/%d，{proxies}。
#     #         "start_url": "http://www.fzsyun.cn/tjgrb/%Y-%m/%d/node_01.html",
#     #         "cookiestr": "",
#     #         # 版面url。
#     #         "layout_url_xpath": ['//li[@class="layout-catalogue-item"]/a[1]/@href'],
#     #         # 下一版链接
#     #         "layout_next_xpath": ['//a[@class="pic-info-ctrl pic-info-ctrl-next"]/@href'],
#     #         # 版面名称
#     #         "layout_title_xpath": ['//span[@class="pic-info-summary fl"]/text()'],
#     #         # 版面标签
#     #         "layout_map_xpath": ["//map[@name='pagepicmap']"],
#     #         # 版面图链接
#     #         "layout_map_image_xpath": ["//img[@usemap='#pagepicmap']/@src"],
#     #         "layout_large_image_xpath": [],
#     #         # 版面图链接pdf（大图）链接
#     #         "layout_pdf_xpath": [],
#     #         # 稿件详情。
#     #         "detail_url_xpath": ["//map[@name='pagepicmap']/area/@href"],
#     #         # 预标题
#     #         "detail_pre_title_xpath": ['//div[@class="main-content"]/h3[1]/text()'],
#     #         # 主标题
#     #         "detail_title_xpath": ['//div[@class="main-content"]/h1/text()'],
#     #         # 子标题
#     #         "detail_sub_title_xpath": ['//div[@class="main-content"]/h3[2]/text()'],
#     #         # 作者
#     #         "detail_author_xpath": [],
#     #         # 正文内容
#     #         "detail_content_xpath": ['//div[@id="news_content"]/cms-content'],
#     #         # 提交时间
#     #         "detail_pubTime_xpath": [],
#     #
#     #     },
#     #     # 南川日报(更新时间久远)
#     #     {
#     #         "platformName": "南川日报",
#     #         "sourceProvince": "重庆",
#     #         "sourceCity": "南川",
#     #         # 1：国家级，2：省级，3：市级，0：商业类网站。
#     #         "sourceLevel": 3,
#     #         # 1：媒体类，2：政务类，3：商业类。
#     #         "sourceClassify": 1,
#     #         # 是否重点渠道。
#     #         "sourceImportance": 0,
#     #         # 是否主流媒体。
#     #         "mainMedia": 0,
#     #         # %Y-%m/%d，{proxies}。
#     #         "start_url": "http://ncrb.cqncnews.com/html/%Y-%m/%d/node_1.htm?v=1",
#     #         "cookiestr": "",
#     #         # 版面url。
#     #         "layout_url_xpath": ['//td[@class="default"]/a[@id="pageLink"]/@href'],
#     #         # 下一版链接
#     #         "layout_next_xpath": ['//td[@align="left"]/a[@id="ed_next"]/@href'],
#     #         # 版面名称
#     #         "layout_title_xpath": ['//td[@align="left"]/strong/text()'],
#     #         # 版面标签
#     #         "layout_map_xpath": ["//map[@name='PagePicMap']"],
#     #         # 版面图链接
#     #         "layout_map_image_xpath": ["//img[@usemap='#PagePicMap']/@src"],
#     #         "layout_large_image_xpath": [],
#     #         # 版面图链接pdf链接
#     #         "layout_pdf_xpath": ['//td[@valign="center"]/a/@href'],
#     #         # 稿件详情。
#     #         "detail_url_xpath": ["//map[@name='PagePicMap']/area/@href"],
#     #         # 预标题
#     #         "detail_pre_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][1]/td/text()'],
#     #         # 主标题
#     #         "detail_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][2]/td//text()'],
#     #         # 子标题
#     #         "detail_sub_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][3]/td/text()'],
#     #         # 作者
#     #         "detail_author_xpath": [],
#     #         # 正文内容
#     #         "detail_content_xpath": ['//table[@id="newspic"]//table//td | //div[@id="ozoom"]'],
#     #         # 提交时间
#     #         "detail_pubTime_xpath": [],
#     #
#     #     },
#     #     # 忠州日报(更新时间久远)
#     #     {
#     #         "platformName": "忠州日报",
#     #         "sourceProvince": "重庆",
#     #         "sourceCity": "忠州",
#     #         # 1：国家级，2：省级，3：市级，0：商业类网站。
#     #         "sourceLevel": 3,
#     #         # 1：媒体类，2：政务类，3：商业类。
#     #         "sourceClassify": 1,
#     #         # 是否重点渠道。
#     #         "sourceImportance": 0,
#     #         # 是否主流媒体。
#     #         "mainMedia": 0,
#     #         # %Y-%m/%d，{proxies}。
#     #         "start_url": "http://epaper.zzxw.net/html/%Y-%m/%d/node_30332.htm",
#     #         "cookiestr": "",
#     #         # 版面url。
#     #         "layout_url_xpath": ['//td[@class="default"]/a[@id="pageLink"]/@href'],
#     #         # 下一版链接
#     #         "layout_next_xpath": ['//td[@align="left"]/a[@id="ed_next"]/@href'],
#     #         # 版面名称
#     #         "layout_title_xpath": ['//td[@align="left"]/strong/text()'],
#     #         # 版面标签
#     #         "layout_map_xpath": ["//map[@name='PagePicMap']"],
#     #         # 版面图链接
#     #         "layout_map_image_xpath": ["//img[@usemap='#PagePicMap']/@src"],
#     #         "layout_large_image_xpath": [],
#     #         # 版面图链接pdf链接
#     #         "layout_pdf_xpath": ['//td[@valign="center"]/a/@href'],
#     #         # 稿件详情。
#     #         "detail_url_xpath": ["//map[@name='PagePicMap']/area/@href"],
#     #         # 预标题
#     #         "detail_pre_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][1]/td/text()'],
#     #         # 主标题
#     #         "detail_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][2]/td//text()'],
#     #         # 子标题
#     #         "detail_sub_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][3]/td/text()'],
#     #         # 作者
#     #         "detail_author_xpath": [],
#     #         # 正文内容
#     #         "detail_content_xpath": ['//table[@id="newspic"]//table//td | //div[@id="ozoom"]'],
#     #         # 提交时间
#     #         "detail_pubTime_xpath": [],
#     #
#     #     },
#     #     # 长寿日报
#     #     {
#     #         "platformName": "长寿日报",
#     #         "sourceProvince": "重庆",
#     #         "sourceCity": "",
#     #         # 1：国家级，2：省级，3：市级，0：商业类网站。
#     #         "sourceLevel": 3,
#     #         # 1：媒体类，2：政务类，3：商业类。
#     #         "sourceClassify": 1,
#     #         # 是否重点渠道。
#     #         "sourceImportance": 0,
#     #         # 是否主流媒体。
#     #         "mainMedia": 0,
#     #         # %Y%m/%d，{proxies}。
#     #         "start_url": "http://epaper.ccs.cn/pc/%Y%m/%d/col01.html",
#     #         "cookiestr": "",
#     #         # 版面url。
#     #         "layout_url_xpath": ['//ul[@id="widthNone"]/li/a[2]/@href'],
#     #         # 下一版链接
#     #         "layout_next_xpath": ['//div[@class="newsnext"]/a/@href'],
#     #         # 版面名称
#     #         "layout_title_xpath": ['//div[@class="newslisttit"]/em/text()'],
#     #         # 版面标签
#     #         "layout_map_xpath": ["//map[@name='PagePicMap']"],
#     #         # 版面图链接
#     #         "layout_map_image_xpath": ["//img[@usemap='#PagePicMap']/@src"],
#     #         "layout_large_image_xpath": [],
#     #         # 版面图链接pdf链接
#     #         "layout_pdf_xpath": ['//div[@class="newslisttit"]/em/a/@href'],
#     #         # 稿件详情。
#     #         "detail_url_xpath": ["//map[@name='PagePicMap']/area/@href"],
#     #         # 预标题
#     #         "detail_pre_title_xpath": ['//p[@id="PreTitle"]/text()'],
#     #         # 主标题
#     #         "detail_title_xpath": ['//h3[@id="Title"]/text()'],
#     #         # 子标题
#     #         "detail_sub_title_xpath": ['//p[@id="SubTitle"]/text()'],
#     #         # 作者
#     #         "detail_author_xpath": [],
#     #         # 正文内容
#     #         "detail_content_xpath": ['//div[@class="newsdetatext"]'],
#     #         # 提交时间
#     #         "detail_pubTime_xpath": [],
#     #
#     #     },
#     #     # 万州时报
#     #     {
#     #         "platformName": "万州时报",
#     #         "sourceProvince": "重庆",
#     #         "sourceCity": "万州",
#     #         # 1：国家级，2：省级，3：市级，0：商业类网站。
#     #         "sourceLevel": 3,
#     #         # 1：媒体类，2：政务类，3：商业类。
#     #         "sourceClassify": 1,
#     #         # 是否重点渠道。
#     #         "sourceImportance": 0,
#     #         # 是否主流媒体。
#     #         "mainMedia": 0,
#     #         # %Y%m/%d，{proxies}。
#     #         "start_url": "http://dpaper.sxcm.net/wzsb/html/%Y%m/%d/node_01.html",
#     #         "cookiestr": "",
#     #         # 版面url。
#     #         "layout_url_xpath": ['//ul[@id="widthNone"]/li/a[2]/@href'],
#     #         # 下一版链接
#     #         "layout_next_xpath": ['//div[@class="newsnext"]/a/@href'],
#     #         # 版面名称
#     #         "layout_title_xpath": ['//div[@class="newslisttit"]/em/text()'],
#     #         # 版面标签
#     #         "layout_map_xpath": ["//map[@name='PagePicMap']"],
#     #         # 版面图链接
#     #         "layout_map_image_xpath": ["//img[@usemap='#PagePicMap']/@src"],
#     #         "layout_large_image_xpath": [],
#     #         # 版面图链接pdf链接
#     #         "layout_pdf_xpath": [],
#     #         # 稿件详情。
#     #         "detail_url_xpath": ["//map[@name='PagePicMap']/area/@href"],
#     #         # 预标题
#     #         "detail_pre_title_xpath": ['//p[@id="PreTitle"]/text()'],
#     #         # 主标题
#     #         "detail_title_xpath": ['//h3[@id="Title"]/text()'],
#     #         # 子标题
#     #         "detail_sub_title_xpath": ['//p[@id="SubTitle"]/text()'],
#     #         # 作者
#     #         "detail_author_xpath": [],
#     #         # 正文内容
#     #         "detail_content_xpath": ['//div[@class="newsdetatext"]'],
#     #         # 提交时间
#     #         "detail_pubTime_xpath": [],
#     #
#     #     },
#     #     # 沙坪坝报(并未能实时更新)
#     #     {
#     #         "platformName": "沙坪坝报",
#     #         "sourceProvince": "重庆",
#     #         "sourceCity": "",
#     #         # 1：国家级，2：省级，3：市级，0：商业类网站。
#     #         "sourceLevel": 3,
#     #         # 1：媒体类，2：政务类，3：商业类。
#     #         "sourceClassify": 1,
#     #         # 是否重点渠道。
#     #         "sourceImportance": 0,
#     #         # 是否主流媒体。
#     #         "mainMedia": 0,
#     #         # %Y-%m/%d，{proxies}。
#     #         "start_url": "http://www.cnepaper.com/spbb/html/%Y-%m/%d/node_100641.htm",
#     #         "cookiestr": "",
#     #         # 版面url。
#     #         "layout_url_xpath": ['//td[@class="default"]/a[@id="pageLink"]/@href'],
#     #         # 下一版链接
#     #         "layout_next_xpath": ['//a[@id="ed_next"][@class="preart"]/@href'],
#     #         # 版面名称
#     #         "layout_title_xpath": ['//td[@align="left"]/strong/text()'],
#     #         # 版面标签
#     #         "layout_map_xpath": ["//map[@name='PagePicMap']"],
#     #         # 版面图链接
#     #         "layout_map_image_xpath": ["//img[@usemap='#PagePicMap']/@src"],
#     #         "layout_large_image_xpath": [],
#     #         # 版面图链接pdf链接
#     #         "layout_pdf_xpath": ['//td[@valign="center"]/a/@href'],
#     #         # 稿件详情。
#     #         "detail_url_xpath": ["//map[@name='PagePicMap']/area/@href"],
#     #         # 预标题
#     #         "detail_pre_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][1]/td/text()'],
#     #         # 主标题
#     #         "detail_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][2]/td//text()'],
#     #         # 子标题
#     #         "detail_sub_title_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][3]/td/text()'],
#     #         # 作者
#     #         "detail_author_xpath": ['//table[@class="wz"]//table//tr[@valign="top"][4]/td/text()'],
#     #         # 正文内容
#     #         "detail_content_xpath": ['//table[@id="newspic"]//table//td | //div[@id="ozoom"]'],
#     #         # 提交时间
#     #         "detail_pubTime_xpath": [],
#     #
#     #     },
#     # ]
#     for paper_template in con_mysql():
#         try:
#             name = paper_template["platformName"]
#             paper_template["platformType"] = 6
#             # source_level = paper_template["sourceLevel"]
#             # source_classify = paper_template["sourceClassify"]
#             # source_importance = paper_template["sourceImportance"]
#             media = paper_template['mainMedia']
#             p = eval(paper_template["epaperTemplate"])
#             pp = eval(p["epaperTemplate"])
#             # ppp = eval(pp["epaperTemplate"])
#             # d = eval(ppp["epaperTemplate"])
#             # dd = eval(d["epaperTemplate"])
#             paper_temp = json.dumps(pp)
#             print(paper_temp)
#
#             sql = "UPDATE epaper_template SET epaperTemplate=%s where id=2"
#             val = (paper_temp, name)
#             try:
#                 cursor.execute(sql, val)
#                 conmysql.commit()
#                 print(f'{name}ok')
#             except Exception as e:
#                 continue
#         except Exception as e:
#             print(e)
#             continue
#     print("全部更新完成")
#     cursor.close()
#     conmysql.close()


# def update_one():
#     """
#     更新单条数据
#     :return:
#     """
#     conmysql, cursor = conn_mysql()
#     paper = {
#
#             "platformName": "人民日报海外版",
#             "sourceProvince": "北京",
#             "sourceCity": "",
#             # 1：国家级，2：省级，3：市级，0：商业类网站。
#             "sourceLevel": 1,
#             # 1：媒体类，2：政务类，3：商业类。
#             "sourceClassify": 2,
#             # 是否重点渠道。
#             "sourceImportance": 1,
#             # 是否主流媒体。
#             "mainMedia": 1,
#             # %Y-%m/%d，{proxies}。
#             "start_url": "http://paper.people.com.cn/rmrbhwb/html/%Y-%m/%d/node_865.htm",
#             "cookiestr": "",
#             # 版面url。
#             "layout_url_xpath": ["//a[@id='pageLink']/@href"],
#             # 下一版链接
#             "layout_next_xpath": [],
#             # 版面名称
#             "layout_title_xpath": ["//div[@class='paper-bot']/p/text()"],
#             # 版面标签
#             "layout_map_xpath": ["//div[@class='paper']/map"],
#             # 版面图链接
#             "layout_map_image_xpath": ["//div[@class='paper']/img/@src"],
#             "layout_large_image_xpath": [],
#             # 版面图链接pdf（大图）链接
#             "layout_pdf_xpath": ["//p[@class='right btn']/a/@href"],
#             # 稿件详情。
#             # 从版面图的map标签中获取详情页链接
#             "detail_url_xpath": ["//map[@name='PagePicMap']/area/@href"],
#             # 预标题
#             "detail_pre_title_xpath": ["//div[@class='article']/h3/text()"],
#             # 主标题
#             "detail_title_xpath": ["//div[@class='article']/h1/text()"],
#             # 子标题
#             "detail_sub_title_xpath": ["//div[@class='article']/h2/text()"],
#             # 作者
#             "detail_author_xpath": [],
#             # 正文内容
#             "detail_content_xpath": ["//table[@class='pci_c']//td | //div[@id='ozoom']"],
#             # 提交时间
#             "detail_pubTime_xpath": [],
#             "platformType": 6
#
#         }
#     paper_temp = json.dumps(paper)
#     sql = "UPDATE epaper_template SET epaperTemplate=%s where id=2"
#     try:
#         cursor.execute(sql, paper_temp)
#         conmysql.commit()
#         print(f'更新成功')
#     except Exception as e:
#         print(e)
#     cursor.close()
#     conmysql.close()

# update_one()


# def select():
#     """
#     检索数据
#     :return:
#     """
#     conmysql, cursor = conn_mysql()
#     for paper_template in con_mysql():
#         try:
#             name = paper_template["platformName"]
#             paper_temp = eval(paper_template["epaperTemplate"])
#             # paper_temp = json.loads(p)
#             if "platformType" in paper_temp:
#                 print(f"{name}数据体中存在该属性")
#                 continue
#             else:
#                 print(f"{name}数据体中不hanyou该属性")
#                 paper_temp["platformType"] = 6
#                 paper_temps = json.dumps(paper_temp)
#                 sql = "UPDATE epaper_template SET epaperTemplate=%s where platformName=%s"
#                 val = (paper_temps, name)
#                 try:
#                     cursor.execute(sql, val)
#                     conmysql.commit()
#                     print(f'{name}添加成功')
#                 except Exception as e:
#                     continue
#         except Exception as e:
#             print(e)
#             continue
#     cursor.close()
#     conmysql.close()

# select()
