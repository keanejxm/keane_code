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


class Jinrishida(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://feed.shida.sogou.com/discover_agent/getchlist"
        headers = {
            'Host': 'feed.shida.sogou.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.6.0',
        }
        data = {
            'r1': '2116',
            'cmd': 'getchlist',
            'simplejson': '1',
            'phone': '1',
            'clab': '-1',
            'h': '00000000-4571-b75a-831c-9c0a00000000',
            'imei': '010000000308435',
            'sys': 'android',
            'r': '2116',
            'pf': 'android',
            'pkg': 'com.sogou.toptennews',
            'v': '2.8.4.8009',
            'duid': 'DuHgCgsHD80WFPCnCrsry15WCZm/4GQhGN2VC6G7dP470/rtkCUganwATgmSpSds2F6vPnLaRgnN/83RtT6TC7XQ',
            'hid': '00000000-4571-b75a-831c-9c0a00000000',
            'omid': 'fadf010000000308435',
            'mid': '00000000-4571-b75a-831c-9c0a00000000',
            'xid': '00f978632bdcffa3bb4a4494a2feeb26fac6',
            'user_id': '',
            'api': '11',
            'appid': '1000',
            'smeiid': '2021010414195921f7469be78e2e4f9a913ca1dd60927601a8789905790d15',
            'oaid': '',
            'vaid': '',
            'aaid': '',
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))
        for channel in channelslists['category_infos']:
            channelname = channel["name"]
            channelid = channel["id"]
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam

    def getarticlelistparams(self, channelsres):
        url = "https://feed.shida.sogou.com/discover_agent/getlist"
        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) TopTenNews Android/2.8.4',
            'Host': 'feed.shida.sogou.com',
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
            data = {
                'aaid': '',
                'ac': 'refresh',
                'ad': '5',
                'ad_like': 'false',
                'aid': '635c485bc510fde',
                'api': '11',
                'appid': '1000',
                'b': channelname,
                'cid': 'dc4750593ffb11e819c9554558adc4f6',
                'clab': '-1',
                'cmd': 'getnewslist',
                'count': '15',
                'duid': 'DuHgCgsHD80WFPCnCrsry15WCZm/4GQhGN2VC6G7dP470/rtkCUganwATgmSpSds2F6vPnLaRgnN/83RtT6TC7XQ',
                'f': '',
                'h': '00000000-4571-b75a-831c-9c0a00000000',
                'hid': '00000000-4571-b75a-831c-9c0a00000000',
                'imei': '010000000308435',
                'lastindex': '0',
                'lat': '3990718',
                'loctime': '1609833179',
                'loctype': '4',
                'lon': '11639107',
                'maxindex': '0',
                'mid': '00000000-4571-b75a-831c-9c0a00000000',
                'mn': 'Netease',
                'mode': 'up',
                'nt': 'wifi',
                'oaid': '',
                'omid': 'fadf010000000308435',
                'pf': 'android',
                'phone': '1',
                'pkg': 'com.sogou.toptennews',
                'playg': '-1',
                'pn': 'MuMu',
                'r': '2116',
                'r1': '2116',
                'simplejson': '1',
                'smeiid': '2021010414195921f7469be78e2e4f9a913ca1dd60927601a8789905790d15',
                'sn': 'ZX1G42CPJD',
                'sys': 'android',
                't': '1609820695',
                'toptenuuid': 'topten83b34499-b199-4b2f-88ed-f5d26a838fb073267',
                'user_id': '',
                'user_like': 'true',
                'v': '2.8.4.8009',
                'vaid': '',
                'xid': '00f978632bdcffa3bb4a4494a2feeb26fac6',
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
            channel_type = articleslistres.get("channeltype")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    print(articleslists)
                    if 'url_infos' in articleslists.keys():
                        for article in articleslists['url_infos']:
                            if not 'ad_source' in article.keys() and 'doc_id' in article.keys():
                                article_fields = InitClass().article_fields()
                                articleparam = InitClass().article_list_fields()
                                article_id = article['doc_id']
                                article_title = article["title"]
                                article_type = article["type"]
                                share_url = article['share_url']
                                pubtime = int(article['publish_time']) * 1000
                                article_covers = [article['images'][0]['name']]
                                try:
                                    if 'source_url' in article.keys():
                                        # videos = list()
                                        # videos.append(article['source_url'])
                                        article_fields["videos"] = [article['source_url']]
                                    else:
                                        article_fields["videos"] = []
                                except Exception as e:
                                    print(e)
                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["channelindexid"] = channel_index_id
                                article_fields["channeltype"] = channel_type
                                article_fields["workerid"] = article_id
                                article_fields["title"] = article_title
                                # article_fields["contentType"] = article_type
                                article_fields["url"] = share_url
                                article_fields["pubtime"] = pubtime
                                article_fields["articlecovers"] = article_covers
                                yield article_fields
                                # 将请求文章必需信息存入
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")

    def getarticleparams(self,articleslistsres):
        for article in self.analyze_articlelists(articleslistsres):
            articleid = article.get("workerid")
            url = "http://feed.shida.sogou.com/discover_agent/getcontent"
            headers = {
                'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) TopTenNews Android/2.8.4',
                'Host': 'feed.shida.sogou.com',
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip',
            }
            data = {
                'fontsize': '25',
                'simplejson': '1',
                'url': 'http%3A//shida.sogou.com/na%3Fshida%5Ffeed%3D1%26shida%5Ffeed%5Furl%3Dhttp%253A//politics.people.com.cn/n1/2021/0105/c1001%252D31988772.html%26shida%5Ffeed%5Fdid%3D793eaebbd0c05e229cead0aae400af71%26shida%5Ffeed%5Ftitle%3D%25E7%2594%259F%25E6%2580%2581%25E4%25BC%2598%25E5%2585%2588%2520%25E6%258A%25A4%25E4%25B8%2580%25E6%25B1%259F%25E7%25A2%25A7%25E6%25B0%25B4',
                'phone': '1',
                'words': '1',
                'imei': '010000000308435',
                'ad_like': 'false',
                'docid': articleid,
                'r1': '2116',
                'cmd': 'getcontent',
                'listid': '8148944474316614010',
                'newstag': '10',
                'clab': '-1',
                'from': 'default',
                'h': '00000000-4571-b75a-831c-9c0a00000000',
                'ad': '5',
                'dtrans': '||33|人民网||1|||-1|-1|-1|-1||1609834966|-1|-1|-1||||0|-1|793eaebbd0c05e229cead0aae400af71|||||-1||-1|-1||793eaebbd0c05e229cead0aae400af71|||-1,-1,-1,-1,-1',
                'sys': 'android',
                'pn': 'MuMu',
                'r': '2116',
                'user_like': 'true',
                'aid': '635c485bc510fde',
                'pf': 'android',
                'pkg': 'com.sogou.toptennews',
                'v': '2.8.4.8009',
                'duid': 'DuHgCgsHD80WFPCnCrsry15WCZm/4GQhGN2VC6G7dP470/rtkCUganwATgmSpSds2F6vPnLaRgnN/83RtT6TC7XQ',
                'hid': '00000000-4571-b75a-831c-9c0a00000000',
                'omid': 'fadf010000000308435',
                'mid': '00000000-4571-b75a-831c-9c0a00000000',
                'xid': '00f978632bdcffa3bb4a4494a2feeb26fac6',
                'user_id': '',
                'api': '11',
                'appid': '1000',
                'smeiid': '2021010414195921f7469be78e2e4f9a913ca1dd60927601a8789905790d15',
                'oaid': '',
                'vaid': '',
                'aaid': '',
            }
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, data=data, sleeptime=5,
                                                             article_field=article)
            yield [articleparam]

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            try:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                if 'doc_id' in content_s.keys():
                    worker_id = content_s["doc_id"]
                    article_title = content_s['url_info'][0]["title"]
                    content = content_s['url_info'][0]["content"]
                    source = content_s['url_info'][0]["source"]
                    videos = InitClass().get_video(content)
                    images = InitClass().get_images(content)
                    fields["appname"] = self.newsname
                    fields["platformID"] = self.platform_id
                    fields["title"] = article_title
                    fields["workerid"] = worker_id
                    fields["content"] = content
                    fields["source"] = source
                    fields["videos"] = videos
                    fields["images"] = images
                    fields = InitClass().wash_article_data(fields)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                num += 1
                logging.info(f"错误数量{num},{e}")

def fetch_yield(appname, logger, platform_id, self_typeid):
    pass
    # appspider = Jinrishida(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    # for article_data in appspider.fethch_yieldaaaa(appspider):
    #     yield article_data
