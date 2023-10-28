# Author Keane
# coding=utf-8
# @Time    : 2021/1/12 15:38
# @File    : tianshanwang.py
# @Software: PyCharm
import json
import logging
import time

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class TaiYuanRiBao(Appspider):

    def app_headers(self):
        app_headers = {
            "Host":"st-m-api.xjmty.com",
            "Connection":"Keep-Alive",
            "Accept-Encoding":"gzip",
            "User-Agent":"okhttp/3.8.1",
        }
        return app_headers

    def get_app_params(self):
        app_params = list()
        url = "http://st-m-api.xjmty.com/v2/start?"
        headers = self.app_headers()
        method = "get"
        data = {
            "cachetime":"0",
            "system_version":"6.0.1",
            "sign":"21a52fcae23f0c01d2c7a9bef3fbef68",
            "nav_width":"288",
            "time":"1610436970654",
            "sharetime":"0",
            "siteid":"10001",
            "clientid":"1",
            "modules":"common:4",
            "app_version":"4.1.5",
            "device_id":"08:00:27:E1:4F:1C",
            "system_width":"576",
            "system_name":"android",
            "ip":"10.0.2.15",
            "device_model":"MuMu",
            "nav_height":"81",
            "system_height":"1024",
            "device_version":"AndroidMuMu",
            "type":"android",
        }
        app_param = InitClass().app_params(url, headers, method,data=data)
        app_params.append(app_param)
        yield app_params

    @staticmethod
    def analyze_channel(channelsress):
        channelsparams = []
        for channelsres in channelsress:
            channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
            print(channelslists)
            for channellists in channelslists["data"]["common"]["menu"][0]["submenu"]:
                channel_name = channellists["name"]
                channel_id = channellists["menuid"]
                channelparam = InitClass().channel_fields(channel_id, channel_name)
                channelsparams.append(channelparam)
        yield channelsparams

    def getarticlelistparams(self, channelsparams):
        articlelistsparams = []
        method = "get"
        channel_num = 0
        for channel in channelsparams:
            channel_num += 1
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            url = "http://st-m-api.xjmty.com/v2/menudata?"
            headers = self.app_headers()
            data = {
                "sign":"5260f920bf12b48a0a1b3511b3234a87",
                "time":"1610439259705",
                "siteid":"10001",
                "clientid":"1",
                "modules":"common:2",
                "app_version":"4.1.5",
                "thumbrate":"2",
                "device_id":"08:00:27:E1:4F:1C",
                "listsiteid":"0",
                "system_name":"android",
                "ip":"10.0.2.15",
                "areas":",,",
                "type":"android",
                "page":"1",
                "slide":"0",
                "pagesize":"20",
                "menuid":channelid,
            }
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            print(channel_field, channel_index_id)
            # yield channel_field
            articlelist_param_banner = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid = channelid, data = data,
                                                                       channel_index_id = channel_index_id)

            articlelistsparams.append(articlelist_param_banner)
        yield articlelistsparams

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
                # for article in articleslists["data"]:
                #     article_param = self.article_gen(article, banners, channelid, channelname, channel_index_id,"","")
                #     print(article_param)
                #     articlesparams.append(article_param)
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
        # videoss = article["medias"] if "medias" in article.keys() else list()
        # if videoss:
        #     videos = list()
        #     images = list()
        #     videocover = list()
        #     for video in videoss:
        #         if video["type"] == "video":
        #             videos.append(video["source_url"])
        #             videocover.append(video["img_url"])
        #         elif video["type"] == "img":
        #             images.append(video["img_url"])
        #     fields["videos"] = videos
        #     fields["videocover"] = videocover
        #     fields["images"] = images
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
                    print(article_json)

                    fields = self.signal_article_analyze(article_json, fields)
                    print(json.dumps(fields, indent = 4, ensure_ascii = False))
                except Exception as e:
                    self.logger.info(f"{articleres}json失败{e}")
        except Exception as e:
            num += 1
            self.logger.info(f"{num}解析错误{e}")


def run(appname, logger,platform_id, self_typeid,):
    print(appname, platform_id, self_typeid)
    appspider = TaiYuanRiBao(appname, logger,platform_id = platform_id, self_typeid = self_typeid)
    appparams = appspider.get_app_params()
    channelsres = appspider.getchannel(appparams.__next__())
    channelsparams = appspider.analyze_channel(channelsres.__next__())
    articlelistparames = appspider.getarticlelistparams(channelsparams.__next__())
    articleslistsres = appspider.getarticlelists(articlelistparames.__next__())
    articles = appspider.analyze_articlelists(articleslistsres.__next__())
    articleparams = appspider.getarticleparams(articles.__next__())
    articlesres = appspider.getarticlehtml(articleparams.__next__())
    appspider.analyzearticle(articlesres.__next__())
