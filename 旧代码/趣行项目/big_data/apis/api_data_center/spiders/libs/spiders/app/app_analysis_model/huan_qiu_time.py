"""
解析模板，对app爬虫爬出的页面解析
环球timeapp模板
author:keane
data:2020/11/3
"""
import json
import re
import logging
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


# 问题：海外看中国频道和环球时报没有采集到


# from lib.crawler.spiders.app.akafkaproduert import KafkaProducer


class Huanqiutime(Appspider):
    logging.basicConfig(level=logging.INFO)

    @staticmethod
    def get_app_params():
        url = "https://api.hqtime.huanqiu.com/api/news/category"
        headers = {
            'accept': 'application/vnd.hq_time.v2+json',
            'content-type': 'application/json',
            'user-agent': '(Linux; Android 6.0.1; Build/Android MuMu) huanqiuTIME/9.11.3',
            'clientversion': 'Android/v9.11.3',
            'x-timestamp': '1604394657',
            'x-nonce': '38w9li1b',
            'x-sign': 'cee88dc08c9e0789542a93a3670b84f64970f17dbf17b483c88df57f6cdc43e6',
            'Host': 'api.hqtime.huanqiu.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'If-Modified-Since': 'Mon, 02 Nov 2020 09:27:38 GMT'
        }
        data = {}
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))
        for channels in channelslists['data']:
            channelid = channels['news_link']
            channelname = channels['name']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    def getarticlelistparams(self, channelsparams):
        articlelistsparams = list()
        channel_data = list()
        headers = {
            'accept': 'application/vnd.hq_time.v2+json',
            'content-type': 'application/json',
            'user-agent': '(Linux; Android 6.0.1; Build/Android MuMu) huanqiuTIME/9.11.3',
            'clientversion': 'Android/v9.11.3',
            'x-timestamp': '1604396245',
            'x-nonce': '96n1nmkq',
            'x-sign': '6d7c4fa35d6e441b2dba210c52b2d50d1c2c33fe680c438786a7ef429ef8bd7d',
            'Host': 'api.hqtime.huanqiu.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'If-Modified-Since': 'Tue, 03 Nov 2020 09:11:47 GMT',
        }
        method = 'get'
        channel_num = 0
        for channel in channelsparams:
            channel_num += 1
            url = channel.get("channelid")
            data = dict()
            channelname = channel.get("channelname")
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
                logging.info(f"解析文章列表{e}")
            try:
                for articles in articleslists['data']:
                    for article in articles['group_data']:
                        articleparam = InitClass().article_list_fields()
                        article = article
                        articleid = article['id']
                        articletitle = article['title']
                        imageurl = article['thumb']
                        articleurl = article['url']
                        pubtime = article["time_publish"]
                        likenum = article["like_amount"]
                        try:
                            commentnum = article["comment_count"]
                            articleparam["commentnum"] = commentnum
                        except Exception as e:
                            logging.info(f"此文章无评论数{e}")
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["imageurl"] = imageurl
                        articleparam["channelname"] = channelname
                        articleparam["channelindexid"] = channel_index_id
                        articleparam["articleurl"] = articleurl
                        articleparam["pubtime"] = pubtime
                        articleparam["likenum"] = likenum
                        articlesparams.append(articleparam)
            except Exception as e:
                logging.info(f"解析文章表{e}")
                for article in articleslists['data']['chinese']:
                    print(article)
                    articleparam = InitClass().article_list_fields()
                    article = article
                    try:
                        try:
                            articleid = article['id']
                        except Exception as e:
                            logging.info(f"id字段不存在{e},获取aid字段")
                            articleid = article['aid']
                    except Exception as e:
                        logging.info(f"获取id失败{e}")
                        articleid = ""
                    articletitle = article['title']
                    try:
                        imageurl = article['thumb']
                    except Exception as e:
                        logging.info(f"获取封面图片失败{e}")
                        imageurl = ''
                    articleurl = article['url']
                    articleparam["articleid"] = articleid
                    articleparam["articletitle"] = articletitle
                    articleparam["imageurl"] = imageurl
                    articleparam["channelname"] = channelname
                    articleparam["channelindexid"] = channel_index_id
                    articleparam["articleurl"] = articleurl
                    articlesparams.append(articleparam)
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        headers = {
            'Cookie': 'UM_distinctid=17569c917a45d8-09dc7604425e5d-3323767-1fa400-17569c917a5473; Hm_lvt_1fc983b4c305d'
                      '209e7e05d96e713939f=1603797588,1603869823',
            'Host': 'hqtime.huanqiu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84'
                          '.0.4147.125 Safari/537.36'
        }
        for article in articles:
            url = article.get("articleurl")
            imgurl = article.get("imageurl")
            channelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            pubtime = article.get("pubtime")
            likenum = article.get("likenum")
            commentnum = article.get("commentnum")
            try:
                data = dict()
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                                 pubtime=pubtime, likenum=likenum,
                                                                 commentnum=commentnum,
                                                                 channel_index_id=channel_index_id)
                articleparams.append(articleparam)
            except Exception as e:
                logging.info(f"生成文章信息失败{e}")
        yield articleparams

    def analyzearticle(self,articleres):
        num = 0
        for article in articleres:
            channelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            imgurl = article.get("imageurl")
            appname = article.get("appname")
            pubtime = article.get("pubtime")
            likenum = article.get("likenum")
            commentnum = article.get("commentnum")
            article_s = re.findall('var article = JSON.parse(.*);', article.get("articleres"))
            if article_s:
                content_s = article_s[0][1:-1]
                content_s.replace("'", '"')
                try:
                    content_s = json.loads(content_s, strict=False)
                    content_s = json.loads(content_s)
                    content_s = json.dumps(content_s, indent=4, ensure_ascii=False)
                    content_s = json.loads(content_s)
                    fields = InitClass().article_fields()
                    fields["channelname"] = channelname
                    fields["platformID"] = self.platform_id
                    fields["channelindexid"] = channel_index_id
                    fields["appname"] = appname
                    fields["title"] = content_s["title"]
                    fields["workerid"] = content_s["aid"]
                    fields["content"] = content_s["content"]
                    fields["articlecovers"] = [imgurl]
                    fields["images"] = [content_s["cover"]]  # 如果有视频采集视频信息
                    if content_s["typedata"]["video"]["members"]:
                        videos = []
                        videocover = []
                        width = []
                        height = []
                        for i in content_s["typedata"]["video"]["members"]:
                            videos.append(i["url"])
                            videocover.append(i["cover"])
                            width.append(i["width"])
                            height.append(i["height"])
                        fields["videos"] = videos
                        fields["videocover"] = videocover
                        fields["width"] = width
                        fields["height"] = height
                    fields["source"] = content_s["source"]["name"]
                    fields["url"] = content_s["source"]["url"]
                    fields["pubtime"] = int(pubtime) * 1000
                    fields["createtime"] = content_s["ctime"]
                    fields["updatetime"] = content_s["utime"]
                    fields["commentnum"] = commentnum
                    fields["likenum"] = likenum
                    fields["author"] = content_s["author"]
                    fields = InitClass().wash_article_data(fields)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
                except Exception as e:
                    num += 1
                    logging.info(f"错误数量{num},{e},{content_s}")


def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = Huanqiutime(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
    appspider = Huanqiutime(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
