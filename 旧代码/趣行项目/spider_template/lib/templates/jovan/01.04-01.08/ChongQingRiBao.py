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
        article_fields["url"] = item['targetUrl']  # 分享的网址，字符串
        article_fields["workerid"] = item['id']  # 文章id，字符串
        article_fields["title"] = item['title']  # 文章标题，字符串
        # # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
        # imgList = []
        # if item['thumbnail']:
        #     imgList.append(item['thumbnail'])
        article_fields["articlecovers"] = item['imageUrl']  # 列表封面，数组
        # # article_fields["images"] = ''  # 正文图片，数组
        if 'videoUrl' in item.keys() and item['videoUrl']:
            article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
        # if 'videoPoster' in item.keys() and item['videoPoster']:
        #     article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
        # article_fields["width"] = ''  # 视频宽，字符串
        # article_fields["height"] = ''  # 视频高，字符串
        article_fields["source"] = item['sourceName']  # 文章来源，字符串
        article_fields["pubtime"] = InitClass().date_time_stamp(item['publishTime'])  # 发布时间，时间戳（毫秒级，13位）
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
        article_fields["classId"] = item['classId']  # 自己添加新闻类型
        article_fields["dataType"] = item['dataType']  # 自己添加新闻类型
    except Exception as e:
        print(e)
    return article_fields


