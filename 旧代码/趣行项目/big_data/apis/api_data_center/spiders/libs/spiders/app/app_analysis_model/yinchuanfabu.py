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


class Yinchuanfabu(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://ycapi.ycfbapp.com/api/v2/menus?tabType=1&platform=android&clientVersionCode=78&deviceOs=6.0.1&pjCode=code_ycrb&device_size=1170.0x1872.0&clientVersion=6.0.4&deviceModel=Netease-MuMu&udid=008796757400929&channel=qq"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
            "Host": "ycapi.ycfbapp.com",
            "Accept-Encoding": "gzip",
            "Connection": "keep-alive"
        }
        data = {
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))
        channellist = channelslists["items"]
        for channel in channellist:
            channelname = channel["name"]
            channelid = channel["categoryId"]
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam

    def getarticlelistparams(self, channelsres):
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
            "Host": "ycapi.ycfbapp.com",
            "Accept-Encoding": "gzip",
            "Connection": "keep-alive"
        }
        method = 'get'
        data = {
            "pageToken": "",
            "size": 20,
            "headPageSize": "",
            "platform": "android",
            "clientVersionCode": 78,
            "deviceOs": "6.0.1",
            "pjCode": "code_ycrb",
            "device_size": "1170.0x1872.0",
            "clientVersion": "6.0.4",
            "deviceModel": "Netease-MuMu",
            "udid": "008796757400929",
            "channel": "qq"
        }
        channel_num = 0
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = ""  # channel.get("channeltype")  # 此处没有若有可加上，其他一样
            url = "http://ycapi.ycfbapp.com/api/v2/articles/" + str(channelid)
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
    def formatearticlelist(article, channelid, channelname, channeltype, bannertag):

        articleid = article["articleId"]
        articletitle = article["title"]

        covers = []
        try:
            covers = article["images"]
        except Exception as e:
            print("无封面")

        # common、video、image、audio、help、live
        # link
        # subject
        articletype = article["type"]
        # print("articletype=",articletype,"articletitle=",articletitle)

        if articletype == 'common' or articletype == 'video' or articletype == "image" or articletype == "audio" or articletype == 'help' or articletype == "live":
            # return
            article_fields = InitClass().article_fields()
            articleparam = InitClass().article_list_fields()
            article_fields["channelID"] = channelid
            article_fields["channelname"] = channelname
            article_fields["channelType"] = channeltype
            article_fields["workerid"] = articleid
            article_fields["articlecovers"] = covers
            article_fields["banner"] = bannertag

            if articletype == "live":
                article_fields["livetag"] = 1
            else:
                article_fields["livetag"] = 0

            articleparam["articleField"] = article_fields  # 携带文章采集的数据
            articleparam["articleid"] = articleid
            articleparam["articletype"] = articletype
            return articleparam

        elif articletype == 'subject':

            # 专题新闻
            topic_fields = InitClass().topic_fields()
            articleparam = InitClass().article_list_fields()

            topic_fields["topicID"] = articleid
            topic_fields["channelName"] = channelname
            topic_fields["channelID"] = channelid
            topic_fields["channelType"] = channeltype
            # topic_fields["topicUrl"] = url
            topic_fields["livetag"] = 0
            topic_fields["topic"] = 1
            topic_fields["banner"] = bannertag
            articleparam["articleField"] = topic_fields  # 携带文章采集的数据
            articleparam["articleid"] = articleid
            articleparam["channelname"] = channelname

            return articleparam

        elif articletype == 'link':
            # 外链

            articleid = article["articleId"]
            articletitle = article["title"]
            url = article["shareUrl"]
            covers = article["images"]
            likenum = article["likes"]
            readnum = article["hits"]
            commentnum = article["comments"]
            pubtime = article["date"]
            pubtime = pubtime.replace("+0800", "")
            pubtime = pubtime.replace("T", " ")
            pubtime = InitClass().date_time_stamp(pubtime)

            source = ""
            createtime = 0
            updatetime = 0

            article_fields = InitClass().article_fields()
            article_fields["channelID"] = channelid
            article_fields["channelname"] = channelname
            article_fields["channelType"] = channeltype
            article_fields["workerid"] = articleid
            article_fields["articlecovers"] = covers
            article_fields["banner"] = bannertag

            article_fields["title"] = articletitle
            article_fields["source"] = source
            article_fields["createtime"] = createtime

            article_fields["appname"] = "银川发布"
            article_fields["url"] = url
            article_fields["pubtime"] = pubtime
            article_fields["updatetime"] = updatetime
            article_fields["likenum"] = likenum
            article_fields["readnum"] = readnum
            article_fields["commentnum"] = commentnum

            print("外链==", json.dumps(article_fields, indent=4, ensure_ascii=False))
        else:
            print("未知 ", article)
            print("articletype=", articletype, "articletitle=", articletitle)

    # @staticmethod
    def analyze_articlelists(self, articleslistsres):
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channel_index_id = articleslistres.get("channelindexid")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            channel_type = articleslistres.get("channelType")
            banner = articleslistres.get("banner")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    datalist = articleslists["item"]
                    try:
                        bannerlist = datalist["head"]
                        for article in bannerlist:
                            articleparam = self.formatearticlelist(article, channelid, channelname, channel_type, 1)
                            articleparam["channelindexid"] = channel_index_id
                            if articleparam:
                                yield articleparam
                    except Exception as e:
                        print("无banner", e)

                    try:
                        contentlist = datalist["list"]
                        for article in contentlist:
                            articleparam = self.formatearticlelist(article, channelid, channelname, channel_type, 0)
                            articleparam["channelindexid"] = channel_index_id
                            if articleparam:
                                yield articleparam
                    except Exception as e:
                        print("无list", e)
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e, channelname}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")

    @staticmethod
    def getarticleparams(articles):
        for article in articles:
            articleid = article.get("workerid")
            topic = article.get("topic")
            if topic == 1:
                url = "http://ycapi.ycfbapp.com/api/v2/subjects/" + str(article.get("topicID"))
                headers = {
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
                    "Host": "ycapi.ycfbapp.com",
                    "Accept-Encoding": "gzip",
                    "Connection": "keep-alive"
                }
                data = {
                    "size": 5,
                    "platform": "android",
                    "clientVersionCode": 78,
                    "deviceOs": "6.0.1",
                    "pjCode": "code_ycrb",
                    "device_size": "1170.0x1872.0",
                    "clientVersion": "6.0.4",
                    "deviceModel": "Netease-MuMu",
                    "udid": "008796757400929",
                    "channel": "qq"
                }
                method = 'get'
            else:
                livetag = article["livetag"]
                if livetag == 1:
                    url = "http://ycapi.ycfbapp.com/api/v2/live/detail/" + str(articleid)
                else:
                    url = "http://ycapi.ycfbapp.com/api/v2/articles/detail/" + str(articleid)
                headers = {
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
                    "Host": "ycapi.ycfbapp.com",
                    "Accept-Encoding": "gzip",
                    "Connection": "keep-alive"
                }
                data = {
                    "platform": "android",
                    "clientVersionCode": "78",
                    "deviceOs": "6.0.1",
                    "pjCode": "code_ycrb",
                    "device_size": "1170.0x1872.0",
                    "clientVersion": "6.0.4",
                    "deviceModel": "Netease-MuMu",
                    "udid": "008796757400929",
                    "channel": "qq"
                }
                method = 'get'

            articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                             article_field=article)
            yield [articleparam]

    @staticmethod
    def formatearticledetail(article, fields):

        article_title = article["title"]

        livetag = 0
        try:
            livetag = fields["livetag"]
        except Exception as e:
            print("无")

        if livetag == 1:
            # print("article=",article,"fields=",fields)

            fields["title"] = article_title

            cover = article["image"]
            covers = list()
            covers.append(cover)

            url = article["shareUrl"]
            readnum = article["hits"]

            pubtime = article["date"]
            pubtime = pubtime.replace("+0800", "")
            pubtime = pubtime.replace("T", " ")
            pubtime = InitClass().date_time_stamp(pubtime)

            fields["pubtime"] = pubtime
            fields["url"] = url
            fields["readnum"] = readnum
            fields["articlecovers"] = covers
            fields["createtime"] = 0
            fields["updatetime"] = 0
            return fields

        else:

            type = article["type"]
            source = ""
            try:
                source = article["source"]
            except Exception as e:
                print("无source")

            likenum = article["likes"]
            readnum = article["hits"]
            commentnum = article["comments"]
            sharenum = article["shareCounts"]

            url = article["shareUrl"]

            pubtime = article["date"]
            pubtime = pubtime.replace("+0800", "")
            pubtime = pubtime.replace("T", " ")
            pubtime = InitClass().date_time_stamp(pubtime)

            uptime = 0
            createtime = 0
            author = ""

            fields["title"] = article_title
            fields["updatetime"] = uptime
            fields["pubtime"] = pubtime
            fields["createtime"] = createtime
            fields["url"] = url

            fields["source"] = source
            fields["commentnum"] = commentnum
            fields["likenum"] = likenum
            fields["readnum"] = readnum
            fields["sharenum"] = sharenum
            fields["author"] = author

            if type == "video":

                meidalist = article["medias"]
                videos = list()
                videocovers = list()

                for media in meidalist:
                    coverurl = media["image"]
                    videocovers.append(coverurl)

                    resources = media["resources"]
                    for videoitem in resources:
                        vurl = videoitem["url"]
                        videos.append(vurl)
                        break
                fields["videos"] = videos
                fields["videocover"] = videocovers
            elif type == "image":

                contentimages = list()
                medias = article["medias"]
                for imageitem in medias:
                    imgurl = imageitem['image']
                    contentimages.append(imgurl)

                fields["images"] = contentimages
            elif type == "audio":

                audios = list()
                audiocovers = list()

                mediaslist = article["medias"]
                for media in mediaslist:
                    coverurl = media["image"]
                    audiocovers.append(coverurl)

                    resources = media["resources"]
                    for audioitem in resources:
                        vurl = audioitem["url"]
                        audios.append(vurl)
                        break

                fields["videos"] = audios
                fields["videocover"] = audiocovers
            elif type == "link":
                print("link")
            else:
                content = article["content"]
                fields["content"] = content
                fields["videocover"] = []

                try:
                    videos = InitClass().get_video(content)
                    fields["videos"] = videos

                except Exception as e:
                    print("无视频")

                try:
                    images = InitClass().get_images(content)
                    fields["images"] = images
                except Exception as e:
                    print("无图片")

            return fields

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            topic = fields.get("topic")
            content_s = json.loads(
                json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
            # print("content_s=", content_s)
            try:

                if topic == 1:

                    channelid = fields["channelID"]
                    channelname = fields["channelName"]
                    bannertag = fields["banner"]

                    contentdetail = content_s["item"]

                    topictitle = contentdetail["title"]
                    topicid = contentdetail["id"]

                    pubtime = contentdetail["date"]
                    pubtime = pubtime.replace("+0800", "")
                    pubtime = pubtime.replace("T", " ")
                    pubtime = InitClass().date_time_stamp(pubtime)

                    cover = contentdetail["image"]
                    covers = list()
                    covers.append(cover)

                    url = contentdetail["shareUrl"]

                    des = ""

                    fields["title"] = topictitle
                    fields["digest"] = des
                    fields["topicCover"] = covers
                    fields["topicUrl"] = url
                    fields["pubTime"] = pubtime
                    fields["createTime"] = 0
                    fields["updateTime"] = 0

                    topicnum = 0
                    newestarticleid = ""
                    newestpubtime = 0

                    childlist = contentdetail["blocks"]
                    for section in childlist:
                        datalist = section["articles"]
                        for article in datalist:
                            topicnum += 1

                            articleid = article["articleId"]
                            #
                            detailurl = "http://ycapi.ycfbapp.com/api/v2/articles/detail/" + str(articleid)
                            detailheaders = {
                                "Content-Type": "application/json",
                                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
                                "Host": "ycapi.ycfbapp.com",
                                "Accept-Encoding": "gzip",
                                "Connection": "keep-alive"
                            }
                            detaildata = {
                                "platform": "android",
                                "clientVersionCode": "78",
                                "deviceOs": "6.0.1",
                                "pjCode": "code_ycrb",
                                "device_size": "1170.0x1872.0",
                                "clientVersion": "6.0.4",
                                "deviceModel": "Netease-MuMu",
                                "udid": "008796757400929",
                                "channel": "qq"
                            }
                            time.sleep(0.5)
                            detailres = requests.get(detailurl, headers=detailheaders, params=detaildata).text
                            # print("detailres=",detailres)
                            detailjson = json.loads(
                                json.dumps(json.loads(detailres, strict=False), indent=4, ensure_ascii=False))

                            # print("detailjson==",detailjson)

                            # 解析专题内文章
                            article_fields = InitClass().article_fields()
                            adetail = detailjson["item"]

                            article_fields = self.formatearticledetail(adetail, article_fields)
                            article_fields["banner"] = article_fields

                            # atitle = adetail["title"]
                            # atype = adetail["type"]

                            # asource = ""
                            # try:
                            #     asource = adetail["source"]
                            # except Exception as e:
                            #     print("无source")

                            # alikenum = adetail["likes"]
                            # areadnum = adetail["hits"]
                            # acommentnum = adetail["comments"]
                            # asharenum = adetail["shareCounts"]
                            #
                            # aurl = adetail["shareUrl"]

                            try:
                                acovers = adetail["images"]
                                article_fields["articlecovers"] = acovers
                            except Exception as e:
                                print("无封面图")

                            apubtime = article_fields["pubtime"]
                            # apubtime = adetail["date"]
                            # apubtime = apubtime.replace("+0800", "")
                            # apubtime = apubtime.replace("T", " ")
                            # apubtime = InitClass().date_time_stamp(apubtime)

                            if apubtime > newestpubtime:
                                newestpubtime = apubtime
                                newestarticleid = articleid

                            # auptime = 0
                            # acreatetime = 0
                            # aauthor = ""
                            article_fields["channelname"] = channelname
                            article_fields["channelID"] = channelid
                            article_fields["workerid"] = articleid
                            article_fields["appname"] = self.newsname
                            article_fields["platformID"] = self.platform_id

                            article_fields["specialtopic"] = 1
                            article_fields["topicid"] = topictitle
                            article_fields["topicTitle"] = topicid
                            yield {"code": 1, "msg": "OK", "data": {"works": article_fields}}

                    fields["platformName"] = self.newsname
                    fields["articleNum"] = topicnum
                    fields["newestArticleID"] = newestarticleid
                    print("大专题==", json.dumps(fields, indent=4, ensure_ascii=False))
                else:

                    contentdetail = content_s["item"]
                    fields["appname"] = self.newsname
                    fields["platformID"] = self.platform_id
                    fields = self.formatearticledetail(contentdetail, fields)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}

            except Exception as e:
                num += 1
                # print("error content_s=",content_s)
                logging.info(f"错误数量{num},{e}")

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Yinchuanfabu(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
