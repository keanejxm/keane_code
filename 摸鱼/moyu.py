#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  moyu.py
:time  2023/6/20 8:51
:desc  
"""

import requests
from lxml import etree

url = "https://m.aishangba.info/122_122597/667005.html"
while 1:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }

    res = requests.get(url, headers=headers)
    if res.status_code == requests.codes.ok:
        res_html = etree.HTML(res.text)
        title = res_html.xpath("//span[@class = 'title']/text()")
        next_url = res_html.xpath("//a[@id = 'pt_next']/@href")
        url = f"https://m.aishangba.info{next_url[0]}"
        print(title,url)
    print(res)
