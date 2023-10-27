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
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


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
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))
        for channel in channelslists:
            # channelname = channel['channelName'].encode("ISO-8859-1").decode("utf8")
            channelname = channel['channelName']
            channelid = channel['channelid']
            channeltype = channel['LINKURL']
            channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channeltype)
            yield channelparam

    def getarticlelistparams(self, channelsres):
        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': 'www.tibetapp.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        method = 'get'
        channel_num = 0
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            url = channel.get("channeltype")
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid=channelid,
                                                                       channel_index_id=channel_index_id)
            yield channel_field,[articlelist_param]

    @staticmethod
    def analyze_articlelists(articleslistsres):
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channel_index_id = articleslistres.get("channelindexid")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            channel_type = articleslistres.get("channeltype")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    if 'topic_datas' in articleslists:
                        # banner
                        for article in articleslists['topic_datas']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article['docid']
                            share_url = article['docURL']
                            article_title = article['MetaDataTitle'].encode("ISO-8859-1").decode("utf8")
                            pubtime = int(InitClass().date_time_stamp(article['PubDate'])) * 1000
                            article_type = article['type']
                            article_covers = list()
                            for img in article['RelPhoto']:
                                article_covers.append(img['picurl'])
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channelindexid"] = channel_index_id
                            article_fields["channeltype"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["contentType"] = article_type
                            article_fields["url"] = share_url
                            article_fields['articlecovers'] = article_covers
                            article_fields["pubtime"] = pubtime
                            article_fields["banner"] = 1
                            yield article_fields
                            # 将请求文章必需信息存入

                    if 'datas' in articleslists:
                        for article in articleslists['datas']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article['docid']
                            share_url = article['docURL']
                            article_title = article['MetaDataTitle'].encode("ISO-8859-1").decode("utf8")
                            pubtime = int(InitClass().date_time_stamp(article['PubDate'])) * 1000
                            article_type = article['type']
                            article_covers = list()
                            for img in article['RelPhoto']:
                                article_covers.append(img['picurl'])
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channelindexid"] = channel_index_id
                            article_fields["channeltype"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["contentType"] = article_type
                            article_fields["url"] = share_url
                            article_fields['articlecovers'] = article_covers
                            article_fields["pubtime"] = pubtime
                            yield article_fields
                            # 将请求文章必需信息存入
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")

    def getarticleparams(self,articleslistsres):
        for article in self.analyze_articlelists(articleslistsres):
            articleid = article.get("workerid")
            url = article.get('url')
            headers = {
                'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
                'Host': 'www.tibetapp.cn',
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip',
            }
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method,
                                                             article_field=article)
            yield [articleparam]

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            articleid = fields.get('fields')
            try:
                bf = bs4.BeautifulSoup(article.get("articleres"), 'html.parser')
                title = str(bf.find('div', class_='content_title'))
                source = bf.select('.content_time p')[0].text
                pubtime = int(InitClass().date_time_stamp(bf.select('.content_time p')[1].text)) * 1000
                readnum = bf.find('span', id=f'monitor_{articleid}')
                if readnum == '' or readnum == None:
                    readnum = '0'
                author = bf.select('.editor')[0].text
                content = bf.find('div', class_='content1')
                content = str(content)  # 文章内容
                videos = InitClass().get_video(content)
                images = InitClass().get_images(content)
                fields["appname"] = self.newsname
                fields["platformID"] = self.platform_id
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
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                num += 1
                logging.info(f"错误数量{num},{e}")

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Kuaisouxizang(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
