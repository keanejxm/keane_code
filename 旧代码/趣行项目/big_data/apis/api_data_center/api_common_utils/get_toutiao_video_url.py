#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
功能描述。
# author: Keane
# create date: 2020/11/14
# update date: 2020/11/14
"""
import random
import re
from zlib import crc32
import requests
import json
import base64


class GetToutiaoVideoUrl(object):
    @staticmethod
    def get_toutiao_video_url(url):
        try:
            video_id = re.compile("videoid=(.*)").findall(url)[0]
            r = str(random.random())[2:]
            url_part = "/video/urls/v/l/toutiao/mp4/{}?r={}".format(video_id, r)
            s = crc32(url_part.encode())
            url_t = "https://ib.365yg.com{}&s={}".format(url_part, s)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTHL, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
            }
            res = requests.get(url_t, headers = headers).text
            res = json.loads(res)
            res = res["data"]["video_list"]["video_1"]["main_url"]
            video_url = base64.b64decode(res).decode()
            return video_url
        except Exception as e:
            return e
