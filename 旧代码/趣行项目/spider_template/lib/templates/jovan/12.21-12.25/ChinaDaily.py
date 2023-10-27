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


class ChinaDaily(Appspider):

    @staticmethod
    def get_app_params():
        url1 = "https://enapp.chinadaily.com.cn/custom-columns.json"
        headers1 = {
            "If-Modified-Since": time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.localtime()),
            "User-Agent": "okhttp/4.2.0 Build/1.0 (HUAWEI; ALP-AL00; Android 10) Emulator/2.0 (false) Mozilla/5.0 (Linux; Android 10; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 CDAndroid/7.5.2 (huawei; 6000030)",
            "Cache-Control": "no-store",
            "Host": "enapp.chinadaily.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        method1 = "get"
        app_params1 = InitClass().app_params(url1, headers1, method1)

        yield [app_params1]

    def analyze_channel(self, channelsres):
        print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            if 'https://enapp.chinadaily.com.cn/custom-columns.json' == k:
                # channelList = json.loads(v)
                # for channel in channelList:
                #     if 'children' in channel.keys() and len(channel['children']):
                #         for channelChild in channel['children']:
                #             channelid = channelChild['uuid']
                #             channelname = channelChild['name']
                #             channelType = channelChild['type']
                #             channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channelType)
                #             channelparams.append(channelparam)
                #     else:
                #         channelid = channel['uuid']
                #         channelname = channel['name']
                #         channelType = channel['type']
                #         channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channelType)
                #         channelparams.append(channelparam)
                # channelparam1 = InitClass().channel_fields('5a001da1a3108b7ccb3762a9', 'Home', channeltype=0)
                # channelparams.append(channelparam1)
                # channelparam2 = InitClass().channel_fields('5a0029f8a3108b7ccb3762cd', 'Photos', channeltype=0)
                # channelparams.append(channelparam2)
                # channelparam2 = InitClass().channel_fields('5a001d84a3108b7ccb3762a8', 'Audio', channeltype=0)
                # channelparams.append(channelparam2)
                # channelparam2 = InitClass().channel_fields('5a001d5ca3108b7ccb3762a6', 'Video', channeltype=0)
                # channelparams.append(channelparam2)
                # channelparam2 = InitClass().channel_fields('5f816e62a310b0a661bf17dc', 'Live', channeltype=0)
                # channelparams.append(channelparam2)
                channelparam3 = InitClass().channel_fields('5ddc858ea310aba8ca8cc3dc', 'Qinghai special',
                                                           channeltype=1)
                channelparams.append(channelparam3)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channelType = channel.get("channeltype")
            if 0 == channelType:
                url = f"https://enapp.chinadaily.com.cn/channels/enapp/columns/{channelid}/stories.json"
                headers = {
                    "If-Modified-Since": time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.localtime()),
                    "User-Agent": "okhttp/4.2.0 Build/1.0 (HUAWEI; ALP-AL00; Android 10) Emulator/2.0 (false) Mozilla/5.0 (Linux; Android 10; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 CDAndroid/7.5.2 (huawei; 6000030)",
                    "Cache-Control": "no-store",
                    "Host": "enapp.chinadaily.com.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                method = "get"
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           channelid=channelid)
                articlelistsparams.append(articlelist_param)
            elif 1 == channelType:
                # topicParamList.clear()
                topicParamList.append(channel)
            else:
                print(channel)
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
                    if 'blocks' in articleslists.keys():
                        for item in articleslists['blocks']:
                            if len(item['stories']):
                                for story in item['stories']:
                                    article_fields = InitClass().article_fields()
                                    article_fields["channelname"] = channelname  # 频道名称，字符串
                                    article_fields["channelID"] = channelid  # 频道id，字符串
                                    # article_fields["channelType"] = channel_type  # 频道type，字符串
                                    article_fields["url"] = story['jsonUrl']  # 分享的网址，字符串
                                    article_fields["title"] = story['title']  # 文章标题，字符串
                                    # article_fields["content"] = ''  # 文章内容，字符串
                                    # article_fields["articlecovers"] = item1['image_list']  # 列表封面，数组
                                    # article_fields["images"] = ''  # 正文图片，数组
                                    # article_fields["videos"] = ''  # 视频地址，数组
                                    # article_fields["videocover"] = ''  # 视频封面，数组
                                    # article_fields["width"] = ''  # 视频宽，字符串
                                    # article_fields["height"] = ''  # 视频高，字符串
                                    # article_fields["source"] = ''  # 文章来源，字符串
                                    # article_fields["pubtime"] = ''  # 发布时间，时间戳（毫秒级，13位）
                                    # article_fields["createtime"] = ''  # 创建时间，时间戳（毫秒级，13位）
                                    # article_fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
                                    # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                                    # article_fields["playnum"] = ''  # 播放数，数值
                                    # article_fields["commentnum"] = ''  # 评论数，数值
                                    # article_fields["readnum"] = ''  # 阅读数，数值
                                    # article_fields["trannum"] = ''  # 转发数，数值
                                    # article_fields["sharenum"] = ''  # 分享数，数值
                                    # article_fields["author"] = ''  # 作者，字符串
                                    article_fields["banner"] = 1  # banner标记，数值（0标识不是，1标识是）
                                    article_fields["workerid"] = story['id']  # 文章id，字符串
                                    # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                                    # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                            else:
                                print(item)
                    if 'stories' in articleslists.keys():
                        for item in articleslists['stories']:
                            article_fields = InitClass().article_fields()
                            article_fields["channelname"] = channelname  # 频道名称，字符串
                            article_fields["channelID"] = channelid  # 频道id，字符串
                            # article_fields["channelType"] = channel_type  # 频道type，字符串
                            article_fields["url"] = item['jsonUrl']  # 分享的网址，字符串
                            article_fields["title"] = item['title']  # 文章标题，字符串
                            # article_fields["content"] = ''  # 文章内容，字符串
                            # article_fields["articlecovers"] = item1['image_list']  # 列表封面，数组
                            # article_fields["images"] = ''  # 正文图片，数组
                            # article_fields["videos"] = ''  # 视频地址，数组
                            # article_fields["videocover"] = ''  # 视频封面，数组
                            # article_fields["width"] = ''  # 视频宽，字符串
                            # article_fields["height"] = ''  # 视频高，字符串
                            # article_fields["source"] = ''  # 文章来源，字符串
                            # article_fields["pubtime"] = ''  # 发布时间，时间戳（毫秒级，13位）
                            # article_fields["createtime"] = ''  # 创建时间，时间戳（毫秒级，13位）
                            # article_fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
                            # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                            # article_fields["playnum"] = ''  # 播放数，数值
                            # article_fields["commentnum"] = ''  # 评论数，数值
                            # article_fields["readnum"] = ''  # 阅读数，数值
                            # article_fields["trannum"] = ''  # 转发数，数值
                            # article_fields["sharenum"] = ''  # 分享数，数值
                            # article_fields["author"] = ''  # 作者，字符串
                            article_fields["banner"] = 0  # banner标记，数值（0标识不是，1标识是）
                            article_fields["workerid"] = item['id']  # 文章id，字符串
                            # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                            # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                            articleparam = InitClass().article_list_fields()
                            articleparam["articelField"] = article_fields
                            articlesparams.append(articleparam)
                    else:
                        print(articleslists)
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")
        for topicParam in topicParamList:
            article_fields = InitClass().article_fields()
            article_fields["channelname"] = topicParam['channelname']  # 频道名称，字符串
            article_fields["channelID"] = topicParam['channelid']  # 频道id，字符串
            article_fields["channelType"] = topicParam['channeltype']  # 频道type，字符串
            # article_fields["url"] = item['jsonUrl']  # 分享的网址，字符串
            article_fields["title"] = topicParam['channelname']  # 文章标题，字符串
            # article_fields["content"] = ''  # 文章内容，字符串
            # article_fields["articlecovers"] = item1['image_list']  # 列表封面，数组
            # article_fields["images"] = ''  # 正文图片，数组
            # article_fields["videos"] = ''  # 视频地址，数组
            # article_fields["videocover"] = ''  # 视频封面，数组
            # article_fields["width"] = ''  # 视频宽，字符串
            # article_fields["height"] = ''  # 视频高，字符串
            # article_fields["source"] = ''  # 文章来源，字符串
            # article_fields["pubtime"] = ''  # 发布时间，时间戳（毫秒级，13位）
            # article_fields["createtime"] = ''  # 创建时间，时间戳（毫秒级，13位）
            # article_fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
            # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
            # article_fields["playnum"] = ''  # 播放数，数值
            # article_fields["commentnum"] = ''  # 评论数，数值
            # article_fields["readnum"] = ''  # 阅读数，数值
            # article_fields["trannum"] = ''  # 转发数，数值
            # article_fields["sharenum"] = ''  # 分享数，数值
            # article_fields["author"] = ''  # 作者，字符串
            article_fields["banner"] = 0  # banner标记，数值（0标识不是，1标识是）
            article_fields["workerid"] = topicParam['channelid']  # 文章id，字符串
            article_fields["specialtopic"] = 0  # 是否是专题，数值（0标识不是，1标识是）
            article_fields["topicid"] = topicParam['channelid']  # 专题id，字符串
            article_fields["topicList"] = 1  # 自己添加参数，标识是专题列表
            articleparam = InitClass().article_list_fields()
            articleparam["articelField"] = article_fields
            articlesparams.append(articleparam)

        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        for article in articles:
            article_field = article.get('articelField')
            topicList = article_field.get('topicList')
            if topicList == 1:
                url = f"https://enapp.chinadaily.com.cn/specials/{article_field.get('topicid')}/stories.json"
                headers = {
                    "If-Modified-Since": time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.localtime()),
                    "User-Agent": "okhttp/4.2.0 Build/1.0 (HUAWEI; ALP-AL00; Android 10) Emulator/2.0 (false) Mozilla/5.0 (Linux; Android 10; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 CDAndroid/7.5.2 (huawei; 6000030)",
                    "Cache-Control": "no-store",
                    "Host": "enapp.chinadaily.com.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                method = "get"
                articleparam = InitClass().article_params_fields(url, headers, method,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            else:
                url = article_field.get('url')
                headers = {
                    "User-Agent": "okhttp/4.2.0 Build/1.0 (HUAWEI; ALP-AL00; Android 10) Emulator/2.0 (false) Mozilla/5.0 (Linux; Android 10; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 CDAndroid/7.5.2 (huawei; 6000030)",
                    "Cache-Control": "no-store",
                    "Host": "enapp.chinadaily.com.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                method = "get"
                articleparam = InitClass().article_params_fields(url, headers, method,
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
                print(contentJson)
                topicList = fields.get('topicList')
                if topicList == 1:  # 专题
                    print(contentJson)
                    topicFields = InitClass().topic_fields()
                    topicFields["_id"] = fields['workerid']  # 专题id，app内唯一标识
                    topicFields["platformName"] = article['appname']  # 平台名字（app名字）
                    topicFields["platformID"] = ''  #
                    topicFields["channelName"] = fields['channelname']  # 频道名字
                    topicFields["channelID"] = fields['channelID']  # 频道id
                    # topicFields["topicUrl"] = contentJson['blocks']['stories']  # topicUrl
                    topicFields["title"] = fields['title']  #
                    # topicFields["digest"] = contentJson['introduction']  # 简介，摘要
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
                                                          fields['workerid'], contentJson['blocks'],
                                                          contentJson['stories'])
                    articleparams = self.getarticleparams(topicArticles.__next__())
                    articlesres = self.getarticlehtml(articleparams.__next__())
                    self.analyzearticle(articlesres.__next__())
                else:
                    print(contentJson)
                    fields["appname"] = appname  # 应用名称，字符串
                    fields["channelname"] = fields.get('channelname')  # 频道名称，字符串
                    fields["channelID"] = fields.get('channelID')  # 频道id，字符串
                    # article_fields["channelType"] = channel_type  # 频道type，字符串
                    fields["url"] = contentJson['shareUrl']  # 分享的网址，字符串
                    fields["title"] = contentJson['title']  # 文章标题，字符串
                    if 'content' in contentJson.keys():
                        fields["content"] = contentJson['content']  # 文章内容，字符串
                    imgThumList = []
                    for imgUrl in contentJson['thumbnails']:
                        imgThumList.append(imgUrl['url'])
                    fields["articlecovers"] = imgThumList  # 列表封面，数组
                    imgList = []
                    for imgUrl in contentJson['images']:
                        imgList.append(imgUrl['url'])
                    fields["images"] = imgList  # 正文图片，数组
                    if 'mediaStream' in contentJson.keys() and 'url' in contentJson['mediaStream'].keys():
                        fields["videos"] = [contentJson['mediaStream']['url']]  # 视频地址，数组
                    # fields["videocover"] = [contentJson['data']['news_detail']['video_cover']]  # 视频封面，数组
                    # article_fields["width"] = ''  # 视频宽，字符串
                    # article_fields["height"] = ''  # 视频高，字符串
                    fields["source"] = contentJson['source']  # 文章来源，字符串
                    fields["pubtime"] = InitClass().date_time_stamp(
                        contentJson['publishTime'])  # 发布时间，时间戳（毫秒级，13位）
                    # fields["createtime"] = ''  # 创建时间，时间戳（毫秒级，13位）
                    fields["updatetime"] = InitClass().date_time_stamp(
                        contentJson['updated'])  # 更新时间，时间戳（毫秒级，13位）
                    # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                    # fields["playnum"] = ''  # 播放数，数值
                    # fields["commentnum"] = ''  # 评论数，数值
                    # fields["readnum"] = ''  # 阅读数，数值
                    # fields["trannum"] = ''  # 转发数，数值
                    # fields["sharenum"] = ''  # 分享数，数值
                    if 'author' in contentJson.keys():
                        fields["author"] = contentJson['author']  # 作者，字符串
                    # fields["banner"] = 1  # banner标记，数值（0标识不是，1标识是）
                    # if 7 == bannerItem['contentType']:  # 专题
                    #     article_fields["specialtopic"] = 1
                    #     article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                    # else:
                    #     article_fields["specialtopic"] = 0
                    #     article_fields["workerid"] = bannerItem['contentId']  # 文章id，字符串
                    fields["workerid"] = contentJson['id']  # 文章id，字符串
                    # article_fields["specialtopic"] = 0  # 是否是专题，数值（0标识不是，1标识是）
                    # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                    # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                print(json.dumps(fields, indent=4, ensure_ascii=False))
            except Exception as e:
                num += 1
                logging.info(f"错误数量{num},{e}")

    def getTopicArticles(self, channelname, channelid, topicTitle, topicId, blocks, topicNewsList):
        articlesparams = []
        for item in blocks:
            if len(item['stories']):
                for story in item['stories']:
                    article_fields = InitClass().article_fields()
                    article_fields["channelname"] = channelname  # 频道名称，字符串
                    article_fields["channelID"] = channelid  # 频道id，字符串
                    # article_fields["channelType"] = channel_type  # 频道type，字符串
                    article_fields["url"] = story['jsonUrl']  # 分享的网址，字符串
                    article_fields["title"] = story['title']  # 文章标题，字符串
                    # article_fields["content"] = ''  # 文章内容，字符串
                    # article_fields["articlecovers"] = item1['image_list']  # 列表封面，数组
                    # article_fields["images"] = ''  # 正文图片，数组
                    # article_fields["videos"] = ''  # 视频地址，数组
                    # article_fields["videocover"] = ''  # 视频封面，数组
                    # article_fields["width"] = ''  # 视频宽，字符串
                    # article_fields["height"] = ''  # 视频高，字符串
                    # article_fields["source"] = ''  # 文章来源，字符串
                    # article_fields["pubtime"] = ''  # 发布时间，时间戳（毫秒级，13位）
                    # article_fields["createtime"] = ''  # 创建时间，时间戳（毫秒级，13位）
                    # article_fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
                    # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                    # article_fields["playnum"] = ''  # 播放数，数值
                    # article_fields["commentnum"] = ''  # 评论数，数值
                    # article_fields["readnum"] = ''  # 阅读数，数值
                    # article_fields["trannum"] = ''  # 转发数，数值
                    # article_fields["sharenum"] = ''  # 分享数，数值
                    # article_fields["author"] = ''  # 作者，字符串
                    # article_fields["banner"] = 1  # banner标记，数值（0标识不是，1标识是）
                    article_fields["workerid"] = story['id']  # 文章id，字符串
                    article_fields["specialtopic"] = 1  # 是否是专题，数值（0标识不是，1标识是）
                    article_fields["topicid"] = topicId  # 专题id，字符串
                    article_fields["topicTitle"] = topicTitle  # 专题id，字符串
                    articleparam = InitClass().article_list_fields()
                    articleparam["articelField"] = article_fields
                    articlesparams.append(articleparam)
            else:
                print(item)
        for topicNews in topicNewsList:
            article_fields = InitClass().article_fields()
            article_fields["channelname"] = channelname  # 频道名称，字符串
            article_fields["channelID"] = channelid  # 频道id，字符串
            # article_fields["channelType"] = channel_type  # 频道type，字符串
            article_fields["url"] = topicNews['jsonUrl']  # 分享的网址，字符串
            article_fields["title"] = topicNews['title']  # 文章标题，字符串
            # article_fields["content"] = ''  # 文章内容，字符串
            # article_fields["articlecovers"] = item1['image_list']  # 列表封面，数组
            # article_fields["images"] = ''  # 正文图片，数组
            # article_fields["videos"] = ''  # 视频地址，数组
            # article_fields["videocover"] = ''  # 视频封面，数组
            # article_fields["width"] = ''  # 视频宽，字符串
            # article_fields["height"] = ''  # 视频高，字符串
            # article_fields["source"] = ''  # 文章来源，字符串
            # article_fields["pubtime"] = ''  # 发布时间，时间戳（毫秒级，13位）
            # article_fields["createtime"] = ''  # 创建时间，时间戳（毫秒级，13位）
            # article_fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
            # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
            # article_fields["playnum"] = ''  # 播放数，数值
            # article_fields["commentnum"] = ''  # 评论数，数值
            # article_fields["readnum"] = ''  # 阅读数，数值
            # article_fields["trannum"] = ''  # 转发数，数值
            # article_fields["sharenum"] = ''  # 分享数，数值
            # article_fields["author"] = ''  # 作者，字符串
            # article_fields["banner"] = 1  # banner标记，数值（0标识不是，1标识是）
            article_fields["workerid"] = topicNews['id']  # 文章id，字符串
            article_fields["specialtopic"] = 1  # 是否是专题，数值（0标识不是，1标识是）
            article_fields["topicid"] = topicId  # 专题id，字符串
            article_fields["topicTitle"] = topicTitle  # 专题id，字符串
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
    appspider = ChinaDaily("中国日报")
    appspider.run()
