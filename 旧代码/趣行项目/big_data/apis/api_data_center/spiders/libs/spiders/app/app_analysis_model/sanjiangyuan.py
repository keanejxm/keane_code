# -*- encoding:utf-8 -*-
"""
@功能:黄河融媒解析模板
@AUTHOR：Keane
@文件名：huangherongmei.py
@时间：2020/12/23  19:58
"""
import json
import logging
import re
import requests
from bs4 import BeautifulSoup
from lxml import etree
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class Sanjiangyuan(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://mobile.qhbtv.com/app/home_news_recomend_column.php"
        headers = {
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_263 1.0.0',
            'X-API-TIMESTAMP': '1610429210953AW3Yz4',
            'X-API-SIGNATURE': 'MmJkNjgyYjRlYWM2NzFiNmVjOGU2OWRjNzE5ZmQxNGY2NTIzN2U1Yw==',
            'X-API-VERSION': '1.0.5',
            'X-AUTH-TYPE': 'sha1',
            'X-API-KEY': '8c19f571e251e61cb8dd3612f26d5ecf',
            'Host': 'mobile.qhbtv.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        data = {
            'system_version': '6.0.1',
            'app_version': '1.0.5',
            'client_type': 'android',
            'client_id_android': '5f28d8fb4e69968a32cdbdc8690cc447',
            'locating_city': '西宁',
            'appkey': '9kHNaMrFu2zqXwcOjrUI59vqcumyz6My',
            'version': '1.0.5',
            'appid': '6',
            'language': 'Chinese',
            'location_city': '西宁',
            'device_token': '0cf6d90963892a97dad193521805baec',
            'phone_models': 'MuMu',
            'package_name': 'com.hoge.android.qinghaisjy',
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))
        for channellists in channelslists:
            if channellists["id"] != '2708':
                channel_name = channellists["name"]
                channel_id = channellists["id"]
                channel_url = channellists['column_url']
                if channellists["id"] == '2706':
                    res = requests.get(
                        'http://mobile.qhbtv.com/app/news_recomend_column.php?system_version=6.0.1&app_version=1.0.5&c'
                        'lient_type=android&client_id_android=5f28d8fb4e69968a32cdbdc8690cc447&locating_city=%E8%A5%BF'
                        '%E5%AE%81&appkey=9kHNaMrFu2zqXwcOjrUI59vqcumyz6My&version=1.0.5&appid=6&language=Chinese&loca'
                        'tion_city=%E8%A5%BF%E5%AE%81&device_token=0cf6d90963892a97dad193521805baec&phone_models=MuMu&'
                        'package_name=com.hoge.android.qinghaisjy&fid=2706&name=%E6%96%B0%E9%97%BB').text
                    channel_child = json.loads(json.dumps(json.loads(res), indent=4, ensure_ascii=False))
                    for channel in channel_child:
                        child_id = channel["id"]
                        child_name = channel["name"]
                        child_url = channel["column_url"]
                        channelparam = InitClass().channel_fields(child_id, child_name, channel_url=child_url)
                        yield channelparam
                elif channellists["id"] == '2711':
                    res = requests.get(
                        'http://mobile.qhbtv.com/app/news_recomend_column.php?system_version=6.0.1&app_version=1.0.5&client_type=android&client_id_android=5f28d8fb4e69968a32cdbdc8690cc447&locating_city=%E8%A5%BF%E5%AE%81&appkey=9kHNaMrFu2zqXwcOjrUI59vqcumyz6My&version=1.0.5&appid=6&language=Chinese&location_city=%E8%A5%BF%E5%AE%81&device_token=0cf6d90963892a97dad193521805baec&phone_models=MuMu&package_name=com.hoge.android.qinghaisjy&fid=2711&name=%E5%B8%82%E5%B7%9E').text

                    channel_child = json.loads(json.dumps(json.loads(res), indent=4, ensure_ascii=False))
                    for channel in channel_child:
                        child_id = channel["id"]
                        child_name = channel["name"]
                        child_url = channel["column_url"]
                        channelparam = InitClass().channel_fields(child_id, child_name, channel_url=child_url)
                        yield channelparam
                elif channellists["id"] == '3205':
                    res = requests.get(
                        'http://mobile.qhbtv.com/app/news_recomend_column.php?system_version=6.0.1&app_version=1.0.5&client_type=android&client_id_android=5f28d8fb4e69968a32cdbdc8690cc447&locating_city=%E8%A5%BF%E5%AE%81&appkey=9kHNaMrFu2zqXwcOjrUI59vqcumyz6My&version=1.0.5&appid=6&language=Chinese&location_city=%E8%A5%BF%E5%AE%81&device_token=0cf6d90963892a97dad193521805baec&phone_models=MuMu&package_name=com.hoge.android.qinghaisjy&fid=3205&name=%E5%8C%BA%E5%8E%BF').text

                    channel_child = json.loads(json.dumps(json.loads(res), indent=4, ensure_ascii=False))
                    for channel in channel_child:
                        child_id = channel["id"]
                        child_name = channel["name"]
                        child_url = channel["column_url"]
                        channelparam = InitClass().channel_fields(child_id, child_name, channel_url=child_url)
                        yield channelparam
                else:
                    channelparam = InitClass().channel_fields(channel_id, channel_name, channel_url=channel_url)
                    yield channelparam

    def getarticlelistparams(self, channelsres):

        headers = {
            "Host": "hwcb.jnetdata.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.10.0",
            "If-Modified-Since": "Wed, 23 Dec 2020 12:46:39 GMT"
        }
        channel_num = 0
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            url = 'http://mobile.qhbtv.com/app/news.php'
            data = {
                'system_version': '6.0.1',
                'app_version': '1.0.5',
                'client_type': 'android',
                'client_id_android': '5f28d8fb4e69968a32cdbdc8690cc447',
                'locating_city': '5f28d8fb4e69968a32cdbdc8690cc447',
                'appkey': '9kHNaMrFu2zqXwcOjrUI59vqcumyz6My',
                'version': '1.0.5',
                'appid': '6',
                'language': 'Chinese',
                'location_city': '西宁',
                'device_token': '0cf6d90963892a97dad193521805baec',
                'phone_models': 'MuMu',
                'package_name': 'com.hoge.android.qinghaisjy',
                'count': '20',
                'offset': '0',
                'third_offset': '0',
                'column_name': channelname,
                'column_id': channelid,
            }
            method = "get"
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
                    if 'slide' in articleslists:
                        # banner
                        for articles in articleslists["slide"]:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = articles["id"]
                            article_title = articles["title"]
                            share_url = articles['content_url']
                            pubtime = int(articles['verify_time']) * 1000
                            if type(articles['indexpic']).__name__ == 'list' and len(articles['indexpic']) > 0:
                                article_cover = list()
                                for img in articles['indexpic']:
                                    article_cover.append(img)
                                article_fields["articlecovers"] = article_cover
                            elif type(articles['indexpic']).__name__ == 'dict':
                                article_cover = [
                                    articles['indexpic']['host'] + articles['indexpic']['dir'] + articles['indexpic'][
                                        'filepath'] + articles['indexpic']['filename']]
                                article_fields["articlecovers"] = article_cover
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channelindexid"] = channel_index_id
                            article_fields["channeltype"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["url"] = share_url
                            article_fields["pubtime"] = pubtime
                            article_fields["banner"] = 1
                            yield article_fields
                            # 将请求文章必需信息存入
                    if 'list' in articleslists:
                        for articles in articleslists["list"]:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = articles["id"]
                            article_title = articles["title"]
                            share_url = articles['content_url']
                            pubtime = int(articles['verify_time']) * 1000
                            if type(articles['indexpic']).__name__ == 'list' and len(articles['indexpic']) > 0:
                                article_cover = list()
                                for img in articles['indexpic']:
                                    article_cover.append(img)
                                article_fields["articlecovers"] = article_cover
                            # article_cover = [articles['indexpic']['host']+articles['indexpic']['dir']+articles['indexpic']['filepath']+articles['indexpic']['filename']]
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channelindexid"] = channel_index_id
                            article_fields["channeltype"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
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
            article_id = article.get("workerid")
            url = 'http://mobile.qhbtv.com/app/item.php'
            headers = {
                "Host": "hwcb.jnetdata.com",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,en-US;q=0.8",
                "Cookie": "__FT10000028=2020-12-24-9-4-30; __NRU10000028=1608771870982; __RT10000028=2020-12-24-9-4-30",
                "X-Requested-With": "com.future.huangwei",
            }
            method = 'get'
            data = {
                'system_version': '6.0.1',
                'app_version': '1.0.5',
                'client_type': 'android',
                'client_id_android': '5f28d8fb4e69968a32cdbdc8690cc447',
                'locating_city': '西宁',
                'appkey': '9kHNaMrFu2zqXwcOjrUI59vqcumyz6My',
                'version': '1.0.5',
                'appid': '6',
                'language': 'Chinese',
                'location_city': '西宁',
                'device_token': '0cf6d90963892a97dad193521805baec',
                'phone_models': 'MuMu',
                'package_name': 'com.hoge.android.qinghaisjy',
                'id': article_id,
            }
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
                workerid = content_s['id']
                title = content_s['title']
                source = content_s['source']
                url = fields.get('url')
                pubtime = int(content_s['publish_time']) * 1000
                author = content_s['author']
                if 'content' in content_s.keys():
                    content = content_s['content']
                    videos = InitClass().get_video(content)
                    images = InitClass().get_images(content)
                else:
                    content = ''
                    images = InitClass().get_images(content)
                    videos = [content_s['video']['host'] + content_s['video']['dir'] + content_s['video']['filepath'] +
                              content_s['video']['filename']]
                comm_num = content_s['comment_num']
                readnum = content_s['click_num']
                share_num = content_s['share_num']
                fields["appname"] = self.newsname
                fields["platformID"] = self.platform_id
                fields["title"] = title
                fields["author"] = author
                fields["workerid"] = workerid
                fields["content"] = content
                fields["source"] = source
                fields["pubtime"] = pubtime
                fields["images"] = images
                fields["videos"] = videos
                fields["commentnum"] = comm_num
                fields["sharenum"] = share_num
                fields["readnum"] = readnum
                fields["url"] = url
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                num += 1
                logging.info(f"错误数量{num},{e}")

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Sanjiangyuan(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
