#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
检查网站爬取情况。
2020年1月15日，更新，加入对content字段的提炼（去掉script等标签，链接改为绝对路径）。
2020年1月15日，更新，保留链接对应的文字。
2020年1月15日，更新，增加fields字段提取时的规则处理，如just_target参数。
2020年1月21日，更新，加入导航链接递归采集深度参数及逻辑。
# author: Trico
# date: 2020.1.9
# update: 2020.1.16
"""

import datetime
import re
import bs4
import html
import json
import time
import random
import requests
import functools
import traceback

from lxml import etree
from urllib.parse import urljoin

from api_common_utils.date_utils import str_to_timestamp, relative_str_to_timestamp
from api_common_utils.llog import LLog
from test.website.tld_extract_1 import get_primary_domain
from api_common_utils.proxy import get_abuyun_proxies


class WebsiteSpider(object):
    """
    网站爬虫。
    """

    def __init__(self, row, logger=None):
        """
        初始化。
        :param row: 网站的采集模板信息，来源于数据库中的条目。
        :param logger: 日志对象。
        """
        self._logger = logger
        # 需要转换的编码集合。
        self._convert_zh_charsets = {
            "gb2312": "gb18030",
            "gbk": "gb18030",
        }
        # 编码集。
        self._charsets = {"utf-8", "utf8", "gb2312", "gbk", "gb18030", "big5"}
        # 起始url
        self.start_url = ""
        # 验证参数。
        self._row = row
        assert self._row and isinstance(self._row, dict), "Error param, row."
        assert "id" in self._row, "Error param, row.id."
        assert "platformName" in self._row, "Error param, row.platformName."
        # 名称。
        self._platformName = self._row["platformName"]

        # 公共参数信息，如爬取间隔、是否使用代理、字符集、爬取深度等。
        self._params = json.loads(self._row["params"])

        # 默认字符集。
        if "charset" in self._params and self._params["charset"]:
            charset = self._params["charset"].strip().lower()
            if charset in self._charsets:
                self._default_charset = charset
            else:
                raise ValueError("Error param, unknown charset: '{}'.".format(charset))
        else:
            self._default_charset = None
        # 是否开启采集间隔时长。
        if "interval" in self._params and self._params["interval"]:
            interval = self._params["interval"]
            # 数值型的间隔时长。
            if isinstance(interval, (int, float)):
                # 转为float格式。
                interval = float(interval)
                assert 0 <= interval < 10, \
                    "Error param, interval: {}, value should be more than 0 and less than 10.".format(interval)
                self._interval = interval
            elif isinstance(interval, str):
                # 字符串型的间隔时长，转为float。
                interval = float(interval)
                assert 0 <= interval < 10, \
                    "Error param, interval: {}, value should be more than 0 and less than 10.".format(interval)
                self._interval = float(interval)
            elif isinstance(interval, (list, tuple)):
                # 数组类型的间隔时长。
                assert len(interval) >= 2, "Error param, interval: {}, length should be 2 at least.".format(interval)
                assert isinstance(interval[0], (int, float)) and isinstance(interval[1], (int, float)), \
                    "Error param, interval: {}, each cell should be int or float.".format(interval)
                assert 0 <= interval[0] <= interval[1] < 10, \
                    "Error param, interval: {}, each cell should be more than 0 and less than 10.".format(interval)
                self._interval = tuple(interval[:2])
            else:
                self._interval = None
        else:
            self._interval = None
        # 是否允许网址重定向。
        if "allowRedirects" in self._params:
            if self._params["allowRedirects"] in (1, "1") or self._params["allowRedirects"] is True:
                self._allow_redirects = True
            else:
                raise ValueError("Error param, allowRedirects: {}.".format(self._params["allowRedirects"]))
        else:
            self._allow_redirects = False
        # 从导航页获取导航链接的递归深度，更多的导航链接意味着更多的稿件链接。
        if "depth" in self._params:
            min_depth = 0
            max_depth = 4
            depth = int(self._params["depth"])
            if min_depth <= depth <= max_depth:
                self._depth = depth
            else:
                raise ValueError("Error param, depth: {}, which should be more than {} and less than {}.".format(
                    depth, min_depth, max_depth
                ))
        else:
            # 1代表起始页。
            self._depth = 1

        # 模板信息。
        self._templates = json.loads(self._row["templates"])
        assert self._templates and isinstance(self._templates, list), "Error param, row.templates."

        # 正则模式。
        # 清空标题、版题里的换行符。
        self._line_feed_pattern = re.compile(r"[\r\n]")

        # 获取会话。
        self._session = requests.Session()

        # 请求头。
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/74.0.3729.169 Safari/537.36",
        }
        self._session.headers.update(self._headers)
        # 开启代理
        self._session.proxies = get_abuyun_proxies()
        # Cookies。
        self._cookies = dict()
        # 超时时间。
        self._timeout = 10
        self._api_timeout = 3600

        # 通用a标签xpath定位。
        self._a_tags_xpath = "//a[@href and not(starts-with(@href, 'javascript:') and not(@href='#'))]"

        # 导航链接队列。
        self.pending_navi_links = list()
        # 已存在的导航链接。
        self.exist_navi_links = dict()

        # 稿件链接集合。
        self.exist_doc_links = set()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        """
        停止相关服务。
        :return:
        """

        # noinspection PyBroadException
        try:
            self._session.close()
        except Exception:
            pass

    def __del__(self):
        self.__exit__()

    def get_charset(self, response):
        """
        获取response编码。
        :return:
        """

        # 参数验证。
        if not response or not isinstance(response, requests.Response):
            raise ValueError("The 'response' is not a type of 'requests.Response'.")

        # 如果存在自定义编码，则直接使用它。
        if self._default_charset:
            return self._default_charset

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

    def fetch_page_source_by_session(self, url):
        """
        通过session获取页面内容。
        :return:
        """

        # 检查是否需要等待，即设置采集间隔。
        if self._interval is not None:
            if isinstance(self._interval, (float, int)):
                # 休息指定的时长。
                time.sleep(self._interval)
            elif isinstance(self._interval, (tuple, list)):
                # 休息范围内的随机时长。
                time.sleep(random.uniform(self._interval[0], self._interval[1]))
            else:
                pass

        # 请求页面。
        response = self._session.get(
            url,
            headers=self._headers,
            cookies=self._cookies,
            timeout=self._timeout,
            allow_redirects=self._allow_redirects,
        )
        if response.status_code == requests.codes.ok:
            # 重置cookies。
            self._cookies = response.cookies.get_dict()
            # 判定字符集。
            charset = self.get_charset(response)
            response.encoding = charset
            return response.text, response.url
        else:
            raise ValueError("Failed to fetch page source, {}, '{}'.".format(url, response.status_code))

    def fetch_page_source(self, url):
        """
        获取页面内容。
        :return:
        """

        return self.fetch_page_source_by_session(url)

    @staticmethod
    def extract_content(url, content):
        """
        清洗content字段，去除首尾空白、删除script/style标签、删除注释标签、链接转为绝对路径等。
        :return:
        """

        # 参数验证。
        assert url and isinstance(url, str), "Error param, url."
        assert content and isinstance(content, str), "Error param, content."

        # 转换两遍是为了避免"&amp;"符号（&）。
        content = html.unescape(content)
        content = html.unescape(content)

        # 清洗正文。
        content_soup = bs4.BeautifulSoup(content, "html.parser")
        # 删除script、style标签
        for tag in content_soup(("script", "style")):
            tag.extract()
        # 删除注释。
        for tag in content_soup(text=lambda text: isinstance(text, bs4.Comment)):
            tag.extract()
        # 将content中的href、src更换成绝对路径。
        for tag in content_soup(["img", "video", "audio", "source"]):
            if "src" in tag.attrs and tag.attrs["src"]:
                # 将链接中的反斜杠替换为正斜杠。
                slash_src = tag.attrs["src"].replace("\\", "/")
                tag.attrs["src"] = urljoin(url, slash_src)
        for tag in content_soup('a'):
            if "href" in tag.attrs and tag.attrs["href"]:
                # 将链接中的反斜杠替换为正斜杠。
                slash_href = tag.attrs["href"].replace("\\", "/")
                tag.attrs["href"] = urljoin(url, slash_href)
        # 去除首尾空白。
        content = str(content_soup).strip()

        # 返回结果。
        return content

    @staticmethod
    def parse_doc_rules(tree, rules, default=None, all_groups=False):
        """
        解析详情的规则，从中提取内容。
        :return:
        """

        # 参数验证。
        assert len(tree) > 0, "Error param, tree."
        assert rules, "Error param, rules."

        # 遍历解析规则。
        for rule in rules:
            item = default
            if rule:
                if "xpath" in rule and rule["xpath"]:
                    item_list = tree.xpath(rule["xpath"])
                    if item_list:
                        new_item_list = list()
                        for sub_item in item_list:
                            # noinspection PyBroadException
                            try:
                                sub_item = etree.tostring(sub_item, encoding="unicode").strip()
                            except Exception:
                                sub_item = str(sub_item).strip()
                            new_item_list.append(sub_item)
                        item = "".join(new_item_list).strip()
                        # 转换两遍是为了避免"&amp;"符号（&）。
                        item = html.unescape(item)
                        item = html.unescape(item)
                # 检查正则。
                if "regex" in rule and rule["regex"]:
                    if item:
                        match_obj = re.search(rule["regex"], item)
                        if match_obj:
                            # 目标内容。
                            groups = match_obj.groups()
                            if groups:
                                # 检查是否需要返回全部匹配结果。
                                if all_groups is True:
                                    groups = filter(lambda x: x, groups)
                                    groups = map(lambda x: x.strip(), groups)
                                    item = list(filter(lambda x: x, groups))
                                else:
                                    item = groups[0].strip()
                                # 正则解析后的结果。
                                if item:
                                    yield item, rule
                else:
                    # 未配置正则时取定位结果。
                    if item:
                        yield item, rule

        # 无数据时返回默认值。
        yield default, dict()

    def parse_doc_page(self, doc_link, template):
        """
        解析页面内容，提取标题、正文、发布时间等数据。
        :return:
        """

        # 参数验证。
        assert doc_link and isinstance(doc_link, str), "Error param, doc_link."
        assert template and isinstance(template, dict), "Error param, template."
        # 详情采集规则。
        template_fields = template["fields"]
        assert template_fields["title"], "Error param, template.fields.title."
        assert template_fields["content"], "Error param, template.fields.title."

        # 下载详情内容。
        page_source, url = self.fetch_page_source(doc_link)
        if not page_source:
            raise ValueError("Error empty page_source, {}.".format(doc_link))
        else:
            tree = etree.HTML(page_source)

        # 结果体。
        fields = dict(
            url=url,
        )

        # 解析标题。
        title, rule = next(self.parse_doc_rules(tree, template_fields["title"], default=""))
        # 替换掉换行符。
        title = re.sub(self._line_feed_pattern, "", title)
        # 验证必须满足的字段。
        assert title, "Error, title is empty, {}.".format(doc_link)

        # 解析正文。
        content, rule = next(self.parse_doc_rules(tree, template_fields["content"], default=""))
        if content:
            content = self.extract_content(doc_link, content)
        # 验证必须满足的字段。
        assert content, "Error, content is empty, {}.".format(doc_link)

        # 解析来源。
        pub_source = ""
        if "pubSource" in template_fields and template_fields["pubSource"]:
            pub_source, rule = next(self.parse_doc_rules(tree, template_fields["pubSource"], default=""))
            # 替换掉换行符。
            pub_source = re.sub(self._line_feed_pattern, "", pub_source)

        # 解析时间。
        pub_time = None
        if "pubTime" in template_fields and template_fields["pubTime"]:
            for pub_time_str, rule in self.parse_doc_rules(tree, template_fields["pubTime"], default=None):
                if pub_time_str:
                    if "just_target" in rule and (rule["just_target"] in (1, "1") or rule["just_target"] is True):
                        pub_time = int(pub_time_str.strip())
                        break
                    else:
                        # 替换掉换行符。
                        pub_time_str = re.sub(self._line_feed_pattern, "", pub_time_str)
                        # 将发布时间字符串转换为时间戳。
                        temp_pub_time = str_to_timestamp(pub_time_str)
                        if temp_pub_time:
                            pub_time = temp_pub_time
                            break
                        else:
                            # 将相对时间字符串转为时间戳，如"昨天"、"1小时前"。
                            temp_pub_time = relative_str_to_timestamp(pub_time_str)
                            if temp_pub_time:
                                pub_time = temp_pub_time
                                break

        # 解析频道。
        channel = ""
        if "channel" in template_fields and template_fields["channel"]:
            channel, rule = next(self.parse_doc_rules(tree, template_fields["channel"], default=""))
            # 替换掉换行符。
            channel = re.sub(self._line_feed_pattern, "", channel)

        # 解析作者。
        authors = list()
        if "authors" in template_fields and template_fields["authors"]:
            authors, rule = next(
                self.parse_doc_rules(tree, template_fields["authors"], default=list(), all_groups=True)
            )
            if isinstance(authors, (list, tuple)):
                # 替换掉换行符。
                authors = list(map(lambda x: re.sub(r"\s", "", x), authors))
            elif isinstance(authors, str):
                authors = [re.sub(r"\s", "", authors), ]
            else:
                authors = list()

        # 解析摘要。
        summary = ""
        if "summary" in template_fields and template_fields["summary"]:
            summary, rule = next(self.parse_doc_rules(tree, template_fields["summary"], default=""))
            # 替换掉换行符。
            summary = re.sub(self._line_feed_pattern, "", summary)

        # 整理结果集并返回。
        fields["title"] = title
        fields["content"] = content
        fields["pubSource"] = pub_source
        fields["pubTime"] = pub_time
        fields["channel"] = channel
        fields["authors"] = authors
        fields["summary"] = summary
        return fields

    def parse_navi_page(self, template, primary_domain, url, page_source, current_depth):
        """
        解析导航页内容，获取链接数据。
        :return:
        """

        # 找出所有a标签里的链接。
        tree = etree.HTML(page_source)
        a_tags = tree.xpath(self._a_tags_xpath)
        if a_tags:
            # 整理链接。
            links = list()
            for a_tag in a_tags:
                # noinspection PyBroadException
                try:
                    # 获取链接。
                    href = a_tag.get("href")
                    if href:
                        # 去除链接首尾空白。
                        href = href.strip()
                        # 过滤明显不需要的链接。
                        if href and href not in ("/", "#") and not href.startswith("javascript:"):
                            if "#" in href:
                                # 去掉锚点。
                                href = href.split("#")[0]
                            if href:
                                # 将反斜杠更换为正斜杠。
                                if "\\" in href:
                                    href = href.replace("\\", "/")
                                # 将链接里的反斜杠替换为正斜杠。
                                link = urljoin(url, href.replace("\\", "/")).strip()
                                # 外域的link不做处理。
                                current_primary_domain = get_primary_domain(link)
                                if current_primary_domain == primary_domain:
                                    # 新增链接及其文本内容。
                                    link_text = str(a_tag.xpath("string()")).strip()
                                    if not link_text:
                                        link_text = str("".join(a_tag.xpath("@title"))).strip()
                                    links.append((link, link_text))
                                else:
                                    # 备注外域链接。
                                    self._logger.debug("Cross domain link: {}.".format(link))
                                    continue
                except Exception as e:
                    self._logger.debug(str(e))

            # 整理导航链接和稿件链接的正则参数。
            # noinspection PyBroadException
            try:
                doc_link_ignore_patterns = template["doc_links"]["regex"]["ignore"]
                assert doc_link_ignore_patterns and isinstance(doc_link_ignore_patterns, list)
            except Exception:
                doc_link_ignore_patterns = list()
            # noinspection PyBroadException
            try:
                doc_link_target_patterns = template["doc_links"]["regex"]["target"]
                assert doc_link_target_patterns and isinstance(doc_link_target_patterns, list)
            except Exception:
                doc_link_target_patterns = list()

            # 判断是否需要采集导航链接，递归深度未超过最大时采集导航链接。
            if current_depth <= self._depth:
                # 整理导航链接的参数。
                # noinspection PyBroadException
                try:
                    navi_link_ignore_patterns = template["navi_links"]["regex"]["ignore"]
                    assert navi_link_ignore_patterns and isinstance(navi_link_ignore_patterns, list)
                except Exception:
                    navi_link_ignore_patterns = list()
                # noinspection PyBroadException
                try:
                    navi_link_target_patterns = template["navi_links"]["regex"]["target"]
                    assert navi_link_target_patterns and isinstance(navi_link_target_patterns, list)
                except Exception:
                    navi_link_target_patterns = list()

                # 遍历每一条链接，将合适的导航链接或稿件链接加入到对应的集合中。
                for link, link_text in links:
                    # 获取导航链接。
                    navi_ignore_flag = False
                    for navi_link_ignore_pattern in navi_link_ignore_patterns:
                        match = re.match(navi_link_ignore_pattern, link)
                        if match is not None:
                            navi_ignore_flag = True
                            break
                    if navi_ignore_flag is False:
                        for navi_link_target_pattern in navi_link_target_patterns:
                            match = re.match(navi_link_target_pattern, link)
                            if match is not None:
                                if link not in self.exist_navi_links:
                                    # 当前导航链接深度加一。
                                    self.pending_navi_links.append((link, link_text, current_depth + 1))
                                    self.exist_navi_links[link] = link_text
                                else:
                                    # noinspection PyBroadException
                                    try:
                                        # 将有文本内容的导航链接替换掉已存在的导航链接中的文本。
                                        if link_text and not self.exist_navi_links[link]:
                                            self.exist_navi_links[link] = link_text
                                    except Exception as e:
                                        self._logger.debug(str(e))
                                break

                    # 获取稿件链接。
                    doc_ignore_flag = False
                    for doc_link_ignore_pattern in doc_link_ignore_patterns:
                        match = re.match(doc_link_ignore_pattern, link)
                        if match is not None:
                            doc_ignore_flag = True
                            break
                    if doc_ignore_flag is False:
                        for doc_link_target_pattern in doc_link_target_patterns:
                            match = re.match(doc_link_target_pattern, link)
                            if match is not None:
                                if link not in self.exist_doc_links:
                                    self.exist_doc_links.add(link)
                                    yield link
                                break
            else:
                # 已超过递归深度时，不再采集导航链接，只采集稿件链接。
                # 遍历每一条链接，只采集稿件链接。
                for link, link_text in links:
                    # 获取稿件链接。
                    doc_ignore_flag = False
                    for doc_link_ignore_pattern in doc_link_ignore_patterns:
                        match = re.match(doc_link_ignore_pattern, link)
                        if match is not None:
                            doc_ignore_flag = True
                            break
                    if doc_ignore_flag is False:
                        for doc_link_target_pattern in doc_link_target_patterns:
                            match = re.match(doc_link_target_pattern, link)
                            if match is not None:
                                if link not in self.exist_doc_links:
                                    self.exist_doc_links.add(link)
                                    yield link
                                break
        # 无数据时，返回None。
        yield None

    def fetch_links(self, batch_size=5):
        """
        分批次采集数据。
        :return:
        """

        # 详情链接。
        doc_links = list()

        # 遍历所有的采集模版。
        for template in self._templates:
            # 标记开始。
            self._logger.info("Template started, start_url: {}.".format(template["start_url"]))

            # 导航链接计数。
            count = 0

            # noinspection PyBroadException
            try:
                # 获取主域名。
                primary_domain = get_primary_domain(template["start_url"])
                # 导航链接采集队列。
                if "start_url_name" in template and template["start_url_name"]:
                    self.pending_navi_links = [(template["start_url"], template["start_url_name"], 1), ]
                    self.exist_navi_links[template["start_url"]] = template["start_url_name"]
                else:
                    self.pending_navi_links = [(template["start_url"], "", 1), ]
                    self.exist_navi_links[template["start_url"]] = ""
                # 将起始页加入已存在稿件链接中。
                self.exist_doc_links.add(template["start_url"])
                # 用偏函数包装一下。
                parse_navi_page_by_template = functools.partial(
                    self.parse_navi_page, template, primary_domain
                )
                # 循环处理导航列表。
                while True:
                    # 导航链接队列为空时结束循环。
                    if not self.pending_navi_links:
                        break

                    # 首位出列，导航链接计数加一。
                    link, link_text, current_depth = self.pending_navi_links.pop(0)
                    count += 1

                    # 标记导航页解析开始。
                    self._logger.debug("Navi link started: {}({}).".format(link, link_text))
                    temp_doc_links_count = len(self.exist_doc_links)

                    # noinspection PyBroadException
                    try:
                        # 下载页面。
                        page_source, real_url = self.fetch_page_source(link)
                    except Exception as e:
                        self._logger.warning(str(e))
                        continue

                    # 深度未达到时，递归采集导航链接。
                    for doc_link in parse_navi_page_by_template(real_url, page_source, current_depth):
                        if doc_link:
                            doc_links.append(doc_link)
                            # 返回当前模板下的详情链接。
                            if len(doc_links) >= batch_size:
                                yield doc_links, template
                                doc_links = list()

                    # 标记导航页解析结束。
                    self._logger.info("Navi link finished: {}({}), new doc links: {}.".format(
                        link, link_text, len(self.exist_doc_links) - temp_doc_links_count)
                    )

                # 返回数量不足batch_size的数据。
                yield doc_links, template
                doc_links = list()
            except Exception as e:
                self._logger.warning("Failed to fetch data, {}, '{}'.".format(self._platformName, e))
                # 返回数量不足batch_size的数据。
                yield doc_links, template
                doc_links = list()

        # 检查采集情况。
        if not self.exist_doc_links:
            raise ValueError("No doc links found.")

    def fetch_batch(self, batch_size=5, check_mode=False):
        """
        获取链接。
        :return:
        """

        # 参数验证。
        assert batch_size and isinstance(batch_size, int) and batch_size > 0, "Error param, batch_size."

        # 批数据。
        doc_batch = list()
        # 总数、成功数和失败数。
        seq = total_count = succ_count = fail_count = 0

        # 标记开始。
        self._logger.info("{} started.".format(self._platformName))

        # 遍历详情页链接，采集稿件内容。
        for i, (doc_links, template) in enumerate(self.fetch_links(batch_size=batch_size), start=1):
            # noinspection PyBroadException
            try:
                if doc_links:
                    # 当前模板下的详情链接数。
                    current_total_count = len(doc_links)
                    # 初始化成功和失败数。
                    current_succ_count = current_fail_count = 0

                    for j, doc_link in enumerate(doc_links, start=1):
                        # 序号。
                        seq += 1
                        # noinspection PyBroadException
                        try:
                            # 检查是否已满足batch_size。
                            if len(doc_batch) >= batch_size:
                                yield doc_batch
                                doc_batch = list()
                            # 从详情页中提取稿件数据。
                            data = self.parse_doc_page(doc_link, template)
                            if data:
                                # 成功数加一。
                                current_succ_count += 1
                                doc_batch.append(data)
                                self._logger.info("{}/{}, {}, {} ok.".format(j, current_total_count, seq, doc_link))
                            else:
                                raise ValueError("Empty data.")
                        except Exception as e:
                            if check_mode is True:
                                # 如果是检测模式，则每条失败的结果也需要返回。
                                doc_batch.append(dict(code=0, msg=str(e)))
                            current_fail_count += 1
                            self._logger.info("{}/{}, {}, failed to parse, '{}'.".format(
                                j, current_total_count, seq, e)
                            )
                            self._logger.debug("{}/{}, {}, failed to parse, '{}'.\n{}".format(
                                j, current_total_count, seq, e, traceback.format_exc())
                            )
                            continue

                    # 打印成功和失败数。
                    self._logger.info("Batch finished, {} total, {} ok, {} fail, {}.".format(
                        current_total_count, current_succ_count, current_fail_count, template["start_url"])
                    )

                    # 统计总数。
                    succ_count += current_succ_count
                    fail_count += current_fail_count
                    total_count += current_total_count

                    # 返回当前模板的剩余结果。
                    if doc_batch:
                        yield doc_batch
                        doc_batch = list()
                else:
                    continue
            except Exception as e:
                self._logger.warning("{} {}.\n{}".format(i, e, traceback.format_exc()))
                continue

        # 记录总数。
        self._logger.info("All finished, {}, {} total, {} ok, {} fail.".format(
            self._platformName, total_count, succ_count, fail_count)
        )

    def collect_links(self):
        """
        收集链接信息，导航链接、稿件链接。
        :return:
        """

        # 遍历详情页链接，产生已存在导航链接和稿件链接。
        for _, _ in self.fetch_links():
            pass

        # 结果集。
        return dict(
            platformName=self._platformName,
            navi_links_num=len(self.exist_navi_links),
            navi_links=self.exist_navi_links,
            doc_links_num=len(self.exist_doc_links),
            doc_links=list(self.exist_doc_links),
        )

    def fetch(self):
        """
        执行入口。
        :return:
        """

        # noinspection PyBroadException
        try:
            return self.fetch_batch()
        except Exception as e:
            self._logger.error("'{}'.\n{}".format(e, traceback.format_exc()))


if __name__ == '__main__':
    # 遍历结果集。
    log = LLog("Test", log_path=None, only_console=False, logger_level="DEBUG").logger

    template = {'id': 5, 'platformName': '华商网', 'platformType': 5, 'logo': '', 'sourceProvince': '陕西省', 'sourceCity': '西安市', 'sourceCounty': '', 'sourceLevel': 2, 'sourceClassify': 1, 'sourceImportance': 1, 'mainMedia': 1, 'categoryFirst': '', 'categorySecond': '', 'categoryThird': '', 'rankCoefficient': 1.0, 'status': 0, 'spiderType': 1, 'params': '{}', 'templates': '[{"start_url":"http://www.hsw.cn/","navi_links":{"regex":{"ignore":["http://hsb.hsw.cn","http://biz.hsw.cn"],"target":["http://[a-z]+.hsw.cn/"]}},"doc_links":{"regex":{"ignore":[],"target":["https?://[a-z]+.dbw.cn/system/\\\\d{4}/\\\\d{2}/\\\\d{2}/\\\\d+.shtml"]}},"fields":{"title":[{"xpath":"//h1/text()"}],"content":[{"xpath":"//div[@class=\'bd\']"}],"pubSource":[{"describe":"http://news.hsw.cn/system/2020/0113/1146502.shtml","xpath":"//span[@class=\'ly-name\']/a/text()"}],"pubTime":[{"xpath":"//span[@class=\'article-time\']/text()"}],"channel":[{"xpath":"//div[@class=\'Crumbs-Article\']/span/a[last()]/text()"}]}}]', 'createTime': datetime.datetime(2020, 1, 13, 18, 58, 16, 789602), 'updateTime': datetime.datetime(2020, 1, 13, 19, 1, 12, 658161)}

    ws_obj = WebsiteSpider(template, logger=log)
    for batch in ws_obj.fetch_batch(batch_size=5, check_mode=True):
        print(dict(msg="OK", code=1, naviLinks=ws_obj.exist_navi_links, docList=batch,))