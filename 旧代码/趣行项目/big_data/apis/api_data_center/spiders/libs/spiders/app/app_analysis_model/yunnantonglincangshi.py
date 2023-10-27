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

APPID = 127
APPKEY = 'd0195'
PROJECTID = 1
STYLEID = 359
TOKEN = 'e3c078ca990f3cc452c9cc02e4cad89b2df5c1071a46552539a931f6e6113f82df588fa91fef1d3abec46e826b8d7f74a7461c196d8a4bd578a17512d3ca0f721609325353850'
COOKIE = 'acw_tc=2f624a7416093253542332581e030b2e21db6277245403055b529e0bff5ba4'
USERAGENT = 'YunNanTong/3.0.0 (iPhone; iOS 12.0.1; Scale/2.00)'
APPNAME = '云南通·临沧市'


# contenttype
# 0,1 ，16音频
# 32 直播
# 8 外链（新华社）
# 64 专题

# 列表Template 字段
# TNWS001 普通
# TNWS002 画廊
# TNWS004  外链
# TNWS003 专题
# TNWS005 专题
# TNWS006 专题
# TNWS007 时间轴专题

# TNWS501 微视

class Yunnantongqujingshi(Appspider):

    # 请求频道
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
            "cityCode": 0
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    # 解析频道列表
    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))
        # print("channelslists=",channelslists)
        fixeds = channelslists['Data']['Fixeds']
        modilars = channelslists['Data']['Modilars']
        for channel in fixeds + modilars:
            channelid = channel['ModliarId']
            channelname = channel['Title']
            ishare = channel["IsShare"]
            if channelname == "现场云":
                print("外链忽略")
                continue
            else:
                channelparam = InitClass().channel_fields(channelid, channelname)
                yield channelparam

    # 请求频道列表
    def getarticlelistparams(self, channelsres):
        channel_num = 0
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = ""  # channel.get("channeltype")  # 此处没有若有可加上，其他一样

            if channelname == "推荐":
                # 首页频道列表数据
                url = "https://apiparty.xinhuaapp.com/Service/IndexSvr.svc/GetIndexPage"
            else:
                # 其余频道列表数据
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

    # 解析列表文章
    @staticmethod
    def formatearticlelist(article, channelid, channelname, bannertag):

        articletitle = article["Title"]
        articleid = article["Id"]
        template = article["Template"]
        shareurl = article["LinkUrl"]
        source = article["Source"]
        author = ""
        likenum = 0
        commentnum = 0
        readnum = 0
        try:
            author = article["Authors"]
            likenum = article["Likes"]
            commentnum = article["Comments"]
            readnum = article["Reads"]
        except Exception as e:
            print("")

        issuetime = article["IssueTime"]
        if '/Date(' in issuetime:
            issuetime = issuetime.replace("/Date(", "")
            issuetime = issuetime.replace("+0800)/", "")
        else:
            issuetime = InitClass().date_time_stamp(issuetime)

        pubtime = issuetime
        img = article["ImgUrl"]

        imgcovers = list()
        imgcovers.append(img)

        if template == "TNWS003" or template == "TNWS005" or template == 'TNWS006' or template == 'TNWS007':
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
            topic_fields["pubTime"] = pubtime
            topic_fields["topic"] = 1
            topic_fields["banner"] = bannertag

            intro = article["Meno"]
            topic_fields["digest"] = intro
            # 将请求文章必需信息存入
            return topic_fields

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
            article_fields["banner"] = bannertag
            article_fields["template"] = template

            avideoslist = list()
            if arvideourl:
                avideoslist.append(arvideourl)
            article_fields["videos"] = avideoslist

            if template == "TNWS004":
                # 外部
                article_fields["pubtime"] = pubtime
                article_fields["appname"] = APPNAME
                print("外链文章=", json.dumps(article_fields, indent=4, ensure_ascii=False))
                return None
            else:
                # 内部
                return article_fields

    # 解析频道数据
    # @staticmethod
    def analyze_articlelists(self, articleslistsres):
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channel_index_id = articleslistres.get("channelindexid")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            channel_type = ""  # articleslistres.get("channeltype")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    data_list = articleslists["Data"]
                    # 今日推荐
                    try:
                        rollinglist = data_list["Rolling"]
                        # 关
                        # rollinglist = []
                        if len(rollinglist) > 0:
                            tjurl = "https://apiparty.xinhuaapp.com/Service/ContentSvr.svc/GetContentByIsHot"
                            tjheader = {
                                "Host": "apiparty.xinhuaapp.com",
                                "Content-Type": "application/json; charset=utf-8",
                                "Cookie": COOKIE,
                                "Connection": "keep - alive",
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
                                articleparam = self.formatearticlelist(tjitem, subchannelid, subchannelname, 0)
                                articleparam["channelindexid"] = channel_index_id
                                if articleparam:
                                    yield articleparam
                    except Exception as e:
                        print("无推荐 eee=", e)

                    try:
                        # 频道下二级频道
                        recommendlist = data_list["Recommend"]
                        # 关
                        # recommendlist = []
                        if len(recommendlist) > 0:
                            for recomitem in recommendlist:
                                tmpchannelid = str(recomitem["Id"])
                                tmpchannelname = recomitem["Title"]
                                # 请求下级列表
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
                                    articleparam = self.formatearticlelist(tjitem, subchannelid, subchannelname, 0)
                                    articleparam["channelindexid"] = channel_index_id
                                    if articleparam:
                                        articleparam
                    except Exception as e:
                        print("无 二级菜单 eee=", e)

                    # banner
                    try:
                        banner_list = data_list["Focus"]
                        # 关
                        # banner_list = []
                        for banner_item in banner_list:
                            articleparam = self.formatearticlelist(banner_item, channelid, channelname, 1)
                            articleparam["channelindexid"] = channel_index_id
                            if articleparam:
                                yield articleparam
                    except Exception as e:
                        print("非首页banner")

                    n_list = []
                    sy_list = []
                    try:
                        # 首页列表
                        sy_list = data_list["IndexContent"]
                    except Exception as e:
                        print("非 首页 列表")
                    try:
                        # 普通页列表
                        n_list = data_list["Contents"]
                    except Exception as e:
                        print("非普通页 列表")
                    # #关
                    # n_list = []
                    # sy_list = []
                    for article in sy_list + n_list:
                        articleparam = self.formatearticlelist(article, channelid, channelname, 0)
                        articleparam["channelindexid"] = channel_index_id
                        if articleparam:
                            yield articleparam
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")

    def getarticleparams(self,articleslistsres):
        for article in self.analyze_articlelists(articleslistsres):
            articleid = article.get("workerid")
            topic = article.get("topic")
            template = article.get("template")

            if topic == 1:
                articleid = article.get("topicID")
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
                if template == 'TNWS001' or template == 'TNWS501':
                    if template == 'TNWS501':
                        # 微视
                        url = "https://apiparty.xinhuaapp.com/Service/ContentSvr.svc/GetContentDetailByVideo"
                    else:
                        # 普通
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

                elif template == 'TNWS002':
                    # elif contenttype == 4:
                    # 画廊
                    # method = 'get'
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
                    continue

            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                             article_field=article)
            yield [articleparam]

    @staticmethod
    def formatearticledetail(content_s, fields):

        detail = content_s["Data"]
        template = fields["template"]

        if template == 'TNWS001':
            # 普通
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
                        print("text eee=", detail)

                    try:
                        images = InitClass().get_images(content)
                        fields["images"] = images
                    except Exception as e:
                        print("text eee=", detail)

            except Exception as e:
                print("无 DetailUrl eee=", e)

        elif template == 'TNWS501':
            # 微视
            detail = detail["Detail"]

        elif template == 'TNWS002':
            # 画廊
            try:
                contentimages = detail['ContentImage']
                imageslist = list()
                for imgitem in contentimages:
                    imgurl = imgitem["ImgUrl"]
                    imageslist.append(imgurl)
                fields["images"] = imageslist
            except Exception as e:
                print("非画廊 eee=")

        pubtime = detail["IssueTime"]
        if pubtime:
            fields["pubtime"] = InitClass().date_time_stamp(pubtime)
        else:
            fields["pubtime"] = 0

        return fields

    # 解析详情
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
                    bannertag = fields["banner"]

                    newestarticleiD = ""
                    newestpubtime = 0
                    topicnum = 0

                    themedata = topiclist["ThemeData"]
                    for themeitem in themedata:
                        contentlist = themeitem["ContentList"]
                        topicnum += len(contentlist)

                        for normalarticle in contentlist:
                            # 专题内普通文章

                            articletitle = normalarticle["Title"]
                            articleid = normalarticle["Id"]
                            videourl = normalarticle["VodUrl"]
                            template = normalarticle["Template"]
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
                            article_fields["banner"] = bannertag
                            article_fields["template"] = template

                            arvideoslist = list()
                            if videourl:
                                arvideoslist.append(videourl)
                            article_fields["videos"] = arvideoslist

                            if template == 'TNWS004':
                                # if contenttype == 8:
                                # 外部
                                print("专题 外链文章=", json.dumps(article_fields, indent=4, ensure_ascii=False))
                            else:
                                # 内部
                                # 请求详情
                                detail_url = ""
                                if template == 'TNWS501':
                                    detail_url = "https://apiparty.xinhuaapp.com/Service/ContentSvr.svc/GetContentDetailByVideo"
                                else:
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

                                detailres = requests.get(detail_url, headers=detail_headers, params=detail_data).text
                                detailjson = json.loads(json.dumps(json.loads(detailres, strict=False), indent=4,
                                                                   ensure_ascii=False))

                                article_fields = self.formatearticledetail(detailjson, article_fields)
                                print("专题 内部文章=", json.dumps(article_fields, indent=4, ensure_ascii=False))

                    fields["articleNum"] = topicnum
                    if newestarticleiD:
                        fields["newestArticleID"] = newestarticleiD

                    fields["createTime"] = 0
                    fields["updateTime"] = 0
                    fields["platformName"] = self.newsname

                    print("大专题===", json.dumps(fields, indent=4, ensure_ascii=False))

                except Exception as e:
                    num += 1
                    logging.info(f"错误数量{num},{e}")
            else:
                # 普通
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                    fields["appname"] = self.newsname
                    fields = self.formatearticledetail(content_s, fields)

                    fields = InitClass().wash_article_data(fields)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}

                except Exception as e:
                    num += 1
                    logging.info(f"错误数量{num},{e}")

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Yunnantongqujingshi(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
