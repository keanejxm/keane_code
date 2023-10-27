"""
解析模板，对app爬虫爬出的页面解析
国务院app模板
author:keane
data:2020/10/29
"""
import json
# import re
# import time
# import hashlib
import logging

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class Guowuyuan(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://app.www.gov.cn/govdata/gov/source.json"
        headers = {
            'User-Agent': 'okhttp/3.14.1 GovCnAndroid/4.1.0 (yingyongbao; 24)',
            'Cache-Control': 'no-store',
            'Host': 'app.www.gov.cn'
        }
        data = {}
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))
        for key in channelslists['columns'].keys():
            channels = channelslists['columns'][key]
            channelid = channels['columnId']
            channelname = channels['title']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    def getarticlelistparams(self, channelsparams):
        articlelistsparams = []
        channel_data = list()
        headers = {
            'User-Agent': 'okhttp/3.14.1 GovCnAndroid/4.1.0 (yingyongbao; 24)',
            'Cache-Control': 'no-store',
            'Host': 'app.www.gov.cn'
        }
        channel_num = 0
        for channelparam in channelsparams:
            channel_num += 1
            url = 'https://app.www.gov.cn/govdata/gov/columns/column_' + str(channelparam.get("channelid")) + '_0.json'
            data = {
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
            articleslists = articleslistres.get("channelres")
            channel_index_id = articleslistres.get("channelindexid")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists)))
            except Exception as e:
                logging.info(f"解析文章列表失败{e}")
            articles = articleslists['articles']
            for key in articles.keys():
                articleparam = InitClass().article_list_fields()
                article = articles[key]
                articleid = article['path']
                articletitle = article['title']
                articleparam["articleid"] = articleid
                articleparam["articletitle"] = articletitle
                articleparam["channelname"] = channelname
                articleparam["channelindexid"] = channel_index_id
                try:
                    try:
                        imageurl = article['imgUrl']
                    except Exception as e:
                        logging.info(f"获取封面图片{e}")
                        imageurl = article['thumbnails']["1"]['file']
                    articleparam["imageurl"] = imageurl
                except Exception as e:
                    logging.info(f"获取文章封面图片失败{e}")
                pubtime = article["publishTime"]
                updatetime = article["updateTime"]
                try:
                    source = article["source"]
                    articleparam["source"] = source
                except Exception as e:
                    logging.info(f"没有获取到文章来源{e}")
                try:
                    author = article["author"]
                    articleparam["author"] = author
                except Exception as e:
                    logging.info(f"没有获取到文章作者{e}")
                articleparam["pubtime"] = pubtime
                articleparam["updatetime"] = updatetime
                articlesparams.append(articleparam)
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        for article in articles:
            imgurl = article.get("imageurl")
            channelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            pubtime = article.get("pubtime")
            updatetime = article.get("updatetime")
            source = article.get("source")
            author = article.get("author")
            try:
                url = 'https://app.www.gov.cn/govdata/gov/' + article.get("articleid")
                headers = {
                    'User-Agent': 'okhttp/3.14.1 GovCnAndroid/4.1.0 (yingyongbao; 24)',
                    'Cache-Control': 'no-store',
                    'Host': 'app.www.gov.cn'

                }
                data = {
                }
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                                 pubtime=pubtime, updatetime=updatetime,
                                                                 source=source, author=author,
                                                                 channel_index_id=channel_index_id)
                articleparams.append(articleparam)
            except Exception as e:
                logging.info(f"{e}")
        yield articleparams

    def analyzearticle(self, articleres):
        for article in articleres:
            fields = InitClass().article_fields()
            appname = article.get("appname")
            channnelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            imgurl = 'https://app.www.gov.cn/govdata/gov/' + article.get("imageurl")
            updatetime = article.get("updatetime")
            fields["updatetime"] = int(updatetime) * 1000
            fields["appname"] = appname
            try:
                articlejson = json.loads(
                    json.dumps(json.loads(article.get("articleres")), indent=4, ensure_ascii=False))
                # print(json.dumps(articlejson,indent=4,ensure_ascii=False))

                # return 'ss'
                try:
                    title = articlejson['title']
                    fields["title"] = title
                except Exception as e:
                    logging.info(f"获取文章标题失败{e}")
                try:
                    url = articlejson["shareUrl"]
                    fields["url"] = url
                except Exception as e:
                    logging.info(f"没有获取到地址{e}")
                try:
                    pubtime = articlejson['publishTime']
                    fields["pubtime"] = int(pubtime) * 1000
                    # timearray = time.localtime(pubtime)
                    # pubtime = time.strftime("%Y-%m-%d %H:%M:%S", timearray)
                except Exception as e:
                    logging.info(f"获取发布时间失败{e}")
                try:
                    source = articlejson['source']
                    fields["source"] = source
                except Exception as e:
                    logging.info(f"获取文章来源失败{e}")
                try:
                    content = articlejson['content']
                    fields["content"] = content
                except Exception as e:
                    logging.info(f"获取文章内容失败{e}")
                try:
                    commentnum = articlejson['commentCount']
                    fields["commentnum"] = commentnum
                except Exception as e:
                    logging.info(f"获取文章评论数失败{e}")
                try:
                    author = articlejson['author']
                    fields["author"] = author
                except Exception as e:
                    logging.info(f"获取文章作者信息失败{e}")
                fields["channelname"] = channnelname
                fields["platformID"] = self.platform_id
                fields["channelindexid"] = channel_index_id
                fields["articlecovers"] = [imgurl]
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)


def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = Guowuyuan(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
    appspider = Guowuyuan(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
