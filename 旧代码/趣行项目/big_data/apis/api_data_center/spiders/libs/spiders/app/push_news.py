#!/usr/bin/env python3
# -*- coding:utf-8
# Author Keane
# coding=utf-8
# @Time    : 2021/1/21 18:04
# @File    : push_news.py
# @Software: PyCharm
import hashlib
import json
import logging
import re
import time

import requests

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class PushNews(Appspider):
    @staticmethod
    def md5(data):
        ha = hashlib.md5()
        ha.update(data.encode("utf-8"))
        res = ha.hexdigest()
        return res

    def huan_qiu_time(self):
        url = "https://api.hqtime.huanqiu.com/api/news/list/push/history"
        headers = {
            "accept": "application/vnd.hq_time.v2+json",
            "content-type": "application/json",
            "user-agent": "(Linux; Android 6.0.1; Build/Android MuMu) huanqiuTIME/10.1.0",
            "clientversion": "Android/v10.1.0",
            "x-timestamp": "1611228319",
            "x-nonce": "uooh4ag1",
            "x-sign": "806eca39f292db1b64f61139d321df9ced63a0c803c0b6c28942fbfb8e132d88",
            "Host": "api.hqtime.huanqiu.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        list_res = self.session.get(url, headers=headers)
        if list_res.status_code == requests.codes.ok:
            list_res = json.loads(list_res.content)
            for date, newses in list_res["data"].items():
                for news in newses:
                    worker_id = news["aid"]
                    share_url = news["url"]
                    url = f"https://hqtime.huanqiu.com/article/{worker_id}?recommend=1&app=1&ver=1&fontSize=normal"
                    article_headers = {
                        "Host": "hqtime.huanqiu.com",
                        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 "
                                      "(KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
                        "X-Requested-With": "com.huanqiu.news",
                    }
                    article_res = self.session.get(url, headers=article_headers)
                    if article_res.status_code == requests.codes.ok:
                        article_res = article_res.content.decode()
                        article_data = re.findall(r'var article = JSON.parse\((.*?)\)', article_res)
                        # article_data = json.loads(json.dumps(json.loads(article_data[0]),indent=4,ensure_ascii=False))
                        article_data = json.loads(json.loads(article_data[0]))
                        article_fields = InitClass().article_fields()
                        article_fields["appname"] = self.newsname
                        article_fields["platformID"] = self.platform_id
                        article_fields["workerid"] = article_data["aid"]
                        article_fields["url"] = share_url
                        article_fields["pubtime"] = article_data["ctime"]
                        article_fields["title"] = article_data["title"]
                        article_fields["editor"] = article_data["editor"]["name"]
                        article_fields["source"] = article_data["source"]["name"]
                        article_fields["content"] = article_data["content"]
                        if article_data["cover"]:
                            article_fields["articlecovers"] = [article_data["cover"]]
                        article_fields["ispush"] = 1
                        article_fields = InitClass().wash_article_data(article_fields)
                        yield {"code": 1, "msg": "OK", "data": {"works": article_fields}}

    def ren_min_ri_bao(self):
        url = "https://app.peopleapp.com/Api/700/MineApi/pushHistory?"
        headers = {
            'Cookie': 'acw_tc="2760825816112971405924254e36a334573515c0d7751715fed41a208995f7";$Path="/";$Domain="'
                      'app.peopleapp.com"; SERVERID=0ada8651e904573396f35517addf582c|1611298754|1611298754',
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR);DailyNewspaper/7.0.2",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "app.peopleapp.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Content-Length": "0",
        }
        data = {
            "city": "北京市",
            "citycode": "010",
            "device": "6fcb5018-aaeb-3195-ab04-16b4581463ed",
            "device_model": "MuMu",
            "device_os": "Android 6.0.1",
            "device_product": "Netease",
            "device_size": "576*1024",
            "device_type": "1",
            "district": "东城区",
            "fake_id": "66483287",
            "interface_code": "702",
            "latitude": "39.908581634349815",
            "longitude": "116.39732329636996",
            "page": "1",
            "province": "北京市",
            "province_code": "4406542",
            "show_num": "20",
            "user_id": "0",
            "version": "7.0.2",
            # "securitykey":"1c350c4f71e09e16beaea6838295d85c",
        }
        n = ''
        for key in data.keys():
            n += data[key] + '|'
        n = n[0:-1] + 'rmrbsecurity$#%sut49fbb427a508bcc'
        securitykey = self.md5(n)
        data['securitykey'] = securitykey
        article_lists = self.session.get(url, headers=headers, params=data)
        if article_lists.status_code == requests.codes.ok:
            article_lists = json.loads(article_lists.content)
            if isinstance(article_lists, dict):
                for article_list in article_lists["data"]:
                    for article_bre in article_list["article"]:
                        article_url = "https://app.peopleapp.com/Api/700/ArtInfoApi/getArticleData?"
                        article_id = article_bre["id"]
                        article_type = article_bre["news_type"]
                        article_types = {"cms": "0", "gov": "2"}
                        article_type = article_types.get(article_type)
                        article_data = {
                            "article_id": article_id,
                            "city": "北京市",
                            "citycode": "010",
                            "device": "6fcb5018-aaeb-3195-ab04-16b4581463ed",
                            "device_model": "MuMu",
                            "device_os": "Android 6.0.1",
                            "device_product": "Netease",
                            "device_size": "576*1024",
                            "device_type": "1",
                            "district": "东城区",
                            "fake_id": "66483287",
                            "interface_code": "702",
                            "latitude": "39.908581634349815",
                            "longitude": "116.39732329636996",
                            "province": "北京市",
                            "province_code": "4958643",
                            "type": article_type,
                            "user_gov_id": "0",
                            "user_id": "0",
                            "version": "7.0.2",
                            # "securitykey":"dc8d8ef89c1963e3a96b4bb88982a0da",
                        }
                        n = ''
                        for key in article_data:
                            n += article_data[key] + '|'
                        n = n[0:-1] + 'rmrbsecurity$#%sut49fbb427a508bcc'
                        securitykey = self.md5(n)
                        article_data['securitykey'] = securitykey
                        time.sleep(1)
                        article_res = self.session.get(article_url, headers=headers, params=article_data)
                        if article_res.status_code == requests.codes.ok:
                            article = json.loads(article_res.content)
                            article = article["frontend"]
                            article_field = InitClass().article_fields()
                            article_field["appname"] = self.newsname
                            article_field["platformID"] = self.platform_id
                            article_field["title"] = article["title_inner"]
                            article_field["workerid"] = article_bre["id"]
                            article_field["url"] = article_bre["share_url"]
                            article_field["content"] = article["contents"]
                            article_field["articlecovers"] = [article_bre["share_image"]]
                            article_field["pubtime"] = int(article["news_datetime"]) * 1000
                            article_field["readnum"] = int(article["read_count"])
                            article_field["source"] = article["copyfrom"]
                            article_field["ispush"] = 1
                            article_field["author"] = article["authors"]
                            article_field["editor"] = article["admin_name"]
                            fields = InitClass().wash_article_data(article_field)
                            yield {"code": 1, "msg": "OK", "data": {"works": fields}}

    def push_news_yield(self):
        if self.newsname == "人民日报客户端":
            for data in self.ren_min_ri_bao():
                yield data
        elif self.newsname == "环球Time移动端":
            for data in self.huan_qiu_time():
                yield data
        else:
            pass


if __name__ == '__main__':
    push_news = PushNews("人民日报客户端", logging)
    for i in push_news.ren_min_ri_bao():
        print(i, type(i))
