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


class Guangxizhengfu(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://fun.gxzf.gov.cn/php/api/init.php"
        headers = {
            'Host': 'fun.gxzf.gov.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.3.1',
        }
        data = {
            'branch':'2',
            'apptype':'1',
            'uuid':'6c283cdc-b919-36da-8a52-6cdb142aa600',
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        for channel in channelslists['appColumn']:
            channelname = channel['sortname']
            channelid = channel['sortid']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        headers = {
            'Host': 'fun.gxzf.gov.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.3.1',
        }
        method = 'get'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            url = 'http://fun.gxzf.gov.cn/php/api/index.php'
            data = {
                'action':'listnews',
                'sortid':channelid,
                'limit':'20',
                'start':'0',
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
                    if 'topPics' in articleslists.keys() and articleslists['topPics']:
                        #banner
                        for article in articleslists['topPics']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            if 'articleid' in article.keys():
                                article_id = article['articleid']
                            else:
                                article_id = article['sortid']
                            article_title = article["title"]
                            article_type = article['type']
                            if 'sharelink' in article.keys():
                                share_url = article['sharelink']
                            else:
                                share_url = ''
                            pubtime = int(InitClass().date_time_stamp(article['humantime']))*1000
                            article_covers = [article['imgTop']['uploadpic']]
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
                    if 'results' in articleslists.keys() and articleslists['results']:
                        for article in articleslists['results']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            if 'articleid' in article.keys():
                                article_id = article['articleid']
                            else:
                                article_id = article['sortid']
                            article_title = article["title"]
                            article_type = article['type']
                            if 'sharelink' in article.keys():
                                share_url = article['sharelink']
                            else:
                                share_url = ''
                            pubtime = int(InitClass().date_time_stamp(article['humantime']))*1000
                            article_covers = [article['img']['uploadpic']]
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
            url = 'http://fun.gxzf.gov.cn/php/api/index.php'
            headers = {
                'Host': 'fun.gxzf.gov.cn',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 gxrbapp/V1.0.7',
                'Accept': '*/*',
                'Referer': f'http://www.gxzf.gov.cn/html/app/article.html?id={articleid}',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,en-US;q=0.8',
                'Cookie': '_trs_uv=kjs0stbs_3625_jr9o; Hm_lvt_a013af4793f2380a4bcf49ca1ce393eb=1610336544; Hm_lpvt_a013af4793f2380a4bcf49ca1ce393eb=1610344759',
                'X-Requested-With': 'cn.com.gxrb.govenment',
            }
            data = {
                'action':'article',
                'articleid':articleid,
                # 'callback':'jsonp1',
                '_': round(time.time()*1000)
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
            try:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                print(content_s)
                workerid = content_s['news']['articleid']
                title = content_s['news']['title']
                source = content_s['news']['source']
                url = content_s['news']['articlelink']
                pubtime = int(InitClass().date_time_stamp(content_s['news']['humantime']))*1000
                content = content_s['news']['content']
                author = content_s['news']['editor']
                videos = InitClass().get_video(content)
                images = InitClass().get_images(content)
                fields["appname"] = self.newsname
                fields["title"] = title
                fields["author"] = author
                fields["workerid"] = fields.get("workerid")
                fields["content"] = content
                fields["source"] = source
                fields["pubtime"] = pubtime
                fields["images"] = images
                fields["videos"] = videos
                fields["workerid"] = workerid
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
    appspider = Guangxizhengfu("广西政府")
    appspider.run()
