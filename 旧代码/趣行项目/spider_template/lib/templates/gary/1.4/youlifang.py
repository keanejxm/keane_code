# -*- encoding:utf-8 -*-
"""
@功能:新湖南解析模板
@AUTHOR：Keane
@文件名：xinhunan.py
@时间：2020/12/17  17:33
"""

import json
import logging
import re
from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


class Youlifang(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://117.78.36.36:8995/app-if/getColumns"
        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': '117.78.36.36:8995',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        data = {
            'siteId':'1',
            'parentColumnId':'2',
            'version':'0',
            'columnType':'-1',
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        for channel in channelslists['columns']:
            channelname = channel['columnName']
            channelid = channel['columnId']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "http://117.78.36.36:8995/app-if/getArticles"
        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': '117.78.36.36:8995',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        method = 'get'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            data = {
                'columnId':channelid,
                'version':'0',
                'lastFileId':'0',
                'count':'20',
                'rowNumber':'0',
                'adv':'1',
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
            channel_type = articleslistres.get("channeltype")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent = 4, ensure_ascii = False))
                try:
                    print(articleslists)
                    if channelid == 8:
                        #首页
                        for article in articleslists["list"]:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article['fileId']
                            article_title = article["title"]
                            article_type = article['articleType']
                            share_url = article['shareUrl']
                            res = re.findall(r"(\d*-\d*-\d* \d*:\d*:\d*)\.\d*", article['publishtime'])[0]
                            pubtime = int(InitClass().date_time_stamp(res)) * 1000
                            article_covers = list()
                            if 'picMiddle' in article.keys():
                                article_cover = article['picMiddle']
                            elif 'picBig' in article.keys():
                                article_cover = article['picBig']
                            else:
                                article_cover = None
                            article_covers.append(article_cover)
                            if articleslists['list'].index(article) < 4:
                                article_fields["banner"] = 1
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channeltype"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["contentType"] = article_type
                            article_fields["articlecovers"] = article_covers
                            article_fields["url"] = share_url
                            article_fields["pubtime"] = pubtime
                            articleparam["articleField"] = article_fields  # 携带文章采集的数据
                            articleparam["articleid"] = article_id
                            articlesparams.append(articleparam)
                    elif channelid == 56:
                        #专题
                        for article in articleslists["list"]:
                            topic_fields = InitClass().topic_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article['fileId']
                            article_title = article["title"]
                            share_url = article['shareUrl']
                            res = re.findall(r"(\d*-\d*-\d* \d*:\d*:\d*)\.\d*", article['publishtime'])[0]
                            pubtime = int(InitClass().date_time_stamp(res)) * 1000
                            article_covers = list()
                            if 'picMiddle' in article.keys():
                                article_cover = article['picMiddle']
                            elif 'picBig' in article.keys():
                                article_cover = article['picBig']
                            else:
                                article_cover = None
                            article_covers.append(article_cover)
                            topic_fields["channelName"] = channelname
                            topic_fields["channelID"] = channelid
                            topic_fields["channeltype"] = channel_type
                            topic_fields["topicCover"] = article_covers
                            topic_fields["workerid"] = article_id
                            topic_fields["topicID"] = article['linkID']
                            topic_fields["title"] = article_title
                            topic_fields["topicUrl"] = share_url
                            topic_fields["pubtime"] = pubtime
                            topic_fields["topic"] = 1
                            # 将请求文章必需信息存入
                            articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                            articleparam["articleid"] = article_id
                            articlesparams.append(articleparam)
                    else:
                        for article in articleslists["list"]:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article['fileId']
                            article_title = article["title"]
                            article_type = article['articleType']
                            share_url = article['shareUrl']
                            res = re.findall(r"(\d*-\d*-\d* \d*:\d*:\d*)\.\d*", article['publishtime'])[0]
                            pubtime = int(InitClass().date_time_stamp(res)) * 1000
                            article_covers = list()
                            if 'picMiddle' in article.keys():
                                article_cover = article['picMiddle']
                            elif 'picBig' in article.keys():
                                article_cover = article['picBig']
                            else:
                                article_cover = None
                            article_covers.append(article_cover)
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channeltype"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["articlecovers"] = article_covers
                            article_fields["title"] = article_title
                            article_fields["contentType"] = article_type
                            article_fields["url"] = share_url
                            article_fields["pubtime"] = pubtime
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
                url = "http://117.78.36.36:8995/app-if/getArticles"
                headers = {
                    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
                    'Host': '117.78.36.36:8995',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                }
                data = {
                    'columnId':article_field.get('topicID'),
                    'version':'0',
                    'lastFileId':'0',
                    'count':'20',
                    'rowNumber':'0',
                    'adv':'1'
                }
            else:
                url = "http://117.78.36.36:8995/app-if/getArticleContent"
                headers = {
                    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
                    'Host': '117.78.36.36:8995',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                }
                data = {
                    'articleId':articleid,
                    'colID':article_field.get('channelID'),
                    'version':'1609725790070'
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
                if "list" in content_s.keys():
                    articlesparams = []
                    for article in content_s['list']:
                        # 获取文章列表内的有用信息
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        article_id = article['fileId']
                        article_title = article["title"]
                        article_type = article['articleType']
                        share_url = article['shareUrl']
                        res = re.findall(r"(\d*-\d*-\d* \d*:\d*:\d*)\.\d*", article['publishtime'])[0]
                        pubtime = int(InitClass().date_time_stamp(res)) * 1000
                        article_covers = list()
                        if 'picMiddle' in article.keys():
                            article_cover = article['picMiddle']
                        elif 'picBig' in article.keys():
                            article_cover = article['picBig']
                        else:
                            article_cover = None
                        article_covers.append(article_cover)
                        article_fields["channelID"] = fields.get('channelID')
                        article_fields["channelname"] = fields.get('channelName')
                        article_fields["channeltype"] = fields.get('channeltype')
                        article_fields["workerid"] = article_id
                        article_fields["articlecovers"] = article_covers
                        article_fields["title"] = article_title
                        article_fields["contentType"] = article_type
                        article_fields["url"] = share_url
                        article_fields["pubtime"] = pubtime
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
                    worker_id = content_s['fileId']
                    article_title = content_s["title"]
                    author = content_s['editor']
                    source = content_s['source']
                    content = content_s["content"]
                    hit_num = content_s['countClick']  # 点击数
                    url = content_s['shareUrl']
                    videos = InitClass().get_video(content)
                    images = InitClass().get_images(content)
                    fields["appname"] = self.newsname
                    fields["title"] = article_title
                    fields["videos"] = videos
                    fields["images"] = images
                    fields["workerid"] = worker_id
                    fields["content"] = content
                    fields["source"] = source
                    fields["author"] = author
                    fields["readnum"] = hit_num
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
    appspider = Youlifang("油立方")
    appspider.run()
