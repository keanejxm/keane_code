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
        # article_fields["url"] = item['h5url']  # 分享的网址，字符串
        article_fields["title"] = item['title']  # 文章标题，字符串
        # article_fields["content"] = item['webLink']  # 文章内容，字符串
        imgList = []
        if "pic1" in item.keys() and len(item['pic1']):
            imgList.append(item['pic1'])
        if "pic2" in item.keys() and len(item['pic2']):
            imgList.append(item['pic2'])
        if "pic3" in item.keys() and len(item['pic3']):
            imgList.append(item['pic3'])
        article_fields["articlecovers"] = imgList  # 列表封面，数组
        # article_fields["images"] = ''  # 正文图片，数组
        # article_fields["videocover"] = [item['videoImg']]  # 视频封面，数组
        videoList = []
        if "video" in item.keys() and len(item['video']):
            videoList.append(item['video'])
        article_fields["videos"] = videoList  # 视频地址，数组
        # article_fields["width"] = ''  # 视频宽，字符串
        # article_fields["height"] = ''  # 视频高，字符串
        # article_fields["source"] = item['source']  # 文章来源，字符串
        article_fields["pubtime"] = InitClass().date_time_stamp(item['publish_time'])  # 发布时间，时间戳（毫秒级，13位）
        # article_fields["createtime"] = item['createdate']  # 创建时间，时间戳（毫秒级，13位）
        # article_fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
        # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
        # article_fields["playnum"] = ''  # 播放数，数值
        # article_fields["commentnum"] = item['commentNum']  # 评论数，数值
        # article_fields["readnum"] = ''  # 阅读数，数值
        # article_fields["trannum"] = ''  # 转发数，数值
        # article_fields["sharenum"] = ''  # 分享数，数值
        # article_fields["author"] = ''  # 作者，字符串
        # article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）

        # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
        # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串

        if 'link_id' in item.keys() and item['link_id'] != 0:
            if "others" in item.keys() and isinstance(item['others'], list) and len(item['others']):
                article_fields["workerid"] = item['article_id']  # 文章id，字符串
                article_fields["newstype"] = "QXDef"  # 自己添加新闻类型
                article_fields["childNews"] = item['others']  # 相当于是个专题
            else:
                article_fields["workerid"] = item['link_id']  # 文章id，字符串
                article_fields["newstype"] = "QXTopic"  # 自己添加新闻类型
        else:
            article_fields["workerid"] = item['article_id']  # 文章id，字符串
            article_fields["newstype"] = "QXDef"  # 自己添加新闻类型

        articleparam = InitClass().article_list_fields()
        articleparam["articelField"] = article_fields
        articlesparams.append(articleparam)
    except Exception as e:
        logging.info(e)
    return articlesparams


