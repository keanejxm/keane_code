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
import bs4
from appspider_m import Appspider
from initclass import InitClass



class XinHuNan(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://dtrmmapi.qhxndx.cn/api/open/datong/news_recommend_column.php"
        headers = {
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_393 1.0.0',
            'X-API-TIMESTAMP': '1608857964766Jsu7cq',
            'X-API-SIGNATURE': 'MTA4YjhhNDI0NmE4YWI5YzM3MjUxOGRkMjM5Mzg2YzM2OGRiYmU1Ng==',
            'X-API-VERSION': '1.0.2',
            'X-AUTH-TYPE': 'sha1',
            'X-API-KEY': '70c639df5e30bdee440e4cdf599fec2b',
            'Host': 'dtrmmapi.qhxndx.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'Cookie': 'dtrmm2o_mapi_qhxndx.cn=eyJpdiI6IkVSU254ZGo0UlwvcU9xbTB1MHFGUjRRPT0iLCJ2YWx1ZSI6InpsZjhBMWhPNkRBaUQzMjI2WUJ1NUM1K25rdGw3dEp4VFM1RGhCUW5cL2QxM3BaZEZzN1BENlk2a3ZUb2lueFNFeGJOSGlWc1FvaFB6N2dRbUtUOXlJUT09IiwibWFjIjoiMmQ1NDY2ZTgxMmUzZDg4NmY0YjRlNGJjZjMxNmRmMzQwNWIzYTc1MmNmODg1YzNlNTNjYmMzMzQyYmJjZTk0YSJ9',

        }
        data = {
            'count':'10',
            'system_version':'6.0.1',
            'app_version':'1.0.2',
            'client_type':'android',
            'client_id_android':'06aa128c8b82e098799677297e770303',
            'locating_city':'西宁',
            'appkey':'66716e0b8b96b52ab7c1b819c57343de',
            'version':'1.0.2',
            'appid':'m2oesmxu2sh2xcjsgz',
            'language':'Chinese',
            'location_city':'西宁',
            'device_token':'bd3708a74bd0dd6ed0d9097b8a87e464',
            'phone_models':'MuMu',
            'package_name':'com.hoge.android.app.datong',
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, appjson=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        for channel in channelslists:
            if channel["id"] != 138 and channel["id"] != 117 and channel["id"] != 128 and channel["id"] != 135:
                channelname = channel["name"]
                channelid = channel["id"]
                channelparam = InitClass().channel_fields(channelid, channelname)
                channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            method = 'get'
            url = "http://dtrmmapi.qhxndx.cn/api/open/datong/news.php"
            headers = {
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_393 1.0.0',
                'X-API-TIMESTAMP': '1608857964766Jsu7cq',
                'X-API-SIGNATURE': 'MTA4YjhhNDI0NmE4YWI5YzM3MjUxOGRkMjM5Mzg2YzM2OGRiYmU1Ng==',
                'X-API-VERSION': '1.0.2',
                'X-AUTH-TYPE': 'sha1',
                'X-API-KEY': '70c639df5e30bdee440e4cdf599fec2b',
                'Host': 'dtrmmapi.qhxndx.cn',
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip',
                'Cookie': 'dtrmm2o_mapi_qhxndx.cn=eyJpdiI6IkVSU254ZGo0UlwvcU9xbTB1MHFGUjRRPT0iLCJ2YWx1ZSI6InpsZjhBMWhPNkRBaUQzMjI2WUJ1NUM1K25rdGw3dEp4VFM1RGhCUW5cL2QxM3BaZEZzN1BENlk2a3ZUb2lueFNFeGJOSGlWc1FvaFB6N2dRbUtUOXlJUT09IiwibWFjIjoiMmQ1NDY2ZTgxMmUzZDg4NmY0YjRlNGJjZjMxNmRmMzQwNWIzYTc1MmNmODg1YzNlNTNjYmMzMzQyYmJjZTk0YSJ9',

            }
            data = {
                'site_id':'1',
                'client_type':'2',
                'count':'20',
                'except_weight':'90',
                'system_version':'6.0.1',
                'app_version':'1.0.2',
                'client_type':'android',
                'client_id_android':'06aa128c8b82e098799677297e770303',
                'locating_city':'西宁',
                'appkey':'66716e0b8b96b52ab7c1b819c57343de',
                'version':'1.0.2',
                'appid':'m2oesmxu2sh2xcjsgz',
                'language':'Chinese',
                'location_city':'西宁',
                'device_token':'bd3708a74bd0dd6ed0d9097b8a87e464',
                'phone_models':'MuMu',
                'package_name':'com.hoge.android.app.datong',
                'count':'20',
                'offset':'0',
                'third_offset':'0',
                'column_id':channelid,
                'column_name':channelname,
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
                            article_type = article["type"]
                            if article["type"] == 'link':
                                share_url = article["uri"]
                            else:
                                share_url = ''
                            pubtime = InitClass.date_time_stamp(article['publish_time'])
                            article_covers = list()
                            article_cover = article['index_pic']
                            article_covers.append(article_cover)
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channeltype"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["contentType"] = article_type
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
                            article_type = article["type"]
                            if article["type"] == 'link':
                                share_url = article["uri"]
                            else:
                                share_url = ''
                            pubtime = InitClass.date_time_stamp(article['publish_time'])
                            article_covers = list()
                            article_cover = article['index_pic']
                            article_covers.append(article_cover)
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
            if article_field.get('url') == '':
                url = "http://dtrmmapi.qhxndx.cn/api/v1/item.php"
                headers = {
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_393 1.0.0',
                    'X-API-TIMESTAMP': '1608857964766Jsu7cq',
                    'X-API-SIGNATURE': 'MTA4YjhhNDI0NmE4YWI5YzM3MjUxOGRkMjM5Mzg2YzM2OGRiYmU1Ng==',
                    'X-API-VERSION': '1.0.2',
                    'X-AUTH-TYPE': 'sha1',
                    'X-API-KEY': '70c639df5e30bdee440e4cdf599fec2b',
                    'Host': 'dtrmmapi.qhxndx.cn',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                    'Cookie': 'dtrmm2o_mapi_qhxndx.cn=eyJpdiI6IkVSU254ZGo0UlwvcU9xbTB1MHFGUjRRPT0iLCJ2YWx1ZSI6InpsZjhBMWhPNkRBaUQzMjI2WUJ1NUM1K25rdGw3dEp4VFM1RGhCUW5cL2QxM3BaZEZzN1BENlk2a3ZUb2lueFNFeGJOSGlWc1FvaFB6N2dRbUtUOXlJUT09IiwibWFjIjoiMmQ1NDY2ZTgxMmUzZDg4NmY0YjRlNGJjZjMxNmRmMzQwNWIzYTc1MmNmODg1YzNlNTNjYmMzMzQyYmJjZTk0YSJ9',
                }
                data = {
                    'system_version':'6.0.1',
                    'app_version':'1.0.2',
                    'client_type':'android',
                    'client_id_android':'06aa128c8b82e098799677297e770303',
                    'locating_city':'西宁',
                    'appkey':'66716e0b8b96b52ab7c1b819c57343de',
                    'version':'1.0.2',
                    'appid':'m2oesmxu2sh2xcjsgz',
                    'language':'Chinese',
                    'location_city':'西宁',
                    'device_token':'bd3708a74bd0dd6ed0d9097b8a87e464',
                    'phone_models':'MuMu',
                    'package_name':'com.hoge.android.app.datong',
                    'id':articleid,
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
            if fields.get("url") != '':
               url = fields.get("url")
               print(url)
            else:
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                    print(content_s)
                    worker_id = content_s['id']
                    article_title = content_s["title"]
                    if 'author' in content_s.keys():
                        author = content_s["author"]
                    else:
                        author = ''
                    source = content_s['source']
                    if 'content' in content_s.keys():
                        content = content_s['content']
                    else:
                        content = ''
                    comment_num = content_s['comments']
                    hit_num = content_s['clicks']  # 点击数
                    try:
                        if 'streams' in  content_s.keys():
                            videocovers = list()
                            videos = list()
                            videocovers.append(content_s['index_pic'])
                            videoss = content_s["streams"]["media_url"]
                            videos.append(videoss)
                            fields["videos"] = videos
                            fields["videocover"] = videocovers
                    except Exception as e:
                        logging.info(f"此新闻无视频{e}")
                    try:
                        imagess = content_s['index_pic']
                        images = list()
                        images.append(imagess)
                        fields["images"] = images
                    except Exception as e:
                        self.logger.info(f"获取文章内图片失败{e}")
                    fields["appname"] = self.newsname
                    fields["title"] = article_title
                    fields["workerid"] = worker_id
                    fields["content"] = content
                    fields["readnum"] = hit_num
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
    appspider = XinHuNan("大通融媒")
    appspider.run()
