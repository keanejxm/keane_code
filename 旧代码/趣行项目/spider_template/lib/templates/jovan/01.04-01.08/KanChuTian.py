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
        # article_fields["channelType"] = channel_type  # 频道type，字符串
        url = ""
        if 'specialid=' in item['commentsUrl']:
            temp = item['commentsUrl'].split('specialid=')
            url = "http://www3.ctdsb.net/index.php?m=app&c=index&a=get_special_news&specialid=" + temp[len(temp) - 1]
        else:
            url = item['url']
        article_fields["url"] = url  # 分享的网址，字符串
        article_fields["workerid"] = item['documentId']  # 文章id，字符串
        article_fields["title"] = item['title']  # 文章标题，字符串
        # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
        imgList = []
        if item['thumbnail']:
            imgList.append(item['thumbnail'])
        article_fields["articlecovers"] = imgList  # 列表封面，数组
        # article_fields["images"] = ''  # 正文图片，数组
        if 'videoUrl' in item.keys() and item['videoUrl']:
            article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
        if 'videoPoster' in item.keys() and item['videoPoster']:
            article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
        # article_fields["width"] = ''  # 视频宽，字符串
        # article_fields["height"] = ''  # 视频高，字符串
        # article_fields["source"] = ''  # 文章来源，字符串
        # article_fields["pubtime"] = ''  # 发布时间，时间戳（毫秒级，13位）
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


