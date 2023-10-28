# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
from App.appspider_m import Appspider
from App.initclass import InitClass
import requests


class Huayangsousou(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "https://appapi.chinaso.com/young/v2/feed/channel/list"
        # 频道请求头
        headers = {
            "User-Agent": "Young/3.9.6(com.chinaso.so; build:1911161810; Android:23; phone)",
            "TOKEN": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MzkyMTg0NDQsImd1ZXN0SWQiOiIxNGVkYjVhN2Y2ODkxM2RhMGNlZWJhOWZjMzAwYzA2OSIsInV1aWQiOiI5MzA2OTg2MjUiLCJpYXQiOjE2MDc2ODI0NDR9.k69DGoyAFkL33pMjoRdCOsp0Z2dS50_hgs0V8mIM6hQ",
            "guestId": "14edb5a7f68913da0ceeba9fc300c069",
            "auth": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MzkyMTg0NDQsImd1ZXN0SWQiOiIxNGVkYjVhN2Y2ODkxM2RhMGNlZWJhOWZjMzAwYzA2OSIsInV1aWQiOiI5MzA2OTg2MjUiLCJpYXQiOjE2MDc2ODI0NDR9.k69DGoyAFkL33pMjoRdCOsp0Z2dS50_hgs0V8mIM6hQ",
            "Host": "appapi.chinaso.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        # 频道数据体
        data = {
            "ui":"9xMIzh7Up1Knt8L1pfI5gimgU3I49XDGpIOa5VVzmP5ZhNnlutdZY2UFwyxpWwC/"
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
        # print("channelslists====",channelslists)
        channelparams = []
        for channel in channelslists['data']['channel']:
            channelid = channel['chid']
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
            # 若有两个请求接口则如下： 例如：banner列表和文章列表时两个请求接口
            # url_banner = "http://cms.farmer.com.cn/api/app/front/content/list"  # banner请求接口
            url = "https://appapi.chinaso.com/young/v2/phone/feed/list?pull=1&ui=9xMIzh7Up1Knt8L1pfI5givdSsJHQuXovnaxReKlwW5ZhNnlutdZY2UFwyxpWwC%2F"+"&topic="+str(channelid)

            headers = {
                "User-Agent": "Young/3.9.6(com.chinaso.so; build:1911161810; Android:23; phone)",
                "TOKEN": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MzkyMTg0NDQsImd1ZXN0SWQiOiIxNGVkYjVhN2Y2ODkxM2RhMGNlZWJhOWZjMzAwYzA2OSIsInV1aWQiOiI5MzA2OTg2MjUiLCJpYXQiOjE2MDc2ODI0NDR9.k69DGoyAFkL33pMjoRdCOsp0Z2dS50_hgs0V8mIM6hQ",
                "guestId": "14edb5a7f68913da0ceeba9fc300c069",
                "auth": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MzkyMTg0NDQsImd1ZXN0SWQiOiIxNGVkYjVhN2Y2ODkxM2RhMGNlZWJhOWZjMzAwYzA2OSIsInV1aWQiOiI5MzA2OTg2MjUiLCJpYXQiOjE2MDc2ODI0NDR9.k69DGoyAFkL33pMjoRdCOsp0Z2dS50_hgs0V8mIM6hQ",
                "Host": "appapi.chinaso.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
            }

            data = {}
            method = 'post'
            # data_banner = {
            #     'orderBy': '4',
            #     'channelIds': channelid,
            #     'count': '4',
            #     'typeIds': '5',
            # }
            # articlelist_param_banner = InitClass().articlelists_params_fields(url_banner, headers, method, channelname,
            #                                                                   data = data_banner,
            #                                                                   banners = 1)  # 添加banner请求数据体，或其他接口请求数据
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,channelid=channelid, data = data)
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
            channelid = articleslist_res.get("channelid")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                # 可在下面打印处打断点，查看请求到的数据
                # print("articlelist_json",articlelist_json)
                #若banner图在articlelist_json中则分来开取并给其复制banner = 1
                datas = []
                try:
                    datas = articlelist_json['data']['data']
                except Exception as  e:
                    print("data",e)

                try:
                    blocks = articlelist_json['data']['blocks']['data']
                    tuijian = []
                    for blcok in blocks:
                      tuijian += blcok['feeds']
                except Exception as  e:
                    print("blocks e",e)
                    tuijian = []

                for article in datas + tuijian:
                    articleparam = InitClass().article_list_fields()
                    articletitle = article['title']

                    # 文章类型
                    type = int(article['type'])
                    rendertype = int(article['rendertype'])

                    extend_json = article['extend']
                    extend = json.loads(extend_json)

                    # articletype 自定义字段，区分详情如何请求接口
                    # 0 未知
                    # 100 文字
                    # 101 文字 ，有artid
                    # 200 音频
                    # 300 视频 用album_docid
                    # 301 视频 用docid
                    # 400 专题
                    # 500 广告
                    articletype = "100"
                    articleid = ""
                    if type == 0 and rendertype == 14:
                        # 文字
                        articleid = article['docid']  # 不是请求详情id
                        if "artid" in extend.keys():
                            articletype = "100"
                        else:
                            articletype = "101"
                    elif type == 105:
                        articletitle = article['title']
                        # print("articletitle ==",articletitle)
                        if rendertype == 75:
                            # 专辑 视频
                            try:
                                articleid = extend['album_docid']
                                articletype = "300"
                            except Exception as e:
                                articletype = "200"
                                articleid = str(extend['efid'])
                        elif rendertype == 76:
                            # print("音频 1111")
                            articleid = str(extend['efid'])
                            articletype = "200"
                        else:
                            print("未知类型2")
                    elif type == 106:
                        # type 106 专题
                        articleid = extend['scid']
                        articletype = "400"
                    elif type == 100:
                        # 广告
                        articletype = "500"
                        continue
                    elif type == 1 and (rendertype == 24 or rendertype == 15):
                        # 视频
                        articleid = article['docid']
                        articletype = "301"

                    #纯短视频
                    elif type == 101 and rendertype == 18:
                        # 纯短视频
                        fields = InitClass().article_fields()
                        workerid = article['docid']
                        title = article['title']
                        author = article['author']
                        videos = article['videosrc']
                        # radios = article['radiosrc']
                        pubtime = article['publishtime']
                        pubtime = pubtime.split(".")[0]

                        source = article['originalsource']
                        try:
                            #imgurl = [0]
                            fields["articlecovers"] = article['imgs']
                        except Exception as e:
                            print("e==", e)
                        width = extend['img_size']['img']['width']
                        height = extend['img_size']['img']['height']
                        readnum = extend['f_readnum']
                        # appname = articleslist_res.get("appname")

                        #contentType，作品类型，-1未知，1文字，2图文，3视频文，4纯长视频，5纯短视频，6画廊，7纯音频，8短消息（动态、微头条、微博消息等）
                        fields["contentType"] = 5
                        fields["appname"] = "花漾搜索"
                        fields["workerid"] = workerid
                        fields["title"] = title
                        fields["author"] = author
                        if videos:
                            fields["videos"] = [videos]
                        else:
                            fields["videos"] = []
                        fields['source'] = source
                        fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                        fields["updatetime"] = 0
                        fields["createtime"] = 0
                        fields["videocover"] = []
                        fields["images"] = []
                        fields["width"] = width
                        fields["height"] = height
                        fields["readnum"] = readnum
                        fields["channelname"] = channelname
                        fields["channelID"] = channelid
                        fields["banner"] = 0
                        # print("纯短视频==")
                        print("纯短视频==",json.dumps(fields, indent=4, ensure_ascii=False))
                        continue

                    else:
                        print("type==",type,"rendertype==",rendertype)
                        print("未知类型", article)
                        articletype = "0"
                        continue

                    readnum = 0
                    try:
                        readnum = extend['f_readnum']
                    except Exception as e:
                        print("无阅读数")
                    # videos = article["videourl"] #在此处获取到文章视频url，避免在文章详情获取不到视频链接，数据类型list
                    # videocover = article["videocover"]#在此处获取到文章视频封面图，避免在文章详情获取不到视频封面图链接，数据类型list
                    pubtime = article["publishtime"]  # 在此处获取到文章的发布时间，避免在文章详情获取不到发布时间
                    # createtime = article["createtime"]#在此处获取到文章的创建时间，避免在文章详情获取不创建时间
                    # updatetime = article["updatetime"]#在此处获取到文章的更新时间，避免在文章详情获取不到更新时间
                    source = article["originalsource"]  # 在此处获取到文章的来源，避免在文章详情获取不到来源
                    author = article["author"]  # 在此处获取到文章的作者，避免在文章详情获取不到作者
                    # likenum = article["likenum"]#在此处获取到文章的点赞数，避免在文章详情获取不到点赞数
                    # commentnum = article["commentnum"]#在此处获取到文章的评论数，避免在文章详情获取不到评论数
                    # sharenum = article["sharenum"]#在此处获取到文章的评论数，避免在文章详情获取不到评论数
                    # readnum = article["readnum"]#在此处获取到文章的阅读数，避免在文章详情获取不到阅读数
                    # articleurl = article["articleurl"]#在此处获取到文章html地址，避免在文章详情获取不到html地址
                    # articleparam["video"] = videos #此步骤为存储视频url
                    # articleparam["videocover"] = videocover#此步骤为存储视频封面
                    articleparam["pubtime"] = pubtime  # 此步骤为存储发布时间
                    # articleparam["createtime"] = createtime#此步骤为存储创建时间
                    # articleparam["updatetime"] = updatetime#此步骤为存储更新时间
                    articleparam["source"] = source  # 此步骤为存储文章来源
                    articleparam["author"] = author  # 此步骤为存储作者
                    # articleparam["likenum"] = likenum#此步骤为存储点赞数
                    # articleparam["commentnum"] = commentnum#此步骤为存储评论数
                    articleparam["readnum"] = readnum

                    try:
                        # 只取一个图片地址
                        articleparam["imageurl"] = article['imgs'][0]
                    except Exception as e:
                        logging.info(f"在文章列表出无法获得封面图{e}")

                    articleparam["articletype"] = articletype
                    articleparam["articleid"] = articleid
                    articleparam["articletitle"] = articletitle
                    articleparam["channelname"] = channelname
                    articleparam["channelID"] = channelid
                    articleparam["banner"] = banners
                    articlesparams.append(articleparam)
            except Exception as e:
                print("错误数eee111=",e)
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
        headers = {
            "User-Agent": "Young/3.9.6(com.chinaso.so; build:1911161810; Android:23; phone)",
            "TOKEN": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2Mzk0NDYyMTAsImd1ZXN0SWQiOiIyMTEzZDJlNzdmNTU4NDQ0ODYwYzNiNTQ4MGRiMmIxMCIsInV1aWQiOiIxMDcwNzI2ODgxIiwiaWF0IjoxNjA3OTEwMjEwfQ.NesicGRWbEyLkhectzodRC5pnNrdIdFwAWau5zS2G4g",
            "guestId": "2113d2e77f558444860c3b5480db2b10",
            "auth": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2Mzk0NDYyMTAsImd1ZXN0SWQiOiIyMTEzZDJlNzdmNTU4NDQ0ODYwYzNiNTQ4MGRiMmIxMCIsInV1aWQiOiIxMDcwNzI2ODgxIiwiaWF0IjoxNjA3OTEwMjEwfQ.NesicGRWbEyLkhectzodRC5pnNrdIdFwAWau5zS2G4g",
            "Host": "appapi.chinaso.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        #articlejson = {}
        data = {}
        url = ""

        for articleparam in articles:

            articleid = articleparam.get("articleid")
            articletype = articleparam.get("articletype")

            if articletype == "100":
                url = "https://appapi.chinaso.com/young/v1/feed/detail/docid/" + articleid
            elif articletype == "101":
                url = "https://appapi.chinaso.com/young/v1/phone/feed/detail/docid/"+articleid
            elif articletype == "200":
                url = "https://appapi.chinaso.com/young/v1/feed/entityfeed/detail/efid/"+articleid
                data = {
                    "norec": "1",
                    "pn": "1",
                    "current": "",
                    "lpos": "",
                    "rpos": "",
                    "desc": "",
                    "ps": "10",
                }

            elif articletype == "300" or articletype == "301":
                url = "https://appapi.chinaso.com/young/v1/feed/detail/docid/"+articleid
            elif articletype == "400":
                #基础信息
                url = "https://appapi.chinaso.com/young/v2/user/social/specialColumn/specialColumnDetail"
                data = {
                    "id": articleid,
                }

                # print("articleparam==",articleparam)


            #传递articletype
            articleurl = articletype

            #videos字段传递url
            videos = url

            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
            channelid = articleparam.get("channelID")
            banner = articleparam.get("banner")
            imgurl = articleparam.get("imageurl")
            #videos = articleparam.get("videos")
            videocover = channelid #articleparam.get("videocover")
            pubtime = articleparam.get("pubtime")
            createtime = articleparam.get("createtime")
            updatetime = articleparam.get("updatetime")
            source = articleparam.get("source")
            author = articleparam.get("author")
            likenum = articleparam.get("likenum")
            commentnum = articleparam.get("commentnum")
            sharenum = articleparam.get("sharenum")
            readnum = articleparam.get("readnum")
            #articleurl = articleparam.get("articleurl")
            # 若APP有关于时间的反爬加sleeptime = 1，若发送为json数据体，则添加articlejson = articlejson
            article = InitClass().article_params_fields(url, headers, method, channelname, imageurl= imgurl, data = data,
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
            #channelid = articleres.get("channelID")
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            banners = articleres.get("banner")
            articleurl = articleres.get("articleurl")
            # 若上面存储了此字段需用下列方式获取
            videos = articleres.get("videourl")

            #通过videos接收url
            url = videos
            videos = ""

            channelid = articleres.get("videocover")
            # pubtime = articleres.get("pubtime")
            # createtime = articleres.get("createtime")
            # updatetime = articleres.get("updatetime")
            # source = articleres.get("source")
            # likenum = articleres.get("author")
            # commentnum = articleres.get("author")
            # sharenum = articleres.get("sharenum")
            readnum = articleres.get("readnum")
            # author = articleres.get("author")
            # articleurl = articleres.get("articleurl")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["channelID"] = channelid
            # fields["imageurl"] = imgurl
            fields["banner"] = banners
            fields["url"] = url
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
            fields["readnum"] = readnum #文章的阅读数
            # fields["trannum"] = trannum #文章的转发数
            # fields["sharenum"] = sharenum #文章分享数
            # fields["author"] = author #文章作者
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent = 4, ensure_ascii = False))
                #print("articlejson==",articlejson)

                # 0 未知
                # 100 文字
                # 101 文字 ，有artid
                # 200 音频
                # 300 视频 用album_docid
                # 301 视频 用docid
                # 400 专题
                # 500 广告

                covers = list()
                if imgurl:
                    covers.append(imgurl)
                fields["articlecovers"] = covers
                fields["createtime"] = 0
                fields["updatetime"] = 0
                fields["appname"] = appname

                articletype = articleurl

                #contentType，作品类型，-1未知，1文字，2图文，3视频文，4纯长视频，5纯短视频，6画廊，7纯音频，8短消息（动态、微头条、微博消息等）

                if articletype == "100" or articletype == "101":
                    #文字

                    article = articlejson['data']['data']

                    workerid = article['docid']
                    title = article['title']
                    author = article['author']
                    source = article['originalsource']
                    pubtime = article['publishtime']
                    pubtime = pubtime.split(".")[0]
                    content = article['content']['content']

                    fields["contentType"] = 1

                    fields["workerid"] = workerid
                    fields["title"] = title
                    fields["author"] = author
                    fields['source'] = source
                    fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                    fields["content"] = content

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

                    print("文字==", json.dumps(fields, indent=4, ensure_ascii=False))
                    continue

                elif articletype == "200":
                    #音频

                    articlelist = articlejson['data']['playlist']['list']
                    # print("articlelist==",articlelist)
                    for article in articlelist:

                        extend_json = article['extend']
                        extend = json.loads(extend_json)

                        workerid = article['docid']
                        title = article['name']

                        try:
                            author = extend['publisher']['headname']
                            fields["author"] = author
                        except Exception as e:
                            print("e",e)

                        try:
                            content = extend['radiosrc']
                            fields["content"] = content
                        except Exception as e:
                            #列表，需要重新请求
                            print("radiosrc e",e)

                        try:
                            playnum = extend['playcount']
                            fields["playnum"] = playnum
                        except Exception as e:
                            print("playnum 无 ",e)

                        fields["contentType"] = 7

                        fields["title"] = title

                        fields["images"] = []
                        fields["videos"] = []
                        fields["videocover"] = []

                        fields["workerid"] = workerid

                        fields["pubtime"] = 0
                        # print("纯音频结果==")
                        print("纯音频结果==", json.dumps(fields, indent=4, ensure_ascii=False))
                    continue

                elif articletype == "300" or articletype == "301":
                    # 视频

                    article = articlejson['data']['data']

                    workerid = article['docid']
                    title = article['title']
                    author = article['author']
                    source = article['originalsource']
                    pubtime = article['publishtime']
                    pubtime = pubtime.split(".")[0]

                    # content = article['content']
                    videos = article['videosrc']

                    width = 0
                    height = 0
                    try:
                        extend_json = article['extend']
                        extend = json.loads(extend_json)
                        img_size = extend['img_size']
                        width = img_size['img']['width']
                        height = img_size['img']['height']
                    except Exception as e:
                        print("无尺寸")

                    fields["width"] = width
                    fields["height"] = height


                    fields["contentType"] = 3

                    fields["workerid"] = workerid
                    fields["title"] = title
                    fields["author"] = author
                    fields['source'] = source
                    fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                    # fields["content"] = content
                    if videos:
                        fields["videos"] = [videos]
                    else:
                        fields["videos"] = []

                    fields["images"] = []
                    # fields["articlecovers"] = []


                    try:
                        fields["videocover"] = article['imgs']
                    except Exception as e:
                        print("cover",e)

                    # print("视频文章==")
                    print("视频文章==", json.dumps(fields, indent=4, ensure_ascii=False))

                    continue

                elif articletype == "400":
                    #专题
                    # print("articlejson==", articlejson)

                    # fields["articlecovers"] = covers
                    # fields["createtime"] = 0
                    # fields["updatetime"] = 0
                    # fields["appname"] = appname
                    # fields["channelname"] = channelname
                    # fields["channelID"] = channelid
                    # # fields["imageurl"] = imgurl
                    # fields["banner"] = banners
                    # fields["url"] = url
                    # fields["readnum"] = readnum

                    article = articlejson['data']['info']

                    workerid = article['scid']
                    title = article['name']
                    topicnum = article["articleNum"]
                    desc = article["description"]

                    topic_fields = InitClass().topic_fields()
                    topic_fields["topicID"] = workerid
                    topic_fields["platformName"] = appname
                    topic_fields["channelName"] = channelname
                    topic_fields["channelID"] = channelid
                    topic_fields["topicUrl"] = url
                    topic_fields["title"] = title
                    topic_fields["digest"] = desc
                    topic_fields["topicCover"] = covers
                    topic_fields["articleNum"] = topicnum
                    topic_fields["pubTime"] = 0

                    # topic_fields["pubTime"]

                    # topic_fields["region"]
                    topic_fields["createTime"] = 0
                    topic_fields["updateTime"] = 0

                    newestarticleid = ""
                    newestpubtime = 0

                    try:
                        # 请求专题内新闻列表
                        url_list = "https://appapi.chinaso.com/young/v2/user/social/specialColumn/specialColumnArticleList?pageNo=1&pageSize=20&id="+str(workerid)
                        headers = {
                            "User-Agent": "Young/3.9.6(com.chinaso.so; build:1911161810; Android:23; phone)",
                            "TOKEN": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2Mzk0NDYyMTAsImd1ZXN0SWQiOiIyMTEzZDJlNzdmNTU4NDQ0ODYwYzNiNTQ4MGRiMmIxMCIsInV1aWQiOiIxMDcwNzI2ODgxIiwiaWF0IjoxNjA3OTEwMjEwfQ.NesicGRWbEyLkhectzodRC5pnNrdIdFwAWau5zS2G4g",
                            "guestId": "2113d2e77f558444860c3b5480db2b10",
                            "auth": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2Mzk0NDYyMTAsImd1ZXN0SWQiOiIyMTEzZDJlNzdmNTU4NDQ0ODYwYzNiNTQ4MGRiMmIxMCIsInV1aWQiOiIxMDcwNzI2ODgxIiwiaWF0IjoxNjA3OTEwMjEwfQ.NesicGRWbEyLkhectzodRC5pnNrdIdFwAWau5zS2G4g",
                            "Host": "appapi.chinaso.com",
                            "Connection": "Keep-Alive",
                            "Accept-Encoding": "gzip",
                        }

                        topicres = requests.get(url_list, headers=headers).text
                        topiclistjson = json.loads(
                            json.dumps(json.loads(topicres, strict=False), indent=4, ensure_ascii=False))

                        itemlist = topiclistjson["data"]["data"]
                        for topicarticle in itemlist:

                            aid = topicarticle["docid"]
                            acovers = topicarticle["imgs"]
                            asource = topicarticle["originalsource"]
                            aauthor = topicarticle["author"]
                            atitle = topicarticle["title"]

                            apubtime = topicarticle["publishtime"]
                            apubtime = apubtime.split(".")[0]
                            apubtime = InitClass().date_time_stamp(apubtime)
                            if int(apubtime) > newestpubtime:
                                newestpubtime = int(apubtime)
                                newestarticleid = aid

                            alink = ""
                            try:
                                aextend = topicarticle["extend"]
                                aextendjsont = json.loads(aextend)
                                alink = aextendjsont["externallinks"]
                            except Exception as e:
                                print("无扩展")

                            article_fields = InitClass().article_fields()

                            article_fields["appname"] = appname
                            article_fields["channelname"] = channelname
                            article_fields["channelID"] = channelid
                            article_fields["channelType"] = ""
                            article_fields["url"] = alink
                            article_fields["workerid"] = aid
                            article_fields["title"] = atitle
                            article_fields["content"] = ""
                            article_fields["articlecovers"] = acovers
                            article_fields["images"] = []
                            article_fields["videos"] = []
                            article_fields["videocover"] = []
                            article_fields["source"] = asource
                            article_fields["pubtime"] = apubtime
                            article_fields["createtime"] = 0
                            article_fields["updatetime"] = 0
                            article_fields["author"] = aauthor
                            article_fields["specialtopic"] = 1
                            article_fields["topicid"] = workerid
                            article_fields["topicTitle"] = title
                            print("专题内文章==", json.dumps(article_fields, indent=4, ensure_ascii=False))
                    except Exception as e:
                        print("请求详情失败 e",e)

                    topic_fields["newestArticleID"] = newestarticleid
                    print("大专题==", json.dumps(topic_fields, indent=4, ensure_ascii=False))

                    continue

                # title = articlejson['data']['title']  # 标题
                # source = articlejson['data']['origin']  # 来源
                # content = articlejson['data']['txt']  # 文章内容
                # pubtime = articlejson['data']['date']  # 发布时间
                # workerid = articlejson['data']['id']
                # url = articlejson['data']["shareUrl"]
                # author = articlejson['data']["author"]
                # commentnum = articlejson['data']["comments"]
                # fields["appname"] = appname

                # fields["title"] = title
                # fields["url"] = url
                # fields["workerid"] = workerid
                # fields["source"] = source
                # fields["content"] = content
                # fields["author"] = author
                # fields["commentnum"] = commentnum
                # fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                # print("结果==",json.dumps(fields, indent = 4, ensure_ascii = False))
                print("未知结果==")

            except Exception as e:
                print("错误数eeeee==",e)

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
    spider = Huayangsousou('花漾搜索')
    spider.run()
