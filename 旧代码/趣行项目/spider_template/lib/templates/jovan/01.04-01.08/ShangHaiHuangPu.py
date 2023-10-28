# -*- encoding:utf-8 -*-
"""
@功能:湖北日报解析模板
@AUTHOR：jovan
@文件名：HuBeiRiBao.py
@时间：2020年12月22日 15:58:24
"""

import json
from urllib.parse import urlparse
import logging
import random
import time

import requests

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass

banner_data = []


def setListNewsParam(channelname, channelid, banner, item):
    try:
        article_fields = InitClass().article_fields()
        article_fields["channelname"] = channelname  # 频道名称，字符串
        article_fields["channelID"] = channelid  # 频道id，字符串
        # article_fields["channelType"] = channel_type  # 频道type，字符串
        # article_fields["url"] = url  # 分享的网址，字符串
        article_fields["workerid"] = item['ID']  # 文章id，字符串
        article_fields["title"] = item['Title']  # 文章标题，字符串
        # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
        imgList = []
        if item['Logo']:
            imgList.append(item['Logo'])
        article_fields["articlecovers"] = imgList  # 列表封面，数组
        # article_fields["images"] = ''  # 正文图片，数组
        # if 'videoUrl' in item.keys() and item['videoUrl']:
        #     article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
        # if 'videoPoster' in item.keys() and item['videoPoster']:
        #     article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
        # article_fields["width"] = ''  # 视频宽，字符串
        # article_fields["height"] = ''  # 视频高，字符串
        article_fields["source"] = item['source']  # 文章来源，字符串
        article_fields["pubtime"] = InitClass().date_time_stamp(item['PublishDate'])  # 发布时间，时间戳（毫秒级，13位）
        # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
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
        # article_fields["newsType"] = item['type']  # 自己添加新闻类型
    except Exception as e:
        print(e)
    return article_fields


