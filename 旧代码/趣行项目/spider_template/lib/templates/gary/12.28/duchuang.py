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


class XinHuNan(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://api.netwin.cn/nayun-api/news/category/single/v1/0/index.json"
        headers = {
            'Accept-Encoding': '',
            'IMEI': '010000000308435',
            'version': '4.8.6',
            'Cookie': 'token=',
            'platform': '10',
            'Host': 'api.netwin.cn',
            'Connection': 'Keep-Alive',
            'User-Agent': 'okhttp/3.14.7',
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method,)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        for channel in channelslists['data']['arr']:
            if channel['categoryId'] != 2877:
                channelname = channel['categoryName']
                channelid = channel['categoryId']
                channelparam = InitClass().channel_fields(channelid, channelname)
                channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        headers = {
            'Accept-Encoding': '',
            'IMEI': '010000000308435',
            'version': '4.8.6',
            'Cookie': 'token=',
            'platform': '10',
            'Host': 'api.netwin.cn',
            'Connection': 'Keep-Alive',
            'User-Agent': 'okhttp/3.14.7',
        }
        method = 'get'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            if channelsparams.index(channel) == 0:
                url = 'https://api.netwin.cn/nayun-api/news/news/v1/lst/1/1/1/index.json'
                url24 = 'https://api.netwin.cn/nayun-api/news/news/24hour/index.json'
                hoturl = 'https://api.netwin.cn/nayun-api/news/news/lst/34/0/index.json'
                subjectUrl = 'https://api.netwin.cn/nayun-api//subject/subject/main//1/index.json'
                articlelist_param_subject = InitClass().articlelists_params_fields(subjectUrl, headers, method, channelname,
                                                                       channelid=channelid,)
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           channelid=channelid,
                                                                           channeltype=channeltype)
                articlelist_param_url24 = InitClass().articlelists_params_fields(url24, headers, method, channelname,
                                                                           channelid=channelid,
                                                                           channeltype=channeltype)
                articlelist_param_hot = InitClass().articlelists_params_fields(hoturl, headers, method, channelname,
                                                                           channelid=channelid,
                                                                           channeltype=channeltype)
                articlelistsparams.append(articlelist_param)
                articlelistsparams.append(articlelist_param_url24)
                articlelistsparams.append(articlelist_param_hot)
                articlelistsparams.append(articlelist_param_subject)
            else:
                url = f'https://api.netwin.cn/nayun-api/news/news/lst/{channelid}/1/index.json'

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
                    if 'first' in articleslists['data'].keys():
                        for article in articleslists['data']['first']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            # 获取文章列表内的有用信息
                            article_id = article["id"]
                            article_title = article["title"]
                            article_type = article['newsType']
                            share_url = article['newsUrl']
                            pubtime = article['publishTime']
                            article_covers = article['imgUrl']
                            source = article['source']
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channeltype"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["contentType"] = article_type
                            article_fields["url"] = share_url
                            article_fields["source"] = source
                            article_fields['articlecovers'] = article_covers
                            article_fields["pubtime"] = pubtime
                            article_fields["banner"] = 1
                            # 将请求文章必需信息存入
                            articleparam["articleField"] = article_fields  # 携带文章采集的数据
                            articleparam["articleid"] = article_id
                            articlesparams.append(articleparam)
                    for article in articleslists['data']['arr']:
                        if 'subjectId' in article.keys():
                            #专题
                            topic_fields = InitClass().topic_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article['subjectId']
                            article_title = article["subjectName"]
                            # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                            # 专题标记topic = 1
                            topic_fields["channelName"] = channelname
                            topic_fields["channelID"] = channelid
                            topic_fields["channeltype"] = channel_type
                            topic_fields["workerid"] = article_id
                            topic_fields["_id"] = article_id
                            topic_fields["title"] = article_title
                            topic_fields["topic"] = 1
                            # 将请求文章必需信息存入
                            articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                            articleparam["articleid"] = article_id
                            articlesparams.append(articleparam)
                        else:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            # 获取文章列表内的有用信息
                            article_id = article["id"]
                            article_title = article["title"]
                            article_type = article['newsType']
                            share_url = article['newsUrl']
                            pubtime = article['publishTime']
                            article_covers = article['imgUrl']
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
                url = f"https://api.netwin.cn/nayun-api//subject/subject/main/get/{article_field['workerid']}/index.json"
                headers = {
                    'Accept': 'application/json',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Connection': 'keep-alive',
                    'Host': 'api.netwin.cn',
                    'Origin': 'https://m.netwin.cn',
                    'Referer': 'https://m.netwin.cn/',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-site',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
                }
                data = {
                    "time": int(time.time())
                }
            else:
                url = article_field['url']
                headers = {
                    'Accept-Encoding':'',
                    'IMEI': '010000000308435',
                    'version': '4.8.6',
                    'Cookie': 'token=',
                    'platform': '10',
                    'Host': 'api.netwin.cn',
                    'Connection': 'Keep-Alive',
                    'User-Agent': 'okhttp/3.14.7',
                }
                data = {

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
                print(content_s)
                if "data" in content_s.keys():
                    articlesparams = []
                    for articles in content_s["data"]['news']:
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        # 获取文章列表内的有用信息
                        article_id = articles["id"]
                        article_title = articles["title"]
                        article_type = articles['newsType']
                        share_url = articles['newsUrl']
                        pubtime = articles['publishTime']
                        article_covers = articles['imgUrl']
                        source = article['source']
                        article_fields["channelID"] = fields.get('channelID')
                        article_fields["channelname"] = fields.get('channelName')
                        article_fields["channeltype"] = fields.get('channeltype')
                        article_fields["workerid"] = article_id
                        article_fields["title"] = article_title
                        article_fields["contentType"] = article_type
                        article_fields["url"] = share_url
                        article_fields["source"] = source
                        article_fields['articlecovers'] = article_covers
                        article_fields["pubtime"] = pubtime
                        article_fields["banner"] = 1
                        # 将请求文章必需信息存入
                        articleparam["articleField"] = article_fields  # 携带文章采集的数据
                        articleparam["articleid"] = article_id
                        articlesparams.append(articleparam)
                    aaaa = self.getarticleparams(articlesparams)
                    bbbb = self.getarticlehtml(aaaa.__next__())
                    self.analyzearticle(bbbb.__next__())
            else:
                try:
                    url = fields.get("url")
                    res = requests.get(url)
                    res.encoding = res.apparent_encoding
                    html = res.text
                    bf = bs4.BeautifulSoup(html, 'html.parser')
                    title = fields.get("title")
                    source = fields.get('source')
                    pubtime = fields.get('pubtime')
                    content = bf.find('div', class_='new_detail')
                    content = str(content)  # 文章内容
                    videos = InitClass.get_video(content)
                    images = InitClass.get_video(content)
                    fields["appname"] = self.newsname
                    fields["title"] = title
                    fields["workerid"] = fields.get("workerid")
                    fields["content"] = content
                    fields["source"] = source
                    fields["pubtime"] = pubtime
                    fields["images"] = images
                    fields["videos"] = videos
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
    appspider = XinHuNan("读创")
    appspider.run()
