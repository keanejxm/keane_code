# -*- coding:utf-8 -*-

"""
# author: Chris
# date: 2020/12/3
# update: 2020/12/3
"""

import json
import time
import random
import hashlib
import requests
import traceback
import pandas as pd
from lxml import etree
from urllib.parse import urljoin
from threading import Thread

from api_common_utils.mysql_utils import MySQLUtils
from api.config import mysql_config

from api_common_utils.proxy import get_abuyun_proxies   # 阿布云代理

from api_common_utils.llog import LLog
log_path = r"/home/debugger/chris/big_data/big_data_platform/lib/resources/weibo/"
logger = LLog("test", log_path=log_path, logger_level="DEBUG").logger


def md5(strsea, charset="UTF-8"):
    # 字符串转md5格式
    _md5 = hashlib.md5()
    _md5.update(strsea.encode(charset))
    return _md5.hexdigest()


class XinYuanAccount:

    def __init__(self, info):
        self.keyword = info[0]      # 昵称
        part_sort = {"政府类微博": 1, "企业类微博": 2, "自媒体类微博": 3}
        self.part_sort = part_sort[info[4]]     # 所属分类
        self._request_headers = {
            "Host": "s.weibo.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "Keep-Alive",
            "Referer": "https://s.weibo.com/",
        }
        self._session = requests.Session()
        self._timeout = 10
        self._logger = logger

    def fetch(self):
        search_url = "https://s.weibo.com/user?q={}&Refer=index".format(self.keyword)
        a_proxies = get_abuyun_proxies()
        self._session.proxies = a_proxies
        resp = self._session.get(search_url, timeout=self._timeout)
        resp.encoding = "utf-8"
        if resp.status_code == requests.codes.ok:
            tree = etree.HTML(resp.text)
            card_list = tree.xpath("//div[@class='card card-user-b s-pg16 s-brt1']")
            ret1 = []
            if card_list:
                for card in card_list:
                    fields = {
                        "nick_name": self.keyword,
                        "avatar": "",
                        "url": "",
                        "uid": "",
                        "sex": 0,
                        "province": "",
                        "city": "",
                        # "auth_info": "",
                        # "desc": "",
                        # "label": ""
                    }
                    nick = "".join(card.xpath(".//div[@class='info']//a[@class='name']//text()"))
                    fields["nick_name"] = nick
                    # if nick == self.keyword:
                    fields["url"] = urljoin(resp.url, card.xpath(".//a[@class='name']/@href")[0].split("?")[0])
                    fields["avatar"] = urljoin(resp.url, card.xpath(".//div[@class='avator']//img/@src")[0].split("?")[0])
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
                    # fields["auth_info"] = card.xpath(".//p[2]/text()")[0]
                    # x = ",".join(card.xpath(".//p[2]/text()"))
                    # try:
                    #     fields["desc"] = card.xpath(".//p[4]/text()")[0]
                    # except:
                    #     fields["desc"] = ""
                    # try:
                    #     fields["label"] = ",".join(card.xpath("string(.//p[5])"))
                    # except:
                    #     fields["label"] = ""
                    ret1.append(fields)
                """处理excel表时用以下，而正常搜索时则返回结果列表"""
                ret2 = [i["nick_name"] for i in ret1]
                self._logger.info(f"--{self.keyword}--的搜索结果是：{ret2}")
                result = [i for i in ret1 if i["nick_name"] == self.keyword]
                if len(result) == 0:
                    self._logger.warning(f"{self.keyword}的搜索结果在没有匹配项，除昵称外全部记录空值")
                    result = [{"nick_name": self.keyword, "avatar": "", "url": "", "uid": "", "sex": 0, "province": "",
                               "city": "", "auth_info": "", "desc": "", "label": ""}]
            else:
                result = [{"nick_name": self.keyword, "avatar": "", "url": "", "uid": "", "sex": 0, "province": "",
                           "city": "", "auth_info": "", "desc": "", "label": ""}]
                self._logger.warning("{}搜索，未找到相关目标……".format(self.keyword))
        else:
            result = [{"nick_name": self.keyword, "avatar": "", "url": "", "uid": "", "sex": 0, "province": "",
                       "city": "", "auth_info": "", "desc": "", "label": ""}]
            self._logger.warning(f"请求出错……状态码是：{resp.status_code}")
        return result

    def xinyuan_to_sql(self):
        # 连接MuSQL。
        result = self.fetch()
        db = MySQLUtils(**mysql_config)
        # result = XinYuanAccount("大邑县妇联").fetch()
        try:
            ret = result[0]
            fields = dict(
                platformName="微博",
                platformType=2,
                mediaUid=ret["uid"],
                name=ret["nick_name"],
                avatar=ret["url"],
                sex=ret["sex"],
                province=ret["province"],
                city=ret["city"],
                classify=self.part_sort,
                createTime=int(time.time() * 1000),
                updateTime=int(time.time() * 1000)
            )
            res = db.insert("weibo_copy", fields)
            # print(res)
        except Exception as e:
            self._logger.warning(f" {e}.\n{traceback.format_exc()}")
        time.sleep(random.uniform(3, 6))

    def fetch_api(self):
        # ret = self.fetch()
        # # print(json.dumps(ret, indent=4, ensure_ascii=False))
        # return ret
        self.xinyuan_to_sql()


def part_read_excel(df_name, i):

    df1 = df_name.iloc[i * 300:(i + 1) * 300, :]
    info_list = df1.values.tolist()
    for info in info_list:
        try:
            XinYuanAccount(info).fetch_api()
        except Exception as e:
            logger.warning(f"--{info[0]}--的搜索报错准备进入txt文档: {e}.\n{traceback.format_exc()}")
            # 记录搜索报错的微博昵称，以待再次搜索
            with open(log_path + "error_res.txt", "a", encoding="utf8") as f:
                f.write(json.dumps(info, ensure_ascii=False))
                f.write("\n")
            continue


if __name__ == '__main__':
    exe_path = r"/home/debugger/chris/big_data/big_data_platform/lib/sourceExcel/weibo/lewis_0927.xlsx"
    df = pd.read_excel(exe_path)
    ret = []
    part_read_excel(df, 1)
    # for j in range(11):
    #     t = Thread(target=part_read_excel, args=(df, j))
    #     t.setDaemon(True)
    #     ret.append(t)
    # for t in ret:
    #     t.start()
    #     time.sleep(3)
    # for t in ret:
    #     t.join()
# 企业类、自媒体类、政府类


