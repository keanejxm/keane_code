# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
import requests
from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass

APPID = 128
APPKEY = 'd0217'
PROJECTID = 1
STYLEID = 360
TOKEN = '632bdac4b2b16a68024f6848d5cc630822b6486a288539a95aca61d6a2eec8c264adc168e5a74343befc09485d30b19a18cfe055ada160ae0369e60848f151981609157394397'
COOKIE = 'acw_tc=707c9fda16091573947594705e0e0541ce4a7aa627afaefdd86d979eec3a96'
USERAGENT = 'YunNanTong/3.0.0 (iPhone; iOS 12.0.1; Scale/2.00)'
APPNAME = '云南通·楚雄州'

TOPICARTICLES = ["TNWS003", "TNWS005", "TNWS006", "TNWS007"]
H5ARTICLES = ["TNWS004","TNWS502"]

class Yunnantongchuxiongzhou(Appspider):
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

    #解析列表文章
    @staticmethod
    def formatearticlelist(article,channelid,channelname,bannertag):

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

        if template in TOPICARTICLES:
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
            articleparam["articleField"] = topic_fields  # 携带文章采集的数据
            articleparam["articleid"] = articleid
            articleparam["channelname"] = channelname
            return articleparam

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

            if template in H5ARTICLES:
                # 外部
                article_fields["pubtime"] = pubtime
                article_fields["appname"] = APPNAME
                print("外链文章=", json.dumps(article_fields, indent=4, ensure_ascii=False))
                return None
            else:
                # 内部
                articleparam["articleField"] = article_fields  # 携带文章采集的数据
                articleparam["articleid"] = articleid
                return articleparam

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
                        #关
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
                                articleparam = self.formatearticlelist(tjitem, subchannelid, subchannelname,0)
                                if articleparam:
                                    articlesparams.append(articleparam)
                    except Exception as e:
                        print("无推荐 eee=",e)

                    try:
                        # 频道下二级频道
                        recommendlist = data_list["Recommend"]
                        #关
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
                                    if articleparam:
                                        articlesparams.append(articleparam)
                    except Exception as e:
                        print("无 二级菜单 eee=", e)
                        #banner

                    try:
                        banner_list = data_list["Focus"]
                        #关
                        # banner_list = []
                        for banner_item in banner_list:
                            articleparam = self.formatearticlelist(banner_item, channelid, channelname, 1)
                            if articleparam:
                                articlesparams.append(articleparam)
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
                        articleparam = self.formatearticlelist(article,channelid,channelname,0)
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
            template = article_field.get("template")

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
                    #画廊
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
                    print("未知类型 template ==",template,"article_field ==",article_field)
                    continue

            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, data = data,
                                                             article_field = article_field)
            articleparams.append(articleparam)
        yield articleparams

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
                    bannertag = fields["banner"]

                    newestarticleiD = ""
                    newestpubtime = 0
                    topicnum = 0

                    themedata = topiclist["ThemeData"]
                    for themeitem in themedata:
                        contentlist = themeitem["ContentList"]
                        topicnum += len(contentlist)

                        for normalarticle in contentlist:
                            #专题内普通文章

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

                            if template in H5ARTICLES:
                                # 外部
                                print("专题 外链文章=", json.dumps(article_fields, indent=4, ensure_ascii=False))
                            else:
                                # 内部
                                #请求详情
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

                                detailres = requests.get(detail_url,headers=detail_headers,params=detail_data).text
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
                #普通
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                    fields["appname"] = self.newsname
                    fields = self.formatearticledetail(content_s,fields)

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
    appspider = Yunnantongchuxiongzhou(APPNAME)
    appspider.run()
