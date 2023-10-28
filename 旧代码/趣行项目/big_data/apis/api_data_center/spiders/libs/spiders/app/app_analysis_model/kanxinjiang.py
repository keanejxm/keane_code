# Author Keane
# coding=utf-8
# @Time    : 2021/1/12 14:39
# @File    : kanxinjiang.py
# @Software: PyCharm
import json
import logging

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class KanXinJiang(Appspider):

    def app_headers(self):
        app_headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
            "Host":"api.xinjiangnet.com.cn",
            "Connection":"Keep-Alive",
            "Accept-Encoding":"gzip",

        }
        return app_headers

    def get_app_params(self):
        app_params = list()
        url = "http://api.xinjiangnet.com.cn/mobile/index.php?app=mobile&controller=content&action=category&thumbsize=576&type=mobile&phonetype=android&version=6.0.0"
        headers = self.app_headers()
        method = "get"
        app_param = InitClass().app_params(url, headers, method)
        app_params.append(app_param)
        yield app_params

    @staticmethod
    def analyze_channel(channelsress):
        channelsparams = []
        for channelsres in channelsress:
            channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
            channel_name = "新闻头条"
            channel_id = "0"
            channelparam = InitClass().channel_fields(channel_id, channel_name)
            channelsparams.append(channelparam)
            for channellists in channelslists["data"]["news"]:
                channel_name = channellists["catname"]
                channel_id = channellists["catid"]
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
            url = "http://api.xinjiangnet.com.cn/mobile/index.php?"
            headers = self.app_headers()
            data_bannel = {
                "app":"mobile",
                "controller":"content",
                "action":"slide",
                "catid":channelid,
                "time":"",
                "version":"6.0.0",
                "type":"mobile",
                "phonetype":"android",
                "thumbsize":"576",
            }
            data_news_list = {
                "app":"mobile",
                "controller":"content",
                "action":"index",
                "catid":channelid,
                "page":"1",
                "time":"",
                "keyword":"",
                "version":"6.0.0",
                "type":"mobile",
                "phonetype":"android",
                "thumbsize":"576",
            }
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            print(channel_field, channel_index_id)
            # yield channel_field
            articlelist_param_banner = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid = channelid, data = data_bannel,
                                                                       channel_index_id = channel_index_id,banners=1)
            articlelist_param_list = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid = channelid, data = data_news_list,
                                                                       channel_index_id = channel_index_id)
            channel_data.append(channel_field)
            articlelistsparams.append(articlelist_param_banner)
            articlelistsparams.append(articlelist_param_list)
        yield [channel_data,articlelistsparams]

    # 在新闻列表页存储新闻的方法
    def article_gen(self, articles, banners, channelid, channelname, channelindexid,topic_id,topic_title):
        article_fields = InitClass().article_fields()
        articleparam = InitClass().article_list_fields()
        # 获取文章列表内的有用信息
        article_id = articles["contentid"]
        article_title = articles["title"]
        article_cover = [articles["thumb"]]
        article_fields["articlecovers"] = article_cover
        # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
        article_fields["appname"] = self.newsname
        article_fields["channelID"] = channelid
        article_fields["channelname"] = channelname
        article_fields["channelindexid"] = channelindexid
        article_fields["workerid"] = article_id
        article_fields["title"] = article_title
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
            banners = articleslistres.get("banner")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent = 4, ensure_ascii = False))
                print(articleslists)
                for article in articleslists["data"]:
                    article_param = self.article_gen(article, banners, channelid, channelname, channel_index_id,"","")
                    print(article_param)
                    articlesparams.append(article_param)
            except Exception as e:
                    logging.info(f"解析文章列表{e}")
        yield articlesparams

    def getarticleparams(self,articles):
        articleparams = []
        for article in articles:
            article_field = article.get("articleField")
            article_id = article_field.get("workerid")
            if article_id:
                url = "http://api.xinjiangnet.com.cn/mobile/index.php?"
                headers = self.app_headers()
                method = 'get'
                data = {
                    "app":"mobile",
                    "controller":"article",
                    "action":"content",
                    "contentid":article_id,
                    "version":"6.0.0",
                    "type":"mobile",
                    "phonetype":"android",
                    "thumbsize":"576",
                }
                articleparam = InitClass().article_params_fields(url, headers, method, data = data,
                                                             article_field = article_field)
                articleparams.append(articleparam)
        yield articleparams

    @staticmethod
    def signal_article_analyze(articlejson, fields):
        article = articlejson["data"]
        source = article["source"]
        digest = article["description"]
        comment_num = article["comments"]
        pubtime = int(article["published"])*1000
        content = article["content"]
        images = InitClass().get_images(content)
        url = article["shareurl"]
        fields["source"] = source
        fields["images"] = images
        fields["commentnum"] = comment_num
        fields["pubtime"] = pubtime
        fields["content"] = content
        fields["url"] = url
        fields["digest"] = digest
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
    appspider = KanXinJiang(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
    appspider = KanXinJiang(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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



