# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
import requests
from App.appspider_m import Appspider
from App.initclass import InitClass


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
        app_params = InitClass().app_params(url, headers, method, data = data)
        # 如果携带json数据，用下列方式存储发送数据
        # app_params = InitClass().app_params(url, headers, method, data = data ,appjson=app_json)
        yield app_params

    @staticmethod
    def analyzechannels(channelsres):
        """
        此方法主要获取channelid,channelname即可
        若请求文章列表页需要channeltype，categoryname，categoryid,则以categoryname= categoryname形式传递参数
        :param channelsres:
        :return:
        """
        # 将返回的数据转为json数据
        channelslists = json.loads(channelsres)
        # 返回的数据是编码错误，则用下面代码解析数据
        # channelslists = json.loads(json.dumps(channelsres,indent=4,ensure_ascii=False))
        print(channelslists)
        channelparams = []

        fixeds = channelslists['Data']['Fixeds']
        for channel in fixeds:
            channelid = channel['ModliarId']
            channelname = channel['Title']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)

        modilars = channelslists['Data']['Modilars']
        for channel in modilars:
            channelid = channel['ModliarId']
            channelname = channel['Title']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)

        yield channelparams

    @staticmethod
    def getarticlelistsparams(channelsparams):
        """
        此方法目的是组建请求文章列页面数据参数，url，headers，data，若以json形式发送数据，则channeljson = channeljson
        :param channelsparams:
        :return:
        """
        articleparams = []
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")


            if channelname == "首页":
                #首页频道列表数据
                url = "https://apiparty.xinhuaapp.com/Service/IndexSvr.svc/GetIndexPage"
            else:
                #其余频道列表数据
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

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,channel_id = channelid, data = data)
            # 若数据体以json形式发送则以下面方式发送数据上面方式注释

            articleparams.append(articlelist_param)
        yield articleparams

    @staticmethod
    def analyze_articlelists(articleslist_ress):
        """
        解析文章列表页，目的是为了获取文章具体信息，组建请求文章详情数据体
        :param articleslist_ress:
        :return:
        """
        articlesparams = []
        for articleslist_res in articleslist_ress:
            banners = articleslist_res.get("banner")
            channelname = articleslist_res.get("channelname")
            channelid = articleslist_res.get("channelID")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}

            try:
                articlelist_json = json.loads(articlelist_res)
                # 可在下面打印处打断点，查看请求到的数据
                #print("articlelist_json==",articlelist_json)

                #ModilarData 未找到数据

                #总新闻列表
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

                    #区分文章类型
                    contenttype = article['ContentType']

                    #外链
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
                        print("pubtime==",pubtime)
                        print("article==",article)
                        print("外链==", json.dumps(fields, indent=4, ensure_ascii=False))
                        continue

                    articleparam["contenttype"] = contenttype
                    articleparam["projectid"] = projectid
                    articleparam["template"] = template
                    articleparam["appId"] = appId
                    articleparam["articleurl"] = shareurl
                    articleparam["source"] = source#此步骤为存储文章来源
                    articleparam["author"] = author#此步骤为存储作者
                    articleparam["likenum"] = likenum#此步骤为存储点赞数
                    articleparam["commentnum"] = commentnum#此步骤为存储评论数
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

                    #articleparam["articleurl"] = url
                    print("article==",article)
                    print("articleparam==",articleparam)
                    articlesparams.append(articleparam)

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
                    print("banner_item==",banner_item)
                    print("articleparam_ba==",articleparam_ba)
                    articlesparams.append(articleparam_ba)

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
                    print("reitem=", re_item)
                    print("articleparam_re =",articleparam_re)
                    articlesparams.append(articleparam_re)

            except Exception as e:
                print('eeee====',e, articlelist_json)
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        """
        组建请求文章详情所需要的数据体
        :param articles:
        :return:
        """
        articlesparam = []


        for articleparam in articles:

            # 0
            #1 文字
            #2 正文有视频
            #4 画廊
            #8 外链
            #64 专题
            # 自定义 -100 今日推荐列表
            # -200 推荐，类似订阅号
            contenttype = articleparam.get("contenttype")

            if contenttype == 1 or contenttype == 2 or contenttype == 0:

                #文字新闻
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
                #画廊

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
                    "PageNo" : 1,
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
            #
            # elif contenttype == -100:
            #    #首页，今日推荐列表
            #     url = "https://apiparty.xinhuaapp.com/Service/ContentSvr.svc/GetContentByIsHot"
            #     method = 'get'
            #     headers = {
            #         "token": "01238e900eef1035343f11ed98b24fa365e39d47fdb56604eff668e3b2f8370b284495a340ae52adc1ccb3652f6faeb50ef97cce8afd6871e2c4ab44ec7c4f0f1608081008049",
            #         "random": "999",
            #         "Host": "apiparty.xinhuaapp.com",
            #         "Connection": "Keep-Alive",
            #         "Accept-Encoding": "gzip",
            #         "User-Agent": "okhttp/3.10.0"
            #     }
            #     data = {
            #         "appId": "128",
            #         "isHot": "1",
            #         "pageNo": "1",
            #         "pageSize": "20",
            #         "states": "8"
            #     }
            else:
                print("未知类型")
                continue
            videos = url

            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
            channelid = articleparam.get("channelID")
            banner = articleparam.get("banner")
            imgurl = articleparam.get("imageurl")
            #videos = articleparam.get("videos")
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
            article = InitClass().article_params_fields(url, headers, method, channelname,channel_id = channelid, imageurl = imgurl, data = data,
                                                        videourl = videos, videocover = videocover, pubtime = pubtime,
                                                        createtime = createtime, updatetime = updatetime,
                                                        source = source, author = author, likenum = likenum,
                                                        commentnum = commentnum, sharenum = sharenum, readnum = readnum,
                                                        articleurl = articleurl,banners = banner)
            articlesparam.append(article)
        yield articlesparam

    @staticmethod
    def analyzearticles(articles_res):
        for articleres in articles_res:
            channelname = articleres.get("channelname")
            channelid = articleres.get("channelID")
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            banners = articleres.get("banner")
            url = articleres.get("videourl")

            # 若上面存储了此字段需用下列方式获取
            # videos = articleres.get("videos")
            # videocover = articleres.get("videocover")
            # pubtime = articleres.get("pubtime")
            # createtime = articleres.get("createtime")
            # updatetime = articleres.get("updatetime")
            # source = articleres.get("source")
            # likenum = articleres.get("author")
            # commentnum = articleres.get("author")
            # sharenum = articleres.get("sharenum")
            # readnum = articleres.get("readnum")
            # author = articleres.get("author")
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


             #文章的html网址，提取shareurl
            # fields["workerid"] = workerid #文章的id
            # fields["title"] = title #文章的标题
            # fields["content"] = content #文章的内容详情
            # fields["articlecovers"] = imgurl #文章的封面，一般为上面get到的字段
            # fields["images"] = iamges #文章详情内的图片url，一般为列表需遍历获取
            # fields["videos"] = videos #文章的视频链接地址
            # fields["videocover"] = videocover #文章的视频封面地址
            # fields["width"] = width #文章的视频宽
            # fields["height"] = height #文章的视频高
            # fields["source"] = source #文章的来源
            # fields["pubtime"] = pubtime #文章的发布时间
            # fields["createtime"] = createtime #文章的发布时间
            # fields["updatetime"] = updatetime #文章的更新时间
            # fields["likenum"] = likenum #文章的点赞数
            # fields["playnum"] = playnum #视频的播放数
            # fields["commentnum"] = commentnum #文章评论数
            # fields["readnum"] = readnum #文章的阅读数
            # fields["trannum"] = trannum #文章的转发数
            # fields["sharenum"] = sharenum #文章分享数
            # fields["author"] = author #文章作者
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent = 4, ensure_ascii = False))
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


                    fields["appname"] = appname

                    print("详情结果")
                    print("结果===", json.dumps(fields, indent=4, ensure_ascii=False))
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


                    fields["appname"] = appname
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
                    #print("详情结果")
                    print("结果===", json.dumps(fields, indent=4, ensure_ascii=False))

            except Exception as e:
                print("eeeee11===",e)

    def run(self):
        appparams = self.get_app_params()
        channelsres = self.getchannels(appparams.__next__())
        channelsparams = self.analyzechannels(channelsres.__next__())
        articleparams = self.getarticlelistsparams(channelsparams.__next__())
        articles_ress = self.getarticlelists(articleparams.__next__())
        articles = self.analyze_articlelists(articles_ress.__next__())
        articlesparam = self.getarticleparams(articles.__next__())
        articles_html = self.getarticlehtml(articlesparam.__next__())
        self.analyzearticles(articles_html.__next__())


if __name__ == '__main__':
    spider = Yunnantongchuxiongzhou('云南通·楚雄州')
    spider.run()
