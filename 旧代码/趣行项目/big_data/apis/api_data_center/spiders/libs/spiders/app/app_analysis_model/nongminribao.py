# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class NongMenRiBo(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "http://cms.farmer.com.cn/api/app/front/channel/list"
        # 频道请求头
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "0",
            "Host": "cms.farmer.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.9.1",
        }
        # 频道数据体
        data = {}
        # 如果携带的是json数据体,用appjson发送
        # app_json = {}
        # 频道请求方式
        method = "post"
        app_params = InitClass().app_params(url, headers, method, data=data)
        # 如果携带json数据，用下列方式存储发送数据
        # app_params = InitClass().app_params(url, headers, method, data = data ,appjson=app_json)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
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
        channelparams = []
        for channel in channelslists['data']:
            channelid = channel['id']
            channelname = channel['name']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)
        yield channelparams

    def getarticlelistparams(self, channelsparams):
        """
        此方法目的是组建请求文章列页面数据参数，url，headers，data，若以json形式发送数据，则channeljson = channeljson
        :param channelsparams:
        :return:
        """
        articleparams = []
        channel_data = list()
        channel_num = 0
        for channel in channelsparams:
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            # 若有两个请求接口则如下： 例如：banner列表和文章列表时两个请求接口
            url_banner = "http://cms.farmer.com.cn/api/app/front/content/list"  # banner请求接口
            url = "http://cms.farmer.com.cn/api/app/front/content/page"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Content-Length": "45",
                "Host": "cms.farmer.com.cn",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "Cookie": "_site_id_cookie=1; JSESSIONID=BEA684576DD1D3434B24CC7CF7A044E0; SF_cookie_26=15597303",
                "User-Agent": "okhttp/3.9.1"

            }
            data = {
                "orderBy": "4",
                "channelIds": channelid,
                "pageSize": "20",
                "pageNo": "1"
            }
            method = 'post'
            data_banner = {
                'orderBy': '4',
                'channelIds': channelid,
                'count': '4',
                'typeIds': '5',
            }
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            channel_data.append(channel_field)
            articlelist_param_banner = InitClass().articlelists_params_fields(url_banner, headers, method, channelname,
                                                                              data=data_banner,
                                                                              banners=1,
                                                                              channel_index_id=channel_index_id)  # 添加banner请求数据体，或其他接口请求数据
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                       channel_index_id=channel_index_id)
            # 若数据体以json形式发送则以下面方式发送数据上面方式注释
            # articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data,channeljson = channeljson)
            articleparams.append(articlelist_param_banner)
            articleparams.append(articlelist_param)
        yield [channel_data, articleparams]

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
            channel_index_data = articleslist_res.get("channelindexid")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                # 可在下面打印处打断点，查看请求到的数据
                print(articlelist_json)
                # 若banner图在articlelist_json中则分来开取并给其复制banner = 1
                try:
                    articlelists = articlelist_json['data']
                    for article in articlelists:
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        print(article)
                        articleparam = InitClass().article_list_fields()
                        articletitle = article['title']
                        articleid = article['id']
                        try:
                            articleparam["imageurl"] = article['photoList']['photo']
                        except Exception as e:
                            logging.info(f"在文章列表出无法获得封面图{e}")
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["channelname"] = channelname
                        articleparam["channelindexid"] = channel_index_data
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
        url = 'http://cms.farmer.com.cn/api/app/front/content/get'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '8',
            'Host': 'cms.farmer.com.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'Cookie': '_site_id_cookie=1; JSESSIONID=BB7FED8F33A52279EDAEF1FCED40CDB4; SF_cookie_26=15597303',
            'User-Agent': 'okhttp/3.9.1'
        }
        method = 'post'
        for articleparam in articles:
            data = {
                'id': articleparam.get("articleid"),
            }
            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
            channel_index_id = articleparam.get("channelindexid")
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
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                        videourl=videos, videocover=videocover, pubtime=pubtime,
                                                        createtime=createtime, updatetime=updatetime,
                                                        source=source, author=author, likenum=likenum,
                                                        commentnum=commentnum, sharenum=sharenum, readnum=readnum,
                                                        articleurl=articleurl, banners=banner,
                                                        channel_index_id=channel_index_id)
            articlesparam.append(article)
        yield articlesparam

    def analyzearticle(self,articles_res):
        for articleres in articles_res:
            channelname = articleres.get("channelname")
            channel_index_id = articleres.get("channelindexid")
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            banners = articleres.get("banner")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["platformID"] = self.platform_id
            fields["channelindexid"] = channel_index_id
            fields["imageurl"] = imgurl
            fields["banner"] = banners
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                title = articlejson['data']['title']  # 标题
                source = articlejson['data']['origin']  # 来源
                content = articlejson['data']['txt']  # 文章内容
                pubtime = articlejson['data']['date']  # 发布时间
                workerid = articlejson['data']['id']
                url = articlejson['data']["shareUrl"]
                author = articlejson['data']["author"]
                commentnum = articlejson['data']["comments"]
                fields["appname"] = appname
                fields["title"] = title
                fields["url"] = url
                fields["workerid"] = workerid
                fields["source"] = source
                fields["content"] = content
                fields["author"] = author
                fields["commentnum"] = commentnum
                fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)


def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = NongMenRiBo(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    appparams = appspider.get_app_params()
    channelsres = appspider.getchannels(appparams.__next__())
    channelsparams = appspider.analyze_channel(channelsres.__next__())
    articlelistparameses = appspider.getarticlelistparams(channelsparams.__next__())
    articlelistparamess = list()
    for articlelistparamesss in articlelistparameses:
        articlelistparamess = articlelistparamesss
    channel_data = articlelistparamess[0]
    articlelistparames = articlelistparamess[1]
    articleslistsres = appspider.getarticlelists(articlelistparames)
    articles = appspider.analyze_articlelists(articleslistsres.__next__())
    articleparams = appspider.getarticleparams(articles.__next__())
    articlesres = appspider.getarticlehtml(articleparams.__next__())
    app_data = appspider.analyzearticle(articlesres.__next__())
    article_retu = {
        "code": "1",
        "msg": "json",
        "data": dict(),
    }
    data_dict = dict()
    data_dict["channels"] = channel_data
    articles_list = list()
    topics_list = list()
    for data in app_data:
        if "works" in data["data"]:
            articles_list.append(data["data"]["works"])
        elif "topic" in data["data"]:
            topics_list.append(data["data"]["topic"])
        else:
            pass
    article_retu["data"]["topics"] = topics_list
    article_retu["data"]["worksList"] = articles_list
    yield article_retu


def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = NongMenRiBo(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    appparams = appspider.get_app_params()
    channelsres = appspider.getchannels(appparams.__next__())
    channelsparams = appspider.analyze_channel(channelsres.__next__())
    articlelistparameses = appspider.getarticlelistparams(channelsparams.__next__())
    articlelistparamess = list()
    for articlelistparamesss in articlelistparameses:
        articlelistparamess = articlelistparamesss
    channel_data = articlelistparamess[0]
    channel_flag = 1
    articlelistparames = articlelistparamess[1]
    articleslistsres = appspider.getarticlelists(articlelistparames)
    articles = appspider.analyze_articlelists(articleslistsres.__next__())
    articleparams = appspider.getarticleparams(articles.__next__())
    articlesres = appspider.getarticlehtml(articleparams.__next__())
    app_data = appspider.analyzearticle(articlesres.__next__())
    for data in app_data:
        datas = data["data"]
        if channel_flag:
            datas["channels"] = channel_data
            channel_flag = 0
        yield data