class JiuPaiXinWen(Appspider):

    @staticmethod
    def get_app_params():
        url1 = "http://www3.ctdsb.net/index.php?m=app&c=fuli&a=get_categorys"
        headers = {
            "Host": "www3.ctdsb.net",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/2.5.0",
        }
        method = "get"

        app_params1 = InitClass().app_params(url1, headers, method)

        yield [app_params1]

    def analyze_channel(self, channelsres):
        print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            if "http://www3.ctdsb.net/index.php?m=app&c=fuli&a=get_categorys" == k:
                channelList = json.loads(v)
                for channel in channelList:
                    channelid = channel['catid']
                    channelname = channel['catname']
                    channelType = channel['api']
                    channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channelType)
                    channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = ""
        headers = {
            "Host": "www3.ctdsb.net",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/2.5.0",
        }
        method = "get"
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channelType = channel.get("channeltype")
            url = channelType
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
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
                    if isinstance(articleslists, list):
                        for item in articleslists:
                            if "list" in item['type']:
                                for itemList in item['item']:
                                    article_fields = setListNewsParam(channelname, channelid, 0, itemList)
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                            elif "focus" in item['type']:  # banner
                                for itemFocus in item['item']:
                                    article_fields = setListNewsParam(channelname, channelid, 1, itemFocus)
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                            elif "word" in item['type']:
                                for itemWord in item['content']:
                                    article_fields = setListNewsParam(channelname, channelid, 0, itemWord)
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                            elif "spic" in item['type']:
                                for itemSpic in item['content']:
                                    article_fields = setListNewsParam(channelname, channelid, 0, itemSpic)
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                            elif "bpic" in item['type']:
                                for itemBpic in item['content']:
                                    article_fields = setListNewsParam(channelname, channelid, 0, itemBpic)
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                            else:
                                print(articleslists)
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
            url = article_field.get('url')
            # newsType = article_field.get('newsType')
            # if "ct" == newsType:
            #     continue
            headers = {
                "Host": "www3.ctdsb.net",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/2.5.0",
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

                    if 'msg' in contentJson.keys() and 'success' in contentJson.keys() and 'data' in contentJson.keys():
                        if 'sphead' in contentJson['data'].keys() and 'listdata' in contentJson['data'].keys():
                            topicFields = InitClass().topic_fields()
                            topicFields["topicID"] = contentJson['data']['sphead'][0]['id']  # 专题id，app内唯一标识
                            topicFields["platformName"] = appname  # 平台名字（app名字）
                            # topicFields["platformID"] = fields['workerid']
                            topicFields["channelName"] = fields['channelname']  # 频道名字
                            topicFields["channelID"] = fields['channelID']  # 频道id
                            topicFields["topicUrl"] = contentJson['data']['sphead'][0]['shareUrl']  # topicUrl
                            topicFields["title"] = contentJson['data']['sphead'][0]['title']
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
                            topicItem = []
                            for topicCate in contentJson['data']['listdata']:
                                topicItem += topicCate['item']
                            topicArticles = self.getTopicArticles(fields['channelname'], fields['channelID'],
                                                                  topicFields['title'],
                                                                  topicFields["topicID"], topicItem)
                            articleparams = self.getarticleparams(topicArticles.__next__())
                            articlesres = self.getarticlehtml(articleparams.__next__())
                            self.analyzearticle(articlesres.__next__())
                        else:
                            print(contentJson)
                    else:
                        fields["appname"] = appname  # 应用名称，字符串
                        # fields["channelname"] = channelname  # 频道名称，字符串
                        # fields["channelID"] = channelid  # 频道id，字符串
                        # fields["channelType"] = channel_type  # 频道type，字符串
                        fields["url"] = contentJson['source_url']  # 分享的网址，字符串
                        # fields["workerid"] = item['ctId']  # 文章id，字符串
                        # fields["title"] = item['title']  # 文章标题，字符串
                        fields["content"] = contentJson['body']  # 文章内容，字符串
                        # fields["articlecovers"] = imgList  # 列表封面，数组
                        fields["images"] = InitClass.get_images(fields["content"])  # 正文图片，数组
                        # fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                        # fields["videocover"] = [item['videoImg']]  # 视频封面，数组
                        # fields["width"] = ''  # 视频宽，字符串
                        # fields["height"] = ''  # 视频高，字符串
                        fields["source"] = contentJson['source']  # 文章来源，字符串
                        fields["pubtime"] = contentJson['ptime']  # 发布时间，时间戳（毫秒级，13位）
                        # fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                        # fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                        # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                        # fields["playnum"] = ''  # 播放数，数值
                        # fields["commentnum"] = item['commentNum']  # 评论数，数值
                        fields["readnum"] = contentJson['views']  # 阅读数，数值
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

    def getTopicArticles(self, channelname, channelid, topicTitle, topicId, topicNewsList):
        articlesparams = []
        for item in topicNewsList:
            try:
                article_fields = InitClass().article_fields()
                article_fields["channelname"] = channelname  # 频道名称，字符串
                article_fields["channelID"] = channelid  # 频道id，字符串
                # article_fields["channelType"] = channel_type  # 频道type，字符串
                article_fields[
                    "url"] = f"http://www3.ctdsb.net/index.php?m=app&c=index&a=get_news&type=doc&aid={item['id']}"  # 分享的网址，字符串
                article_fields["workerid"] = item['id']  # 文章id，字符串
                article_fields["title"] = item['title']  # 文章标题，字符串
                # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
                imgList = []
                if item['thumb']:
                    imgList.append(item['thumb'])
                article_fields["articlecovers"] = imgList  # 列表封面，数组
                # article_fields["images"] = ''  # 正文图片，数组
                if 'videoUrl' in item.keys() and item['videoUrl']:
                    article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                if 'videoPoster' in item.keys() and item['videoPoster']:
                    article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
                # article_fields["width"] = ''  # 视频宽，字符串
                # article_fields["height"] = ''  # 视频高，字符串
                # article_fields["source"] = ''  # 文章来源，字符串
                # article_fields["pubtime"] = ''  # 发布时间，时间戳（毫秒级，13位）
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
                article_fields["specialtopic"] = 1  # 是否是专题，数值（0标识不是，1标识是）
                article_fields["topicid"] = topicId  # 专题id，字符串
                article_fields["topicTitle"] = topicTitle  # 专题标题，字符串
                # article_fields["newsType"] = item['type']  # 自己添加新闻类型
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
    appspider = JiuPaiXinWen("看楚天")
    appspider.run()
