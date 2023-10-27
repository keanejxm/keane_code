# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class XinHua15Miao(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "http://appa.cncnews.cn/cnc/column_list_new2"
        # 频道请求头
        headers = {
            'Authorization': 'your token',
            'Content-Type': 'application/json',
            'Content-Length': '105',
            'Host': 'appa.cncnews.cn',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Apache-HttpClient/UNAVAILABLE (java 1.4)'
        }
        # 频道数据体
        head = {
            "imei": "863064186012417", "oc": "123123", "plat": "android", "sid": "", "st": "", "uid": "", "ver": "v4.1"
        }
        # 如果携带的是json数据体,用appjson发送
        # app_json = {
        #
        # }
        # 频道请求方式
        method = "post"
        app_params = InitClass().app_params(url, headers, method, data=head)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        """
        此方法主要获取channelid,channelname即可
        若请求文章列表页需要channeltype，categoryname，categoryid,则以categoryname= categoryname形式传递参数
        :param channelsres:
        :return:
        """
        # 将返回的数据转为json数据
        channelslists = json.loads(channelsres)
        for channel in channelslists['body']['channels']:
            channelid = channel['channel_id']
            channelname = channel['channel_name']
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam

    def getarticlelistparams(self, channelsres):
        """
        此方法目的是组建请求文章列页面数据参数，url，headers，data，若以json形式发送数据，则channeljson = channeljson
        :param channelsres:
        :return:
        """
        channel_num = 0
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            if channelid == '99':
                # 推荐banner、专题
                url = "http://appa.cncnews.cn/cnc/recommend/subject_new"
                headers = {
                    "Authorization": "your token",
                    "Content-Type": "application/json",
                    "Content-Length": "143",
                    "Host": "appa.cncnews.cn",
                    "Connection": "Keep-Alive",
                    "User-Agent": "Apache-HttpClient/UNAVAILABLE (java 1.4)"
                }
                method = "post"
                data = {}
                # 推荐正文内容
                url_articlelist = "http://appa.cncnews.cn/cnc/recommend_list"
                channel_json = {"body": {"pageno": "1", "pagesize": "10"},
                                "head": {"imei": "863064186012417", "oc": "123123", "plat": "android", "sid": "",
                                         "st": "", "uid": "", "ver": "v4.1"}}
                self_typeid = self.self_typeid
                platform_id = self.platform_id
                platform_name = self.newsname
                channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                                   self_typeid, channelname,
                                                                                   channel_num)

                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           data=data, channel_index_id=channel_index_id,
                                                                           channeljson=channel_json)
                articlelist_param_articlelists = InitClass().articlelists_params_fields(
                    url_articlelist, headers,
                    method, channelname,
                    data=data,
                    channel_index_id=channel_index_id,
                    channeljson=channel_json)
                yield channel_field, [articlelist_param, articlelist_param_articlelists]

            else:
                url = "http://appa.cncnews.cn/cnc/column_news_list"
                headers = {
                    'Authorization': 'your token',
                    'Content-Type': 'application/json',
                    'Content-Length': '165',
                    'Host': 'appa.cncnews.cn',
                    'Connection': 'Keep-Alive',
                    'User-Agent': 'Apache-HttpClient/UNAVAILABLE(java 1.4)'
                }
                data = {}
                method = 'post'
                channel_json = {
                    'body': {"column_id": channelid, "name": "", "pageno": 1, "pagesize": 20},
                    "head": {"imei": "863064186012417", "oc": "123123", "plat": "android", "sid": "", "st": "",
                             "uid": "", "ver": "v4.1"}
                }
                self_typeid = self.self_typeid
                platform_id = self.platform_id
                platform_name = self.newsname
                channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                                   self_typeid, channelname,
                                                                                   channel_num)
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           data=data, channeljson=channel_json,
                                                                           channel_index_id=channel_index_id)
                # articleparams.append(articlelist_param)

                yield channel_field, [articlelist_param]

    def analyze_articlelists(self, articleslist_ress):
        """
        解析文章列表页，目的是为了获取文章具体信息，组建请求文章详情数据体
        :param articleslist_ress:
        :return:
        """
        # articlesparams = []
        for articleslist_res in articleslist_ress:
            channelname = articleslist_res.get("channelname")
            channel_index_id = articleslist_res.get("channelindexid")
            articlelist_res = articleslist_res.get("channelres")
            try:
                articlelist_json = json.loads(articlelist_res)
                # 可在下面打印处打断点，查看请求到的数据
                # 若banner图在articlelist_json中则分来开取并给其复制banner = 1
                try:
                    articlelists = articlelist_json['body']
                    if "subitems" in articlelists:
                        banners = 1
                        for article in articlelists["subitems"]:
                            articleparam = InitClass().article_list_fields()
                            articleid = article["id"]
                            articletitle = article["title"]
                            articlecover = article["imagePath"]
                            pubtime = article["pubDate"]
                            favnum = article["favSum"]
                            sharenum = article["shareSum"]
                            commentnum = article["commentSum"]
                            articleparam["articleid"] = articleid
                            articleparam["articletitle"] = articletitle
                            articleparam["channelname"] = channelname
                            articleparam["channelindexid"] = channel_index_id
                            articleparam["imageurl"] = articlecover
                            articleparam["pubtime"] = pubtime
                            articleparam["favnum"] = favnum
                            articleparam["sharenum"] = sharenum
                            articleparam["commentnum"] = commentnum
                            articleparam["banner"] = banners
                            yield articleparam
                            # articlesparams.append(articleparam)
                        if "subitems2" in articlelists:
                            for article in articlelists["subitems2"]:
                                # 此处为专题需要多请求一次接口，专题设置special_topic
                                special_topic = 1
                                articleparam = InitClass().article_list_fields()
                                articleid = article["id"]
                                articletitle = article["title"]
                                articleparam["articleid"] = articleid
                                articleparam["articletitle"] = articletitle
                                articleparam["channelname"] = channelname
                                articleparam["channelindexid"] = channel_index_id
                                articlecover = article["imagePath"]
                                pubtime = article["pubDate"]
                                favnum = article["favSum"]
                                sharenum = article["shareSum"]
                                commentnum = article["commentSum"]
                                articleparam["imageurl"] = articlecover
                                articleparam["pubtime"] = pubtime
                                articleparam["favnum"] = favnum
                                articleparam["sharenum"] = sharenum
                                articleparam["commentnum"] = commentnum
                                articleparam["specialtopic"] = special_topic
                                yield articleparam
                                # articlesparams.append(articleparam)
                    else:
                        for article in articlelists['news_set']:
                            # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                            articleparam = InitClass().article_list_fields()
                            articletitle = article['title']
                            articleid = article['id']
                            pubtime = article["date"]
                            favnum = article["fav"]
                            sharenum = article["share"]
                            commentnum = article["comment_num"]
                            try:
                                if article['image_set']['image_url']:
                                    images = list()
                                    images.append(article['image_set']['image_url'])
                                    articleparam["imageurl"] = images
                            except Exception as e:
                                logging.info(f"在文章列表出无法获得封面图{e}")
                            articleparam["articleid"] = articleid
                            articleparam["articletitle"] = articletitle
                            articleparam["channelname"] = channelname
                            articleparam["channelindexid"] = channel_index_id
                            articleparam["pubtime"] = pubtime
                            articleparam["favnum"] = favnum
                            articleparam["sharenum"] = sharenum
                            articleparam["commentnum"] = commentnum
                            yield articleparam
                            # articlesparams.append(articleparam)
                except Exception as e:
                    print(f"{self.newsname}解析文章列表数据失败{e}")
            except Exception as e:
                print(f"{self.newsname}json文章列表数据失败{e}")
        # yield articlesparams

    def getarticleparams(self, articleslist_ress):
        """
        组建请求文章详情所需要的数据体
        :param articleslist_ress:
        :return:
        """
        # articlesparam = []

        headers = {
            "Authorization": "your token",
            "Content-Type": "application/json",
            "Content-Length": "132",
            "Host": "appa.cncnews.cn",
            "Connection": "Keep-Alive",
            "User-Agent": "Apache-HttpClient/UNAVAILABLE (java 1.4)",
        }
        url = 'http://appa.cncnews.cn/cnc/recommend_video_detail'
        data = {}
        method = 'post'
        for articleparam in self.analyze_articlelists(articleslist_ress):
            channelname = articleparam.get("channelname")
            channel_index_id = articleparam.get("channelindexid")
            article_json = {"body": {"new_id": articleparam.get("articleid")},
                            "head": {"imei": "863064186012417", "oc": "123123", "plat": "android", "sid": "", "st": "",
                                     "uid": "", "ver": "v4.1"}}
            # 此处代码不需要改动
            imgurl = articleparam.get("imageurl")
            videos = articleparam.get("videos")
            videocover = articleparam.get("videocover")
            pubtime = articleparam.get("pubtime")
            createtime = articleparam.get("createtime")
            updatetime = articleparam.get("updatetime")
            source = articleparam.get("source")
            author = articleparam.get("author")
            likenum = articleparam.get("likenum")
            commentnum = articleparam.get("commentnum")
            sharenum = articleparam.get("sharenum")
            readnum = articleparam.get("readnum")
            articleurl = articleparam.get("articleurl")
            # 若APP有关于时间的反爬加sleeptime = 1，若发送为json数据体，则添加articlejson = articlejson
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                        videourl=videos, videocover=videocover, pubtime=pubtime,
                                                        createtime=createtime, updatetime=updatetime,
                                                        source=source, author=author, likenum=likenum,
                                                        commentnum=commentnum, sharenum=sharenum, readnum=readnum,
                                                        articleurl=articleurl, articlejson=article_json,
                                                        channel_index_id=channel_index_id)

            # articlesparam.append(article)
            yield [article]

    def analyzearticle(self, articles_res):
        for articleres in articles_res:
            channelname = articleres.get("channelname")
            channel_index_id = articleres.get("channelindexid")
            appname = articleres.get("appname")
            imgurl = articleres.get("imageurl")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["channelindexid"] = channel_index_id
            fields["platformID"] = self.platform_id
            fields["articlecovers"] = imgurl
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                title = articlejson['body']['news_info']['title']  # 标题
                pubtime = articlejson['body']['news_info']['date']  # 发布时间
                workerid = articlejson['body']['news_info']['id']
                url = articlejson['body']['news_info']['url']
                videos = articlejson['body']['news_info']['image_set']['video_url']
                videocover = articlejson['body']['news_info']['image_set']['image_url']
                commentnum = articlejson['body']['news_info']['comment_num']
                sharenum = articlejson["body"]["news_info"]["share"]
                fields["commentnum"] = commentnum
                fields["sharenum"] = sharenum
                fields["videos"] = videos
                fields["appname"] = appname
                fields["title"] = title
                fields["url"] = url
                fields["workerid"] = workerid
                fields["videocover"] = videocover
                fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)


def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = XinHua15Miao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
