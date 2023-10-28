# -*- coding:utf-8 -*-

"""
# author: Chris
# date: 2020/11/30
# update: 2020/11/30
"""

import json
import requests
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class ZhongXinWangNews:

    def __init__(self):
        self._session = requests.Session()
        self._headers = {
            "User-Agent": "NewsApp/74.1 Android/5.1.1 (HUAWEI/VOG-AL10)",
        }

    def get_channel(self):
        url = "https://dw.chinanews.com/cns/app/v1/news_list/home"
        data = {
            "version_chinanews": "6.7.9",
            "deviceId_chinanews": "863064578382402",
            "platform_chinanews": "android",
            "source": "chinanews",
        }
        resp = self._session.get(url, params=data, headers=self._headers)
        print(resp.text)


ZhongXinWangNews().get_channel()
