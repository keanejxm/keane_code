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


class Shanxiribao(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://sxapi.sxrbw.com/api/v2/menus/"
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36',
            'Host': 'sxapi.sxrbw.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        data = {
            'platform':'android',
            'clientVersionCode':'61',
            'deviceOs':'6.0.1',
            'pjCode':'code_sxrb',
            'device_size':'810.0x1440.0',
            'clientVersion':'4.4.6',
            'deviceModel':'Netease-MuMu',
            'udid':'010000000308435',
            'channel':'xiaomi',
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        for channel in channelslists["items"]:
            channelname = channel['name']
            channelid = channel['categoryId']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36',
            'Host': 'sxapi.sxrbw.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        method = 'get'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            url = f'http://sxapi.sxrbw.com/api/v2/articles/{channelid}'
            data = {
                'pageToken': '',
                'size': '20',
                'platform': 'android',
                'clientVersionCode': '61',
                'deviceOs': '6.0.1',
                'pjCode': 'code_sxrb',
                'device_size': '810.0x1440.0',
                'clientVersion': '4.4.6',
                'deviceModel': 'Netease-MuMu',
                'udid': 'Netease-MuMu',
                'channel': 'xiaomi',
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
                    if 'head' in articleslists['item'].keys():
                        # banner
                        for article in articleslists["item"]['head']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article['articleId']
                            article_title = article["title"]
                            article_type = article['type']
                            share_url = article['shareUrl']
                            pubtime = int(InitClass().date_time_stamp(InitClass.format_date(article["date"]))) * 1000
                            try:
                                article_covers = article['images']
                            except Exception as e:
                                print(e)
                            if article['type'] == 'subject':
                                topic_fields = InitClass().topic_fields()
                                topic_fields["channelName"] = channelname
                                topic_fields["channelID"] = channelid
                                topic_fields["channeltype"] = channel_type
                                topic_fields["workerid"] = article_id
                                topic_fields["topicID"] = article_id
                                topic_fields["title"] = article_title
                                topic_fields["topicUrl"] = share_url
                                topic_fields["pubtime"] = pubtime
                                topic_fields['topicCover'] = article_covers
                                topic_fields["topic"] = 1
                                # 将请求文章必需信息存入
                                articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)
                            else:
                                if 'medias' in article.keys() and article['type']=='video':
                                    for video in article['medias']:
                                        videos = [video['resources'][0]['url']]
                                        article_fields["videos"] = videos
                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["channeltype"] = channel_type
                                article_fields["workerid"] = article_id
                                article_fields["title"] = article_title
                                article_fields["contentType"] = article_type
                                article_fields["url"] = share_url
                                article_fields["pubtime"] = pubtime
                                article_fields["articlecovers"] = article_covers
                                article_fields["banner"] = 1
                                # 将请求文章必需信息存入
                                articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)
                    if 'list' in articleslists['item'].keys():
                        for article in articleslists["item"]['list']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article['articleId']
                            article_title = article["title"]
                            article_type = article['type']
                            share_url = article['shareUrl']
                            pubtime = int(InitClass().date_time_stamp(InitClass().format_date(article["date"]))) * 1000
                            if article['type'] == 'card' and 'cardArticleList' in article.keys():
                                for card in article['cardArticleList']:
                                    article_id = card['articleId']
                                    article_title = card["title"]
                                    article_type = card['type']
                                    share_url = card['shareUrl']
                                    pubtime = int(InitClass().date_time_stamp(InitClass().format_date(card["date"]))) * 1000
                                    try:
                                        article_covers = [card['imageUrl']]
                                    except Exception as e:
                                        print(e)
                                    if card['type'] == 'subject':
                                        topic_fields = InitClass().topic_fields()
                                        topic_fields["channelName"] = channelname
                                        topic_fields["channelID"] = channelid
                                        topic_fields["channeltype"] = channel_type
                                        topic_fields["workerid"] = article_id
                                        topic_fields["topicID"] = article_id
                                        topic_fields["title"] = article_title
                                        topic_fields["topicUrl"] = share_url
                                        topic_fields["pubtime"] = pubtime
                                        topic_fields['topicCover'] = article_covers
                                        # 将请求文章必需信息存入
                                        articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                        articleparam["articleid"] = article_id
                                        articlesparams.append(articleparam)
                                    else:
                                        if 'medias' in card.keys():
                                            for video in card['medias']:
                                                videos = [video['resources'][0]['url']]
                                                article_fields["videos"] = videos
                                        article_fields["channelID"] = channelid
                                        article_fields["channelname"] = channelname
                                        article_fields["channeltype"] = channel_type
                                        article_fields["workerid"] = article_id
                                        article_fields["title"] = article_title
                                        article_fields["contentType"] = article_type
                                        article_fields["url"] = share_url
                                        article_fields["pubtime"] = pubtime
                                        article_fields["articlecovers"] = article_covers
                                        # 将请求文章必需信息存入
                                        articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                        articleparam["articleid"] = article_id
                                        articlesparams.append(articleparam)
                            elif article['type'] == 'subject':
                                try:
                                    article_covers = article['images']
                                except Exception as e:
                                    print(e)
                                topic_fields = InitClass().topic_fields()
                                topic_fields["channelName"] = channelname
                                topic_fields["channelID"] = channelid
                                topic_fields["channeltype"] = channel_type
                                topic_fields["workerid"] = article_id
                                topic_fields["topicID"] = article_id
                                topic_fields["title"] = article_title
                                topic_fields["topicUrl"] = share_url
                                topic_fields["pubtime"] = pubtime
                                topic_fields['topicCover'] = article_covers
                                topic_fields["topic"] = 1
                                # 将请求文章必需信息存入
                                articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)
                            else:
                                try:
                                    article_covers = article['images']
                                except Exception as e:
                                    print(e)
                                if 'medias' in article.keys() and article['type']=='video':
                                    for video in article['medias']:
                                        videos = [video['resources'][0]['url']]
                                        article_fields["videos"] = videos
                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["channeltype"] = channel_type
                                article_fields["workerid"] = article_id
                                article_fields["title"] = article_title
                                article_fields["contentType"] = article_type
                                article_fields["url"] = share_url
                                article_fields["pubtime"] = pubtime
                                article_fields["articlecovers"] = article_covers
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
                url = f"http://sxapi.sxrbw.com/api/v2/subjects/{articleid}"
                headers = {
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36',
                    'Host': 'sxapi.sxrbw.com',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                }
                data = {
                    'size':'5',
                    'platform':'android',
                    'clientVersionCode':'61',
                    'deviceOs':'6.0.1',
                    'pjCode':'code_sxrb',
                    'device_size':'810.0x1440.0',
                    'clientVersion':'4.4.6',
                    'deviceModel':'Netease-MuMu',
                    'udid':'010000000308435',
                    'channel':'xiaomi',
                }
            else:
                url = f"http://sxapi.sxrbw.com/api/v2/articles/detail/{articleid}"
                headers = {
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36',
                    'Host': 'sxapi.sxrbw.com',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                }
                data = {
                    'platform':'android',
                    'clientVersionCode':'61',
                    'deviceOs':'6.0.1',
                    'pjCode':'6.0.1',
                    'device_size':'810.0x1440.0',
                    'clientVersion':'4.4.6',
                    'deviceModel':'Netease-MuMu',
                    'udid':'010000000308435',
                    'channel':'xiaomi',
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
            channel_type = fields.get('channeltype')
            channelid = fields.get('channelID')
            channelname = fields.get('channelName')
            if topic:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                if "item" in content_s.keys():
                    try:
                        articlesparams = []
                        if 'blocks' in content_s["item"].keys():
                            for articles in content_s["item"]['blocks']:
                                article_fields = InitClass().article_fields()
                                articleparam = InitClass().article_list_fields()
                                for articless in articles['articles']:
                                    article_id = articless['articleId']
                                    article_title = articless["title"]
                                    article_type = articless['type']
                                    share_url = articless['shareUrl']
                                    pubtime = int(InitClass().date_time_stamp(InitClass().format_date(articless["date"]))) * 1000
                                    if articless['type'] == 'card' and 'cardArticleList' in articless.keys():
                                        for card in articless['cardArticleList']:
                                            article_id = card['articleId']
                                            article_title = card["title"]
                                            article_type = card['type']
                                            share_url = card['shareUrl']
                                            pubtime = int(InitClass().date_time_stamp(InitClass().format_date(card["date"]))) * 1000
                                            try:
                                                article_covers = [card['imageUrl']]
                                            except Exception as e:
                                                print(e)
                                            if card['type'] == 'subject':
                                                topic_fields = InitClass().topic_fields()
                                                topic_fields["channelName"] = channelname
                                                topic_fields["channelID"] = channelid
                                                topic_fields["channeltype"] = channel_type
                                                topic_fields["workerid"] = article_id
                                                topic_fields["topicID"] = article_id
                                                topic_fields["title"] = article_title
                                                topic_fields["topicUrl"] = share_url
                                                topic_fields["pubtime"] = pubtime
                                                topic_fields['topicCover'] = article_covers
                                                # 将请求文章必需信息存入
                                                articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                                articleparam["articleid"] = article_id
                                                articlesparams.append(articleparam)
                                            else:
                                                if 'medias' in card.keys():
                                                    for video in card['medias']:
                                                        videos = [video['resources'][0]['url']]
                                                        article_fields["videos"] = videos
                                                article_fields["channelID"] = channelid
                                                article_fields["channelname"] = channelname
                                                article_fields["channeltype"] = channel_type
                                                article_fields["workerid"] = article_id
                                                article_fields["title"] = article_title
                                                article_fields["contentType"] = article_type
                                                article_fields["url"] = share_url
                                                article_fields["pubtime"] = pubtime
                                                article_fields["articlecovers"] = article_covers
                                                # 将请求文章必需信息存入
                                                articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                                articleparam["articleid"] = article_id
                                                articlesparams.append(articleparam)
                                    elif articless['type'] == 'subject':
                                        try:
                                            article_covers = articless['images']
                                        except Exception as e:
                                            print(e)
                                        topic_fields = InitClass().topic_fields()
                                        topic_fields["channelName"] = channelname
                                        topic_fields["channelID"] = channelid
                                        topic_fields["channeltype"] = channel_type
                                        topic_fields["workerid"] = article_id
                                        topic_fields["topicID"] = article_id
                                        topic_fields["title"] = article_title
                                        topic_fields["topicUrl"] = share_url
                                        topic_fields["pubtime"] = pubtime
                                        topic_fields['topicCover'] = article_covers
                                        topic_fields["topic"] = 1
                                        # 将请求文章必需信息存入
                                        articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                        articleparam["articleid"] = article_id
                                        articlesparams.append(articleparam)
                                    else:
                                        try:
                                            article_covers = articless['images']
                                        except Exception as e:
                                            print(e)
                                        if 'medias' in articless.keys() and articless['type'] == 'video':
                                            for video in article['medias']:
                                                videos = [video['resources'][0]['url']]
                                                article_fields["videos"] = videos
                                        article_fields["channelID"] = channelid
                                        article_fields["channelname"] = channelname
                                        article_fields["channeltype"] = channel_type
                                        article_fields["workerid"] = article_id
                                        article_fields["title"] = article_title
                                        article_fields["contentType"] = article_type
                                        article_fields["url"] = share_url
                                        article_fields["pubtime"] = pubtime
                                        article_fields["articlecovers"] = article_covers
                                        # 将请求文章必需信息存入
                                        articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                        articleparam["articleid"] = article_id
                                        articlesparams.append(articleparam)
                    except Exception as e:
                        print(e)
                    aaaa = self.getarticleparams(articlesparams)
                    bbbb = self.getarticlehtml(aaaa.__next__())
                    self.analyzearticle(bbbb.__next__())
            try:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                if 'item' in content_s.keys() and 'content' in content_s["item"].keys():
                    worker_id = content_s["item"]["id"]
                    article_title = content_s["item"]["title"]
                    if 'source' in content_s["item"].keys():
                        source = content_s["item"]["source"]
                    else:
                        source = ''
                    content = content_s["item"]["content"]
                    comment_num = content_s["item"]['comments']
                    hit_num = content_s["item"]["hits"]  # 点击数
                    like_num = content_s["item"]["likes"]
                    images = InitClass.get_images(content)
                    videos = InitClass.get_video(content)
                    fields["appname"] = self.newsname
                    fields["title"] = article_title
                    fields["workerid"] = worker_id
                    fields["content"] = content
                    fields["source"] = source
                    fields["commentnum"] = comment_num
                    fields["videos"] = videos
                    fields["videocover"] = images
                    fields["images"] = images
                    fields["readnum"] = hit_num
                    fields["likenum"] = like_num
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
    appspider = Shanxiribao("山西日报")
    appspider.run()
