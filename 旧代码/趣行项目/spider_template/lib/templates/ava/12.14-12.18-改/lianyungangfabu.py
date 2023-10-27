# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
from appspider_m import Appspider
from initclass import InitClass


class Lianyungangfabunews(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "http://open.tmtsp.com/app/main/config?format=json"
        # 频道请求头
        headers = {
            "token":"c2b719dd5def33d92920259ce1ad8f24",
            "If-Modified-Since":"Wed, 16 Dec 2020 10:08:39 GMT+00:00",
            "User-Agent":"Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
            "Host":"open.tmtsp.com",
            "Connection":"Keep-Alive",
            "Accept-Encoding":"gzip",
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
        channel_arr = channelslists['app_main_btns'][0]['channel']
        channelparams = []
        for channel in channel_arr:
            channelid = channel['key']
            channelname = channel['name']
            channeltype = channel['focus_map']
            if channelname != '部门' and channelname != '县区' and channelname != '政情':
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
        articleparams = []
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")
            # 若有两个请求接口则如下： 例如：banner列表和文章列表时两个请求接口

            url = "http://open.tmtsp.com/app/multivariate/list?page=1&pagesize=12"
            headers = {
                "token":"c2b719dd5def33d92920259ce1ad8f24",
                "If-Modified-Since":"Thu, 17 Dec 2020 01:16:30 GMT+00:00",
                "User-Agent":"Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
                "Host":"open.tmtsp.com",
                "Connection":"Keep-Alive",
                "Accept-Encoding":"gzip",
            }
            data = {
                "key": channelid,
                "page": "1",
                "pagesize": "12"
            }
            method = 'get'
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data, channel_id = channelid)
            articleparams.append(articlelist_param)
            if channeltype != '':
                url_banner = "http://open.tmtsp.com/plugin/focus-api/contentlist?id=5743b0a027f38e9809000073"  # banner请求接口
                data_banner = {
                    'id': channeltype
                }
                articlelist_param_banner = InitClass().articlelists_params_fields(url_banner, headers, method, channelname,data = data_banner,banners = 1, channel_id = channelid)  # 添加banner请求数据体，或其他接口请求数据
                articleparams.append(articlelist_param_banner)
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
                print(articlelist_json)
                try:
                    articlelists = articlelist_json
                    for article in articlelists:
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        print(article)
                        articleparam = InitClass().article_list_fields()
                        articletitle = article['title']
                        articleurl = article['link']
                        if 'key' in article:
                            articleid = article['key']
                        elif 'info_key' in article:
                            articleid = article['info_key']
                        try:
                            articleparam["imageurl"] = []
                            if 'indexpic' in article:
                                img = list()
                                img.append(article['indexpic'])
                                articleparam["imageurl"] = img
                        except Exception as e:
                            logging.info(f"在文章列表出无法获得封面图{e}")
                        articleparam["articleurl"] = articleurl
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
        url = 'http://open.tmtsp.com/app/article/content-detail'
        headers = {
            "token":"c2b719dd5def33d92920259ce1ad8f24",
            "If-Modified-Since":"Wed, 16 Dec 2020 10:07:28 GMT+00:00",
            "User-Agent":"Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
            "Host":"open.tmtsp.com",
            "Connection":"Keep-Alive",
            "Accept-Encoding":"gzip",
        }
        method = 'get'
        for articleparam in articles:
            data = {
                'key': articleparam.get("articleid"),
            }
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
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data = data,
                                                        videourl = videos, videocover = videocover, pubtime = pubtime,
                                                        createtime = createtime, updatetime = updatetime,
                                                        source = source, author = author, likenum = likenum,
                                                        commentnum = commentnum, sharenum = sharenum, readnum = readnum,
                                                        articleurl = articleurl,banners = banner, channel_id = channelid)
            articlesparam.append(article)
        yield articlesparam

    @staticmethod
    def analyzearticles(articles_res):
        for articleres in articles_res:
            channelid = articleres.get("channelID")
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
            articleurl = articleres.get("articleurl")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["articlecovers"] = imgurl
            fields["channelID"] = channelid
            fields["images"] = imgurl
            fields["banner"] = banners
            # 如果有下列字段需添加
            fields["url"] = articleurl #文章的html网址，提取shareurl
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
                if articlejson['content'] != '':
                    title = articlejson['title']  # 标题
                    source = articlejson['source']  # 来源
                    content = articlejson['content']  # 文章内容
                    pubtime = articlejson['createtime']  # 发布时间
                    workerid = articlejson['createtime']
                    author = articlejson["author"]
                    commentnum = articlejson["comment"]
                    likenum = articlejson["like"]
                    content_type = 2
                    videos = InitClass().get_video(content)
                    if videos:
                        fields["videos"] = videos
                        fields["videocover"] = imgurl  # 文章的视频封面地址
                    url = f"http://open.tmtsp.com/app/article/content-detail?key={workerid}"
                    fields["url"] = url
                    fields["contentType"] = content_type
                    fields["likenum"] = likenum
                    fields["appname"] = appname
                    fields["title"] = title
                    fields["workerid"] = workerid
                    fields["source"] = source
                    fields["content"] = content
                    fields["author"] = author
                    fields["commentnum"] = commentnum
                    fields["pubtime"] = int(pubtime)*1000
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
    spider = Lianyungangfabunews('连云港发布')
    spider.run()
