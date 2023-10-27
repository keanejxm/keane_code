# -*- coding:utf-8 -*-
"""
# project: 百度搜索
# author: Neil
# date: 2020/12/8
# update: 2020/12/8
"""

import random
import time
import traceback
import requests
from lxml import etree
from api_common_utils.proxy import get_abuyun_proxies
from api_common_utils.comm_utils import CommUtils


class BaiDuSearch:

    def __init__(self, log, queryword):
        self._session = requests.session()
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/69.0.3497.81 Safari/537.36",
            "Host": "www.baidu.com",
            "Cookie": "BIDUPSID=78268B528AF1647C595CBD245F721021; PSTM=1606725886; BD_UPN=12314753; "
                      "BDUSS=HpuazdkeEhaeXVhNE5ib1gzWnB-WHNMUzR0Wk1yN2lvMkJSWUlLVlc2SXppTzVmRVFBQUFBJCQAAAAAAAAAAAE"
                      "AAABp8j4vwffQ0M6o0rs5MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                      "AADP7xl8z-8ZfS; BDUSS_BFESS=HpuazdkeEhaeXVhNE5ib1gzWnB-WHNMUzR0Wk1yN2lvMkJSWUlLVlc2SXppTzVmRV"
                      "FBQUFBJCQAAAAAAAAAAAEAAABp8j4vwffQ0M6o0rs5MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                      "AAAAAAAAAAAAAAAAAAAAAADP7xl8z-8ZfS; BAIDUID=FEFD08A46B87593EE1E4CD0A237464D1:FG=1; "
                      "BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1433_33224_33059_32974_33098_33100_33218_"
                      "33198_33240_33149; delPer=0; BD_CK_SAM=1; PSINO=1; H_PS_645EC=9f15ZcLcHxh4AHOfhSig2K5BnB6NFXx"
                      "kNROJuWQn2AUZqcVwvBe4IzvLVE0; BA_HECTOR=2ha48421a00g2k2gt51ft3c5v0r",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,"
            "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }
        self._session.headers.update(self._headers)
        self._session.proxies = get_abuyun_proxies()
        self._logger = log
        self._queryword = queryword

    def baidusearch(self):
        """
        百度搜索
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
            # 默认取五页
            for i in range(0, 30, 10):
                try:
                    time.sleep(random.random())
                    start_url = f"https://www.baidu.com/s?wd={queryword}&pn={i}"
                    response = self._session.get(start_url, timeout=10)
                    tree = etree.HTML(response.text)
                    baiduresultlist = tree.xpath("//div[contains(@class, 'c-container') and contains(@class, 'result')]")
                    for baiduresult in baiduresultlist:
                        try:
                            baiduresultdict = dict()
                            elementa = baiduresult.xpath("h3/a")
                            if elementa:
                                elementa = elementa[0]
                            else:
                                continue
                            baiduresultdict["title"] = elementa.xpath("string(.)").replace("\n", "").replace("  ", "")
                            digest = "".join(baiduresult.xpath("//div[@class='c-abstract']//text()"))
                            if digest:
                                baiduresultdict["digest"] = digest.replace("\n", "").replace("  ", "")
                            else:
                                baiduresultdict["digest"] = ""
                            baiduurl = elementa.xpath("@href")
                            if baiduurl:
                                baiduurl = baiduurl[0]
                            else:
                                continue
                            if baiduresultdict["title"] in result:
                                continue
                            else:
                                baiduresultdict["matchtitle"] = "".join(elementa.xpath("em/text()"))
                                simValue = CommUtils().getsimilarity(queryword, baiduresultdict["matchtitle"])
                                findnum = baiduresultdict["matchtitle"].find(queryword)
                                if simValue > 0.6 or findnum != -1:
                                    baiduresultdict["matchScore"] = simValue
                                    time.sleep(random.random())
                                    r = self._session.get(baiduurl, allow_redirects=False, timeout=10)
                                    etree.HTML(r.text)
                                    baiduresultdict["url"] = r.headers["location"]
                                    baiduresultdict["source"] = "百度"
                                    returnlist.append(baiduresultdict)
                                    result.add(baiduresultdict["title"])
                        except Exception as e:
                            self._logger.warning(f"baidusearch{e}\n{traceback.format_exc()}")
                            continue
                except Exception as e:
                    self._logger.warning(f"baidusearch{e}\n{traceback.format_exc()}")
                continue
            returndict = dict()
            returndict["data"] = returnlist
            return returndict
        except Exception as e:
            self._logger.warning(f"baidusearch{e}\n{traceback.format_exc()}")
            return {"msg": "baidusearch failed"}
