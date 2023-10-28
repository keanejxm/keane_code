# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
import time
from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


class Yangshicaijing(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 请求频道url
        url = "http://cbox.cctv.com/caijing/mobileconfig/index.json"
        # 频道请求头
        headers = {
            "Cache-Control": "no-cache",
            "Host": "cbox.cctv.com",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.11.0",
            "Connection": "keep-alive",
        }
        data = {}
        # 频道数据体
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

        ##### 请求频道的列表
        channelparams = []

        channelid = ""
        channelArr = ["7*24", "banner", "要闻", "直播","微视频","经济之声","交通广播"]
        for channel in channelArr:
            if channel == "7*24":
                channelid = "4617104411729068032"

            elif channel == "banner":
                channelid = "4616246792659402752"

            elif channel == "要闻":
                channelid = "4616194016101269504"

            elif channel == "直播":
                channelid = "4616220404380336128"

            elif channel == "微视频":
                channelid = "4617148392194179072"

            elif channel == "经济之声":
                channelid = "2"
            elif channel == "交通广播":
                channelid = "16"

            channelname = channel
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)

        #cctv2
        for channel in channelslists['data']:
            title = channel["title"]
            if title == "cctv2_lanmu_data":
                channelname = "CCTV2"
                channelid = channel["url"]
                #channelid == http://cbox.cctv.com/caijing/lanmu/index.json
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
        ##### 请求频道列表数据

        articleparams = []
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            banner = 0

            if channelname == "CCTV2":

                url = channelid
                headers = {}
                listJson = {}
                data = {}
                method = 'get'

                channelid = "0"

                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                           channeljson=listJson, banners=banner,channelid=channelid)
                articleparams.append(articlelist_param)

            elif channelname == "经济之声" or channelname == "交通广播":

                url = "https://a0.news.ghwx.com.cn/server/radio/cn/channel"
                headers = {
                    "authority": "a0.news.ghwx.com.cn",
                    "scheme": "https",
                    "x-app-agent": "corp_zx_app",
                    "x-os": "Android",
                    "x-app-aid": "20181130000009",
                    "x-device-type": "USERNAME",
                    "appid": "281",
                    "businesstype": "610001",
                    "accept-encoding": "gzip",
                    "user-agent": "okhttp/3.11.0",
                }
                listJson = {}

                today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
                data = {
                    "channel": channelid,
                    "date": today,
                }
                method = 'get'
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                           channeljson=listJson, banners=banner,channelid=channelid)
                articleparams.append(articlelist_param)

            else:

                url = "https://a0.news.ghwx.com.cn/server/article/list"
                listJson = {}
                headers = {}
                data = {}

                if channelname == "7*24":
                    headers = {
                        "authority": "a0.news.ghwx.com.cn",
                        "scheme": "https",
                        "x-app-agent": "corp_zx_app",
                        "x-os": "Android",
                        "x-app-aid": "20181130000009",
                        "x-device-type": "USERNAME",
                        "appid": "281",
                        "businesstype": "610001",
                        "accept-encoding": "gzip",
                        "user-agent": "okhttp/3.11.0"
                    }
                    data = {
                        "pageSize": "10",
                        "page": "0",
                        "gid": channelid,
                        "version": "1.1",
                        "isParent": "0",
                        "sf": "",
                        "more": "0",
                    }

                elif channelname == "banner":

                    banner = 1
                    headers = {
                        "authority": "a0.news.ghwx.com.cn",
                        "scheme": "https",
                        "accept-encoding": "gzip",
                        "user-agent": "okhttp/3.11.0"
                    }
                    data = {
                        "gid": channelid,
                        "version": "1.1",
                        "page": "0",
                        "pageSize": "5",
                        "sf": ""
                    }

                elif channelname == "要闻":

                    headers = {
                        "authority": "a0.news.ghwx.com.cn",
                        "scheme": "https",
                        "accept-encoding": "gzip",
                        "user-agent": "okhttp/3.11.0",
                        "x-app-agent": "corp_zx_app",
                        "x-os": "Android",
                        "x-app-aid": "20181130000009",
                        "x-device-type": "USERNAME",
                        "appid": "281",
                        "businesstype": "610001",
                    }
                    data = {
                        "gid": channelid,
                        "version": "1.1",
                        "page": "0",
                        "pageSize": "10",
                        "sf": "",
                        "more": "0"
                    }

                elif channelname == "直播":

                    headers = {
                        "authority": "a0.news.ghwx.com.cn",
                        "scheme": "https",
                        "accept-encoding": "gzip",
                        "user-agent": "okhttp/3.11.0",
                        "x-app-agent": "corp_zx_app",
                        "x-os": "Android",
                        "x-app-aid": "20181130000009",
                        "x-device-type": "USERNAME",
                        "appid": "281",
                        "businesstype": "610001",
                    }
                    data = {
                        "gid": channelid,
                        "version": "1.1",
                        "page": "0",
                        "pageSize": "10",
                        "isParent": "0",
                        "more": "0"
                    }

                elif channelname == "微视频":

                    headers = {
                        "authority": "a0.news.ghwx.com.cn",
                        "scheme": "https",
                        "accept-encoding": "gzip",
                        "user-agent": "okhttp/3.11.0",
                        "x-app-agent": "corp_zx_app",
                        "x-os": "Android",
                        "x-app-aid": "20181130000009",
                        "x-device-type": "USERNAME",
                        "appid": "281",
                        "businesstype": "610001",
                    }
                    data = {
                        "gid": channelid,
                        "version": "1.1",
                        "page": "0",
                        "pageSize": "10",
                        "isParent": "0",
                        "more": "0"
                    }

                method = 'get'
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                           channeljson=listJson, banners=banner,channelid=channelid)
                articleparams.append(articlelist_param)
        yield articleparams

    @staticmethod
    def analyze_articlelists(articleslist_ress):
        """
        解析文章列表页，目的是为了获取文章具体信息，组建请求文章详情数据体
        :param articleslist_ress:
        :return:
        """
        ##### 解析新闻列表数据

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
                if channelname == "CCTV2":
                    try:
                        articlelists = articlelist_json['data']
                        itemList = articlelists['itemList']

                        for item in itemList:
                            articleparam = InitClass().article_list_fields()

                            articleparam["channelname"] = channelname
                            articleparam["channelid"] = channelid

                            articletitle = item["title"]
                            articleid = item['vsetId']
                            pubtime = item["publicData"]

                            articleparam["articleid"] = articleid
                            articleparam["articletitle"] = articletitle
                            articleparam["pubtime"] = pubtime

                            articleparam["imageurl"] = item['imgUrl']
                            articlesparams.append(articleparam)

                    except Exception as e:
                        print("abc e==",e)

                    continue

                elif channelname == "经济之声" or channelname == "交通广播":
                    # print("articlelist_json==",articlelist_json)
                    icon = articlelist_json["icon"]
                    articlelists = articlelist_json["program"]

                    for item in articlelists:
                        # print("item===",item)
                        articleparam = InitClass().article_list_fields()

                        articletitle = item["name"]
                        articleid = item["id"]
                        stream = item["stream"]
                        streamurl = ""

                        for streaminfo in stream:
                            uuul = streaminfo["url"]
                            if uuul:
                                streamurl = uuul


                        articleparam["imageurl"] = icon
                        articleparam["streamurl"] = streamurl
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["banner"] = banners
                        articleparam["channelname"] = channelname
                        articleparam["channelid"] = channelid

                        articlesparams.append(articleparam)

                    continue

                #若banner图在articlelist_json中则分来开取并给其复制banner = 1
                try:
                    articlelists = articlelist_json['list']
                    for article in articlelists:
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        #print("article==",article)
                        articleparam = InitClass().article_list_fields()
                        articletitle = article['title']
                        articleid = article['said']

                        try:
                            articleparam["imageurl"] = article['thumbnails']
                        except Exception as e:
                            logging.info(f"在文章列表出无法获得封面图{e}")
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["channelname"] = channelname
                        articleparam["channelid"] = channelid
                        articleparam["banner"] = banners
                        articlesparams.append(articleparam)
                except Exception as e:
                    print('e1==',e, articlelist_json)
            except Exception as e:
                print('e2==',e, articlelist_json)
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        """
        组建请求文章详情所需要的数据体
        :param articles:
        :return:
        """
        #### 请求新闻详情
        # 固定
        uid = "6297273747340541952"
        articlesparam = []
        url = 'https://a0.news.ghwx.com.cn/server/article/load'
        headers = {
            "authority": "a0.news.ghwx.com.cn",
            "scheme": "https",
            "accept": "*/*",
            "origin": "https://s0.news.ghwx.com.cn",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 yscj/2020040310 vn/V2.1.1 netType/wifi vendor/4611804765687382016",
            "accept-encoding": "gzip, deflate",
            "accept-language": "zh-CN,en-US;q=0.8",
            "x-requested-with": "com.cctv.caijing",
        }
        method = 'get'

        #print("articles ==",articles)
        for articleparam in articles:

            articleid = articleparam.get("articleid")
            channelname = articleparam.get("channelname")
            channelid = articleparam.get("channelid")

            if channelname == "CCTV2":
                url = 'http://api.cntv.cn/video/videolistById'
                headers = {
                    "Cache-Control": "no-cache",
                    "Host": "api.cntv.cn",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.11.0",
                    "Connection": "keep-alive",
                }
                data = {
                    "vsid": articleid,
                    "serviceId": "cbox",
                    "em": "01",
                    "p": "1",
                    "n": "4",
                    "o": "desc"
                }

            elif channelname == "经济之声" or channelname == "交通广播":

                # print("articleparam ==", articleparam)
                # appname = articleres.get("appname")
                title = articleparam["articletitle"]
                articleid = articleparam["articleid"]
                channelname = articleparam["channelname"]
                channelid = articleparam["channelid"]
                banners = articleparam["banner"]
                imageurl = articleparam["imageurl"]
                streamurl = articleparam["streamurl"]

                fields = InitClass().article_fields()
                fields["channelname"] = channelname
                fields["channelID"] = channelid
                fields["url"] = streamurl


                if imageurl:
                    fields["articlecovers"] = [imageurl]

                fields["banner"] = banners
                fields["appname"] = "央视财经"
                fields["title"] = title
                # fields["url"] = url
                fields["workerid"] = articleid
                #fields["stream"] = stream
                fields["images"] = []
                fields["videos"] = []
                fields["videocover"] = []
                fields["pubtime"] = 0
                fields["createtime"] = 0
                fields["updatetime"] = 0

                print("音频文章==",json.dumps(fields, indent=4, ensure_ascii=False))
                continue
            else:
                data = {
                    "aid": articleid,
                    "uid": uid
                }
                # 此处代码不需要改动
                # channelname = articleparam.get("channelname")
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
            articleurl = articleparam.get("articleurl")
            # 若APP有关于时间的反爬加sleeptime = 1，若发送为json数据体，则添加articlejson = articlejson
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                        videourl=videos, videocover=videocover, pubtime=pubtime,
                                                        createtime=createtime, updatetime=updatetime,
                                                        source=source, author=author, likenum=likenum,
                                                        commentnum=commentnum, sharenum=sharenum, readnum=readnum,
                                                        articleurl=articleurl, banners=banner)
            articlesparam.append(article)

        yield articlesparam

    @staticmethod
    def analyzearticles(articles_res):
        # 解析新闻详情

        for articleres in articles_res:
            channelname = articleres.get("channelname")
            channelid = articleres.get("videourl")
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            banners = articleres.get("banner")
            # 若上面存储了此字段需用下列方式获取
            # videos = articleres.get("videos")
            # videocover = articleres.get("videocover")
            pubtime = articleres.get("pubtime")
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

            if imgurl:
                fields["articlecovers"] = [imgurl]

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
            fields["pubtime"] = pubtime #文章的发布时间
            # fields["createtime"] = createtime #文章的发布时间
            # fields["updatetime"] = updatetime #文章的更新时间
            # fields["likenum"] = likenum #文章的点赞数
            # fields["playnum"] = playnum #视频的播放数
            # fields["commentnum"] = commentnum #文章评论数
            # fields["readnum"] = readnum #文章的阅读数
            # fields["trannum"] = trannum #文章的转发数
            # fields["sharenum"] = sharenum #文章分享数
            # fields["author"] = author #文章作者
            if channelname == "CCTV2":
                try:
                    articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                    # print("articlejson==",articlejson)
                    videosets = articlejson["videoset"]

                    videosetinfo = videosets["0"]

                    # video = articles['videoUrl']
                    # height = articles['videoHeight']
                    # width = articles['videoWidth']

                    title = videosetinfo['name']

                    workerid = videosetinfo['vsid']
                    url = videosetinfo["url"]
                    # desc = videosetinfo["desc"]

                    pubtime = InitClass().date_time_stamp(pubtime)

                    fields["appname"] = appname
                    fields["title"] = title
                    fields["url"] = url
                    fields["workerid"] = workerid
                    fields["pubtime"] = pubtime
                    fields["updatetime"] = 0
                    fields["createtime"] = 0
                    fields["videocover"] = []
                    fields["videos"] = []
                    fields["images"] = []

                    print("cctv2 文章===",json.dumps(fields, indent=4, ensure_ascii=False))

                except Exception as e:
                    print("eeee33==", e)
                continue
            elif channelname == "经济之声" or channelname == "交通广播":
                #print("articleres ==",articleres)
                continue
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent = 4, ensure_ascii = False))
                # print("articlejson==",articlejson)

                article = articlejson["article"]

                videourl = article['videoUrl']
                videolist = list()
                if videourl:
                    videolist.append(videourl)


                imagejson = article["images"]
                imageobject = json.loads(imagejson)
                contentimages = list()
                for imginfo in imageobject:
                    imgurlll = imginfo["original"]
                    contentimages.append(imgurlll)


                height = article['videoHeight']
                width = article['videoWidth']

                title = article['title']  # 标题
                source = article['from']  # 来源
                content = article['body']  # 文章内容

                updatetime = article["lasTime"]
                pubtime = article['pubTime']
                createtime = article["addTime"]

                workerid = article['said']
                url = article["urlShare"]
                commentnum = article["commentCount"]

                fields["appname"] = appname
                fields["title"] = title
                fields["url"] = url
                fields["workerid"] = workerid
                fields["source"] = source
                fields["content"] = content

                fields["width"] = width
                fields["height"] = height

                fields["createtime"] = createtime
                fields["pubtime"] = pubtime
                fields["updatetime"] = updatetime
                fields["commentnum"] = commentnum

                # try:
                #     videos = InitClass().get_video(content)
                #     fields["videos"] = videos
                # except Exception as e:
                #     print("无视频")
                fields["videocover"] = []

                fields["videos"] = videolist
                fields["images"] = contentimages

                # try:
                #     images = InitClass().get_images(content)
                #     fields["images"] = images
                # except Exception as e:
                #     print("无图片")

                print("文章===",json.dumps(fields, indent = 4, ensure_ascii = False))
            except Exception as e:
                print("eeee==",e)

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
    spider = Yangshicaijing('央视财经')
    spider.run()
