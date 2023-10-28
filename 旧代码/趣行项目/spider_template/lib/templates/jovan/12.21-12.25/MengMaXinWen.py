# -*- encoding:utf-8 -*-
"""
@功能:湖北日报解析模板
@AUTHOR：jovan
@文件名：HuBeiRiBao.py
@时间：2020年12月22日 15:58:24
有的新闻正文被删除了会报错
"""

import json
import logging
import time

import requests

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass

topicParamList = []


def setListNewsParam(articlesparams, channelname, channelid, banner, item):
    try:
        article_fields = InitClass().article_fields()
        article_fields["channelname"] = channelname  # 频道名称，字符串
        article_fields["channelID"] = channelid  # 频道id，字符串
        # article_fields["channelType"] = channel_type  # 频道type，字符串
        if 'h5url' in item.keys():
            article_fields["url"] = item['h5url']  # 分享的网址，字符串
        if 'title' in item.keys():
            article_fields["title"] = item['title']  # 文章标题，字符串
        elif 'typename' in item.keys():
            article_fields["title"] = item['typename']  # 文章标题，字符串
        else:
            print(item)
        # article_fields["content"] = item['webLink']  # 文章内容，字符串
        # article_fields["articlecovers"] = imgList  # 列表封面，数组
        # article_fields["images"] = ''  # 正文图片，数组
        # article_fields["videocover"] = [item['videoImg']]  # 视频封面，数组
        # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
        # article_fields["width"] = ''  # 视频宽，字符串
        # article_fields["height"] = ''  # 视频高，字符串
        if 'source' in item.keys():
            article_fields["source"] = item['source']  # 文章来源，字符串
        if 'publishdate' in item.keys():
            article_fields["pubtime"] = item['publishdate']  # 发布时间，时间戳（毫秒级，13位）
        if 'createdate' in item.keys():
            article_fields["createtime"] = item['createdate']  # 创建时间，时间戳（毫秒级，13位）
        # article_fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
        # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
        # article_fields["playnum"] = ''  # 播放数，数值
        # article_fields["commentnum"] = item['commentNum']  # 评论数，数值
        # article_fields["readnum"] = ''  # 阅读数，数值
        # article_fields["trannum"] = ''  # 转发数，数值
        # article_fields["sharenum"] = ''  # 分享数，数值
        # article_fields["author"] = ''  # 作者，字符串
        article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
        if 'newid' in item.keys() and item['newid'] is not None:
            article_fields["workerid"] = item['newid']  # 文章id，字符串
        elif 'typeid' in item.keys() and item['typeid'] is not None:
            article_fields["workerid"] = item['typeid']  # 文章标题，字符串
        else:
            print(item)

        # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
        # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
        if ('typeflag' in item.keys() and 3 == item['typeflag']) or ('type' in item.keys() and 3 == item['type']):  # 专题
            article_fields["newstype"] = "QxDataTopic"  # 自己添加新闻类型
        elif '图文直播' == channelname:
            article_fields["newstype"] = "QxDataLiveTxtPic"  # 自己添加新闻类型
        else:
            article_fields["newstype"] = "QxDataDef"  # 自己添加新闻类型
        articleparam = InitClass().article_list_fields()
        articleparam["articelField"] = article_fields
        articlesparams.append(articleparam)
    except Exception as e:
        logging.info(e)
    # if 'type' in item.keys() and 2 == item['type']:  # 直播
    #     print(item)  # 未出现
    # elif 'type' in item.keys() and 3 == item['type']:  # 专题
    #     print(item)  # 未出现
    # else:
    #     if 'personid' in item.keys():  # 政库领导人
    #         print(item)
    #     elif 'typeflag' in item.keys():  # 频道直观
    #         if 3 == item['typeflag']:  # 专题
    #             print(item)
    #         elif 4 == item['typeflag']:  # 图文直播
    #             print(item)
    #         else:
    #             print(item)  # 未出现
    #     else:
    #         if 1 == item['newstype']:  # 普通新闻
    #             print(item)
    #         elif 2 == item['newstype']:  # 图片新闻
    #             print(item)
    #         elif 3 == item['newstype']:
    #             print(item)  # 未出现
    #         elif 4 == item['newstype']:  # 外链
    #             print(item)
    #         elif 5 == item['newstype']:  # 活动
    #             print(item)  # 未出现
    #         elif 6 == item['newstype']:
    #             print(item)  # 未出现
    #         elif 7 == item['newstype']:  # 视频
    #             print(item)
    #         else:
    #             print(item)  # 未出现
    return articlesparams


