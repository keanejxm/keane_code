# -*- coding:utf-8 -*-
"""
# project:
# author: Neil
# date: 2020/12/28
# update: 2020/12/28
"""

import pymysql


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
    sql = f"select * from dxwz where sourceClassify = 2 and mainMedia = 1"
    try:
        cursor.execute(sql)
    except Exception as e:
        raise Exception('query error')
    mysql_result = cursor.fetchall()
    cursor.close()
    conmysql.close()
    return mysql_result


result_list = []
for i in con_mysql():
    web_dict = {
        "platformName": i.get("platformName"),
        "sourceCity": i.get("sourceCity", ""),
        "sourceProvince": i.get("sourceProvince", ""),
        "sourceLevel": i.get("sourceLevel", ""),
        "sourceClassify": i.get("sourceClassify", ""),
        "sourceImportance": i.get("sourceImportance", ""),
        "mainMedia": i.get("sourceLevel", ""),
        "start_url": i.get("start_url", ""),
        # cookie
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//div[@class=\"f-l w-839\"]/h2/a | //div[@class=\"f-l w-839\"]/p/a"],
        # 轮播信息
        "banner_news": ["//ul[@id=\"slide_pictures\"]/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//ul[@class=\"new-slider\"]/li/a | //div[@class=\"yaowen YH\"]/p/a | "
                             "//div[@class=\"allcontent mar-t-15\"]/div/p/a"],
        # 导航信息
        "channel_info_xpath": ["//div[@class=\"navWrap column\"]/ul/li/a"],
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
    }
    result_list.append(web_dict)

print(len(result_list))
print({"code": 0, "data": result_list})
