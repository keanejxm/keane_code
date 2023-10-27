# -*- coding:utf-8 -*-
"""
Cookie操作。
# author: Trico
# date: 2020/9/11
# update: 2020/9/11
"""


def cookie_str_to_dict(cookie_str):
    """
    cookie字符串转字典。
    :return:
    """

    cookies = dict()
    for cookie in cookie_str.split(";"):
        pos = cookie.index("=")
        key = str(cookie[0:pos]).strip()
        value = str(cookie[pos + 1:]).strip()
        cookies[key] = value
    return cookies


def cookie_dict_to_list(cookie_dict):
    """
    cookie字典转为列表。
    :return:
    """

    cookies = list()
    for key, value in cookie_dict.items():
        cookies.append(dict(name=key, value=value))
    return cookies


def cookie_str_to_list(cookie_str):
    """
    cookie字符串转列表。
    :return:
    """

    return cookie_dict_to_list(cookie_str_to_dict(cookie_str))
