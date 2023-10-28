# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
import requests
from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


class Xinhuaribaocaijing(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "http://116.62.167.116/article/getNavChannel.htm"
        # 频道请求头
        headers = {
            "Host": "116.62.167.116",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.9.1",
            "device": "app",
            "X-Requested-With": "XMLHttpRequest",
            "deviceid": "71179c812e3cc1f2",
            "token": "",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
        # 频道数据体
        data = {}
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
        # print("channelslists==",channelslists)
        channelparams = []

        ttid = "0"
        ttname = "头条"
        ttparam = InitClass().channel_fields(ttid, ttname)
        channelparams.append(ttparam)

        ##视频详情需要登录
        # spid = "0"
        # spname = "视频"
        # spparam = InitClass().channel_fields(spid, spname)
        # channelparams.append(spparam)

        for channel in channelslists['data']:
            channelid = channel['id']
            channelname = channel['name']
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

            if channelname == "头条":
                url_banner ="http://116.62.167.116/article/getIdxBanner.htm"
                headers_banner = {
                    "Host": "116.62.167.116",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.9.1",
                    "device": "app",
                    "X-Requested-With": "XMLHttpRequest",
                    "deviceid": "71179c812e3cc1f2",
                    "token": "",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                }

                url_zhuanti = "http://116.62.167.116/article/getSpecialChannelList.htm"
                headers_zhuanti = {
                    "Host": "116.62.167.116",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.9.1",
                    "device": "app",
                    "X-Requested-With": "XMLHttpRequest",
                    "deviceid": "71179c812e3cc1f2",
                    "token": "",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive"
                }

                data_zhuanti = {}

                # toutiao列表
                url = "http://116.62.167.116/article/getIdxRecommendArticles.htm"
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Content-Length": "14",
                    "Host": "116.62.167.116",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.9.1",
                    "device": "app",
                    "X-Requested-With": "XMLHttpRequest",
                    "deviceid": "71179c812e3cc1f2",
                    "token": "",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive"
                }

                data = {
                    "page":"1",
                    "rows":"10"
                }

                method = 'get'
                methodpost = 'post'

                articlelist_param_banner = InitClass().articlelists_params_fields(url_banner,
                                                                                  headers_banner,
                                                                                  method,
                                                                                  channelname,
                                                                                  banners=1,channelid=channelid)  # 添加banner请求数据体，或其他接口请求数据

                articlelist_param_list = InitClass().articlelists_params_fields(url,
                                                                                headers,
                                                                                methodpost,
                                                                                channelname,
                                                                                data=data,channelid=channelid)

                articlelist_param_zhuanti = InitClass().articlelists_params_fields(url_zhuanti,
                                                                                   headers_zhuanti,
                                                                                   method,
                                                                                   channelname,
                                                                                   data=data_zhuanti,channelid=channelid)

                # 若数据体以json形式发送则以下面方式发送数据上面方式注释
                #articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data,channeljson = channeljson)
                articleparams.append(articlelist_param_banner)
                articleparams.append(articlelist_param_zhuanti)
                articleparams.append(articlelist_param_list)

            elif channelname == "视频":
                url = "http://116.62.167.116/live/getLivePageList.htm"
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Content-Length": "14",
                    "Host": "116.62.167.116",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.9.1",
                    "device": "app",
                    "X-Requested-With": "XMLHttpRequest",
                    "deviceid": "71179c812e3cc1f2",
                    "token": "",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive"
                }
                data = {
                    "page":"1",
                    "rows": "10"
                }
                method = 'post'
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,channelid=channelid)
                articleparams.append(articlelist_param)

            else:
                # 若有两个请求接口则如下： 例如：banner列表和文章列表时两个请求接口
                url_banner = "http://116.62.167.116/article/getChannelCoverArticles.htm"  # banner请求接口
                url = "http://116.62.167.116/article/getArticlePage.htm"
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Content-Length": "26",
                    "Host": "116.62.167.116",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.9.1",
                    "device": "app",
                    "X-Requested-With": "XMLHttpRequest",
                    "deviceid": "71179c812e3cc1f2",
                    "token": "",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                }
                data = {
                    "channelid": channelid,
                    "rows": "10",
                    "page": "1"
                }
                method = 'post'
                data_banner = {
                    'channelid': channelid,
                }

                articlelist_param_banner = InitClass().articlelists_params_fields(url_banner, headers, method,
                                                                                  channelname,
                                                                                  data=data_banner,
                                                                                  banners=1,channelid=channelid)  # 添加banner请求数据体，或其他接口请求数据
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,channelid=channelid)
                # 若数据体以json形式发送则以下面方式发送数据上面方式注释
                # articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data,channeljson = channeljson)
                articleparams.append(articlelist_param_banner)
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
            channelid = articleslist_res.get("channelid")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            #print("articlelist_res==",articlelist_res)
            try:
                articlelist_json = json.loads(articlelist_res)
                # 可在下面打印处打断点，查看请求到的数据
                # print("articlelist_json"==articlelist_json)
                #若banner图在articlelist_json中则分来开取并给其复制banner = 1
                try:
                    if banners == 1:
                        # 专题和banner 返回结果格式一样
                        articlelists = articlelist_json['data']
                    else:
                        try:
                            articlelists = articlelist_json['data']['list']
                        except Exception as e:
                            articlelists = articlelist_json['data']
                    for article in articlelists:
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        # print('article==',article)
                        articleparam = InitClass().article_list_fields()

                        articleid = article['id']

                        # special\grasp\normal
                        type = "normal"
                        try:
                            type = article['type']
                            articleparam["articletype"] = type
                        except Exception as e:
                            print(e)
                        if type == "special":
                            articletitle = article['name']
                            imageurl = article["preimgpath"]
                            channelname = "专题"  # 传递参数，详情解析时使用
                        else:
                            articletitle = article['title']

                            imageurl = ""
                            try:
                                imageurl = article["titleimgpath"]
                            except Exception as e:
                                print("")

                            try:
                                imageurl = article["preimgpath"]
                            except Exception as e:
                                print("")


                            if not imageurl :
                                try:
                                    imageurl = article["preimglist"][0]
                                except Exception as e:
                                    print("eee",e)

                            pubtime = article["publishdate"]
                            source = article["source"]
                            author = article["publisher"]

                            articleparam["pubtime"] = pubtime
                            articleparam["source"] = source
                            articleparam["author"] = author


                        articleparam["imageurl"] = imageurl
                        articleparam["articletitle"] = articletitle
                        articleparam["articleid"] = articleid
                        articleparam["channelname"] = channelname
                        articleparam["channelid"] = channelid

                        articleparam["banner"] = banners
                        articlesparams.append(articleparam)
                except Exception as e:
                    print('e111==',e, articlelist_json)
            except Exception as e:
                print('e22222==',e, articlelist_json)
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        """
        组建请求文章详情所需要的数据体
        :param articles:
        :return:
        """
        articlesparam = []
        method = 'post'
        for articleparam in articles:

            articletype = articleparam.get("articletype")

            if articletype == 'special':
                articleid = articleparam.get("articleid")
                articletitle = articleparam.get("articletitle")

                #专题
                url = "http://116.62.167.116/article/getArticlePage.htm"
                data = {
                    "page":"1",
                    "channelid": articleid,
                    "rows": "10"
                }
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Content-Length": "28",
                    "Host": "116.62.167.116",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.9.1",
                    "device": "app",
                    "X-Requested-With": "XMLHttpRequest",
                    "deviceid": "71179c812e3cc1f2",
                    "token": "",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                }

                url_banner = "http://116.62.167.116/article/getChannelCoverArticles.htm"
                data_banner = {
                    "channelid": articleid,
                }
                headers_banner = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Content-Length": "12",
                    "Host": "116.62.167.116",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.9.1",
                    "device": "app",
                    "X-Requested-With": "XMLHttpRequest",
                    "deviceid": "71179c812e3cc1f2",
                    "token": "",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive"
                }

                # 此处代码不需要改动
                channelname = articleparam.get("channelname")
                channelid = articleparam.get("channelid")

                banner = articleparam.get("banner")
                imgurl = articleparam.get("imageurl")
                videos = channelid #articleparam.get("videos")
                videocover = articletitle #articleparam.get("videocover")
                pubtime = articleparam.get("pubtime")
                createtime = articleparam.get("createtime")
                updatetime = articleparam.get("updatetime")
                source = articleparam.get("source")
                author = articleparam.get("author")
                likenum = articleparam.get("likenum")
                commentnum = articleparam.get("commentnum")
                sharenum = articleparam.get("sharenum")
                readnum = articleparam.get("readnum")
                articleurl = articleid #articleparam.get("articleurl")
                # 若APP有关于时间的反爬加sleeptime = 1，若发送为json数据体，则添加articlejson = articlejson
                article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                            videourl=videos, videocover=videocover, pubtime=pubtime,
                                                            createtime=createtime, updatetime=updatetime,
                                                            source=source, author=author, likenum=likenum,
                                                            commentnum=commentnum, sharenum=sharenum, readnum=readnum,
                                                            articleurl=articleurl, banners=banner)

                article_banner = InitClass().article_params_fields(url_banner, headers_banner, method, channelname, imgurl, data=data_banner,
                                                            videourl=videos, videocover=videocover, pubtime=pubtime,
                                                            createtime=createtime, updatetime=updatetime,
                                                            source=source, author=author, likenum=likenum,
                                                            commentnum=commentnum, sharenum=sharenum, readnum=readnum,
                                                            articleurl=articleurl, banners=1)

                articlesparam.append(article)
                articlesparam.append(article_banner)

            else:
                url = 'http://116.62.167.116/article/articleDetail.htm'
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Content-Length": "13",
                    "Host": "116.62.167.116",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.9.1",
                    "device": "app",
                    "X-Requested-With": "XMLHttpRequest",
                    "deviceid": "71179c812e3cc1f2",
                    "token": "",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                }

                data = {
                    'id': articleparam.get("articleid"),
                }

                # 此处代码不需要改动
                channelname = articleparam.get("channelname")
                channelid = articleparam.get("channelid")

                banner = articleparam.get("banner")
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
                articleurl = url#articleparam.get("articleurl")
                # 若APP有关于时间的反爬加sleeptime = 1，若发送为json数据体，则添加articlejson = articlejson
                article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data = data,
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
            channelid = articleres.get("videourl")
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            banners = articleres.get("banner")
            source = articleres.get("source")
            articleurl = articleres.get("articleurl")
            origianlvideocover = articleres.get("videocover")

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
            # articleurl = articleres.get("articleurl")
            articleres = articleres.get("articleres")


            # 如果有下列字段需添加
            # fields["url"] = articleurl #文章的html网址，提取shareurl
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
                if channelname == "专题":

                    topic_fields = InitClass().topic_fields()

                    topicid = articleurl
                    topictitle = origianlvideocover

                    topic_fields["channelName"]= channelname
                    topic_fields["channelID"]= channelid
                    topic_fields["platformName"] = appname
                    topic_fields["title"] = topictitle
                    topic_fields["topicID"] = topicid
                    topic_fields["updateTime"] = 0
                    topic_fields["createTime"] = 0
                    topic_fields["pubTime"] = 0

                    if imgurl:
                        topic_fields["topicCover"] = [imgurl]

                    print("articlejson==",articlejson)

                    content = []
                    if banners == 1:
                        #专题banner，title等信息没传过来
                        content = articlejson['data']
                    else:
                        content = articlejson['data']['list']

                    if len(content) == 0:
                        print("专题banner无数据")
                        continue

                    topicnum = len(content)
                    topic_fields["articleNum"] = topicnum
                    newestarticleid = ""
                    newestarticlepubtime = 0

                    #专题内新闻
                    for articleitem in content:

                        apubtime = articleitem["publishdate"]
                        aauthor = articleitem["publisher"]
                        aid = articleitem["id"]

                        if apubtime > newestarticlepubtime:
                            newestarticlepubtime = apubtime
                            newestarticleid = aid

                        atitle =articleitem["title"]
                        asource = articleitem["source"]
                        acovers = articleitem["preimglist"]

                        article_fields = InitClass().article_fields()
                        article_fields["appname"] = appname
                        article_fields["channelname"] = channelname
                        article_fields["channelID"] = channelid
                        article_fields["channelType"] = ""
                        article_fields["workerid"] = aid
                        article_fields["title"] = atitle
                        article_fields["articlecovers"] = acovers
                        article_fields["source"] = asource
                        article_fields["pubtime"] = apubtime
                        article_fields["author"] = aauthor
                        article_fields["banner"] = banners

                        #请求详情
                        detailurl = 'http://116.62.167.116/article/articleDetail.htm'
                        detailheaders = {
                            "Content-Type": "application/x-www-form-urlencoded",
                            "Content-Length": "13",
                            "Host": "116.62.167.116",
                            "Accept-Encoding": "gzip",
                            "User-Agent": "okhttp/3.9.1",
                            "device": "app",
                            "X-Requested-With": "XMLHttpRequest",
                            "deviceid": "71179c812e3cc1f2",
                            "token": "",
                            "Cache-Control": "no-cache",
                            "Connection": "keep-alive",
                        }

                        detaildata = {
                            'id': aid,
                        }
                        detailres = requests.post(detailurl,headers=detailheaders,data=detaildata).text
                        detailjson = json.loads(detailres)

                        detailcontent = detailjson["data"]["content"]
                        detailcom = detailjson["data"]["commentNum"]

                        article_fields["content"] = detailcontent
                        article_fields["videocover"] = []
                        article_fields["url"] = detailurl
                        try:
                            videos = InitClass().get_video(detailcontent)
                            article_fields["videos"] = videos
                        except Exception as e:
                            print("无视频")

                        try:
                            images = InitClass().get_images(detailcontent)
                            article_fields["images"] = images
                        except Exception as e:
                            print("无图片")

                        article_fields["specialtopic"] = 1
                        article_fields["topicid"] = topicid
                        article_fields["topicTitle"] = topictitle
                        article_fields["commentnum"] = detailcom

                        article_fields["createtime"] = 0
                        article_fields["updatetime"] = 0

                        print("专题内文章===", json.dumps(article_fields, indent=4, ensure_ascii=False))
                    topic_fields["newestArticleID"] = newestarticleid
                    print("大专题===", json.dumps(topic_fields, indent=4, ensure_ascii=False))

                else:

                    fields = InitClass().article_fields()
                    fields["channelname"] = channelname
                    fields["channelID"] = channelid
                    # fields["imageurl"] = imgurl
                    fields["banner"] = banners
                    print("articlejson==",articlejson)
                    article = articlejson['data']
                    if "list" in article.keys():
                        content = articlejson['data']['list']
                        fields["content"] = content
                        continue
                    title = articlejson['data']['title']  # 标题
                    # source = articlejson['data']['origin']  # 来源
                    content = articlejson['data']['content']  # 文章内容
                    pubtime = articlejson['data']['publishdate']  # 发布时间
                    workerid = articlejson['data']['id']
                    # url = articlejson['data']["shareUrl"]
                    author = articlejson['data']["author"]
                    # commentnum = articlejson['data']["comments"]
                    try:
                        contentchannelid = articlejson['data']["channelid"]
                        contentchannelname = articlejson['data']["channelname"]

                        fields["channelID"] = contentchannelid
                        fields["channelname"] = contentchannelname

                    except Exception as e:
                        print("详情无channelid")

                    if imgurl:
                        fields["articlecovers"] = [imgurl]

                    fields["appname"] = appname
                    fields["title"] = title
                    fields["url"] = articleurl
                    fields["workerid"] = workerid
                    # fields["source"] = source
                    fields["content"] = content
                    fields["author"] = author
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

                    fields["createtime"] = 0
                    fields["updatetime"] = 0

                    if source:
                        fields["source"] = source

                    fields["pubtime"] = pubtime  # InitClass().date_time_stamp(pubtime)
                    print("文章===",json.dumps(fields, indent = 4, ensure_ascii = False))
            except Exception as e:
                print("解析文章e==",e)

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
    spider = Xinhuaribaocaijing('新华日报财经')
    spider.run()
