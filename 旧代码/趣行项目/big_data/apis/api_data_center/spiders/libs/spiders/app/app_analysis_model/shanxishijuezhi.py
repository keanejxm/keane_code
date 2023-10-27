"""
解析模板，对app爬虫爬出的页面解析
山西视觉志app模板
author:keane
data:2020/10/29
"""
import json
# import re
# import time
# import hashlib
import time

from spiders.libs.spiders.app.initclass import InitClass
from spiders.libs.spiders.app.appspider_m import Appspider


class Shanxishijue(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://sjz.sxrb.com/app/channel/config/v1.0"
        headers = {
            'version': 'android-1.5',
            'Host': 'sjz.sxrb.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.2.0'
        }
        data = {}
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(channelsres)
        for channels in channelslists['object']:
            channelid = channels['id']
            channelname = channels['name']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    def getarticlelistparams(self,channelsparams):
        articlelistsparams = []
        channel_data = list()
        headers = {
            'version': 'android-1.5',
            'Host': 'sjz.sxrb.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'Cookie': 'JSESSIONID=7683D75D11CD42696578F13D96DD56D6; __jsluid_h=d2231855d9f2a8edc3cfe623bc73b839',
            'User-Agent': 'okhttp/3.2.0',
        }
        channel_num = 0
        for channelparam in channelsparams:
            channel_num += 1
            url = 'http://sjz.sxrb.com/app/article/rec/v1.1/' + str(channelparam.get("channelid"))
            data = {}
            method = 'get'
            channelname = channelparam.get("channelname")
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            channel_data.append(channel_field)
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data,
                                                                       channel_index_id=channel_index_id)
            articlelistsparams.append(articlelist_param)
        yield [channel_data,articlelistsparams]

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channel_index_id = articleslistres.get("channelindexid")
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(articleslists)
            except Exception as e:
                print(e)
            for article in articleslists['object']['list']:
                articleparam = InitClass().article_list_fields()
                articleid = article['id']
                articletitle = article['title']
                imageurl = article['imgUrl']
                articleparam["articleid"] = articleid
                articleparam["articletitle"] = articletitle
                articleparam["imageurl"] = imageurl
                articleparam["channelname"] = channelname
                articleparam["channelindexid"] = channel_index_id
                articlesparams.append(articleparam)
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        for article in articles:
            imgurl = article.get("imageurl")
            channelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            try:
                url = 'http://sjz.sxrb.com/app/article/detail/v1.0/' + str(article.get("articleid"))
                headers = {
                    'version': 'android-1.5',
                    'Host': 'sjz.sxrb.com',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                    'Cookie': 'JSESSIONID=7683D75D11CD42696578F13D96DD56D6; __jsluid_h=d2231855d9f2a8edc3cfe623bc73b83'
                              '9',
                    'User-Agent': 'okhttp/3.2.0',
                }
                data = {}
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, channelname, imgurl,
                                                                 data = data, channel_index_id=channel_index_id)
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
                articlejson = articlejson['object']
                print(articlejson)
                fields = InitClass().article_fields()
                fields["appname"] = appname
                fields["platformID"] = self.platform_id
                fields["channelname"] = channnelname
                fields["channelindexid"] = channel_index_id
                fields["articlecovers"] = imgurl
                workerid = articlejson["id"]
                fields["workerid"] = workerid
                try:
                    title = articlejson['title']
                    fields["title"] = title
                except Exception as e:
                    print(e)
                try:
                    pubtime = articlejson['pubTime']
                    pubtime = pubtime.replace("月","-")
                    pubtime = pubtime.replace("日","")
                    pubtimes = "2021-"+pubtime
                    pubtime = InitClass().date_time_stamp(pubtimes)
                    now = time.time()*1000
                    if pubtime > now:
                        pubtime = pubtimes.replace("2021","2020")
                        pubtime = InitClass().date_time_stamp(pubtime)
                    fields["pubtime"] = pubtime
                except Exception as e:
                    print(e)
                try:
                    source = articlejson['source']
                    fields["source"] = source
                except Exception as e:
                    print(e)
                images = list()
                image = articlejson["imgUrl"]
                if image:
                    images.append(image)
                fields["images"] = images
                try:
                    content = articlejson['content']
                    fields["content"] = content
                except Exception as e:
                    print(e)
                try:
                    commentnum = articlejson['commentCount']
                    fields["commentnum"] = commentnum
                except Exception as e:
                    print(e)
                try:
                    likenum = articlejson['likeCount']
                    fields["likenum"] = likenum
                except Exception as e:
                    print(e)
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)

def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = Shanxishijue(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
    appspider = Shanxishijue(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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

