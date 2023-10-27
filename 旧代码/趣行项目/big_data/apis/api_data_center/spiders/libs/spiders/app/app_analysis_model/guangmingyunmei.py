#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class GuanMingYunMei(Appspider):
    @staticmethod
    def analyze_channel():
        nav_list = [{'sa': 'wh', 'name': '文化'},
                    {'sa': 'kj', 'name': '科技'},
                    {'sa': 'jy', 'name': '教育'},
                    {'sa': 'ty', 'name': '体育'},
                    {'sa': 'jk', 'name': '健康'},
                    {'sa': 'tq', 'name': '天气'},
                    {'sa': 'jt', 'name': '交通'},
                    {'sa': 'ly', 'name': '旅游'}]
        channelparams = []
        for channel in nav_list:
            channelid = channel['sa']
            channelname = channel['name']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)
        yield channelparams

    def getarticlelistparams(self, channelsparams):
        articleparams = []
        channel_data = list()
        channel_num = 0
        for channel in channelsparams:
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            url = f"http://gmym.gmw.cn/api/list/{channelid}/"
            headers = {
                "Accept-Encoding": "",
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
                "Host": "gmym.gmw.cn",
                "Connection": "Keep-Alive"
            }
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
            channel_data.append(channel_field)
            articleparams.append(articlelist_param)
        yield [channel_data, articleparams]

    def analyze_articlelists(self, articleslist_ress):
        articlesparams = []
        for articleslist_res in articleslist_ress:
            channelname = articleslist_res.get("channelname")
            channel_index_id = articleslist_res.get("channelindexid")
            articlelist_res = articleslist_res.get("channelres")
            try:
                articlelist_json = json.loads(articlelist_res)
                try:
                    articlelists = articlelist_json['list']
                    for article in articlelists:
                        articleparam = InitClass().article_list_fields()
                        articletitle = article['title']
                        articleid = article['articleId']
                        try:
                            articleparam["imageurl"] = article['picLinks']
                        except Exception as e:
                            self.logger.info(f"{self.newsname}没有获取到封面图{e}")
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["channelname"] = channelname
                        articleparam["channelindexid"] = channel_index_id
                        articlesparams.append(articleparam)
                except Exception as e:
                    self.logger.info(f"{self.newsname}提取文章列表字段失败{e}")
            except Exception as e:
                self.logger.info(f"{self.newsname}，json化文章列表页失败{e}")
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articlesparam = []
        headers = {
            "Accept-Encoding": "",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
            "Host": "gmym.gmw.cn",
            "Connection": "Keep-Alive"
        }
        method = 'get'
        for articleparam in articles:
            data = {
                'id': articleparam.get("articleid"),
                'cb': 'test.setMyArticalContent',
            }
            url = f'http://gmym.gmw.cn/api/item/{articleparam.get("articleid")}/'
            channelname = articleparam.get("channelname")
            channel_index_id = articleparam.get("channelindexid")
            imgurl = articleparam.get("imageurl")
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data ,
                                                        channel_index_id=channel_index_id)
            articlesparam.append(article)
        yield articlesparam

    def analyzearticle(self,articles_res):
        for articleres in articles_res:
            channelname = articleres.get("channelname")
            channel_index_id = articleres.get("channelindexid")
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["channelindexid"] = channel_index_id
            fields["platformID"] = self.platform_id
            fields["articlecovers"] = imgurl
            fields["appname"] = appname
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                if "data" in articlejson and articlejson["data"]:
                    title = articlejson['data']['title']  # 标题
                    source = articlejson['data']['source']  # 来源
                    content = articlejson['data']['artContent']  # 文章内容
                    pubtime = articlejson['data']['pubTime']  # 发布时间
                    workerid = articlejson['data']['articleId']
                    url = articlejson['data']["artUrl"]
                    videos = articlejson['data']["videoUrl"]
                    videocover = articlejson['data']["videoPoster"]
                    images = articlejson["data"]["images"]
                    fields["title"] = title
                    fields["url"] = url
                    fields["workerid"] = workerid
                    fields["source"] = source
                    fields["content"] = content
                    fields["pubtime"] = pubtime
                    fields["images"] = images
                    fields["videos"] = videos
                    fields["videocover"] = videocover
                    fields = InitClass().wash_article_data(fields)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)


def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = GuanMingYunMei(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    channelsparams = appspider.analyze_channel()
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
    appspider = GuanMingYunMei(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    channelsparams = appspider.analyze_channel()
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

