# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
# from App.appspider_m import Appspider
# from App.initclass import InitClass

from App.spider_analy_model.jiu.appspider_m import Appspider
from App.spider_analy_model.jiu.initclass import InitClass

#pip install requests-toolbelt
from requests_toolbelt import MultipartEncoder


class Wenyiyun(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "http://wenyizhiku.artnchina.com/microinformation/app/homepage/info"
        # 频道请求头
        headers = {
            "Host": "wenyizhiku.artnchina.com",
            "Content-Length": "44",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Origin": "http://wenyiyun.artnchina.com",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
            "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary46BMpTcX4pjteJTS",
            "Accept": "*/*",
            "Referer": "http://wenyiyun.artnchina.com/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,en-US;q=0.8",
            "Cookie": "groupId=zgwl.microinfo; JSESSIONID=FD65F52EF342E9CB664124DA764D775B",
            "X-Requested-With": "com.artnchina.wenyiyun",
            "Connection": "keep-alive",
        }
        # 频道数据体
        data = {}
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
        for channel in channelslists['data']['topicList']:
            channelcount = channel['blogCount']
            if channelcount < 10:
                #有测试的频道，在app上也未显示
                continue
            channelid = channel['topicId']
            channelname = channel['title']
            channeltype = channel['hasCarousel']
            channelparam = InitClass().channel_fields(channelid, channelname,channeltype=channeltype)
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
            has_banner = channel.get("channeltype")

            method = 'post'
            # 若有两个请求接口则如下： 例如：banner列表和文章列表时两个请求接口
            if has_banner:
                url_banner = "http://wenyizhiku.artnchina.com/microinformation/app/blogtopic/carousel"

                data_banner = MultipartEncoder(
                    fields={
                        'topicId': channelid,
                    }
                )

                json_banner = {
                    "groupId":"zgwl.microinfo"
                }

                headers_banner = {
                    "Host": "wenyizhiku.artnchina.com",
                    "Content-Length": "792",
                    "Pragma": "no-cache",
                    "Cache-Control": "no-cache",
                    "Origin": "http://wenyiyun.artnchina.com",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
                    "Accept": "*/*",
                    "Referer": "http://wenyiyun.artnchina.com/",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,en-US;q=0.8",
                    "Cookie": "groupId=zgwl.microinfo; JSESSIONID=FD65F52EF342E9CB664124DA764D775B",
                    "X-Requested-With": "com.artnchina.wenyiyun",
                    "Connection": "keep-alive",
                    "Content-Type": data_banner.content_type
                }

                # banner请求接口
                articlelist_param_banner = InitClass().articlelists_params_fields(url_banner, headers_banner, method,
                                                                                  channelname, channel_id = channelid,
                                                                                  data=data_banner,
                                                                                  channeljson=json_banner,
                                                                                  banners=1)
                articleparams.append(articlelist_param_banner)

            url = "http://wenyizhiku.artnchina.com/microinformation/app/blogtopic/bloglist"
            data = MultipartEncoder(
                fields={
                    'authorId': '',
                    'typeId': channelid,
                    'topicId': channelid,
                    'history': '',
                    'pageSize': '10',
                    'pageNum': '1',
                    'type': 'micro_information'}
            )
            headers = {
                "Host": "wenyizhiku.artnchina.com",
                "Content-Length": "792",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "Origin": "http://wenyiyun.artnchina.com",
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
                "Accept": "*/*",
                "Referer": "http://wenyiyun.artnchina.com/",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,en-US;q=0.8",
                "Cookie": "groupId=zgwl.microinfo; JSESSIONID=FD65F52EF342E9CB664124DA764D775B",
                "X-Requested-With": "com.artnchina.wenyiyun",
                "Connection": "keep-alive",
                "Content-Type": data.content_type
            }
            channel_json = {
                "groupId": "zgwl.microinfo",
                "JSESSIONID": "FD65F52EF342E9CB664124DA764D775B"
            }

              # 添加banner请求数据体，或其他接口请求数据
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, channel_id = channelid, data = data,channeljson=channel_json)
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
            channelid = articleslist_res.get("channelID")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                # 可在下面打印处打断点，查看请求到的数据
                #print("articlelist_json==",articlelist_json)
                #若banner图在articlelist_json中则分来开取并给其复制banner = 1

                if banners == 1:
                    #banner
                    try:
                        articlelists = articlelist_json['data']
                        for article in articlelists:
                            # print("banner = ", article)
                            articleparam = InitClass().article_list_fields()

                            articletitle = article['title']
                            blogurl = article['blogUrl']

                            start = blogurl.rindex('/')
                            articleid = blogurl[start + 1:]

                            imageurl = article['imgUrl']

                            articleparam["articleid"] = articleid
                            articleparam["articletitle"] = articletitle
                            articleparam["imageurl"] = imageurl

                            articleparam["channelname"] = channelname
                            articleparam["channelID"] = channelid
                            articleparam["articleurl"] = blogurl

                            articleparam["banner"] = banners
                            articlesparams.append(articleparam)
                    except Exception as e:
                        print("eee==",e)

                else:
                    #列表
                    try:
                        articlelists = articlelist_json['data']['blogList']
                        for article in articlelists:
                            # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                            # print("article==",article)

                            articleparam = InitClass().article_list_fields()
                            articletitle = article['title']
                            articleid = article['blogId']
                            videos = article["videoUrl"] #在此处获取到文章视频url，避免在文章详情获取不到视频链接，数据类型list
                            # videocover = article["videocover"]#在此处获取到文章视频封面图，避免在文章详情获取不到视频封面图链接，数据类型list
                            # pubtime = article["pubtime"]#在此处获取到文章的发布时间，避免在文章详情获取不到发布时间
                            createtime = article["createTime"]#在此处获取到文章的创建时间，避免在文章详情获取不创建时间
                            # updatetime = article["updatetime"]#在此处获取到文章的更新时间，避免在文章详情获取不到更新时间
                            source = article["source"]#在此处获取到文章的来源，避免在文章详情获取不到来源
                            author = article["author"]#在此处获取到文章的作者，避免在文章详情获取不到作者
                            # likenum = article["likenum"]#在此处获取到文章的点赞数，避免在文章详情获取不到点赞数
                            commentnum = article["commentCount"]#在此处获取到文章的评论数，避免在文章详情获取不到评论数
                            # sharenum = article["sharenum"]#在此处获取到文章的评论数，避免在文章详情获取不到评论数
                            # readnum = article["readnum"]#在此处获取到文章的阅读数，避免在文章详情获取不到阅读数
                            #articleurl = article["articleurl"]#在此处获取到文章html地址，避免在文章详情获取不到html地址
                            # detailurl = article["detailURL"]
                            # print("detailurl==",detailurl)
                            articleparam["video"] = videos #此步骤为存储视频url
                            # articleparam["videocover"] = videocover#此步骤为存储视频封面
                            # articleparam["pubtime"] = pubtime#此步骤为存储发布时间
                            articleparam["createtime"] = createtime#此步骤为存储创建时间
                            # articleparam["updatetime"] = updatetime#此步骤为存储更新时间
                            articleparam["source"] = source#此步骤为存储文章来源
                            articleparam["author"] = author#此步骤为存储作者
                            # articleparam["likenum"] = likenum#此步骤为存储点赞数
                            # articleparam["commentnum"] = commentnum#此步骤为存储评论数
                            try:
                                articleparam["imageurl"] = article['imgUrl'][0]
                            except Exception as e:
                                logging.info(f"在文章列表出无法获得封面图{e}")
                            articleparam["articleid"] = articleid
                            articleparam["articletitle"] = articletitle
                            articleparam["channelname"] = channelname
                            articleparam["channelID"] = channelid
                            articleparam["banner"] = banners
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
        url = 'http://wenyizhiku.artnchina.com/microinformation/app/blog/detail'

        method = 'post'

        detail_josn = {
            "groupId":"zgwl.microinfo"
        }

        for articleparam in articles:
            banner = articleparam.get("banner")

            articleid = articleparam.get("articleid")

            data = MultipartEncoder(
                fields={
                    'blogId': articleid,
                }
            )

            headers = {
                "Host": "wenyizhiku.artnchina.com",
                "Content-Length": "146",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "Origin": "http://wenyiyun.artnchina.com",
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
                "Accept": "*/*",
                "Referer": "http://wenyiyun.artnchina.com/",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,en-US;q=0.8",
                "Cookie": "groupId=zgwl.microinfo",
                "X-Requested-With": "com.artnchina.wenyiyun",
                "Connection": "keep-alive",
                "Content-Type": data.content_type
            }
            #通过videos 传递url
            videos = url

            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
            channelid = articleparam.get("channelID")
            imgurl = articleparam.get("imageurl")
            #videos = articleparam.get("videos")
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
            article = InitClass().article_params_fields(url, headers, method, channelname,channel_id = channelid, imageurl = imgurl, data = data,articlejson=detail_josn,
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
            #fields["imageurl"] = imgurl
            fields["banner"] = banners
            # 如果有下列字段需添加
            if articleurl:
                fields["url"] = articleurl
            else:
                fields["url"] = url #文章的html网址，提取shareurl
            # fields["workerid"] = workerid #文章的id
            # fields["title"] = title #文章的标题
            # fields["content"] = content #文章的内容详情
            if imgurl:
                fields["articlecovers"] = [imgurl] #文章的封面，一般为上面get到的字段
            else:
                fields["articlecovers"] = []
            #fields["images"] = []#iamges #文章详情内的图片url，一般为列表需遍历获取
            # fields["videos"] = #videos #文章的视频链接地址
            fields["videocover"] = []#videocover #文章的视频封面地址
            # fields["width"] = width #文章的视频宽
            # fields["height"] = height #文章的视频高
            # fields["source"] = source #文章的来源
            fields["pubtime"] = 0#pubtime #文章的发布时间
            # fields["createtime"] = createtime #文章的发布时间
            fields["updatetime"] = 0#updatetime #文章的更新时间
            # fields["likenum"] = likenum #文章的点赞数
            # fields["playnum"] = playnum #视频的播放数
            # fields["commentnum"] = commentnum #文章评论数
            # fields["readnum"] = readnum #文章的阅读数
            # fields["trannum"] = trannum #文章的转发数
            # fields["sharenum"] = sharenum #文章分享数
            # fields["author"] = author #文章作者

            articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
            #print(articlejson)

            try:
                articledetail = articlejson['data']['blog']
                #print("articledetail==",articledetail)
                title = articledetail['blogTitle']  # 标题
                source = articledetail['source']  # 来源
                content = articledetail['blogContent']  # 文章内容
                workerid = articledetail['blogId']
                author = articledetail["author"]
                commentnum = articledetail["commentCount"]
                createtime = articledetail["createDate"]
                videos = articledetail["videoUrl"]

                #contentType，作品类型，-1未知，1文字，2图文，3视频文，4纯长视频，5纯短视频，6画廊，7纯音频，8短消息（动态、微头条、微博消息等）
                fields["contentType"] = 1

                fields["appname"] = appname
                fields["title"] = title
                fields["workerid"] = workerid
                fields["source"] = source
                fields["content"] = content
                fields["author"] = author
                fields["commentnum"] = commentnum
                fields["createtime"] = createtime

                try:
                    contentvideos = InitClass().get_video(content)
                    if not videos in contentvideos and videos:
                        contentvideos.append(videos)
                    fields["videos"] = contentvideos
                except Exception as e:
                    print("正文无视频")

                try:
                    images = InitClass().get_images(content)
                    fields["images"] = images
                except Exception as e:
                    print("正文无图片")


                print("结果==",json.dumps(fields, indent=4, ensure_ascii=False))
            except Exception as e:
                print("eeeee=",e)

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
    spider = Wenyiyun('文艺云')
    spider.run()
