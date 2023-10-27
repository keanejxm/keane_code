#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
爬虫资源接口。
2020年11月20日，更新，阿布云代理加入经典模式。
# author: Trico
# date: 2020/8/9
# date: 2020/11/20
"""

import traceback
from django.http import JsonResponse
from api_common_utils.llog import LLog
from crawler_resources.lib.resources.crawler_resources import CrawlerResourcesAPI
from crawler_resources.lib.resources.hbrb_author_resources import HBRBAuthorResourcesAPI

# 工作目录。
from api.settings import BASE_DIR


# 全局日志对象，同一名称的logger只能生成一次，否则多线程操作时会出现不记录日志的问题。
api_log_path = f"{BASE_DIR}/logs"
g_logger = LLog(logger_name="crawler_resource", log_path=api_log_path, logger_level="DEBUG").logger


def get_random_wx_great_key(request):
    # 获取微信万能Key。
    try:
        result = CrawlerResourcesAPI(request, g_logger).get_random_wx_great_key()
        return JsonResponse(dict(code=1, msg="success", data=result))
    except Exception as e:
        g_logger.warning(f"{e}\n{traceback.format_exc()}")
        return JsonResponse(dict(code=0, msg=str(e)))


def get_random_wb_cookie(request):
    # 获取微博采集用cookie。
    try:
        result = CrawlerResourcesAPI(request, g_logger).get_random_wb_cookie()
        return JsonResponse(dict(code=1, msg="success", data=result))
    except Exception as e:
        g_logger.warning(f"{e}\n{traceback.format_exc()}")
        return JsonResponse(dict(code=0, msg=str(e)))


def get_abuyun_proxy(request):
    # 获取阿布云代理配置。
    try:
        result = CrawlerResourcesAPI(request, g_logger).get_abuyun_proxy()
        return JsonResponse(dict(code=1, msg="success", data=result))
    except Exception as e:
        g_logger.warning(f"{e}\n{traceback.format_exc()}")
        return JsonResponse(dict(code=0, msg=str(e)))


def get_hbrb_authors(request):
    # 获取河北日报作者列表。
    try:
        result = HBRBAuthorResourcesAPI(request, g_logger).get_hbrb_authors()
        return JsonResponse(dict(code=1, msg="success", data=result))
    except Exception as e:
        g_logger.warning(f"{e}\n{traceback.format_exc()}")
        return JsonResponse(dict(code=0, msg=str(e)))