class MengMaXinWen(Appspider):

    @staticmethod
    def get_app_params():
        url1 = "http://mengma.jinbw.com.cn/newsTypeList.do?clienttype=android&clientversion=4.1.0"
        headers = {
            "Content-Type": "application/json",
            "Content-Length": "66",
            "Host": "mengma.jinbw.com.cn",
            "Connection": "Keep-Alive",
            "User-Agent": "android-async-http/1.4.4 (http://loopj.com/android-async-http)",
            "Accept-Encoding": "gzip",
        }
        method = "post"
        appJson = {"page": 1, "pagesize": 10000, "deleteflag": 1, "flag": 211, "sortflag": 1}
        app_params1 = InitClass().app_params(url1, headers, method, appjson=appJson)

        yield [app_params1]

    def analyze_channel(self, channelsres):
        print(channelsres)
        channelparams = []
        channelparam = InitClass().channel_fields(0, "猛犸", channeltype=1, categoryid=0)
        channelparams.append(channelparam)
        for k, v in channelsres.items():
            if 'http://mengma.jinbw.com.cn/newsTypeList.do?clienttype=android&clientversion=4.1.0' == k:
                channelList = json.loads(v)
                for channel in channelList['rows']:
                    channelid = channel['typeid']
                    channelname = channel['typename']
                    categoryidId = channel['pid']
                    channelType = 0
                    if 500 == channel['typeid'] or 500 == categoryidId:  # "河南政库"
                        continue
                    # if 500 == channel['typeid']:  # "河南政库"
                    #     channelType = 3
                    channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channelType,
                                                              categoryid=categoryidId)
                    channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channelType = channel.get("channeltype")
            categoryidId = channel.get("categoryid")
            url = ""
            headers = {
                "Content-Type": "application/json",
                "Content-Length": "33",
                "Host": "mengma.jinbw.com.cn",
                "Connection": "Keep-Alive",
                "User-Agent": "android-async-http/1.4.4 (http://loopj.com/android-async-http)",
                "Cookie": "SESSION=0694fd88-0ae8-4424-a0f0-8ed2b36a924d",
                "Cookie2": "$Version=1",
                "Accept-Encoding": "gzip",
            }
            method = "post"
            appJson = {}
            if channelid == 287:
                url = "http://mengma.jinbw.com.cn/newsTypeListByApp.do?clienttype=android&clientversion=4.1.0"
                appJson = {"page": 1, "pagesize": 10, "pid": 287}
            else:
                if categoryidId == 0:
                    if channelType == 1:
                        url = "http://mengma.jinbw.com.cn/queryIndexNewsListByApp.do?clienttype=android&clientversion=4.1.0"
                        appJson = {"page": 1, "pagesize": 10, "flag": 1}
                    elif channelType == 3:
                        url = "http://mengma.jinbw.com.cn/personList.do?clienttype=android&clientversion=4.1.0"
                        appJson = {"page": 1, "pagesize": 10}
                    else:  # 0
                        url = "http://mengma.jinbw.com.cn/queryNewsInfoByPidListByApp.do?clienttype=android&clientversion=4.1.0"
                        appJson = {"page": 1, "pagesize": 10, "typeid": channelid, "publishflag": 2, "flag": 112}
                else:
                    if categoryidId == 500:
                        url = "http://mengma.jinbw.com.cn/personList.do?clienttype=android&clientversion=4.1.0"
                        appJson = {"page": 1, "pagesize": 10, "typeid": channelid}
                    else:
                        url = "http://mengma.jinbw.com.cn/newsListByApp.do?clienttype=android&clientversion=4.1.0"
                        appJson = {"page": 1, "pagesize": 10, "typeid": channelid, "publishflag": 2}

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channeljson=appJson, channelid=channelid)
            articlelistsparams.append(articlelist_param)
        url1 = "http://mengma.jinbw.com.cn/queyAllZhiBoByVedioByApp.do?clienttype=android&clientversion=4.1.0"
        url2 = "http://mengma.jinbw.com.cn/queyAllZhiBoByWordByApp.do?clienttype=android&clientversion=4.1.0"
        url3 = "http://mengma.jinbw.com.cn/queyAllZhuantiNewsByApp.do?clienttype=android&clientversion=4.1.0"
        url4 = "http://mengma.jinbw.com.cn/queyAllZhiBoByVedioByApp.do?clienttype=android&clientversion=4.1.0"
        url5 = "http://mengma.jinbw.com.cn/queyAllPicNewsByApp.do?clienttype=android&clientversion=4.1.0 "
        headers = {
            "Content-Type": "application/json",
            "Content-Length": "33",
            "Host": "mengma.jinbw.com.cn",
            "Connection": "Keep-Alive",
            "User-Agent": "android-async-http/1.4.4 (http://loopj.com/android-async-http)",
            "Cookie": "SESSION=0694fd88-0ae8-4424-a0f0-8ed2b36a924d",
            "Cookie2": "$Version=1",
            "Accept-Encoding": "gzip",
        }
        method = "post"
        appJson = {"page": 1, "pagesize": 10}
        articlelist_param1 = InitClass().articlelists_params_fields(url1, headers, method, "视频直播",
                                                                    channeljson=appJson, channelid=-1)
        articlelist_param2 = InitClass().articlelists_params_fields(url2, headers, method, "图文直播",
                                                                    channeljson=appJson, channelid=-2)
        articlelist_param3 = InitClass().articlelists_params_fields(url3, headers, method, "专题",
                                                                    channeljson=appJson, channelid=-3)
        articlelist_param4 = InitClass().articlelists_params_fields(url4, headers, method, "视频",
                                                                    channeljson=appJson, channelid=-4)
        articlelist_param5 = InitClass().articlelists_params_fields(url5, headers, method, "图片",
                                                                    channeljson=appJson, channelid=-5)
        articlelistsparams.append(articlelist_param1)
        articlelistsparams.append(articlelist_param2)
        articlelistsparams.append(articlelist_param3)
        articlelistsparams.append(articlelist_param4)
        articlelistsparams.append(articlelist_param5)

        yield articlelistsparams

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    print(articleslists)
                    if 'rows' in articleslists.keys():
                        for item in articleslists['rows']:
                            articlesparams = setListNewsParam(articlesparams, channelname, channelid, 0, item)

                    if 'hotNewsList' in articleslists.keys():
                        for item1 in articleslists['hotNewsList']:
                            articlesparams = setListNewsParam(articlesparams, channelname, channelid, 0, item1)
                    if 'headlineList' in articleslists.keys():  # banner
                        for item2 in articleslists['headlineList']:
                            articlesparams = setListNewsParam(articlesparams, channelname, channelid, 1, item2)
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        for article in articles:
            article_field = article.get('articelField')
            newsType = article_field.get('newstype')
            if newsType == "QxDataTopic":  # 专题
                url = "http://mengma.jinbw.com.cn/newsList.do"
                headers = {
                    "Host": "mengma.jinbw.com.cn",
                    "Connection": "keep-alive",
                    "Content-Length": "68",
                    "Pragma": "no-cache",
                    "Cache-Control": "no-cache",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36",
                    "Content-Type": "application/json",
                    "X-Requested-With": "com.qingyii.mammoth",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                }
                method = "post"
                appJson = {"page": "1", "pagesize": "10000000", "publishflag": "2",
                           "typeid": article_field.get('workerid')}
                articleparam = InitClass().article_params_fields(url, headers, method, articlejson=appJson,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            elif newsType == "QxDataLiveTxtPic":  # 图文直播
                url = "http://mengma.jinbw.com.cn/showZhibo.do?clienttype=android&clientversion=4.1.0"
                headers = {
                    "Content-Type": "application/json",
                    "Content-Length": "40",
                    "Host": "mengma.jinbw.com.cn",
                    "Connection": "Keep-Alive",
                    "User-Agent": "android-async-http/1.4.4 (http://loopj.com/android-async-http)",
                    "Cookie": "SESSION=0694fd88-0ae8-4424-a0f0-8ed2b36a924d",
                    "Cookie2": "$Version=1",
                    "Accept-Encoding": "gzip",
                }
                method = "post"
                appJson = {"page": 1, "pagesize": 10, "typeid": article_field.get('workerid')}
                articleparam = InitClass().article_params_fields(url, headers, method, articlejson=appJson,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            else:
                url = "http://mengma.jinbw.com.cn/queryNewsInfoById.do?clienttype=android&clientversion=4.1.0 "
                headers = {
                    "Content-Type": "application/json",
                    "Content-Length": "40",
                    "Host": "mengma.jinbw.com.cn",
                    "Connection": "Keep-Alive",
                    "User-Agent": "android-async-http/1.4.4 (http://loopj.com/android-async-http)",
                    "Cookie": "SESSION=0694fd88-0ae8-4424-a0f0-8ed2b36a924d",
                    "Cookie2": "$Version=1",
                    "Accept-Encoding": "gzip",
                }
                method = "post"
                appJson = {"newid": article_field.get('workerid')}
                articleparam = InitClass().article_params_fields(url, headers, method, articlejson=appJson,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            appname = article.get("appname")
            fields = article.get("articleField")
            try:
                contentJson = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                # print(contentJson)
                newsType = fields.get('newstype')
                if newsType == "QxDataTopic":  # 专题
                    topicFields = InitClass().topic_fields()
                    topicFields["_id"] = fields['workerid']  # 专题id，app内唯一标识
                    topicFields["platformName"] = article['appname']  # 平台名字（app名字）
                    # topicFields["platformID"] = ''  #
                    topicFields["channelName"] = fields['channelname']  # 频道名字
                    topicFields["channelID"] = fields['channelID']  # 频道id
                    # topicFields["topicUrl"] = contentJson['data']['shareEntity']['webLink']  # topicUrl
                    topicFields["title"] = fields['title']  #
                    # topicFields["digest"] = contentJson['data']['summary']  # 简介，摘要
                    # topicFields["topicCover"] = [contentJson['imgUrl']]  # list(),
                    # topicFields["pubTime"] = ''  # 时间戳
                    # topicFields["articleNum"] = ''  # 专题内的文章数量
                    # topicFields["newestArticleID"] = ''  # 最新发布的文章id
                    # topicFields["newestPubtime"] = ''  #
                    # topicFields["articleIDs"] = ''  # 专题内的文章ID
                    # topicFields["articlesNumPerHour"] = ''
                    # topicFields["original"] = ''
                    # topicFields["firstMedia"] = ''
                    # topicFields["transPower"] = ''
                    # topicFields["hotDegree"] = ''
                    # topicFields["wordsFreq"] = ''
                    # topicFields["hotDegreeTrend"] = ''
                    # topicFields["emotionTrend"] = ''
                    # topicFields["region"] = ''
                    # topicFields["spreadPath"] = ''
                    # topicFields["createTime"] = contentJson['createTime']
                    # topicFields["updateTime"] = ''
                    topicArticles = self.getTopicArticles(fields['channelname'], fields['channelID'], fields['title'],
                                                          fields['workerid'], contentJson['rows'])
                    articleparams = self.getarticleparams(topicArticles.__next__())
                    articlesres = self.getarticlehtml(articleparams.__next__())
                    self.analyzearticle(articlesres.__next__())
                elif newsType == "QxDataLiveTxtPic":  # 图文直播
                    fields["appname"] = appname  # 应用名称，字符串
                    # fields["channelname"] = fields.get('channelname')  # 频道名称，字符串
                    # fields["channelID"] = fields.get('channelID')  # 频道id，字符串
                    # article_fields["channelType"] = channel_type  # 频道type，字符串
                    # fields["url"] = contentJson['news']['webLink']  # 分享的网址，字符串
                    # fields["title"] = contentJson['news']['title']  # 文章标题，字符串
                    # if 'content' in contentJson.keys():
                    content = ""
                    for contentItem in contentJson['newsTypeRelaList']:
                        content += contentItem['news']['content']
                    fields["content"] = content  # 文章内容，字符串
                    if 'picaddress' in contentJson['news'].keys() and contentJson['news']['picaddress']:
                        fields["articlecovers"] = [
                            f"http://mengma.jinbw.com.cn/{contentJson['news']['picaddress']}"]  # 列表封面，数组
                    # imgList = []
                    # for imgUrl in contentJson['images']:
                    #     imgList.append(imgUrl['url'])
                    # fields["images"] = imgList  # 正文图片，数组
                    # if 'mediaStream' in contentJson.keys() and 'url' in contentJson['mediaStream'].keys():
                    # if fields['url'] is not None and (".mp4" in fields['url'] or ".MP4" in fields['url']):
                    #     fields["videos"] = [fields['url']]  # 视频地址，数组
                    # fields["videocover"] = [contentJson['data']['video']['videoImg']]  # 视频封面，数组
                    # article_fields["width"] = ''  # 视频宽，字符串
                    # article_fields["height"] = ''  # 视频高，字符串
                    # fields["source"] = contentJson['source']  # 文章来源，字符串
                    # fields["pubtime"] = InitClass().date_time_stamp(
                    #     contentJson['publishTime'])  # 发布时间，时间戳（毫秒级，13位）
                    # fields["createtime"] = ''  # 创建时间，时间戳（毫秒级，13位）
                    # fields["updatetime"] = InitClass().date_time_stamp(
                    #     contentJson['updated'])  # 更新时间，时间戳（毫秒级，13位）
                    # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                    # fields["playnum"] = ''  # 播放数，数值
                    # fields["commentnum"] = ''  # 评论数，数值
                    # fields["readnum"] = ''  # 阅读数，数值
                    # fields["trannum"] = ''  # 转发数，数值
                    # fields["sharenum"] = ''  # 分享数，数值
                    # if 'author' in contentJson.keys():
                    #     fields["author"] = contentJson['author']  # 作者，字符串
                    # fields["banner"] = 1  # banner标记，数值（0标识不是，1标识是）
                    # if 7 == bannerItem['contentType']:  # 专题
                    #     article_fields["specialtopic"] = 1
                    #     article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                    # else:
                    #     article_fields["specialtopic"] = 0
                    #     article_fields["workerid"] = bannerItem['contentId']  # 文章id，字符串
                    # fields["workerid"] = contentJson['id']  # 文章id，字符串
                    # article_fields["specialtopic"] = 0  # 是否是专题，数值（0标识不是，1标识是）
                    # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                    # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                else:
                    fields["appname"] = appname  # 应用名称，字符串
                    fields["channelname"] = fields.get('channelname')  # 频道名称，字符串
                    fields["channelID"] = fields.get('channelID')  # 频道id，字符串
                    # article_fields["channelType"] = channel_type  # 频道type，字符串
                    # fields["url"] = contentJson['news']['webLink']  # 分享的网址，字符串
                    fields["title"] = contentJson['news']['title']  # 文章标题，字符串
                    # if 'content' in contentJson.keys():
                    fields["content"] = contentJson['news']['content']  # 文章内容，字符串
                    # if 'picaddress' in contentJson['news'].keys() and contentJson['news']['picaddress']:
                    fields["articlecovers"] = InitClass().get_images(fields["content"])  # 列表封面，数组
                    # imgThumList = []
                    # for imgUrl in contentJson['thumbnails']:
                    #     imgThumList.append(imgUrl['url'])
                    # fields["articlecovers"] = imgThumList  # 列表封面，数组
                    # imgList = []
                    # for imgUrl in contentJson['images']:
                    #     imgList.append(imgUrl['url'])
                    # fields["images"] = imgList  # 正文图片，数组
                    # if 'mediaStream' in contentJson.keys() and 'url' in contentJson['mediaStream'].keys():
                    if fields['url'] is not None and (".mp4" in fields['url'] or ".MP4" in fields['url']):
                        fields["videos"] = [fields['url']]  # 视频地址，数组
                    # fields["videocover"] = [contentJson['data']['video']['videoImg']]  # 视频封面，数组
                    # article_fields["width"] = ''  # 视频宽，字符串
                    # article_fields["height"] = ''  # 视频高，字符串
                    # fields["source"] = contentJson['source']  # 文章来源，字符串
                    # fields["pubtime"] = InitClass().date_time_stamp(
                    #     contentJson['publishTime'])  # 发布时间，时间戳（毫秒级，13位）
                    # fields["createtime"] = ''  # 创建时间，时间戳（毫秒级，13位）
                    # fields["updatetime"] = InitClass().date_time_stamp(
                    #     contentJson['updated'])  # 更新时间，时间戳（毫秒级，13位）
                    # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                    # fields["playnum"] = ''  # 播放数，数值
                    # fields["commentnum"] = ''  # 评论数，数值
                    # fields["readnum"] = ''  # 阅读数，数值
                    # fields["trannum"] = ''  # 转发数，数值
                    # fields["sharenum"] = ''  # 分享数，数值
                    # if 'author' in contentJson.keys():
                    #     fields["author"] = contentJson['author']  # 作者，字符串
                    # fields["banner"] = 1  # banner标记，数值（0标识不是，1标识是）
                    # if 7 == bannerItem['contentType']:  # 专题
                    #     article_fields["specialtopic"] = 1
                    #     article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                    # else:
                    #     article_fields["specialtopic"] = 0
                    #     article_fields["workerid"] = bannerItem['contentId']  # 文章id，字符串
                    # fields["workerid"] = contentJson['id']  # 文章id，字符串
                    # article_fields["specialtopic"] = 0  # 是否是专题，数值（0标识不是，1标识是）
                    # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                    # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                print(json.dumps(fields, indent=4, ensure_ascii=False))
            except Exception as e:
                num += 1
                logging.info(f"错误数量{num},{e}")

    def getTopicArticles(self, channelname, channelid, topicTitle, topicId, topicNewsList):
        articlesparams = []
        for item in topicNewsList:
            try:
                article_fields = InitClass().article_fields()
                article_fields["channelname"] = channelname  # 频道名称，字符串
                article_fields["channelID"] = channelid  # 频道id，字符串
                # article_fields["channelType"] = channel_type  # 频道type，字符串
                if 'h5url' in item.keys():
                    article_fields["url"] = item['h5url']  # 分享的网址，字符串
                if 'title' in item.keys():
                    article_fields["title"] = item['title']  # 文章标题，字符串
                elif 'typename' in item.keys():
                    article_fields["title"] = item['typename']  # 文章标题，字符串
                else:
                    print(item)
                # article_fields["content"] = item['webLink']  # 文章内容，字符串
                # article_fields["articlecovers"] = imgList  # 列表封面，数组
                # article_fields["images"] = ''  # 正文图片，数组
                # article_fields["videocover"] = [item['videoImg']]  # 视频封面，数组
                # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                # article_fields["width"] = ''  # 视频宽，字符串
                # article_fields["height"] = ''  # 视频高，字符串
                if 'source' in item.keys():
                    article_fields["source"] = item['source']  # 文章来源，字符串
                if 'publishdate' in item.keys():
                    article_fields["pubtime"] = item['publishdate']  # 发布时间，时间戳（毫秒级，13位）
                if 'createdate' in item.keys():
                    article_fields["createtime"] = item['createdate']  # 创建时间，时间戳（毫秒级，13位）
                # article_fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
                # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                # article_fields["playnum"] = ''  # 播放数，数值
                # article_fields["commentnum"] = item['commentNum']  # 评论数，数值
                # article_fields["readnum"] = ''  # 阅读数，数值
                # article_fields["trannum"] = ''  # 转发数，数值
                # article_fields["sharenum"] = ''  # 分享数，数值
                # article_fields["author"] = ''  # 作者，字符串
                # article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                if 'newid' in item.keys() and item['newid'] is not None:
                    article_fields["workerid"] = item['newid']  # 文章id，字符串
                elif 'typeid' in item.keys() and item['typeid'] is not None:
                    article_fields["workerid"] = item['typeid']  # 文章标题，字符串
                else:
                    print(item)
                article_fields["specialtopic"] = 1  # 是否是专题，数值（0标识不是，1标识是）
                article_fields["topicid"] = topicId  # 专题id，字符串
                article_fields["topicTitle"] = topicTitle  # 专题id，字符串
                article_fields["newstype"] = "QxDataDef"  # 自己添加新闻类型
                articleparam = InitClass().article_list_fields()
                articleparam["articelField"] = article_fields
                articlesparams.append(articleparam)
            except Exception as e:
                logging.info(e)
            articleparam = InitClass().article_list_fields()
            articleparam["articelField"] = article_fields
            articlesparams.append(articleparam)

        yield articlesparams

    def run(self):
        appParamsList = self.get_app_params().__next__()
        channelsres = {}
        for appParams in appParamsList:
            name = appParams['appurl']
            value = self.getchannels(appParams).__next__()
            channelsres[name] = value
        channelsparams = self.analyze_channel(channelsres)
        articlelistparames = self.getarticlelistparams(channelsparams.__next__())
        articleslistsres = self.getarticlelists(articlelistparames.__next__())
        articles = self.analyze_articlelists(articleslistsres.__next__())
        articleparams = self.getarticleparams(articles.__next__())
        articlesres = self.getarticlehtml(articleparams.__next__())
        self.analyzearticle(articlesres.__next__())


if __name__ == '__main__':
    appspider = MengMaXinWen("猛犸新闻")
    appspider.run()
