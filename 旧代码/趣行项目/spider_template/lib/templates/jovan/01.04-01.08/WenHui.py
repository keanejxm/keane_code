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
        article_fields["url"] = item['shareUrl']  # 分享的网址，字符串
        if 3084 == channelid or 3083 == channelid:  # 专题 # 活动
            article_fields["workerid"] = item['channelId']  # 文章id，字符串
            article_fields["title"] = item['channelName']  # 文章标题，字符串
            # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
            imgList = []
            if item['imgUrl']:
                imgList.append(item['imgUrl'])
            article_fields["articlecovers"] = imgList  # 列表封面，数组
            # article_fields["images"] = ''  # 正文图片，数组
            # article_fields["videos"] = [item['rtmpPath']]  # 视频地址，数组
            # if 'videoPoster' in item.keys() and item['videoPoster']:
            #     article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
            # article_fields["width"] = ''  # 视频宽，字符串
            # article_fields["height"] = ''  # 视频高，字符串
            # article_fields["source"] = ''  # 文章来源，字符串
            # article_fields["pubtime"] = InitClass().date_time_stamp(item['publishTime'])  # 发布时间，时间戳（毫秒级，13位）
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
            article_fields["contentViewType"] = ""  # 自己添加新闻类型
            article_fields["contentUrl"] = ""  # 自己添加新闻类型
        else:
            article_fields["workerid"] = item['contentId']  # 文章id，字符串
            article_fields["title"] = item['title']  # 文章标题，字符串
            # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
            imgList = []
            if item['imageUrl']:
                imgList.append(item['imageUrl'])
            article_fields["articlecovers"] = imgList  # 列表封面，数组
            # article_fields["images"] = ''  # 正文图片，数组
            if 'rtmpPath' in item.keys() and item['rtmpPath']:
                article_fields["videos"] = [item['rtmpPath']]  # 视频地址，数组
            # if 'videoPoster' in item.keys() and item['videoPoster']:
            #     article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
            # article_fields["width"] = ''  # 视频宽，字符串
            # article_fields["height"] = ''  # 视频高，字符串
            # article_fields["source"] = ''  # 文章来源，字符串
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
            article_fields["contentViewType"] = item['contentViewType']  # 自己添加新闻类型
            article_fields["contentUrl"] = item['contentUrl']  # 自己添加新闻类型
            if item['contentUrl']:
                pass
            else:
                print(item)
    except Exception as e:
        print(e)
    return article_fields


