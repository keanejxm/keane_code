#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  下载中国日历.py
:time  2024/5/24 15:05
:desc
"""
import json

import requests

calendar_data = dict()
for i in range(12):
    url = "https://opendata.baidu.com/data/inner"
    data = {
        "tn": "reserved_all_res_tn",
        "type": "json",
        "resource_id": "52109",
        "query": f"2025年{i+1}月",
        "apiType": "yearMonthData",
        "cb": "jsonp_1716539518418_58850",
    }
    res = requests.get(url, params=data)
    res_text = res.text.lstrip("jsonp_1716539518418_58850(")
    res_text = res_text.rstrip(")")
    res_json = json.loads(res_text)
    almanacs = res_json["Result"][0]["DisplayData"]["resultData"]["tplData"]["data"]["almanac"]

    for almanac in almanacs:
        year = almanac["year"]
        month = almanac["month"]
        day = almanac["day"]
        # 节假日
        if 'festivalList' in almanac:
            festival_list = almanac["festivalList"]
        else:
            festival_list = ""
        if "status" in almanac:
            status = almanac["status"]
        else:
            status = ""
        week = almanac["cnDay"]
        if status == "1":
            is_work = "休息日"
        elif status == "2":
            is_work = "工作日"
        elif status == "" and week in ["六", "日"]:
            is_work = "休息日"
        else:
            is_work = "工作日"
        if year in calendar_data:
            cal_year = calendar_data[year]
            if month not in cal_year:
                calendar_data[year][month] = dict()
                calendar_data[year][month][day] = dict(year=year, month=month, day=day, festival=festival_list,
                                                       status=status, isWork=is_work, week=week)
            else:
                cal_month = calendar_data[year][month]
                if day not in cal_month:
                    calendar_data[year][month][day] = dict(year=year, month=month, day=day, festival=festival_list,
                                                           status=status, isWork=is_work, week=week)
                else:
                    continue
        else:
            calendar_data[year] = dict()
            calendar_data[year][month] = dict()
            calendar_data[year][month][day] = dict(year=year, month=month, day=day, festival=festival_list, status=status,
                                                   isWork=is_work, week=week)

with open("中国日历.json","w",encoding="utf8") as w:
    w.write(json.dumps(calendar_data,ensure_ascii=False))

