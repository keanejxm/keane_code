#!-*- coding:utf-8 -*-
"""
app爬虫通用模板，用于发送请求，获取响应
# author: Keane
# create date:
# update date: 2020/11/11
"""
import requests
import time
# import json
# import re
# from lxml import etree
# from appspider_total.appspiderrun import Appsider_param
from initclass import InitClass
import logging


# import numpy as np


class Appspider(object):
    def __init__(self, appname):
        self._session = requests
        self.newsname = appname
        logging.basicConfig(level=logging.INFO)
        self.logger = logging
        # self.logger = LLog("APP客户端", only_console = True, logger_level = "INFO").logger

    @staticmethod
    def judge_type(url, headers, data):
        """
        对请求频道信息时对数据类型的判断
        :param url:
        :param headers:
        :param data:
        :return:
        """
        if not isinstance(url, str):
            print('url类型应为字符串类型')
        if not isinstance(headers, dict):
            print('headers类型应为dict')
        if not isinstance(data, dict):
            print('data类型应为dict')

    @staticmethod
    def analyze_dict(dict_data):
        """
        用于分析json格式，暂时不具体使用
        :param dict_data:
        :return:
        """
        dict_keys = []
        if dict_data:
            for dict_key in dict_data:  # 获取json格式的键
                dict_keys.append(dict_key)
            return dict_keys

    def getchannels(self, appparams):
        """
        获取新闻频道页面，需参数appparams，由模板传递
        :param appparams:
        :return: channelres:
        """
        self.logger.info("正在获取频道信息......")
        url = appparams['appurl']
        headers = appparams['appheaders']
        data = appparams['appdata']
        method = appparams['appmethod']
        appjsons = appparams["appjson"]
        self.judge_type(url, headers, data)
        # channelsres = []
        if method == "get":
            if appjsons:
                channelres = requests.get(url, headers=headers, params=data, json=appjsons).text
            else:
                channelres = requests.get(url, headers=headers, params=data).text
            # channelsres.append(channelres)
            yield channelres
        if method == "post":
            channelres = requests.post(url, headers=headers, data=data, json=appjsons).text
            # channelsres.append(channelres)
            yield channelres

    def getarticlelists(self, channel_datas):
        """
        通过传入的数据对频道发送请求采集文章列表的信息
        :param channel_datas: 发送请求携带的，请求头，数据，请求方式，
        :return:携带文章列表信息的响应网页
        """

        articleslists = []
        for channel_data in channel_datas:
            method = channel_data.get("method")
            channelname = channel_data.get("channelname")
            channelid = channel_data.get("channelid")
            channeljson = channel_data.get("channeljson")
            banners = channel_data.get("banner")
            channel_type = channel_data.get("channeltype")
            self.logger.info(f"正在采集频道{channelname}内容")
            if method == 'get':
                try:
                    articlelist_res = requests.get(channel_data.get("url"), headers=channel_data.get("headers"),
                                                   params=channel_data.get("data")).text
                    articleslist = InitClass().articlelist_model(channelname, articlelist_res, banners,
                                                                 channelid=channelid, channel_type=channel_type)
                    articleslists.append(articleslist)
                except Exception as e:
                    self.logger.info(f"{e}")
            elif method == 'post':
                try:
                    articlelist_res = requests.post(channel_data.get("url"), headers=channel_data.get("headers"),
                                                    data=channel_data.get("data"), json=channeljson).text
                    articleslist = InitClass().articlelist_model(channelname, articlelist_res, banners=banners,
                                                                 channelid=channelid, channel_type=channel_type)
                    articleslists.append(articleslist)
                except Exception as e:
                    self.logger.info(f"{e}")
        yield articleslists

    def getarticlehtml(self, articleparams):
        """
         通过传输的数据对详情页进行数据采集，获取详情页数据
        :param articleparams: articleparams,包含请求头，发送请求需要携带的数据，请求方式
        :return: 采集的网页信息
        """
        articles_res = []
        for articleparam in articleparams:
            try:
                st = articleparam.get("sleeptime")
            except Exception as e:
                self.logger.info(f"此app无需设置睡眠时间'{e}'")
                st = 0
            url = articleparam.get("url")
            headers = articleparam.get("headers")
            data = articleparam.get("data")
            method = articleparam.get("method")
            banners = articleparam.get("banner")
            articlejson = articleparam.get("articlejson")
            article_field = articleparam.get("articleField")
            channelname = articleparam.get("channelname")
            if not channelname:
                channelname = article_field.get("channelname")
            imgurl = articleparam.get("imageurl")
            articleurl = articleparam.get("articleurl")
            videourl = articleparam.get("videourl")
            videocover = articleparam.get("videocover")
            articleid = articleparam.get("articleid")
            pubtime = articleparam.get("pubtime")
            createtime = articleparam.get("createtime")
            updatetime = articleparam.get("updatetime")
            likenum = articleparam.get("likenum")
            readnum = articleparam.get("readnum")
            sharenum = articleparam.get("sharenum")
            commentnum = articleparam.get("commentnum")
            source = articleparam.get("source")
            author = articleparam.get("author")
            self.logger.info(f"正在采集文章内容:{channelname}，{url}")
            res = ''
            try:
                if method == "get":
                    res = requests.get(url, headers=headers, params=data).text
                if method == "post":
                    res = requests.post(url, headers=headers, data=data, json=articlejson).text
            except Exception as e:
                print(e)
            articleres = InitClass().article_method(self.newsname, res, channelname, imgurl, pubtime=pubtime,
                                                    createtime=createtime, updatetime=updatetime, source=source,
                                                    aurthor=author, likenum=likenum, commentnum=commentnum,
                                                    articleurl=articleurl, articleid=articleid, videourl=videourl,
                                                    videocover=videocover, readnum=readnum, sharenum=sharenum,
                                                    banners=banners, article_field=article_field)
            articles_res.append(articleres)
            time.sleep(st)
        yield articles_res

    def send_request(self, request_params, retry=0, code='utf8'):
        """
        增加发送单次请求模板，针对对单个文章的请求，可用来请求专题下的文章，
        :param request_params:从initclass内组成
        :return:返回{"request_res":res,"articlefields":"article_fields"},下一步用get获取
        """

        sleeptime = request_params.get("sleeptime")
        if sleeptime:
            time.sleep(sleeptime)
        url = request_params.get('url')
        headers = request_params.get('headers')
        data = request_params.get('data')
        method = request_params.get('method')
        request_json = request_params.get("requestjson")
        article_fields = request_params.get("articlefields")
        response_res = dict()
        try:
            if method == "get":
                if request_json:
                    res = requests.get(url, headers=headers, params=data,
                                       json=request_json, timeout=10).content.decode(code)
                else:
                    res = requests.get(url, headers=headers, params=data, timeout=10).content.decode(code)
                response_res["request_res"] = res
                response_res["articlefields"] = article_fields
                yield response_res

            elif method == "post":
                res = requests.post(url, headers=headers, data=data, json=request_json, timeout=10).content.decode(
                    code)
                response_res["request_res"] = res
                response_res["articlefields"] = article_fields
                yield response_res
            else:
                self.logger.warning(f"暂时无此请求方式需添加此请求方式")
        except TimeoutError as e:
            print(e)
            if retry < 10:
                retry += 1
                return self.send_request(request_params=request_params, retry=retry)
            else:
                self.logger.warning(f"多次请求超时")
