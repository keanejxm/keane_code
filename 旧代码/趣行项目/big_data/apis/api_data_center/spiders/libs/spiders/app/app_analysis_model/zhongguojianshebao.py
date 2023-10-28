# -*- encoding:utf-8 -*-
"""
@功能:中国建设报app解析模板
@AUTHOR：Keane
@文件名：zhongguojianshebao.py
@时间：2021/1/4  16:12
"""
import json
import logging

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class ZhongGuoJianSheBao(Appspider):
    @staticmethod
    def app_headers():
        app_headers = {
            "Host": "apis.183read.cc",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Cookie": "PHPSESSID=04dbbec34eb3fd6abada2a367e850dca; PHPSESSID=00dc59dd782be2f8546783d3eef392e8",
            "User-Agent": "okhttp/3.8.0",
        }
        return app_headers

    def get_app_params(self):
        app_params = list()
        url = "https://apis.183read.cc/open_api/rest6.php?"
        headers = self.app_headers()
        data = {
            "act": "newspaper.history.items.get",
            "param": '{"app_key":"15a4fc098f856afc10b11ffbbb5aa3e3","identify_key":"fb8cea13ad5fbe6f45571'
                     'c03ff5da130","opt":1,"page_limit":"20","page_num":"1","platform":"1","resource_id":"387'
                     '96","user_id":"4022306"}'
        }
        method = "get"
        app_param = InitClass().app_params(url, headers, method, data = data)
        app_params.append(app_param)
        yield app_params

    @staticmethod
    def analyze_channel(channelsress):
        channelsparams = []
        for channelsres in channelsress:
            channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
            print(channelslists)
            for channellists in channelslists.get("result").get("history_item_list"):
                channel_name = channellists["item_name"]
                channel_id = channellists["item_id"]
                channel_volume = channellists["volume"]
                channel_name = channel_name + channel_volume
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
            url = "https://apis.183read.cc/open_api/rest6.php?"
            headers = self.app_headers()
            data = {
                'act': 'newspaper.latest.all.article',
                'param': '{"app_key":"15a4fc098f856afc10b11ffbbb5aa3e3","identify_key":"fb8cea13ad5fbe6f45571c03ff'
                         '5da130","item_id":' + channelid + ',"no_page_limit":"0","opt":1,"page_limit":"20","page_'
                                                            'num":"1","use_magazine_info":"1"}'
            }
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            channel_data.append(channel_field)
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid = channelid, data = data,
                                                                       channel_index_id = channel_index_id)
            articlelistsparams.append(articlelist_param)
        yield [channel_data,articlelistsparams]

    # 在新闻列表页存储新闻的方法
    def article_gen(self, articles, channelid, channelname, channelindexid, topic_id, topic_title):
        article_fields = InitClass().article_fields()
        articleparam = InitClass().article_list_fields()
        # 获取文章列表内的有用信息
        article_id = articles["magazine_article_id"]
        article_title = articles["title"]
        article_digest = articles["introduction"]
        pub_time = articles["pub_date"]
        banners_name = articles["page_name"]
        banners = 1 if banners_name == "头版" else 0
        if pub_time:
            pub_time = InitClass().date_time_stamp(pub_time)
        # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
        article_fields["appname"] = self.newsname
        article_fields["platformID"] = self.platform_id
        article_fields["channelID"] = channelid
        article_fields["channelname"] = channelname
        article_fields["channelindexid"] = channelindexid
        article_fields["workerid"] = article_id
        article_fields["title"] = article_title
        article_fields["digest"] = article_digest
        article_fields["pubtime"] = pub_time
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
                for article in articleslists["result"]["magazine_article_list"]:
                    article_param = self.article_gen(article, channelid, channelname, channel_index_id, "", "")
                    print(article_param)
                    articlesparams.append(article_param)
            except Exception as e:
                logging.info(f"解析文章列表{e}")
        yield articlesparams

    def getarticleparams(self, articles):
        articleparams = []
        for article in articles:
            article_field = article.get("articleField")
            article_id = article_field.get("workerid")
            url = "https://apis.183read.cc/open_api/rest6.php?"
            headers = self.app_headers()
            method = 'get'
            data = {
                "act": "newspaper.article.info.get",
                'param': '{"app_key":"15a4fc098f856afc10b11ffbbb5aa3e3","article_id":' + article_id +
                         ',"identify_key":"fb8cea13ad5fbe6f45571c03ff5da130","opt":1,"platform":"1","user_id":"402'
                         '2306"}'
            }
            articleparam = InitClass().article_params_fields(url, headers, method, data = data,
                                                             article_field = article_field)
            articleparams.append(articleparam)
        yield articleparams

    @staticmethod
    def signal_article_analyze(articlejson, fields):
        article = articlejson["result"]["newspaper_article_info"]
        author = article["author"]
        read_num = article["view_count"]
        comment_num = article["comment_count"]
        audios = article["mp3_http_file"]
        pubtime = article["create_time"]
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
        content = article["content"]
        url = article["share_url"]
        fields["readnum"] = read_num
        fields["commentnum"] = comment_num
        fields["audios"] = [audios]
        fields["author"] = author
        fields["pubtime"] = pubtime
        fields["content"] = content
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
                try:
                    article_json = json.loads(json.dumps(json.loads(article_res), indent = 4, ensure_ascii = False))
                    fields = self.signal_article_analyze(article_json, fields)
                    fields = InitClass().wash_article_data(fields)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
                except Exception as e:
                    self.logger.info(f"{articleres}json失败{e}")
        except Exception as e:
            num += 1
            self.logger.info(f"{num}解析错误{e}")


def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = ZhongGuoJianSheBao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
    appspider = ZhongGuoJianSheBao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
