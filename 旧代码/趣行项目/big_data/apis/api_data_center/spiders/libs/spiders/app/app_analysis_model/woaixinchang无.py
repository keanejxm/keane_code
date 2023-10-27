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


class Woaixinchang(Appspider):

    #请求各频道
    @staticmethod
    def getarticlelistparams():

        articlelistsparams = []
        method = 'post'
        headers = {
            "Host": "www.waxcapp.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": "acw_tc=76b20f6016092309770632362e22d055f7694f90a09cbe46dae4aadd803038",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "User-Agent": "iPhone10,3(iOS/14.1) Uninview(Uninview/1.0.0) Weex/0.26.0 1125x2436",
            "Content-Length": "59",
            "Accept-Language": "zh-cn",
            "Accept-Encoding": "gzip, deflate, br",
        }

        # 融媒体
        rmname = "融媒体"
        rchannelid = "0"

        #video
        xwurl = "https://www.waxcapp.com/web/video/get_video_channel.php"
        xwdata = {
            "if_radio": 0,
            "user_id": "",
            "version": "1.2.2"
        }
        xw_param = InitClass().articlelists_params_fields(xwurl, headers, method, rmname,channelid=rchannelid, data=xwdata)
        articlelistsparams.append(xw_param)

        #radio
        radiodata = {
            "if_radio": 1,
            "user_id": "",
            "version": "1.2.2"
        }
        radio_param = InitClass().articlelists_params_fields(xwurl, headers, method, rmname, channelid=rchannelid,
                                                          data=radiodata)
        articlelistsparams.append(radio_param)

        #直播
        livechannelname = "直播"
        liveurl = "https://www.waxcapp.com/web/video/get_video_live_playback.php"
        livedata = {
            "page": 1,
            "recs": 100,
            "user_id": "",
            "version": "1.2.2"
        }
        live_param = InitClass().articlelists_params_fields(liveurl, headers, method, livechannelname, channelid=rchannelid,
                                                          data=livedata)
        articlelistsparams.append(live_param)

        channeltype = ""
        channelid = 0
        channelname = "首页"

        url = "https://www.waxcapp.com/web/news/get_main_news.php"
        #banner 5
        # 政事 4
        # 热点 3
        # 推荐 2
        hots = [2,3,4,5]
        banner = 0
        for hottag in hots:
            if hottag == 5:
                banner = 1

            data = {
                "if_hot": hottag,
                "recs": 7,
                "hot_news": "",
                "user_id": "",
                "version": "1.2.2",
                "page": 1
            }
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid=channelid, data=data,
                                                                       channeltype=channeltype, banners=banner)
            articlelistsparams.append(articlelist_param)
        yield articlelistsparams

    #解析各频道列表
    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            channel_type = articleslistres.get("channeltype")
            banner = articleslistres.get("banner")

            try:

                if channelname == '直播':
                    articlejson = eval(articleslists)
                    print("articlejson==", articlejson)
                    for liveitem in articlejson:
                        articleid = liveitem["live_id"]
                        articletitle = liveitem["live_name"]
                        readnum = liveitem["click_num"]
                        imgurl = liveitem["pic_url"]

                        createtime = liveitem["create_date"]
                        createtime = InitClass().date_time_stamp(createtime)

                        videourl = liveitem["video_url"]
                        intro = liveitem["introduce"]

                        # 普通
                        article_fields = InitClass().article_fields()
                        article_fields["appname"] = "我爱新昌"

                        article_fields["channelID"] = channelid
                        article_fields["channelname"] = channelname
                        article_fields["channelType"] = ""
                        article_fields["url"] = videourl

                        article_fields["workerid"] = articleid
                        article_fields["title"] = articletitle
                        article_fields["content"] = intro
                        article_fields["articlecovers"] = [imgurl]
                        article_fields["images"] = []
                        article_fields["videos"] = []
                        article_fields["videocover"] = []
                        article_fields["source"] = ""
                        article_fields["pubtime"] = 0
                        article_fields["createtime"] = createtime
                        article_fields["readnum"] = 0
                        article_fields["banner"] = 0
                        article_fields["specialtopic"] = 0
                        article_fields["likenum"] = 0
                        article_fields["playnum"] = 0
                        article_fields["updatetime"] = 0
                        print("融媒体直播文章=====", json.dumps(article_fields, indent=4, ensure_ascii=False))
                    continue
                else:
                    articleslists = json.loads(json.dumps(json.loads(articleslists), indent = 4, ensure_ascii = False))
                    try:

                        if channelname == "融媒体":
                            # 融媒体列表
                            recomlist = articleslists["ondemand"]
                            # print("recomlist=",recomlist)
                            for reitem in recomlist:
                                itemid = reitem["channel_id"]
                                itemname = reitem["channel_name"]
                                # itempic = reitem["pic_url"]

                                itemurl = "https://www.waxcapp.com/web/video/get_video_channel_program.php"
                                itemheader = {
                                    "Host": "www.waxcapp.com",
                                    "Content-Type": "application/x-www-form-urlencoded",
                                    "Cookie": "acw_tc=76b20f6016092309770632362e22d055f7694f90a09cbe46dae4aadd803038",
                                    "Connection": "keep-alive",
                                    "Accept": "*/*",
                                    "User-Agent": "iPhone10,3(iOS/14.1) Uninview(Uninview/1.0.0) Weex/0.26.0 1125x2436",
                                    "Content-Length": "59",
                                    "Accept-Language": "zh-cn",
                                    "Accept-Encoding": "gzip, deflate, br",
                                }
                                itemdata = {
                                    "channel_id": itemid,
                                    "page": 1,
                                    "recs": 14
                                }

                                itemres = requests.post(itemurl, headers=itemheader, data=itemdata).text
                                itemlist = json.loads(json.dumps(json.loads(itemres, strict=False), indent=4, ensure_ascii=False))

                                for row in itemlist:
                                    articleid = row["program_id"]
                                    articletitle = row["program_name"]
                                    videourl = row["play_url"]
                                    videocover = row["detail_pic"]
                                    imgurl = row["pic_url"]
                                    intro = row["introduce"]

                                    createtime = row["create_date"]
                                    createtime = InitClass().date_time_stamp(createtime)

                                    # 普通
                                    article_fields = InitClass().article_fields()
                                    article_fields["appname"] = "我爱新昌"

                                    article_fields["channelID"] = itemid
                                    article_fields["channelname"] = itemname
                                    article_fields["channelType"] = ""
                                    article_fields["url"] = itemurl

                                    article_fields["workerid"] = articleid
                                    article_fields["title"] = articletitle
                                    article_fields["content"] = intro
                                    article_fields["articlecovers"] = [imgurl]
                                    article_fields["images"] = []
                                    article_fields["videos"] = [videourl]
                                    article_fields["videocover"] = [videocover]
                                    article_fields["source"] = ""
                                    article_fields["pubtime"] = 0
                                    article_fields["createtime"] = createtime
                                    article_fields["readnum"] = 0
                                    article_fields["banner"] = 0
                                    article_fields["specialtopic"] = 0
                                    article_fields["likenum"] = 0
                                    article_fields["playnum"] = 0
                                    article_fields["updatetime"] = 0
                                    print("融媒体文章=====", json.dumps(article_fields, indent=4, ensure_ascii=False))
                                    continue

                        else:
                            #列表新闻
                            for article in articleslists:
                                if "linkID" in article.keys():

                                    articleid = article["news_id"]
                                    articletitle = article["news_title"]

                                    imgurl = article["pic_uri"]
                                    covers = list()
                                    covers.append(imgurl)

                                    createtime = article["create_date"]
                                    createtime = InitClass().date_time_stamp(createtime)

                                    istopic = article["if_miui"]
                                    readnum = article["click_num"]

                                    # print("istopic==",istopic,"articleid==",articleid,"articletitle=",articletitle)
                                    if istopic == "1" and banner == 1:
                                        # 专题
                                        topic_fields = InitClass().topic_fields()
                                        articleparam = InitClass().article_list_fields()

                                        topic_fields["topicID"] = articleid
                                        topic_fields["channelName"] = channelname
                                        topic_fields["channelID"] = channelid
                                        topic_fields["title"] = articletitle
                                        topic_fields["topicCover"] = covers
                                        topic_fields["createTime"] = createtime
                                        topic_fields["topic"] = 1
                                        topic_fields["banner"] = banner

                                        articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                        articleparam["articleid"] = articleid
                                        articlesparams.append(articleparam)
                                    else:
                                        # 普通
                                        article_fields = InitClass().article_fields()
                                        articleparam = InitClass().article_list_fields()

                                        article_fields["channelID"] = channelid
                                        article_fields["channelname"] = channelname
                                        article_fields["channelType"] = ""
                                        article_fields["workerid"] = articleid
                                        article_fields["title"] = articletitle
                                        article_fields["articlecovers"] = covers
                                        article_fields["readnum"] = readnum
                                        article_fields["banner"] = banner
                                        article_fields["specialtopic"] = 0
                                        article_fields["videocover"] = []
                                        article_fields["createtime"] = createtime

                                        articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                        articleparam["articleid"] = articleid
                                        articleparam["channelID"] = channelid
                                        articlesparams.append(articleparam)
                                else:
                                    #列表中"更多"等占位
                                    continue

                    except Exception as e:
                        logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")
        yield articlesparams

    #请求稿件
    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        for article in articles:
            articleid = article.get("articleid")
            channelid = article.get("channelID")
            article_field = article.get("articleField")
            topic = article_field.get("topic")

            if topic == 1:
                # get categoryid
                topicurl = "https://www.waxcapp.com/web/news/get_special_news_category.php"
                topicheaders = {
                    "Host": "www.waxcapp.com",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Cookie": "acw_tc=76b20f6016092309770632362e22d055f7694f90a09cbe46dae4aadd803038",
                    "Connection": "keep-alive",
                    "Accept": "*/*",
                    "User-Agent": "iPhone10,3(iOS/14.1) Uninview(Uninview/1.0.0) Weex/0.26.0 1125x2436",
                    "Content-Length": "35",
                    "Accept-Language": "zh-cn",
                    "Accept-Encoding": "gzip, deflate, br",
                }
                topicdata = {
                    "news_id": articleid,
                    "user_id": "",
                    "version": "1.2.2"
                }

                topicres = requests.post(topicurl, headers=topicheaders, data=topicdata).text
                topicjson = json.loads(json.dumps(json.loads(topicres, strict=False), indent=4,ensure_ascii=False))
                topicinfo = topicjson[0]
                categoryid = topicinfo["special_news_category_id"]

                #get topic info
                nameurl = "https://www.waxcapp.com/web/news/get_special_news_title.php"
                namedata = {
                    "special_news_id": articleid,
                    "user_id": "",
                    "version": "1.2.2"
                }
                nameres = requests.post(nameurl, headers=topicheaders, data=namedata).text
                namejson = json.loads(json.dumps(json.loads(nameres, strict=False), indent=4, ensure_ascii=False))
                nameinfo = namejson[0]
                desinfo = nameinfo["news_content"]

                article_field["digest"] = desinfo
                # print("categoryid==",categoryid,"desinfo=",desinfo)

                #请求列表
                url = "https://www.waxcapp.com/web/news/get_special_news_list.php"
                headers = topicheaders
                data = {
                    "special_news_id":articleid,
                    "special_news_category_id": categoryid,
                    "user_id":"",
                    "version":"1.2.2",
                    "page":1,
                    "recs":10
                }
                article_field["topicUrl"] = url

            else:
                url = "https://www.waxcapp.com/web/news/get_news_detail_content.php"
                headers = {
                    "Host": "www.waxcapp.com",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Cookie": "acw_tc=76b20f6016092309770632362e22d055f7694f90a09cbe46dae4aadd803038",
                    "Connection": "keep-alive",
                    "Accept": "*/*",
                    "User-Agent": "iPhone10,3(iOS/14.1) Uninview(Uninview/1.0.0) Weex/0.26.0 1125x2436",
                    "Content-Length": "59",
                    "Accept-Language": "zh-cn",
                    "Accept-Encoding": "gzip, deflate, br",
                }
                data = {
                    "news_id": articleid,
                    "user_id": ""
                }
                article_field["url"] = "https://www.waxcapp.com/m.web/news_detail_content/news_detail_content.php?news_id="+ str(articleid)

            method = 'post'
            articleparam = InitClass().article_params_fields(url, headers, method, data = data,
                                                             article_field = article_field)
            articleparams.append(articleparam)
        yield articleparams

    #解析稿件详情
    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            topic = fields.get("topic")
            if topic:
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                    # print("专题content_s=",content_s)

                    channelid = fields["channelID"]
                    channelname = fields["channelName"]
                    topicid = fields["topicID"]
                    topicname = fields["title"]

                    topicnum = len(content_s)
                    newestarticleid = ""
                    newestarticlepub = 0

                    for article in content_s:
                        articleid = article["news_id"]
                        articletitle = article["news_title"]

                        imgurl = article["pic_uri"]
                        covers = list()
                        covers.append(imgurl)

                        readnum = article["click_num"]

                        article_fields = InitClass().article_fields()

                        article_fields["channelID"] = channelid
                        article_fields["channelname"] = channelname
                        article_fields["channelType"] = ""
                        article_fields["workerid"] = articleid
                        article_fields["title"] = articletitle
                        article_fields["articlecovers"] = covers
                        article_fields["readnum"] = readnum
                        article_fields["banner"] = 0
                        article_fields["specialtopic"] = 1
                        article_fields["topicid"] = topicid
                        article_fields["topicTitle"] = topicname

                        article_fields["videocover"] = []
                        article_fields["url"] = "https://www.waxcapp.com/m.web/news_detail_content/news_detail_content.php?news_id=" + str(articleid)
                        # article_fields["createtime"] = createtime

                        url = "https://www.waxcapp.com/web/news/get_news_detail_content.php"
                        headers = {
                            "Host": "www.waxcapp.com",
                            "Content-Type": "application/x-www-form-urlencoded",
                            "Cookie": "acw_tc=76b20f6016092309770632362e22d055f7694f90a09cbe46dae4aadd803038",
                            "Connection": "keep-alive",
                            "Accept": "*/*",
                            "User-Agent": "iPhone10,3(iOS/14.1) Uninview(Uninview/1.0.0) Weex/0.26.0 1125x2436",
                            "Content-Length": "59",
                            "Accept-Language": "zh-cn",
                            "Accept-Encoding": "gzip, deflate, br",
                        }
                        data = {
                            "news_id": articleid,
                            "user_id": ""
                        }

                        detailres = requests.post(url, headers=headers, data=data).text
                        detailjson = json.loads(json.dumps(json.loads(detailres, strict=False), indent=4, ensure_ascii=False))
                        detail = detailjson[0]

                        createtime = detail["create_date"]
                        createtime = InitClass().date_time_stamp(createtime)

                        if createtime > newestarticlepub:
                            newestarticlepub = createtime
                            newestarticleid = articleid

                        content = detail["news_content2"]
                        author = detail["author"]

                        commentnum = detail["comment_num"]
                        likenum = detail["like_num"]

                        article_fields["appname"] = self.newsname
                        article_fields["author"] = author
                        article_fields["content"] = content
                        article_fields["commentnum"] = commentnum
                        article_fields["likenum"] = likenum
                        article_fields["createtime"] = createtime

                        article_fields["pubtime"] = 0
                        article_fields["updatetime"] = 0

                        try:
                            images = InitClass().get_images(content)
                            article_fields["images"] = images
                        except Exception as e:
                            print("无图片")

                        try:
                            videos = InitClass().get_video(content)
                            article_fields["videos"] = videos
                        except Exception as e:
                            print("无视频")
                        print("专题内文章=====", json.dumps(article_fields, indent=4, ensure_ascii=False))

                    fields["articleNum"] = topicnum
                    fields["newestArticleID"] = newestarticleid
                    fields["platformName"] = self.newsname
                    fields["pubTime"] = 0
                    fields["updateTime"] = 0

                    print("大专题=====", json.dumps(fields, indent=4, ensure_ascii=False))
                except Exception as e:
                    num += 1
                    logging.info(f"错误数量{num},{e}")

            else:
                #普通新闻
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                    # print("普通content_s==",content_s)

                    for article in content_s:

                        content = article["news_content2"]
                        author = article["author"]
                        commentnum = article["comment_num"]
                        likenum = article["like_num"]

                        fields["appname"] = self.newsname
                        fields["author"] = author
                        fields["content"] = content
                        fields["commentnum"] = commentnum
                        fields["likenum"] = likenum
                        fields["pubtime"] = 0
                        fields["updatetime"] = 0

                        try:
                            images = InitClass().get_images(content)
                            fields["images"] = images
                        except Exception as e:
                            print("无图片")

                        try:
                            videos = InitClass().get_video(content)
                            fields["videos"] = videos
                        except Exception as e:
                            print("无视频")

                        print("文章=====",json.dumps(fields, indent = 4, ensure_ascii = False))
                except Exception as e:
                    num += 1
                    logging.info(f"错误数量{num},{e}")

    def run(self):
        # appparams = self.get_app_params()
        # channelsres = self.getchannels(appparams.__next__())
        #channelsparams = self.analyze_channel(channelsres.__next__())
        articlelistparames = self.getarticlelistparams()
        articleslistsres = self.getarticlelists(articlelistparames.__next__())
        articles = self.analyze_articlelists(articleslistsres.__next__())
        articleparams = self.getarticleparams(articles.__next__())
        articlesres = self.getarticlehtml(articleparams.__next__())
        self.analyzearticle(articlesres.__next__())


if __name__ == '__main__':
    appspider = Woaixinchang("我爱新昌")
    appspider.run()
