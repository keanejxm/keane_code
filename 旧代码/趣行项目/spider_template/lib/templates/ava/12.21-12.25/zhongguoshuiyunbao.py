# -*- encoding:utf-8 -*-
"""
@功能:中国水运报解析模板
@AUTHOR：Keane
@文件名：zhongguoshuiyunbao.py
@时间：2020/12/17  17:33
"""

import json
import logging

from appspider_m import Appspider
from initclass import InitClass


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
        app_params = InitClass().app_params(url, headers, method, data = data)
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
        channelparams = []
        for channel in channelslists['columns']:
            channelid = channel['columnID']
            channelname = channel['columnName']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)
        channelparams = channelparams + navList
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        print(channelsparams)
        articlelistsparams = []
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Host": "api.zgsyb.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.11.0"
        }
        url = "http://api.zgsyb.com/api/getArticles"
        for channel in channelsparams:
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
                            topic_fields["channelID"] = channelid
                            topic_fields["channeltype"] = channel_type
                            topic_fields["_id"] = article_id
                            topic_fields["contentType"] = article_type
                            topic_fields["pubtime"] = pubtime
                            topic_fields["topic"] = topic
                            topic_fields["title"] = article_title
                            # 将请求文章必需信息存入
                            articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                            articleparam["articleid"] = article_id
                            articlesparams.append(articleparam)
                        elif article_type != 3:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            # 获取文章列表内的有用信息
                            article_id = articles["fileID"]
                            article_title = articles["title"]
                            article_type = articles["articleType"]
                            share_url =articles['articleUrl']
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
                            article_fields["channeltype"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["contentType"] = article_type
                            article_fields["url"] = share_url
                            article_fields["pubtime"] = pubtime
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
            channelid = article_field.get("channelID")
            if topic == 1:
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
            articleparam = InitClass().article_params_fields(url, headers, method, data = data,
                                                             article_field = article_field,sleeptime=5)
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
                bbbb= self.getarticlehtml(aaaa.__next__())
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
                    print(json.dumps(fields, indent=4, ensure_ascii=False))
                except Exception as e:
                    num += 1
                    logging.info(f"错误数量{num},{e}")

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
    appspider = ZhongGuoShuiYunBaoNews("中国水运报")
    appspider.run()
