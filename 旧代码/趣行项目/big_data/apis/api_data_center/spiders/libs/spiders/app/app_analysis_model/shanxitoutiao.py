# -*- encoding:utf-8 -*-
"""
@功能:陕西头条客户端
@AUTHOR：Keane
@文件名：shanxitoutiao.py
@时间：2020/12/29  13:22
"""
import json
import logging
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class ShanXiTouTiao(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://toutiao.cnwest.com/sxtoutiao/getNewsClassListV6"
        headers = {
            "Host": "toutiao.cnwest.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.10.0",
        }
        method = "get"
        app_param = InitClass().app_params(url, headers, method)
        yield app_param

    def analyze_channel(self, channelsress):
        channelslists = json.loads(json.dumps(json.loads(channelsress), indent=4, ensure_ascii=False))
        for channellists in channelslists.get("data"):
            channel_name = channellists["newsClassName"]
            channel_id = channellists["id"]
            channelparam = InitClass().channel_fields(channel_id, channel_name)
            yield channelparam

    def getarticlelistparams(self, channelsress):
        method = "get"
        channel_num = 0
        for channel in self.analyze_channel(channelsress):
            channel_num += 1
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            if channelname == "推荐":
                url = "http://toutiao.cnwest.com/sxtoutiao/getPersonal?size=10&page=1&deviceId=ffffffff-c795-b5cb-ffff-ffffc2e834d9&city=%E8%A5%BF%E5%AE%89%E5%B8%82"
                headers = {
                    "Host": "toutiao.cnwest.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.10.0",
                }
                data = ""
            elif channelname == "专题":
                url = "http://toutiao.cnwest.com/sxtoutiao/getTopicListV3"
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Content-Length": "60",
                    "Host": "toutiao.cnwest.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.10.0",
                }
                method = "post"
                data = "size=10&deviceId=ffffffff-c795-b5cb-ffff-ffffc2e834d9&page=1"
            else:
                url = "http://toutiao.cnwest.com/sxtoutiao/getNewsListByClassIdV5"
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Content-Length": "98",
                    "Host": "toutiao.cnwest.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.10.0",
                }
                method = "post"
                data = f"deviceId=ffffffff-c795-b5cb-ffff-ffffc2e834d9&newsclassid={channelid}&size=10&page=1&version=android_5.1.0"
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid=channelid, data=data,
                                                                       channel_index_id=channel_index_id)
            yield channel_field, [articlelist_param]

    # 在新闻列表页存储新闻的方法
    def article_gen(self, articles, banners, channelid, channelname, channelindexid):
        article_fields = InitClass().article_fields()
        # 获取文章列表内的有用信息
        article_id = articles["id"]
        article_title = articles["newsTitle"]
        share_url = articles["shareUrl"]
        source = articles["newsFrom"]
        commentnum = articles["newsCommentNum"]
        banners = banners
        article_type = articles["newsListType"]
        pubtime = articles["createTime"]
        if pubtime:
            pubtime = InitClass().date_time_stamp(pubtime)
        article_cover = [articles["postcard"]]
        article_fields["articlecovers"] = article_cover

        # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
        article_fields["appname"] = self.newsname
        article_fields["platformID"] = self.platform_id
        article_fields["channelID"] = channelid
        article_fields["channelname"] = channelname
        article_fields["channelindexid"] = channelindexid
        article_fields["workerid"] = article_id
        article_fields["contentType"] = article_type
        article_fields["title"] = article_title
        article_fields["url"] = share_url
        article_fields["source"] = source
        article_fields["commentnum"] = commentnum
        article_fields["pubtime"] = pubtime
        article_fields["banner"] = banners
        # 将请求文章必需信息存入
        return article_fields

    def analyze_articlelists(self, articleslistsres):
        for articleslistres in articleslistsres:
            print(articleslistres)
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            channel_index_id = articleslistres.get("channelindexid")
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                print(articleslists)
                try:
                    articleslists = articleslists["data"]
                    if isinstance(articleslists, dict):
                        for articles_key in articleslists.keys():
                            banners = 1 if articles_key == "top" else 0
                            if articleslists[articles_key]:
                                for articles in articleslists[articles_key]:
                                    articleparam = self.article_gen(articles, banners, channelid, channelname,
                                                                    channel_index_id)
                                    yield articleparam
                    else:
                        num = 0
                        for articles in articleslists:
                            num += 1
                            banners = 1 if num == 1 else 0
                            if "newslist" in articles.keys():
                                for articles in articles["newslist"]:
                                    articleparam = self.article_gen(articles, banners, channelid, channelname,
                                                                    channel_index_id)
                                    yield articleparam
                            else:
                                articleparam = self.article_gen(articles, banners, channelid, channelname,
                                                                channel_index_id)
                                yield articleparam
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")

    def getarticleparams(self,articleslistsres):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "67",
            "Host": "toutiao.cnwest.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.10.0",
        }
        for article in self.analyze_articlelists(articleslistsres):
            channel_name = article.get("channelname")
            article_id = article.get("workerid")
            url = "http://toutiao.cnwest.com/sxtoutiao/v1/getNewsDetailsV3"
            method = 'post'
            data = f"newsId={article_id}&deviceId=ffffffff-c795-b5cb-ffff-ffffc2e834d9&page=1"
            if channel_name == "专题":
                url = "http://toutiao.cnwest.com/sxtoutiao/getTopicListV3"
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Content-Length": "60",
                    "Host": "toutiao.cnwest.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.10.0",
                }
                method = "post"
                data = "size=10&deviceId=ffffffff-c795-b5cb-ffff-ffffc2e834d9&page=1"
            articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                             article_field=article)
            yield [articleparam]

    def topic_article(self, article_json, channelid, channelname):
        fields = InitClass().article_fields()
        article_id = article_json["data"]["id"]
        article_title = article_json["data"]["newsTitle"]
        article_cover = article_json["data"]["newsListpicurl"]
        article_source = article_json["data"]["newsFrom"]
        article_url = article_json["data"]["shareUrl"]
        article_pubtime = article_json["data"]["createTime"]
        if article_pubtime:
            pubtime = InitClass().date_time_stamp(article_pubtime)
        else:
            pubtime = 0
        article_content = article_json["data"]["newsContent"]
        article_author = article_json["data"]["creator"]
        imagess = article_json["data"]["newsPicurl"]
        if imagess:
            images = list()
            for image in imagess:
                images.append(image["url"])
            fields["images"] = images
        videoss = article_json["data"]["newsVideourl"]
        if videoss:
            videos = list()
            videocover = list()
            for video in videoss:
                videos.append(video["url"])
                videocover.append(video["picurl"])
            fields["videos"] = videos
            fields["videocover"] = videocover
        like_num = article_json["data"]["likeNum"]
        comment_num = article_json["data"]["commentNum"]
        fields["appname"] = self.newsname
        fields["channelID"] = channelid
        fields["channelname"] = channelname
        # fields["channelindexid"] = channelindexid
        fields["workerid"] = article_id
        fields["title"] = article_title
        fields["url"] = article_url
        fields["source"] = article_source
        fields["commentnum"] = comment_num
        fields["pubtime"] = pubtime
        # 将请求文章必需信息存入
        fields["content"] = article_content
        fields["articlecovers"] = article_cover
        fields["author"] = article_author
        fields["likenum"] = like_num
        fields["commentnum"] = comment_num
        return fields

    def analyzearticle(self, articleres):
        num = 0
        try:
            for article in articleres:
                fields = article.get("articleField")
                article_res = article.get("articleres")
                content_type = fields.get("contentType")
                channel_name = fields.get("channelname")
                # print(article_res.encode("ISO-8859-1").decode("utf8"))
                # article_res = article_res.encode("ISO-8859-1").decode("utf8")
                if content_type == 3 or channel_name == "专题" and article_res:
                    if channel_name == "图片":
                        pass
                    else:
                        topic_field = InitClass().article_topic(fields)
                        channelid = topic_field.get("channelID")
                        topic_jsons = json.loads(json.dumps(json.loads(article_res), indent=4, ensure_ascii=False))
                        if isinstance(topic_jsons["data"], list):
                            for topic_json in topic_jsons["data"]:
                                fields = InitClass().topic_fields()
                                fields["topicID"] = topic_json.get("id")
                                fields["title"] = topic_json.get("newsTitle")
                                fields["platformName"] = self.newsname
                                fields["platformID"] = self.platform_id
                                fields["topicUrl"] = topic_json.get("shareUrl")
                                fields["topicCover"] = [topic_json.get("postcard")]
                                topic_fields, _id = InitClass().wash_topic_data(fields)
                                topic_id = fields["topicID"]
                                url = "http://toutiao.cnwest.com/sxtoutiao/getTopicClassAndNewsListV2"
                                headers = {
                                    "Content-Type": "application/x-www-form-urlencoded",
                                    "Content-Length": "69",
                                    "Host": "toutiao.cnwest.com",
                                    "Connection": "Keep-Alive",
                                    "Accept-Encoding": "gzip",
                                    "User-Agent": "okhttp/3.10.0",
                                }
                                data = f"userId=&deviceId=ffffffff-c795-b5cb-ffff-ffffc2e834d9&topicid={topic_id}"
                                method = "post"
                                topic_request_param = InitClass().request_params(url, headers, method, data=data)
                                topic_res = self.send_request(topic_request_param).__next__()["request_res"]
                                topic_articles = json.loads(
                                    json.dumps(json.loads(topic_res), indent=4, ensure_ascii=False))
                                if "newslist" in topic_articles["data"] and topic_articles["data"]["newslist"]:
                                    for article in topic_articles["data"]["newslist"]:
                                        article_id = article["id"]
                                        url = "http://toutiao.cnwest.com/sxtoutiao/v1/getNewsDetailsV3"
                                        method = 'post'
                                        data = f"newsId={article_id}&deviceId=ffffffff-c795-b5cb-ffff-ffffc2e834d9&page=1"
                                        headers = {
                                            "Content-Type": "application/x-www-form-urlencoded",
                                            "Content-Length": "67",
                                            "Host": "toutiao.cnwest.com",
                                            "Connection": "Keep-Alive",
                                            "Accept-Encoding": "gzip",
                                            "User-Agent": "okhttp/3.10.0",
                                        }
                                        article_param = InitClass().request_params(url, headers, method, data=data)
                                        article_res = self.send_request(article_param).__next__()["request_res"]
                                        article_json = json.loads(
                                            json.dumps(json.loads(article_res), indent=4, ensure_ascii=False))
                                        article_fields = self.topic_article(article_json, channelid, channel_name)
                                        article_fields["topicid"] = _id
                                        article_fields = InitClass().wash_article_data(article_fields)
                                        if article_fields["digest"]:
                                            topic_fields["digest"] = article_fields["digest"]
                                        yield {"code": 1, "msg": "OK", "data": {"works": article_fields}}
                                    print(json.dumps(topic_fields,indent=4,ensure_ascii=False))
                                    yield {"code": 1, "msg": "OK", "data": {"topic": topic_fields}}
                        else:
                            topic_id = topic_jsons["data"]["id"]
                            url = "http://toutiao.cnwest.com/sxtoutiao/getTopicClassAndNewsListV2"
                            headers = {
                                "Content-Type": "application/x-www-form-urlencoded",
                                "Content-Length": "69",
                                "Host": "toutiao.cnwest.com",
                                "Connection": "Keep-Alive",
                                "Accept-Encoding": "gzip",
                                "User-Agent": "okhttp/3.10.0",
                            }
                            data = f"userId=&deviceId=ffffffff-c795-b5cb-ffff-ffffc2e834d9&topicid={topic_id}"
                            method = "post"
                            topic_request_param = InitClass().request_params(url, headers, method, data=data)
                            topic_res = self.send_request(topic_request_param).__next__()["request_res"]
                            topic_articles = json.loads(
                                json.dumps(json.loads(topic_res), indent=4, ensure_ascii=False))
                            if "newslist" in topic_articles["data"] and topic_articles["data"]["newslist"]:
                                fields, _id = InitClass().wash_topic_data(topic_field)
                                if topic_articles["data"]["newslist"]:
                                    try:
                                        for article in topic_articles["data"]["newslist"]:
                                            article_id = article["id"]
                                            url = "http://toutiao.cnwest.com/sxtoutiao/v1/getNewsDetailsV3"
                                            method = 'post'
                                            data = f"newsId={article_id}&deviceId=ffffffff-c795-b5cb-ffff-ffffc2e834d9&page=1"
                                            headers = {
                                                "Content-Type": "application/x-www-form-urlencoded",
                                                "Content-Length": "67",
                                                "Host": "toutiao.cnwest.com",
                                                "Connection": "Keep-Alive",
                                                "Accept-Encoding": "gzip",
                                                "User-Agent": "okhttp/3.10.0",
                                            }
                                            article_param = InitClass().request_params(url, headers, method, data=data)
                                            article_res = self.send_request(article_param).__next__()["request_res"]
                                            article_json = json.loads(
                                                json.dumps(json.loads(article_res), indent=4, ensure_ascii=False))
                                            article_fields = self.topic_article(article_json, channelid, channel_name)
                                            article_fields["topicid"] = _id
                                            article_fields = InitClass().wash_article_data(article_fields)
                                            fields["digest"] = article_fields["digest"]
                                            yield {"code": 1, "msg": "OK", "data": {"works": article_fields}}
                                    except Exception as e:
                                        self.logger.info(f"{e}{topic_articles['data']['newslist']}")
                                print(json.dumps(fields, indent=4, ensure_ascii=False))
                                yield {"code": 1, "msg": "OK", "data": {"topic": fields}}
                            else:
                                self.logger.info("可能是新闻")

                else:
                    if article_res:
                        article_json = json.loads(json.dumps(json.loads(article_res), indent=4, ensure_ascii=False))
                        author = article_json["data"]["creator"]
                        content = article_json["data"]["newsContent"]
                        like_num = article_json["data"]["likeNum"]
                        comment_num = article_json["data"]["commentNum"]
                        imagess = article_json["data"]["newsPicurl"]
                        if imagess:
                            images = list()
                            for image in imagess:
                                images.append(image["url"])
                            fields["images"] = images
                        videoss = article_json["data"]["newsVideourl"]
                        if videoss:
                            videos = list()
                            videocover = list()
                            for video in videoss:
                                videos.append(video["url"])
                                videocover.append(video["picurl"])
                            fields["videos"] = videos
                            fields["videocover"] = videocover
                        fields["content"] = content
                        fields["author"] = author
                        fields["likenum"] = like_num
                        fields["commentnum"] = comment_num
                        fields = InitClass().wash_article_data(fields)
                        yield {"code": 1, "msg": "OK", "data": {"works": fields}}
        except Exception as e:
            num += 1
            self.logger.info(f"{num}解析错误{e}")


def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = ShanXiTouTiao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
