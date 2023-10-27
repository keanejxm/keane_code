#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
工具。
# author: Trico
# date: 2019.4.4
"""

import time


def elapse(logger=None):
    """
    计算逝去的时间。
    :param logger: 日志对象。
    :return: 函数对象。
    """

    def wrapper(func):
        def _wrapper(*args, **kwargs):
            t1 = time.time()
            result = func(*args, **kwargs)
            t2 = time.time()
            if logger:
                logger.info('[{0}] time used: {1} seconds.'.format(func.__name__, (t2 - t1)))
            else:
                print('[{0}] time used: {1} seconds.'.format(func.__name__, (t2 - t1)))
            return result
        return _wrapper
    return wrapper
