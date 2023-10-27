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
        print(channelslists)
        channelparams = []
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

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,channel_id = channelid, data = data)
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
                                                                                  channelname,channel_id = channelid,
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
            channelid = articleslist_res.get("channelID")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                # 可在下面打印处打断点，查看请求到的数据
                # print(articlelist_json)
                #若banner图在articlelist_json中则分来开取并给其复制banner = 1
                try:
                    articlelists = articlelist_json['data']
                    for article in articlelists:
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        articleparam = InitClass().article_list_fields()

                        if "icodata" in article.keys():

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
                                        print(json.dumps(fields, indent=4, ensure_ascii=False))
                                        continue
                            else:
                                #其他banner
                                continue
                        else:
                            #print("普通")
                            articletitle = article['title']
                            articleid = article['id']

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
                                    res = requests.get(jump)
                                    tree = html.fromstring(res.text)

                                    # 定位到内容
                                    name = tree.xpath('//div[@class="text"]')

                                    try:
                                        name1 = html.tostring(name[0])
                                        content = HTMLParser().unescape(name1.decode())

                                        fields = InitClass().article_fields()
                                        fields["channelID"] = channelid
                                        fields["images"] = []
                                        fields["videos"] = []
                                        fields["videocover"] = []
                                        # fields["width"] = 0
                                        # fields["height"] = 0
                                        fields["createtime"] = 0
                                        fields["updatetime"] = 0

                                        if recordtype == '1':
                                            fields["contentType"] = 1
                                        elif recordtype == '2':
                                            fields["contentType"] = 6
                                        else:
                                            fields["contentType"] = -1

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
                                        fields["content"] = content
                                        fields["author"] = author
                                        pubtime = pubtime.rstrip()
                                        fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                                        print(json.dumps(fields, indent=4, ensure_ascii=False))
                                        continue
                                    except Exception as e:
                                        print("e===",e)

                                elif recordtype == '3':
                                    #专题
                                    articleparam["recordtype"] = '3'
                                    if "http://www.shcnxwxczx.com/news/more" in jump:
                                        paramList = jump.strip().split('?')[1].split('&')
                                        for item in paramList:
                                            key = item.split('=')[0]

                                            if key == "key":
                                                specialkey = item.split('=')[1]

                                                articleparam["specialkey"] = specialkey
                                    else:
                                        #外部链接
                                        fields = InitClass().article_fields()
                                        fields["channelID"] = channelid

                                        fields["images"] = []
                                        fields["videos"] = []
                                        fields["videocover"] = []
                                        # fields["width"] = 0
                                        # fields["height"] = 0
                                        fields["createtime"] = 0
                                        fields["updatetime"] = 0

                                        fields["contentType"] = -1
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
                                        fields["content"] = jump
                                        fields["author"] = author
                                        pubtime = pubtime.rstrip()
                                        fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                                        print(json.dumps(fields, indent=4, ensure_ascii=False))
                                        continue
                                else:
                                    print("未知类型")
                                    continue

                            # print("jump===",jump)
                            # res = requests.get(jump)
                            # tree = html.fromstring(res.text)
                            # name = tree.xpath('//body/div[@class="container"]/div[@class="row"]')
                            # name1 = html.tostring(name[0])
                            # name2 = HTMLParser().unescape(name1.decode())
                            # print("name2==",name2)

                            # videos = article["VideoUrl"] #在此处获取到文章视频url，避免在文章详情获取不到视频链接，数据类型list
                            # videocover = article["videocover"]#在此处获取到文章视频封面图，避免在文章详情获取不到视频封面图链接，数据类型list
                            # pubtime = article["time"]#在此处获取到文章的发布时间，避免在文章详情获取不到发布时间
                            # createtime = article["createtime"]#在此处获取到文章的创建时间，避免在文章详情获取不创建时间
                            # updatetime = article["updatetime"]#在此处获取到文章的更新时间，避免在文章详情获取不到更新时间
                            # source = article["source"]#在此处获取到文章的来源，避免在文章详情获取不到来源
                            # author = article["companyName"]#在此处获取到文章的作者，避免在文章详情获取不到作者
                            # likenum = article["likenum"]#在此处获取到文章的点赞数，避免在文章详情获取不到点赞数
                            # commentnum = article["commentnum"]#在此处获取到文章的评论数，避免在文章详情获取不到评论数
                            # sharenum = article["sharenum"]#在此处获取到文章的评论数，避免在文章详情获取不到评论数
                            # readnum = article["readnum"]#在此处获取到文章的阅读数，避免在文章详情获取不到阅读数
                            # articleurl = article["articleurl"]#在此处获取到文章html地址，避免在文章详情获取不到html地址
                            articleparam["video"] = videos #此步骤为存储视频url
                            # articleparam["videocover"] = videocover#此步骤为存储视频封面
                            articleparam["pubtime"] = pubtime#此步骤为存储发布时间
                            # articleparam["createtime"] = createtime#此步骤为存储创建时间
                            # articleparam["updatetime"] = updatetime#此步骤为存储更新时间
                            # articleparam["source"] = source#此步骤为存储文章来源
                            # articleparam["author"] = author#此步骤为存储作者
                            # articleparam["likenum"] = likenum#此步骤为存储点赞数
                            # articleparam["commentnum"] = commentnum#此步骤为存储评论数
                            articleparam["channelID"] = channelid
                            articleparam["articletitle"] = articletitle
                            articleparam["articleid"] = articleid
                            articleparam["channelname"] = channelname
                            articleparam["banner"] = banners
                            articleparam["articleurl"] = jump
                            # print("articleparam==",articleparam)
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

            # 此处代码不需要改动
            channelid = articleparam.get("channelID")
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
            articleurl = articleparam.get("articleurl")
            # 若APP有关于时间的反爬加sleeptime = 1，若发送为json数据体，则添加articlejson = articlejson
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl,channel_id = channelid, data = data,
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
            channelid = articleres.get("channelID")
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
            fields["url"] = articleurl

            if imgurl:
                fields["articlecovers"] = [imgurl]
            else:
                fields["articlecovers"] = []

            fields["banner"] = banners
            fields["images"] = []
            fields["videos"] = []
            fields["videocover"] = []
            # fields["width"] = 0
            # fields["height"] = 0
            fields["createtime"] = 0
            fields["updatetime"] = 0

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
                # print("articlejson==",articlejson)

                articles = articlejson["data"]
                for article in articles:
                    title = article["title"]
                    try:
                        author = article["companyName"]
                        fields["author"] = author
                    except Exception as e:
                        print("eee")

                    pubtime = article["time"]
                    jumpurl = article["RecordJumpUrl"]
                    workerid = article["id"]
                    # article["img"]
                    recordtype = article["RecordType"]

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
                                    print("e===", e, article)




                    # title = articlejson['data']['title']  # 标题
                    # source = articlejson['data']['origin']  # 来源
                    # content = articlejson['data']['txt']  # 文章内容
                    # pubtime = articlejson['data']['date']  # 发布时间
                    # workerid = articlejson['data']['id']
                    # url = articlejson['data']["shareUrl"]
                    # author = articlejson['data']["author"]
                    # commentnum = articlejson['data']["comments"]
                    fields["appname"] = appname
                    fields["title"] = title
                    fields["workerid"] = workerid
                    # fields["source"] = source
                    # fields["commentnum"] = commentnum
                    pubtime = pubtime.rstrip()
                    fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                    print(json.dumps(fields, indent=4, ensure_ascii=False))
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
    spider = Shanghaichangning('上海长宁')
    spider.run()
