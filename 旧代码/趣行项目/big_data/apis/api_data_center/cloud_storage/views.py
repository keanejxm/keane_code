# -*- coding:utf-8 -*-
"""
云资源接口。
1、上传BOS。
2、解析html，并将img、video、audio标签里的内容上传至BOS。
# author: Trico
# date: 2020/8/24
# update: 2020/8/24
"""

from django.http import JsonResponse
import traceback

from cloud_storage.lib.parse_html import ParseHtmlBos
from cloud_storage.lib.bos_operate import BaiduBosOperate
from api_common_utils.llog import LLog
from api.config import api_log_path

# 全局日志对象，同一名称的logger只能生成一次，否则多线程操作时会出现不记录日志的问题。
g_logger = LLog(logger_name="cloud_storage", log_path=api_log_path, logger_level="DEBUG").logger


def bos_exists(request):
    """
    检查文件是否已存在，会检查文件长度。
    :return:
    """

    try:
        return JsonResponse(BaiduBosOperate(g_logger).api_exists(request))
    except Exception as e:
        g_logger.warning(f"{e}\n{traceback.format_exc()}")
        return JsonResponse(dict(code=0, msg=str(e), exists=None))


def bos_check_key_exists(request):
    """
    检查文件是否已存在。
    :return:
    """

    try:
        return JsonResponse(BaiduBosOperate(g_logger).api_check_key_exists(request))
    except Exception as e:
        g_logger.warning(f"{e}\n{traceback.format_exc()}")
        return JsonResponse(dict(code=0, msg=str(e), exists=None))


def bos_upload(request):
    """
    上传文件至BOS。
    :return:
    """

    try:
        return JsonResponse(BaiduBosOperate(g_logger).api_upload(request))
    except Exception as e:
        g_logger.warning(f"{e}\n{traceback.format_exc()}")
        return JsonResponse(dict(code=0, msg=str(e), exists=None))


def bos_upload_by_url(request):
    """
    下载文件并上传至BOS，如果已经存在于BOS则跳过。
    :return:
    """

    try:
        return JsonResponse(BaiduBosOperate(g_logger).api_upload_by_url(request))
    except Exception as e:
        g_logger.warning(f"{e}\n{traceback.format_exc()}")
        return JsonResponse(dict(code=0, msg=str(e), exists=None))


def bos_upload_image_by_url_and_compute_hash(request):
    """
    下载文件，计算出哈希值，之后上传至BOS，如果已经存在于BOS则直接返回bos链接。
    :return:
    """

    try:
        return JsonResponse(BaiduBosOperate(g_logger).api_bos_upload_image_by_url_and_compute_hash(request))
    except Exception as e:
        g_logger.warning(f"{e}\n{traceback.format_exc()}")
        return JsonResponse(dict(code=0, msg=str(e), exists=None))


def bos_parse_html(request):
    """
    解析html文本，并将图片、视频、音频等资源上传至云存储。
    返回带新链接的html文本。
    :return:
    """

    try:
        return JsonResponse(ParseHtmlBos(g_logger).api_parse_html(request))
    except Exception as e:
        g_logger.warning(f"{e}\n{traceback.format_exc()}")
        return JsonResponse(dict(code=0, msg=str(e), exists=None))
