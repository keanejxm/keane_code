#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
功能描述。
# author: Keane
# create date: 2020/11/26
# update date: 2020/11/26
# appversion: 
"""
import json
import logging

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class JieFangJunBao(Appspider):
    logging.basicConfig(level=logging.INFO)

    @staticmethod
    def get_app_params():
        url = "http://111.203.147.58/v4/i/statuses/taglist.json"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '6',
            'Host': '111.203.147.58',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.8.0',
        }
        data = {}
        app_json = "type=1"
        method = "post"
        app_params = InitClass().app_params(url, headers, method, data=data, appjson=app_json)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))
        for channellists in channelslists:
            channels = channellists["column"]
            for channel in channels:
                channelid = channel['tag_id']
                channelname = channel['tag_name']
                channelcolumtype = channel['target_type']
                channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channelcolumtype)
                channelsparams.append(channelparam)
        yield channelsparams

    def getarticlelistparams(self, channelsparams):
        articlelistsparams = []
        channel_data = list()
        channel_num = 1
        url = "http://111.203.147.58/v4/i/statuses/getlist.json"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '6',
            'Host': '111.203.147.58',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.8.0',
        }
        method = 'post'
        for channel in channelsparams:
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channelcolumtype = channel.get("channelcolumtype")
            data = "devicetype={}&device_size=810.0x1440.0&version=196&tagid={}".format(channelcolumtype, channelid)
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                       channeltype=channelcolumtype,
                                                                       channel_index_id=channel_index_id)
            channel_data.append(channel_field)
            articlelistsparams.append(articlelist_param)
        yield [channel_data, articlelistsparams]

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            articleslists = articleslistres.get("channelres")
            channelcolumtype = articleslistres.get("channeltype")
            channel_index_id = articleslistres.get("channelindexid")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    for articles in articleslists:
                        articleparam = InitClass().article_list_fields()
                        articleid = articles['item_id']
                        articletitle = articles['title']
                        imageurl = articles['image_list']
                        commentnum = articles['comment_num']
                        author = articles['authors']
                        pubtime = articles['time']
                        try:
                            source = articles["doings_source"]
                            articleparam["source"] = source
                        except Exception as e:
                            logging.info(f"没有新闻来源{e}")
                        articleparam["articleid"] = articleid
                        articleparam["articletype"] = channelcolumtype
                        articleparam["articletitle"] = articletitle
                        articleparam["imageurl"] = imageurl
                        articleparam["channelname"] = channelname
                        articleparam["commentnum"] = commentnum
                        articleparam["pubtime"] = pubtime
                        articleparam["author"] = author
                        articleparam["channelindexid"] = channel_index_id
                        articlesparams.append(articleparam)
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        url = "http://111.203.147.58/v4/i/statuses/detail.json"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '6',
            'Host': '111.203.147.58',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.8.0',
        }
        for article in articles:
            articleid = article.get("articleid")
            articletype = article.get("articletype")
            imgurl = article.get("imageurl")
            channelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            commentnum = article.get("commentnum")
            pubtime = article.get("pubtime")
            source = article.get("source")
            author = article.get("author")
            data = "devicetype={}&itemid={}".format(articletype, articleid)
            method = 'post'
            articleparam = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                             pubtime=pubtime, source=source, author=author,
                                                             commentnum=commentnum,channel_index_id=channel_index_id)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            channelname = article.get("channelname")
            pubtime = article.get("pubtime")
            appname = article.get("appname")
            source = article.get("source")
            commentnum = article.get("commentnum")
            author = article.get("author")
            channel_index_id = article.get("channelindexid")
            try:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                fields = InitClass().article_fields()
                fields["channelname"] = channelname
                fields["appname"] = appname
                fields["platformID"] = self.platform_id
                fields["channelindexid"] = channel_index_id
                fields["title"] = content_s[0]["title"]
                fields["content"] = content_s[0]["content"]
                if "cover" in content_s[0] and content_s[0]["cover"]:
                    fields["articlecovers"] = [content_s[0]["cover"]]
                fields["url"] = content_s[0]["share_url"]
                fields["workerid"] = content_s[0]["item_id"]
                # 如果有视频采集视频信息
                imagesss = content_s[0]["image_list"]
                if imagesss:
                    images = list()
                    for image in imagesss:
                        images.append(image["url"])
                    fields["images"] = images
                try:
                    videos = content_s[0]["video"]
                    fields["videos"] = [videos]
                except Exception as e:
                    logging.info(f"此新闻无视频{e}")
                fields["source"] = source
                fields["pubtime"] = pubtime
                fields["commentnum"] = commentnum
                fields["author"] = author
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                num += 1
                logging.info(f"错误数量{num},{e}")


def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = JieFangJunBao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
    appspider = JieFangJunBao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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


if __name__ == '__main__':
    appspider = JieFangJunBao("解放军报")
    appspider.run()
