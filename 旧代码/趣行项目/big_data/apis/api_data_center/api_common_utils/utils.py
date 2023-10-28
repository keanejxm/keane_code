#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
工具。
# author: Trico
# date: 2020.4.15
# update: 2020.4.15
"""

import os
import sys
import json
import types
import ctypes
import hashlib
import requests
import datetime

from api_common_utils.sm3 import SM3


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


def hash_sm3(input_str, charset="UTF-8"):
    """
    sm3加密。
    :return:
    """

    _sm3 = SM3()
    if isinstance(input_str, str):
        _sm3.sm3_update(bytearray(input_str.encode(charset)))
    elif isinstance(input_str, bytes):
        _sm3.sm3_update(bytearray(input_str))
    else:
        raise ValueError("Unknown type while compute sm3, '{}'.".format(type(input_str)))
    return _sm3.sm3_final()


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


def get_proxy_session():
    """
    获取session对象。
    :return:
    """

    # 代理。
    proxy_meta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": "http-dyn.abuyun.com",
        "port": "9020",
        "user": "HR91J1A4881W7H1D",
        "pass": "6A8682072812B30F",
    }
    proxies = {
        "http": proxy_meta,
        "https": proxy_meta,
    }

    # HTTP会话。
    session = requests.Session()
    session.proxies = proxies

    return session


def overlook(obj, subscripts=None, func=None, func_params=None, default=None):
    """
    按一定规则取值，失败时取默认值。
    列表、字典等对象取逐个下标或按函数取值。
    当取值失败时，返回默认值。
    适用于提取非必须值的场合。
    :param obj: 数据源对象。
    :param subscripts: 下标数组。
    :param func: 函数对象。
    :param func_params: 函数参数。
    :param default: 默认值。
    :return: 结果值或默认值。
    """

    # 参数验证。
    if not obj:
        return default

    # 返回值。
    value = obj
    # noinspection PyBroadException
    try:
        # 按下标定位数据。
        if subscripts and isinstance(subscripts, (tuple, list, dict)):
            for subscript in subscripts:
                value = value[subscript]
        # 由函数对数据进行处理。
        if func and isinstance(func, (types.FunctionType,
                                      types.MethodType,
                                      types.BuiltinFunctionType,
                                      types.BuiltinMethodType)):
            if func_params and isinstance(func_params, dict):
                value = func(value, **func_params)
            else:
                value = func(value)
            return value
        else:
            # 没有函数的话直接
            return value
    except Exception as e:
        print("Failed to get value, '{}'.".format(e))
        return default


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


class ExpiredCookieError(Exception):
    # cookie失效异常。
    pass


def convert_video_src_of_article(src):
    """
    转换文章中的视频链接，不做特殊处理，只是清除掉多余的参数。
    应对【<video src="...?weibo-material-src=...&wangyi-material-src=..." ...>...</video>】的形式。
    :param src: 例如：【http://....mp4?weibo-material-src=...&wangyi-material-src=...】，处理成http://....mp4。
    :return:
    """

    # 处理视频链接。
    # 应对【<video src="...?
    # weibo-material-src=...&wangyi-material-src=..." ...>...</video>】的形式。
    if "?" in src:
        src_parts = src.split("?")
        if len(src_parts) > 1:
            src_main = src_parts[0]
            src_params_str = src_parts[1]
            src_params = src_params_str.split("&")
            new_src_params = list()
            for src_param in src_params:
                # 去掉无关的参数。
                if src_param.startswith("weibo-material-src"):
                    continue
                elif src_param.startswith("wangyi-material-src"):
                    continue
                else:
                    # 保留有用的参数。
                    new_src_params.append(src_param)
            src = f"{src_main}?{'&'.join(new_src_params)}"
        else:
            src = src_parts[0]
    return src


def log_request_info(logger, request):
    """
    记录请求体日志。
    :return:
    """

    # 记录请求体。
    client = request.META.get('HTTP_X_REAL_IP')
    # logger.debug(f"HTTP_X_REAL_IP: {client}")
    if not client:
        client = request.META.get('HTTP_X_FORWARDED_FOR')
        # logger.debug(f"HTTP_X_FORWARDED_FOR: {client}")
    if not client:
        client = request.META.get('REMOTE_ADDR')
        # logger.debug(f"REMOTE_ADDR: {client}")
    # noinspection PyBroadException
    try:
        body = json.loads(request.body)
    except Exception:
        body = "非json形式的post体"
    # logger.debug(f"客户端: {client}，"
    #             f"全路径: {request.get_full_path()}\n"
    #             f"POST体: {json.dumps(body, ensure_ascii=False)}。")
    logger.info(f"客户端: {client}，"
                f"全路径: {request.get_full_path()}")

    return body
