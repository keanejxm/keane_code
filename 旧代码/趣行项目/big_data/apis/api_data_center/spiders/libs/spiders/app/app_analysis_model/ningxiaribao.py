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

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class Ningxiaribao(Appspider):

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
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))
        for channellists in channelslists["response"]:
            if 'channelItems' in channellists.keys():
                for channel in channellists["channelItems"]:
                    channelname = channel["title"]
                    channelid = channel["channelId"],
                    channeltype = channel['url']
                    channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channeltype)
                    yield channelparam
            else:
                if channellists['channelId'] != '8229':
                    channelname = channellists["title"],
                    channelid = channellists["channelId"],
                    channeltype = channellists['url']
                    channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channeltype)
                    yield channelparam

    def getarticlelistparams(self, channelsres):
        headers = {
            'User-Agent': 'Android',
            'Host': 'app.nxnews.net',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'If-None-Match': "5fe14488-d55f",
        }
        method = 'get'
        channel_num = 0
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")[0]
            channelname = channel.get("channelname")
            url = channel.get('channeltype')
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid=channelid,
                                                                       channel_index_id=channel_index_id)
            yield channel_field, [articlelist_param]

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
                    if 'topic_datas' in articleslists['response'].keys():
                        for articles in articleslists['response']['topic_datas']:
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
                            if channelname == '专题' or articles['docType'] == '30' or articles[
                                'docType'] == '40' or channelname == '政情':
                                topic = 1
                                topic_fields["channelName"] = channelname
                                topic_fields["channelindexid"] = channel_index_id
                                topic_fields["channelID"] = channelid
                                topic_fields["channeltype"] = channel_type
                                topic_fields["topicID"] = article_id
                                topic_fields["title"] = article_title
                                topic_fields["contentType"] = article_type
                                topic_fields["topicUrl"] = share_url
                                topic_fields["pubtime"] = pubtime
                                topic_fields["topic"] = topic
                                yield topic_fields
                            else:
                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["channelindexid"] = channel_index_id
                                article_fields["channeltype"] = channel_type
                                article_fields["workerid"] = article_id
                                article_fields["title"] = article_title
                                article_fields["contentType"] = article_type
                                article_fields["url"] = share_url
                                article_fields["pubtime"] = pubtime
                                article_fields["banner"] = 1
                                yield article_fields
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
                            if channelname == '专题' or articles['docType'] == '30' or articles[
                                'docType'] == '40' or channelname == '政情' or 'showSpecifyPage' in articles.keys():
                                topic = 1
                                topic_fields["channelName"] = channelname
                                topic_fields["channelID"] = channelid
                                topic_fields["channeltype"] = channel_type
                                topic_fields["topicID"] = article_id
                                topic_fields["title"] = article_title
                                topic_fields["contentType"] = article_type
                                topic_fields["topicUrl"] = share_url
                                topic_fields["pubtime"] = pubtime
                                topic_fields["topic"] = topic
                                yield topic_fields
                            else:
                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["channelindexid"] = channel_index_id
                                article_fields["channeltype"] = channel_type
                                article_fields["workerid"] = article_id
                                article_fields["title"] = article_title
                                article_fields["contentType"] = article_type
                                article_fields["url"] = share_url
                                article_fields["pubtime"] = pubtime
                                article_fields["banner"] = 0
                                yield article_fields
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")

    def getarticleparams(self,articleslistsres):
        articleparams = []
        for article in self.analyze_articlelists(articleslistsres):
            articleid = article.get("articleid")
            topic = article.get("topic")
            if topic == 1:
                articleid = article.get("topicID")
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
                    'wcmid': article['workerid']
                }
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                             article_field=article, )
            yield [articleparam]

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
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                # print(content_s)
            if (not topic and banner == 1) or (
                    'content' in articleresjson.keys() and len(articleresjson['content']) < 1 and banner == 0):
                try:
                    url = fields.get("url")
                    res = requests.get(url, header)
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
            if (not topic and banner == 0) and (
                    'content' in articleresjson.keys() and len(articleresjson['content']) > 0):
                try:
                    if 'content' in articleresjson.keys():
                        content_s = json.loads(
                            json.dumps(json.loads(article.get("articleres"), strict=False), indent=4,
                                       ensure_ascii=False))
                        print(content_s)
                        url = fields.get("url")
                        res = requests.get(url, header)
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
                        print(json.dumps(fields, indent=4, ensure_ascii=False))
                    else:
                        try:
                            url = fields.get("url")
                            res = requests.get(url, header)
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
                        fields["platformID"] = self.platform_id
                        fields["title"] = title
                        fields["workerid"] = fields.get('workerid')
                        fields["content"] = content
                        fields["source"] = source
                        fields["pubtime"] = pubtime
                        fields["video"] = video
                        fields = InitClass().wash_article_data(fields)
                        yield {"code": 1, "msg": "OK", "data": {"works": fields}}
                except Exception as e:
                    num += 1
                    logging.info(f"错误数量{num},{e}")

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Ningxiaribao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
