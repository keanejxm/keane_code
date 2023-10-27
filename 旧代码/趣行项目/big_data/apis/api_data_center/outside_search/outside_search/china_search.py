# -*- coding:utf-8 -*-
"""
# project:  中国搜索
# author: Neil
# date: 2020/12/9
# update: 2020/12/9
"""

import random
import time
import traceback
import requests
from lxml import etree
from api_common_utils.comm_utils import CommUtils
from api_common_utils.proxy import get_abuyun_proxies


class ChinaSearch:

    def __init__(self, log, queryword):
        self._session = requests.session()
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/69.0.3497.81 Safari/537.36",
            "Cookie": "__WWW_CARD__DISSTATUS__=false; __WWW_nav__DISSTATUS__=false; "
            "cookie_name=222.223.213.34.1607425123475945; uid=CgqATl/PXGOxaw9IA14qAg==; "
            "sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221764200e77c879-031aa167f06f8b-c791039-2359296"
            "-1764200e77d8c1%22%2C%22%24device_id%22%3A%221764200e77c879-031aa167f06f8b-c791039-2359296-"
            "1764200e77d8c1%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%"
            "E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2"
            "Flink%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D",
            "Host": "www.chinaso.com",
            "Accept": "application/json, text/plain, */*"
        }
        self._session.headers.update(self._headers)
        self._session.proxies = get_abuyun_proxies()
        self._queryword = queryword
        self._logger = log

    def chinasearch(self):
        """
        中国搜索
        :return:
        """
        result = set()
        returnlist = []
        queryword = self._queryword
        if queryword == "":
            return {"msg": "空值，无法查询"}
        if len(queryword) > 38:
            queryword = queryword[-38:]

        try:
            start_url = f"http://www.chinaso.com/v5/general/v1/web/search?q={queryword}&ps=30"
            response = self._session.get(start_url, timeout=10)
            response_json = response.json()["data"]
            if "data" in response_json and response_json["data"]:
                chinaresultlist = response_json["data"]
                for chinaresult in chinaresultlist:
                    try:
                        chinaresultdict = dict()
                        # 处理标签
                        if "title" in chinaresult and chinaresult["title"]:
                            title = chinaresult["title"].replace("\n", "").replace("  ", "").replace("\r", "")
                        else:
                            continue
                        # 摘要
                        if "snippet" in chinaresult and chinaresult["snippet"]:
                            digest = chinaresult["snippet"]
                            chinaresultdict["digest"] = \
                                digest.replace("\n", "").replace("  ", "").replace("\r", "")\
                                    .replace("<em>", "").replace("</em>", "")
                        else:
                            chinaresultdict["digest"] = ""
                        # url
                        if "url" in chinaresult and chinaresult["url"]:
                            chinaurl = chinaresult["url"]
                        else:
                            continue
                        # 时间戳
                        if "timestamp" in chinaresult and chinaresult["timestamp"]:
                            chinaresultdict["pubTime"] = chinaresult["timestamp"]
                        else:
                            chinaresultdict["pubTime"] = 0
                        # 来源
                        if "source" in chinaresult and chinaresult["source"]:
                            chinaresultdict["source"] = chinaresult["source"]
                        else:
                            chinaresultdict["source"] = ""

                        if title in result:
                            continue
                        else:
                            elementa = etree.HTML(title)
                            chinaresultdict["matchtitle"] = "".join(elementa.xpath(".//em/text()")).replace("\n", "") \
                                .replace("  ", "")
                            chinaresultdict["title"] = title.replace("<em>", "").replace("</em>", "")
                            simvalue = CommUtils().getsimilarity(queryword, chinaresultdict["matchtitle"])
                            findnum = chinaresultdict["matchtitle"].find(queryword)
                            if simvalue > 0.6 or findnum != -1:
                                chinaresultdict["matchScore"] = simvalue
                                time.sleep(random.random())
                                r = self._session.get(chinaurl, allow_redirects=False, timeout=10)
                                etree.HTML(r.text)
                                chinaresultdict["url"] = r.headers["location"]
                                chinaresultdict["source"] = "中国搜索"
                                returnlist.append(chinaresultdict)
                                result.add(chinaresultdict["title"])
                    except Exception as e:
                        self._logger.warning(f"chinasearch{e}\n{traceback.format_exc()}")
                        continue
                returndict = dict()
                returndict["data"] = returnlist
                return returndict
            else:
                return {"msg": "获取内容失败"}
        except Exception as e:
            self._logger.warning(f"chinasearch{e}\n{traceback.format_exc()}")
            return {"msg": "chinasearch failed"}