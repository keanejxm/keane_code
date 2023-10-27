# -*- coding:utf-8 -*-

"""
# 法制日报-法制号app
# author: Chris
# date: 2020/12/3
# update: 2020/12/3
"""
import json
import requests
import traceback

from spiders.libs.spiders.app.initclass import InitClass
from spiders.libs.spiders.app.appspider_m import Appspider


class FaZhiHaoApp:
    """不用了，InitClass中的参数字段值写死了，不适合在这里用,整体思路是获取频道列表，然后新闻列表，然后新闻详细"""

    def __init__(self):
        self._session = requests.Session()
        self._headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; VOG-AL10 Build/HUAWEIVOG-AL10",
        }

    def get_channel_list(self):
        """
        获取全部频道列表--未解析
        :return:
        """
        url = "http://appwx.legaldaily.com.cn:8080/amc/client/listSubscribeColumn"
        data = {
            "nodeCode": "ecdc5307-888e-4322-8817-f04bd81a7e82",
            "contentType": "0,6,11",
        }
        resp = self._session.get(url, params = data, headers = self._headers)
        res = json.loads(resp.text)
        if not res["data"]["list"]:
            raise ValueError("获取频道列表失败")
        channel_res = []
        for channel in res["data"]["list"]:
            channel_dict = dict()
            channel_dict["name"] = channel["columnName"]
            channel_dict["id"] = channel["columnId"]
            channel_res.append(channel_dict)
        return channel_res


    def run(self):
        channels_res = self.get_channel_list()


if __name__ == '__main__':
    FaZhiHaoApp().run()
