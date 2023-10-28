# -*- encoding:utf-8 -*-
"""
@功能:新湖南解析模板
@AUTHOR：Keane
@文件名：xinhunan.py
@时间：2020/12/17  17:33
"""

import json
import logging

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class Liebaoliulanqi(Appspider):

    @staticmethod
    def analyze_channel():
        channelsparams = {'channelid': 'liebao', 'channelname': '猎豹浏览器'}
        yield channelsparams

    def getarticlelistparams(self):
        url = "https://cr.m.liebao.cn/news/fresh"
        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': 'cr.m.liebao.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        method = 'get'
        channel_num = 0
        for channel in self.analyze_channel():
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")  # 此处没有若有可加上，其他一样
            data = {
                'act': '3',
                'scenario': '0x004a0101',
                'osv': '6.0.1',
                'app_lan': 'zh_CN',
                'ch': '20000009',
                'action': '0x219faf',
                'offset': '',
                'uuid': 'or57vbncwdwcibtmr2hfqpnm7vzz',
                'count': '20',
                'pf': 'android',
                'v': '4',
                'imei': '010000000308435',
                'itime': '1609741208',
                'mcc': '',
                'nmcc': '',
                'imsi': '888888888888888',
                'lan': 'zh_CN',
                'appv': '5.23.1',
                'pid': '3',
                'net': 'wifi',
                'mnc': '',
                'ctype': '0xe1a7b',
                'display': '0x11eedf',
                'mode': '1',
                'brand': 'Android',
                'nmnc': '',
                'aid': '635c485bc510fde',
                'model': 'MuMu',
            }
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid=channelid, data=data,
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
                    print(articleslists)
                    for article in articleslists["data"]:
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        print(article)
                        # 获取文章列表内的有用信息
                        article_id = article['contentid']
                        article_title = article["title"]
                        share_url = article["url"]
                        pubtime = int(article['pulltime']) * 1000
                        article_covers = article['images']
                        article_fields["channelID"] = channelid
                        article_fields["channelname"] = channelname
                        article_fields["channelindexid"] = channel_index_id
                        article_fields["channeltype"] = channel_type
                        article_fields["workerid"] = article_id
                        article_fields["title"] = article_title
                        article_fields["url"] = share_url
                        article_fields["pubtime"] = pubtime
                        article_fields["articlecovers"] = article_covers
                        yield article_fields
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")

    def getarticleparams(self, articleslistsres):
        for article in self.analyze_articlelists(articleslistsres):
            articleid = article.get("workerid")
            url = "https://cr.m.liebao.cn/news/detail"
            headers = {
                'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
                'Host': 'cr.m.liebao.cn',
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip',
            }
            data = {
                'scenario': '0x004a0101',
                'lan': 'zh_CN',
                'osv': '6.0.1',
                'appv': '5.23.1',
                'app_lan': 'zh_CN',
                'ch': '20000009',
                'pid': '3',
                'action': '0x219faf',
                'uuid': 'or57vbncwdwcibtmr2hfqpnm7vzz',
                'pf': 'android',
                'net': 'wifi',
                'v': '4',
                'mnc': '',
                'ctype': '0xe1a7b',
                'display': '0x11eedf',
                'contentid': articleid,
                'imei': '010000000308435',
                'brand': 'Android',
                'itime': '1609741208',
                'mcc': '',
                'nmnc': '',
                'nmcc': '',
                'aid': '635c485bc510fde',
                'imsi': '888888888888888',
                'model': 'MuMu',
            }
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                             article_field=article)
            yield [articleparam]

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            try:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                if len(content_s["data"]) > 0:
                    worker_id = content_s["data"][0]['contentid']
                    article_title = content_s["data"][0]["title"]
                    author = content_s["data"][0]['author']
                    source = content_s["data"][0]["source"]
                    content = content_s["data"][0]["body"]
                    comment_num = content_s["data"][0]['commentcount']
                    pubtime = int(content_s["data"][0]['pubtime'])
                    hit_num = content_s["data"][0]['clickcount']  # 点击数
                    likenum = content_s["data"][0]['likecount']
                    sharenum = content_s['data'][0]['sharecount']
                    videos = InitClass.get_video(content)
                    images = InitClass.get_images(content)
                    fields["videos"] = videos
                    fields["pubtime"] = pubtime
                    fields["images"] = images
                    fields["appname"] = self.newsname
                    fields["platformID"] = self.platform_id
                    fields["title"] = article_title
                    fields["workerid"] = worker_id
                    fields["content"] = content
                    fields["source"] = source
                    fields["commentnum"] = comment_num
                    fields["author"] = author
                    fields["readnum"] = hit_num
                    fields["likenum"] = likenum
                    fields["sharenum"] = sharenum
                    fields = InitClass().wash_article_data(fields)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                num += 1
                logging.info(f"错误数量{num},{e}")


def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Liebaoliulanqi(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for channel_field, channel_param in appspider.getarticlelistparams():
        for article_list_res in appspider.getarticlelists(channel_param):
            for article_param in appspider.getarticleparams(article_list_res):
                for article_res in appspider.getarticlehtml(article_param):
                    for data in appspider.analyzearticle(article_res):
                        yield data
        yield {"code": 1, "msg": "OK", "data": {"channel": channel_field}}
