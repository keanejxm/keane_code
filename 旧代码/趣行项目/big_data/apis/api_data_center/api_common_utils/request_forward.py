# -*- coding:utf-8 -*-
"""
请求转发。
一般用于运行时间较长的接口，如发文。
只为快速地为请求者返回状态。
# author: Trico
# date: 2020/11/24
# update: 2020/11/24
"""

import logging
import requests
import traceback

from api.config import api_host
from api_common_utils.utils import log_request_info


def __request_forward(logger, request, method, api_url):
    """
    请求转发。
    :param logger: 日志对象。
    :param request: django请求对象。
    :param method: 请求方法，post或get。
    :param api_url: 请求地址。
    :return:
    """

    try:
        # 参数验证。
        assert method in ("get", "post"), f"参数错误，method：{method}"
        assert isinstance(logger, logging.Logger), f"参数错误，logger"
        assert api_url and isinstance(api_url, str), f"参数错误，api_url: {api_url}"

        # 记录请求体。
        log_request_info(logger, request)
        # 以及短的超时时间请求传播效果分析接口，将成功状态返回前端。
        requests.request(method=method, url=api_url, data=request.body, timeout=0.1)
        return dict(code=1, msg=f"成功")
    except requests.exceptions.ReadTimeout:
        # 强制返回成功，告知前端传播效果分析任务已下发执行。
        return dict(code=1, msg=f"成功")
    except Exception as e:
        logger.warning(f"{e}\n{traceback.format_exc()}")
        # 强制返回成功，告知前端传播效果分析任务已下发执行。
        return dict(code=0, msg=f"{e}")


def request_forward(logger, request, method, whole_path):
    """
    请求转发。
    :param logger: 日志对象。
    :param request: django请求对象。
    :param method: 请求方法，post或get。
    :param whole_path: 请求地址。
    :return:
    """

    # 参数验证。
    assert whole_path and isinstance(whole_path, str), f"参数错误，whole_path: {whole_path}"

    # 以及短的超时时间请求传播效果分析接口，将成功状态返回前端。
    whole_path.lstrip("/")
    api_url = f"{api_host}/{whole_path}"
    return __request_forward(logger=logger, request=request, method=method, api_url=api_url)
