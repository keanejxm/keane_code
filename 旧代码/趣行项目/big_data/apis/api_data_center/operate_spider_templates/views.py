#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
电子报
# author: Trico
# date: 2020.6.1
# update: 2020.6.1
"""
import json
import traceback
from django.http.response import JsonResponse

from api.config import api_log_path
from api_common_utils.llog import LLog
from operate_spider_templates.lib.templates.epaper.epaper_templates import EPaperTemplate


LOGGER = LLog(logger_name="operate_spider_templates", log_path=api_log_path, logger_level="DEBUG").logger


def epaper_template_create(request):
    # 新增电子报采集模板。
    try:
        obj = EPaperTemplate(LOGGER)
        res = obj.create(json.loads(request.body))
        return JsonResponse(dict(code=0, msg="success", data=res))
    except Exception as e:
        LOGGER.warning("{}\n{}".format(e, traceback.format_exc()))
        return JsonResponse(dict(code=0, msg="failed"))


def epaper_template_delete(request):
    # 删除电子报采集模板。
    try:
        obj = EPaperTemplate(LOGGER)
        res = obj.delete(json.loads(request.body))
        return JsonResponse(dict(code=0, msg="success", data=res))
    except Exception as e:
        LOGGER.warning("{}\n{}".format(e, traceback.format_exc()))
        return JsonResponse(dict(code=0, msg="failed"))


def epaper_template_update(request):
    # 更新电子报采集模板。
    try:
        obj = EPaperTemplate(LOGGER)
        res = obj.update(json.loads(request.body))
        return JsonResponse(dict(code=0, msg="success", data=res))
    except Exception as e:
        LOGGER.warning("{}\n{}".format(e, traceback.format_exc()))
        return JsonResponse(dict(code=0, msg="failed"))