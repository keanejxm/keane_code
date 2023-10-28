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
import requests
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


def md5_bytes(input_bytes):
    """
    字符串转md5格式。
    :return:
    """

    _md5 = hashlib.md5()
    _md5.update(input_bytes)
    return _md5.hexdigest()


def thread_print(input_string, *args, **kwargs):
    """
    带信息打印。
    :return:
    """

    thread_id = ctypes.CDLL('libc.so.6').syscall(186)
    print(f"{datetime.datetime.now()} [{thread_id}] {input_string}", flush=True, *args, **kwargs)


def hash_sha1(input_str, charset="UTF-8"):
    """
    sha1加密。
    :return:
    """

    _sha = hashlib.sha1()
    if isinstance(input_str, str):
        _sha.update(input_str.encode(charset))
    elif isinstance(input_str, bytes):
        _sha.update(input_str)
    else:
        raise ValueError("Unknown type while compute sha1, '{}'.".format(type(input_str)))
    return _sha.hexdigest()


def get_charset(response):
    """
    获取response编码。
    :return:
    """

    if not response or not isinstance(response, requests.Response):
        raise ValueError("The 'response' is not a type of 'requests.Response'.")

    current_encoding = response.encoding
    if not current_encoding or current_encoding.lower() not in common_charset:
        header_encoding = requests.utils.get_encoding_from_headers(response.headers)
        content_encoding_list = list()
        # noinspection PyBroadException
        try:
            # requests.utils.get_encodings_from_content()方法可能会被移除。
            content_encoding_list = requests.utils.get_encodings_from_content(response.text)
        except Exception:
            pass
        if header_encoding and header_encoding.lower() in common_charset:
            return header_encoding
        elif content_encoding_list:
            for content_encoding in content_encoding_list:
                if content_encoding.lower() in common_charset:
                    return content_encoding
    else:
        return current_encoding

    return response.apparent_encoding
