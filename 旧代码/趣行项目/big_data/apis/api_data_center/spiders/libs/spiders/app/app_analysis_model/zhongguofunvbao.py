"""
解析模板，对app爬虫爬出的页面解析
中国妇女报app模板
author:keane
data:2020/10/29
"""
import json
# import re
# import time
# import hashlib
import logging

from spiders.libs.spiders.app.initclass import InitClass
from spiders.libs.spiders.app.appspider_m import Appspider


class Zhongguofunv(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://weixing.cnwomen.com.cn:8080/amc/client/listSubscribeColumn?"
        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': 'weixing.cnwomen.com.cn:8080'
        }
        data = {
            'nodeCode': '3372ff6d-56e1-4a0a-b812-e9b6d3ba2dcd',
            'contentType': '0,6,11'
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(channelsres)
        for channels in channelslists['data']['list']:
            channelid = channels['columnId']
            channelname = channels['columnName']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    def getarticlelistparams(self, channelsparams):
        articlelistsparams = []
        channel_data = list()
        channel_num = 0
        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': 'weixing.cnwomen.com.cn:8080'
        }
        for channelparam in channelsparams:
            channel_num += 1
            url = 'http://weixing.cnwomen.com.cn:8080/amc/client/getColumnHomePageData?'
            data = {
                'column': str(channelparam.get("channelid")),
                'publishFlag': '1',
                'focusNo': '5',
                'pageNo': '0',
                'pageSize': '10'
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
                articleslists = json.loads(articleslists)
                a = articleslists['data']['focusList']
                b = articleslists['data']['contentList']
                articleslist = a + b
                for article in articleslist:
                    articleparam = InitClass().article_list_fields()
                    articleid = article['contentId']
                    articletitle = article['title']
                    try:
                        imageurl = article['imgUrl']
                    except Exception as e:
                        logging.info(f"{e}")
                        imageurl = article['imgList'][0]['url']
                    articleparam["articleid"] = articleid
                    articleparam["articletitle"] = articletitle
                    articleparam["imageurl"] = imageurl
                    articleparam["channelname"] = channelname
                    articleparam["channelindexid"] = channel_index_id
                    articlesparams.append(articleparam)
            except Exception as e:
                logging.info(f"{e}")
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        for article in articles:
            imgurl = article.get("imageurl")
            channelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            try:
                url = 'http://weixing.cnwomen.com.cn:8080/amc/client/getImageTextContentById?'
                headers = {
                    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
                    'Host': 'weixing.cnwomen.com.cn:8080'
                }
                data = {
                    'contentId': article.get("articleid"),
                    'fromFlag': '0'
                }
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                                 channel_index_id=channel_index_id)
                articleparams.append(articleparam)
            except Exception as e:
                print(e)
        yield articleparams

    def analyzearticle(self,articleres):
        for article in articleres:
            channnelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            imgurl = article.get("imageurl")
            appname = article.get("appname")
            try:
                articlejson = json.loads(article.get("articleres"))
                # print(json.dumps(articlejson,indent=4,ensure_ascii=False))
                # yield 'ss'
                articlejson = articlejson['data']
                fields = InitClass().article_fields()
                fields["channelname"] = channnelname
                fields["channelindexid"] = channel_index_id
                fields["articlecovers"] = imgurl
                fields["appname"] = appname
                fields["platformID"] = self.platform_id
                try:
                    title = articlejson['title']
                    fields["title"] = title
                except Exception as e:
                    print(e)
                try:
                    pubtime = articlejson['publishTime']
                    fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                except Exception as e:
                    print(e)
                try:
                    source = articlejson['source']
                    fields["source"] = source
                except Exception as e:
                    print(e)
                try:
                    content = articlejson['text']
                    fields["content"] = content
                except Exception as e:
                    print(e)
                try:
                    commentnum = articlejson['commentCount']
                    fields["commentnum"] = commentnum
                except Exception as e:
                    print(e)
                try:
                    author = articlejson['editor']
                    fields["author"] = author
                except Exception as e:
                    print(e)
                url = articlejson["shareUlr"]
                fields["url"] = url
                workerid = articlejson["contentId"]
                fields["workerid"] = workerid
                video = articlejson["relatedVideo"]
                if video:
                    videos = list()
                    videos.append(video)
                    fields["videos"] = [videos]
                fields = InitClass().wash_article_data(fields)
                print(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)


def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = Zhongguofunv(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
    appspider = Zhongguofunv(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
