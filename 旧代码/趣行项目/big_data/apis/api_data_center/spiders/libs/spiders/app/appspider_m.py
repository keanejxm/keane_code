#!-*- coding:utf-8 -*-
"""
app爬虫通用模板，用于发送请求，获取响应
# author: Keane
# create date:
# update date: 2020/11/11
"""
import requests
import time
from spiders.libs.spiders.app.initclass import InitClass
from spiders.libs.spiders.app.es_untils import EsUtils


class Appspider(object):
    def __init__(self, appname, logger, platform_id="", self_typeid=""):
        self.session = requests
        self.newsname = appname
        self.platform_id = platform_id
        self.self_typeid = self_typeid
        self.es_utils = EsUtils()
        # self.logger = LLog("APP客户端", only_console = True, logger_level = "INFO").logger
        self.logger = logger

    # 对app发送请求，获取频道数据
    def getchannels(self, appparams):
        """
        获取新闻频道页面，需参数appparams，由模板传递
        :param appparams:
        :return: channelres:
        """
        self.logger.info("正在获取频道信息......")
        url = appparams['appurl']
        headers = appparams['appheaders']
        data = appparams['appdata']
        method = appparams['appmethod']
        appjsons = appparams["appjson"]
        if method == "get":
            if appjsons:
                channelres = self.session.get(url, headers=headers, params=data, json=appjsons).content.decode()
            else:
                channelres = self.session.get(url, headers=headers, params=data).content.decode()
            # channelsres.append(channelres)
            yield channelres
        if method == "post":
            channelres = self.session.post(url, headers=headers, data=data, json=appjsons).content.decode()
            # channelsres.append(channelres)
            yield channelres

    # 对app发送请求，获取频道数据（适用于对多个一级频道发送请求）
    def getchannel(self, appparams):
        """
        获取新闻频道页面，需参数appparams，由模板传递
        :param appparams:
        :return: channelres:
        """
        self.logger.info("正在获取频道信息......")
        channelsres = list()
        for appparam in appparams:
            url = appparam['appurl']
            headers = appparam['appheaders']
            data = appparam['appdata']
            method = appparam['appmethod']
            appjsons = appparam["appjson"]
            if method == "get":
                if appjsons:
                    channelres = self.session.get(url, headers=headers, params=data,
                                                  json=appjsons).content.decode()
                else:
                    channelres = self.session.get(url, headers=headers, params=data).content.decode()
                channelsres.append(channelres)
            if method == "post":
                channelres = self.session.post(url, headers=headers, data=data, json=appjsons).content.decode()
                channelsres.append(channelres)
        yield channelsres

    # 对频道发送请求获取文章列表数据
    def getarticlelists(self, channel_datas):
        """
        通过传入的数据对频道发送请求采集文章列表的信息
        :param channel_datas: 发送请求携带的，请求头，数据，请求方式，
        :return:携带文章列表信息的响应网页
        """

        articleslists = []
        for channel_data in channel_datas:
            method = channel_data.get("method")
            channelname = channel_data.get("channelname")
            channelid = channel_data.get("channelid")
            channeljson = channel_data.get("channeljson")
            banners = channel_data.get("banner")
            sleep_time = channel_data.get("sleeptime")
            time.sleep(sleep_time)
            channel_index_id = channel_data.get("channelindexid")
            self.logger.info(f"正在采集频道{channelname}内容")
            if method == 'get':
                try:
                    articlelist_res = self.session.get(channel_data.get("url"), headers=channel_data.get("headers"),
                                                       params=channel_data.get("data")).text
                    articleslist = InitClass().articlelist_model(channelname, articlelist_res, banners,
                                                                 channelid=channelid,
                                                                 channel_index_id=channel_index_id)
                    articleslists.append(articleslist)
                except Exception as e:
                    self.logger.info(f"getarticlelists方法get请求{e}")
            elif method == 'post':
                try:
                    articlelist_res = self.session.post(channel_data.get("url"), headers=channel_data.get("headers"),
                                                        data=channel_data.get("data"), json=channeljson).text
                    articleslist = InitClass().articlelist_model(channelname, articlelist_res, banners=banners,
                                                                 channelid=channelid,
                                                                 channel_index_id=channel_index_id)
                    articleslists.append(articleslist)
                except Exception as e:
                    self.logger.info(f"getarticlelists方法post请求{e}")
        yield articleslists

    # 对文章发送请求获取文章详情
    def getarticlehtml(self, articleparams):
        """
         通过传输的数据对详情页进行数据采集，获取详情页数据
        :param articleparams: articleparams,包含请求头，发送请求需要携带的数据，请求方式
        :return: 采集的网页信息
        """
        articles_res = []
        for articleparam in articleparams:
            st = articleparam.get("sleeptime")
            if not st:
                st = 0
            url = articleparam.get("url")
            headers = articleparam.get("headers")
            data = articleparam.get("data")
            method = articleparam.get("method")
            banners = articleparam.get("banner")
            articlejson = articleparam.get("articlejson")
            article_field = articleparam.get("articleField")
            channelname = articleparam.get("channelname") if articleparam.get("channelname") else article_field.get(
                "channelName")
            if not channelname:
                channelname = article_field.get("channelname")
            channel_index_id = articleparam.get("channelindexid")
            imgurl = articleparam.get("imageurl")
            articleurl = articleparam.get("articleurl")
            videourl = articleparam.get("videourl")
            videocover = articleparam.get("videocover")
            articleid = articleparam.get("articleid")
            pubtime = articleparam.get("pubtime")
            createtime = articleparam.get("createtime")
            updatetime = articleparam.get("updatetime")
            likenum = articleparam.get("likenum")
            readnum = articleparam.get("readnum")
            sharenum = articleparam.get("sharenum")
            commentnum = articleparam.get("commentnum")
            source = articleparam.get("source")
            author = articleparam.get("author")
            self.logger.info(f"正在采集文章内容:{channelname}，{url}")
            res = ''
            try:
                if method == "get":
                    res = self.session.get(url, headers=headers, params=data).text
                if method == "post":
                    res = self.session.post(url, headers=headers, data=data, json=articlejson).text
            except Exception as e:
                self.logger.info(f"getarticlehtml方法请求{e}")
            articleres = InitClass().article_method(self.newsname, res, channelname, imgurl, pubtime=pubtime,
                                                    createtime=createtime, updatetime=updatetime, source=source,
                                                    aurthor=author, likenum=likenum, commentnum=commentnum,
                                                    articleurl=articleurl, articleid=articleid, videourl=videourl,
                                                    videocover=videocover, readnum=readnum, sharenum=sharenum,
                                                    banners=banners, article_field=article_field,
                                                    channel_index_id=channel_index_id)
            articles_res.append(articleres)
            time.sleep(st)
        yield articles_res

    # 单独发送一次请求
    def send_request(self, request_params):
        """
        增加发送单次请求模板，针对对单个文章的请求，可用来请求专题下的文章，
        :param request_params:从initclass内组成
        :return:返回{"request_res":res,"articlefields":"article_fields"},下一步用get获取
        """
        sleeptime = request_params.get("sleeptime")
        if sleeptime:
            time.sleep(sleeptime)
        url = request_params.get('url')
        headers = request_params.get('headers')
        data = request_params.get('data')
        method = request_params.get('method')
        request_json = request_params.get("requestjson")
        article_fields = request_params.get("articlefields")
        response_res = dict()
        if method == "get":
            if request_json:
                res = requests.get(url, headers=headers, params=data,
                                   json=request_json).content.decode()
            else:
                res = requests.get(url, headers=headers, params=data).content.decode()
            response_res["request_res"] = res
            response_res["articlefields"] = article_fields
            yield response_res

        elif method == "post":
            res = requests.post(url, headers=headers, data=data, json=request_json).content.decode()
            response_res["request_res"] = res
            response_res["articlefields"] = article_fields
            yield response_res
        else:
            self.logger.warning(f"暂时无此请求方式需添加此请求方式")

    def fethch_yieldaaaa(self, appspider):
        for appparam in appspider.get_app_params():
            for channelres in appspider.getchannels(appparam):
                for channel_field, channel_param in appspider.getarticlelistparams(channelres):
                    for article_list_res in appspider.getarticlelists(channel_param):
                        for article_param in appspider.getarticleparams(article_list_res):
                            for article_res in appspider.getarticlehtml(article_param):
                                for data in appspider.analyzearticle(article_res):
                                    yield data
                    yield {"code": 1, "msg": "OK", "data": {"channel": channel_field}}
