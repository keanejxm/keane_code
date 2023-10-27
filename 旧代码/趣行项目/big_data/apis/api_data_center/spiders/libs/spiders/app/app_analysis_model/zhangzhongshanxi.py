# -*- encoding:utf-8 -*-
"""
@功能:新湖南解析模板
@AUTHOR：Keane
@文件名：xinhunan.py
@时间：2020/12/17  17:33
"""

import json
import logging
import requests
import time

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class Zhangzhongshanxi(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://xzzsx.sxdaily.com.cn/app_if/getColumns"
        headers = {
            "Host": "xzzsx.sxdaily.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.0",
        }
        data = {
            "siteId": 4,
            "parentColumnId": 5556,
            "version": 0,
            "columnType": -1
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))
        toparr = channelslists["topColumns"]
        columns = channelslists["columns"]
        channelidmap = list()
        totallist = list()
        for item in toparr:
            channelid = item["columnID"]
            channelidmap.append(channelid)
            totallist.append(item)

        for item in columns:
            channelid = item["columnID"]
            if channelid in channelidmap:
                # 有重复
                print("重复频道")
            else:
                channelidmap.append(channelid)
                totallist.append(item)
        for channel in totallist:
            channelname = channel["columnName"]
            channelid = channel["columnID"]
            columnstyle = channel["columnStyle"]
            topcount = channel["topCount"]
            # print("channelname==",channelname,"channelid==",channelid,"columnstyle=",columnstyle,"topcount=",topcount)
            channelparam = InitClass().channel_fields(channelid, channelname, categoryid=topcount,
                                                      categoryname=columnstyle)
            yield channelparam

    def getarticlelistparams(self, channelsres):
        url = "https://xzzsx.sxdaily.com.cn/app_if/getArticles"
        headers = {
            "Host": "xzzsx.sxdaily.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.0"
        }
        method = 'get'
        channel_num = 0
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            categoryname = channel.get("categoryname")
            topcount = channel.get("categoryid")
            # print("channelname==",channelname,"topcount==",topcount)
            data = {
                "columnId": channelid,
                "version": 0,
                "lastFileId": 0,
                "page": 0,
                "adv": 1,
                "columnStyle": categoryname
            }
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid=channelid, data=data,
                                                                       channeltype=channeltype, banners=topcount,
                                                                       channel_index_id=channel_index_id)
            yield channel_field,[articlelist_param]

    @staticmethod
    def analyze_articlelists(articleslistsres):
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channel_index_id = articleslistres.get("channelindexid")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            # channel_type = articleslistres.get("channeltype")
            bannertag = articleslistres.get("banner")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                # print("articleslists==",articleslists)
                try:
                    datalist = articleslists["list"]
                    for article in datalist:
                        articleid = article["fileId"]
                        articletitle = article["title"]
                        pubtime = article["publishtime"]
                        pubtime = pubtime.replace(".0", "")
                        source = article["source"]
                        readnum = article["countClick"]
                        shareurl = article["shareUrl"]
                        # contenturl = article["contentUrl"]
                        sharenum = article["countShare"]
                        likenum = article["countPraise"]
                        covers = article["pic_list_title"]
                        videourl = ""
                        try:
                            videourl = article["videoUrl"]
                        except Exception as e:
                            print("列表无视频")
                        banner = 0
                        if bannertag > 0:
                            position = article["position"]
                            # print("position=",position,"bannertag==",bannertag)
                            if position <= bannertag:
                                banner = 1
                        # 0 普通新闻
                        # 3 专题
                        # 4 外链
                        articletype = article["articleType"]

                        if articletype == 3:
                            # 专题
                            topic_fields = InitClass().topic_fields()
                            articleparam = InitClass().article_list_fields()

                            articleid = article["linkID"]
                            topic_fields["topicID"] = articleid
                            topic_fields["channelName"] = channelname
                            topic_fields["channelID"] = channelid
                            topic_fields["topicUrl"] = shareurl
                            topic_fields["title"] = articletitle
                            topic_fields["topicCover"] = covers
                            topic_fields["pubTime"] = InitClass().date_time_stamp(pubtime)
                            topic_fields["original"] = source
                            topic_fields["topic"] = 1
                            topic_fields["banner"] = banner
                            yield topic_fields
                        else:

                            # print("articletype==",articletype)
                            # 普通
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()

                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channelType"] = ""
                            article_fields["workerid"] = articleid
                            article_fields["url"] = shareurl
                            article_fields["title"] = articletitle

                            article_fields["articlecovers"] = covers
                            article_fields["images"] = []
                            article_fields["source"] = source
                            article_fields["createtime"] = 0
                            article_fields["updatetime"] = 0

                            article_fields["likenum"] = likenum
                            # article_fields["sharenum"] = sharenum
                            # article_fields["playnum"] = 0
                            # article_fields["commentnum"] = 0
                            article_fields["readnum"] = readnum

                            article_fields["sharenum"] = sharenum

                            article_fields["banner"] = banner
                            article_fields["specialtopic"] = 0

                            if videourl:
                                article_fields["videos"] = [videourl]
                            else:
                                article_fields["videos"] = []

                            article_fields["videocover"] = []
                            article_fields["contentType"] = articletype
                            article_fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                            yield article_fields
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")

    def getarticleparams(self,articleslistsres):
        for article in self.analyze_articlelists(articleslistsres):
            articleid = article.get("workerid")
            channelid = article.get("channelID")
            topic = article.get("topic")
            if topic == 1:
                articleid = article.get("topicID")
                url = "https://xzzsx.sxdaily.com.cn/app_if/getColumn"
                headers = {
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
                    "Host": "xzzsx.sxdaily.com.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                data = {
                    "siteId": 4,
                    "columnId": articleid
                }
            else:

                url = "https://xzzsx.sxdaily.com.cn/app_if/getArticleContent"
                headers = {
                    "Host": "xzzsx.sxdaily.com.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.8.0"
                }
                data = {
                    "articleId": articleid,
                    "colID": channelid
                }
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                             article_field=article)
            yield [articleparam]

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            topic = fields.get("topic")
            if topic:
                try:
                    # content_s = json.loads(json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                    # print("专题content_s=",content_s)

                    topicid = fields["topicID"]
                    topictitle = fields["title"]
                    channelid = fields["channelID"]
                    channelname = fields["channelName"]
                    banner = fields["banner"]

                    # 请求专题详情
                    url = "https://xzzsx.sxdaily.com.cn/app_if/getColumns"
                    data = {
                        "siteId": 4,
                        "parentColumnId": topicid,
                        "version": 0,
                        "columnType": -1
                    }
                    header = {
                        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
                        "Host": "xzzsx.sxdaily.com.cn",
                        "Connection": "Keep-Alive",
                        "Accept-Encoding": "gzip"
                    }

                    ztlistres = requests.get(url, headers=header, params=data).text
                    ztjson = json.loads(json.dumps(json.loads(ztlistres, strict=False), indent=4, ensure_ascii=False))
                    ztsections = ztjson["columns"]

                    topicnum = 0
                    newestarticleid = ""
                    newestarticlepub = 0
                    for column in ztsections:
                        sectionid = column["columnId"]

                        # 请求专题下新闻列表
                        sectionurl = "https://xzzsx.sxdaily.com.cn/app_if/getArticles"
                        sectionheader = {
                            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
                            "Host": "xzzsx.sxdaily.com.cn",
                            "Connection": "Keep-Alive",
                            "Accept-Encoding": "gzip"
                        }
                        sectiondata = {
                            "columnId": sectionid,
                            "version": 0,
                            "lastFileId": 0,
                            "adv": 1
                        }
                        sectionres = requests.get(sectionurl, headers=sectionheader, params=sectiondata).text
                        time.sleep(0.5)
                        sectionjson = json.loads(
                            json.dumps(json.loads(sectionres, strict=False), indent=4, ensure_ascii=False))
                        sectinlist = sectionjson["list"]

                        topicnum += len(sectinlist)

                        for item in sectinlist:
                            articleid = item["fileId"]
                            articletitle = item["title"]

                            pubtime = item["publishtime"]
                            pubtime = pubtime.replace(".0", "")
                            pubtime = InitClass().date_time_stamp(pubtime)
                            if pubtime > newestarticlepub:
                                newestarticlepub = pubtime
                                newestarticleid = articleid

                            source = item["source"]
                            readnum = item["countClick"]
                            shareurl = item["shareUrl"]
                            # contenturl = item["contentUrl"]
                            sharenum = item["countShare"]
                            likenum = item["countPraise"]
                            covers = item["pic_list_title"]

                            videourl = ""
                            try:
                                videourl = item["videoUrl"]
                            except Exception as e:
                                print("列表无视频")

                            # articleType:
                            # 0 普通新闻
                            # 3 专题
                            # 4 外链
                            articletype = item["articleType"]

                            # print("articletype==", articletype)
                            # 普通
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()

                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channelType"] = ""
                            article_fields["workerid"] = articleid
                            article_fields["url"] = shareurl
                            article_fields["title"] = articletitle

                            article_fields["articlecovers"] = covers
                            article_fields["images"] = []
                            article_fields["source"] = source
                            article_fields["createtime"] = 0
                            article_fields["updatetime"] = 0

                            article_fields["likenum"] = likenum

                            article_fields["readnum"] = readnum

                            article_fields["sharenum"] = sharenum

                            article_fields["banner"] = banner
                            article_fields["specialtopic"] = 1
                            article_fields["topicid"] = topicid
                            article_fields["topicTitle"] = topictitle

                            if videourl:
                                article_fields["videos"] = [videourl]
                            else:
                                article_fields["videos"] = []

                            article_fields["videocover"] = []
                            article_fields["contentType"] = articletype
                            article_fields["pubtime"] = pubtime
                            article_fields["appname"] = self.newsname

                            articleparam["articleField"] = article_fields  # 携带文章采集的数据
                            articleparam["articleid"] = articleid
                            articleparam["channelID"] = channelid

                            detailurl = "https://xzzsx.sxdaily.com.cn/app_if/getArticleContent"
                            detailheaders = {
                                "Host": "xzzsx.sxdaily.com.cn",
                                "Connection": "Keep-Alive",
                                "Accept-Encoding": "gzip",
                                "User-Agent": "okhttp/3.8.0"
                            }
                            detaildata = {
                                "articleId": articleid,
                                "colID": channelid
                            }

                            detailres = requests.get(detailurl, headers=detailheaders, params=detaildata).text
                            time.sleep(0.5)

                            detailjson = json.loads(
                                json.dumps(json.loads(detailres, strict=False), indent=4, ensure_ascii=False))
                            # print("detailjson==",detailjson)

                            article_fields["author"] = detailjson["liability"]
                            content = detailjson["content"]
                            article_fields["content"] = content

                            try:
                                imageinfolist = detailjson["images"]
                                contentimages = list()
                                for imageinfo in imageinfolist:
                                    for imgdic in imageinfo["imagearray"]:
                                        imgurl = imgdic["imageUrl"]
                                        contentimages.append(imgurl)
                                article_fields["images"] = contentimages
                            except Exception as e:
                                print("无图片")

                            try:
                                videoinfolist = detailjson["videos"]
                                videos = list()
                                videocovers = list()
                                for videoitem in videoinfolist:
                                    for videodic in videoitem["videoarray"]:
                                        vurl = videodic["videoUrl"]
                                        vcurl = videodic["imageUrl"]
                                        videos.append(vurl)
                                        videocovers.append(vcurl)
                                article_fields["videos"] = videos
                                article_fields["videocover"] = videocovers
                            except Exception as e:
                                print("无视频")
                            print("专题内文章=====", json.dumps(article_fields, indent=4, ensure_ascii=False))

                    fields["articleNum"] = topicnum
                    fields["newestArticleID"] = newestarticleid
                    fields["platformName"] = self.newsname
                    print("大专题=====", json.dumps(fields, indent=4, ensure_ascii=False))
                except Exception as e:
                    num += 1
                    logging.info(f"错误数量{num},{e}")

            else:
                # 普通新闻
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                    # print("普通content_s==",content_s)
                    fields["appname"] = self.newsname
                    fields["platformID"] = self.platform_id
                    fields["author"] = content_s["liability"]

                    content = content_s["content"]
                    fields["content"] = content

                    try:
                        imageinfolist = content_s["images"]
                        contentimages = list()
                        for imageinfo in imageinfolist:
                            for imgdic in imageinfo["imagearray"]:
                                imgurl = imgdic["imageUrl"]
                                contentimages.append(imgurl)
                        fields["images"] = contentimages
                    except Exception as e:
                        print("无图片")

                    try:
                        videoinfolist = content_s["videos"]
                        videos = list()
                        videocovers = list()
                        for videoitem in videoinfolist:
                            for videodic in videoitem["videoarray"]:
                                vurl = videodic["videoUrl"]
                                vcurl = videodic["imageUrl"]
                                videos.append(vurl)
                                videocovers.append(vcurl)
                        fields["videos"] = videos
                        fields["videocover"] = videocovers
                    except Exception as e:
                        print("无视频 ")

                    fields = InitClass().wash_article_data(fields)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
                except Exception as e:
                    num += 1
                    logging.info(f"错误数量{num},{e}")

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Zhangzhongshanxi(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
