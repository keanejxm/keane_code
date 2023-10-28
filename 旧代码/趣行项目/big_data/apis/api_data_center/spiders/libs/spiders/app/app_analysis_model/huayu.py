# -*- encoding:utf-8 -*-
"""
@功能:华舆解析模板
@AUTHOR：Keane
@文件名：huayu.py
@时间：2020/12/17  17:33
"""

import json
import logging

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class HuaYuNews(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://apps2.newsduan.com/newsyun/forApp/getAllMyOrderByUserId.jspx"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "48",
            "Host": "apps2.newsduan.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.0"
        }
        data = {
            "appToken": "v963e1609726631299",
            "userId": "",
            "isPushType": "1"
        }
        method = "post"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        navList = [
            {
                'orderId': '600',
                'orderName': '北京'
            },
            {
                'orderId': '1234',
                'orderName': '华媒'
            }
        ]
        channelslists = json.loads(channelsres)
        for channel in channelslists['msg'] + navList:
            channelid = channel['orderId']
            channelname = channel['orderName']
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam

    def getarticlelistparams(self, channelsres):
        channel_num = 0
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            if channelname == '北京':
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Content-Length": "59",
                    "Host": "apps2.newsduan.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "Cookie": "clientlanguage=zh_CN",
                    "User-Agent": "okhttp/3.8.0",
                }
                data = {
                    "appToken": "v963e1609726631299",
                    "contentIds": "0",
                    "cityId": channelid,
                    "userId": "",
                }
                method = 'post'
                url = "http://apps2.newsduan.com/newsyun/forApp/getContentsByCId.jspx"
            elif channelname == '华媒':
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Content-Length": "7",
                    "Host": "apps2.newsduan.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.8.0",
                }
                data = {
                    "userId": "",
                }
                method = 'post'
                url = "http://apps2.newsduan.com/newsyun/forApp/getJxChannelList.jspx"
            else:
                headers = {
                    "Host": "apps2.newsduan.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "Cookie": "clientlanguage=zh_CN",
                    "User-Agent": "okhttp/3.8.0"
                }
                data = {
                    "orderId": channelid,
                    "appToken": "v963e1609726631299",
                    "pageNo": "1",
                    "channelType": "1",
                    "contentIds": "0",
                    "userId": "",
                }
                url = "http://apps2.newsduan.com/newsyun/forApp/getOrderContentList.jspx"
                method = 'get'
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid=channelid, data=data,
                                                                       channeltype=channeltype,
                                                                       channel_index_id=channel_index_id)
            yield channel_field, [articlelist_param]

    @staticmethod
    def analyze_articlelists(articleslistsres):
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channel_index_id = articleslistres.get("channelindexid")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            channel_type = articleslistres.get("channeltype")
            try:
                articleslists = json.loads(articleslists)
                if channelname == '华媒':
                    for articles_arr in articleslists["msg"]:
                        for articles in articles_arr['listChannelApp']:
                            topic_fields = InitClass().topic_fields()
                            articleparam = InitClass().article_list_fields()
                            # 获取文章列表内的有用信息
                            article_id = articles["channelId"]
                            article_title = articles["channelName"]
                            topic = 1
                            topic_fields["channelName"] = channelname
                            topic_fields["channelindexid"] = channel_index_id
                            topic_fields["channelID"] = channelid
                            topic_fields["topicID"] = article_id
                            topic_fields["topic"] = topic
                            topic_fields["title"] = article_title
                            yield topic_fields
                            # 将请求文章必需信息存入
                else:
                    try:
                        for articles in articleslists["data"]["generalContent"]:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            # 获取文章列表内的有用信息
                            article_id = articles["contentId"]
                            article_title = articles["contentTitile"]
                            article_type = articles["type"]
                            share_url = articles['contentUrl']
                            pubtime = InitClass().date_time_stamp(articles["contentDateFormat"])
                            article_covers = list()
                            if 'contentTitleImg' in articles.keys():
                                article_covers.append('http://www.newsduan.com' + articles["contentTitleImg"])
                            article_fields["articlecovers"] = article_covers
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channelindexid"] = channelname
                            article_fields["channeltype"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["contentType"] = article_type
                            article_fields["url"] = share_url
                            article_fields["pubtime"] = pubtime
                            yield article_fields
                    except Exception as e:
                        logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")

    def getarticleparams(self,articleslistsres):
        articleparams = []
        for article in self.analyze_articlelists(articleslistsres):
            articleid = article.get("workerid")
            topic = article.get("topic")
            if topic == 1:
                articleid = article.get("topicID")
                url = "http://apps2.newsduan.com/newsyun/forApp/getContentListByChannelId.jspx"
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Content-Length": "86",
                    "Host": "apps2.newsduan.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "Cookie": "clientlanguage=zh_CN",
                    "User-Agent": "okhttp/3.8.0"
                }
                data = {
                    "versionId": "3",
                    "pageIndex": "1",
                    "appToken": "v963e1609726631299",
                    "pageSize": "15",
                    "userId": "",
                    "channelId": articleid,
                }
            else:
                url = "http://apps2.newsduan.com/newsyun/forApp/getContentByContentId.jspx"
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Content-Length": "64",
                    "Host": "apps2.newsduan.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "Cookie": "clientlanguage=zh_CN",
                    "User-Agent": "okhttp/3.8.0",
                }
                data = {
                    "versionId": "3",
                    "appToken": "v963e1609726631299",
                    "contentId": articleid,
                    "userId": "",
                }
            method = 'post'
            articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                             article_field=article)
            yield [articleparam]

    def analyzearticle(self, articleres):
        print(articleres)
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            topic = fields.get("topic")
            channelid = article.get("channelid")
            channel_type = article.get("channeltype")
            if topic:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                articlesparams = []
                for articles in content_s["msg"]:
                    article_fields = InitClass().article_fields()
                    articleparam = InitClass().article_list_fields()
                    # 获取文章列表内的有用信息
                    article_id = articles["contentId"]
                    article_title = articles["contentTitile"]
                    article_type = articles["type"]
                    share_url = articles['contentUrl']
                    pubtime = InitClass().date_time_stamp(articles["contentDateFormat"])
                    article_covers = list()
                    if 'contentTitleImg' in articles.keys():
                        article_covers.append('http://www.newsduan.com' + articles["contentTitleImg"])
                    article_fields["articlecovers"] = article_covers
                    article_fields["channelID"] = channelid
                    article_fields["channelname"] = fields.get('channelName')
                    article_fields["channeltype"] = channel_type
                    article_fields["workerid"] = article_id
                    article_fields["title"] = article_title
                    article_fields["contentType"] = article_type
                    article_fields["url"] = share_url
                    article_fields["pubtime"] = pubtime
                    article_fields["specialtopic"] = topic
                    article_fields["topicid"] = fields.get('_id')
                    article_fields["topicTitle"] = fields.get('title')
                    # 将请求文章必需信息存入
                    articleparam["articleField"] = article_fields  # 携带文章采集的数据
                    articleparam["articleid"] = article_id
                    articlesparams.append(articleparam)
                aaaa = self.getarticleparams(articlesparams)
                bbbb = self.getarticlehtml(aaaa.__next__())
                self.analyzearticle(bbbb.__next__())
            else:
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                    print(content_s)
                    worker_id = content_s["msg"][0]["contentId"]
                    article_title = content_s["msg"][0]["contentTitile"]
                    author = content_s["msg"][0]["contentAuthor"]
                    source = content_s["msg"][0]["contentOrigin"]
                    content = content_s["msg"][0]["contentText"]
                    commentnum = content_s["msg"][0]["commentCount"]
                    readnum = content_s["msg"][0]["viewCount"]
                    url = content_s["msg"][0]["contentUrl"]
                    try:
                        videocovers = list()
                        videos = list()
                        videoss = content_s["msg"][0]["contentVideo"]
                        if videoss:
                            videocovers.append(content_s["msg"][0]["videoBgImg"])
                            videos.append(videoss)
                        fields["videos"] = videos
                        fields["videocover"] = videocovers
                    except Exception as e:
                        logging.info(f"此新闻无视频{e}")
                    try:
                        imagess = InitClass().get_images(content)
                        img_list = list()
                        for img in imagess:
                            img_list.append('http://www.newsduan.com' + img)
                        fields["images"] = img_list
                    except Exception as e:
                        self.logger.info(f"获取文章内图片失败{e}")
                    fields["appname"] = self.newsname
                    fields["platformID"] = self.platform_id
                    fields["url"] = url
                    fields["commentnum"] = commentnum
                    fields["readnum"] = readnum
                    fields["title"] = article_title
                    fields["workerid"] = worker_id
                    fields["content"] = content
                    fields["source"] = source
                    fields["author"] = author
                    fields = InitClass().wash_article_data(fields)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
                except Exception as e:
                    num += 1
                    logging.info(f"错误数量{num},{e}")

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = HuaYuNews(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
