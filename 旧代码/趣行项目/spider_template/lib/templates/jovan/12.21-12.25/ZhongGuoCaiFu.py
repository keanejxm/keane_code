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


class ZhongGuoCaiFu(Appspider):

    @staticmethod
    def get_app_params():
        url1 = "https://a.cfbond.com/wealth/home_tab_info"
        headers1 = {
            "TOKEN": "",
            "TIMESTAMP": str(int(time.time())),
            "SOURCE": "android",
            "DEVICE-ID": "2921d1e2d9e346ab8bc7b3f0b01d9c15",
            "SIGN-RESULT": "",
            "VERSION": "2.2.4",
            "Host": "a.cfbond.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.10.0",
        }
        data1 = {
            "is_all": "0",
        }
        method1 = "get"
        app_params1 = InitClass().app_params(url1, headers1, method1, data=data1)

        url2 = "https://a.cfbond.com/wealth/look_tab_info"
        headers2 = {
            "TOKEN": "",
            "TIMESTAMP": str(int(time.time())),
            "SOURCE": "android",
            "DEVICE-ID": "2921d1e2d9e346ab8bc7b3f0b01d9c15",
            "SIGN-RESULT": "",
            "VERSION": "2.2.4",
            "Host": "a.cfbond.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.10.0",
        }
        method2 = "get"
        app_params2 = InitClass().app_params(url2, headers2, method2)
        yield [app_params1, app_params2]

    def analyze_channel(self, channelsres):
        print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            if 'https://a.cfbond.com/wealth/home_tab_info' == k:
                channelList = json.loads(v)
                for channel in channelList['data']['tab_list']:
                    channelid = channel['id']
                    channelname = channel['name']
                    channelType = channel['type']
                    if len(channel['url']):
                        pass
                    else:
                        channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channelType)
                        channelparams.append(channelparam)
            if 'https://a.cfbond.com/wealth/look_tab_info' == k:
                channelList = json.loads(v)
                for channel in channelList['data']['data_list']:
                    channelid = channel['id']
                    channelname = channel['name']
                    channelparam = InitClass().channel_fields(channelid, channelname, channeltype="QXLookTab")
                    channelparams.append(channelparam)

        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            if 'recommend' == channelid:
                url = "https://a.cfbond.com/wealth/home_news_list"
                headers = {
                    "TOKEN": "",
                    "TIMESTAMP": str(int(time.time())),
                    "SOURCE": "android",
                    "DEVICE-ID": "2921d1e2d9e346ab8bc7b3f0b01d9c15",
                    "SIGN-RESULT": "",
                    "VERSION": "2.2.4",
                    "Host": "a.cfbond.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.10.0",
                }
                method = "get"
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           channelid=channelid, channeltype=channeltype)
                articlelistsparams.append(articlelist_param)
            elif 'newsletter' == channelid:
                url = "https://a.cfbond.com/wealth/search"
                headers = {
                    "TOKEN": "",
                    "TIMESTAMP": str(int(time.time())),
                    "SOURCE": "android",
                    "DEVICE-ID": "2921d1e2d9e346ab8bc7b3f0b01d9c15",
                    "SIGN-RESULT": "",
                    "VERSION": "2.2.4",
                    "Host": "a.cfbond.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.10.0",
                }
                method = "get"
                data = {
                    "api_type": "2393",
                    "page_num": "1",
                    "page_size": "10",
                }
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                           channelid=channelid, channeltype=channeltype)
                articlelistsparams.append(articlelist_param)

            elif 'cwcq' == channelid:
                url = "https://a.cfbond.com/wealth/search"
                headers = {
                    "TOKEN": "",
                    "TIMESTAMP": str(int(time.time())),
                    "SOURCE": "android",
                    "DEVICE-ID": "2921d1e2d9e346ab8bc7b3f0b01d9c15",
                    "SIGN-RESULT": "",
                    "VERSION": "2.2.4",
                    "Host": "a.cfbond.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.10.0",
                }
                method = "get"
                data1 = {
                    "api_type": "3618533350",
                    "page_num": "1",
                    "page_size": "10",
                }
                data2 = {
                    "api_type": "3618533351",
                    "page_num": "1",
                    "page_size": "10",
                }
                data3 = {
                    "api_type": "3618533352",
                    "page_num": "1",
                    "page_size": "10",
                }
                articlelist_param1 = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                            data=data1,
                                                                            channelid=channelid,
                                                                            channeltype=channeltype)
                articlelist_param2 = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                            data=data2,
                                                                            channelid=channelid,
                                                                            channeltype=channeltype)
                articlelist_param3 = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                            data=data3,
                                                                            channelid=channelid,
                                                                            channeltype=channeltype)
                articlelistsparams.append(articlelist_param1)
                articlelistsparams.append(articlelist_param2)
                articlelistsparams.append(articlelist_param3)
            # GET https://a.cfbond.com/wealth/search?api_type=3618533350&page_num=1&page_size=3 HTTP/1.1
            # GET https://a.cfbond.com/wealth/search?api_type=3618533351&page_num=1&page_size=3 HTTP/1.1
            # GET GET https://a.cfbond.com/wealth/search?api_type=3618533352&page_num=1&page_size=3 HTTP/1.1
            else:
                url = "https://a.cfbond.com/wealth/search"
                headers = {
                    "TOKEN": "",
                    "TIMESTAMP": str(int(time.time())),
                    "SOURCE": "android",
                    "DEVICE-ID": "2921d1e2d9e346ab8bc7b3f0b01d9c15",
                    "SIGN-RESULT": "",
                    "VERSION": "2.2.4",
                    "Host": "a.cfbond.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.10.0",
                }
                method = "get"
                data = {
                    "api_type": channelid,
                    "page_num": "1",
                    "page_size": "10",
                }
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                           channelid=channelid, channeltype=channeltype)
                articlelistsparams.append(articlelist_param)
            # 添加推送历史
            url = "https://a.cfbond.com/wealth/push_info"
            headers = {
                "TOKEN": "",
                "TIMESTAMP": str(int(time.time())),
                "SOURCE": "android",
                "DEVICE-ID": "2921d1e2d9e346ab8bc7b3f0b01d9c15",
                "SIGN-RESULT": "",
                "VERSION": "2.2.4",
                "Host": "a.cfbond.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.10.0",
            }
            method = "get"
            data = {
                "page_num": "1",
                "page_size": "10",
            }
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, "推送历史", data=data,
                                                                       channelid=-1, channeltype=-1)
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
                        if 'data_list' in articleslists['data']:  # banner
                            for item in articleslists['data']['data_list']:
                                if 'tab_type' in item.keys() and (
                                        item['tab_type'] == 'home_tab' or item['tab_type'] == 'ad' or item[
                                    'tab_type'] == 'qa'):
                                    continue
                                else:
                                    if 'tab_data_list' in item:  # banner
                                        for item1 in item['tab_data_list']:
                                            if 'id' in item1.keys() and len(item1['id']):
                                                article_fields = InitClass().article_fields()
                                                article_fields["channelname"] = channelname  # 频道名称，字符串
                                                article_fields["channelID"] = channelid  # 频道id，字符串
                                                # article_fields["channelType"] = channel_type  # 频道type，字符串
                                                article_fields["url"] = item1['detail_url']  # 分享的网址，字符串
                                                article_fields["title"] = item1['title']  # 文章标题，字符串
                                                # article_fields["content"] = ''  # 文章内容，字符串
                                                if 'image_list' in item1.keys():
                                                    article_fields["articlecovers"] = item1['image_list']  # 列表封面，数组
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
                                                # if 7 == bannerItem['contentType']:  # 专题
                                                #     article_fields["specialtopic"] = 1
                                                #     article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                                                # else:
                                                #     article_fields["specialtopic"] = 0
                                                #     article_fields["workerid"] = bannerItem['contentId']  # 文章id，字符串
                                                article_fields["workerid"] = item1['id']  # 文章id，字符串
                                                article_fields["specialtopic"] = 0  # 是否是专题，数值（0标识不是，1标识是）
                                                # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                                                # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                                                article_fields["articleType"] = item1['first_type']  # 文章类型，自己添加
                                                article_fields["detailMode"] = item1[
                                                    'detail_mode']  # 这个是2的时候，且articleType为news，才是专题，自己添加
                                                articleparam = InitClass().article_list_fields()
                                                articleparam["articelField"] = article_fields
                                                articlesparams.append(articleparam)
                                    else:
                                        if 'first_type' in item.keys() and 'look' != item[
                                            'first_type'] and 'id' in item.keys() and len(item['id']):
                                            article_fields = InitClass().article_fields()
                                            article_fields["channelname"] = channelname  # 频道名称，字符串
                                            article_fields["channelID"] = channelid  # 频道id，字符串
                                            # article_fields["channelType"] = channel_type  # 频道type，字符串
                                            article_fields["url"] = item['detail_url']  # 分享的网址，字符串
                                            article_fields["title"] = item['title']  # 文章标题，字符串
                                            # article_fields["content"] = ''  # 文章内容，字符串
                                            if 'image_list' in item.keys():
                                                article_fields["articlecovers"] = item['image_list']  # 列表封面，数组
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
                                            # if 7 == bannerItem['contentType']:  # 专题
                                            #     article_fields["specialtopic"] = 1
                                            #     article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                                            # else:
                                            #     article_fields["specialtopic"] = 0
                                            #     article_fields["workerid"] = bannerItem['contentId']  # 文章id，字符串
                                            article_fields["workerid"] = item['id']  # 文章id，字符串
                                            article_fields["specialtopic"] = 0  # 是否是专题，数值（0标识不是，1标识是）
                                            # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                                            # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                                            article_fields["articleType"] = item['first_type']  # 文章类型，自己添加
                                            article_fields["detailMode"] = item[
                                                'detail_mode']  # 这个是2的时候，且articleType为news，才是专题，自己添加
                                            articleparam = InitClass().article_list_fields()
                                            articleparam["articelField"] = article_fields
                                            articlesparams.append(articleparam)
                                        if 'look' == item['first_type']:  # 这个列表就是详情
                                            article_fields = InitClass().article_fields()
                                            article_fields["channelname"] = channelname  # 频道名称，字符串
                                            article_fields["channelID"] = channelid  # 频道id，字符串
                                            # article_fields["channelType"] = channel_type  # 频道type，字符串
                                            article_fields["url"] = item['detail_url']  # 分享的网址，字符串
                                            article_fields["title"] = item['title']  # 文章标题，字符串
                                            # article_fields["content"] = ''  # 文章内容，字符串
                                            if 'image_list' in item.keys():
                                                article_fields["articlecovers"] = item['image_list']  # 列表封面，数组
                                            # article_fields["images"] = ''  # 正文图片，数组
                                            article_fields["videos"] = [
                                                item['look_video_url']['general_url']]  # 视频地址，数组
                                            # article_fields["videocover"] = ''  # 视频封面，数组
                                            # article_fields["width"] = ''  # 视频宽，字符串
                                            # article_fields["height"] = ''  # 视频高，字符串
                                            article_fields["source"] = item['source']  # 文章来源，字符串
                                            article_fields["pubtime"] = InitClass().date_time_stamp(
                                                item['published_time_original'])  # 发布时间，时间戳（毫秒级，13位）
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
                                            # if 7 == bannerItem['contentType']:  # 专题
                                            #     article_fields["specialtopic"] = 1
                                            #     article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                                            # else:
                                            #     article_fields["specialtopic"] = 0
                                            #     article_fields["workerid"] = bannerItem['contentId']  # 文章id，字符串
                                            article_fields["workerid"] = item['id']  # 文章id，字符串
                                            article_fields["specialtopic"] = 0  # 是否是专题，数值（0标识不是，1标识是）
                                            # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                                            # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
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
            articleType = article_field.get("articleType")
            url = "https://a.cfbond.com/wealth/news_detail"
            headers = {
                "TOKEN": "",
                "TIMESTAMP": str(int(time.time())),
                "SOURCE": "android",
                "DEVICE-ID": "2921d1e2d9e346ab8bc7b3f0b01d9c15",
                "SIGN-RESULT": "",
                "VERSION": "2.2.4",
                "Host": "a.cfbond.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.10.0",
            }
            method = "get"
            data = {
                "news_id": article_field.get('workerid'),
            }
            articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                             article_field=article_field)
            articleparams.append(articleparam)

        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            appname = article.get("appname")
            fields = article.get("articleField")
            articleType = fields.get("articleType")
            detailMode = fields.get('detailMode')
            try:
                contentJson = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                if 'news' == articleType and 2 == detailMode and 'specials.cfbond.com' in fields[
                    'url']:  # 专题 但是专题详情是个网址
                    topicFields = InitClass().topic_fields()
                    topicFields["_id"] = fields['workerid']  # 专题id，app内唯一标识
                    topicFields["platformName"] = article['appname']  # 平台名字（app名字）
                    topicFields["platformID"] = ''  #
                    topicFields["channelName"] = fields['channelname']  # 频道名字
                    topicFields["channelID"] = fields['channelID']  # 频道id
                    topicFields["topicUrl"] = fields['url']  # topicUrl
                    topicFields["title"] = fields['title']  #
                    # topicFields["digest"] = newsDetail['introduction']  # 简介，摘要
                    topicFields["topicCover"] = fields['articlecovers']  # list(),
                    topicFields["pubTime"] = InitClass().date_time_stamp(
                        contentJson['data']['news_detail']['published_time'])  # 时间戳
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
                    # topicFields["createTime"] = ''
                    # topicFields["updateTime"] = ''
                else:
                    fields["appname"] = appname  # 应用名称，字符串
                    # article_fields["channelname"] = channelname  # 频道名称，字符串
                    # article_fields["channelID"] = channelid  # 频道id，字符串
                    # article_fields["channelType"] = channel_type  # 频道type，字符串
                    # article_fields["url"] = ''  # 分享的网址，字符串
                    # article_fields["title"] = bannerItem['title']  # 文章标题，字符串
                    fields["content"] = contentJson['data']['news_detail']['content']  # 文章内容，字符串
                    fields["articlecovers"] = contentJson['data']['news_detail']['image_list']  # 列表封面，数组
                    fields["images"] = InitClass().get_images(fields["content"])  # 正文图片，数组
                    fields["videos"] = [contentJson['data']['news_detail']['video_url']]  # 视频地址，数组
                    fields["videocover"] = [contentJson['data']['news_detail']['video_cover']]  # 视频封面，数组
                    # article_fields["width"] = ''  # 视频宽，字符串
                    # article_fields["height"] = ''  # 视频高，字符串
                    # article_fields["source"] = ''  # 文章来源，字符串
                    # article_fields["pubtime"] = InitClass().date_time_stamp(
                    #                         contentJson['data']['news_detail']['published_time'])  # 发布时间，时间戳（毫秒级，13位）
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
                    # if 7 == bannerItem['contentType']:  # 专题
                    #     article_fields["specialtopic"] = 1
                    #     article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                    # else:
                    #     article_fields["specialtopic"] = 0
                    #     article_fields["workerid"] = bannerItem['contentId']  # 文章id，字符串
                    # article_fields["workerid"] = bannerItem['contentId']  # 文章id，字符串
                    # article_fields["specialtopic"] = 0  # 是否是专题，数值（0标识不是，1标识是）
                    # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                    # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                print(json.dumps(fields, indent=4, ensure_ascii=False))
            except Exception as e:
                num += 1
                logging.info(f"错误数量{num},{e}")

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
    appspider = ZhongGuoCaiFu("中国财富")
    appspider.run()
