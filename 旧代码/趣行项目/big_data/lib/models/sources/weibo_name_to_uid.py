# -*- coding:utf-8 -*-

"""
# author: Chris
# date: 2020/12/22
# update: 2020/12/22
"""

import json
import time
import random
import requests
from lxml import etree
from urllib.parse import urljoin

from common_utils.proxy import get_abuyun_proxies
from api_common_utils.llog import LLog


log_path = "/home/debugger/chris/big_data/big_data_platform/lib/models/sources_weibo_json/"
logger = LLog("test", log_path=log_path, logger_level="DEBUG").logger


class XinYuanAccount:

    def __init__(self):
        self._session = requests.Session()
        self._timeout = 10
        self._request_headers = {
            "Host": "s.weibo.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "Keep-Alive",
            "Referer": "https://s.weibo.com/",
        }

    def fetch(self, keyword):
        """这里传入的参数keyword是一个字典"""
        search_url = "https://s.weibo.com/user?q={}&Refer=index".format(keyword["name"])
        a_proxies = get_abuyun_proxies()
        self._session.proxies = a_proxies
        resp = self._session.get(search_url, timeout=self._timeout)
        resp.encoding = "utf-8"
        ret1 = []
        if resp.status_code == requests.codes.ok:
            tree = etree.HTML(resp.text)
            card_list = tree.xpath("//div[@class='card card-user-b s-pg16 s-brt1']")
            if card_list:
                for card in card_list:
                    fields = {
                        "nick_name": "",
                        "avatar": "",
                        "url": "",
                        "uid": "",
                        "sex": 0,
                        "province": "",
                        "city": ""
                    }
                    nick = "".join(card.xpath(".//div[@class='info']//a[@class='name']//text()"))
                    fields["nick_name"] = nick
                    fields["url"] = urljoin(resp.url, card.xpath(".//a[@class='name']/@href")[0].split("?")[0])
                    fields["avatar"] = urljoin(resp.url,
                                               card.xpath(".//div[@class='avator']//img/@src")[0].split("?")[0])
                    fields["uid"] = card.xpath(".//a[@class='s-btn-c']/@uid")[0]
                    sex_li = card.xpath(".//p[1]/i/@class")[0]
                    sex_lis = sex_li.split("-")[-1]
                    if sex_lis == "male":
                        fields["sex"] = 1
                    elif sex_lis == "female":
                        fields["sex"] = 2
                    area_info = "".join(card.xpath(".//p[1]//text()")[:-2])
                    area = area_info.split(" ")
                    area = [i for i in area if i and i != "\n"]
                    fields["province"] = area[0].strip()
                    try:
                        fields["city"] = area[1].strip()
                    except:
                        fields["city"] = ""
                    if nick == keyword["name"]:
                        logger.info(f"----{keyword['name']}已经找到了目标账号")
                        ret1.append(fields)
                        break
                if len(ret1) == 0:
                    logger.info(f"----{keyword['name']}经过比对未找到目标")
                    with open(log_path + "search_empty_res.txt", "a", encoding="utf8") as f:
                        f.write(json.dumps(keyword, ensure_ascii=False))
                        f.write("\n")
            else:
                with open(log_path + "search_empty_res.txt", "a", encoding="utf8") as f:
                    f.write(json.dumps(keyword, ensure_ascii=False))
                    f.write("\n")
                logger.warning(f"-------{keyword['name']}搜索，未找到相关目标……")
        else:
            logger.warning(f"------{keyword['name']}请求出错……状态码是：{resp.status_code}")
            with open(log_path + "error_res.txt", "a", encoding="utf8") as f:
                f.write(json.dumps(keyword, ensure_ascii=False))
                f.write("\n")
        time.sleep(random.uniform(1, 3))
        return ret1


if __name__ == '__main__':
    ret = XinYuanAccount().fetch("大美织金")
    print(ret)
