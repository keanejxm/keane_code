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
# import time

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass

class Jingzhouribao(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://app.cnchu.com/app/index.html"
        headers = {
            "Charset": "UTF-8",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 apicloud",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Host": "app.cnchu.com"
        }
        data = {
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        #print("channelslists==",channelslists)
        channellist = channelslists["category"]

        for channel in channellist:
            channelname = channel["catname"]
            channelid = channel["catid"]
            ismenu = channel["ismenu"]
            parentid = channel["parentid"]
            if ismenu == "1" and parentid == "0":
                channelparam = InitClass().channel_fields(channelid, channelname)
                channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        headers = {
            "Charset": "UTF-8",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 apicloud",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Host": "app.cnchu.com"
        }
        method = 'get'
        data = {}
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = ""#channel.get("channeltype")  # 此处没有若有可加上，其他一样
            url = "https://app.cnchu.com/index.php?m=content&c=index&a=lists&page=1&catid=" + str(channelid)

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,channelid = channelid, data = data,channeltype = channeltype)
            articlelistsparams.append(articlelist_param)

        yield articlelistsparams

    @staticmethod
    def formatearticlelist(article,channelid,channelname,channeltype,bannertag):

        articleid = article["id"]
        articletitle = article["title"]
        cover = article["pic"]
        covers = list()
        covers.append(cover)

        #7 专题
        #3 外链H5
        #5 有视频文章
        #0 文字
        #4 画廊
        #6 直播
        articletype = article["typeid"]

        if articletype == '0' or articletype == '5' or articletype == '4' or articletype == 6:

            article_fields = InitClass().article_fields()
            articleparam = InitClass().article_list_fields()
            article_fields["channelID"] = channelid
            article_fields["channelname"] = channelname
            article_fields["channelType"] = channeltype
            article_fields["workerid"] = articleid
            article_fields["articlecovers"] = covers
            article_fields["banner"] = bannertag

            articleparam["articleField"] = article_fields  # 携带文章采集的数据
            articleparam["articleid"] = articleid
            articleparam["articletype"] = articletype
            return articleparam

        elif articletype == '7':

            url = article["url"]

            # 专题新闻
            topic_fields = InitClass().topic_fields()
            articleparam = InitClass().article_list_fields()

            topic_fields["topicID"] = articleid
            topic_fields["channelName"] = channelname
            topic_fields["channelID"] = channelid
            topic_fields["channelType"] = channeltype
            topic_fields["topicUrl"] = url

            topic_fields["topic"] = 1

            topic_fields["banner"] = bannertag

            articleparam["articleField"] = topic_fields  # 携带文章采集的数据
            articleparam["articleid"] = articleid
            articleparam["channelname"] = channelname
            return articleparam

        elif articletype == '3':
            #外链
            createtime = 0
            source = ""
            title = article["title"]

            article_fields = InitClass().article_fields()
            article_fields["channelID"] = channelid
            article_fields["channelname"] = channelname
            article_fields["channelType"] = channeltype
            article_fields["workerid"] = articleid
            article_fields["articlecovers"] = covers
            article_fields["banner"] = bannertag

            article_fields["title"] = title
            article_fields["source"] = source
            article_fields["createtime"] = createtime

            url = article["url"]

            article_fields["appname"] = "荆州日报"
            article_fields["url"] = url
            article_fields["pubtime"] = 0
            article_fields["updatetime"] = 0

            print("外链==", json.dumps(article_fields, indent=4, ensure_ascii=False))
        else:

            print("未知 ",article)
            print("articletype=", articletype, "articletitle=", articletitle)

    # @staticmethod
    def analyze_articlelists(self,articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            channel_type = articleslistres.get("channelType")
            banner = articleslistres.get("banner")

            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent = 4, ensure_ascii = False))
                # print("articleslists=", articleslists)
                try:
                    datalist = articleslists

                    try:
                        bannerlist = datalist["position"]
                        for article in bannerlist:
                            articleparam = self.formatearticlelist(article, channelid, channelname, channel_type, 1)
                            if articleparam:
                                articlesparams.append(articleparam)
                    except Exception as e:
                        print("无banner",e)

                    try:
                        contentlist = datalist["lists"]
                        for article in contentlist:

                            articleparam = self.formatearticlelist(article, channelid, channelname, channel_type, 0)
                            if articleparam:
                                articlesparams.append(articleparam)
                    except Exception as e:
                        print("无list", e)

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
            topic = article_field.get("topic")
            channelname = article_field.get("channelname")
            channelid = article_field.get("channelID")
            articletype = article.get("articletype")

            if topic == 1:
                url = article_field["topicUrl"]
                headers = {
                    "Charset": "UTF-8",
                    "Accept": "*/*",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 apicloud",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "Host": "app.cnchu.com"
                }
                data = {

                }
                method = 'get'
            else:
                url = "https://app.cnchu.com/index.php"
                headers = {
                    "Charset": "UTF-8",
                    "Accept": "*/*",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 apicloud",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "Host": "app.cnchu.com"
                }

                m = "content"
                if articletype == 6:
                    m = "live"

                data = {
                    "m": m,
                    "c": "index",
                    "a": "show",
                    "catid": channelid,
                    "id": articleid
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
                content_s = json.loads(json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))

                if "error" in content_s.keys():
                    print("数据异常",content_s)
                    continue

                if topic == 1:

                    channelid = fields["channelID"]
                    channelname = fields["channelName"]
                    # channeltype = fields["channelType"]
                    #
                    topicid = fields["topicID"]
                    topictitle = content_s["title"]
                    des = content_s["description"]
                    cover = content_s["pic"]
                    covers = list()
                    covers.append(cover)

                    bannertag = fields["banner"]


                    fields["title"] = topictitle
                    fields["digest"] = des
                    fields["topicCover"] = covers
                    fields["pubTime"] = 0
                    fields["createTime"] = 0
                    fields["updateTime"] = 0

                    topicnum = 0
                    newestarticleid = ""
                    newestpubtime = 0

                    childlist = content_s["specat"]
                    for section in childlist:
                        datalist = section["lists"]
                        for article in datalist:
                            topicnum += 1

                            article_fields = InitClass().article_fields()
                            achildid = article["id"]
                            acover = article["pic"]
                            acovers = list()
                            acovers.append(acover)

                            aurl = article["url"]
                            atitle = article["title"]

                            articletype = article["typeid"]


                            url = "https://app.cnchu.com/index.php"
                            headers = {
                                "Charset": "UTF-8",
                                "Accept": "*/*",
                                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 apicloud",
                                "Connection": "Keep-Alive",
                                "Accept-Encoding": "gzip",
                                "Host": "app.cnchu.com"
                            }

                            m = "content"
                            if articletype == 6:
                                m = "live"

                            data = {
                                "m": m,
                                "c": "index",
                                "a": "show",
                                "catid": channelid,
                                "id": achildid
                            }

                            itemres = requests.get(url, headers=headers, params=data).text
                            detailjson = json.loads(json.dumps(json.loads(itemres, strict=False), indent=4, ensure_ascii=False))
                            # print("detailjson=",detailjson)
                            if "error" in detailjson.keys():
                                print("数据异常", detailjson)
                                continue

                            #结果
                            # 普通
                            readnum = 0
                            author = ""
                            source = ""
                            copyfrom = detailjson["copyfrom"]
                            #print("copyfrom==",copyfrom)
                            if " " in copyfrom:
                                aindex = copyfrom.index(" ")
                                if aindex > 0:
                                    source = copyfrom[0:aindex]
                                    remain = copyfrom[aindex:]

                                    remain = remain.strip()
                                    if "来源" in remain:
                                        aindex = remain.index(" ")
                                        if aindex > 0:
                                            bbb = remain[aindex:]
                                            author = bbb
                                    else:
                                        author = remain
                                    author = author.replace("通讯员", "")
                                    author = author.replace("记者", "")
                                    author = author.replace("编辑", "")
                                    author = author.strip()
                            else:
                                source = copyfrom

                            createtime = 0
                            pubtime = detailjson["inputtime"]
                            pubtime = InitClass().date_time_stamp(pubtime)

                            if pubtime > newestpubtime:
                                newestpubtime = pubtime
                                newestarticleid = achildid

                            uptime = 0
                            likenum = 0
                            commentnum = 0
                            content = detailjson["content"]

                            type = detailjson["typeid"]
                            if type == "4":
                                contentimgs = detailjson["pictureurls"]
                                # prelist = fields["images"]
                                # prelist.extend(contentimgs)
                                # fields["images"] = prelist

                            article_fields["channelname"] = channelname
                            article_fields["channelID"] = channelid
                            article_fields["channelType"] = ""

                            article_fields["articlecovers"] = acovers
                            article_fields["specialtopic"] = 1
                            article_fields["topicid"] = topictitle
                            article_fields["topicTitle"] = topicid


                            article_fields["title"] = atitle
                            article_fields["updatetime"] = uptime
                            article_fields["pubtime"] = pubtime
                            article_fields["createtime"] = createtime
                            article_fields["url"] = aurl

                            article_fields["appname"] = self.newsname
                            article_fields["content"] = content
                            article_fields["source"] = source
                            article_fields["commentnum"] = commentnum
                            article_fields["likenum"] = likenum
                            article_fields["readnum"] = readnum
                            article_fields["author"] = author

                            article_fields["videocover"] = []

                            contentimgs = []
                            type = detailjson["typeid"]
                            if type == "4":
                                contentimgs = detailjson["pictureurls"]

                            try:
                                videourl = detailjson["video"]
                                videolist = list()
                                if videourl:
                                    videolist.append(videourl)
                                article_fields["videos"] = videolist

                            except Exception as e:
                                print("无视频")

                            try:
                                images = InitClass().get_images(content)

                                images.extend(contentimgs)

                                article_fields["images"] = images
                            except Exception as e:
                                print("无图片")
                            article_fields["banner"] = bannertag
                            print("专题内部文章==", json.dumps(article_fields, indent=4, ensure_ascii=False))

                    fields["platformName"] = self.newsname
                    fields["articleNum"] = topicnum
                    fields["newestArticleID"] = newestarticleid
                    print("大专题==",json.dumps(fields, indent = 4, ensure_ascii = False))
                else:

                    contentdetail = content_s
                    contentimgs = []
                    if "starttime" in contentdetail.keys():
                        #直播

                        createtime = contentdetail["createtime"]
                        createtime = int(createtime) *1000
                        pubtime = 0
                        uptime = 0
                        likenum = 0
                        commentnum = 0
                        readnum = contentdetail["views"]

                        content = ""
                        source = ""
                        author = ""

                    else:

                        #普通
                        readnum = 0
                        author = ""
                        source = ""
                        copyfrom = contentdetail["copyfrom"]
                        #print("copyfrom==",copyfrom)
                        if " " in copyfrom:
                            aindex = copyfrom.index(" ")
                            if aindex > 0:
                                source = copyfrom[0:aindex]
                                remain = copyfrom[aindex:]

                                remain = remain.strip()
                                if "来源" in remain:
                                    aindex = remain.index(" ")
                                    if aindex > 0:
                                        bbb = remain[aindex:]
                                        author = bbb
                                else:
                                    author = remain
                                author = author.replace("通讯员", "")
                                author = author.replace("记者", "")
                                author = author.replace("编辑", "")
                                author = author.strip()
                        else:
                            source = copyfrom

                        createtime = 0
                        pubtime = contentdetail["inputtime"]
                        pubtime = InitClass().date_time_stamp(pubtime)
                        uptime = 0
                        likenum = 0
                        commentnum = 0
                        content = contentdetail["content"]


                        type = contentdetail["typeid"]
                        if type == "4":
                            contentimgs = contentdetail["pictureurls"]
                            # prelist = fields["images"]
                            # prelist.extend(contentimgs)
                            # fields["images"] = prelist

                    title = contentdetail["title"]
                    url = contentdetail["url"]

                    fields["title"] = title
                    fields["updatetime"] = uptime
                    fields["pubtime"] = pubtime
                    fields["createtime"] = createtime
                    fields["url"] = url

                    fields["appname"] = self.newsname
                    fields["content"] = content
                    fields["source"] = source
                    fields["commentnum"] = commentnum
                    fields["likenum"] = likenum
                    fields["readnum"] = readnum
                    fields["author"] = author

                    fields["videocover"] = []

                    try:
                        videourl = contentdetail["video"]
                        videolist = list()
                        if videourl:
                            videolist.append(videourl)
                        fields["videos"] = videolist

                    except Exception as e:
                        print("无视频")

                    try:
                        images = InitClass().get_images(content)
                        images.extend(contentimgs)
                        fields["images"] = images
                    except Exception as e:
                        print("无图片")

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
    appspider = Jingzhouribao("荆州日报")
    appspider.run()
