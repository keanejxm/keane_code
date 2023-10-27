# -*- coding:utf-8 -*-
"""
云易媒，文件上传BOS。
2021年1月4日，更新，设置新的BOS桶。
# author: Trico
# date: 2020.8.24
# update: 2021.1.4
"""

import io
import re
import json
import logging
import hashlib
import requests
import traceback
from urllib.parse import urlparse

# 导入百度云BOS相关模块。
from baidubce import utils
from baidubce.exception import BceError
from baidubce.services.bos.bos_client import BosClient
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration

from api_common_utils.llog import LLog
from api.config import api_log_path
from api_common_utils.utils import md5_bytes
from api_common_utils.image.image_hash import image_hash


class BaiduBosOperate(object):

    def __init__(self, logger, prefix="bdp/files"):
        """
        初始化。
        :param logger: 日志对象。
        :param prefix: 目录前缀。
        """

        # 日志对象。
        if logger and isinstance(logger, logging.Logger):
            self._logger = logger
        else:
            if api_log_path and isinstance(api_log_path, str):
                log_path = api_log_path
            else:
                log_path = "./logs"
            self._logger = LLog(
                logger_name=self.__class__.__name__,
                log_path=log_path,
                logger_level="INFO",
            ).logger

        # 参数验证。
        assert prefix and isinstance(prefix, str), "Param prefix error."

        # 获取百度BOS连接对象。
        self._endpoint = "https://bj.bcebos.com"
        self._bucket = "quxing-bigdata"
        self._key_prefix = prefix
        self._access_key_id = "0e4dc632116e473d8f314f7e0f9e18a3"
        self._secret_access_key = "147eb813946b40f2a4405476b9682b81"
        self._cloud_client = self.get_bos_client()

        # 下载文件的会话。
        self._download_session = requests.Session()
        self._download_timeout = 1

        # 后缀类型。
        self._suffix_map = {
            # 图片。
            "gif": "image/gif",
            "jpeg": "image/jpeg",
            "jpg": "image/jpeg",
            "png": "image/png",
            "bmp": "image/bmp",
            "webp": "image/webp",
            # 视频。
            "mp4": "video/mp4",
        }
        # 内容类型。
        self._content_type_map = {
            # 图片。
            "image/gif": "gif",
            "image/jpeg": "jpg",
            "image/png": "png",
            "image/bmp": "bmp",
            "image/webp": "webp",
            # 视频。
            "video/mp4": "mp4",
        }
        # 默认内容类型。
        self._default_content_type = "application/octet-stream"

        # 符合条件的链接被过滤。
        self._filter_pattern = re.compile(r"http[s]?://[\w]*?\.bcebos\.com", flags=re.I | re.S)

    def get_bos_client(self):
        """
        获取百度BOS连接对象。
        :return:
        """

        # 创建BceClientConfiguration。
        config = BceClientConfiguration(
            credentials=BceCredentials(self._access_key_id, self._secret_access_key),
            endpoint=self._endpoint
        )
        # 新建BosClient。
        bos_client = BosClient(config)

        return bos_client

    @staticmethod
    def md5_baidubce(obj, charset="UTF-8"):
        """
        BaiduBCE计算MD5的方法。
        :return:
        """

        _md5 = hashlib.md5()
        if isinstance(obj, str):
            fp = io.BytesIO(obj.encode(charset))
            _md5 = utils.get_md5_from_fp(fp)
        elif isinstance(obj, bytes):
            fp = io.BytesIO(obj)
            _md5 = utils.get_md5_from_fp(fp)
        else:
            raise ValueError("Not a str type or bytes type.")

        return _md5

    def convert_key_to_url(self, key):
        """
        将key组合成url。
        :param key:
        :return:
        """

        return "/".join([self._endpoint, self._bucket, key])

    def add_object_size_to_url(self, url, key):
        """
        获取对象文件大小。
        :return:
        """

        # noinspection PyBroadException
        try:
            key = "{}/{}".format(self._key_prefix, key)
            key = key.replace("//", "/")
            # 检查key是否存在。
            meta_data = self._cloud_client.get_object_meta_data(self._bucket, key)
            bos_content_length = int(meta_data.metadata.content_length)
            if "?" in url:
                url = f"{url}&data-size={bos_content_length}"
            else:
                url = f"{url}?data-size={bos_content_length}"
        except Exception as e:
            # 报错意味着不存在。
            self._logger.debug(f"BOS对象不存在，{e}，bucket：{self._bucket}，key：{key}")
        finally:
            return url

    def exists(self, file, file_meta):
        """
        检查文件是否已存在，会检查文件长度。
        :return:
        """

        # 参数验证。
        assert file and isinstance(file, str), "Param file error."
        assert file_meta and isinstance(file_meta, dict), "Param file_meta error."

        # 上传路径。
        key = "{}/{}".format(self._key_prefix, file)
        key = key.replace("//", "/")
        url = self.convert_key_to_url(key)

        # noinspection PyBroadException
        try:
            # 检查key是否存在。
            meta_data = self._cloud_client.get_object_meta_data(self._bucket, key)
        except BceError:
            # 报错意味着不存在。
            return False, url

        # 通过长度判断是否已存在。
        bos_content_length = int(meta_data.metadata.content_length)
        if int(file_meta["content_length"]) == bos_content_length:
            url = self.convert_key_to_url(key)
            self._logger.info("Existed, {}.".format(url))
            return True, url
        else:
            return False, url

    def check_key_exists(self, file):
        """
        判断文件是否已存在。
        :return:
        """

        # 参数验证。
        assert file and isinstance(file, str), "Param file error."

        # 上传路径。
        key = "{}/{}".format(self._key_prefix, file)
        key = key.replace("//", "/")
        url = self.convert_key_to_url(key)

        # noinspection PyBroadException
        try:
            # 检查key是否存在。
            self._cloud_client.get_object_meta_data(self._bucket, key)
        except BceError:
            return False, url

        # 返回数据。
        self._logger.info("Existed, {}.".format(url))
        return True, url

    def download_file(self, url, headers=None, proxies=None, suffix=None):
        """
        下载文件并上传至BOS，如果已经存在于BOS则跳过。
        :param url: 文件下载地址。
        :param headers: 请求头。
        :param proxies: 代理信息。
        :param suffix: 后缀。
        :return:
        """

        # 参数验证。
        assert url and isinstance(url, str) and url.startswith("http"), f"Error param, url: {url}."
        # 替换反斜杠。
        url = url.replace("\\", "/")

        # 请求头。
        if not headers or not isinstance(headers, dict):
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/74.0.3729.169 Safari/537.36",
                "Host": str(urlparse(url).netloc),
            }

        # 下载文件。
        resp = self._download_session.get(url, headers=headers, proxies=proxies, timeout=self._download_timeout)
        if resp.status_code == requests.codes.ok:
            # 文件内容。
            file_bytes = resp.content
            # 内容类型默认为None。
            content_type = None
            # 检查文件后缀。
            if suffix is None:
                suffix = ""
                # 分析URL后缀。
                temp_url = url
                if "?" in temp_url:
                    temp_url = temp_url.split("?")[0]
                if "." in temp_url:
                    url_suffix = temp_url.split(".")[-1]
                    if url_suffix and url_suffix.lower() in self._suffix_map:
                        suffix = url_suffix
                # 检查响应头里的文件后缀。
                elif "Content-Type" in resp.headers and resp.headers["Content-Type"]:
                    content_type = resp.headers.get("Content-Type")
                    # 检查响应头的内容格式是否认识。
                    if content_type in self._content_type_map:
                        # 无法通过URL定位文件类型时，通过"Content-Type"定位。
                        suffix = self._content_type_map[content_type]
            # 将后缀小写化。
            suffix = suffix.lower()
            # 返回结果。
            return file_bytes, content_type, suffix
        else:
            raise ValueError(f"Error response: {resp.status_code}.")

    def upload(self, file, content, content_type=None):
        """
        上传链接的内容至云存储上，返回新的URL。
        :param file: 文件名（带后缀）。
        :param content: 文件名（带后缀）。
        :param content_type: MIME-Type字符串。
        :return:
        """

        # 参数验证。
        assert file and isinstance(file, str), f"Error param, file: {file}."
        assert content and isinstance(content, bytes), "Error param, content."

        # 根据文件后缀决定类型是否为流。
        if content_type is None:
            # 设置一个默认值。
            content_type = self._default_content_type
            # 从文件名中提取文件后缀。
            if "." in file:
                file_suffix = str(file.split(".")[-1]).strip().lower()
                if file_suffix:
                    # 根据文件后缀映射得到content_type。
                    map_content_type = self._suffix_map.get(file_suffix)
                    if map_content_type is not None:
                        content_type = map_content_type
        else:
            # 参数验证。
            assert content_type and isinstance(content_type, str) and "/" in content_type, \
                f"Error param, content_type: {content_type}."
            content_type = content_type.lower()
            if content_type in self._content_type_map and "." not in file:
                file_suffix = self._content_type_map[content_type]
                file = f"{file}.{file_suffix}"

        # 上传路径。
        key = "{}/{}".format(self._key_prefix, file)
        key = key.replace("//", "/")
        url = self.convert_key_to_url(key)

        # 执行上传，并测试重复上传相同文件时的返回结果。
        self._cloud_client.put_object(
            bucket_name=self._bucket,
            key=key,
            data=content,
            content_length=len(content),
            content_md5=self.md5_baidubce(content),
            content_type=content_type
        )

        # 列出上传路径的图片。
        # response = self._bos_client.list_objects(self._bucket, prefix=self._key_prefix)
        # for obj in response.contents:
        #     print(obj.key)

        self._logger.info("Upload ok, {}.".format(url))
        return url

    def named_by_content_then_upload(self, file_bytes, content_type=None, suffix=None):
        """
        根据文件内容制定文件名，并上传至BOS。
        :param file_bytes: 文件内容。
        :param content_type: 内容类型。
        :param suffix: 后缀。
        :return:
        """

        # 文件名称，通过文件内容算得。
        file_key = md5_bytes(file_bytes)
        if suffix:
            file_name = f"{file_key}.{suffix}"
        else:
            file_name = file_key

        # 判断文件是否已存在。
        flag, bos_url = self.exists(file=file_name, file_meta=dict(content_length=len(file_bytes)))
        if flag is False:
            # 不存在时才上传。
            bos_url = self.upload(file=file_name, content=file_bytes, content_type=content_type)

        # 返回链接。
        return bos_url

    def api_exists(self, request):
        """
        接口，检查文件是否已存在，会检查文件长度。
        :param request: 请求体。
        :return:
        """

        # 初始化参数。
        file = ""

        try:
            # 获取文件名。
            body = json.loads(request.body)
            file = body["file"]
            file_meta = body["file_meta"]

            # 检查是否存在。
            flag, url = self.exists(file, file_meta)
            if flag in (True, False):
                return dict(code=1, msg="ok", data=dict(exists=flag, url=url))
            else:
                raise ValueError("Unknown flag: {}.".format(flag))
        except Exception as e:
            self._logger.warning(f"{file}, {e}\n{traceback.format_exc()}")
            return dict(code=0, msg=str(e), data=dict())

    def api_check_key_exists(self, request):
        """
        接口，检查文件是否已存在。
        :param request: 请求体。
        :return:
        """

        # 初始化参数。
        file = ""

        try:
            # 获取文件名。
            body = json.loads(request.body)
            file = body["file"]

            # 检查是否存在。
            flag, url = self.check_key_exists(file)
            if flag in (True, False):
                return dict(code=1, msg="ok", data=dict(exists=flag, url=url))
            else:
                raise ValueError("Unknown flag: {}.".format(flag))
        except Exception as e:
            self._logger.warning(f"{file}, {e}\n{traceback.format_exc()}")
            return dict(code=0, msg=str(e), exists=None)

    def api_upload(self, request):
        """
        接口，上传文件流。
        :param request: 请求体。
        :return:
        """

        # 初始化参数。
        file = ""

        try:
            # 记录请求。
            self._logger.info("Path: {}".format(request.get_full_path()))
            # 获取文件名和文件内容。
            body = request.POST
            file = body["file"]

            # 读取一个文件。
            content = b""
            for _file in request.FILES:
                _file = request.FILES[_file]
                if _file:
                    content = b""
                    for chunk in _file.chunks():
                        content += chunk
                break
            if not content:
                raise ValueError("Empty content, {}.".format(file))

            # 保存本地测试。
            # with open("./test.jpg", "wb") as fw:
            #     fw.write(content)

            # 上传至BOS。
            url = self.upload(file, content)
            if url:
                return dict(code=1, msg="ok", data=dict(url=url))
            else:
                raise ValueError("Empty url result.")
        except Exception as e:
            self._logger.warning(f"{file}, {e}\n{traceback.format_exc()}")
            return dict(code=0, msg=str(e), data=dict())

    def api_upload_by_url(self, request):
        """
        下载文件并上传至BOS，如果已经存在于BOS则跳过。
        :param request: 请求体。
        :return:
        """

        # 初始化参数。
        url = ""

        try:
            # 记录请求。
            self._logger.info("Path: {}".format(request.get_full_path()))
            # 获取文件名和文件内容。
            # 获取文件名。
            body = json.loads(request.body)
            url = body["url"]

            # 下载。
            file_bytes, content_type, suffix = self.download_file(url)
            # 上传至BOS。
            url = self.named_by_content_then_upload(file_bytes=file_bytes, content_type=content_type, suffix=suffix)
            if url:
                return dict(code=1, msg="ok", data=dict(url=url))
            else:
                raise ValueError("Empty url result.")
        except Exception as e:
            self._logger.warning(f"{url}, {e}")
            return dict(code=0, msg=str(e), data=dict())

    def api_bos_upload_image_by_url_and_compute_hash(self, request):
        """
        下载图片，计算出哈希值，之后上传至BOS，如果已经存在于BOS则直接返回bos链接。
        :param request: 请求体。
        :return:
        """

        # 初始化参数。
        url = ""

        try:
            # 记录请求。
            self._logger.info("Path: {}".format(request.get_full_path()))
            # 获取文件名和文件内容。
            # 获取文件名。
            body = json.loads(request.body)
            url = body["url"]

            # 下载。
            file_bytes, content_type, suffix = self.download_file(url)

            # 计算图片哈希值。
            try:
                img_hash = image_hash(file_bytes)
            except Exception as e:
                self._logger.debug(f"{e}\n{traceback.format_exc()}")
                img_hash = ""

            # 上传至BOS。
            url = self.named_by_content_then_upload(file_bytes=file_bytes, content_type=content_type, suffix=suffix)
            if url:
                return dict(code=1, msg="ok", data=dict(url=url, imgHash=img_hash))
            else:
                raise ValueError("Empty url result.")
        except Exception as e:
            self._logger.warning(f"{url}, {e}")
            return dict(code=0, msg=str(e), data=dict())
