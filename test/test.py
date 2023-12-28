#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  test.py
:time  2023/8/10 15:46
:desc  
"""
# 数字转换
num_map = {
    "0": "零",
    "1": "壹",
    "2": "贰",
    "3": "叁",
    "4": "肆",
    "5": "伍",
    "6": "陆",
    "7": "柒",
    "8": "捌",
    "9": "玖",
}
length_map = {
    "1": "元",
    "2": "拾",
    "3": "佰",
    "4": "仟",
    "5": "万",
    "6": "拾万",
    "7": "佰万",
    "8": "仟万",
    "9": "亿",
    "10": "拾亿",
    "11": "佰亿",
    "12": "仟亿",
}
a = dict()
for key,value in length_map.items():
    a[value] = ""
print(a)

# def translate_number(num, result:str):
#     if not isinstance(num, list):
#         num = list(str(num))
#     num_length = len(num)
#     num_head = num[0]
#     if num_head == "0":
#         if result[-1] != "零":
#             result += "零"
#     else:
#         result += (num_map[num_head] + length_map[str(num_length)])
#     num.remove(num_head)
#     if num:
#         result = translate_number(num, result)
#     if result.endswith("零"):
#         result = result.rstrip("零") + "元整"
#     return result


def translate_num(num:str, result):
    if not isinstance(num, list):
        num = list(str(num))
    num_length = len(num)
    num_head = num[0]
    result[length_map[str(num_length)]] = num_map[num_head]
    if num_head == "0":
        result[length_map[str(num_length)]] = "/"
    num.remove(num_head)
    if num:
        result = translate_num(num, result)
    return result


a = "12345哈哈"
print(a.isdigit())
