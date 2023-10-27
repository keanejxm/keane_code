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


def setListNewsParam(channelname, channelid, banner, item):
    try:
        article_fields = InitClass().article_fields()
        article_fields["channelname"] = channelname  # 频道名称，字符串
        article_fields["channelID"] = channelid  # 频道id，字符串
        if 'm2o_href' in item.keys() and 'm2o_title' in item.keys():
            article_fields["url"] = item['m2o_href']  # 分享的网址，字符串
            article_fields["title"] = item['title']  # 文章标题，字符串
            article_fields["content"] = item['m2o_href']  # 文章内容，字符串
            article_fields["articlecovers"] = [item['image_url']]  # 列表封面，数组
            # article_fields["images"] = ''  # 正文图片，数组
            # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
            # article_fields["videocover"] = [item['coverUrl']]  # 视频封面，数组
            # article_fields["width"] = ''  # 视频宽，字符串
            # article_fields["height"] = ''  # 视频高，字符串
            # article_fields["source"] = item['source']  # 文章来源，字符串
            # article_fields["pubtime"] = item['publish_time_stamp']  # 发布时间，时间戳（毫秒级，13位）
            article_fields["createtime"] = item['create_time']  # 创建时间，时间戳（毫秒级，13位）
            article_fields["updatetime"] = item['update_time']  # 更新时间，时间戳（毫秒级，13位）
            # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
            # article_fields["playnum"] = ''  # 播放数，数值
            # article_fields["commentnum"] = item['commentNum']  # 评论数，数值
            # article_fields["readnum"] = item['realRead']  # 阅读数，数值
            # article_fields["trannum"] = ''  # 转发数，数值
            # article_fields["sharenum"] = ''  # 分享数，数值
            # article_fields["author"] = ''  # 作者，字符串
            article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
            # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
            # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
            # article_fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
            article_fields["newsType"] = "qxweb"  # 自己添加新闻类型
        else:
            # article_fields["channelType"] = channel_type  # 频道type，字符串
            article_fields["url"] = item['content_url']  # 分享的网址，字符串
            if "news" == item['module_id']:
                article_fields["workerid"] = item['content_id']  # 文章id，字符串
            elif "special" == item['module_id']:
                article_fields["workerid"] = item['content_fromid']  # 文章id，字符串
            elif "livmedia" == item['module_id']:
                article_fields["workerid"] = item['content_id']  # 文章id，字符串
            elif "vod" == item['module_id']:
                article_fields["workerid"] = item['content_id']  # 文章id，字符串
            else:
                print(item)
            article_fields["title"] = item['title']  # 文章标题，字符串
            # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
            imgList = []
            if 'childs_data' in item.keys():
                for pic in item['childs_data']:
                    imgUrl = pic['host'] + pic['dir'] + pic['filepath'] + pic['filename']
                    imgList.append(imgUrl)
            article_fields["articlecovers"] = imgList  # 列表封面，数组
            # article_fields["images"] = ''  # 正文图片，数组
            # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
            # article_fields["videocover"] = [item['coverUrl']]  # 视频封面，数组
            # article_fields["width"] = ''  # 视频宽，字符串
            # article_fields["height"] = ''  # 视频高，字符串
            article_fields["source"] = item['source']  # 文章来源，字符串
            article_fields["pubtime"] = item['publish_time_stamp']  # 发布时间，时间戳（毫秒级，13位）
            article_fields["createtime"] = item['create_time_stamp']  # 创建时间，时间戳（毫秒级，13位）
            # article_fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
            # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
            # article_fields["playnum"] = ''  # 播放数，数值
            # article_fields["commentnum"] = item['commentNum']  # 评论数，数值
            # article_fields["readnum"] = item['realRead']  # 阅读数，数值
            # article_fields["trannum"] = ''  # 转发数，数值
            # article_fields["sharenum"] = ''  # 分享数，数值
            # article_fields["author"] = ''  # 作者，字符串
            article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
            # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
            # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
            # article_fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
            article_fields["newsType"] = item['module_id']  # 自己添加新闻类型
    except Exception as e:
        print(e)
    return article_fields


