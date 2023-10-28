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


class Kuaisouxizang(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://www.tibetapp.cn/zixun/index_new.json"
        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': 'www.tibetapp.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        for channel in channelslists:
            channelname = channel['channelName'].encode("ISO-8859-1").decode("utf8")
            channelid = channel['channelid']
            channeltype = channel['LINKURL']
            channelparam = InitClass().channel_fields(channelid, channelname,channeltype=channeltype)
            channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': 'www.tibetapp.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        method = 'get'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            url = channel.get("channeltype")
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
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
                    if 'topic_datas' in articleslists.keys():
                        #banner
                        for article in articleslists['topic_datas']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article['docid']
                            share_url = article['docURL']
                            article_title = article['MetaDataTitle'].encode("ISO-8859-1").decode("utf8")
                            pubtime = int(InitClass().date_time_stamp(article['PubDate']))*1000
                            article_type = article['type']
                            article_covers = list()
                            for img in article['RelPhoto']:
                                article_covers.append(img['picurl'])
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

                    if 'datas' in articleslists.keys():
                        for article in articleslists['datas']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article['docid']
                            share_url = article['docURL']
                            article_title = article['MetaDataTitle'].encode("ISO-8859-1").decode("utf8")
                            pubtime = int(InitClass().date_time_stamp(article['PubDate']))*1000
                            article_type = article['type']
                            article_covers = list()
                            for img in article['RelPhoto']:
                                article_covers.append(img['picurl'])
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
            url = article_field.get('url')
            headers = {
                'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
                'Host': 'www.tibetapp.cn',
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip',
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
            articleid = fields.get('fields')
            try:
                bf = bs4.BeautifulSoup(article.get("articleres"), 'html.parser')
                title = str(bf.find('div', class_= 'content_title'))
                source = bf.select('.content_time p')[0].text
                pubtime = int(InitClass().date_time_stamp(bf.select('.content_time p')[1].text))*1000
                readnum = bf.find('span', id=f'monitor_{articleid}')
                if readnum == '' or readnum == None:
                    readnum = '0'
                author = bf.select('.editor')[0].text
                content = bf.find('div', class_='content1')
                content = str(content)  # 文章内容
                videos = InitClass().get_video(content)
                images = InitClass().get_images(content)
                fields["appname"] = self.newsname
                fields["title"] = title.encode("ISO-8859-1").decode("utf8")
                fields["workerid"] = fields.get("workerid")
                fields["content"] = content
                fields["source"] = source.encode("ISO-8859-1").decode("utf8")
                fields["pubtime"] = pubtime
                fields["images"] = images
                fields["videos"] = videos
                fields["readnum"] = (readnum.encode("ISO-8859-1").decode("utf8")).replace('阅读量：', '')
                fields["author"] = (author.encode("ISO-8859-1").decode("utf8")).replace('责任编辑：', '')
                fields["url"] = fields.get("url")
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
    appspider = Kuaisouxizang("快搜西藏")
    appspider.run()
