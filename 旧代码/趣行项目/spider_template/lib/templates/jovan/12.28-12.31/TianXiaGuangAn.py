# -*- encoding:utf-8 -*-
"""
@功能:湖北日报解析模板
@AUTHOR：jovan
@文件名：HuBeiRiBao.py
@时间：2020年12月22日 15:58:24
"""

import json
import logging
import random
import time

import requests

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass

bannerCountDir = {}


def setListNewsParam(channelname, channelid, item):
    try:
        article_fields = InitClass().article_fields()
        article_fields["channelname"] = channelname  # 频道名称，字符串
        article_fields["channelID"] = channelid  # 频道id，字符串
        # article_fields["channelType"] = channel_type  # 频道type，字符串
        article_fields["url"] = item['shareUrl']  # 分享的网址，字符串
        if 3 == item['articleType']:
            article_fields["workerid"] = item['linkID']  # 文章id，字符串
        else:
            article_fields["workerid"] = item['fileId']  # 文章id，字符串
        article_fields["title"] = item['title']  # 文章标题，字符串
        # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
        img_list = []
        if 'picBig' in item.keys():
            img_list.append(item['picBig'])
        elif 'picMiddle' in item.keys():
            img_list.append(item['picMiddle'])
        elif 'picSmall' in item.keys():
            img_list.append(item['picSmall'])
        article_fields["articlecovers"] = img_list  # 列表封面，数组
        # article_fields["images"] = ''  # 正文图片，数组
        # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
        # article_fields["videocover"] = [item['coverUrl']]  # 视频封面，数组
        # article_fields["width"] = ''  # 视频宽，字符串
        # article_fields["height"] = ''  # 视频高，字符串
        article_fields["source"] = item['source']  # 文章来源，字符串
        article_fields["pubtime"] = InitClass().date_time_stamp(item['publishtime'])  # 发布时间，时间戳（毫秒级，13位）
        # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
        # article_fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
        article_fields["likenum"] = item['countPraise']  # 点赞数（喜欢数），数值
        # article_fields["playnum"] = ''  # 播放数，数值
        if 'commentNum' in item.keys():
            article_fields["commentnum"] = item['commentNum']  # 评论数，数值
        article_fields["readnum"] = item['countClick']  # 阅读数，数值
        # article_fields["trannum"] = ''  # 转发数，数值
        article_fields["sharenum"] = item['countShareClick']  # 分享数，数值
        # article_fields["author"] = ''  # 作者，字符串
        if item['colID'] in bannerCountDir.keys():
            bannerCount = bannerCountDir[item['colID']]
            if bannerCount > 0:
                article_fields["banner"] = 1  # banner标记，数值（0标识不是，1标识是）
                bannerCountDir[item['colID']] = bannerCount - 1
                print(bannerCountDir)
            else:
                article_fields["banner"] = 0  # banner标记，数值（0标识不是，1标识是）
        else:
            article_fields["banner"] = 0  # banner标记，数值（0标识不是，1标识是）
        # article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
        # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
        # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
        # article_fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
        article_fields["newsType"] = item['articleType']  # 自己添加新闻类型
    except Exception as e:
        print(e)
    return article_fields


