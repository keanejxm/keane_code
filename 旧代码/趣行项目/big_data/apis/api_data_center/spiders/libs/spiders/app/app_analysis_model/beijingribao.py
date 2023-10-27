#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
解析模板，对app爬虫爬出的页面解析
北京日报app模板
author:keane
data:2020/10/28
"""
import json
import logging
# import time
# import hashlib
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class BeiJingRiBao(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://ie.bjd.com.cn/rest/site/api/5b165687a010550e5ddc0e6a/column/list/customer/get?"
        headers = {
            'app_key': 'newsroom-cms',
            'app_secret': 'bbbbbbaaaaaaaaaaaaa',
            'Host': 'ie.bjd.com.cn',
            'Connection': 'Keep-Alive',
            'User-Agent': 'okhttp/3.11.0',
        }
        data = {'udid': 'e8e733778f9dfc1e'}
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        """
        分析携带频道信息的网页，从网页中获取所需的id,以及频道名字信息
        :param channelsres:
        :return:
        """
        channelsparams = []

        # 解析app首页获取channelid及channelname，channeltype，categoryid，categoryname
        channelslists = json.loads(channelsres)
        for channels in channelslists['data']:
            channelid = channels['uuid']
            channelname = channels['name']

            # 创建对频道发送请求的数据模块
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    def getarticlelistparams(self, channelsparams):
        """
        对信息进行加工，得到对获取文章列表信息发送请求所需要的数据。
        :param channelsparams:分析channle获取的数据
        :return:
        """
        articlelistsparams = []
        channel_data = list()
        channel_num = 0
        headers = {
            'app_key': 'newsroom-cms',
            'app_secret': 'bbbbbbaaaaaaaaaaaaa',
            'Host': 'ie.bjd.com.cn',
            'User-Agent': 'okhttp/3.11.0',

        }
        for channelparam in channelsparams:
            channel_num += 1
            channelname = channelparam["channelname"]
            url = 'https://ie.bjd.com.cn/rest/site/api/5b165687a010550e5ddc0e6a/story/' + channelparam[
                "channelid"] + '/list/c/10/ls/blank/lc/0.json'
            data = {}
            method = 'get'
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                       channel_index_id=channel_index_id)
            articlelistsparams.append(articlelist_param)
            channel_data.append(channel_field)
        yield [channel_data, articlelistsparams]

    @staticmethod
    def analyze_articlelists(articleslistsres):
        """
        解析返回的文章列表页信息，获取文章对应的id，标题，以及封面图片信息。
        :param articleslistsres:
        :return:
        """
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            articleslists = articleslistres.get("channelres")
            channel_index_id = articleslistres.get("channelindexid")
            try:
                articleslists = json.loads(articleslists)
            except Exception as e:
                logging.info(f"解析文章失败{e}")
            a = articleslists['data']['recommends']
            b = articleslists['data']['sticks']
            c = articleslists['data']['list']
            #     # d=articleslists['data']['transverseSpecialData']['5de8be9be4b0fe93cc167bbc']
            for i in a + b + c:
                articleid = i['jsonUrl']
                articletitle = i['title']
                pubtime = i['publishTime']
                commentnum = i['commentNum']
                imageurl = ""
                try:
                    imageurl = i['thumbnails'][0]['thumbnailUrl']
                except Exception as e:
                    logging.info(f"获取封面图片失败{e}")
                articleparam = InitClass().article_list_fields()
                articleparam["articleid"] = articleid
                articleparam["articletitle"] = articletitle
                articleparam["imageurl"] = imageurl
                articleparam["channelname"] = channelname
                articleparam["channelindexid"] = channel_index_id
                articleparam["pubtime"] = pubtime
                articleparam["commentnum"] = commentnum
                articlesparams.append(articleparam)
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        """
        对信息进行加工，得到采集文章具体信息所需的数据
        :param articles:
        :return:
        """
        articleparams = []
        for article in articles:
            url = article.get("articleid")
            imgurl = article.get("imageurl")
            channelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            pubtime = article.get("pubtime")
            commentnum = article.get("commentnum")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (K'
                              'HTML, like Gecko) Version/4.0 Chrome/77.0.3865.92 Mobile Safari/537.36;sxrbdaily_android'
            }
            data = {}
            method = 'get'
            # 可添加字段，必填url，headers，method，channelname，imageurl
            # 可选字段，data，articlejson，pubtime，createtime，updatetime，source，author，likenum，commentnum
            articleparam = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                             pubtime=pubtime, commentnum=commentnum,
                                                             channel_index_id=channel_index_id)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        """
        对文章具体信息进行分析，得到所需要的数据
        :param articleres:
        :return:
        """
        for article in articleres:
            appname = article.get("appname")
            channnelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            imgurl = article.get("imageurl")
            pubtime = article.get("pubtime")
            createtime = article.get("createtime")
            updatetime = article.get("updatetime")
            likenum = article.get("likenum")
            commentnum = article.get("commentnum")
            articlejson = json.loads(article.get("articleres"))
            fields = InitClass().article_fields()
            if "title" in articlejson and articlejson["title"]:
                title = articlejson['title']
                fields["title"] = title
            if "source" in articlejson and articlejson["source"]:
                source = articlejson['source']
                fields["source"] = source
            if "content" in articlejson and articlejson['content']:
                content = articlejson['content']
                fields["content"] = content
            if "mediaStream" in articlejson and articlejson["mediaStream"]:
                videos = articlejson["mediaStream"]["url"]
                fields["videos"] = [videos]
            if "images" in articlejson and articlejson["images"]:
                images = []
                for image in articlejson["images"]:
                    images.append(image["url"])
                fields["images"] = images
            if "author" in articlejson and articlejson["author"]:
                author = articlejson["author"]
                fields["author"] = author
            url = articlejson["url"]
            fields["url"] = url
            fields["appname"] = appname
            fields["platformID"] = self.platform_id
            fields["channelname"] = channnelname
            fields["channelindexid"] = channel_index_id
            fields["articlecovers"] = imgurl
            fields["pubtime"] = pubtime
            fields["createtime"] = createtime
            fields["updatetime"] = updatetime
            fields["likenum"] = likenum
            fields["commentnum"] = commentnum
            fields = InitClass().wash_article_data(fields)
            yield {"code": 1, "msg": "OK", "data": {"works": fields}}


def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = BeiJingRiBao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
    appspider = BeiJingRiBao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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

# if __name__ == '__main__':
#     run()
