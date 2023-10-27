# -*- encoding:utf-8 -*-
"""
@功能:观海新闻解析模板
@AUTHOR：Keane
@文件名：guanhai.py
@时间：2020/12/17  17:33
"""

import json
import logging

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


class guanhai(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://m-api.guanhai.com.cn/v2/start"
        headers = {
            "Host": "m-api.guanhai.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.11.0"
        }
        data = {
            "cachetime": "1610173071",
            "system_version": "6.0.1",
            "sign": "074fde63bf3ca39094df5ee19fa85540",
            "nav_width": "405",
            "time": "1610175855939",
            "sharetime": "1610171274",
            "siteid": "10001",
            "clientid": "1",
            "modules": "common:4",
            "app_version": "1.0.8",
            "device_id": "08:00:27:F8:67:71",
            "system_width": "810",
            "system_name": "android",
            "ip": "10.0.2.15",
            "device_model": "MuMu",
            "nav_height": "115",
            "system_height": "1440",
            "device_version": "AndroidMuMu",
            "type": "android"
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(channelsres)
        channelparams = []
        for channel_list in channelslists['data']['common']['menu']:
            # channel_list['name'] == '新闻' or
            if channel_list['name'] == '新闻':
                for channel in channel_list['submenu']:
                    channelid = channel['menuid']
                    channelname = channel['name']
                    if channelname != "直播":
                        channelparam = InitClass().channel_fields(channelid, channelname)
                        channelparams.append(channelparam)
        channelparams = channelparams
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        print(channelsparams)
        articlelistsparams = []
        headers = {
            "Host": "m-api.guanhai.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.11.0"
        }
        url = "https://m-api.guanhai.com.cn/v2/menudata"
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")
            data = {
                "sign": "fa75e2fc7ea739ba8d9f2239f4210fb7",
                "time": "1610178678545",
                "siteid": "10001",
                "clientid": "1",
                "modules": "common:3",
                "app_version": "1.0.8",
                "thumbrate": "2",
                "device_id": "08:00:27:F8:67:71",
                "listsiteid": "0",
                "system_name": "android",
                "ip": "10.0.2.15",
                "areas": "null,null,null",
                "type": "android",
                "page": "1",
                "slide": "0",
                "pagesize": "20",
                "menuid": channelid
            }
            method = 'get'
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid = channelid, data = data,
                                                                       channeltype = channeltype)
            articlelistsparams.append(articlelist_param)
        yield articlelistsparams

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            channel_type = articleslistres.get("channeltype")
            try:
                articleslists = json.loads(articleslists)
                print(articleslists)
                try:
                    if "data" in articleslists.keys():
                        for key,articles_arr in articleslists["data"]["common"].items():
                            if (key == 'slide' or key == 'list') and 'lists' in articles_arr.keys():
                                for articles in articles_arr['lists']:
                                    article_type = articles["appid"]
                                    if article_type == '10':
                                        topic_fields = InitClass().topic_fields()
                                        articleparam = InitClass().article_list_fields()
                                        # 获取文章列表内的有用信息
                                        article_id = articles["contentid"]
                                        article_title = articles["title"]
                                        article_type = articles["appid"]
                                        # share_url = articles['shareInfo']["shareUrl"]
                                        try:
                                            if 'published' in articles.keys():
                                                pubtime = InitClass().date_time_stamp(articles["published"])
                                                article_fields["pubtime"] = pubtime
                                        except Exception as e:
                                            logging.info(e)
                                        topic = 1
                                        topic_fields["channelName"] = channelname
                                        topic_fields["channelID"] = channelid
                                        topic_fields["channeltype"] = channel_type
                                        topic_fields["_id"] = article_id
                                        topic_fields["contentType"] = article_type
                                        # topic_fields["topicUrl"] = share_url
                                        topic_fields["topic"] = topic
                                        topic_fields["title"] = article_title
                                        # 将请求文章必需信息存入
                                        articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                        articleparam["articleid"] = article_id
                                        articlesparams.append(articleparam)
                                    elif article_type in [1,2,4]:
                                        article_fields = InitClass().article_fields()
                                        articleparam = InitClass().article_list_fields()
                                        # 获取文章列表内的有用信息
                                        article_id = articles["contentid"]
                                        article_title = articles["title"]
                                        article_type = articles["appid"]
                                        if 'source' in articles.keys():
                                            source = articles["source"]
                                            article_fields["source"] = source
                                        # share_url = articles['shareInfo']["shareUrl"]
                                        try:
                                            if 'published' in articles.keys():
                                                pubtime = InitClass().date_time_stamp(articles["published"])
                                                article_fields["pubtime"] = pubtime
                                        except Exception as e:
                                            logging.info(e)
                                        article_covers = list()
                                        article_covers.append(articles["thumb"])
                                        if article_type == 2:
                                            article_type = 6
                                        article_fields["articlecovers"] = article_covers
                                        article_fields["channelID"] = channelid
                                        article_fields["channelname"] = channelname
                                        article_fields["channeltype"] = channel_type
                                        article_fields["workerid"] = article_id
                                        article_fields["title"] = article_title
                                        article_fields["contentType"] = article_type
                                        # article_fields["url"] = share_url
                                        # article_fields["pubtime"] = pubtime
                                        # 将请求文章必需信息存入
                                        articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                        articleparam["articleid"] = article_id
                                        articlesparams.append(articleparam)
                                    elif article_type in [800003, 800005]:
                                        if 'lists' in articles.keys():
                                            for articless in articles['lists']:
                                                article_type = articless["appid"]
                                                if article_type == '10':
                                                    topic_fields = InitClass().topic_fields()
                                                    articleparam = InitClass().article_list_fields()
                                                    # 获取文章列表内的有用信息
                                                    article_id = articless["contentid"]
                                                    article_title = articless["title"]
                                                    article_type = articless["appid"]
                                                    # share_url = articless['shareInfo']["shareUrl"]
                                                    try:
                                                        if 'published' in articles.keys():
                                                            pubtime = InitClass().date_time_stamp(articles["published"])
                                                            article_fields["pubtime"] = pubtime
                                                    except Exception as e:
                                                        logging.info(e)
                                                    topic = 1
                                                    topic_fields["channelName"] = channelname
                                                    topic_fields["channelID"] = channelid
                                                    topic_fields["channeltype"] = channel_type
                                                    topic_fields["_id"] = article_id
                                                    topic_fields["contentType"] = article_type
                                                    # topic_fields["topicUrl"] = share_url
                                                    # topic_fields["pubtime"] = pubtime
                                                    topic_fields["topic"] = topic
                                                    topic_fields["title"] = article_title
                                                    # 将请求文章必需信息存入
                                                    articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                                    articleparam["articleid"] = article_id
                                                    articlesparams.append(articleparam)
                                                elif article_type in [1, 2, 4]:
                                                    article_fields = InitClass().article_fields()
                                                    articleparam = InitClass().article_list_fields()
                                                    # 获取文章列表内的有用信息
                                                    article_id = articless["contentid"]
                                                    article_title = articless["title"]
                                                    article_type = articless["appid"]
                                                    # share_url = articless['shareInfo']["shareUrl"]
                                                    try:
                                                        if 'published' in articles.keys():
                                                            pubtime = InitClass().date_time_stamp(articles["published"])
                                                            article_fields["pubtime"] = pubtime
                                                    except Exception as e:
                                                        logging.info(e)
                                                    article_covers = list()
                                                    article_covers.append(articless["thumb"])
                                                    if article_type == 2:
                                                        article_type = 6
                                                    article_fields["articlecovers"] = article_covers
                                                    article_fields["channelID"] = channelid
                                                    article_fields["channelname"] = channelname
                                                    article_fields["channeltype"] = channel_type
                                                    article_fields["workerid"] = article_id
                                                    article_fields["title"] = article_title
                                                    article_fields["contentType"] = article_type
                                                    # article_fields["url"] = share_url
                                                    # article_fields["pubtime"] = pubtime
                                                    # 将请求文章必需信息存入
                                                    articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                                    articleparam["articleid"] = article_id
                                                    articlesparams.append(articleparam)
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        for article in articles:
            articleid = article.get("articleid")
            article_field = article.get("articleField")
            topic = article_field.get("topic")
            appid = article_field.get("contentType")
            if topic == 1:
                url = "https://m-api.guanhai.com.cn/v2/special?app_version=1.0.8&sign=6b6dcea07eab992f4cd49eb697cec207&device_id=08:00:27:F8:67:71&time=1610183014224&system_name=android&ip=10.0.2.15&siteid=10001&clientid=1&modules=newcom:2&type=android"
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Content-Length": "45",
                    "Host": "m-api.guanhai.com.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.11.0"
                }
                data = {
                    "contentid": articleid,
                    "thumbrate": "2",
                    "sharesiteid": "10001",
                }
                method = 'post'
                articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            else:
                headers = {
                    "Host": "m-api.guanhai.com.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.11.0"
                }
                data = {}
                method = 'get'
                if appid == 1:
                    url = f"https://m-api.guanhai.com.cn/v2/article?app_version=1.0.8&sign=6c406dbafb21b2cd9de00c7d5c2f6901&device_id=08%3A00%3A27%3AF8%3A67%3A71&time=1610186308362&contentid={articleid}&system_name=android&ip=10.0.2.15&siteid=10001&sharesiteid=10001&clientid=1&modules=common%3A4&type=android"
                elif appid == 6:
                    url = f"https://m-api.guanhai.com.cn/v2/gallery?app_version=1.0.8&sign=e7191b119c1c0f1c75fb9534b84cd12d&device_id=08%3A00%3A27%3AF8%3A67%3A71&time=1610186165217&contentid={articleid}&system_name=android&ip=10.0.2.15&siteid=10001&sharesiteid=10001&clientid=1&modules=common%3A1&type=android"
                elif appid == 4:
                    url = f"https://m-api.guanhai.com.cn/v2/video?app_version=1.0.8&sign=6b033c4a4579734a927ab663d9b72e25&device_id=08%3A00%3A27%3AF8%3A67%3A71&time=1610186347832&contentid={articleid}&system_name=android&ip=10.0.2.15&siteid=10001&sharesiteid=10001&clientid=1&modules=common%3A2&type=android HTTP/1.1"
                if appid in [1,2,4]:
                    articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                                     article_field=article_field)
                    articleparams.append(articleparam)

        yield articleparams

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
                    json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                if 'data' in content_s.keys():
                    articlesparams = []
                    for articles in content_s["data"]["newcom"]["list"]:
                        if articles['appid'] in [1, 2, 4]:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            # 获取文章列表内的有用信息
                            article_id = articles["contentid"]
                            article_title = articles["title"]
                            article_type = articles["appid"]
                            # share_url = articles['shareInfo']["shareUrl"]
                            pubtime = InitClass().date_time_stamp(articles["published"])
                            article_covers = list()
                            article_covers.append(articles["thumb"])
                            if article_type == 2:
                                article_type = 6
                            article_fields["articlecovers"] = article_covers
                            article_fields["channelID"] = channelid
                            article_fields["channelType"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["contentType"] = article_type
                            article_fields["pubtime"] = pubtime
                            article_fields["specialtopic"] = topic
                            article_fields["channelname"] = fields.get("channelName")
                            article_fields["topicid"] = fields.get('_id')
                            article_fields["topicTitle"] = fields.get('title')
                            # 将请求文章必需信息存入
                            articleparam["articleField"] = article_fields  # 携带文章采集的数据
                            articleparam["articleid"] = article_id
                            articlesparams.append(articleparam)
                    aaaa = self.getarticleparams(articlesparams)
                    bbbb= self.getarticlehtml(aaaa.__next__())
                    self.analyzearticle(bbbb.__next__())
            else:
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                    print(content_s)
                    if 'data' in content_s.keys():
                        worker_id = content_s["data"]["common"]["contentid"]
                        article_title = content_s["data"]["common"]["title"]
                        author = content_s["data"]["common"]["property"]["propertyName"]
                        content = content_s["data"]["common"]["content"]
                        content = InitClass().wash_tag(content)
                        shareurl = content_s["data"]["common"]["share_url"]
                        pubtime = InitClass().date_time_stamp(content_s["data"]["common"]["published"])
                        contenttype = fields.get("contentType")
                        try:
                            if fields.get("contentType") == 4:
                                videos = list()
                                videos.append(content_s["data"]["common"]["video"])
                                fields["videos"] = videos
                                fields["videocover"] = fields.get("articlecovers")
                            elif fields.get("contentType") == 6:
                                img = list()
                                for imgs in  content_s["data"]["common"]["images"]:
                                    img.append(imgs['image'])
                                fields["images"] = img
                            if fields.get("contentType") != 6:
                                imagess = InitClass().get_images(content)
                                if len(imagess):
                                    contenttype = 2
                                fields["images"] = imagess
                        except Exception as e:
                            logging.info(f"此新闻无视频{e}")
                        fields["appname"] = self.newsname
                        fields["url"] = shareurl
                        fields["contentType"] = contenttype
                        fields["pubtime"] = pubtime
                        fields["title"] = article_title
                        fields["workerid"] = worker_id
                        fields["content"] = content
                        fields["author"] = author
                        print(json.dumps(fields, indent=4, ensure_ascii=False))
                except Exception as e:
                    num += 1
                    logging.info(f"错误数量{num},{e}")

    def run(self):
        appparams = self.get_app_params()
        channelsres = self.getchannels(appparams.__next__())
        channelsparams = self.analyze_channel(channelsres.__next__())
        articlelistparames = self.getarticlelistparams(channelsparams.__next__())
        articleslistsres = self.getarticlelists(articlelistparames.__next__())
        articles = self.analyze_articlelists(articleslistsres.__next__())
        articleparams = self.getarticleparams(articles.__next__())
        articlesres = self.getarticlehtml(articleparams.__next__())
        self.analyzearticle(articlesres.__next__())


if __name__ == '__main__':
    appspider = guanhai("观海新闻")
    appspider.run()
