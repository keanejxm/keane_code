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
import time

from App.appspider_m import Appspider
from App.initclass import InitClass


class XinHuNan(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://yun.99cms.com/bt/jhxt/api.php?s=/Type/getTypeListCache"
        headers = {
            "Content-Type":"application/x-www-form-urlencoded",
            "Host": "yun.99cms.com",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.1",
            "Connection": "keep-alive"
        }
        data = {
            "siteid": "1",
            "flag": "1"
        }
        method = "post"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []

        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        # print("channelslists==",channelslists)
        dataobj = channelslists["data"]
        channellist = dataobj["common"]
        for channel in channellist:
            channelname = channel["cnname"]
            channelid = channel["tid"]
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)

        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "http://yun.99cms.com/bt/jhxt/api.php?s=/News/getNewsListCache"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "yun.99cms.com",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.1",
            "Connection": "keep-alive"
        }
        method = 'post'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            data = {
                "device": "ffffffff-c491-1740-648a-260300000000",
                "siteid": 1,
                "Page": 1,
                "PageSize": 15,
                "tid": channelid
            }

            if channelname == "党媒":
                url = "https://rev.uar.hubpd.com/recom"
                headers = {
                    "method": "GET",
                    "authority": "rev.uar.hubpd.com",
                    "scheme": "https",
                    "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
                    "accept": "*/*",
                    "referer": "https://rev.uar.hubpd.com/static/tpl/recom/default/recom.html?",
                    "accept-encoding": "gzip, deflate",
                    "accept-language": "zh-CN,en-US;q=0.8",
                    "cookie": "_ma_tk=qlcqw3qu9y8p7tiqpyy7dguj9fa4laqn",
                    "cookie": "_ma_starttm=1609755729727",
                    "cookie": "_ma_is_new_u=0",
                    "cookie": "_sdk_uuid=09B97C65BD93040E9D8A5EF03959DC6E",
                    "x-requested-with": "com.hzpd.bingtuan"
                }
                now = int(time.time())*1000
                data = {
                    "t": now,
                    "appkey": "UAR-000339_883",
                    "adspot": "zhangshangbingtuan",
                    "uuid": "09B97C65BD93040E9D8A5EF03959DC6E",
                    "source": "2",
                    "format": "complex",
                    "show_model": "1",
                    "max_behot_time": "-1",
                    "from": "m",
                    "province": "",
                    "city": "",

                }
                method = "get"


            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid = channelid, data = data,
                                                                       channeltype = channeltype)
            articlelistsparams.append(articlelist_param)
            if channelname != "党媒":
                bannerurl = "http://yun.99cms.com/bt/jhxt/api.php?s=/Flash/getFlashCache"
                bannerdata = {
                    "siteid": 1,
                    "type": 0,
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
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent = 4, ensure_ascii = False))
                # print("articleslists=", articleslists)
                try:
                    if channelname == "党媒":
                        contentlist = articleslists["result_list"]
                        for article in contentlist:

                            articleid = article["itemId"]


                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["workerid"] = articleid
                            article_fields["banner"] = 0
                            article_fields["appname"] = "兵团日报"

                            articleparam["articleField"] = article_fields  # 携带文章采集的数据
                            articleparam["articleid"] = articleid
                            articlesparams.append(articleparam)

                    else:
                        if banner == 1:
                            try:
                                # banner
                                bannerlist = articleslists["data"]["flash"]
                                for banneritem in bannerlist:
                                    articleid = banneritem["nid"]

                                    article_fields = InitClass().article_fields()
                                    articleparam = InitClass().article_list_fields()

                                    article_fields["channelID"] = channelid
                                    article_fields["channelname"] = channelname
                                    article_fields["workerid"] = articleid
                                    article_fields["banner"] = 1

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
                                    articleid = article["nid"]

                                    article_fields = InitClass().article_fields()
                                    articleparam = InitClass().article_list_fields()

                                    article_fields["channelID"] = channelid
                                    article_fields["channelname"] = channelname
                                    article_fields["workerid"] = articleid
                                    article_fields["banner"] = 0

                                    articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                    articleparam["articleid"] = articleid
                                    articlesparams.append(articleparam)
                            except Exception as e:
                                print("无列表")

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
            # topic = article_field.get("topic")
            channelname = article_field.get("channelname")

            if channelname == "党媒":
                url = "https://rev.uar.hubpd.com/recom/midmodpage"
                headers = {
                    "method": "GET",
                    "authority": "rev.uar.hubpd.com",
                    "scheme": "https",
                    "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
                    "accept": "*/*",
                    "referer": "https://rev.uar.hubpd.com/static/tpl/recom/default/recom.html?",
                    "accept-encoding": "gzip, deflate",
                    "accept-language": "zh-CN,en-US;q=0.8",
                    "cookie": "_ma_tk=qlcqw3qu9y8p7tiqpyy7dguj9fa4laqn",
                    "cookie": "_ma_starttm=1609755729727",
                    "cookie": "_ma_is_new_u=0",
                    "cookie": "_sdk_uuid=09B97C65BD93040E9D8A5EF03959DC6E",
                    "x-requested-with": "com.hzpd.bingtuan"
                }
                data = {
                    "itemid": articleid,
                    "appkey": "UAR-000339_883",
                    "callback": "load_callback"
                }
                method = 'get'
            else:

                url = "http://yun.99cms.com/bt/jhxt/api.php?s=/News/newsinfo"
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Host": "yun.99cms.com",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.8.1",
                    "Connection": "keep-alive"
                }
                data = {
                    "nid": articleid
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
            # topic = fields.get("topic")
            # if topic:
            #     content_s = json.loads(
            #         json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
            #     print("专题content_s=",content_s)
            try:
                channelname = fields.get("channelname")
                ajson = article.get("articleres")

                if channelname == "党媒":

                    ajson = ajson.lstrip("load_callback(")
                    contentstr= ajson[:-1]
                    contentstr = contentstr.replace("false", "False")
                    contentstr = contentstr.replace("true", "True")
                    contentdetail = eval(contentstr)

                    content = contentdetail["body"]
                    pubtime = contentdetail["publishTime"]
                    url = contentdetail["url"]
                    author = contentdetail["editor"]
                    title = contentdetail["title"]
                    source = contentdetail["source"]
                    # articleid = contentdetail["item_id"]
                    cover = contentdetail["pic"]
                    covers = list()
                    if cover:
                        covers.append(cover)

                    fields["title"] = title
                    fields["articlecovers"] = covers
                    fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                    fields["url"] = url
                    fields["source"] = source
                    fields["author"] = author
                    fields["content"] = content
                    fields["createtime"] = 0
                    fields["updatetime"] = 0

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

                    print("fields==", json.dumps(fields, indent=4, ensure_ascii=False))

                else:
                    content_s = json.loads(json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                    # print("普通content_s=",content_s)
                    contentdetail = content_s["data"]

                    ariticletitle = contentdetail["title"]
                    source = contentdetail["copyfrom"]
                    uptime = contentdetail["sort_order"]
                    uptimes = uptime.split(".")
                    uptime = uptimes[0]
                    uptime = int(uptime) * 1000

                    content = contentdetail["content"]
                    covers = contentdetail["imgs"]
                    newsurl = contentdetail["newsurl"]
                    comnum = contentdetail["comcount"]
                    likenum = contentdetail["praisecount"]
                    readnum = contentdetail["viewcount"]

                    videourl = contentdetail["videourl"]

                    fields["title"] = ariticletitle
                    fields["articlecovers"] = covers
                    fields["updatetime"] = uptime
                    fields["url"] = newsurl

                    try:
                        # 请求newsurl 获取正文
                        res = requests.get(newsurl)
                        res.encoding = 'utf8'
                        bf = bs4.BeautifulSoup(res.text, 'html.parser')
                        content = bf.find('div',class_='cont_bottom').decode()
                    except Exception as e:
                        print("无html格式正文")

                    fields["appname"] = self.newsname
                    fields["content"] = content
                    fields["source"] = source
                    fields["commentnum"] = comnum
                    fields["likenum"] = likenum
                    fields["readnum"] = readnum
                    #
                    fields["pubtime"] = 0
                    fields["createtime"] = 0
                    fields["videocover"] = []
                    try:
                        videos = InitClass().get_video(content)
                        if videourl:
                            videos.append(videourl)

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
    appspider = XinHuNan("兵团日报")
    appspider.run()
