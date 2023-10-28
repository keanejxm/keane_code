#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
光明日报解析模板
# author: Keane
# create date: 2020/11/27
# update date: 2020/11/27
# appversion: 
"""
import json
import logging

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class GuangMingRiBao(Appspider):
    logging.basicConfig(level=logging.INFO)

    @staticmethod
    def get_app_params():
        url = "https://api.gmdaily.cn/api/channel/list"
        headers = {
            'token': '',
            'deviceId': '537cc19f4771bd98f67b56520e33e651',
            'UA': 'Android+Android+9.0.5+CloudTibet',
            'Content-Type': 'application/json; charset=utf-8',
            'Content-Length': '2',
            'Host': 'api.gmdaily.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.14.0',

        }
        data = {}
        method = "post"
        appjson = ''
        app_params = InitClass().app_params(url, headers, method, data=data, appjson=appjson)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))
        for channel in channelslists["data"]["myChannels"]:
            channelid = channel['channelId']
            channelname = channel['name']
            channelcolumtype = channel['type']
            channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channelcolumtype)
            channelsparams.append(channelparam)
        yield channelsparams

    def getarticlelistparams(self, channelsparams):
        articlelistsparams = []
        channel_data = list()
        channel_num = 0
        url = "https://api.gmdaily.cn/api/content/home"
        headers = {
            'token': '',
            'deviceId': '537cc19f4771bd98f67b56520e33e651',
            'UA': 'Android+Android+9.0.5+CloudTibet',
            'Content-Type': 'application/json; charset=utf-8',
            'Content-Length': '2',
            'Host': 'api.gmdaily.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.14.0',

        }
        method = 'post'
        for channel in channelsparams:
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channelcolumtype = channel.get("channeltype")
            data = '{"channelId":"' + channelid + '","firstId":"378057"}'
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
                for articles in articleslists["data"]["banners"] + articleslists["data"]["records"]:
                    print(articles)
                    articleparam = InitClass().article_list_fields()
                    articleid = articles['contentId']
                    try:
                        articletitle = articles["contentVo"]['title']
                    except KeyError:
                        articletitle = articles["title"]
                    articleparam["articletitle"] = articletitle
                    try:
                        try:
                            imageurl = articles['imageUrl']
                        except KeyError:
                            imageurl = articles["abridgePictures"]["url"]
                        articleparam["imageurl"] = imageurl
                    except Exception as e:
                        logging.info(f"列表页无封面信息{e}")
                    try:
                        try:
                            source = articles["contentVo"]["source"]
                        except KeyError:
                            source = articles["source"]
                        articleparam["source"] = source
                    except Exception as e:
                        logging.info(f"列表页无新闻来源信息{e}")
                    try:
                        author = articles["contentVo"]['author']
                        articleparam["author"] = author
                    except Exception as e:
                        logging.info(f"列表页无作者信息{e}")
                    try:
                        try:
                            pubtime = articles["contentVo"]['publishDt']
                        except KeyError:
                            pubtime = articles["publishDt"]
                        articleparam["pubtime"] = pubtime
                    except Exception as e:
                        logging.info(f"列表页无发布时间信息{e}")
                    articleparam["articleid"] = articleid
                    articleparam["articletype"] = channelcolumtype
                    articleparam["channelname"] = channelname
                    articleparam["channelindexid"] = channel_index_id
                    articlesparams.append(articleparam)
            except Exception as e:
                logging.info(f"提取文章列表信息失败{e}")
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        url = "https://api.gmdaily.cn/api/content/detail"
        headers = {
            'token': '',
            'deviceId': '537cc19f4771bd98f67b56520e33e651',
            'UA': 'Android+Android+9.0.5+CloudTibet',
            'Content-Type': 'application/json; charset=utf-8',
            'Content-Length': '2',
            'Host': 'api.gmdaily.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.14.0',

        }
        for article in articles:
            articleid = article.get("articleid")
            imgurl = article.get("imageurl")
            channelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            source = article.get("source")
            author = article.get("author")
            pubtime = article.get("pubtime")
            createtime = article.get("createtime")
            updatetime = article.get("updatetime")
            likenum = article.get("likenum")
            commentnum = article.get("commentnum")
            data = dict()
            data["contentId"] = articleid
            method = 'post'
            articleparam = InitClass().article_params_fields(url, headers, method, channelname, imgurl,
                                                             articlejson=data, channel_index_id=channel_index_id,
                                                             pubtime=pubtime, createtime=createtime,
                                                             updatetime=updatetime, source=source, author=author,
                                                             likenum=likenum, commentnum=commentnum)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            channelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            imageurl = article.get("imageurl")
            pubtime = article.get("pubtime")
            appname = article.get("appname")
            source = article.get("source")
            commentnum = article.get("commentnum")
            author = article.get("author")
            try:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                print(content_s)
                fields = InitClass().article_fields()
                fields["channelname"] = channelname
                fields["appname"] = appname
                fields["platformID"] = self.platform_id
                fields["channelindexid"] = channel_index_id
                fields["title"] = content_s["data"]["title"]
                fields["workerid"] = content_s["data"]["contentId"]
                fields["content"] = content_s["data"]["contentTxt"]
                fields["articlecovers"] = [imageurl]
                fields["url"] = content_s["data"]["shareUrl"]
                imagess = content_s["data"]["pictures"]
                if imagess:
                    images = list()
                    for image in imagess:
                        images.append(image["url"])
                    fields["images"] = images
                # 如果有视频采集视频信息
                try:
                    videoss = content_s["data"]["videos"]
                    videos = list()
                    videocovers = list()
                    if videoss:
                        for video in videoss:
                            videos.append(video["url"])
                            videos.append(video["cover"])
                    fields["videocover"] = videocovers
                    fields["videos"] = videos
                except Exception as e:
                    logging.info(f"此新闻无视频{e}")
                fields["source"] = source
                fields["pubtime"] = pubtime
                fields["updatetime"] = content_s["data"]["updtDt"]
                fields["commentnum"] = commentnum
                fields["author"] = author
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                num += 1
                logging.info(f"错误数量{num},{e}")


def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = GuangMingRiBao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
        print(data)
        yield data

# if __name__ == '__main__':
#     appspider = GuangMingRiBao("光明日报")
#     appspider.run()
