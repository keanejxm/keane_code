# -*- encoding:utf-8 -*-
"""
@功能:湖北日报解析模板
@AUTHOR：jovan
@文件名：HuBeiRiBao.py
@时间：2020年12月22日 15:58:24
"""

import json
import logging
import time

import requests

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass

topicParamList = []


def setListNewsParam(channelname, channelid, banner, item):
    article_fields = InitClass().article_fields()
    article_fields["channelname"] = channelname  # 频道名称，字符串
    article_fields["channelID"] = channelid  # 频道id，字符串
    # article_fields["channelType"] = channel_type  # 频道type，字符串
    # article_fields["url"] = item['jsonUrl']  # 分享的网址，字符串
    article_fields["title"] = item['title']  # 文章标题，字符串
    if (item['type'] == 4 or item['type'] == 5) and \
            'webLink' in item.keys() and isinstance(item['webLink'], str) and len(item['webLink']):
        article_fields["content"] = item['webLink']  # 文章内容，字符串
    # if item['type'] == 5:
    #     print(item)
    # if item['isLive'] == 2:
    #     print(item)
    imgList = []
    for img in item['titlePics']:
        imgList.append(img['url'])
    article_fields["articlecovers"] = imgList  # 列表封面，数组
    # article_fields["images"] = ''  # 正文图片，数组
    if isinstance(item['videoImg'], str) and len(item['videoImg']):
        article_fields["videocover"] = [item['videoImg']]  # 视频封面，数组
    if len(item['videoUrl']):
        article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
    # article_fields["width"] = ''  # 视频宽，字符串
    # article_fields["height"] = ''  # 视频高，字符串
    # article_fields["source"] = ''  # 文章来源，字符串
    # article_fields["pubtime"] = ''  # 发布时间，时间戳（毫秒级，13位）
    # article_fields["createtime"] = ''  # 创建时间，时间戳（毫秒级，13位）
    # article_fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
    # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
    # article_fields["playnum"] = ''  # 播放数，数值
    article_fields["commentnum"] = item['commentNum']  # 评论数，数值
    # article_fields["readnum"] = ''  # 阅读数，数值
    # article_fields["trannum"] = ''  # 转发数，数值
    # article_fields["sharenum"] = ''  # 分享数，数值
    # article_fields["author"] = ''  # 作者，字符串
    article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
    article_fields["workerid"] = item['contentid']  # 文章id，字符串
    # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
    # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
    if item['isLive'] != 0 and item['type'] == 1:
        # print('isLive', item['isLive'])
        article_fields["newstype"] = -1  # 自己添加新闻类型，这个是底部直播tab中的江报视频
    else:
        article_fields["newstype"] = item['type']  # 自己添加新闻类型
    # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
    return article_fields


