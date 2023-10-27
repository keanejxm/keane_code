"""
解析模板，对app爬虫爬出的页面解析
山西日报app模板
author:keane
data:2020/10/28
"""
import json
# import time
# import hashlib
import logging

from spiders.libs.spiders.app.initclass import InitClass
from spiders.libs.spiders.app.appspider_m import Appspider


class Shanxiribao(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://sxapi.sxrbw.com/api/v2/menus/?"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/'
                          '537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.92 Mobile Safari/537.3'
                          '6',
            'Host': 'sxapi.sxrbw.com'
        }
        data = {
            'clientVersionCode': '61',
            'pjCode': 'code_sxrb',
            'device_size': '1080.0x2200.0',
            'deviceOs': '10',
            'channel': 'huawei',
            'deviceModel': 'OPPO-PACM00',
            'clientVersion': '4.4.6',
            'udid': 'e0f96ff828fd0219',
            'platform': 'android'
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(channelsres)
        for channels in channelslists['items']:
            channelid = channels['categoryId']
            channelname = channels['name']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    def getarticlelistparams(self,channelsparams):
        print(channelsparams)
        articlelistsparams = []
        channel_data = list()
        channel_num = 0
        headers = {
            'User-Agent': 'Maa-Proxymaa-http-ok',
            'Host': 'sxapi.sxrbw.com',
        }
        data = {
            'pageToken': '',
            'size': '20',
            'clientVersionCode': '61',
            'pjCode': 'code_sxrb',
            'device_size': '1080.0x2200.0',
            'deviceOs': '10',
            'channel': 'huawei',
            'deviceModel': 'OPPO-PACM00',
            'clientVersion': '4.4.6',
            'udid': 'e0f96ff828fd0219',
            'platform': 'android'
        }
        for channelparam in channelsparams:
            channel_num += 1
            url = 'http://sxapi.sxrbw.com/api/v2/articles/' + str(channelparam.get("channelid")) + '?'
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
            try:
                articleshead = articleslists['item']['head']
            except Exception as e:
                logging.info(f"此频道无头部信息{e}")
                articleshead = []
            try:
                articleslist = articleslists['item']['list']
            except Exception as e:
                logging.info(f"收集频道信息失败{e}")
                articleslist = []
            articleslist = articleshead + articleslist
            for article in articleslist:
                articleparam = InitClass().article_list_fields()
                articleid = article['articleId']
                articletitle = article['title']
                try:
                    imageurl = article['imageUrl']
                    articleparam["imageurl"] = imageurl
                except Exception as e:
                    logging.info(f"没有获取到文章封面{e}")
                try:
                    videourl = article['medias'][0]["resources"][0]["url"]
                    articleparam["videourl"] = videourl
                except Exception as e:
                    logging.info(f"没有获取到文章封面{e}")
                articleparam["articleid"] = articleid
                articleparam["articletitle"] = articletitle
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
            videourl = article.get("videourl")
            url = 'http://sxapi.sxrbw.com/api/v2/articles/detail/' + str(article.get("articleid"))
            headers = {
                'Host': 'sxapi.sxrbw.com',
                'Connection': 'keep-alive',
                'Origin': 'http://sxshare.sxrbw.com',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (K'
                              'HTML, like Gecko) Version/4.0 Chrome/77.0.3865.92 Mobile Safari/537.36;sxrbdaily_android'
            }
            data = {}
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data = data,
                                                             videourl = videourl,channel_index_id=channel_index_id)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self,articleres):
        for article in articleres:
            channnelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            imgurl = article.get("imageurl")
            videourl = article.get("videourl")
            appname = article.get("appname")
            articlejson = json.loads(article.get("articleres"))
            fields = InitClass().article_fields()
            fields["channelname"] = channnelname
            fields["channelindexid"] = channel_index_id
            fields["articlecovers"] = imgurl
            fields["appname"] = appname
            fields["platformID"] = self.platform_id
            try:
                articlec = articlejson['item']
                try:
                    workerid = articlec["articleId"]
                    fields["workerid"] = workerid
                except Exception:
                    logging.info("没有获取到文章id")
                try:
                    url = articlec["shareUrl"]
                    fields["url"] = url
                except Exception:
                    logging.info("没有获取到文章url")
                try:
                    title = articlec['title']
                    fields["title"] = title
                except Exception as e:
                    logging.info(f"没有获取到标题{e}")
                try:
                    pubtime = articlec['date']
                    fields["pubtime"] = InitClass().date_time_stamp(InitClass().format_date(pubtime))
                except Exception as e:
                    logging.info(f"没有获取到文章发布时间{e}")
                try:
                    source = articlec['source']
                    fields["source"] = source
                except Exception as e:
                    logging.info(f"没有获取到文章来源{e}")
                try:
                    content = articlec['content']
                    fields["content"] = content
                except Exception as e:
                    logging.info(f"没有获取到文章内容{e}")
                try:
                    commentnum = articlec['comments']
                    fields["commentnum"] = commentnum
                except Exception as e:
                    logging.info(f"没有获取到文章评论数{e}")
                try:
                    likenum = articlec['likes']
                    fields["likenum"] = likenum
                except Exception as e:
                    logging.info(f"没有获取到文章点赞数{e}")
                try:
                    images = articlec['images']
                    fields["images"] = images
                except Exception as e:
                    logging.info(f"没有获取到文章图片{e}")
                if videourl:
                    videos = list()
                    videos.append(videourl)
                    fields["videos"] = videos
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                logging.info(f"{e}")

def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = Shanxiribao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
    appspider = Shanxiribao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
