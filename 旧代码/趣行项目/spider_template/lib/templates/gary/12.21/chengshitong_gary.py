# -*- encoding:utf-8 -*-
"""
@功能:新湖南解析模板
@AUTHOR：Keane
@文件名：xinhunan.py
@时间：2020/12/17  17:33
"""

import json
import logging
from appspider_m import Appspider
from initclass import InitClass


class Chengshitong(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://api.smartfengze.com/tongplatform/business/content/v1/article-user-subscription/my-subscription/50170bcd48694eb588d4bb90d1bb5c09"
        headers = {
            'base-params': '{"appId":"d151b2f667ed433d891e2ae5b79bb527","areaCode":"350500","attribute":{},"clientParams":{"appPackageName":"com.linewell.citizencloud","appVersion":"2.0.1","carrierName":"","deviceId":"010000000308435","deviceType":"Android MuMu","network":"wifi","os":"android","systemVersion":"6.0.1","timeStamp":1608703550571},"loginTerminal":"1","orgCode":""}',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': 'api.smartfengze.com',
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
        for channellists in channelslists["content"]:
            channelname = channellists["name"]
            channelid = channellists["id"]
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "https://api.smartfengze.com/tongplatform/business/content/v1/article-recomm/list-article"
        method = 'post'
        headers = {
            'base-params': '{"appId":"d151b2f667ed433d891e2ae5b79bb527","areaCode":"350500","attribute":{},"clientParams":{"appPackageName":"com.linewell.citizencloud","appVersion":"2.0.1","carrierName":"","deviceId":"010000000308435","deviceType":"Android MuMu","network":"wifi","os":"android","systemVersion":"6.0.1","timeStamp":1608705302474},"loginTerminal":"1","orgCode":""}',
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': 'api.smartfengze.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'Content-Length': '406',

        }
        channelname = '政策资讯'
        indexUrl = 'https://api.smartfengze.com/tongplatform/business/content/v1/article-recomm/list-index-article'
        indexData = {"id":"a03190e4185b4613bd256f2dbc402745","attribute":{},"pageSize":30,"type":"DOWN","authParams":{},"clientParams":{"appPackageName":"com.linewell.citizencloud","appVersion":"2.0.1","carrierName":"","deviceId":"010000000308435","deviceType":"Android MuMu","network":"wifi","os":"Android","systemVersion":"6.0.1","timeStamp":1608708193150},"appId":"d151b2f667ed433d891e2ae5b79bb527","siteAreaCode":"350500"}
        articlelist_param_index = InitClass().articlelists_params_fields(indexUrl, headers, method, channelname, channeljson=indexData,
                                                                   channelid='a03190e4185b4613bd256f2dbc402745',
                                                                   channeltype='')
        articlelistsparams.append(articlelist_param_index)
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样

            data = {"id":channelid,"attribute":{},"pageSize":30,"type":"DOWN","authParams":{},"clientParams":{"appPackageName":"com.linewell.citizencloud","appVersion":"2.0.1","carrierName":"","deviceId":"010000000308435","deviceType":"Android MuMu","network":"wifi","os":"Android","systemVersion":"6.0.1","timeStamp":1608705302466},"appId":"d151b2f667ed433d891e2ae5b79bb527","siteAreaCode":"350500"}
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, channeljson = data,
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
                print(articleslists)
                try:
                    print(articleslists)
                    if 'content' in articleslists.keys():
                        for article in articleslists['content']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article["id"]
                            article_title = article["title"]
                            article_type = article["type"]
                            share_url = article["linkUrl"]
                            pubtime = InitClass.date_time_stamp(article['publishTime'])
                            images = article['imageUrlArray']
                            videos = article['videoDTO']
                            article_cover = article['coverPicUrl']
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channeltype"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["contentType"] = article_type
                            article_fields["url"] = share_url
                            article_fields["pubtime"] = pubtime
                            article_fields["images"] = images
                            article_fields["videos"] = videos
                            article_fields["articlecovers"] = article_cover
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
            url = f'https://api.smartfengze.com/tongplatform/business/content/v1/article-recomm/{articleid} '
            headers = {
               'base-params': '{"appId":"d151b2f667ed433d891e2ae5b79bb527","areaCode":"350500","attribute":{},"clientParams":{"appPackageName":"com.linewell.citizencloud","appVersion":"2.0.1","carrierName":"","deviceId":"010000000308435","deviceType":"Android MuMu","network":"wifi","os":"android","systemVersion":"6.0.1","timeStamp":1608707134625},"loginTerminal":"1","orgCode":""}',
                'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
                'Host': 'api.smartfengze.com',
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
            try:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                print(content_s)
                worker_id = content_s["content"]["id"]
                article_title = content_s["content"]["title"]
                source = content_s["content"]['sourceName']
                content = content_s["content"]["content"]
                comment_num = content_s["content"]['comment']
                likenum = content_s["content"]['favoriteCount']  # 点击数
                pubtime = content_s["content"]['publishTime']
                try:
                    videos = content_s["content"]['videoDTO']
                except Exception as e:
                    videos = []
                fields["videos"] = videos
                fields["appname"] = self.newsname
                fields["title"] = article_title
                fields["workerid"] = worker_id
                fields["content"] = content
                fields["source"] = source
                fields["commentnum"] = comment_num
                fields["likenum"] = likenum
                fields["articlecovers"] = fields.get('articlecovers')
                fields["pubtime"] = pubtime
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
    appspider = Chengshitong("城事通")
    appspider.run()
