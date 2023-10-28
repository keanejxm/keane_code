#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
工具。
# author: Trico
# date: 2020.4.15
# update: 2020.4.15
"""

import re
import requests
from urllib.parse import urlparse


# 文件名正则。
g_file_name_pattern = re.compile(r"\w", flags=re.S)


# 后缀类型。
g_suffixes = {
    # 图片。
    "tif", "tiff", "fax", "gif", "ico", "jfif", "jpe", "jpeg", "jpg", "png",
    "bmp", "wbmp", "rp",
    # 视频。
    "ogg", "asf", "asx", "avi", "ivf", "m1v", "m2v", "m4e", "movie", "mp2v",
    "mp4", "mpa", "mpe", "mpeg", "mpg", "mps", "mpv", "mpv2", "rv", "wm",
    "wmv", "wmx", "wvx",
    # 音频。
    "acp", "aif", "aifc", "aiff", "au", "la1", "lavs", "lmsff", "m3u", "mid",
    "midi", "mnd", "mns", "mp1", "mp2", "mp3", "mpga", "pls", "ra", "ram",
    "rmi", "rmm", "rpm", "snd", "wav", "wax", "wma", "xpl",
}
# 响应头content-type与文件后缀映射，参考https://www.w3cschool.cn/http/ahkmgfmz.html。
g_content_types_map = {
    # 图片。
    "image/tiff": "tif",
    "image/fax": "fax",
    "image/gif": "gif",
    "image/x-icon": "ico",
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/png": "png",
    "image/pnetvue": "net",
    "image/vnd.rn-realpix": "rp",
    "image/vnd.wap.wbmp": "wbmp",

    # 视频。
    "video/mp4": "mp4",
    "video/x-ms-asf": "asf",
    "video/avi": "avi",
    "video/x-ivf": "ivf",
    "video/x-sgi-movie": "movie",
    "video/mpeg4": "mp4",
    "video/x-mpg": "mpa",
    "video/x-mpeg": "mpe",
    "video/mpg": "mpg",
    "video/mpeg": "mpv2",
    "video/vnd.rn-realvideo": "rv",
    "video/x-ms-wm": "wm",
    "video/x-ms-wmv": "wmv",
    "video/x-ms-wmx": "wmx",
    "video/x-ms-wvx": "wvx",

    # 音频。
    "audio/x-mei-aac": "acp",
    "audio/aiff": "aif",
    "audio/basic": "au",
    "audio/x-liquid-file": "la1",
    "audio/x-liquid-secure": "lavs",
    "audio/x-la-lms": "lmsff",
    "audio/mpegurl": "m3u",
    "audio/mid": "mid",
    "audio/x-musicnet-download": "mnd",
    "audio/x-musicnet-stream": "mns",
    "audio/mp1": "mp1",
    "audio/mp2": "mp2",
    "audio/mp3": "mp3",
    "audio/rn-mpeg": "mpga",
    "audio/scpls": "pls",
    "audio/vnd.rn-realaudio": "ra",
    "audio/x-pn-realaudio": "ram",
    "audio/x-pn-realaudio-plugin": "rpm",
    "audio/wav": "wav",
    "audio/x-ms-wax": "wax",
    "audio/x-ms-wma": "wma",

    # 数据流。
    "application/octet-stream": "",
}


def get_file_name_from_url(url):
    """
    按百度云BOS等URL的识别方式，从URL中提取文件名和文件后缀。
    :return:
    """

    # 文件名和文件后缀。
    file_name = url.split("?")[0].split("/")[-1]
    match_file_name = re.match(g_file_name_pattern, file_name)
    if not match_file_name:
        raise ValueError("File name not recognized, {}.".format(url))
    if "." in file_name:
        file_suffix = file_name.split(".")[-1]
        match_file_name = re.match(g_file_name_pattern, file_suffix)
        if not match_file_name:
            raise ValueError("File name not recognized, {}.".format(url))
    else:
        file_suffix = ""

    return file_name, file_suffix


def fetch_file(url):
    """
    获取文件内容和文件类型。
    :return:
    """

    # 参数验证。
    assert url and isinstance(url, str), "Error param, url."

    # 请求文件内容。
    request_headers = {
        "Host": str(urlparse(url).netloc).split(":")[0],
        "Accept": "*/*",
        "Connection": "Keep-Alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                      "like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    }
    response = requests.get(url, headers=request_headers, timeout=10)
    if response.status_code == requests.codes.ok:
        response_headers = response.headers
        content = response.content
    else:
        raise ValueError("Failed to fetch file, {}, {}.".format(response.status_code, url))

    # 分析响应头，获取内容类型。
    content_type = None
    if "Content-Type" in response_headers and response_headers["Content-Type"]:
        content_type = response_headers.get("Content-Type")
        # 检查响应头的内容格式是否认识。
        if not content_type:
            raise ValueError("Empty content type.")

    return content, content_type


def fetch_file_info(url):
    """
    获取文件信息。
    :return:
    """

    file_name, file_suffix = get_file_name_from_url(url)
    file_content, content_type = fetch_file(url)
    return file_name, file_suffix, file_content, content_type


if __name__ == "__main__":
    fetch_file_info("https://bj.bcebos.com/v1/python-spider/zycf_gk/img/mainapp/38d5458025f77b13bb0034ed5425729f")
