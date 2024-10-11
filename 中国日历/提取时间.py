#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  提取时间.py
:time  2024/5/27 16:19
:desc  
"""
import re


def extract_date(text):
    # 正则表达式匹配多种日期格式
    pattern1 = r'(\d{4})[-\/](\d{1,2})[-\/](\d{1,2})'
    # pattern2 = r'(\d{4})[-\/](\d{1,2})'
    pattern2 = r'(\d{4})[-\/年](\d{1,2})月'
    patterns = {3:pattern1, 2:pattern2}
    for pat_key,pattern in patterns.items():
        match = re.search(pattern, text)
        if match and pat_key==3:
            year, month, day = match.groups()
            return {'year': year, 'month': month, 'day': day}
        elif match and pat_key==2:
            year,month = match.groups()
            return {'year': year, 'month': month}
    else:
        return None


# a = "2024-5-4 12:00:00"
a = "2024-05-04 8:00:00"
print(extract_date(a))
