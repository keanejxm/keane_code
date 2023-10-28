#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
功能描述。
# author: Keane
# create date: 2020/11/24
# update date: 2020/11/24
# appversion: 
"""
import json
import logging
import re
import time
from urllib import parse
import hashlib

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class CanKaoXiaoXi(Appspider):
    logging.basicConfig(level=logging.INFO)

    @staticmethod
    def md5(md5_value):
        a = hashlib.md5()
        b = md5_value.encode("utf8")
        a.update(b)
        c = a.hexdigest()
        return c

    def get_sign(self, params, currenttime):
        keys = []
        for key in params.keys():
            keys.append(key)
        keys = sorted(keys)
        param = ''
        for key in keys:
            if len(param) > 0:
                param += "&"
            param += (key + "=" + parse.quote(params[key]))
        param = param.replace("*", "%2A").replace("%7E", "~").replace("+", "%20")
        param = self.md5(param)
        param = param + 'da9706d0faccbf382797d5c162406620' + currenttime
        sign = self.md5(param)
        return sign

    @staticmethod
    def date_time_stamp(date):
        # 转为时间数组
        time_array = time.strptime(date, "%Y-%m-%d %H:%M:%S")
        # timeArray可以调用tm_year等
        # 转为时间戳
        time_stamp = int(time.mktime(time_array))
        return time_stamp

    @staticmethod
    def get_app_params():
        """
        构建app首页请求参数
        :return:
        """
        url = "http://m.api.ckxx.net/v2/start?"
        headers = {
            'User-Agent': 'Maa-Proxymaa-http-ok',
            'Host': 'm.api.ckxx.net',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',

        }
        data = {
            'cachetime': '1606200506',
            'system_version': '6.0.1',
            'sign': '76b6bc2954d0d9aa8d54ea4f7c45c607',
            'nav_width': '405',
            'time': '1606202545805',
            'siteid': '10001',
            'newmigu': 'migu',
            'clientid': '1',
            'modules': 'common:2',
            'app_version': '2.3.8',
            'device_id': '08:00:27:3F:09:3B',
            'system_width': '810',
            'system_name': 'android',
            'ip': '10.0.2.15',
            'device_model': 'MuMu',
            'nav_height': '115',
            'system_height': '1440',
            'device_version': 'AndroidMuMu',
            'type': 'android',
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        """
        对文章首页解析获取频道信息
        :param channelsres:
        :return:
        """
        channelsparams = []
        print("+++", channelsres)
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))
        datas = channelslists["data"]["common"]["menu"]
        for channels in datas:
            channelid = channels['menuid']
            channelname = channels['name']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        for channels in datas[0]["submenu"]:
            channelid = channels['menuid']
            channelname = channels['name']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    def getarticlelistparams(self, channelsparams):
        """
        构建对频道发送请求的参数
        :param channelsparams:
        :return:
        """
        articlelistsparams = []
        channel_data = list()
        url = "http://m.api.ckxx.net/v2/menudata?"
        headers = {
            'User-Agent': 'Maa-Proxymaa-http-ok',
            'Host': 'm.api.ckxx.net',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        method = 'get'
        channel_num = 0
        for channel in channelsparams:
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            currenttime = str(int(time.time() * 1000))
            data = {
                'siteid': '10001',
                'clientid': '1',
                'modules': 'common:2',
                'thumbrate': '2',
                'device_id': '08:00:27:3F:09:3B',
                'listsiteid': '0',
                'system_name': 'android',
                'ip': '10.0.2.15',
                'type': 'android',
                'page': '1',
                'slide': '0',
                'pagesize': '20',
                'menuid': str(channelid),
            }
            sign = self.get_sign(data, currenttime)
            data["time"] = currenttime
            data["sign"] = sign
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                       channel_index_id=channel_index_id)
            articlelistsparams.append(articlelist_param)
            channel_data.append(channel_field)
        yield [channel_data, articlelistsparams]

    @staticmethod
    def analyze_articlelists(articleslistsres):
        """
        对返回的文章列表信息解析
        :param articleslistsres:
        :return:
        """
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            articleslists = articleslistres.get("channelres")
            channel_index_id = articleslistres.get("channelindexid")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    for articles in articleslists['data']['common']['list']['lists']:
                        # 解析新闻列表获取新闻详细信息，可提取字段，imageurl，pubtime，createtime，updatetime，source，author，likenum，commentnum
                        articleparam = InitClass().article_list_fields()
                        articleid = articles['contentid']
                        articletitle = articles['title']
                        imageurl = articles['thumb']
                        commentnum = articles['comments']
                        pubtime = articles['published']
                        createtime = articles['created']
                        try:
                            source = articles["source"]
                            articleparam["source"] = source
                        except Exception as e:
                            logging.info(f"没有新闻来源{e}")
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["imageurl"] = imageurl
                        articleparam["channelname"] = channelname
                        articleparam["channelindexid"] = channel_index_id
                        articleparam["pubtime"] = pubtime
                        articleparam["createtime"] = createtime
                        articleparam["commentnum"] = commentnum
                        articlesparams.append(articleparam)
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")
        yield articlesparams

    def getarticleparams(self, articles):
        """
        构建文章详情所需参数
        :param articles:
        :return: articleparam
        """
        articleparams = []
        url = "http://m.api.ckxx.net/v2/article?"
        headers = {
            'Content-Length': '0',
            'Host': 'm.api.ckxx.net',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',

        }
        for article in articles:
            articleid = article.get("articleid")
            imgurl = article.get("imageurl")
            channelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            pubtime = article.get("pubtime")
            createtime = article.get("createtime")
            updatetime = article.get("updatetime")
            source = article.get("source")
            author = article.get("author")
            likenum = article.get("likenum")
            commentnum = article.get("commentnum")
            currenttime = str(int(time.time() * 1000))
            data = {
                'clientid': '1',
                'device_id': '08:00:27:3F:09:3B',
                'ip': '10.0.2.15',
                'system_name': 'android',
                'contentid': str(articleid),
                'siteid': '10001',
                'type': 'android',
                'styleblack': '0',
                'modules': 'common:2',
            }
            sign = self.get_sign(data, currenttime)
            data["sign"] = sign
            data["time"] = currenttime
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                             pubtime=pubtime, createtime=createtime,
                                                             updatetime=updatetime, source=source, author=author,
                                                             likenum=likenum, commentnum=commentnum,
                                                             channel_index_id=channel_index_id)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        """
        解析文章详情页
        :param articleres:
        :return:
        """
        num = 0
        for article in articleres:
            appname = article.get("appname")
            channelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            imgurl = article.get("imageurl")
            source = article.get("source")
            createtime = article.get("createtime")
            commentnum = article.get("commentnum")
            try:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                print(channelname, content_s)
                workerid = content_s["data"]["common"]["contentid"]
                fields = InitClass().article_fields()
                fields["channelname"] = channelname
                fields["channelindexid"] = channel_index_id
                fields["appname"] = appname
                fields["platformID"] = self.platform_id
                fields["workerid"] = workerid
                fields["title"] = content_s["data"]["common"]["title"]
                fields["content"] = content_s["data"]["common"]["content"]
                fields["images"] = content_s["data"]["common"]["share_image"]
                fields["url"] = content_s["data"]["common"]["share_url"]
                fields["articlecovers"] = imgurl
                # 如果有视频采集视频信息
                try:
                    videos = content_s["data"]["common"]["video"]
                    fields["videos"] = videos
                except Exception as e:
                    logging.info(f"此新闻无视频{e}")
                fields["source"] = source
                fields["pubtime"] = self.date_time_stamp(content_s["data"]["common"]["published"]) * 1000
                try:
                    fields["createtime"] = self.date_time_stamp(
                        re.sub('-(\d){1,2}-(\d){1,2}', "-" + createtime, content_s["data"]["common"]["published"]))
                except Exception as e:
                    logging.info(f"{e}")
                fields["commentnum"] = commentnum
                fields["banner"] = 1

                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
                # fields = self.es_utils.wash_article_data(fields)
                # print(fields)
                # _id = fields.pop("_id")
                # res = self.es_utils._es_create_new_works("dc_works", fields = fields, field_id = _id)
                # print(res)
            except Exception as e:
                num += 1
                logging.info(f"错误数量{num},{e}")


def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = CanKaoXiaoXi(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
    appspider = CanKaoXiaoXi(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
