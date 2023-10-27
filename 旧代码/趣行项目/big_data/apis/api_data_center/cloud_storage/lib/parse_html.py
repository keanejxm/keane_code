# -*- coding:utf-8 -*-
"""
解析html数据体，将img、video、audio标签对应的src链接上传至云存储，并替换新的链接后返回。
相当于“一键保存本地”功能。
# author: Trico
# date: 2020/8/24
# update: 2020/8/24
"""

import re
import bs4
import logging
import datetime
import requests
import traceback
import html as html_parse
from urllib.parse import urljoin

from cloud_storage.lib.bos_operate import BaiduBosOperate
from api_common_utils.utils import md5, md5_bytes
from api_common_utils.llog import LLog
from api.config import api_log_path
from api_common_utils.get_weibo_video_url import GetWeiboVideoUrl
from api_common_utils.get_dayu_new_videos import GetDaYuVideo
from api_common_utils.get_toutiao_video_url import GetToutiaoVideoUrl


class ParseHtml(object):
    """
    解析html数据体，将img、video、audio标签对应的src链接上传至云存储，并替换新的链接后返回。
    """

    def __init__(self, logger):

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

        # 获取会话，用于获取各频道XHR数据。
        self._session = self.get_session()

        # 匹配模式。
        self._resource_patterns = {
            "img": re.compile(
                r"<img\b[^<>]*?\bsrc[\s]*=[\s]*[\"\']?[\s]*(?P<href>[^\s\"\'<>]*)[^<>]*?/?[\s]*>",
                flags=re.I | re.S),
            "video": re.compile(
                r"<video\b[^<>]*?\bsrc[\s]*=[\s]*[\"\']?[\s]*(?P<href>[^\s\"\'<>]*)[^<>]*?/?[\s]*>",
                flags=re.I | re.S),
            "audio": re.compile(
                r"<audio\b[^<>]*?\bsrc[\s]*=[\s]*[\"\']?[\s]*(?P<href>[^\s\"\'<>]*)[^<>]*?/?[\s]*>",
                flags=re.I | re.S),
            "source": re.compile(
                r"<source\b[^<>]*?\bsrc[\s]*=[\s]*[\"\']?[\s]*(?P<href>[^\s\"\'<>]*)[^<>]*?/?[\s]*>",
                flags=re.I | re.S),
        }

        # 后缀类型。
        self._suffixes = {
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
        self._content_types_map = {
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
        }

        # 符合条件的链接被过滤，根据子类设置。
        self._filter_pattern = None

        # 既定的视频标签封面图链接后缀。
        self._video_poster_suffix = ""

        # 未知文件后缀。
        self._unknown_suffix = "unknown"
        # 默认图片后缀。
        self._default_img_suffix = "jpg"
        # 默认视频后缀。
        self._default_video_suffix = "mp4"
        # 默认音频后缀。
        self._default_audio_suffix = "mp3"

    @staticmethod
    def get_session():
        """
        获取session对象。
        :return:
        """

        # 请求头。
        request_headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; '
                          '.NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',
            'Connection': 'Keep-Alive',
        }

        # HTTP会话。
        session = requests.Session()
        session.headers.update(request_headers)

        return session

    def fetch(self, resource_href, default_suffix=None):
        """
        下载资源，并分析资源的后缀格式。
        :return:
        """

        # 参数验证。
        if not resource_href or not isinstance(resource_href, str) or not resource_href.startswith("http"):
            raise ValueError("Param error!")
        if not default_suffix or not isinstance(default_suffix, str):
            default_suffix = self._unknown_suffix

        # 首先通过图片URL定位文件类型。
        resource_suffix = default_suffix
        resource_href_suffix = resource_href.split(".")[-1]
        if resource_href_suffix and resource_href_suffix in self._suffixes:
            resource_suffix = resource_href_suffix

        # 请求文件内容。
        response = self._session.get(resource_href, timeout=5)
        if str(response.status_code).startswith("2"):
            response_headers = response.headers
            content = response.content
        else:
            raise requests.RequestException("Error {}".format(response.status_code))

        # 分析响应头。
        content_type = None
        if not resource_suffix or resource_suffix == self._unknown_suffix:
            if "Content-Type" in response_headers and response_headers["Content-Type"]:
                content_type = response_headers.get("Content-Type")
                # 检查响应头的内容格式是否认识。
                if content_type in self._content_types_map:
                    # 无法通过URL定位文件类型时，通过"Content-Type"定位。
                    resource_suffix = self._content_types_map[content_type]

        return dict(
            content=content,
            resource_suffix=resource_suffix,
            content_type=content_type,
        )

    def _convert_video_tag(self, tag, default_suffix, sub_path, source_url=""):
        """
        修改video标签，增加controls属性，如果有poster，则将poster里的链接页上传至云存储。
        :return:
        """

        # 初始化video数据信息。
        src = tag.attrs["src"]
        size = 0
        try:
            if "data-size" in src:
                size_list = re.findall(r"[?&]data-size=(\d+)[&]?", src, flags=re.I)
                if size_list:
                    size = int(size_list[0])
        except Exception as e:
            self._logger.warning(f"未能获取视频大小（data-size）, {src}, {e}\n{traceback.format_exc()}")
        video_info = dict(poster="", src=src, size=size)
        # 处理video标签。
        tag.attrs["controls"] = "controls"
        try:
            if "poster" in tag.attrs:
                if tag.attrs["poster"]:
                    poster_link = str(tag.attrs["poster"]).strip()
                    # 过滤链接。
                    if self._filter_pattern and re.match(self._filter_pattern, poster_link):
                        return tag
                    if source_url and not poster_link.startswith("http"):
                        poster_link = urljoin(source_url, poster_link)
                    if poster_link and poster_link.startswith("http"):
                        ret = self.fetch(poster_link, default_suffix)
                        if ret:
                            # 提取参数。
                            content = ret["content"]
                            resource_suffix = ret["resource_suffix"]
                            content_type = ret["content_type"]
                            # 上传至云存储。
                            new_poster_link = self.upload(
                                poster_link, content, sub_path,
                                resource_suffix, content_type
                            )
                            if new_poster_link:
                                tag.attrs["poster"] = new_poster_link
                                video_info["poster"] = new_poster_link
        except Exception as e:
            self._logger.warning(f"未能解析视频的poster，{tag}，{e}\n{traceback.format_exc()}")

        return video_info

    def upload(self, resource_href, content, sub_path, resource_suffix, content_type):
        """
        上传链接的内容至云存储上，返回新的URL。
        :return:
        """

        pass

    def parse_html_by_soup(self, input_text, source_url=""):
        """
        BeautifulSoup方案。
        从html文本中解析出图片、视频、音频等资源的链接。
        上传至Cloud后，更新html文本并返回该文本。
        :param input_text: html片段。
        :param source_url: 信息来源的网址，用于拼接相对路径的src链接。
        :return:
        """

        # 初始化解析的视频链接体，[{"poster": "...", "src": "..."}, ]。
        videos = list()
        try:
            # 参数验证。
            text = input_text.strip()
            assert text, f"Error input_text, text empty."
            assert isinstance(source_url, str), f"Error input_text, source_url: {source_url}."

            # html转码，执行两遍是为了&符号自身转码。
            text = html_parse.unescape(text)
            text = html_parse.unescape(text)

            # 转为soup。
            soup = bs4.BeautifulSoup(text, "html.parser")
            assert soup, "Error, failed to parse html into soup."

            # 找出资源链接。
            target_type_selectors = {
                "img": [{"selector": "img[src]", "default_suffix": self._default_img_suffix}, ],
                "video": [{"selector": "video[src]", "default_suffix": self._default_video_suffix}, ],
                "audio": [{"selector": "audio[src]", "default_suffix": self._default_audio_suffix}, ],
                "source": [
                    {"selector": "video > source[src]", "default_suffix": self._default_video_suffix},
                    {"selector": "audio > source[src]", "default_suffix": self._default_audio_suffix},
                ]
            }
            # 标签的链接均为src属性。
            change_flag = False
            for sub_path, type_selectors in target_type_selectors.items():
                for type_selector in type_selectors:
                    if type_selector:
                        selector = type_selector["selector"]
                        default_suffix = type_selector["default_suffix"]
                        try:
                            tags = soup.select(selector)
                        except Exception as e:
                            self._logger.warning(
                                f"Failed to parse selector '{selector}', {e}\n{traceback.format_exc()}"
                            )
                            continue

                        # 抽取资源链接并上传至云。
                        if tags:
                            for tag in tags:
                                if isinstance(tag, bs4.Tag):
                                    if tag.has_attr("src"):
                                        src = tag.attrs["src"]
                                        try:
                                            # 简易处理和验证，跳过相对路径。
                                            src = str(src).strip()
                                            if source_url and not src.startswith("http"):
                                                src = urljoin(source_url, src)
                                            if src and src.startswith("http"):
                                                # 过滤链接。
                                                if self._filter_pattern and re.match(self._filter_pattern, src):
                                                    continue

                                                # 微博根据视频链接获取临时视频链接
                                                if "https://m.weibo.cn/s/video/show?object_id=" in src:
                                                    try:
                                                        src = GetWeiboVideoUrl().get_weibo_video_url(src)
                                                    except Exception as e:
                                                        self._logger.debug(f"获取视频临时链接失败，{e}")
                                                # 大鱼根据视频连接获取临时视频连接
                                                elif "https://dayu.com/wid" in src:
                                                    try:
                                                        src = GetDaYuVideo().get_new_videos_url(src)
                                                    except Exception as e:
                                                        self._logger.debug(f"获取大鱼视频临时链接失败，{e}")
                                                # 头条视频中转处理。
                                                elif "http://toutiao.com/videoid=" in src:
                                                    try:
                                                        src = GetToutiaoVideoUrl().get_toutiao_video_url(src)
                                                    except Exception as e:
                                                        self._logger.debug(f"获取头条视频临时链接失败，{e}")

                                                # 获取链接内容。
                                                ret = self.fetch(src, default_suffix)
                                                if ret:
                                                    # 提取参数。
                                                    content = ret["content"]
                                                    resource_suffix = ret["resource_suffix"]
                                                    content_type = ret["content_type"]
                                                    # 上传至云存储。
                                                    cloud_src = self.upload(
                                                        src, content, sub_path, resource_suffix, content_type
                                                    )
                                                    if cloud_src:
                                                        self._logger.info(f"Upload '{src}'->'{cloud_src}' OK.")
                                                        # 上传成功后，将原始链接替换为云链接。
                                                        tag.attrs["src"] = cloud_src
                                                        change_flag = True
                                                        # 对视频、音频标签进行特殊加工。
                                                        if tag.name == "video":
                                                            # 处理video标签。
                                                            video_info = self._convert_video_tag(
                                                                tag, default_suffix, sub_path,
                                                                source_url=source_url
                                                            )
                                                            # 增加视频信息，含poster和src。
                                                            videos.append(video_info)
                                                        elif tag.name == "source":
                                                            # source标签的父级如果是video标签，则加入封面图链接和控制器。
                                                            parent_tag = tag.parent
                                                            if parent_tag.name == "video":
                                                                # 处理video标签。
                                                                video_info = self._convert_video_tag(
                                                                    tag, default_suffix, sub_path,
                                                                    source_url=source_url
                                                                )
                                                                # 增加视频信息，含poster和src。
                                                                videos.append(video_info)
                                                        elif tag.name == "audio":
                                                            # 音频标签加入控制器。
                                                            tag.attrs["controls"] = "controls"
                                                        elif tag.name == "source":
                                                            # source标签的父级如果是audio标签，则加入控制器。
                                                            parent_tag = tag.parent
                                                            if parent_tag.name == "audio":
                                                                parent_tag.attrs["controls"] = "controls"
                                                        else:
                                                            pass
                                        except Exception as e:
                                            self._logger.warning(
                                                f"Failed to upload '{src}' to cloud, {e}\n{traceback.format_exc()}")
                                            continue
                                else:
                                    self._logger.debug(f"Not a bs4.Tag, {tag}.")
                                    continue
            # 根据修改情况判断返回方式。
            if change_flag is True:
                # 返回修改后的html文本。
                return str(soup), videos
            else:
                return input_text, videos
        except Exception as e:
            self._logger.warning(f"Failed to parse html content, {e}\n{traceback.format_exc()}")
            return input_text, videos

    def parse_html(self, input_text, source_url=""):
        """
        从html文本中解析出图片、视频、音频等资源的链接。
        上传至Cloud后，更新html文本并返回该文本。
        相当于“一键保存本地”功能。
        :param input_text: html片段。
        :param source_url: 信息来源的网址，用于拼接相对路径的src链接。
        :return:
        """

        # 通过BeautifulSoup的方案替换html文本，可为video标签生成poster属性。
        return self.parse_html_by_soup(input_text, source_url)

    def api_parse_html(self, request):
        """
        接口，解析html文本，
        :param request:
        :return:
        """

        try:
            # 记录请求。
            self._logger.info("Path: {}".format(request.get_full_path()))
            # 后端验证信息。
            _token_str = "{}{}".format(datetime.datetime.now().strftime("%Y%m%d"), "hebeiquxing")
            _token = md5(_token_str)

            # 前端令牌验证。
            post_token = request.POST.get("token")
            self._logger.debug(f"_token:'{_token}', post_token:'{post_token}'.")
            if not post_token or post_token != _token:
                raise ValueError("Unknown request.")
            # 获取html文本。
            html_text = request.POST.get("html_text").strip()
            assert html_text, f"Error request param, html_text."
            # 资源所在网址。
            source_url = request.POST.get("source_url")
            if source_url is None:
                source_url = ""
            else:
                source_url = str(source_url).strip()
                assert source_url and source_url.startswith("http"), f"Error request param, source_url: {source_url}."

            # 解析html文本。
            html_text, videos = self.parse_html(html_text, source_url=source_url)
            if html_text:
                return dict(code=1, msg="ok", data=dict(html_text=html_text, videos=videos))
            else:
                raise ValueError("Empty html text result.")
        except Exception as e:
            self._logger.warning(f"{e}\n{traceback.format_exc()}")
            return dict(code=0, msg=str(e), data=dict())


