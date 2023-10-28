# -*- coding:utf-8 -*-
"""
# project:
# author: Neil
# date: 2020/12/15
# update: 2020/12/15
"""
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
from api_common_utils.date_utils import str_to_timestamp, relative_str_to_timestamp
from api_common_utils.llog import LLog
from api_common_utils.proxy import get_abuyun_proxies
from lib.test.epaper_test.extract_digest import GetExtractDigest
from lib.test.epaper_test.save_to_ES import LayoutsCrawlerESUtils


def md5(unicode_str, charset="UTF-8"):
    """
    字符串转md5格式。
    :return:
    """
    _md5 = hashlib.md5()
    _md5.update(unicode_str.encode(charset))
    return _md5.hexdigest()


class WebSpider(object):

    def __init__(self, paper_template, logger=None):
        """
        初始化
        :param paper_template: 网站的xpath模板信息，来源于数据库中的条目。
        :param logger:
        """
        self._platform_type = 3
        # self._platform_id = paper_template["platformID"]
        self._platform_id = " "
        # assert self._platform_id and isinstance(self._platform_id, str), "Error param, _platform_id."
        # 该平台所属是父级ID
        # self._parents_id = paper_template["types"]
        self._parents_id = ["1-2-3"]
        assert self._parents_id and isinstance(self._parents_id, list), "Error param, _parents_id."
        self._logger = logger
        # epaper_template = eval(paper_template["value"])
        # self._paper = epaper_template
        self._paper = paper_template
        assert self._paper and isinstance(self._paper, dict), "Error param, paper_template."
        assert "platformName" in self._paper, "Error param, paper_template.platformName."
        assert "start_url" in self._paper, "Error param, paper_template.start_url."
        # 网站名称
        self._platform_name = self._paper["platformName"]
        # 起始地址
        self._start_url = self._paper["start_url"]
        assert self._start_url and isinstance(self._start_url, str), "Param start_url error."
        # 首页头条新闻
        self._headline_news = self._paper["headline_news"]
        # 首页轮播新闻
        self._banner_news = self._paper["banner_news"]
        # 轮播旁边新闻
        self._banner_news_side = self._paper["banner_news_side"]
        # 频道信息
        self._channel_info_xpaths = list()
        # 频道链接提取方式(可以直接定位到频道列表，方便下面直接提取连接和频道名称)。
        if "channel_info_xpath" in self._paper:
            if self._paper["channel_info_xpath"]:
                self._channel_info_xpaths = self._paper["channel_info_xpath"]
            else:
                raise ValueError("Param channel_info_xpaths error.")
        else:
            raise ValueError("Param channel_info_xpaths error.")
        # 获取cookie
        if "cookie" in self._paper and self._paper["cookie"]:
            cookie = self._paper["cookie"]
        else:
            cookie = ""
        # 获取会话。
        self._session = requests.Session()
        # 请求头。
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/87.0.4280.88 Safari/537.36",
            "Cookie": cookie
        }
        self._session.headers.update(self._headers)
        # 开启代理
        self._session.proxies = get_abuyun_proxies()
        # 通用a标签xpath定位。
        self._a_tags_xpath = "//a[@href and not(starts-with(@href, 'javascript:') and not(@href='#'))]"
        # 清空标题、版题里的换行符。
        self._line_feed_pattern = re.compile(r"[\r\n]")
        # 提取数字。
        self._href_xpath_pattern = re.compile(r"/@href$")
        # 超时时间。
        self._timeout = 15
        # 默认编码集。
        self._default_charset = None
        # 需要转换的编码集合。
        self._convert_zh_charsets = {
            "gb2312": "gb18030",
            "gbk": "gb18030",
        }
        # 编码集。
        self._charsets = {"utf-8", "utf8", "gb2312", "gbk", "gb18030", "big5"}

    def _get_charset(self, response):
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
                        item = "".join(new_item_list).strip().replace("\n", "").replace("\t", "").replace("\r", "")
                        # 转换两遍是为了避免"&amp;"符号（&）。
                        item = html.unescape(item)
                        item = html.unescape(item)
                        item = unicodedata.normalize('NFKC', item)
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

    def fetch_page_source_by_session(self, url):
        """
        通过session获取页面内容。
        :return:
        """
        # 请求页面。
        time.sleep(random.random() / 10 + 1.2)
        response = self._session.get(
            url,
            headers=self._headers,
            timeout=self._timeout,
        )
        if response.status_code == requests.codes.ok:
            # 判定字符集。
            charset = self._get_charset(response)
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

    def parse_detail_url(self, url):
        """
        解析频道页内容，获取稿件数据。
        :param url: 导航url
        :return: 每个频道详情页url连接
        """
        # 稿件链接集合。
        exist_doc_links = list()
        try:
            response, real_url = self.fetch_page_source(url)
            url = real_url
            # noinspection PyBroadException
            # 解析成树。
            tree = etree.HTML(response)
            a_tags = tree.xpath(self._a_tags_xpath)
            if a_tags:
                # 整理链接。
                links = set()
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
                                    links.add(link)
                                else:
                                    continue
                    except Exception as e:
                        self._logger.debug(str(e))

                # 整理稿件链接的正则参数。
                try:
                    doc_link_target_patterns = self._paper["doc_links"]
                    assert doc_link_target_patterns and isinstance(doc_link_target_patterns, list)
                except Exception:
                    doc_link_target_patterns = list()

                # 遍历每一条链接，将合适的导航链接或稿件链接加入到对应的集合中。
                for link in links:
                    # 获取稿件链接。
                    for doc_link_target_pattern in doc_link_target_patterns:
                        match = re.match(doc_link_target_pattern, link)
                        if match:
                            exist_doc_links.append(link)
            return exist_doc_links
        except Exception as e:
            self._logger.debug(str(e))

    def parse_doc_page(self, doc_link, channel_name):
        """
        解析页面内容，提取标题、正文、发布时间等数据。
        :return:
        """
        # 参数验证。
        assert doc_link and isinstance(doc_link, str), "Error param, doc_link."
        # 详情采集规则。
        template_fields = self._paper["fields"]
        assert template_fields["title"], "Error param, template.fields.title."
        assert template_fields["content"], "Error param, template.fields.title."
        # 结果体。
        fields = dict()
        # 下载详情内容。
        url = doc_link
        time.sleep(random.random() / 10 + 0.2)
        response = self._session.get(doc_link, timeout=self._timeout)
        if response.status_code == requests.codes.ok:
            # 得到真实的URL地址。
            url = response.url
            # noinspection PyBroadException
            # 解析成树。
            try:
                response.encoding = self._get_charset(response)
            except Exception as e:
                raise ValueError("Failed to encoding {}, '{}'.".format(url, e))
        if not response.text:
            raise ValueError("Error empty page_source, {}.".format(doc_link))
        else:
            tree = etree.HTML(response.text)
        _html = response.text.replace("   ", '').replace("\n", "").replace("\r", "").replace("\t", "")
        # 解析标题不能为空
        title, rule = next(self.parse_doc_rules(tree, template_fields["title"], default=""))
        # 替换掉换行符。
        # title = re.sub(self._line_feed_pattern, "", title)
        # 验证必须满足的字段。
        assert title, "Error, title is empty, {}.".format(url)

        # 解析正文。不能为空
        content, rule = next(self.parse_doc_rules(tree, template_fields["content"], default=""))
        if content:
            content = self.extract_content(doc_link, content)

        # 验证必须满足的字段。
        assert content, "Error, content is empty, {}.".format(url)

        # 解析来源。
        pub_source = ""
        if "pubSource" in template_fields and template_fields["pubSource"]:
            pub_source, rule = next(self.parse_doc_rules(tree, template_fields["pubSource"], default=""))
            # 替换掉换行符。
            pub_source = re.sub(self._line_feed_pattern, "", pub_source)
        # 通过判断来源 检查是否原创
        if self._platform_name in pub_source:
            fields["isOriginal"] = 1
        else:
            fields["isOriginal"] = 0

        # 解析时间。
        pub_time = None
        if "pubTime" in template_fields and template_fields["pubTime"]:
            for pub_time_str, rule in self.parse_doc_rules(tree, template_fields["pubTime"], default=None):
                if pub_time_str:
                    if "just_target" in rule and (rule["just_target"] in (1, "1") or rule["just_target"] is True):
                        pub_time = int(pub_time_str.strip() * 1000)
                        break
                    else:
                        # 替换掉换行符。
                        pub_time_str = re.sub(self._line_feed_pattern, "", pub_time_str)
                        # 将发布时间字符串转换为时间戳。
                        temp_pub_time = str_to_timestamp(pub_time_str)
                        if temp_pub_time:
                            pub_time = temp_pub_time * 1000
                            break
                        else:
                            # 将相对时间字符串转为时间戳，如"昨天"、"1小时前"。
                            temp_pub_time = relative_str_to_timestamp(pub_time_str)
                            if temp_pub_time:
                                pub_time = temp_pub_time * 1000
                                break

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
        # digest
        digest, content_num = GetExtractDigest().extract(content)

        # 判断文章类型，通过正文中是否含有图片，视频，或者音频来判断文章类型
        # 判断文章类型如果含有图片将图片链接提取出来
        images = list()
        video_urls = list()
        poster_url = ""
        if "<video" in content:
            fields["contentType"] = 3
            content_tree = etree.HTML(content)
            video_list = content_tree.xpath(".//video/@src")
            for video in video_list:
                if video:
                    video_url = urljoin(url, video)
                    video_urls.append(video_url)
                else:
                    continue
            # 视频封面图
            video_poster = content_tree.xpath(".//video/@poster")
            for poster in video_poster:
                if poster:
                    poster_url = urljoin(url, poster)
                else:
                    continue

        elif "<img" in content:
            fields["contentType"] = 2
            content_tree = etree.HTML(content)
            img_list = content_tree.xpath(".//img/@src")
            for img in img_list:
                if img:
                    img_url = urljoin(url, img)
                    images.append(img_url)
                else:
                    continue

        elif "<image" in content:
            fields["contentType"] = 2
            content_tree = etree.HTML(content)
            img_list = content_tree.xpath(".//image/@src")
            for img in img_list:
                if img:
                    img_url = urljoin(url, img)
                    images.append(img_url)
                else:
                    continue
        else:
            fields["contentType"] = 1
        # 封面图
        covers = list()
        if images:
            covers.append(images[0])
        else:
            covers = list()
        # 视频封面图
        if video_urls:
            covers.append(poster_url)
        else:
            pass

        # 整理结果集并返回
        # 结果体。
        fields["status"] = 1
        fields["platformWorksID"] = md5(f"{channel_name}{doc_link}{title}")  # 频道名字,详情链接,文章题目
        fields["platformID"] = self._platform_id
        fields["_id"] = md5(f'{fields["platformID"]}{fields["platformWorksID"]}')
        fields["platformName"] = self._paper["platformName"]
        fields["platformType"] = 3
        fields["channelID"] = ""
        fields["channelName"] = ""
        fields["url"] = url
        # fields["html"] = _html
        fields["title"] = title
        fields["titleWordsNum"] = len(title)
        fields["digest"] = digest
        fields["digestOriginal"] = summary
        fields["digestCompute"] = ""
        fields["content"] = content
        fields["contentWordsNum"] = content_num
        fields["images"] = images
        fields["covers"] = covers
        fields["videos"] = video_urls
        fields["audios"] = []
        fields["source"] = pub_source
        fields["pubTime"] = pub_time
        # fields["channel"] = channel
        fields["authors"] = authors

        # 为首页轮播新闻,头条新闻,添加标签
        if channel_name == "首页":
            if "3_3_1" in self._parents_id:
                fields["classifications"] = ["rcmd_2"]
            else:
                fields["classifications"] = []
        else:
            fields["classifications"] = []
        return fields

    def fetch_channels(self, url):
        """
        获取频道信息 首页除外
        :return: 版面信息
        :param url: 起始页面url
        :return:
        """
        try:
            response, real_url = self.fetch_page_source(url)
            # 得到真实的URL地址。
            url = real_url
            tree = etree.HTML(response)
            # 所有版面的链接。
            # 版面名称
            channel_names = ""
            if self._channel_info_xpaths:
                # 先把首页返回。
                # row = dict()
                # row["status"] = 1
                # row["platformID"] = self._platform_id
                # row["platformName"] = self._paper["platformName"]
                # row["url"] = url
                # row["name"] = "首页"
                # row["_id"] = md5(f'{row["platformID"]}{row["name"]}')
                # row["region"] = []
                # row["types"] = []
                # row["selfTypesIDs"] = []
                # yield row
                for channel_info_xpath in self._channel_info_xpaths:
                    if not channel_info_xpath:
                        continue
                    for channel_info in tree.xpath(channel_info_xpath):
                        try:
                            channel_url = channel_info.xpath("./@href")[0].strip()
                            channel_url = re.sub(self._href_xpath_pattern, "", channel_url)
                            if channel_info.xpath("./text()"):
                                channel_names = channel_info.xpath("./text()")
                            elif channel_info.xpath("./span/text()"):
                                channel_names = channel_info.xpath("./span/text()")
                            elif channel_info.xpath("./i[2]/text()"):
                                channel_names = channel_info.xpath("./i[2]/text()")
                            elif channel_info.xpath("./@title"):
                                channel_names = channel_info.xpath("./@title")
                            channel_name = "".join(
                                [str(channel_name).strip().replace("|", '').replace("\r", '').replace("\n", '') for
                                 channel_name
                                 in channel_names]).strip()
                            channel_name = "".join(channel_name.split())
                            channel_name = unicodedata.normalize('NFKC', channel_name)
                            if channel_name == "首页":
                                continue
                            elif channel_name == "网站首页":
                                continue
                            if channel_url and channel_url != "#" and channel_url != "/":
                                channel_url = urljoin(url, channel_url)
                            # 结果集。
                            row = dict()
                            row["status"] = 1
                            row["platformID"] = self._platform_id
                            row["platformName"] = self._paper["platformName"]
                            row["url"] = channel_url
                            row["name"] = channel_name
                            row["_id"] = md5(f'{row["platformID"]}{row["name"]}')
                            row["region"] = []
                            row["types"] = []
                            row["selfTypesIDs"] = []
                            yield row
                        except Exception as e:
                            self._logger.warning("{}\n{}".format(e, traceback.format_exc()))
                            continue
        except Exception as e:
            self._logger.debug(str(e))

    def fetch_index_detail_urls(self, url):
        """
        采集首页新闻列表
        包含轮播信息，首页头条，以及轮播旁边的新闻信息
        :return:
        """
        try:
            response, real_url = self.fetch_page_source(url)
            # 得到真实的URL地址。
            url = real_url
            tree = etree.HTML(response)
            # 存储首页新闻链接
            index_url = set()
            # 所有头条新闻链接。
            if self._headline_news:
                for headline_news in self._headline_news:
                    if not headline_news:
                        continue
                    for headline_new in tree.xpath(headline_news):
                        try:
                            headline_new_url = headline_new.xpath("./@href")[0].strip()
                            headline_new_url = re.sub(self._href_xpath_pattern, "", headline_new_url)
                            if headline_new_url and headline_new_url != "#" and headline_new_url != "/":
                                headline_new_url = urljoin(url, headline_new_url)
                                index_url.add(headline_new_url)
                        except Exception as e:
                            self._logger.warning("{}\n{}".format(e, traceback.format_exc()))
                            continue
            # 首页轮播新闻
            if self._banner_news:
                for banner_news in self._banner_news:
                    if not banner_news:
                        continue
                    for banner_new in tree.xpath(banner_news):
                        try:
                            banner_news_url = banner_new.xpath("./@href")[0].strip()
                            banner_news_url = re.sub(self._href_xpath_pattern, "", banner_news_url)
                            if banner_news_url and banner_news_url != "#" and banner_news_url != "/":
                                banner_news_url = urljoin(url, banner_news_url)
                                index_url.add(banner_news_url)
                        except Exception as e:
                            self._logger.warning("{}\n{}".format(e, traceback.format_exc()))
                            continue
            # 轮播旁边新闻
            if self._banner_news_side:
                for banner_news_side in self._banner_news_side:
                    if not banner_news_side:
                        continue
                    for banner_new_side in tree.xpath(banner_news_side):
                        try:
                            banner_news_side_url = banner_new_side.xpath("./@href")[0].strip()
                            banner_news_side_url = re.sub(self._href_xpath_pattern, "", banner_news_side_url)
                            if banner_news_side_url and banner_news_side_url != "#" and banner_news_side_url != "/":
                                banner_news_side_url = urljoin(url, banner_news_side_url)
                                index_url.add(banner_news_side_url)
                        except Exception as e:
                            self._logger.warning("{}\n{}".format(e, traceback.format_exc()))
                            continue
            return list(index_url)
        except Exception as e:
            self._logger.debug(str(e))
            return None

    def fetch_start(self):
        """
        采集开始,频道信息，稿件信息结果集
        :return:
        """
        self._logger.info(f"{self._paper['platformName']}开始采集")
        start_url = self._start_url
        # noinspection PyBroadException
        try:
            # 循环频道URL进行爬取。
            for channel_row in self.fetch_channels(start_url):
                # 每一个频道连带其详情作为一条基础数据。
                base_item = dict(
                    code=1,
                    msg="成功",
                    channel=channel_row,
                    article=list(),
                )
                try:
                    channel_url = channel_row.get("url")
                    channel_name = channel_row.get("name")
                    # 获取每一个频道新闻详情列表
                    if channel_name == "首页":
                        continue
                        # detail_urls = self.fetch_index_detail_urls(channel_url)
                    else:
                        detail_urls = self.parse_detail_url(channel_url)
                    for detail_url in detail_urls:
                        try:
                            result = self.parse_doc_page(detail_url, channel_name)
                            result["channelID"] = channel_row.get("_id")
                            result["channelName"] = channel_row.get("name", "")
                            base_item["article"].append(result)
                        except Exception as e:
                            self._logger.warning("Failed to parse_doc_page, '{}'.".format(e))
                            # print(e)
                            continue
                    self._logger.info(f"{self._paper['platformName']}-<{channel_name}>频道下的稿件数据为【{len(base_item['article'])}】")
                except Exception as e:
                    self._logger.warning("Failed to fetch channel, '{}'.".format(e))
                    # print(e)
                    continue
                yield base_item
        except Exception as e:
            self._logger.warning("Failed to start crawler, '{}'.".format(e))

    def fetch_yield(self):
        """
        程序入库
        :return:
        """
        for result in self.fetch_start():
            pass
            print(result)
            LayoutsCrawlerESUtils(self._logger).es_save_channel_and_works(result)