class TianXiaGuangAn(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://api.gazx.org/app_if/getColumns"
        headers = {
            "Host": "api.gazx.org",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.1",
        }
        method = "get"
        app_params_list = []
        # for channel_id in ["24", "167"]:
        for channel_id in ["24"]:
            data = {
                "siteId": "1",
                "parentColumnId": channel_id,
                "version": "0",
                "columnType": "-1",
            }
            app_params = InitClass().app_params(url, headers, method, data=data)
            app_params_list.append(app_params)
        yield app_params_list

    def analyze_channel(self, channelsres):
        print(channelsres)
        channelparams = []
        for item in channelsres:
            channelList = json.loads(item)
            for channel in channelList['columns'][0:2]:
                channelid = channel['columnId']
                channelname = channel['columnName']
                channelType = channel['columnStyle']
                topCount = channel['topCount']
                bannerCountDir[channelid] = topCount
                channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channelType)
                channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "http://api.gazx.org/app_if/getArticles"
        headers = {
            "Host": "api.gazx.org",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.1",
        }
        method = "get"
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channelType = channel.get("channeltype")
            data = {
                "columnId": channelid,
                "version": "0",
                "lastFileId": "0",
                "page": "0",
                "adv": "1",
                "columnStyle": channelType,
            }
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                       channelid=channelid, channeltype=channelType)
            articlelistsparams.append(articlelist_param)

        yield articlelistsparams

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            banners = articleslistres.get("banners")
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    print(articleslists)
                    if 'list' in articleslists.keys() and isinstance(articleslists['list'], list):
                        for article in articleslists['list']:
                            article_fields = setListNewsParam(channelname, channelid, article)
                            articleparam = InitClass().article_list_fields()
                            articleparam["articelField"] = article_fields
                            articlesparams.append(articleparam)

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
            newsType = article_field.get('newsType')
            if 3 == newsType:  # 专题
                url = "http://api.gazx.org/app_if/getColumns"
                headers = {
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; ALP-AL00 Build/HUAWEIALP-AL00)",
                    "Host": "api.gazx.org",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                method = "get"
                data = {
                    "siteId": "1",
                    "parentColumnId": article_field.get('workerid'),
                    "version": "0",
                    "columnType": "-1",
                }
                articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            else:
                url = "http://api.gazx.org/app_if/getArticleContent"
                headers = {
                    "Host": "api.gazx.org",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.8.1",
                }
                method = "get"
                data = {
                    "articleId": article_field.get('workerid'),
                    "colID": article_field.get('channelID'),
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
            try:
                contentJson = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                print(contentJson)
                newsContentUrl = fields.get('newsContentUrl')
                newsType = fields.get('newsType')
                fields["appname"] = appname
                if 0 == newsType:  # 普通
                    # fields["appname"] = appname  # 应用名称，字符串
                    # fields["channelname"] = channelname  # 频道名称，字符串
                    # fields["channelID"] = channelid  # 频道id，字符串
                    # fields["channelType"] = channel_type  # 频道type，字符串
                    # fields["url"] = contentJson['infoCont']  # 分享的网址，字符串
                    # fields["workerid"] = item['ctId']  # 文章id，字符串
                    # fields["title"] = item['title']  # 文章标题，字符串
                    content = contentJson['content']
                    if 'images' in contentJson.keys():
                        images = contentJson['images']
                        for item in images:
                            if 'imagearray' in item.keys():
                                for item1 in item['imagearray']:
                                    # temp = f"<img {item1['imageStyle']} src=\"{item1['imageUrl']}\" />"
                                    temp = f"<img src=\"{item1['imageUrl']}\" />"
                                    content = content.replace(item1['ref'], temp)
                            else:
                                print(item.keys())
                    fields["content"] = content  # 文章内容，字符串
                    # fields["content"] = contentJson['infoCont']  # 文章内容，字符串
                    # fields["articlecovers"] = imgList  # 列表封面，数组
                    fields["images"] = InitClass.get_images(fields["content"])  # 正文图片，数组
                    # fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                    # fields["videocover"] = [item['videoImg']]  # 视频封面，数组
                    # fields["width"] = ''  # 视频宽，字符串
                    # fields["height"] = ''  # 视频高，字符串
                    # fields["source"] = ''  # 文章来源，字符串
                    # fields["pubtime"] = InitClass.date_time_stamp(contentJson['pubDate'])  # 发布时间，时间戳（毫秒级，13位）
                    # fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                    # fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                    # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                    # fields["playnum"] = ''  # 播放数，数值
                    # fields["commentnum"] = item['commentNum']  # 评论数，数值
                    # fields["readnum"] = item['realRead']  # 阅读数，数值
                    # fields["trannum"] = ''  # 转发数，数值
                    # fields["sharenum"] = ''  # 分享数，数值
                    # fields["author"] = contentJson['pubAuthor']  # 作者，字符串
                    # fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                    # fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                    # fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                    # fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
                elif 1 == newsType:  # 画廊
                    # fields["appname"] = appname  # 应用名称，字符串
                    # fields["channelname"] = channelname  # 频道名称，字符串
                    # fields["channelID"] = channelid  # 频道id，字符串
                    # fields["channelType"] = channel_type  # 频道type，字符串
                    # fields["url"] = contentJson['infoCont']  # 分享的网址，字符串
                    # fields["workerid"] = item['ctId']  # 文章id，字符串
                    # fields["title"] = item['title']  # 文章标题，字符串
                    # fields["content"] = contentJson['infoCont']  # 文章内容，字符串
                    # fields["articlecovers"] = imgList  # 列表封面，数组
                    imgList = []
                    if 'images' in contentJson.keys():
                        images = contentJson['images']
                        for item in images:
                            if 'imagearray' in item.keys():
                                for item1 in item['imagearray']:
                                    imgList.append(item1['imageUrl'])
                            else:
                                print(item.keys())
                    fields["images"] = imgList  # 正文图片，数组
                    # fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                    # fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                    # fields["videocover"] = [item['videoImg']]  # 视频封面，数组
                    # fields["width"] = ''  # 视频宽，字符串
                    # fields["height"] = ''  # 视频高，字符串
                    # fields["source"] = ''  # 文章来源，字符串
                    # fields["pubtime"] = InitClass.date_time_stamp(contentJson['pubDate'])  # 发布时间，时间戳（毫秒级，13位）
                    # fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                    # fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                    # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                    # fields["playnum"] = ''  # 播放数，数值
                    # fields["commentnum"] = item['commentNum']  # 评论数，数值
                    # fields["readnum"] = item['realRead']  # 阅读数，数值
                    # fields["trannum"] = ''  # 转发数，数值
                    # fields["sharenum"] = ''  # 分享数，数值
                    # fields["author"] = contentJson['pubAuthor']  # 作者，字符串
                    # fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                    # fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                    # fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                    # fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
                elif 2 == newsType:  # 视频
                    # fields["appname"] = appname  # 应用名称，字符串
                    # fields["channelname"] = channelname  # 频道名称，字符串
                    # fields["channelID"] = channelid  # 频道id，字符串
                    # fields["channelType"] = channel_type  # 频道type，字符串
                    # fields["url"] = contentJson['infoCont']  # 分享的网址，字符串
                    # fields["workerid"] = item['ctId']  # 文章id，字符串
                    # fields["title"] = item['title']  # 文章标题，字符串
                    # fields["content"] = content  # 文章内容，字符串
                    # fields["content"] = contentJson['infoCont']  # 文章内容，字符串
                    # fields["articlecovers"] = imgList  # 列表封面，数组
                    # fields["images"] = InitClass.get_images(fields["content"])  # 正文图片，数组
                    videoList = []
                    videoPicList = []
                    if 'videos' in contentJson.keys():
                        videos = contentJson['videos']
                        for item in videos:
                            if 'videoarray' in item.keys():
                                for item1 in item['videoarray']:
                                    # temp = f"<img {item1['imageStyle']} src=\"{item1['imageUrl']}\" />"
                                    videoList.append(item1['videoUrl'])
                                    videoPicList.append(item1['imageUrl'])
                            else:
                                print(item.keys())
                    fields["videos"] = videoList  # 视频地址，数组
                    fields["videocover"] = videoPicList  # 视频封面，数组
                    # fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                    # fields["videocover"] = [item['videoImg']]  # 视频封面，数组
                    # fields["width"] = ''  # 视频宽，字符串
                    # fields["height"] = ''  # 视频高，字符串
                    # fields["source"] = ''  # 文章来源，字符串
                    # fields["pubtime"] = InitClass.date_time_stamp(contentJson['pubDate'])  # 发布时间，时间戳（毫秒级，13位）
                    # fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                    # fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                    # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                    # fields["playnum"] = ''  # 播放数，数值
                    # fields["commentnum"] = item['commentNum']  # 评论数，数值
                    # fields["readnum"] = item['realRead']  # 阅读数，数值
                    # fields["trannum"] = ''  # 转发数，数值
                    # fields["sharenum"] = ''  # 分享数，数值
                    # fields["author"] = contentJson['pubAuthor']  # 作者，字符串
                    # fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                    # fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                    # fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                    # fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
                elif 3 == newsType:  # 专题
                    topicFields = InitClass().topic_fields()
                    topicFields["topicID"] = contentJson['columns'][0]['columnId']  # 专题id，app内唯一标识
                    topicFields["platformName"] = appname  # 平台名字（app名字）
                    # topicFields["platformID"] = fields['workerid']
                    topicFields["channelName"] = fields['channelname']  # 频道名字
                    topicFields["channelID"] = fields['channelID']  # 频道id
                    # topicFields["topicUrl"] = fields['workerid']  # topicUrl
                    topicFields["title"] = fields['title']
                    # topicFields["digest"] = contentJson['description']  # 简介，摘要
                    topicFields["topicCover"] = fields['articlecovers']
                    # topicFields["pubTime"] = fields['workerid']  # 时间戳
                    # topicFields["articleNum"] = fields['workerid']  # 专题内的文章数量
                    # topicFields["newestArticleID"] = fields['workerid']  # 最新发布的文章id
                    # topicFields["articlesNumPerHour"] = fields['workerid']
                    # topicFields["original"] = fields['workerid']
                    # topicFields["firstMedia"] = fields['workerid']
                    # topicFields["transPower"] = fields['workerid']
                    # topicFields["hotDegree"] = fields['workerid']
                    # topicFields["wordsFreq"] = fields['workerid']
                    # topicFields["hotDegreeTrend"] = fields['workerid']
                    # topicFields["emotionTrend"] = fields['workerid']
                    # topicFields["region"] = fields['workerid']
                    # topicFields["spreadPath"] = fields['workerid']
                    # topicFields["createTime"] = fields['workerid']
                    # topicFields["updateTime"] = fields['workerid']
                    url = "http://api.gazx.org/app_if/getArticles"
                    headers = {
                        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; ALP-AL00 Build/HUAWEIALP-AL00)",
                        "Host": "api.gazx.org",
                        "Connection": "Keep-Alive",
                        "Accept-Encoding": "gzip",
                    }
                    data = {
                        "columnId": topicFields["topicID"],
                        "version": "0",
                        "lastFileId": "0",
                        "count": "9",
                        "rowNumber": "0",
                        "adv": "1",
                    }
                    topic_list_res = requests.get(url, headers=headers, params=data).content.decode()
                    topic_list = json.loads(topic_list_res)

                    topicArticles = self.getTopicArticles(topicFields["channelName"], topicFields["channelID"],
                                                          topicFields["title"],
                                                          topicFields["topicID"], topic_list['list'])
                    articleparams = self.getarticleparams(topicArticles.__next__())
                    articlesres = self.getarticlehtml(articleparams.__next__())
                    self.analyzearticle(articlesres.__next__())
                elif 4 == newsType:  # 网址
                    # fields["appname"] = appname  # 应用名称，字符串
                    # fields["channelname"] = channelname  # 频道名称，字符串
                    # fields["channelID"] = channelid  # 频道id，字符串
                    # fields["channelType"] = channel_type  # 频道type，字符串
                    fields["url"] = contentJson['url']  # 分享的网址，字符串
                    # fields["workerid"] = item['ctId']  # 文章id，字符串
                    # fields["title"] = item['title']  # 文章标题，字符串
                    # fields["content"] = content  # 文章内容，字符串
                    # fields["content"] = contentJson['infoCont']  # 文章内容，字符串
                    # fields["articlecovers"] = imgList  # 列表封面，数组
                    # fields["images"] = InitClass.get_images(fields["content"])  # 正文图片，数组
                    # fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                    # fields["videocover"] = [item['videoImg']]  # 视频封面，数组
                    # fields["width"] = ''  # 视频宽，字符串
                    # fields["height"] = ''  # 视频高，字符串
                    # fields["source"] = ''  # 文章来源，字符串
                    # fields["pubtime"] = InitClass.date_time_stamp(contentJson['pubDate'])  # 发布时间，时间戳（毫秒级，13位）
                    # fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                    # fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                    # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                    # fields["playnum"] = ''  # 播放数，数值
                    # fields["commentnum"] = item['commentNum']  # 评论数，数值
                    # fields["readnum"] = item['realRead']  # 阅读数，数值
                    # fields["trannum"] = ''  # 转发数，数值
                    # fields["sharenum"] = ''  # 分享数，数值
                    # fields["author"] = contentJson['pubAuthor']  # 作者，字符串
                    # fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                    # fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                    # fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                    # fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
                else:
                    print('未识别类型', contentJson)
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
                article_fields["url"] = item['shareUrl']  # 分享的网址，字符串
                if 3 == item['articleType']:
                    article_fields["workerid"] = item['linkID']  # 文章id，字符串
                else:
                    article_fields["workerid"] = item['fileId']  # 文章id，字符串
                article_fields["title"] = item['title']  # 文章标题，字符串
                # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
                img_list = []
                if 'picBig' in item.keys():
                    img_list.append(item['picBig'])
                elif 'picMiddle' in item.keys():
                    img_list.append(item['picMiddle'])
                elif 'picSmall' in item.keys():
                    img_list.append(item['picSmall'])
                article_fields["articlecovers"] = img_list  # 列表封面，数组
                # article_fields["images"] = ''  # 正文图片，数组
                # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                # article_fields["videocover"] = [item['coverUrl']]  # 视频封面，数组
                # article_fields["width"] = ''  # 视频宽，字符串
                # article_fields["height"] = ''  # 视频高，字符串
                article_fields["source"] = item['source']  # 文章来源，字符串
                article_fields["pubtime"] = InitClass().date_time_stamp(item['publishtime'])  # 发布时间，时间戳（毫秒级，13位）
                # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                # article_fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                article_fields["likenum"] = item['countPraise']  # 点赞数（喜欢数），数值
                # article_fields["playnum"] = ''  # 播放数，数值
                if 'commentNum' in item.keys():
                    article_fields["commentnum"] = item['commentNum']  # 评论数，数值
                article_fields["readnum"] = item['countClick']  # 阅读数，数值
                # article_fields["trannum"] = ''  # 转发数，数值
                article_fields["sharenum"] = item['countShareClick']  # 分享数，数值
                # article_fields["author"] = ''  # 作者，字符串
                # article_fields["banner"] = 0  # banner标记，数值（0标识不是，1标识是）
                # article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                article_fields["specialtopic"] = 1  # 是否是专题，数值（0标识不是，1标识是）
                article_fields["topicid"] = topicId  # 专题id，字符串
                article_fields["topicTitle"] = topicTitle  # 专题标题，字符串
                article_fields["newsType"] = item['articleType']  # 自己添加新闻类型
                articleparam = InitClass().article_list_fields()
                articleparam["articelField"] = article_fields
                articlesparams.append(articleparam)
            except Exception as e:
                print(e)

        yield articlesparams

    def run(self):
        appParamsList = self.get_app_params().__next__()
        channelsres = []
        for appParams in appParamsList:
            channel_res = self.getchannels(appParams).__next__()
            channelsres.append(channel_res)
        channelsparams = self.analyze_channel(channelsres)
        articlelistparames = self.getarticlelistparams(channelsparams.__next__())
        articleslistsres = self.getarticlelists(articlelistparames.__next__())
        articles = self.analyze_articlelists(articleslistsres.__next__())
        articleparams = self.getarticleparams(articles.__next__())
        articlesres = self.getarticlehtml(articleparams.__next__())
        self.analyzearticle(articlesres.__next__())


if __name__ == '__main__':
    appspider = TianXiaGuangAn("天下广安")
    appspider.run()
