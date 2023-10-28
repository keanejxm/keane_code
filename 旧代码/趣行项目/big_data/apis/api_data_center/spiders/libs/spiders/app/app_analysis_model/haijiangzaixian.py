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


class Haijiangzaixian(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://api.haijiangzx.com/mobile/index.php?app=mobile&controller=content&action=category"
        headers = {
            'Content-Length': '25',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'api.haijiangzx.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0(Linux;U;Android 2.2.1;en-us;Nexus One Build.FRG83) AppleWebKit/553.1(KHTML,like Gecko) Version/4.0 Mobile Safari/533.1',
            'Expect': '100-continue',
        }
        method = "post"
        data = f'version=5.0.0&type=mobile'
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelname = '头条'
        channelid = '0'
        channelparam = InitClass().channel_fields(channelid, channelname)
        yield channelparam
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))
        for channel in channelslists['data']:
            channelname = channel['catname']
            channelid = channel['catid']
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam

    def getarticlelistparams(self, channelsres):
        headers = {
            'Host': 'api.haijiangzx.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0(Linux;U;Android 2.2.1;en-us;Nexus One Build.FRG83) AppleWebKit/553.1(KHTML,like Gecko) Version/4.0 Mobile Safari/533.1',
        }
        method = 'get'
        channel_num = 0
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
            channelid = channel.get('channelid')
            channelname = channel.get('channelname')
            url = 'http://api.haijiangzx.com/mobile/index.php'
            data = {
                'app': 'mobile',
                'controller': 'content',
                'action': 'index',
                'catid': channelid,
                'page': '1',
                'time': '',
                'keyword': '',
                'version': '5.0.0',
                'type': 'mobile',
            }
            banner_data = {
                'app': 'mobile',
                'controller': 'content',
                'action': 'index',
                'catid': channelid,
                'page': '1',
                'time': '',
                'keyword': '',
                'version': '5.0.0',
                'type': 'mobile',
            }
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)

            articlelist_param_banner = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                              data=banner_data,
                                                                              channelid=channelid, banners=1,
                                                                              channel_index_id=channel_index_id)
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                       channelid=channelid,
                                                                       channel_index_id=channel_index_id)
            yield channel_field,[articlelist_param_banner,articlelist_param]

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
                    for article in articleslists['data']:
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        article_id = article["contentid"]
                        article_title = article["title"]
                        pubtime = int(article['sorttime']) * 1000
                        article_covers = [article['thumb']]
                        article_fields["channelID"] = channelid
                        article_fields["channelname"] = channelname
                        article_fields["channelindexid"] = channel_index_id
                        article_fields["workerid"] = article_id
                        article_fields["title"] = article_title
                        article_fields['articlecovers'] = article_covers
                        article_fields["pubtime"] = pubtime
                        article_fields["banner"] = articleslistres.get('banner')
                        yield article_fields
                        # 将请求文章必需信息存入
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")

    def getarticleparams(self,articleslistsres):
        for article in self.analyze_articlelists(articleslistsres):
            articleid = article.get("workerid")
            url = 'http://api.haijiangzx.com/mobile/index.php'
            headers = {
                'Host': 'api.haijiangzx.com',
                'Connection': 'Keep-Alive',
                'User-Agent': 'Mozilla/5.0(Linux;U;Android 2.2.1;en-us;Nexus One Build.FRG83) AppleWebKit/553.1(KHTML,like Gecko) Version/4.0 Mobile Safari/533.1',
            }
            data = {
                'app': 'mobile',
                'controller': 'article',
                'action': 'content',
                'contentid': articleid,
                'version': '5.0.0',
                'type': 'mobile',
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
                if 'data' in content_s.keys():
                    workerid = content_s['data']['contentid']
                    title = content_s['data']['title']
                    source = content_s['data']['source']
                    url = content_s['data']['shareurl']
                    pubtime = int(content_s['data']['published']) * 1000
                    comments = content_s['data']['comments']
                    if 'content' in content_s['data'].keys():
                        content = content_s['data']['content']
                        videos = InitClass().get_video(content)
                        images = InitClass().get_video(content)
                    else:
                        content = ''
                        videos = [content_s['data']['video']]
                        images = [content_s['data']['thumb']]
                    fields["appname"] = self.newsname
                    fields["platformID"] = self.platform_id
                    fields["title"] = title
                    fields["workerid"] = fields.get("workerid")
                    fields["content"] = content
                    fields["source"] = source
                    fields["pubtime"] = pubtime
                    fields["images"] = images
                    fields["videos"] = videos
                    fields["workerid"] = workerid
                    fields["url"] = url
                    fields["commentnum"] = comments
                    fields = InitClass().wash_article_data(fields)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                num += 1
                logging.info(f"错误数量{num},{e}")

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Haijiangzaixian(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
