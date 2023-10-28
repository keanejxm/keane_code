"""
解析模板，对app爬虫爬出的页面解析
中国青年报app模板
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


class Zhongguoqingnian(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://i.cyol.com/peony/v1/group?"
        headers = {
            'cache': '2000',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBpZCI6MSwiZGV2aWNlX2lkIj'
                             'oiMWI3NTNmNmItODc0NS0zNDg2LWEwYzAtNWM3N2RlZGQ1NmQzIiwiZXhwIjoxNjExOTczODY0'
                             'LCJpc3MiOiI5cDZ5anVvYVZ4bjBWd3dtU3R0SWNtM1hKd21jZlJDayIsInBsYXRmb3JtIjoibW'
                             '9iaWxlIiwic2l0ZSI6MCwidWlkIjoiYW5vbnltb3VzIn0.ZbNNXxLCwrl8OBFNZD1a6-xfH6zO'
                             'U3a0gOzL-nwsr10',
            'X-Request-Id': '1b753f6b-8745-3486-a0c0-5c77dedd56d3',
            'Content-Type': 'application/json',
            'X-Platform': 'android',
            'X-Version': '4.3.3',
            'X-Brand': 'Android MuMu',
            'Host': 'i.cyol.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.11.0',
            'If-Modified-Since': 'Fri, 30 Oct 2020 02:34:26 GMT'
        }
        data = {
            'module_name': 'home',
            'type': 'nav',
            'channel': '28Dga1xp'
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(channelsres)
        for channels in channelslists['data']['groups']:
            channelid = channels['id']
            channelname = channels['name']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    def getarticlelistparams(self, channelsparams):
        articlelistsparams = []
        channel_data = list()
        channel_num = 0
        headers = {
            'cache': '2000',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBpZCI6MSwiZGV2aWNlX2lkIjoiMWI3NTNmNmIt'
                             'ODc0NS0zNDg2LWEwYzAtNWM3N2RlZGQ1NmQzIiwiZXhwIjoxNjExOTczODY0LCJpc3MiOiI5cDZ5anVvYVZ4bjBW'
                             'd3dtU3R0SWNtM1hKd21jZlJDayIsInBsYXRmb3JtIjoibW9iaWxlIiwic2l0ZSI6MCwidWlkIjoiYW5vbnltb3VzI'
                             'n0.ZbNNXxLCwrl8OBFNZD1a6-xfH6zOU3a0gOzL-nwsr10',
            'X-Request-Id': '1b753f6b-8745-3486-a0c0-5c77dedd56d3',
            'Content-Type': 'application/json',
            'X-Platform': 'android',
            'X-Version': '4.3.3',
            'X-Brand': 'Android MuMu',
            'Host': 'i.cyol.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.11.0',
            'If-Modified-Since': 'Fri, 30 Oct 2020 02:34:26 GMT'
        }
        for channelparam in channelsparams:
            channel_num += 1
            url = 'https://i.cyol.com/peony/v1/content?'
            data = {
                'group_type': 'cascade',
                'gid': channelparam.get("channelid"),
                'pageindex': '1',
                'payload': 'default',
                'group_name': 'home',
                'pagesize': '15',
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
                a = articleslists['data']['banners']['posts']
                b = articleslists['data']['tops']
                c = articleslists['data']['posts']
                if not a:
                    a = []
                if not b:
                    b = []
                if not c:
                    c = []
                articleslist = a + b + c
                for article in articleslist:
                    articleparam = InitClass().article_list_fields()
                    try:
                        for artic in article["extra"]["posts"]:
                            articleid = artic['post_id']
                            articletitle = artic['title']
                            try:
                                imageurl = artic['style']['data'][0]["thumb"]
                                articleparam["imageurl"] = imageurl
                            except Exception as e:
                                print(e)
                            try:
                                videos = list()
                                video = artic["payload"]["url"]
                                videocover = artic["payload"]["thumb"]
                                videos.append(video)
                                articleparam["videos"] = videos
                                articleparam["videocover"] = videocover
                            except Exception as e:
                                logging.info(f"此文章没有视频{e}")
                            articleparam["articleid"] = articleid
                            articleparam["articletitle"] = articletitle
                            articleparam["channelname"] = channelname
                            articleparam["channelindexid"] = channel_index_id
                            articlesparams.append(articleparam)
                    except Exception as e:
                        logging.info(f"此文章不是专题{e}")

                    articleid = article['post_id']
                    articletitle = article['title']
                    try:
                        imageurl = article['style']['data'][0]["thumb"]
                        articleparam["imageurl"] = imageurl
                    except Exception as e:
                        print(e)
                    try:
                        videos = list()
                        video = article["payload"]["url"]
                        videocover = article["payload"]["thumb"]
                        videos.append(video)
                        articleparam["videos"] = videos
                        articleparam["videocover"] = videocover
                    except Exception as e:
                        logging.info(f"此文章没有视频{e}")
                    articleparam["articleid"] = articleid
                    articleparam["articletitle"] = articletitle
                    articleparam["channelname"] = channelname
                    articleparam["channelindexid"] = channel_index_id
                    articlesparams.append(articleparam)
            except Exception as e:
                print(e)
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        for article in articles:
            imgurl = article.get("imageurl")
            channelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            videos = article.get("videos")
            videocover = article.get("videocover")
            try:
                url = 'https://i.cyol.com/peony/v1/content/' + article.get("articleid") + '?less=false&p_type=0'
                headers = {
                    'cache': '2000',
                    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBpZCI6MSwiZGV2aWNlX2lkIjoiMWI3'
                                     'NTNmNmItODc0NS0zNDg2LWEwYzAtNWM3N2RlZGQ1NmQzIiwiZXhwIjoxNjExOTczODY0LCJpc3MiOiI5'
                                     'cDZ5anVvYVZ4bjBWd3dtU3R0SWNtM1hKd21jZlJDayIsInBsYXRmb3JtIjoibW9iaWxlIiwic2l0ZSI6'
                                     'MCwidWlkIjoiYW5vbnltb3VzIn0.ZbNNXxLCwrl8OBFNZD1a6-xfH6zOU3a0gOzL-nwsr10',
                    'X-Request-Id': '1b753f6b-8745-3486-a0c0-5c77dedd56d3',
                    'Content-Type': 'application/json',
                    'X-Platform': 'android',
                    'X-Version': '4.3.3',
                    'X-Brand': 'Android MuMu',
                    'Host': 'i.cyol.com',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                    'User-Agent': 'okhttp/3.11.0',
                    'If-Modified-Since': 'Fri, 30 Oct 2020 02:34:26 GMT'
                }
                data = {}
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                                 videourl=videos, videocover=videocover,
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
            videos = article.get("videourl")
            videocover = article.get("videocover")
            try:
                articlejson = json.loads(article.get("articleres"))
                articlejson = articlejson['data']
                fields = InitClass().article_fields()
                fields["channelname"] = channnelname
                fields["channelindexid"] = channel_index_id
                fields["articlecovers"] = [imgurl]
                fields["appname"] = appname
                fields["platformID"] = self.platform_id
                fields["videos"] = [videos]
                fields["videocover"] = [videocover]
                try:
                    title = articlejson['title']
                    fields["title"] = title
                except Exception as e:
                    print(e)
                try:
                    pubtime = articlejson['publish_at']
                    fields["pubtime"] = int(pubtime) * 1000
                except Exception as e:
                    print(e)
                try:
                    source = articlejson['source_alias']
                    fields["source"] = source
                except Exception as e:
                    print(e)
                try:
                    content = articlejson['content']
                    fields["content"] = content
                except Exception as e:
                    print(e)
                try:
                    commentnum = articlejson['comment_count']
                    fields["commentnum"] = commentnum
                except Exception as e:
                    print(e)
                c_images = articlejson["style"]["data"]
                if c_images:
                    images = list()
                    for image in c_images:
                        images.append(image["thumb"])
                    fields["images"] = images
                url = articlejson["share_link"]
                fields["url"] = url
                workerid = articlejson['post_id']
                fields["workerid"] = workerid
                author = articlejson["author"]
                fields["author"] = author
                readnum = articlejson["read_count"]
                likenum = articlejson["like_count"]
                fields["readnum"] = readnum
                fields["likenum"] = likenum
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)


def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = Zhongguoqingnian(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
    appspider = Zhongguoqingnian(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
