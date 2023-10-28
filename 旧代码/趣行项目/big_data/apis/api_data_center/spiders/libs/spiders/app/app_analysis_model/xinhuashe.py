#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
新华社app解析模板
# author: Keane
# create date: 2020/11/23
# update date: 2020/11/23
# appversion:
"""
import json
import re
import logging
import time

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


# from lib.crawler.spiders.app.akafkaproduert import KafkaProducer


class XinHuaShe(Appspider):
    logging.basicConfig(level=logging.INFO)

    @staticmethod
    def get_app_params():
        url = "https://xhpfmapi.zhongguowangshi.com/v708/core/nav"
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Content-Length": "541",
            "Host": "xhpfmapi.zhongguowangshi.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.11.0"
        }
        data = {}
        method = "post"
        appjson = {"address": "", "city": "", "clientApp": "104", "clientBundleID": "net.xinhuamm.mainclient",
                   "clientDate": 1611394674, "clientDev": 0, "clientHeight": 1024,
                   "clientId": "8f98851a8de550633503b314c43c3eb5",
                   "clientLable": "00000000-7f00-1df9-ffff-ffffa8e77524", "clientLatitude": 0.0, "clientLongitude": 0.0,
                   "clientMarket": "337", "clientModel": "MuMu", "clientNet": "wifi", "clientOS": "6.0.1",
                   "clientPrison": "0", "clientToken": "8f98851a8de550633503b314c43c3eb5", "clientType": 2,
                   "clientVer": "8.0.2", "clientWidth": 576, "h5request": 0, "loginStatus": 0, "province": "",
                   "userID": 0}
        app_params = InitClass().app_params(url, headers, method, data=data, appjson=appjson)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(channelsres)
        datas = channelslists["data"]["data"] + channelslists["data"]["order_data"]
        for channels in datas:
            channelid = channels['id']
            channelname = channels['name']
            channelcolumtype = channels['columntype']
            channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channelcolumtype)
            channelsparams.append(channelparam)
        yield channelsparams

    def getarticlelistparams(self, channelsparams):
        articlelistsparams = []
        channel_data = list()
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Content-Length': '643',
            'Host': 'xhpfmapi.zhongguowangshi.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.11.0',
        }
        method = 'post'
        channel_num = 0
        for channel in channelsparams:
            channel_num += 1
            url = "https://xhpfmapi.zhongguowangshi.com/v708/core/indexlist"
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channelcolumtype = channel.get("channeltype")
            channeljson = {"columnid": channelid, "columntype": channelcolumtype, "count": 0, "excludeRecommend": 0, "groupCategoryId": 0, "id": 0,
        "pn": 1, "address": "", "city": "", "clientApp": "104", "clientBundleID": "net.xinhuamm.mainclient",
        "clientDate": 1611403623, "clientDev": 0, "clientHeight": 1024, "clientId": "8f98851a8de550633503b314c43c3eb5",
        "clientLable": "00000000-7f00-1df9-ffff-ffffa8e77524", "clientLatitude": 0.0, "clientLongitude": 0.0,
        "clientMarket": "337", "clientModel": "MuMu", "clientNet": "wifi", "clientOS": "6.0.1", "clientPrison": "0",
        "clientToken": "8f98851a8de550633503b314c43c3eb5", "clientType": 2, "clientVer": "8.0.2", "clientWidth": 576,
        "h5request": 0, "loginStatus": 0, "province": "", "userID": 0}
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            channel_data.append(channel_field)
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channeljson=channeljson,
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
                articleslists = json.loads(articleslists)
                try:
                    for articles in (articleslists['data']['data'] + articleslists['data']['data_scroll']):
                        articleparam = InitClass().article_list_fields()
                        articleid = articles['id']
                        articletitle = articles['topic']
                        imageurl = articles['detailImg']
                        commentnum = articles['commentCount']
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["imageurl"] = imageurl
                        articleparam["channelname"] = channelname
                        articleparam["channelindexid"] = channel_index_id
                        articleparam["commentnum"] = commentnum
                        articlesparams.append(articleparam)
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        headers = {
            "Host": "xhpfmapi.zhongguowangshi.com",
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.11.0"',
        }
        for article in articles:
            articleid = article.get("articleid")
            url = "https://xhpfmapi.zhongguowangshi.com/v600/news/{}.js?ts=0&share=0".format(articleid)
            imgurl = article.get("imageurl")
            channelname = article.get("channelname")
            channelindexid = article.get("channelindexid")
            commentnum = article.get("commentnum")
            try:
                data = dict()
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                                 commentnum=commentnum, channel_index_id=channelindexid)
                articleparams.append(articleparam)
            except Exception as e:
                logging.info(f"生成文章信息失败{e}")
        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            channelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            imgurl = article.get("imageurl")
            appname = article.get("appname")
            likenum = article.get("likenum")
            article_s = re.findall('var XinhuammNews =(.*)', article.get("articleres"))
            if article_s:
                content_s = article_s[0]
                try:
                    content_s = json.loads(content_s, strict=False)
                    fields = InitClass().article_fields()
                    fields["channelname"] = channelname
                    fields["channelindexid"] = channel_index_id
                    fields["platformID"] = self.platform_id
                    fields["appname"] = appname
                    fields["title"] = content_s["topic"]
                    fields["content"] = content_s["content"]
                    fields["articlecovers"] = [imgurl]
                    fields["images"] = content_s["imglist"]  # 如果有视频采集视频信息
                    url = content_s["shareurl"]
                    workerid = content_s["id"]
                    fields["url"] = url
                    fields["workerid"] = workerid
                    if content_s["videourl"]:
                        videos = content_s["videourl"]
                        fields["videos"] = videos
                        fields["videoscover"] = content_s["videoImageurl"]
                        fields["width"] = content_s["videoWidth"]
                        fields["height"] = content_s["videoHeight"]
                    fields["source"] = content_s["docSource"]
                    fields["pubtime"] = content_s["relaseDateTimeStamp"]
                    fields["sharenum"] = content_s["share"]
                    fields["createtime"] = content_s["createDate"]
                    fields["commentnum"] = content_s["commentCount"]
                    fields["likenum"] = likenum
                    fields = InitClass().wash_article_data(fields)
                    print(fields)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
                except Exception as e:
                    num += 1
                    logging.info(f"错误数量{num},{e},{content_s}")


def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = XinHuaShe(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    appparams = appspider.get_app_params()
    channelsres = appspider.getchannels(appparams.__next__())
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
    appspider = XinHuaShe(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
