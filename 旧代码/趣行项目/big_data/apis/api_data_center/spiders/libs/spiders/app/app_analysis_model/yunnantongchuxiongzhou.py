# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
import requests
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class Yunnantongchuxiongzhou(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "https://apiparty.xinhuaapp.com/Service/IndexSvr.svc/GetNavigation"
        # 频道请求头
        headers = {
            "token": "832183c6be16ec4b9fc105266b53d227e8931dadeebb47df8e2a3c4fcbf8b12be52a7ff5d06fe32823d6ae7074403002b85fb3403af7a7cf97de5ed03a5653891608109021005",
            "random": "999",
            "Host": "apiparty.xinhuaapp.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.10.0",
        }
        # 频道数据体
        data = {
            "styleId": "360",
            "appId": "128",
            "appKey": "d0217",
            "projectId": "1"
        }
        # 如果携带的是json数据体,用appjson发送
        # app_json = {}
        # 频道请求方式
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyzechannels(channelsres):
        """
        此方法主要获取channelid,channelname即可
        若请求文章列表页需要channeltype，categoryname，categoryid,则以categoryname= categoryname形式传递参数
        :param channelsres:
        :return:
        """
        channelslists = json.loads(channelsres)
        fixeds = channelslists['Data']['Fixeds'] + channelslists['Data']['Modilars']
        for channel in fixeds:
            channelid = channel['ModliarId']
            channelname = channel['Title']
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam

    def getarticlelistsparams(self, channelsres):
        """
        此方法目的是组建请求文章列页面数据参数，url，headers，data，若以json形式发送数据，则channeljson = channeljson
        :param channelsparams:
        :return:
        """
        channel_num = 0
        for channel in self.analyzechannels(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            if channelname == "首页":
                url = "https://apiparty.xinhuaapp.com/Service/IndexSvr.svc/GetIndexPage"
            else:
                url = "https://apiparty.xinhuaapp.com/Service/ContentSvr.svc/GetContentList"
            headers = {
                "token": "832183c6be16ec4b9fc105266b53d227e8931dadeebb47df8e2a3c4fcbf8b12be52a7ff5d06fe32823d6ae7074403002b85fb3403af7a7cf97de5ed03a5653891608109021005",
                "random": "999",
                "Host": "apiparty.xinhuaapp.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.10.0"
            }
            data = {
                "modilarId": channelid,
                "pageNo": "1",
                "styleId": "360",
                "appId": "128",
                "appKey": "d0217",
                "projectId": "1"
            }
            method = 'get'
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channel_index_id=channel_index_id, data=data)
            yield channel_field, [articlelist_param]

    @staticmethod
    def analyze_articlelists(articleslist_ress):
        """
        解析文章列表页，目的是为了获取文章具体信息，组建请求文章详情数据体
        :param articleslist_ress:
        :return:
        """
        for articleslist_res in articleslist_ress:
            banners = articleslist_res.get("banner")
            channelname = articleslist_res.get("channelname")
            channelid = articleslist_res.get("channelID")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                # 总新闻列表
                articlelists = articlelist_json['Data']
                n_list = []
                sy_list = []
                try:
                    # 首页列表
                    sy_list = articlelists["IndexContent"]
                except Exception as e:
                    print("非 首页 列表")
                try:
                    # 普通页列表
                    n_list = articlelists["Contents"]
                except Exception as e:
                    print("非普通页 列表")

                for article in n_list + sy_list:

                    articleparam = InitClass().article_list_fields()

                    articleid = article['Id']
                    template = article['Template']
                    appId = article['AppId']

                    projectid = article['ProjectId']
                    shareurl = article['LinkUrl']
                    source = article["Source"]  # 在此处获取到文章的来源，避免在文章详情获取不到来源
                    author = article["Authors"]  # 在此处获取到文章的作者，避免在文章详情获取不到作者
                    likenum = article["Likes"]  # 在此处获取到文章的点赞数，避免在文章详情获取不到点赞数
                    commentnum = article["Comments"]  # 在此处获取到文章的评论数，避免在文章详情获取不到评论数
                    readnum = article["Reads"]  # 在此处获取到文章的阅读数，避免在文章详情获取不到阅读数
                    articletitle = article['Title']

                    # 区分文章类型
                    contenttype = article['ContentType']

                    # 外链
                    if contenttype == 8:
                        fields = InitClass().article_fields()
                        source = article["Source"]  # 在此处获取到文章的来源，避免在文章详情获取不到来源
                        author = article["Authors"]  # 在此处获取到文章的作者，避免在文章详情获取不到作者
                        likenum = article["Likes"]  # 在此处获取到文章的点赞数，避免在文章详情获取不到点赞数
                        commentnum = article["Comments"]  # 在此处获取到文章的评论数，避免在文章详情获取不到评论数
                        readnum = article["Reads"]
                        pubtime = article["IssueTime"]
                        imgurl = article["ImgUrl"]
                        images = article["ImgUrls"]
                        workerid = article["Id"]
                        videos = article["VodUrl"]
                        url = article['LinkUrl']

                        fields["videocover"] = []
                        fields["title"] = articletitle
                        fields["channelname"] = channelname
                        fields["channelID"] = channelid
                        fields["articlecovers"] = [imgurl]
                        fields["banner"] = 0

                        if videos:
                            fields["videos"] = [videos]
                        else:
                            fields["videos"] = []
                        fields["readnum"] = readnum
                        fields["likenum"] = likenum
                        fields["images"] = images
                        fields["appname"] = "云南通·楚雄州"
                        fields["url"] = url
                        fields["workerid"] = workerid
                        fields["source"] = source
                        fields["author"] = author
                        fields["commentnum"] = commentnum
                        fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                        fields["createtime"] = 0
                        fields["updatetime"] = 0
                        print("pubtime==", pubtime)
                        print("article==", article)
                        print("外链==", json.dumps(fields, indent=4, ensure_ascii=False))
                        continue

                    articleparam["contenttype"] = contenttype
                    articleparam["projectid"] = projectid
                    articleparam["template"] = template
                    articleparam["appId"] = appId
                    articleparam["articleurl"] = shareurl
                    articleparam["source"] = source  # 此步骤为存储文章来源
                    articleparam["author"] = author  # 此步骤为存储作者
                    articleparam["likenum"] = likenum  # 此步骤为存储点赞数
                    articleparam["commentnum"] = commentnum  # 此步骤为存储评论数
                    articleparam["readnum"] = readnum
                    try:
                        articleparam["imageurl"] = article['ImgUrl']
                    except Exception as e:
                        logging.info(f"在文章列表出无法获得封面图{e}")
                    articleparam["articleid"] = articleid
                    articleparam["articletitle"] = articletitle
                    articleparam["channelname"] = channelname
                    articleparam["channelID"] = channelid
                    articleparam["banner"] = banners
                    # articleparam["articleurl"] = url
                    yield articleparam
                # banner
                banner_list = []
                try:
                    banner_list = articlelists["Focus"]
                except Exception as e:
                    print("非首页banner")

                for banner_item in banner_list:

                    banners = 1
                    articleparam_ba = InitClass().article_list_fields()

                    articleid = banner_item['Id']
                    template = banner_item['Template']
                    appId = banner_item['AppId']

                    projectid = banner_item['ProjectId']
                    articletitle = banner_item['Title']
                    # 区分文章类型
                    contenttype = banner_item['ContentType']

                    # 外链
                    if contenttype == 8:
                        fields = InitClass().article_fields()
                        source = banner_item["Source"]  # 在此处获取到文章的来源，避免在文章详情获取不到来源
                        author = banner_item["Authors"]  # 在此处获取到文章的作者，避免在文章详情获取不到作者
                        likenum = banner_item["Likes"]  # 在此处获取到文章的点赞数，避免在文章详情获取不到点赞数
                        commentnum = banner_item["Comments"]  # 在此处获取到文章的评论数，避免在文章详情获取不到评论数
                        readnum = banner_item["Reads"]
                        pubtime = banner_item["IssueTime"]
                        imgurl = banner_item["ImgUrl"]
                        images = banner_item["ImgUrls"]
                        workerid = banner_item["Id"]
                        videos = banner_item["VodUrl"]
                        url = banner_item['LinkUrl']

                        fields["title"] = articletitle
                        fields["channelname"] = channelname
                        fields["articlecovers"] = [imgurl]
                        fields["banner"] = 0

                        if videos:
                            fields["videos"] = [videos]
                        else:
                            fields["videos"] = []

                        fields["readnum"] = readnum
                        fields["likenum"] = likenum
                        fields["images"] = images
                        fields["appname"] = "云南通·楚雄州"
                        fields["url"] = url
                        fields["workerid"] = workerid
                        fields["source"] = source
                        fields["author"] = author
                        fields["commentnum"] = commentnum
                        fields["pubtime"] = pubtime
                        fields["banner"] = banners
                        print("外链==", json.dumps(fields, indent=4, ensure_ascii=False))
                        continue
                    shareurl = banner_item['LinkUrl']

                    try:
                        articleparam_ba["imageurl"] = banner_item['ImgUrl']
                    except Exception as e:
                        logging.info(f"在文章列表出无法获得封面图{e}")

                    articleparam_ba["contenttype"] = contenttype
                    articleparam_ba["articleurl"] = shareurl
                    articleparam_ba["projectid"] = projectid
                    articleparam_ba["template"] = template
                    articleparam_ba["appId"] = appId
                    articleparam_ba["articleid"] = articleid
                    articleparam_ba["articletitle"] = articletitle
                    articleparam_ba["channelname"] = channelname
                    articleparam_ba["channelID"] = channelid
                    articleparam_ba["banner"] = banners
                    yield articleparam_ba
                re_list = []
                try:
                    # 推荐 ，进入一个和首页滚动一样的列表
                    re_list = articlelists["Recommend"]
                except Exception as e:
                    print("非 推荐")

                for re_item in re_list:
                    articleparam_re = InitClass().article_list_fields()
                    # 区分文章类型
                    articleparam_re["contenttype"] = -200
                    articleid = re_item['Id']
                    projectid = re_item['ProjectId']  # "1"
                    articleparam_re["projectid"] = projectid
                    articletitle = re_item['Title']
                    try:
                        articleparam_re["imageurl"] = re_item['ImgUrl']
                    except Exception as e:
                        logging.info(f"在文章列表出无法获得封面图{e}")
                    articleparam_re["articleid"] = articleid
                    articleparam_re["articletitle"] = articletitle
                    articleparam_re["channelname"] = channelname
                    articleparam_re["channelID"] = channelid
                    articleparam_re["banner"] = banners
                    yield articleparam_re
            except Exception as e:
                print('eeee====', e, articlelist_json)

    def getarticleparams(self, articles):
        """
        组建请求文章详情所需要的数据体
        :param articles:
        :return:
        """
        articlesparam = []
        for articleparam in articles:

            # 0
            # 1 文字
            # 2 正文有视频
            # 4 画廊
            # 8 外链
            # 64 专题
            # 自定义 -100 今日推荐列表
            # -200 推荐，类似订阅号
            contenttype = articleparam.get("contenttype")
            if contenttype == 1 or contenttype == 2 or contenttype == 0:
                # 文字新闻
                method = 'get'
                url = "https://apiparty.xinhuaapp.com/Service/ContentSvr.svc/GetContentDetail"
                headers = {
                    "token": "01238e900eef1035343f11ed98b24fa365e39d47fdb56604eff668e3b2f8370b284495a340ae52adc1ccb3652f6faeb50ef97cce8afd6871e2c4ab44ec7c4f0f1608081008049",
                    "random": "999",
                    "Host": "apiparty.xinhuaapp.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.10.0"
                }
                articleid = articleparam.get("articleid")
                template = articleparam.get("template")
                appId = articleparam.get("appId")
                projectid = articleparam.get("projectid")
                data = {
                    "contentId": articleid,
                    "template": template,
                    "appId": appId,
                    "appKey": "d0217",
                    "projectId": projectid
                }
            elif contenttype == 4:
                # 画廊

                method = 'get'
                url = "https://apiparty.xinhuaapp.com/Service/ContentSvr.svc/GetContentAtlas"
                headers = {
                    "token": "01238e900eef1035343f11ed98b24fa365e39d47fdb56604eff668e3b2f8370b284495a340ae52adc1ccb3652f6faeb50ef97cce8afd6871e2c4ab44ec7c4f0f1608081008049",
                    "random": "999",
                    "Host": "apiparty.xinhuaapp.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.10.0"
                }

                articleid = articleparam.get("articleid")
                appId = articleparam.get("appId")
                projectid = articleparam.get("projectid")
                data = {
                    "contentId": articleid,
                    "appId": appId,
                    "appKey": "d0217",
                    "projectId": projectid
                }

            elif contenttype == 64:
                url = "https://apiparty.xinhuaapp.com/Service/ContentSvr.svc/GetContentTheme"
                method = 'get'
                headers = {
                    "token": "01238e900eef1035343f11ed98b24fa365e39d47fdb56604eff668e3b2f8370b284495a340ae52adc1ccb3652f6faeb50ef97cce8afd6871e2c4ab44ec7c4f0f1608081008049",
                    "random": "999",
                    "Host": "apiparty.xinhuaapp.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.10.0"
                }

                articleid = articleparam.get("articleid")
                appId = articleparam.get("appId")
                projectid = articleparam.get("projectid")

                data = {
                    "PageNo": 1,
                    "contentId": articleid,
                    "appId": appId,
                    "appKey": "d0217",
                    "projectId": projectid
                }
            elif contenttype == -200:

                url = "https://apiparty.xinhuaapp.com/Service/ContentSvr.svc/GetContentList"
                method = 'get'
                headers = {
                    "token": "01238e900eef1035343f11ed98b24fa365e39d47fdb56604eff668e3b2f8370b284495a340ae52adc1ccb3652f6faeb50ef97cce8afd6871e2c4ab44ec7c4f0f1608081008049",
                    "random": "999",
                    "Host": "apiparty.xinhuaapp.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.10.0"
                }
                articleid = articleparam.get("articleid")
                projectid = articleparam.get("projectid")
                data = {
                    "PageNo": 1,
                    "modilarId": articleid,
                    "appId": 128,
                    "appKey": "d0217",
                    "projectId": projectid
                }
            else:
                print("未知类型")
                continue
            videos = url
            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
            channel_index_id = articleparam.get("channelindexid")
            channelid = articleparam.get("channelID")
            banner = articleparam.get("banner")
            imgurl = articleparam.get("imageurl")
            # videos = articleparam.get("videos")
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
            article = InitClass().article_params_fields(url, headers, method, channelname,
                                                        channel_index_id=channel_index_id,
                                                        imageurl=imgurl, data=data,
                                                        videourl=videos, videocover=videocover, pubtime=pubtime,
                                                        createtime=createtime, updatetime=updatetime,
                                                        source=source, author=author, likenum=likenum,
                                                        commentnum=commentnum, sharenum=sharenum, readnum=readnum,
                                                        articleurl=articleurl, banners=banner)
            yield [article]

    def analyzearticles(self,articles_res):
        for articleres in articles_res:
            channelname = articleres.get("channelname")
            channel_index_id = articleres.get("channelindexid")
            channelid = articleres.get("channelID")
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            banners = articleres.get("banner")
            url = articleres.get("videourl")

            articleurl = articleres.get("articleurl")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["channelID"] = channelid
            fields["articlecovers"] = [imgurl]
            fields["banner"] = banners
            # 如果有下列字段需添加

            if articleurl:
                fields["url"] = articleurl
            else:
                fields["url"] = url

            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                article_detail = articlejson["Data"]

                if "Contents" in article_detail.keys():
                    title = article_detail['Title']  # 标题
                    content = article_detail['Contents']  # 文章列表
                    fields["title"] = title
                    fields["content"] = content
                    fields["contentType"] = -1
                    fields["createtime"] = 0
                    fields["updatetime"] = 0
                    fields["videocover"] = []

                    try:
                        videos = InitClass().get_video(content)
                        fields["videos"] = videos
                    except Exception as e:
                        print("正文无视频")

                    try:
                        images = InitClass().get_images(content)
                        fields["images"] = images
                    except Exception as e:
                        print("正文无图片")

                    fields["appname"] = self.newsname
                    fields["platformID"] = self.platform_id
                    fields["channelindexid"] = channel_index_id

                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
                else:
                    title = article_detail['Title']  # 标题
                    source = article_detail['Source']  # 来源
                    # 专题
                    try:
                        content = article_detail['ThemeData']
                        fields["content"] = content
                        fields["contentType"] = -1
                    except Exception as e:
                        print("非专题 e==", e)

                    # 画廊
                    try:
                        content = article_detail['ContentImage']
                        fields["content"] = content
                        fields["contentType"] = 6
                    except Exception as e:
                        print("非画廊 e==", e)

                    videos = article_detail['VodUrl']
                    images = article_detail['ImgUrls']
                    # 文字新闻
                    try:
                        detail_url = article_detail['DetailUrl']  # 文章内容

                        res = requests.get(detail_url)
                        res.encoding = 'utf-8'
                        content = res.text
                        content = content.lstrip("var ContentDetail = ")
                        content = eval(content)

                        fields["content"] = content
                        fields["contentType"] = 1

                        try:
                            contentvideos = InitClass().get_video(content)
                            if not videos in contentvideos and videos:
                                contentvideos.append(videos)
                            fields["videos"] = contentvideos
                        except Exception as e:
                            print("正文无视频")

                        try:
                            contentimages = InitClass().get_images(content)

                            fields["images"] = images + contentimages
                        except Exception as e:
                            print("正文无图片")

                    except Exception as e:
                        print("非文字新闻 e==", e)

                    pubtime = article_detail['IssueTime']  # 发布时间
                    workerid = article_detail['Id']

                    readnum = article_detail['Reads']

                    url = article_detail["ShareUrl"]
                    author = article_detail["Authors"]
                    commentnum = article_detail["Comments"]
                    likenum = article_detail["Likes"]

                    fields["readnum"] = readnum
                    fields["likenum"] = likenum

                    fields["appname"] = self.newsname
                    fields["platformID"] = self.platform_id
                    fields["channelindexid"] = channel_index_id
                    fields["title"] = title
                    fields["url"] = url
                    fields["workerid"] = workerid
                    fields["source"] = source

                    fields["author"] = author
                    fields["commentnum"] = commentnum

                    fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                    fields["createtime"] = 0
                    fields["updatetime"] = 0
                    fields["videocover"] = []
                    # print("详情结果")
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}

            except Exception as e:
                print("eeeee11===", e)

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Yunnantongchuxiongzhou(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
