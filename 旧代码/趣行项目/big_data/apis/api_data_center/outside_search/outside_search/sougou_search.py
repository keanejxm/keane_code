# -*- coding:utf-8 -*-
"""
# project: 搜狗搜索
# author: Neil
# date: 2020/12/9
# update: 2020/12/9
"""

import re
import random
import time
import traceback
import requests
from lxml import etree
from api_common_utils.proxy import get_abuyun_proxies
from api_common_utils.comm_utils import CommUtils


class SouGouSearch:

    def __init__(self, log, queryword):

        self._queryword = queryword
        self._session = requests.session()
        self._headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,"
                      "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/87.0.4280.88 Safari/537.36",
            "Cookie": "ssuid=6519673930; ABTEST=4|1607429762|v17; IPLOC=CN1301; "
                      "SUID=22D5DFDE2208990A000000005FCF6E82; SUV=1607429762510684; "
                      "browerV=3; osV=1; SNUID=9A6C6766B9BD0C4A508F4225B9C14ABE; pgv_pvi=2844106752; sst0=413;"
                      "ld=jlllllllll2K8LfglllllV@yg6llllllTH@qwkllllGllllljylll5@@@@@@@@@@",
            "Host": "www.sogou.com"
        }
        self._session.headers.update(self._headers)
        self._session.proxies = get_abuyun_proxies()
        self._timeout = 15
        self._logger = log

    def sougousearch(self):
        """
        搜狗搜索
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
            for i in range(1, 5):
                try:
                    next_url = f"https://www.sogou.com/web?query={queryword}&page={i}&ie=utf8"
                    time.sleep(random.random())
                    response = self._session.get(url=next_url, timeout=self._timeout)
                    tree = etree.HTML(response.text)
                    sougouresultlist = tree.xpath("//div[@class='results']/div")
                    for sougouresult in sougouresultlist:
                        try:
                            sougouresultdict = dict()
                            elementa = sougouresult.xpath(".//h3/a")
                            if elementa:
                                elementa = elementa[0]
                            else:
                                continue
                            sougouresultdict["title"] = elementa.xpath("string(.)") \
                                .replace("\n", "").replace("  ", "").replace("\r", "")
                            digest = "".join(sougouresult.xpath(".//p[@class='str_info']//text()"))
                            if digest:
                                sougouresultdict["digest"] = digest.replace\
                                    ("\n", "").replace("  ", "").replace("\r", "")
                            else:
                                sougouresultdict["digest"] = ""
                            sougouurl = elementa.xpath("@href")
                            if sougouurl:
                                sougouurl = sougouurl[0]
                                sougouurl = f"https://www.sogou.com{sougouurl}"
                            else:
                                continue
                            if sougouresultdict["title"] in result:
                                continue
                            else:
                                sougouresultdict["matchtitle"] = "".join\
                                    (elementa.xpath(".//em/text()")).replace("\n", "").replace("  ", "")
                                simvalue = CommUtils().getsimilarity(queryword, sougouresultdict["matchtitle"])
                                findnum = sougouresultdict["matchtitle"].find(queryword)
                                if simvalue > 0.6 or findnum != -1:
                                    sougouresultdict["matchScore"] = simvalue
                                    time.sleep(random.random())
                                    r = requests.get(sougouurl, allow_redirects=False, timeout=self._timeout)
                                    resulturl = re.findall(r"window.location.replace\((.*)\)", r.text)[0][1:-1]
                                    sougouresultdict["url"] = resulturl
                                    sougouresultdict["source"] = "搜狗搜索"
                                    returnlist.append(sougouresultdict)
                                    result.add(sougouresultdict["title"])
                        except Exception as e:
                            self._logger.warning(f"sougousearch{e}\n{traceback.format_exc()}")
                            continue
                except Exception as e:
                    self._logger.warning(f"sougousearch{e}\n{traceback.format_exc()}")
                    continue
            returndict = dict()
            returndict["data"] = returnlist
            return returndict
        except Exception as e:
            self._logger.warning(f"sougousearch{e}\n{traceback.format_exc()}")
            return {"msg": "sougousearch failed"}