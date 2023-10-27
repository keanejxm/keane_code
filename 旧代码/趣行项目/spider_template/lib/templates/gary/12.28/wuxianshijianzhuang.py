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
        url = "http://mobile.sjzntv.cn/sjz3/news_recomend_column_sy.php"
        headers = {
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_167 1.0.0',
            'X-API-TIMESTAMP': '16092042728180zw8tJ',
            'X-API-SIGNATURE': 'YWVjMDBkZWJiNjc1NWE3ZGI1MDdjYzBiMGUwYmRkNTg4YjZhMjBkOA==',
            'X-API-VERSION': '3.0.2',
            'X-AUTH-TYPE': 'sha1',
            'X-API-KEY': '5878a7ab84fb43402106c575658472fa',
            'Host': 'mobile.sjzntv.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        data = {
            'system_version': '6.0.1',
            'app_version': '3.0.2',
            'client_type': 'android',
            'client_id_android': 'c7c27e697870fa1eb69c8614e003f4fe',
            'locating_city': '石家庄',
            'appkey': 'BJaFDrsqqZQelNRXE6EhUXmlfzhq5Rox',
            'version': '3.0.2',
            'appid': '8',
            'language': 'Chinese',
            'location_city': '石家庄',
            'device_token': '0e0c31f2960d924f9452002c744814f0',
            'phone_models': 'MuMu',
            'package_name': 'com.hoge.android.app.wxsjz',
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        for channel in channelslists:
            channelname = channel["name"]
            channelid = channel["id"]
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        headers = {
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_167 1.0.0',
            'X-API-TIMESTAMP': '1609205801869wwGm9x',
            'X-API-SIGNATURE': 'MzQxYzgzYmIyMzA0NGQ0YzcwZjUxYTIyNzYzYTJlNDg1YjE5YzRhOQ==',
            'X-API-VERSION': '3.0.2',
            'X-AUTH-TYPE': 'sha1',
            'X-API-KEY': '5878a7ab84fb43402106c575658472fa',
            'Host': 'mobile.sjzntv.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        method = 'get'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            if channelid == '2584':
                url = 'http://mobile.sjzntv.cn/sjz3/news_tj.php'
            else:
                url = 'http://mobile.sjzntv.cn/sjz3/news.php'
            data = {
                'site_id': '1',
                'client_type': '2',
                'count': '20',
                'except_weight': '90',
                'system_version': '6.0.1',
                'app_version': '3.0.2',
                'client_type': 'android',
                'client_id_android': 'c7c27e697870fa1eb69c8614e003f4fe',
                'locating_city': '石家庄',
                'appkey': 'BJaFDrsqqZQelNRXE6EhUXmlfzhq5Rox',
                'version': '3.0.2',
                'appid': '8',
                'language': 'Chinese',
                'location_city': '石家庄',
                'device_token': '0e0c31f2960d924f9452002c744814f0',
                'phone_models': 'MuMu',
                'package_name': 'com.hoge.android.app.wxsjz',
                'column_id': channelid,
                'since_id': '738804',
                'group': '1',
                'column_id': channelid,
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
                    if 'slide' in articleslists.keys():
                        #banner
                        for article in articleslists["slide"]:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article["id"]
                            article_title = article["title"]
                            article_type = article['bundle_id']
                            share_url = article['content_url']
                            pubtime = int(article['publish_time_stamp']) * 1000
                            article_covers = list()
                            article_cover = article['indexpic']['host']+article['indexpic']['dir']+article['indexpic']['filepath']+article['indexpic']['filename']
                            article_covers.append(article_cover)
                            if article['bundle_id'] == 'special':
                                #专题
                                topic_fields = InitClass().topic_fields()
                                topic_fields["channelName"] = channelname
                                topic_fields["channelID"] = channelid
                                topic_fields["channeltype"] = channel_type
                                topic_fields["workerid"] = article_id
                                topic_fields["_id"] = article['content_fromid']
                                topic_fields["contentType"] = article_type
                                topic_fields["topicUrl"] = share_url
                                topic_fields["title"] = article_title
                                topic_fields["pubtime"] = pubtime
                                topic_fields["topic"] = 1
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
                                article_fields["articlecovers"] = article_covers
                                article_fields["url"] = share_url
                                article_fields["pubtime"] = pubtime
                                article_fields["banner"] = 1
                                # 将请求文章必需信息存入
                                articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)
                    if 'list' in articleslists.keys():
                        for article in articleslists["list"]:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article["id"]
                            article_title = article["title"]
                            article_type = article['bundle_id']
                            share_url = article['content_url']
                            pubtime = int(article['publish_time_stamp']) * 1000
                            article_covers = list()
                            article_cover = article['indexpic']['host']+article['indexpic']['dir']+article['indexpic']['filepath']+article['indexpic']['filename']
                            article_covers.append(article_cover)
                            if article['bundle_id'] == 'special':
                                #专题
                                topic_fields = InitClass().topic_fields()
                                topic_fields["channelName"] = channelname
                                topic_fields["channelID"] = channelid
                                topic_fields["channeltype"] = channel_type
                                topic_fields["workerid"] = article_id
                                topic_fields["_id"] = article['content_fromid']
                                topic_fields["contentType"] = article_type
                                topic_fields["topicUrl"] = share_url
                                topic_fields["title"] = article_title
                                topic_fields["pubtime"] = pubtime
                                topic_fields["topic"] = 1
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
                                article_fields["articlecovers"] = article_covers
                                article_fields["url"] = share_url
                                article_fields["pubtime"] = pubtime
                                # 将请求文章必需信息存入
                                articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)
                    if 'toutiao' in articleslists.keys():
                        for article in articleslists["toutiao"]:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article["id"]
                            article_title = article["title"]
                            article_type = article['bundle_id']
                            share_url = article['content_url']
                            pubtime = int(article['publish_time_stamp']) * 1000
                            article_covers = list()
                            article_cover = article['indexpic']['host']+article['indexpic']['dir']+article['indexpic']['filepath']+article['indexpic']['filename']
                            article_covers.append(article_cover)
                            if article['bundle_id'] == 'special':
                                #专题
                                topic_fields = InitClass().topic_fields()
                                topic_fields["channelName"] = channelname
                                topic_fields["channelID"] = channelid
                                topic_fields["channeltype"] = channel_type
                                topic_fields["workerid"] = article_id
                                topic_fields["_id"] = article['content_fromid']
                                topic_fields["contentType"] = article_type
                                topic_fields["topicUrl"] = share_url
                                topic_fields["title"] = article_title
                                topic_fields["pubtime"] = pubtime
                                topic_fields["topic"] = 1
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
                                article_fields["articlecovers"] = article_covers
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
                url = "http://mobile.sjzntv.cn/sjz3/special_content.php"
                headers = {
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_167 1.0.0',
                    'X-API-TIMESTAMP': '16092141148976lKoHJ',
                    'X-API-SIGNATURE': 'YmVmZDhjMjUzYTZiMGYyYjU0NGNiZDBjODdjMDRiY2QwN2VjMGQ3Nw==',
                    'X-API-VERSION': '3.0.2',
                    'X-AUTH-TYPE': 'sha1',
                    'X-API-KEY': '5878a7ab84fb43402106c575658472fa',
                    'Host': 'mobile.sjzntv.cn',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                }
                data = {
                    'system_version': '6.0.1',
                    'app_version': '3.0.2',
                    'client_type': 'android',
                    'client_id_android': 'c7c27e697870fa1eb69c8614e003f4fe',
                    'locating_city': '石家庄',
                    'appkey': 'BJaFDrsqqZQelNRXE6EhUXmlfzhq5Rox',
                    'version': '3.0.2',
                    'appid': '8',
                    'language': 'Chinese',
                    'location_city': '石家庄',
                    'device_token': '0e0c31f2960d924f9452002c744814f0',
                    'phone_models': 'MuMu',
                    'package_name': 'com.hoge.android.app.wxsjz',
                    'column_id': article_field.get('_id'),
                    'offset': '0',
                    'new_style': '2',
                }
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            else:
                url = "http://mobile.sjzntv.cn/sjz3/item.php"
                headers = {
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_167 1.0.0',
                    'X-API-TIMESTAMP': '1609210250609nRpHSn',
                    'X-API-SIGNATURE': 'YTE2Zjc2ZmQ2MWRmYzdkMGU2N2YwNjU5NDIxZjEzNzI4MDk3NTE2YQ==',
                    'X-API-VERSION': '3.0.2',
                    'X-AUTH-TYPE': 'sha1',
                    'X-API-KEY': '5878a7ab84fb43402106c575658472fa',
                    'Host': 'mobile.sjzntv.cn',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                }
                data = {
                    'system_version':'6.0.1',
                    'app_version':'3.0.2',
                    'client_type':'android',
                    'client_id_android':'c7c27e697870fa1eb69c8614e003f4fe',
                    'locating_city':'石家庄',
                    'appkey':'BJaFDrsqqZQelNRXE6EhUXmlfzhq5Rox',
                    'version':'3.0.2',
                    'appid':'8',
                    'language':'Chinese',
                    'location_city':'石家庄',
                    'device_token':'0e0c31f2960d924f9452002c744814f0',
                    'phone_models':'MuMu',
                    'package_name':'com.hoge.android.app.wxsjz',
                    "id": articleid,
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
                print(content_s)
                try:
                    articlesparams = []
                    for article in content_s:
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        article_id = article["id"]
                        article_title = article["title"]
                        article_type = article['bundle_id']
                        share_url = article['content_url']
                        pubtime = int(article['publish_time_stamp']) * 1000
                        article_covers = list()
                        article_cover = article['indexpic']['host'] + article['indexpic']['dir'] + article['indexpic'][
                            'filepath'] + article['indexpic']['filename']
                        article_covers.append(article_cover)
                        article_fields["channelID"] = fields.get('channelID')
                        article_fields["channelname"] = fields.get('channelName')
                        article_fields["channeltype"] = fields.get('channeltype')
                        article_fields["workerid"] = article_id
                        article_fields["title"] = article_title
                        article_fields["contentType"] = article_type
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
                except Exception as e:
                    print(e)
            else:
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                    print(content_s)
                    worker_id = content_s["id"]
                    article_title = content_s["title"]
                    source = content_s["source"]
                    if 'content' in content_s.keys():
                        content = content_s["content"]
                    else:
                        content=''
                    comment_num = content_s['comment_num']
                    hit_num = content_s['click_num']  # 点击数
                    share_num = content_s['share_num']
                    if content != '':
                        images = InitClass.get_images(content)
                        videos = InitClass.get_video(content)
                    else:
                        images = [content_s['indexpic']['host']+content_s['indexpic']['dir']+content_s['indexpic']['filepath']+content_s['indexpic']['filename']]
                        videos = [content_s['indexpic']['host']+content_s['indexpic']['filepath']+content_s['indexpic']['filename']]
                    fields["appname"] = self.newsname
                    fields["title"] = article_title
                    fields["images"] = images
                    fields["videos"] = videos
                    fields["workerid"] = worker_id
                    fields["content"] = content
                    fields["source"] = source
                    fields["commentnum"] = comment_num
                    fields["sharenum"] = share_num
                    fields["readnum"] = hit_num
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
    appspider = XinHuNan("新湖南")
    appspider.run()
