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
        # article_fields["url"] = url  # 分享的网址，字符串
        if 4 == item['articleType']:  # 专题
            article_fields["workerid"] = item['linkID']  # 文章id，字符串
        else:
            article_fields["workerid"] = item['fileID']  # 文章id，字符串
        # article_fields["workerid"] = item['fileID']  # 文章id，字符串
        article_fields["title"] = item['title']  # 文章标题，字符串
        # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
        imgList = []
        if "pic1" in item.keys() and len(item['pic1']):
            imgList.append(item['pic1'])
        if "pic2" in item.keys() and len(item['pic2']):
            imgList.append(item['pic2'])
        if "pic3" in item.keys() and len(item['pic3']):
            imgList.append(item['pic3'])
        article_fields["articlecovers"] = imgList  # 列表封面，数组
        # article_fields["images"] = ''  # 正文图片，数组
        # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
        # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
        # article_fields["width"] = ''  # 视频宽，字符串
        # article_fields["height"] = ''  # 视频高，字符串
        article_fields["source"] = item['source']  # 文章来源，字符串
        article_fields["pubtime"] = InitClass().date_time_stamp(item['publishTime'])  # 发布时间，时间戳（毫秒级，13位）
        # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
        # article_fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
        article_fields["likenum"] = item['countPraise']  # 点赞数（喜欢数），数值
        # article_fields["playnum"] = ''  # 播放数，数值
        # article_fields["commentnum"] = item['commentNum']  # 评论数，数值
        article_fields["readnum"] = item['countClick']  # 阅读数，数值
        # article_fields["trannum"] = ''  # 转发数，数值
        article_fields["sharenum"] = item['countShare']  # 分享数，数值
        article_fields["author"] = item['createUser']  # 作者，字符串
        if item['columnID'] in bannerCountDir.keys():
            bannerCount = bannerCountDir[item['columnID']]
            if bannerCount > 0:
                article_fields["banner"] = 1
                bannerCountDir[item['columnID']] = bannerCount - 1
                print(bannerCountDir)
            else:
                article_fields["banner"] = 0
        else:
            article_fields["banner"] = 0
        # article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
        # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
        # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
        # article_fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
        article_fields["newsType"] = item['articleType']  # 自己添加新闻类型
    except Exception as e:
        print(e)
    return article_fields