class ParseHtmlBos(ParseHtml):
    """
    解析html数据体，将img、video、audio标签对应的src链接上传至云存储，并替换新的链接后返回。
    解析后上传至BOS。
    """

    def __init__(self, logger):
        super(ParseHtmlBos, self).__init__(logger)

        # 符合条件的链接被过滤。
        self._filter_pattern = re.compile(r"http[s]?://[\w]*?\.bcebos\.com", flags=re.I | re.S)

    def upload(self, resource_href, content, sub_path, resource_suffix, content_type):
        """
        上传链接的内容至云存储上，返回新的URL。
        :return:
        """

        # 参数验证。
        assert content and isinstance(content, bytes), f"Error param, content: {content}."
        assert resource_suffix and isinstance(resource_suffix, str), f"Error param, resource_suffix: {resource_suffix}."

        # 上传路径。
        bos_obj = BaiduBosOperate(self._logger)
        key = "{}.{}".format(md5_bytes(content), resource_suffix)
        key = key.replace("//", "/")

        # 先判断是否已存在，如果存在则直接返回URL。
        flag, url = bos_obj.exists(key, file_meta=dict(content_length=len(content)))
        if flag is False:
            url = bos_obj.upload(key, content)
        # 标记文件大小。
        url = bos_obj.add_object_size_to_url(url, key)

        # 返回结果。
        return url
