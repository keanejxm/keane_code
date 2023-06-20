#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  moyu.py
:time  2023/6/20 8:51
:desc  
"""

import requests

url = "https://m.aishangba.info/122_122597/664056.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

res = requests.get(url,headers = headers)
print(res)