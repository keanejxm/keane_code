# -*- encoding:utf-8 -*-
"""
@功能:新湖南解析模板
@AUTHOR：Keane
@文件名：xinhunan.py
@时间：2020/12/17  17:33
"""

import json
import logging
import time
import bs4
import requests
from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


class Kanqing(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://mobile.gsqytv.com.cn/qingyang/news_recomend_column_shouye.php"
        headers = {
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_171 1.0.0',
            'X-API-TIMESTAMP': '1610178147824yh6VLA',
            'X-API-SIGNATURE': 'YmRmMTI2MjE2ZmNiNWY5NjIzNDU0YmE4YjU3MmIzNzEzYzM0ZjAwOA==',
            'X-API-VERSION': '2.0.5',
            'X-AUTH-TYPE': 'sha1',
            'X-API-KEY': 'a4a042cf4fd6bfb47701cbc8a1653ada',
            'Host': 'mobile.gsqytv.com.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        data = {
            'count': '50',
            'system_version': '6.0.1',
            'app_version': '2.0.5',
            'client_id_android': 'c3877b8e0686fd154477975487573619',
            'locating_city': '庆阳',
            'appkey': 'VhCgejBlxshBChlENWrB5BVOvyUTllP6',
            'version': '2.0.5',
            'appid': '14',
            'language': 'Chinese',
            'location_city': '庆阳',
            'device_token': 'c99951915cf475b22fafc9132c5010cc',
            'phone_models': 'c99951915cf475b22fafc9132c5010cc',
            'package_name': 'com.hoge.android.app.qingyang',
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        for channel in channelslists:
            channelname = channel['name']
            channelid = channel['id']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        headers = {
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_171 1.0.0',
            'X-API-TIMESTAMP': '1610179126703EduiF1',
            'X-API-SIGNATURE': 'MDEwMTAyNmYxMzg3YTM2YTMzODQ2NjQ3YWQ5YTQ3NWRjYjUzNjc3Ng==',
            'X-API-VERSION': '2.0.5',
            'X-AUTH-TYPE': 'sha1',
            'X-API-KEY': 'a4a042cf4fd6bfb47701cbc8a1653ada',
            'Host': 'mobile.gsqytv.com.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        method = 'get'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            url = 'http://mobile.gsqytv.com.cn/qingyang/news_copy.php'
            data = {
                'site_id': '1',
                'client_type': '2',
                'count': '20',
                'except_weight': '90',
                'system_version': '6.0.1',
                'app_version': '2.0.5',
                'client_id_android': 'c3877b8e0686fd154477975487573619',
                'locating_city': '庆阳',
                'appkey': 'VhCgejBlxshBChlENWrB5BVOvyUTllP6',
                'version': '2.0.5',
                'appid': '14',
                'language': 'Chinese',
                'location_city': '庆阳',
                'device_token': 'c99951915cf475b22fafc9132c5010cc',
                'phone_models': 'MuMu',
                'package_name': 'com.hoge.android.app.qingyang',
                'count': '20',
                'offset': '0',
                'third_offset': '0',
                'column_id': channelid,
            }
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,data=data,
                                                                       channelid = channelid,)
            articlelistsparams.append(articlelist_param)
        yield articlelistsparams

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            channel_type = articleslistres.get("channeltype")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent = 4, ensure_ascii = False))
                try:
                    print(articleslists)
                    if 'slide' in articleslists.keys():
                        #banner
                        for article in articleslists['slide']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article["id"]
                            article_title = article["title"]
                            article_type = article['struct_id']
                            share_url = article['content_url']
                            pubtime = int(article['publish_time_stamp'])*1000
                            article_covers = [(article['indexpic']['host']+article['indexpic']['dir']+article['indexpic']['filepath']+article['indexpic']['filename'])]
                            if article['struct_id'] == 'special':
                                #专题
                                topic_fields = InitClass().topic_fields()
                                articleparam = InitClass().article_list_fields()
                                topic_fields["channelName"] = channelname
                                topic_fields["channelID"] = channelid
                                topic_fields["channeltype"] = channel_type
                                topic_fields["workerid"] = article_id
                                topic_fields["topicID"] = article['content_fromid']
                                topic_fields["title"] = article_title
                                topic_fields["topic"] = 1
                                # 将请求文章必需信息存入
                                articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)
                            else:
                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["channeltype"] = channel_type
                                article_fields["workerid"] = article_id
                                article_fields["title"] = article_title
                                article_fields["contentType"] = article_type
                                article_fields["url"] = share_url
                                article_fields['articlecovers'] = article_covers
                                article_fields["pubtime"] = pubtime
                                article_fields["banner"] = 1
                                # 将请求文章必需信息存入
                                articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)
                    if 'list' in articleslists.keys():
                        for article in articleslists['list']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article["id"]
                            article_title = article["title"]
                            article_type = article['struct_id']
                            share_url = article['content_url']
                            pubtime = int(article['publish_time_stamp'])*1000
                            article_covers = [(article['indexpic']['host']+article['indexpic']['dir']+article['indexpic']['filepath']+article['indexpic']['filename'])]
                            if article['struct_id'] == 'special':
                                #专题
                                topic_fields = InitClass().topic_fields()
                                articleparam = InitClass().article_list_fields()
                                topic_fields["channelName"] = channelname
                                topic_fields["channelID"] = channelid
                                topic_fields["channeltype"] = channel_type
                                topic_fields["workerid"] = article_id
                                topic_fields["topicID"] = article['content_fromid']
                                topic_fields["title"] = article_title
                                topic_fields["topic"] = 1
                                # 将请求文章必需信息存入
                                articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)
                            else:
                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["channeltype"] = channel_type
                                article_fields["workerid"] = article_id
                                article_fields["title"] = article_title
                                article_fields["contentType"] = article_type
                                article_fields["url"] = share_url
                                article_fields['articlecovers'] = article_covers
                                article_fields["pubtime"] = pubtime
                                # 将请求文章必需信息存入
                                articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        for article in articles:
            articleid = article.get("articleid")
            article_field = article.get("articleField")
            topic = article_field.get("topic")
            if topic == 1:
                url = 'http://mobile.gsqytv.com.cn/qingyang/news.php'
                headers = {
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_171 1.0.0',
                    'X-API-TIMESTAMP': '1610329069671fWCMkS',
                    'X-API-SIGNATURE': 'NmU1Mjc2OTZhNzBlNDM5ZmE2YzRmNjIxZmU3YTY2ODNiNGFlMTVkMw==',
                    'X-API-VERSION': '2.0.5',
                    'X-AUTH-TYPE': 'sha1',
                    'X-API-KEY': 'a4a042cf4fd6bfb47701cbc8a1653ada',
                    'Host': 'mobile.gsqytv.com.cn',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                }
                data = {
                    'system_version': '6.0.1',
                    'app_version': '2.0.5',
                    'client_id_android': 'c3877b8e0686fd154477975487573619',
                    'locating_city': '庆阳',
                    'appkey': 'VhCgejBlxshBChlENWrB5BVOvyUTllP6',
                    'version': '2.0.5',
                    'appid': '14',
                    'language': 'Chinese',
                    'location_city': '庆阳',
                    'device_token': 'c99951915cf475b22fafc9132c5010cc',
                    'phone_models': 'MuMu',
                    'package_name': 'com.hoge.android.app.qingyang',
                    'offset': '0',
                    'new_style': '2',
                    'column_id': article_field.get('topicID'),
                }
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            else:
                url = 'http://mobile.gsqytv.com.cn/qingyang/item.php'
                headers = {
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_171 1.0.0',
                    'X-API-TIMESTAMP': '1610183102556vzjMlH',
                    'X-API-SIGNATURE': 'N2QwZTllZDU3MGYzNzA0ZGIzODkwNTQ5MWFmZDBjNWEyZGE5NDgxYQ==',
                    'X-API-VERSION': '2.0.5',
                    'X-AUTH-TYPE': 'sha1',
                    'X-API-KEY': 'a4a042cf4fd6bfb47701cbc8a1653ada',
                    'Host': 'mobile.gsqytv.com.cn',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                }
                data = {
                    'system_version': '6.0.1',
                    'app_version': '2.0.5',
                    'client_id_android': 'c3877b8e0686fd154477975487573619',
                    'locating_city': '庆阳',
                    'appkey': 'VhCgejBlxshBChlENWrB5BVOvyUTllP6',
                    'version': '2.0.5',
                    'appid': '14',
                    'language': 'Chinese',
                    'location_city': '庆阳',
                    'device_token': 'c99951915cf475b22fafc9132c5010cc',
                    'phone_models': 'MuMu',
                    'package_name': 'com.hoge.android.app.qingyang',
                    'id': articleid,
                }
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, data = data,
                                                                 article_field = article_field)
                articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            topic = fields.get("topic")
            if topic:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                if 'list' in content_s.keys() and type(content_s['list']).__name__ == 'list':
                    articlesparams = []
                    for article in content_s['list']:
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        article_id = article["id"]
                        article_title = article["title"]
                        article_type = article['struct_id']
                        share_url = article['content_url']
                        pubtime = int(article['publish_time_stamp']) * 1000
                        article_covers = [(article['indexpic']['host'] + article['indexpic']['dir'] +
                                           article['indexpic']['filepath'] + article['indexpic']['filename'])]
                        article_fields["channelID"] = fields.get('channelID')
                        article_fields["channelname"] = fields.get('channelName')
                        article_fields["workerid"] = article_id
                        article_fields["title"] = article_title
                        article_fields["contentType"] = article_type
                        article_fields["url"] = share_url
                        article_fields['articlecovers'] = article_covers
                        article_fields["pubtime"] = pubtime
                        # 将请求文章必需信息存入
                        articleparam["articleField"] = article_fields  # 携带文章采集的数据
                        articleparam["articleid"] = article_id
                        articlesparams.append(articleparam)
                    aaaa = self.getarticleparams(articlesparams)
                    bbbb = self.getarticlehtml(aaaa.__next__())
                    self.analyzearticle(bbbb.__next__())
            else:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                try:
                    workerid = content_s['id']
                    title = content_s["title"]
                    source = content_s["source"]
                    url = content_s['content_url']
                    pubtime = int(content_s['publish_time'])*1000
                    if 'material' in content_s.keys():
                        content = content_s["content"]
                        images = list()
                        for img in content_s['material']:
                            images.append((img['pic']['host']+img['pic']['dir']+img['pic']['filepath']+img['pic']['filename']))
                        videos = InitClass().get_video(content)
                    elif 'video' in content_s.keys() and content_s['video'] != '':
                        content = ''
                        images = InitClass().get_images(content)
                        videos = [(content_s['video']['host'] + content_s['video']['filepath'] + content_s['video'][
                            'filename'])]
                    else:
                        content =''
                        images = InitClass().get_images(content)
                        videos = InitClass().get_video(content)
                    commentnum = content_s['comment_num']
                    readnum = content_s['click_num']
                    sharenum = content_s['share_num']
                    fields["appname"] = self.newsname
                    fields["title"] = title
                    fields["workerid"] = fields.get("workerid")
                    fields["content"] = content
                    fields["source"] = source
                    fields["pubtime"] = pubtime
                    fields["images"] = images
                    fields["videos"] = videos
                    fields["workerid"] = workerid
                    fields["commentnum"] = commentnum
                    fields["readnum"] = readnum
                    fields["sharenum"] = sharenum
                    fields["url"] = url
                    print(json.dumps(fields, indent = 4, ensure_ascii = False))
                except Exception as e:
                    num += 1
                    logging.info(f"错误数量{num},{e}")

    def run(self):
        appparams = self.get_app_params()
        channelsres = self.getchannels(appparams.__next__())
        channelsparams = self.analyze_channel(channelsres.__next__())
        articlelistparames = self.getarticlelistparams(channelsparams.__next__())
        articleslistsres = self.getarticlelists(articlelistparames.__next__())
        articles = self.analyze_articlelists(articleslistsres.__next__())
        articleparams = self.getarticleparams(articles.__next__())
        articlesres = self.getarticlehtml(articleparams.__next__())
        self.analyzearticle(articlesres.__next__())


if __name__ == '__main__':
    appspider = Kanqing("看清")
    appspider.run()
