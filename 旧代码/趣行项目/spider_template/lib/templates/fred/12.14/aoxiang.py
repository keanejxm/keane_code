# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
# from App.appspider_m import Appspider
# from App.initclass import InitClass

from App.spider_analy_model.jiu.appspider_m import Appspider
from App.spider_analy_model.jiu.initclass import InitClass

import requests
from lxml import html
from html.parser import HTMLParser

class Aoxiang(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "https://apiaoxiang.eastday.com/api/NavBar/List"
        # 频道请求头
        headers = {
            "Host": "apiaoxiang.eastday.com",
            "Content-Type": "application/json;charset=utf-8",
            "Accept": "*/*",
            "User-Agent": "ao xiang/6.0.3 (iPhone; iOS 12.0.1; Scale/2.00)",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "br, gzip, deflate",
            "Connection": "keep-alive",
        }
        # 频道数据体
        data = {
            "appId": "190511",
            "deviceId": "3bbef1bf4ee8d9115841c89b8051f5fb5a7de7c7",
            "version": "6.0.3"
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

        # channelname = "新时代"
        # url = "/api/news/TotalList"
        # channeltype = 3
        # channelid = 4
        # remarkid = ""
        # channelparam = InitClass().channel_fields(channelid, channelname,channeltype=channeltype,categoryid=url,categoryname=remarkid)
        # channelparams.append(channelparam)

        for channel in channelslists['list']:
            # channeltype == 8 十六区大频道内小频道
            remarkid = ""
            channeltype = channel['channelType']
            if channeltype == 8:
                #十六区内各分区id
                remarkid = channel['remarkId']

            channelid = channel['id']
            channelname = channel['title']
            #url是列表api地址
            url = channel['url']

            channelparam = InitClass().channel_fields(channelid, channelname,channeltype = channeltype,categoryid = url,categoryname = remarkid)
            channelparams.append(channelparam)

        zhengwuname = "政务"
        zhengwuid = "6b8403d763791161"
        channelparam = InitClass().channel_fields(zhengwuid, zhengwuname)
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
            channeltype = channel.get("channeltype")
            remarkid = channel.get("categoryname")
            channelname = channel.get("channelname")

            headers = {}
            data = {}
            method = ""
            channeljson = {}

            if channelname == "政务":
                url = "https://apiaoxiang.eastday.com/api/news/List"
                headers = {
                    "Host": "apiaoxiang.eastday.com",
                    "Content-Type": "application/json;charset=utf-8",
                    "Cookie": "eastdaywdcid=6b8403d763791161",
                    "Connection": "keep-alive",
                    "Accept": "*/*",
                    "User-Agent": "ao xiang/6.0.3 (iPhone; iOS 12.0.1; Scale/2.00)",
                    "Accept-Language": "zh-Hans-CN;q=1",
                    "Content-Length": "137",
                    "Accept-Encoding": "br, gzip, deflate"
                }
                channeljson = {
                    "appId": "190511",
                    "deviceId": "3bbef1bf4ee8d9115841c89b8051f5fb5a7de7c7",
                    "currentPage": 1,
                    "pageSize": 20,
                    "channelId": "14",
                    "version": "6.0.3"
                }

                method = "post"
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,channel_id = channelid,channeltype=channeltype, data=data,
                                                                           channeljson=channeljson)
                articleparams.append(articlelist_param)
                continue
            # channeltype = channel.get("channeltype")
            suburl = channel.get("categoryid")
            # 域名
            defaulturl = "https://apiaoxiang.eastday.com"
            url = defaulturl + suburl

            if suburl == '/api/Paradigm4/List':
                #推荐
                headers = {
                    "Host": "apiaoxiang.eastday.com",
                    "Content-Type": "application/json;charset=utf-8",
                    "Accept": "*/*",
                    "User-Agent": "ao xiang/6.0.3 (iPhone; iOS 12.0.1; Scale/2.00)",
                    "Accept-Language": "zh-Hans-CN;q=1",
                    "Accept-Encoding": "br, gzip, deflate",
                    "Connection": "keep-alive"
                }
                data = {
                    "appId": "190511",
                    "channelId": channelid,
                    "currentPage": "1",
                    "deviceId": "3bbef1bf4ee8d9115841c89b8051f5fb5a7de7c7",
                    "newsType": "0",
                    "pageSize": "20",
                    "userId": "0",
                    "version": "6.0.3"
                }
                method = "get"
                # continue
            elif suburl == "/api/news/LookShanghaiList":
                #看上海
                headers = {
                    "Host": "apiaoxiang.eastday.com",
                    "Content-Type": "application/json;charset=utf-8",
                    "Connection": "keep-alive",
                    "Accept": "*/*",
                    "User-Agent": "ao xiang/6.0.3 (iPhone; iOS 12.0.1; Scale/2.00)",
                    "Accept-Language": "zh-Hans-CN;q=1",
                    "Content-Length": "120",
                    "Accept-Encoding": "br, gzip, deflate",
                }
                channeljson = {
                    "appId": "190511",
                    "currentPage": 1,
                    "deviceId": "3bbef1bf4ee8d9115841c89b8051f5fb5a7de7c7",
                    "pageSize": 20,
                    "version": "6.0.3"
                }
                method = "post"
                # continue
            elif suburl == "/api/news/Portrait":
                #原创
                headers = {
                    "Host": "apiaoxiang.eastday.com",
                    "Content-Type": "application/json;charset=utf-8",
                    "Connection": "keep-alive",
                    "Accept": "*/*",
                    "User-Agent": "ao xiang/6.0.3 (iPhone; iOS 12.0.1; Scale/2.00)",
                    "Accept-Language": "zh-Hans-CN;q=1",
                    "Content-Length": "120",
                    "Accept-Encoding": "br, gzip, deflate",
                }
                channeljson = {
                    "appId": "190511",
                    "currentPage": 1,
                    "deviceId": "3bbef1bf4ee8d9115841c89b8051f5fb5a7de7c7",
                    "pageSize": 20,
                    "version": "6.0.3"
                }
                method = "post"
                # continue
            elif suburl == "/api/Special/SpecialNewsListByRemark":
                #十六区
                headers = {
                    "Host": "apiaoxiang.eastday.com",
                    "Content-Type": "application/json;charset=utf-8",
                    "Connection": "keep-alive",
                    "Accept": "*/*",
                    "User-Agent": "ao xiang/6.0.3 (iPhone; iOS 12.0.1; Scale/2.00)",
                    "Accept-Language": "zh-Hans-CN;q=1",
                    "Content-Length": "135",
                    "Accept-Encoding": "br, gzip, deflate",
                }
                channeljson = {
                    "appId": "190511",
                    "deviceId": "3bbef1bf4ee8d9115841c89b8051f5fb5a7de7c7",
                    "skipCount": 0,
                    "remarkIds": remarkid,
                    "limitCount": 20,
                    "version": "6.0.3"
                }
                method = "post"

                #区县id
                channelid = remarkid

            elif suburl == "/api/news/TotalList":
                headers = {
                    "Host": "apiaoxiang.eastday.com",
                    "Content-Type": "application/json;charset=utf-8",
                    "Connection": "keep-alive",
                    "Accept": "*/*",
                    "User-Agent": "ao xiang/6.0.3 (iPhone; iOS 12.0.1; Scale/2.00)",
                    "Accept-Language": "zh-Hans-CN;q=1",
                    "Content-Length": "136",
                    "Accept-Encoding": "br, gzip, deflate",
                }
                channeljson = {
                    "appId": "190511",
                    "deviceId": "3bbef1bf4ee8d9115841c89b8051f5fb5a7de7c7",
                    "currentPage": 1,
                    "pageSize": 20,
                    "channelId":channelid,
                    "version": "6.0.3"
                }
                method = "post"
                # continue
            elif suburl == "https://news.eastday.com/eastday/Special/xxfy/index.html":
                url = "https://apiaoxiang.eastday.com/api/Special/SpecialNewsList"
                headers = {
                    "Host": "apiaoxiang.eastday.com",
                    "Content-Type": "application/json",
                    "Origin": "https://news.eastday.com",
                    "Accept-Encoding": "br, gzip, deflate",
                    "Connection": "keep-alive",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A404/aoxiangapp_ios/https://apiaoxiang.eastday.com/config.json/version3",
                    "Referer": "https://news.eastday.com/eastday/Special/xxfy/index.html",
                    "Content-Length": "53",
                    "Accept-Language": "zh-cn"
                }
                channeljson = {
                    "specialId": "1052280",
                    "skipCount": 0,
                    "limitCount": 20
                }
                method = "post"
                # continue
            else:
                #https://news.eastday.com/eastday/Special/xxfy/index.html
                print("未知 url==",suburl)
                continue

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,channel_id = channelid,channeltype=channeltype, data = data,channeljson=channeljson)
            # 若数据体以json形式发送则以下面方式发送数据上面方式注释
            # articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data,channeljson = channeljson)
            # articleparams.append(articlelist_param_banner)
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
            #mark
            #channeltype = articleslist_res.get("channeltype")

            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                # 可在下面打印处打断点，查看请求到的数据
                # print("articlelist_json==",articlelist_json)
                #若banner图在articlelist_json中则分来开取并给其复制banner = 1
                try:
                    articlelists = articlelist_json['list']
                    for article in articlelists:
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        # print(article)
                        articleparam = InitClass().article_list_fields()
                        articletitle = article['title']
                        articleid = article['newsId']
                        contenturl = article['url']
                        workerid = article['urlId']
                        newstype = article['newsType']
                        styletype = article['styleType']
                        # print("articletitle==",articletitle,"newstype==",newstype,"styletype==",styletype)
                        if not contenturl:
                            print("contenturl 为空")

                        imgurls = article['imgUrls']
                        videos = article['videoUrl'] #一个地址
                        pubtime = article['time']
                        isouterurl = article['isOuterUrl']
                        height = article['videoImgHeight']
                        width = article['videoImgWidth']

                        # videos = article["videourl"] #在此处获取到文章视频url，避免在文章详情获取不到视频链接，数据类型list
                        # videocover = article["videocover"]#在此处获取到文章视频封面图，避免在文章详情获取不到视频封面图链接，数据类型list
                        # pubtime = article["pubtime"]#在此处获取到文章的发布时间，避免在文章详情获取不到发布时间
                        # createtime = article["createtime"]#在此处获取到文章的创建时间，避免在文章详情获取不创建时间
                        # updatetime = article["updatetime"]#在此处获取到文章的更新时间，避免在文章详情获取不到更新时间
                        source = article["infoSource"]#在此处获取到文章的来源，避免在文章详情获取不到来源
                        # author = article["author"]#在此处获取到文章的作者，避免在文章详情获取不到作者
                        # likenum = article["likenum"]#在此处获取到文章的点赞数，避免在文章详情获取不到点赞数
                        commentnum = article["replyCount"]#在此处获取到文章的评论数，避免在文章详情获取不到评论数
                        # sharenum = article["sharenum"]#在此处获取到文章的评论数，避免在文章详情获取不到评论数
                        # readnum = article["readnum"]#在此处获取到文章的阅读数，避免在文章详情获取不到阅读数
                        # articleurl = article["articleurl"]#在此处获取到文章html地址，避免在文章详情获取不到html地址
                        articleparam["video"] = videos #此步骤为存储视频url
                        # articleparam["videocover"] = videocover#此步骤为存储视频封面
                        articleparam["pubtime"] = pubtime#此步骤为存储发布时间
                        articleparam["createtime"] = 0#createtime#此步骤为存储创建时间
                        articleparam["updatetime"] = 0# updatetime#此步骤为存储更新时间
                        articleparam["source"] = source#此步骤为存储文章来源
                        # articleparam["author"] = author#此步骤为存储作者
                        # articleparam["likenum"] = likenum#此步骤为存储点赞数
                        articleparam["commentnum"] = commentnum#此步骤为存储评论数

                        articleparam["articleurl"] = contenturl
                        articleparam["imageurl"] = imgurls
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["channelname"] = channelname
                        articleparam["channelID"] = channelid
                        articleparam["banner"] = banners
                        articleparam["width"] = width
                        articleparam["height"] = height

                        content = ""
                        # print("isouterurl==",isouterurl)
                        fields = InitClass().article_fields()

                        if isouterurl == True:
                            #外部链接
                            specialid = contenturl.split("/")[-1]
                            # print("specialid==", specialid)
                            # print("article=",article)
                            # print("articleparam =",articleparam)
                            articleparam["specialid"] = specialid
                            articlesparams.append(articleparam)
                            continue
                        else:
                            #内部新闻
                            res = requests.get(contenturl)
                            tree = html.fromstring(res.text)

                            # contentType，作品类型，-1未知，1文字，2图文，3视频文，4纯长视频，5纯短视频，6画廊，7纯音频，8短消息（动态、微头条、微博消息等）
                            if newstype == 1 or newstype == 2:
                                # 文字
                                name = tree.xpath('//div[@class="detail"]')
                                fields["contentType"] = 1
                            elif newstype == 8:
                                # 画廊
                                name = tree.xpath('//div[@class="detailLists"]')
                                fields["contentType"] = 6
                            else:
                                name = tree.xpath('//div[@class="detail"]')
                                # print("article==",article)
                                fields["contentType"] = 1

                            try:
                                name1 = html.tostring(name[0])
                                content = HTMLParser().unescape(name1.decode())
                                # print("content ==",content)
                                # print("正文")
                            except Exception as e:
                                print("content e ===", e, article)
                                specialid = contenturl.split("/")[-1]
                                # print("specialid==", specialid)

                        fields["appname"] = "翱翔"
                        fields["channelname"] = channelname
                        fields["url"] = contenturl
                        fields["workerid"] = workerid
                        fields["title"] = articletitle
                        fields["content"] = content

                        try:
                            contentvideos = InitClass().get_video(content)
                            if not videos in contentvideos and videos:
                                contentvideos.append(videos)
                            fields["videos"] = contentvideos
                        except Exception as e:
                            print("正文无视频")

                        fields["articlecovers"] = imgurls

                        try:
                            images = InitClass().get_images(content)
                            fields["images"] = images
                        except Exception as e:
                            print("正文无图片")

                        fields["videocover"] = []
                        fields["width"] = width
                        fields["height"] = height
                        fields["source"] = source

                        fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                        fields["createtime"] = 0
                        fields["updatetime"] = 0
                        fields["likenum"] = 0
                        fields["playnum"] = 0
                        fields["commentnum"] = commentnum
                        fields["readnum"] = 0
                        fields["trannum"] = 0
                        fields["sharenum"] = 0
                        fields["author"] = ""
                        fields["banner"] = banners
                        fields["channelID"] = channelid
                        # print("采集结果")
                        print("采集结果==",json.dumps(fields, indent=4, ensure_ascii=False))
                        continue
                        # articlesparams.append(articleparam)
                except Exception as e:
                    print("e1====",e, articlelist_json)
            except Exception as e:
                print("e2====",e, articlelist_json)
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        """
        组建请求文章详情所需要的数据体
        :param articles:
        :return:
        """
        articlesparam = []

        url = ""
        headers = {}
        data = {}
        detailjson = {}

        for articleparam in articles:

            specialid = articleparam.get("specialid")
            articleurl = articleparam.get("articleurl")

            if specialid and articleurl:
                url = "https://apiaoxiang.eastday.com/api/Special/SpecialNewsList"
                method = 'post'
                detailjson = {
                    "specialId": specialid,
                    "skipCount": 0,
                    "limitCount": 20
                }
                headers = {
                    "Host": "apiaoxiang.eastday.com",
                    "Content-Type": "application/json",
                    "Origin": "https://n.eastday.com",
                    "Accept-Encoding": "br, gzip, deflate",
                    "Connection": "keep-alive",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A404/aoxiangapp_ios/https://apiaoxiang.eastday.com/config.json/version3",
                    "Referer": articleurl,
                    "Content-Length": "53",
                    "Accept-Language": "zh-cn"
                }
            else:
                print("articleparam")
                continue

            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
            banner = articleparam.get("banner")
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
            # articleurl = articleparam.get("articleurl")
            width = articleparam.get("width")
            height = articleparam.get("height")

            # 若APP有关于时间的反爬加sleeptime = 1，若发送为json数据体，则添加articlejson = articlejson
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data = data,articlejson=detailjson,
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
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            banners = articleres.get("banner")
            # 若上面存储了此字段需用下列方式获取
            videos = articleres.get("videos")
            videocover = articleres.get("videocover")
            pubtime = articleres.get("pubtime")
            # createtime = articleres.get("createtime")
            # updatetime = articleres.get("updatetime")
            source = articleres.get("source")
            likenum = articleres.get("likenum")
            commentnum = articleres.get("commentnum")
            sharenum = articleres.get("sharenum")
            readnum = articleres.get("readnum")

            # width = articleres.get("width")
            # height = articleres.get("height")

            articleurl = articleres.get("articleurl")
            # author = articleres.get("author")
            # articleurl = articleres.get("articleurl")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["articlecovers"] = imgurl
            fields["banner"] = banners
            # 如果有下列字段需添加
            fields["url"] = articleurl #文章的html网址，提取shareurl
            fields["workerid"] = articleurl #文章的id
            # fields["title"] = title #文章的标题
            # fields["content"] = content #文章的内容详情
            # fields["articlecovers"] = imgurl #文章的封面，一般为上面get到的字段


            fields["videocover"] = videocover #文章的视频封面地址
            fields["width"] = "" #文章的视频宽
            fields["height"] = "" #文章的视频高
            fields["source"] = source #文章的来源
            # fields["pubtime"] = pubtime #文章的发布时间
            fields["createtime"] = 0#createtime #文章的发布时间
            fields["updatetime"] = 0#updatetime #文章的更新时间
            fields["likenum"] = likenum #文章的点赞数
            # fields["playnum"] = playnum #视频的播放数
            fields["commentnum"] = commentnum #文章评论数
            fields["readnum"] = readnum #文章的阅读数
            # fields["trannum"] = trannum #文章的转发数
            fields["sharenum"] = sharenum #文章分享数
            # fields["author"] = author #文章作者
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent = 4, ensure_ascii = False))
                # print(articlejson)
                title = articlejson['title']  # 标题
                # source = articlejson['data']['origin']  # 来源
                content = articlejson['list'] # 文章内容
                # pubtime = articlejson['data']['date']  # 发布时间
                # workerid = articlejson['data']['id']
                # url = articlejson['data']["shareUrl"]
                # author = articlejson['data']["author"]
                # commentnum = articlejson['data']["comments"]
                fields["appname"] = appname
                fields["title"] = title

                # fields["workerid"] = workerid
                # fields["source"] = source
                fields["content"] = content

                try:
                    contentvideos = InitClass().get_video(content)
                    if not videos in contentvideos and videos:
                        contentvideos.append(videos)
                    fields["videos"] = contentvideos
                except Exception as e:
                    print("正文无视频")

                try:
                    images = InitClass().get_images(content)
                    fields["images"] = images
                except Exception as e:
                    print("正文无图片")

                # fields["author"] = author
                # fields["commentnum"] = commentnum
                fields["pubtime"] = InitClass().date_time_stamp(pubtime)

                # contentType，作品类型，-1未知，1文字，2图文，3视频文，4纯长视频，5纯短视频，6画廊，7纯音频，8短消息（动态、微头条、微博消息等）
                fields["contentType"] = 1

                # print("采集结果")
                print("专题==",json.dumps(fields, indent = 4, ensure_ascii = False))
            except Exception as e:
                print("eeeeee=",e)

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
    spider = Aoxiang('翱翔')
    spider.run()
