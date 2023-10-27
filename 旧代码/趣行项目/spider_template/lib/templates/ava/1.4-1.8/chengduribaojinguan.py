# -*- encoding:utf-8 -*-
"""
@功能:成都日报锦观解析模板
@AUTHOR：Keane
@文件名：chengduribaojinguan.py
@时间：2020/12/17  17:33
"""

import json
import logging

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


class chengduribaojinguan(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://v5api.cdrb.com.cn/api/v2/menus/category/list"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
            "Host": "v5api.cdrb.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",

        }
        data = {
            "platform": "android",
            "clientVersionCode": "37",
            "deviceOs": "6.0.1",
            "pjCode": "cdrb_2_201503",
            "device_size": "810.0x1440.0",
            "clientVersion": "6.0.4",
            "deviceModel": "Netease-MuMu",
            "udid": "490000000245552",
            "channel": "m360"
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        navList = [
            {
                'channelid': '42',
                'channelname': '小视频',
            },
            # {
            #     'channelid': '139',
            #     'channelname': '在看',
            #     'categoryname': '/api/getShortVideo?id=139',
            # }
        ]
        channelslists = json.loads(channelsres)
        channelparams = []
        for channel in channelslists['item']['menus']:
            channelid = channel['id']
            channelname = channel['name']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)
        channelparams = channelparams + navList
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        print(channelsparams)
        articlelistsparams = []
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
            "Host": "v5api.cdrb.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")
            url = f"https://v5api.cdrb.com.cn/api/v2/articles/{channelid}"
            data = {
                "pageToken": "",
                "size": "20",
                "headPageSize": "",
                "platform": "android",
                "clientVersionCode": "37",
                "deviceOs": "6.0.1",
                "pjCode": "cdrb_2_201503",
                "device_size": "810.0x1440.0",
                "clientVersion": "6.0.4",
                "deviceModel": "Netease-MuMu",
                "udid": "490000000245552",
                "channel": "m360"
            }
            method = 'get'
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid = channelid, data = data,
                                                                       channeltype = channeltype)
            articlelistsparams.append(articlelist_param)


            url1 = f"https://v5api.cdrb.com.cn/api/v2/articles/fast/list/{channelid}"
            data1 = {
                "platform": "android",
                "clientVersionCode": "37",
                "deviceOs": "6.0.1",
                "pjCode": "cdrb_2_201503",
                "device_size": "810.0x1440.0",
                "clientVersion": "6.0.4",
                "deviceModel": "Netease-MuMu",
                "udid": "490000000245552",
                "channel": "m360",
            }
            method1 = 'get'
            articlelist_param1 = InitClass().articlelists_params_fields(url1, headers, method1, channelname,
                                                                       channelid=channelid, data=data1,
                                                                       channeltype=channeltype)
            articlelistsparams.append(articlelist_param1)
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
                    if "item" in articleslists.keys():
                        if type(articleslists['item']) is list:
                            for articles in articleslists['item']:
                                article_type = articles["type"]
                                if article_type == 'subject':
                                    # 这种类型为专题
                                    print(articles)
                                    topic_fields = InitClass().topic_fields()
                                    articleparam = InitClass().article_list_fields()
                                    # 获取文章列表内的有用信息
                                    article_id = articles["articleId"]
                                    article_title = articles["title"]
                                    article_type = articles["type"]
                                    # share_url = articles['shareUrl']
                                    # pubtime = InitClass().date_time_stamp(InitClass().format_date(articles["date"]))
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
                                elif article_type != "link":
                                    article_fields = InitClass().article_fields()
                                    articleparam = InitClass().article_list_fields()
                                    # 获取文章列表内的有用信息
                                    article_id = articles["articleId"]
                                    article_title = articles["title"]
                                    article_type = articles["type"]
                                    # share_url = articles['shareUrl']
                                    # pubtime = InitClass().date_time_stamp(InitClass().format_date(articles["date"]))
                                    # article_covers = articles["images"]
                                    # if key == "head":
                                    #     banner = 1
                                    #     article_fields["banner"] = banner
                                    article_fields["articlecovers"] = []
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

                        else:
                            for key,articles_arr in articleslists["item"].items():
                                if key == "head" or key == "list":
                                    for articles in articles_arr:
                                        article_type = articles["sysCode"]
                                        if article_type == 'subject':
                                            # 这种类型为专题
                                            topic_fields = InitClass().topic_fields()
                                            articleparam = InitClass().article_list_fields()
                                            # 获取文章列表内的有用信息
                                            article_id = articles["articleId"]
                                            article_title = articles["title"]
                                            article_type = articles["type"]
                                            # share_url = articles['shareUrl']
                                            pubtime = InitClass().date_time_stamp(InitClass().format_date(articles["date"]))
                                            topic = 1
                                            topic_fields["channelName"] = channelname
                                            topic_fields["channelID"] = channelid
                                            topic_fields["channeltype"] = channel_type
                                            topic_fields["_id"] = article_id
                                            topic_fields["contentType"] = article_type
                                            # topic_fields["topicUrl"] = share_url
                                            topic_fields["pubtime"] = pubtime
                                            topic_fields["topic"] = topic
                                            topic_fields["title"] = article_title
                                            # 将请求文章必需信息存入
                                            articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                            articleparam["articleid"] = article_id
                                            articlesparams.append(articleparam)
                                        elif article_type != "link":
                                            article_fields = InitClass().article_fields()
                                            articleparam = InitClass().article_list_fields()
                                            # 获取文章列表内的有用信息
                                            article_id = articles["articleId"]
                                            article_title = articles["title"]
                                            article_type = articles["type"]
                                            share_url = articles['shareUrl']
                                            pubtime = InitClass().date_time_stamp(InitClass().format_date(articles["date"]))
                                            article_covers = []
                                            if "images" in articles:
                                                article_covers = articles["images"]
                                            if key == "head":
                                                banner = 1
                                                article_fields["banner"] = banner
                                            article_fields["articlecovers"] = article_covers
                                            article_fields["channelID"] = channelid
                                            article_fields["channelname"] = channelname
                                            article_fields["channeltype"] = channel_type
                                            article_fields["workerid"] = article_id
                                            article_fields["title"] = article_title
                                            article_fields["contentType"] = article_type
                                            article_fields["url"] = share_url
                                            article_fields["pubtime"] = pubtime
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
        data = {
            "size": "5",
            "platform": "android",
            "clientVersionCode": "37",
            "deviceOs": "6.0.1",
            "pjCode": "cdrb_2_201503",
            "device_size": "810.0x1440.0",
            "clientVersion": "6.0.4",
            "deviceModel": "Netease-MuMu",
            "udid": "490000000245552",
            "channel": "m360",
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
            "Host": "v5api.cdrb.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",

        }
        for article in articles:
            articleid = article.get("articleid")
            article_field = article.get("articleField")
            topic = article_field.get("topic")
            if topic == 1:
                url = f"https://v5api.cdrb.com.cn/api/v2/subjects/{articleid}"
            else:
                url = f"https://v5api.cdrb.com.cn/api/v2/articles/detail/{articleid}"
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, data = data,
                                                             article_field = article_field)
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
                print(content_s)
                articlesparams = []
                if 'item' in content_s:
                    for articles_arr in content_s["item"]["blocks"]:
                        for articles in articles_arr['articles']:
                            if articles['type'] != 'link':
                                article_fields = InitClass().article_fields()
                                articleparam = InitClass().article_list_fields()
                                # 获取文章列表内的有用信息
                                article_id = articles["articleId"]
                                article_title = articles["title"]
                                article_type = articles["type"]
                                share_url = articles['shareUrl']
                                pubtime = InitClass().date_time_stamp(InitClass().format_date(articles["date"]))
                                article_covers = []
                                if "images" in articles:
                                    article_covers = articles["images"]
                                article_fields["articlecovers"] = article_covers
                                article_fields["channelID"] = channelid
                                article_fields["channeltype"] = channel_type
                                article_fields["workerid"] = article_id
                                article_fields["title"] = article_title
                                article_fields["contentType"] = article_type
                                article_fields["url"] = share_url
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
                    if "item" in content_s.keys():
                        worker_id = content_s["item"]["articleId"]
                        article_title = content_s["item"]["title"]
                        author = ""
                        source = ""
                        content= ""
                        if "authors" in content_s["item"].keys():
                            author = content_s["item"]["authors"]
                        if "source" in content_s["item"].keys():
                            source = content_s["item"]["source"]
                        if "content" in content_s["item"].keys():
                            content = content_s["item"]["content"]
                        likenum = content_s["item"]["likes"]
                        commentnum = content_s["item"]["comments"]
                        readnum = content_s["item"]["hits"]
                        contenttype = 1
                        try:
                            if content_s["item"]["type"] == "video":
                                videocovers = list()
                                videos = list()
                                videoss = content_s["item"]["medias"]
                                for video in videoss:
                                    if "type" in video and video['type'] == "video":
                                        videocover = video["resources"][-1]['url']
                                        videocovers.append(videocover)
                                        videos.append(video['image'])
                                contenttype = 4
                                fields["videos"] = videos
                                fields["videocover"] = videocovers
                            elif content_s["item"]["type"] == "film":
                                videocovers = list()
                                videos = list()
                                videoss = content_s["item"]["medias"]
                                for video in videoss:
                                    if "type" in video and video['type'] == "video":
                                        videocover = video["resources"][-1]['url']
                                        videocovers.append(videocover)
                                        videos.append(video['image'])
                                contenttype = 5
                                fields["videos"] = videos
                                fields["videocover"] = videocovers
                        except Exception as e:
                            logging.info(f"此新闻无视频{e}")
                        try:
                            imagess = InitClass().get_images(content)
                            if len(imagess):
                                contenttype = 2
                            fields["images"] = imagess
                        except Exception as e:
                            self.logger.info(f"获取文章内图片失败{e}")
                        fields["appname"] = self.newsname
                        fields["likenum"] = likenum
                        fields["contentType"] = contenttype
                        fields["commentnum"] = commentnum
                        fields["readnum"] = readnum
                        fields["title"] = article_title
                        fields["workerid"] = worker_id
                        fields["content"] = content
                        fields["source"] = source
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
    appspider = chengduribaojinguan("成都日报锦观")
    appspider.run()
