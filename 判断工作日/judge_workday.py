#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  judge_workday.py
:time  2023/4/12 11:46
:desc  
"""
import time
from chinese_calendar import is_in_lieu, is_workday, is_holiday
import datetime


def _judge_workday(now, num=1):
    """
    判断是否是工作日
    :return:
    """
    year = time.strftime("%Y", time.localtime(now - 24 * num * 60 * 60))
    month = time.strftime("%m", time.localtime(now - 24 * num * 60 * 60))
    day = time.strftime("%d", time.localtime(now - 24 * num * 60 * 60))
    print(year, month, day)
    date = datetime.datetime(int(year), int(month), int(day))
    if not is_workday(date) or is_holiday(date) or is_in_lieu(date):
        print('休息日，节假日，调休日')
        num += 1
        year, month, day = _judge_workday(now, num)
        return year, month, day
    else:
        print('工作日')
        return year, month, day
