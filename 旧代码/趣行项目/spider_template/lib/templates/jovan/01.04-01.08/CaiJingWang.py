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
import re
import time

import requests

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


def setListNewsParam(channelname, channelid, channeltype, banner, item):
    try:
        article_fields = InitClass().article_fields()
        article_fields["channelname"] = channelname  # 频道名称，字符串
        article_fields["channelID"] = channelid  # 频道id，字符串
        article_fields["channelType"] = channeltype  # 频道type，字符串
        # article_fields["url"] = item['url']  # 分享的网址，字符串
        if 'contentid' in item.keys():
            article_fields["workerid"] = item['contentid']  # 文章id，字符串
        article_fields["title"] = item['title']  # 文章标题，字符串
        # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
        imgList = []
        if 'thumb' in item.keys() and item['thumb']:
            imgList.append(item['thumb'])
        article_fields["articlecovers"] = imgList  # 列表封面，数组
        # article_fields["images"] = ''  # 正文图片，数组
        videoList = []
        if 'video' in item.keys() and item['video']:
            videoList.append(item['video'])
        article_fields["videos"] = videoList  # 视频地址，数组
        # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
        # article_fields["width"] = ''  # 视频宽，字符串
        # article_fields["height"] = ''  # 视频高，字符串
        if 'source' in item.keys():
            article_fields["source"] = item['source']  # 文章来源，字符串
        if 'published' in item.keys():
            article_fields["pubtime"] = item['published']  # 发布时间，时间戳（毫秒级，13位）
        # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
        # article_fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
        # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
        # article_fields["playnum"] = ''  # 播放数，数值
        # article_fields["commentnum"] = item['CommentCount']  # 评论数，数值
        # article_fields["readnum"] = item['ReadCount']  # 阅读数，数值
        # article_fields["trannum"] = ''  # 转发数，数值
        # article_fields["sharenum"] = item['ShareCount']  # 分享数，数值
        # article_fields["author"] = ''  # 作者，字符串
        article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
        # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
        # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
        # article_fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
        if 'type' in item.keys():
            article_fields["newsType"] = item['type']  # 自己添加新闻类型
        else:
            article_fields["newsType"] = channeltype  # 自己添加新闻类型
        if 'url' in item.keys():
            article_fields["detailUrl"] = item['url']  # 自己添加新闻类型
        else:
            article_fields["detailUrl"] = ""  # 自己添加新闻类型
    except Exception as e:
        print(e)
    return article_fields


