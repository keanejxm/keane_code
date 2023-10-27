# -*- encoding:utf-8 -*-
"""
@功能:半月谈解析模板
@AUTHOR：Keane
@文件名：banyuetan.py
@时间：2020/12/17  17:33
"""

import json
import logging

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class BanYueTanNews(Appspider):

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
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(channelsres)
        for channel in channelslists['result']['notRegularChannelList']:
            channelid = channel['id']
            channelname = channel['channelName']
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam

    def getarticlelistparams(self, channelsres):
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
        channel_num = 0
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
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
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid=channelid, data=data,
                                                                       channeltype=channeltype,
                                                                       channel_index_id=channel_index_id)
            yield channel_field,[articlelist_param]

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
                    for articles in articleslists["result"]["newsList"]:
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        # 获取文章列表内的有用信息
                        article_id = articles["id"]
                        article_title = articles["title"]
                        pubtime = articles["startTime"]
                        article_covers = list()
                        if "imgUrlForList" in articles.keys():
                            article_covers.append("https://www.bytapp.com/" + articles["imgUrlForList"])
                        article_fields["articlecovers"] = article_covers
                        article_fields["channelID"] = channelid
                        article_fields["channelname"] = channelname
                        article_fields["channelindexid"] = channel_index_id
                        article_fields["channeltype"] = channel_type
                        article_fields["workerid"] = article_id
                        article_fields["title"] = article_title
                        article_fields["pubtime"] = pubtime
                        yield article_fields
                        # 将请求文章必需信息存入
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")

    def getarticleparams(self,articleslistsres):
        for article in self.analyze_articlelists(articleslistsres):
            articleid = article.get("workerid")
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
            articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                             article_field=article)
            yield [articleparam]

    def analyzearticle(self, articleres):
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
                url = "https://www.bytapp.com/" + content_s["result"]["htmlUrl"]
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
                        img_list.append("https://www.bytapp.com/" + img)
                    if len(img_list):
                        content_type = 2
                    fields["images"] = img_list
                except Exception as e:
                    self.logger.info(f"获取文章内图片失败{e}")
                fields["contentType"] = content_type
                fields["appname"] = self.newsname
                fields["platformID"] = self.platform_id
                fields["readnum"] = readnum
                fields["url"] = url
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
    appspider = BanYueTanNews(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
