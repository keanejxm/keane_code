# -*- coding:utf-8 -*-
"""
# project: 电子报爬虫
# author: Neil
# date: 2020/10/15

"""

import datetime
import hashlib
import html
import json
import random
import re
import time
import traceback
import unicodedata
from urllib.parse import urljoin

import bs4
import requests
from lxml import etree

from api_common_utils.proxy import get_abuyun_proxies
from lib.common_utils.llog import LLog
from lib.test.epaper_test.extract_digest import GetExtractDigest
from lib.test.epaper_test.save_to_ES import LayoutsCrawlerESUtils
from lib.test.epaper_test.deal_with_epaper_templates import DealWithTemplates


def md5_(str):
    """
    产生md5加密
    :param str: 字符串
    :return: 加密字段
    """
    str = str.encode('utf-8')
    md5_ = hashlib.md5(str).hexdigest()
    return md5_


class NewspaperSpider(object):

    def __init__(self, paper_template, target_dates=None, roll_back_days=0, use_proxies=True, logger=None):
        """
        初始化
        :param paper_template: 电子报的xpath模板信息，来源于数据库中的条目。
        """
        # 平台类型
        self._platform_type = 5
        # 平台名称
        self._platform_name = paper_template["platformName"]
        # 平台ID
        self._platform_id = paper_template["platformID"]
        assert self._platform_id and isinstance(self._platform_id, str), "Error param, _platform_id."
        # 该平台所属是父级ID
        self._parents_id = paper_template["types"]
        assert self._parents_id and isinstance(self._parents_id, list), "Error param, _parents_id."
        self._logger = logger
        epaper_template = json.loads(paper_template["value"])
        self._paper = epaper_template
        # assert "id" in paper_template, "Error param, paper_template.id."
        assert self._paper and isinstance(self._paper, dict), "Error param, paper_template."
        assert "platformName" in self._paper, "Error param, paper_template.platformName."
        assert "start_url" in self._paper, "Error param, paper_template.start_url."
        # 起始地址。
        self._start_url = self._paper["start_url"]
        assert self._start_url and isinstance(self._start_url, str), "Param start_url error."
        # 版面信息
        self._layout_url_xpaths = list()
        # 版面链接提取方式。
        if "layout_url_xpath" in self._paper or "layout_next_xpath" in self._paper:
            if self._paper["layout_url_xpath"]:
                self._layout_url_xpaths = self._paper["layout_url_xpath"]
            elif self._paper["layout_next_xpath"]:
                self._layout_next_xpaths = self._paper["layout_next_xpath"]
            else:
                raise ValueError("Param layout_url_xpath error.")
        else:
            raise ValueError("Param layout_url_xpath error.")

        # 详情页相关xpath。
        self._type = self._paper["detail_url_xpath"]
        if isinstance(self._type, str):
            self._detail_url_xpaths = json.loads(self._paper["detail_url_xpath"])
            self._detail_pre_title_xpaths = json.loads(self._paper["detail_pre_title_xpath"])
            self._detail_title_xpaths = json.loads(self._paper["detail_title_xpath"])
            self._detail_sub_title_xpaths = json.loads(self._paper["detail_sub_title_xpath"])
            self._detail_content_xpaths = json.loads(self._paper["detail_content_xpath"])
        elif isinstance(self._type, list):
            # 详情页相关xpath。
            self._detail_url_xpaths = self._paper["detail_url_xpath"]
            self._detail_pre_title_xpaths = self._paper["detail_pre_title_xpath"]
            self._detail_title_xpaths = self._paper["detail_title_xpath"]
            self._detail_sub_title_xpaths = self._paper["detail_sub_title_xpath"]
            self._detail_content_xpaths = self._paper["detail_content_xpath"]
        # 请求头。
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/74.0.3729.169 Safari/537.36",
        }
        # 整理成多个日期的起始链接。
        self._start_urls = dict()
        if target_dates and isinstance(target_dates, (tuple, list)):
            # 从日期列表中循环执行。
            for target_date in target_dates:
                # noinspection PyBroadException
                try:
                    current_day = datetime.datetime.strptime(target_date, "%Y-%m-%d")
                    start_url = current_day.strftime(self._start_url)
                    pub_time = int(current_day.replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
                    self._start_urls[start_url] = pub_time
                except Exception as e:
                    self._logger.warning("Failed to parse '{}', '{}'.".format(target_date, e))
        else:
            # 以当前日期开始回滚执行。
            # noinspection PyBroadException
            try:
                # 采集报纸回滚的天数，0代表只采集当天。
                self._roll_back_days = int(roll_back_days)
                if self._roll_back_days < 0:
                    self._roll_back_days = 0
            except Exception:
                self._logger.warning("Error param, roll_back_days: {}.".format(roll_back_days))
                self._roll_back_days = 0
            # 从新到旧迭代。
            now = datetime.datetime.now()
            for i in range(0, 0 - (self._roll_back_days + 1), -1):
                current_day = (now + datetime.timedelta(days=i))
                start_url = current_day.strftime(self._start_url)
                pub_time = int(current_day.replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
                # 整理成不同日期的起始地址。
                self._start_urls[start_url] = pub_time

        # 已存在的版面链接。
        self._exist_layout_urls = set()
        # 清空标题、版题里的换行符。
        self._line_feed_pattern = re.compile(r"[\r\n]")
        # 提取数字。
        self._layout_number_pattern = re.compile(r"0*\d{1,4}")
        self._href_xpath_pattern = re.compile(r"/@href$")
        # 超时时间。
        self._timeout = 30
        # 获取会话。
        self._session = requests.Session()
        self._session.headers.update(self._headers)
        # 听过判断报纸名字确定是否使用代理
        if "新华每日电讯" in self._paper["platformName"] or "中国纪检监察报" in self._paper["platformName"]:
            use_proxies = False
        else:
            use_proxies = True
        # 使用代理。
        if use_proxies is True:
            self._session.proxies = get_abuyun_proxies()
        else:
            pass
        # self._session.proxies = get_abuyun_proxies()
        # 默认编码集。
        self._default_charset = None
        # 需要转换的编码集合。
        self._convert_zh_charsets = {
            "gb2312": "gb18030",
            "gbk": "gb18030",
        }
        # 编码集。
        self._charsets = {"utf-8", "utf8", "gb2312", "gbk", "gb18030", "big5","UTF-8-SIG"}

    @staticmethod
    def parse_map(url, map_content):
        """
        解析map标签。
        :return:
        """

        soup = bs4.BeautifulSoup(map_content, "html.parser")
        area_tags = soup.find_all("area")
        areas = dict()
        for area_tag in area_tags:
            if area_tag.has_attr("url"):
                areas[urljoin(url, area_tag.attrs["url"])] = dict(
                    shape=area_tag.attrs["shape"],
                    coords=area_tag.attrs["coords"],
                )
            else:
                areas[urljoin(url, area_tag.attrs["href"])] = dict(
                    shape=area_tag.attrs["shape"],
                    coords=area_tag.attrs["coords"],
                )

        return areas

    def _get_charset(self, response):
        """
        获取response编码。
        :return:
        """

        # 参数验证。
        if not response or not isinstance(response, requests.Response):
            raise ValueError("The 'response' is not a type of 'requests.Response'.")

        # 最终结果。
        final_encoding = None
        # 从正文中解析编码格式。
        content_encoding_list = list()
        # noinspection PyBroadException
        try:
            # requests.utils.get_encodings_from_content()方法可能会被移除。
            content_encoding_list = requests.utils.get_encodings_from_content(response.text)
        except Exception:
            pass
        if content_encoding_list:
            for content_encoding in content_encoding_list:
                if content_encoding.lower() in self._charsets:
                    final_encoding = content_encoding
                    break

        # 从响应头中解析编码格式。
        if not final_encoding:
            header_encoding = requests.utils.get_encoding_from_headers(response.headers)
            if header_encoding and header_encoding.lower() in self._charsets:
                final_encoding = header_encoding

        # 返回近似编码。
        if not final_encoding:
            final_encoding = response.apparent_encoding

        # 针对gb2312、gbk字符集进行超集处理。
        if final_encoding and final_encoding.lower() in self._convert_zh_charsets:
            final_encoding = self._convert_zh_charsets[final_encoding.lower()]

        return final_encoding

    def get_layout_number_from_string(self, input_string):
        """
        字符串提取版号数字。
        :return:
        """

        # noinspection PyBroadException
        try:
            number = int(re.search(self._layout_number_pattern, input_string).group())
            if number > 1000 or number <= 0:
                raise ValueError("Wrong layout number: {}.".format(number))
            else:
                return number
        except Exception as e:
            self._logger.warning("Failed to get number '{}', '{}'.".format(input_string, e))
            return None

    def fetch_detail(self, urls, layout_num):
        """
        获取稿件详情。
        :return:
        """

        rows = list()
        for i, url in enumerate(urls, start=1):
            row = {
                "url": url,
                "preTitle": "",
                "title": "",
                "subTitle": "",
                "content": "",
            }

            # noinspection PyBroadException
            try:
                time.sleep(random.random() / 10 + 1.2)
                response = self._session.get(url, headers=self._headers, timeout=self._timeout)
                if response.status_code == requests.codes.ok:
                    # 得到真实的URL地址。
                    url = response.url
                    try:
                        response.encoding = self._get_charset(response)
                    except Exception as e:
                        raise ValueError("Failed to encoding {}, '{}'.".format(url, e))
                    # 解析成树。
                    tree = etree.HTML(response.text)
                    # 预标题。
                    pre_title = ""
                    for detail_pre_title_xpath in self._detail_pre_title_xpaths:
                        if not detail_pre_title_xpath:
                            continue
                        if not detail_pre_title_xpath.endswith("/text()"):
                            detail_pre_title_xpath = "{}/text()".format(detail_pre_title_xpath)
                        pre_title_list = tree.xpath(detail_pre_title_xpath)
                        if pre_title_list:
                            pre_title = "".join(pre_title_list).strip()
                            if pre_title:
                                pre_title = re.sub(self._line_feed_pattern, " ", pre_title)
                                break

                    # 标题。
                    title = ""
                    for detail_title_xpath in self._detail_title_xpaths:
                        if not detail_title_xpath:
                            continue
                        if not detail_title_xpath.endswith("/text()"):
                            detail_title_xpath = "{}/text()".format(detail_title_xpath)
                        title_list = tree.xpath(detail_title_xpath)
                        if title_list:
                            title = "".join(title_list).strip()
                            if title:
                                title = re.sub(self._line_feed_pattern, " ", title)
                                break

                    # 子标题。
                    sub_title = ""
                    for detail_sub_title_xpath in self._detail_sub_title_xpaths:
                        if not detail_sub_title_xpath:
                            continue
                        if not detail_sub_title_xpath.endswith("/text()"):
                            detail_sub_title_xpath = "{}/text()".format(detail_sub_title_xpath)
                        sub_title_list = tree.xpath(detail_sub_title_xpath)
                        if sub_title_list:
                            sub_title = "".join(sub_title_list).strip()
                            if sub_title:
                                sub_title = re.sub(self._line_feed_pattern, " ", sub_title)
                                break

                    # 正文。
                    content = ""
                    for detail_content_xpath in self._detail_content_xpaths:
                        if not detail_content_xpath:
                            continue
                        content_list = tree.xpath(detail_content_xpath)
                        content_list = list(map(lambda x: etree.tostring(x, encoding="unicode").strip(), content_list))
                        content = "".join(content_list).strip().replace("  ", "").replace("\n", "").replace("\r", "")

                        # 转换两遍是为了避免"&amp;"符号（&）。
                        content = html.unescape(content)
                        content = html.unescape(content)
                        # unicodedata模块提供了normalize方法将Unicode字符转换为正常字符
                        content = unicodedata.normalize('NFKC', content)
                        # 清洗正文。
                        content_soup = bs4.BeautifulSoup(content, "html.parser")
                        # 删除script、style标签
                        for tag in content_soup(("script", "style")):
                            tag.extract()
                        # 删除注释。
                        for tag in content_soup(text=lambda text: isinstance(text, bs4.Comment)):
                            tag.extract()
                        # 将content中的href、src更换成绝对路径。
                        for tag in content_soup(["img", "image", "video", "audio", "source"]):
                            if "src" in tag.attrs and tag.attrs["src"]:
                                # 将链接中的反斜杠替换为正斜杠。
                                slash_src = tag.attrs["src"].replace("\\", "/")
                                tag.attrs["src"] = urljoin(url, slash_src)
                        for tag in content_soup('a'):
                            if "href" in tag.attrs and tag.attrs["href"]:
                                # 将链接中的反斜杠替换为正斜杠。
                                slash_href = tag.attrs["href"].replace("\\", "/")
                                tag.attrs["href"] = urljoin(url, slash_href)
                        content = str(content_soup).strip()
                        # 抓取到后中断循环。
                        if content:
                            break
                    assert content, "The content is empty."

                    # digest获取摘要
                    digest, content_num = GetExtractDigest().extract(content)

                    # 判断文章类型如果含有图片将图片链接提取出来
                    images = list()
                    if "<img" in content:
                        row["contentType"] = 2
                        content_tree = etree.HTML(content)
                        img_list = content_tree.xpath(".//img/@src")
                        for img in img_list:
                            if img:
                                img_url = urljoin(url, img)
                                images.append(img_url)
                            else:
                                continue
                    elif "<image" in content:
                        row["contentType"] = 2
                        content_tree = etree.HTML(content)
                        img_list = content_tree.xpath(".//img/@src")
                        for img in img_list:
                            if img:
                                img_url = urljoin(url, img)
                                images.append(img_url)
                            else:
                                continue
                    else:
                        row["contentType"] = 1
                    # 封面图
                    covers = list()
                    if images:
                        covers.append(images[0])
                    else:
                        covers = list()

                    # 判断头版头条
                    if layout_num == 1 and i == 1:
                        # "5_2_1"中党党报 "5_2_2"省市级党报
                        if "5_2_1" in self._parents_id or "5_2_2" in self._parents_id:
                            row["classifications"] = ["rcmd_1"]
                        else:
                            row["classifications"] = []
                    else:
                        row["classifications"] = []
                    # 整理结果集。
                    row["url"] = url
                    row["status"] = 1
                    row["preTitle"] = pre_title
                    row["title"] = title
                    row["authors"] = []
                    row["subTitle"] = sub_title
                    row["digest"] = digest
                    row["digestOriginal"] = ""
                    row["content"] = content
                    row["images"] = images
                    row["covers"] = covers
                    row["contentWordsNum"] = content_num
                    row["channelID"] = ""
                    row["platformID"] = self._platform_id
                    row["platformName"] = self._platform_name
                    row["platformType"] = self._platform_type
                    row["platformWorksID"] = md5_(url)
                    rows.append(row)
            except Exception as e:
                self._logger.warning("Failed to parse {}, '{}'.".format(url, e))

        return rows

    def fetch_layout(self, url, layout_seq, check_next_layout_url=True):
        """
        获取版面信息
        :param url: 版面页面url
        :param layout_seq: 版本号
        :return: 版面信息
        """
        try:
            layout_number = None
            time.sleep(random.random() / 10 + 1.2)
            response = self._session.get(url, headers=self._headers, timeout=self._timeout)
            # response = self._session.get("http://mrdx.cn/content/20210122/Page01DK.htm")
            if response.status_code == requests.codes.ok:
                # 得到真实的URL地址。
                url = response.url
                # noinspection PyBroadException
                # 解析成树。
                try:
                    response.encoding = self._get_charset(response)
                except Exception as e:
                    raise ValueError("Failed to encoding {}, '{}'.".format(url, e))
                tree = etree.HTML(response.text)
                # 存储版面链接。
                layout_urls = list()
                if check_next_layout_url is True:
                    if self._layout_url_xpaths:
                        # 所有版面的链接。
                        for layout_url_xpath in self._layout_url_xpaths:
                            if not layout_url_xpath:
                                continue
                            # 处理成a标签。
                            if layout_url_xpath.endswith("/@href"):
                                layout_url_xpath = re.sub(self._href_xpath_pattern, "", layout_url_xpath)
                                for a_tag in tree.xpath(layout_url_xpath):
                                    href = a_tag.get("href").strip()
                                    if href and href != "#":
                                        layout_url = urljoin(url, href)
                                        if layout_url not in layout_urls:
                                            layout_urls.append(layout_url)
                            else:
                                # 不处理。
                                for href in tree.xpath(layout_url_xpath):
                                    href = href.strip()
                                    if href and href != "#":
                                        layout_url = urljoin(url, href)
                                        if layout_url not in layout_urls:
                                            layout_urls.append(layout_url)
                            if layout_urls:
                                break
                        check_next_layout_url = False

                    elif self._layout_next_xpaths:
                        # 下一版链接。存在的意义不大
                        for layout_next_xpath in self._layout_next_xpaths:
                            if not layout_next_xpath:
                                continue
                            layout_next_hrefs = tree.xpath(layout_next_xpath)
                            if layout_next_hrefs:
                                href = layout_next_hrefs[0].strip()
                                if href and href != "#":
                                    layout_url = urljoin(url, href)
                                    # 这是一步去重，避免我们点击下一版按钮后跳转到相同的版面，形成无限循环，逻辑处理为停止采集。
                                    # 如：青岛早报，20200311，第三版。
                                    if layout_url not in self._exist_layout_urls:
                                        self._exist_layout_urls.add(layout_url)
                                        if layout_url not in layout_urls:
                                            layout_urls.append(layout_url)
                                        break
                                    else:
                                        self._logger.warning(
                                            "Find same layout url after click next layout button: {}.".format(
                                                layout_url)
                                        )
                        if not layout_urls:
                            check_next_layout_url = False
                    else:
                        raise ValueError("Param layout_url_xpath or layout_next_xpath error.")

                # 提取详情页链接。
                detail_urls = list()
                for detail_url_xpath in self._detail_url_xpaths:
                    if not detail_url_xpath:
                        continue
                    hrefs = tree.xpath(detail_url_xpath)
                    if hrefs:
                        for href in hrefs:
                            if href and href != "#":
                                detail_urls.append(urljoin(url, href))

                # 版面的map标签。
                layout_areas = dict()
                if "layout_map_xpath" in self._paper and self._paper["layout_map_xpath"]:
                    layout_map_xpaths = self._paper["layout_map_xpath"]
                    for layout_map_xpath in layout_map_xpaths:
                        if not layout_map_xpath:
                            continue
                        map_list = tree.xpath(layout_map_xpath)
                        map_list = list(map(lambda x: etree.tostring(x, encoding="unicode").strip(), map_list))
                        map_content = "".join(map_list).strip()
                        layout_areas = self.parse_map(url, map_content)

                # 版面标题。
                layout_title = ""
                if "layout_title_xpath" in self._paper and self._paper["layout_title_xpath"]:
                    layout_title_xpaths = self._paper["layout_title_xpath"]
                    for layout_title_xpath in layout_title_xpaths:
                        if not layout_title_xpath:
                            continue
                        if not layout_title_xpath.endswith("/text()"):
                            layout_title_xpath = "{}/text()".format(layout_title_xpath)
                        layout_titles = tree.xpath(layout_title_xpath)
                        if layout_titles:
                            layout_title = "".join(
                                [str(layout_title).strip().replace("|", '').replace("\r", '').replace("\n", '') for
                                 layout_title
                                 in layout_titles]).strip()
                            # 尝试从版面标题中取得版号。
                            layout_number_from_text = self.get_layout_number_from_string(layout_title)
                            if layout_number_from_text:
                                layout_number = layout_number_from_text
                            # 替换版题中出现的换行符。
                            layout_title = re.sub(self._line_feed_pattern, "", layout_title)
                            break

                # 版面map标签对应的缩略图。
                layout_map_image_url = ""
                if "layout_map_image_xpath" in self._paper \
                        and self._paper["layout_map_image_xpath"]:
                    layout_map_image_xpaths = self._paper["layout_map_image_xpath"]
                    for layout_map_image_xpath in layout_map_image_xpaths:
                        if not layout_map_image_xpath:
                            continue
                        layout_map_image_hrefs = tree.xpath(layout_map_image_xpath)
                        if layout_map_image_hrefs:
                            # 将链接中的反斜杠替换为正斜杠。
                            slash_href = layout_map_image_hrefs[0].replace("\\", "/")
                            layout_map_image_url = urljoin(url, slash_href)
                            break

                # 版面PDF链接。
                layout_pdf_url = ""
                if "layout_pdf_xpath" in self._paper \
                        and self._paper["layout_pdf_xpath"]:
                    layout_pdf_xpaths = self._paper["layout_pdf_xpath"]
                    for layout_pdf_xpath in layout_pdf_xpaths:
                        if not layout_pdf_xpath:
                            continue
                        layout_pdf_hrefs = tree.xpath(layout_pdf_xpath)
                        if layout_pdf_hrefs:
                            # 将链接中的反斜杠替换为正斜杠。
                            slash_href = layout_pdf_hrefs[0].replace("\\", "/")
                            layout_pdf_url = urljoin(url, slash_href)
                            break
                # 如果没找到版号，则取迭代的版次号。
                if layout_number is None:
                    layout_number = layout_seq
                # 结果集。
                row = dict()
                row["url"] = url
                row["platformID"] = self._platform_id
                row["platformName"] = self._platform_name
                row["layout_urls"] = layout_urls
                row["layoutSeq"] = layout_seq
                row["layoutNum"] = layout_number
                row["check_next_layout_url"] = check_next_layout_url
                row["layoutMapAreas"] = layout_areas
                row["detail_urls"] = detail_urls
                row["layoutTitle"] = layout_title
                row["mapImage"] = layout_map_image_url
                row["pdf"] = layout_pdf_url
                return row
            else:
                raise ValueError("Error response, {}, {}.".format(response.status_code, url))
        except Exception as e:
            self._logger.warning("Failed to layouts_info, '{}'.".format(e))

    def fetch_start(self):
        """
        获取版面信息。
        :return:
        """
        for start_url, pub_time in self._start_urls.items():
            # noinspection PyBroadException
            try:
                # 初始化版面序号。
                layout_seq = 1
                # 获取版面信息。
                layout_row = self.fetch_layout(start_url, layout_seq)
                layout_row["pubTime"] = int(pub_time * 1000)
                layout_urls = layout_row.pop("layout_urls")
                check_next_layout_url = layout_row.pop("check_next_layout_url")
                # start_url对应的页面相当于独立于循环之外采集。
                yield layout_row
                # 版面序号加一。
                layout_seq += 1
                # 判断有没有下一版链接。
                if layout_urls:
                    # 检查爬取方式为"遍历版面URL列表"还是"循环点击下一版按钮"。
                    if check_next_layout_url is False:
                        real_start_url = layout_row["url"]
                        try:
                            # 删除第一版链接。
                            layout_urls.remove(real_start_url)
                        except Exception:
                            self._logger.warning("Start url not existed in layout urls, {}.".format(real_start_url))

                        # 循环版面URL进行爬取。
                        for layout_url in layout_urls:
                            # noinspection PyBroadException
                            try:
                                layout_row = self.fetch_layout(layout_url, layout_seq)
                                layout_row.pop("layout_urls")
                                layout_row.pop("check_next_layout_url")
                                layout_row["pubTime"] = int(pub_time * 1000)
                                yield layout_row
                                layout_seq += 1
                            except Exception as e:
                                self._logger.warning("Failed to fetch layout, '{}'.".format(e))
                                layout_seq += 1
                                continue
                else:
                    raise ValueError("No layout urls found, {}.".format(start_url))
            except Exception as e:
                self._logger.warning("Failed to start crawler, '{}'.".format(e))

    def fetch_one(self):
        """
        获取批量数据。
        :return:
        """
        self._logger.info(f"{self._platform_name}开始采集")
        # 按start_url列表从新到旧迭代采集。
        for layout_row in self.fetch_start():
            try:
                # 每一个版面连带其详情作为一条基础数据。
                base_item = {
                    "code": 1,
                    "msg": "ok",
                    "epaperLayout": dict(),
                    "worksList": list(),
                }
                # 根据详情链接取得详情结果。
                detail_urls = layout_row.pop("detail_urls")
                # layoutMapAreas是版面与稿件的联系，是从map标签中解析出的内容。
                layout_areas = layout_row["layoutMapAreas"]
                layout_row["layoutMapAreas"] = list()

                # 计算出版面ID。
                layout_row["_id"] = md5_("{}{}{}{}".format(
                    self._platform_name, layout_row["url"], layout_row["pubTime"], layout_row["layoutSeq"])
                )
                # 获取版面号
                layout_num = layout_row.get("layoutSeq")
                for article_row in self.fetch_detail(detail_urls, layout_num):
                    # noinspection PyBroadException
                    try:
                        # 整合部分必要字段。
                        article_row["pubTime"] = layout_row["pubTime"]
                        # article_row["layoutSeq"] = layout_row["layoutSeq"]
                        # 计算出稿件ID。
                        article_id = md5_("{}{}{}{}".format(
                            self._platform_name, article_row["url"],
                            article_row["pubTime"], layout_row["layoutSeq"])
                        )
                        detail_url = article_row["url"]
                        # 详情链接与map标签中的链接一致时即可正确映射。
                        if detail_url in layout_areas:
                            area = layout_areas[detail_url]
                            layout_row["layoutMapAreas"].append(dict(
                                worksID=article_id,
                                href=article_row["url"],
                                shape=area["shape"],
                                coords=area["coords"],
                                title=article_row["title"]
                            ))
                        article_row["_id"] = article_id
                        article_row["epaperLayoutID"] = layout_row["_id"]
                        # 添加详情页结果。
                        base_item["worksList"].append(article_row)
                    except Exception as e:
                        self._logger.warning("'{}'.\n{}".format(e, traceback.format_exc()))
                        continue
                # 对结果集添加字段
                # 添加版面页结果。
                base_item["epaperLayout"] = layout_row
                # 计算map长度
                base_item["epaperLayout"]["layoutMapAreasLength"] = len(layout_row["layoutMapAreas"])
                # 头版头条
                if layout_num == 1:
                    target_date = datetime.datetime.now().strftime("%Y-%m-%d")
                    current_day = datetime.datetime.strptime(target_date, "%Y-%m-%d")
                    pub_time = int(current_day.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()) * 1000
                    if layout_row.get("pubTime") == pub_time:
                        layout_img = layout_row.get("mapImage", "")
                        pub_time = layout_row.get("pubTime", 0)
                        extend = json.dumps({"latestPaperTime": pub_time, "latestPaperFrontPageImage": layout_img})
                        _id = md5_(f"{self._platform_name}{5}")
                        platform = {"_id": _id, "extendData": extend}
                        # base_item["platform"] = platform
                        LayoutsCrawlerESUtils(self._logger).save_to_platform(platform)

                    elif layout_row.get("pubTime") == layout_row.get("pubTime"):
                        layout_img = layout_row.get("mapImage", "")
                        pub_time = layout_row.get("pubTime", 0)
                        extend = json.dumps({"latestPaperTime": pub_time, "latestPaperFrontPageImage": layout_img})
                        _id = md5_(f"{self._paper['platformName']}{5}")
                        platform = {"_id": _id, "extendData": extend}
                        LayoutsCrawlerESUtils(self._logger).save_to_platform(platform)
                else:
                    pass
                yield base_item
            except Exception as e:
                # self._logger.warning("'{}'.\n{}".format(e, traceback.format_exc()))
                print("'{}'.\n{}".format(e, traceback.format_exc()))
                continue

    def fetch_yield(self):
        """
        执行入口
        :return:
        """
        # 获取版面页信息
        for result in self.fetch_one():
            # yield result
            print(result)
            LayoutsCrawlerESUtils(self._logger).es_save_layout_and_works(result)
            self._logger.info(
                f"{self._platform_name}-<第{result['epaperLayout']['layoutSeq']}版>-作品：[{len(result['worksList'])}]>")


if __name__ == '__main__':
    log = LLog("Test", only_console=True, logger_level="DEBUG").logger
    # mysql_result = get_paper_template_from_mysql()
    print("=======================================start======================================")

    paper_templates = [
        # https://epaper.tibet3.com/qhrb/html/202101/22/node_1.html

        {'status': 1, 'name': '', 'describe': '',
         'value': '{"platformName": "青海日报", "sourceProvince": "青海", "sourceCity": "西宁", "sourceLevel": 2, "sourceClassify": 1, "sourceImportance": 1, "mainMedia": 1, "start_url": "https://epaper.tibet3.com/qhrb/html/%Y%m/%d/node_1.html", "cookiestr": "", "layout_url_xpath": ["//nav[@class=\'layout-nav\']/ul/li/a/@href"], "layout_next_xpath": [], "layout_title_xpath": ["//div[@class=\'epaper-meta\']/span/text()"], "layout_map_xpath": ["//map[@name=\'PagePicMap\']"], "layout_map_image_xpath": ["//img[@usemap=\'#PagePicMap\']/@src"], "layout_large_image_xpath": [], "layout_pdf_xpath": ["//div[@class=\'epaper-meta\']/a[1]/@href"], "detail_url_xpath": "[\\"//map[@name=\'PagePicMap\']/area/@href\\"]", "detail_pre_title_xpath": "[\\"//h2[@class=\'suptitle\']/text()\\"]", "detail_title_xpath": "[\\"//h1[@class=\'title\']/text()\\"]", "detail_sub_title_xpath": "[\\"//h2[@class=\'subtitle\']/text()\\"]", "detail_content_xpath": "[\\"//div[@class=\'article-entry\']\\"]", "detail_pubTime_xpath": "[]"}',
         'platformID': 'a90ec4d6c4f9fe15508545bf566f5e0d', 'platformName': '青海日报', 'platformType': 5, 'channelID': '',
         'channelName': '', 'accountID': '', 'accountName': '', 'topicID': '', 'topicTitle': '', 'worksID': '',
         'worksTitle': '', 'createTime': 1611036716350, 'updateTime': 1611036716350, 'types': ['5_1_26', '5_2_2'],
         '_id': 'eb3fa4639d178d8946c8660d89087c83'}

        # {
        #     "status": 1,
        #     "name": "",
        #     "describe": "",
        #     "value": """{"platformName": "\u4eba\u6c11\u65e5\u62a5", "sourceProvince": "\u5317\u4eac", "sourceCity": "", "sourceLevel": 1, "sourceClassify": 2, "sourceImportance": 1, "mainMedia": 1, "start_url": "http://paper.people.com.cn/rmrb/html/%Y-%m/%d/nbs.D110000renmrb_01.htm", "cookiestr": "", "layout_url_xpath": ["//a[@id='pageLink']/@href"], "layout_next_xpath": [], "layout_title_xpath": ["//div[@class='paper-bot']/p/text()"], "layout_map_xpath": ["//div[@class='paper']/map"], "layout_map_image_xpath": ["//div[@class='paper']/img/@src"], "layout_large_image_xpath": [], "layout_pdf_xpath": ["//p[@class='right btn']/a/@href"], "detail_url_xpath": ["//map[@name='PagePicMap']/area/@href"], "detail_pre_title_xpath": ["//div[@class='article']/h3/text()"], "detail_title_xpath": ["//div[@class='article']/h1/text()"], "detail_sub_title_xpath": ["//div[@class='article']/h2/text()"], "detail_author_xpath": ["//p[@class='sec']/text()"], "detail_content_xpath": ["//table[@class='pci_c']//td | //div[@id='ozoom']"], "detail_pubTime_xpath": []}""",
        #     "platformID": "e69e422edbb468f59d49134bbc791001",
        #     "platformName": "兰州日报",
        #     "platformType": 5,
        #     "channelID": "",
        #     "channelName": "",
        #     "accountID": "",
        #     "accountName": "",
        #     "topicID": "",
        #     "topicTitle": "",
        #     "worksID": "",
        #     "worksTitle": "",
        #     "types": [
        #         "5_2_1",
        #         "5_1_1"
        #     ],
        # },

        # {
        #     "status": 1,
        #     "name": "",
        #     "describe": "",
        #     "value": """{"platformName": "解放军报", "sourceProvince": "北京", "sourceCity": "", "sourceLevel": 1, "sourceClassify": 2, "sourceImportance": 1, "mainMedia": 1, "start_url": "http://www.81.cn/jfjbmap/content/%Y-%m/%d/node_2.htm", "cookiestr": "", "layout_url_xpath": ["//ul[@id='APP-SectionNav']/li/a/@href"], "layout_next_xpath": [], "layout_title_xpath": ["//div[@id='APP-SectionTitle']/text()"], "layout_map_xpath": ["//map[@name='pagepicmap']"], "layout_map_image_xpath": ["//img[@usemap='#pagepicmap']/@src"], "layout_large_image_xpath": [], "layout_pdf_xpath": ["//a[@id='APP-Pdf']/@href"], "detail_url_xpath": "[\"//map[@name='pagepicmap']/area/@href\"]", "detail_pre_title_xpath": "[\"//div[@class='article-header']/p[@id='APP-PreTitle']\"]", "detail_title_xpath": "[\"//div[@class='article-header']/h2[@id='APP-Title']\"]", "detail_sub_title_xpath": "[\"//div[@class='article-header']/p[@id='APP-Subtitle']\"]", "detail_content_xpath": "[\"//div[@class='attachment-image APP-Image'] | //div[@id='APP-Content']\"]", "detail_pubTime_xpath": "[]", "platformType": 6}""",
        #     "platformID": '755cf1623daca965f05bb8fd3f3102df',
        #     "platformName": "解放军报",
        #     "platformType": 5,
        #     "channelID": "",
        #     "channelName": "",
        #     "accountID": "",
        #     "accountName": "",
        #     "topicID": "",
        #     "topicTitle": "",
        #     "worksID": "",
        #     "worksTitle": "",
        #     "types": [
        #         "5_2_1",
        #         "5_1_1"
        #     ],
        # },
        # {
        #     "status": 1,
        #     "name": "",
        #     "describe": "",
        #     "value": """{"platformName": "重庆日报", "sourceProvince": "重庆", "sourceCity": "", "sourceLevel": 2, "sourceClassify": 1, "sourceImportance": 1, "mainMedia": 1, "start_url": "https://epaper.cqrb.cn/html/cqrb/%Y-%m/%d/001/node.htm", "cookiestr": "", "layout_url_xpath": ["//td[@class='default']/a[contains(@href, 'node.htm')]/@href"], "layout_next_xpath": [], "layout_title_xpath": ["//td[@class='px12' and @align='left']//text()"], "layout_map_xpath": ["//map[@name='PagePicMap']"], "layout_map_image_xpath": ["//img[@usemap='#PagePicMap']/@src"], "layout_large_image_xpath": [], "layout_pdf_xpath": ["//td[@class='px12']/a[contains(@href, '.pdf')]/@href"], "detail_url_xpath": "[\"//map[@name='PagePicMap']/area/@href\"]", "detail_pre_title_xpath": "[\"//span[contains(@style,'font-size:14px;')][1]/text()\"]", "detail_title_xpath": "[\"//strong[contains(@style,'font-size:23px')]/text()\"]", "detail_sub_title_xpath": "[\"//span[contains(@style,'font-size:14px;')][2]/text()\"]", "detail_content_xpath": "[\"//div[@id='ozoom']\"]", "detail_pubTime_xpath": "[]", "platformType": 6}""",
        #     "platformID": '1929fff981127abc57c01fbb6ca0b2bc',
        #     "platformName": "重庆日报",
        #     "platformType": 5,
        #     "channelID": "",
        #     "channelName": "",
        #     "accountID": "",
        #     "accountName": "",
        #     "topicID": "",
        #     "topicTitle": "",
        #     "worksID": "",
        #     "worksTitle": "",
        #     "types": [
        #         "5_2_2",
        #         "5_1_3"
        #     ],
        # },
        # {
        #     "status": 1,
        #     "name": "",
        #     "describe": "",
        #     "value": '{"platformName": "\\u6cb3\\u5317\\u65e5\\u62a5", "sourceProvince": "\\u6cb3\\u5317", "sourceCity": "", "sourceLevel": 2, "sourceClassify": 1, "sourceImportance": 0, "mainMedia": 1, "start_url": "http://hbrb.hebnews.cn/pc/paper/layout/%Y%m/%d/node_01.html", "cookiestr": "", "layout_url_xpath": ["//ul[@id=\'layoutlist\']/li/a/@href"], "layout_next_xpath": [], "layout_title_xpath": ["//div[@class=\'content clearfix\']/div[1]/text()"], "layout_map_xpath": ["//map[@name=\'PagePicMap\']"], "layout_map_image_xpath": ["//img[@usemap=\'#PagePicMap\']/@src"], "layout_large_image_xpath": [], "layout_pdf_xpath": ["//div[@class=\'content clearfix\']/div[1]/a[contains(@href, \'.pdf\')]/@href"], "detail_url_xpath": "[\\"//map[@name=\'PagePicMap\']/area/@href\\"]", "detail_pre_title_xpath": "[\\"//p[@id=\'PreTitle\']/text()\\"]", "detail_title_xpath": "[\\"//h2[@id=\'Title\']/text()\\"]", "detail_sub_title_xpath": "[\\"//p[@id=\'SubTitle\']/text()\\"]", "detail_content_xpath": "[\\"//div[@class=\'attachment\'] | //div[@id=\'ozoom\']//p\\"]", "detail_pubTime_xpath": "[]", "platformType": 6}',
        #     "platformID": "26d1a39d2007d2c38e52edbb5c91ab71",
        #     "platformName": "河北日报",
        #     "platformType": 5,
        #     "channelID": "",
        #     "channelName": "",
        #     "accountID": "",
        #     "accountName": "",
        #     "topicID": "",
        #     "topicTitle": "",
        #     "worksID": "",
        #     "worksTitle": "",
        #     "types": [
        #         "5_2_2",
        #         "5_1_5"
        #     ]
        # }
    ]
    # paper_templates = [DealWithTemplates().intergration_data_save_to_es()]

    target_dates = [datetime.datetime.now().strftime("%Y-%m-%d")]
    # 637报纸
    for paper_template in paper_templates:
        nw = NewspaperSpider(paper_template=paper_template, target_dates=target_dates, logger=log)
        nw.fetch_yield()
    print("=========================================end=========================================")
