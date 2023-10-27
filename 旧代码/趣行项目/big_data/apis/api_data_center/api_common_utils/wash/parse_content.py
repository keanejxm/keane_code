# -*- coding:utf-8 -*-
"""
解析正文，提取必要数据。
# author: Trico
# date: 2021/1/21
# update: 2021/1/21
"""

import re
import bs4
import html
from urllib.parse import urljoin


class ParseContent(object):
    """
    解析正文。
    """

    def __init__(self):
        pass

    @staticmethod
    def do_parse(content, site_url=None):
        """
        解析正文，提取必要数据。
        :param content: 正文内容。
        :param site_url: 正文链接，用于获取准确的资源url。
        :return: dict(
            content=content,
            contentWordsNum=0,
            digest="",
            images=[],
            covers=[],
            videos=[],
            audios=[],
        )
        """

        # 调取PHP回调接口。
        result = dict(
            content=content,
            contentWordsNum=0,
            digest="",
            images=[],
            covers=[],
            videos=[],
            audios=[],
        )

        # 参数验证。
        assert content and isinstance(content, str), "Error param, content."

        # 去除首尾空白。
        content = str(content).strip()

        # 转换两遍是为了避免"&amp;"符号（&）。
        content = html.unescape(content)
        content = html.unescape(content)

        # 开始清洗正文。
        content_soup = bs4.BeautifulSoup(content, "html.parser")

        # 删除script、style、link等标签。
        for tag in content_soup(("head", "script", "style", "link", "meta")):
            tag.extract()
        # 删除注释。
        for tag in content_soup(text=lambda text: isinstance(text, bs4.Comment)):
            tag.extract()

        # 统计字数。
        content_text = str(content_soup.get_text()).strip()
        content_text = re.sub(r"\s{2,}", " ", content_text)
        result["digest"] = content_text[:200]
        content_text = re.sub(r"\s", "", content_text)
        result["contentWordsNum"] = len(content_text)
        # 提取摘要（前200个字）。

        # 图片。
        for tag in content_soup("img"):
            if "src" in tag.attrs:
                if site_url:
                    tag["src"] = urljoin(site_url, str(tag.attrs["src"]).strip())
                else:
                    tag["src"] = str(tag.attrs["src"]).strip()
                result["images"].append(tag["src"])
        # 封面图。
        if result["images"]:
            result["covers"].append(result["images"][0])

        # 视频。
        for tag in content_soup("video"):
            if "src" in tag.attrs:
                if site_url:
                    tag["src"] = urljoin(site_url, str(tag.attrs["src"]).strip())
                else:
                    tag["src"] = str(tag.attrs["src"]).strip()
                result["videos"].append(tag["src"])
            # 检查source子标签。
            for tag_source in tag("source"):
                if "src" in tag_source.attrs:
                    if site_url:
                        tag_source["src"] = urljoin(site_url, str(tag_source.attrs["src"]).strip())
                    else:
                        tag_source["src"] = str(tag_source.attrs["src"]).strip()
                    result["videos"].append(tag_source["src"])

        # 音频。
        for tag in content_soup("audio"):
            if "src" in tag.attrs:
                if site_url:
                    tag["src"] = urljoin(site_url, str(tag.attrs["src"]).strip())
                else:
                    tag["src"] = str(tag.attrs["src"]).strip()
                result["audios"].append(tag["src"])
            # 检查source子标签。
            for tag_source in tag("source"):
                if "src" in tag_source.attrs:
                    if site_url:
                        tag_source["src"] = urljoin(site_url, str(tag_source.attrs["src"]).strip())
                    else:
                        tag_source["src"] = str(tag_source.attrs["src"]).strip()
                    result["audios"].append(tag_source["src"])

        # 去除首尾空白。
        result["content"] = str(content_soup).strip()

        # 返回结果。
        return result


def test_request():
    # 测试。

    import json
    import requests
    from lxml import etree
    url = "https://www.sohu.com/a/290159073_116366"
    resp = requests.get(url)
    tree = etree.HTML(resp.text)
    content_xpath = "//article"
    contents = tree.xpath(content_xpath)
    if contents:
        content = etree.tostring(contents[0], encoding='utf-8').decode('utf-8')
    else:
        raise ValueError(f"正则匹配失败，{content_xpath}，{url}")
    res = ParseContent.do_parse(content, site_url=url)
    print(json.dumps(res, ensure_ascii=False, indent=4))


def test_html():
    # 测试。

    import json
    # content = """<!DOCTYPE html><html><body>
    #     <audio controls>
    #         <source src="/i/horse.ogg" type="audio/ogg">
    #         <source src="/i/horse.mp3" type="audio/mpeg">
    #                您的浏览器不支持此元素标签，Your browser    does    not support   the element.
    #     </audio>
    #     </body></html>
    # """
    content = """<!DOCTYPE html>
            <html><body>
            <image src="/i/dog.jpg" />
            <video src="/i/cat.mp4" />
            <video controls>
                <source src="/i/horse.mp4" type="video/mp4">
                <source src="/i/horse.3gp" type="video/3gpp">
                       您的浏览器不支持此元素标签，Your browser    does    not support   the element.          
            </video>
            </body></html>
        """
    res = ParseContent.do_parse(content, site_url="https://www.w3school.com.cn/tiy/t.asp?f=html5_source_src")
    print(json.dumps(res, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    test_html()
