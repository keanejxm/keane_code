"""
解析模板，对app爬虫爬出的页面解析
河南日报app模板
author:keane
data:2020/10/28
https://api.henandaily.cn/v2/content/getcategorylist?cat_id=content_21&device_type=android&number=10&offset=0&user_i
d=0&token=8de8af6f01e8a9b8b2a649a9
"""
import json
# import time
# import hashlib
import logging

from spiders.libs.spiders.app.initclass import InitClass
from spiders.libs.spiders.app.appspider_m import Appspider


class Heinanribao(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://api.henandaily.cn/v2/content/gettopcategory?"
        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': 'api.henandaily.cn'
        }
        data = {
            'device_type': 'android',
            'user_id': '0',
            'token': '8de8af6f01e8a9b8b2a649a9'
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        print(channelsres)
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))
        for channel in channelslists['Info']:
            channelname = channel['catname']
            channelid = channel['cat_id']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    def getarticlelistparams(self, channelsparams):
        articlelistsparams = []
        channel_data = list()
        url = 'https://api.henandaily.cn/v2/content/getcategorylist?'
        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': 'api.henandaily.cn'
        }
        channel_num = 0
        for channelparam in channelsparams:
            channel_num += 1
            data = {
                'cat_id': channelparam.get("channelid"),
                'device_type': 'android',
                'number': '10',
                'offset': '0',
                'user_id': '0',
                'token': '8de8af6f01e8a9b8b2a649a9',
            }
            method = 'get'
            channelname = channelparam.get("channelname")
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
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channel_index_id = articleslistres.get("channelindexid")
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
            except Exception as e:
                logging.info(f"解析文章列表失败{e}")
            articleslist = articleslists['Info']
            for article in articleslist:
                articleparam = InitClass().article_list_fields()
                try:
                    articleid = article['content_id']
                except Exception as e:
                    logging.info(f"没有获取到文章id{e}")
                    articleid = article['special_id']
                articletitle = article['title']
                try:
                    imageurl = article['thumb']
                    articleparam["imageurl"] = imageurl
                except Exception as e:
                    logging.info(f"没有获取到文章封面图片{e}")
                createtime = article["created"]
                try:
                    updatetime = article["updated"]
                    articleparam["updatetime"] = updatetime
                except Exception as e:
                    logging.info(f"没有获取到更新时间{e}")
                try:
                    commentnum = article["comment"]
                    articleparam["commentnum"] = commentnum
                except Exception as e:
                    logging.info(f"没有获取到新闻评论数{e}")
                articleparam["createtime"] = createtime
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
            createtime = article.get("createtime")
            updatetime = article.get("updatetime")
            url = 'https://api.henandaily.cn/v2/content/getnewsbyid?'
            headers = {
                'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
                'Host': 'api.henandaily.cn'
            }
            data = {
                'content_id': article.get("articleid"),
                'device_type': 'android',
                'user_id': '0',
                'token': '8de8af6f01e8a9b8b2a649a9',
                'onlymarker': 'OL572u8v5',
            }
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                             updatetime=updatetime, createtime=createtime,
                                                             channel_index_id=channel_index_id)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        for article in articleres:
            fields = InitClass().article_fields()
            channnelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            imgurl = article.get("imageurl")
            appname = article.get("appname")
            updatetime = article.get("updatetime")
            createtime = article.get("createtime")
            articlejson = json.loads(
                json.dumps(json.loads(article.get("articleres")), indent=4, ensure_ascii=False))
            try:
                articlec = articlejson['Info']
                try:
                    title = articlec['title']
                    fields["title"] = title
                except Exception as e:
                    logging.info(f"没有获取到标题信息{e}")
                try:
                    pubtime = articlec['inputtime']
                    fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                except Exception as e:
                    logging.info(f"没有获取到发布时间{e}")
                try:
                    source = articlec['copyfrom']
                    fields["source"] = source
                except Exception as e:
                    logging.info(f"没有获取到来源信息{e}")
                try:
                    content = articlec['content']
                    fields["content"] = content
                except Exception as e:
                    logging.info(f"没有获取到内容信息{e}")
                try:
                    commentnum = articlec['comment']
                    fields["commentnum"] = commentnum
                except Exception as e:
                    logging.info(f"没有获取到评论数信息{e}")
                try:
                    author = articlec['editor']
                    fields["author"] = author
                except Exception as e:
                    logging.info(f"没有获取到作者信息{e}")
                url = articlec["url"]
                workerid = articlec["content_id"]
                videos = articlec["myvideo"]
                fields["channelname"] = channnelname
                fields["channelindexid"] = channel_index_id
                fields["platformID"] = self.platform_id
                fields["articlecovers"] = imgurl
                fields["appname"] = appname
                fields["platformID"] = self.platform_id
                fields["url"] = url
                fields["workerid"] = workerid
                fields["videos"] = videos
                fields["updatetime"] = int(updatetime) * 1000
                if createtime:
                    fields["createtime"] = int(createtime) * 1000
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                logging.info(f"获取文章信息失败{e}")


def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = Heinanribao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    appparams = appspider.get_app_params()
    channelsres = appspider.getchannel(appparams.__next__())
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
    appspider = Heinanribao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
