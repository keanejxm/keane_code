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
from bs4 import BeautifulSoup
import time
import base64
import logging
from lxml import etree
from urllib.parse import urljoin

class InitClass(object):
    def __init__(self):
        logging.basicConfig(level = logging.INFO)
        # self.logger = LLog("APP客户端基础配置", only_console = True, logger_level = "INFO").logger
        self.logger = logging

    # 从html字符串格式中获取mp4视频地址
    @staticmethod
    def get_video(content):
        videos = list()
        if "<video" in content:
            content_tree = etree.HTML(content)
            video_list = content_tree.xpath(".//video/@src")
            for video in video_list:
                if video:
                    videos.append(video)
                else:
                    continue
        if "<source" in content:
            content_tree = etree.HTML(content)
            video_list = content_tree.xpath(".//source/@src")
            for video in video_list:
                if video:
                    videos.append(video)
                else:
                    continue
        return videos

    # 从html字符串格式获取图片地址
    @staticmethod
    def get_images(content,type = 0):
        # imagess = re.findall(r"http(\S*).jpg", content)
        # images = list()
        # for image in imagess:
        #     image_url = "http" + image + ".jpg"
        #     images.append(image_url)
        images = list()
        if "<img" in content:
            content_tree = etree.HTML(content)
            if type == 0:
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
        data_formates = ["%Y-%m-%d", "%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d%H:%M:%S", "%Y/%m/%d","%m-%d %H:%M"]
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
    def app_params(url, headers, method, data = "", appjson = ""):
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
    def channel_fields(channelid, channelname, channeltype = "", categoryid = "", categoryname = ""):
        """
        存储构建请求频道参数所需字段
        :param channelid:频道id
        :param channelname:频道名字
        :param channeltype:频道类型
        :param categoryid:
        :param categoryname:
        :return:
        """
        fields = {
            "categoryid": categoryid,
            "categoryname": categoryname,
            "channelid": channelid,
            "channelname": channelname,
            "channeltype": channeltype
        }
        return fields

    # 构建对频道发送请求的url参数
    @staticmethod
    def articlelists_params_fields(url, headers, method, channel_name, data = "", channeljson = "", channeltype = "",
                                   banners = 0, channelid = ""):
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
            "channelid": channelid
        }
        return fields

    # 存储对频道请求后的参数
    @staticmethod
    def articlelist_model(channelname, channelres, banners = 0, channelid = "", channel_type = ""):
        """
        构建文章列表
        :param channelname:
        :param channelres:
        :param banners:
        :param channelid:
        :param channel_type:
        :return:
        """
        fields = {
            "channelname": channelname,
            "channelres": channelres,
            "banner": banners,
            "channelid": channelid,
            "channelType": channel_type
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
            "articelField": "",
            "channelid": "",
            "articleid": "",
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
    def article_params_fields(url, headers, method, channelname = "", imageurl = "", article_field = "", data = "",
                              articlejson = "", sleeptime = 0, channel_id = "",
                              pubtime = "", createtime = "", updatetime = "", source = "", author = "", likenum = "",
                              readnum = "", sharenum = "", commentnum = "", articleurl = "", articleid = "",
                              videourl = "", videocover = "", banners = 0):
        """

        :param url:请求地址
        :param headers:请求头
        :param method:请求方式
        :param channelname:频道名字
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
        :param channel_id:频道id
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
            "channelid": channel_id,
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
    def article_method(appname, articleres, channelname, imageurl, article_field = "", pubtime = "", createtime = "",
                       updatetime = "",
                       source = "", aurthor = "", likenum = "", readnum = "", sharenum = "", commentnum = "",
                       articleurl = "", articleid = "", videourl = "", videocover = "", banners = 0):
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
            "appname": "",  # 应用名称，字符串
            "channelname": "",  # 频道名称，字符串
            "channelID": "",  # 频道id，字符串
            "channelType": "",  # 频道type，字符串
            "url": "",  # 分享的网址，字符串
            "workerid": "",  # 文章id，字符串
            "title": "",  # 文章标题，字符串
            "content": "",  # 文章内容，字符串
            "articlecovers": list(),  # 列表封面，数组
            "images": list(),  # 正文图片，数组
            "videos": list(),  # 视频地址，数组
            "videocover": list(),  # 视频封面，数组
            "width": "",  # 视频宽，字符串
            "height": "",  # 视频高，字符串
            "source": "",  # 文章来源，字符串
            "pubtime": "",  # 发布时间，时间戳（毫秒级，13位）
            "createtime": "",  # 创建时间，时间戳（毫秒级，13位）
            "updatetime": "",  # 更新时间，时间戳（毫秒级，13位）
            "likenum": 0,  # 点赞数（喜欢数），数值
            "playnum": 0,  # 播放数，数值
            "commentnum": 0,  # 评论数，数值
            "readnum": 0,  # 阅读数，数值
            "trannum": 0,  # 转发数，数值
            "sharenum": 0,  # 分享数，数值
            "author": "",  # 作者，字符串
            "banner": 0,  # banner标记，数值（0标识不是，1标识是）
            "specialtopic": 0,  # 是否是专题，数值（0标识不是，1标识是）
            "topicid": "",  # 专题id，字符串
            "topicTitle": "",  # 专题标题，字符串
        }
        return fields

    # 专题采集数据汇总
    @staticmethod
    def topic_fields():
        fields = {
            "topicID": "",  # 专题id，app内唯一标识
            "platformName": "",  # 平台名字（app名字）
            "platformID": "",
            "channelName": "",  # 频道名字
            "channelID": "",  # 频道id
            "topicUrl": "",  # topicUrl
            "title": "",
            "digest": "",  # 简介，摘要
            "topicCover": "",
            "pubTime": "",  # 时间戳
            "articleNum": "",  # 专题内的文章数量
            "newestArticleID": "",  # 最新发布的文章id
            "articlesNumPerHour": "",
            "original": "",
            "firstMedia": "",
            "transPower": "",
            "hotDegree": "",
            "wordsFreq": "",
            "hotDegreeTrend": "",
            "emotionTrend": "",
            "region": "",
            "spreadPath": "",
            "createTime": "",
            "updateTime": ""
        }
        return fields

    # 发送一次请求用这个构建参数
    @staticmethod
    def request_params(url, headers, method, data = "", request_json = "", channelname = "", channeltype = "",
                       articlefield = "", sleeptime = 0):
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

    #解码带转义字符的unicode字符串，结果为unicode字符串。
    def decode_unicode(self,unicodes):
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
