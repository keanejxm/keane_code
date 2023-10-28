# -*- encoding:utf-8 -*-
"""
@功能:FX168财经解析模板
@AUTHOR：Keane
@文件名：ZhongGuoLan.py
@时间：2020/12/17  17:33
"""

import json
import logging

from appspider_m import Appspider
from initclass import InitClass


class FX168CaiJing(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://app5.fx168api.com/common/getNewsChannelConfig.json"
        headers = {
            "Host": "app5.fx168api.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.1"
        }
        data = {
            "appSource": "xmsd.3.0",
            "appCategory": "android",
            "appVersion": "3.6.0",
            "apiSign": "0883BCC9A766258A64DD207F8BC7B97AkjDHFkq2rqHvP4q3/OpPl5fOOGle0Ye05fWsrWL9+WU+1U/HCSy+N0xsjpUdcCx1IXgE57+rhl/ne4C5TRM9VIh4nhyrvsmPi5otDv7ax0U=U40nESHUXlLNXKQ/bRIu/UEAHwAfxH6g7AtpallM3MlkdirUzJIQE0XlWR34N/cMosQ+E+34Z0+lhCRuJ+Muxc5Wwu3yhMsSX71/6DuuH04tneFdiuURldNbptWBPcu3uexPeU1AAg/4WIMh8Eohw6dW9UbFgzyqRDwi27ucsUU="
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(channelsres)
        channelparams = []
        for channel in channelslists['data']['channelConfig']:
            channelid = channel['channelId']
            channelname = channel['channelName']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        print(channelsparams)
        articlelistsparams = []
        headers = {
            "Host": "app5.fx168api.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.1",
            "If-Modified-Since": "Mon, 21 Dec 2020 10:05:05 GMT"
        }
        url = 'https://app5.fx168api.com/news/3.3.0/getMergeNewsByChannel.json'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")
            data = {
                "minId": "",
                "channelId": channelid,
                "maxId": "",
                "direct": "first",
                "pageSize": "20"
            }
            method = 'get'
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid=channelid, data=data,
                                                                       channeltype=channeltype)
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
                articleslists = json.loads(articleslists)
                try:
                    for articles in articleslists["data"]["pager"]["result"]:
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        # 获取文章列表内的有用信息
                        article_id = articles["id"]
                        article_title = articles["newsTitle"]
                        article_type = articles["hotType"]
                        share_url = articles['appNewsUrl']
                        pubtime = articles["publishTime"]
                        readnum = articles['clickNum']
                        article_covers = list()
                        article_covers.append(articles['image'])
                        article_fields["readnum"] = readnum
                        article_fields["articlecovers"] = article_covers
                        article_fields["channelID"] = channelid
                        article_fields["channelname"] = channelname
                        article_fields["channeltype"] = channel_type
                        article_fields["workerid"] = article_id
                        article_fields["title"] = article_title
                        article_fields["contentType"] = article_type
                        article_fields["url"] = share_url
                        find1 = "."
                        if find1 in pubtime:
                            a = pubtime.find(find1)
                            b = len(pubtime)
                            c = b-a
                            pubtime = pubtime[:-c]
                        article_fields["pubtime"] = InitClass().date_time_stamp(pubtime)
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

            url = f"https://app5.fx168api.com/news/getNews.json?newsId={articleid}"
            headers = {
                "Host": "app5.fx168api.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.8.1"
            }
            data = {}
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                             article_field=article_field)
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
                worker_id = content_s["data"]['result']["id"]
                article_title = content_s["data"]['result']["newsTitle"]
                author = content_s["data"]['result']["nickname"]
                source = content_s["data"]['result']["newsSource"]
                content = InitClass().wash_tag(content_s["data"]['result']["newsHtmlContent"])
                if 'newsImage' in content_s["data"]['result'].keys():
                    img_list = content_s['data']['result']['newsImage']
                    imgs = list()
                    for img in img_list:
                        imgs.append(img['url'])
                    fields["images"] = imgs
                fields["appname"] = self.newsname
                fields["contentType"] = 2
                fields["title"] = article_title
                fields["workerid"] = worker_id
                fields["content"] = content
                fields["source"] = source
                fields["author"] = author
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
    appspider = FX168CaiJing("FX168财经")
    appspider.run()
