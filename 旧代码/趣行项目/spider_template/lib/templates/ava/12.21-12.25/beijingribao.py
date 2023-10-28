# -*- encoding:utf-8 -*-
"""
@功能:北京日报解析模板
@AUTHOR：Keane
@文件名：ZhongGuoLan.py
@时间：2020/12/17  17:33
"""

import json
import logging

from appspider_m import Appspider
from initclass import InitClass


class BeiJingRiBao(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://ie.bjd.com.cn/rest/site/api/5b165687a010550e5ddc0e6a/column/list/customer/get?udid=4b8408b015d70ec4"
        headers = {
            "app_key": "newsroom-cms",
            "app_secret": "bbbbbbaaaaaaaaaaaaa",
            "Host": "ie.bjd.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.9.0"
        }
        data = {
            "udid": "4b8408b015d70ec4"
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(channelsres)
        channelparams = []
        nav_list = [{
            "channelid": "bjrbbeijinghao",
            "channelname": "北京号"
        }]
        for channel in channelslists['data']:
            channelid = channel['uuid']
            channelname = channel['name']
            if channelname != '纸上听' and channelname != '看报' and channelname != '云课堂' and channelname != '订阅':
                channelparam = InitClass().channel_fields(channelid, channelname)
                channelparams.append(channelparam)
        channelparams = channelparams + nav_list
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []

        data = {}
        method = 'get'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            if channelname == '北京号':
                url = 'https://ie.bjd.com.cn/rest/site/api/bjrbbeijinghao/bjhStory/bjh/1/list/c/10/ls/blank/lc/10/4b8408b015d70ec4.json'
                headers = {
                    "Host": "ie.bjd.com.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.9.0"
                }
            else:
                url = f'https://ie.bjd.com.cn/rest/site/api/5b165687a010550e5ddc0e6a/story/{channelid}/list/c/10/ls/blank/lc/0.json'
                headers = {
                    "app_key": "newsroom-cms",
                    "app_secret": "bbbbbbaaaaaaaaaaaaa",
                    "Host": "ie.bjd.com.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.9.0"
                }
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid = channelid, data = data,)
            articlelistsparams.append(articlelist_param)
        yield articlelistsparams

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(articleslists)
                try:
                    for key,value in articleslists["data"].items():
                        if (channelname == '北京号' and (key == 'bjhList' or key == 'bjhRecommends')) or key == 'list' or key == 'recommends' or key == 'sticks':
                            for articles in value:
                                if articles['title'] != '2020首页横划圆角':
                                    article_type = articles["contentType"]
                                    if article_type == 1:
                                        # 这种类型为专题
                                        print(articles)
                                        topic_fields = InitClass().topic_fields()
                                        articleparam = InitClass().article_list_fields()
                                        # 获取文章列表内的有用信息
                                        article_id = articles["specialId"]
                                        article_title = articles["title"]
                                        article_type = articles["contentType"]
                                        share_url = articles['shareUrl']
                                        pubtime = pubtime
                                        topic = 1
                                        topic_fields["channelName"] = channelname
                                        topic_fields["channelID"] = channelid
                                        topic_fields["_id"] = article_id
                                        topic_fields["contentType"] = article_type
                                        topic_fields["topicUrl"] = share_url
                                        topic_fields["pubtime"] = pubtime
                                        topic_fields["topic"] = topic
                                        topic_fields["title"] = article_title
                                        # 将请求文章必需信息存入
                                        articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                        articleparam["articleid"] = article_id
                                        articlesparams.append(articleparam)
                                    else:
                                        article_fields = InitClass().article_fields()
                                        articleparam = InitClass().article_list_fields()
                                        if key == 'recommends':
                                            article_fields['banner'] = 1
                                        # 获取文章列表内的有用信息
                                        article_id = articles["jsonUrl"]
                                        article_title = articles["title"]
                                        article_type = articles["contentType"]
                                        share_url = articles['shareUrl']
                                        pubtime = articles["publishTime"]
                                        if channelname == '北京号':
                                            worker_id = articles["storyId"]
                                            article_id = f'https://ie.bjd.com.cn:443/a/202012/22/{worker_id}.json'
                                        article_fields["channelID"] = channelid
                                        article_fields["channelname"] = channelname
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
        print(articles)
        articleparams = []
        for article in articles:
            articleid = article.get("articleid")
            article_field = article.get("articleField")
            topic = article_field.get("topic")
            if topic == 1:
                url = f"https://ie.bjd.com.cn/rest/site/api/5b165687a010550e5ddc0e6a/story/special/{articleid}/pinned/list/blank/lc/0.json"
                headers = {
                    "app_key": "newsroom-cms",
                    "app_secret": "bbbbbbaaaaaaaaaaaaa",
                    "Host": "ie.bjd.com.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.9.0"
                }
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            else:
                url = articleid
                headers = {}
                data = {}
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
            channelname = fields.get("channelname")
            channelid = article.get("channelid")

            if topic:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                articlesparams = []
                if content_s["data"]['appStoryDSList']:
                    for articles in content_s["data"]["appStoryDSList"]:
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        article_id = articles["jsonUrl"]
                        article_title = articles["title"]
                        article_type = articles["contentType"]
                        share_url = articles['shareUrl']
                        pubtime = articles["publishTime"]
                        article_fields["channelID"] = channelid
                        article_fields["channelname"] = fields.get("channelName")
                        article_fields["workerid"] = article_id
                        article_fields["title"] = article_title
                        article_fields["contentType"] = article_type
                        article_fields["url"] = share_url
                        article_fields["pubtime"] = pubtime
                        article_fields["specialtopic"] = 1
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
                    for key,value in content_s["data"]["subSpecialsStories"].items():
                        for articles in value:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = articles["jsonUrl"]
                            article_title = articles["title"]
                            article_type = articles["contentType"]
                            share_url = articles['shareUrl']
                            pubtime = articles["publishTime"]
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["contentType"] = article_type
                            article_fields["url"] = share_url
                            article_fields["pubtime"] = pubtime
                            article_fields["specialtopic"] = 1
                            article_fields["topicid"] = fields.get('_id')
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
                    worker_id = content_s["id"]
                    article_title = content_s["title"]
                    author = content_s["author"]
                    source = content_s["source"]
                    content = content_s["content"]
                    contentType = 2
                    try:
                        if content_s["content"]["mediaStream"]["url"]:
                            videocovers = list()
                            videos = list()
                            videoss = content_s["content"]["mediaStream"]["url"]
                            videocovers.append(content_s["thumbnails"][0]["url"])
                            videos.append(videoss)
                            fields["videos"] = videos
                            fields["videocover"] = videocovers
                            contentType = 4
                    except Exception as e:
                        logging.info(f"此新闻无视频{e}")
                    try:
                        images = InitClass().get_images(content)
                        fields["images"] = images
                        fields["articlecovers"] = images
                    except Exception as e:
                        self.logger.info(f"获取文章内图片失败{e}")
                    fields["contentType"] = contentType
                    fields["appname"] = self.newsname
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
    appspider = BeiJingRiBao("北京日报")
    appspider.run()
