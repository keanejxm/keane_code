# -*- encoding:utf-8 -*-
"""
@功能:新湖南解析模板
@AUTHOR：Keane
@文件名：xinhunan.py
@时间：2020/12/17  17:33
"""

import json
import logging
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class Lijiangwang(Appspider):

    # 请求频道
    @staticmethod
    def get_app_params():
        url = "http://api.lijiang.cn/app.php/index/index"
        headers = {
            "user-agent": "MuMu(Android/6.0.1) (com.lijiang.cn/2.0.2) Weex/0.26.0 810x1440",
            "Host": "api.lijiang.cn",
            "Accept-Encoding": "gzip",
            "Connection": "keep-alive",
        }
        data = {}
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    # 解析频道列表
    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))

        ztid = "zhuantiliebiao"
        ztname = "专题"
        channelparam_zhuanti = InitClass().channel_fields(ztid, ztname)

        bannerid = "banner"
        bannername = "banner"
        # print("channelname==", bannername, "bannerid==", bannerid)
        channelparam_banner = InitClass().channel_fields(bannerid, bannername)
        # 自定义接口，再次请求频道列表，目的是获取banenr，置顶等数据
        pindaoid = "pindao"
        pindaoname = "pindao"
        # print("pindaoid==", pindaoid, "pindaoname==", pindaoname)
        channelparam_pindao = InitClass().channel_fields(pindaoid, pindaoname)
        class_list = channelslists["class"]
        for item in class_list:
            charclass = item["charclass"]
            for channel in charclass:
                channelid = str(channel["classid"])
                channelname = channel["classname"]
                # print("channelname==",channelname,"channelid==",channelid)
                channelparam = InitClass().channel_fields(channelid, channelname)
                yield channelparam
            for channelparam in [channelparam_zhuanti, channelparam_banner, channelparam_pindao]:
                yield channelparam

    # 请求各频道列表数据
    def getarticlelistparams(self, channelsres):
        headers = {
            "Host": "api.lijiang.cn",
            "Accept": "*/*",
            "User-Agent": "iPhone10,3(iOS/14.1) Uninview(Uninview/1.0.0) Weex/0.26.0 1125x2436",
            "Accept-Language": "zh-cn",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive"
        }
        method = 'get'
        channel_num = 0
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = ""
            data = {}
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            if channelid == "zhuantiliebiao":
                # 请求专题列表
                url = "http://api.lijiang.cn/app.php/Listing/articlelink/page/1"
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           channelid=channelid, data=data,
                                                                           channeltype=channeltype,
                                                                           channel_index_id=channel_index_id)
                yield channel_field, [articlelist_param]
            elif channelid == "banner":
                # 旅游banner
                url_ly = "http://api.lijiang.cn/app.php/Listing/getHdp/varname/app_ljly"
                # 本地banner
                url_sh = "http://api.lijiang.cn/app.php/Listing/getHdp/varname/app_ljsh"
                articlelist_param_ly = InitClass().articlelists_params_fields(url_ly, headers, method, "丽江旅游",
                                                                              channelid=channelid, data=data,
                                                                              channeltype=channeltype, banners=1)

                articlelist_param_sh = InitClass().articlelists_params_fields(url_sh, headers, method, "本地生活",
                                                                              channelid=channelid, data=data,
                                                                              channeltype=channeltype, banners=1)
                yield channel_field, [articlelist_param_ly, articlelist_param_sh]
            elif channelid == "pindao":
                # 再次请求频道，获取banner等信息
                url = "http://api.lijiang.cn/app.php/index/index"
                headers = {
                    "user-agent": "MuMu(Android/6.0.1) (com.lijiang.cn/2.0.2) Weex/0.26.0 810x1440",
                    "Host": "api.lijiang.cn",
                    "Accept-Encoding": "gzip",
                    "Connection": "keep-alive",
                }
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           channelid=channelid, data=data,
                                                                           channeltype=channeltype,
                                                                           channel_index_id=channel_index_id)
                yield channel_field,[articlelist_param]

            else:
                # 非专题列表
                url = "http://api.lijiang.cn/app.php/Listing/index/classid/" + channelid + "/page/1"
                # print("url===",url)
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           channelid=channelid, data=data,
                                                                           channeltype=channeltype,
                                                                           channel_index_id=channel_index_id)
                yield channel_field,[articlelist_param]

    # 解析各频道列表数据
    @staticmethod
    def analyze_articlelists(articleslistsres):
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channel_index_id = articleslistres.get("channelindexid")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            channel_type = articleslistres.get("channeltype")
            banners = articleslistres.get("banner")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    code = articleslists["code"]
                    if code != 200:
                        # 接口数据异常
                        continue
                    if channelid == "banner":
                        banner_list = articleslists["hdp"]
                        for banneritem in banner_list:
                            # 普通新闻
                            articleparam = InitClass().article_list_fields()
                            article_fields = InitClass().article_fields()
                            article_id = str(banneritem["id"])
                            classid = str(banneritem["classid"])
                            article_title = banneritem["title"]
                            article_cover = banneritem["titlepic"]
                            try:
                                source = banneritem["befrom"]
                                article_fields["source"] = source
                            except Exception as e:
                                print("eee=== befrom")
                            readnum = banneritem["onclick"]
                            pubtime = banneritem["newstime"] * 1000
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channelindexid"] = channel_index_id
                            article_fields["channelType"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["pubtime"] = pubtime
                            article_fields["banner"] = banners
                            article_fields["readnum"] = readnum
                            article_fields["tmpclassid"] = classid
                            article_covers = list()
                            if article_cover:
                                article_covers.append(article_cover)
                            article_fields["articlecovers"] = article_covers
                            yield article_fields
                    elif channelid == "pindao":
                        # banner
                        # print("articleslists==",articleslists)
                        banner_list = articleslists["mes"]["banner"]
                        for banneritem in banner_list:
                            adtype = banneritem["adtype"]
                            # 只发现有1 的为专题
                            if adtype == 1:
                                # 专题
                                articleid = banneritem["alt"]
                                if articleid != "":
                                    picurl = banneritem["picurl"]
                                    onclick = banneritem["onclick"]
                                    title = banneritem["title"]
                                    channelname = "首页"
                                    articleparam = InitClass().article_list_fields()
                                    topic_fields = InitClass().topic_fields()
                                    article_covers = list()
                                    if picurl:
                                        article_covers.append(picurl)
                                    topic_fields["topic"] = 1
                                    topic_fields["topicID"] = articleid
                                    topic_fields["channelName"] = channelname
                                    topic_fields["channelindexid"] = channel_index_id
                                    topic_fields["channelID"] = ""
                                    topic_fields["title"] = title
                                    topic_fields["topicCover"] = article_covers
                                    topic_fields["banner"] = 1
                                    articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                    articleparam["articleid"] = articleid
                                    yield topic_fields
                        # 置顶
                        frist_title = articleslists["mes"]["frist_title"]
                        # 滚动
                        left_banner = articleslists["mes"]["left_banner"]
                        # 热点新闻
                        banner_list = articleslists["mes"]["col_6"]
                        shouye_list = frist_title + left_banner + banner_list
                        for item in shouye_list:
                            # 普通新闻
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()

                            article_id = str(item["id"])
                            classid = str(item["classid"])
                            article_title = item["title"]
                            article_cover = item["titlepic"]
                            try:
                                source = item["befrom"]
                                article_fields["source"] = source
                            except Exception as e:
                                print("eee=== befrom")
                            readnum = item["onclick"]
                            pubtime = item["newstime"] * 1000
                            # article["titleurl"]
                            article_fields["channelID"] = ""
                            article_fields["channelname"] = channelname
                            article_fields["channelindexid"] = channel_index_id
                            article_fields["channelType"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            # article_fields["contentType"] = article_type
                            # article_fields["url"] = share_url
                            article_fields["pubtime"] = pubtime
                            article_fields["banner"] = banners
                            article_fields["readnum"] = readnum
                            article_fields["tmpclassid"] = classid
                            article_covers = list()
                            if article_cover:
                                article_covers.append(article_cover)
                            article_fields["articlecovers"] = article_covers
                            yield article_fields
                    articles = articleslists["message"]
                    for article in articles:
                        articleparam = InitClass().article_list_fields()
                        if channelid == "zhuantiliebiao":
                            # 专题
                            topic_fields = InitClass().topic_fields()
                            article_id = str(article["ztid"])
                            article_title = str(article["ztname"])
                            readnum = article["onclick"]
                            article_cover = article["ztimg"]
                            topicnum = article["ztnum"]
                            # listtempid
                            infotext = article["intro"]
                            createtime = article["addtime"] * 1000

                            article_covers = list()
                            if article_cover:
                                article_covers.append(article_cover)

                            topic_fields["topic"] = 1
                            topic_fields["topicID"] = article_id
                            topic_fields["channelName"] = channelname
                            topic_fields["channelindexid"] = channel_index_id
                            topic_fields["channelID"] = ""
                            # ["topicUrl"]
                            topic_fields["title"] = article_title
                            topic_fields["digest"] = infotext
                            topic_fields["topicCover"] = article_covers
                            # ["pubTime"]
                            topic_fields["articleNum"] = topicnum
                            # ["newestArticleID"]
                            # ["newestPubtime"]
                            # ["articleIDs"]
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
                            topic_fields["createTime"] = createtime
                            # ["updateTime"]
                            topic_fields["readnum"] = readnum
                            articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                            articleparam["articleid"] = article_id
                            yield articleparam
                        else:
                            # 普通新闻
                            article_fields = InitClass().article_fields()

                            article_id = str(article["id"])
                            classid = str(article["classid"])
                            article_title = article["title"]
                            article_cover = article["titlepic"]
                            try:
                                source = article["befrom"]
                                article_fields["source"] = source
                            except Exception as e:
                                print("eee=== befrom")
                            readnum = article["onclick"]
                            pubtime = article["newstime"] * 1000
                            # article["titleurl"]
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channelindexid"] = channel_index_id
                            article_fields["channelType"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            # article_fields["contentType"] = article_type
                            # article_fields["url"] = share_url
                            article_fields["pubtime"] = pubtime
                            article_fields["banner"] = banners
                            article_fields["readnum"] = readnum
                            article_fields["tmpclassid"] = classid
                            article_covers = list()
                            if article_cover:
                                article_covers.append(article_cover)
                            article_fields["articlecovers"] = article_covers
                            yield article_fields
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")

    # 请求新闻详情
    def getarticleparams(self,articleslistsres):
        for article in self.analyze_articlelists(articleslistsres):
            articleid = article.get("workerid")
            topic = article.get("topic")
            headers = {
                "Host": "api.lijiang.cn",
                "Accept": "*/*",
                "User-Agent": "iPhone10,3(iOS/14.1) Uninview(Uninview/1.0.0) Weex/0.26.0 1125x2436",
                "Accept-Language": "zh-cn",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive"
            }
            method = 'get'
            data = {}
            if topic == 1:
                articleid = article.get("topicID")
                url = "http://api.lijiang.cn/app.php/articlelink/index/ztid/" + articleid + "/page/1"
                articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                                 article_field=article)
                article["topicUrl"] = url
                yield [articleparam]

            else:
                classid = article.get("tmpclassid")
                url = "http://api.lijiang.cn/app.php/Article/indexapp/classid/" + classid + "/id/" + articleid

                article["url"] = url
                articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                                 article_field=article)
                yield [articleparam]

    # 解析文章详情统一方法
    @staticmethod
    def formatearticledetail(detail, fields):
        # print("detail ==",detail)
        worker_id = detail["id"]
        article_title = detail["title"]
        author = detail["username"]

        try:
            source = detail["befrom"]
            fields["source"] = source
        except Exception as e:
            print("eee===", detail)

        try:
            content = detail["text"]
            fields["content"] = content
            videos = InitClass().get_video(content)
            fields["videos"] = videos
        except Exception as e:
            print("text eee==", detail)

        try:
            content = detail["text"]
            images = InitClass().get_images(content)
            fields["images"] = images
        except Exception as e:
            print("text eee==", detail)

        try:
            videosrc = detail["video_src"]
            if videosrc:
                fields["videos"] = [videosrc]
        except Exception as e:
            print("")

        # content = InitClass().decode_base64(content)
        updatetime = detail["lastdotime"] * 1000
        pubtime = detail["newstime"] * 1000
        readnum = detail["onclick"]
        plnum = detail["plnum"]

        article_cover = detail["titlepic"]
        if article_cover:
            article_covers = list()
            article_covers.append(article_cover)
            fields["articlecovers"] = article_covers

        fields["videocover"] = []
        fields["width"] = 0
        fields["height"] = 0
        fields["createtime"] = 0
        fields["channelType"] = ""

        try:
            comment_num = detail["comment_num"]
            fields["commentnum"] = comment_num
        except Exception as e:
            print("commentnum")

        # fields["appname"] = self.newsname
        fields["title"] = article_title
        fields["workerid"] = worker_id
        fields["readnum"] = readnum
        fields["author"] = author
        fields["updatetime"] = updatetime
        fields["pubtime"] = pubtime
        fields["playnum"] = plnum
        return fields

    # 解析新闻详情
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
                    code = content_s["code"]
                    if code != 200:
                        # 数据异常
                        continue
                    zhuanti = content_s["zt"]

                    zhuanti_id = zhuanti["ztid"]

                    article_covers = list()
                    article_covers.append(zhuanti["ztimg"])

                    ##fields["topic"]
                    fields["topicID"] = zhuanti_id
                    fields["platformName"] = self.newsname
                    fields["platformID"] = ""
                    ##fields["channelName"]
                    ##fields["channelID"]
                    ##fields["topicUrl"]
                    zhuanti_title = zhuanti["ztname"]
                    fields["title"] = zhuanti_title
                    fields["digest"] = zhuanti["intro"]
                    fields["topicCover"] = article_covers
                    fields["pubTime"] = 0
                    fields["articleNum"] = zhuanti["ztnum"]
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
                    fields["createTime"] = zhuanti["addtime"] * 1000
                    # ["updateTime"]
                    fields["readnum"] = zhuanti["onclick"]

                    banner = 0
                    try:
                        banner = fields["banner"]
                    except Exception as e:
                        print("banner")

                    articleids = list()
                    newestarticleiD = ""
                    newestpubtime = 0

                    zhuanti_list = content_s["mes"]
                    fields, topic_id = InitClass().wash_topic_data(fields)
                    for zhuanti_item in zhuanti_list:
                        articleid = str(zhuanti_item["id"])
                        classid = str(zhuanti_item["classid"])

                        articleids.append(articleid)

                        url = "http://api.lijiang.cn/app.php/Article/indexapp/classid/" + classid + "/id/" + articleid
                        headers = {
                            "Host": "api.lijiang.cn",
                            "Accept": "*/*",
                            "User-Agent": "iPhone10,3(iOS/14.1) Uninview(Uninview/1.0.0) Weex/0.26.0 1125x2436",
                            "Accept-Language": "zh-cn",
                            "Accept-Encoding": "gzip, deflate",
                            "Connection": "keep-alive"
                        }

                        data = {}

                        res = self.session.get(url, headers=headers, data=data).text
                        topic_json = json.loads(json.dumps(json.loads(res, strict=False), indent=4,
                                                           ensure_ascii=False))
                        # print("topic_json ==",topic_json)
                        code = topic_json["code"]
                        if code != 200:
                            continue
                        topic_detail = topic_json["mes"]

                        # 时间最近的新闻
                        newstime = topic_detail["newstime"]

                        if newstime > newestpubtime:
                            newestarticleiD = topic_detail["id"]
                            newestpubtime = newstime

                        article_fields = InitClass().article_fields()
                        article_fields["appname"] = self.newsname
                        article_fields["platformID"] = self.platform_id
                        article_fields["specialtopic"] = 1  # 是否是专题
                        article_fields["topicid"] = topic_id
                        article_fields["topicTitle"] = zhuanti_title
                        article_fields["channelname"] = "专题"
                        article_fields["channelID"] = ""
                        article_fields["url"] = url
                        article_fields["banner"] = banner
                        article_fields = self.formatearticledetail(topic_detail, article_fields)
                        fields = InitClass().wash_article_data(fields)
                        yield {"code": 1, "msg": "OK", "data": {"works": article_fields}}
                    yield {"code": 1, "msg": "OK", "data": {"topic": fields}}
                except Exception as e:
                    logging.info(f"错误数量{num},{e}")
                    num += 1

            else:
                # 普通新闻
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                    # print("content_s==",content_s)

                    detail = content_s["mes"]
                    fields["appname"] = self.newsname
                    fields["platformID"] = self.platform_id
                    fields = self.formatearticledetail(detail, fields)
                    fields = InitClass().wash_article_data(fields)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
                except Exception as e:
                    num += 1
                    logging.info(f"错误数量{num},{e}")

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Lijiangwang(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
