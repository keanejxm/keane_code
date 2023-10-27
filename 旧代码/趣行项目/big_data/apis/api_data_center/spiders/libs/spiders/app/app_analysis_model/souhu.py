#!-*- coding:utf-8 -*-
"""
搜狐新闻app爬虫解析模板
# author: Keane
# create date:
# update date: 2020/11/11
"""
import json
import time

from spiders.libs.spiders.app.initclass import InitClass
from spiders.libs.spiders.app.appspider_m import Appspider


class Souhunews(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://api.k.sohu.com/api/channel/v7/list.go?"
        headers = {
            'Cookie': 'SUV=1602589077883sk9jo8; IPLOC=CN5300; gidinf=x099980109ee12434ceb7fc7a000b04931be'
                      '0487c7b7; t=1602749719576',
            'Host': 'api.k.sohu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko'
                          ') Chrome/84.0.4147.125 Safari/537.36'
        }
        data = {
            'rt': 'xml',
            'supportLive': '1',
            'supportWeibo': '1',
            'v': '6.4.6',
            'version': '6.4.6',
            'cdma_lng': '',
            'cdma_lat': '',
            'up': '1, 13557, 297993, 2063, 3, 283, 4, 6, 5, 2, 11, 50, 45, 960591, 279, 12, 954509, 337, '
                  '98, 16, 177, 248, 49, 65, 960377, 25, 4313, 960596, 960516, 960614, 8922, 790793',
            'down': '',
            'local': '283',
            'change': '0',
            'isStartUp': '1',
            'recomState': '1',
            'browseOnly': '0',
            'gbcode': '130100',
            'localgbcode': '130100',
            'housegbcode': '',
            'p1': 'NjcyNDIwNzk3MjEzMTk4NDM4Ng ==',
            'gid': '02ffff11061101da51831f3e1fffc99d7c5e8af9bca87b',
            'pid': '-1',
            'apiVersion': '42'
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(channelsres)
        channel_datas = []
        channelslist = channelslists['data']
        for channels in channelslist:
            categorylist = channels['channelList']
            for channel in categorylist:
                categoryid = channel['categoryId']
                categoryname = channel['categoryName']
                channelid = channel['id']
                channelname = channel['name']
                channel_data = InitClass().channel_fields(channelid, channelname, categoryid = categoryid,
                                                          categoryname = categoryname)
                channel_datas.append(channel_data)
        yield channel_datas

    def getarticlelistparams(self,channels):

        articlelistsparams = []
        channel_data = list()
        url = 'https://api.k.sohu.com/api/channel/v7/news.go?'
        headers = {
            'Cookie': 'SUV=1602589077883sk9jo8; IPLOC=CN5300; '
                      'gidinf=x099980109ee12434ceb7fc7a000b04931be0487c7b7; t=1602749719576',
            'Host': 'api.k.sohu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
        }
        channel_num = 0
        for channel in channels:
            channel_num += 1
            data = {
                'p1': 'NjcyNDIwNzk3MjEzMTk4NDM4Ng==',
                'pid': '-1',
                'channelId': channel.get("channelid"),
                'num': '20',
                'net': 'wifi',
                'picScale': '18',
                'cdma_lat': '29.001249',
                'cdma_lng': '111.563581',
                'mac': '92:61: AE:3A: F1:9C',
                'AndroidID': 'a0e44e2d8424c653',
                'carrier': 'CMCC',
                'imei': '863254312424111',
                'imsi': '460073075241156',
                'density': '2.0',
                'apiVersion': '42',
                'serial': '863254312424111',
                'skd': '4beec3360307226b09efa6d44e45a2af6d79ba4bc5735b7c23ca7803279132bda863bbc5a050be'
                       '0427286de3fccdcbd38a3c3c88138206c39fc34164075f365e5cb100e8c1eb6866d577ae0bae088'
                       'dd3a309d7bfa7738b6582768adc9bac2288ce2d4d815f4365cf28b2736518df5d9e',
                'v': '1603123200',
                't': str(int(time.time())),
                'cursor': '0',
                'version': '6.4.6',
                'platformId': '3',
                'gbcode': '430700',
                'u': '1',
                'recomState': '1',
                'browseOnly': '0',
                'oaid': '',
                'cursorId': '0',
                'cursorIdR': '0',
                'forceRefresh': '0',
                'times': '0',
                'page': '1',
                'action': '0',
                'needRecommend': '0',
                'rr': '1',
                'isFirst': '0',
                'hasRecomData': '0',
            }
            method = 'get'
            channelname = channel.get("channelname")
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            channel_data.append(channel_field)
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data,
                                                                       channel_index_id=channel_index_id)
            articlelistsparams.append(articlelist_param)
        yield [channel_data,articlelistsparams]

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channel_index_id = articleslistres.get("channelindexid")
            articleslists = articleslistres.get("channelres")
            articleslist = []
            articleslist2 = []
            channelid = None
            try:
                articleslists = json.loads(articleslists)
            except Exception as e:
                print(e)
            try:
                channelid = articleslists['channelId']
            except Exception as e:
                print(e)
            try:
                articleslist1 = articleslists['newsArticles']
            except Exception as e:
                print(e)
                articleslist1 = articleslists['snsArticles']
            try:
                articleslist2 = articleslists['topArticles']
            except Exception as e:
                print(e)
            try:
                articleslist = articleslist1 + articleslist2
            except Exception as e:
                print(e)
            if articleslist:
                for articlelist in articleslist:
                    articleparam = InitClass().article_list_fields()
                    try:
                        articletitle = articlelist['title']
                        articleid = articlelist['newsId']
                        commentnum = articlelist['commentNum']
                        imageurl = articlelist['pics'][0]
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["imageurl"] = imageurl
                        articleparam["channelname"] = channelname
                        articleparam["channelindexid"] = channel_index_id
                        articleparam["channelid"] = channelid
                        articleparam["commentnum"] = commentnum
                        articlesparams.append(articleparam)
                    except Exception as e:
                        print(e)

        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        for article in articles:
            imgurl = article.get("imageurl")
            channelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            commentnum = article.get("commentnum")
            url = 'https://api.k.sohu.com/api/news/v5/article.go?'
            data = {
                'channelId': article.get("channelid"),
                'apiVersion': '42',
                'gid': '-1',
                'imgTag': '1',
                'newsId': article.get("articleid"),
                'openType': '',
                'u': '1',
                'p1': 'NjcyNDIwNzk3MjEzMTk4NDM4Ng==',
                'pid': '-1',
                'recommendNum': '3',
                'refer': '130',
                'rt': 'json',
                'showSdkAd': '1',
                'moreCount': '8',
                'articleDebug': '0',
                '_': str(int(time.time() * 1000)),
            }
            headers = {
                'Cookie': 'SUV=1602589077883sk9jo8; IPLOC=CN5300; '
                          'gidinf=x099980109ee12434ceb7fc7a000b04931be0487c7b7; t=1602749719576',
                'Host': 'api.k.sohu.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
            }
            method = 'get'
            # articleparam.append(url)
            articleparam = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data = data,
                                                             commentnum = commentnum,channel_index_id=channel_index_id)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self,articleres):
        try:
            for article in articleres:
                channnelname = article.get("channelname")
                channel_index_id = article.get("channelindexid")
                imgurl = article.get("imageurl")
                appname = article.get("appname")
                commentnum = article.get("commentnum")
                articlejson = json.loads(article.get("articleres"))
                fields = InitClass().article_fields()
                fields["channelname"] = channnelname
                fields["channelindexid"] = channel_index_id
                fields["platformID"] = self.platform_id
                fields["articlecovers"] = imgurl
                fields["appname"] = appname
                fields["commentnum"] = commentnum
                if "title" in articlejson and articlejson["title"]:
                    title = articlejson['title']
                    workerid = articlejson["newsId"]
                    url = articlejson["originalAddr"]
                    pubtime = articlejson['timestamp']
                    updatetime = articlejson['updateTime']
                    imagess = articlejson["photos"]
                    images = list()
                    if imagess:
                        for image in imagess:
                            images.append(image["pic"])
                    fields["images"] = images
                    videoss = articlejson["tvInfos"]
                    videos = list()
                    if videoss:
                        for video in videoss:
                            videos.append(video["tvUrl"])
                        fields["videos"] = videos
                    source = articlejson['media']['mediaName']
                    content = articlejson['content']
                    fields["title"] = title
                    fields["pubtime"] = pubtime
                    fields["source"] = source
                    fields["content"] = content
                    fields["workerid"] = workerid
                    fields["url"] = url
                    fields["updatetime"] = updatetime
                    fields = InitClass().wash_article_data(fields)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
        except Exception as e:
            self.logger.info(f"{e}")

def fetch_batch(appname, logger, platform_id, self_typeid):
        appspider = Souhunews(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
        appspider = Souhunews(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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

