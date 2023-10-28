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
        url = "http://app.nxnews.net/ningxia/cfwz/index.json"
        headers = {
            'User-Agent': 'Android',
            'Host': 'app.nxnews.net',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'If-None-Match': "5fb63a42-1547",
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        for channellists in channelslists["response"]:
                if 'channelItems' in channellists.keys():
                    for channel in channellists["channelItems"]:
                        channelname = channel["title"]
                        channelid = channel["channelId"],
                        channeltype = channel['url']
                        channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channeltype)
                        channelsparams.append(channelparam)
                else:
                    if channellists['channelId'] != '8229':
                        channelname = channellists["title"],
                        channelid = channellists["channelId"],
                        channeltype = channellists['url']
                    channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channeltype)
                    channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        headers = {
            'User-Agent': 'Android',
            'Host': 'app.nxnews.net',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'If-None-Match': "5fe14488-d55f",
        }
        method = 'get'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            url = channel.get('channeltype')
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid = channelid)
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
                    if 'topic_datas' in articleslists['response'].keys():
                        for  articles in articleslists['response']['topic_datas']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            topic_fields = InitClass().topic_fields()
                            article_id = articles['docId']
                            article_title = articles["title"]
                            article_type = articles['docType']
                            share_url = articles["url"]
                            pubtime = InitClass().date_time_stamp(articles['ptime'])
                            article_covers = list()
                            article_cover = articles['imagesUrl']
                            article_covers.append(article_cover)
                            topic = 0
                            if channelname == '专题' or articles['docType'] == '30' or articles['docType'] == '40' or channelname=='政情':
                                topic = 1
                                topic_fields["channelName"] = channelname
                                topic_fields["channelID"] = channelid
                                topic_fields["channeltype"] = channel_type
                                topic_fields["workerid"] = article_id
                                topic_fields["title"] = article_title
                                topic_fields["contentType"] = article_type
                                topic_fields["topicUrl"] = share_url
                                topic_fields["pubtime"] = pubtime
                                topic_fields["topic"] = topic
                                articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articleparam['articlecovers'] = article_covers
                                articlesparams.append(articleparam)
                            else:
                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["channeltype"] = channel_type
                                article_fields["workerid"] = article_id
                                article_fields["title"] = article_title
                                article_fields["contentType"] = article_type
                                article_fields["url"] = share_url
                                article_fields["pubtime"] = pubtime
                                article_fields["banner"] = 1
                                # 将请求文章必需信息存入
                                articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articleparam['articlecovers'] = article_covers
                                articlesparams.append(articleparam)
                    if 'datas' in articleslists['response'].keys():
                        for articles in articleslists['response']['datas']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            topic_fields = InitClass().topic_fields()
                            article_id = articles['docId']
                            article_title = articles["title"]
                            article_type = articles['docType']
                            share_url = articles["url"]
                            pubtime = InitClass().date_time_stamp(articles['ptime'])
                            article_covers = list()
                            article_cover = articles['imagesUrl']
                            article_covers.append(article_cover)
                            topic = 0
                            if channelname == '专题' or articles['docType'] == '30' or articles['docType'] == '40' or channelname=='政情' or 'showSpecifyPage' in articles.keys():
                                topic = 1
                                topic_fields["channelName"] = channelname
                                topic_fields["channelID"] = channelid
                                topic_fields["channeltype"] = channel_type
                                topic_fields["workerid"] = article_id
                                topic_fields["title"] = article_title
                                topic_fields["contentType"] = article_type
                                topic_fields["topicUrl"] = share_url
                                topic_fields["pubtime"] = pubtime
                                topic_fields["topic"] = topic
                                articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articleparam['articlecovers'] = article_covers
                                articlesparams.append(articleparam)
                            else:
                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["channeltype"] = channel_type
                                article_fields["workerid"] = article_id
                                article_fields["title"] = article_title
                                article_fields["contentType"] = article_type
                                article_fields["url"] = share_url
                                article_fields["pubtime"] = pubtime
                                article_fields["banner"] = 0
                                # 将请求文章必需信息存入
                                articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articleparam['articlecovers'] = article_covers
                                articlesparams.append(articleparam)




                    # for articles in articleslists['response']["value"]:
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
            if topic == 1:
                url = "http://cgi.voc.com.cn/app/wxhn/xhn_topic.php?"
                headers = {
                }
                data = {
                    "id": articleid
                }
            else:
                url = "http://app.nxnews.net/analysis/data/findDataInfoByWcmid"
                headers = {
                    'Host': 'app.nxnews.net',
                    'Connection': 'keep-alive',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'X-Requested-With': 'XMLHttpRequest',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36',
                    'Referer': 'http://app.nxnews.net/ningxia/cfwz/yw/202012/t20201221_6974218.html',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,en-US;q=0.8',
                    'Cookie': '_trs_uv=kizaill4_1120_ah3n; _trs_ua_s_1=kizd9rt1_1120_khb2',

                }
                data = {
                    'wcmid': article_field['workerid']
                }
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, data = data,
                                                             article_field = article_field,)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        header = {
            'Host': 'app.nxnews.net',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'Cookie': '_trs_uv=kizaill4_1120_ah3n',
            'X-Requested-With': 'com.trs.nxnews',
        }
        for article in articleres:
            fields = article.get("articleField")
            topic = fields.get("topic")
            banner = fields.get("banner")
            articleresjson = json.loads(article.get("articleres"))
            if topic:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                # print(content_s)
            if (not topic and banner == 1) or ( 'content' in articleresjson.keys() and len(articleresjson['content'])<1 and banner == 0):
                try:
                    url = fields.get("url")
                    res = requests.get(url,header)
                    res.encoding = res.apparent_encoding
                    html = res.text
                    bf = bs4.BeautifulSoup(html, 'html.parser')
                    title = bf.find('h2').text
                    source = bf.select('header p span')[0].text.replace('来源:', '')
                    pubtime = bf.select('header p span')[1].text.replace('时间:', '')
                    content = bf.find('section', class_='content')
                    title = title  # 标题
                    source = source  # 来源
                    content = str(content)  # 文章内容
                    if '<video' in content:
                        video = InitClass.get_video(content)
                    else:
                        video = []
                    pubtime = InitClass().date_time_stamp(pubtime)  # 发布时间
                except Exception as e:
                    print(e)
                fields["appname"] = self.newsname
                fields["title"] = title
                fields["workerid"] = fields.get('workerid')
                fields["content"] = content
                fields["source"] = source
                fields["pubtime"] = pubtime
                fields["video"] = video
                print(json.dumps(fields, indent=4, ensure_ascii=False))
            if (not topic and banner == 0) and ( 'content' in articleresjson.keys() and len(articleresjson['content'])>0):
                try:
                    if 'content' in articleresjson.keys():
                        content_s = json.loads(
                            json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                        print(content_s)
                        url = fields.get("url")
                        res = requests.get(url,header)
                        res.encoding = res.apparent_encoding
                        html = res.text
                        bf = bs4.BeautifulSoup(html, 'html.parser')
                        worker_id = fields.get('workerid')
                        title = bf.find('h2').text
                        source = bf.select('header p span')[0].text.replace('来源:', '')
                        pubtime = bf.select('header p span')[1].text.replace('时间:', '')
                        content = bf.find('section', class_='content')
                        content = str(content)  # 文章内容
                        if '.mp4' in content:
                            video = InitClass.get_video(content)
                        else:
                            video = []
                        pubtime = InitClass().date_time_stamp(articleresjson["content"][0]['DOCPUBTIME'])  # 发布时间
                        fields["appname"] = self.newsname
                        fields["title"] = title
                        fields["workerid"] = worker_id
                        fields["content"] = content
                        fields["source"] = source
                        fields["video"] = video
                        print(json.dumps(fields, indent = 4, ensure_ascii = False))
                    else:
                        try:
                            url = fields.get("url")
                            res = requests.get(url,header)
                            res.encoding = res.apparent_encoding
                            html = res.text
                            bf = bs4.BeautifulSoup(html, 'html.parser')
                            title = bf.find('h2').text
                            source = bf.select('header p span')[0].text.replace('来源:', '')
                            pubtime = bf.select('header p span')[1].text.replace('时间:', '')
                            content = bf.find('section', class_='content')
                            title = title  # 标题
                            source = source  # 来源
                            content = str(content)  # 文章内容
                            if '<video' in content:
                                video = InitClass.get_video(content)
                            else:
                                video = []
                            pubtime = InitClass().date_time_stamp(pubtime)  # 发布时间
                        except Exception as e:
                            print(e)
                        fields["appname"] = self.newsname
                        fields["title"] = title
                        fields["workerid"] = fields.get('workerid')
                        fields["content"] = content
                        fields["source"] = source
                        fields["pubtime"] = pubtime
                        fields["video"] = video
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
    appspider = XinHuNan("宁夏日报")
    appspider.run()
