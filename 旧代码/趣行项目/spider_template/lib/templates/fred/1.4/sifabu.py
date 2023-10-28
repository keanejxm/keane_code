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

class XinHuNan(Appspider):

    @staticmethod
    def get_app_params():
        # 司法部-首页
        url = "https://app.moj.gov.cn/api/rest/api/v1.0/bootdiagramAndFirstPage/channelList"
        headers = {
            "Host": "app.moj.gov.cn",
            "Accept": "*/*",
            "Accept-Language": "zh-cn",
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "%E5%8F%B8%E6%B3%95%E9%83%A8/3 CFNetwork/1197 Darwin/20.0.0",
        }
        data = {
            "siteId": 1,
            "deviceId": "E5D428A8-F04C-424D-8D5D-D0434D29CF26",
            "deviceManufacture": "Apple",
            "deviceModel": "iPhone",
            "appChannel": "yingyongbao",
            "appCode": 3,
            "appVersion": "1.2",
            "deviceSysVersion": "14.1",
            "deviceSysType": "iOS",
            "network": ""
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []

        # 司法部-政务公开
        url = "https://app.moj.gov.cn/api/rest/api/v1.0/bootdiagramAndFirstPage/channelBycode"
        headers = {
            "Host": "app.moj.gov.cn",
            "Accept": "*/*",
            "Accept-Language": "zh-cn",
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "%E5%8F%B8%E6%B3%95%E9%83%A8/3 CFNetwork/1197 Darwin/20.0.0",
        }
        data = {
            "siteId": 1,
            "uniqueCode": "zhengwugongkai",
            "deviceId": "E5D428A8-F04C-424D-8D5D-D0434D29CF26",
            "deviceManufacture": "Apple",
            "deviceModel": "iPhone",
            "appChannel": "yingyongbao",
            "appCode": 3,
            "appVersion": "1.2",
            "deviceSysVersion": "14.1",
            "deviceSysType": "iOS",
            "network": ""
        }


        zwres = requests.get(url, headers=headers, params=data).text
        zujson = json.loads(json.dumps(json.loads(zwres, strict=False), indent=4, ensure_ascii=False))
        zwretobj = zujson["ret"]
        zwchannellist = zwretobj["list"]
        for channel in zwchannellist:
            channelname = channel["name"]
            channelid = channel["id"]
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)

        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        retobj = channelslists["ret"]
        channellist = retobj["list"]
        for channel in channellist:
            channelname = channel["name"]
            channelid = channel["id"]
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "https://app.moj.gov.cn/api/rest/api/v1.0/showContent"
        headers = {
            "Host": "app.moj.gov.cn",
            "Accept": "*/*",
            "Accept-Language": "zh-cn",
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "%E5%8F%B8%E6%B3%95%E9%83%A8/3 CFNetwork/1197 Darwin/20.0.0",
        }
        method = 'get'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            data = {
                "siteId": 1,
                "pageNo": 1,
                "channelId": channelid,
                "deviceId": "E5D428A8-F04C-424D-8D5D-D0434D29CF26",
                "deviceManufacture": "Apple",
                "deviceModel": "iPhone",
                "appChannel": "yingyongbao",
                "appCode": 3,
                "appVersion": "1.2",
                "deviceSysVersion": "14.1",
                "deviceSysType": "iOS",
                "network": "",
            }
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid = channelid, data = data,
                                                                       channeltype = channeltype)
            articlelistsparams.append(articlelist_param)
        yield articlelistsparams

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            channel_type = articleslistres.get("channeltype")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent = 4, ensure_ascii = False))

                try:
                    # print("articleslists==", articleslists)
                    retobj = articleslists["ret"]
                    contentlist = retobj["contentList"]
                    bannerlist = retobj["carouselList"]

                    #banner列表
                    # bannerlist = []
                    for article in bannerlist:

                        #1 普通 可能有url
                        #11 专题 advertUrl
                        articleid = article["contentId"]
                        articlename = article["imgTitile"]

                        coverurl = article["imgUrl"]
                        if coverurl:
                            coverurl = "https://app.moj.gov.cn" + coverurl
                        article_covers = list()
                        article_covers.append(coverurl)

                        contenttype = article["contentType"]
                        if contenttype == "11":

                            adverturl = article["advertUrl"]

                            topic_fields = InitClass().topic_fields()
                            topic_fields["topicID"] = articleid
                            topic_fields["platformName"] = "司法部"
                            topic_fields["channelName"] = channelname
                            topic_fields["channelID"] = channelid
                            topic_fields["topicUrl"] = adverturl
                            topic_fields["title"] = articlename
                            topic_fields["topicCover"] = article_covers
                            topic_fields["topic"] = 1
                            topic_fields["pubTime"] = 0
                            topic_fields["articleNum"] = 0
                            topic_fields["createTime"] = 0
                            topic_fields["updateTime"] = 0
                            print("外部专题或h5页=", json.dumps(topic_fields, indent=4, ensure_ascii=False))
                            continue
                        else:
                            #普通
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()

                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["workerid"] = articleid
                            article_fields["title"] = articlename
                            article_fields["articlecovers"] = article_covers
                            article_fields["banner"] = 1

                            articleparam["articleField"] = article_fields  # 携带文章采集的数据
                            articleparam["articleid"] = articleid
                            articlesparams.append(articleparam)

                    #列表
                    #contentlist = []
                    for article in contentlist:

                        articleid = article["id"]
                        articlename = article["title"]

                        coverurl = article["imgOneUrl"]
                        if coverurl:
                            coverurl = "https://app.moj.gov.cn" + coverurl
                        article_covers = list()
                        article_covers.append(coverurl)

                        contenttype = article["contentType"]
                        if contenttype == "11":
                            #专题
                            adverturl = article["advertUrl"]

                            topic_fields = InitClass().topic_fields()
                            topic_fields["topicID"] = articleid
                            topic_fields["platformName"] = "司法部"
                            topic_fields["channelName"] = channelname
                            topic_fields["channelID"] = channelid
                            topic_fields["topicUrl"] = adverturl
                            topic_fields["title"] = articlename
                            topic_fields["topicCover"] = article_covers
                            topic_fields["topic"] = 1
                            topic_fields["pubTime"] = 0
                            topic_fields["articleNum"] = 0
                            topic_fields["createTime"] = 0
                            topic_fields["updateTime"] = 0
                            print("外部专题或h5页===", json.dumps(topic_fields, indent=4, ensure_ascii=False))
                            continue
                        else:
                            #普通
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()

                            # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["workerid"] = articleid
                            article_fields["title"] = articlename
                            article_fields["articlecovers"] = article_covers
                            article_fields["banner"] = 0

                            articleparam["articleField"] = article_fields
                            articleparam["articleid"] = articleid
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
            if topic == 1:
                print("zhuanti")
                continue
            else:
                url = "https://app.moj.gov.cn/api/rest/api/v1.0/contentDetail"
                headers = {
                    "Host": "app.moj.gov.cn",
                    "Accept": "*/*",
                    "Accept-Language": "zh-cn",
                    "Connection": "keep-alive",
                    "Accept-Encoding": "gzip, deflate, br",
                    "User-Agent": "%E5%8F%B8%E6%B3%95%E9%83%A8/3 CFNetwork/1197 Darwin/20.0.0",
                }
                data = {
                    "contentId": articleid,
                    "memberId": "E5D428A8-F04C-424D-8D5D-D0434D29CF26",
                    "siteId": 1,
                    "deviceId": "E5D428A8-F04C-424D-8D5D-D0434D29CF26",
                    "deviceManufacture": "Apple",
                    "deviceModel": "iPhone",
                    "appChannel": "yingyongbao",
                    "appCode": 3,
                    "appVersion": "1.2",
                    "deviceSysVersion": "14.1",
                    "deviceSysType": "iOS",
                    "network": "",
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
            if topic:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                print("专题content_s=",content_s)
            try:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                #print("普通content_s=",content_s)

                contentdetail = content_s["ret"]
                content = contentdetail["conent"]
                source = contentdetail["sourceid"]
                commentnum = contentdetail["commentnum"]
                likenum =contentdetail["supportcount"]

                pubtime = contentdetail["publishDate"]
                pubtime = InitClass().date_time_stamp(pubtime)

                shareUrl = contentdetail["shareUrl"]
                shareUrl = "https://app.moj.gov.cn" + shareUrl

                fields["pubtime"] = pubtime
                fields["url"] = shareUrl
                fields["appname"] = self.newsname
                fields["content"] = content
                fields["source"] = source
                fields["commentnum"] = int(commentnum)
                fields["likenum"] = likenum

                fields["createtime"] = 0
                fields["updatetime"] = 0
                fields["videocover"] = []
                try:
                    videos = InitClass().get_video(content)
                    videolist = list()
                    for videoitem in videos:
                        if not "http" in videoitem:
                            newurl = "https://app.moj.gov.cn" + videoitem
                            videolist.append(newurl)
                    fields["videos"] = videolist
                except Exception as e:
                    print("无视频")

                try:
                    images = InitClass().get_images(content)
                    imglist = list()
                    for imgitem in images:
                        if not "http" in imgitem:
                            newurl = "https://app.moj.gov.cn" + imgitem
                            imglist.append(newurl)
                    fields["images"] = imglist

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
    appspider = XinHuNan("司法部")
    appspider.run()
