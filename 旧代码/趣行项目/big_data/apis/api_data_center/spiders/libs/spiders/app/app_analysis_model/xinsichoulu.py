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
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass
from lxml import html
from html.parser import HTMLParser


class Xinsilu(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://cmsapi.sxdaily.com.cn/mobile/index.php"
        headers = {
            "Host": "cmsapi.sxdaily.com.cn",
            "User-Agent": "æ°ä¸è·¯ 2.0 rv:1 (iPhone; iOS 12.0.1; zh_CN)",
            "Accept-Encoding": "gzip",
        }
        data = {
            "app": "mobile",
            "controller": "content",
            "action": "category",
            "version": "6.0.0"
        }

        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))
        ttname = "头条"
        ttid = '0'
        ttparam = InitClass().channel_fields(ttid, ttname)
        channelsparams.append(ttparam)
        tpname = "组图"
        tpid = "0"
        tpparam = InitClass().channel_fields(tpid, tpname)
        channelsparams.append(tpparam)

        datas = channelslists["data"]
        channel_list = datas["news"]
        for channel in channel_list:
            channelname = channel["catname"]
            channelid = channel["catid"]

            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam

    def getarticlelistparams(self, channelsres):
        method = 'get'
        channel_num = 0
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = ""  # channel.get("channeltype")  # 此处没有若有可加上，其他一样
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)

            if channelname == "组图":
                url = "http://cmsapi.sxdaily.com.cn/mobile/index.php"
                headers = {
                    "Host": "cmsapi.sxdaily.com.cn",
                    "User-Agent": "Mozilla/5.0(Linux;U;Android 2.2.1;en-us;Nexus One Build.FRG83) AppleWebKit/553.1(KHTML,like Gecko) Version/4.0 Mobile Safari/533.1",
                    "Connection": "keep-alive"
                }

                data = {
                    "app": "mobile",
                    "controller": "picture",
                    "action": "index",
                    "page": 1,
                    "time": "",
                    "classifyid": 0,
                    "version": "6.0.0",
                    "type": "mobile",
                    "phonetype": "android",
                    "thumbsize": "810"
                }
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           channelid=channelid, data=data,
                                                                           channeltype=channeltype,
                                                                           channel_index_id=channel_index_id)
                yield channel_field,[articlelist_param]
            else:
                url = "http://cmsapi.sxdaily.com.cn/mobile/index.php"
                headers = {
                    "Host": "cmsapi.sxdaily.com.cn",
                    "User-Agent": "æ°ä¸è·¯ 2.0 rv:1 (iPhone; iOS 12.0.1; zh_CN)",
                    "Accept-Encoding": "gzip",
                }
                data_banner = {
                    "app": "mobile",
                    "controller": "content",
                    "action": "slide",
                    "catid": channelid,
                    "time": 0,
                    "version": "6.0.0",
                    "thumbsize": 750
                }
                data = {
                    "app": "mobile",
                    "controller": "content",
                    "action": "index",
                    "catid": channelid,
                    "keyword": "",
                    "page": 1,
                    "time": 0,
                    "version": "6.0.0",
                    "thumbsize": 710
                }
                articlelist_param_banner = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                                  channelid=channelid, data=data_banner,
                                                                                  channeltype=channeltype, banners=1,
                                                                                  channel_index_id=channel_index_id)

                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           channelid=channelid, data=data,
                                                                           channeltype=channeltype,
                                                                           channel_index_id=channel_index_id)
                yield channel_field,[articlelist_param_banner,articlelist_param]

    @staticmethod
    def analyze_articlelists(articleslistsres):
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channel_index_id = articleslistres.get("channelindexid")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            channel_type = ""  # articleslistres.get("channeltype")
            banner = articleslistres.get("banner")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                list_data = articleslists["data"]
                for item in list_data:
                    articleid = item["contentid"]
                    articletitle = item["title"]
                    imgurl = item["thumb"]
                    des = item["description"]
                    updatetime = item["sorttime"] * 1000
                    article_covers = list()
                    article_covers.append(imgurl)
                    if channelid == "18":
                        # 专题
                        topic_fields = InitClass().topic_fields()
                        articleparam = InitClass().article_list_fields()

                        topic_fields["topicID"] = articleid
                        topic_fields["channelName"] = channelname
                        topic_fields["channelindexid"] = channel_index_id
                        topic_fields["channelID"] = channelid
                        topic_fields["channeltype"] = ""
                        topic_fields["title"] = articletitle
                        topic_fields["digest"] = des
                        topic_fields["topicCover"] = article_covers
                        topic_fields["updateTime"] = updatetime
                        topic_fields["topic"] = 1
                        yield topic_fields
                    else:

                        # 其余频道
                        comnum = item["comments"]
                        modelid = item["modelid"]

                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()

                        article_fields["channelID"] = channelid
                        article_fields["channelname"] = channelname
                        article_fields["channelindexid"] = channel_index_id
                        article_fields["channelType"] = channel_type
                        article_fields["workerid"] = articleid
                        article_fields["title"] = articletitle
                        article_fields["articlecovers"] = article_covers
                        article_fields["updatetime"] = updatetime
                        article_fields["commentnum"] = comnum
                        article_fields["banner"] = banner
                        article_fields["modelid"] = modelid
                        yield article_fields
            except Exception as e:
                logging.info(f"解析文章列表{e}")

    def getarticleparams(self,articleslistsres):
        for article in self.analyze_articlelists(articleslistsres):
            articleid = article.get("workerid")
            topic = article.get("topic")
            if topic == 1:
                articleid = article.get("topicID")
                url = "http://cmsapi.sxdaily.com.cn/mobile/index.php?app=mobile&controller=special&action=content&version=6.0.0&type=mobile&phonetype=android&thumbsize=810&contentid=" + str(
                    articleid)
                headers = {
                    "Host": "cmsapi.sxdaily.com.cn",
                    "User-Agent": "Mozilla/5.0(Linux;U;Android 2.2.1;en-us;Nexus One Build.FRG83) AppleWebKit/553.1(KHTML,like Gecko) Version/4.0 Mobile Safari/533.1",
                    "Connection": "keep-alive",
                }
                data = {}

            else:
                modelid = article["modelid"]
                if modelid == 1:

                    url = "http://cmsapi.sxdaily.com.cn/mobile/index.php?app=mobile&controller=article&action=content&version=6.0.0&thumbsize=375&phonetype=ios&contentid=" + str(
                        articleid)
                else:

                    url = "http://cmsapi.sxdaily.com.cn/mobile/index.php?app=mobile&controller=picture&action=content&version=6.0.0&thumbsize=375&phonetype=ios&contentid=" + str(
                        articleid)

                # url = "http://cmsapi.sxdaily.com.cn/mobile/index.php?app=mobile&controller=article&action=content&version=6.0.0&thumbsize=375&phonetype=ios&contentid="+str(articleid)
                headers = {
                    "Host": "cmsapi.sxdaily.com.cn",
                    "User-Agent": "æ°ä¸è·¯ 2.0 rv:1 (iPhone; iOS 12.0.1; zh_CN)",
                    "Content-Length": "0",
                    "Accept-Encoding": "gzip",
                }
                data = {}

                article["url"] = url

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
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                # print("content_s===",content_s)

                topicinfo = content_s["data"]

                shareurl = topicinfo["shareurl"]
                fields["topicUrl"] = shareurl

                articleids = list()
                newestarticleiD = ""
                newestpubtime = 0
                topicnum = 0

                channelid = fields["channelID"]
                channelname = fields["channelName"]
                topicid = fields["topicID"]
                topictitle = fields["title"]
                sections = topicinfo["data"]

                for topicitem in sections:
                    # print("topicitem==",topicitem)
                    rows = topicitem["data"]
                    # print("rows ==",rows)
                    for topicarticle in rows:
                        topicnum += 1
                        articleid = topicarticle["contentid"]
                        articleids.append(articleid)
                        articlename = topicarticle["title"]

                        # print("articleid==",articleid, "articlename==",articlename)

                        pic = topicarticle["thumb"]
                        aurl = topicarticle["shareurl"]
                        comnum = topicarticle["comments"]

                        article_fields = InitClass().article_fields()
                        article_fields["channelID"] = channelid
                        article_fields["channelname"] = channelname
                        article_fields["channelType"] = ""
                        article_fields["workerid"] = articleid
                        article_fields["title"] = articlename
                        article_fields["articlecovers"] = [pic]
                        article_fields["url"] = aurl
                        article_fields["commentnum"] = comnum
                        article_fields["banner"] = 0
                        article_fields["specialtopic"] = 1
                        article_fields["topicid"] = topicid
                        article_fields["topicTitle"] = topictitle
                        article_fields["appname"] = self.newsname

                        modelid = topicarticle["modelid"]

                        areurl = ""
                        if modelid == 1:
                            areurl = "http://cmsapi.sxdaily.com.cn/mobile/index.php?app=mobile&controller=article&action=content&version=6.0.0&type=mobile&phonetype=android&thumbsize=810&contentid=" + str(
                                articleid)
                        else:
                            areurl = "http://cmsapi.sxdaily.com.cn/mobile/index.php?app=mobile&controller=picture&action=content&version=6.0.0&type=mobile&phonetype=android&thumbsize=810&contentid=" + str(
                                articleid)

                        aheader = {
                            "Host": "cmsapi.sxdaily.com.cn",
                            "User-Agent": "Mozilla/5.0(Linux;U;Android 2.2.1;en-us;Nexus One Build.FRG83) AppleWebKit/553.1(KHTML,like Gecko) Version/4.0 Mobile Safari/533.1",
                            "Connection": "keep-alive"
                        }
                        detailres = requests.get(areurl, headers=aheader).text
                        detailjson = json.loads(json.dumps(json.loads(detailres, strict=False), indent=4,
                                                           ensure_ascii=False))
                        # print("detailjson==",detailjson)
                        adetail = detailjson["data"]
                        ptime = adetail["published"] * 1000
                        source = adetail["source"]
                        uptime = adetail["sorttime"] * 1000

                        if modelid == 1:
                            content = adetail["content"]
                            tree = html.fromstring(content)
                            name = tree.xpath('//div[@id="content-show"]')
                            name1 = html.tostring(name[0])
                            content = HTMLParser().unescape(name1.decode())
                            article_fields["content"] = content

                            try:
                                videos = InitClass().get_video(content)
                                article_fields["videos"] = videos
                            except Exception as e:
                                print("正文无视频")

                            try:
                                images = InitClass().get_images(content)
                                article_fields["images"] = images
                            except Exception as e:
                                print("正文无图片")
                        else:
                            # 图片
                            contentimages = []
                            contentimgs = adetail["images"]
                            for img in contentimgs:
                                picurl = img["image"]
                                contentimages.append(picurl)
                            article_fields["images"] = contentimages
                            article_fields["videos"] = []

                        if ptime > newestpubtime:
                            newestarticleiD = articleid
                            newestpubtime = ptime

                        article_fields["pubtime"] = ptime
                        article_fields["updatetime"] = uptime
                        article_fields["source"] = source
                        article_fields["createtime"] = 0
                        article_fields["videocover"] = []

                        print("专题内文章 == ", json.dumps(article_fields, indent=4, ensure_ascii=False))

                fields["articleIDs"] = articleids
                fields["newestArticleID"] = newestarticleiD
                fields["newestPubtime"] = newestpubtime
                fields["platformName"] = self.newsname
                fields["pubTime"] = 0
                fields["createTime"] = 0
                fields["articleNum"] = topicnum

                print("专题文章 == ", json.dumps(fields, indent=4, ensure_ascii=False))
            else:
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                    # print("content_s==",content_s)

                    modelid = fields["modelid"]

                    detail = content_s["data"]

                    pubtime = detail["published"] * 1000
                    source = detail["source"]

                    if modelid == 1:
                        # 文章
                        content = detail["content"]

                        tree = html.fromstring(content)
                        name = tree.xpath('//div[@id="content-show"]')
                        name1 = html.tostring(name[0])
                        content = HTMLParser().unescape(name1.decode())

                        fields["content"] = content

                        try:
                            videos = InitClass().get_video(content)
                            fields["videos"] = videos
                        except Exception as e:
                            print("正文无视频")

                        try:
                            images = InitClass().get_images(content)
                            fields["images"] = images
                        except Exception as e:
                            print("正文无图片")
                    else:
                        # 图片
                        contentimages = []
                        contentimgs = detail["images"]
                        for img in contentimgs:
                            picurl = img["image"]
                            contentimages.append(picurl)
                        fields["images"] = contentimages
                        fields["videos"] = []

                    fields["pubtime"] = pubtime
                    fields["source"] = source

                    fields["videocover"] = []
                    fields["createtime"] = 0

                    fields["appname"] = self.newsname
                    fields["platformID"] = self.platform_id

                    fields = InitClass().wash_article_data(fields)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}

                except Exception as e:
                    num += 1
                    logging.info(f"错误数量{num},{e}")

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Xinsilu(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
