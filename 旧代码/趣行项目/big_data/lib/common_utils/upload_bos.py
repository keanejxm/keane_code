# -*- coding:utf-8 -*-
"""
上传数据至BOS。
# author: Trico
# date: 2020/8/25
# update: 2020/8/25
"""

import json
import requests

from lib_conf.config import bos_upload_image_by_url_and_compute_hash_api


def bos_upload_image_by_url_and_compute_hash(input_url, timeout=3600):
    """
    将图片上传至BOS，并且计算图片的哈希值。
    :param input_url: 资源链接。
    :param timeout: 超时时间，秒级。
    :return bos_url: BOS图片链接。
    :return img_hash: 图片哈希值。
    """

    # 参数验证。
    assert input_url and isinstance(input_url, str) and input_url.startswith("http"), \
        f"Error param, input_url: {input_url}."
    assert isinstance(timeout, (int, float)) and timeout > 0, f"Error param, timeout: {timeout}."

    # 发送URL至接口，接口负责下载文件并上传至BOS中。
    data = dict(url=input_url)
    resp = requests.post(bos_upload_image_by_url_and_compute_hash_api, json=data, timeout=timeout)
    if resp.status_code == requests.codes.ok:
        resp_data = json.loads(resp.content)
        if resp_data["code"] in (1, "1"):
            bos_url = resp_data["data"]["url"]
            img_hash = resp_data["data"]["imgHash"]
            assert bos_url and isinstance(bos_url, str) and bos_url.startswith("http"), \
                f"Error response param, url: {bos_url}."
            return bos_url, img_hash
        else:
            raise ValueError(f"Failed to upload {input_url}, {resp_data}.")
    else:
        raise ValueError(f"Error response: {resp.status_code}, {bos_upload_image_by_url_and_compute_hash_api}.")
