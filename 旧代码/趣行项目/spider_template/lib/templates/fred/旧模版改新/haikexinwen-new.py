# Author Keane
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json

from lib.templates.appspider_m import Appspider
import requests
# import time　　
from lib.templates.initclass import InitClass


class Haikexinwen(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        #获取所有频道url
        url = "https://apinews.haiwainet.cn/column/channels/subscribes/every/list"
        #频道请求头
        headers = {
            "access_token": "",
            "clientCode": "100002",
            "secret": "ViEL1JR+FvKr8Vbo/Dq8v69VoigfFGZ5XgREL5ymi6TnWgGOT7Aw9P4my1vEcPWo6a0Vrgt97oif0QBVRMrSlGKQGQA6CWfcPoYARP8nNYjqrLtae/3qNKNRZP4Oam282VDcB5sCZbsPOJgYSCz9xAZLihERBCnel/mE7sE6ciQ=",
            "autograph": "12345678",
            "X-Tingyun-Id": "kcoKoJaDT54;c=2;r=1596789487;u=7f1cceb0b0316ff51c48b294bc860492::1CE42AC505BE1FB2",
            "Content-Type": "application/json;charset=utf-8",
            "Content-Length": "50",
            "Host": "apinews.haiwainet.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.11.0"
        }
        #频道数据体
        data = {}
        #如果携带的是json数据体,用appjson发送
        app_json = {"productVersion": "6.2.20",
                    "productCode": "PRD001"}
        #频道请求方式
        method = "post"
        app_params = InitClass().app_params(url, headers, method, data = data ,appjson=app_json)
        yield app_params

    @staticmethod
    def analyzechannels(channelsres):
        """
        此方法获取channelid,channelname即可
        :param channelsres:
        :return:
        """
        channelparams = []

        # channelid = "1"
        # channelname = "推荐"
        # categoryid = "PRD001"
        # channeltype = 0
        # channeltype = "0"

        # channelid = "24"
        # channelname = "评论"
        # categoryid = "PRD001"
        # channeltype = "1"

        # channelid = "28624494088294400"
        # channelname = "热点"
        # categoryid = "PRD001"
        # channeltype = "1"

        # channelid = "2"
        # channelname = "读报"
        # categoryid = "PRD001"
        # channeltype = "1"

        # channelid = "15"
        # channelname = "关注"
        # categoryid = "PRD001"
        # channeltype = "1"

        # channelid = "1192358909034024961"
        # channelname = "留学"
        # categoryid = "PRD001"
        # channeltype = "1"

        # channelid = "17"
        # channelname = "专题"
        # categoryid = "PRD001"
        # channeltype = "1"

        # channelid = "17"
        # channelname = "专题"
        # categoryid = "PRD001"
        # channeltype = "1"

        # channelparam = InitClass().channel_fields(channelid, channelname,channeltype=channeltype,categoryid=categoryid)
        # channelparams.append(channelparam)


        # #将返回的数据转为json数据
        channelslists = json.loads(channelsres)
        # channelslists = json.loads(json.dumps(channelsres,indent=4,ensure_ascii=False))
        # print(channelslists)
        channelparams = []
        for channel in channelslists['data']['showList']:
            channelid = channel['channelCode']
            channelname = channel['channelName']
            categoryid = channel['productCode']
            channeltype = channel["channelType"]

            channelparam = InitClass().channel_fields(channelid, channelname,channeltype=channeltype,categoryid=categoryid)
            channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistsparams(channelsparams):
        articleparams = []
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")
            categoryid = channel.get("categoryid")

            #获取频道列表
            if channelname == "推荐":
                #推荐频道列表
                url = "https://apinews.haiwainet.cn/recommend/every/res"
                url_banner = "https://apinews.haiwainet.cn/column/adverts/positions/every/materials"  # banner请求接口

                headers_banner ={
                    "access_token": "",
                    "clientCode": "100002",
                    "secret": "ViEL1JR+FvKr8Vbo/Dq8v69VoigfFGZ5XgREL5ymi6TnWgGOT7Aw9P4my1vEcPWo6a0Vrgt97oif0QBVRMrSlGKQGQA6CWfcPoYARP8nNYjqrLtae/3qNKNRZP4Oam282VDcB5sCZbsPOJgYSCz9xAZLihERBCnel/mE7sE6ciQ=",
                    "autograph": "12345678",
                    "X-Tingyun-Id": "kcoKoJaDT54;c=2;r=1827817616;u=7d8899b36fbae21bf19a2b99e96477fe::479CE70CA8C78408",
                    "Content-Type": "application/json;charset=utf-8",
                    "Content-Length": "46",
                    "Host": "apinews.haiwainet.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.11.0",
                }

                headers = {
                    "access_token": "",
                    "clientCode": "100002",
                    "secret": "ViEL1JR+FvKr8Vbo/Dq8v69VoigfFGZ5XgREL5ymi6TnWgGOT7Aw9P4my1vEcPWo6a0Vrgt97oif0QBVRMrSlGKQGQA6CWfcPoYARP8nNYjqrLtae/3qNKNRZP4Oam282VDcB5sCZbsPOJgYSCz9xAZLihERBCnel/mE7sE6ciQ=",
                    "autograph": "12345678",
                    "X-Tingyun-Id": "kcoKoJaDT54;c=2;r=779520492;u=e82fc801b03bad83cf964d032e709b93::199AD9E4FB7F6418",
                    "Content-Type": "application/json;charset=utf-8",
                    "Content-Length": "124",
                    "Host": "apinews.haiwainet.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.11.0",
                }

                channelJson_header = {
                    "advertCode": 1,
                    "size": 5,
                    "sourceType": "SUT02"
                }

                channelJson = {"latitude": 23.128668333333334,
                               "recommendCode": 1,
                               "deviceId": "008796760196586",
                               "action": 0,
                               "longitude": 113.36772,
                               "mediaId": ""}
                data = {}
                method = 'post'

                articlelist_param_banner = InitClass().articlelists_params_fields(url_banner,headers_banner,method,channelname,data=data,channeljson=channelJson_header,
                                                                                  banners=1,channelid=channelid,channeltype=channeltype)  # 添加banner请求数据体，或其他接口请求数据


                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                           channeljson=channelJson,channelid=channelid,channeltype=channeltype)

                #print("推荐 channelname=", channelname, "channelid=", channelid, "categoryid=", categoryid)
                articleparams.append(articlelist_param_banner)
                articleparams.append(articlelist_param)
                continue

            #其余频道请求列表url
            url = "https://apinews.haiwainet.cn/search/every/contentSearch"
            headers = {
                "access_token": "",
                "clientCode": "100002",
                "secret": "ViEL1JR+FvKr8Vbo/Dq8v69VoigfFGZ5XgREL5ymi6TnWgGOT7Aw9P4my1vEcPWo6a0Vrgt97oif0QBVRMrSlGKQGQA6CWfcPoYARP8nNYjqrLtae/3qNKNRZP4Oam282VDcB5sCZbsPOJgYSCz9xAZLihERBCnel/mE7sE6ciQ=",
                "autograph": "12345678",
                "X-Tingyun-Id": "kcoKoJaDT54;c=2;r=1817191217;u=6c79ee1c0d4e8359a005b5c861eb82df::E7E953FDAB3E25E3",
                "Content-Type": "application/json;charset=utf-8",
                "Content-Length": "372",
                "Host": "apinews.haiwainet.cn",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.11.0",

            }
            data = {}
            if channelname == "专题":
                channelJson = {
                    "size": 10,
                    "contentCollectReturnSwitch": "true",
                    "contentType": "CT005",
                    "replyReturnSwitch": "true",
                    "channelId": channelid,
                    "filterBlackSwitch": "true",
                    "contentCountReturnSwitch": "true",
                    "productCode": categoryid,
                    "current": "1",
                    "mediaIsFollowReturnSwitch": "true",
                    "contentUpReturnSwitch": "true",
                    "mediaIsBlackReturnSwitch": "true",
                    "commentReturnSwitch": "true",
                    "sort": "releaseTime"
                }
            else:
                channelJson = {
                    "size": 10,
                    "contentCollectReturnSwitch": "true",
                    "contentType": "CT001,CT002,CT003,CT004,CT005,CT007,CT008",
                    "replyReturnSwitch": "true",
                    "channelId": channelid,
                    "filterBlackSwitch": "true",
                    "contentCountReturnSwitch": "true",
                    "productCode": categoryid,
                    "current": "1",
                    "mediaIsFollowReturnSwitch": "true",
                    "contentUpReturnSwitch": "true",
                    "mediaIsBlackReturnSwitch": "true",
                    "commentReturnSwitch": "true",
                    "sort": "createTime"
                }
            method = 'post'
            # print("其他 channelname=", channelname, "channelid=", channelid, "categoryid=", categoryid)
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data,channeljson=channelJson,channelid=channelid,channeltype=channeltype)
            articleparams.append(articlelist_param)
        yield articleparams

    @staticmethod
    def analyze_articlelists(articleslist_ress):
        articlesparams = []

        for articleslist_res in articleslist_ress:

            #print("articleslist_res==",articleslist_res)
            banners = articleslist_res.get("banner")
            channelname = articleslist_res.get("channelname")
            channelid = articleslist_res.get("channelid")
            channeltype = articleslist_res.get("channelType")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}

            try:
                articlelist_json = json.loads(articlelist_res)
                # print("articlelist_json==",articlelist_json)
                try:
                    articlelists = articlelist_json['data']
                    if channelname == "专题":
                        #专题新闻
                        # print("articlelists===",articlelists)
                        for topicinfo in articlelists:

                            covers = topicinfo["cover"]
                            title = topicinfo["title"]
                            summary = topicinfo["summary"]
                            shareurl = topicinfo["shareUrl"]
                            updatetime = topicinfo["updateTimeStamp"]
                            createtime = topicinfo["createTimeStamp"]
                            pubTime = topicinfo["releaseTimeStamp"]

                            # sharenum = topicinfo["shareCount"]
                            # topicinfo["viewCount"]
                            articleid = topicinfo["id"]

                            ish5 = "0"
                            try:
                                ish5 = topicinfo["isH5"]
                                # print("ish5==",ish5)
                            except Exception as e:
                                print("内部专题")


                            articleparam = InitClass().article_list_fields()

                            articleparam["articleid"] = articleid
                            articleparam["channelname"] = channelname
                            articleparam["channelid"] = channelid
                            articleparam["channeltype"] = channeltype
                            articleparam["covers"] = covers
                            articleparam["title"] = title
                            articleparam["summary"] = summary
                            articleparam["shareurl"] = shareurl
                            articleparam["updatetime"] = updatetime
                            articleparam["createtime"] = createtime
                            articleparam["pubTime"] = pubTime
                            articleparam["ish5"] = ish5

                            articlesparams.append(articleparam)


                    else:
                        #普通新闻
                        if banners == 1:
                            #banner
                            articlelists = articlelists["contentMaterialList"]
                            #print("articlelists==",articlelists)

                        for article in articlelists:
                            articleparam = InitClass().article_list_fields()

                            if banners == 1:
                                articleparam["banner"] = banners

                                try:
                                    #banner 用fileCode
                                    articleid = article['fileCode']
                                    articleparam["articleid"] = articleid
                                except Exception as e:
                                    print("e id", e)

                            else:
                                try:
                                    #普通新闻 用id
                                    articleid = article['id']
                                    articleparam["articleid"] = articleid
                                except Exception as e:
                                    print("e id", e)

                            try:
                                articletitle = article['title']
                                articleparam["articletitle"] = articletitle
                            except Exception as e:
                                print("e title =",e)



                            # try:
                            #     imageurl = article['cover']
                            #     articleparam["imageurl"] = imageurl
                            # except Exception as e:
                            #     #print(" e cover",e)
                            #
                            #     try:
                            #         imageurl = article['horizontal']
                            #         articleparam["imageurl"] = imageurl
                            #     except Exception as e:
                            #         print(" e cover", e)


                            articleparam["channelname"] = channelname
                            articleparam["channelid"] = channelid
                            articleparam["channeltype"] = channeltype
                            articlesparams.append(articleparam)

                except Exception as e:
                    print("Exception e",e)
            except Exception as e:
                print("Exception e111 = ",e)
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articlesparam = []
        #请求详情url
        url = 'https://apinews.haiwainet.cn/search/every/contentSearch'
        headers = {
            "access_token": "",
            "clientCode": "100002",
            "secret": "ViEL1JR+FvKr8Vbo/Dq8v69VoigfFGZ5XgREL5ymi6TnWgGOT7Aw9P4my1vEcPWo6a0Vrgt97oif0QBVRMrSlGKQGQA6CWfcPoYARP8nNYjqrLtae/3qNKNRZP4Oam282VDcB5sCZbsPOJgYSCz9xAZLihERBCnel/mE7sE6ciQ=",
            "autograph": "12345678",
            "X-Tingyun-Id": "kcoKoJaDT54;c=2;r=1950649457;u=7d8899b36fbae21bf19a2b99e96477fe::479CE70CA8C78408",
            "Content-Type": "application/json;charset=utf-8",
            "Content-Length": "349",
            "Host": "apinews.haiwainet.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.11.0",
        }

        method = 'post'
        for articleparam in articles:
            data = {}
            # print("articleid==",articleparam.get("articleid"))
            detailJson = {
                "word": "",
                 "size": "10",
                 "ids": articleparam.get("articleid"),
                 "contentCollectReturnSwitch": "true",
                 "contentType": "CT001,CT002,CT003,CT004,CT007,CT008",
                 "replyReturnSwitch": "true",
                 "breakingReturnSwitch": "true",
                 "contentCountReturnSwitch": "true",
                 "productCode": "PRD001",
                 "current": "1",
                 "mediaIsFollowReturnSwitch": "true",
                 "contentUpReturnSwitch": "true",
                 "mediaIsBlackReturnSwitch": "false",
                 "commentReturnSwitch": "true"
            }

            # channelname = articleparam.get("channelname")
            # imgurl = articleparam.get("imageurl")

            channelname = articleparam.get("channelname")
            channelid = articleparam.get("channelid")
            channeltype = articleparam.get("channeltype")

            banner = articleparam.get("banner")
            imgurl = articleparam.get("imageurl")
            videos = channelid #articleparam.get("videos")
            videocover = channeltype#articleparam.get("videocover")
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

            if channelname == "专题":
                covers = articleparam.get("covers")
                title = articleparam.get("title")
                summary = articleparam.get("summary")
                shareurl = articleparam.get("shareurl")
                updatetime = articleparam.get("updatetime")
                createtime = articleparam.get("createtime")
                pubtime = articleparam.get("pubTime")

                articleid = articleparam.get("articleid")
                ish5 = articleparam.get("ish5")

                readnum = articleid
                sharenum = ish5

                imgurl = covers
                author = title
                source = summary
                articleurl = shareurl



            # 若APP有关于时间的反爬加sleeptime = 1，若发送为json数据体，则添加articlejson = detailJson
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data, articlejson=detailJson,
                                                        videourl=videos, videocover=videocover, pubtime=pubtime,
                                                        createtime=createtime, updatetime=updatetime,
                                                        source=source, author=author, likenum=likenum,
                                                        commentnum=commentnum, sharenum=sharenum, readnum=readnum,
                                                        articleurl=articleurl, banners=banner)
            # article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
            #                                             articlejson=detailJson,banners=banner)

            articlesparam.append(article)
        yield articlesparam

    @staticmethod
    def analyzearticles(articles_res):
        for articleres in articles_res:
            channelname = articleres.get("channelname")
            channelid = articleres.get("videourl")
            channeltype = articleres.get("videocover")
            # imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            banners = articleres.get("banner")

            covers = []
            title = ""
            summary = ""
            shareurl = ""
            updatetime = 0
            createtime = 0
            pubtime = 0
            ish5 = "0"
            articleid = ""


            if channelname == "专题":
                covers = articleres.get("imageurl")
                title = articleres.get("author")
                summary = articleres.get("source")
                shareurl = articleres.get("articleurl")
                updatetime = articleres.get("updatetime")
                createtime = articleres.get("createtime")
                pubtime = articleres.get("pubtime")

                articleid = articleres.get("readnum")
                ish5 = articleres.get("sharenum")


            articleres = articleres.get("articleres")

            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent = 4, ensure_ascii = False))

                if channelname == "专题":
                    # covers = articleres.get("imgurl")
                    # title = articleres.get("author")
                    # summary = articleres.get("source")
                    # shareurl = articleres.get("articleurl")
                    # updatetime = articleres.get("updatetime")
                    # createtime = articleres.get("createtime")
                    # pubtime = articleres.get("pubTime")

                    topic_fields = InitClass().topic_fields()

                    topic_fields["platformName"] = appname
                    topic_fields["topicID"] = articleid
                    topic_fields["channelName"] = channelname
                    topic_fields["channelID"] = channelid
                    topic_fields["channelType"] = channeltype
                    topic_fields["topicUrl"] = shareurl
                    topic_fields["title"] = title
                    topic_fields["topicCover"] = covers
                    topic_fields["original"] = ""
                    topic_fields["pubTime"] = pubtime
                    topic_fields["topic"] = 1
                    topic_fields["banner"] = 0
                    topic_fields["updateTime"] = updatetime
                    topic_fields["createtime"] = createtime
                    topic_fields["digest"] = summary

                    if ish5 == "1":
                        print("外链大专题===", json.dumps(topic_fields, indent=4, ensure_ascii=False))
                    else:

                        topicurl = "https://apinews.haiwainet.cn/hk-service-special/6.0.0/special/client/every/detail"
                        topicdata = {
                            "size": 10,
                            "special_id": articleid
                        }
                        headers = {
                            "access_token": "",
                            "clientCode": "100002",
                            "secret": "ViEL1JR+FvKr8Vbo/Dq8v69VoigfFGZ5XgREL5ymi6TnWgGOT7Aw9P4my1vEcPWo6a0Vrgt97oif0QBVRMrSlGKQGQA6CWfcPoYARP8nNYjqrLtae/3qNKNRZP4Oam282VDcB5sCZbsPOJgYSCz9xAZLihERBCnel/mE7sE6ciQ=",
                            "autograph": "12345678",
                            "X-Tingyun-Id": "kcoKoJaDT54;c=2;r=1950649457;u=7d8899b36fbae21bf19a2b99e96477fe::479CE70CA8C78408",
                            "Content-Type": "application/json;charset=utf-8",
                            "Host": "apinews.haiwainet.cn",
                            "Connection": "Keep-Alive",
                            "Accept-Encoding": "gzip",
                            "User-Agent": "okhttp/3.11.0",
                        }

                        topicres = requests.get(topicurl,headers=headers,params=topicdata).text
                        topicjson = json.loads(json.dumps(json.loads(topicres, strict=False), indent=4, ensure_ascii=False))
                        subspeciallist = topicjson["data"]["subSpecialList"]


                        topicnum = 0
                        newestarticleid = ""
                        newestarticlepubtime = 0



                        for subtopic in subspeciallist:
                            infolist = subtopic["newsInfoList"]
                            topicnum += len(infolist)
                            for article in infolist:

                                a_commentnum = article["commentCount"]
                                a_author = article["author"]
                                a_content = article["content"]
                                a_createtime = article["createTimeStamp"]
                                a_pubtime = article["releaseTimeStamp"]

                                a_articletitle = article["title"]
                                a_updatetime = article["updateTimeStamp"]
                                a_covers = article["cover"]
                                if not a_covers:
                                    a_covers = []
                                a_articleid = article["id"]
                                a_shareurl = article["shareUrl"]

                                if int(a_pubtime) > newestarticlepubtime:
                                    newestarticlepubtime = int(a_pubtime)
                                    newestarticleid = a_articleid

                                article_fields = InitClass().article_fields()
                                article_fields["channelname"] = channelname
                                article_fields["channelID"] = channelid

                                article_fields["appname"] = appname
                                article_fields["banner"] = 0
                                article_fields["channelType"] = channeltype
                                article_fields["source"] = ""
                                article_fields["title"] = a_articletitle
                                article_fields["url"] = a_shareurl
                                article_fields["workerid"] = a_articleid
                                article_fields["content"] = a_content
                                article_fields["pubtime"] = a_pubtime
                                article_fields["createtime"] = a_createtime
                                article_fields["updatetime"] = a_updatetime
                                article_fields["readnum"] = 0
                                article_fields["author"] = a_author
                                article_fields["commentnum"] = a_commentnum
                                article_fields["articlecovers"] = a_covers
                                article_fields["videocover"] = []
                                article_fields["specialtopic"] = 1
                                article_fields["topicid"] = articleid
                                article_fields["topicTitle"] = title


                                try:
                                    videos = InitClass().get_video(a_content)
                                    article_fields["videos"] = videos
                                except Exception as e:
                                    print("无视频")

                                try:
                                    images = InitClass().get_images(a_content)
                                    article_fields["images"] = images
                                except Exception as e:
                                    print("无图片")
                                print("专题内文章===", json.dumps(article_fields, indent=4, ensure_ascii=False))

                        topic_fields["articleNum"] = topicnum
                        topic_fields["newestArticleID"] = newestarticleid
                        print("内部大专题===", json.dumps(topic_fields, indent=4, ensure_ascii=False))


                else:
                    # 普通

                    fields = InitClass().article_fields()
                    fields["channelname"] = channelname
                    fields["channelID"] = channelid
                    # fields["imageurl"] = imgurl
                    fields["appname"] = appname
                    fields["banner"] = banners
                    fields["channelType"] = channeltype

                    print("articlejson==",articlejson)
                    data = articlejson['data'][0]
                    title = data['title'] # 标题
                    try:
                        source = data['origin']['mediaName']  # 来源
                        fields["source"] = source
                    except Exception as e:
                        print("source e =",e)

                    content = data['content']  # 文章内容
                    pubtime = data['releaseTimeStamp']  # 发布时间
                    createtime = data['createTimeStamp']  # 创建时间
                    updateTime = data['updateTimeStamp']  # 更新时间
                    viewNum = data['viewCount']  # 阅读数
                    author = data['author'] #作者
                    workerid = data['id'] #新闻id
                    url = data['shareUrl'] #分享url
                    cover = data['cover'] #封面图

                    fields["title"] = title
                    fields["url"] = url
                    fields["workerid"] = workerid

                    fields["content"] = content
                    fields["pubtime"] = pubtime
                    fields["createtime"] = createtime
                    fields["updatetime"] = updateTime
                    fields["readnum"] = viewNum
                    fields["author"] = author
                    fields["articlecovers"] = cover
                    fields["videocover"] = []
                    try:
                        video = data['video'][0]
                        print("video===",video)
                    #     fields["videos"] = video['url']  # 视频
                    #     fields["width"] = video['width']  # 视频宽
                    #     fields["height"] = video['height']  # 视频高
                    except Exception as e :
                        print("e video")

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
                    print("文章===",json.dumps(fields, indent = 4, ensure_ascii = False))
            except Exception as e:
                print("e data=",e)

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
    spider = Haikexinwen('海客新闻')
    spider.run()