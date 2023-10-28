#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
功能描述。
# author: Keane
# create date: 2020/11/9
# update date: 2020/11/9
"""

import json
import requests


def get_wb_cookie():
    """
    获取微博Cookie，采集用。
    :return:
    """

    resp = requests.get("http://192.168.16.7:16100/crawler_resources/get_random_wb_cookie", timeout=10)
    resp_data = json.loads(resp.content)
    return resp_data["data"]["wbCookie"]