class ChongQingRiBao(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://api.cqrb.cn/api/column/getList"
        headers = {
            "Authorization": "",
            "udId": "a7ff38fce50fc9d8",
            "appKey": "d8def12b988c9e6b02306c4f33091f28",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; LIO-AL00 Build/HUAWEILIO-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36CQDAILY_UIWebViewCQDAILY_EPAPER",
            "AppVersion": "2.2.1",
            "AppVersionCode": "13",
            "ClientOS": "Android",
            "OSVersion": "LIO-AL00 10",
            "Host": "api.cqrb.cn",
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
            if "https://api.cqrb.cn/api/column/getList" == k:
                channelList = json.loads(v)
                for channel in channelList['data']:
                    channelid = channel['classid']
                    channelname = channel['classname']
                    channelparam = InitClass().channel_fields(channelid, channelname)
                    channelparams.append(channelparam)
                    if 'sub' in channel.keys():
                        for channel_child in channel['sub']:
                            channelid = channel_child['classid']
                            channelname = channel_child['classname']
                            channelparam = InitClass().channel_fields(channelid, channelname)
                            channelparams.append(channelparam)

        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = ""
        headers = {
            "Accept": "application/prs.shangyouapi.v2+json",
            "Authorization": "",
            "udId": "a7ff38fce50fc9d8",
            "appKey": "d8def12b988c9e6b02306c4f33091f28",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; LIO-AL00 Build/HUAWEILIO-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36CQDAILY_UIWebViewCQDAILY_EPAPER",
            "AppVersion": "2.2.1",
            "AppVersionCode": "13",
            "ClientOS": "Android",
            "OSVersion": "LIO-AL00 10",
            "Host": "api.cqrb.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        method = "get"
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            url = f' https://api.cqrb.cn/api/news/getListByColumnId?classId={channelid}&page=1'
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid=channelid)
            articlelistsparams.append(articlelist_param)
        yield articlelistsparams

    def analyze_articlelists(self, articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    print(articleslists)
                    if "data" in articleslists.keys():
                        if 'newslist' in articleslists['data'].keys():
                            for item_news in articleslists['data']['newslist']:
                                if 'showType' in item_news.keys():
                                    if 1 == item_news['showType']:
                                        for item_banner in item_news['list']:
                                            article_fields = setListNewsParam(channelname, channelid, 1, item_banner)
                                            articleparam = InitClass().article_list_fields()
                                            articleparam["articelField"] = article_fields
                                            articlesparams.append(articleparam)
                                    elif 5 == item_news['showType']:
                                        channelcityparams = []
                                        for item_city in item_news['cityList']:
                                            channelid = item_city['classid']
                                            channelname = item_city['classname']
                                            channelparam = InitClass().channel_fields(channelid, channelname)
                                            channelcityparams.append(channelparam)
                                        articlecitylistparames = self.getarticlelistparams(
                                            channelcityparams).__next__()
                                        articlescitylistsres = self.getarticlelists(articlecitylistparames).__next__()
                                        articlescity = self.analyze_articlelists(articlescitylistsres).__next__()
                                        articlesparams += articlescity
                                    else:
                                        article_fields = setListNewsParam(channelname, channelid, 0, item_news['data'])
                                        articleparam = InitClass().article_list_fields()
                                        articleparam["articelField"] = article_fields
                                        articlesparams.append(articleparam)
                                else:
                                    print("未找到showType属性", item_news)
                        else:
                            print("未找到newslist属性", articleslists['data'])
                    else:
                        print("未找到data属性", articleslists)
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
            classId = article_field.get('classId')
            dataType = article_field.get('dataType')
            if 5 == dataType:  # 专题
                url = f"https://api.cqrb.cn/api/topic/getListByCategory?classId={classId}&page=1"
                headers = {
                    "Authorization": "",
                    "udId": "a7ff38fce50fc9d8",
                    "appKey": "d8def12b988c9e6b02306c4f33091f28",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10; LIO-AL00 Build/HUAWEILIO-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36CQDAILY_UIWebViewCQDAILY_EPAPER",
                    "AppVersion": "2.2.1",
                    "AppVersionCode": "13",
                    "ClientOS": "Android",
                    "OSVersion": "LIO-AL00 10",
                    "Host": "api.cqrb.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                method = "get"
                articleparam = InitClass().article_params_fields(url, headers, method, article_field=article_field)
                articleparams.append(articleparam)
            else:
                url = f"https://api.cqrb.cn/api/news/getDetails?classId={classId}&newsId={workerid}"
                headers = {
                    "Authorization": "",
                    "udId": "a7ff38fce50fc9d8",
                    "appKey": "d8def12b988c9e6b02306c4f33091f28",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10; LIO-AL00 Build/HUAWEILIO-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36CQDAILY_UIWebViewCQDAILY_EPAPER",
                    "AppVersion": "2.2.1",
                    "AppVersionCode": "13",
                    "ClientOS": "Android",
                    "OSVersion": "LIO-AL00 10",
                    "Host": "api.cqrb.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
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
                    if 'data' in contentJson.keys() and isinstance(contentJson['data'], dict):
                        if 5 == fields.get('dataType'):  # 专题
                            topicFields = InitClass().topic_fields()
                            topicFields["topicID"] = fields['classId']  # 专题id，app内唯一标识
                            topicFields["platformName"] = appname  # 平台名字（app名字）
                            # topicFields["platformID"] = fields['workerid']
                            topicFields["channelName"] = fields['channelname']  # 频道名字
                            topicFields["channelID"] = fields['channelID']  # 频道id
                            topicFields["topicUrl"] = fields['url']  # topicUrl
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
                            topicItem = contentJson['data']['newslist']
                            topicArticles = self.getTopicArticles(fields['channelname'], fields['channelID'],
                                                                  topicFields['title'],
                                                                  topicFields["topicID"], topicItem)
                            articleparams = self.getarticleparams(topicArticles.__next__())
                            articlesres = self.getarticlehtml(articleparams.__next__())
                            self.analyzearticle(articlesres.__next__())
                        else:
                            fields["appname"] = appname  # 应用名称，字符串
                            # fields["channelname"] = channelname  # 频道名称，字符串
                            # fields["channelID"] = channelid  # 频道id，字符串
                            # fields["channelType"] = channel_type  # 频道type，字符串
                            # fields["url"] = contentJson['source_url']  # 分享的网址，字符串
                            # fields["workerid"] = item['ctId']  # 文章id，字符串
                            # fields["title"] = item['title']  # 文章标题，字符串
                            fields["content"] = contentJson['data']['contents']  # 文章内容，字符串
                            # fields["articlecovers"] = imgList  # 列表封面，数组
                            fields["images"] = InitClass.get_images(fields["content"])  # 正文图片，数组
                            # fields["videos"] = [item['videoUrl']]  # 视频地址，数组
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
                    else:
                        print("未获取到详情", fields)
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
                article_fields["url"] = item['targetUrl']  # 分享的网址，字符串
                article_fields["workerid"] = item['id']  # 文章id，字符串
                article_fields["title"] = item['title']  # 文章标题，字符串
                # # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
                # imgList = []
                # if item['thumbnail']:
                #     imgList.append(item['thumbnail'])
                article_fields["articlecovers"] = item['imageUrl']  # 列表封面，数组
                # # article_fields["images"] = ''  # 正文图片，数组
                if 'videoUrl' in item.keys() and item['videoUrl']:
                    article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                # if 'videoPoster' in item.keys() and item['videoPoster']:
                #     article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
                # article_fields["width"] = ''  # 视频宽，字符串
                # article_fields["height"] = ''  # 视频高，字符串
                article_fields["source"] = item['sourceName']  # 文章来源，字符串
                article_fields["pubtime"] = InitClass().date_time_stamp(item['publishTime'])  # 发布时间，时间戳（毫秒级，13位）
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
                article_fields["classId"] = item['classId']  # 自己添加新闻类型
                article_fields["dataType"] = item['dataType']  # 自己添加新闻类型
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
    appspider = ChongQingRiBao("重庆日报")
    appspider.run()
