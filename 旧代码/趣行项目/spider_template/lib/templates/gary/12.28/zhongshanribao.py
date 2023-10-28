# -*- encoding:utf-8 -*-
"""
@功能:新湖南解析模板
@AUTHOR：Keane
@文件名：xinhunan.py
@时间：2020/12/17  17:33
"""

import json
import logging
import bs4
import requests
from appspider_m import Appspider
from initclass import InitClass


class XinHuNan(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://zsrbapp.zsnews.cn/api/category/index"
        headers = {
            'apiVersion': '9',
            'clientid': '8c2e1a133f484255da663b6030142669',
            'giuid': '9b828e16f3536c30a731f1125ef8b263',
            'deviceId': 'aa59b7a5a10a2e7d77601f058f4bf3bc',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Content-Length': '88',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': 'zsrbapp.zsnews.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        data = {
            'giuid':'9b828e16f3536c30a731f1125ef8b263',
            'clientid':'8c2e1a133f484255da663b6030142669',
            'userId':''
        }
        method = "post"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        for channel in channelslists["data"]:
            channelname = channel["cart"]
            channelid = channel["id"]
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "https://zsrbapp.zsnews.cn/api/news-list/list"
        headers = {
            'apiVersion': '9',
            'clientid': '8c2e1a133f484255da663b6030142669',
            'giuid': '9b828e16f3536c30a731f1125ef8b263',
            'deviceId': 'aa59b7a5a10a2e7d77601f058f4bf3bc',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': 'zsrbapp.zsnews.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        method = 'get'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            data = {
                'categoryId': channelid,
                'page':'1',
                'order':'0',
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
                    if 'slideList' in articleslists['data'].keys():
                        #banner
                        for article in articleslists['data']['slideList']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            # 获取文章列表内的有用信息
                            article_id = article["id"]
                            article_title = article["title"]
                            article_type = article["type"]
                            share_url = article["url"]
                            pubtime = int(InitClass.date_time_stamp(article['publishTime'])) * 1000
                            article_covers = list()
                            article_cover = article["img"]
                            article_covers.append(article_cover)
                            if article["type"] == 2:
                                topic_fields = InitClass().topic_fields()
                                topic_fields["channelName"] = channelname
                                topic_fields["channelID"] = channelid
                                topic_fields["channeltype"] = channel_type
                                topic_fields["workerid"] = article_id
                                topic_fields["_id"] = article_id
                                topic_fields["contentType"] = article_type
                                topic_fields["topicUrl"] = share_url
                                topic_fields["pubtime"] = pubtime
                                topic_fields['topicCover'] = article_covers
                                topic_fields["topic"] = 1
                                # 将请求文章必需信息存入
                                articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)
                            else:
                                comment = article["commentCount"]
                                hits = article["hits"]
                                likes = article["likes"]
                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["channeltype"] = channel_type
                                article_fields["workerid"] = article_id
                                article_fields["title"] = article_title
                                article_fields["contentType"] = article_type
                                article_fields["articlecovers"] = article_covers
                                article_fields["url"] = share_url
                                article_fields["pubtime"] = pubtime
                                article_fields["commentnum"] = comment
                                article_fields["readnum"] = hits
                                article_fields["likenum"] = likes
                                article_fields["banner"] = 1
                                # 将请求文章必需信息存入
                                articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)
                    if 'list' in articleslists['data'].keys():
                        for article in articleslists['data']['list']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            # 获取文章列表内的有用信息
                            article_id = article["id"]
                            article_title = article["title"]
                            article_type = article["type"]
                            share_url = article["url"]
                            pubtime = int(InitClass.date_time_stamp(article['publishTime'])) * 1000
                            article_covers = list()
                            article_cover = article["img"]
                            article_covers.append(article_cover)
                            if article["type"] == 2:
                                topic_fields = InitClass().topic_fields()
                                topic_fields["channelName"] = channelname
                                topic_fields["channelID"] = channelid
                                topic_fields["channeltype"] = channel_type
                                topic_fields["workerid"] = article_id
                                topic_fields["_id"] = article_id
                                topic_fields["contentType"] = article_type
                                topic_fields["topicUrl"] = share_url
                                topic_fields["pubtime"] = pubtime
                                topic_fields['topicCover'] = article_covers
                                topic_fields["topic"] = 1
                                # 将请求文章必需信息存入
                                articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)
                            else:
                                comment = article["commentCount"]
                                hits = article["hits"]
                                likes = article["likes"]
                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["channeltype"] = channel_type
                                article_fields["workerid"] = article_id
                                article_fields["title"] = article_title
                                article_fields["contentType"] = article_type
                                article_fields["url"] = share_url
                                article_fields["pubtime"] = pubtime
                                article_fields["articlecovers"] = article_covers
                                article_fields["commentnum"] = comment
                                article_fields["readnum"] = hits
                                article_fields["likenum"] = likes
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
                url = "https://zsrbapp.zsnews.cn/api/topic/view"
                headers = {
                    'apiVersion': '9',
                    'clientid': '8c2e1a133f484255da663b6030142669',
                    'giuid': '9b828e16f3536c30a731f1125ef8b263',
                    'deviceId': 'aa59b7a5a10a2e7d77601f058f4bf3bc',
                    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
                    'Host': 'zsrbapp.zsnews.cn',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                }
                data = {
                    "id": articleid
                }
            else:
                url = f'https://zsrbapp.zsnews.cn/mobile/news/viewNews/1/{articleid}'
                headers = {
                    'Host': 'zsrbapp.zsnews.cn',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 ZsrbApp/6.5.3.2',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,en-US;q=0.8',
                    'Cookie': 'Hm_lvt_6dc2d1e1700848bd3fa3527da6eabd74=1609140662; Hm_lpvt_6dc2d1e1700848bd3fa3527da6eabd74=1609140697',
                    'X-Requested-With': 'com.zszs.activity',

                }
                data = {}
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method,data=data,
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
                try:
                    if "data" in content_s.keys():
                        articlesparams = []
                        for articles in content_s["data"]['list']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            # 获取文章列表内的有用信息
                            article_id = articles["id"]
                            article_title = articles["title"]
                            article_type = articles["type"]
                            share_url = articles["url"]
                            pubtime = int(InitClass.date_time_stamp(articles['publishTime'])) * 1000
                            article_covers = list()
                            article_cover = articles["img"]
                            article_covers.append(article_cover)
                            comment = articles["commentCount"]
                            hits = articles["hits"]
                            likes = articles["likes"]
                            article_fields["channelID"] = fields.get('channelID')
                            article_fields["channelname"] = fields.get('channelName')
                            article_fields["channeltype"] = fields.get('channeltype')
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["contentType"] = article_type
                            article_fields["url"] = share_url
                            article_fields["pubtime"] = pubtime
                            article_fields["articlecovers"] = article_covers
                            article_fields["commentnum"] = comment
                            article_fields["readnum"] = hits
                            article_fields["likenum"] = likes
                            # 将请求文章必需信息存入
                            articleparam["articleField"] = article_fields  # 携带文章采集的数据
                            articleparam["articleid"] = article_id
                            articlesparams.append(articleparam)
                        aaaa = self.getarticleparams(articlesparams)
                        bbbb = self.getarticlehtml(aaaa.__next__())
                        self.analyzearticle(bbbb.__next__())
                except Exception as e:
                    print(e)
            else:
                try:
                    url = fields.get("url")
                    res = requests.get(url)
                    res.encoding = res.apparent_encoding
                    html = res.text
                    bf = bs4.BeautifulSoup(html, 'html.parser')
                    if bf.select('.info span'):
                        title = bf.find('h1').text
                        source = bf.select('.info span')[1].text
                        pubtime = bf.select('.info span')[0].text
                        content = bf.find('div', class_='content')
                        content = str(content)  # 文章内容
                        videos = InitClass.get_video(content)
                        images = InitClass.get_video(content)
                        fields["images"] = images
                        fields["videos"] = videos
                        fields["videocover"] = images
                        fields["appname"] = self.newsname
                        fields["title"] = title
                        fields["workerid"] = fields.get('workerid')
                        fields["content"] = content
                        fields["source"] = source
                        fields["pubtime"] = pubtime
                        fields["commentnum"] = fields.get("commentnum")
                        fields["readnum"] = fields.get("readnum")
                        fields["likenum"] = fields.get("likenum")
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
    appspider = XinHuNan("新湖南")
    appspider.run()
