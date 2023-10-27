# -*- coding:utf-8 -*-
"""
# project: 360搜索
# author: Neil
# date: 2020/12/8
# update: 2020/12/8
"""


import random
import re
import time
import traceback
import requests
from lxml import etree
from api_common_utils.comm_utils import CommUtils
from api_common_utils.proxy import get_abuyun_proxies


class SanLiuOSearch:

    def __init__(self, log, queryword):
        self._session = requests.session()
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/69.0.3497.81 Safari/537.36",
            "Cookie": "QiHooGUID=1826C193B1BED3EFE01740202DB8F92B.1607411929895;"
            " __guid=15484592.4025295237584162300.1607411930888.706; dpr=1.25; "
            "webp=1; _S=pdc9uhp20cgvt5anej8048v975; so_huid=114NK3n2r4LhGld%2FzT44UMzGQlE%2FEZCZNpXP0UBIZ70FQ%3D; "
            "__huid=114NK3n2r4LhGld%2FzT44UMzGQlE%2FEZCZNpXP0UBIZ70FQ%3D; gtHuid=1; homeopenad=1; "
            "_uc_silent=1; count=15; erules=p1-42%7Ckd-2%7Cp4-27%7Cecr-1%7Cp2-3",
            "Host": "www.so.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                      "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }
        self._session.headers.update(self._headers)
        self._session.proxies = get_abuyun_proxies()
        self._queryword = queryword
        self._logger = log

    def search360(self):
        """
        360搜索
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
            for i in range(1, 4):
                try:
                    time.sleep(random.random())
                    start_url = f"https://www.so.com/s?q={queryword}&pn={i}"
                    response = self._session.get(start_url, timeout=10)
                    tree = etree.HTML(response.text)
                    _360resultlist = tree.xpath("//li[@class='res-list']")
                    for _360result in _360resultlist:
                        try:
                            _360resultdict = {}
                            elementa = _360result.xpath("h3/a")
                            if elementa:
                                elementa = elementa[0]
                            else:
                                continue
                            _360resultdict["title"] = elementa.xpath("string(.)").replace("\n", "").replace("  ", "")
                            # 摘要
                            digest = "".join(_360result.xpath(".//p[@class='res-desc']//text()"))
                            if digest:
                                _360resultdict["digest"] = digest.replace("\n", "").replace("  ", "").replace("\r", "")
                            else:
                                _360resultdict["digest"] = ""
                            # url
                            _360url = elementa.xpath("@href")
                            if _360url:
                                _360url = _360url[0]
                            else:
                                continue
                            if _360resultdict["title"] in result:
                                continue
                            else:
                                _360resultdict["matchtitle"] = "".join(elementa.xpath("em/text()"))
                                simvalue = CommUtils().getsimilarity(queryword, _360resultdict["matchtitle"])
                                findnum = _360resultdict["matchtitle"].find(queryword)
                                if simvalue > 0.6 or findnum != -1:
                                    _360resultdict["matchScore"] = simvalue
                                    time.sleep(random.random())
                                    r = requests.get(_360url, headers=self._headers, allow_redirects=False, timeout=5)
                                    resulturl = re.findall(r"window.location.replace\((.*)\)", r.text)[0][1:-1]
                                    _360resultdict["url"] = resulturl
                                    _360resultdict["source"] = "360搜索"
                                    returnlist.append(_360resultdict)
                                    result.add(_360resultdict["title"])
                        except Exception as e:
                            self._logger.warning(f"360search{e}\n{traceback.format_exc()}")
                            continue
                except Exception as e:
                    self._logger.warning(f"360search{e}\n{traceback.format_exc()}")
                continue
            returndict = dict()
            returndict["data"] = returnlist
            return returndict
        except Exception as e:
            self._logger.warning(f"360search{e}\n{traceback.format_exc()}")
            return {"msg": "360search failed"}
