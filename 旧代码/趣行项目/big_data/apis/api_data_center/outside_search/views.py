from django.shortcuts import render

# Create your views here

import json
import traceback
from django.http.response import JsonResponse

from api.config import api_log_path
from api_common_utils.llog import LLog
from outside_search.outside_search.xinlang_search import XinLangSearch
from outside_search.outside_search.baidu_search import BaiDuSearch
from outside_search.outside_search.sanliu0_search import SanLiuOSearch
from outside_search.outside_search.china_search import ChinaSearch
from outside_search.outside_search.sougou_search import SouGouSearch
from outside_search.outside_search.bing_search import BingSearch


LOGGER = LLog(logger_name="outside_templates", log_path=api_log_path, logger_level="DEBUG").logger


def china_search_(request):
    """
    中国搜索
    :param request:
    :return:
    """
    try:
        queryword = json.loads(request.body)["keyword"]
        obj = ChinaSearch(LOGGER, queryword)
        res = obj.chinasearch()
        return JsonResponse(dict(code=1, msg="success", data=res))
    except Exception as e:
        LOGGER.warning("{}\n{}".format(e, traceback.format_exc()))
        return JsonResponse(dict(code=0, msg="failed"))


def xinlang_search_(request):
    """
    新浪搜索
    :param request:
    :return:
    """
    try:
        queryword = json.loads(request.body)["keyword"]
        obj = XinLangSearch(LOGGER, queryword)
        res = obj.xinlangsearch()
        return JsonResponse(dict(code=1, msg="success", data=res))
    except Exception as e:
        LOGGER.warning("{}\n{}".format(e, traceback.format_exc()))
        return JsonResponse(dict(code=0, msg="failed"))


def sougou_search_(request):
    """
    搜狗搜索
    :param request:
    :return:
    """
    try:
        queryword = json.loads(request.body)["keyword"]
        obj = SouGouSearch(LOGGER, queryword)
        res = obj.sougousearch()
        return JsonResponse(dict(code=1, msg="success", data=res))
    except Exception as e:
        LOGGER.warning("{}\n{}".format(e, traceback.format_exc()))
        return JsonResponse(dict(code=0, msg="failed"))


def bing_search_(request):
    """
    Bing搜索
    :param request:
    :return:
    """
    try:
        queryword = json.loads(request.body)["keyword"]
        obj = BingSearch(LOGGER, queryword)
        res = obj.bingsearch()
        return JsonResponse(dict(code=1, msg="success", data=res))
    except Exception as e:
        LOGGER.warning("{}\n{}".format(e, traceback.format_exc()))
        return JsonResponse(dict(code=0, msg="failed"))


def baidu_search_(request):
    """
    百度搜索
    :param request:
    :return:
    """
    try:
        queryword = json.loads(request.body)["keyword"]
        obj = BaiDuSearch(LOGGER, queryword)
        res = obj.baidusearch()
        return JsonResponse(dict(code=1, msg="success", data=res))
    except Exception as e:
        LOGGER.warning("{}\n{}".format(e, traceback.format_exc()))
        return JsonResponse(dict(code=0, msg="failed"))


def san60_search_(request):
    """
    360搜索
    :param request:
    :return:
    """
    try:
        queryword = json.loads(request.body)["keyword"]
        obj = SanLiuOSearch(LOGGER, queryword)
        res = obj.search360()
        return JsonResponse(dict(code=1, msg="success", data=res))
    except Exception as e:
        LOGGER.warning("{}\n{}".format(e, traceback.format_exc()))
        return JsonResponse(dict(code=0, msg="failed"))