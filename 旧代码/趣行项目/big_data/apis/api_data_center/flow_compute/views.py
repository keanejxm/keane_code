# -*- coding:utf-8 -*-
"""
云资源接口。
1、上传BOS。
2、解析html，并将img、video、audio标签里的内容上传至BOS。
# author: Trico
# date: 2021/1/26
# update: 2021/1/26
"""

import json
import traceback
from django.http import JsonResponse

from api_common_utils.llog import LLog
from api.config import api_log_path
from api_common_utils.utils import log_request_info

from flow_compute.lib.baidu_api.nlp import Nlp

# 日志对象。
LOGGER = LLog(logger_name="flow_compute", log_path=api_log_path, logger_level="INFO").logger


def flow_compute_options(request):
    """可选择的执行流计算"""

    try:
        # 记录请求体。
        log_request_info(LOGGER, request)

        # 解析请求体。
        body = json.loads(request.body)

        # 执行。
        resp = Nlp(logger=LOGGER).run(spider_data=body)

        return JsonResponse(resp)
    except Exception as e:
        LOGGER.error(f"{e}\n{traceback.format_exc()}")
        return JsonResponse(dict(code=0, msg=str(e)))
