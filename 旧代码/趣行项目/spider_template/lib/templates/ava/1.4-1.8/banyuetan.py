# -*- encoding:utf-8 -*-
"""
@功能:半月谈解析模板
@AUTHOR：Keane
@文件名：banyuetan.py
@时间：2020/12/17  17:33
"""

import json
import logging

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


class banyuetanNews(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://www.bytapp.com/byt-api/channel/channelList"
        headers = {
            "x-platform": "1",
            "Content-Type": "application/json;charset=UTF-8",
            "X-Access-Token": "",
            "channel": "android",
            "unionID": "",
            "Host": "www.bytapp.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.10.0",
            "If-Modified-Since": "Mon, 04 Jan 2021 07:47:11 GMT",
        }
        data = {
            "flag": "1",
            "userId": "",
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        print(channelsres)
        channelslists = json.loads(channelsres)
        channelparams = []
        for channel in channelslists['result']['notRegularChannelList']:
            channelid = channel['id']
            channelname = channel['channelName']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        print(channelsparams)
        articlelistsparams = []
        headers = {
            "x-platform": "1",
            "Content-Type": "application/json;charset=UTF-8",
            "X-Access-Token": "",
            "channel": "android",
            "unionID": "",
            "Host": "www.bytapp.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.10.0",
            "If-Modified-Since": "Mon, 04 Jan 2021 07:49:40 GMT",

        }
        url = "https://www.bytapp.com/byt-api/news/newsList"
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")

            data = {
                "startTime": "0",
                "channelId": channelid,
                "pageNo": "1",
                "pageSize": "10"
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
                    for articles in articleslists["result"]["newsList"]:
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        # 获取文章列表内的有用信息
                        article_id = articles["id"]
                        article_title = articles["title"]
                        pubtime = articles["startTime"]
                        article_covers = list()
                        if "imgUrlForList" in articles.keys():
                            article_covers.append("https://www.bytapp.com/"+articles["imgUrlForList"])
                        article_fields["articlecovers"] = article_covers
                        article_fields["channelID"] = channelid
                        article_fields["channelname"] = channelname
                        article_fields["channeltype"] = channel_type
                        article_fields["workerid"] = article_id
                        article_fields["title"] = article_title
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
        for article in articles:
            articleid = article.get("articleid")
            article_field = article.get("articleField")
            url = "https://www.bytapp.com/byt-api/news/newsDetail"
            headers = {
                "x-platform": "1",
                "Content-Type": "application/json;charset=UTF-8",
                "X-Access-Token": "",
                "channel": "android",
                "unionID": "",
                "Host": "www.bytapp.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.10.0",

            }
            data = {
                "newsId": articleid,
            }
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
            try:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                print(content_s)
                worker_id = content_s["result"]["id"]
                article_title = content_s["result"]["title"]
                author = content_s["result"]["author"]
                source = content_s["result"]["newsOrigin"]
                content = content_s["result"]["content"]
                readnum = content_s["result"]["visitCount"]
                url = "https://www.bytapp.com/"+content_s["result"]["htmlUrl"]
                content_type = 1
                try:
                    videocovers = list()
                    videos = InitClass().get_video(content)
                    for video in videos:
                        videocovers.append("https://www.bytapp.com/" + content_s["result"]["imgUrlForList"])
                    if len(videos):
                        content_type = 3
                    fields["videos"] = videos
                    fields["videocover"] = videocovers
                except Exception as e:
                    logging.info(f"此新闻无视频{e}")
                try:
                    imagess = InitClass().get_images(content)
                    img_list = list()
                    for img in imagess:
                        img_list.append("https://www.bytapp.com/"+img)
                    if len(img_list):
                        content_type = 2
                    fields["images"] = img_list
                except Exception as e:
                    self.logger.info(f"获取文章内图片失败{e}")
                fields["contentType"] = content_type
                fields["appname"] = self.newsname
                fields["readnum"] = readnum
                fields["url"] = url
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
    appspider = banyuetanNews("半月谈")
    appspider.run()
