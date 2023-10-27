#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
工具。
# author: Trico
# date: 2020.4.15
# update: 2020.4.15
"""

import ctypes
import hashlib
import datetime


# 编码集。
common_charset = ("utf-8", "utf8", "gb2312", "gbk", "gb18030", "big5")


def md5(unicode_str, charset="UTF-8"):
    """
    字符串转md5格式。
    :return:
    """

    _md5 = hashlib.md5()
    _md5.update(unicode_str.encode(charset))
    return _md5.hexdigest()


def thread_print(input_string, *args, **kwargs):
    """
    带信息打印。
    :return:
    """

    thread_id = ctypes.CDLL('libc.so.6').syscall(186)
    print(f"{datetime.datetime.now()} [{thread_id}] {input_string}", flush=True, *args, **kwargs)
