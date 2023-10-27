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


class XinHuNan(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://f.rednet.cn/dispatch"
        headers = {
            'Content-type': 'application/json',
            'traceId': '5cef66cf4fa74bcbac3c970ef8726a0e',
            'terminal': '3',
            'bizType': 'channelInfo',
            'bizOp': 'queryAllChannelByGroup',
            'userid': 'W7SuAB06F42h8hFMVRQryg==',
            'version': '3.0',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': 'f.rednet.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'Content-Length': '66',
        }
        data = {"userName":'',"initialFlag":0,"areaCode":"1018001","siteId":31}
        method = "post"
        app_params = InitClass().app_params(url, headers, method, appjson = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        for channel in channelslists["data"]['momentChannel'][0]['channelInfoVoList']:
            channelname = channel['channelName']
            channelid = channel['channelId']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "https://f.rednet.cn/dispatch"
        headers = {
            'Content-type': 'application/json',
            'traceId': 'd6b47d50c1b74f598520909b159aa0f9',
            'terminal': '3',
            'bizType': 'contentIndexDigest',
            'bizOp': 'queryIndexList',
            'version': '3.0',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': 'f.rednet.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'Content-Length': '80',
        }
        method = 'post'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            data = {"channelId":channelid,"areaCode":"1018","siteId":31,"datetime":'',"pageSize":20}
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid = channelid, channeljson=data,
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
                    if 'bannerList' in articleslists['data']:
                        #banner
                        for article in articleslists['data']["bannerList"]:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article['contentId']
                            article_title = article["title"]
                            article_type = article['contentType']
                            share_url = article['shareUrl']
                            pubtime = article['showDate']
                            if  article['contentType'] == 4:
                                #专题
                                topic_fields = InitClass().topic_fields()
                                topic_fields["channelName"] = channelname
                                topic_fields["channelID"] = channelid
                                topic_fields["channeltype"] = channel_type
                                topic_fields["workerid"] = article_id
                                topic_fields["_id"] = article['h5Link']
                                topic_fields["contentType"] = article['contentType']
                                topic_fields["topicUrl"] = share_url
                                topic_fields["pubtime"] = pubtime
                                topic_fields["topic"] = 1
                                articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)
                            else:
                                article_covers = list()
                                article_cover = article['titleImg']
                                article_covers.append(article_cover)
                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["channeltype"] = channel_type
                                article_fields["workerid"] = article_id
                                article_fields["title"] = article_title
                                article_fields["contentType"] = article_type
                                article_fields["url"] = share_url
                                article_fields["pubtime"] = pubtime
                                article_fields["banner"] = 1
                                articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)
                    if 'digestList' in articleslists['data']:
                        for article in articleslists['data']["digestList"]:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article['contentId']
                            article_title = article["title"]
                            article_type = article['contentType']
                            share_url = article['shareUrl']
                            pubtime = article['showDate']
                            if article['contentType'] == 4:
                                # 专题
                                topic_fields = InitClass().topic_fields()
                                topic_fields["channelName"] = channelname
                                topic_fields["channelID"] = channelid
                                topic_fields["channeltype"] = channel_type
                                topic_fields["workerid"] = article_id
                                topic_fields["_id"] =  article['h5Link']
                                topic_fields["contentType"] = article['contentType']
                                topic_fields["topicUrl"] = share_url
                                topic_fields["pubtime"] = pubtime
                                topic_fields["topic"] = 1
                                articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)
                            else:
                                article_covers = list()
                                article_cover = article['titleImg']
                                article_covers.append(article_cover)
                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["channeltype"] = channel_type
                                article_fields["workerid"] = article_id
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
                url = "https://f.rednet.cn/dispatch"
                headers = {
                    'Access-Control-Allow-Credentials': 'true',
                    'Access-Control-Allow-Origin': 'https://hecheng.rednet.cn',
                    'Connection':' keep-alive',
                    'Content-Encoding': 'gzip',
                    'Content-Type': 'text/plain;charset=UTF-8',
                    'Date': 'Fri, 25 Dec 2020 10:17:08 GMT',
                    'Server': 'nginx',
                    'traceid': '1231231',
                    'Transfer-Encoding': 'chunked',
                    'Vary': 'Accept-Encoding',
                    'Vary': 'Origin',
                    'version': '3.0',
                    'X-Application-Context': 'app-api:datasource,rabbitmq,redis-pro,mongodb,pro:8080',
                    'X-Trace-Id': 'a3c5060cbece4fcb885651038a7b8ad3',
                    'X-Version': 'v1',
                }
                data = {
                    "id": articleid
                }
            else:
                url = "https://f.rednet.cn/dispatch"
                headers = {
                    'traceId': '3fb5cca5615647c6b786232edaf12b50',
                    'terminal': '3',
                    'bizType': 'contentDetail',
                    'bizOp': 'queryContentDetail',
                    'userid': 'W7SuAB06F42h8hFMVRQryg==',
                    'version': '3.0',
                    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
                    'Host': 'f.rednet.cn',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                    'Content-Length': '33',
                }
                data = {"contentId":articleid,"siteId":31}
                method = 'post'
                articleparam = InitClass().article_params_fields(url, headers, method, articlejson=data,
                                                                 article_field = article_field)
                articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            topic = fields.get("topic")
            if topic:
                # content_s = json.loads(
                #     json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                print(topic)
            else:
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                    print(content_s)
                    worker_id = content_s["data"]['contentDetailVo']['contentId']
                    article_title = content_s["data"]['contentDetailVo']["title"]
                    author = content_s["data"]['contentDetailVo']["author"]
                    source = content_s["data"]['contentDetailVo']['brand']
                    content = content_s["data"]['contentDetailVo']['contentTex']
                    # print(content)
                    # content = json.loads(f'"{content}"')
                    # content = content.encode('ascii').decode('unicode_escape')
                    comment_num = content_s["data"]['contentDetailVo']['commentCount']
                    url = content_s["data"]['contentDetailVo']['shareUrl']  # 点击数
                    try:
                        if 'Video' in content_s["data"]['contentDetailVo']:
                            fields["videos"] =[content_s["data"]['contentDetailVo']['Video']]
                            fields["videocover"] = [content_s["data"]['contentDetailVo']['titleImg']]
                    except Exception as e:
                        logging.info(f"此新闻无视频{e}")
                    imagess = [content_s["data"]['contentDetailVo']['titleImg']]
                    fields["images"] = imagess
                    fields["appname"] = self.newsname
                    fields["title"] = article_title
                    fields["workerid"] = worker_id
                    fields["content"] = content
                    fields["source"] = source
                    fields["commentnum"] = comment_num
                    fields["author"] = author
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
    appspider = XinHuNan("鹤城融媒")
    appspider.run()
