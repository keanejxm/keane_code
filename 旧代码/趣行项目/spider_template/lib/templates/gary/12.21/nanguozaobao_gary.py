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
import requests
from appspider_m import Appspider
from initclass import InitClass


class XinHuNan(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://app-h5.ngzb.com.cn/v2/channel/list"
        headers = {
            'sysType': 'android',
            'versionCode': '87',
            'deviceInfo': '%7B%22os%22%3A%22Android%22%2C%22osVersion%22%3A23%2C%22appVersion%22%3A%223.1.3%22%2C%22brand%22%3A%22Android%22%2C%22board%22%3A%22unknown%22%2C%22name%22%3A%22cancro%22%2C%22device%22%3A%22x86%22%2C%22model%22%3A%22MuMu%22%2C%22hardware%22%3A%22cancro%22%2C%22id%22%3A%22V417IR%22%2C%22manufacturer%22%3A%22Netease%22%2C%22codename%22%3A%22REL%22%2C%22incremental%22%3A%22eng.luoweiqiao.20201126.145300%22%2C%22release%22%3A%226.0.1%22%2C%22network%22%3A%22WIFI%22%2C%22carrier%22%3A%22%E6%9C%AA%E7%9F%A5%22%7D',
            'version': '3.1.3',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': 'app-h5.ngzb.com.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'Content-Length': '268',
        }
        data = {
            'app_id':'5020',
            'app_key':'731e52172f9872d6062a5c48c46ab863',
            'device_info':'MuMu',
            'device_manufacturer':'Netease',
            'equip_type':'0',
            'lat':'0.0',
            'lng':'0.0',
            'market_channel':'xiaomi',
            'news_type':'0',
            'sysType':'Android',
            't_login':'0',
            'timestamp':int(time.time()),
            'uid':'FAFD5191B65EF6D00BB97113A9EFB80E',
            'uuid':'',
            'version':'3.13',
        }
        method = "post"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        for channel in channelslists["data"]['channel_list']:
            if channel["id"]!='300001292' and channel["id"]!='300001269':
                channelname = channel["name"]
                channelid = channel["id"]
                channelparam = InitClass().channel_fields(channelid, channelname)
                channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "http://app-h5.ngzb.com.cn/v2/news/list"
        headers = {
            'versionCode': '87',
            'sysType': 'Android',
            'version': '3.1.3',
            'version': '3.1.3',
            'versionCode': '87',
            'sysType': 'Android',
            'Host': 'app-h5.ngzb.com.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.12.0'
        }
        method = 'get'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            data = {
                'app_id':'5020',
                'app_key':'731e52172f9872d6062a5c48c46ab863',
                'equip_type':'0',
                'uid':'FAFD5191B65EF6D00BB97113A9EFB80E',
                'type_id':channelid,
                'timestamp':int(time.time()),
                'updown':'0',
                'sysType':'Android',
                'version':'3.1.3',
                'showed_newslist':'',
                'page':'1',
                'address':'广西壮族自治区南宁市青秀区民主路21-16号',
                'lat':'39.914938',
                'lng':'116.403699',
                'pos_code':'18607718647（07712083353）',
                'pos_name':'南宁（默认定位）',
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
                    for articles in articleslists["data"]:
                        if articles:
                            if 'recycle_newslist' in articles.keys():
                                for article in articles["recycle_newslist"]['newslist']:
                                    if not 'reply' in article.keys():
                                        article_fields = InitClass().article_fields()
                                        articleparam = InitClass().article_list_fields()
                                        topic_fields = InitClass().topic_fields()
                                        article_id = article["news_id"]
                                        article_title = article["title"]
                                        article_type = article["type"]
                                        share_url = article["url"]
                                        pubtime = int(article['import_time'])
                                        if article['type'] == '3':
                                            topic_fields = InitClass().topic_fields()
                                            articleparam = InitClass().article_list_fields()
                                            # 专题
                                            topic = 1
                                            article_id = article["news_id"]
                                            article_title = article["title"]
                                            article_type = article["type"]
                                            share_url = article["url"]
                                            pubtime = int(article['import_time'])
                                            topic_fields["channelName"] = channelname
                                            topic_fields["channelID"] = channelid
                                            topic_fields["channeltype"] = channel_type
                                            topic_fields["workerid"] = article_id
                                            topic_fields["_id"] = article_id
                                            topic_fields["contentType"] = article_type
                                            topic_fields["topicUrl"] = share_url
                                            topic_fields["pubtime"] = pubtime
                                            topic_fields["topic"] = topic
                                            # 将请求文章必需信息存入
                                            articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                            articleparam["articleid"] = article_id
                                            articlesparams.append(articleparam)
                                        if 'live_info' in article.keys():
                                            video_cover = [article['live_info']['cover']]
                                            videos = [article['live_info']['videoUrl']]
                                            article_fields["videos"] = videos
                                            article_fields["videocovers"] = video_cover
                                        if 'isIOSTopCarousel' in article.keys():
                                            #banner
                                            article_fields["banner"] = 1
                                        article_fields["channelID"] = channelid
                                        article_fields["channelname"] = channelname
                                        article_fields["channeltype"] = channel_type
                                        article_fields["workerid"] = article_id
                                        article_fields["title"] = article_title
                                        article_fields["contentType"] = article_type
                                        article_fields["url"] = share_url
                                        article_fields["pubtime"] = pubtime
                                        # 将请求文章必需信息存入
                                        articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                        articleparam["articleid"] = article_id
                                        articlesparams.append(articleparam)
                            else:
                                if articles['type'] == '3':
                                    topic_fields = InitClass().topic_fields()
                                    articleparam = InitClass().article_list_fields()
                                    #专题
                                    topic = 1
                                    article_id = articles["news_id"]
                                    article_title = articles["title"]
                                    article_type = articles["type"]
                                    share_url = articles["url"]
                                    pubtime = int(articles['import_time'])
                                    topic_fields["channelName"] = channelname
                                    topic_fields["channelID"] = channelid
                                    topic_fields["channeltype"] = channel_type
                                    topic_fields["workerid"] = article_id
                                    topic_fields["_id"] = article_id
                                    topic_fields["contentType"] = article_type
                                    topic_fields["topicUrl"] = share_url
                                    topic_fields["pubtime"] = pubtime
                                    topic_fields["topic"] = topic
                                    # 将请求文章必需信息存入
                                    articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                    articleparam["articleid"] = article_id
                                    articlesparams.append(articleparam)
                                if articles['type'] != '3' and articles['type'] != '8':
                                    article_fields = InitClass().article_fields()
                                    articleparam = InitClass().article_list_fields()
                                    article_id = articles["news_id"]
                                    article_title = articles["title"]
                                    article_type = articles["type"]
                                    share_url = articles["url"]
                                    pubtime = int(articles['import_time'])
                                    if 'live_info' in articles.keys():
                                        video_cover = [articles['live_info']['cover']]
                                        videos = [articles['live_info']['videoUrl']]
                                        article_fields["videos"] = videos
                                        article_fields["videocovers"] = video_cover
                                    article_fields["channelID"] = channelid
                                    article_fields["channelname"] = channelname
                                    article_fields["channeltype"] = channel_type
                                    article_fields["workerid"] = article_id
                                    article_fields["title"] = article_title
                                    article_fields["contentType"] = article_type
                                    article_fields["url"] = share_url
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
                topicmoduleurl = f"http://app-h5.ngzb.com.cn/newsSpecialGetModelBySpecialId?specialId={articleid}"
                res = requests.get(topicmoduleurl).json()
                if res['moduleList']:
                    url = 'http://app-h5.ngzb.com.cn/special/newsList'
                    headers = {
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Cookie': 'Hm_lvt_b47affbfae8961532cba4cda75ab81db=1608793136; JSESSIONID=aaaJyH16LRNny6RBSNBwx; Hm_lpvt_b47affbfae8961532cba4cda75ab81db=1608793539',
                        'Host': 'app-h5.ngzb.com.cn',
                        'Proxy-Connection': 'keep-alive',
                        'Referer': 'http://app-h5.ngzb.com.cn/newsSpecialgetSpecialInfo?app_id=5020&platform_id=6&specialId=1683',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
                        'X-Requested-With': 'XMLHttpRequest',
                    }
                    for module in res['moduleList']:
                        data = {
                            'specialId': articleid,
                            'moduleId': module['id'],
                            'pageNum': '1',
                            'pageSize': '10',
                        }
                        method = 'get'
                        channelname = '专题'
                        articleparam = InitClass().article_params_fields(url,headers, method, channelname,  data=data,
                                                                         article_field=article_field)
                        articleparams.append(articleparam)
            else:
                url = "https://app-h5.ngzb.com.cn/index.action"
                headers = {
                    'Host': 'app-h5.ngzb.com.cn',
                    'Connection': 'keep-alive',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36',
                    'Accept': '*/*',
                    'Referer': 'https://app-h5.ngzb.com.cn/testSw.js',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,en-US;q=0.8',
                    'X-Requested-With': 'com.myxianwen.nanguozaobao',
                }
                data = {
                    'action':'getNewsById',
                    'app_id':'5020',
                    'app_key':'6b88046faebf9775e2c75d84113c6f34',
                    'params':'{"news_id":"'+str(articleid)+'"}'
                }
                method = 'get'
                channelname = article_field.get('channelname')
                articleparam = InitClass().article_params_fields(url, headers, method, channelname,data = data,
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
                articlesparams = []
                if "data" in content_s.keys():
                    for articles in content_s["data"]:
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        # 获取文章列表内的有用信息
                        article_id = articles['news_id']
                        article_title = articles["title"]
                        article_covers = articles['image']
                        if "videoUrl" in articles.keys():
                            videos = [articles['videoUrl']]
                        else:
                            videos = []
                        article_fields["videos"] = videos
                        article_fields["videocovers"] = article_covers
                        article_fields["channelID"] = articles['specialId']
                        article_fields["channelname"] = fields.get("channelName")
                        article_fields["workerid"] = article_id
                        article_fields["title"] = article_title
                        article_fields["specialtopic"] = topic
                        article_fields["topicid"] = fields.get('_id')
                        articleparam["articleField"] = article_fields  # 携带文章采集的数据
                        articleparam["articleid"] = article_id
                        articlesparams.append(articleparam)
                    aaaa = self.getarticleparams(articlesparams)
                    bbbb = self.getarticlehtml(aaaa.__next__())
                    self.analyzearticle(bbbb.__next__())
            else:
                try:
                    if article.get("articleres") != '':
                        content_s = json.loads(
                            json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                        if "news" in content_s["data"]:
                            worker_id = content_s["data"]["news"]['news_id']
                            article_title = content_s["data"]["news"]["title"]
                            author = content_s["data"]["news"]['editor_name']
                            source = content_s["data"]["news"]['media_name']
                            content = content_s["data"]["news"]["content"]
                            comment_num = content_s["data"]['commentCount']
                            read_num = content_s["data"]['browseCount']
                            like_num = content_s["data"]['likeCount']
                            videos = [content_s["data"]['tts']]
                            videocovers = [content_s["data"]["news"]["image"]]
                            images = [content_s["data"]["news"]["image"]]
                            fields["readnum"] = read_num
                            fields["likenum"] = like_num
                            fields["images"] = images
                            fields["videos"] = videos
                            fields["videocover"] = videocovers
                            fields["appname"] = self.newsname
                            fields["title"] = article_title
                            fields["workerid"] = worker_id
                            fields["content"] = content
                            fields["source"] = source
                            fields["commentnum"] = comment_num
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
    appspider = XinHuNan("南国早报")
    appspider.run()
