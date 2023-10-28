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

from App.appspider_m import Appspider
from App.initclass import InitClass

class XinHuNan(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://ordosdaily.cn/ordos_jhxt/api.php?s=/Type/getTypeListCache"
        headers = {
            "Host": "ordosdaily.cn",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "User-Agent": "e er duo si ri bao/1.6.7 (iPhone; iOS 14.1; Scale/3.00)",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Length": "15",
            "Connection": "keep-alive",
        }
        data = {
            "siteid": "1",
            "flag": "0"
        }
        method = "post"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []

        # channelname = "政情"
        # channelid = "211"
        # channelparam = InitClass().channel_fields(channelid, channelname)
        # channelsparams.append(channelparam)

        channelslists = eval(channelsres)
        # print("channelslists==",channelslists)
        channellist = channelslists["data"]
        for channel in channellist:
            channelname = channel["cnname"]
            channelid = channel["tid"]
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "http://ordosdaily.cn/ordos_jhxt/api.php?s=//News/getNewsListCache"
        headers = {
            "Host": "ordosdaily.cn",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "Cookie": "PHPSESSID=0l83it4r6r5ft0fj9qgfa2odv3",
            "User-Agent": "e er duo si ri bao/1.6.7 (iPhone; iOS 14.1; Scale/3.00)",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Length": "23",
            "Connection": "keep-alive",
        }
        method = 'post'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            data = {
                "Page": 1,
                "PageSize": 20,
                "device": "0E6E0B84-1D6A-4A58-B720-E716939AC646",
                "flag": 0,
                "siteid": 1,
                "tid": channelid,
                "uid": ""
            }
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid = channelid, data = data,
                                                                       channeltype = channeltype)
            articlelistsparams.append(articlelist_param)

            #banner
            bannerurl = "http://ordosdaily.cn/ordos_jhxt/api.php?s=/Flash/getFlashCache"
            bannerdata = {
                "flag": 0,
                "siteid": 1,
                "tid": channelid
            }
            banner_param = InitClass().articlelists_params_fields(bannerurl, headers, method, channelname,
                                                                       channelid=channelid, data=bannerdata,
                                                                       channeltype=channeltype,banners=1)
            articlelistsparams.append(banner_param)

        yield articlelistsparams

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
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    if banner == 1:
                        try:
                            # banner
                            bannerlist = articleslists["data"]["flash"]
                            for banneritem in bannerlist:
                                # print("banneritem==",banneritem)
                                articleid = banneritem["nid"]
                                cover = banneritem["imgurl"]
                                covers = list()
                                if cover:
                                    covers.append(cover)

                                article_fields = InitClass().article_fields()
                                articleparam = InitClass().article_list_fields()

                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["workerid"] = articleid
                                article_fields["banner"] = 1
                                article_fields["articlecovers"] = covers

                                articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                articleparam["articleid"] = articleid
                                articlesparams.append(articleparam)
                        except Exception as e:
                            print("无banner")
                    else:
                        try:
                            # 列表
                            contentlist = articleslists["data"]
                            for article in contentlist:

                                # print("article==",article)
                                articleid = article["nid"]
                                covers = article["imgs"]

                                rtype = article["rtype"]
                                if rtype == "4":
                                    #专题
                                    topic_fields = InitClass().topic_fields()
                                    articleparam = InitClass().article_list_fields()

                                    topic_fields["topicID"] = articleid
                                    topic_fields["channelName"] = channelname
                                    topic_fields["channelID"] = channelid
                                    topic_fields["topicCover"] = covers

                                    topic_fields["topic"] = 1
                                    topic_fields["banner"] = 0

                                    uptime = article["sort_order"]
                                    uptimes = uptime.split(".")
                                    uptime = uptimes[0]
                                    uptime = int(uptime) * 1000
                                    topic_fields["updateTime"] = uptime
                                    topic_fields["createTime"] = 0
                                    topic_fields["pubTime"] = 0

                                    articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                    articleparam["articleid"] = articleid
                                    articlesparams.append(articleparam)

                                else:
                                    #普通
                                    article_fields = InitClass().article_fields()
                                    articleparam = InitClass().article_list_fields()

                                    article_fields["channelID"] = channelid
                                    article_fields["channelname"] = channelname
                                    article_fields["workerid"] = articleid
                                    article_fields["banner"] = 0
                                    article_fields["articlecovers"] = covers

                                    articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                    articleparam["articleid"] = articleid
                                    articlesparams.append(articleparam)

                        except Exception as e:
                            print("无列表")

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

                url = "http://ordosdaily.cn/ordos_jhxt/api.php?s=//Subject/getSubjectTypes"
                headers = {
                    "Host": "ordosdaily.cn",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "*/*",
                    "Cookie": "PHPSESSID=0l83it4r6r5ft0fj9qgfa2odv3",
                    "User-Agent": "e er duo si ri bao/1.6.7 (iPhone; iOS 14.1; Scale/3.00)",
                    "Accept-Language": "zh-Hans-CN;q=1",
                    "Accept-Encoding": "gzip, deflate",
                    "Content-Length": "14",
                    "Connection": "keep-alive",
                }
                data = {
                    "flag": 0,
                    "sid": articleid
                }

                article_field["topicUrl"] = url

            else:

                url = "http://ordosdaily.cn/ordos_jhxt/api.php?s=/News/newsinfo"
                headers = {
                    "Host": "ordosdaily.cn",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "*/*",
                    "Cookie": "PHPSESSID=0l83it4r6r5ft0fj9qgfa2odv3",
                    "User-Agent": "e er duo si ri bao/1.6.7 (iPhone; iOS 14.1; Scale/3.00)",
                    "Accept-Language": "zh-Hans-CN;q=1",
                    "Accept-Encoding": "gzip, deflate",
                    "Content-Length": "14",
                    "Connection": "keep-alive",
                }
                data = {
                    "nid":articleid,
                    "uid" :""
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
            if topic:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                # print("专题content_s=",content_s)
                try:

                    channelid = fields["channelID"]
                    channelname = fields["channelName"]
                    topicid = fields["topicID"]
                    # banner = fields["banner"]

                    topicdetail = content_s["data"]
                    topictitle = topicdetail["title"]

                    fields["title"] = topictitle

                    topiccolumns = topicdetail["columns"]

                    topicnum = 0
                    newestarticleid = ""
                    newestarticleuptime = 0

                    for section in topiccolumns:
                        cid = section["cid"]

                        surl = "http://ordosdaily.cn/ordos_jhxt/api.php?s=/Subject/getColumnNews"
                        sdata = {
                            "Page": 0,
                            "PageSize": 20,
                            "cid": cid,
                            "flag": 0
                        }
                        sheader = {
                            "Host": "ordosdaily.cn",
                            "Content-Type": "application/x-www-form-urlencoded",
                            "Accept": "*/*",
                            "Cookie": "PHPSESSID=0l83it4r6r5ft0fj9qgfa2odv3",
                            "User-Agent": "e er duo si ri bao/1.6.7 (iPhone; iOS 14.1; Scale/3.00)",
                            "Accept-Language": "zh-Hans-CN;q=1",
                            "Accept-Encoding": "gzip, deflate",
                            "Content-Length": "14",
                            "Connection": "keep-alive",
                        }

                        sres = requests.post(surl, headers=sheader, data=sdata).text
                        sectionlist = json.loads(json.dumps(json.loads(sres, strict=False), indent=4, ensure_ascii=False))
                        # print("sectionlist==",sectionlist)
                        for item in sectionlist["data"]:

                            topicnum += 1

                            articleid = item["nid"]
                            articletitle = item["title"]
                            source = item["copyfrom"]

                            uptime = item["sort_order"]
                            uptimes = uptime.split(".")
                            uptime = uptimes[0]
                            uptime = int(uptime) * 1000

                            if uptime > newestarticleuptime:
                                newestarticleuptime = uptime
                                newestarticleid = articleid

                            comnum = item["comcount"]
                            covers = item["imgs"]
                            articleurl = item["newsurl"]

                            article_fields = InitClass().article_fields()

                            article_fields["appname"] = self.newsname
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["url"] = articleurl
                            article_fields["workerid"] = articleid
                            article_fields["title"] = articletitle
                            article_fields["banner"] = 0
                            article_fields["articlecovers"] = covers

                            article_fields["updatetime"] = uptime
                            article_fields["pubtime"] = 0
                            article_fields["createtime"] = 0

                            article_fields["source"] = source


                            # article_fields["likenum"] =
                            article_fields["commentnum"] = comnum
                            # article_fields["readnum"] =
                            # article_fields["sharenum"] =
                            article_fields["specialtopic"] = 1
                            article_fields["topicid"] = topicid
                            article_fields["topicTitle"] = topictitle

                            try:
                                # 请求newsurl 获取正文
                                res = requests.get(articleurl)
                                res.encoding = 'utf8'
                                bf = bs4.BeautifulSoup(res.text, 'html.parser')
                                content = bf.find('div', id='aritcleContent').decode()
                                article_fields["content"] = content

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

                            article_fields["videocover"] = []
                            print("专题内部文章==", json.dumps(article_fields, indent=4, ensure_ascii=False))

                    fields["articleNum"] = topicnum
                    fields["newestArticleID"] = newestarticleid
                    fields["platformName"] = self.newsname

                    print("大专题==", json.dumps(fields, indent=4, ensure_ascii=False))

                except Exception as e:
                    num += 1
                    logging.info(f"错误数量{num},{e}")

            else:
                #普通
                try:
                    content_s = json.loads(json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))

                    # print("普通content_s=",content_s)

                    detail = content_s["data"]

                    articletitle = detail["title"]
                    source = detail["copyfrom"]

                    uptime = detail["sort_order"]
                    uptimes = uptime.split(".")
                    uptime = uptimes[0]
                    uptime = int(uptime) * 1000

                    url = detail["newsurl"]
                    comnum = detail["comcount"]
                    readnum = detail["viewnum"]
                    likenum = detail["praisenum"]

                    # images = detail["imgs"]
                    #
                    # url = content_s["url"]
                    # content = content_s["content"]
                    # content = urllib.parse.unquote(content)

                    fields["title"] = articletitle
                    fields["source"] = source
                    fields["commentnum"] = comnum
                    fields["readnum"] = readnum
                    fields["likenum"] = likenum


                    fields["url"] = url
                    fields["appname"] = self.newsname
                    # fields["images"] = images
                    # fields["content"] = content

                    fields["pubtime"] = 0
                    fields["createtime"] = 0
                    fields["updatetime"] = uptime

                    try:
                        # 请求newsurl 获取正文
                        res = requests.get(url)
                        res.encoding = 'utf8'
                        bf = bs4.BeautifulSoup(res.text, 'html.parser')
                        content = bf.find('div', id='aritcleContent').decode()
                        fields["content"] = content

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

                    except Exception as e:
                        print("无html格式正文")

                    fields["videocover"] = []

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
    appspider = XinHuNan("鄂尔多斯日报")
    appspider.run()
