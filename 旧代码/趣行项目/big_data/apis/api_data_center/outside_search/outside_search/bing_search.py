# -*- coding:utf-8 -*-
"""
# project:  Bing搜索,协议
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


class BingSearch:

    def __init__(self, log, queryword):

        self._queryword = queryword
        self._session = requests.session()
        self._headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/87.0.4280.88 Safari/537.36",
            "cookie": "SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=FC70A593F20E4A07819212173B36151C&dmnchg=1;"
                      " _EDGE_V=1; MUID=0A61D9707F0A6C672DA5D6EA7E496D8E; "
                      "MUIDB=0A61D9707F0A6C672DA5D6EA7E496D8E; SRCHUSR=DOB=20201208&T=1607425052000; "
                      "ipv6=hit=1607428653190&t=4; "
                      "ULC=P=1D7F4|1:1&H=1D7F4|1:1&T=1D7F4|1:1; _"
                      "SS=SID=3D133A4FBC64607E191B35D5BD27618F&bIm=413749; "
                      "ENSEARCH=BENVER=0; "
                      "SRCHHPGUSR=CW=2048&CH=178&DPR=1.25&UTC=480&DM=0&HV=1607425813&WTS=63743021852;"
                      "EDGE_S=mkt=zh-cn&F=1&SID=3D133A4FBC64607E191B35D5BD27618F"
        }
        self._session.headers.update(self._headers)
        self._session.proxies = get_abuyun_proxies()
        self._timeout = 20
        self._logger = log

    def bingsearch(self):
        result = set()
        returnlist = []
        queryword = self._queryword
        if queryword == "":
            return {"msg": "空值，无法查询"}
        if len(queryword) > 38:
            queryword = queryword[-38:]
        try:
            for i in range(1, 40, 10):
                try:
                    time.sleep(random.random())
                    next_url = f"https://cn.bing.com/search?q={queryword}&first={i}&FORM=PERE1"
                    response = self._session.get(url=next_url, timeout=self._timeout)
                    tree = etree.HTML(response.text)
                    bingresultlist = tree.xpath("//li[@class='b_algo']")
                    for bingresult in bingresultlist:
                        try:
                            bingresultdict = dict()
                            elementa = bingresult.xpath(".//h2/a")
                            if elementa:
                                elementa = elementa[0]
                            else:
                                continue
                            bingresultdict["title"] = elementa.xpath("string(.)").replace("\n", "").replace("  ", "")
                            digest = "".join(bingresult.xpath(".//div[@class='b_caption']/p//text()"))
                            if digest:
                                bingresultdict["digest"] = digest.replace("\n", "").replace("  ", "")
                            else:
                                bingresultdict["digest"] = ""
                            bingurl = elementa.xpath("@href")
                            if bingurl:
                                bingurl = bingurl[0]
                            else:
                                continue
                            if bingresultdict["title"] in result:
                                continue
                            else:
                                bingresultdict["matchtitle"] = "".join(elementa.xpath(".//strong/text()"))\
                                    .replace("\n", "")  .replace("  ", "")
                                simvalue = CommUtils().getsimilarity(queryword, bingresultdict["matchtitle"])
                                findnum = bingresultdict["matchtitle"].find(queryword)
                                if simvalue > 0.6 or findnum != -1:
                                    # 对比结果
                                    bingresultdict["matchScore"] = simvalue
                                    try:
                                        # time.sleep(random.random())
                                        # r = self._session.get(bingurl, allow_redirects=False,
                                        #                       timeout=self._timeout)
                                        # etree.HTML(r.text)
                                        bingresultdict["url"] = bingurl
                                        bingresultdict["source"] = "Bing"
                                        returnlist.append(bingresultdict)
                                        result.add(bingresultdict["title"])
                                    except Exception as e:
                                        self._logger.warning(f"bingsearch{e}\n{traceback.format_exc()}")
                                        continue
                        except Exception as e:
                            self._logger.warning(f"bingsearch{e}\n{traceback.format_exc()}")
                            continue
                except Exception as e:
                    self._logger.warning(f"bingsearch{e}\n{traceback.format_exc()}")
                    continue

            returndict = dict()
            returndict["data"] = returnlist
            return returndict
        except Exception as e:
            self._logger.warning(f"bingsearch{e}\n{traceback.format_exc()}")
            return {"msg": "bingsearch failed"}