# -*- encoding:utf-8 -*-
"""
@功能:掌上西宁解析模板
@AUTHOR：Keane
@文件名：zhangshangxining.py
@时间：2020/12/17  17:33
"""

import json
import logging

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class ZhangShangXiNingNews(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://orientalxining.zainanjing365.com/siteapp/gdmmArticleCat/list"
        headers = {
            "Connection": "close",
            "HP_AppVersion": "6.9.2",
            "HP_ModelVersion": "6.0.1",
            "phoneModels": "MuMu",
            "User-Agent": "Android versionName=6.9.2;systemVersion=6.0.1;phoneModels=MuMu",
            "Host": "orientalxining.zainanjing365.com",
            "Accept-Encoding": "gzip",
            "Cookie": "JSESSIONID=1D545DF1E839CF5C6B3ADA5853318298.node3",

        }
        data = {}
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(channelsres)
        for channel in channelslists['data']:
            channelid = channel['id']
            channelname = channel['catName']
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam

    def getarticlelistparams(self, channelsres):
        headers = {
            "HP_AppVersion": "6.9.2",
            "HP_ModelVersion": "6.0.1",
            "phoneModels": "MuMu",
            "User-Agent": "Android versionName=6.9.2;systemVersion=6.0.1;phoneModels=MuMu",
            "Host": "orientalxining.zainanjing365.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Cookie": "JSESSIONID=1D545DF1E839CF5C6B3ADA5853318298.node3"
        }
        channel_num = 0
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")
            url = "https://orientalxining.zainanjing365.com/siteapp/gdmm/list"
            data = {
                "service_name": "gdmmArticle",
                "catId": channelid,
                "currentPage": "1",
                "pageSize": "15",
                "nst": "1"
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
                    for articles in articleslists["data"]:
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        # 获取文章列表内的有用信息
                        article_id = articles["articleId"]
                        article_title = articles["title"]
                        if channelname == '短视频' or channelname == '电视':
                            article_type = 4
                        else:
                            article_type = 2
                        share_url = ''
                        pubtime = int(articles["createTime"]) * 1000
                        article_covers = list()
                        article_covers.append(articles['imgUrl'])
                        # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                        article_fields["articlecovers"] = article_covers
                        article_fields["channelID"] = channelid
                        article_fields["channelname"] = channelname
                        article_fields["channelindexid"] = channel_index_id
                        article_fields["channeltype"] = channel_type
                        article_fields["workerid"] = article_id
                        article_fields["title"] = article_title
                        article_fields["contentType"] = article_type
                        article_fields["url"] = share_url
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
            url = "https://orientalxining.zainanjing365.com/siteapp/gdmmArticle/detail"
            headers = {
                "HP_AppVersion": "6.9.2",
                "HP_ModelVersion": "6.0.1",
                "phoneModels": "MuMu",
                "User-Agent": "Android versionName=6.9.2;systemVersion=6.0.1;phoneModels=MuMu",
                "Host": "orientalxining.zainanjing365.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "Cookie": "JSESSIONID=1D545DF1E839CF5C6B3ADA5853318298.node3"
            }
            data = {
                "articleId": articleid,
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
                worker_id = content_s["data"]["articleId"]
                article_title = content_s["data"]["title"]
                author = content_s["data"]["author"]
                source = content_s["data"]["source"]
                content = content_s["data"]["content"]
                url = content_s["data"]["articleDetailUrl"]
                commentNum = content_s["data"]["commentNum"]
                try:
                    videos = InitClass().get_video(content)
                    if len(videos):
                        videoss = content_s["data"]["imgUrl"]
                        videocovers = list()
                        videocovers.append(videoss)
                        fields["videos"] = videos
                        fields["videocover"] = videocovers
                except Exception as e:
                    logging.info(f"此新闻无视频{e}")
                try:
                    imagess = list()
                    imagess.append(content_s["data"]["imgUrl"])
                    fields["images"] = imagess
                except Exception as e:
                    self.logger.info(f"获取文章内图片失败{e}")
                fields["url"] = url
                fields["commentnum"] = commentNum
                fields["appname"] = self.newsname
                fields["platformID"] = self.platform_id
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
    appspider = ZhangShangXiNingNews(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
