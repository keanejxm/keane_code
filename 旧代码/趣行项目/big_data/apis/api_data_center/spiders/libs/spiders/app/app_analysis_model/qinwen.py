# -*- encoding:utf-8 -*-
"""
@功能:秦闻解析模板
@AUTHOR：Keane
@文件名：ZhongGuoLan.py
@时间：2020/12/17  17:33
"""

import json
import logging

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


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
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(channelsres)
        for channel in channelslists['columns']:
            channelid = channel['columnId']
            channelname = channel['columnName']
            if channelname != '专题':
                channelparam = InitClass().channel_fields(channelid, channelname)
                yield channelparam
        yield {"channelid": "6677", "channelname": "视频"}

    def getarticlelistparams(self, channelsres):
        headers = {
            "Host": "qinwen.sanqin.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.0"
        }
        url = "https://qinwen.sanqin.com/app_if/getArticles"
        channel_num = 0
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
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
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid=channelid, data=data,
                                                                       channeltype=channeltype,
                                                                       channel_index_id=channel_index_id)
            yield channel_field, [articlelist_param]

    @staticmethod
    def analyze_articlelists(articleslistsres):
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channel_index_id = articleslistres.get("channelindexid")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            channel_type = articleslistres.get("channeltype")
            try:
                articleslists = json.loads(articleslists)
                try:
                    for articles in articleslists["list"]:
                        article_type = articles["articleType"]
                        if article_type == 3:
                            # 这种类型为专题
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
                            topic_fields["channelindexid"] = channel_index_id
                            topic_fields["channelID"] = channelid
                            topic_fields["channeltype"] = channel_type
                            topic_fields["topicID"] = article_id
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
                            yield topic_fields
                            # 将请求文章必需信息存入
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
                            article_fields["channelindexid"] = channel_index_id
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
                            yield article_fields
                            # 将请求文章必需信息存入
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")

    def getarticleparams(self,articleslistsres):
        for article in self.analyze_articlelists(articleslistsres):
            articleid = article.get("workerid")
            topic = article.get("topic")
            if topic == 1:
                articleid = article.get("topicID")
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
                    "colID": article.get("channelID")
                }
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                             article_field=article)
            yield [articleparam]

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            topic = fields.get("topic")
            channelname = article.get("channelname")
            if topic:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                print(content_s)
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
                    fields["platformID"] = self.platform_id
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
                    fields = InitClass().wash_article_data(fields)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
                except Exception as e:
                    num += 1
                    logging.info(f"详情错误数量{num},{e}")

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = QinWenNews(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data

