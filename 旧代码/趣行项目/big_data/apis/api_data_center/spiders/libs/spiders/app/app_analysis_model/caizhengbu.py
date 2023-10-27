#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
from urllib.parse import urlparse

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class CaiZhengBu(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        url = "http://app.mof.gov.cn/mofmobilenew/xinwen/channels_7972.json"
        headers = {
            "Host": urlparse(url).netloc,
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.0",
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method)
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
        channelparams = []
        for channel in channelslists['model']:
            channelid = channel['channels']
            channelname = channel['cname']
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
            url = channelid
            headers = {
                "Host": urlparse(url).netloc,
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.12.0",
            }
            method = 'get'
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channel_index_id=channel_index_id)
            articleparams.append(articlelist_param)
            channel_data.append(channel_field)
        yield [channel_data, articleparams]

    @staticmethod
    def setarticlelistparam(channelname, banner, articleparam, article):
        if ('url' in article and article['url'].endswith(".json")) or \
                ('link' in article.keys() and article['link'].endswith(".json")):
            articleparam["channelname"] = channelname
            if 'url' in article:
                articleparam["articleid"] = article['url']
            if 'link' in article:
                articleparam["articleid"] = article['link']
            articleparam["articletitle"] = article['title']
            articleparam["banner"] = banner
            if 'cimgs' in article and len(article['cimgs']):
                articleparam["imageurl"] = article['cimgs'][0]
            if 'videourl' in article:
                articleparam["videos"] = article['videourl']
            if 'pubDate' in article:
                articleparam["pubtime"] = article['pubDate']
        return articleparam

    def analyze_articlelists(self, articleslist_ress):
        """
        解析文章列表页，目的是为了获取文章具体信息，组建请求文章详情数据体
        :param articleslist_ress:
        :return:
        """
        articlesparams = []
        for articleslist_res in articleslist_ress:
            channelname = articleslist_res.get("channelname")
            articlelist_res = articleslist_res.get("channelres")
            channel_index_id = articleslist_res.get("channelindexid")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                print(articlelist_json)
                try:
                    if isinstance(articlelist_json, dict):
                        if 'top_text_datas' in articlelist_json and articlelist_json["top_text_datas"]:
                            toptextdatas = articlelist_json['top_text_datas']
                            for article in toptextdatas:
                                articleparam = InitClass().article_list_fields()
                                articleparam = self.setarticlelistparam(channelname, 1, articleparam, article)
                                articleparam["channelindexid"] = channel_index_id
                                if articleparam['articleid']:
                                    articlesparams.append(articleparam)
                                else:
                                    print('网址新闻：', article)

                        if 'top_datas' in articlelist_json:
                            topdatas = articlelist_json['top_datas']
                            for article in topdatas:
                                articleparam = InitClass().article_list_fields()
                                articleparam = self.setarticlelistparam(channelname, 1, articleparam, article)
                                articleparam["channelindexid"] = channel_index_id
                                if articleparam['articleid']:
                                    articlesparams.append(articleparam)
                                else:
                                    print('网址新闻：', article)

                        if 'top_datas_2' in articlelist_json:
                            topdatas2 = articlelist_json['top_datas_2']
                            for article in topdatas2:
                                articleparam = InitClass().article_list_fields()
                                articleparam = self.setarticlelistparam(channelname, 0, articleparam, article)
                                articleparam["channelindexid"] = channel_index_id
                                if articleparam['articleid']:
                                    articlesparams.append(articleparam)
                                else:
                                    print('网址新闻：', article)

                        if 'list_datas' in articlelist_json:
                            listdatas = articlelist_json['list_datas']
                            for article in listdatas:
                                articleparam = InitClass().article_list_fields()
                                articleparam = self.setarticlelistparam(channelname, 0, articleparam, article)
                                articleparam["channelindexid"] = channel_index_id
                                if articleparam['articleid']:
                                    articlesparams.append(articleparam)
                                else:
                                    print('网址新闻：', article)

                        if 'list_datas_2' in articlelist_json:
                            listdatas2 = articlelist_json['list_datas_2']
                            for article in listdatas2:
                                articleparam = InitClass().article_list_fields()
                                articleparam = self.setarticlelistparam(channelname, 0, articleparam, article)
                                articleparam["channelindexid"] = channel_index_id
                                if articleparam['articleid']:
                                    articlesparams.append(articleparam)
                                else:
                                    print('网址新闻：', article)

                    elif isinstance(articlelist_json, list):
                        for article in articlelist_json:
                            articleparam = InitClass().article_list_fields()
                            articleparam = self.setarticlelistparam(channelname, 0, articleparam, article)
                            articleparam["channelindexid"] = channel_index_id
                            if articleparam['articleid']:
                                articlesparams.append(articleparam)
                            else:
                                print('网址新闻：', article)
                    else:
                        print("解析未识别:" + articlelist_json)
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

        method = 'get'
        for articleparam in articles:
            url_show = articleparam.get('articleid')
            headers = {
                "Host": urlparse(url_show).netloc,
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.12.0",
            }
            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
            channel_index_id = articleparam.get("channelindexid")
            articleid = articleparam.get("articleid")
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
            article_show = InitClass().article_params_fields(url_show, headers, method, channelname, imgurl,
                                                             videourl=videos, videocover=videocover,
                                                             pubtime=pubtime,
                                                             createtime=createtime, updatetime=updatetime,
                                                             source=source, author=author, likenum=likenum,
                                                             commentnum=commentnum, sharenum=sharenum,
                                                             readnum=readnum,
                                                             articleid=articleid, articleurl=articleurl,
                                                             banners=banner,channel_index_id=channel_index_id)
            articlesparam.append(article_show)
        yield articlesparam

    def analyzearticle(self,articleresponsedata):
        for articleresponse in articleresponsedata:
            appname = articleresponse.get("appname")
            banner = articleresponse.get("banner")
            articleres = articleresponse.get("articleres")
            channel_index_id = articleresponse.get("channelindexid")
            try:
                articlejson = eval(articleres)
                print(articlejson)
                fields = InitClass().article_fields()
                fields["appname"] = appname# 应用名称，字符串
                fields["channelindexid"] = channel_index_id
                fields["platformID"] = self.platform_id
                fields["channelname"] = articlejson['datas']['cname']  # 频道名称，字符串
                fields["channelID"] = articlejson['datas']['cid']  # 频道id，字符串
                fields["channelType"] = ""  # 频道type，字符串
                fields["url"] = articlejson['datas']['sharelink']  # 分享的网址，字符串
                fields["workerid"] = articlejson['datas']['docid']  # 文章id，字符串
                fields["title"] = articlejson['datas']['title']  # 文章标题，字符串
                fields["content"] = articlejson['datas']['body']  # 文章内容，字符串
                fields["articlecovers"] = [] if not articlejson['datas']['imgurl'] else [
                    articlejson['datas']['imgurl']]  # 列表封面，数组
                fields["images"] = InitClass().get_images(fields["content"])  # 正文图片，数组
                if 'videourl' in articlejson['datas'].keys():
                    fields["videos"] = [] if not articlejson['datas']['videourl'] else [
                        articlejson['datas']['videourl']]  # 视频地址，数组
                fields["width"] = ""  # 视频宽，字符串
                fields["height"] = ""  # 视频高，字符串
                fields["source"] = ""  # 文章来源，字符串
                fields["pubtime"] = InitClass().date_time_stamp(
                    articlejson['datas']['updatedate'].replace("发布时间：", ""))  # 发布时间，时间戳（毫秒级，13位）
                fields["createtime"] = 0  # 创建时间，时间戳（毫秒级，13位）
                fields["updatetime"] = 0  # 更新时间，时间戳（毫秒级，13位）
                fields["likenum"] = 0  # 点赞数（喜欢数），数值
                fields["playnum"] = 0  # 播放数，数值
                fields["commentnum"] = 0  # 评论数，数值
                fields["readnum"] = 0  # 阅读数，数值
                fields["trannum"] = 0  # 转发数，数值
                fields["sharenum"] = 0  # 分享数，数值
                fields["author"] = ""  # 作者，字符串
                fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                fields["specialtopic"] = 0  # 是否是专题，数值（0标识不是，1标识是）
                fields["topicid"] = ""  # 专题id，字符串
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)


def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = CaiZhengBu(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    appparams = appspider.get_app_params()
    channelsres = appspider.getchannel(appparams.__next__())
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
    appspider = CaiZhengBu(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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

#
# if __name__ == '__main__':
#     run()
