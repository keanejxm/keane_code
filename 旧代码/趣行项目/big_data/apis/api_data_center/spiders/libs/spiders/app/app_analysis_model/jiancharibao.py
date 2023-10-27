#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
检察日报解析模板
# author: Keane
# create date: 2020/11/27
# update date: 2020/11/27
# appversion: 
"""
import json
import logging
# import re
# import time
# import hashlib
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class JianChaRiBao(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://jcrbapp.techjc.cn/api/getColumns?sid=1&cid=1"
        headers = {
            'Host': 'jcrbapp.techjc.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.7.0',
        }
        data = {}
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))
        for channels in channelslists['columns']:
            channelid = channels['columnID']
            channelname = channels['columnName']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        channelparam = InitClass().channel_fields(7, "视觉")
        channelsparams.append(channelparam)
        yield channelsparams

    def getarticlelistparams(self, channelsparams):
        articlelistsparams = []
        channel_data = list()
        headers = {
            'Host': 'jcrbapp.techjc.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.7.0',
        }
        url = 'http://jcrbapp.techjc.cn/api/getArticles?'
        channel_num = 0
        for channelparam in channelsparams:
            channel_num += 1
            channelid = channelparam.get("channelid")
            data = {
                'sid': '1',
                'cid': channelid,
                'lastFileID': '0',
                'rowNumber': '0',
            }
            method = 'get'
            channelname = channelparam.get("channelname")
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            channel_data.append(channel_field)
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                       channel_index_id=channel_index_id)
            articlelistsparams.append(articlelist_param)
        yield [channel_data, articlelistsparams]

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channel_index_id = articleslistres.get("channelindexid")
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists)))
                try:
                    for articles in articleslists["list"]:
                        articleid = articles["fileID"]
                        articletitle = articles["title"]
                        pubtime = articles["publishTime"]
                        imageurl = articles["pic1"]
                        author = articles["createUser"]
                        channelid = articles["columnID"]
                        articleparam = InitClass().article_list_fields()
                        articleparam["channelid"] = channelid
                        articleparam["channelindexid"] = channel_index_id
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["pubtime"] = pubtime
                        articleparam["imageurl"] = imageurl
                        articleparam["channelname"] = channelname
                        articleparam["author"] = author
                        articlesparams.append(articleparam)
                except Exception as e:
                    logging.info(f"获取文章列表数据失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表失败{e}")
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        for article in articles:
            imgurl = article.get("imageurl")
            articleid = article.get("articleid")
            channelid = article.get("channelid")
            channelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            pubtime = article.get("pubtime")
            author = article.get("author")
            url = "http://jcrbapp.techjc.cn/api/getArticle?"
            headers = {
                'Host': 'jcrbapp.techjc.cn',
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip',
                'User-Agent': 'okhttp/3.7.0',
            }
            data = {
                'sid': '1',
                'aid': articleid,
                'cid': channelid,
            }
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                             pubtime=pubtime, author=author,
                                                             channel_index_id=channel_index_id)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self,articleres):
        for article in articleres:
            fields = InitClass().article_fields()
            channnelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            imageurl = article.get("imageurl")
            appname = article.get("appname")
            try:
                articlejson = json.loads(
                    json.dumps(json.loads(article.get("articleres")), indent=4, ensure_ascii=False))
                workerid = articlejson['fileID']
                title = articlejson['title']
                pubtime = articlejson['publishTime']
                source = articlejson['source']
                content = articlejson['content']
                author = articlejson['author']
                try:
                    video = articlejson["videos"][0]["videoUrl"]
                    fields["videos"] = video
                except Exception as e:
                    print(f"此新闻无视频{e}")
                fields["appname"] = appname
                fields["platformID"] = self.platform_id
                fields["channelindexid"] = channel_index_id
                fields["content"] = content
                fields["workerid"] = workerid
                fields["title"] = title
                fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                fields["source"] = source
                fields["author"] = author
                fields["channelname"] = channnelname
                fields["articlecovers"] = imageurl
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)


def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = JianChaRiBao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    appparams = appspider.get_app_params()
    channelsres = appspider.getchannel(appparams.__next__())
    channelsparams = appspider.analyze_channel(channelsres.__next__())
    articlelistparameses = appspider.getarticlelistparams(channelsparams.__next__())
    articlelistparamess = list()
    for articlelistparamesss in articlelistparameses:
        articlelistparamess = articlelistparamesss
    channel_data = articlelistparamess[0]
    articlelistparames = articlelistparamess[1]
    articleslistsres = appspider.getarticlelists(articlelistparames)
    articles = appspider.analyze_articlelists(articleslistsres.__next__())
    articleparams = appspider.getarticleparams(articles.__next__())
    articlesres = appspider.getarticlehtml(articleparams.__next__())
    app_data = appspider.analyzearticle(articlesres.__next__())
    article_retu = {
        "code": "1",
        "msg": "json",
        "data": dict(),
    }
    data_dict = dict()
    data_dict["channels"] = channel_data
    articles_list = list()
    topics_list = list()
    for data in app_data:
        if "works" in data["data"]:
            articles_list.append(data["data"]["works"])
        elif "topic" in data["data"]:
            topics_list.append(data["data"]["topic"])
        else:
            pass
    article_retu["data"]["topics"] = topics_list
    article_retu["data"]["worksList"] = articles_list
    yield article_retu


def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = JianChaRiBao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    appparams = appspider.get_app_params()
    channelsres = appspider.getchannels(appparams.__next__())
    channelsparams = appspider.analyze_channel(channelsres.__next__())
    articlelistparameses = appspider.getarticlelistparams(channelsparams.__next__())
    articlelistparamess = list()
    for articlelistparamesss in articlelistparameses:
        articlelistparamess = articlelistparamesss
    channel_data = articlelistparamess[0]
    channel_flag = 1
    articlelistparames = articlelistparamess[1]
    articleslistsres = appspider.getarticlelists(articlelistparames)
    articles = appspider.analyze_articlelists(articleslistsres.__next__())
    articleparams = appspider.getarticleparams(articles.__next__())
    articlesres = appspider.getarticlehtml(articleparams.__next__())
    app_data = appspider.analyzearticle(articlesres.__next__())
    for data in app_data:
        datas = data["data"]
        if channel_flag:
            datas["channels"] = channel_data
            channel_flag = 0
        yield data
