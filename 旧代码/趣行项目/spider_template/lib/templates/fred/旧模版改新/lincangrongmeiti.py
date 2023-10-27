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
from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass

class Lincangrongmeiti(Appspider):

    #请求频道
    @staticmethod
    def get_app_params():
        url = "https://lincangapp.booyao.cn/API/getMenuList"
        headers = {
            "Host": "lincangapp.booyao.cn",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "User-Agent": "0.4.7 rv:1.4 (iPhone; iOS 12.0.1; zh_CN)",
            "Content-Length": "7",
            "Accept-Encoding": "gzip",
        }
        data = {
            "UserID":""
        }
        method = "post"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    #解析频道列表
    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        # print("channelslists==",channelslists)

        # channelid ="08d59fb9-9767-4a21-9ee1-e6ea5f2e1d2b"
        # channelname = "栏目"
        # channelparam = InitClass().channel_fields(channelid, channelname)
        # channelsparams.append(channelparam)

        for channel in channelslists:
            channelname = channel["Name"]
            if channelname == "矩阵":
                #都是介绍，外链
                continue
            channelid = channel["ID"]
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    #请求各频道列表数据
    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []

        headers = {
            "Host": "lincangapp.booyao.cn",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "User-Agent": "0.4.7 rv:1.4 (iPhone; iOS 12.0.1; zh_CN)",
            "Content-Length": "46",
            "Accept-Encoding": "gzip"
        }
        method = 'post'

        for channel in channelsparams:

            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = "" #channel.get("channelType")  # 此处没有若有可加上，其他一样

            url = ""
            data = {}

            if channelname == "要闻" or channelname == "微视频" or channelname == "栏目":
                url = "https://lincangapp.booyao.cn/API/getNewsListWithMenuID"
                data = {
                    "ID": channelid,
                    "Page": "1",
                }

            elif channelname == "直播":
                url = "https://lincangapp.booyao.cn/API/getLivesListWithMenuID"
                data = {
                    "ID": channelid
                }
            else:
                continue

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid = channelid, data = data,
                                                                       channeltype = channeltype)
            articlelistsparams.append(articlelist_param)

        yield articlelistsparams

    # 解析各频道列表数据
    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            channel_type = ""#articleslistres.get("channeltype")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent = 4, ensure_ascii = False))
                try:
                    #print("articleslists==",articleslists)

                    if channelname == "要闻":
                        banner_list = []
                        mid_list = []
                        article_list = []
                        count = len(articleslists)
                        if count == 3:
                            banner_list = articleslists[0]
                            mid_list = articleslists[1]
                            article_list = articleslists[2]
                        elif count > 3:
                            #数据异常
                            print("数据异常")
                        elif count == 2:
                            banner_list = articleslists[0]
                            article_list = articleslists[1]
                        elif count == 1:
                            article_list = articleslists[0]

                        #banner
                        for banneritem in banner_list:
                            articleid = banneritem["NewsID"]
                            # banneritem["Type"]
                            articlename = banneritem["Name"]
                            cover = banneritem["FileName"]
                            cover = "https://lincangapp.booyao.cn" + cover
                            article_covers = list()
                            article_covers.append(cover)

                            createtime = banneritem["CreateDateTime"]
                            createtime = createtime.replace("/Date(","")
                            createtime = createtime.replace(")/", "")

                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()

                            # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channelType"] = channel_type
                            article_fields["workerid"] = articleid
                            article_fields["title"] = articlename
                            article_fields["createtime"] = createtime
                            article_fields["articlecovers"] = article_covers
                            article_fields["banner"] = 1
                            # 将请求文章必需信息存入
                            articleparam["articleField"] = article_fields  # 携带文章采集的数据
                            articleparam["articleid"] = articleid
                            articlesparams.append(articleparam)

                        #topic
                        for topic in mid_list:
                            topicid = topic["LinkTopicID"]
                            topicname = topic["Name"]
                            topicurl = topic["FileName"]
                            topicurl = "https://lincangapp.booyao.cn" + topicurl

                            topiccreatetime = topic["CreateDateTime"]
                            topiccreatetime = topiccreatetime.replace("/Date(", "")
                            topiccreatetime = topiccreatetime.replace(")/", "")

                            topic = 1
                            article_covers = list()
                            article_covers.append(topicurl)

                            topic_fields = InitClass().topic_fields()
                            articleparam = InitClass().article_list_fields()

                            topic_fields["channelName"] = channelname
                            topic_fields["channelID"] = channelid
                            #topic_fields["channelType"] = channel_type
                            topic_fields["title"] = topicname
                            topic_fields["topicID"] = topicid
                            topic_fields["topicCover"] = article_covers
                            topic_fields["topic"] = topic
                            topic_fields["createTime"] = topiccreatetime

                            articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                            articleparam["articleid"] = topicid
                            articlesparams.append(articleparam)

                        #list
                        for article in article_list:
                            articleid = article["ID"]
                            articlename = article["Name"]
                            content = article["Content"]
                            author = article["CreateUserName"]
                            source = article["TopicName"]
                            readnum = article["Access"]
                            url = article["FileName"]
                            url = "https://lincangapp.booyao.cn" + url
                            article_covers = list()
                            article_covers.append(url)

                            pubtime = article["PassedDateTime"]
                            pubtime = pubtime.replace("/Date(", "")
                            pubtime = pubtime.replace(")/", "")

                            createtime = article["CreateDateTime"]
                            createtime = createtime.replace("/Date(", "")
                            createtime = createtime.replace(")/", "")

                            updatetime = article["ModifyDateTime"]
                            updatetime = updatetime.replace("/Date(", "")
                            updatetime = updatetime.replace(")/", "")

                            article_fields = InitClass().article_fields()
                            # articleparam = InitClass().article_list_fields()

                            article_fields["url"] = "https://lincangapp.booyao.cn/API/getNewsInfo?ID="+articleid
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channelType"] = channel_type
                            article_fields["workerid"] = articleid
                            article_fields["title"] = articlename
                            article_fields["readnum"] = readnum
                            article_fields["author"] = author
                            article_fields["pubtime"] = pubtime
                            article_fields["updatetime"] = updatetime
                            article_fields["content"] = content
                            article_fields["source"] = source
                            article_fields["createtime"] = createtime
                            article_fields["articlecovers"] = article_covers
                            article_fields["appname"] = "临沧融媒体"

                            article_fields["videocover"] = []


                            try:
                                videos = InitClass().get_video(content)
                                article_fields["videos"] = videos
                            except Exception as e:
                                print("正文无视频", )

                            try:
                                images = InitClass().get_images(content)
                                article_fields["images"] = images
                            except Exception as e:
                                print("正文无tupian")
                            # 将请求文章必需信息存入
                            # articleparam["articleField"] = article_fields  # 携带文章采集的数据
                            # articleparam["articleid"] = articleid
                            # articlesparams.append(articleparam)
                            print("文章==", json.dumps(article_fields, indent=4, ensure_ascii=False))
                        continue

                    elif channelname == "直播":
                        for zhibo in articleslists:

                            articletitle = zhibo["Name"]
                            liveid = zhibo["ID"]

                            url = zhibo["FileName"]
                            url = "https://lincangapp.booyao.cn" + url
                            article_covers = list()
                            article_covers.append(url)

                            pubtime = zhibo["PassedDateTime"]
                            pubtime = pubtime.replace("/Date(", "")
                            pubtime = pubtime.replace(")/", "")

                            createtime = zhibo["CreateDateTime"]
                            createtime = createtime.replace("/Date(", "")
                            createtime = createtime.replace(")/", "")

                            updatetime = zhibo["ModifyDateTime"]
                            updatetime = updatetime.replace("/Date(", "")
                            updatetime = updatetime.replace(")/", "")

                            liveurl = zhibo["OutWeb"]
                            readnum = zhibo["Access"]

                            article_fields = InitClass().article_fields()

                            article_fields["url"] = liveurl
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channelType"] = channel_type
                            article_fields["workerid"] = liveid
                            article_fields["title"] = articletitle
                            article_fields["readnum"] = readnum

                            article_fields["pubtime"] = pubtime
                            article_fields["updatetime"] = updatetime

                            article_fields["createtime"] = createtime
                            article_fields["articlecovers"] = article_covers
                            article_fields["appname"] = "临沧融媒体"
                            article_fields["images"] = []
                            article_fields["videocover"] = []



                            print("直播==", json.dumps(article_fields, indent=4, ensure_ascii=False))
                        continue

                    elif channelname == "微视频":
                        count = len(articleslists)
                        video_list = articleslists[count - 1]
                        for videoitem in video_list:

                            articleid = videoitem["ID"]
                            articlename =  videoitem["Name"]

                            source = videoitem["TopicName"]
                            content = videoitem["Content"]

                            cover = videoitem["FileName"]
                            cover = "https://lincangapp.booyao.cn" + cover
                            article_covers = list()
                            article_covers.append(cover)

                            createtime = videoitem["CreateDateTime"]
                            createtime = createtime.replace("/Date(", "")
                            createtime = createtime.replace(")/", "")

                            updatetime = videoitem["ModifyDateTime"]
                            updatetime = updatetime.replace("/Date(", "")
                            updatetime = updatetime.replace(")/", "")

                            pubtime = videoitem["PassedDateTime"]
                            pubtime = pubtime.replace("/Date(", "")
                            pubtime = pubtime.replace(")/", "")

                            readnum = videoitem["Access"]
                            author = videoitem["CreateUserName"]

                            article_fields = InitClass().article_fields()

                            # article_fields["url"] = liveurl
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channelType"] = channel_type
                            article_fields["workerid"] = articleid
                            article_fields["title"] = articlename
                            article_fields["readnum"] = readnum

                            article_fields["pubtime"] = pubtime
                            article_fields["updatetime"] = updatetime

                            article_fields["createtime"] = createtime
                            article_fields["articlecovers"] = article_covers
                            article_fields["appname"] = "临沧融媒体"
                            article_fields["author"] = author
                            article_fields["source"] = source
                            article_fields["content"] = content

                            article_fields["videocover"] = []


                            try:
                                videos = InitClass().get_video(content)
                                article_fields["videos"] = videos
                            except Exception as e:
                                print("正文无视频")

                            try:
                                images = InitClass().get_images(content)
                                article_fields["images"] = images
                            except Exception as e:
                                print("正文无tupian")

                            print("微视频", json.dumps(article_fields, indent=4, ensure_ascii=False))
                        continue

                    elif channelname == "栏目":

                        count = len(articleslists)
                        lanmu_list = articleslists[count - 1]

                        for lanmu in lanmu_list:

                            articleid = lanmu["ID"]
                            articlename = lanmu["Name"]
                            # createtime = lanmu["CreateDateTime"]
                            # createtime = createtime.replace("/Date(", "")
                            # createtime = createtime.replace(")/", "")

                            subchannelname = channelname + "-" + articlename
                            subchannelid = channelid + "-" + articleid

                            #请求二级列表

                            url = "https://lincangapp.booyao.cn/API/getNewsListWithProgramID"
                            headers = {
                                "Host": "lincangapp.booyao.cn",
                                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                                "User-Agent": "0.4.7 rv:1.4 (iPhone; iOS 12.0.1; zh_CN)",
                                "Content-Length": "46",
                                "Accept-Encoding": "gzip",
                            }
                            data = {
                                "ID": articleid
                            }

                            listres = requests.post(url,headers = headers,data=data).text
                            lanmulistjson = json.loads(json.dumps(json.loads(listres, strict=False), indent=4, ensure_ascii=False))
                            sublist = lanmulistjson
                            print("lanmulistjson ==", lanmulistjson)

                            for sublanmu in sublist:
                                articleid = sublanmu["ID"]
                                articlename = sublanmu["Name"]
                                content = sublanmu["Content"]
                                author = sublanmu["CreateUserName"]
                                source = sublanmu["TopicName"]
                                readnum = sublanmu["Access"]
                                url = sublanmu["FileName"]
                                url = "https://lincangapp.booyao.cn" + url
                                article_covers = list()
                                article_covers.append(url)

                                pubtime = sublanmu["PassedDateTime"]
                                pubtime = pubtime.replace("/Date(", "")
                                pubtime = pubtime.replace(")/", "")

                                createtime = sublanmu["CreateDateTime"]
                                createtime = createtime.replace("/Date(", "")
                                createtime = createtime.replace(")/", "")

                                updatetime = sublanmu["ModifyDateTime"]
                                updatetime = updatetime.replace("/Date(", "")
                                updatetime = updatetime.replace(")/", "")

                                article_fields = InitClass().article_fields()
                                # articleparam = InitClass().article_list_fields()

                                article_fields["url"] = "https://lincangapp.booyao.cn/API/getNewsInfo?ID=" + articleid
                                article_fields["channelID"] = subchannelid
                                article_fields["channelname"] = subchannelname
                                article_fields["channelType"] = channel_type
                                article_fields["workerid"] = articleid
                                article_fields["title"] = articlename
                                article_fields["readnum"] = readnum
                                article_fields["author"] = author
                                article_fields["pubtime"] = pubtime
                                article_fields["updatetime"] = updatetime
                                article_fields["content"] = content
                                article_fields["source"] = source
                                article_fields["createtime"] = createtime
                                article_fields["articlecovers"] = article_covers
                                article_fields["appname"] = "临沧融媒体"

                                article_fields["videocover"] = []


                                try:
                                    videos = InitClass().get_video(content)
                                    article_fields["videos"] = videos
                                except Exception as e:
                                    print("正文无视频", )

                                try:
                                    images = InitClass().get_images(content)
                                    article_fields["images"] = images
                                except Exception as e:
                                    print("正文无tupian")
                                # 将请求文章必需信息存入
                                # articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                # articleparam["articleid"] = articleid
                                # articlesparams.append(articleparam)
                                print("文章==", json.dumps(article_fields, indent=4, ensure_ascii=False))


                            #requests.post(url, headers = headers, data = data, json = appjsons)
                            #ost(url, data=None, json=None, **kwargs):

                            # cover = lanmu["FileName"]
                            # cover = "https://lincangapp.booyao.cn" + cover
                            # article_covers = list()
                            # article_covers.append(cover)

                            # article_fields = InitClass().article_fields()
                            #
                            # article_fields["channelname"] = subchannelname
                            # article_fields["channelID"] = subchannelid
                            # article_fields["channelType"] = ""
                            # article_fields["url"] = ""
                            # article_fields["workerid"] = articleid
                            # article_fields["channelID"]
                            # article_fields["channelID"]
                            #
                            # # topic_fields = InitClass().topic_fields()
                            # topic_fields["topic"] = 1
                            # topic_fields["topicID"] = articleid
                            # topic_fields["channelName"] = channelname
                            # topic_fields["channelID"] = channelid
                            # topic_fields["title"] = articlename
                            # topic_fields["topicCover"] = article_covers
                            # topic_fields["createTime"] = createtime
                            #
                            # articleparam = InitClass().article_list_fields()
                            # articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                            # articleparam["articleid"] = articleid
                            # articleparam["channelName"] = channelname
                            #
                            # articlesparams.append(articleparam)

                            # print("栏目", json.dumps(topic_fields, indent=4, ensure_ascii=False))


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
            channelname = article.get("channelName")
            article_field = article.get("articleField")

            topic = article_field.get("topic")
            if topic == 1:
                # if channelname == "栏目":
                #     url = "https://lincangapp.booyao.cn/API/getNewsListWithProgramID"
                #     headers = {
                #         "Host": "lincangapp.booyao.cn",
                #         "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                #         "User-Agent": "0.4.7 rv:1.4 (iPhone; iOS 12.0.1; zh_CN)",
                #         "Content-Length": "46",
                #         "Accept-Encoding": "gzip",
                #     }
                #     data = {
                #         "ID": articleid
                #     }
                # else:
                url = "https://lincangapp.booyao.cn/API/getNewsListWithTopicID"
                headers = {
                    "Host": "lincangapp.booyao.cn",
                    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                    "User-Agent": "0.4.7 rv:1.4 (iPhone; iOS 12.0.1; zh_CN)",
                    "Content-Length": "39",
                    "Accept-Encoding": "gzip",
                }
                data = {
                    "ID": articleid
                }

            else:
                url = "https://lincangapp.booyao.cn/API/getNewsInfo"
                headers = {
                    "Host": "lincangapp.booyao.cn",
                    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                    "User-Agent": "0.4.7 rv:1.4 (iPhone; iOS 12.0.1; zh_CN)",
                    "Content-Length": "39",
                    "Accept-Encoding": "gzip",
                }
                data = {
                    "ID": articleid
                }
                article_field["url"] = url+"?ID="+articleid

            method = 'post'
            articleparam = InitClass().article_params_fields(url, headers, method, data = data,
                                                             article_field = article_field)
            articleparams.append(articleparam)
        yield articleparams

    # 解析详情
    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            topic = fields.get("topic")
            if topic:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                #print(content_s)

                topicid = fields["topicID"]
                topictitle = fields["title"]
                channelid = fields["channelID"]
                channelname = fields["channelName"]

                articleids = list()
                newestarticleiD = ""
                newestpubtime = 0


                for article in  content_s:
                    source = article["TopicName"]
                    aritcleid = article["ID"]

                    articleids.append(aritcleid)

                    articletitle = article["Name"]
                    content = article["Content"]
                    cover = article["FileName"]
                    author = article["CreateUserName"]
                    readnum = article["Access"]
                    cover = "https://lincangapp.booyao.cn" + cover
                    article_covers = list()
                    article_covers.append(cover)

                    pubtime = article["PassedDateTime"]
                    pubtime = pubtime.replace("/Date(", "")
                    pubtime = pubtime.replace(")/", "")

                    if int(pubtime) > newestpubtime:
                        newestarticleiD = aritcleid
                        newestpubtime = int(pubtime)

                    updatetime = article["ModifyDateTime"]
                    updatetime = updatetime.replace("/Date(", "")
                    updatetime = updatetime.replace(")/", "")

                    createtime = article["CreateDateTime"]
                    createtime = createtime.replace("/Date(", "")
                    createtime = createtime.replace(")/", "")

                    article_fields = InitClass().article_fields()

                    article_fields["url"] = "https://lincangapp.booyao.cn/API/getNewsInfo?ID=" + aritcleid
                    article_fields["channelID"] = channelid
                    article_fields["channelname"] = channelname
                    article_fields["channelType"] = ""
                    article_fields["workerid"] = aritcleid
                    article_fields["title"] = articletitle
                    article_fields["readnum"] = readnum
                    article_fields["author"] = author
                    article_fields["pubtime"] = pubtime
                    article_fields["updatetime"] = updatetime
                    article_fields["content"] = content
                    article_fields["source"] = source
                    article_fields["createtime"] = createtime
                    article_fields["articlecovers"] = article_covers
                    article_fields["appname"] = self.newsname

                    article_fields["videocover"] = []

                    article_fields["specialtopic"] = 1
                    article_fields["topicid"] = topicid
                    article_fields["topicTitle"] = topictitle
                    try:
                        videos = InitClass().get_video(content)
                        article_fields["videos"] = videos
                    except Exception as e:
                        print("正文无视频")

                    try:
                        images = InitClass().get_images(content)
                        article_fields["images"] = images
                    except Exception as e:
                        print("正文无tupian")

                    print("专题文章=", json.dumps(article_fields, indent=4, ensure_ascii=False))

                fields["articleIDs"] = articleids
                fields["newestArticleID"] = newestarticleiD
                fields["newestPubtime"] = newestpubtime
                fields["platformName"] = self.newsname
                fields["pubTime"] = 0
                fields["updateTime"] = 0
                fields["articleNum"] = len(content_s)

                print("专题 fields=", json.dumps(fields, indent=4, ensure_ascii=False))

                continue


            try:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))

                for article in content_s:

                    if isinstance(article,list):
                        #不是详情内容
                        continue

                    source = article["TopicName"]
                    content = article["Content"]

                    pubtime = article["PassedDateTime"]
                    pubtime = pubtime.replace("/Date(", "")
                    pubtime = pubtime.replace(")/", "")

                    updatetime = article["ModifyDateTime"]
                    updatetime = updatetime.replace("/Date(", "")
                    updatetime = updatetime.replace(")/", "")

                    readnum = article["Access"]
                    author = article["CreateUserName"]

                    try:
                        videos = InitClass().get_video(content)
                        fields["videos"] = videos
                    except Exception as e:
                        print("正文无视频", )

                    try:
                        images = InitClass().get_images(content)
                        fields["images"] = images
                    except Exception as e:
                        print("正文无tupian")

                    fields["content"] = content
                    fields["appname"] = self.newsname

                    fields["videocover"] = []
                    fields["source"] = source
                    fields["pubtime"] = pubtime
                    fields["updatetime"] = updatetime
                    fields["readnum"] = readnum
                    fields["author"] = author

                    print("文章fields==", json.dumps(fields, indent=4, ensure_ascii=False))

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
    appspider = Lincangrongmeiti("临沧融媒体")
    appspider.run()
