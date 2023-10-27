# -*- encoding:utf-8 -*-
"""
@功能:秦闻解析模板
@AUTHOR：Keane
@文件名：ZhongGuoLan.py
@时间：2020/12/17  17:33
"""

import json
import logging

from appspider_m import Appspider
from initclass import InitClass


class QinWenNews(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://qinwen.sanqin.com/app_if/getColumns?siteId=2&parentColumnId=5539&version=0&columnType=-1"
        headers = {
            "Host": "qinwen.sanqin.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.0"
        }
        data = {}
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(channelsres)
        channelparams = []
        nav_list = [{
            "channelid": "6677",
            "channelname": "视频"
        }]
        for channel in channelslists['columns']:
            channelid = channel['columnId']
            channelname = channel['columnName']
            if channelname !='专题':
                channelparam = InitClass().channel_fields(channelid, channelname)
                channelparams.append(channelparam)
        channelparams = channelparams + nav_list
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        print(channelsparams)
        articlelistsparams = []
        headers = {
            "Host": "qinwen.sanqin.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.0"
        }
        url = "https://qinwen.sanqin.com/app_if/getArticles"
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")
            data = {
                "columnId": channelid,
                "version": "0",
                "lastFileId": "0",
                "page": "0",
                "adv": "1",
                "appID": "1",
                "columnStyle": "101",
            }
            method = 'get'
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid = channelid, data = data,
                                                                       channeltype = channeltype)
            articlelistsparams.append(articlelist_param)
        yield articlelistsparams

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            channel_type = articleslistres.get("channeltype")
            try:
                articleslists = json.loads(articleslists)
                print(articleslists)
                try:
                    for articles in articleslists["list"]:
                        article_type = articles["articleType"]
                        if article_type == 3:
                            # 这种类型为专题
                            print(articles)
                            topic_fields = InitClass().topic_fields()
                            articleparam = InitClass().article_list_fields()
                            # 获取文章列表内的有用信息
                            article_id = articles["subColumnID"]
                            article_title = articles["title"]
                            article_type = articles["articleType"]
                            share_url = articles['shareUrl']
                            pubtime = articles["publishtime"]
                            topic = 1
                            topic_fields["channelName"] = channelname
                            topic_fields["channelID"] = channelid
                            topic_fields["channeltype"] = channel_type
                            topic_fields["_id"] = article_id
                            topic_fields["contentType"] = article_type
                            topic_fields["topicUrl"] = share_url
                            find1 = "."
                            if find1 in pubtime:
                                a = pubtime.find(find1)
                                b = len(pubtime)
                                c = b - a
                                pubtime = pubtime[:-c]
                            topic_fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                            topic_fields["topic"] = topic
                            topic_fields["title"] = article_title
                            # 将请求文章必需信息存入
                            articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                            articleparam["articleid"] = article_id
                            articlesparams.append(articleparam)
                        else:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            # 获取文章列表内的有用信息
                            article_id = articles["fileId"]
                            article_title = articles["title"]
                            article_type = articles["articleType"]
                            share_url = articles['shareUrl']
                            pubtime = articles["publishtime"]
                            article_covers = articles['pic_list_title']
                            images = articles['pic_list']
                            # 采集视频
                            try:
                                if 'videoUrl' in articles.keys():
                                    videoss = articles["videoUrl"]
                                    videos = list()
                                    videos.append(videoss)
                                    article_fields["videos"] = videos
                                    if 'pic0' in articles.keys():
                                        videocovers = list()
                                        videocover = articles["pic0"]
                                        videocovers.append(videocover)
                                        article_fields["videocovers"] = videocovers
                                    else:
                                        article_fields["videocovers"] = article_covers
                            except Exception as e:
                                logging.info(f"此新闻无视频{e}")
                            # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                            article_fields["articlecovers"] = article_covers
                            article_fields["images"] = images
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channeltype"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["contentType"] = article_type
                            article_fields["url"] = share_url
                            find1 = "."
                            if find1 in pubtime:
                                a = pubtime.find(find1)
                                b = len(pubtime)
                                c = b - a
                                pubtime = pubtime[:-c]
                            article_fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                            # 将请求文章必需信息存入
                            articleparam["articleField"] = article_fields  # 携带文章采集的数据
                            articleparam["articleid"] = article_id
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
            articleid = article.get("articleid")
            article_field = article.get("articleField")
            topic = article_field.get("topic")
            if topic == 1:
                headers = {
                    "Host": "qinwen.sanqin.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.8.0"
                }
                url = "https://qinwen.sanqin.com/app_if/getArticles"
                data = {
                    "columnId": articleid,
                    "version": "0",
                    "lastFileId": "0",
                    "page": "0",
                    "adv": "1",
                    "appID": "1",
                    "columnStyle": "101",
                }
            else:
                url = "https://qinwen.sanqin.com/app_if/getArticleContent"
                headers = {
                    "Host": "qinwen.sanqin.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.8.0"
                }
                data = {
                    "articleId": articleid,
                    "colID": article_field.get("channelID")
                }
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, data = data,
                                                             article_field = article_field)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        print(articleres)
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            topic = fields.get("topic")
            channelname = article.get("channelname")
            channelid = article.get("channelid")
            channel_type = article.get("channeltype")
            if topic:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                print(content_s)
                # articlesparams = []
                # for articles_arr in content_s["data"]["nodeList"]:
                #     for articles in articles_arr['contents']:
                #         article_fields = InitClass().article_fields()
                #         articleparam = InitClass().article_list_fields()
                #         # 获取文章列表内的有用信息
                #         article_id = articles["fileId"]
                #         article_title = articles["title"]
                #         article_type = articles["articleType"]
                #         share_url = articles['shareUrl']
                #         pubtime = articles["publishtime"]
                #         img = list()
                #         img.append(articles['pic_list_title'])
                #         article_covers = img
                #         images = articles['pic_list']
                #         # 采集视频
                #         try:
                #             if 'videoUrl' in articles.keys():
                #                 videoss = articles["videoUrl"]
                #                 videos = list()
                #                 videos.append(videoss)
                #                 article_fields["videos"] = videos
                #                 if 'pic0' in articles.keys():
                #                     videocovers = list()
                #                     videocover = articles["pic0"]
                #                     videocovers.append(videocover)
                #                     article_fields["videocovers"] = videocovers
                #                 else:
                #                     article_fields["videocovers"] = img
                #         except Exception as e:
                #             logging.info(f"此新闻无视频{e}")
                #         # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                #         article_fields["imageurl"] = article_covers
                #         article_fields["images"] = images
                #         article_fields["channelID"] = channelid
                #         article_fields["channelname"] = channelname
                #         article_fields["channeltype"] = channel_type
                #         article_fields["workerid"] = article_id
                #         article_fields["title"] = article_title
                #         article_fields["contentType"] = article_type
                #         article_fields["url"] = share_url
                #         find1 = "."
                #         if find1 in pubtime:
                #             a = pubtime.find(find1)
                #             b = len(pubtime)
                #             c = b - a
                #             pubtime = pubtime[:-c]
                #         article_fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                #         # 将请求文章必需信息存入
                #         articleparam["articleField"] = article_fields  # 携带文章采集的数据
                #         articleparam["articleid"] = article_id
                #         articlesparams.append(articleparam)
                # aaaa = self.getarticleparams(articlesparams)
                # bbbb= self.getarticlehtml(aaaa.__next__())
                # self.analyzearticle(bbbb.__next__())
            else:
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                    print(content_s)
                    worker_id = content_s["fileId"]
                    article_title = content_s["title"]
                    author = content_s["editor"]
                    source = content_s["source"]
                    content = content_s["content"]
                    likenum = content_s['countPraise']
                    commentnum = content_s['countDiscuss']
                    readnum = content_s['countClick']
                    sharenum = content_s['countShare']
                    contentType = 2
                    if channelname == '视频':
                        contentType = 4
                    fields["appname"] = self.newsname
                    fields["contentType"] = contentType
                    fields["likenum"] = likenum
                    fields["commentnum"] = commentnum
                    fields["readnum"] = readnum
                    fields["sharenum"] = sharenum
                    fields["title"] = article_title
                    fields["workerid"] = worker_id
                    fields["content"] = content
                    fields["source"] = source
                    fields["author"] = author
                    print(json.dumps(fields, indent=4, ensure_ascii=False))
                except Exception as e:
                    num += 1
                    logging.info(f"详情错误数量{num},{e}")

    def run(self):
        appparams = self.get_app_params()
        channelsres = self.getchannels(appparams.__next__())
        channelsparams = self.analyze_channel(channelsres.__next__())
        articlelistparames = self.getarticlelistparams(channelsparams.__next__())
        articleslistsres = self.getarticlelists(articlelistparames.__next__())
        articles = self.analyze_articlelists(articleslistsres.__next__())
        articleparams = self.getarticleparams(articles.__next__())
        articlesres = self.getarticlehtml(articleparams.__next__())
        self.analyzearticle(articlesres.__next__())


if __name__ == '__main__':
    appspider = QinWenNews("秦闻")
    appspider.run()
