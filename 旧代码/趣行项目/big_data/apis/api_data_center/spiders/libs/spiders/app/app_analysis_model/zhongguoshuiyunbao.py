# -*- encoding:utf-8 -*-
"""
@功能:中国水运报解析模板
@AUTHOR：Keane
@文件名：zhongguoshuiyunbao.py
@时间：2020/12/17  17:33
"""

import json
import logging

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class ZhongGuoShuiYunBaoNews(Appspider):

    @staticmethod
    def get_app_params():

        url = "http://api.zgsyb.com/api/getColumns"
        headers = {
            "Host": "api.zgsyb.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.11.0"
        }
        data = {
            "sid": "1",
            "cid": "11141"
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        navList = [
            {
                'channelid': '27602',
                'channelname': '专题',
            },
            {
                'channelid': '23194',
                'channelname': '中运课堂',
            },
            {
                'channelid': '11202',
                'channelname': '航行安全',
            },
            {
                'channelid': '11204',
                'channelname': '航运报告',
            },
            {
                'channelid': '11205',
                'channelname': '船民直通车',
            }
        ]
        channelslists = json.loads(channelsres)
        for channel in channelslists['columns']:
            channelid = channel['columnID']
            channelname = channel['columnName']
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam
        for channel in navList:
            yield channel

    def getarticlelistparams(self, channelsres):
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Host": "api.zgsyb.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.11.0"
        }
        url = "http://api.zgsyb.com/api/getArticles"
        channel_num = 0
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")
            data = {
                "sid": "1",
                "cid": channelid,
                "lastFileID": "0",
                "rowNumber": "0",
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
                        if article_type == 4:
                            # 这种类型为专题
                            print(articles)
                            topic_fields = InitClass().topic_fields()
                            articleparam = InitClass().article_list_fields()
                            # 获取文章列表内的有用信息
                            article_id = articles["linkID"]
                            article_title = articles["title"]
                            article_type = articles["articleType"]
                            pubtime = InitClass().date_time_stamp(articles["publishTime"])
                            topic = 1
                            topic_fields["channelName"] = channelname
                            topic_fields["channelindexid"] = channel_index_id
                            topic_fields["channelID"] = channelid
                            topic_fields["channeltype"] = channel_type
                            topic_fields["toppicID"] = article_id
                            topic_fields["contentType"] = article_type
                            topic_fields["pubtime"] = pubtime
                            topic_fields["topic"] = topic
                            topic_fields["title"] = article_title
                            yield topic_fields
                        elif article_type != 3:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            # 获取文章列表内的有用信息
                            article_id = articles["fileID"]
                            article_title = articles["title"]
                            article_type = articles["articleType"]
                            share_url = articles['articleUrl']
                            pubtime = InitClass().date_time_stamp(articles["publishTime"])
                            article_covers = list()
                            if 'pic1' in articles.keys():
                                article_covers.append(articles['pic1'])

                            # 采集视频
                            try:
                                if articles['videoUrl']:
                                    videocovers = list()
                                    videocovers.append(articles['pic1'])
                                    videos = list()
                                    videos.append(articles['videoUrl'])
                                    article_fields["videos"] = videos
                                    article_fields["videocovers"] = videocovers
                            except Exception as e:
                                logging.info(f"此新闻无视频{e}")
                            # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                            article_fields["articlecovers"] = article_covers
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channelindexid"] = channel_index_id
                            article_fields["channeltype"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["contentType"] = article_type
                            article_fields["url"] = share_url
                            article_fields["pubtime"] = pubtime
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
            channelid = article.get("channelID")
            if topic == 1:
                articleid = article.get("topicID")
                headers = {
                    "Host": "api.zgsyb.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.11.0"
                }
                url = "http://api.zgsyb.com/api/getSubColumns"
                data = {
                    "cid": articleid,
                    "type": "3",
                    "order": "desc"
                }
            else:
                url = "http://api.zgsyb.com/api/getArticle"
                headers = {
                    "Host": "api.zgsyb.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.11.0"
                }
                data = {
                    "sid": "1",
                    "aid": articleid,
                    "cid": channelid
                }
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                             article_field=article, sleeptime=5)
            yield [articleparam]

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            topic = fields.get("topic")
            channelid = article.get("channelid")
            channel_type = article.get("channeltype")
            if topic:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                print(content_s)
                articlesparams = []
                for article_list in content_s['list']:
                    for articles in article_list['list']:
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        # 获取文章列表内的有用信息
                        article_id = articles["fileID"]
                        article_title = articles["title"]
                        article_type = articles["articleType"]
                        share_url = ''
                        pubtime = InitClass().date_time_stamp(articles["publishTime"])
                        article_covers = list()
                        if 'pic1' in articles.keys():
                            article_covers.append(articles['pic1'])

                        # 采集视频
                        try:
                            if articles['videoUrl']:
                                videocovers = list()
                                videocovers.append(articles['pic1'])
                                videos = list()
                                videos.append(articles['videoUrl'])
                                article_fields["videos"] = videos
                                article_fields["videocovers"] = videocovers
                        except Exception as e:
                            logging.info(f"此新闻无视频{e}")
                        # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入

                        article_fields["articlecovers"] = article_covers
                        article_fields["channelID"] = channelid
                        article_fields["channelname"] = fields.get('channelName')
                        article_fields["channeltype"] = channel_type
                        article_fields["workerid"] = article_id
                        article_fields["title"] = article_title
                        article_fields["contentType"] = article_type
                        article_fields["url"] = share_url
                        article_fields["pubtime"] = pubtime
                        article_fields["specialtopic"] = topic
                        article_fields["topicid"] = fields.get('_id')
                        article_fields["topicTitle"] = fields.get('title')
                        # 将请求文章必需信息存入
                        articleparam["articleField"] = article_fields  # 携带文章采集的数据
                        articleparam["articleid"] = article_id
                        articlesparams.append(articleparam)
                aaaa = self.getarticleparams(articlesparams)
                bbbb = self.getarticlehtml(aaaa.__next__())
                self.analyzearticle(bbbb.__next__())
            else:
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                    print(content_s)
                    worker_id = content_s["fileID"]
                    article_title = content_s["title"]
                    author = content_s["editor"]
                    source = content_s["source"]
                    content = content_s["content"]
                    try:
                        imagess = content_s["data"]["images"]
                        images = list()
                        for image in imagess:
                            images.append(image["url"])
                        fields["images"] = images
                    except Exception as e:
                        self.logger.info(f"获取文章内图片失败{e}")

                    likenum = content_s["countPraise"]
                    readnum = content_s["countClick"]
                    sharenum = content_s["countShare"]
                    commentnum = content_s["countDiscuss"]
                    fields["likenum"] = likenum
                    fields["readnum"] = readnum
                    fields["sharenum"] = sharenum
                    fields["commentnum"] = commentnum
                    fields["appname"] = self.newsname
                    fields["title"] = article_title
                    fields["workerid"] = worker_id
                    fields["content"] = content
                    fields["source"] = source
                    fields["author"] = author
                    fields = InitClass().wash_article_data(fields)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
                except Exception as e:
                    num += 1
                    logging.info(f"错误数量{num},{e}")

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = ZhongGuoShuiYunBaoNews(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
