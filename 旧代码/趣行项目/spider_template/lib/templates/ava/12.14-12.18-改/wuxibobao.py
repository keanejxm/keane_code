# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
from appspider_m import Appspider
from initclass import InitClass


class Wuxibobaonews(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "http://wxbb-api.wifiwx.com/mobile/api/bbapp2/lb_news_recomend_column.php?count=10&system_version=6.0.1&app_version=2.2.7&client_id_android=0297b4f3430ca5360c4a326e17d8dde1&locating_city=%E5%8D%97%E4%BA%AC&appkey=qm31EZoorKe0oCu3GfAY3pmxQmw8TZoa&version=2.2.7&appid=36&location_city=%E5%8D%97%E4%BA%AC&device_token=25907d3b0c33083c013735ff99cf14f7&phone_models=MuMu&package_name=com.hoge.android.app.wuxibobao&system_version=6.0.1&app_version=2.2.7&client_id_android=0297b4f3430ca5360c4a326e17d8dde1&locating_city=%E5%8D%97%E4%BA%AC&appkey=qm31EZoorKe0oCu3GfAY3pmxQmw8TZoa&version=2.2.7&appid=36&location_city=%E5%8D%97%E4%BA%AC&device_token=25907d3b0c33083c013735ff99cf14f7&phone_models=MuMu&package_name=com.hoge.android.app.wuxibobao"
        # 频道请求头
        headers = {
            "X-API-TIMESTAMP":"1608088449371kfw93M",
            "X-API-SIGNATURE":"ZmQ0NWE5NDAwOWI1OTMyMWUyMDkzNWVkN2YxNGZiY2JjZTM5YTZhMQ==",
            "X-API-VERSION":"2.2.7",
            "X-AUTH-TYPE":"sha1",
            "X-API-KEY":"70efdf2ec9b086079795c442636b55fb",
            "Host":"wxbb-api.wifiwx.com",
            "Connection":"Keep-Alive",
            "Accept-Encoding":"gzip",
            "Cookie":"__jsluid_h=013276033ffaef88f07c6412f9b68e0a",
            "User-Agent":"okhttp/3.9.1",
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
        for channel in channelslists:
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
            url = "http://wxbb-api.wifiwx.com/mobile/api/bbapp2/news.php"
            headers = {
                "Accept-Language":"zh-CN,zh;q=0.8",
                "User-Agent":"Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_17 1.0.0",
                "X-API-TIMESTAMP":"1608089479735RqmQNQ",
                "X-API-SIGNATURE":"Y2Q4NzFiMTIwMDFmNzVhODYwYWQ0MTRkMmFjMGE5ZjgxNDU2MDJlYg==",
                "X-API-VERSION":"2.2.7",
                "X-AUTH-TYPE":"sha1",
                "X-API-KEY":"70efdf2ec9b086079795c442636b55fb",
                "Host":"wxbb-api.wifiwx.com",
                "Connection":"Keep-Alive",
                "Accept-Encoding":"gzip",
                "Cookie":"__jsluid_h=013276033ffaef88f07c6412f9b68e0a",
            }
            data = {
                "site_id":"1",
                "client_type":"2",
                "count":"20",
                "except_weight":"90",
                "system_version":"6.0.1",
                "app_version":"2.2.7",
                "client_id_android":"0297b4f3430ca5360c4a326e17d8dde1",
                "locating_city":"南京",
                "appkey":"qm31EZoorKe0oCu3GfAY3pmxQmw8TZoa",
                "version":"2.2.7",
                "appid":"36",
                "location_city":"南京",
                "device_token":"25907d3b0c33083c013735ff99cf14f7",
                "phone_models":"MuMu",
                "package_name":"com.hoge.android.app.wuxibobao",
                "count":"20",
                "offset":"0",
                "column_name":channelname,
                "column_id":channelid,
            }
            method = 'get'
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data,channel_id = channelid)
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
                # 可在下面打印处打断点，查看请求到的数据
                print(articlelist_json)
                #若banner图在articlelist_json中则分来开取并给其复制banner = 1
                try:
                    articlelists = articlelist_json['slide']
                    banners = 1
                    for article in articlelists:
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        print(article)
                        articleparam = InitClass().article_list_fields()
                        articletitle = article['title']
                        articleid = article['id']
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
                        except Exception as e:
                            logging.info(f"在文章列表出无法获得封面图{e}")
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["channelname"] = channelname
                        articleparam["channelID"] = channelID
                        articleparam["banner"] = banners
                        articlesparams.append(articleparam)

                    articlelists1 = articlelist_json['list']
                    banners = 0
                    for article in articlelists1:
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        print(article)
                        articleparam = InitClass().article_list_fields()
                        articletitle = article['title']
                        articleid = article['id']
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
                        except Exception as e:
                            logging.info(f"在文章列表出无法获得封面图{e}")
                        articleparam["channelID"] = channelID
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["channelname"] = channelname
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
        url = 'http://wxbb-api.wifiwx.com/mobile/api/bbapp2/item.php'
        headers = {
            "Accept-Language":"zh-CN,zh;q=0.8",
            "User-Agent":"Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_17 1.0.0",
            "X-API-TIMESTAMP":"1608090875652gQbZPv",
            "X-API-SIGNATURE":"YWI2ZjJiZTJiMmQ2MzhiN2YxOWU5YjJhNzgxMzgzZDcyM2RiNDBkNQ==",
            "X-API-VERSION":"2.2.7",
            "X-AUTH-TYPE":"sha1",
            "X-API-KEY":"70efdf2ec9b086079795c442636b55fb",
            "Host":"wxbb-api.wifiwx.com",
            "Connection":"Keep-Alive",
            "Accept-Encoding":"gzip",
            "Cookie":"__jsluid_h=013276033ffaef88f07c6412f9b68e0a",
        }
        method = 'post'
        for articleparam in articles:
            data = {
                "system_version":"6.0.1",
                "app_version":"2.2.7",
                "client_id_android":"02b4f3430ca5360c4a326e17d8dde1",
                "locating_city":"南京",
                "appkey":"qm31EZoorKe0oCu3GfAY3pmxQmw8TZoa",
                "version":"2.2.7",
                "appid":"36",
                "location_city":"南京",
                "device_token":"25907d3b0c33083c013735ff99cf14f7",
                "phone_models":"MuMu",
                "package_name":"com.hoge.android.app.wuxibobao",
                'id': articleparam.get("articleid"),
            }
            # 此处代码不需要改动
            channelID = articleparam.get("channelID")
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
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data = data,
                                                        videourl = videos, videocover = videocover, pubtime = pubtime,
                                                        createtime = createtime, updatetime = updatetime,
                                                        source = source, author = author, likenum = likenum,
                                                        commentnum = commentnum, sharenum = sharenum, readnum = readnum,
                                                        articleurl = articleurl,banners = banner, channel_id = channelID)
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
                if 'title' in articlejson:
                    title = articlejson['title']  # 标题

                    workerid = articlejson['id']
                    url = articlejson["content_url"]
                    author = articlejson["author"]
                    pubtime= articlejson['publish_time']
                    createtime = articlejson['create_time']
                    if 'content' in articlejson.keys():
                        content = articlejson['content']  # 文章内容
                        fields["content"] = content
                        # images = InitClass().get_images(content, type=1)
                        # fields["images"] = images  # 文章评论数
                    if 'childs_data' in articlejson.keys():
                        img = list()
                        for imgsrc in articlejson['childs_data']:
                            img.append(imgsrc['host']+imgsrc['dir']+imgsrc['filepath']+imgsrc['filename'])
                        fields["images"] = img
                        fields["articlecovers"] = img
                    if 'video_filename' in articlejson.keys():
                        videos = list()
                        videos.append(articlejson['hostwork']+'/'+articlejson['video_path']+articlejson['video_filename'])
                        fields["videos"] = videos
                        fields["width"] = articlejson['width']
                        fields["height"] = articlejson['height']
                    if 'from_appname' in articlejson.keys():
                        source = articlejson['from_appname']  # 来源
                        fields["source"] = source
                    if 'content' in articlejson.keys() and 'video_filename' in articlejson.keys():
                        fields["contentType"] = 3
                    elif 'content' in articlejson.keys():
                        fields["contentType"] = 2
                    elif 'video_filename' in articlejson.keys():
                        if articlejson['width'] >= articlejson['height']:
                            fields["contentType"] = 4
                        else:
                            fields["contentType"] = 5

                    fields["appname"] = appname
                    fields["title"] = title
                    fields["url"] = url
                    fields["workerid"] = workerid
                    fields["author"] = author
                    fields["pubtime"] = int(pubtime)*1000
                    fields["createtime"] = int(createtime)*1000
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
    spider = Wuxibobaonews('无锡博报')
    spider.run()