class ShangHaiHuangPu(Appspider):

    @staticmethod
    def get_app_params():
        url1 = "http://conf.i2863.com/App_Config/app/home"
        headers = {
            "Host": "conf.i2863.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.0",
        }
        method = "get"
        data = {
            "tagName": "shshpqxwzx",
            "siteId": "204",
        }

        app_params1 = InitClass().app_params(url1, headers, method, data=data)

        yield [app_params1]

    def analyze_channel(self, channelsres):
        print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            if "http://conf.i2863.com/App_Config/app/home" == k:
                channelList = json.loads(v)
                for banner in channelList['data']['topNews']:
                    banner_data.append(banner)
                for channel in channelList['data']['secMenus']:
                    if 1 == channel['typeId']:
                        url = f'http://conf.i2863.com/App_Config/menuSec/getMenuSecList'
                        headers = {
                            "Host": "conf.i2863.com",
                            "Connection": "Keep-Alive",
                            "Accept-Encoding": "gzip",
                            "User-Agent": "okhttp/3.12.0",
                        }
                        data = {
                            "tagName": "shshpqxwzx",
                            "siteId": "204",
                            "menuId": channel['secondId'],
                            "menuType": "-1",
                        }
                        channel_res = requests.get(url, headers=headers, params=data).content.decode()
                        channel_list = json.loads(channel_res)
                        for channel_child in channel_list['data']:
                            channelid = channel_child['sectionId']
                            channelname = channel_child['sectionName']
                            channelparam = InitClass().channel_fields(channelid, channelname)
                            channelparams.append(channelparam)
                    else:
                        channelid = channel['url']
                        channelname = channel['menuName']
                        if channelid.isnumeric():
                            channelparam = InitClass().channel_fields(channelid, channelname)
                            channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        headers = {
            "Host": "conf.i2863.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.0",
        }
        method = "get"
        url = f'http://conf.i2863.com/App_Config/app/polNews'
        data = {
            "siteId": "204",
            "tagName": "shshpqxwzx",
            "ID": "0",
            "page": "1",
            "sectionId": "null",
            "type": "0",
        }
        articlelist_param = InitClass().articlelists_params_fields(url, headers, method, "推荐", data=data,
                                                                   channelid=-1)
        articlelistsparams.append(articlelist_param)

        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            url = f'http://conf.i2863.com/App_Config/app/homeNews'
            data = {
                "siteId": "204",
                "InnerCode": channelid,
                "ID": "0",
                "tagName": "shshpqxwzx",
            }
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                       channelid=channelid)
            articlelistsparams.append(articlelist_param)
        url = f'http://conf.i2863.com/App_Config/live/listByType'
        data = {
            "siteId": "204",
            "tagName": "shshpqxwzx",
        }
        articlelist_param = InitClass().articlelists_params_fields(url, headers, method, "直播", data=data,
                                                                   channelid=-2)
        articlelistsparams.append(articlelist_param)
        yield articlelistsparams

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for item_banner in banner_data:
            article_fields = InitClass().article_fields()
            # article_fields["channelname"] = channelname  # 频道名称，字符串
            # article_fields["channelID"] = channelid  # 频道id，字符串
            # article_fields["channelType"] = channel_type  # 频道type，字符串
            article_fields["url"] = item_banner['ArticleURL']  # 分享的网址，字符串
            article_fields["workerid"] = item_banner['ArticleID']  # 文章id，字符串
            article_fields["title"] = item_banner['ArticleTitle']  # 文章标题，字符串
            # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
            imgList = []
            if item_banner['ArticleImg']:
                imgList.append(item_banner['ArticleImg'])
            article_fields["articlecovers"] = imgList  # 列表封面，数组
            # article_fields["images"] = ''  # 正文图片，数组
            # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
            # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
            # article_fields["width"] = ''  # 视频宽，字符串
            # article_fields["height"] = ''  # 视频高，字符串
            # article_fields["source"] = ''  # 文章来源，字符串
            article_fields["pubtime"] = InitClass().date_time_stamp(item_banner['PublishDate'])  # 发布时间，时间戳（毫秒级，13位）
            # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
            # article_fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
            # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
            # article_fields["playnum"] = ''  # 播放数，数值
            # article_fields["commentnum"] = item['commentNum']  # 评论数，数值
            # article_fields["readnum"] = item['realRead']  # 阅读数，数值
            # article_fields["trannum"] = ''  # 转发数，数值
            # article_fields["sharenum"] = ''  # 分享数，数值
            # article_fields["author"] = ''  # 作者，字符串
            article_fields["banner"] = 1  # banner标记，数值（0标识不是，1标识是）
            # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
            # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
            # article_fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
            # article_fields["newsType"] = item['type']  # 自己添加新闻类型
            articleparam = InitClass().article_list_fields()
            articleparam["articelField"] = article_fields
            articlesparams.append(articleparam)
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    if isinstance(articleslists['data'], list):
                        for item in articleslists['data']:
                            article_fields = {}
                            if 'news' in item.keys():
                                article_fields = setListNewsParam(channelname, channelid, 0, item['news'])
                            else:
                                article_fields = setListNewsParam(channelname, channelid, 0, item)
                            articleparam = InitClass().article_list_fields()
                            articleparam["articelField"] = article_fields
                            articlesparams.append(articleparam)
                    elif isinstance(articleslists['data'], dict):
                        for k, v in articleslists['data'].items():
                            if isinstance(v, list):
                                for item in v:
                                    article_fields = InitClass().article_fields()
                                    article_fields["channelname"] = channelname  # 频道名称，字符串
                                    article_fields["channelID"] = channelid  # 频道id，字符串
                                    # article_fields["channelType"] = channel_type  # 频道type，字符串
                                    article_fields["url"] = item['roomShareUrl']  # 分享的网址，字符串
                                    article_fields["workerid"] = item['roomId']  # 文章id，字符串
                                    article_fields["title"] = item['title']  # 文章标题，字符串
                                    # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
                                    imgList = []
                                    if item['logo']:
                                        imgList.append(item['logo'])
                                    article_fields["articlecovers"] = imgList  # 列表封面，数组
                                    # article_fields["images"] = ''  # 正文图片，数组
                                    # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                                    # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
                                    # article_fields["width"] = ''  # 视频宽，字符串
                                    # article_fields["height"] = ''  # 视频高，字符串
                                    # article_fields["source"] = ''  # 文章来源，字符串
                                    article_fields["pubtime"] = InitClass().date_time_stamp(
                                        item['publishdate'])  # 发布时间，时间戳（毫秒级，13位）
                                    # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                                    # article_fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                                    # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                                    # article_fields["playnum"] = ''  # 播放数，数值
                                    # article_fields["commentnum"] = item['commentNum']  # 评论数，数值
                                    # article_fields["readnum"] = item['realRead']  # 阅读数，数值
                                    # article_fields["trannum"] = ''  # 转发数，数值
                                    # article_fields["sharenum"] = ''  # 分享数，数值
                                    # article_fields["author"] = ''  # 作者，字符串
                                    article_fields["banner"] = 0  # banner标记，数值（0标识不是，1标识是）
                                    # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                                    # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                                    # article_fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
                                    # article_fields["newsType"] = item['type']  # 自己添加新闻类型
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                            else:
                                print(k, v)
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
            workerid = article_field.get('workerid')
            channelID = article_field.get('channelID')
            # newsType = article_field.get('newsType')
            url = ""
            if -2 == channelID:  # 直播
                url = f'http://livenewsapi.i2863.com/scene/detail?userName=null&sceneId={workerid}'
            else:
                url = f'http://conf.i2863.com/App_Config/news/commonNews?tagName=shshpqxwzx&userName=null&siteId=204&newsId={workerid}'
            headers = {
                "Host": urlparse(url).netloc,
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.12.0",
            }
            method = "get"
            articleparam = InitClass().article_params_fields(url, headers, method, article_field=article_field)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            appname = article.get("appname")
            fields = article.get("articleField")
            try:
                if article.get("articleres"):
                    contentJson = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                    print(contentJson)

                    # if 'activeArticle' in contentJson['data'] and len(contentJson['data']['activeArticle']):
                    #     topicFields = InitClass().topic_fields()
                    #     topicFields["topicID"] = fields['workerid']  # 专题id，app内唯一标识
                    #     topicFields["platformName"] = appname  # 平台名字（app名字）
                    #     # topicFields["platformID"] = fields['workerid']
                    #     topicFields["channelName"] = fields['channelname']  # 频道名字
                    #     topicFields["channelID"] = fields['channelID']  # 频道id
                    #     topicFields["topicUrl"] = fields['url']  # topicUrl
                    #     topicFields["title"] = fields['title']
                    #     topicFields["digest"] = contentJson['data']['Content']  # 简介，摘要
                    #     topicFields["topicCover"] = fields['articlecovers']
                    #     topicFields["pubTime"] = fields['pubtime']  # 时间戳
                    #     # topicFields["articleNum"] = fields['workerid']  # 专题内的文章数量
                    #     # topicFields["newestArticleID"] = fields['workerid']  # 最新发布的文章id
                    #     # topicFields["articlesNumPerHour"] = fields['workerid']
                    #     # topicFields["original"] = fields['workerid']
                    #     # topicFields["firstMedia"] = fields['workerid']
                    #     # topicFields["transPower"] = fields['workerid']
                    #     # topicFields["hotDegree"] = fields['workerid']
                    #     # topicFields["wordsFreq"] = fields['workerid']
                    #     # topicFields["hotDegreeTrend"] = fields['workerid']
                    #     # topicFields["emotionTrend"] = fields['workerid']
                    #     # topicFields["region"] = fields['workerid']
                    #     # topicFields["spreadPath"] = fields['workerid']
                    #     # topicFields["createTime"] = fields['workerid']
                    #     # topicFields["updateTime"] = fields['workerid']
                    #     topicItem = contentJson['data']['activeArticle']
                    #     # for topicCate in contentJson['data']['listdata']:
                    #     #     topicItem += topicCate['item']
                    #     topicArticles = self.getTopicArticles(fields['channelname'], fields['channelID'],
                    #                                           topicFields['title'],
                    #                                           topicFields["topicID"], topicItem)
                    #     articleparams = self.getarticleparams(topicArticles.__next__())
                    #     articlesres = self.getarticlehtml(articleparams.__next__())
                    #     self.analyzearticle(articlesres.__next__())
                    # else:
                    fields["appname"] = appname  # 应用名称，字符串
                    # fields["channelname"] = channelname  # 频道名称，字符串
                    # fields["channelID"] = channelid  # 频道id，字符串
                    # fields["channelType"] = channel_type  # 频道type，字符串
                    # fields["url"] = contentJson['source_url']  # 分享的网址，字符串
                    # fields["workerid"] = item['ctId']  # 文章id，字符串
                    # fields["title"] = item['title']  # 文章标题，字符串
                    if 'Content' in contentJson['data'].keys():
                        fields["content"] = contentJson['data']['Content']  # 文章内容，字符串
                    # fields["articlecovers"] = imgList  # 列表封面，数组
                    fields["images"] = InitClass.get_images(fields["content"])  # 正文图片，数组
                    if 'playerpath' in contentJson['data'].keys() and contentJson['data']['playerpath']:
                        fields["videos"] = [contentJson['data']['playerpath']]  # 视频地址，数组
                    if 'hlsUrl' in contentJson['data'].keys() and contentJson['data']['hlsUrl']:
                        fields["videos"] = [contentJson['data']['hlsUrl']]  # 视频地址，数组
                    # fields["videocover"] = [item['videoImg']]  # 视频封面，数组
                    # fields["width"] = ''  # 视频宽，字符串
                    # fields["height"] = ''  # 视频高，字符串
                    # fields["source"] = contentJson['source']  # 文章来源，字符串
                    # fields["pubtime"] = contentJson['ptime']  # 发布时间，时间戳（毫秒级，13位）
                    # fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                    # fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                    # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                    # fields["playnum"] = ''  # 播放数，数值
                    # fields["commentnum"] = item['commentNum']  # 评论数，数值
                    # fields["readnum"] = contentJson['views']  # 阅读数，数值
                    # fields["trannum"] = ''  # 转发数，数值
                    # fields["sharenum"] = ''  # 分享数，数值
                    # fields["author"] = contentJson['username']  # 作者，字符串
                    # fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                    # fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                    # fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                    # fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
                    print(json.dumps(fields, indent=4, ensure_ascii=False))
                else:
                    print("未获取到详情", fields)
            except Exception as e:
                num += 1
                logging.info(f"错误数量{num},{e}")

    # def getTopicArticles(self, channelname, channelid, topicTitle, topicId, topicNewsList):
    #     articlesparams = []
    #     for item in topicNewsList:
    #         try:
    #             article_fields = InitClass().article_fields()
    #             article_fields["channelname"] = channelname  # 频道名称，字符串
    #             article_fields["channelID"] = channelid  # 频道id，字符串
    #             # article_fields["channelType"] = channel_type  # 频道type，字符串
    #             # article_fields["url"] = url  # 分享的网址，字符串
    #             article_fields["workerid"] = item['ID']  # 文章id，字符串
    #             article_fields["title"] = item['Title']  # 文章标题，字符串
    #             # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
    #             imgList = []
    #             if item['Logo']:
    #                 imgList.append(item['Logo'])
    #             article_fields["articlecovers"] = imgList  # 列表封面，数组
    #             # article_fields["images"] = ''  # 正文图片，数组
    #             # if 'videoUrl' in item.keys() and item['videoUrl']:
    #             #     article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
    #             # if 'videoPoster' in item.keys() and item['videoPoster']:
    #             #     article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
    #             # article_fields["width"] = ''  # 视频宽，字符串
    #             # article_fields["height"] = ''  # 视频高，字符串
    #             # article_fields["source"] = item['source']  # 文章来源，字符串
    #             article_fields["pubtime"] = InitClass().date_time_stamp(item['PublishDate'])  # 发布时间，时间戳（毫秒级，13位）
    #             # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
    #             # article_fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
    #             # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
    #             # article_fields["playnum"] = ''  # 播放数，数值
    #             # article_fields["commentnum"] = item['commentNum']  # 评论数，数值
    #             # article_fields["readnum"] = item['realRead']  # 阅读数，数值
    #             # article_fields["trannum"] = ''  # 转发数，数值
    #             # article_fields["sharenum"] = ''  # 分享数，数值
    #             # article_fields["author"] = ''  # 作者，字符串
    #             article_fields["banner"] = 0  # banner标记，数值（0标识不是，1标识是）
    #             article_fields["specialtopic"] = 1  # 是否是专题，数值（0标识不是，1标识是）
    #             article_fields["topicid"] = topicId  # 专题id，字符串
    #             article_fields["topicTitle"] = topicTitle  # 专题标题，字符串
    #             # article_fields["newsType"] = item['type']  # 自己添加新闻类型
    #             articleparam = InitClass().article_list_fields()
    #             articleparam["articelField"] = article_fields
    #             articlesparams.append(articleparam)
    #         except Exception as e:
    #             print(e)
    #
    #     yield articlesparams

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
    appspider = ShangHaiHuangPu("上海黄浦")
    appspider.run()
