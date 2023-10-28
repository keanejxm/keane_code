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
        url = "https://api.hndaily.cn/api_hn/index.php/column/all3"
        headers = {
            'Content-Length': '0',
            'Host': 'api.hndaily.cn',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MuMu Build/V417IR) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
            'Accept-Encoding': 'gzip',
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method,)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        for channellists in channelslists["result"]:
            channelname = channellists["name"]
            channelid = channellists['colId']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "https://api.hndaily.cn/api_hn/index.php/news/all"
        headers = {
            'Content-Length': '0',
            'Host': 'api.hndaily.cn',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MuMu Build/V417IR) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
            'Accept-Encoding': 'gzip',
        }
        method = 'get'
        topicUrl = 'https://api.hndaily.cn/api_hn/index.php/activity/index'
        topicData = {
            'pageNo': '0'
        }
        channelname = '专题'
        articlelist_param_topic = InitClass().articlelists_params_fields(topicUrl, headers, method, channelname, data= topicData,)
        articlelistsparams.append(articlelist_param_topic)
        videourl = 'https://api.hndaily.cn/api_hn/index.php/news/recommend_video'
        videoData = {
            'pageNo': '0'
        }
        channelname = '视频'
        articlelist_param_video = InitClass().articlelists_params_fields(videourl, headers, method, channelname,
                                                                   data=videoData, )
        articlelistsparams.append(articlelist_param_video)
        smallvideourl = 'https://api.hndaily.cn/api_hn/index.php/news/recommend_video'
        smallvideoData = {
            'pageNo': '0'
        }
        articlelist_param_smallvideo = InitClass().articlelists_params_fields(smallvideourl, headers, method, channelname,
                                                                         data=smallvideoData, )
        articlelistsparams.append(articlelist_param_smallvideo)
        liveurl = 'https://api.hndaily.cn/api_hn/index.php/news/recommend_video'
        liveData = {
            'pageNo': '0'
        }
        articlelist_param_live = InitClass().articlelists_params_fields(liveurl, headers, method,
                                                                              channelname,
                                                                              data=liveData, )
        articlelistsparams.append(articlelist_param_live)
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            data = {
                'pageNo':'0',
                'columnId':channelid
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
                    if 'result' in articleslists.keys():
                        if 'hot' in articleslists['result']:
                            for article in articleslists['result']['hot']:
                                article_fields = InitClass().article_fields()
                                articleparam = InitClass().article_list_fields()
                                topic_fields = InitClass().topic_fields()
                                article_id = article['newsId']
                                article_title = article["title"]
                                article_type = article["type"]
                                images = article["imgUrl"]
                                url = article["url"]
                                if 'sid' in article.keys():
                                    sid = article["sid"]
                                else:
                                    sid = ''
                                topic = 0
                                try:
                                    video = [article["videoUrl"]]
                                    videoCover = images
                                except Exception as e:
                                    print(e)
                                if article["type"] == 'SPECIAL':
                                    topic = 1
                                    topic_fields["channelName"] = channelname
                                    topic_fields["channelID"] = channelid
                                    topic_fields["channeltype"] = channel_type
                                    topic_fields["workerid"] = article_id
                                    topic_fields['_id'] = sid
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
                                    article_fields["video"] = video
                                    article_fields["videocovers"] = videoCover
                                    article_fields["banner"] = 1
                                    # 将请求文章必需信息存入
                                    articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                    articleparam["articleid"] = article_id
                                    articlesparams.append(articleparam)
                        elif 'list' in articleslists['result']:
                            for article in articleslists['result']['hot']:
                                article_fields = InitClass().article_fields()
                                articleparam = InitClass().article_list_fields()
                                topic_fields = InitClass().topic_fields()
                                article_id = article['newsId']
                                article_title = article["title"]
                                article_type = article["type"]
                                images = article["imgUrl"]
                                url = article["url"]
                                topic = 0
                                try:
                                    video = [article["videoUrl"]]
                                    videoCover = images
                                except Exception as e:
                                    print(e)
                                if article["type"] == 'SPECIAL':
                                    topic = 1
                                    topic_fields["channelName"] = channelname
                                    topic_fields["channelID"] = channelid
                                    topic_fields["channeltype"] = channel_type
                                    topic_fields["workerid"] = article_id
                                    topic_fields['_id'] = article_id
                                    topic_fields["title"] = article_title
                                    topic_fields["contentType"] = article_type
                                    topic_fields["topicUrl"] = url
                                    topic_fields["topic"] = topic
                                    # 将请求文章必需信息存入
                                    articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                    articleparam["articleid"] = article_id
                                    articlesparams.append(articleparam)
                                else:
                                    article_fields['channelID'] = channelid
                                    article_fields["channelname"] = channelname
                                    article_fields["channeltype"] = channel_type
                                    article_fields["workerid"] = article_id
                                    article_fields["title"] = article_title
                                    article_fields["contentType"] = article_type
                                    article_fields["url"] = url
                                    article_fields["images"] = images
                                    article_fields["video"] = video
                                    article_fields["videocovers"] = videoCover
                                    article_fields["banner"] = 0
                                    # 将请求文章必需信息存入
                                    articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                    articleparam["articleid"] = article_id
                                    articlesparams.append(articleparam)
                        else:
                            for article in articleslists['result']:
                                print(article)
                                if articleslists['result'].index(article) == 0:
                                    for articless in article['findlist']:
                                        article_fields = InitClass().article_fields()
                                        articleparam = InitClass().article_list_fields()
                                        topic_fields = InitClass().topic_fields()
                                        article_id = articless['newsId']
                                        article_title = articless["title"]
                                        article_type = articless["type"]
                                        images = articless["imgUrl"]
                                        url = articless["url"]
                                        if 'sid' in article.keys():
                                            sid = article["sid"]
                                        else:
                                            sid = ''
                                        topic = 1
                                        topic_fields["channelName"] = channelname
                                        topic_fields["channelID"] = channelid
                                        topic_fields["channeltype"] = channel_type
                                        topic_fields["workerid"] = article_id
                                        topic_fields['_id'] = sid
                                        topic_fields["title"] = article_title
                                        topic_fields["contentType"] = article_type
                                        topic_fields["images"] = images
                                        topic_fields["topicUrl"] = url
                                        topic_fields["topic"] = topic
                                        # 将请求文章必需信息存入
                                        articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                        articleparam["articleid"] = article_id
                                        articlesparams.append(articleparam)
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
                                else:
                                    for articless in article['findlist']:
                                        article_fields = InitClass().article_fields()
                                        articleparam = InitClass().article_list_fields()
                                        topic_fields = InitClass().topic_fields()
                                        article_id = articless['newsId']
                                        article_title = articless["title"]
                                        article_type = articless["type"]
                                        images = articless["imgUrl"]
                                        url = articless["url"]
                                        if 'sid' in article.keys():
                                            sid = article["sid"]
                                        else:
                                            sid = ''
                                        topic = 1
                                        topic_fields["channelName"] = channelname
                                        topic_fields["channelID"] = channelid
                                        topic_fields["channeltype"] = channel_type
                                        topic_fields["workerid"] = article_id
                                        topic_fields['_id'] = sid
                                        topic_fields["title"] = article_title
                                        topic_fields["contentType"] = article_type
                                        topic_fields["images"] = images
                                        topic_fields["topicUrl"] = url
                                        topic_fields["topic"] = topic
                                        # 将请求文章必需信息存入
                                        articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                        articleparam["articleid"] = article_id
                                        articlesparams.append(articleparam)
                                        article_fields["channelID"] = channelid
                                        article_fields["channelname"] = channelname
                                        article_fields["channeltype"] = channel_type
                                        article_fields["workerid"] = article_id
                                        article_fields["title"] = article_title
                                        article_fields["contentType"] = article_type
                                        article_fields["url"] = url
                                        article_fields["images"] = images
                                        article_fields["banner"] = 0
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
                url = "https://api.hndaily.cn/api_hn/index.php/special/index"
                headers = {
                    'Content-Length': '0',
                    'Host': 'api.hndaily.cn',
                    'Connection': 'Keep-Alive',
                    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MuMu Build/V417IR) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
                    'Accept-Encoding': 'gzip',
                }
                data = {
                    'sid': article_field['_id']
                }
            else:
                url = "https://api.hndaily.cn/api_hn/index.php/news/one"
                headers = {
                    'Content-Length': '0',
                    'Host': 'api.hndaily.cn',
                    'Connection': 'Keep-Alive',
                    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MuMu Build/V417IR) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
                    'Accept-Encoding': 'gzip',
                }
                data = {
                    'colId':article_field.get('channelID'),
                    'newsId':articleid,
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
                articlesparams = []
                if "result" in content_s.keys():
                    for articles_arr in content_s["result"]["type"]:
                        for articles in articles_arr['listnews']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            # 获取文章列表内的有用信息
                            article_id = articles["newsId"]
                            article_title = articles["title"]
                            article_type = articles["type"]
                            share_url = articles['url']
                            article_covers = articles['imgUrl']
                            if "videoUrl" in articles.keys():
                                videos = [articles ['videoUrl']]
                            else:
                                videos = []
                            article_fields["videos"] = videos
                            article_fields["channelID"] = articles ['colId']
                            article_fields["videocovers"] = article_covers
                            article_fields["channelID"] = articles ['colId']
                            article_fields["channelname"] = fields.get("channelName")
                            article_fields["channeltype"] = article_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["contentType"] = article_type
                            article_fields["url"] = share_url
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
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                    if "result" in content_s.keys():
                        worker_id = content_s["result"]["news"]['newsId']
                        article_title = content_s["result"]["news"]["title"]
                        source = content_s["result"]["news"]["source"]
                        content = content_s["result"]["news"]["content"]
                        comment_num = content_s["result"]["news"]['allow_comment']
                        pubtime = InitClass().date_time_stamp(content_s["result"]["news"]['createTime'])
                        if 'videoUrl' in content_s["result"]["news"]:
                            videos = [content_s["result"]["news"]['videoUrl']]
                        else:
                            videos = []
                        if content != '':
                            images = InitClass.get_images(content)
                        else:
                            images = content_s["result"]["news"]['imgUrl']
                        videocovers = images
                        fields["videos"] = videos
                        fields["videocover"] = videocovers
                        fields["images"] = images
                        fields["appname"] = self.newsname
                        fields["title"] = article_title
                        fields["workerid"] = worker_id
                        fields["content"] = content
                        fields["source"] = source
                        fields["commentnum"] = comment_num
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
    appspider = XinHuNan("海南日报")
    appspider.run()
