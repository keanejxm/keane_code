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


class XinHuNan(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://app.zhld.com:8090/app_if/getColumns"
        headers = {
            'Host': 'app.zhld.com:8090',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.8.0',

        }
        data = {
            'siteId': '2',
            'parentColumnId': '1',
            'version': '0',
            'columnType': '-1',
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        for channellists in channelslists['columns']:
            channelname = channellists['columnName']
            channelid = channellists['columnId']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "http://app.zhld.com:8090/app_if/getArticles"
        headers = {
            'Host': 'app.zhld.com:8090',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.8.0',
        }
        method = 'get'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            data = {
                "columnId": channelid,
                "version": "0",
                "lastFileId":'0',
                "page": "0",
                "adv": "1",
                "columnStyle": "201",
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
                print(articleslists)
                try:
                    if 'list' in articleslists.keys():
                        for article in articleslists['list']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            topic_fields = InitClass().topic_fields()
                            article_id = article['fileId']
                            article_title = article["title"]
                            article_type = article['articleType']
                            if article['picCount'] != "0" :
                                if 'picBig' in article.keys():
                                    images = [article['picBig']]
                                else:
                                    images = [article['pic0']]
                            else:
                                images = []
                            url = article["urlPad"]
                            topic = 0
                            if article['articleType'] == 4:
                                topic = 1
                                topic_fields["channelName"] = channelname
                                topic_fields["channelID"] = channelid
                                topic_fields["channeltype"] = channel_type
                                topic_fields["workerid"] = article_id
                                topic_fields['_id'] = article['url']
                                topic_fields["title"] = article_title
                                topic_fields["contentType"] = article_type
                                topic_fields["topicUrl"] = url
                                topic_fields["topic"] = topic
                                # 将请求文章必需信息存入
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
                                article_fields["url"] = url
                                article_fields["images"] = images
                                article_fields["banner"] = 1
                                # 将请求文章必需信息存入
                                articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)




                    # for articles in articleslists["data"]["value"]:
                    #     if "data" in articles.keys():
                    #         # 可能是轮播图或置顶新闻，里面可能有专题【jumpdata】
                    #         for article in articles["data"]:
                    #             article_fields = InitClass().article_fields()
                    #             articleparam = InitClass().article_list_fields()
                    #             print(article)
                    #             # 获取文章列表内的有用信息
                    #             article_id = article["ID"]
                    #             article_title = article["title"]
                    #             article_type = article["biaoqian"]
                    #             share_url = article["Url"]
                    #             pubtime = int(article["PublishTime"]) * 1000
                    #             article_covers = list()
                    #             article_cover = article["pic"]
                    #             article_covers.append(article_cover)
                    #             # 采集视频
                    #             try:
                    #                 videocovers = list()
                    #                 videocover = article["video"]["cover"]
                    #                 videocovers.append(videocover)
                    #                 videoss = article["video"]["data"]
                    #                 videos = list()
                    #                 for video in videoss:
                    #                     videos.append(video["url"])
                    #                 article_fields["videos"] = videos
                    #                 article_fields["videocovers"] = videocovers
                    #             except Exception as e:
                    #                 logging.info(f"此新闻无视频{e}")
                    #             # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                    #             article_fields["channelID"] = channelid
                    #             article_fields["channelname"] = channelname
                    #             article_fields["channeltype"] = channel_type
                    #             article_fields["workerid"] = article_id
                    #             article_fields["title"] = article_title
                    #             article_fields["contentType"] = article_type
                    #             article_fields["url"] = share_url
                    #             article_fields["pubtime"] = pubtime
                    #             article_fields["banner"] = 1
                    #             # 将请求文章必需信息存入
                    #             articleparam["articleField"] = article_fields  # 携带文章采集的数据
                    #             articleparam["articleid"] = article_id
                    #             articlesparams.append(articleparam)
                    #     if "jumpdata" in articles.keys():
                    #         # 这种类型为专题
                    #         print(articles)
                    #         topic_fields = InitClass().topic_fields()
                    #         articleparam = InitClass().article_list_fields()
                    #         # 获取文章列表内的有用信息
                    #         article_id = articles["jumpdata"]["ID"]
                    #         article_title = articles["jumpdata"]["title"]
                    #         article_type = articles["jumpdata"]["biaoqian"]
                    #         topic = 0
                    #         if article_type == "专题":
                    #             topic = 1
                    #         share_url = articles["jumpdata"]["Url"]
                    #         pubtime = int(articles["jumpdata"]["PublishTime"]) * 1000
                    #         article_covers = list()
                    #         article_cover = articles["jumpdata"]["pic"]
                    #         article_covers.append(article_cover)
                    #         # 采集视频
                    #         try:
                    #             videocovers = list()
                    #             videocover = articles["video"]["cover"]
                    #             videocovers.append(videocover)
                    #             videoss = articles["video"]["data"]
                    #             videos = list()
                    #             for video in videoss:
                    #                 videos.append(video["url"])
                    #             topic_fields["videos"] = videos
                    #             topic_fields["videocovers"] = videocovers
                    #         except Exception as e:
                    #             logging.info(f"此新闻无视频{e}")
                    #         # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                    #         # 专题标记topic = 1
                    #         topic_fields["channelName"] = channelname
                    #         topic_fields["channelID"] = channelid
                    #         topic_fields["channeltype"] = channel_type
                    #         topic_fields["workerid"] = article_id
                    #         topic_fields["_id"] = article_title
                    #         topic_fields["contentType"] = article_type
                    #         topic_fields["topicUrl"] = share_url
                    #         topic_fields["pubtime"] = pubtime
                    #         topic_fields["topic"] = topic
                    #         # 将请求文章必需信息存入
                    #         articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                    #         articleparam["articleid"] = article_id
                    #         articlesparams.append(articleparam)
                    #         break
                    #     else:
                    #         article_fields = InitClass().article_fields()
                    #         articleparam = InitClass().article_list_fields()
                    #         # 获取文章列表内的有用信息
                    #         article_id = articles["ID"]
                    #         article_title = articles["title"]
                    #         article_type = articles["biaoqian"]
                    #         share_url = articles["Url"]
                    #         pubtime = int(articles["PublishTime"]) * 1000
                    #         article_covers = list()
                    #         article_cover = articles["pic"]
                    #         article_covers.append(article_cover)
                    #         # 采集视频
                    #         try:
                    #             videocovers = list()
                    #             videocover = articles["video"]["cover"]
                    #             videocovers.append(videocover)
                    #             videoss = articles["video"]["data"]
                    #             videos = list()
                    #             for video in videoss:
                    #                 videos.append(video["url"])
                    #             article_fields["videos"] = videos
                    #             article_fields["videocovers"] = videocovers
                    #         except Exception as e:
                    #             logging.info(f"此新闻无视频{e}")
                    #         # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                    #         article_fields["channelID"] = channelid
                    #         article_fields["channelname"] = channelname
                    #         article_fields["channeltype"] = channel_type
                    #         article_fields["workerid"] = article_id
                    #         article_fields["title"] = article_title
                    #         article_fields["contentType"] = article_type
                    #         article_fields["url"] = share_url
                    #         article_fields["pubtime"] = pubtime
                    #         # 将请求文章必需信息存入
                    #         articleparam["articleField"] = article_fields  # 携带文章采集的数据
                    #         articleparam["articleid"] = article_id
                    #         articlesparams.append(articleparam)
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
            # if topic == 1:
            #     url = "http://cgi.voc.com.cn/app/wxhn/xhn_topic.php?"
            #     headers = {
            #         "Host": "cgi.voc.com.cn",
            #         "Connection": "keep-alive",
            #         "Accept": "application/json, text/javascript, */*; q=0.01",
            #         "Origin": "http://zt.voc.com.cn",
            #         "User-Agent": "xhn-8.6.0-Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKi"
            #                       "t/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
            #         "Referer": "http://zt.voc.com.cn/Topic/xjpfhnkcdytbbdzt/mobile/",
            #         "Accept-Encoding": "gzip, deflate",
            #         "Accept-Language": "zh-CN,en-US;q=0.8",
            #         "X-Requested-With": "com.dingtai.wxhn.activity",
            #     }
            #     data = {
            #         "id": articleid
            #     }
            # else:
            url = "http://app.zhld.com:8090/app_if/getArticleContent"
            headers = {
                'Host': 'app.zhld.com:8090',
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip',
                'User-Agent': 'okhttp/3.8.0',
            }
            data = {
                'articleId':articleid
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
                # print(content_s)
            try:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                print(content_s)
                worker_id = content_s['fileId']
                article_title = content_s["title"]
                author = content_s['editor']
                source = content_s['source']
                content = content_s['content']
                videos = InitClass.get_video(content)
                images = InitClass.get_images(content)
                fields["videocovers"] = images
                fields["images"] = images
                fields["videos"] = videos
                # videos = content_s['widgets']['video']
                # videocovers = content_s['widgets']['pic']
                # fields["videos"] = videos
                # fields["videocover"] = videocovers
                # try:
                #     imagess = content_s['imageUrl']
                #     images = list()
                #     for image in imagess:
                #         images.append(image["url"])
                #     fields["images"] = images
                # except Exception as e:
                #     fields["images"] = []
                fields["appname"] = self.newsname
                fields["title"] = article_title
                fields["workerid"] = worker_id
                fields["content"] = content
                fields["source"] = source
                fields["author"] = author
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
    appspider = XinHuNan("新周口")
    appspider.run()