class WenHui(Appspider):

    @staticmethod
    def get_app_params():
        url1 = "https://wenhui.whb.cn/whbApi/content/getConfigV2.action"
        url2 = "https://wenhui.whb.cn/whbApi/content/getConfigVideo.action"
        headers = {
            "Accept-Encoding": "gzip",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.0.2; Coolpad 8675-A Build/LRX22G)",
            "Host": "wenhui.whb.cn",
            "Connection": "Keep-Alive",
        }
        method = "get"
        data1 = {
            "_dc": "-5994630308504908006",
            "version": "728",
        }
        data2 = {
            "_dc": "3157412965770676964",
            "version": "728",
        }
        app_params1 = InitClass().app_params(url1, headers, method, data=data1)
        app_params2 = InitClass().app_params(url2, headers, method, data=data2)

        yield [app_params1, app_params2]

    def analyze_channel(self, channelsres):
        print(channelsres)
        channelparams = []
        channelparam = InitClass().channel_fields(0, "首页", categoryid=0)
        channelparams.append(channelparam)
        for k, v in channelsres.items():
            if "https://wenhui.whb.cn/whbApi/content/getConfigV2.action" == k:
                channelList = json.loads(v)
                for channel in channelList['channels']:
                    channelid = channel['id']
                    channelname = channel['name']
                    channelparam = InitClass().channel_fields(channelid, channelname, categoryid=0)
                    channelparams.append(channelparam)
            if "https://wenhui.whb.cn/whbApi/content/getConfigVideo.action" == k:
                channelList = json.loads(v)
                for channel in channelList['channels']:
                    channelid = channel['id']
                    channelname = channel['name']
                    channelparam = InitClass().channel_fields(channelid, channelname, categoryid=1)
                    channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "https://wenhui.whb.cn/whbApi/content/findContentsV2.action"
        headers = {
            "Accept-Encoding": "gzip",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.0.2; Coolpad 8675-A Build/LRX22G)",
            "Host": "wenhui.whb.cn",
            "Connection": "Keep-Alive",
        }
        method = "get"
        data = {}
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            categoryid = channel.get("categoryid")
            url = "https://wenhui.whb.cn/whbApi/content/findContentsV2.action"
            if 1 == categoryid:
                if 3120 == channelid:  # 直播
                    url = "https://wenhui.whb.cn/whbApi/content/findLives.action"
                    data = {
                        "videoChannel": "1",
                        "page": "1",
                        # "_dc": "7147879867743356755",
                    }
                else:
                    data = {
                        # "_dc": "7147879867743356755",
                        "channelId": channelid,
                        "page": "1",
                        "videoChannel": "1",
                        "version": "728",
                    }
            else:
                if 0 == channelid:
                    data = {
                        "page": "1",
                        # "_dc": "7147879867743356755",
                        "version": "728",
                    }
                else:
                    if 3084 == channelid:  # 专题
                        url = "https://wenhui.whb.cn/whbApi/content/findColumnPageV2.action"
                        data = {
                            "page": "1",
                            # "_dc": "7147879867743356755",
                            "channelId": channelid,
                        }
                    if 3083 == channelid:  # 活动
                        url = "https://wenhui.whb.cn/whbApi/content/findColumnPageV2.action"
                        data = {
                            "page": "1",
                            # "_dc": "7147879867743356755",
                            "channelId": channelid,
                        }
                    else:
                        data = {
                            "page": "1",
                            # "_dc": "7147879867743356755",
                            "channelId": channelid,
                            "version": "728",
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
                    for item in articleslists['dataList']:
                        banner = 0
                        if 'viewType' in item.keys() and 'list' in item.keys():
                            banner = 1 if item['viewType'] == 1 else 0
                            for itemList in item['list']:
                                article_fields = setListNewsParam(channelname, channelid, banner, itemList)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        else:
                            article_fields = setListNewsParam(channelname, channelid, banner, item)
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
            "Accept-Encoding": "gzip",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.0.2; Coolpad 8675-A Build/LRX22G)",
            "Host": "wenhui.whb.cn",
            "Connection": "Keep-Alive",
        }
        method = "get"
        data = {}
        for article in articles:
            article_field = article.get('articelField')
            channelid = article_field.get('channelID')
            workerid = article_field.get('workerid')
            url = article_field.get('contentUrl')
            # newsType = article_field.get('newsType')
            if 3084 == channelid or 3083 == channelid:  # 专题 # 活动
                url = "https://wenhui.whb.cn/whbApi/content/findContentsV2.action"
                data = {
                    "page": "1",
                    # "_dc": "7147879867743356755",
                    "channelId": workerid,
                    "version": "728",
                }
            if url:
                articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            appname = article.get("appname")
            fields = article.get("articleField")
            channelid = fields.get('channelID')
            try:
                if article.get("articleres"):
                    contentJson = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                    if 3084 == channelid or 3083 == channelid:  # 专题 # 活动
                        topicFields = InitClass().topic_fields()
                        topicFields["topicID"] = fields['workerid']  # 专题id，app内唯一标识
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
                        topicArticles = []
                        for item in contentJson['dataList']:
                            banner = 0
                            if 'viewType' in item.keys() and 'list' in item.keys():
                                for itemList in item['list']:
                                    article_fields = self.getTopicArticles(fields['channelname'], fields['channelID'],
                                                                           topicFields['title'],
                                                                           topicFields["topicID"],
                                                                           itemList)
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    topicArticles.append(articleparam)
                            else:
                                article_fields = self.getTopicArticles(fields['channelname'], fields['channelID'],
                                                                       topicFields['title'],
                                                                       topicFields["topicID"],
                                                                       item)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                topicArticles.append(articleparam)
                        articleparams = self.getarticleparams(topicArticles)
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
                        content = contentJson['html']
                        if 'images' in contentJson.keys():
                            for img in contentJson['images']:
                                temp = f"<img src=\"{img['imageUrl']}\" />"
                                content = content.replace(img['ref'], temp)
                        if 'videos' in contentJson.keys():
                            for video in contentJson['videos']:
                                temp = f"<video src=\"{video['url']}\" controls=\"controls\">您的浏览器不支持 video 标签。</video>"
                                content = content.replace(video['ref'], temp)
                        fields["content"] = content  # 文章内容，字符串
                        # fields["articlecovers"] = imgList  # 列表封面，数组
                        fields["images"] = InitClass.get_images(fields["content"])  # 正文图片，数组
                        fields["videos"] = InitClass.get_video(fields["content"])  # 视频地址，数组
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

    def getTopicArticles(self, channelname, channelid, topicTitle, topicId, item):
        article_fields = InitClass().article_fields()
        article_fields["channelname"] = channelname  # 频道名称，字符串
        article_fields["channelID"] = channelid  # 频道id，字符串
        # article_fields["channelType"] = channel_type  # 频道type，字符串
        article_fields["workerid"] = item['contentId']  # 文章id，字符串
        article_fields["title"] = item['title']  # 文章标题，字符串
        # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
        imgList = []
        if item['imageUrl']:
            imgList.append(item['imageUrl'])
        article_fields["articlecovers"] = imgList  # 列表封面，数组
        # article_fields["images"] = ''  # 正文图片，数组
        if 'rtmpPath' in item.keys() and item['rtmpPath']:
            article_fields["videos"] = [item['rtmpPath']]  # 视频地址，数组
        # if 'videoPoster' in item.keys() and item['videoPoster']:
        #     article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
        # article_fields["width"] = ''  # 视频宽，字符串
        # article_fields["height"] = ''  # 视频高，字符串
        # article_fields["source"] = ''  # 文章来源，字符串
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
        article_fields["contentViewType"] = item['contentViewType']  # 自己添加新闻类型
        article_fields["contentUrl"] = item['contentUrl']  # 自己添加新闻类型
        if item['contentUrl']:
            pass
        else:
            print(item)
        return article_fields

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
    appspider = WenHui("文汇")
    appspider.run()
