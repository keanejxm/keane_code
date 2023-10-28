#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
将微博的rid转换为mid。
# author: Trico
# date: 2020.4.27
# update: 2020.5.15
"""

import re
import math


def convert_str62_to_int10(input_str):
    """
    62进制字符串转为10进制整数。
    :return:
    """

    # 参数验证。
    assert input_str and isinstance(input_str, str), f"Error param, input_str {input_str}."

    # 基础参数。
    data62_known_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    scale = len(data62_known_chars)

    num = 0
    for i in range(len(input_str)):
        position_str = str(input_str[i])
        position = data62_known_chars.index(position_str)
        power = int(math.pow(scale, len(input_str) - i - 1))
        num += position * power

    return int(num)


def convert_int10_to_str62(input_int):
    """
    62进制字符串转为10进制整数。
    :return:
    """

    # 参数验证。
    assert input_int and isinstance(input_int, int), f"Error param, input_int {input_int}."

    data62_known_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if input_int == 0:
        return data62_known_chars[0]
    arr = []
    base = len(data62_known_chars)
    while input_int:
        rem = input_int % base
        input_int = input_int // base
        arr.append(data62_known_chars[rem])
    arr.reverse()

    return ''.join(arr)


def convert_wb_mid_to_rid(mid):
    """
    将微博mid转为详情链接中的rid。
    :return:
    """

    # 参数验证。
    assert isinstance(mid, str), f"Error param, mid: {mid}."

    mid = str(mid)[::-1]
    size = int(len(mid) / 7 if len(mid) % 7 == 0 else len(mid) / 7 + 1)
    result = []
    for i in range(size):
        s = mid[i * 7: (i + 1) * 7][::-1]
        s = convert_int10_to_str62(int(s))
        s_len = len(s)
        if i < size - 1 and len(s) < 4:
            s = '0' * (4 - s_len) + s
        result.append(s)
    result.reverse()
    return ''.join(result)


def convert_wb_rid_to_mid(rid):
    """
    根据微博URL中的rid经过62进制转换为mid。
    :return:
    """

    rid = str(rid)[::-1]
    size = len(rid) / 4 if len(rid) % 4 == 0 else len(rid) / 4 + 1
    result = []
    for i in range(int(size)):
        s = rid[i * 4: (i + 1) * 4][::-1]
        s = str(convert_str62_to_int10(str(s)))
        s_len = len(s)
        if i < size - 1 and s_len < 7:
            s = (7 - s_len) * "0" + s
        result.append(s)
    result.reverse()
    return str(int("".join(result)))


def convert_wb_rid_to_mid_from_url(url):
    """
    从URL中提取rid，并转换为mid。
    :param url:  例如：https://weibo.com/3222735304/IFgTnhGFo。
    :return:
    """

    # 参数验证。
    assert url and isinstance(url, str), "Error param, url."

    wb_rid_matchs = re.findall(r"^https?://\w*?\.?weibo\.com/[0-9a-zA-Z]+/([0-9a-zA-Z]+)$", url, flags=re.I)
    if wb_rid_matchs:
        wb_rid = wb_rid_matchs[0]
        wb_mid = convert_wb_rid_to_mid(wb_rid)
    else:
        raise ValueError("Failed to get rid from {}.".format(url))

    return wb_mid


if __name__ == "__main__":
    print(convert_wb_rid_to_mid_from_url("https://weibo.com/2966211953/J88ly05Bq"))
    print(convert_wb_rid_to_mid("J88ly05Bq"))
    print(convert_wb_mid_to_rid("4519387120021540"))