if __name__ == '__main__':
    # 遍历结果集。
    log = LLog("Test", only_console=False, logger_level="DEBUG").logger

    web_data = {
        "platformName": "七台河新闻网",
        "sourceProvince": "黑龙江省",
        "sourceCity": "七台河市",
        "sourceCounty": "",
        # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
        "sourceLevel": 3,
        # 1：媒体类，2：政务类，3：商业类。
        "sourceClassify": 1,
        # 是否重点渠道。 #高中低 0 1
        "sourceImportance": 1,
        # 是否主流媒体。#高中低
        "mainMedia": 1,
        # 起始地址。
        "start_url": "http://www.qthnews.org.cn/",
        # 可无
        "cookie": "",
        # 首页头条新闻
        "headline_news": ["//td[@class='STYLE91']/a"],
        # 轮播信息
        "banner_news": ["//ul[@id='conScroll_100004767']/div/div[1]/li/a"],
        # 轮播旁边新闻
        "banner_news_side": ["//span[@class='STYLE94']/a"],
        # 导航信息
        "channel_info_xpath": ["//td[@class='STYLE13']/table//tr/td/a"],
        # 详情链接。
        "doc_links": [
            r"https?://[\w\-\.]+/\w{4,}/system/\d{4}/\d{2}/\d{2}/\d{9}.shtml$"
        ],
        # 目标采集字段，成功时忽略后续模板。
        "fields": {
            "title": [
                {"xpath": "//td[@class='heiti20 STYLE112 zi12 STYLE114']/text()", },
                {"xpath": "//td[@class='heiti20 STYLE112 zi12 zi12 zi12 STYLE114']//text()"},
                {"xpath": "//div[@class='STYLE59 zhuti']//text()"},
                {"xpath": "//div[@class='heiti20 STYLE59']/text() | //div[@class='zi18']/text()"}
            ],

            "content": [
                {"xpath": "//td[@class='zi14']", },
                {"xpath": "//td[@class='zi16']"},
            ],

            "pubSource": [
                # {
                #     #稿源：七台河新闻网　作者：李凤茹 李想　2018/05/30　编辑：陈荣娣
                #     #稿源：七台河新闻网 2018/05/30　编辑：陈荣娣
                # 两种情况，取稿源不安全
                #     "xpath": "//span[@class='STYLE112']/text()",
                #     "regex": r"稿源[: ：]\s*?(.*?)",
                # },
                {
                    "xpath": "//span[@id='source_baidu'][1]/text()",
                    "regex": r"来源[: ：]\s*?(.*)$",
                }
            ],

            "pubTime": [
                {
                    "xpath": "//span[@class='STYLE112']/text()",
                    "regex": r"(\d{4}/\d{1,2}/\d{1,2})"
                },
                {
                    "xpath": "//span[@id='pubtime_baidu']/text()"
                }
            ],
            "channel": [{"xpath": "//span[@class='cms_block_span']/a[2]/text()", }, ],
            "authors": [
                {
                    "xpath": "//span[@class='STYLE112']/text()",
                    "regex": r"编辑[: ：]\s*?(.*)$",
                },
                {
                    "xpath": "//span[@id='editor_baidu']/text()",
                    "regex": r"编辑[: ：]\s*?(.*)$",
                }
            ],
            "summary": [],
        }
    }
    paper_templates = {
        "status": 1,
        "name": "",
        "describe": "",
        "value": json.dumps(web_data, ensure_ascii=False),
        "platformID": "08b57e047625505bccc56de53841a6f8",
        "platformName": "中国政府网",
        "platformType": 3,
        "channelID": "",
        "channelName": "",
        "accountID": "",
        "accountName": "",
        "topicID": "",
        "topicTitle": "",
        "worksID": "",
        "worksTitle": "",
        "createTime": "",
        "updateTime": "",
        "types": [
            "3_3_1"
        ],
    }
    WebSpider(paper_template=web_data, logger=log).fetch_yield()
    # WebSpider(paper_template=paper_templates, logger=log).fetch_yield()
