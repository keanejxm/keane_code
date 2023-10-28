# -*- encoding:utf-8 -*-
"""
@功能:文旅中国解析模板
@AUTHOR：Keane
@文件名：wenlvzhongguo.py
@时间：2020/12/17  17:33
"""

import json
import logging

import requests

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class WenLvZhongGuo(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://gateway.ccmapp.cn/terminal/getColumnChildByPid"
        headers = {
            "Accept": "application/json",
            "url_name": "gateway",
            "Content-Type": "application/json",
            "Host": "gateway.ccmapp.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.1",

        }
        data = {
            "token": "",
            "terminalId": "1",
            "pid": "786470b3-e509-4222-ba56-9c8b03dbc327",
            "imei": "4b8408b015d70ec4",
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(channelsres)
        for channel in channelslists['data']:
            channelid = channel['columnId']
            channelname = channel['name']
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam
        yield {"channelid": "2eeab938-cac7-4743-b45e-a7b176ff595f", "channelname": "小视频"}

    def getarticlelistparams(self, channelsres):
        headers = {
            "url_name": "gateway",
            "Content-Type": "application/json; charset=UTF-8",
            "Content-Length": "164",
            "Host": "gateway.ccmapp.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.1",
        }
        url = "https://gateway.ccmapp.cn/terminal/pullInfoStream"
        channel_num = 0
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")
            data = {}
            method = 'post'
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)

            channeljson = {"clientType": "api", "clitype": "android", "columnId": channelid, "currentPage": "1",
                           "gid": "080027f86771", "imei": "4b8408b015d70ec4", "pageSize": "10", "terminalId": "1",
                           "token": ""}
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid=channelid, data=data,
                                                                       channeltype=channeltype, channeljson=channeljson,
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
                try:
                    for articles in articleslists["data"]["list"]:
                        find1 = "CAYETORY"
                        article_type = articles["templateid"]
                        find2 = "special"
                        if find1 in article_type:
                            article_type = articles["templateid"]
                        else:
                            if "items" in articles.keys():
                                for articles_list in articles['items']:
                                    if find2 in articles_list['action']:
                                        # 这种类型为专题
                                        topic_fields = InitClass().topic_fields()
                                        articleparam = InitClass().article_list_fields()
                                        # 获取文章列表内的有用信息
                                        idlist = articles_list["action"].split(";")
                                        article_id = idlist[-1]
                                        res = requests.get(
                                            f'https://www.ccmapp.cn/middleware/getdetail?terminalId=1&type=special&id={article_id}').content.decode()
                                        topic_detail = json.loads(res)
                                        article_id = topic_detail['data']['columns'][0]['id']
                                        article_title = topic_detail['data']['title']
                                        topic = 1
                                        topic_fields["channelName"] = channelname
                                        topic_fields["channelindexid"] = channel_index_id
                                        topic_fields["channelID"] = channelid
                                        topic_fields["channeltype"] = channel_type
                                        topic_fields["topicID"] = article_id
                                        topic_fields["topic"] = topic
                                        topic_fields["title"] = article_title
                                        yield topic_fields
                                        # 将请求文章必需信息存入
                                    else:
                                        article_fields = InitClass().article_fields()
                                        articleparam = InitClass().article_list_fields()
                                        # 获取文章列表内的有用信息
                                        idlist = articles_list["action"].split(";")
                                        article_id = idlist[-1]
                                        article_title = articles_list["title"]
                                        article_covers = list()
                                        for img in articles_list["coverimage"]:
                                            article_covers.append(img['url'])
                                        share_url = "https://www.ccmapp.cn/pages/wx/apps/page/information/information-detail/information-detail.html?id=" + article_id
                                        article_fields["banner"] = 1
                                        article_fields["url"] = share_url
                                        article_fields["articlecovers"] = article_covers
                                        article_fields["channelID"] = channelid
                                        article_fields["channelname"] = channelname
                                        article_fields["channelindexid"] = channel_index_id
                                        article_fields["channeltype"] = channel_type
                                        article_fields["workerid"] = article_id
                                        article_fields["title"] = article_title
                                        yield article_fields
                            else:
                                if find2 in articles['action']:
                                    topic_fields = InitClass().topic_fields()
                                    articleparam = InitClass().article_list_fields()
                                    idlist = articles["action"].split(";")
                                    article_id = idlist[-1]
                                    res = requests.get(
                                        f'https://www.ccmapp.cn/middleware/getdetail?terminalId=1&type=special&id={article_id}').content.decode()
                                    topic_detail = json.loads(res)
                                    article_title = topic_detail['data']['title']
                                    topic = 1
                                    topic_fields["channelName"] = channelname
                                    topic_fields["channelindexid"] = channel_index_id
                                    topic_fields["channelID"] = channelid
                                    topic_fields["channeltype"] = channel_type
                                    topic_fields["topicID"] = article_id
                                    topic_fields["topic"] = topic
                                    topic_fields["title"] = article_title
                                    yield topic_fields
                                    # 将请求文章必需信息存入
                                else:
                                    if channelname == "小视频":
                                        article_fields = InitClass().article_fields()
                                        articleparam = InitClass().article_list_fields()
                                        # 获取文章列表内的有用信息
                                        article_id = articles["id"]
                                        article_title = articles["title"]

                                        pubtime = InitClass().date_time_stamp(articles["publictime"])
                                        article_covers = list()
                                        for img in articles["coverimage"]:
                                            article_covers.append(img['url'])
                                        share_url = ""
                                        article_fields["url"] = share_url
                                        likenum = articles['goodcount']
                                        source = articles['source']
                                        author = articles['author']
                                        contenttype = 5
                                        readnum = articles['pageview']
                                        videos = list()
                                        videoscover = list()
                                        videos.append(articles["attr"]["manuscripturl"])
                                        article_fields["videos"] = videos
                                        for img in articles["coverimage"]:
                                            videoscover.append(img["url"])
                                        article_fields["videocover"] = videoscover
                                        article_fields["channelindexid"] = channel_index_id
                                        article_fields["contentType"] = contenttype
                                        article_fields["title"] = article_title
                                        article_fields["content"] = ""
                                        article_fields["source"] = source
                                        article_fields["images"] = []
                                        article_fields["author"] = author
                                        article_fields["likenum"] = likenum
                                        article_fields["readnum"] = readnum
                                        article_fields["articlecovers"] = article_covers
                                        article_fields["channelID"] = channelid
                                        article_fields["channelname"] = channelname
                                        article_fields["channeltype"] = channel_type
                                        article_fields["workerid"] = article_id
                                        article_fields["title"] = article_title
                                        article_fields["pubtime"] = pubtime
                                        yield article_fields
                                        # 将请求文章必需信息存入
                                    else:
                                        article_fields = InitClass().article_fields()
                                        articleparam = InitClass().article_list_fields()
                                        # 获取文章列表内的有用信息
                                        article_id = articles["id"]
                                        article_title = articles["title"]

                                        pubtime = InitClass().date_time_stamp(articles["publictime"])
                                        article_covers = list()
                                        for img in articles["coverimage"]:
                                            article_covers.append(img['url'])
                                        if 'shareurl' in articles:
                                            share_url = articles['shareurl']
                                            article_fields["url"] = share_url
                                        likenum = articles['goodcount']
                                        readnum = articles['pageview']
                                        article_fields["likenum"] = likenum
                                        article_fields["readnum"] = readnum
                                        article_fields["articlecovers"] = article_covers
                                        article_fields["channelID"] = channelid
                                        article_fields["channelname"] = channelname
                                        article_fields["channelindexid"] = channel_index_id
                                        article_fields["channeltype"] = channel_type
                                        article_fields["workerid"] = article_id
                                        article_fields["title"] = article_title
                                        article_fields["pubtime"] = pubtime
                                        yield article_fields
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")

    def getarticleparams(self,articleslistsres):
        for article in self.analyze_articlelists(articleslistsres):
            articleid = article.get("workerid")
            topic = article.get("topic")
            if topic == 1:
                articleid = article.get("topicID")
                url = "https://gateway.ccmapp.cn/terminal/pullInfoStream"
                headers = {
                    "url_name": "gateway",
                    "Content-Type": "application/json; charset=UTF-8",
                    "Content-Length": "216",
                    "Host": "gateway.ccmapp.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.8.1",
                }
                data = {}
                articlejson = {"clientType": "api", "clitype": "android", "columnId": articleid, "currentPage": "1",
                               "gid": "080027f86771", "imei": "4b8408b015d70ec4", "pageSize": "10", "terminalId": "1",
                               "token": ""}
                method = 'post'
            else:
                url = "https://www.ccmapp.cn/middleware/getdetail"
                headers = {
                    "Host": "www.ccmapp.cn",
                    "Connection": "keep-alive",
                    "Pragma": "no-cache",
                    "Cache-Control": "no-cache",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 Html5Plus/1.0",
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,en-US;q=0.8",
                    "X-Requested-With": "com.ccmapp.news",
                }
                data = {
                    "id": articleid,
                    "token": "",
                    "type": "richtext",
                    "imei": "4b8408b015d70ec4",
                    "terminalId": "1",
                    "gid": "080027f86771",
                    "clitype": "android",
                    "uid": "",
                }
                articlejson = ""
                method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                             article_field=article, articlejson=articlejson)
            yield [articleparam]

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            topic = fields.get("topic")
            channelname = fields.get("channelname")
            channelid = article.get("channelid")
            channel_type = article.get("channeltype")
            if channelname == "小视频":
                print(json.dumps(fields, indent=4, ensure_ascii=False))
            else:
                if topic:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                    print(content_s)
                    articlesparams = []
                    for articles in content_s["data"]["list"]:
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        # 获取文章列表内的有用信息
                        article_id = articles["id"]
                        article_title = articles["title"]
                        share_url = articles['shareurl']
                        pubtime = InitClass().date_time_stamp(articles["publictime"])
                        article_covers = list()
                        for img in articles["coverimage"]:
                            article_covers.append(img['url'])
                        likenum = articles['goodcount']
                        readnum = articles['pageview']
                        article_fields["likenum"] = likenum
                        article_fields["readnum"] = readnum
                        article_fields["articlecovers"] = article_covers
                        article_fields["channelID"] = channelid
                        article_fields["channelname"] = fields.get('channelName')
                        article_fields["channeltype"] = channel_type
                        article_fields["workerid"] = article_id
                        article_fields["title"] = article_title
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
                            json.dumps(json.loads(article.get("articleres"), strict=False), indent=4,
                                       ensure_ascii=False))
                        print(content_s)
                        article_title = content_s["data"]["title"]
                        author = content_s["data"]["author"]
                        source = content_s["data"]["sourceSite"]
                        content = content_s["data"]["menuscriptdata"]["content"]
                        contenttype = content_s["data"]["menuscriptdata"]["type"]
                        pubtime = InitClass().date_time_stamp(content_s["data"]["createtime"])
                        try:
                            imagess = InitClass().get_images(content)
                            if len(imagess):
                                contenttype = 2
                            fields["images"] = imagess
                        except Exception as e:
                            self.logger.info(f"获取文章内图片失败{e}")
                        try:
                            if contenttype == "4":
                                videos = list()
                                videos.append(content_s["data"]["menuscriptdata"]["video"]["url"])
                                fields["videos"] = videos
                                fields["videocover"] = fields.get('articlecovers')
                        except Exception as e:
                            logging.info(f"此新闻无视频{e}")
                        fields["pubtime"] = pubtime
                        fields["contentType"] = contenttype
                        fields["appname"] = self.newsname
                        fields["platformID"] = self.platform_id
                        fields["title"] = article_title
                        fields["content"] = content
                        fields["source"] = source
                        fields["author"] = author
                        fields = InitClass().wash_article_data(fields)
                        yield {"code": 1, "msg": "OK", "data": {"works": fields}}
                    except Exception as e:
                        num += 1
                        logging.info(f"错误数量{num},{e}")

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = WenLvZhongGuo(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
