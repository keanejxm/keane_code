#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  方法.py
:time  2023/11/9 14:12
:desc  
"""
a = "aaaaa"
try:
    print(float(a))
except ValueError as e:
    a = a