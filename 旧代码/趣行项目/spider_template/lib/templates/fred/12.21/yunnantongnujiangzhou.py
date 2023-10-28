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
from App.appspider_m import Appspider
from App.initclass import InitClass
from lxml import html
from html.parser import HTMLParser

APPID = 134
APPKEY = 'd0186'
PROJECTID = 1
STYLEID = 366
TOKEN = '3dc12b54b79b26083248589ed756cbe28d5369678a69b63fa7a29132f60c2880816077903dd8230141740a05598f39cac891453462875be781baaafd1714e3251608857911443'
COOKIE = 'acw_tc=2f624a1d16088758335076395e06e0b71b3ec52a2d94343792473a626364fa'
USERAGENT = 'YunNanTong/3.0.0 (iPhone; iOS 12.0.1; Scale/2.00)'
APPNAME = '云南通·怒江洲'

class Yunnantongnujiangzhou(Appspider):

    #请求频道
    @staticmethod
    def get_app_params():
        url = "https://apiparty.xinhuaapp.com/Service/IndexSvr.svc/GetNavigation"
        headers = {
            "Host": "apiparty.xinhuaapp.com",
            "Content-Type": "application/json; charset=utf-8",
            "Cookie": COOKIE,
            "Connection": "keep-alive",
            "Accept": "application/json",
            "User-Agent": USERAGENT,
            "Accept-Language": "zh-Hans-CN;q=1",
            "Token": TOKEN,
            "Accept-Encoding": "br, gzip, deflate",
        }
        data = {
            "appId": APPID,
            "appKey": APPKEY,
            "projectId": PROJECTID,
            "styleId": STYLEID,
            "template": "TAPP001",
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    #解析频道列表
    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        # print("channelslists=",channelslists)

        # channelid = "2681"
        # channelname = "首页"

        # channelid = "1228"
        # channelname = "怒江动态"

        # channelid = "1884"
        # channelname = "文化怒江"

        # channelid = "1213"
        # channelname = "环球"

        # channelid = "1212"
        # channelname = "云南"

        # channelid = "1214"
        # channelname = "人事"

        # channelid = "1960"
        # channelname = "云风尚"

        # channelid = "1933"
        # channelname = "纪委发布"

        # channelid = "1953"
        # channelname = "专题"

        # channelid = "112357"
        # channelname = "现场云"

        # channelid = "1220"
        # channelname = "图闻"

        # channelparam = InitClass().channel_fields(channelid, channelname)
        # channelsparams.append(channelparam)

        fixeds = channelslists['Data']['Fixeds']
        modilars = channelslists['Data']['Modilars']
        for channel in fixeds + modilars:
            channelid = channel['ModliarId']
            channelname = channel['Title']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)

        yield channelsparams

    #请求频道列表
    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []

        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype =  "" #channel.get("channeltype")  # 此处没有若有可加上，其他一样

            if channelname == "首页":
                #首页频道列表数据
                url = "https://apiparty.xinhuaapp.com/Service/IndexSvr.svc/GetIndexPage"
            else:
                #其余频道列表数据
                url = "https://apiparty.xinhuaapp.com/Service/ContentSvr.svc/GetContentList"

            headers = {
                "Host": "apiparty.xinhuaapp.com",
                "Content-Type": "application/json; charset=utf-8",
                "Cookie": COOKIE,
                "Connection": "keep-alive",
                "Accept": "application/json",
                "User-Agent": USERAGENT,
                "Accept-Language": "zh-Hans-CN;q=1",
                "Token": TOKEN,
                "Accept-Encoding": "br, gzip, deflate"
            }

            data = {
                "pageNo": 1,
                "appId": APPID,
                "appKey": APPKEY,
                "projectId": PROJECTID,
                "modilarId": channelid,
                "styleId": STYLEID
            }

            method = "get"

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid = channelid, data = data,
                                                                       channeltype = channeltype)
            articlelistsparams.append(articlelist_param)
        yield articlelistsparams

    @staticmethod
    def formatearticlelist(article,channelid,channelname):

        contenttype = article["ContentType"]
        articletitle = article["Title"]
        articleid = article["Id"]
        # print("contenttype==",contenttype,"channelname=",channelname,"articletitle==",articletitle)

        # template = article["Template"]
        shareurl = article["LinkUrl"]
        source = article["Source"]
        author = article["Authors"]
        likenum = article["Likes"]
        commentnum = article["Comments"]
        readnum = article["Reads"]
        issuetime = article["IssueTime"]
        img = article["ImgUrl"]
        imgcovers = list()
        imgcovers.append(img)
        # contenttype
        # 0,1 ，16音频
        # 32 直播
        # 8 外链（新华社）
        # 64 专题
        if contenttype == 64:
            # 专题新闻
            topic_fields = InitClass().topic_fields()
            articleparam = InitClass().article_list_fields()

            topic_fields["topicID"] = articleid
            topic_fields["channelName"] = channelname
            topic_fields["channelID"] = channelid
            topic_fields["channelType"] = ""
            topic_fields["topicUrl"] = shareurl
            topic_fields["title"] = articletitle
            topic_fields["topicCover"] = imgcovers
            topic_fields["original"] = source
            topic_fields["pubTime"] = InitClass().date_time_stamp(issuetime)
            topic_fields["topic"] = 1

            # 将请求文章必需信息存入
            articleparam["articleField"] = topic_fields  # 携带文章采集的数据
            articleparam["articleid"] = articleid
            articleparam["contenttype"] = contenttype
            return articleparam
            # articlesparams.append(articleparam)

        else:
            # 普通新闻
            arvideourl = article["VodUrl"]
            article_fields = InitClass().article_fields()
            articleparam = InitClass().article_list_fields()

            try:
                soundurl = article["SoundUrl"]
                if soundurl:
                    article_fields["soundurl"] = soundurl
            except Exception as e:
                print("不是音频")

            article_fields["channelID"] = channelid
            article_fields["channelname"] = channelname
            article_fields["channelType"] = ""
            article_fields["url"] = shareurl
            article_fields["workerid"] = articleid
            article_fields["title"] = articletitle
            article_fields["content"] = ""
            article_fields["articlecovers"] = imgcovers
            article_fields["images"] = []

            article_fields["videocover"] = []
            article_fields["source"] = source
            article_fields["createtime"] = 0
            article_fields["updatetime"] = 0
            article_fields["likenum"] = 0
            article_fields["playnum"] = 0
            article_fields["commentnum"] = commentnum
            article_fields["readnum"] = readnum
            article_fields["trannum"] = likenum
            article_fields["sharenum"] = 0
            article_fields["author"] = author
            article_fields["specialtopic"] = 0
            avideoslist = list()
            if arvideourl:
                avideoslist.append(arvideourl)
            article_fields["videos"] = avideoslist

            if contenttype == 8:
                # 外部
                article_fields["pubtime"] = InitClass().date_time_stamp(issuetime)
                article_fields["appname"] = APPNAME
                print("外链文章=", json.dumps(article_fields, indent=4, ensure_ascii=False))
                return
            else:
                # 内部
                articleparam["articleField"] = article_fields  # 携带文章采集的数据
                articleparam["articleid"] = articleid
                articleparam["contenttype"] = contenttype
                return articleparam
                # articlesparams.append(articleparam)


    #解析频道数据
    # @staticmethod
    def analyze_articlelists(self,articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            channel_type = "" #articleslistres.get("channeltype")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent = 4, ensure_ascii = False))
                try:

                    data_list = articleslists["Data"]

                    #今日推荐
                    try:
                        rollinglist = data_list["Rolling"]
                        if len(rollinglist) > 0:
                            tjurl = "https://apiparty.xinhuaapp.com/Service/ContentSvr.svc/GetContentByIsHot"
                            tjheader = {
                                "Host": "apiparty.xinhuaapp.com",
                                "Content-Type": "application/json; charset=utf-8",
                                "Cookie": COOKIE,
                                "Connection": "keep - alive",
                                "Accept": "application / json",
                                "User-Agent": USERAGENT,
                                "Accept-Language": "zh-Hans-CN;q=1",
                                "Token": TOKEN,
                                "Accept-Encoding": "br, gzip, deflate"
                            }
                            tjdata = {
                                "appId": APPID,
                                "appKey": APPKEY,
                                "projectId": PROJECTID,
                                "isHot": 1,
                                "states": 8,
                                "pageSize": 20,
                                "pageNo": 1
                            }
                            tjres = requests.get(tjurl, headers=tjheader, params=tjdata).text
                            tjjson = json.loads(
                                json.dumps(json.loads(tjres, strict=False), indent=4, ensure_ascii=False))
                            tjlist = tjjson["Data"]
                            subchannelid = str(channelid) + "-" + ""
                            subchannelname = channelname + "-" + "今日推荐"
                            for tjitem in tjlist:
                                articleparam = self.formatearticlelist(tjitem, subchannelid, subchannelname)
                                if articleparam:
                                    articlesparams.append(articleparam)
                    except Exception as e:
                        print("无推荐 eee=")


                    #频道下推荐的频道
                    recommendlist = data_list["Recommend"]
                    if len(recommendlist) > 0:
                        for recomitem in recommendlist:
                            tmpchannelid = str(recomitem["Id"])
                            tmpchannelname = recomitem["Title"]

                            #请求下级列表
                            tjurl = "https://apiparty.xinhuaapp.com/Service/ContentSvr.svc/GetContentList"
                            tjheader = {
                                "Host": "apiparty.xinhuaapp.com",
                                "Content-Type": "application/json; charset=utf-8",
                                "Cookie": COOKIE,
                                "Connection": "keep-alive",
                                "Accept": "application/json",
                                "User-Agent": USERAGENT,
                                "Accept-Language": "zh-Hans-CN;q=1",
                                "Token": TOKEN,
                                "Accept-Encoding": "br, gzip, deflate"
                            }
                            tjdata = {
                                "appId": APPID,
                                "appKey": APPKEY,
                                "projectId": PROJECTID,
                                "modilarId": tmpchannelid,
                                "pageNo": 1
                            }
                            tjres = requests.get(tjurl, headers=tjheader, params=tjdata).text
                            tjjson = json.loads(
                                json.dumps(json.loads(tjres, strict=False), indent=4, ensure_ascii=False))
                            tjlist = tjjson["Data"]["Contents"]
                            subchannelid = str(channelid) + "-" + tmpchannelid
                            subchannelname = channelname + "-" + tmpchannelname
                            for tjitem in tjlist:
                                articleparam = self.formatearticlelist(tjitem, subchannelid, subchannelname)
                                if articleparam:
                                    articlesparams.append(articleparam)


                    #banner
                    try:
                        banner_list = data_list["Focus"]
                        for banner_item in banner_list:

                            articleid = banner_item["Id"]
                            img = banner_item["ImgUrl"]
                            bannervideourl = banner_item["VodUrl"]
                            linkurl = banner_item["LinkUrl"]
                            shareurl = banner_item["ShareUrl"]
                            articletitle = banner_item["Title"]
                            contenttype = banner_item["ContentType"]

                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()

                            try:
                                soundurl = banner_item["SoundUrl"]
                                if soundurl:
                                    article_fields["soundurl"] = soundurl
                            except Exception as e:
                                print("不是音频")

                            try:
                                pubtime = banner_item["IssueTimeText"]
                                article_fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                            except Exception as e:
                                print("banner issuetime eee=",e)

                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channelType"] = channel_type
                            article_fields["articlecovers"] = [img]
                            article_fields["url"] = linkurl

                            article_fields["workerid"] = articleid
                            article_fields["title"] = articletitle
                            article_fields["contentType"] = contenttype
                            article_fields["url"] = shareurl

                            article_fields["banner"] = 1
                            article_fields["images"] = []
                            article_fields["videocover"] = []
                            article_fields["createtime"] = 0
                            article_fields["updatetime"] = 0

                            videourls = list()
                            if bannervideourl:
                                videourls.append(bannervideourl)
                            article_fields["videos"] = videourls

                            articleparam["articleField"] = article_fields  # 携带文章采集的数据
                            articleparam["articleid"] = articleid
                            articleparam["contenttype"] = contenttype
                            articlesparams.append(articleparam)
                    except Exception as e:
                        print("非首页banner eee=",e)

                    n_list = []
                    sy_list = []
                    try:
                        # 首页列表
                        sy_list = data_list["IndexContent"]
                    except Exception as e:
                        print("非 首页 列表 eee=")
                    try:
                        # 普通页列表
                        n_list = data_list["Contents"]
                    except Exception as e:
                        print("非普通页 列表 eee=")

                    for article in sy_list + n_list:
                        articleparam = self.formatearticlelist(article,channelid,channelname)
                        if articleparam:
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
            topic = article_field.get("topic")
            contenttype = article.get("contenttype")

            if topic == 1:
                url = "https://apiparty.xinhuaapp.com/Service/ContentSvr.svc/GetContentTheme"
                headers = {
                    "Host": "apiparty.xinhuaapp.com",
                    "Content-Type": "application/json; charset=utf-8",
                    "Cookie": COOKIE,
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "User-Agent": USERAGENT,
                    "Accept-Language": "zh-Hans-CN;q=1",
                    "Token": TOKEN,
                    "Accept-Encoding": "br, gzip, deflate"
                }
                data = {
                    "pageNo": 1,
                    "contentId": articleid,
                    "appId": APPID,
                    "appKey": APPKEY,
                    "projectId": PROJECTID
                }
            else:
                if contenttype == 1 or contenttype == 2 or contenttype == 0 or contenttype == 16 or contenttype == 32 or contenttype == 256:
                    # 普通
                    method = 'get'
                    url = "https://apiparty.xinhuaapp.com/Service/ContentSvr.svc/GetContentDetail"
                    headers = {
                        "Host": "apiparty.xinhuaapp.com",
                        "Content-Type": "application/json; charset=utf-8",
                        "Cookie": COOKIE,
                        "Connection": "keep-alive",
                        "Accept": "application/json",
                        "User-Agent": USERAGENT,
                        "Accept-Language": "zh-Hans-CN;q=1",
                        "Token": TOKEN,
                        "Accept-Encoding": "br, gzip, deflate"
                    }
                    data = {
                        "contentId": articleid,
                        "appId": APPID,
                        "appKey": APPKEY,
                        "projectId": PROJECTID
                    }
                elif contenttype == 4:
                    #画廊
                    method = 'get'
                    url = "https://apiparty.xinhuaapp.com/Service/ContentSvr.svc/GetContentAtlas"
                    headers = {
                        "Host": "apiparty.xinhuaapp.com",
                        "Content-Type": "application/json; charset=utf-8",
                        "Cookie": COOKIE,
                        "Connection": "keep-alive",
                        "Accept": "application/json",
                        "User-Agent": USERAGENT,
                        "Accept-Language": "zh-Hans-CN;q=1",
                        "Token": TOKEN,
                        "Accept-Encoding": "br, gzip, deflate"
                    }
                    data = {
                        "contentId": articleid,
                        "appId": APPID,
                        "appKey": APPKEY,
                        "projectId": PROJECTID
                    }
                else:
                    print("未知类型 contenttype ==",contenttype)
                    continue

            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, data = data,
                                                             article_field = article_field)
            articleparams.append(articleparam)
        yield articleparams

    #解析详情
    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            topic = fields.get("topic")

            if topic:
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))

                    topiclist = content_s["Data"]

                    channelid = fields["channelName"]
                    channelname = fields["channelID"]
                    topicid = fields["topicID"]
                    topictitle = fields["title"]

                    articleids = list()
                    newestarticleiD = ""
                    newestpubtime = 0
                    topicnum = 0

                    themedata = topiclist["ThemeData"]
                    for themeitem in themedata:
                        contentlist = themeitem["ContentList"]
                        topicnum += len(contentlist)

                        for normalarticle in contentlist:
                            #专题内普通文章

                            contenttype = normalarticle["ContentType"]
                            articletitle = normalarticle["Title"]
                            articleid = normalarticle["Id"]

                            videourl = normalarticle["VodUrl"]

                            articleids.append(articleid)

                            # template = normalarticle["Template"]
                            shareurl = normalarticle["LinkUrl"]
                            source = normalarticle["Source"]
                            author = normalarticle["Authors"]
                            likenum = normalarticle["Likes"]
                            commentnum = normalarticle["Comments"]
                            readnum = normalarticle["Reads"]
                            img = normalarticle["ImgUrl"]
                            issuetime = normalarticle["IssueTime"]
                            issuetime = InitClass().date_time_stamp(issuetime)
                            if issuetime:
                                if issuetime > newestpubtime:
                                    newestarticleiD = articleid
                                    newestpubtime = issuetime

                            article_fields = InitClass().article_fields()

                            try:
                                soundurl = normalarticle["SoundUrl"]
                                if soundurl:
                                    article_fields["soundurl"] = soundurl
                            except Exception as e:
                                print("不是音频")

                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channelType"] = ""
                            article_fields["url"] = shareurl
                            article_fields["workerid"] = articleid
                            article_fields["title"] = articletitle
                            article_fields["content"] = ""
                            article_fields["articlecovers"] = [img]
                            article_fields["images"] = []

                            article_fields["videocover"] = []
                            article_fields["source"] = source
                            article_fields["createtime"] = 0
                            article_fields["updatetime"] = 0
                            article_fields["likenum"] = 0
                            article_fields["playnum"] = 0
                            article_fields["commentnum"] = commentnum
                            article_fields["readnum"] = readnum
                            article_fields["trannum"] = likenum
                            article_fields["sharenum"] = 0
                            article_fields["author"] = author
                            article_fields["specialtopic"] = 1
                            article_fields["topicid"] = topicid
                            article_fields["topicTitle"] = topictitle
                            article_fields["appname"] = self.newsname
                            article_fields["pubtime"] = issuetime

                            arvideoslist = list()
                            if videourl:
                                arvideoslist.append(videourl)
                            article_fields["videos"] = arvideoslist

                            if contenttype == 8:
                                # 外部
                                # print("外部")
                                print("专题 外链文章=", json.dumps(article_fields, indent=4, ensure_ascii=False))
                            else:
                                # 内部
                                # print("内部")
                                # print("videourl==",videourl)
                                #请求详情

                                detail_method = 'get'
                                detail_url = "https://apiparty.xinhuaapp.com/Service/ContentSvr.svc/GetContentDetail"
                                detail_headers = {
                                    "Host": "apiparty.xinhuaapp.com",
                                    "Content-Type": "application/json; charset=utf-8",
                                    "Cookie": COOKIE,
                                    "Connection": "keep-alive",
                                    "Accept": "application/json",
                                    "User-Agent": USERAGENT,
                                    "Accept-Language": "zh-Hans-CN;q=1",
                                    "Token": TOKEN,
                                    "Accept-Encoding": "br, gzip, deflate"
                                }
                                detail_data = {
                                    "contentId": articleid,
                                    "appId": APPID,
                                    "appKey": APPKEY,
                                    "projectId": PROJECTID
                                }

                                detailres = requests.get(detail_url,headers=detail_headers,params=detail_data).text
                                detailjson = json.loads(json.dumps(json.loads(detailres, strict=False), indent=4,
                                                                   ensure_ascii=False))
                                # print("detailjson==",detailjson)

                                try:
                                    detail_url = detailjson["Data"]["DetailUrl"]
                                    if detail_url:
                                        res = requests.get(detail_url)
                                        res.encoding = 'utf-8'
                                        content = res.text
                                        content = content.lstrip("var ContentDetail = ")
                                        content = eval(content)
                                        article_fields["content"] = content
                                        try:
                                            videos = InitClass().get_video(content)
                                            # print("videos==",videos)
                                            prelist = article_fields["videos"]
                                            prelist.extend(videos)
                                            article_fields["videos"] = prelist

                                            #article_fields["videos"] = videos
                                        except Exception as e:
                                            print("text eee==", e)

                                        try:
                                            images = InitClass().get_images(content)
                                            article_fields["images"] = images
                                        except Exception as e:
                                            print("text eee==", e)

                                except Exception as e:
                                    print("无 DetailUrl ee===", e)

                                print("专题 内部文章=", json.dumps(article_fields, indent=4, ensure_ascii=False))

                    fields["articleIDs"] = articleids
                    fields["articleNum"] = topicnum

                    if newestarticleiD:
                        fields["newestArticleID"] = newestarticleiD
                        fields["newestPubtime"] = newestpubtime
                    fields["createTime"] = 0
                    fields["updateTime"] = 0

                    fields["platformName"] = self.newsname
                    print("大专题===", json.dumps(fields, indent=4, ensure_ascii=False))

                except Exception as e:
                    num += 1
                    logging.info(f"错误数量{num},{e}")
            else:
                #普通
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))

                    detail = content_s["Data"]

                    pubtime = detail["IssueTime"]
                    if pubtime:
                        fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                    else:
                        fields["pubtime"] = 0

                    fields["appname"] = self.newsname

                    # 画廊
                    try:
                        contentimages = detail['ContentImage']
                        imageslist = list()
                        for imgitem in contentimages:
                            imgurl = imgitem["ImgUrl"]
                            imageslist.append(imgurl)
                        fields["images"] = imageslist
                    except Exception as e:
                        print("非画廊 e==")


                    try:
                        detail_url = detail["DetailUrl"]
                        if detail_url:
                            res = requests.get(detail_url)
                            res.encoding = 'utf-8'
                            content = res.text
                            content = content.lstrip("var ContentDetail = ")
                            content = eval(content)
                            fields["content"] = content
                            try:
                                videos = InitClass().get_video(content)
                                # print("videos==", videos)
                                prelist = fields["videos"]
                                prelist.extend(videos)
                                fields["videos"] = prelist
                                # fields["videos"] = videos
                            except Exception as e:
                                print("text eee==", detail)

                            try:
                                 images = InitClass().get_images(content)
                                 fields["images"] = images
                            except Exception as e:
                                 print("text eee==", detail)

                    except Exception as e:
                        print("无 DetailUrl ee=",e)

                    print("文章===",json.dumps(fields, indent=4, ensure_ascii=False))

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
    appspider = Yunnantongnujiangzhou("云南通·怒江州")
    appspider.run()
