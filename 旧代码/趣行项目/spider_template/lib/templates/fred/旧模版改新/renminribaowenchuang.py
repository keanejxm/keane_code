# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass

class Renminribaowenchuang(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "http://rmrbwc.com/rest/themeTypes/client"
        # 频道请求头
        headers = {
            "token": "",
            "Host": "rmrbwc.com",
            "Accept-Encoding": "gzip",
            "Cookie": "JSESSIONID=C8826175D8C13DEB77A2ECF5F7630E00",
            "User-Agent": "okhttp/3.9.1",
            "Connection": "keep-alive",
        }
        # 频道数据体
        data = {}

        # 频道请求方式
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data = data)

        yield app_params

    @staticmethod
    def analyzechannels(channelsres):

        # 将返回的数据转为json数据
        channelslists = json.loads(channelsres)
        # 返回的数据是编码错误，则用下面代码解析数据
        # print("channelslists==",channelslists)
        channelparams = []


        for channel in channelslists['payload']:
            channelid = channel['id']
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
            url = "http://rmrbwc.com/rest/themes/v1/list"
            headers = {
                "token": "",
                "Host": "rmrbwc.com",
                "Accept-Encoding": "gzip",
                "Cookie": "JSESSIONID=C8826175D8C13DEB77A2ECF5F7630E00",
                "User-Agent": "okhttp/3.9.1",
                "Connection": "keep-alive"
            }

            data = {
                "id": channelid,
                "currentPage": 0,
                "pageSize": 6,
            }

            method = 'get'

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,channelid=channelid, data = data)

            articleparams.append(articlelist_param)
        yield articleparams

    @staticmethod
    def analyze_articlelists(articleslist_ress):

        articlesparams = []
        for articleslist_res in articleslist_ress:
            # banners = articleslist_res.get("banner")
            channelname = articleslist_res.get("channelname")
            channelid = articleslist_res.get("channelid")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)

                try:
                    articlelists = articlelist_json['payload']

                    newslist = articlelists['themeList']['list']
                    banner_list = articlelists['bannerList']

                    activitys = []
                    try:
                        activity_list = articlelists['activityList']
                        for activityitem in activity_list:
                            actype = activityitem['type']
                            if actype != 1:
                                #1 为 商城
                                activitys += activityitem['objectList']
                    except Exception as e:
                        activitys = []


                    #banner
                    for article in banner_list:
                        banners = 1
                        # print("banneritem==", article)
                        articleparam = InitClass().article_list_fields()
                        articletitle = article['description']

                        try:
                            articleid = article['targetId']
                        except Exception as e:
                            articleid = article['id']

                        createtime = article["creationTime"]  # 在此处获取到文章的创建时间，避免在文章详情获取不创建时间
                        updatetime = article["updateTime"]  # 在此处获取到文章的更新时间，避免在文章详情获取不到更新时间

                        articleparam["createtime"] = createtime  # 此步骤为存储创建时间
                        articleparam["updatetime"] = updatetime  # 此步骤为存储更新时间

                        try:
                            articleparam["imageurl"] = article['pictureInfo']['url']
                        except Exception as e:
                            logging.info(f"在文章列表出无法获得封面图{e}")
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["channelname"] = channelname
                        articleparam["channelID"] = channelid
                        articleparam["banner"] = banners

                        articlesparams.append(articleparam)

                    #列表
                    for article in newslist + activitys:
                        banners = 0
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        print("article==",article)
                        articleparam = InitClass().article_list_fields()
                        articletitle = article['title']
                        articleid = article['id']

                        pubtime = article["publishTime"]#在此处获取到文章的发布时间，避免在文章详情获取不到发布时间
                        createtime = article["creationTime"]#在此处获取到文章的创建时间，避免在文章详情获取不创建时间
                        updatetime = article["updateTime"]#在此处获取到文章的更新时间，避免在文章详情获取不到更新时间
                        source = article["source"]#在此处获取到文章的来源，避免在文章详情获取不到来源
                        author = article["author"]#在此处获取到文章的作者，避免在文章详情获取不到作者

                        readnum = article["viewCount"]#在此处获取到文章的阅读数，避免在文章详情获取不到阅读数
                        # articleurl = article["themeUrl"]#在此处获取到文章html地址，避免在文章详情获取不到html地址

                        articleparam["pubtime"] = pubtime#此步骤为存储发布时间
                        articleparam["createtime"] = createtime#此步骤为存储创建时间
                        articleparam["updatetime"] = updatetime#此步骤为存储更新时间
                        articleparam["source"] = source#此步骤为存储文章来源
                        articleparam["author"] = author#此步骤为存储作者
                        articleparam["readnum"] = readnum
                        # articleparam["articleurl"] = articleurl

                        try:
                            coverinfo = article["coverInfo"]
                            articleparam["imageurl"] = coverinfo["url"]
                        except Exception as e:
                            logging.info(f"在文章列表出无法获得封面图{e}")
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["channelname"] = channelname
                        articleparam["channelID"] = channelid
                        articleparam["banner"] = banners

                        articlesparams.append(articleparam)

                except Exception as e:
                    print('eeeee==== ',e, articlelist_json)
            except Exception as e:
                print('eee===== ',e, articlelist_json)
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        """
        组建请求文章详情所需要的数据体
        :param articles:
        :return:
        """
        articlesparam = []
        headers = {
            'token': '',
            'Host': 'rmrbwc.com',
            'Accept-Encoding': 'gzip',
            'Cookie': 'JSESSIONID=C8826175D8C13DEB77A2ECF5F7630E00',
            'User-Agent': 'okhttp/3.9.1',
            'Connection': 'keep-alive'
        }
        data = {}
        method = 'get'
        for articleparam in articles:

            articleid = articleparam.get("articleid")
            url = 'http://rmrbwc.com/rest/themes/' + str(articleid)

            #通过videos 传递url
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
            articleurl = articleparam.get("articleurl")
            # 若APP有关于时间的反爬加sleeptime = 1，若发送为json数据体，则添加articlejson = articlejson
            article = InitClass().article_params_fields(url, headers, method, channelname, imageurl=imgurl, data = data,
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
            # channelid = articleres.get("channelID")
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            banners = articleres.get("banner")
            url = articleres.get("videourl")

            # 若上面存储了此字段需用下列方式获取
            # videos = articleres.get("videos")
            channelid = articleres.get("videocover")
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

            # if articleurl:
            #     fields["url"] = articleurl
            # else:
            #     fields["url"] = url

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
                # articlejson = eval(articleres)
                articlejson = json.loads(json.dumps(json.loads(articleres), indent = 4, ensure_ascii = False))
                # print("articlejson==",articlejson)
                code = articlejson['code']
                if code != 0:
                    print("code != 0")
                    continue

                article = articlejson['payload']

                workerid = article['id']
                title = article['title']  # 标题
                content = article['content']  # 文章内容
                createtime = article['creationTime']
                updatetime = article['updateTime']
                pubtime = article['publishTime']
                readnum = article['viewCount']
                author = article["author"]
                source = article['source']  # 来源
                themeurl = article["themeUrl"]

                fields["url"] = themeurl

                #contentType，作品类型，-1未知，1文字，2图文，3视频文，4纯长视频，5纯短视频，6画廊，7纯音频，8短消息（动态、微头条、微博消息等）
                fields["contentType"] = 1

                fields["readnum"] = readnum  # 文章的阅读数
                fields["appname"] = appname
                fields["title"] = title

                fields["workerid"] = workerid
                fields["source"] = source
                fields["content"] = content
                fields["author"] = author
                #fields["commentnum"] = commentnum
                fields["createtime"] = InitClass().date_time_stamp(createtime)
                fields['updatetime'] = InitClass().date_time_stamp(updatetime)
                fields["pubtime"] = InitClass().date_time_stamp(pubtime)

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

                print("结果==",json.dumps(fields, indent = 4, ensure_ascii = False))
            except Exception as e:
                print('eeeee=',e)

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
    spider = Renminribaowenchuang('人民日报文创')
    spider.run()