class XinJiangRiBao(Appspider):

    @staticmethod
    def get_app_params():
        url1 = "http://app.xjdaily.com/webapi/api/getColumns"
        headers = {
            "Host": "app.xjdaily.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.7.0",
        }
        method = "get"
        data = {
            "sid": "1",
            "cid": "10",
        }
        app_params1 = InitClass().app_params(url1, headers, method, data=data)

        yield [app_params1]

    def analyze_channel(self, channelsres):
        print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            if "http://app.xjdaily.com/webapi/api/getColumns" == k:
                channelList = json.loads(v)
                for channel in channelList['columns']:
                    channelid = channel['columnID']
                    channelname = channel['columnName']
                    topCount = channel['topCount']
                    bannerCountDir[channelid] = topCount
                    channelparam = InitClass().channel_fields(channelid, channelname)
                    channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "http://app.xjdaily.com/webapi/api/getArticles"
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Host": "app.xjdaily.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.7.0",
        }
        method = "get"
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            data = {
                "sid": "1",
                "cid": channelid,
                "lastFileId": "0",
                "rowNumber": "0",
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
            channelid = article_field.get('channelID')
            workerid = article_field.get('workerid')
            newsType = article_field.get('newsType')
            if 4 == newsType:  # 专题
                url = "http://app.xjdaily.com/webapi/api/getColumns"
                headers = {
                    "Host": "app.xjdaily.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.7.0",
                }
                method = "get"
                data = {
                    "sid": "1",
                    "cid": workerid,
                    "order": "desc",
                }
                articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            else:
                url = "http://app.xjdaily.com/webapi/api/getArticle"
                headers = {
                    "Host": "app.xjdaily.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.7.0",
                }
                method = "get"
                data = {
                    "sid": "1",
                    "aid": workerid,
                    "cid": channelid,
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
                if article.get("articleres"):
                    contentJson = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                    if 'column' in contentJson.keys() and 'columns' in contentJson.keys():
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
                        topicItem = []
                        headers = {
                            "Host": "app.xjdaily.com",
                            "Connection": "Keep-Alive",
                            "Accept-Encoding": "gzip",
                            "User-Agent": "okhttp/3.7.0",
                        }
                        if len(contentJson['columns']) == 1:
                            cid = contentJson['columns'][0]['columnID']
                            type = contentJson['columns'][0]['channelType']
                            topicFields["topicID"] = cid
                            url = f'http://app.xjdaily.com/webapi/api/getArticles?sid=1&cid={cid}&lastFileID=0&rowNumber=0'
                            res_temp = requests.get(url, headers=headers).content.decode()
                            res_info_temp = json.loads(
                                json.dumps(json.loads(res_temp, strict=False), indent=4, ensure_ascii=False))
                            topicItem += res_info_temp['list']
                        else:
                            cid = contentJson['column']['columnID']
                            type = contentJson['column']['channelType']
                            topicFields["topicID"] = cid
                            url = f'http://app.xjdaily.com/webapi/api/getSubColumns?&cid={cid}&type={type}&order=desc'
                            res_temp = requests.get(url, headers=headers).content.decode()
                            res_info_temp = json.loads(
                                json.dumps(json.loads(res_temp, strict=False), indent=4, ensure_ascii=False))
                            for item in res_info_temp['list']:
                                # for item_child in item ['list']:
                                topicItem += item['list']
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
                        content = contentJson['content']
                        if 'images' in contentJson.keys():
                            for img in contentJson['images']:
                                temp = f"<img src=\"{img['imgUrl']}\" />"
                                content = content.replace(img['placeholder'], temp)
                        # if 'videos' in contentJson.keys():
                        #     for video in contentJson['videos']:
                        #         temp = f"<video src=\"{video['url']}\" controls=\"controls\">您的浏览器不支持 video 标签。</video>"
                        #         content = content.replace(video['ref'], temp)
                        fields["content"] = content  # 文章内容，字符串
                        # fields["articlecovers"] = imgList  # 列表封面，数组
                        fields["images"] = InitClass.get_images(fields["content"])  # 正文图片，数组
                        # fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                        # fields["videocover"] = [item['videoImg']]  # 视频封面，数组
                        # fields["width"] = ''  # 视频宽，字符串
                        # fields["height"] = ''  # 视频高，字符串
                        fields["source"] = contentJson['source']  # 文章来源，字符串
                        # fields["pubtime"] = contentJson['ptime']  # 发布时间，时间戳（毫秒级，13位）
                        # fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                        # fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                        # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                        # fields["playnum"] = ''  # 播放数，数值
                        # fields["commentnum"] = item['commentNum']  # 评论数，数值
                        # fields["readnum"] = contentJson['views']  # 阅读数，数值
                        # fields["trannum"] = ''  # 转发数，数值
                        # fields["sharenum"] = ''  # 分享数，数值
                        fields["author"] = contentJson['author']  # 作者，字符串
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
                # article_fields["url"] = url  # 分享的网址，字符串
                if 4 == item['articleType']:  # 专题
                    article_fields["workerid"] = item['linkID']  # 文章id，字符串
                else:
                    article_fields["workerid"] = item['fileID']  # 文章id，字符串
                # article_fields["workerid"] = item['fileID']  # 文章id，字符串
                article_fields["title"] = item['title']  # 文章标题，字符串
                # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
                imgList = []
                if "pic1" in item.keys() and len(item['pic1']):
                    imgList.append(item['pic1'])
                if "pic2" in item.keys() and len(item['pic2']):
                    imgList.append(item['pic2'])
                if "pic3" in item.keys() and len(item['pic3']):
                    imgList.append(item['pic3'])
                article_fields["articlecovers"] = imgList  # 列表封面，数组
                # article_fields["images"] = ''  # 正文图片，数组
                # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
                # article_fields["width"] = ''  # 视频宽，字符串
                # article_fields["height"] = ''  # 视频高，字符串
                article_fields["source"] = item['source']  # 文章来源，字符串
                article_fields["pubtime"] = InitClass().date_time_stamp(item['publishTime'])  # 发布时间，时间戳（毫秒级，13位）
                # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                # article_fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                article_fields["likenum"] = item['countPraise']  # 点赞数（喜欢数），数值
                # article_fields["playnum"] = ''  # 播放数，数值
                # article_fields["commentnum"] = item['commentNum']  # 评论数，数值
                article_fields["readnum"] = item['countClick']  # 阅读数，数值
                # article_fields["trannum"] = ''  # 转发数，数值
                article_fields["sharenum"] = item['countShare']  # 分享数，数值
                article_fields["author"] = item['createUser']  # 作者，字符串
                article_fields["banner"] = 0  # banner标记，数值（0标识不是，1标识是）
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
    appspider = XinJiangRiBao("新疆日报")
    appspider.run()
