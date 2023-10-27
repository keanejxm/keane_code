# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
import re

# from App.appspider_m import Appspider
# from App.initclass import InitClass
from App.spider_analy_model.jiu.appspider_m import Appspider
from App.spider_analy_model.jiu.initclass import InitClass

class Jingjicankaobao(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "https://h5.newaircloud.com/api/getColumns?sid=jjckb&cid=15179"
        # 频道请求头
        headers = {
            "Host": "h5.newaircloud.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.1",
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
        print(channelslists)
        channelparams = []

        channelid = 35416
        channelname = "民族品牌"
        topcount = 1
        channelparam = InitClass().channel_fields(channelid, channelname, channeltype=topcount)
        channelparams.append(channelparam)

        # for channel in channelslists['columns']:
        #    if not channel['isHide']:
        #        channelid = channel['columnID']
        #        channelname = channel['columnName']
        #        #channeltype 传递各频道列表 banner个数
        #        topcount = channel['topCount']
        #        channelparam = InitClass().channel_fields(channelid, channelname,channeltype=topcount)
        #        channelparams.append(channelparam)

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
            bannercount = channel.get("channeltype")
            #print("channelname==",channelname,"bannercount==",bannercount)

            url = "https://h5.newaircloud.com/api/getArticles"
            headers = {
                "Content-Type": "application/json;charset=UTF-8",
                "Host": "h5.newaircloud.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.8.1"

            }
            data = {
                "sid": "jjckb",
                "cid": channelid,
                "lastFileID": "0",
                "rowNumber": "0"
            }
            method = 'get'
            # data_banner = {
            #     'orderBy': '4',
            #     'channelIds': channelid,
            #     'count': '4',
            #     'typeIds': '5',
            # }
            # articlelist_param_banner = InitClass().articlelists_params_fields(url_banner, headers, method, channelname,
            #                                                                   data = data_banner,
            #                                                                   banners = 1)  # 添加banner请求数据体，或其他接口请求数据
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,channel_id=channelid, data = data,banners=bannercount)
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
            articlelist_res = articleslist_res.get("channelres")

            index = 0
            isbanner = 0
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                # 可在下面打印处打断点，查看请求到的数据
                # print("articlelist_json===",articlelist_json)
                #若banner图在articlelist_json中则分来开取并给其复制banner = 1
                try:
                    articlelists = articlelist_json['list']
                    for article in articlelists:
                        print("article== ",article)
                        if banners - index > 0 :
                            isbanner = 1
                        else:
                            isbanner = 0
                        index += 1

                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        articleparam = InitClass().article_list_fields()
                        articletitle = article['title']
                        articletype = article['articleType']
                        articleparam["articletype"] = articletype
                        articleurl = article['contentUrl']

                        if articletype == 6:
                            #直播
                            articleid = article['linkID']
                            fileid = article['fileID']

                            articleparam["fileid"] = fileid
                        elif articletype == 4:
                            #h5页

                            content = article['contentUrl']
                            title = article['title']
                            workerid = article['fileID']
                            author = article['editor']
                            pubtime = article['publishTime']
                            source = article['source']
                            readnum = article['countClick']
                            likenum = article['countPraise']
                            sharenum = article['countShare']
                            imgurl = article['pic1']

                            fields = InitClass().article_fields()
                            fields["channelname"] = channelname
                            fields["channelID"] = channelid
                            if imgurl:
                                fields["articlecovers"] = [imgurl]
                            else:
                                fields["articlecovers"] = []

                            fields["banner"] = isbanner

                            #contentType，作品类型，-1未知，1文字，2图文，3视频文，4纯长视频，5纯短视频，6画廊，7纯音频，8短消息（动态、微头条、微博消息等）
                            fields["contentType"] = -1
                            fields["readnum"] = readnum
                            fields["likenum"] = likenum
                            fields["likenum"] = sharenum

                            fields["appname"] = "经济参考报"
                            fields["title"] = title

                            fields["workerid"] = workerid
                            fields["source"] = source
                            fields["content"] = content
                            fields["url"] = content
                            fields["author"] = author
                            # fields["commentnum"] = commentnum
                            fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                            fields["createtime"] = 0
                            fields["updatetime"] = 0
                            fields["images"] = []
                            fields["videos"] = []
                            fields["videocover"] = []

                            print("h5结果==", json.dumps(fields, indent=4, ensure_ascii=False))
                            print("")
                            continue

                        else:
                            articleid = article['contentUrl']

                        # videos = article["videourl"] #在此处获取到文章视频url，避免在文章详情获取不到视频链接，数据类型list
                        # videocover = article["videocover"]#在此处获取到文章视频封面图，避免在文章详情获取不到视频封面图链接，数据类型list
                        # pubtime = article["realPublishTime"]#在此处获取到文章的发布时间，避免在文章详情获取不到发布时间
                        # createtime = article["createtime"]#在此处获取到文章的创建时间，避免在文章详情获取不创建时间
                        # updatetime = article["updatetime"]#在此处获取到文章的更新时间，避免在文章详情获取不到更新时间
                        source = article["source"]#在此处获取到文章的来源，避免在文章详情获取不到来源
                        author = article["author"]#在此处获取到文章的作者，避免在文章详情获取不到作者
                        likenum = article["countPraise"]#在此处获取到文章的点赞数，避免在文章详情获取不到点赞数
                        # commentnum = article["commentnum"]#在此处获取到文章的评论数，避免在文章详情获取不到评论数
                        sharenum = article["countShare"]#在此处获取到文章的评论数，避免在文章详情获取不到评论数
                        readnum = article["countClick"]#在此处获取到文章的阅读数，避免在文章详情获取不到阅读数
                        # articleurl = article["articleurl"]#在此处获取到文章html地址，避免在文章详情获取不到html地址
                        # articleparam["video"] = videos #此步骤为存储视频url
                        # articleparam["videocover"] = videocover#此步骤为存储视频封面
                        # articleparam["pubtime"] = pubtime#此步骤为存储发布时间
                        # articleparam["createtime"] = createtime#此步骤为存储创建时间
                        # articleparam["updatetime"] = updatetime#此步骤为存储更新时间
                        articleparam["source"] = source#此步骤为存储文章来源
                        # articleparam["author"] = author#此步骤为存储作者
                        articleparam["likenum"] = likenum#此步骤为存储点赞数
                        # articleparam["commentnum"] = commentnum#此步骤为存储评论数
                        try:
                            articleparam["imageurl"] = article['pic1']
                        except Exception as e:
                            try:
                                articleparam["imageurl"] = article['pic2']
                            except Exception as e:
                                try:
                                    articleparam["imageurl"] = article['pic3']
                                except Exception as e:
                                    print("图片无")
                        articleparam["articleurl"] = articleurl
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["channelname"] = channelname
                        articleparam["channelID"] = channelid

                        articleparam["banner"] = isbanner

                        articlesparams.append(articleparam)
                except Exception as e:
                    print(e, articlelist_json)
            except Exception as e:
                print(e, articlelist_json)
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        """
        组建请求文章详情所需要的数据体
        :param articles:
        :return:
        """
        articlesparam = []

        method = 'get'
        for articleparam in articles:
            articletype = articleparam.get("articletype")
            #contentType，作品类型，-1未知，1文字，2图文，3视频文，4纯长视频，5纯短视频，6画廊，7纯音频，8短消息（动态、微头条、微博消息等）
            # 0 普通新闻
            # 4 h5页
            # 6 直播

            if articletype == 6:
                #6 直播
                articleid = articleparam.get("articleid")
                fileid = articleparam.get("fileid")
                headers = {
                    "Host": "h5.newaircloud.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.8.1"
                }
                url = "https://h5.newaircloud.com/api/getLiveList"
                data = {

                    "sid": "jjckb",
                    "id": articleid,
                    "lastFileID": "0",
                    "rowNumber": "0",
                    "aid": fileid,
                    "isAsc": "0"
                }


            elif articletype == 4:
                continue
            else:

                headers = {
                    "authority": "jjckboss.newaircloud.com",
                    "scheme": "https",
                    "accept-encoding": "gzip",
                    "user-agent": "okhttp/3.8.1"
                }
                url = articleparam.get("articleid")
                data = {}

            #通过videos 传递url
            videos = url

            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
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
            article = InitClass().article_params_fields(url, headers, method, channelname,channel_id=channelid, imageurl= imgurl, sleeptime=1,data = data,
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

            if imgurl:
                fields["articlecovers"] = [imgurl]
            else:
                fields["articlecovers"] = []

            fields["banner"] = banners
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
                # print("articleres==",articleres)
                isnormal = "var gArticleJson = " in articleres
                if isnormal:
                    articleres = articleres.lstrip("var gArticleJson = ")
                    articlejson = eval(articleres)

                    fields["contentType"] = 1

                    title = articlejson['title']  # 标题
                    source = articlejson['source']  # 来源
                    content = articlejson['content']  # 文章内容
                    pubtime = articlejson['publishtime']  # 发布时间
                    workerid = articlejson['fileId']
                    # url = articlejson["shareUrl"]
                    author = articlejson["author"]
                    # commentnum = articlejson["comments"]
                    sharenum = articlejson['countShare']
                    likenum = articlejson['countPraise']
                    readnum = articlejson['countClick']

                    articlecovers = articlejson['imageUrl']
                    # videos = articlejson['videos']
                    # try:
                    # images = articlejson['images']
                    # except Exception as e:
                    # print("images")

                    fields["readnum"] = readnum
                    fields["likenum"] = likenum
                    fields["likenum"] = sharenum
                    if articlecovers:
                        fields["articlecovers"] = [articlecovers]
                    else:
                        fields["articlecovers"] = []

                    fields["appname"] = appname
                    fields["title"] = title
                    fields["url"] = url
                    fields["workerid"] = workerid
                    fields["source"] = source
                    fields["content"] = content
                    fields["author"] = author
                    # fields["commentnum"] = commentnum
                    fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                    fields["createtime"] = 0
                    fields["updatetime"] = 0
                    fields["videocover"] = []

                    # fields["videos"] = []
                    # fields["images"] = []
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

                    print("详情",json.dumps(fields, indent=4, ensure_ascii=False))


                else:
                    articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                    # print("articlejson==",articlejson)
                    #直播
                    fields["contentType"] = -1

                    article = articlejson['main']['articleInfo']
                    title = article['title']
                    pubtime = article['publishtime']
                    workerid = article['fileID']
                    author = article['editor']
                    readnum = article['countClick']
                    likenum = article['countPraise']
                    sharenum = article['countShare']

                    createtime = articlejson['main']['createTime']

                    live = articlejson['main']['liveStream']
                    content = live['flvUrl']
                    #rtmpUrl
                    #hlsUrl

                    fields["readnum"] = readnum
                    fields["likenum"] = likenum
                    fields["likenum"] = sharenum

                    fields["appname"] = appname
                    fields["title"] = title
                    fields["url"] = content
                    fields["workerid"] = workerid
                    #fields["source"] = source
                    #fields["content"] = content
                    fields["author"] = author
                    fields["createtime"] = InitClass().date_time_stamp(createtime)
                    # fields["commentnum"] = commentnum
                    fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                    fields["videocover"] = []
                    fields["videos"] = []
                    fields["images"] = []

                    print("直播 结果==", json.dumps(fields, indent=4, ensure_ascii=False))
                    print("")

            except Exception as e:
                print('e===',e)


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
    spider = Jingjicankaobao('经济参考报')
    spider.run()