class ZhangShangWuHan(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://mobile.appwuhan.com/zswh6/news_recomend_column_v6.php"
        headers = {}
        method = "get"
        data = {
            "site_id": "1",
            "appid": "16",
            "appkey": "rFUm5PYocCj6e1h0m03t3WarVJcMV98c",
            "device_token": "ad8a80b197751caeece6bd6746e17766",
            "_member_id": "",
            "version": "5.6.1",
            "app_version": "5.6.1",
            "app_version": "5.6.1",
            "package_name": "com.hoge.android.wuhan",
            "system_version": "10",
            "phone_models": "ALP-AL00",
        }

        app_params1 = InitClass().app_params(url, headers, method, data=data)

        yield [app_params1]

    def analyze_channel(self, channelsres):
        print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            if "http://mobile.appwuhan.com/zswh6/news_recomend_column_v6.php" == k:
                channelList = json.loads(v)
                for channel in channelList:
                    channelid = str(channel['id'])
                    channelname = channel['name']
                    if '334' == channelid:  # 城区
                        url_city = "http://mobile.appwuhan.com/zswh6/news_recomend_column_fid.php"
                        headers_city = {}
                        data_city = {
                            "appid": "16",
                            "appkey": "rFUm5PYocCj6e1h0m03t3WarVJcMV98c",
                            "client_id_android": "5db1985483eda6fdffa003033bdf0015",
                            "device_token": "ad8a80b197751caeece6bd6746e17766",
                            "_member_id": "",
                            "version": "5.6.1",
                            "app_version": "5.6.1",
                            "app_version": "5.6.1",
                            "package_name": "com.hoge.android.wuhan",
                            "system_version": "10",
                            "phone_models": "ALP-AL00",
                            "fid": "334",
                            "name": "城区",
                        }
                        channel_city_res = requests.get(url_city, headers=headers_city,
                                                        params=data_city).content.decode()
                        channel_city_list = json.loads(channel_city_res)
                        for channel_city in channel_city_list:
                            channel_city_id = str(channel_city['id'])
                            channel_city_name = channel_city['name']
                            channel_city_param = InitClass().channel_fields(channel_city_id, channel_city_name)
                            channelparams.append(channel_city_param)
                    else:
                        channelparam = InitClass().channel_fields(channelid, channelname)
                        channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        headers = {}
        method = "get"
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            if "-1" == channelid:  # 头条
                url = "http://mobile.appwuhan.com/zswh6/index.php"
                data = {
                    "site_id": "1",
                    "appid": "16",
                    "appkey": "rFUm5PYocCj6e1h0m03t3WarVJcMV98c",
                    "client_id_android": "5db1985483eda6fdffa003033bdf0015",
                    "device_token": "ad8a80b197751caeece6bd6746e17766",
                    "_member_id": "",
                    "version": "5.6.1",
                    "app_version": "5.6.1",
                    "app_version": "5.6.1",
                    "package_name": "com.hoge.android.wuhan",
                    "system_version": "10",
                    "phone_models": "ALP-AL00",
                    "count": "20",
                    "offset": "0",
                }
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                           channelid=channelid)
                articlelistsparams.append(articlelist_param)
            elif '336' == channelid:  # 见微
                url = "http://plive.appwuhan.com/Common/getWxLiveList"
                data = {
                    "num": "10",
                    "page": "1",
                }
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                           channelid=channelid)
                articlelistsparams.append(articlelist_param)
            else:
                url = "http://mobile.appwuhan.com/zswh6/news.php"
                data = {
                    "num": "10",
                    "site_id": "1",
                    "appid": "16",
                    "appkey": "rFUm5PYocCj6e1h0m03t3WarVJcMV98c",
                    "client_id_android": "5db1985483eda6fdffa003033bdf0015",
                    "device_token": "ad8a80b197751caeece6bd6746e17766",
                    "_member_id": "",
                    "version": "5.6.1",
                    "app_version": "5.6.1",
                    "app_version": "5.6.1",
                    "package_name": "com.hoge.android.wuhan",
                    "system_version": "10",
                    "phone_models": "ALP-AL00",
                    "count": "20",
                    "offset": "0",
                    "column_id": channelid,
                    "column_name": channelname,
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
            banners = articleslistres.get("banners")
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    print(articleslists)
                    if isinstance(articleslists, dict):
                        if 'list' in articleslists.keys():
                            for item_list in articleslists['list']:
                                article_fields = setListNewsParam(channelname, channelid, 0, item_list)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        if 'shortVideo' in articleslists.keys():
                            for item_short in articleslists['shortVideo']:
                                article_fields = setListNewsParam(channelname, channelid, 0, item_short)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        if 'top' in articleslists.keys():
                            for item_top in articleslists['top']:
                                article_fields = setListNewsParam(channelname, channelid, 0, item_top)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        if 'hot' in articleslists.keys():
                            for item_slide in articleslists['slide']:
                                article_fields = setListNewsParam(channelname, channelid, 0, item_slide)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        if 'slide' in articleslists.keys():
                            for item_slide in articleslists['slide']:
                                article_fields = setListNewsParam(channelname, channelid, 1, item_slide)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        else:
                            print(articleslists)
                    elif isinstance(articleslists, list):
                        for item_live in articleslists:
                            article_fields = setListNewsParam(channelname, channelid, 1, item_live)
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
            newsType = article_field.get('newsType')
            workerid = article_field.get('workerid')
            if workerid:
                if "special" == newsType:
                    url = "http://mobile.appwuhan.com/zswh6/special_content.php"
                    headers = {}
                    method = "get"
                    data = {
                        "appid": "16",
                        "appkey": "rFUm5PYocCj6e1h0m03t3WarVJcMV98c",
                        "client_id_android": "5db1985483eda6fdffa003033bdf0015",
                        "device_token": "ad8a80b197751caeece6bd6746e17766",
                        "_member_id": "",
                        "version": "5.6.1",
                        "app_version": "5.6.1",
                        "app_version": "5.6.1",
                        "package_name": "com.hoge.android.wuhan",
                        "system_version": "10",
                        "phone_models": "ALP-AL00",
                        "column_id": workerid,
                        "offset": "0",
                        "new_style": "2",
                    }
                    articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                                     article_field=article_field)
                    articleparams.append(articleparam)
                else:
                    url = "http://mobile.appwuhan.com/zswh6/item.php"
                    headers = {}
                    method = "get"
                    data = {
                        "appid": "16",
                        "appkey": "rFUm5PYocCj6e1h0m03t3WarVJcMV98c",
                        "client_id_android": "5db1985483eda6fdffa003033bdf0015",
                        "device_token": "ad8a80b197751caeece6bd6746e17766",
                        "_member_id": "",
                        "version": "5.6.1",
                        "app_version": "5.6.1",
                        "app_version": "5.6.1",
                        "package_name": "com.hoge.android.wuhan",
                        "system_version": "10",
                        "phone_models": "ALP-AL00",
                        "id": workerid,
                    }
                    articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                                     article_field=article_field)
                    articleparams.append(articleparam)
            else:
                print("外链详情", article_field)
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
                newsType = fields.get('newsType')
                if "special" == newsType:  # 跳转到专题
                    topicFields = InitClass().topic_fields()
                    topicFields["topicID"] = fields['workerid']  # 专题id，app内唯一标识
                    topicFields["platformName"] = appname  # 平台名字（app名字）
                    # topicFields["platformID"] = fields['workerid']
                    topicFields["channelName"] = fields['channelname']  # 频道名字
                    topicFields["channelID"] = fields['channelID']  # 频道id
                    topicFields["topicUrl"] = fields['url']  # topicUrl
                    topicFields["title"] = fields['title']
                    # topicFields["digest"] = contentJson['description']  # 简介，摘要
                    # topicFields["topicCover"] = [contentJson['topicImgUrl']]
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
                    topicFields["createTime"] = fields['createtime']
                    # topicFields["updateTime"] = fields['workerid']
                    # topicItem = []
                    # for topicCate in contentJson:
                    #     topicItem += topicCate['childs_data']
                    topicArticles = self.getTopicArticles(fields['channelname'], fields['channelID'], fields['title'],
                                                          fields['workerid'], contentJson)
                    articleparams = self.getarticleparams(topicArticles.__next__())
                    articlesres = self.getarticlehtml(articleparams.__next__())
                    self.analyzearticle(articlesres.__next__())
                else:
                    fields["appname"] = appname  # 应用名称，字符串
                    # fields["channelname"] = channelname  # 频道名称，字符串
                    # fields["channelID"] = channelid  # 频道id，字符串
                    # fields["channelType"] = channel_type  # 频道type，字符串
                    # fields["url"] = item['jsonUrl']  # 分享的网址，字符串
                    # fields["workerid"] = item['ctId']  # 文章id，字符串
                    # fields["title"] = item['title']  # 文章标题，字符串
                    if 'content' in contentJson.keys():
                        content = contentJson['content']
                        index = 0
                        for img_item in contentJson['material']:
                            if len(img_item.keys()) == 1 and "pic" in img_item.keys():
                                img_url = img_item['pic']['host'] + img_item['pic']['dir'] + img_item['pic'][
                                    'filepath'] + img_item['pic']['filename']
                                content.replace(f'<div m2o_mark="pic_{index}" style="display:none"></div>',
                                                f'<img src={img_url}/>')
                                index += 1
                            else:
                                print(img_item)
                        fields["content"] = content  # 文章内容，字符串
                        # fields["articlecovers"] = imgList  # 列表封面，数组
                        fields["images"] = InitClass.get_images(fields["content"])  # 正文图片，数组
                    if 'hostwork' in contentJson.keys() and 'video_path' in contentJson.keys() and 'video_filename' in contentJson.keys():
                        videourl = contentJson['hostwork'] + "/" + contentJson['video_path'] + contentJson[
                            'video_filename']
                        fields["videos"] = [videourl]  # 视频地址，数组
                    # fields["videocover"] = [item['videoImg']]  # 视频封面，数组
                    # fields["width"] = ''  # 视频宽，字符串
                    # fields["height"] = ''  # 视频高，字符串
                    # fields["source"] = ''  # 文章来源，字符串
                    # fields["pubtime"] = ''  # 发布时间，时间戳（毫秒级，13位）
                    # fields["createtime"] = contentJson['resultData']['createDate']  # 创建时间，时间戳（毫秒级，13位）
                    # fields["updatetime"] = contentJson['resultData']['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                    # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                    # fields["playnum"] = ''  # 播放数，数值
                    # fields["commentnum"] = item['commentNum']  # 评论数，数值
                    # fields["readnum"] = contentJson['resultData']['read']  # 阅读数，数值
                    # fields["trannum"] = ''  # 转发数，数值
                    # fields["sharenum"] = ''  # 分享数，数值
                    # fields["author"] = ''  # 作者，字符串
                    # fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                    # fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                    # fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                    # fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
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
                if 'm2o_href' in item.keys() and 'm2o_title' in item.keys():
                    article_fields["url"] = item['m2o_href']  # 分享的网址，字符串
                    article_fields["title"] = item['title']  # 文章标题，字符串
                    article_fields["content"] = item['m2o_href']  # 文章内容，字符串
                    article_fields["articlecovers"] = [item['image_url']]  # 列表封面，数组
                    # article_fields["images"] = ''  # 正文图片，数组
                    # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                    # article_fields["videocover"] = [item['coverUrl']]  # 视频封面，数组
                    # article_fields["width"] = ''  # 视频宽，字符串
                    # article_fields["height"] = ''  # 视频高，字符串
                    # article_fields["source"] = item['source']  # 文章来源，字符串
                    # article_fields["pubtime"] = item['publish_time_stamp']  # 发布时间，时间戳（毫秒级，13位）
                    article_fields["createtime"] = item['create_time']  # 创建时间，时间戳（毫秒级，13位）
                    article_fields["updatetime"] = item['update_time']  # 更新时间，时间戳（毫秒级，13位）
                    # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                    # article_fields["playnum"] = ''  # 播放数，数值
                    # article_fields["commentnum"] = item['commentNum']  # 评论数，数值
                    # article_fields["readnum"] = item['realRead']  # 阅读数，数值
                    # article_fields["trannum"] = ''  # 转发数，数值
                    # article_fields["sharenum"] = ''  # 分享数，数值
                    # article_fields["author"] = ''  # 作者，字符串
                    article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                    # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                    # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                    # article_fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
                    article_fields["newsType"] = "qxweb"  # 自己添加新闻类型
                else:
                    # article_fields["channelType"] = channel_type  # 频道type，字符串
                    article_fields["url"] = item['content_url']  # 分享的网址，字符串
                    if "news" == item['module_id']:
                        article_fields["workerid"] = item['content_id']  # 文章id，字符串
                    elif "special" == item['module_id']:
                        article_fields["workerid"] = item['content_fromid']  # 文章id，字符串
                    elif "livmedia" == item['module_id']:
                        article_fields["workerid"] = item['content_id']  # 文章id，字符串
                    elif "vod" == item['module_id']:
                        article_fields["workerid"] = item['content_id']  # 文章id，字符串
                    else:
                        print(item)
                    article_fields["title"] = item['title']  # 文章标题，字符串
                    # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
                    imgList = []
                    if 'childs_data' in item.keys():
                        for pic in item['childs_data']:
                            imgUrl = pic['host'] + pic['dir'] + pic['filepath'] + pic['filename']
                            imgList.append(imgUrl)
                    article_fields["articlecovers"] = imgList  # 列表封面，数组
                    # article_fields["images"] = ''  # 正文图片，数组
                    # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                    # article_fields["videocover"] = [item['coverUrl']]  # 视频封面，数组
                    # article_fields["width"] = ''  # 视频宽，字符串
                    # article_fields["height"] = ''  # 视频高，字符串
                    article_fields["source"] = item['source']  # 文章来源，字符串
                    article_fields["pubtime"] = item['publish_time_stamp']  # 发布时间，时间戳（毫秒级，13位）
                    article_fields["createtime"] = item['create_time_stamp']  # 创建时间，时间戳（毫秒级，13位）
                    # article_fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                    # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                    # article_fields["playnum"] = ''  # 播放数，数值
                    # article_fields["commentnum"] = item['commentNum']  # 评论数，数值
                    # article_fields["readnum"] = item['realRead']  # 阅读数，数值
                    # article_fields["trannum"] = ''  # 转发数，数值
                    # article_fields["sharenum"] = ''  # 分享数，数值
                    # article_fields["author"] = ''  # 作者，字符串
                    # article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                    article_fields["specialtopic"] = 1  # 是否是专题，数值（0标识不是，1标识是）
                    article_fields["topicid"] = topicId  # 专题id，字符串
                    article_fields["topicTitle"] = topicTitle  # 专题标题，字符串
                    article_fields["newsType"] = item['module_id']  # 自己添加新闻类型
                articleparam = InitClass().article_list_fields()
                articleparam["articelField"] = article_fields
                articlesparams.append(articleparam)
            except Exception as e:
                print(e)

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
    appspider = ZhangShangWuHan("掌上武汉")
    appspider.run()
