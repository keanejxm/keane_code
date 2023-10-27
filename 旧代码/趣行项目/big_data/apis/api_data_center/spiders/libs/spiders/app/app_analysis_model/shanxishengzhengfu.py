"""
解析模板，对app爬虫爬出的页面解析
山西省政府app模板
author:keane
data:2020/10/29
"""
import json
import logging
import re
# import time
# import hashlib
from spiders.libs.spiders.app.initclass import InitClass
from spiders.libs.spiders.app.appspider_m import Appspider


class Shanxishengzhengfu(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://app2017.shanxi.gov.cn/model_1/channels.json"
        headers = {
            'Host': 'app2017.shanxi.gov.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.4.1'
        }
        data = {}
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(channelsres)
        for channels in channelslists['gd']:
            channelid = channels['documents']
            channelname = channels['cname']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    def getarticlelistparams(self,channelsparams):
        articlelistsparams = []
        channel_data = list()
        channel_num = 0
        headers = {
            'Host': 'app2017.shanxi.gov.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.4.1'
        }
        for channelparam in channelsparams:
            channel_num += 1
            url = channelparam.get("channelid")
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
                logging.info(f"解析文章列表失败{e}")
            for article in articleslists['list_datas']:
                articleparam = InitClass().article_list_fields()
                articleid = article['url']
                articletitle = article['title']
                imageurl = ''
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
            articleurl = article.get("articleid")
            article_p = re.findall('(model_1\S*.json)', articleurl)
            try:
                article_p = article_p[0]
                url = 'http://app2017.shanxi.gov.cn/' + article_p
                headers = {
                    'Host': 'app2017.shanxi.gov.cn',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                    'User-Agent': 'okhttp/3.4.1'
                }
                data = {}
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data = data,
                                                                 channel_index_id=channel_index_id)
                articleparams.append(articleparam)
            except Exception as e:
                logging.info(f"获取文章数据失败{e}")
        yield articleparams

    def analyzearticle(self,articleres):
        for article in articleres:
            channnelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            imgurl = article.get("imageurl")
            appname = article.get("appname")
            s = article.get("articleres").replace('\n', '')
            s = s.replace(" ", '')
            fields = InitClass().article_fields()
            fields["channelname"] = channnelname
            fields["channelindexid"] = channel_index_id
            fields["platformID"] = self.platform_id
            fields["articlecovers"] = imgurl
            fields["appname"] = appname
            try:
                articlejson = json.loads(s)
                articlejson = articlejson['datas']
                url = articlejson["sharelink"]
                imagess = articlejson["images"]
                if imagess:
                    images = list()
                    for image in imagess:
                        images.append(image["src"])
                    fields["images"] = images
                workerid = articlejson["docid"]
                fields["url"] = url
                fields["workerid"] = workerid
                try:
                    title = articlejson['title']
                    fields["title"] = title
                except Exception as e:
                    print(e)
                try:
                    updatetime = articlejson['updatedate']
                    fields["updatetime"] = InitClass().date_time_stamp(updatetime)
                except Exception as e:
                    print(e)
                try:
                    source = articlejson['source']
                    fields["source"] = source
                except Exception as e:
                    print(e)
                try:
                    content = articlejson['body']
                    fields["content"] = content
                except Exception as e:
                    print(e)
                try:
                    commentnum = articlejson['comments']
                    fields["commentnum"] = commentnum
                except Exception as e:
                    print(e)
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)

def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = Shanxishengzhengfu(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
    appspider = Shanxishengzhengfu(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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