class CaiJingWang(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://seecappcjs.caijing.com.cn/android.json"
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; ALP-AL00 Build/HUAWEIALP-AL00)",
            "Host": "seecappcjs.caijing.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        method = "get"
        app_params1 = InitClass().app_params(url, headers, method)

        yield [app_params1]

    def analyze_channel(self, channelsres):
        print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            if "http://seecappcjs.caijing.com.cn/android.json" == k:
                channelList = json.loads(v)
                for channel in channelList['data']['category']:
                    channelid = re.findall(r'\b\d+\b', channel['url'])[0]
                    channelname = channel['title']
                    channelType = channel['type']
                    url = channel['url']
                    channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channelType,
                                                              categoryid=url)
                    channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = ""
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; ALP-AL00 Build/HUAWEIALP-AL00)",
            "Host": "seecappcjs.caijing.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        method = "get"
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channelType = channel.get("channeltype")
            url = channel.get("categoryid")
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid=channelid, channeltype=channelType)
            articlelistsparams.append(articlelist_param)
        yield articlelistsparams

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            channeltype = articleslistres.get("channelType")
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    print(articleslists)
                    if 'data' in articleslists.keys():  # banner
                        if 'slider' in articleslists['data'].keys():
                            for item_head in articleslists['data']['slider']:
                                article_fields = setListNewsParam(channelname, channelid, channeltype, 1, item_head)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        if 'lists' in articleslists['data'].keys():
                            for item_article in articleslists['data']['lists']:
                                article_fields = setListNewsParam(channelname, channelid, channeltype, 0, item_article)
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
        url = ""
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; ALP-AL00 Build/HUAWEIALP-AL00)",
            "Host": "seecappcjs.caijing.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        method = "get"
        for article in articles:
            article_field = article.get('articelField')
            url = article_field.get('detailUrl')
            newsType = article_field.get('newsType')
            if 5 == newsType:  # 外链
                print("没有详情接口外链：", article_field)
            else:
                if url:
                    articleparam = InitClass().article_params_fields(url, headers, method, article_field=article_field)
                    articleparams.append(articleparam)
                else:
                    print("没有详情接口：", article_field)

        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            appname = article.get("appname")
            fields = article.get("articleField")
            newsType = fields.get('newsType')

            try:
                if article.get("articleres"):
                    contentJson = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                    # print(contentJson)
                    if 3 == newsType:  # 专题
                        topicFields = InitClass().topic_fields()
                        topicFields["topicID"] = fields['workerid']  # 专题id，app内唯一标识
                        topicFields["platformName"] = appname  # 平台名字（app名字）
                        # topicFields["platformID"] = fields['workerid']
                        topicFields["channelName"] = fields['channelname']  # 频道名字
                        topicFields["channelID"] = fields['channelID']  # 频道id
                        topicFields["topicUrl"] = contentJson['data']['share']  # topicUrl
                        topicFields["title"] = fields['title']
                        topicFields["digest"] = contentJson['data']['description']  # 简介，摘要
                        topicFields["topicCover"] = fields['articlecovers']
                        topicFields["pubTime"] = contentJson['data']['published']  # 时间戳
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
                        topicItem = []
                        for category in contentJson['data']['category']:
                            topicItem += category['lists']
                        topicArticles = self.getTopicArticles(fields['channelname'], fields['channelID'],
                                                              fields['channelType'], topicFields['title'],
                                                              topicFields["topicID"], topicItem)
                        articleparams = self.getarticleparams(topicArticles.__next__())
                        articlesres = self.getarticlehtml(articleparams.__next__())
                        self.analyzearticle(articlesres.__next__())
                    elif 6 == newsType:  # 杂志
                        topicFields = InitClass().topic_fields()
                        topicFields["topicID"] = fields['workerid']  # 专题id，app内唯一标识
                        topicFields["platformName"] = appname  # 平台名字（app名字）
                        # topicFields["platformID"] = fields['workerid']
                        topicFields["channelName"] = fields['channelname']  # 频道名字
                        topicFields["channelID"] = fields['channelID']  # 频道id
                        topicFields["topicUrl"] = contentJson['data']['share']  # topicUrl
                        topicFields["title"] = fields['title']
                        # topicFields["digest"] = contentJson['description']  # 简介，摘要
                        topicFields["topicCover"] = fields['articlecovers']
                        topicFields["pubTime"] = fields['workerid']  # 时间戳
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
                        topicItem = contentJson['data']['lists']
                        topicArticles = self.getTopicArticles(fields['channelname'], fields['channelID'],
                                                              fields['channelType'], topicFields['title'],
                                                              topicFields["topicID"], topicItem)
                        articleparams = self.getarticleparams(topicArticles.__next__())
                        articlesres = self.getarticlehtml(articleparams.__next__())
                        self.analyzearticle(articlesres.__next__())
                    else:
                        if 'data' in contentJson.keys():
                            fields["appname"] = appname  # 应用名称，字符串
                            # fields["channelname"] = channelname  # 频道名称，字符串
                            # fields["channelID"] = channelid  # 频道id，字符串
                            # fields["channelType"] = channel_type  # 频道type，字符串
                            fields["url"] = contentJson['data']['share']  # 分享的网址，字符串
                            fields["workerid"] = contentJson['data']['contentid']  # 文章id，字符串
                            # fields["title"] = item['title']  # 文章标题，字符串
                            fields["content"] = contentJson['data']['content']  # 文章内容，字符串
                            # fields["articlecovers"] = imgList  # 列表封面，数组
                            fields["images"] = InitClass.get_images(fields["content"])  # 正文图片，数组
                            # fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                            # fields["videocover"] = [item['videoImg']]  # 视频封面，数组
                            # fields["width"] = ''  # 视频宽，字符串
                            # fields["height"] = ''  # 视频高，字符串
                            fields["source"] = contentJson['data']['source']  # 文章来源，字符串
                            fields["pubtime"] = contentJson['data']['published']  # 发布时间，时间戳（毫秒级，13位）
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
                        else:
                            print("内容已下线或待更新：", fields)
                    print(json.dumps(fields, indent=4, ensure_ascii=False))
            except Exception as e:
                num += 1
                logging.info(f"错误数量{num},{e}")

    def getTopicArticles(self, channelname, channelid, channeltype, topicTitle, topicId, topicNewsList):
        articlesparams = []
        for item in topicNewsList:
            try:
                article_fields = InitClass().article_fields()
                article_fields["channelname"] = channelname  # 频道名称，字符串
                article_fields["channelID"] = channelid  # 频道id，字符串
                article_fields["channelType"] = channeltype  # 频道type，字符串
                # article_fields["url"] = item['url']  # 分享的网址，字符串
                if 'contentid' in item.keys():
                    article_fields["workerid"] = item['contentid']  # 文章id，字符串
                article_fields["title"] = item['title']  # 文章标题，字符串
                # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
                imgList = []
                if 'thumb' in item.keys() and item['thumb']:
                    imgList.append(item['thumb'])
                article_fields["articlecovers"] = imgList  # 列表封面，数组
                # article_fields["images"] = ''  # 正文图片，数组
                videoList = []
                if 'video' in item.keys() and item['video']:
                    videoList.append(item['video'])
                article_fields["videos"] = videoList  # 视频地址，数组
                # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
                # article_fields["width"] = ''  # 视频宽，字符串
                # article_fields["height"] = ''  # 视频高，字符串
                if 'source' in item.keys():
                    article_fields["source"] = item['source']  # 文章来源，字符串
                if 'published' in item.keys():
                    article_fields["pubtime"] = item['published']  # 发布时间，时间戳（毫秒级，13位）
                # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                # article_fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                # article_fields["playnum"] = ''  # 播放数，数值
                # article_fields["commentnum"] = item['CommentCount']  # 评论数，数值
                # article_fields["readnum"] = item['ReadCount']  # 阅读数，数值
                # article_fields["trannum"] = ''  # 转发数，数值
                # article_fields["sharenum"] = item['ShareCount']  # 分享数，数值
                # article_fields["author"] = ''  # 作者，字符串
                # article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                article_fields["specialtopic"] = 1  # 是否是专题，数值（0标识不是，1标识是）
                article_fields["topicid"] = topicId  # 专题id，字符串
                article_fields["topicTitle"] = topicTitle  # 专题标题，字符串
                if 'type' in item.keys():
                    article_fields["newsType"] = item['type']  # 自己添加新闻类型
                else:
                    article_fields["newsType"] = channeltype  # 自己添加新闻类型
                if 'url' in item.keys():
                    article_fields["detailUrl"] = item['url']  # 自己添加新闻类型
                else:
                    article_fields["detailUrl"] = ""  # 自己添加新闻类型
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
    appspider = CaiJingWang("财经网")
    appspider.run()
