# -*- encoding:utf-8 -*-
"""
@功能:新湖南解析模板
@AUTHOR：Keane
@文件名：xinhunan.py
@时间：2020/12/17  17:33
"""

import json
import logging

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


class Shanxishengzhengfu(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://app2017.shanxi.gov.cn/model_1/channels.json"
        headers = {
            'Host': 'app2017.shanxi.gov.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.4.1',
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        for channel in channelslists["gd"]:
            channelname = channel["cname"]
            channelid = channel["cid"]
            if channel["cid"] == '16269' :
                channeltype = channel['documents'].replace('documents','index')
            elif channel["cid"] == '16272' or channel['cid'] == '16274':
                channeltype = channel['documents'].replace('documents', 'list')
            else:
                channeltype = channel['documents']
            channelparam = InitClass().channel_fields(channelid, channelname,channeltype=channeltype)
            channelsparams.append(channelparam)
        for channel in channelslists["more"]:
            channelname = channel["cname"]
            channelid = channel["cid"]
            if channel["cid"] == '16269':
                channeltype = channel['documents'].replace('documents', 'index')
            elif channel["cid"] == '16272' or channel['cid'] == '16274':
                channeltype = channel['documents'].replace('documents', 'list')
            else:
                channeltype = channel['documents']
            channelparam = InitClass().channel_fields(channelid, channelname,channeltype=channeltype)
            channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        headers = {
            'Host': 'app2017.shanxi.gov.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.4.1',
        }
        method = 'get'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            url = channeltype
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid = channelid,
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
            channel_type = articleslistres.get("channeltype")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent = 4, ensure_ascii = False))
                try:
                    print(articleslists)
                    if 'lunbo' in articleslists.keys():
                        #banner
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        for article in articleslists["lunbo"]:
                            article_id = article['docid']
                            article_title = article["title"]
                            article_type = article["cname"]
                            share_url = article["url"]
                            pubtime = int(InitClass.date_time_stamp(article['updatedate'])) * 1000
                            article_covers = list()
                            article_cover = article['imgurl']
                            article_covers.append(article_cover)
                            if article["cname"].find('专题') > -1 and share_url.find('json') > -1:
                                #专题
                                topic_fields = InitClass().topic_fields()
                                topic_fields["channelName"] = channelname
                                topic_fields["channelID"] = channelid
                                topic_fields["channeltype"] = channel_type
                                topic_fields["topicID"] = article_id
                                topic_fields["title"] = article_title
                                topic_fields["contentType"] = article_type
                                topic_fields["topicUrl"] = share_url
                                topic_fields["pubtime"] = pubtime
                                topic_fields["topic"] = 1
                                topic_fields['topicCover']  = article_covers
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
                                article_fields["pubtime"] = pubtime
                                article_fields["articlecovers"] = article_covers
                                article_fields["banner"] = 1
                                # 将请求文章必需信息存入
                                articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)
                    if 'channellist' in articleslists.keys():
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        for article in articleslists["lunbo"]:
                            article_id = article['docid']
                            article_title = article["title"]
                            article_type = article["cname"]
                            share_url = article["url"]
                            pubtime = int(InitClass.date_time_stamp(article['updatedate'])) * 1000
                            article_covers = list()
                            article_cover = article['imgurl']
                            article_covers.append(article_cover)
                            if article["cname"].find('专题') > -1 and share_url.find('json') > -1:
                                #专题
                                topic_fields = InitClass().topic_fields()
                                topic_fields["channelName"] = channelname
                                topic_fields["channelID"] = channelid
                                topic_fields["channeltype"] = channel_type
                                topic_fields["topicID"] = article_id
                                topic_fields["title"] = article_title
                                topic_fields["contentType"] = article_type
                                topic_fields["topicUrl"] = share_url
                                topic_fields["pubtime"] = pubtime
                                topic_fields["topic"] = 1
                                topic_fields['topicCover']  = article_covers
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
                                article_fields["pubtime"] = pubtime
                                article_fields["articlecovers"] = article_covers
                                # 将请求文章必需信息存入
                                articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)
                    if 'channels' in articleslists.keys():
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        for articles in articleslists['channels']:
                            if 'list' in articles.keys():
                                for article in articles['list']:
                                    article_id = article['docid']
                                    article_title = article["title"]
                                    article_type = article["cname"]
                                    share_url = article["url"]
                                    pubtime = int(InitClass.date_time_stamp(article['updatedate'])) * 1000
                                    article_covers = list()
                                    article_cover = article['imgurl']
                                    article_covers.append(article_cover)
                                    if article["cname"].find('专题') > -1 and share_url.find('json') > -1:
                                        # 专题
                                        topic_fields = InitClass().topic_fields()
                                        topic_fields["channelName"] = channelname
                                        topic_fields["channelID"] = channelid
                                        topic_fields["channeltype"] = channel_type
                                        topic_fields["topicID"] = article_id
                                        topic_fields["title"] = article_title
                                        topic_fields["contentType"] = article_type
                                        topic_fields["topicUrl"] = share_url
                                        topic_fields["pubtime"] = pubtime
                                        topic_fields["topic"] = 1
                                        topic_fields['topicCover'] = article_covers
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
                                        article_fields["pubtime"] = pubtime
                                        article_fields["articlecovers"] = article_covers
                                        # 将请求文章必需信息存入
                                        articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                        articleparam["articleid"] = article_id
                                        articlesparams.append(articleparam)
                    if 'list_datas' in articleslists.keys():
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        for article in articleslists["list_datas"]:
                            if article['docid']:
                                article_id = article['docid']
                                article_title = article["title"]
                                article_type = article["cname"]
                                share_url = article["url"]
                                pubtime = int(InitClass.date_time_stamp(article['updatedate'])) * 1000
                                article_covers = list()
                                article_cover = article['imgurl']
                                article_covers.append(article_cover)
                                if article["cname"].find('专题') > -1 and share_url.find('json') > -1:
                                    #专题
                                    topic_fields = InitClass().topic_fields()
                                    topic_fields["channelName"] = channelname
                                    topic_fields["channelID"] = channelid
                                    topic_fields["channeltype"] = channel_type
                                    topic_fields["topicID"] = article_id
                                    topic_fields["title"] = article_title
                                    topic_fields["contentType"] = article_type
                                    topic_fields["topicUrl"] = share_url
                                    topic_fields["pubtime"] = pubtime
                                    topic_fields["topic"] = 1
                                    topic_fields['topicCover']  = article_covers
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
                                    article_fields["pubtime"] = pubtime
                                    article_fields["articlecovers"] = article_covers
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
                if article_field.get('topicUrl').find('json') > -1:
                    url = article_field.get('topicUrl')
                    headers = {
                        'Host': 'app2017.shanxi.gov.cn',
                        'Connection': 'Keep-Alive',
                        'Accept-Encoding': 'gzip',
                        'User-Agent': 'okhttp/3.4.1',
                    }
            else:
                if article_field.get('url').find('json') > -1:
                    url = article_field.get('url')
                    headers = {
                        'Host': 'app2017.shanxi.gov.cn',
                        'Connection': 'Keep-Alive',
                        'Accept-Encoding': 'gzip',
                        'User-Agent': 'okhttp/3.4.1',
                    }
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method,
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
            else:
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                    worker_id = content_s["datas"]['docid']
                    article_title = content_s["datas"]["title"]
                    source = content_s["datas"]["source"]
                    content = content_s["datas"]["body"]
                    videos = InitClass.get_video(content)
                    images = InitClass.get_images(content)
                    fields["appname"] = self.newsname
                    fields["title"] = article_title
                    fields["workerid"] = worker_id
                    fields["content"] = content
                    fields["source"] = source
                    fields["videos"] = videos
                    fields["videocover"] = images
                    fields["images"] = images
                    print(json.dumps(fields, indent=4, ensure_ascii=False))
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
    appspider = Shanxishengzhengfu("山西省政府")
    appspider.run()