class JiangXiXinWen(Appspider):

    @staticmethod
    def get_app_params():
        url1 = "http://www.jxxw.com.cn/app/v3/channel/index?modelid=1"
        url2 = "http://www.jxxw.com.cn/app/v3/channel/index?modelid=2"
        headers = {
            "platform": "2",
            "deviceid": "ffffffff-ed4b-3692-0033-c5870033c587",
            "version": "5.5.1",
            "siteid": "55",
            "Host": "www.jxxw.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.9.1",
        }
        method = "get"

        app_params1 = InitClass().app_params(url1, headers, method)
        app_params2 = InitClass().app_params(url2, headers, method)

        yield [app_params1, app_params2]

    def analyze_channel(self, channelsres):
        print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            if 'http://www.jxxw.com.cn/app/v3/channel/index?modelid=1' == k:
                channelList = json.loads(v)
                for channelData in channelList['data']['sub']:
                    for channel in channelData['data']:
                        if 'url' in channel.keys() and len(channel['url']):
                            print("频道内容是网址:", channel)
                        else:
                            channelid = channel['channelId']
                            channelname = channel['channelName']
                            channelType = channel['type']
                            channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channelType,
                                                                      categoryid=1)
                            channelparams.append(channelparam)
                for channel in channelList['data']['user']:
                    if 'url' in channel.keys() and len(channel['url']):
                        print("频道内容是网址:", channel)
                    else:
                        channelid = channel['channelId']
                        channelname = channel['channelName']
                        channelType = channel['type']
                        channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channelType,
                                                                  categoryid=1)
                        channelparams.append(channelparam)
            if 'http://www.jxxw.com.cn/app/v3/channel/index?modelid=2' == k:
                channelList = json.loads(v)
                for channel in channelList['data']['main']:
                    if 'url' in channel.keys() and len(channel['url']):
                        print("频道内容是网址:", channel)
                    else:
                        channelid = channel['channelId']
                        channelname = channel['channelName']
                        channelType = channel['type']
                        channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channelType,
                                                                  categoryid=2)
                        channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channelType = channel.get("channeltype")
            categoryid = channel.get("categoryid")
            url = "http://www.jxxw.com.cn/app/v4/news/index"
            headers = {
                "timestamp": str(int(time.time())),
                "platform": "2",
                "deviceid": "ffffffff-ed4b-3692-0033-c5870033c587",
                "version": "5.5.1",
                "siteid": "55",
                "Host": "www.jxxw.com.cn",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.9.1",
            }
            method = "get"
            data = {
                "modelid": categoryid,
                "categoryId": channelid,
                "page": "1",
                "type": channelType,
            }
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                       channelid=channelid)
            articlelistsparams.append(articlelist_param)

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
                    if 'data' in articleslists.keys():
                        for item in articleslists['data']:
                            if 'falshList' in item.keys() and len(item['falshList']):
                                for itemBanner in item['falshList']:
                                    article_fields = setListNewsParam(channelname, channelid, 1, itemBanner)
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                            elif 'topicList' in item.keys() and len(item['topicList']):
                                for itemTopic in item['topicList']:
                                    article_fields = setListNewsParam(channelname, channelid, 0, itemTopic)
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                            else:
                                if item['contentid'] == 0:
                                    print('这个不是新闻是nav:', item)
                                else:
                                    article_fields = setListNewsParam(channelname, channelid, 0, item)
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                    else:
                        print(articleslists)
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
            if newsType == 1:  # 普通新闻
                url = f"http://www.jxxw.com.cn/app/v4/news/show?modelid=1&contentid={article_field.get('workerid')}"
                headers = {
                    "platform": "2",
                    "deviceid": "ffffffff-ed4b-3692-0033-c5870033c587",
                    "version": "5.5.1",
                    "siteid": "55",
                    "Host": "www.jxxw.com.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.9.1",
                }
                method = "get"
                articleparam = InitClass().article_params_fields(url, headers, method,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            elif newsType == 2:  # 专题
                url = f"http://www.jxxw.com.cn/app/topic/index?topicId={article_field.get('workerid')}&page=1"
                headers = {
                    "platform": "2",
                    "deviceid": "ffffffff-ed4b-3692-0033-c5870033c587",
                    "version": "5.5.1",
                    "siteid": "55",
                    "Host": "www.jxxw.com.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.9.1",
                }
                method = "get"
                articleparam = InitClass().article_params_fields(url, headers, method,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            elif newsType == 3:  # 图片新闻
                url = f"http://www.jxxw.com.cn/app/v4/news/picture?contentid={article_field.get('workerid')}"
                headers = {
                    "platform": "2",
                    "deviceid": "ffffffff-ed4b-3692-0033-c5870033c587",
                    "version": "5.5.1",
                    "siteid": "55",
                    "Host": "www.jxxw.com.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.9.1",
                }
                method = "get"
                articleparam = InitClass().article_params_fields(url, headers, method,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            elif newsType == 4:  # 外链新闻
                print("外链新闻===", article)
            elif newsType == 5:  # 图文直播
                print("图文直播===", article)
            elif newsType == -1:  # 这个是底部直播tab中的江报视频
                url = f"http://www.jxxw.com.cn/app/v4/news/showVideo?modelid=2&contentid={article_field.get('workerid')}"
                headers = {
                    "platform": "2",
                    "deviceid": "ffffffff-ed4b-3692-0033-c5870033c587",
                    "version": "5.5.1",
                    "siteid": "55",
                    "Host": "www.jxxw.com.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.9.1",
                }
                method = "get"
                articleparam = InitClass().article_params_fields(url, headers, method,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            else:
                print('未识别类型', newsType, article_field.get('channelname'), article_field.get('title'))
        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            appname = article.get("appname")
            fields = article.get("articleField")
            try:
                contentJson = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                print(contentJson)
                newsType = fields.get('newstype')
                if newsType == 1:  # 普通新闻
                    print(contentJson)
                    fields["appname"] = appname  # 应用名称，字符串
                    # fields["channelname"] = fields.get('channelname')  # 频道名称，字符串
                    # fields["channelID"] = fields.get('channelID')  # 频道id，字符串
                    # article_fields["channelType"] = channel_type  # 频道type，字符串
                    fields["url"] = contentJson['data']['share']['webLink']  # 分享的网址，字符串
                    # fields["title"] = contentJson['title']  # 文章标题，字符串
                    fields["content"] = contentJson['data']['data']  # 文章内容，字符串
                    # imgThumList = []
                    # for imgUrl in contentJson['thumbnails']:
                    #     imgThumList.append(imgUrl['url'])
                    # fields["articlecovers"] = imgThumList  # 列表封面，数组
                    # imgList = []
                    # for imgUrl in contentJson['images']:
                    #     imgList.append(imgUrl['url'])
                    # fields["images"] = imgList  # 正文图片，数组
                    # if 'mediaStream' in contentJson.keys() and 'url' in contentJson['mediaStream'].keys():
                    #     fields["videos"] = [contentJson['mediaStream']['url']]  # 视频地址，数组
                    # fields["videocover"] = [contentJson['data']['news_detail']['video_cover']]  # 视频封面，数组
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
                elif newsType == 2:  # 专题
                    print(contentJson)
                    topicFields = InitClass().topic_fields()
                    topicFields["_id"] = fields['workerid']  # 专题id，app内唯一标识
                    topicFields["platformName"] = article['appname']  # 平台名字（app名字）
                    # topicFields["platformID"] = ''  #
                    topicFields["channelName"] = fields['channelname']  # 频道名字
                    topicFields["channelID"] = fields['channelID']  # 频道id
                    topicFields["topicUrl"] = contentJson['data']['shareEntity']['webLink']  # topicUrl
                    # topicFields["title"] = fields['title']  #
                    topicFields["digest"] = contentJson['data']['summary']  # 简介，摘要
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
                                                          fields['workerid'], contentJson['data']['newsList'])
                    articleparams = self.getarticleparams(topicArticles.__next__())
                    articlesres = self.getarticlehtml(articleparams.__next__())
                    self.analyzearticle(articlesres.__next__())
                elif newsType == 3:  # 图片新闻
                    print(contentJson)
                    fields["appname"] = appname  # 应用名称，字符串
                    # fields["channelname"] = fields.get('channelname')  # 频道名称，字符串
                    # fields["channelID"] = fields.get('channelID')  # 频道id，字符串
                    # article_fields["channelType"] = channel_type  # 频道type，字符串
                    # fields["url"] = contentJson['shareUrl']  # 分享的网址，字符串
                    # fields["title"] = contentJson['title']  # 文章标题，字符串
                    # if 'content' in contentJson.keys():
                    #     fields["content"] = contentJson['content']  # 文章内容，字符串
                    # imgThumList = []
                    # for imgUrl in contentJson['thumbnails']:
                    #     imgThumList.append(imgUrl['url'])
                    # fields["articlecovers"] = imgThumList  # 列表封面，数组
                    imgList = []
                    for imgUrl in contentJson['data']['Gallerys']:
                        imgList.append(imgUrl['imageURL'])
                    fields["images"] = imgList  # 正文图片，数组
                    # if 'mediaStream' in contentJson.keys() and 'url' in contentJson['mediaStream'].keys():
                    #     fields["videos"] = [contentJson['mediaStream']['url']]  # 视频地址，数组
                    # fields["videocover"] = [contentJson['data']['news_detail']['video_cover']]  # 视频封面，数组
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
                elif newsType == 4:  # 外链新闻
                    print("外链新闻===")
                    fields["appname"] = appname  # 应用名称，字符串
                elif newsType == 5:  # 图文直播
                    print("图文直播===")
                    fields["appname"] = appname  # 应用名称，字符串
                elif newsType == -1:  # 这个是底部直播tab中的江报视频
                    print(contentJson)
                    fields["appname"] = appname  # 应用名称，字符串
                    # fields["channelname"] = fields.get('channelname')  # 频道名称，字符串
                    # fields["channelID"] = fields.get('channelID')  # 频道id，字符串
                    # article_fields["channelType"] = channel_type  # 频道type，字符串
                    fields["url"] = contentJson['data']['share']['webLink']  # 分享的网址，字符串
                    # fields["title"] = contentJson['title']  # 文章标题，字符串
                    # if 'content' in contentJson.keys():
                    fields["content"] = contentJson['data']['data']  # 文章内容，字符串
                    # imgThumList = []
                    # for imgUrl in contentJson['thumbnails']:
                    #     imgThumList.append(imgUrl['url'])
                    # fields["articlecovers"] = imgThumList  # 列表封面，数组
                    # imgList = []
                    # for imgUrl in contentJson['images']:
                    #     imgList.append(imgUrl['url'])
                    # fields["images"] = imgList  # 正文图片，数组
                    # if 'mediaStream' in contentJson.keys() and 'url' in contentJson['mediaStream'].keys():
                    fields["videos"] = [contentJson['data']['video']['videoUrl']]  # 视频地址，数组
                    fields["videocover"] = [contentJson['data']['video']['videoImg']]  # 视频封面，数组
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
                    print('未识别类型', contentJson)
                print(json.dumps(fields, indent=4, ensure_ascii=False))
            except Exception as e:
                num += 1
                logging.info(f"错误数量{num},{e}")

    def getTopicArticles(self, channelname, channelid, topicTitle, topicId, topicNewsList):
        articlesparams = []
        for item in topicNewsList:
            article_fields = InitClass().article_fields()
            article_fields["channelname"] = channelname  # 频道名称，字符串
            article_fields["channelID"] = channelid  # 频道id，字符串
            # article_fields["channelType"] = channel_type  # 频道type，字符串
            # article_fields["url"] = item['jsonUrl']  # 分享的网址，字符串
            article_fields["title"] = item['title']  # 文章标题，字符串
            if (item['type'] == 4 or item['type'] == 5) and \
                    'webLink' in item.keys() and isinstance(item['webLink'], str) and len(item['webLink']):
                article_fields["content"] = item['webLink']  # 文章内容，字符串
            # if item['type'] == 5:
            #     print(item)
            # if item['isLive'] == 2:
            #     print(item)
            imgList = []
            for img in item['titlePics']:
                imgList.append(img['url'])
            article_fields["articlecovers"] = imgList  # 列表封面，数组
            # article_fields["images"] = ''  # 正文图片，数组
            if isinstance(item['videoImg'], str) and len(item['videoImg']):
                article_fields["videocover"] = [item['videoImg']]  # 视频封面，数组
            if len(item['videoUrl']):
                article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
            # article_fields["width"] = ''  # 视频宽，字符串
            # article_fields["height"] = ''  # 视频高，字符串
            # article_fields["source"] = ''  # 文章来源，字符串
            # article_fields["pubtime"] = ''  # 发布时间，时间戳（毫秒级，13位）
            # article_fields["createtime"] = ''  # 创建时间，时间戳（毫秒级，13位）
            # article_fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
            # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
            # article_fields["playnum"] = ''  # 播放数，数值
            article_fields["commentnum"] = item['commentNum']  # 评论数，数值
            # article_fields["readnum"] = ''  # 阅读数，数值
            # article_fields["trannum"] = ''  # 转发数，数值
            # article_fields["sharenum"] = ''  # 分享数，数值
            # article_fields["author"] = ''  # 作者，字符串
            article_fields["banner"] = 0  # banner标记，数值（0标识不是，1标识是）
            article_fields["workerid"] = item['contentid']  # 文章id，字符串
            article_fields["specialtopic"] = 1  # 是否是专题，数值（0标识不是，1标识是）
            article_fields["topicid"] = topicId  # 专题id，字符串
            article_fields["topicTitle"] = topicTitle  # 专题id，字符串
            if item['isLive'] != 0 and item['type'] == 1:
                # print('isLive', item['isLive'])
                article_fields["newstype"] = -1  # 自己添加新闻类型，这个是底部直播tab中的江报视频
            else:
                article_fields["newstype"] = item['type']  # 自己添加新闻类型
            # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
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
    appspider = JiangXiXinWen("江西新闻")
    appspider.run()
