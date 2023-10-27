# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
import traceback
from django.http.response import JsonResponse
from batch_compute.libs.works_analyze import BigDataWorksAnalyze
from batch_compute.libs.spread_effect import WorksSpreadEffect
from batch_compute.libs.distance_spread_effect import DistanceWorksSpreadEffect
from api.config import api_log_path
from api_common_utils.llog import LLog

logger = LLog("batch_compute", log_path=api_log_path, logger_level="DEBUG").logger
# logger = LLog("test", only_console=True).logger


def get_query_works_list(request):
    try:
        obj = BigDataWorksAnalyze(logger)
        return JsonResponse(obj.api_query_get_works_list(request))
    except Exception as e:
        logger.warning(f"根据query查询相似文章结果集报错：{e}.\n{traceback.format_exc()}")


def judge_work_original(request):
    try:
        obj = BigDataWorksAnalyze(logger)
        return JsonResponse(obj.api_judge_work_original(request))
    except Exception as e:
        logger.warning(f"判断文章原创与否报错：{e}.\n{traceback.format_exc()}")


def get_query_works_similar(request):
    try:
        obj = WorksSpreadEffect(logger)
        return JsonResponse(obj.api_search_es_by_query(request))
    except Exception as e:
        logger.warning(f"获取相似文章原创与否报错：{e}.\n{traceback.format_exc()}")


def get_simhash_works_similar(request):
    try:
        obj = WorksSpreadEffect(logger)
        return JsonResponse(obj.api_search_es_by_simhash(request))
    except Exception as e:
        logger.warning(f"获取相似文章原创与否报错：{e}.\n{traceback.format_exc()}")


def get_query_simhash_works_similar(request):
    try:
        obj = WorksSpreadEffect(logger)
        return JsonResponse(obj.api_search_es_by_query_and_simhash(request))
    except Exception as e:
        logger.warning(f"获取相似文章原创与否报错：{e}.\n{traceback.format_exc()}")


def get_distance_works_similar(request):
    try:
        obj = DistanceWorksSpreadEffect(logger)
        return JsonResponse(obj.api_search_es_by_distance(request))
    except Exception as e:
        logger.warning(f"获取相似文章原创与否报错：{e}.\n{traceback.format_exc()}")

