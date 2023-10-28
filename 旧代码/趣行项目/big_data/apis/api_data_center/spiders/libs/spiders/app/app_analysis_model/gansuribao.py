# -*- encoding:utf-8 -*-
"""
@功能:甘肃日报模板
@AUTHOR：Keane
@文件名：gansuribao.py
@时间：2020/12/30  14:50
"""
import json
import logging
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class GanSuRiBao(Appspider):

    @staticmethod
    def get_app_params():
        app_params = list()
        url = "http://appuser.people.cn/i/menu/gettaglist.json?timestamp=1609310723&pjcode=2_2015_11_26&udid=" \
              "300000000122678&device_size=810.0x1440.0&version=11&devicetype=2&uid=0&time=1609310972166&securit" \
              "ykey=2dcb732ccbcf452def5e31def491a408"
        headers = {
            "Accept-Encoding": "gzip, deflate",
            "Accept-Charset": "UTF-8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
            "Host": "appuser.people.cn",
            "Connection": "Keep-Alive",
        }
        method = "get"
        app_param = InitClass().app_params(url, headers, method)
        app_params.append(app_param)
        yield app_params

    @staticmethod
    def analyze_channel(channelsress):
        channelsparams = []
        for channelsres in channelsress:
            channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
            for channellists in channelslists.get("data")[0]["children"]:
                channel_name = channellists["name"]
                channel_id = channellists["id"]
                channelparam = InitClass().channel_fields(channel_id, channel_name)
                channelsparams.append(channelparam)
        yield channelsparams

    def getarticlelistparams(self, channelsparams):
        articlelistsparams = []
        channel_data = list()
        method = "get"
        channel_num = 0
        for channel in channelsparams:
            channel_num += 1
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            url = "http://appuser.people.cn/i/content/getcontentlist.json?"
            headers = {
                "Accept-Encoding": "gzip, deflate",
                "Accept-Charset": "UTF-8",
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
                "Host": "appuser.people.cn",
                "Connection": "Keep-Alive"
            }
            data = {
                "tagid": channelid,
                "timestamp": "1609310780",
                "menutype": "article",
                "pjcode": "2_2015_11_26",
                "udid": "300000000122678",
                "device_size": "810.0x1440.0",
                "version": "11",
                "devicetype": "2",
                "uid": "0",
                "time": "1609311506240",
                "securitykey": "551ea561268d1594cc72d8ea4af6d04c",
            }
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            print(channel_field, channel_index_id)
            # yield channel_field
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid = channelid, data = data,
                                                                       channel_index_id = channel_index_id)
            articlelistsparams.append(articlelist_param)
            channel_data.append(channel_field)
        yield [channel_data,articlelistsparams]

    # 在新闻列表页存储新闻的方法
    def article_gen(self, articles, banners, channelid, channelname, channelindexid):
        article_fields = InitClass().article_fields()
        articleparam = InitClass().article_list_fields()
        # 获取文章列表内的有用信息
        article_id = articles["id"]
        article_title = articles["title"]
        article_source = articles["source"]
        article_author = articles["author"]
        videoss = articles["medias"]
        if videoss:
            videos = list()
            videocover = list()
            for video in videoss:
                videos.append(video["source_url"])
                videocover.append(video["img_url"])
            article_fields["videos"] = videos
            article_fields["videocover"] = videocover
        commentnum = articles["nums"][0]["nums_num"]
        banners = banners
        article_cover = [articles["cover"]]
        article_fields["articlecovers"] = article_cover

        # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
        article_fields["appname"] = self.newsname
        article_fields["channelID"] = channelid
        article_fields["channelname"] = channelname
        article_fields["channelindexid"] = channelindexid
        article_fields["workerid"] = article_id
        article_fields["title"] = article_title
        article_fields["source"] = article_source
        article_fields["author"] = article_author
        article_fields["commentnum"] = commentnum
        article_fields["banner"] = banners
        # 将请求文章必需信息存入
        articleparam["articleField"] = article_fields  # 携带文章采集的数据
        return articleparam

    def analyze_articlelists(self, articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            channel_index_id = articleslistres.get("channelindexid")
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent = 4, ensure_ascii = False))
                print(articleslists)
                articleslists = articleslists["data"]
                for articles in articleslists:
                    for article1 in articles["items"]:
                        banners = 1 if article1["style"] == "list_pic1_type3" else 0
                        for article in article1["items_sub"]:
                            article_param = self.article_gen(article, banners, channelid, channelname, channel_index_id)
                            articlesparams.append(article_param)
            except Exception as e:
                logging.info(f"解析文章列表{e}")
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        headers = {
            "Accept-Encoding": "gzip, deflate",
            "Accept-Charset": "UTF-8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
            "Host": "appuser.people.cn",
            "Connection": "Keep-Alive",
        }
        for article in articles:
            article_field = article.get("articleField")
            channel_id = article_field.get("channelID")
            article_id = article_field.get("workerid")
            url = "http://appuser.people.cn/i/content/getdetail.json?"
            method = 'get'
            data = {
                "tagid": channel_id,
                "itemid": article_id,
                "pjcode": "2_2015_11_26",
                "udid": "300000000122678",
                "device_size": "810.0x1440.0",
                "version": "11",
                "devicetype": "2",
                "uid": "0",
                "time": "1609313445794",
                "securitykey": "c89a65f39c2dfd2787ec7ecc9aa4e6f6",
            }
            articleparam = InitClass().article_params_fields(url, headers, method, data = data,
                                                             article_field = article_field)
            articleparams.append(articleparam)
        yield articleparams

    @staticmethod
    def signal_article_analyze(articlejson, fields):
        article = articlejson["data"]["article"]
        if "source" in article and article["source"]:
            source = article["source"]
            fields["source"] = source
        pubtime = article["time"]
        pubtime = InitClass().date_time_stamp(pubtime) if pubtime else ""
        videoss = article["medias"] if "medias" in article.keys() else list()
        if videoss:
            videos = list()
            images = list()
            videocover = list()
            for video in videoss:
                if video["type"] == "video":
                    videos.append(video["source_url"])
                    videocover.append(video["img_url"])
                elif video["type"] == "img":
                    images.append(video["img_url"])
            fields["videos"] = videos
            fields["videocover"] = videocover
            fields["images"] = images
        if "content" in article and article["content"]:
            content = article["content"]
            fields["content"] = content
        else:
            fields["content"] = ""
        url = article["share_url"]
        fields["pubtime"] = pubtime
        fields["url"] = url
        return fields

    def analyzearticle(self, articleres):
        num = 0
        try:
            for article in articleres:
                fields = article.get("articleField")
                article_res = article.get("articleres")
                # print(article_res.encode("ISO-8859-1").decode("utf8"))
                # article_res = article_res.encode("ISO-8859-1").decode("utf8")
                article_json = json.loads(json.dumps(json.loads(article_res), indent = 4, ensure_ascii = False))
                fields = self.signal_article_analyze(article_json, fields)
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
        except Exception as e:
            num += 1
            self.logger.info(f"{num}解析错误{e}")


def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = GanSuRiBao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
    appspider = GanSuRiBao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    appparams = appspider.get_app_params()
    channelsres = appspider.getchannel(appparams.__next__())
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

