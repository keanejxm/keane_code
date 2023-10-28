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


class Guangmingribao2(Appspider):

    #请求频道
    @staticmethod
    def get_app_params():
        url = "https://api.gmdaily.cn/api/famous/person/channel/list"
        headers = {
            "method": "POST",
            "scheme": "https",
            "path": "/api/famous/person/channel/list",
            "authority": "api.gmdaily.cn",
            "content-type": "application/json",
            "accept": "*/*",
            "accept-language": "zh-Hans-CN;q=1",
            "token": "",
            "accept-encoding": "br, gzip, deflate",
            "deviceid": "D0561E6E-BFCE-4956-AF43-E1DA07D8E1FC",
            "user-agent": "guang ming ri bao/9.0.2 (iPhone; iOS 12.0.1; Scale/2.00)",
            "language": "1",
            "ua": "IOS+iPhone 6s+9.0.2+",
            "content-length": "2",
            "cookie":"jcloud_alb_route=4c92d156850a0d82371e14563f3a825d"
        }
        data = {}
        method = "post"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    # 解析频道列表
    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        # print("channelslists==",channelslists)

        for channel in channelslists["data"]:
            channelname = channel["name"]
            channelid = channel["channelId"]
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    #请求各频道列表数据
    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []

        method = 'post'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            if channelname == "访谈":
                continue

            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样

            url = "https://api.gmdaily.cn/api/famous/person/recall"

            headers = {
                "method": "POST",
                "scheme": "https",
                "path": "/api/famous/person/interview",
                "authority": "api.gmdaily.cn",
                "content-type": "application/json",
                "accept": "*/*",
                "accept-language": "zh-Hans-CN;q=1",
                "token": "",
                "accept-encoding": "br, gzip, deflate",
                "deviceid": "D0561E6E-BFCE-4956-AF43-E1DA07D8E1FC",
                "content-length": "65",
                "language": "1",
                "ua": "IOS+iPhone 6s+9.0.2+",
                "user-agent": "guang ming ri bao/9.0.2 (iPhone; iOS 12.0.1; Scale/2.00)",
                "cookie": "jcloud_alb_route=4c92d156850a0d82371e14563f3a825d"
            }

            data = {}
            channeljson = {
                "firstId": 0,
                "channelId": channelid,
            }

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid = channelid, data = data,channeljson=channeljson,
                                                                       channeltype = channeltype)
            articlelistsparams.append(articlelist_param)
            break

        yield articlelistsparams

    #解析各频道列表数据
    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []

        for articleslistres in articleslistsres:
            # print("articleslistres==", articleslistres)
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            channel_type = articleslistres.get("channeltype")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent = 4, ensure_ascii = False))
                try:
                    print("articleslists==",articleslists)

                    banners = articleslists["data"]["banners"]
                    records = articleslists["data"]["records"]

                    #banner
                    for banneritem in banners:
                        # print("banner item==",banneritem)
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()

                        contentvo = banneritem["contentVo"]
                        contenttype = contentvo["contentType"]
                        if contenttype == 7:
                            #banner 专题
                            # print("banner 专题")
                            # print("banner item==", banneritem)
                            topic_fields = InitClass().topic_fields()
                            articleparam = InitClass().article_list_fields()

                            article_id = banneritem["contentId"]
                            article_title = banneritem["bannerTitle"]

                            picinfos = contentvo["abridgePictures"]
                            article_covers = list()
                            for picinfo in picinfos:
                                article_covers.append(picinfo["url"])


                            topic_fields["topicCover"] = article_covers
                            topic_fields["topic"] = 1
                            topic_fields["_id"] = article_id
                            topic_fields["channelName"] = channelname
                            topic_fields["channelID"] = channelid
                            topic_fields["title"] = article_title
                            # topic_fields["source"] = source
                            # topic_fields["pubtime"] = pubtime
                            topic_fields["banner"] = 1
                            articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                            articleparam["articleid"] = article_id
                            articlesparams.append(articleparam)

                        else:

                            #banner 普通
                            article_id = banneritem["contentId"]
                            imageurl = banneritem["imageUrl"]
                            article_title = banneritem["bannerTitle"]

                            article_covers = list()
                            article_covers.append(imageurl)
                            article_fields["articlecovers"] = article_covers
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title

                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channeltype"] = channel_type
                            article_fields["banner"] = 1

                            articleparam["articleField"] = article_fields  # 携带文章采集的数据
                            articleparam["articleid"] = article_id

                            articlesparams.append(articleparam)

                    #列表
                    for item in records:

                        # print("新闻列表 item===",item)
                        contenttype = item["contentType"]
                        if contenttype == 7:
                            # print("普通 列表 专题")
                            # 专题新闻
                            topic_fields = InitClass().topic_fields()
                            articleparam = InitClass().article_list_fields()

                            article_id = str(item["contentId"])
                            article_title = item["title"]
                            source = item["source"]
                            pubtime = item["publishDt"]

                            # 封面图
                            picinfos = item["abridgePictures"]
                            article_covers = list()
                            for picinfo in picinfos:
                                article_covers.append(picinfo["url"])
                            topic_fields["topicCover"] = article_covers
                            topic_fields["topic"] = 1
                            topic_fields["_id"] = article_id
                            topic_fields["channelName"] = channelname
                            topic_fields["channelID"] = channelid
                            topic_fields["title"] = article_title
                            topic_fields["source"] = source
                            topic_fields["pubtime"] = pubtime
                            topic_fields["banner"] = 0
                            articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                            articleparam["articleid"] = article_id
                            articlesparams.append(articleparam)

                        else:
                            # 普通新闻
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()

                            article_id = str(item["contentId"])
                            article_title = item["title"]
                            source = item["source"]
                            pubtime = item["publishDt"]

                            #正文内视频
                            videos = item["videos"]
                            article_videos = list()
                            article_videocovers = list()
                            for vid in videos:
                                try:
                                    tmpcover = vid["cover"]
                                    article_videocovers.append(tmpcover)
                                except Exception as e:
                                    print("cover e")
                                article_videos.append(vid["url"])
                            article_fields["videos"] = article_videos
                            article_fields["videocover"] = article_videocovers

                            # 正文内图片
                            pictures = item["pictures"]
                            article_images = list()
                            for pic in pictures:
                                article_images.append(pic["url"])
                            article_fields["images"] = article_images

                            #封面图
                            picinfos = item["abridgePictures"]
                            article_covers = list()
                            for picinfo  in picinfos:
                                article_covers.append(picinfo["url"])
                            article_fields["articlecovers"] = article_covers
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["source"] = source
                            article_fields["pubtime"] = pubtime
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channeltype"] = channel_type
                            article_fields["banner"] = 0

                            articleparam["articleField"] = article_fields  # 携带文章采集的数据
                            articleparam["articleid"] = article_id
                            articlesparams.append(articleparam)

                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")
        yield articlesparams

    #请求详情
    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        for article in articles:
            articleid = article.get("articleid")
            article_field = article.get("articleField")
            topic = article_field.get("topic")
            if topic == 1:
                url = "https://api.gmdaily.cn/api/content/topic/contentList"
                headers = {
                    "method": "POST",
                    "scheme": "https",
                    "path": "/api/content/topic/contentList",
                    "authority": "api.gmdaily.cn",
                    "content-type": "application/json",
                    "accept": "*/*",
                    "accept-language": "zh-Hans-CN;q=1",
                    "token": "",
                    "accept-encoding": "br, gzip, deflate",
                    "deviceid": "D0561E6E-BFCE-4956-AF43-E1DA07D8E1FC",
                    "content-length": "48",
                    "language": "1",
                    "ua": "IOS+iPhone 6s+9.0.2+",
                    "user-agent": "guang ming ri bao/9.0.2 (iPhone; iOS 12.0.1; Scale/2.00)",
                    "cookie": "jcloud_alb_route=4c92d156850a0d82371e14563f3a825d"
                }
                detailjson = {
                    "contentId": articleid
                }
                data = {}
                method = 'post'
                articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                                 articlejson=detailjson,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            else:

                url = "https://api.gmdaily.cn/api/content/detail"
                headers = {
                    "method": "POST",
                    "scheme": "https",
                    "path": "/api/content/detail",
                    "authority": "api.gmdaily.cn",
                    "content-type": "application/json",
                    "accept": "*/*",
                    "accept-language": "zh-Hans-CN;q=1",
                    "token": "",
                    "accept-encoding": "br, gzip, deflate",
                    "deviceid": "D0561E6E-BFCE-4956-AF43-E1DA07D8E1FC",
                    "user-agent": "guang ming ri bao/9.0.2 (iPhone; iOS 12.0.1; Scale/2.00)",
                    "language": "1",
                    "ua": "IOS+iPhone 6s+9.0.2+",
                    "content-length": "48",
                }
                data = {}
                detailjson = {
                    "contentId": articleid
                }

                method = 'post'
                articleparam = InitClass().article_params_fields(url, headers, method, data = data,articlejson=detailjson,
                                                                 article_field = article_field)
                articleparams.append(articleparam)
        yield articleparams

    # 解析文章详情统一方法
    @staticmethod
    def formatearticledetail(content_s, fields):
        worker_id = content_s["contentId"]
        article_title = content_s["title"]
        try:
            content = content_s["contentTxt"]
            fields["content"] = content
        except Exception as e:
            print("contentTxt content_s ==",content_s)

        source = content_s["source"]
        pubtime = content_s["publishDt"]
        updatetime = content_s["updtDt"]
        comment_num = content_s["commentCount"]
        url = content_s["shareUrl"]
        likenum = content_s["praiseCount"]

        try:
            author = content_s["editorName"]
            fields["author"] = author
        except Exception as e:
            print("无 editorName")
            try:
                author = content_s["author"]
                fields["author"] = author
            except Exception as e:
                print("无 author")

        # 正文内视频
        videos = content_s["videos"]
        article_videos = list()
        article_videocovers = list()
        for vid in videos:
            try:
                tmpcover = vid["cover"]
                article_videocovers.append(tmpcover)
            except Exception as e:
                print("cover e")
            article_videos.append(vid["url"])
        fields["videos"] = article_videos
        fields["videocover"] = article_videocovers

        # 正文内图片
        pictures = content_s["pictures"]
        article_images = list()
        for pic in pictures:
            article_images.append(pic["url"])
        fields["images"] = article_images

        # 封面图
        picinfos = content_s["abridgePictures"]
        article_covers = list()
        for picinfo in picinfos:
            article_covers.append(picinfo["url"])
        fields["articlecovers"] = article_covers

        fields["title"] = article_title
        fields["workerid"] = worker_id
        fields["source"] = source
        fields["commentnum"] = comment_num
        fields["likenum"] = likenum
        fields["url"] = url
        fields["updatetime"] = updatetime
        fields["pubtime"] = pubtime
        fields["createtime"] = 0

        contenttype = content_s["contentType"]
        # 1 文字
        # 5 画廊

        # contentType，作品类型，-1未知，1文字，2图文，3视频文，4纯长视频，5纯短视频，6画廊，7纯音频，8短消息（动态、微头条、微博消息等）
        if contenttype == 1:
            fields["contentType"] = 1
        elif contenttype == 5:
            fields["contentType"] = 6

        print("文章 ==", json.dumps(fields, indent=4, ensure_ascii=False))
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
                    print("专题 content_s==", content_s)

                    content_s = content_s["data"]

                    zhuanti_id = content_s["contentId"]
                    zhuanti_title = content_s["title"]
                    # turl = content_s["topicBanner"]
                    tintro = content_s["introduction"]
                    tshare = content_s["shareUrl"]
                    # tauthor = content_s["editorName"]
                    tmpvos = content_s["moduleContentVos"]

                    ##fields["topic"]
                    fields["_id"] = zhuanti_id
                    fields["platformName"] = self.newsname
                    fields["platformID"] = ""
                    ##fields["channelName"]
                    ##fields["channelID"]
                    fields["topicUrl"] = tshare
                    fields["title"] = zhuanti_title
                    fields["digest"] = tintro
                    # fields["topicCover"] = article_covers
                    # fields["pubTime"] = 0

                    # ["newestArticleID"]
                    # ["newestPubtime"]
                    # ["articlesNumPerHour"]
                    # ["original"]
                    # ["firstMedia"]
                    # ["transPower"]
                    # ["hotDegree"]
                    # ["wordsFreq"]
                    # ["hotDegreeTrend"]
                    # ["emotionTrend"]
                    # ["region"]
                    # ["spreadPath"]
                    # fields["createTime"] =
                    # ["updateTime"]
                    # fields["readnum"] =
                    banner = 0
                    try:
                        banner = fields["banner"]
                    except Exception as e:
                        print("banner")


                    channelid = fields["channelID"]
                    channelname = fields["channelName"]

                    articleids = list()
                    newestarticleiD = ""
                    newestpubtime = 0
                    totaltopicnum = 0
                    for vos in tmpvos:
                        records = vos["records"]
                        print("records===", records)
                        totaltopicnum += len(records)

                        for item in records:
                            #print("item===", item)
                            tmpid = item["contentId"]
                            articleids.append(tmpid)
                            url = "https://api.gmdaily.cn/api/content/detail"
                            headers = {
                                "method": "POST",
                                "scheme": "https",
                                "path": "/api/content/detail",
                                "authority": "api.gmdaily.cn",
                                "content-type": "application/json",
                                "accept": "*/*",
                                "accept-language": "zh-Hans-CN;q=1",
                                "token": "",
                                "accept-encoding": "br, gzip, deflate",
                                "deviceid": "D0561E6E-BFCE-4956-AF43-E1DA07D8E1FC",
                                "user-agent": "guang ming ri bao/9.0.2 (iPhone; iOS 12.0.1; Scale/2.00)",
                                "language": "1",
                                "ua": "IOS+iPhone 6s+9.0.2+",
                                "content-length": "48",
                            }
                            data = {}
                            detailjson = {
                                "contentId": tmpid
                            }

                            res = self._session.post(url, headers=headers, data=data, json=detailjson).text
                            topic_json = json.loads(json.dumps(json.loads(res, strict=False), indent=4,
                                                               ensure_ascii=False))
                            topic_json = topic_json["data"]
                            # print("topicjson==", topic_json)

                            # 时间最近的新闻
                            newstime = topic_json["publishDt"]
                            if newstime > newestpubtime:
                                newestarticleiD = topic_json["contentId"]
                                newestpubtime = newstime

                            article_fields = InitClass().article_fields()
                            article_fields["appname"] = self.newsname
                            article_fields["specialtopic"] = 1  # 是否是专题
                            article_fields["topicid"] = zhuanti_id
                            article_fields["channelname"] = channelname
                            article_fields["channelID"] = channelid
                            article_fields["banner"] = banner
                            article_fields["appname"] = self.newsname
                            self.formatearticledetail(topic_json, article_fields)

                    fields["articleIDs"] = articleids
                    if newestarticleiD:
                        fields["newestArticleID"] = newestarticleiD
                        fields["newestPubtime"] = newestpubtime

                    fields["articleNum"] = totaltopicnum

                    fields["pubTime"] = 0
                    fields["createTime"] = 0
                    fields["updateTime"] = 0

                    print("专题 fields==", json.dumps(fields, indent=4, ensure_ascii=False))
                except Exception as e:
                    logging.info(f"专题 错误数量{num},{e}")
                    num += 1
            else:
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                    # print("普通 content_s==",content_s)
                    content_s = content_s["data"]
                    fields["appname"] = self.newsname
                    self.formatearticledetail(content_s,fields)
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
    appspider = Guangmingribao2("光明日报2")
    appspider.run()
