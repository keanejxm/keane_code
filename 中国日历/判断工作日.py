#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  判断工作日.py
:time  2024/5/27 10:10
:desc  
"""
import json
import time


def fetch_last_workday():
    """查询上一个工作日日期"""
    with open("中国日历.json", "r", encoding="utf8") as r:
        calendar_data = json.load(r)
        # today_timestamp = time.time()
        today_timestamp = time.mktime(time.strptime("2024-05-05","%Y-%m-%d"))
        while 1:
            year = time.strftime("%Y", time.localtime(today_timestamp))
            month = time.strftime("%m", time.localtime(today_timestamp)).lstrip("0")
            day = time.strftime("%d", time.localtime(today_timestamp)).lstrip("0")
            today_info = calendar_data[year][month][day]
            is_work = today_info["isWork"]
            if is_work == "工作日":
                return f"{year}-{month}-{day}"
            else:
                today_timestamp -= 24 * 60 * 60


# a = fetch_last_workday()
# print(a)
