#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  重试.py
:time  2025/2/7 14:07
:desc  
"""


def function_fun(name):
    print(name)


def reset_fun():
    reset_num = 0
    while 1:
        try:
            function_fun(f"xiaoming{reset_num}")
        except Exception as e:
            reset_num += 1
            print(f"报错{e},第{reset_num}次重新执行函数")
            if reset_num == 10:
                print(f"重新尝试{reset_num}次函数，即将终止重试")
                break
reset_fun()