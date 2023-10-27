# -*- coding:utf-8 -*-
"""
# project:
# author: Neil
# date: 2020/12/9
# update: 2020/12/9
"""

import random
import time
import traceback
import requests
from lxml import etree
from api_common_utils.proxy import get_abuyun_proxies
from api_common_utils.comm_utils import CommUtils


class XinLangSearch:

    def __init__(self, log, queryword):

        self._queryword = queryword
        self._session = requests.session()
        self._headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/87.0.4280.88 Safari/537.36",
            "Cookie": "U_TRS1=00000029.1aaa56ee.5fca0726.b06a3fa6; "
                      "UOR=www.baidu.com,blog.sina.com.cn,; "
                      "SINAGLOBAL=222.223.213.34_1607075623.698954; "
                      "vjuids=17a2841e.17642491b89.0.667a5a2047348; vjlast=1607429856; "
                      "beegosessionID=49ef2eaeab7ccd9267bb862f721e74b0; "
                      "SEARCH-SINA-COM-CN=37f74a9f53ebe4bdbdbaca38a6b451f7; "
                      "Apache=222.223.213.34_1607475773.206544; "
                      "_ga=GA1.3.1716967120.1607475774; _gid=GA1.3.841527693.1607475774;"
                      "ULV=1607476020185:5:5:4:222.223.213.34_1607475773.206544:1607475773436;"
                      "UM_distinctid=176451a9c7289f-08ea98558b1bbc-c791039-240000-176451a9c73872;"
                      "__gads=ID=39cba368078375d5-223cd77b13c500d6:T=1607477141:RT=1607477141:"
                      "S=ALNI_MakIF1P3XpcKXtK7-lZKKXpDUEahg; lxlrttp=1578733570"
        }
        self._session.headers.update(self._headers)
        self._session.proxies = get_abuyun_proxies()
        self._timeout = 10
        self._logger = log

    def xinlangsearch(self):
        """
        新浪搜索
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
            for i in range(1, 3):
                try:
                    next_url = f"http://search.sina.com.cn/?q={queryword}&c=news&size=20&page={i}"
                    time.sleep(random.random())
                    response = self._session.get(url=next_url, timeout=self._timeout)
                    tree = etree.HTML(response.text)
                    xinlangresultlist = tree.xpath("//div[@class='box-result clearfix']")
                    for xinlangresult in xinlangresultlist:
                        try:
                            xinlangresultdict = dict()
                            elementa = xinlangresult.xpath(".//h2/a")
                            if elementa:
                                elementa = elementa[0]
                            else:
                                continue
                            xinlangresultdict["title"] = elementa.xpath("string(.)").replace("\n", "").replace("  ", "")
                            digest = "".join(xinlangresult.xpath(".//p[@class='content']//text()"))
                            if digest:
                                xinlangresultdict["digest"] = digest.replace("\n", "").replace("  ", "")
                            else:
                                xinlangresultdict["digest"] = ""

                            xinlangurl = elementa.xpath("@href")
                            if xinlangurl:
                                xinlangurl = xinlangurl[0]
                            else:
                                continue
                            if xinlangresultdict["title"] in result:
                                continue
                            else:
                                xinlangresultdict["matchtitle"] = \
                                    "".join(xinlangresult.xpath
                                            (".//p[@class='content']/font/text()")).replace("\n", "").replace("  ", "")
                                simvalue = CommUtils().getsimilarity(queryword, xinlangresultdict["matchtitle"])
                                findnum = xinlangresultdict["matchtitle"].find(queryword)
                                if simvalue > 0.6 or findnum != -1:
                                    public_time = xinlangresult.xpath(".//span[@class='fgray_time']/text()")[0]
                                    if public_time:
                                        pub_time = public_time.split(" ")[1] + ' ' + public_time.split(" ")[2]
                                        xinlangresultdict["pubTime"] = \
                                            int(time.mktime(time.strptime(pub_time, "%Y-%m-%d %H:%M:%S")))
                                    else:
                                        xinlangresultdict["pubTime"] = 0

                                    xinlangresultdict["source"] = public_time.split(" ")[0]
                                    xinlangresultdict["matchScore"] = simvalue
                                    # time.sleep(random.random())
                                    # # 判断是否会存在跳转地址
                                    # r = requests.get(xinlangurl, allow_redirects=False, timeout=self._timeout)
                                    # etree.HTML(r.text)
                                    xinlangresultdict["url"] = xinlangurl
                                    xinlangresultdict["source"] = "新浪搜索"
                                    returnlist.append(xinlangresultdict)
                                    result.add(xinlangresultdict["title"])
                        except Exception as e:
                            self._logger.warning(f"xinlangsearch{e}\n{traceback.format_exc()}")
                            continue
                except Exception as e:
                    self._logger.warning(f"xinlangsearch{e}\n{traceback.format_exc()}")
                    continue
            returndict = dict()
            returndict["data"] = returnlist
            return returndict
        except Exception as e:
            self._logger.warning(f"xinlangsearch{e}\n{traceback.format_exc()}")
            return {"msg": "xinlangsearch failed"}
