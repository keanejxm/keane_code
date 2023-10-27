# -*- encoding:utf-8 -*-
"""
@功能:内蒙古自治区人民政府解析模板
@AUTHOR：Keane
@文件名：ZhongGuoLan.py
@时间：2020/12/17  17:33
"""

import json
import logging

from appspider_m import Appspider
from initclass import InitClass


class NeiMengGuNews(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://www.nmg.gov.cn/jmportal/interfaces/chancates.do?siteid=2&clienttype=3&uuid=490000000245552&version=1.1.9&channelid=29&flag=47&uniquecode=1608716249366&tokenuuid=5772a31ce248977e3d8ccb163af9c2f2"
        headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
            "Host": "www.nmg.gov.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        data = {}
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(channelsres)
        channelparams = []
        for channel in channelslists['resource']:
            channelid = channel['resourceid']
            channelname = channel['resourcename']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
            "Host": "www.nmg.gov.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        data={}
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")
            if channelname == '今日关注':
                url = f'http://www.nmg.gov.cn/jmportal/interfaces/infolist.do?siteid=2&clienttype=3&version=1.1.9&uuid=490000000245552&resourceid=207,229,226,227,228,208,209,230&topid=&orderid=&time=&flag=1056&type=1&page=10&uniquecode=1608716586120&tokenuuid=62e6178460c48ef5c30b6c58d3349150'
            else:
                url = f'http://www.nmg.gov.cn/jmportal/interfaces/infolist.do?siteid=2&clienttype=3&version=1.1.9&uuid=490000000245552&resourceid={channelid}&topid=&orderid=&time=&flag=1056&type=1&page=10&uniquecode=1608716586120&tokenuuid=62e6178460c48ef5c30b6c58d3349150'
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
                    for articles_arr in articleslists["resource"]:
                        if articles_arr['resname'] != '专题':
                            for articles in articles_arr['resourcetitle']:
                                print(articles)
                                article_fields = InitClass().article_fields()
                                articleparam = InitClass().article_list_fields()
                                # 获取文章列表内的有用信息
                                article_id = articles["titleid"]
                                article_title = articles["titletext"]
                                article_type = articles["infotype"]
                                share_url = articles['url']
                                pubtime = articles["time"]
                                article_covers = list()
                                if articles["imageurl"]:
                                    article_covers = articles["imageurl"].split(',')
                                article_fields["articlecovers"] = article_covers
                                article_fields["images"] = article_covers
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
        print(articles)
        articleparams = []
        url = "http://www.nmg.gov.cn/jmportal/interfaces/infocontent.do"
        method = 'get'
        headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
            "Host": "www.nmg.gov.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        for article in articles:
            articleid = article.get("articleid")
            article_field = article.get("articleField")
            data = {
                "siteid": "2",
                "clienttype": "3",
                "version": "1.1.9",
                "uuid": "490000000245552",
                "resourceid": "",
                "titleid": articleid,
                "uniquecode": "1608717845492",
                "tokenuuid": "954e4a097e11f05574190fa9e40335c4"
            }
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
                worker_id = content_s["titleid"]
                article_title = content_s["titletext"]
                author = content_s["author"]
                source = content_s["source"]
                content = content_s["titlecontent"]
                url = content_s["downurl"]
                images = InitClass().get_images(content)
                fields["images"] = images
                fields["url"] = url
                fields["appname"] = self.newsname
                fields["title"] = article_title
                fields["workerid"] = worker_id
                fields["content"] = content
                fields["source"] = source
                fields["author"] = author
                fields['contentType'] = 2
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
    appspider = NeiMengGuNews("内蒙古自治区人民政府")
    appspider.run()
