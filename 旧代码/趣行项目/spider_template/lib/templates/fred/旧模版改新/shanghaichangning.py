# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
import requests
from App.appspider_m import Appspider
from App.initclass import InitClass
from lxml import html
from html.parser import HTMLParser
# from lxml import etree

class Shanghaichangning(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "http://www.shcnxwxczx.com/Interface/Channel/listChannel.do"
        # 频道请求头
        headers = {
            "Content-Length": "0",
            "Host": "www.shcnxwxczx.com",
            "User-Agent": "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MuMu Build/V417IR) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Accept-Encoding": "gzip",
            "Connection": "keep-alive"
        }
        # 频道数据体
        data = {
            "key":"homepage"
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
        # print(channelslists)
        channelparams = []

        # channelid = "HomePageGDXW"
        # channelname = "头条"

        # channelid = "IIMDLACCTYDTZDAI"
        # channelname = "专题"

        # channelid = "WYBICCTDOZVFFGYI"
        # channelname = "天下"
        # channelparam = InitClass().channel_fields(channelid, channelname)
        # channelparams.append(channelparam)

        for channel in channelslists['data']:
            channelid = channel['key']
            channelname = channel['title']
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

            url = "http://www.shcnxwxczx.com/Interface/Recodrd/listRecod1.do"
            headers = {
                "Content-Length": "0",
                "Host": "www.shcnxwxczx.com",
                "User-Agent": "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MuMu Build/V417IR) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                "Accept-Encoding": "gzip",
                "Connection": "keep-alive"
            }
            data = {
                "pageNum": "1",
                "getSize": "20",
                "key":channelid,
            }
            method = 'post'

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,channelid = channelid, data = data)
            # 若数据体以json形式发送则以下面方式发送数据上面方式注释
            # articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data,channeljson = channeljson)

            if channelname == "头条":
                url_banner = "http://www.shcnxwxczx.com:8020/MIS/visualization/app/column"  # banner请求接口
                headers_banner = {
                    "Content-Length": "0",
                    "Host": "www.shcnxwxczx.com:8020",
                    "User-Agent": "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MuMu Build/V417IR) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                    "Accept-Encoding": "gzip",
                    "Connection": "keep-alive",
                }
                data_banner = {
                    'channelid': 4,
                }
                articlelist_param_banner = InitClass().articlelists_params_fields(url_banner, headers_banner, method,
                                                                                  channelname,channelid = channelid,
                                                                                  data=data_banner,
                                                                                  banners=1)  # 添加banner请求数据体，或其他接口请求数据
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
            try:
                articlelist_json = json.loads(articlelist_res)
                # 可在下面打印处打断点，查看请求到的数据
                # print("articlelist_json==",articlelist_json)
                #若banner图在articlelist_json中则分来开取并给其复制banner = 1
                try:
                    articlelists = articlelist_json['data']
                    for article in articlelists:
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        articleparam = InitClass().article_list_fields()

                        if "icodata" in article.keys():
                            # print("首页")
                            #首页部分
                            control_id = article['controlId']
                            if control_id == "slider" or control_id == "hot":
                                #banner + hot
                                icodatas = article["icodata"]
                                for banneritem in icodatas:
                                    banners = 1
                                    if control_id == 'hot':
                                        banners = 0

                                    articletitle = banneritem['TITLE']
                                    updatetime = banneritem['updateTime']
                                    imgs = banneritem['IMG']
                                    jumpurl = banneritem['URL']
                                    # print("jumpurl==",jumpurl)
                                    if jumpurl :
                                        res = requests.get(jumpurl)
                                        tree = html.fromstring(res.text)

                                        #定位到文章内容
                                        name = tree.xpath('//div[@class="text"]')
                                        name1 = html.tostring(name[0])
                                        content = HTMLParser().unescape(name1.decode())
                                        # print("banner content==", content)

                                        fields = InitClass().article_fields()
                                        fields["channelID"] = channelid
                                        fields["contentType"] = 1
                                        fields["images"] = []
                                        fields["videos"] = []
                                        fields["videocover"] = []
                                        # fields["width"] = 0
                                        # fields["height"] = 0
                                        fields["pubtime"] = 0
                                        fields["createtime"] = 0

                                        fields["channelname"] = channelname

                                        if imgs:
                                            fields["articlecovers"] = [imgs]
                                        else:
                                            fields["articlecovers"] = []

                                        fields["banner"] = banners
                                        fields["appname"] = "上海长宁"
                                        fields["title"] = articletitle
                                        fields["content"] = content
                                        fields["url"] = jumpurl
                                        fields["updatetime"] = InitClass().date_time_stamp(updatetime)
                                        #print("banneritem==",banneritem)
                                        print("文章==",json.dumps(fields, indent=4, ensure_ascii=False))
                                        continue
                            else:
                                # print("其他banner")
                                #其他banner
                                continue

                        else:
                            # print("普通")
                            articletitle = article['title']
                            #articleid = article['id']

                            jump = article['RecordJumpUrl']
                            recordtype = article['RecordType']
                            videos = article["VideoUrl"]
                            pubtime = article["time"]
                            author = article["companyName"]
                            workerid = article["id"]

                            imgurl = ""
                            try:
                                imgurl = article['img']
                                articleparam["imageurl"] = imgurl
                            except Exception as e:
                                logging.info(f"在文章列表出无法获得封面图{e}")

                            if jump :
                                if recordtype == '1' or recordtype == '2':
                                    #文字，画廊
                                    #此处可获取全部信息
                                    #获取正文
                                    res = requests.get(jump)
                                    tree = html.fromstring(res.text)

                                    # 定位到内容
                                    name = tree.xpath('//div[@class="text"]')
                                    try:
                                        name1 = html.tostring(name[0])
                                        content = HTMLParser().unescape(name1.decode())

                                        fields = InitClass().article_fields()
                                        fields["channelID"] = channelid
                                        fields["createtime"] = 0
                                        fields["updatetime"] = 0
                                        fields["channelname"] = channelname

                                        if recordtype == '1':
                                            fields["contentType"] = 1
                                        elif recordtype == '2':
                                            fields["contentType"] = 6
                                        else:
                                            fields["contentType"] = -1

                                        if imgurl:
                                            fields["articlecovers"] = [imgurl]
                                        else:
                                            fields["articlecovers"] = []

                                        fields["banner"] = 0
                                        fields["appname"] = "上海长宁"
                                        fields["title"] = articletitle
                                        fields["url"] = jump
                                        fields["workerid"] = workerid
                                        fields["content"] = content
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

                                        fields["source"] = author
                                        pubtime = pubtime.rstrip()
                                        fields["pubtime"] = InitClass().date_time_stamp(pubtime)

                                        print("普通文章==",json.dumps(fields, indent=4, ensure_ascii=False))
                                        continue
                                    except Exception as e:
                                        print("e===",e)

                                    continue

                                elif recordtype == '3':
                                    #专题
                                    # print("专题")
                                    articleparam["recordtype"] = '3'
                                    if "http://www.shcnxwxczx.com/news/more" in jump:
                                        # print("内部专题")
                                        paramList = jump.strip().split('?')[1].split('&')
                                        for item in paramList:
                                            key = item.split('=')[0]

                                            if key == "key":
                                                specialkey = item.split('=')[1]
                                                articleparam["specialkey"] = specialkey
                                                articleparam["pubtime"] = pubtime  # 此步骤为存储发布时间
                                                articleparam["channelID"] = channelid
                                                articleparam["articletitle"] = articletitle
                                                articleparam["articleid"] = workerid
                                                articleparam["channelname"] = channelname
                                                articleparam["banner"] = banners
                                                articleparam["articleurl"] = jump
                                                articleparam["region"] = author
                                                # print("articleparam===",articleparam)
                                                articlesparams.append(articleparam)

                                    else:
                                        #外部链接
                                        coverlist = list()
                                        if imgurl:
                                            coverlist.append(imgurl)
                                        pubtime = pubtime.rstrip()
                                        pubtime = InitClass().date_time_stamp(pubtime)

                                        topic_fields = InitClass().topic_fields()
                                        topic_fields["topicID"] = workerid
                                        topic_fields["platformName"] = "上海长宁"
                                        topic_fields["channelName"] = channelname
                                        topic_fields["channelID"] = channelid
                                        topic_fields["topicUrl"] = jump
                                        topic_fields["title"] = articletitle
                                        topic_fields["digest"] = ""
                                        topic_fields["topicCover"] = coverlist
                                        topic_fields["pubTime"] = pubtime
                                        topic_fields["articleNum"] = 0

                                        topic_fields["region"] = author
                                        topic_fields["createTime"] = 0
                                        topic_fields["updateTime"] = 0
                                        print("外链专题==",json.dumps(topic_fields, indent=4, ensure_ascii=False))
                                        continue

                                elif recordtype == '4':
                                    #视频
                                    fields = InitClass().article_fields()
                                    fields["channelID"] = channelid
                                    fields["createtime"] = 0
                                    fields["updatetime"] = 0
                                    fields["channelname"] = channelname

                                    if imgurl:
                                        fields["articlecovers"] = [imgurl]
                                    else:
                                        fields["articlecovers"] = []

                                    fields["banner"] = 0
                                    fields["appname"] = "上海长宁"
                                    fields["title"] = articletitle
                                    fields["url"] = jump
                                    fields["workerid"] = workerid
                                    fields["content"] = ""
                                    fields["videocover"] = []
                                    if videos:
                                        fields["videos"] = [videos]
                                    else:
                                        fields["videos"] = []
                                    fields["images"] = []

                                    fields["source"] = author
                                    pubtime = pubtime.rstrip()
                                    fields["pubtime"] = InitClass().date_time_stamp(pubtime)

                                    print("视频文章==", json.dumps(fields, indent=4, ensure_ascii=False))
                                    continue

                                else:
                                    print("未知类型 recordtype==",recordtype)
                                    continue

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

        for articleparam in articles:

            recordtype = articleparam.get("recordtype")
            specialkey = articleparam.get("specialkey")

            url = "http://changning.chinashadt.com:8020/Interface/Recodrd/listRecod1.do"
            data = {
                "pageNum":1,
                "getSize":20,
                'key': specialkey
            }

            headers = {
                "Host": "changning.chinashadt.com:8020",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "Origin": "http://www.shcnxwxczx.com",
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,en-US;q=0.8",
                "X-Requested-With": "com.msqing.cnnews",
                "Connection": "keep-alive"
            }
            method = 'get'

            articletitle = articleparam.get("articletitle")
            region = articleparam.get("region")


            # 此处代码不需要改动
            channelid = articleparam.get("channelID") #topic
            channelname = articleparam.get("channelname") #topic
            banner = articleparam.get("banner")
            imgurl = articleparam.get("imageurl") #topic
            videos = specialkey #articleparam.get("videos") #topic
            videocover = channelid#articleparam.get("videocover")
            pubtime = articleparam.get("pubtime") #topic
            createtime = articletitle #articleparam.get("createtime") #
            updatetime = region #articleparam.get("updatetime") #
            source = articleparam.get("source")
            author = articleparam.get("author")
            likenum = articleparam.get("likenum")
            commentnum = articleparam.get("commentnum")
            sharenum = articleparam.get("sharenum")
            readnum = articleparam.get("readnum")
            articleurl = articleparam.get("articleurl") #topic
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
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            banners = articleres.get("banner")
            #channelid = articleres.get("channelID")
            # 若上面存储了此字段需用下列方式获取
            # videos = articleres.get("videos")
            channelid = articleres.get("videocover")
            pubtime = articleres.get("pubtime")
            specialkey = articleres.get("videourl")
            articletitle = articleres.get("createtime")
            region = articleres.get("updatetime")
            # likenum = articleres.get("author")
            # commentnum = articleres.get("author")
            # sharenum = articleres.get("sharenum")
            # readnum = articleres.get("readnum")
            # author = articleres.get("author")
            articleurl = articleres.get("articleurl")
            articleres = articleres.get("articleres")

            topiccovers = list()
            if imgurl:
                topiccovers.append(imgurl)

            topic_fields = InitClass().topic_fields()

            topic_fields["topicID"] = specialkey
            topic_fields["platformName"] = appname
            topic_fields["channelName"] = channelname
            topic_fields["channelID"] = channelid
            topic_fields["topicUrl"] = articleurl
            topic_fields["title"] = articletitle
            # topic_fields["digest"] =
            topic_fields["topicCover"] = topiccovers

            pubtime = pubtime.rstrip()
            topic_fields["pubTime"] = InitClass().date_time_stamp(pubtime)
            # topic_fields["articleNum"] =
            # topic_fields["newestArticleID"] =
            topic_fields["region"] = region
            topic_fields["createTime"] = 0
            topic_fields["updateTime"] = 0

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

            topicnum = 0
            newestarticleid = ""
            newestpubtime = 0


            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent = 4, ensure_ascii = False))

                # print("专题列表 articlejson==",articlejson)

                articles = articlejson["data"]
                for article in articles:

                    fields = InitClass().article_fields()
                    fields["appname"] = appname
                    fields["channelname"] = channelname
                    fields["channelID"] = channelid
                    fields["channelType"] = ""

                    fields["specialtopic"] = 1
                    fields["topicid"] = specialkey
                    fields["topicTitle"] = articletitle

                    fields["createtime"] = 0
                    fields["updatetime"] = 0


                    title = article["title"]
                    try:
                        author = article["companyName"]
                        fields["source"] = author
                    except Exception as e:
                        print("eee")

                    pubtime = article["time"]
                    jumpurl = article["RecordJumpUrl"]
                    workerid = article["id"]
                    # article["img"]
                    recordtype = article["RecordType"]

                    aimgurl = article["img"]
                    coverlist = list()
                    if aimgurl:
                        coverlist.append(aimgurl)
                    fields["articlecovers"] = coverlist

                    if jumpurl:
                        fields["url"] = jumpurl
                        if recordtype == '1' or recordtype == '2':
                            # 文字，画廊

                            if recordtype == '1':
                                fields["contentType"] = 1
                            elif recordtype == '2':
                                fields["contentType"] = 6
                            else:
                                fields["contentType"] = -1

                            fields["videocover"] = []

                            content = ""
                            res = requests.get(jumpurl)
                            tree = html.fromstring(res.text)
                            # 定位到内容
                            #div class="rich_media_content " id="js_content" style="visibility: hidden;">
                            name = tree.xpath('//div[@class="text"]')
                            try:
                                name1 = html.tostring(name[0])
                                content = HTMLParser().unescape(name1.decode())
                                fields["content"] = content

                            except Exception as e:
                                name = tree.xpath('//div[@class="rich_media_content "]')
                                try:
                                    name1 = html.tostring(name[0])
                                    content = HTMLParser().unescape(name1.decode())
                                    fields["content"] = content
                                except Exception as e:
                                    print("抓不到正文", e, article)

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

                    fields["appname"] = appname
                    fields["title"] = title
                    fields["workerid"] = workerid
                    # fields["source"] = source
                    # fields["commentnum"] = commentnum
                    pubtime = pubtime.rstrip()
                    pubtime = InitClass().date_time_stamp(pubtime)
                    fields["pubtime"] = pubtime

                    topicnum += 1
                    if int(pubtime) > newestpubtime:
                        newestpubtime = int(pubtime)
                        newestarticleid = workerid

                    print("专题内文章==",json.dumps(fields, indent=4, ensure_ascii=False))

            except Exception as e:
                print("e===",e)
            topic_fields["articleNum"] = topicnum
            topic_fields["newestArticleID"] = newestarticleid

            print("大专题==", json.dumps(topic_fields, indent=4, ensure_ascii=False))


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
    spider = Shanghaichangning('上海长宁')
    spider.run()