class JiangHanXinWen(Appspider):

    @staticmethod
    def get_app_params():
        url1 = "http://jhyt.cyparty.com/app/api/news"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "11",
            "Host": "jhyt.cyparty.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.3.0",
        }
        method = "post"
        data = 'action=menu'
        # appJson = 'action=menu'
        app_params1 = InitClass().app_params(url1, headers, method, data=data)

        yield [app_params1]

    def analyze_channel(self, channelsres):
        print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            channelList = json.loads(v)
            for channel in channelList['result']:
                if 19 == channel['id']:  # 活动
                    continue
                else:
                    channelid = channel['id']
                    channelname = channel['name']
                    channelparam = InitClass().channel_fields(channelid, channelname)
                    channelparams.append(channelparam)
        channelparam1 = InitClass().channel_fields('23', '专题')
        channelparams.append(channelparam1)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "http://jhyt.cyparty.com/app/api/news"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "100",
            "Host": "jhyt.cyparty.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.3.0",
        }
        method = "post"
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")

            dataBanner = f'action=show_hot&menu_id={channelid}'
            dataList = f'action=show&menu_id={channelid}&keyword=&page=0&size=10'

            articlelist_param1 = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                        data=dataBanner, banners=1, channelid=channelid)
            articlelistsparams.append(articlelist_param1)
            articlelist_param2 = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                        data=dataList, banners=0, channelid=channelid)
            articlelistsparams.append(articlelist_param2)

        data1 = f'action=show_video&status=1&tag=%E6%96%B0%E9%97%BB%E8%81%94%E6%92%AD&page=0&size=12'
        articlelist_param1 = InitClass().articlelists_params_fields(url, headers, method, '新闻联播',
                                                                    data=data1, banners=0, channelid=-1)
        articlelistsparams.append(articlelist_param1)

        data2 = f'action=show_video&status=1&tag=%E8%81%9A%E7%84%A6%E6%B1%9F%E6%B1%89&page=0&size=12'
        articlelist_param2 = InitClass().articlelists_params_fields(url, headers, method, "聚焦江汉",
                                                                    data=data2, banners=0, channelid=-2)
        articlelistsparams.append(articlelist_param2)

        data3 = f'action=show_jh_video&page=0&size=10'
        articlelist_param3 = InitClass().articlelists_params_fields(url, headers, method, '油田新闻',
                                                                    data=data3, banners=0, channelid=-3)
        articlelistsparams.append(articlelist_param3)

        data4 = f'action=show_hot&key=%E6%8E%A8%E8%8D%90%E8%A7%86%E9%A2%91%E7%BD%AE%E9%A1%B6'
        articlelist_param4 = InitClass().articlelists_params_fields(url, headers, method, "推荐视频置顶",
                                                                    data=data4, banners=0, channelid=-4)
        articlelistsparams.append(articlelist_param4)

        data5 = f'action=show_video&tag=%E6%8E%A8%E8%8D%90%E8%A7%86%E9%A2%91&page=0&size=10'
        articlelist_param5 = InitClass().articlelists_params_fields(url, headers, method, "推荐视频",
                                                                    data=data5, banners=0, channelid=-5)
        articlelistsparams.append(articlelist_param5)

        yield articlelistsparams

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            banner = articleslistres.get('banner')
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    print(articleslists)
                    if 'result' in articleslists.keys():
                        for item in articleslists['result']:
                            articlesparams = setListNewsParam(articlesparams, channelname, channelid, banner, item)
                    elif 'data' in articleslists.keys():
                        for item in articleslists['data']:
                            articlesparams = setListNewsParam(articlesparams, channelname, channelid, banner, item)
                    else:
                        print(articleslists.keys())
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
            url = "http://jhyt.cyparty.com/app/api/news"
            method = "post"
            if "QXTopic" == newsType:  # 专题
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Content-Length": "100",
                    "Host": "jhyt.cyparty.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.3.0",
                }
                data = f'action=show_subject&link_id={article_field.get("workerid")}&type=0'
                articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            else:
                if "childNews" in article_field.keys() and isinstance(article_field.get('childNews'), list) and len(
                        article_field.get('childNews')):
                    headers = {
                        "Host": "jhyt.cyparty.com",
                        "Connection": "keep-alive",
                        "Content-Length": "38",
                        "Accept": "application/json, text/javascript, */*; q=0.01",
                        "X-Requested-With": "XMLHttpRequest",
                        "User-Agent": "Mozilla/5.0 (Linux; Android 10; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36",
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "Origin": "http://jhyt.cyparty.com",
                        "Referer": f"http://jhyt.cyparty.com/video/carousel?id={article_field.get('workerid')}&source=app",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                        "Cookie": "JSESSIONID=178254BA2947B0F543897BE4A0E3BA94",
                    }
                    data = f'action=show_jh_video&article_id={article_field.get("workerid")}'
                    articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                                     article_field=article_field)
                    articleparams.append(articleparam)
                else:
                    if int(article_field.get('channelID')) < 0:
                        headers = {
                            "Host": "jhyt.cyparty.com",
                            "Connection": "keep-alive",
                            "Content-Length": "38",
                            "Accept": "application/json, text/javascript, */*; q=0.01",
                            "X-Requested-With": "XMLHttpRequest",
                            "User-Agent": "Mozilla/5.0 (Linux; Android 10; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36",
                            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                            "Origin": "http://jhyt.cyparty.com",
                            "Referer": f"http://jhyt.cyparty.com/video/detail?id={article_field.get('workerid')}&version=1&source=app",
                            "Accept-Encoding": "gzip, deflate",
                            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                            "Cookie": "JSESSIONID=178254BA2947B0F543897BE4A0E3BA94",
                        }
                        data = f'action=show_video&article_id={article_field.get("workerid")}'
                        articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                                         article_field=article_field)
                        articleparams.append(articleparam)
                    else:
                        headers = {
                            "Host": "jhyt.cyparty.com",
                            "Connection": "keep-alive",
                            "Content-Length": "38",
                            "Accept": "application/json, text/javascript, */*; q=0.01",
                            "X-Requested-With": "XMLHttpRequest",
                            "User-Agent": "Mozilla/5.0 (Linux; Android 10; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36",
                            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                            "Origin": "http://jhyt.cyparty.com",
                            "Referer": f"http://jhyt.cyparty.com/article/detail?id={article_field.get('workerid')}&version=1&source=app",
                            "Accept-Encoding": "gzip, deflate",
                            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                            "Cookie": "JSESSIONID=178254BA2947B0F543897BE4A0E3BA94",
                        }
                        data = f'action=show_info&article_id={article_field.get("workerid")}'
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
                newsType = fields.get('newstype')
                if "QXTopic" == newsType:  # 专题
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
                    topicFields["pubTime"] = fields['pubtime']  # 时间戳
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
                    topicArticles = self.getTopicArticles(fields['channelname'], fields['channelID'],
                                                          fields['workerid'], contentJson['result'])
                    articleparams = self.getarticleparams(topicArticles.__next__())
                    articlesres = self.getarticlehtml(articleparams.__next__())
                    self.analyzearticle(articlesres.__next__())
                else:
                    if "childNews" in fields.keys() and isinstance(fields.get('childNews'), list) and len(
                            fields.get('childNews')):
                        fields["appname"] = appname  # 应用名称，字符串
                        # fields["channelname"] = fields.get('channelname')  # 频道名称，字符串
                        # fields["channelID"] = fields.get('channelID')  # 频道id，字符串
                        # article_fields["channelType"] = channel_type  # 频道type，字符串
                        # fields["url"] = contentJson['news']['webLink']  # 分享的网址，字符串
                        # fields["title"] = contentJson['news']['title']  # 文章标题，字符串
                        # if 'content' in contentJson.keys():
                        # fields["content"] = contentJson['news']['content']  # 文章内容，字符串
                        # imgThumList = []
                        # for imgUrl in contentJson['thumbnails']:
                        #     imgThumList.append(imgUrl['url'])
                        # fields["articlecovers"] = imgThumList  # 列表封面，数组
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
                        topicArticles = self.getTopicArticles(fields['channelname'], fields['channelID'],
                                                              fields['workerid'], contentJson['data'][0]['others'])
                        articleparams = self.getarticleparams(topicArticles.__next__())
                        articlesres = self.getarticlehtml(articleparams.__next__())
                        self.analyzearticle(articlesres.__next__())
                    else:
                        if int(fields.get('channelID')) < 0:
                            fields["appname"] = appname  # 应用名称，字符串
                            # fields["channelname"] = fields.get('channelname')  # 频道名称，字符串
                            # fields["channelID"] = fields.get('channelID')  # 频道id，字符串
                            # article_fields["channelType"] = channel_type  # 频道type，字符串
                            # fields["url"] = contentJson['news']['webLink']  # 分享的网址，字符串
                            # fields["title"] = contentJson['news']['title']  # 文章标题，字符串
                            # if 'content' in contentJson.keys():
                            fields["content"] = contentJson['result'][0]['description']  # 文章内容，字符串
                            fields["images"] = InitClass().get_images(fields["content"])  # 正文图片，数组
                            # imgThumList = []
                            # for imgUrl in contentJson['thumbnails']:
                            #     imgThumList.append(imgUrl['url'])
                            # fields["articlecovers"] = imgThumList  # 列表封面，数组
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
                            # fields["channelname"] = fields.get('channelname')  # 频道名称，字符串
                            # fields["channelID"] = fields.get('channelID')  # 频道id，字符串
                            # article_fields["channelType"] = channel_type  # 频道type，字符串
                            # fields["url"] = contentJson['news']['webLink']  # 分享的网址，字符串
                            # fields["title"] = contentJson['news']['title']  # 文章标题，字符串
                            # if 'content' in contentJson.keys():
                            fields["content"] = contentJson['result'][0]['content']  # 文章内容，字符串
                            fields["images"] = InitClass().get_images(fields["content"])  # 正文图片，数组
                            # imgThumList = []
                            # for imgUrl in contentJson['thumbnails']:
                            #     imgThumList.append(imgUrl['url'])
                            # fields["articlecovers"] = imgThumList  # 列表封面，数组
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
                            fields["readnum"] = contentJson['result'][0]['view_count']  # 阅读数，数值
                            # fields["trannum"] = ''  # 转发数，数值
                            # fields["sharenum"] = ''  # 分享数，数值
                            # if 'author' in contentJson.keys():
                            fields["author"] = contentJson['result'][0]['author']  # 作者，字符串
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

    def getTopicArticles(self, channelname, channelid, topicId, topicNewsList):
        articlesparams = []
        for item in topicNewsList:
            try:
                article_fields = InitClass().article_fields()
                article_fields["channelname"] = channelname  # 频道名称，字符串
                article_fields["channelID"] = channelid  # 频道id，字符串
                # article_fields["channelType"] = channel_type  # 频道type，字符串
                # article_fields["url"] = item['h5url']  # 分享的网址，字符串
                article_fields["title"] = item['title']  # 文章标题，字符串
                # article_fields["content"] = item['webLink']  # 文章内容，字符串
                imgList = []
                if "pic1" in item.keys() and len(item['pic1']):
                    imgList.append(item['pic1'])
                if "pic2" in item.keys() and len(item['pic2']):
                    imgList.append(item['pic2'])
                if "pic3" in item.keys() and len(item['pic3']):
                    imgList.append(item['pic3'])
                article_fields["articlecovers"] = imgList  # 列表封面，数组
                # article_fields["images"] = ''  # 正文图片，数组
                # article_fields["videocover"] = [item['videoImg']]  # 视频封面，数组
                videoList = []
                if "video" in item.keys() and len(item['video']):
                    videoList.append(item['video'])
                article_fields["videos"] = videoList  # 视频地址，数组
                # article_fields["width"] = ''  # 视频宽，字符串
                # article_fields["height"] = ''  # 视频高，字符串
                # article_fields["source"] = item['source']  # 文章来源，字符串
                article_fields["pubtime"] = InitClass().date_time_stamp(item['publish_time'])  # 发布时间，时间戳（毫秒级，13位）
                # article_fields["createtime"] = item['createdate']  # 创建时间，时间戳（毫秒级，13位）
                # article_fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
                # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                # article_fields["playnum"] = ''  # 播放数，数值
                # article_fields["commentnum"] = item['commentNum']  # 评论数，数值
                # article_fields["readnum"] = ''  # 阅读数，数值
                # article_fields["trannum"] = ''  # 转发数，数值
                # article_fields["sharenum"] = ''  # 分享数，数值
                # article_fields["author"] = ''  # 作者，字符串
                # article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）

                article_fields["specialtopic"] = 1  # 是否是专题，数值（0标识不是，1标识是）
                article_fields["topicid"] = topicId  # 专题id，字符串

                if 'link_id' in item.keys() and item['link_id'] != 0:
                    if "others" in item.keys() and isinstance(item['others'], list) and len(item['others']):
                        article_fields["workerid"] = item['article_id']  # 文章id，字符串
                        article_fields["newstype"] = "QXDef"  # 自己添加新闻类型
                        article_fields["childNews"] = item['others']  # 相当于是个专题
                    else:
                        article_fields["workerid"] = item['link_id']  # 文章id，字符串
                        article_fields["newstype"] = "QXTopic"  # 自己添加新闻类型
                else:
                    article_fields["workerid"] = item['article_id']  # 文章id，字符串
                    article_fields["newstype"] = "QXDef"  # 自己添加新闻类型
                articleparam = InitClass().article_list_fields()
                articleparam["articelField"] = article_fields
                articlesparams.append(articleparam)
            except Exception as e:
                logging.info(e)
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
    appspider = JiangHanXinWen("江汉新闻")
    appspider.run()
