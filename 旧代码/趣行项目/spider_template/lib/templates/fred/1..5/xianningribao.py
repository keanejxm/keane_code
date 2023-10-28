# -*- encoding:utf-8 -*-
"""
@功能:新湖南解析模板
@AUTHOR：Keane
@文件名：xinhunan.py
@时间：2020/12/17  17:33
"""


import json
import logging
import bs4
import requests
# import time

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


class Xianningribao(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://dq.xianning.gov.cn/api/wcm/channel/nav.do?clientId=xnnews&clientSecret=eG5OZXdzQDIwMTgjQCNA"
        headers = {
            "Host": "dq.xianning.gov.cn",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 Html5Plus/1.0 (Immersed/23.846153) xnnews/Android-3.3",
            "X-Requested-With": "XMLHttpRequest",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,en-US;q=0.8",
            "Connection": "keep-alive"
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
        channellist = channelslists["data"]

        for channel in channellist:
            channelname = channel["CHNLDESC"]
            channelid = channel["CHANNELID"]
            channeltype = channel["CHNLTYPE"]
            channelparam = InitClass().channel_fields(channelid, channelname,channeltype=channeltype)
            channelsparams.append(channelparam)

        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        headers = {
            "Host": "dq.xianning.gov.cn",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 Html5Plus/1.0 (Immersed/23.846153) xnnews/Android-3.3",
            "X-Requested-With": "XMLHttpRequest",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,en-US;q=0.8",
            "Connection": "keep-alive"
        }
        method = 'post'
        data = {}
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            url = "http://dq.xianning.gov.cn/api/wcm/document/getByChnlId.do?userId=&pageIndex=1&clientId=xnnews&clientSecret=eG5OZXdzQDIwMTgjQCNA&chnlId=" + str(channelid)

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,channelid = channelid, data = data,channeltype = channeltype)
            articlelistsparams.append(articlelist_param)

        yield articlelistsparams

    @staticmethod
    def formatearticlelist(article,channelid,channelname,channeltype,bannertag):

        articleid = article["DOCID"]
        articletitle = article["DOCTITLE"]
        covers = article["LISTPICS"]
        # 20文字
        # 60 有视频
        # 2 专题
        # 30 外链
        articletype = article["DOCTYPE"]
        if articletype == 20 or articletype == 60:
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
            return articleparam

        elif articletype == 2:

            articleid = article["DOCCHANNEL"]
            url = article["DOCPUBURL"]
            source = article["DOCSOURCENAME"]
            createtime = article["DOCRELTIME"]

            # 专题新闻
            topic_fields = InitClass().topic_fields()
            articleparam = InitClass().article_list_fields()

            topic_fields["topicID"] = articleid
            topic_fields["channelName"] = channelname
            topic_fields["channelID"] = channelid
            topic_fields["channelType"] = channeltype

            topic_fields["title"] = articletitle
            topic_fields["topicCover"] = covers

            topic_fields["topic"] = 1
            topic_fields["topicUrl"] = url

            topic_fields["pubTime"] = 0
            topic_fields["updateTime"] = 0
            topic_fields["region"] = source
            topic_fields["createTime"] = InitClass().date_time_stamp(createtime)


            articleparam["articleField"] = topic_fields  # 携带文章采集的数据
            articleparam["articleid"] = articleid
            articleparam["channelname"] = channelname
            return articleparam

        elif articletype == 30:

            createtime = article["DOCRELTIME"]
            source = article["DOCSOURCENAME"]
            title = article["DOCTITLE"]

            article_fields = InitClass().article_fields()
            article_fields["channelID"] = channelid
            article_fields["channelname"] = channelname
            article_fields["channelType"] = channeltype
            article_fields["workerid"] = articleid
            article_fields["articlecovers"] = covers
            article_fields["banner"] = bannertag

            article_fields["title"] = title
            article_fields["source"] = source
            article_fields["createtime"] = InitClass().date_time_stamp(createtime)

            url = article["DOCPUBURL"]
            try:
                # 请求newsurl 获取正文
                res = requests.get(url)
                res.encoding = 'utf8'
                bf = bs4.BeautifulSoup(res.text, 'html.parser')
                content = bf.find('div', class_='mui-text').decode()
                # print("content=",content)
                article_fields["content"] = content

                article_fields["videocover"] = []
                try:
                    videos = InitClass().get_video(content)
                    article_fields["videos"] = videos
                except Exception as e:
                    print("无视频")

                try:
                    images = InitClass().get_images(content)
                    article_fields["images"] = images
                except Exception as e:
                    print("无图片")

            except Exception as e:
                print("无html格式正文")
            article_fields["appname"] = "咸宁日报"
            article_fields["url"] = url
            article_fields["pubtime"] = 0
            article_fields["updatetime"] = 0

            print("外链==", json.dumps(article_fields, indent=4, ensure_ascii=False))
        else:

            print("未知")
            print("articletype=", articletype, "articletitle=", articletitle)
            return

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
                    datalist = articleslists["data"]

                    objlist = datalist["SUBJECTS"]
                    bannerlist = datalist["FOCUSIMAGES"]
                    contentlist = datalist["DOCUMENTS"]
                    for article in bannerlist:
                        articleparam = self.formatearticlelist(article, channelid, channelname, channel_type, 1)
                        if articleparam:
                            articlesparams.append(articleparam)

                    for article in contentlist + objlist:
                        articleparam = self.formatearticlelist(article,channelid,channelname,channel_type,0)
                        if articleparam:
                            articlesparams.append(articleparam)

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
            # channelname = article_field.get("channelname")

            if topic == 1:
                url = 'http://dq.xianning.gov.cn/api/wcm/channel/getSubjectChnlsAndDocs.do'
                headers = {
                    "Host": "dq.xianning.gov.cn",
                    "Accept": "*/*",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 Html5Plus/1.0 (Immersed/23.846153) xnnews/Android-3.3",
                    "X-Requested-With": "XMLHttpRequest",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,en-US;q=0.8",
                    "Connection": "keep-alive"
                }
                data = {
                    "chnlId": articleid,
                    "userId": "",
                    "clientId": "xnnews",
                    "clientSecret": "eG5OZXdzQDIwMTgjQCNA"
                }
                method = 'get'
            else:
                url = "http://dq.xianning.gov.cn/api/wcm/document/getByDocId.do"
                headers = {
                    "Host": "dq.xianning.gov.cn",
                    "Content-Length": "71",
                    "Accept": "*/*",
                    "Origin": "file://",
                    "X-Requested-With": "XMLHttpRequest",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 Html5Plus/1.0 (Immersed/23.846153) xnnews/Android-3.3",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,en-US;q=0.8",
                    "Connection": "keep-alive"
                }
                data = {
                    "docId": articleid,
                    "userId": "",
                    "clientId": "xnnews",
                    "clientSecret": "eG5OZXdzQDIwMTgjQCNA"
                }
                method = 'post'

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

                content_s = json.loads(json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                # print("content_s=",content_s)
                if topic == 1:

                    channelid = fields["channelID"]
                    channelname = fields["channelName"]
                    channeltype = fields["channelType"]

                    topicid = fields["topicID"]
                    topictitle = fields["title"]

                    topicnum = 0
                    newestarticleid = ""
                    newestpubtime = 0

                    childlist = content_s["data"]["CHILDREN"]
                    for section in childlist:

                        # subchannelid = section["CHANNELID"]
                        # suburl = "http://dq.xianning.gov.cn/api/wcm/document/getByChnlId.do"
                        # subheader = {
                        #     "Host": "dq.xianning.gov.cn",
                        #     "Accept": "*/*",
                        #     "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 Html5Plus/1.0 (Immersed/23.846153) xnnews/Android-3.3",
                        #     "X-Requested-With": "XMLHttpRequest",
                        #     "Accept-Encoding": "gzip, deflate",
                        #     "Accept-Language": "zh-CN,en-US;q=0.8",
                        #     "Connection": "keep-alive"
                        # }
                        # subdata = {
                        #     "chnlId": subchannelid,
                        #     "userId": "",
                        #     "pageIndex": 1,
                        #     "clientId": "xnnews",
                        #     "clientSecret": "eG5OZXdzQDIwMTgjQCNA"
                        # }
                        # subres = requests.get(suburl,headers=subheader,params=subdata).text
                        # subjson = json.loads(json.dumps(json.loads(subres, strict=False), indent=4,ensure_ascii=False))
                        datalist = section["DOCUMENTS"]
                        for article in datalist:

                            topicnum += 1

                            achildid = article["DOCID"]
                            acovers = article["LISTPICS"]
                            # aurl = article["DOCPUBURL"]
                            # atitle = article["DOCTITLE"]
                            # asource = article["DOCSOURCENAME"]
                            url = "http://dq.xianning.gov.cn/api/wcm/document/getByDocId.do"
                            headers = {
                                "Host": "dq.xianning.gov.cn",
                                "Content-Length": "71",
                                "Accept": "*/*",
                                "Origin": "file://",
                                "X-Requested-With": "XMLHttpRequest",
                                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 Html5Plus/1.0 (Immersed/23.846153) xnnews/Android-3.3",
                                "Content-Type": "application/x-www-form-urlencoded",
                                "Accept-Encoding": "gzip, deflate",
                                "Accept-Language": "zh-CN,en-US;q=0.8",
                                "Connection": "keep-alive"
                            }
                            data = {
                                "docId": achildid,
                                "userId": "",
                                "clientId": "xnnews",
                                "clientSecret": "eG5OZXdzQDIwMTgjQCNA"
                            }
                            itemres = requests.post(url, headers=headers, data=data).text
                            detailjson = json.loads(json.dumps(json.loads(itemres, strict=False), indent=4, ensure_ascii=False))
                            # print("detailjson=",detailjson)

                            contentdetail = detailjson["data"]["DOCUMENT"]

                            createtime = contentdetail["CRTIME"]
                            pubtime = contentdetail["DOCPUBTIME"]
                            uptime = contentdetail["OPERTIME"]

                            pubtime = InitClass().date_time_stamp(pubtime)
                            pubtime = int(pubtime)
                            if pubtime > newestpubtime:
                                pubtime = newestpubtime
                                newestarticleid = achildid


                            source = contentdetail["DOCSOURCENAME"]
                            title = contentdetail["DOCTITLE"]
                            url = contentdetail["DOCPUBURL"]

                            likenum = contentdetail["LIKECOUNT"]
                            commentnum = contentdetail["COMMENTCOUNT"]
                            content = contentdetail["DOCHTMLCON"]
                            author = contentdetail['CRUSER']

                            article_fields = InitClass().article_fields()
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channelType"] = channeltype
                            article_fields["workerid"] = achildid
                            article_fields["articlecovers"] = acovers

                            article_fields["title"] = title
                            article_fields["updatetime"] = InitClass().date_time_stamp(uptime)
                            article_fields["pubtime"] = pubtime
                            article_fields["createtime"] = InitClass().date_time_stamp(createtime)
                            article_fields["url"] = url

                            article_fields["appname"] = self.newsname
                            article_fields["content"] = content
                            article_fields["source"] = source
                            article_fields["commentnum"] = commentnum
                            article_fields["likenum"] = likenum
                            article_fields["readnum"] = 0
                            article_fields["author"] = author

                            # fields["pubtime"] = 0
                            # fields["createtime"] = 0
                            article_fields["videocover"] = []
                            try:
                                videos = InitClass().get_video(content)
                                article_fields["videos"] = videos
                            except Exception as e:
                                print("无视频")

                            try:
                                images = InitClass().get_images(content)
                                article_fields["images"] = images
                            except Exception as e:
                                print("无图片")
                            article_fields["specialtopic"] = 1
                            article_fields["topicid"] = topicid
                            article_fields["topicTitle"] = topictitle
                            print("专题内文章==", json.dumps(article_fields, indent=4, ensure_ascii=False))
                    fields["platformName"] = self.newsname
                    fields["articleNum"] = topicnum
                    fields["newestArticleID"] = newestarticleid

                    print("大专题==",json.dumps(fields, indent = 4, ensure_ascii = False))


                else:

                    contentdetail = content_s["data"]["DOCUMENT"]

                    createtime = contentdetail["CRTIME"]
                    pubtime = contentdetail["DOCPUBTIME"]
                    uptime = contentdetail["OPERTIME"]
                    source = contentdetail["DOCSOURCENAME"]
                    title = contentdetail["DOCTITLE"]
                    url = contentdetail["DOCPUBURL"]

                    likenum = contentdetail["LIKECOUNT"]
                    commentnum = contentdetail["COMMENTCOUNT"]
                    content = contentdetail["DOCHTMLCON"]
                    author = contentdetail['CRUSER']

                    fields["title"] = title
                    fields["updatetime"] = InitClass().date_time_stamp(uptime)
                    fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                    fields["createtime"] = InitClass().date_time_stamp(createtime)
                    fields["url"] = url


                    fields["appname"] = self.newsname
                    fields["content"] = content
                    fields["source"] = source
                    fields["commentnum"] = commentnum
                    fields["likenum"] = likenum
                    fields["readnum"] = 0
                    fields["author"] = author

                    # fields["pubtime"] = 0
                    # fields["createtime"] = 0
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
    appspider = Xianningribao("咸宁日报")
    appspider.run()
