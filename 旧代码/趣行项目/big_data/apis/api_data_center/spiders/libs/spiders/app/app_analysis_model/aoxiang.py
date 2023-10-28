# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
# from App.appspider_m import Appspider
# from App.initclass import InitClass

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass

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
        headers = {
            "Host": "apiaoxiang.eastday.com",
            "Content-Type": "application/json;charset=utf-8",
            "Accept": "*/*",
            "User-Agent": "ao xiang/6.0.3 (iPhone; iOS 12.0.1; Scale/2.00)",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "br, gzip, deflate",
            "Connection": "keep-alive",
        }
        data = {
            "appId": "190511",
            "deviceId": "3bbef1bf4ee8d9115841c89b8051f5fb5a7de7c7",
            "version": "6.0.3"
        }
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
        # channelname = "新时代"
        # url = "/api/news/TotalList"
        # channeltype = 3
        # channelid = 4
        # remarkid = ""
        # channelparam = InitClass().channel_fields(channelid, channelname,channeltype=channeltype,categoryid=url,categoryname=remarkid)
        # channelparams.append(channelparam)
        for channel in channelslists['list']:
            remarkid = ""
            channeltype = channel['channelType']
            if channeltype == 8:
                remarkid = channel['remarkId']
            channelid = channel['id']
            channelname = channel['title']
            url = channel['url']
            channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channeltype, categoryid=url,
                                                      categoryname=remarkid)
            yield channelparam
        zhengwuname = "政务"
        zhengwuid = "6b8403d763791161"
        channelparam = InitClass().channel_fields(zhengwuid, zhengwuname)
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
            channeltype = channel.get("channeltype")
            remarkid = channel.get("categoryname")
            channelname = channel.get("channelname")
            data = {}
            channeljson = {}
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)

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
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           channel_index_id=channel_index_id,
                                                                           channeltype=channeltype, data=data,
                                                                           channeljson=channeljson)
                yield channel_field, [articlelist_param]
            suburl = channel.get("categoryid")
            defaulturl = "https://apiaoxiang.eastday.com"
            url = defaulturl + suburl
            if suburl == '/api/Paradigm4/List':
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
            elif suburl == "/api/news/LookShanghaiList":
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
            elif suburl == "/api/news/Portrait":
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
            elif suburl == "/api/Special/SpecialNewsListByRemark":
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
                    "channelId": channelid,
                    "version": "6.0.3"
                }
                method = "post"
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
                continue
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channel_index_id=channel_index_id,
                                                                       channeltype=channeltype,
                                                                       data=data, channeljson=channeljson)
            yield channel_field[articlelist_param]

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
            channel_index_id = articleslist_res.get("channelindexid")
            channelid = articleslist_res.get("channelID")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                try:
                    articlelists = articlelist_json['list']
                    for article in articlelists:
                        articleparam = InitClass().article_list_fields()
                        articletitle = article['title']
                        articleid = article['newsId']
                        contenturl = article['url']
                        workerid = article['urlId']
                        newstype = article['newsType']
                        styletype = article['styleType']
                        if not contenturl:
                            print("contenturl 为空")
                        imgurls = article['imgUrls']
                        videos = article['videoUrl']  # 一个地址
                        pubtime = article['time']
                        isouterurl = article['isOuterUrl']
                        height = article['videoImgHeight']
                        width = article['videoImgWidth']
                        source = article["infoSource"]  # 在此处获取到文章的来源，避免在文章详情获取不到来源
                        commentnum = article["replyCount"]  # 在此处获取到文章的评论数，避免在文章详情获取不到评论数
                        articleparam["video"] = videos  # 此步骤为存储视频url
                        articleparam["pubtime"] = pubtime  # 此步骤为存储发布时间
                        articleparam["createtime"] = 0  # createtime#此步骤为存储创建时间
                        articleparam["updatetime"] = 0  # updatetime#此步骤为存储更新时间
                        articleparam["source"] = source  # 此步骤为存储文章来源
                        articleparam["commentnum"] = commentnum  # 此步骤为存储评论数
                        articleparam["articleurl"] = contenturl
                        articleparam["imageurl"] = imgurls
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["channelname"] = channelname
                        articleparam["channelindexid"] = channel_index_id
                        articleparam["channelID"] = channelid
                        articleparam["banner"] = banners
                        articleparam["width"] = width
                        articleparam["height"] = height

                        content = ""
                        fields = InitClass().article_fields()
                        if isouterurl == True:
                            specialid = contenturl.split("/")[-1]
                            articleparam["specialid"] = specialid
                            yield articleparam
                        else:
                            res = requests.get(contenturl)
                            tree = html.fromstring(res.text)
                            if newstype == 1 or newstype == 2:
                                name = tree.xpath('//div[@class="detail"]')
                                fields["contentType"] = 1
                            elif newstype == 8:
                                name = tree.xpath('//div[@class="detailLists"]')
                                fields["contentType"] = 6
                            else:
                                name = tree.xpath('//div[@class="detail"]')
                                fields["contentType"] = 1

                            try:
                                name1 = html.tostring(name[0])
                                content = HTMLParser().unescape(name1.decode())
                            except Exception as e:
                                print("content e ===", e, article)
                                specialid = contenturl.split("/")[-1]
                        fields["channelname"] = channelname
                        fields["channelindexid"] = channel_index_id
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
                        yield fields
                except Exception as e:
                    print("e1====", e, articlelist_json)
            except Exception as e:
                print("e2====", e, articlelist_json)

    def getarticleparams(self,articleslist_ress):
        """
        组建请求文章详情所需要的数据体
        :param articles:
        :return:
        """
        url = ""
        headers = {}
        data = {}
        detailjson = {}
        method = 'post'
        for articleparam in self.analyze_articlelists(articleslist_ress):
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
            channelname = articleparam.get("channelname")
            channel_index_id = articleparam.get("channelindexid")
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
            # 若APP有关于时间的反爬加sleeptime = 1，若发送为json数据体，则添加articlejson = articlejson
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                        articlejson=detailjson,channel_index_id=channel_index_id,
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
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            banners = articleres.get("banner")
            videos = articleres.get("videos")
            videocover = articleres.get("videocover")
            pubtime = articleres.get("pubtime")
            source = articleres.get("source")
            likenum = articleres.get("likenum")
            commentnum = articleres.get("commentnum")
            sharenum = articleres.get("sharenum")
            readnum = articleres.get("readnum")
            articleurl = articleres.get("articleurl")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["appname"] = self.newsname
            fields["platformID"] = self.platform_id
            fields["channelname"] = channelname
            fields["channelindexid"] = channel_index_id
            fields["articlecovers"] = imgurl
            fields["banner"] = banners
            fields["url"] = articleurl  # 文章的html网址，提取shareurl
            fields["workerid"] = articleurl  # 文章的id
            fields["videocover"] = videocover  # 文章的视频封面地址
            fields["width"] = ""  # 文章的视频宽
            fields["height"] = ""  # 文章的视频高
            fields["source"] = source  # 文章的来源
            fields["createtime"] = 0  # createtime #文章的发布时间
            fields["updatetime"] = 0  # updatetime #文章的更新时间
            fields["likenum"] = likenum  # 文章的点赞数
            fields["commentnum"] = commentnum  # 文章评论数
            fields["readnum"] = readnum  # 文章的阅读数
            fields["sharenum"] = sharenum  # 文章分享数
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                title = articlejson['title']  # 标题
                content = articlejson['list']  # 文章内容
                fields["appname"] = appname
                fields["title"] = title
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
                fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                fields["contentType"] = 1
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print("eeeeee=", e)

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Aoxiang(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
