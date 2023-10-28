#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
存放需初始化字段
# author: Keane
# create date: 2020/11/23
# update date: 2020/11/23
"""
import json
import re
import time
import base64
import hashlib
# from api_data_center.api_common_utils.llog import LLog
import logging
from bs4 import BeautifulSoup
from lxml import etree
from api_common_utils.wash.parse_content import ParseContent


# import elasticsearch


class InitClass(object):
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        # self.logger = LLog("APP客户端基础配置", only_console = True, logger_level = "INFO").logger
        self.logger = logging
        self.get_extract = ParseContent()

    @staticmethod
    def encode_md5(a_str):
        """
        md5加密方法
        """
        has = hashlib.md5()
        has.update(a_str.encode("utf-8"))
        md5_res = has.hexdigest()
        return md5_res

    # 构建存储es频道索引方法
    def create_channel_index(self, platform_id, platform_name, partentid, channelname, num):
        md_str = str(platform_id) + str(channelname)
        _id = self.encode_md5(md_str)
        field = {
            "_id": _id,
            "status": 1,
            "platformID": platform_id,
            "platformName": platform_name,
            "platformType": 4,
            "name": channelname,
            "types": [partentid],
            "selfTypesIDs": [partentid + "_" + str(num)],
            "order": num,
            "createTime": int(time.time() * 1000),
            "updateTime": int(time.time() * 1000),
        }
        return field, _id

    # 从html字符串格式中获取mp4视频地址
    @staticmethod
    def get_video(content):
        videoss = re.findall(r"http(\S*).mp4", content)
        videos = list()
        for video in videoss:
            video_url = "http" + video + ".mp4"
            videos.append(video_url)
        return videos

    # 从html字符串格式获取图片地址
    @staticmethod
    def get_images(content, a_type=0):
        # imagess = re.findall(r"http(\S*).jpg", content)
        # images = list()
        # for image in imagess:
        #     image_url = "http" + image + ".jpg"
        #     images.append(image_url)
        images = list()
        if "<img" in content:
            content_tree = etree.HTML(content)
            if a_type == 0:
                img_list = content_tree.xpath(".//img/@src")
                for img in img_list:
                    if img:
                        images.append(img)
                    else:
                        continue
            elif not images or type == 1:
                img_list = content_tree.xpath(".//img/@data-original")
                for img in img_list:
                    if img:
                        images.append(img)
                    else:
                        continue
        elif "<image" in content:
            content_tree = etree.HTML(content)
            img_list = content_tree.xpath(".//img/@src")
            for img in img_list:
                if img:
                    images.append(img)
                else:
                    continue
        return images

    # base64解密
    @staticmethod
    def decode_base64(in_str):
        res = base64.b64decode(in_str).decode("utf-8")
        return res

    # 提取格式化时间
    @staticmethod
    def format_date(a_str):
        """
        格式化时间为2020-12-1 12:00:00形式
        :param a_str: 不规则时间信息
        :return: 格式后的时间
        """
        date = re.findall(r'\d{4}-\d{2}-\d{2}.*\d{2}:\d{2}:\d{2}', a_str)
        if date:
            return date[0].replace("T", " ")
        else:
            return '没有符合的时间格式'

    # 将时间转为时间戳
    def date_time_stamp(self, date):
        """
        将时间转为时间戳
        :param date: 2020-12-12 12:00:00
        :return: 时间戳毫秒级
        """
        # 转为时间戳
        data_formates = ["%Y-%m-%d", "%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d%H:%M:%S", "%Y/%m/%d",
                         "%Y年%m月%d日", "%m-%d %H:%M"]
        time_stamp = 0
        for data_formate in data_formates:
            try:
                if data_formate == "%m-%d %H:%M":
                    this_year = time.strftime('%Y', time.localtime(time.time()))
                    date = str(this_year) + "-" + date
                    data_formate = "%Y-%m-%d %H:%M"
                time_array = time.strptime(date, data_formate)
                time_stamp = int(time.mktime(time_array)) * 1000
                if time_stamp:
                    break
            except Exception:
                pass
        if time_stamp == 0:
            self.logger.info(f"{date}没有合适时间格式，请手动配置时间格式")
        return time_stamp

    # 构建对app请求的参数
    @staticmethod
    def app_params(url, headers, method, data="", appjson=""):
        """
        构建app首页请求参数
        :param url: 请求地址
        :param headers: 请求头
        :param method: 请求方式
        :param data: 携带数据
        :param appjson: 携带json数据
        :return:
        """
        fields = {
            "appurl": url,
            "appheaders": headers,
            "appdata": data,
            "appmethod": method,
            "appjson": appjson
        }
        return fields

    # 存储解析后对频道发送请求所需的参数
    @staticmethod
    def channel_fields(channelid, channelname, channeltype="", channel_index_id="", categoryid="",
                       categoryname="", channel_url=""):
        """
        存储构建请求频道参数所需字段
        :param channelid:频道id
        :param channelname:频道名字
        :param channeltype:频道类型
        :param channel_index_id:频道id(md5加密)
        :param categoryid:
        :param categoryname:
        :param channel_url:频道url
        :para·m channel_index_id:channel在索引中的id
        :return:
        """
        fields = {
            "categoryid": categoryid,
            "categoryname": categoryname,
            "channelid": channelid,
            "channelindexid": channel_index_id,
            "channelname": channelname,
            "channeltype": channeltype,
            "channelUrl": channel_url
        }
        return fields

    # 构建对频道发送请求的url参数
    @staticmethod
    def articlelists_params_fields(url, headers, method, channel_name, data="", channeljson="", channeltype="",
                                   banners=0, channelid="", channel_index_id="", sleep_time=0):
        """
        构建请求频道获取文章列表信息参数
        :param url: 请求地址
        :param headers: 请求头
        :param method: 请求方式
        :param channel_name: 频道名
        :param data:携带数据
        :param channeljson:携带json数据
        :param channeltype:频道类型
        :param banners:是否为头条，是为1，否为0
        :param channelid:是否为头条，是为1，否为0
        :param channel_index_id:频道id（md5加密查询用）
        :param sleep_time:睡眠时间，反爬
        :return:
        """
        fields = {
            "url": url,
            "headers": headers,
            "data": data,
            "method": method,
            "channelname": channel_name,
            "channeljson": channeljson,
            "channeltype": channeltype,
            "banner": banners,
            "channelid": channelid,
            "channelindexid": channel_index_id,
            "sleeptime": sleep_time
        }
        return fields

    # 存储对频道请求后的参数
    @staticmethod
    def articlelist_model(channelname, channelres, banners=0, channelid="", channel_type="",
                          channel_index_id=""):
        """
        构建文章列表
        :param channelname:
        :param channelres:
        :param banners:
        :param channelid:
        :param channel_type:
        :param channel_index_id:
        :return:
        """
        fields = {
            "channelname": channelname,
            "channelres": channelres,
            "banner": banners,
            "channelid": channelid,
            "channelType": channel_type,
            "channelindexid": channel_index_id
        }
        return fields

    # 解析频道下的文章列表，获取请求文章详情的必需参数id，此处可只用articleField存储数据
    @staticmethod
    def article_list_fields():
        """
        存储文章的信息，用于构建文章详情参数
        :return:
        """
        fields = {
            "articleField": "",
            "channelid": "",
            "articleid": "",
            "channelindexid": "",
            "articletype": "",
            "articletitle": "",
            "channelname": "",
            "banner": 0,
            "specialtopic": 0,
            "imageurl": "",
            "articleurl": "",
            "videos": [],
            "videocover": [],
            "pubtime": "",
            "createtime": "",
            "updatetime": "",
            "source": "",
            "author": "",
            "likenum": 0,
            "commentnum": 0,
            "readnum": 0,
            "sharenum": 0,
        }
        return fields

    # 构建对文章详情发起请求所需的url等参数，此处版本已修改，只向下传递artilce_field参数
    @staticmethod
    def article_params_fields(url, headers, method, channelname="", imageurl="", article_field="", data="",
                              articlejson="", sleeptime=0, channel_index_id="",
                              pubtime="", createtime="", updatetime="", source="", author="", likenum="",
                              readnum="", sharenum="", commentnum="", articleurl="", articleid="",
                              videourl="", videocover="", banners=0):
        """

        :param url:请求地址
        :param headers:请求头
        :param method:请求方式
        :param channelname:频道名字
        :param channel_index_id:频道由md5组成的唯一id
        :param imageurl:封面地址
        :param data:请求数据
        :param articlejson:请求json数据
        :param sleeptime:请求是间隔时间，防反爬
        :param pubtime:发布时间
        :param createtime:创建时间
        :param updatetime:更新时间
        :param source:文章来源
        :param author:作者
        :param likenum:点赞数
        :param readnum:阅读数
        :param sharenum:分享数
        :param commentnum:评论数
        :param articleurl:文章url，有的文章详情没有
        :param articleid:文章id，有的文章详情中没有
        :param videourl:视频地址，有的文章详情中没有
        :param videocover:视频封面，有的文章详情中没有
        :param article_field:采集数据集合，用于向下传递
        :param banners:是否是banners
        :return:
        """
        fields = {
            "url": url,
            "headers": headers,
            "data": data,
            "articlejson": articlejson,
            "method": method,
            "sleeptime": sleeptime,
            "articleField": article_field,
            "channelname": channelname,
            "channelindexid": channel_index_id,
            "imageurl": imageurl,
            "videourl": videourl,
            "videocover": videocover,
            "articleurl": articleurl,
            "articleid": articleid,
            "pubtime": pubtime,
            "createtime": createtime,
            "updatetime": updatetime,
            "source": source,
            "author": author,
            "likenum": likenum,
            "readnum": readnum,
            "sharenum": sharenum,
            "commentnum": commentnum,
            "banner": banners
        }
        return fields

    # 存储文章详情
    @staticmethod
    def article_method(appname, articleres, channelname, imageurl, article_field="", pubtime="", createtime="",
                       updatetime="", channel_index_id="",
                       source="", aurthor="", likenum="", readnum="", sharenum="", commentnum="",
                       articleurl="", articleid="", videourl="", videocover="", banners=0):
        """

        :param appname:app的名字
        :param articleres:返回的响应
        :param channelname:频道名字
        :param imageurl:文章封面图片
        :param pubtime:发布时间
        :param createtime:创建时间
        :param updatetime:更新时间
        :param source:文章来源
        :param aurthor:文章作者
        :param likenum:点赞数
        :param commentnum:评论数
        :param articleurl:文章地址
        :param articleid:文章id
        :param videourl:视频地址
        :param videocover:视频封面
        :param article_field:视频封面
        :param readnum:视频封面
        :param sharenum:视频封面
        :param banners:视频封面
        :return:
        """
        fields = {
            "appname": appname,
            "articleres": articleres,
            "channelname": channelname,
            "channelindexid": channel_index_id,
            "articleField": article_field,
            "imageurl": imageurl,
            "articleurl": articleurl,
            "videourl": videourl,
            "videocover": videocover,
            "articleid": articleid,
            "pubtime": pubtime,
            "createtime": createtime,
            "updatetime": updatetime,
            "source": source,
            "author": aurthor,
            "likenum": likenum,
            "readnum": readnum,
            "sharenum": sharenum,
            "commentnum": commentnum,
            "banner": banners
        }
        return fields

    # 文章采集数据汇总
    @staticmethod
    def article_fields():
        """
        初始化存储字段、媒体类型、app名字、频道、新闻地址（html）、新闻id、标题、内容、文章封面图、图片、视频、视频封面、视频宽、视频高、来源、发布时间、创建时间、
        更新时间、点赞数、视频播放数、评论数、阅读数、转发数、分享数、作者
        :return:
        """
        fields = {
            "mediatype": "app数据",
            "appname": "",
            "platformID": "",
            "channelname": "",
            "channelID": "",
            "channelindexid": "",
            "channelType": "",
            "url": "",
            "workerid": "",
            "contentType": "",
            "title": "",
            "digest": "",
            "content": "",
            "articlecovers": list(),
            "images": list(),
            "videos": list(),
            "audios": list(),
            "videocover": list(),
            "width": "",
            "height": "",
            "source": "",
            "pubtime": 0,
            "createtime": 0,
            "updatetime": 0,
            "likenum": 0,
            "playnum": 0,
            "commentnum": 0,
            "readnum": 0,
            "trannum": 0,
            "sharenum": 0,
            "author": "",
            "editor": "",
            "banner": 0,
            "ispush": 0,
            "specialtopic": 0,  # 是否是专题
            "topicid": "",
            "topicTitle": ""
        }
        return fields

    # 专题采集数据汇总
    @staticmethod
    def topic_fields():
        fields = {
            "topicID": "",  # 专题id，app内唯一标识
            "platformName": "",  # 平台名字
            "platformID": "",  # 平台id
            "topicUrl": "",  # 专题url
            "title": "",  # 专题标题
            "digest": "",  # 专题摘要
            "topicCover": list(),  # 专题封面
            "pubTime": 0,  # 专题发布时间
            "createTime": "",
            "updateTime": ""
        }
        return fields

    # 将文章数据转为专题数据
    def article_topic(self, article_field):
        topic_fields = self.topic_fields()
        topic_fields["topicID"] = article_field.get("workerid")
        topic_fields["platformName"] = article_field.get("appname")
        topic_fields["platformID"] = article_field.get("platformID")
        topic_fields["channelName"] = article_field.get("channelname")
        topic_fields["channelID"] = article_field.get("channelindexid")
        topic_fields["topicUrl"] = article_field.get("url")
        topic_fields["title"] = article_field.get("title")
        topic_fields["digest"] = article_field.get("digest")
        topic_fields["topicCover"] = article_field.get("articlecovers")
        topic_fields["pubTime"] = article_field.get("pubtime")
        return topic_fields

    # 发送一次请求用这个构建参数
    @staticmethod
    def request_params(url, headers, method, data="", request_json="", channelname="", channeltype="",
                       articlefield="", sleeptime=0):
        request_param = {
            "url": url,
            "headers": headers,
            "data": data,
            "method": method,
            "requestjson": request_json,
            "channelname": channelname,
            "channeltype": channeltype,
            "articlefields": articlefield,
            "sleeptime": sleeptime
        }
        return request_param

    # 清洗content内的script标签
    # def wash_tag(self,content):
    # 清洗html、script标签
    @staticmethod
    def wash_tag(content):
        soup = BeautifulSoup(content, "lxml")
        [script.extract() for script in soup.findAll("script")]
        content = str(soup).replace("<html>", "")
        content = content.replace("</html>", "")
        content = content.replace("<body>", "")
        content = content.replace("</body>", "")
        return content

    # 清洗数据为存储的格式
    def wash_article_data(self, article_fields):
        try:
            field = {
                "status": 1,
                "platformWorksID": "",
                "platformID": "",
                "platformName": "",
                "platformType": 4,
                "channelID": "",
                "channelName": "",
                "accountID": "",
                "accountName": "",
                "topicID": "",
                "topicTitle": "",
                "epaperLayoutID": "",
                "url": "",
                "authors": [],
                "editors": list(),
                "hbrbAuthors": list(),
                "preTitle": "",
                "subTitle": "",
                "title": "",
                "titleWordsNum": 0,
                "content": "",
                "contentWordsNum": 0,
                "html": "",
                "simhash": "",
                "contentType": -1,
                "digest": "",
                "digestOriginal": "",
                "digestCompute": "",
                "source": "",
                "isOriginal": -1,
                "isOriginalCompute": -1,
                "isPush": 0,
                "isTop": 0,
                "classifications": list(),
                "images": list(),
                "covers": list(),
                "topics": list(),
                "videos": list(),
                "audios": list(),
                "updateParams": "{}",
                "readNum": 0,
                "commentNum": 0,
                "likeNum": 0,
                "collectNum": 0,
                "forwardNum": 0,
                "wxLookNum": 0,
                "sentiment": -1,
                "sentimentPositiveProb": -1,
                "wangYiJoinNum": 0,
                "personNames": list(),
                "regionNames": list(),
                "organizationNames": list(),
                "keywords": list(),
                "segmentWordsRawInfo": "",
                "hasSpread": -1,
                "hasSimilarWorks": -1,
                "hasSimilarOriginalWorks": -1,
                "reprintNum": 0,
                "reprintMediaNum": 0,
                "spreadHI": 0,
                "interactiveHI": 0,
                "pubTime": 0,
                "createTime": int(time.time() * 1000),
                "updateTime": int(time.time() * 1000),
            }
            article_id = article_fields.get("workerid")
            app_name = article_fields.get("appname")
            title = article_fields.get("title")
            pubtime = article_fields.get("pubtime")
            content = article_fields.get("content")
            if content:
                # content = self.get_extract.remove_js_css(content)
                result = self.get_extract.do_parse(content)
                field["digest"] = result["digest"]
                field["content"] = result["content"]
            md5_str = str(article_id) + app_name + title + str(pubtime)
            _id = self.encode_md5(md5_str)
            field["_id"] = _id
            field["topicID"] = article_fields.get("topicid")
            field["topicTitle"] = article_fields.get("topicTitle")
            field["platformName"] = article_fields.get("appname")
            field["platformID"] = article_fields.get("platformID")
            field["platformWorksID"] = article_fields.get("workerid")
            field["channelID"] = article_fields.get("channelindexid")
            field["channelName"] = article_fields.get("channelname")
            field["url"] = article_fields.get("url")
            field["authors"] = article_fields.get("author")
            field["editors"] = article_fields.get("editor")
            field["title"] = article_fields.get("title")
            field["titleWordsNum"] = len(article_fields.get("title"))
            field["contentWordsNum"] = len(article_fields.get("content"))
            field["source"] = article_fields.get("source")
            field["images"] = article_fields.get("images")
            field["covers"] = article_fields.get("articlecovers")
            field["videos"] = article_fields.get("videos")
            field["audios"] = article_fields.get("audios")
            field["readNum"] = article_fields.get("readnum")
            field["commentNum"] = article_fields.get("commentnum")
            field["likeNum"] = article_fields.get("likenum")
            field["forwardNum"] = article_fields.get("trannum")
            field["pubTime"] = article_fields.get("pubtime")
            field["contentType"] = article_fields.get("contentType")
            field["isTop"] = article_fields.get("banner")
            field["isPush"] = article_fields.get("ispush")
            # field["isTop"] = 1
            if article_fields.get("banner") in (1, "1"):
                field["classifications"] = ["rcmd_4"]
            if field["source"] and field["platformName"] in field["source"]:
                field["isOriginal"] = 1
            else:
                field["isOriginal"] = 0
            return field
        except Exception as e:
            self.logger.info(f"{e}")

    def wash_topic_data(self, topic_fields):
        """
        清洗专题的数据
        """
        fields = {
            "_id": "",  # 专题id，app内唯一标识
            "status": 1,
            "topicID": "",  # 专题在平台的id
            "platformName": "",  # 平台名字
            "platformType": 4,
            "platformID": "",  # 平台id
            "url": "",  # 专题url
            "title": "",  # 专题标题
            "digest": "",  # 摘要
            "topicCovers": list(),  # 专题封面
            "pubTime": "",  # 专题发布时间
            "platformReadsNum": 0,
            "platformLikesNum": 0,
            "platformCommentsNum": 0,
            "platformForwardsNum": 0,
            "createTime": int(time.time() * 1000),
            "updateTime": int(time.time() * 1000)
        }
        fields["topicID"] = topic_fields.get("topicID")
        fields["platformName"] = topic_fields.get("platformName")
        fields["platformID"] = topic_fields.get("platformID")
        fields["url"] = topic_fields.get("topicUrl")
        fields["title"] = topic_fields.get("title")
        fields["digest"] = topic_fields.get("digest")
        fields["topicCovers"] = topic_fields.get("topicCover")
        fields["pubTime"] = topic_fields.get("pubTime")
        topic_id = fields.get("topicID")
        app_name = fields.get("platformName")
        title = fields.get("title")
        pubtime = fields.get("pubTime")
        md5_str = str(topic_id) + app_name + title + str(pubtime)
        _id = self.encode_md5(md5_str)
        fields["_id"] = _id
        return fields, _id

    def decode_unicode(self, unicodes):
        """
        解码带转义字符的unicode字符串，结果为unicode字符串。
        :param unicodes: unicode字符串，如："\\u22\\u3e\\u25a0\\u3000"。
        :return:
        """

        item = list()
        items = list()
        for u in unicodes:
            u = str(u)
            if u != "\\":
                item.append(u)
            else:
                if item:
                    items.append(item)
                item = list()
                item.append("\\")
        for i in range(len(items)):
            if len(items[i]) == 4:
                items[i].insert(2, "0")
                items[i].insert(2, "0")
            items[i] = "".join(items[i])
        content = "".join(items)
        return json.loads(f'"{content}"')
