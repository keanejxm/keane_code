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


class Xizangribao(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://xzrbappapi.peopletech.cn/api/v2/menus/category/list"
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36',
            'Host': 'xzrbappapi.peopletech.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        data = {
            'platform': 'android',
            'clientVersionCode': '13',
            'deviceOs': '6.0.1',
            'pjCode': 'xzrbc_10_201705',
            'device_size': '810.0x1440.0',
            'clientVersion': '2.0.3',
            'deviceModel': 'Netease-MuMu',
            'udid': '010000000308435',
            'channel': 'qq',
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        for channellists in channelslists["item"]['categories']:
            if 'children' in channellists.keys():
                for channel in channellists["children"]:
                    channelname = channel["name"]
                    channelid = channel["id"]
                    channelparam = InitClass().channel_fields(channelid, channelname)
                    channelsparams.append(channelparam)
            else:
                channelname = channellists["name"]
                channelid = channellists["id"]
                channelparam = InitClass().channel_fields(channelid, channelname)
                channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36',
            'Host': 'xzrbappapi.peopletech.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        method = 'get'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            url = f"http://xzrbappapi.peopletech.cn/api/v2/articles/{channelid}"
            data = {
                'pageToken': '',
                'size': '20',
                'headPageSize': '',
                'platform': 'android',
                'clientVersionCode': '13',
                'deviceOs': '6.0.1',
                'pjCode': 'xzrbc_10_201705',
                'device_size': '810.0x1440.0',
                'clientVersion': '2.0.3',
                'deviceModel': 'Netease-MuMu',
                'udid': '010000000308435',
                'channel': 'qq',
            }
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid = channelid, data = data,
                                                                       channeltype = channeltype)
            articlelistsparams.append(articlelist_param)
        yield articlelistsparams

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent = 4, ensure_ascii = False))
                try:
                    print(articleslists)
                    if 'head' in articleslists['item'].keys():
                        #banner
                        for article in articleslists['item']['head']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article["articleId"]
                            article_title = article["title"]
                            article_type = article["type"]
                            share_url = article["shareUrl"]
                            pubtime = int(InitClass().date_time_stamp(InitClass().format_date(article["date"]))) * 1000
                            article_covers = article["images"]
                            if article["type"] == 'subject':
                                #专题
                                topic_fields = InitClass().topic_fields()
                                articleparam = InitClass().article_list_fields()
                                topic_fields["channelName"] = channelname
                                topic_fields["channelID"] = channelid
                                topic_fields["workerid"] = article_id
                                topic_fields["topicID"] = article_id
                                topic_fields["title"] = article_title
                                topic_fields["topicUrl"] = share_url
                                topic_fields["pubtime"] = pubtime
                                topic_fields["topicCover"] = article_covers
                                topic_fields["topic"] = 1
                                articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)
                            else:
                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["workerid"] = article_id
                                article_fields["title"] = article_title
                                article_fields["contentType"] = article_type
                                article_fields["articlecovers"] = article_covers
                                article_fields["url"] = share_url
                                article_fields["pubtime"] = pubtime
                                article_fields["banner"] = 1
                                # 将请求文章必需信息存入
                                articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)
                    if 'list' in articleslists['item'].keys():
                        for article in articleslists['item']['list']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article["articleId"]
                            article_title = article["title"]
                            article_type = article["type"]
                            share_url = article["shareUrl"]
                            pubtime = int(InitClass().date_time_stamp(InitClass().format_date(article["date"]))) * 1000
                            article_covers = article["images"]
                            if article["type"] == 'subject':
                                #专题
                                topic_fields = InitClass().topic_fields()
                                articleparam = InitClass().article_list_fields()
                                topic_fields["channelName"] = channelname
                                topic_fields["channelID"] = channelid
                                topic_fields["workerid"] = article_id
                                topic_fields["topicID"] = article_id
                                topic_fields["title"] = article_title
                                topic_fields["topicUrl"] = share_url
                                topic_fields["pubtime"] = pubtime
                                topic_fields["topicCover"] = article_covers
                                topic_fields["topic"] = 1
                                articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)
                            else:
                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["workerid"] = article_id
                                article_fields["title"] = article_title
                                article_fields["contentType"] = article_type
                                article_fields["articlecovers"] = article_covers
                                article_fields["url"] = share_url
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
                url = f"http://xzrbappapi.peopletech.cn/api/v2/subjects/{articleid}"
                headers = {
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36',
                    'Host': 'xzrbappapi.peopletech.cn',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                }
                data = {
                    'size':'5',
                    'platform':'android',
                    'clientVersionCode':'13',
                    'deviceOs':'6.0.1',
                    'pjCode':'xzrbc_10_201705',
                    'device_size':'810.0x1440.0',
                    'clientVersion':'2.0.3',
                    'deviceModel':'Netease-MuMu',
                    'udid':'010000000308435',
                    'channel':'qq',
                }
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, data = data,channelname='专题',
                                                                 article_field = article_field)
                articleparams.append(articleparam)
            else:
                url = f"http://xzrbh5c.peopletech.cn/api/v2/articles/detail/{articleid}"
                headers = {
                    'Host': 'xzrbh5c.peopletech.cn',
                    'Connection': 'keep-alive',
                    'Access-Control-Allow-Origin': '*',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36;cdrbdaily_Android;cdrbdaily_android',
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,en-US;q=0.8',
                    'X-Requested-With': 'com.xizangdaily.activity',
                }
                data = {
                    '_t': int(time.time())
                }
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, data = data, channelname = article_field.get('channelName'),
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
                print(content_s)
                if "item" in content_s.keys():
                    articlesparams = []
                    for articles in content_s["item"]['blocks']:
                        for article in articles['articles']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article["articleId"]
                            article_title = article["title"]
                            article_type = article["type"]
                            share_url = article["shareUrl"]
                            pubtime = int(InitClass().date_time_stamp(InitClass().format_date(article["date"]))) * 1000
                            article_covers = article["images"]
                            article_fields["channelID"] = fields.get("channelID")
                            article_fields["channelname"] = fields.get("channelname")
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["contentType"] = article_type
                            article_fields["articlecovers"] = article_covers
                            article_fields["url"] = share_url
                            article_fields["pubtime"] = pubtime
                            # 将请求文章必需信息存入
                            articleparam["articleField"] = article_fields  # 携带文章采集的数据
                            articleparam["articleid"] = article_id
                            articlesparams.append(articleparam)
                    aaaa = self.getarticleparams(articlesparams)
                    bbbb = self.getarticlehtml(aaaa.__next__())
                    self.analyzearticle(bbbb.__next__())
            else:
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                    print(content_s)
                    if "item" in content_s.keys():
                        worker_id = content_s["item"]["id"]
                        article_title = content_s["item"]["title"]
                        if "content" in content_s["item"].keys() and content_s["item"] != 'video':
                            content = content_s["item"]["content"]
                            videos = InitClass().get_video(content)
                            images = InitClass().get_images(content)
                            source = content_s["item"]["source"]
                            fields["source"] = source
                            fields["images"] = images
                            fields["videos"] = videos
                        elif content_s["item"] != 'video' and 'medias' in content_s["item"].keys():
                            content = ''
                            videos = list()
                            for v in content_s["item"]['medias'][0]['resources']:
                                videos.append(v['url'])
                            fields["videos"] = videos
                            fields["images"] = content_s["item"]['images']
                            fields["videocover"] = [content_s["item"]['medias'][0]['image']]
                            source = content_s["item"]["source"]
                            fields["source"] = source
                        else:
                            content = content_s["item"]['link']
                        comment_num = content_s["item"]["comments"]
                        hit_num = content_s["item"]["hits"]  # 点击数
                        url = content_s["item"]["shareUrl"]
                        likenum = content_s["item"]["likes"]
                        fields["appname"] = self.newsname
                        fields["title"] = article_title
                        fields["workerid"] = worker_id
                        fields["content"] = content
                        fields["commentnum"] = comment_num
                        fields["readnum"] = hit_num
                        fields["url"] = url
                        fields["likenum"] = likenum
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
    appspider = Xizangribao("西藏日报")
    appspider.run()
