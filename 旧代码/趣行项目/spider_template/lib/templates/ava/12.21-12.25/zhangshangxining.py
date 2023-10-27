# -*- encoding:utf-8 -*-
"""
@功能:掌上西宁解析模板
@AUTHOR：Keane
@文件名：zhangshangxining.py
@时间：2020/12/17  17:33
"""

import json
import logging

from appspider_m import Appspider
from initclass import InitClass


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
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(channelsres)
        channelparams = []
        for channel in channelslists['data']:
            channelid = channel['id']
            channelname = channel['catName']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        print(channelsparams)
        articlelistsparams = []
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
        for channel in channelsparams:
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
                        pubtime = int(articles["createTime"])*1000
                        article_covers = list()
                        article_covers.append(articles['imgUrl'])
                        # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
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
        for article in articles:
            articleid = article.get("articleid")
            article_field = article.get("articleField")
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
    appspider = ZhangShangXiNingNews("掌上西宁")
    appspider.run()
