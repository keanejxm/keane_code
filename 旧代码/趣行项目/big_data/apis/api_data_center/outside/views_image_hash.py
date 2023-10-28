# -*- coding:utf-8 -*-
"""
计算图片哈希值。
# author: Trico
# date: 2021/1/28
# update: 2021/1/28
"""

import json
import requests
import traceback
from django.http import JsonResponse

from api_common_utils.llog import LLog
from api.config import api_log_path
from api_common_utils.utils import log_request_info
from api_common_utils.image.image_hash import image_hash

LOGGER = LLog(logger_name="image_hash", log_path=api_log_path, logger_level="INFO").logger


def api_image_hash_by_url(request):
    """
    接口，根据URL计算图片哈希值。
    :param request: 请求体。
    :return:
    """

    try:
        # 记录请求。
        log_request_info(LOGGER, request)
        # 解析请求体。
        body = json.loads(request.body)
        url = body.get("url")
        assert url and isinstance(url, str) and url.startswith("http"), f"参数错误，url：{url}"

        # 请求图片。
        resp = requests.get(url=url, timeout=30)
        if resp.status_code == requests.codes.ok:
            content = resp.content
        else:
            raise ValueError(f"图片下载失败，{resp.status_code}，{resp.reason}")

        # 计算图片哈希值。
        img_hash = image_hash(content)
        return JsonResponse(dict(code=1, msg="ok", data=dict(imgHash=img_hash)))
    except Exception as e:
        LOGGER.warning(f"{e}\n{traceback.format_exc()}")
        return JsonResponse(dict(code=0, msg=str(e), data=dict()))


def api_image_hash_by_content(request):
    """
    接口，根据图片内容计算图片哈希值。
    :param request: 请求体。
    :return:
    """

    try:
        # 记录请求。
        log_request_info(LOGGER, request)

        # 读取一个文件。
        content = b""
        for _file_key, _file_obj in request.FILES.items():
            if _file_key == "image":
                if _file_obj:
                    content = b""
                    for chunk in _file_obj.chunks():
                        content += chunk
                break
        else:
            raise ValueError("参数错误，文件对象的key不是image")

        # 保存本地测试。
        # with open("./test.jpg", "wb") as fw:
        #     fw.write(content)

        # 计算图片哈希值。
        img_hash = image_hash(content)
        return JsonResponse(dict(code=1, msg="ok", data=dict(imgHash=img_hash)))
    except Exception as e:
        LOGGER.warning(f"{e}\n{traceback.format_exc()}")
        return JsonResponse(dict(code=0, msg=str(e), data=dict()))
