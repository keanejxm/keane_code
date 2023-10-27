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
import bs4
import requests
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class Xizangribao(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://xzrbappapi.peopletech.cn/api/v2/menus/category/list"
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36',
            'Host': 'xzrbappapi.peopletech.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        data = {
            'platform': 'android',
            'clientVersionCode': '13',
            'deviceOs': '6.0.1',
            'pjCode': 'xzrbc_10_201705',
            'device_size': '810.0x1440.0',
            'clientVersion': '2.0.3',
            'deviceModel': 'Netease-MuMu',
            'udid': '010000000308435',
            'channel': 'qq',
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))
        for channellists in channelslists["item"]['categories']:
            if 'children' in channellists.keys():
                for channel in channellists["children"]:
                    channelname = channel["name"]
                    channelid = channel["id"]
                    channelparam = InitClass().channel_fields(channelid, channelname)
                    yield channelparam
            else:
                channelname = channellists["name"]
                channelid = channellists["id"]
                channelparam = InitClass().channel_fields(channelid, channelname)
                yield channelparam

    def getarticlelistparams(self, channelsres):
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36',
            'Host': 'xzrbappapi.peopletech.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        method = 'get'
        channel_num = 0
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            url = f"http://xzrbappapi.peopletech.cn/api/v2/articles/{channelid}"
            data = {
                'pageToken': '',
                'size': '20',
                'headPageSize': '',
                'platform': 'android',
                'clientVersionCode': '13',
                'deviceOs': '6.0.1',
                'pjCode': 'xzrbc_10_201705',
                'device_size': '810.0x1440.0',
                'clientVersion': '2.0.3',
                'deviceModel': 'Netease-MuMu',
                'udid': '010000000308435',
                'channel': 'qq',
            }
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid=channelid, data=data,
                                                                       channeltype=channeltype,
                                                                       channel_index_id=channel_index_id)
            yield channel_field,[articlelist_param]

    @staticmethod
    def analyze_articlelists(articleslistsres):
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channel_index_id = articleslistres.get("channelindexid")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    if 'head' in articleslists['item']:
                        # banner
                        for article in articleslists['item']['head']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article["articleId"]
                            article_title = article["title"]
                            article_type = article["type"]
                            share_url = article["shareUrl"]
                            pubtime = int(InitClass().date_time_stamp(InitClass().format_date(article["date"]))) * 1000
                            article_covers = article["images"]
                            if article["type"] == 'subject':
                                # 专题
                                topic_fields = InitClass().topic_fields()
                                articleparam = InitClass().article_list_fields()
                                topic_fields["channelName"] = channelname
                                topic_fields["channelindexid"] = channel_index_id
                                topic_fields["channelID"] = channelid
                                topic_fields["workerid"] = article_id
                                topic_fields["topicID"] = article_id
                                topic_fields["title"] = article_title
                                topic_fields["topicUrl"] = share_url
                                topic_fields["pubtime"] = pubtime
                                topic_fields["topicCover"] = article_covers
                                topic_fields["topic"] = 1
                                yield topic_fields
                            else:
                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["channelindexid"] = channel_index_id
                                article_fields["workerid"] = article_id
                                article_fields["title"] = article_title
                                # article_fields["contentType"] = article_type
                                article_fields["articlecovers"] = article_covers
                                article_fields["url"] = share_url
                                article_fields["pubtime"] = pubtime
                                article_fields["banner"] = 1
                                yield article_fields
                                # 将请求文章必需信息存入
                    if 'list' in articleslists['item'].keys():
                        for article in articleslists['item']['list']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article["articleId"]
                            article_title = article["title"]
                            article_type = article["type"]
                            share_url = article["shareUrl"]
                            pubtime = int(InitClass().date_time_stamp(InitClass().format_date(article["date"]))) * 1000
                            article_covers = article["images"]
                            if article["type"] == 'subject':
                                # 专题
                                topic_fields = InitClass().topic_fields()
                                articleparam = InitClass().article_list_fields()
                                topic_fields["channelName"] = channelname
                                topic_fields["channelindexid"] = channel_index_id
                                topic_fields["channelID"] = channelid
                                topic_fields["workerid"] = article_id
                                topic_fields["topicID"] = article_id
                                topic_fields["title"] = article_title
                                topic_fields["topicUrl"] = share_url
                                topic_fields["pubtime"] = pubtime
                                topic_fields["topicCover"] = article_covers
                                topic_fields["topic"] = 1
                                yield topic_fields
                            else:
                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["channelindexid"] = channel_index_id
                                article_fields["workerid"] = article_id
                                article_fields["title"] = article_title
                                # article_fields["contentType"] = article_type
                                article_fields["articlecovers"] = article_covers
                                article_fields["url"] = share_url
                                article_fields["pubtime"] = pubtime
                                yield article_fields
                                # 将请求文章必需信息存入
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")

    def getarticleparams(self,articleslistsres):
        for article in self.analyze_articlelists(articleslistsres):
            articleid = article.get("workerid")
            topic = article.get("topic")
            if topic == 1:
                articleid = article.get("topicID")
                url = f"http://xzrbappapi.peopletech.cn/api/v2/subjects/{articleid}"
                headers = {
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36',
                    'Host': 'xzrbappapi.peopletech.cn',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                }
                data = {
                    'size': '5',
                    'platform': 'android',
                    'clientVersionCode': '13',
                    'deviceOs': '6.0.1',
                    'pjCode': 'xzrbc_10_201705',
                    'device_size': '810.0x1440.0',
                    'clientVersion': '2.0.3',
                    'deviceModel': 'Netease-MuMu',
                    'udid': '010000000308435',
                    'channel': 'qq',
                }
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, data=data, channelname='专题',
                                                                 article_field=article)
                yield [articleparam]
            else:
                url = f"http://xzrbh5c.peopletech.cn/api/v2/articles/detail/{articleid}"
                headers = {
                    'Host': 'xzrbh5c.peopletech.cn',
                    'Connection': 'keep-alive',
                    'Access-Control-Allow-Origin': '*',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36;cdrbdaily_Android;cdrbdaily_android',
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,en-US;q=0.8',
                    'X-Requested-With': 'com.xizangdaily.activity',
                }
                data = {
                    '_t': int(time.time())
                }
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                                 channelname=article.get('channelname'),
                                                                 article_field=article)
                yield [articleparam]

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            topic = fields.get("topic")
            if topic:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                if "item" in content_s:
                    articlesparams = []
                    for articles in content_s["item"]['blocks']:
                        for article in articles['articles']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article["articleId"]
                            article_title = article["title"]
                            article_type = article["type"]
                            share_url = article["shareUrl"]
                            pubtime = int(InitClass().date_time_stamp(InitClass().format_date(article["date"]))) * 1000
                            article_covers = article["images"]
                            article_fields["channelID"] = fields.get("channelID")
                            article_fields["channelname"] = fields.get("channelname")
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            # article_fields["contentType"] = article_type
                            article_fields["articlecovers"] = article_covers
                            article_fields["url"] = share_url
                            article_fields["pubtime"] = pubtime
                            # 将请求文章必需信息存入
                            articleparam["articleField"] = article_fields  # 携带文章采集的数据
                            articleparam["articleid"] = article_id
                            articlesparams.append(articleparam)
                    aaaa = self.getarticleparams(articlesparams)
                    bbbb = self.getarticlehtml(aaaa.__next__())
                    self.analyzearticle(bbbb.__next__())
            else:
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                    print(content_s)
                    if "item" in content_s.keys():
                        worker_id = content_s["item"]["id"]
                        article_title = content_s["item"]["title"]
                        if "content" in content_s["item"].keys() and content_s["item"] != 'video':
                            content = content_s["item"]["content"]
                            videos = InitClass().get_video(content)
                            images = InitClass().get_images(content)
                            source = content_s["item"]["source"]
                            fields["source"] = source
                            fields["images"] = images
                            fields["videos"] = videos
                        elif content_s["item"] != 'video' and 'medias' in content_s["item"].keys():
                            content = ''
                            videos = list()
                            for v in content_s["item"]['medias'][0]['resources']:
                                videos.append(v['url'])
                            fields["videos"] = videos
                            fields["images"] = content_s["item"]['images']
                            fields["videocover"] = [content_s["item"]['medias'][0]['image']]
                            source = content_s["item"]["source"]
                            fields["source"] = source
                        else:
                            content = content_s["item"]['link']
                        comment_num = content_s["item"]["comments"]
                        hit_num = content_s["item"]["hits"]  # 点击数
                        url = content_s["item"]["shareUrl"]
                        likenum = content_s["item"]["likes"]
                        fields["appname"] = self.newsname
                        fields["platformID"] = self.platform_id
                        fields["title"] = article_title
                        fields["workerid"] = worker_id
                        fields["content"] = content
                        fields["commentnum"] = comment_num
                        fields["readnum"] = hit_num
                        fields["url"] = url
                        fields["likenum"] = likenum
                        fields = InitClass().wash_article_data(fields)
                        yield {"code": 1, "msg": "OK", "data": {"works": fields}}
                except Exception as e:
                    num += 1
                    logging.info(f"错误数量{num},{e}")

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Xizangribao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
