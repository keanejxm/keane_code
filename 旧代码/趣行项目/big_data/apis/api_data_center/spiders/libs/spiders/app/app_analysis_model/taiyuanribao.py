# -*- encoding:utf-8 -*-
"""
@功能:
@AUTHOR：Keane
@文件名：taiyuanribao.py
@时间：2020/12/30  16:34
"""
import json
import logging
import time

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class TaiYuanRiBao(Appspider):

    def app_headers(self):
        app_headers = {
            "Content-Length": "0",
            "Host": "www.tyrbw.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        return app_headers

    def get_app_params(self):
        app_params = list()
        url = "http://www.tyrbw.com//epaper2/index.php?r=news/columns"
        headers = self.app_headers()
        method = "post"
        app_param = InitClass().app_params(url, headers, method)
        app_params.append(app_param)
        yield app_params

    def analyze_channel(self, channelsres):
        channelsparams = []
        for channelsres in channelsres:
            channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))
            for channellists in channelslists.get("columns"):
                channel_name = channellists["name"]
                channel_id = channellists["tid"]
                channelparam = InitClass().channel_fields(channel_id, channel_name)
                channelsparams.append(channelparam)
            yield channelsparams

    def getarticlelistparams(self, channelsparams):
        articlelistsparams = []
        method = "post"
        channel_num = 0
        channel_data = list()
        for channel in channelsparams:
            channel_num += 1
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            url = "http://www.tyrbw.com//epaper2/index.php?r=news/home"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
                "Host": "www.tyrbw.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "Content-Length": "73",
            }
            data = f"reqtime={int(time.time() * 1000)}&v=2.0.0&model=MuMu&app_id=1001&version=6.0.1&tid={channelid}&"
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            # yield channel_field
            channel_data.append(channel_field)
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid=channelid, channeljson=data,
                                                                       channel_index_id=channel_index_id)
            articlelistsparams.append(articlelist_param)
        yield [channel_data, articlelistsparams]

    # 在新闻列表页存储新闻的方法
    def article_gen(self, articles, banners, channelid, channelname, channelindexid, topic_id, topic_title):
        if banners == 1:
            article_fields = InitClass().article_fields()
            articleparam = InitClass().article_list_fields()
            # 获取文章列表内的有用信息
            article_id = articles["topid"]
            article_title = articles["toptitle"]
            article_cover = [articles["topimag"]]
            article_fields["articlecovers"] = article_cover
            # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
            article_fields["appname"] = self.newsname
            article_fields["platformID"] = self.platform_id
            article_fields["channelID"] = channelid
            article_fields["channelname"] = channelname
            article_fields["channelindexid"] = channelindexid
            article_fields["workerid"] = article_id
            article_fields["title"] = article_title
            article_fields["banner"] = banners
            # 将请求文章必需信息存入
            articleparam["articleField"] = article_fields  # 携带文章采集的数据
            return articleparam
        else:
            article_type = articles["newstype"]
            if article_type == 4:  # 专题
                article_fields = InitClass().topic_fields()
                articleparam = InitClass().article_list_fields()
                # 获取文章列表内的有用信息
                article_id = articles["specialid"]
                article_title = articles["specialtitle"]
                article_cover = [articles["specialimag"]]
                article_fields["topicCover"] = article_cover
                # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                article_fields["platformName"] = self.newsname
                article_fields["platformID"] = self.platform_id
                article_fields["topicID"] = article_id
                article_fields["title"] = article_title
                # 将请求文章必需信息存入
                articleparam["articleField"] = article_fields  # 携带文章采集的数据
                return articleparam
            else:
                article_fields = InitClass().article_fields()
                articleparam = InitClass().article_list_fields()
                # 获取文章列表内的有用信息
                article_id = articles["newsid"]
                article_title = articles["newstitle"]
                comment_num = articles["comment_count"]
                article_cover = [articles["newsicon"]]
                article_fields["articlecovers"] = article_cover
                # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                article_fields["appname"] = self.newsname
                article_fields["platformID"] = self.platform_id
                article_fields["channelID"] = channelid
                article_fields["channelname"] = channelname
                article_fields["channelindexid"] = channelindexid
                article_fields["workerid"] = article_id
                article_fields["title"] = article_title
                article_fields["banner"] = banners
                article_fields["topicid"] = topic_id
                article_fields["topicTitle"] = topic_title
                article_fields["commentnum"] = comment_num
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
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                article_types = ["topbanner", "newslist"]
                for article_type in article_types:
                    articlelists = articleslists[article_type]
                    banners = 1 if article_type == "topbanner" else 0
                    for article in articlelists:
                        article_param = self.article_gen(article, banners, channelid, channelname, channel_index_id, "",
                                                         "")
                        articlesparams.append(article_param)
            except Exception as e:
                logging.info(f"解析文章列表{e}")
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        for article in articles:
            article_field = article.get("articleField")
            article_id = article_field.get("workerid")
            if article_id:
                url = "http://www.tyrbw.com//epaper2/index.php?r=news/normal"
                headers = {
                    "Content-Length": "80",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Host": "www.tyrbw.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                method = 'post'
                data = f"newsid={article_id}&reqtime=1609320540619&v=2.0.0&model=MuMu&app_id=1001&version=6.0.1"
            else:
                topic_id = article_field.get("topicID")
                url = "http://www.tyrbw.com//epaper2/index.php?r=news/zhome"
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
                    "Host": "www.tyrbw.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "Content-Length": "81",
                }
                method = 'post'
                data = f"reqtime={int(time.time() * 1000)}&v=2.0.0&specialid={topic_id}&model=MuMu&app_id=1001&versio" \
                       f"n=6.0.1&"
            articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                             article_field=article_field)
            articleparams.append(articleparam)
        yield articleparams

    @staticmethod
    def signal_article_analyze(articlejson, fields):
        article = articlejson
        source = article["newsfrom"]
        author = article["author"]
        pubtime = article["createtime"]
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
        content = article["newscontent"]
        url = article["shareurl"]
        fields["source"] = source
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
                channel_id = fields.get("channelID")
                channel_name = fields.get("channelName")
                channel_index_id = fields.get("channelindexid")
                # article_res = article_res.encode("ISO-8859-1").decode("utf8")
                try:
                    article_json = json.loads(json.dumps(json.loads(article_res), indent=4, ensure_ascii=False))
                    if "topicID" in fields.keys():
                        topic_title = fields.get("title")
                        if "topbanner" in article_json and article_json["topbanner"]:
                            article_banner = article_json["topbanner"]
                        else:
                            article_banner = list()
                        article_list = article_json["newslist"]
                        if article_banner:
                            article_list = article_list + article_banner
                        article_params = list()
                        fields,topic_id = InitClass().wash_topic_data(fields)
                        for article in article_list:
                            article_param = self.article_gen(article, "0", channel_id, channel_name, channel_index_id,
                                                             topic_id, topic_title)
                            article_params.append(article_param)
                        article_params = self.getarticleparams(article_params)
                        article_res = self.getarticlehtml(article_params.__next__())
                        for article_field in self.analyzearticle(article_res.__next__()):
                            pubtime = article_field["data"]["works"]["pubTime"]
                            digest = article_field["data"]["works"]["digest"]
                            fields["digest"] = digest
                            fields["pubTime"] = pubtime
                            yield article_field
                        yield {"code": 1, "msg": "OK", "data": {"topic": fields}}
                        # print(fields)
                    else:
                        fields = self.signal_article_analyze(article_json, fields)
                        fields = InitClass().wash_article_data(fields)
                        yield {"code": 1, "msg": "OK", "data": {"works": fields}}
                    # print(json.dumps(fields, indent=4, ensure_ascii=False))
                except Exception as e:
                    self.logger.info(f"{articleres}json失败{e}")
        except Exception as e:
            num += 1
            self.logger.info(f"{num}解析错误{e}")


def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = TaiYuanRiBao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
    article_retu["data"]["topics"] =topics_list
    article_retu["data"]["worksList"] =articles_list
    yield article_retu


def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = TaiYuanRiBao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    appparams = appspider.get_app_params()
    channelsres = appspider.getchannel(appparams.__next__())
    channelsparams = appspider.analyze_channel(channelsres.__next__())
    articlelistparameses = appspider.getarticlelistparams(channelsparams.__next__())
    articlelistparamess = list()
    for articlelistparamesss in articlelistparameses:
        articlelistparamess = articlelistparamesss
    channel_flag = 1
    channel_data = articlelistparamess[0]
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

# if __name__ == '__main__':
#     appname = "太原日报"
#     platform_id = "2f5b4c4e85ec6fcad9ae235ad39ce53e"
#     self_typeid = "4_1_2_3"
#     run(appname, platform_id, self_typeid)
