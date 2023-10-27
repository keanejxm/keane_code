# -*- encoding:utf-8 -*-
"""
@功能:新湖南解析模板
@AUTHOR：Keane
@文件名：xinhunan.py
@时间：2020/12/17  17:33
"""

import json
import logging

from App.appspider_m import Appspider
from App.initclass import InitClass

class XinHuNan(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://video.dftoutiao.com/app_video/columns"
        headers = {
            "Host": "video.dftoutiao.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "User-Agent": "NativeEastNews/1.8.4 (iPhone; iOS 14.1; Scale/3.00)",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Content-Length": "163",
            "Accept-Encoding": "gzip, deflate, br",
        }
        data = {
            "param":"GanSuTouTiao	GSGTTIOS	84600577-81B6-44CF-BC6D-7D21563706E6	gsgtt210104	GSGTT	1.8.4	iOS 14.1	0	010804	787288D7-6B54-4D16-9D96-C51093685CB1"
        }
        method = "post"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        for channel in channelslists:
            channelname = channel["name"]
            channelid = channel["type"]
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "https://video.dftoutiao.com/app_video/getvideos"
        headers = {
            "Host": "video.dftoutiao.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "User-Agent": "NativeEastNews/1.8.4 (iPhone; iOS 14.1; Scale/3.00)",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Content-Length": "256",
            "Accept-Encoding": "gzip, deflate, br",
        }
        method = 'post'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            data = {
                "categoryId": channelid,
                "count": 20,
                "iswifi": "wifi",
                "newkey": "",
                "param": "GanSuTouTiao	GSGTTIOS	84600577-81B6-44CF-BC6D-7D21563706E6	gsgtt210104	GSGTT	1.8.4	iOS 14.1	0	010804	787288D7-6B54-4D16-9D96-C51093685CB1",
                "pgnum": 1,
                "position": "河北",
                "startkey": "",
            }
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
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent = 4, ensure_ascii = False))

                try:

                    contentlist = articleslists["data"]
                    for article in contentlist:
                        comnum = article["comment_count"]
                        author = article["dfh_nickname"]
                        videourl = article["video_link"]
                        url = article["url"]
                        # type = article["type"]
                        source = article["source"]
                        aritlcetitle = article["topic"]
                        articleid = article["dfh_uid"]
                        likenum = article["praisecnt"]

                        covers = list()
                        bigimgobj = article["lbimg"]
                        for item in bigimgobj:
                            imgurl = item["src"]
                            covers.append(imgurl)

                        article_fields = InitClass().article_fields()

                        article_fields["channelID"] = channelid
                        article_fields["channelname"] = channelname
                        article_fields["workerid"] = articleid
                        article_fields["title"] = aritlcetitle
                        article_fields["articlecovers"] = covers
                        article_fields["banner"] = 0
                        article_fields["commentnum"] = comnum
                        article_fields["author"] = author
                        article_fields["url"] = url
                        article_fields["source"] = source
                        article_fields["likenum"] = likenum

                        article_fields["videos"] = [videourl]
                        article_fields["videocover"] = covers

                        article_fields["appname"] = "甘肃头条移动端"
                        article_fields["createtime"] = 0
                        article_fields["updatetime"] = 0
                        article_fields["pubtime"] = 0

                        print("fields==", json.dumps(article_fields, indent=4, ensure_ascii=False))

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
            type = article_field.get("articletype")
            articleurl = article_field.get("url")

            url = "https://video.dftoutiao.com/app_video/morevideos"
            headers = {
                "Host": "video.dftoutiao.com",
                "Content-Type": "application/x-www-form-urlencoded",
                "Connection": "keep-alive",
                "Accept": "*/*",
                "User-Agent": "NativeEastNews/1.8.4 (iPhone; iOS 14.1; Scale/3.00)",
                "Accept-Language": "zh-Hans-CN;q=1",
                "Content-Length": "256",
                "Accept-Encoding": "gzip, deflate, br",
            }
            data = {
                "iswifi": "wifi",
                "param": "GanSuTouTiao	GSGTTIOS	84600577-81B6-44CF-BC6D-7D21563706E6	gsgtt210104	GSGTT	1.8.4	iOS 14.1	0	010804	787288D7-6B54-4D16-9D96-C51093685CB1",
                "position": "河北",
                "type": type,
                "url": articleurl
            }
            method = 'post'
            articleparam = InitClass().article_params_fields(url, headers, method, data = data,
                                                             article_field = article_field)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            topic = fields.get("topic")
            # if topic:
            #     content_s = json.loads(
            #         json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
            #     print("专题content_s=",content_s)
            try:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                print("普通content_s=",content_s)

                # likenum = content_s["praisecnt"]
                # #
                # # contentdetail = content_s["ret"]
                # # content = contentdetail["conent"]
                # # source = contentdetail["sourceid"]
                # # commentnum = contentdetail["commentnum"]
                # # likenum =contentdetail["supportcount"]
                # #
                # # pubtime = contentdetail["publishDate"]
                # # pubtime = InitClass().date_time_stamp(pubtime)
                # #
                # # shareUrl = contentdetail["shareUrl"]
                # # shareUrl = "https://app.moj.gov.cn" + shareUrl
                # #
                # # fields["pubtime"] = pubtime
                # # fields["url"] = shareUrl
                # fields["appname"] = self.newsname
                # # fields["content"] = content
                # # fields["source"] = source
                # # fields["commentnum"] = int(commentnum)
                # fields["likenum"] = likenum
                # #
                # fields["createtime"] = 0
                # fields["updatetime"] = 0
                # fields["pubtime"] = 0
                # # try:
                # #     videos = InitClass().get_video(content)
                # #     videolist = list()
                # #     for videoitem in videos:
                # #         if not "http" in videoitem:
                # #             newurl = "https://app.moj.gov.cn" + videoitem
                # #             videolist.append(newurl)
                # #     fields["videos"] = videolist
                # # except Exception as e:
                # #     print("无视频")
                # #
                # # try:
                # #     images = InitClass().get_images(content)
                # #     imglist = list()
                # #     for imgitem in images:
                # #         if not "http" in imgitem:
                # #             newurl = "https://app.moj.gov.cn" + imgitem
                # #             imglist.append(newurl)
                # #     fields["images"] = imglist
                # #
                # # except Exception as e:
                # #     print("无图片")
                #
                # print("fields==",json.dumps(fields, indent = 4, ensure_ascii = False))

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
    appspider = XinHuNan("甘肃头条移动端")
    appspider.run()
