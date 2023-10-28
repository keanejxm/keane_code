# Author Keane
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json


import requests
from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass

class Pengpaixinwen(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        #获取所有频道url
        url = "https://app.thepaper.cn/clt/jsp/v6/allNodes.jsp?type=1"
        #频道请求头
        headers = {
            "authority": "app.thepaper.cn",
            "scheme": "https",
            "wd-version": "8.1.6",
            "wd-uuid": "008796760196586",
            "wd-ua": "Dalvik%2F2.1.0%20%28Linux%3B%20U%3B%20Android%206.0.1%3B%20MuMu%20Build%2FV417IR%29%20%E6%BE%8E%E6%B9%83%E6%96%B0%E9%97%BB%2F8.1.6",
            "paper-device-id": "fabb0e04-88c0-47e7-9709-f59c5e26b24a",
            "wd-system": "6.0.1",
            "package_name": "com.wondertek.paper",
            "wd-resolution": "1053*1872",
            "wd-channel": "TX04",
            "paper-client-type": "04",
            "wd-client-type": "04",
            "network": "1",
            "piccardmode": "3",
            "x-tingyun-id": "Sg5W5o3G1Fw;c=2;r=1956336660;",
            "accept-encoding": "gzip",
            "cookie": "JSESSIONID=5B87D483C6E9CCD235A5E73DA55C6B9F; route=030e64943c5930d7318fe4a07bfd2a3c; __ads_session=H5kgJZWwlAmEZ6sBjQA=; SERVERID=srv-omp-ali-app10_80",
            "user-agent": "okhttp/3.12.12",
        }
        #频道数据体
        data = {}
        #如果携带的是json数据体,用appjson发送
        app_json = {}
        #频道请求方式
        method = "get"
        # app_params = InitClass().app_params(url, headers, method, data = data)
        app_params = InitClass().app_params(url, headers, method, data = data ,appjson=app_json)
        yield app_params

    @staticmethod
    def analyzechannels(channelsres):
        """
        此方法获取channelid,channelname即可
        :param channelsres:
        :return:
        """
        #将返回的数据转为json数据
        channelslists = json.loads(channelsres)
        ## channelslists = json.loads(json.dumps(channelsres,indent=4,ensure_ascii=False))
        #频道列表
        #print(channelslists)
        channelparams = []

        # channelid = "25949"
        # channelname = "要闻"
        #
        # channelparam = InitClass().channel_fields(channelid, channelname)
        # channelparams.append(channelparam)

        for channel in channelslists['nodeList']:
            channelid = channel['nodeId']
            channelname = channel['name']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistsparams(channelsparams):
        articleparams = []
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")

            # 频道列表
            url = "https://app.thepaper.cn/clt/jsp/v6/channelContList.jsp?"

            if channelname == "要闻":
                headers = {
                    "authority": "app.thepaper.cn",
                    "scheme": "https",
                    "wd-version": "8.1.6",
                    "wd-uuid": "008796760196586",
                    "wd-ua": "Dalvik%2F2.1.0%20%28Linux%3B%20U%3B%20Android%206.0.1%3B%20MuMu%20Build%2FV417IR%29%20%E6%BE%8E%E6%B9%83%E6%96%B0%E9%97%BB%2F8.1.6",
                    "paper-device-id": "fabb0e04-88c0-47e7-9709-f59c5e26b24a",
                    "wd-system": "6.0.1",
                    "package_name": "com.wondertek.paper",
                    "wd-resolution": "1053*1872",
                    "wd-channel": "TX04",
                    "paper-client-type": "04",
                    "wd-client-type": "04",
                    "network": "1",
                    "piccardmode": "3",
                    "x-tingyun-id": "Sg5W5o3G1Fw;c=2;r=1112165280;",
                    "accept-encoding": "gzip",
                    "user-agent": "okhttp/3.12.12",
                }
                channelJson = {}
                data = {"n": channelid,
                        "pullDownTimes": 1}
                method = 'get'
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                           channeljson=channelJson,channelid=channelid)
                articleparams.append(articlelist_param)

            else:
                #其余频道请求列表url
                headers = {
                    "authority": "app.thepaper.cn",
                    "scheme": "https",
                    "wd-version": "8.1.6",
                    "wd-uuid": "008796760196586",
                    "wd-ua": "Dalvik%2F2.1.0%20%28Linux%3B%20U%3B%20Android%206.0.1%3B%20MuMu%20Build%2FV417IR%29%20%E6%BE%8E%E6%B9%83%E6%96%B0%E9%97%BB%2F8.1.6",
                    "paper-device-id": "fabb0e04-88c0-47e7-9709-f59c5e26b24a",
                    "wd-system": "6.0.1",
                    "package_name": "com.wondertek.paper",
                    "wd-resolution": "1053*1872",
                    "wd-channel": "TX04",
                    "paper-client-type": "04",
                    "wd-client-type": "04",
                    "network": "1",
                    "piccardmode": "3",
                    "x-tingyun-id": "Sg5W5o3G1Fw;c=2;r=1969575906;",
                    "accept-encoding": "gzip",
                    "cookie": "JSESSIONID=781CD58C7FFFC0B209BA30B70200760C; route=ac205598b1fccbab08a64956374e0f11; __ads_session=Pg5dR+mwlAmlB7sB8AA=; SERVERID=srv-omp-ali-app6_80",
                    "user-agent": "okhttp/3.12.12",
                }
                data = {"n": channelid}
                channelJson = {}
                method = 'get'
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data,channeljson=channelJson,channelid=channelid)
                articleparams.append(articlelist_param)
        yield articleparams

    @staticmethod
    def formerArticle(item):

        cardmode = ""
        try:
            cardmode = item["cardMode"]
        except Exception as e:
            print("无cardMode")

        if cardmode == "5" or cardmode == "107" or cardmode == "72" or not cardmode:
            # 广告
            # 24小时最热
            # 72 未知
            return

        # print("item==", item)
        # print("cardmode==", cardmode)

        articleparam = InitClass().article_list_fields()
        try:
            articletitle = item['name']
            articleparam["articletitle"] = articletitle
        except Exception as e:
            print('e1==', e)

        try:
            articleid = item['contId']
            articleparam["articleid"] = articleid
        except Exception as e:
            print('e2==', e, item)

        try:
            referer = item['referer']
            articleparam["referer"] = referer
        except Exception as e:
            print('无 referer')

        try:
            object_type = item['objectInfo']['object_type']
            object_sub_type = item['objectInfo']['object_sub_type']
            articleparam["object_type"] = object_type
            articleparam["object_sub_type"] = object_sub_type
        except Exception as e:
            print(' e9 ==', e)
        return articleparam

    def analyze_articlelists(self, articleslist_ress):
        articlesparams = []
        for articleslist_res in articleslist_ress:
            channelname = articleslist_res.get("channelname")
            channelid = articleslist_res.get("channelid")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            # 各频道列表数据
            try:
                articlelist_json = json.loads(articlelist_res)
                # print('articlelist_json==',articlelist_json)
                try:
                    articlelists = articlelist_json['contList']
                    # articlelistsurl = articlelist_json['data']['listUrl']
                    for article in articlelists:
                        # print('article===',article)

                        # 特殊样式 置顶，滚动，banner
                        item = article
                        if "childList" in item.keys():
                            if len(item['childList']) > 0:
                                try:
                                    if item["cardMode"] == "103":
                                        # banner
                                        for banner in item['childList']:
                                            articleparam = self.formerArticle(banner)
                                            if articleparam:
                                                articleparam["banner"] = 1
                                                articleparam["channelname"] = channelname
                                                articleparam["channelid"] = channelid
                                                articlesparams.append(articleparam)
                                        continue
                                except Exception as e:
                                    print("cardMode=", e)


                                item = item['childList'][0]
                                # cardMode 102 置顶滚动
                                # cardMode 103 banner
                                # cardMode 5 广告
                                # cardMode 107 24小时热文
                                # cardMode 117 大专题

                        articleparam = self.formerArticle(item)
                        if articleparam:
                            articleparam["channelname"] = channelname
                            articleparam["channelid"] = channelid
                            articlesparams.append(articleparam)

                except Exception as e:
                    print('e6==', e,articlelist_json)

            except Exception as e:
                print('e7==', e, articlelist_json)
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articlesparam = []
        #请求详情url
        method = 'get'
        for articleparam in articles:

            articleId = articleparam.get("articleid")
            if articleId == "" :
                print("articleId 为空")
                continue

            channelname = articleparam.get("channelname") #
            channelid = articleparam.get("channelid")

            banner = articleparam.get("banner") #
            imgurl = articleparam.get("imageurl")

            videos = channelid #articleparam.get("videos")
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

            articlename = articleparam.get("articletitle")

            object_type = articleparam.get("object_type")
            object_sub_type = articleparam.get("object_sub_type")

            if object_type == 'article':
                #普通新闻
                if object_sub_type == 'video_normal':
                    # 视频新闻
                    # video_normal
                    url = 'https://app.thepaper.cn/clt/jsp/v6/videoContent.jsp?'
                    headers = {
                        "authority": "app.thepaper.cn",
                        "scheme": "https",
                        "wd-version": "8.1.6",
                        "wd-uuid": "008796760196586",
                        "wd-ua": "Dalvik%2F2.1.0%20%28Linux%3B%20U%3B%20Android%206.0.1%3B%20MuMu%20Build%2FV417IR%29%20%E6%BE%8E%E6%B9%83%E6%96%B0%E9%97%BB%2F8.1.6",
                        "paper-device-id": "fabb0e04-88c0-47e7-9709-f59c5e26b24a",
                        "wd-system": "6.0.1",
                        "package_name": "com.wondertek.paper",
                        "wd-resolution": "1053*1872",
                        "wd-channel": "TX04",
                        "paper-client-type": "04",
                        "wd-client-type": "04",
                        "network": "1",
                        "piccardmode": "3",
                        "x-tingyun-id": "Sg5W5o3G1Fw;c=2;r=1191517487;",
                        "accept-encoding": "gzip",
                        "cookie": "JSESSIONID=21D9B80B18451669DCD8744C0C50803B; route=b03b7d25d906a49107f48461e5952a87; __ads_session=J09+5na0lAl32+cB0AA=; SERVERID=srv-omp-ali-app7_80",
                        "user-agent": "okhttp/3.12.12",
                    }
                else:
                    # 普通新闻
                    url = 'https://app.thepaper.cn/clt/jsp/v6/newDetail.jsp?'
                    headers = {
                        "authority": "app.thepaper.cn",
                        "scheme": "https",
                        "wd-version": "8.1.6",
                        "wd-uuid": "008796760196586",
                        "wd-ua": "Dalvik%2F2.1.0%20%28Linux%3B%20U%3B%20Android%206.0.1%3B%20MuMu%20Build%2FV417IR%29%20%E6%BE%8E%E6%B9%83%E6%96%B0%E9%97%BB%2F8.1.6",
                        "paper-device-id": "fabb0e04-88c0-47e7-9709-f59c5e26b24a",
                        "wd-system": "6.0.1",
                        "package_name": "com.wondertek.paper",
                        "wd-resolution": "1053*1872",
                        "wd-channel": "TX04",
                        "paper-client-type": "04",
                        "wd-client-type": "04",
                        "network": "1",
                        "piccardmode": "3",
                        "x-tingyun-id": "Sg5W5o3G1Fw;c=2;r=315224543;",
                        "accept-encoding": "gzip",
                        "cookie": "JSESSIONID=21D9B80B18451669DCD8744C0C50803B; route=b03b7d25d906a49107f48461e5952a87; __ads_session=WDXIhKu0lAmrgWkClwA=; SERVERID=srv-omp-ali-app7_80",
                        "user-agent": "okhttp/3.12.12",
                    }
                    detailJson = {
                    }

                    data = {
                        "c": articleparam.get("articleid"),
                        "referer": articleparam.get("referer"),
                    }

                    #article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data, articlejson=detailJson)

                    # 若APP有关于时间的反爬加sleeptime = 1，若发送为json数据体，则添加articlejson = articlejson
                    article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                                videourl=videos, videocover=videocover, pubtime=pubtime,
                                                                createtime=createtime, updatetime=updatetime,
                                                                source=source, author=author, likenum=likenum,
                                                                commentnum=commentnum, sharenum=sharenum,
                                                                readnum=readnum,
                                                                articleurl=articleurl, banners=banner)

                    articlesparam.append(article)

            elif object_type == 'special':
                # 专题新闻 请求列表

                url = 'https://app.thepaper.cn/clt/jsp/v6/special.jsp?'
                headers = {
                    "authority": "app.thepaper.cn",
                    "scheme": "https",
                    "wd-version": "8.1.6",
                    "wd-uuid": "008796760196586",
                    "wd-ua": "Dalvik%2F2.1.0%20%28Linux%3B%20U%3B%20Android%206.0.1%3B%20MuMu%20Build%2FV417IR%29%20%E6%BE%8E%E6%B9%83%E6%96%B0%E9%97%BB%2F8.1.6",
                    "paper-device-id": "fabb0e04-88c0-47e7-9709-f59c5e26b24a",
                    "wd-system": "6.0.1",
                    "package_name": "com.wondertek.paper",
                    "wd-resolution": "1053*1872",
                    "wd-channel": "TX04",
                    "paper-client-type": "04",
                    "wd-client-type": "04",
                    "network": "1",
                    "piccardmode": "3",
                    "x-tingyun-id": "Sg5W5o3G1Fw;c=2;r=315224543;",
                    "accept-encoding": "gzip",
                    "cookie": "JSESSIONID=21D9B80B18451669DCD8744C0C50803B; route=b03b7d25d906a49107f48461e5952a87; __ads_session=ufXR+3+7lAnVXQADswA=; SERVERID=srv-omp-ali-app7_80",
                    "user-agent": "okhttp/3.12.12",
                }
                detailJson = {
                }

                data = {
                    "c": articleparam.get("articleid"),
                }

                #article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data, articlejson=detailJson)
                article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                            videourl=videos, videocover=videocover, pubtime=pubtime,
                                                            createtime=createtime, updatetime=updatetime,
                                                            source=source, author=author, likenum=likenum,
                                                            commentnum=commentnum, sharenum=sharenum,
                                                            readnum=readnum,
                                                            articleurl=articleurl, banners=banner)

                articlesparam.append(article)

            else:
                 # operate
                 print("operate object_type=",object_type)

        yield articlesparam

    @staticmethod
    def analyzearticles(articles_res):
        for articleres in articles_res:
            # 详情结果
            #print("详情结果",articleres)
            channelname = articleres.get("channelname")
            channelid = articleres.get("videourl")

            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            banners = articleres.get("banner")

            articleres = articleres.get("articleres")

            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent = 4, ensure_ascii = False))

                # print("articlejson===",articlejson)
                if "childNodeList" in articlejson.keys():
                    #二级专题列表

                    specialinfo = articlejson["specialInfo"]
                    digest = specialinfo["desc"]
                    cover = specialinfo["pic"]
                    shareurl = specialinfo["shareUrl"]
                    topicid = specialinfo["contId"]
                    topictitle = specialinfo["shareName"]

                    topic_fields = InitClass().topic_fields()

                    topic_fields["platformName"] = appname
                    topic_fields["topicID"] = topicid
                    topic_fields["channelName"] = channelname
                    topic_fields["channelID"] = channelid
                    topic_fields["digest"] = digest
                    topic_fields["channelType"] = ""
                    topic_fields["topicUrl"] = shareurl
                    topic_fields["title"] = topictitle
                    topic_fields["topicCover"] = [cover]
                    topic_fields["original"] = ""
                    topic_fields["pubTime"] = 0
                    topic_fields["topic"] = 1
                    topic_fields["banner"] = 0
                    topic_fields["updateTime"] = 0
                    topic_fields["createtime"] = 0

                    topicnum = 0
                    newestpubtime = 0
                    newestarticleid = ""

                    childlist = articlejson["childNodeList"]
                    for childitem in childlist:
                        contentlist = childitem["contList"]

                        topicnum += len(contentlist)

                        for article in contentlist:

                            articleid = article["contId"]
                            detailurl = 'https://app.thepaper.cn/clt/jsp/v6/newDetail.jsp?'
                            detailheaders = {
                                "authority": "app.thepaper.cn",
                                "scheme": "https",
                                "wd-version": "8.1.6",
                                "wd-uuid": "008796760196586",
                                "wd-ua": "Dalvik%2F2.1.0%20%28Linux%3B%20U%3B%20Android%206.0.1%3B%20MuMu%20Build%2FV417IR%29%20%E6%BE%8E%E6%B9%83%E6%96%B0%E9%97%BB%2F8.1.6",
                                "paper-device-id": "fabb0e04-88c0-47e7-9709-f59c5e26b24a",
                                "wd-system": "6.0.1",
                                "package_name": "com.wondertek.paper",
                                "wd-resolution": "1053*1872",
                                "wd-channel": "TX04",
                                "paper-client-type": "04",
                                "wd-client-type": "04",
                                "network": "1",
                                "piccardmode": "3",
                                "x-tingyun-id": "Sg5W5o3G1Fw;c=2;r=315224543;",
                                "accept-encoding": "gzip",
                                "cookie": "JSESSIONID=21D9B80B18451669DCD8744C0C50803B; route=b03b7d25d906a49107f48461e5952a87; __ads_session=WDXIhKu0lAmrgWkClwA=; SERVERID=srv-omp-ali-app7_80",
                                "user-agent": "okhttp/3.12.12",
                            }
                            detaildata = {
                                "c": articleid,
                                "referer": "",
                            }
                            detailres = requests.get(detailurl,headers=detailheaders,params=detaildata).text
                            detailjson = json.loads(json.dumps(json.loads(detailres, strict=False), indent=4, ensure_ascii=False))

                            data = detailjson["content"]
                            article_fields = InitClass().article_fields()
                            article_fields["channelname"] = channelname
                            article_fields["channelID"] = channelid
                            article_fields["appname"] = appname
                            article_fields["banner"] = 0

                            title = data['name']  # 标题
                            source = data['source']  # 来源

                            try:
                                content = data['html']  # 文章内容
                                article_fields["content"] = content
                            except Exception as e:
                                print("无正文")

                            commentNum = data['interactionNum']  # 阅读数
                            if not commentNum:
                                commentNum = 0

                            likeNum = data['praiseTimes']  # 点赞数
                            if not likeNum:
                                likeNum = 0

                            author = data['author']  # 作者
                            workerid = data['contId']  # 新闻id
                            url = data['shareUrl']  # 分享url

                            pubtime = data["pubTime"]
                            pubtime = InitClass().date_time_stamp(pubtime)

                            if pubtime > newestpubtime:
                                newestpubtime = pubtime
                                newestarticleid = articleid

                            article_fields["pubtime"] = pubtime
                            article_fields["createtime"] = 0
                            article_fields["updatetime"] = 0

                            try:
                                cover = articlejson['coverPic']  # 封面图
                                covers = list()
                                covers.append(cover)
                                article_fields["articlecovers"] = covers
                            except  Exception as  e:
                                print("coverPic e==", e)

                            article_fields["title"] = title
                            article_fields["url"] = url
                            article_fields["workerid"] = workerid
                            article_fields["source"] = source
                            article_fields["commentnum"] = commentNum
                            article_fields["likenum"] = likeNum
                            article_fields["author"] = author
                            article_fields["specialtopic"] = 1
                            article_fields["topicid"] = topicid
                            article_fields["topicTitle"] = topictitle


                            try:
                                videos = data['videos']
                                contentvideo = list()
                                videocovers = list()
                                for vd in videos:
                                    vdurl = vd["url"]
                                    contentvideo.append(vdurl)
                                    vcobj = vd["imageObj"]
                                    vdcover = vcobj["url"]
                                    videocovers.append(vdcover)
                                article_fields["videos"] = contentvideo
                                article_fields["videocover"] = videocovers
                            except  Exception as  e:
                                print("e23 ==", e)

                            try:
                                images = data['images']
                                contentimages = list()
                                for img in images:
                                    cimgurl = img["url"]
                                    contentimages.append(cimgurl)
                                article_fields["images"] = contentimages
                            except  Exception as  e:
                                print("e24 ==", e)

                            print("专题内文章===", json.dumps(article_fields, indent=4, ensure_ascii=False))

                    #列表补全，不准确
                    topic_fields["articleNum"] = topicnum
                    topic_fields["newestArticleID"] = newestarticleid

                    print("大专题===",json.dumps(topic_fields, indent = 4, ensure_ascii = False))
                else:

                    fields = InitClass().article_fields()
                    fields["channelname"] = channelname
                    fields["channelID"] = channelid
                    # fields["imageurl"] = imgurl
                    fields["appname"] = appname
                    fields["banner"] = banners

                    data = articlejson['content']
                    title = data['name'] # 标题
                    source = data['source']  # 来源

                    try:
                        content = data['html']  # 文章内容
                        fields["content"] = content
                    except Exception as e:
                        print("无正文")

                    commentNum = data['interactionNum']  # 阅读数
                    if not commentNum:
                        commentNum = 0

                    likeNum = data['praiseTimes'] #点赞数
                    if not likeNum:
                        likeNum = 0

                    author = data['author'] #作者
                    workerid = data['contId'] #新闻id
                    url = data['shareUrl'] #分享url

                    pubtime = data["pubTime"]
                    pubtime = InitClass().date_time_stamp(pubtime)
                    fields["pubtime"] = pubtime
                    fields["createtime"] = 0
                    fields["updatetime"] = 0

                    try:
                        cover = articlejson['coverPic']  # 封面图
                        covers = list()
                        covers.append(cover)
                        fields["articlecovers"] = covers
                    except  Exception as  e:
                        print("coverPic e==",e)

                    fields["title"] = title
                    fields["url"] = url
                    fields["workerid"] = workerid
                    fields["source"] = source
                    fields["commentnum"] = commentNum
                    fields["likenum"] = likeNum
                    fields["author"] = author

                    try:
                        videos = data['videos']
                        contentvideo = list()
                        videocovers = list()
                        for vd in videos:
                            vdurl = vd["url"]
                            contentvideo.append(vdurl)
                            vcobj = vd["imageObj"]
                            vdcover = vcobj["url"]
                            videocovers.append(vdcover)
                        fields["videos"] = contentvideo
                        fields["videocover"] = videocovers
                    except  Exception as  e :
                        print("e23 ==",e)

                    try:
                        images = data['images']
                        contentimages = list()
                        for img in images:
                            cimgurl = img["url"]
                            contentimages.append(cimgurl)
                        fields["images"] = contentimages
                    except  Exception as  e:
                        print("e24 ==", e)

                    print("文章===",json.dumps(fields, indent = 4, ensure_ascii = False))
            except Exception as e:
                print("e22 ==",e,articleres,channelname)


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
    spider = Pengpaixinwen('澎湃新闻')
    spider.run()