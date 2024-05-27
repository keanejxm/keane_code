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
    pattern = r'(\d{4})[-\/](\d{1,2})[-\/](\d{1,2})'
    match = re.search(pattern, text)
    if match:
        year, month, day = match.groups()
        return {'year': year, 'month': month, 'day': day}
    else:
        return None

a = "2024-5-4 12:00:00"
print(extract_date(a))