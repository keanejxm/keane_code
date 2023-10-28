# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
from appspider_m import Appspider
from initclass import InitClass


class Wuxiguanchanews(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "http://wap.wxgc.wxrb.com/api/mchannel/getChildChannelByCode"
        # 频道请求头
        headers = {
            "signature":"194220e595025fb9d6cf9b036ad27248",
            "Content-Type":"application/x-www-form-urlencoded; charset=utf-8",
            "Content-Length":"123",
            "Host":"wap.wxgc.wxrb.com",
            "Connection":"Keep-Alive",
            "Accept-Encoding":"gzip",
            "Cookie":"JSESSIONID=5A345A5EDE736CFF2DA3E913A5B3FB98",
            "User-Agent":"okhttp/3.12.1",
        }
        # 频道数据体
        data = {
            "timestamp":"1608100499710",
            "siteId":"BDF761C7DFF141B486E34383312E1708",
            "sign":"b1feeff36eed89c24993e9f070c5fe64",
            "platform":"app",
            "code":"top",
        }
        # 如果携带的是json数据体,用appjson发送
        # app_json = {}
        # 频道请求方式
        method = "post"
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
        for channel in channelslists['data']['children']:
            channelid = channel['id']
            channelname = channel['name']
            channeltype = channel['alias']
            if channelname == '活动' or channelname == '专题' or channelname == '直播':
                channelname = channel['name']
            else:
                channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channeltype)
                channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistsparams(channelsparams):
        """
        此方法目的是组建请求文章列页面数据参数，url，headers，data，若以json形式发送数据，则channeljson = channeljson
        :param channelsparams:
        :return:
        """
        print(channelsparams)
        articleparams = []
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")
            if channelname == '视频':
                url = 'http://wap.wxgc.wxrb.com/api/mcontent/getContentList'
                headers = {
                    "signature":"831e7a8cadcf3a3f25419cea1fbcd4d8",
                    "Content-Type":"application/x-www-form-urlencoded; charset=utf-8",
                    "Content-Length":"192",
                    "Host":"wap.wxgc.wxrb.com",
                    "Connection":"Keep-Alive",
                    "Accept-Encoding":"gzip",
                    "Cookie":"JSESSIONID=50E063554B8E6F6AAA8118AF96454E34",
                    "User-Agent":"okhttp/3.12.1",
                }
                data = {
                    "platform":"app",
                    "channelId":"3247F7DAC2234AE39C90C5B5B1C115E2",
                    "sign":"2d6d82e82dec9c8b418a6788c291b378",
                    "pageSize":"10",
                    "contentType":"0",
                    "timestamp":"1608107161924",
                    "siteId":"BDF761C7DFF141B486E34383312E1708",
                    "pageNo":"1",
                }
                method = 'post'
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data, channel_id=channelid)
                # 若数据体以json形式发送则以下面方式发送数据上面方式注释
                # articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data,channeljson = channeljson)
                articleparams.append(articlelist_param)
            elif channelname == '直播':
                url = 'http://wap.wxgc.wxrb.com/api/mcontent/getContentList'
                headers = {
                    "signature":"6735c8b7ae328ea81ce66a4888673c20",
                    "Content-Type":"application/x-www-form-urlencoded; charset=utf-8",
                    "Content-Length":"192",
                    "Host":"wap.wxgc.wxrb.com",
                    "Connection":"Keep-Alive",
                    "Accept-Encoding":"gzip",
                    "Cookie":"JSESSIONID=CA821593F5EB62925EAB885244BC5900",
                    "User-Agent":"okhttp/3.12.1",
                }
                data = {
                    "platform": "app",
                    "channelId": "B8E0C8C22FC3498280660BB11F6DBF7D",
                    "sign": "290bad192f6facab55a02d114ddaf3a7",
                    "pageSize": "10",
                    "contentType": "0",
                    "timestamp": "1608107183039",
                    "siteId": "BDF761C7DFF141B486E34383312E1708",
                    "pageNo": "1",
                }
                method = 'post'
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,channel_id=channelid)
                # 若数据体以json形式发送则以下面方式发送数据上面方式注释
                # articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data,channeljson = channeljson)
                articleparams.append(articlelist_param)
            else:
                url = f"http://wap.wxgc.wxrb.com/pages/json/{channeltype}/list.json"
                headers = {
                    "signature":"4f7d1f459a6aae3f25d05a755b519d98",
                    "random":"999",
                    "Host":"wap.wxgc.wxrb.com",
                    "Connection":"Keep-Alive",
                    "Accept-Encoding":"gzip",
                    "Cookie":"JSESSIONID=963FB27CFA3222E34D2CAD5506D58464",
                    "User-Agent":"okhttp/3.12.1",
                }
                data = {}
                method = 'get'
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data,channel_id=channelid)
                # 若数据体以json形式发送则以下面方式发送数据上面方式注释
                # articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data,channeljson = channeljson)
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
            channelID = articleslist_res.get("channelID")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                print(articlelist_json)
                if channelname == '视频' or channelname == '直播':
                    try:
                        articlelists = articlelist_json['list']
                    except Exception as e:
                        print(e, articlelist_json)
                else:
                    try:
                        articlelists = articlelist_json['contents']
                    except Exception as e:
                        print(e, articlelist_json)
                for article in articlelists:
                    print(article)
                    articleparam = InitClass().article_list_fields()
                    articletitle = article['title']
                    articleid = article['id']
                    subjectId = article['siteId']
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
                    try:
                        articleparam["imageurl"] = []
                        if 'mCoverImg' in article.keys():
                            img = list()
                            img.append(article['mCoverImg'])
                            articleparam["imageurl"] = img
                    except Exception as e:
                        print(e)
                    articleparam["subjectId"] = subjectId
                    articleparam["articleid"] = articleid
                    articleparam["articletitle"] = articletitle
                    articleparam["channelname"] = channelname
                    articleparam["channelID"] = channelID
                    articleparam["banner"] = banners
                    articlesparams.append(articleparam)
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
        url = 'http://wap.wxgc.wxrb.com/api/mcontent/getArticleDetails'
        headers = {
            "Content-Type":"application/x-www-form-urlencoded; charset=utf-8",
            "Content-Length":"147",
            "Host":"wap.wxgc.wxrb.com",
            "Connection":"Keep-Alive",
            "Accept-Encoding":"gzip",
            "Cookie":"JSESSIONID=30274E0A7D24C7D73F6C14FC23424ACE",
            "User-Agent":"okhttp/3.12.1",
        }
        method = 'post'
        for articleparam in articles:
            data = {
                "appid":"490000000245552",
                "platform":"app",
                "timestamp":"1608109467032",
                "contentId":articleparam.get("articleid"),
                "userId":"",
            }
            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
            channelID = articleparam.get("channelID")
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
            articleurl = articleparam.get("articleurl")
            # 若APP有关于时间的反爬加sleeptime = 1，若发送为json数据体，则添加articlejson = articlejson
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data = data,
                                                        videourl = videos, videocover = videocover, pubtime = pubtime,
                                                        createtime = createtime, updatetime = updatetime,
                                                        source = source, author = author, likenum = likenum,
                                                        commentnum = commentnum, sharenum = sharenum, readnum = readnum,
                                                        articleurl = articleurl,banners = banner,channel_id = channelID)
            articlesparam.append(article)
        yield articlesparam

    @staticmethod
    def analyzearticles(articles_res):
        for articleres in articles_res:
            channelID = articleres.get("channelID")
            channelname = articleres.get("channelname")
            imgurl = articleres.get("imageurl")
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
            fields["channelID"] = channelID
            fields["images"] = imgurl
            fields["articlecovers"] = imgurl
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
                print(articlejson)
                # if channelname == '直播':
                #     title = articlejson['title']  # 标题
                #     pubtime = articlejson['publishTime']  # 发布时间
                #     workerid = articlejson['id']
                #     url = articlejson["url"]
                #     author = articlejson["userName"]
                #     fields["appname"] = appname
                #     fields["title"] = title
                #     fields["url"] = url
                #     fields["workerid"] = workerid
                #     fields["author"] = author
                #     fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                # else:
                title = articlejson['title']  # 标题
                content = articlejson['txt']  # 文章内容
                # images = InitClass().get_images(content, type=1)
                # fields["images"] = images  # 文章评论数
                pubtime = articlejson['publishTime']  # 发布时间
                createtime = articlejson['createtime']
                workerid = articlejson['id']
                url = articlejson["url"]
                author = articlejson["userName"]
                likenum = articlejson["praiseCount"]
                commentnum = articlejson["commentCount"]
                if 'moVideoPath' in articlejson.keys() and articlejson['moVideoPath'] != '':
                    videos = list()
                    videocover = list()
                    videos.append(articlejson['moVideoPath'])  # 文章的视频链接地址
                    videocover.append(articlejson['mCoverImg'])  # 文章的视频封面地址
                    fields["videos"] = videos
                    fields["videocover"] = videocover
                    fields["contentType"] = 4
                else:
                    fields["contentType"] = 2
                if 'sourceName' in articlejson.keys():
                    source = articlejson['sourceName']  # 来源
                    fields["source"] = source
                fields["appname"] = appname
                fields["title"] = title
                fields["url"] = url
                fields["workerid"] = workerid
                fields["content"] = content
                fields["author"] = author
                fields["likenum"] = likenum
                fields["commentnum"] = commentnum
                fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                fields["createtime"] = InitClass().date_time_stamp(createtime)
                print(json.dumps(fields, indent = 4, ensure_ascii = False))
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
    spider = Wuxiguanchanews('无锡观察')
    spider.run()
