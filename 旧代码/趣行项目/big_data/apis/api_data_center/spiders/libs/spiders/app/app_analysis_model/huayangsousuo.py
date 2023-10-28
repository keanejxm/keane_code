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


class Huayangsousou(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "https://appapi.chinaso.com/young/v2/feed/channel/list"
        headers = {
            "User-Agent": "Young/3.9.6(com.chinaso.so; build:1911161810; Android:23; phone)",
            "TOKEN": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MzkyMTg0NDQsImd1ZXN0SWQiOiIxNGVkYjVhN2Y2ODkxM2RhMGNlZWJhOWZjMzAwYzA2OSIsInV1aWQiOiI5MzA2OTg2MjUiLCJpYXQiOjE2MDc2ODI0NDR9.k69DGoyAFkL33pMjoRdCOsp0Z2dS50_hgs0V8mIM6hQ",
            "guestId": "14edb5a7f68913da0ceeba9fc300c069",
            "auth": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MzkyMTg0NDQsImd1ZXN0SWQiOiIxNGVkYjVhN2Y2ODkxM2RhMGNlZWJhOWZjMzAwYzA2OSIsInV1aWQiOiI5MzA2OTg2MjUiLCJpYXQiOjE2MDc2ODI0NDR9.k69DGoyAFkL33pMjoRdCOsp0Z2dS50_hgs0V8mIM6hQ",
            "Host": "appapi.chinaso.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        data = {
            "ui": "9xMIzh7Up1Knt8L1pfI5gimgU3I49XDGpIOa5VVzmP5ZhNnlutdZY2UFwyxpWwC/"
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
        for channel in channelslists['data']['channel']:
            channelid = channel['chid']
            channelname = channel['name']
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
            url = "https://appapi.chinaso.com/young/v2/phone/feed/list?pull=1&ui=9xMIzh7Up1Knt8L1pfI5givdSsJHQuXovnaxReKlwW5ZhNnlutdZY2UFwyxpWwC%2F" + "&topic=" + str(
                channelid)
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
                datas = []
                try:
                    datas = articlelist_json['data']['data']
                except Exception as  e:
                    print("data", e)
                try:
                    blocks = articlelist_json['data']['blocks']['data']
                    tuijian = []
                    for blcok in blocks:
                        tuijian += blcok['feeds']
                except Exception as  e:
                    print("blocks e", e)
                    tuijian = []
                for article in datas + tuijian:
                    articleparam = InitClass().article_list_fields()
                    articletitle = article['title']
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
                    elif type == 101 and rendertype == 18:
                        # 短视频
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
                            # imgurl = [0]
                            fields["articlecovers"] = article['imgs']
                        except Exception as e:
                            print("e==", e)
                        width = extend['img_size']['img']['width']
                        height = extend['img_size']['img']['height']
                        readnum = extend['f_readnum']
                        appname = articleslist_res.get("appname")

                        # contentType，作品类型，-1未知，1文字，2图文，3视频文，4纯长视频，5纯短视频，6画廊，7纯音频，8短消息（动态、微头条、微博消息等）
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
                        print(json.dumps(fields, indent=4, ensure_ascii=False))
                        continue
                    else:
                        print("type==", type, "rendertype==", rendertype)
                        print("未知类型", article)
                        articletype = "0"
                        continue

                    readnum = 0
                    try:
                        readnum = extend['f_readnum']
                    except Exception as e:
                        print("readnum e", e)
                    pubtime = article["publishtime"]  # 在此处获取到文章的发布时间，避免在文章详情获取不到发布时间
                    source = article["originalsource"]  # 在此处获取到文章的来源，避免在文章详情获取不到来源
                    author = article["author"]  # 在此处获取到文章的作者，避免在文章详情获取不到作者
                    articleparam["pubtime"] = pubtime  # 此步骤为存储发布时间
                    articleparam["source"] = source  # 此步骤为存储文章来源
                    articleparam["author"] = author  # 此步骤为存储作者
                    articleparam["readnum"] = readnum
                    try:
                        articleparam["imageurl"] = article['imgs'][0]
                    except Exception as e:
                        logging.info(f"在文章列表出无法获得封面图{e}")
                    articleparam["articletype"] = articletype
                    articleparam["articleid"] = articleid
                    articleparam["articletitle"] = articletitle
                    articleparam["channelname"] = channelname
                    articleparam["channelID"] = channelid
                    articleparam["banner"] = banners
                    yield articleparam
            except Exception as e:
                print("eee111=", e)

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
        url = ""
        for articleparam in articles:
            articleid = articleparam.get("articleid")
            articletype = articleparam.get("articletype")
            if articletype == "100":
                url = "https://appapi.chinaso.com/young/v1/feed/detail/docid/" + articleid
            elif articletype == "101":
                url = "https://appapi.chinaso.com/young/v1/phone/feed/detail/docid/" + articleid
            elif articletype == "200":
                url = "https://appapi.chinaso.com/young/v1/feed/entityfeed/detail/efid/" + articleid
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
                url = "https://appapi.chinaso.com/young/v1/feed/detail/docid/" + articleid
            elif articletype == "400":
                # 基础信息
                url = "https://appapi.chinaso.com/young/v2/user/social/specialColumn/specialColumnDetail"
                data = {
                    "id": articleid,
                }
            # 传递articletype
            articleurl = articletype
            # videos字段传递url
            videos = url
            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
            channel_index_id = articleparam.get("channelindexid")
            banner = articleparam.get("banner")
            imgurl = articleparam.get("imageurl")
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
            articleurl = articleres.get("articleurl")
            videos = articleres.get("videourl")
            url = videos
            videos = ""
            readnum = articleres.get("readnum")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["appname"] = self.newsname
            fields["platformID"] = self.platform_id
            fields["channelname"] = channelname
            fields["channelindexid"] = channel_index_id
            fields["channelID"] = channelid
            fields["banner"] = banners
            fields["url"] = url
            fields["readnum"] = readnum  # 文章的阅读数
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))

                # 0 未知
                # 100 文字
                # 101 文字 ，有artid
                # 200 音频
                # 300 视频 用album_docid
                # 301 视频 用docid
                # 400 专题
                # 500 广告

                articletype = articleurl
                # contentType，作品类型，-1未知，1文字，2图文，3视频文，4纯长视频，5纯短视频，6画廊，7纯音频，8短消息（动态、微头条、微博消息等）
                if articletype == "100" or articletype == "101":
                    # 文字
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
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
                elif articletype == "200":
                    # 音频
                    # print("音频")
                    articlelist = articlejson['data']['playlist']['list']
                    # print("articlelist==",articlelist)
                    for article in articlelist:
                        # print("音频 for")

                        extend_json = article['extend']
                        extend = json.loads(extend_json)

                        # workerid = extend['efid']
                        # title = extend['album_name']
                        workerid = article['docid']
                        title = article['name']

                        try:
                            author = extend['publisher']['headname']
                            fields["author"] = author
                        except Exception as e:
                            print("e", e)

                        try:
                            content = extend['radiosrc']
                            fields["content"] = content
                        except Exception as e:
                            # 列表，需要重新请求
                            print("radiosrc e", e)

                        try:
                            playnum = extend['playcount']
                            fields["playnum"] = playnum
                        except Exception as e:
                            print("playnum 无 ", e)

                        fields["contentType"] = 7

                        fields["title"] = title
                        if imgurl:
                            fields["articlecovers"] = [imgurl]
                        else:
                            fields["articlecovers"] = []
                        fields["images"] = []
                        fields["videos"] = []
                        fields["videocover"] = []

                        fields["workerid"] = workerid
                        fields["appname"] = appname
                        yield {"code": 1, "msg": "OK", "data": {"works": fields}}
                elif articletype == "300" or articletype == "301":
                    # 视频
                    article = articlejson['data']['data']

                    workerid = article['docid']
                    title = article['title']
                    author = article['author']
                    source = article['originalsource']
                    pubtime = article['publishtime']
                    pubtime = pubtime.split(".")[0]

                    content = article['content']
                    videos = article['videosrc']

                    extend_json = article['extend']
                    extend = json.loads(extend_json)
                    img_size = extend['img_size']
                    width = img_size['img']['width']
                    height = img_size['img']['height']

                    fields["contentType"] = 3

                    fields["workerid"] = workerid
                    fields["title"] = title
                    fields["author"] = author
                    fields['source'] = source
                    fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                    fields["content"] = content
                    if videos:
                        fields["videos"] = [videos]
                    else:
                        fields["videos"] = []

                    fields["images"] = []
                    fields["articlecovers"] = []
                    fields["width"] = width
                    fields["height"] = height
                    try:
                        fields["videocover"] = article['imgs']
                    except Exception as e:
                        print("cover", e)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
                elif articletype == "400":
                    # 专题
                    article = articlejson['data']['info']
                    workerid = article['scid']
                    title = article['name']
                    fields["contentType"] = -1
                    fields["workerid"] = workerid
                    fields["title"] = title
                fields["appname"] = appname
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}

            except Exception as e:
                print("eeeee==", e)

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Huayangsousou(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
