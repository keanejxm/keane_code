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
from appspider_m import Appspider
from initclass import InitClass


class XinHuNan(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://app2.dxhmt.cn:10326/api/common/menu"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '174',
            'Host': 'app2.dxhmt.cn:10326',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/4.6.0',
        }
        data = {
            'appId': 'dxrma6af7651c63bbb9efcc15ddf1578',
            'timestamp': int(time.time()),
            'sign': '1d726a9a1f0f3a8c9362aa5a0a989850',
            'token': '',
            'personId': '',
            'imei': '377818c4-4cbd-46f1-891a-a6f0cd57538e',
            'source': 'Android',
        }
        method = "post"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))

        for channel in channelslists["data"]:
            channelname = channel['pageName']
            channelid = channel['pageId']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "http://app2.dxhmt.cn:10326/api/sub/article/mergeListNew"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '229',
            'Host': 'app2.dxhmt.cn:10326',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/4.6.0',
        }
        method = 'post'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            data = {
                'page':'1',
                'size':'20',
                'pageId':channelid,
                'appId':'dxrma6af7651c63bbb9efcc15ddf1578',
                'timestamp':int(time.time()),
                'sign':'64c8123ad5f07c0ee0889d088f40fcb3',
                'token':'',
                'personId':'',
                'imei':'377818c4-4cbd-46f1-891a-a6f0cd57538e',
                'source':'Android',
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
                    for articles in articleslists["data"]:
                        if articles['objectType']=='25':
                            #banner
                            if "data" in articles.keys():
                                for article in articles["data"]:
                                    article_fields = InitClass().article_fields()
                                    articleparam = InitClass().article_list_fields()
                                    article_id = article['articleId']
                                    article_title = article['articleTitle']
                                    article_type = article['infoType']
                                    pubtime = InitClass().date_time_stamp(article['createTime'])
                                    article_covers = list()
                                    article_cover = article['cover']
                                    article_covers.append(article_cover)
                                    images = article['photo']
                                    # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                                    article_fields["channelID"] = channelid
                                    article_fields["channelname"] = channelname
                                    article_fields["channeltype"] = channel_type
                                    article_fields["workerid"] = article_id
                                    article_fields["title"] = article_title
                                    article_fields["contentType"] = article_type
                                    article_fields["images"] = images
                                    article_fields["pubtime"] = pubtime
                                    article_fields["banner"] = 1
                                    # 将请求文章必需信息存入
                                    articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                    articleparam["articleid"] = article_id
                                    articlesparams.append(articleparam)
                        elif articles['objectType']=='22' or articles['objectType']=='21':
                            topic_fields = InitClass().topic_fields()                            #专题
                            topic = 0
                            if articles['objectType']=='22':
                                topic = 1
                                topic_fields["topic"] = topic
                            if "data" in articles.keys():
                                for article in articles["data"]:
                                    articleparam = InitClass().article_list_fields()
                                    article_id = article['articleId']
                                    article_type = article['infoType']
                                    pubtime = InitClass().date_time_stamp(article['createTime'])
                                    article_covers = list()
                                    article_cover = article['cover']
                                    article_covers.append(article_cover)
                                    topic_fields["channelName"] = channelname
                                    topic_fields["channelID"] = channelid
                                    topic_fields["channeltype"] = channel_type
                                    topic_fields["workerid"] = article_id
                                    topic_fields["_id"] = article['moduleId']
                                    topic_fields["contentType"] = article_type
                                    topic_fields["pubtime"] = pubtime
                                    articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                    articleparam["articleid"] = article_id
                                    articlesparams.append(articleparam)
                        else:
                            for article in articles["data"]:
                                article_fields = InitClass().article_fields()
                                articleparam = InitClass().article_list_fields()
                                # 获取文章列表内的有用信息
                                article_id = article['articleId']
                                article_title = article['articleTitle']
                                article_type = article['type']
                                pubtime = InitClass().date_time_stamp(article['createTime'])
                                article_covers = list()
                                article_cover = article['covers']
                                article_covers.append(article_cover)
                                if 'photo' in article.keys():
                                    images = article['photo']
                                else:
                                    images = []
                                # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["channeltype"] = channel_type
                                article_fields["workerid"] = article_id
                                article_fields["title"] = article_title
                                article_fields["contentType"] = article_type
                                article_fields["images"] = images
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
                url = "http://app2.dxhmt.cn:10326/api/sub/article/zoneNewPro"
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Content-Length': '229',
                    'Host': 'app2.dxhmt.cn:10326',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                    'User-Agent': 'okhttp/4.6.0',
                }
                data = {
                    'page':'1',
                    'size':'20',
                    'zoneId': articleid,
                    'appId': 'dxrma6af7651c63bbb9efcc15ddf1578',
                    'timestamp': int(time.time()),
                    'sign': 'cb21625e150f2f0118061f6430b1cc83',
                    'token': '',
                    'personId': '',
                    'imei': '377818c4-4cbd-46f1-891a-a6f0cd57538e',
                    'source': 'Android',
                }
            else:
                url = "http://app2.dxhmt.cn:10326/api/sub/article/detailNew"
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Content-Length': '217',
                    'Host': 'app2.dxhmt.cn:10326',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                    'User-Agent': 'okhttp/4.6.0',
                }
                data = {
                    'articleId':articleid,
                    'appId':'dxrma6af7651c63bbb9efcc15ddf1578',
                    'timestamp':int(time.time()),
                    'sign':'cb21625e150f2f0118061f6430b1cc83',
                    'token':'',
                    'personId':'',
                    'imei':'377818c4-4cbd-46f1-891a-a6f0cd57538e',
                    'source':'Android',
                }
            method = 'post'
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
                articlesparams = []
                if "result" in content_s.keys():
                    for articles_arr in content_s["result"]["data"]:
                        for articles in articles_arr['list']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            # 获取文章列表内的有用信息
                            article_id = articles['data'][0]['articleId']
                            article_title = articles['data'][0]['articleTitle']
                            article_type = articles['data'][0]["type"]
                            article_covers = articles['data'][0]['covers']
                            if "videoUrl" in articles.keys():
                                videos = [articles['videoUrl']]
                            else:
                                videos = []
                            article_fields["videos"] = videos
                            article_fields["channelID"] = fields['channelID']
                            article_fields["videocovers"] = article_covers
                            article_fields["channelname"] = content_s['data']['zone']['articleTitle']
                            article_fields["channeltype"] = article_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["contentType"] = article_type
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
                    print(content_s)
                    if "data" in content_s.keys():
                        worker_id = content_s["data"]['articleId']
                        article_title = content_s["data"]['articleTitle']
                        source = content_s["data"]['publishName']
                        content = content_s["data"]['htmlContent']
                        comment_num = content_s["data"]['commentNum']
                        read_num = content_s["data"]['viewsNum']
                        author= content_s["data"]['publishName']
                        like_num = content_s["data"]['praiseNum']
                        tran_num = content_s["data"]['forwardNum']
                        url = 'http://app2.dxhmt.cn:10326'+content_s["data"]['share']['shareUrl']
                        videos = InitClass().get_video(content)
                        images = InitClass().get_images(content)
                        videocovers = content_s["data"]['covers']
                        fields["videos"] = videos
                        fields["videocover"] = videocovers
                        fields["images"] = images
                        try:
                            videocovers = content_s["data"]['covers']
                            if content_s["data"]['moduleId'] == 4:
                                fields["videos"] = ['http://app2.dxhmt.cn:10326/'+content]
                                content = ''
                        except Exception as e:
                            logging.info(f"此新闻无视频{e}")
                        # try:
                        #     images = content_s["data"]['resources']
                        #     fields["images"] = images
                        # except Exception as e:
                        #     self.logger.info(f"获取文章内图片失败{e}")
                        fields["appname"] = self.newsname
                        fields["title"] = article_title
                        fields["workerid"] = worker_id
                        fields["content"] = content
                        fields["source"] = source
                        fields["commentnum"] = comment_num
                        fields["author"] = author
                        fields["readnum"] = read_num
                        fields["trannum"] = tran_num
                        fields["likenum"] = like_num
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
    appspider = XinHuNan("汝阳融媒")
    appspider.run()
