# -*- encoding:utf-8 -*-
"""
@功能:新湖南解析模板
@AUTHOR：Keane
@文件名：xinhunan.py
@时间：2020/12/17  17:33
"""

import json
import logging
# import bs4
import requests
import time

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


class Qinghairibao(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://www.qhrbnews.com/app_if//getColumns"
        headers = {
            "Host": "www.qhrbnews.com",
            "Accept": "*/*",
            "Accept-Language": "zh-cn",
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "DZWDP/1 CFNetwork/1197 Darwin/20.0.0",
        }
        data = {
            "siteId": 1,
            "parentColumnId": 27285,
            "version": 0,
            "columnType": -1
        }

        method = "get"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []

        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        # print("channelslists==",channelslists)
        datalist = channelslists["columns"]
        for channel in datalist:
            channelname = channel["columnName"]
            channelid = channel["columnId"]
            topcount = channel["topCount"]
            show = channel.get("columnStyle")
            if show == '101':
                # print("topcount=",topcount,"channelid=",channelid,"channelname=",channelname)
                channelparam = InitClass().channel_fields(channelid, channelname,categoryid=topcount)
                channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []

        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            bannercount = channel.get("categoryid")

            url = "https://www.qhrbnews.com/app_if//getArticles"
            headers = {
                "Host": "www.qhrbnews.com",
                "Accept": "*/*",
                "Accept-Language": "zh-cn",
                "Connection": "keep-alive",
                "Accept-Encoding": "gzip, deflate, br",
                "User-Agent": "DZWDP/1 CFNetwork/1197 Darwin/20.0.0"
            }
            data = {
                "columnId": channelid,
                "lastFileId": 0,
                "page": 0,
                "version": 0,
                "adv": 1
            }
            method = "get"

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid = channelid, data = data,
                                                                       channeltype = channeltype,banners=bannercount)
            articlelistsparams.append(articlelist_param)


        yield articlelistsparams

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            channeltype = articleslistres.get("channeltype")
            banner = articleslistres.get("banner")

            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent = 4, ensure_ascii = False))
                #print("articleslists=", articleslists)
                try:

                    contentlist = articleslists["list"]
                    index = 0

                    for article in contentlist:
                        isbanner = 0
                        if index < banner:
                            isbanner = 1
                        index += 1

                        articleid = article["fileId"]
                        articletype = article["articleType"]
                        # title = article["title"]
                        #print('articletyp==',articletype,"title==",title)

                        if articletype == 3:
                            #专题
                            topic_fields = InitClass().topic_fields()
                            articleparam = InitClass().article_list_fields()

                            topic_fields["topicID"] = articleid
                            topic_fields["topic"] = 1
                            topic_fields["channelName"] = channelname
                            topic_fields["channelID"] = channelid

                            # 将请求文章必需信息存入
                            articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                            articleparam["articleid"] = articleid
                            articleparam["channelname"] = channelname
                            articlesparams.append(articleparam)
                        else:

                            #普通
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["workerid"] = articleid
                            article_fields["banner"] = isbanner

                            articleparam["articleField"] = article_fields  # 携带文章采集的数据
                            articleparam["articleid"] = articleid
                            articlesparams.append(articleparam)

                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e,channelname}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        for article in articles:
            articleid = article.get("articleid")

            article_field = article.get("articleField")
            # topic = article_field.get("topic")
            # channelname = article_field.get("channelname")
            channelid = article_field.get("channelID")

            url = "https://www.qhrbnews.com/app_if//getArticleContent"
            headers = {
                "Host": "www.qhrbnews.com",
                "Accept": "*/*",
                "Accept-Language": "zh-cn",
                "Connection": "keep-alive",
                "Accept-Encoding": "gzip, deflate, br",
                "User-Agent": "DZWDP/1 CFNetwork/1197 Darwin/20.0.0"
            }
            now = int(time.time()) * 1000
            data = {
                "articleId": articleid,
                "time": now,
                "colID": channelid,
                "siteId": 1
            }
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, data = data,
                                                             article_field = article_field)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            topic = fields.get("topic")

            try:

                content_s = json.loads(json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                # print("content_s==",content_s)

                source = content_s["source"]
                author = content_s["editor"]
                url = content_s["url"]
                covers = content_s["pic_list_title"]
                images = content_s["pic_list"]
                content = content_s["content"]
                title = content_s["title"]
                pubtime = content_s["realPubTime"]
                pubtime = pubtime.replace(".0", "")
                likenum = content_s["countPraise"]
                sharenum = content_s["countShare"]
                readnum = content_s["countClick"]

                if topic == 1:
                    linkid = content_s["linkID"]

                    channelid = fields["channelName"]
                    channelname = fields["channelID"]
                    topicid = content_s["fileId"]
                    des = content_s["attAbstract"]


                    fields["platformName"] = self.newsname
                    fields["title"] = title
                    fields["topicUrl"] = url
                    fields["digest"] = des
                    fields["topicCover"] = covers
                    fields["pubTime"] = InitClass().date_time_stamp(pubtime)
                    fields["region"] = source
                    fields["createTime"] = 0
                    fields["updateTime"] = 0

                    articlenum = 0
                    newestarticleid = ""
                    newestpubtime = 0

                    url = 'https://www.qhrbnews.com/app_if/getColumns'
                    headers = {
                        "Host": "www.qhrbnews.com",
                        "Accept": "application/json, text/plain, */*",
                        "Accept-Language": "zh-cn",
                        "Connection": "keep-alive",
                        "Accept-Encoding": "gzip, deflate, br",
                        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148/xiangyuapp",
                    }
                    now = int(time.time()) * 1000
                    data = {
                        "parentColumnId": linkid,
                        "version": 0,
                        "columnType": -1,
                        "t": now,
                        "siteId": 1,
                        "siteID": 1,
                    }
                    columnres = requests.get(url,headers=headers,params=data).text
                    columnjson = json.loads(json.dumps(json.loads(columnres, strict=False), indent=4,ensure_ascii=False))
                    # print("columnjson==",columnjson)
                    for item in columnjson["columns"]:
                        itemid = item["columnId"]

                        itemurl = 'https://www.qhrbnews.com/app_if/getArticles'
                        itemheaders = {
                            "Host": "www.qhrbnews.com",
                            "Accept": "application/json, text/plain, */*",
                            "Accept-Language": "zh-cn",
                            "Connection": "keep-alive",
                            "Accept-Encoding": "gzip, deflate, br",
                            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148/xiangyuapp",
                        }
                        itemdata = {
                            "columnId": itemid,
                            "lastFileId": 0,
                            "t": now,
                            "siteId": 1,
                            "siteID": 1
                        }
                        listres = requests.get(itemurl,headers=itemheaders,params=itemdata).text
                        listjson = json.loads(json.dumps(json.loads(listres, strict=False), indent=4, ensure_ascii=False))
                        # print("listjson==",listjson)

                        for articleitem in listjson["list"]:

                            articlenum += 1

                            contenturl = articleitem["contentUrl"]
                            detailjson = requests.get(contenturl).text
                            # print("detailjson==",detailjson)

                            detailjson = json.loads(json.dumps(json.loads(detailjson, strict=False), indent=4, ensure_ascii=False))
                            particleid = detailjson["fileId"]
                            psource = detailjson["source"]
                            pauthor = detailjson["editor"]
                            purl = detailjson["url"]
                            pcovers = detailjson["pic_list_title"]
                            pimages = detailjson["pic_list"]
                            pcontent = detailjson["content"]
                            pcontent = InitClass().wash_tag(pcontent)

                            ptitle = detailjson["title"]
                            ppubtime = detailjson["realPubTime"]
                            ppubtime = ppubtime.replace(".0", "")
                            ppubtime = InitClass().date_time_stamp(ppubtime)

                            if ppubtime > newestpubtime:
                                newestpubtime = ppubtime
                                newestarticleid = particleid

                            plikenum = detailjson["countPraise"]
                            psharenum = detailjson["countShare"]
                            preadnum = detailjson["countClick"]

                            article_fields = InitClass().article_fields()

                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["workerid"] = particleid
                            article_fields["banner"] = 0

                            article_fields["title"] = ptitle
                            article_fields["articlecovers"] = pcovers
                            article_fields["pubtime"] = ppubtime
                            article_fields["url"] = purl
                            article_fields["source"] = psource
                            article_fields["author"] = pauthor
                            article_fields["content"] = pcontent
                            article_fields["createtime"] = 0
                            article_fields["updatetime"] = 0
                            article_fields["images"] = pimages
                            videolist = list()
                            videocoverlist = list()
                            try:
                                videosinfo = detailjson["videos"]
                                for videoitem in videosinfo:
                                    varr = videoitem["videoarray"]
                                    for video in varr:
                                        vurl = video["videoUrl"]
                                        curl = video["imageUrl"]
                                        videolist.append(vurl)
                                        videocoverlist.append(curl)
                            except Exception as e:
                                print("无视频 ", e)
                            article_fields["videos"] = videolist
                            article_fields["videocover"] = videocoverlist

                            article_fields["appname"] = self.newsname

                            article_fields["likenum"] = plikenum
                            article_fields["readnum"] = preadnum
                            article_fields["sharenum"] = psharenum

                            article_fields["specialtopic"] = 1
                            article_fields["topicid"] = topicid
                            article_fields["topicTitle"] = title

                            print("专题文章==", json.dumps(article_fields, indent=4, ensure_ascii=False))

                    fields["articleNum"] = articlenum
                    fields["newestArticleID"] = newestarticleid
                    print("大专题==", json.dumps(fields, indent=4, ensure_ascii=False))

                else:

                    fields["title"] = title
                    fields["articlecovers"] = covers
                    fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                    fields["url"] = url
                    fields["source"] = source
                    fields["author"] = author
                    content = InitClass().wash_tag(content)
                    fields["content"] = content
                    fields["createtime"] = 0
                    fields["updatetime"] = 0
                    fields["images"] = images

                    videolist = list()
                    videocoverlist = list()
                    try:
                        videosinfo = content_s["videos"]
                        for videoitem in videosinfo:
                            varr = videoitem["videoarray"]
                            for video in varr:
                                vurl = video["videoUrl"]
                                curl = video["imageUrl"]
                                videolist.append(vurl)
                                videocoverlist.append(curl)
                    except Exception as e:
                        print("无视频 ",e)
                    fields["videos"] = videolist
                    fields["videocover"] = videocoverlist

                    fields["appname"] = self.newsname
                    fields["likenum"] = likenum
                    fields["readnum"] = readnum
                    fields["sharenum"] = sharenum

                    print("fields==",json.dumps(fields, indent = 4, ensure_ascii = False))

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
    appspider = Qinghairibao("青海日报")
    appspider.run()
