# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


class Zhongguowenlian(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "https://prod.ccmapp.cn/api-cms-terminal/open/category?imei=008796747591277&id=a7fcda08806544d696a57f698868c5f2"
        # 频道请求头
        headers = {
            #"path": "/api-cms-terminal/open/category?imei=008796747591277&id=a7fcda08806544d696a57f698868c5f2",
            "authority": "prod.ccmapp.cn",
            "scheme": "https",
            "url_name": "find",
            "accept-encoding": "gzip",
            "user-agent": "okhttp/3.6.0",
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
        # print(channelslists)
        #所有频道列表
        channelparams = []
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

            #请求各频道列表数据
            # 若有两个请求接口则如下： 例如：banner列表和文章列表时两个请求接口

            if channelname == "关注":
                # print("关注")
                # "关注"
                url = "http://md.ccmapp.cn:9998/rec"
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": "c5258f9d1505c0caea4026fa2a5b2af6",
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
                    "Host": "md.ccmapp.cn:9998",
                    "Accept-Encoding": "gzip",
                    "Content-Length": "201",
                    "Connection": "keep-alive",
                }
                listjson = {
                    "page": "1",
                    "uid": "",
                    "bid": "602816897101692",
                    "item_type": "NewsBase",
                    "appkey": "36636158d26b7bf147b2059b8443c0c2",
                    "gid": "08002703ee6d",
                    "sid": "08298fb566f1ae6c63c9e7c8ca76e97f",
                    "method": "602816897101692"
                }

            else:
                # print("channelname=",channelname,"channelid=",channelid)
                url = 'https://prod.ccmapp.cn/api-cms-production/app/production/pub/content/listWithAd'
                headers = {
                    "path": "/api-cms-production/app/production/pub/content/listWithAd",
                    "authority": "prod.ccmapp.cn",
                    "scheme": "https",
                    "url_name": "find",
                    "content-type": "application/json; charset=UTF-8",
                    "content-length": "103",
                    "accept-encoding": "gzip",
                    "user-agent": "okhttp/3.6.0",
                }

                listjson = {
                    "categoryId":channelid,
                    "currentPage":"1",
                    "excludeUnitIds":[],
                    "pageSize":"20"
                }

            data = {
            }

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
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data,channeljson=listjson,channelid=channelid)
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
        #解析频道列表结果
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
                # print("channelname ==",channelname, "channelid==",channelid)
                # print("articlelist_json==",articlelist_json)
                #若banner图在articlelist_json中则分来开取并给其复制banner = 1
                try:
                    if channelname == "关注":
                        articlelists = articlelist_json
                        for articlelist in articlelists:
                            if isinstance(articlelist, list):
                                articlelists = articlelist
                                if not articlelists:
                                    continue
                    else:
                        articlelists = articlelist_json['data']

                    for article in articlelists:
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        #print(article)
                        articleparam = InitClass().article_list_fields()
                        articletitle = article['title']
                        articleid = article['id']
                        categoryid = article['categoryId']
                        categorytype = article['templateId']

                        # 'h5URL': 'https://file.ccmapp.cn/group1/M00/1C/A3/rApntV_R3m-AJMEWAAA0FnQBeFA31.html',
                        # 'id': 'c4f6ca04-d71b-4d12-8a4b-d4ed4e4e2cda',
                        # 'categoryId': '2580fbc34e584a089acf2a41ce5338ff',
                        # 'iid': 'c4f6ca04-d71b-4d12-8a4b-d4ed4e4e2cda'

                        # videos = article["videourl"] #在此处获取到文章视频url，避免在文章详情获取不到视频链接，数据类型list
                        # videocover = article["videocover"]#在此处获取到文章视频封面图，避免在文章详情获取不到视频封面图链接，数据类型list
                        # pubtime = article["pubtime"]#在此处获取到文章的发布时间，避免在文章详情获取不到发布时间
                        # createtime = article["createtime"]#在此处获取到文章的创建时间，避免在文章详情获取不创建时间
                        # updatetime = article["updatetime"]#在此处获取到文章的更新时间，避免在文章详情获取不到更新时间
                        # source = article["source"]#在此处获取到文章的来源，避免在文章详情获取不到来源
                        # author = article["author"]#在此处获取到文章的作者，避免在文章详情获取不到作者
                        # likenum = article["likenum"]#在此处获取到文章的点赞数，避免在文章详情获取不到点赞数
                        # commentnum = article["commentnum"]#在此处获取到文章的评论数，避免在文章详情获取不到评论数
                        # sharenum = article["sharenum"]#在此处获取到文章的评论数，避免在文章详情获取不到评论数
                        # readnum = article["readnum"]#在此处获取到文章的阅读数，避免在文章详情获取不到阅读数
                        # articleurl = article["articleurl"]#在此处获取到文章html地址，避免在文章详情获取不到html地址
                        # articleparam["video"] = videos #此步骤为存储视频url
                        # articleparam["videocover"] = videocover#此步骤为存储视频封面
                        # articleparam["pubtime"] = pubtime#此步骤为存储发布时间
                        # articleparam["createtime"] = createtime#此步骤为存储创建时间
                        # articleparam["updatetime"] = updatetime#此步骤为存储更新时间
                        # articleparam["source"] = source#此步骤为存储文章来源
                        # articleparam["author"] = author#此步骤为存储作者
                        # articleparam["likenum"] = likenum#此步骤为存储点赞数
                        # articleparam["commentnum"] = commentnum#此步骤为存储评论数
                        # try:
                        #     articleparam["imageurl"] = article['photoList']['photo']
                        # except Exception as e:
                        #     logging.info(f"在文章列表出无法获得封面图{e}")
                        articleparam["articleid"] = articleid
                        articleparam['categoryid'] = categoryid
                        articleparam['categorytype'] = categorytype
                        articleparam["articletitle"] = articletitle
                        articleparam["channelname"] = channelname
                        articleparam["channelid"] = channelid
                        articleparam["banner"] = banners
                        articlesparams.append(articleparam)
                except Exception as e:
                    print("e111=",e, articlelist_json)
            except Exception as e:
                print("e22=",e, articlelist_json)
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        """
        组建请求文章详情所需要的数据体
        :param articles:
        :return:
        """
        #请求详情
        articlesparam = []
        url = 'http://prod.ccmapp.cn/api-cms-production/app/production/pub/content/info'
        headers = {
            'Host': 'prod.ccmapp.cn',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 Html5Plus/1.0',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'X-Requested-With': 'com.cflac.art',
            'Connection': 'keep-alive',
        }

        method = 'get'
        for articleparam in articles:
            data = {
                'id': articleparam.get("articleid"),
                'categoryId' : articleparam.get("categoryid"),
                'terminalType' :articleparam.get("categorytype"),
                'token':'',
                'imei':'test'
            }

            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
            channelid = articleparam.get("channelid")

            banner = articleparam.get("banner")
            imgurl = articleparam.get("imageurl")
            videos = channelid#articleparam.get("videos")
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
        #解析详情结果
        for articleres in articles_res:
            channelname = articleres.get("channelname")
            channelid = articleres.get("videourl")

            # imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            banners = articleres.get("banner")
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
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["channelID"] = channelid
            # fields["imageurl"] = imgurl
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
                articlejson = json.loads(json.dumps(json.loads(articleres), indent = 4, ensure_ascii = False))
                # print("详情 结果 articlejson==",articlejson)

                article = articlejson['data']

                title = article['title']  # 标题
                source = article['source'] # 来源
                content = article['content']  # 文章内容
                pubtime = article['publishTime'] # 发布时间
                workerid = article['id']
                url = article['h5URL']
                author = article['author']
                cover = article["image"]
                articlecovers = list()
                if cover:
                    articlecovers.append(cover)


                # commentnum = articlejson['data']["comments"]
                fields["appname"] = appname
                fields["title"] = title
                fields["url"] = url
                fields["workerid"] = workerid
                fields["source"] = source
                fields["content"] = content
                fields["author"] = author
                fields["articlecovers"] = articlecovers
                fields["createtime"] = 0
                fields["updatetime"] = 0

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
                fields["videocover"] = []

                fields["pubtime"] = pubtime #InitClass().date_time_stamp(pubtime)
                print("文章==",json.dumps(fields, indent = 4, ensure_ascii = False))
            except Exception as e:
                print(e)

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
    spider = Zhongguowenlian('中国文联')
    spider.run()
