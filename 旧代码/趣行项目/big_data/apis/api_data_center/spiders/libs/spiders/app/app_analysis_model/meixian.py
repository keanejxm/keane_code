# -*- encoding:utf-8 -*-
"""
@功能:魅西安解析模板
@AUTHOR：Keane
@文件名：meixian.py
@时间：2020/12/28  14:03
"""
import json
import logging
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class MeiXiAn(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://h5.newaircloud.com/api/getColumns?sid=xarb&cid=0&version=2"
        headers = {
            "Host": "h5.newaircloud.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.1",
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method)
        yield app_params

    def analyze_channel(self, channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))
        for channellists in channelslists.get("columns"):
            channel_name = channellists["columnName"]
            channel_id = channellists["columnID"]
            url = "https://h5.newaircloud.com/api/getColumns?"
            headers = {
                "Host": "h5.newaircloud.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.8.1",
            }
            data = {
                "sid": "xarb",
                "cid": channel_id,
                "version": "2",
            }
            columns = self.session.get(url, headers=headers, params=data).text
            columns = json.loads(columns)
            for column in columns.get("columns"):
                column_name = column["columnName"]
                column_id = column["columnID"]
                sub_name = channel_name + "-" + column_name  # 第二级子频道名字
                sub_id = str(channel_id) + "-" + str(column_id)
                channelparam = InitClass().channel_fields(sub_id, sub_name, categoryid=column_id)
                channelsparams.append(channelparam)
        yield channelsparams

    def getarticlelistparams(self, channelsparams):
        url = "https://h5.newaircloud.com/api/getArticles?"
        headers = {
            "Host": "h5.newaircloud.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.1",
        }
        articlelistsparams = []
        channel_data = list()
        method = "get"
        channel_num = 0
        for channel in channelsparams:
            channel_num += 1
            channelid = channel.get("categoryid")
            categoryid = channel.get("channelid")
            channelname = channel.get("channelname")
            data = {
                "sid": "xarb",
                "cid": channelid,
                "lastFileID": "0",
                "rowNumber": "0",
                "version": "2",
                "adLastID": "0",
            }
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            channel_data.append(channel_field)
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid=categoryid, data=data,
                                                                       channel_index_id=channel_index_id)
            articlelistsparams.append(articlelist_param)
        yield [channel_data, articlelistsparams]

    def analyze_articlelists(self, articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            channel_index_id = articleslistres.get("channelindexid")
            appname = self.newsname
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    for articles in articleslists["list"]:
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        # 获取文章列表内的有用信息
                        article_id = articles["fileID"]
                        link_id = articles["linkID"]
                        article_title = articles["title"]
                        share_url = articles["contentUrl"]
                        source = articles["source"]
                        editor = articles["editor"]
                        readnum = articles["countClick"]
                        commentnum = articles["countDiscuss"]
                        likenum = articles["countPraise"]
                        sharenum = articles["countShare"]
                        banners = articles["isTop"]
                        pubtime = articles["publishTime"]
                        if pubtime:
                            pubtime = InitClass().date_time_stamp(pubtime)
                        article_cover = [articles["pic1"]]
                        article_fields["articlecovers"] = article_cover

                        # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                        article_fields["appname"] = appname
                        article_fields["platformID"] = self.platform_id
                        article_fields["channelID"] = channelid
                        article_fields["channelname"] = channelname
                        article_fields["channelindexid"] = channel_index_id
                        article_fields["workerid"] = article_id
                        article_fields["linkid"] = link_id
                        article_fields["title"] = article_title
                        article_fields["url"] = share_url
                        article_fields["source"] = source
                        article_fields["editor"] = editor
                        article_fields["readnum"] = readnum
                        article_fields["commentnum"] = commentnum
                        article_fields["likenum"] = likenum
                        article_fields["sharenum"] = sharenum
                        article_fields["pubtime"] = pubtime
                        article_fields["banner"] = banners
                        # 将请求文章必需信息存入
                        articleparam["articleField"] = article_fields  # 携带文章采集的数据
                        articlesparams.append(articleparam)
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        headers = {
            "Host": "xarboss.newaircloud.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.1",
        }
        for article in articles:
            article_field = article.get("articleField")
            article_id = article_field.get("workerid")
            link_id = article_field.get("linkid")
            channel_name = article_field.get("channelname")
            if channel_name == "封面-专题":
                article_url = "https://h5.newaircloud.com/api/getColumns?"
                data = {
                    "sid": "xarb",
                    "cid": link_id,
                }
                headers = {
                    "Host": "h5.newaircloud.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.8.1",
                }
            elif channel_name == "封面-直播":
                article_url = "https://h5.newaircloud.com/api/getLiveList?"
                data = {
                    "sid": "xarb",
                    "id": link_id,
                    "lastFileID": "0",
                    "rowNumber": "0",
                    "aid": article_id,
                    "isAsc": "0",
                }
                headers = {
                    "Host": "h5.newaircloud.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.8.1",

                }
            else:
                article_url = article_field.get("url")
                data = ""
            method = 'get'
            articleparam = InitClass().article_params_fields(article_url, headers, method, data=data,
                                                             article_field=article_field)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        try:
            for article in articleres:
                fields = article.get("articleField")
                article_res = article.get("articleres")
                channel_name = fields.get("channelname")
                if channel_name == "封面-专题":
                    article_res = json.loads(article_res)
                    fields = InitClass().article_topic(fields)
                    channel_id = fields.get("platformID")
                    topic_title = fields.get("title")
                    topic_id = article_res["column"]["columnID"]
                    fields["topicID"] = topic_id
                    topic_articles = article_res.get("columns")
                    for topic_article in topic_articles:
                        article_article_id = topic_article.get("columnID")
                        url = "https://h5.newaircloud.com/api/getArticles?"
                        headers = {
                            "Host": "h5.newaircloud.com",
                            "Connection": "Keep-Alive",
                            "Accept-Encoding": "gzip",
                            "User-Agent": "okhttp/3.8.1",
                        }
                        data = {
                            "sid": "xarb",
                            "cid": article_article_id,
                            "lastFileID": "0",
                            "rowNumber": "0",
                        }
                        request_param = InitClass().request_params(url, headers, "get", data=data)
                        res = self.send_request(request_param)
                        topic_list_res = res.__next__().get("request_res")
                        topic_list_json = json.loads(topic_list_res)
                        for topic_article in topic_list_json["list"]:
                            article_fields = InitClass().article_fields()
                            # 获取文章列表内的有用信息
                            article_id = topic_article["fileID"]
                            link_id = topic_article["linkID"]
                            article_title = topic_article["title"]
                            share_url = topic_article["contentUrl"]
                            source = topic_article["source"]
                            editor = topic_article["editor"]
                            readnum = topic_article["countClick"]
                            commentnum = topic_article["countDiscuss"]
                            likenum = topic_article["countPraise"]
                            sharenum = topic_article["countShare"]
                            banners = topic_article["isTop"]
                            pubtime = topic_article["publishTime"]
                            if pubtime:
                                pubtime = InitClass().date_time_stamp(pubtime)
                            article_cover = [topic_article["pic1"]]
                            article_fields["articlecovers"] = article_cover
                            # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                            article_fields["appname"] = self.newsname
                            article_fields["channelID"] = channel_id
                            article_fields["channelname"] = channel_name
                            article_fields["workerid"] = article_id
                            article_fields["linkid"] = link_id
                            article_fields["title"] = article_title
                            article_fields["url"] = share_url
                            article_fields["source"] = source
                            article_fields["editor"] = editor
                            article_fields["readnum"] = readnum
                            article_fields["commentnum"] = commentnum
                            article_fields["likenum"] = likenum
                            article_fields["sharenum"] = sharenum
                            article_fields["pubtime"] = pubtime
                            article_fields["banner"] = banners
                            article_fields["topicid"] = topic_id
                            article_fields["topicTitle"] = topic_title
                            if share_url:
                                try:
                                    url = share_url
                                    headers = {
                                        "Host": "xarboss.newaircloud.com",
                                        "Connection": "Keep-Alive",
                                        "Accept-Encoding": "gzip",
                                        "User-Agent": "okhttp/3.8.1",
                                    }
                                    request_param = InitClass().request_params(url, headers, "get",
                                                                               articlefield=article_fields)
                                    article_ress = self.send_request(request_param)
                                    article_ress = article_ress.__next__()
                                    article_res = article_ress.get("request_res")
                                    article_fields = article_ress.get("articlefields")
                                    article_res = article_res.lstrip("var gArticleJson = ")
                                    if article_res:
                                        article_json = eval(article_res)
                                        author = article_json["author"]
                                        content = article_json["content"]
                                        imagess = article_json["images"]
                                        if imagess:
                                            images = list()
                                            for image in imagess:
                                                images.append(image["imageUrl"])
                                            article_fields["images"] = images
                                        videoss = article_json["videos"]
                                        if videoss:
                                            videos = list()
                                            for video in videoss:
                                                videos.append(video["videoUrl"])
                                            article_fields["videos"] = videos
                                        article_fields["content"] = content
                                        article_fields["author"] = author
                                        fields = InitClass().wash_article_data(article_fields)
                                        yield {"code": 1, "msg": "OK", "data": {"works": fields}}
                                except Exception as e:
                                    self.logger.info(f"topic文章解析错误{e}")
                    fields = InitClass().wash_topic_data(fields)
                    yield {"code": 1, "msg": "OK", "data": {"topic": fields}}  # topic的数据结果
                elif channel_name == "封面-直播":
                    try:
                        article_json = json.loads(article_res)
                        live_images = article_json["main"]["attachments"]["pics"]
                        content = article_json["main"]["content"]
                        videos = list()
                        live_videos = article_json["main"]["liveStream"]["hlsUrl"]
                        if live_videos:
                            videos.append(live_videos)
                        live_videos = article_json["main"]["liveStream"]["flvUrl"]
                        if live_videos:
                            videos.append(live_videos)
                        fields["images"] = live_images
                        fields["content"] = content
                        fields["videos"] = videos
                        fields = InitClass().wash_article_data(fields)
                        yield {"code": 1, "msg": "OK", "data": {"works": fields}}
                    except Exception as e:
                        self.logger.info(f"直播解析错误{e}")
                else:
                    # article_res = article_res.encode("ISO-8859-1").decode("utf8")
                    article_res = article_res.lstrip("var gArticleJson = ")
                    if article_res:
                        article_json = eval(article_res)
                        author = article_json["author"]
                        content = article_json["content"]
                        imagess = article_json["images"]
                        if imagess:
                            images = list()
                            for image in imagess:
                                images.append(image["imageUrl"])
                            fields["images"] = images
                        videoss = article_json["videos"]
                        if videoss:
                            videos = list()
                            for video in videoss:
                                videos.append(video["videoUrl"])
                            fields["videos"] = videos
                        fields["content"] = content
                        fields["author"] = author
                        fields = InitClass().wash_article_data(fields)
                        yield {"code": 1, "msg": "OK", "data": {"works": fields}}
        except Exception as e:
            num += 1
            self.logger.info(f"{num}解析错误{e}")




def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = MeiXiAn(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
