#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  正则匹配.py
:time  2024/10/17 11:09
:desc  
"""
import re

# 匹配中文
a = "这个一条匹配中文的数据aaaaa"
print(re.findall(r"[\u4e00-\u9fa5]", a))
# 匹配日文
print(re.findall(r"[\u0800-\u4e00]", a))
# 匹配韩文
print(re.findall(r"[\uac00-\ud7ff]", a))
