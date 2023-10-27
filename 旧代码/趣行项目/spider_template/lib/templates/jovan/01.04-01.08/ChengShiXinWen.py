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
        article_fields["url"] = item['Url']  # 分享的网址，字符串
        article_fields["workerid"] = item['Id']  # 文章id，字符串
        article_fields["title"] = item['Title']  # 文章标题，字符串
        # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
        imgList = []
        if item['ImgSrc']:
            imgList.append(f"http://cmsuiv3.chengnews.net{item['ImgSrc']}")
        article_fields["articlecovers"] = imgList  # 列表封面，数组
        # article_fields["images"] = ''  # 正文图片，数组
        # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
        # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
        # article_fields["width"] = ''  # 视频宽，字符串
        # article_fields["height"] = ''  # 视频高，字符串
        article_fields["source"] = item['SourceUrl']  # 文章来源，字符串
        article_fields["pubtime"] = InitClass().date_time_stamp(item['PostDateTime'])  # 发布时间，时间戳（毫秒级，13位）
        # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
        # article_fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
        # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
        # article_fields["playnum"] = ''  # 播放数，数值
        article_fields["commentnum"] = item['CommentCount']  # 评论数，数值
        article_fields["readnum"] = item['ReadCount']  # 阅读数，数值
        # article_fields["trannum"] = ''  # 转发数，数值
        article_fields["sharenum"] = item['ShareCount']  # 分享数，数值
        # article_fields["author"] = ''  # 作者，字符串
        article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
        # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
        # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
        # article_fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
        article_fields["newsType"] = item['Type']  # 自己添加新闻类型
    except Exception as e:
        print(e)
    return article_fields


class ChengShiXinWen(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://cmswebv3.chengnews.net/api/Article/Classify"
        headers = {
            "Host": "cmswebv3.chengnews.net",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.11.0",
            "timestamp": "1609729361146",
            "newspaperid": "6666",
            "nonce": "b476ae81-6a27-45d7-829a-10ea3f1dff17",
            "signature": "83EACA8436A680E030A1974C25D6351C",
        }
        method = "get"
        data = {
            "Pidx": "-1",
            "TypeId": "4",
            "Token": "",
            "Nid": "6666",
        }
        app_params1 = InitClass().app_params(url, headers, method, data=data)

        yield [app_params1]

    def analyze_channel(self, channelsres):
        print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            if "http://cmswebv3.chengnews.net/api/Article/Classify" == k:
                channelList = json.loads(v)
                for channel in channelList:
                    channelid = channel['Id']
                    channelname = channel['Name']
                    channelType = channel['Type']
                    channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channelType)
                    channelparams.append(channelparam)
        channelparam = InitClass().channel_fields(40469, "视频", channeltype=4)
        channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "http://cmswebv3.chengnews.net/api/Article/ListYanBian"
        headers = {
            "Host": "cmswebv3.chengnews.net",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.11.0",
            "timestamp": "1609729492636",
            "newspaperid": "6666",
            "nonce": "dcb3e604-2812-4615-ad5e-ea2cca19de84",
            "signature": "D237C7103E2BCB815E47D66356CE4974",
        }
        method = "get"
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channelType = channel.get("channeltype")
            data = {
                "Type": "0",
                "t": "0",
                "ClassifyIdx": channelid,
                "PageIndex": "1",
                "ClassifyType": channelType,
                "NewspaperIdx": "6666",
                "FirstSumCount": "0",
                "IsFound": "0",
                "PageSize": "15",
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
                    if 'TopArticle' in articleslists.keys():  # banner
                        for item_top in articleslists['TopArticle']:
                            article_fields = setListNewsParam(channelname, channelid, 1, item_top)
                            articleparam = InitClass().article_list_fields()
                            articleparam["articelField"] = article_fields
                            articlesparams.append(articleparam)
                    if 'ArticleList' in articleslists.keys():
                        for item_article in articleslists['ArticleList']:
                            article_fields = setListNewsParam(channelname, channelid, 0, item_article)
                            articleparam = InitClass().article_list_fields()
                            articleparam["articelField"] = article_fields
                            articlesparams.append(articleparam)
                    if 'HeadArticle' in articleslists.keys():
                        for item_head in articleslists['HeadArticle']:
                            article_fields = setListNewsParam(channelname, channelid, 0, item_head)
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
            if 7 == newsType:
                url = f"http://cmswebv3.chengnews.net/api/Article/SubjectList?PageIndex=1&SubjectId={article_field['workerid']}&NewspaperIdx=6666&PageSize=15"
                headers = {
                    "Host": "cmswebv3.chengnews.net",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.11.0",
                    "timestamp": "1609742051747",
                    "newspaperid": "6666",
                    "nonce": "0c146293-68e1-4f13-af65-5e650438ad95",
                    "signature": "F84853FE3BF043EE6BD5FD8EDBDC31E5",
                }
                method = "get"
                articleparam = InitClass().article_params_fields(url, headers, method, article_field=article_field)
                articleparams.append(articleparam)
            else:
                url = f"http://cmswebv3.chengnews.net/api/Article/GetArticle/?NewsPaperGroupIdx=6666&Id={article_field['workerid']}&Token="
                headers = {
                    "Host": "cmswebv3.chengnews.net",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.11.0",
                    "timestamp": "1609739904278",
                    "newspaperid": "6666",
                    "nonce": "6771cdec-e153-471b-bd7f-e923ed073120",
                    "signature": "1BB5413DFB8BF4F8EF59013AF0CDDACE",
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
            newsType = fields.get('newsType')

            try:
                if article.get("articleres"):
                    contentJson = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                    # print(contentJson)
                    if 7 == newsType:
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
                        topicItem = contentJson['ArticleList']
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
                        fields["content"] = contentJson['Detail']  # 文章内容，字符串
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
                article_fields["url"] = item['Url']  # 分享的网址，字符串
                article_fields["workerid"] = item['Id']  # 文章id，字符串
                article_fields["title"] = item['Title']  # 文章标题，字符串
                # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
                imgList = []
                if item['ImgSrc']:
                    imgList.append(f"http://cmsuiv3.chengnews.net{item['ImgSrc']}")
                article_fields["articlecovers"] = imgList  # 列表封面，数组
                # article_fields["images"] = ''  # 正文图片，数组
                # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
                # article_fields["width"] = ''  # 视频宽，字符串
                # article_fields["height"] = ''  # 视频高，字符串
                article_fields["source"] = item['SourceUrl']  # 文章来源，字符串
                article_fields["pubtime"] = InitClass().date_time_stamp(item['PostDateTime'])  # 发布时间，时间戳（毫秒级，13位）
                # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                # article_fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                # article_fields["playnum"] = ''  # 播放数，数值
                article_fields["commentnum"] = item['CommentCount']  # 评论数，数值
                article_fields["readnum"] = item['ReadCount']  # 阅读数，数值
                # article_fields["trannum"] = ''  # 转发数，数值
                article_fields["sharenum"] = item['ShareCount']  # 分享数，数值
                # article_fields["author"] = ''  # 作者，字符串
                # article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                article_fields["specialtopic"] = 1  # 是否是专题，数值（0标识不是，1标识是）
                article_fields["topicid"] = topicId  # 专题id，字符串
                article_fields["topicTitle"] = topicTitle  # 专题标题，字符串
                article_fields["newsType"] = item['Type']  # 自己添加新闻类型
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
    appspider = ChengShiXinWen("橙视新闻")
    appspider.run()
