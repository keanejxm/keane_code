"""
解析模板，对app爬虫爬出的页面解析
冀时app模板
author:keane
data:2020/10/29
"""
import json
# import time
# import hashlib
import logging

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class Jishi(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://mapi.plus.hebtv.com/api/open/js/get_home_columns?"
        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_367 1.0.0',
            'X-API-TIMESTAMP': '1603952072436OdJARo',
            'X-API-SIGNATURE': 'MzA5YzQ5OGM4YTAyZjJkZTY5YTYxYzdhNTJhNGM5ZDIwZDRmYjlmZQ==',
            'X-API-VERSION': '3.2.1',
            'X-AUTH-TYPE': 'sha1',
            'X-API-KEY': '05049e90fa4f5039a8cadc6acbb4b2cc',
            'Host': 'mapi.plus.hebtv.com',
        }
        data = {
            'count': '10',
            'system_version': '6.0.1',
            'app_version': '3.2.1',
            'client_type': 'android',
            'client_id_android': '71156911959c161775965150d97153c7',
            'locating_city': '石家庄',
            'appkey': 'b7269c8f9a318c69a59dc430cef3ab59',
            'version': '3.2.1',
            'appid': 'm2ovki73ruqwcwmw8b',
            'language': 'Chinese',
            'location_city': '石家庄',
            'device_token': '09371b9507237be54a4467d4eb4a7815',
            'phone_models': 'MuMu',
            'package_name': 'com.ihope.hbdt',
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    def analyze_channel(self, channelsres):
        channelsparams = []
        channelslists = json.loads(channelsres)
        for channels in channelslists:
            channelid = channels['id']
            channelname = channels['name']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    def getarticlelistparams(self, channelsparams):
        articlelistsparams = []
        channel_data = list()
        url = 'http://mapi.plus.hebtv.com/api/open/js/news?'
        headers = {
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_367 1.0.0',
            'X-API-TIMESTAMP': '1603952873312dS35PJ',
            'X-API-SIGNATURE': 'OGVkNWMyMjYwYTFjODNlODA5Y2QzMDY4MzY3MTgyODAzNTQ4YWEyMg==',
            'X-API-VERSION': '3.2.1',
            'X-AUTH-TYPE': 'sha1',
            'X-API-KEY': '05049e90fa4f5039a8cadc6acbb4b2cc',
            'Host': 'mapi.plus.hebtv.com',
        }
        channel_num = 0
        for channelparam in channelsparams:
            channel_num += 1
            data = {
                'site_id': '1',
                'client_type': '2',
                'count': '20',
                'except_weight': '90',
                'system_version': '6.0.1',
                'app_version': '3.2.1',
                'client_type': 'android',
                'client_id_android': '71156911959c161775965150d97153c7',
                'locating_city': '石家庄',
                'appkey': 'b7269c8f9a318c69a59dc430cef3ab59',
                'version': '3.2.1',
                'appid': 'm2ovki73ruqwcwmw8b',
                'language': 'Chinese',
                'location_city': '石家庄',
                'device_token': '09371b9507237be54a4467d4eb4a7815',
                'phone_models': 'MuMu',
                'package_name': 'com.ihope.hbdt',
                'count': '20',
                'offset': '0',
                'third_offset': '0',
                'column_id': channelparam.get("channelid"),
                'column_name': channelparam.get("channelname"),
            }
            method = 'get'
            channelname = channelparam.get("channelname")
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            # print(create_res, channel_id)
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                       channel_index_id=channel_index_id)
            articlelistsparams.append(articlelist_param)
            channel_data.append(channel_field)
        yield [channel_data, articlelistsparams]

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channel_index_id = articleslistres.get("channelindexid")
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(articleslists)
            except Exception as e:
                logging.info(f"{e}")
            articlelists = articleslists['slide'] + articleslists['list']
            for article in articlelists:
                print(article)
                articleparam = InitClass().article_list_fields()
                articleid = article['id']
                articletitle = article['title']
                imageurl = article['index_pic']
                createtime = article['created_at']
                updatetime = article['updated_at']
                author = article['author']
                articleparam["articleid"] = articleid
                articleparam["articletitle"] = articletitle
                articleparam["imageurl"] = imageurl
                articleparam["channelname"] = channelname
                articleparam["channelindexid"] = channel_index_id
                articleparam["createtime"] = createtime
                articleparam["updatetime"] = updatetime
                articleparam["author"] = author
                articlesparams.append(articleparam)
        yield articlesparams

    def getarticleparams(self, articles):
        articleparams = []
        for article in articles:
            imgurl = article.get("imageurl")
            channelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            createtime = article.get("createtime")
            updatetime = article.get("updatetime")
            author = article.get("author")
            url = 'http://mapi.plus.hebtv.com/api/open/js/item.php?'
            headers = {
                'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_367 1.0.0',
                'X-API-TIMESTAMP': '16039548751408rnkeJ',
                'X-API-SIGNATURE': 'NzA3OGI4MmRhMjVhNzgxMGU3NTUwNTc3NWUxNGZmMjEyMmM1OWZiNA==',
                'X-API-VERSION': '3.2.1',
                'X-AUTH-TYPE': 'sha1',
                'X-API-KEY': '05049e90fa4f5039a8cadc6acbb4b2cc',
                'Host': 'mapi.plus.hebtv.com',
            }
            data = {
                'system_version': '6.0.1',
                'app_version': '3.2.1',
                'client_type': 'android',
                'client_id_android': '71156911959c161775965150d97153c7',
                'locating_city': '石家庄',
                'appkey': 'b7269c8f9a318c69a59dc430cef3ab59',
                'version': '3.2.1',
                'appid': 'm2ovki73ruqwcwmw8b',
                'language': 'Chinese',
                'location_city': '石家庄',
                'device_token': '09371b9507237be54a4467d4eb4a7815',
                'phone_models': 'MuMu',
                'package_name': 'com.ihope.hbdt',
                'id': article.get("articleid"),
            }
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                             createtime=createtime, updatetime=updatetime,
                                                             author=author,channel_index_id=channel_index_id)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        for article in articleres:
            appname = article.get("appname")
            channnelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            imgurl = article.get("imageurl")
            author = article.get("author")
            articlejson = json.loads(article.get("articleres"))
            print(articlejson)
            fields = InitClass().article_fields()
            fields["channelname"] = channnelname
            fields["articlecovers"] = [imgurl]
            fields["appname"] = appname
            fields["platformID"] = self.platform_id
            fields["channelindexid"] = channel_index_id
            fields["author"] = author
            workerid = articlejson["content_id"]
            fields["workerid"] = workerid
            try:
                title = articlejson['title']
                fields["title"] = title
            except Exception as e:
                logging.info(f"没有获取到文章标题{e}")
            try:
                pubtime = articlejson['created_at']
                fields["pubtime"] = InitClass().date_time_stamp(pubtime)
            except Exception as e:
                logging.info(f"没有获取到文章发布时间{e}")
            try:
                source = articlejson['source']
                fields["source"] = source
            except Exception as e:
                logging.info(f"没有获取到文章来源{e}")
            try:
                medias = articlejson["attachments"]
                images = list()
                videos = list()
                if medias:
                    for media in medias:
                        if media["type"] == "image":
                            image = "http://img.plus.hebtv.com/{}".format(media["file_name"])
                            images.append(image)
                        if media["type"] == "video":
                            video = "http://vod.plus.hebtv.com/{}{}".format(media["file_path"], media["file_name"])
                            videos.append(video)
                    fields["videos"] = videos
                    fields["images"] = images
                else:
                    video = "http://vod.plus.hebtv.com/{}{}".format(articlejson["target_path"],
                                                                    articlejson["target_filename"])
                    image = "http://img.plus.hebtv.com/{}".format(articlejson["index_pic"])
                    videos.append(video)
                    images.append(image)
                    fields["videos"] = videos
                    fields["images"] = images
            except Exception as e:
                logging.info(f"此文章没有视频{e}")
            try:
                url = articlejson["content_url"]
                fields["url"] = url
            except Exception as e:
                logging.info(f"没有获取到文章url{e}")
            try:
                content = articlejson['content']
                fields["content"] = content
            except Exception as e:
                logging.info(f"没有获取到文章内容{e}")
            try:
                commentnum = articlejson['comments']
                fields["commentnum"] = commentnum
            except Exception as e:
                logging.info(f"没有获取到文章评论数{e}")
            fields = InitClass().wash_article_data(fields)
            yield {"code": 1, "msg": "OK", "data": {"works": fields}}


def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = Jishi(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
    appspider = Jishi(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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


if __name__ == '__main__':
    appspider = Jishi('冀时', platform_id="085bbda4c6b1a30ae0bee35fa0b759b1", self_typeid="4_1_26_34")
    appspider.run()
