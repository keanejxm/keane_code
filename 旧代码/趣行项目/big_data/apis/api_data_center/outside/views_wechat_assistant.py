# -*- coding:utf-8 -*-
"""
微信助手视图。
# author: BigDataTeam，Trico
# date: 2021/1/23
# update: 2021/1/23
"""

import re
import bs4
import json
import html
import traceback
import requests
from django.views import View
from django.http import JsonResponse
from lxml import etree, html

from api_common_utils.llog import LLog
from api.config import api_log_path
from api_common_utils.utils import log_request_info
from api_common_utils.proxy import get_abuyun_proxies

LOGGER = LLog(logger_name="wechat_assistant", log_path=api_log_path, logger_level="INFO").logger


class WeChatAssistant(View):

    def __init__(self, *args, **kwargs):
        super(WeChatAssistant, self).__init__(*args, **kwargs)
        self._logger = LOGGER

    def post(self, request):
        """
        入口。
        :param request: 请求体。
        :return:
        """

        try:
            log_request_info(self._logger, request)
            body = json.loads(request.body)
            res = self.fetch_article(body.get("url"))
            return JsonResponse({"code": 1, "msg": "ok", "data": res})
        except Exception as e:
            self._logger.warning(f'{e}\n{traceback.format_exc()}')
            return JsonResponse({"code": 0, "msg": str(e)})

    def fetch_article(self, url):
        """
        根据微信链接获取结果。
        :param url: 微信链接。
        :return:
        """

        assert url and isinstance(url, str) and "weixin.qq.com" in url, f"参数错误，url：{url}"

        try:
            proxies = get_abuyun_proxies()
            resp = requests.get(url=url, proxies=proxies, timeout=30)
            if resp.status_code == requests.codes.ok:
                resp.encoding = "utf-8"
                return self.parse_article(resp.text)
            else:
                raise ValueError(f"请求失败，{resp.status_code}，{url}")
        except Exception as e:
            self._logger.warning(f"{url}，{e}\n{traceback.format_exc()}")
            raise e

    def parse_article(self, resp_text):
        """
        解析响应体。
        :return:
        """

        # 默认字段。
        works = dict(
            accountName="",
            title="",
            content="",
            pubTime=None,
            source="",
            isOriginal=-1,
        )
        # 获取文章详情页。
        content_tree = etree.HTML(resp_text)

        # 账号名。
        accounts = content_tree.xpath("//*[@id='js_name']/text()")
        if accounts:
            works["accountName"] = str(accounts[0]).strip()
        else:
            raise ValueError(f"未能获取账号名称")

        # 标题。
        titles = content_tree.xpath("//*[@class='rich_media_title']//text()")
        if titles:
            works["title"] = str(titles[0]).strip()
        else:
            raise ValueError(f"未能获取标题")

        # 正文。
        works["content"] = html.tostring(
            content_tree.xpath("//div[@id='js_content']")[0], encoding='utf-8'
        ).decode("utf-8")
        works["content"] = str(works["content"]).strip()

        # 添加content处理。
        bs = bs4.BeautifulSoup(works["content"], "html.parser")
        # 处理图片。
        for img_tag in bs.find_all("img"):
            if "data-src" in img_tag.attrs and "src" not in img_tag.attrs:
                img_tag.attrs["src"] = img_tag.attrs["data-src"]
                works["content"] = str(bs).strip()
        # 清洗不可见的标签。
        target_element = bs.find(id="js_content")
        if target_element is not None:
            if "style" in target_element.attrs:
                target_element = bs.find(id="js_content")
                if "visibility: hidden" in target_element["style"]:
                    target_element["style"] = target_element["style"].replace("visibility: hidden", "")
                    works["content"] = str(bs).strip()

        # 检查详情页中是否有视频，有的话就整合成video标签。
        video_string = self._video_parser(works["title"], resp_text)
        if video_string:
            works["content"] = f"{video_string}\n{works['content']}"

        # 发布时间。
        pub_times = re.findall(r'var ct = "(\d+)";', resp_text)
        if pub_times:
            works["pubTime"] = int(pub_times[0]) * 1000
        else:
            raise ValueError("未能获取准确的发布时间")

        # 来源：央视新闻</span>
        source = re.compile('来源：(.*?)<').findall(works["content"])
        if source:
            works["source"] = source[0]
            works["isOriginal"] = 0
            if source[0] == works["accountName"]:
                works["isOriginal"] = 1

        return works

    def _video_parser(self, title, resp_text):
        """
        解析视频信息。
        :param title: 标题。
        :param resp_text: 响应体。
        :return:
        """

        # 检查详情页中是否有视频，有的话就整合成video标签。
        video_url = video_poster = video_height = video_width = video_size = video_duration = None
        if '<div class="js_video_channel_container">' in resp_text:
            # 视频信息。
            video_blocks = re.findall(
                r'{[^}]+?url:\s*"https?://mpvideo\.qpic\.cn/[^"]+",[^}]+?video_quality_level[^}]+?}',
                resp_text
            )
            if video_blocks:
                # 遍历视频js代码块，一般按清晰度高到低。
                for video_block in video_blocks:
                    video_urls = re.findall(r'url: "(https?://mpvideo\.qpic\.cn/[^"]+)",', video_block)
                    if video_urls:
                        # 视频链接。
                        video_url = str(video_urls[0]).strip()
                        video_url = video_url.replace("\\x26amp;", "&")
                        try:
                            # 视频其它信息。
                            video_height = re.findall(r'height: "(\d+)"', video_block)[0]
                            video_width = re.findall(r'width: "(\d+)"', video_block)[0]
                            video_size = re.findall(r'filesize: "(\d+)"', video_block)[0]
                            video_duration = re.findall(r'duration_ms: "(\d+)"', video_block)[0]
                            video_duration = int(int(video_duration) / 1000)
                        except Exception as e:
                            self._logger.debug(f"视频详细信息获取失败：{video_block}，{e}\n{traceback.format_exc()}")
                        break
            # 视频封面图。
            video_posters = re.findall(
                r'window.__mpVideoCoverUrl = "(https?://mmbiz.qpic.cn/mmbiz_jpg/[^"]+)";',
                resp_text
            )
            if video_posters:
                video_poster = str(video_posters[0]).strip()
        if video_url:
            video_string = f'<video ' \
                f'src="{video_url}" ' \
                f'poster="{video_poster}" ' \
                f'title="{title}" ' \
                f'height="{video_height if video_height is not None else ""}" ' \
                f'width="{video_width if video_width is not None else ""}" ' \
                f'size="{video_size if video_size is not None else ""}" ' \
                f'duration="{video_duration}" ' \
                f'controls="controls" />'
            return video_string
        else:
            return None


def test():
    # 测试。

    urls = [
        "https://mp.weixin.qq.com/s/Wl4ZEosLBVhWjPEsPbKnuw",
    ]
    for url in urls:
        res = WeChatAssistant().fetch_article(url)
        print(json.dumps(res, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    test()
