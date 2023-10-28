# -*- encoding:utf-8 -*-
"""
@功能:望昆仑解析模板
@AUTHOR：Keane
@文件名：wangkunlun.py
@时间：2020/12/17  17:33
"""

import json
import logging

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class WangKunLunNews(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://mapi.geermurmt.com/api/open/geermu/news_recomend_column.php"
        headers = {
            "Accept-Language": "zh-CN,zh;q=0.8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_391 1.0.0",
            "X-API-TIMESTAMP": "1608886483651BPQ8vC",
            "X-API-SIGNATURE": "OGEzOTU1ZGMyYWE0MzEyMDYzYzc0ZTgzZjlkZTY0YmVmYjcyMGRhZA==",
            "X-API-VERSION": "1.0.1",
            "X-AUTH-TYPE": "sha1",
            "X-API-KEY": "5a4b25aaed25c2ee1b74de72dc03c14e",
            "Host": "mapi.geermurmt.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Cookie": "m2o_mapi_geermurmt_com=eyJpdiI6Ims1aWNoVkJcL3ZRdUN1eXVVQkZkUnhnPT0iLCJ2YWx1ZSI6Ik5sTEtYUUZYQmIxVHdWS0ZPNm5QUTFXSEt4S1k2ZXpJcVR4RVhlaGNPRGlzcFBuMFwvcFVadk1ZOFdoVG1rRTQyQU1iS05yUUkzalROTXhHSVI5b01Jdz09IiwibWFjIjoiMjZmZTA2YmVhNGQ4ZTdhODA2ZjU5OGQzNjc3NzE1YmNhMzUwMDgzN2FiNzNiMWI3ZjhjYTAxNDcxYWQxNWY2ZSJ9",
        }
        data = {
            "count": "10",
            "system_version": "6.0.1",
            "app_version": "1.0.1",
            "client_id_android": "96f74b7a0458c51f7a6d1adfd0d8bc16",
            "locating_city": "格尔木",
            "appkey": "f693b3bffc454cf71ba0a5f3698b9e8d",
            "version": "1.0.1",
            "appid": "m2otksygeia48nkoqu",
            "language": "Chinese",
            "location_city": "格尔木",
            "device_token": "eae7a5f81c6a4a155864a3376879ec8b",
            "phone_models": "MuMu",
            "package_name": "com.hoge.android.app.wkl"
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(channelsres)
        for channel in channelslists:
            channelid = channel['id']
            channelname = channel['name']
            if channelname != '1' and channelname != '新城视听':
                channelparam = InitClass().channel_fields(channelid, channelname)
                yield channelparam

    def getarticlelistparams(self, channelsres):
        channel_num = 0
        headers = {
            "Accept-Language": "zh-CN,zh;q=0.8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_391 1.0.0",
            "X-API-TIMESTAMP": "16088885820319P7X7j",
            "X-API-SIGNATURE": "MGZlZDFiZjY1ZWE2NzFjYTg0M2VhNTFjYjQ0ZWQyMzM0YjlhMjAzMg==",
            "X-API-VERSION": "1.0.1",
            "X-AUTH-TYPE": "sha1",
            "X-API-KEY": "5a4b25aaed25c2ee1b74de72dc03c14e",
            "Host": "mapi.geermurmt.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Cookie": "m2o_mapi_geermurmt_com=eyJpdiI6ImM0b3VVemd4elF6dUdpXC9VMmtCd3l3PT0iLCJ2YWx1ZSI6ImU2UHVMY25MRGQ5XC9aZTcrR281bHNnSDdURDZwb204VlZtTm9KcjRHN09XRzRUXC9hR2tRWFVXcTFwcTZtQW9OMXJ2RDVacGNYc2lweUM0Mk5RdndDcHc9PSIsIm1hYyI6IjMzOTQ1ZDUzMDFlNDA4MzViZDY3MWZhZTFiMTE5Y2YzZjUxOGZmNDVmMmEwODI1YWNkNGJmMmJlNzU3Yzk3YjAifQ%3D%3D",
        }
        url = "http://mapi.geermurmt.com/api/open/geermu/news.php"
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")
            data = {
                "site_id": "1",
                "weight": "90",
                "client_type": "2",
                "count": "20",
                "except_weight": "90",
                "system_version": "6.0.1",
                "app_version": "1.0.1",
                "client_id_android": "96f74b7a0458c51f7a6d1adfd0d8bc16",
                "locating_city": "格尔木",
                "appkey": "f693b3bffc454cf71ba0a5f3698b9e8d",
                "version": "1.0.1",
                "appid": "m2otksygeia48nkoqu",
                "language": "Chinese",
                "location_city": "格尔木",
                "device_token": "eae7a5f81c6a4a155864a3376879ec8b",
                "phone_models": "MuMu",
                "package_name": "com.hoge.android.app.wkl",
                "count": "20",
                "offset": "0",
                "third_offset": "0",
                "column_id": channelid,
                "fid_name": channelname,
            }
            method = 'get'
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
                articleslists = json.loads(articleslists)
                try:
                    for key, articles_arr in articleslists.items():
                        for articles in articles_arr:
                            article_type = articles["type"]
                            if article_type == 'topic':
                                # 这种类型为专题
                                topic_fields = InitClass().topic_fields()
                                articleparam = InitClass().article_list_fields()
                                # 获取文章列表内的有用信息
                                article_id = articles["content_id"]
                                article_title = articles["title"]
                                article_type = articles["type"]
                                share_url = articles['content_url']
                                pubtime = InitClass().date_time_stamp(articles["created_at"])
                                topic = 1
                                topic_fields["channelName"] = channelname
                                topic_fields["channelindexid"] = channel_index_id
                                topic_fields["channelID"] = channelid
                                topic_fields["channeltype"] = channel_type
                                topic_fields["topicID"] = article_id
                                topic_fields["contentType"] = article_type
                                topic_fields["topicUrl"] = share_url
                                topic_fields["pubtime"] = pubtime
                                topic_fields["topic"] = topic
                                topic_fields["title"] = article_title
                                yield topic_fields
                            else:
                                banners = 1 if key == "slide" else 0
                                article_fields = InitClass().article_fields()
                                articleparam = InitClass().article_list_fields()
                                # 获取文章列表内的有用信息
                                article_id = articles["detail_id"]
                                article_title = articles["title"]
                                article_type = articles["type"]
                                share_url = articles['content_url']
                                pubtime = InitClass().date_time_stamp(articles["created_at"])
                                article_covers = list()
                                if 'index_pic' in articles:
                                    article_covers.append(articles["index_pic"])
                                # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                                article_fields["banner"] = banners
                                article_fields["articlecovers"] = article_covers
                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["channelindexid"] = channel_index_id
                                article_fields["channeltype"] = channel_type
                                article_fields["workerid"] = article_id
                                article_fields["title"] = article_title
                                article_fields["contentType"] = article_type
                                article_fields["url"] = share_url
                                article_fields["pubtime"] = pubtime
                                yield article_fields
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")

    def getarticleparams(self,articleslistsres):
        for article in self.analyze_articlelists(articleslistsres):
            articleid = article.get("workerid")
            topic = article.get("topic")
            headers = {
                "Accept-Language": "zh-CN,zh;q=0.8",
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_391 1.0.0",
                "X-API-TIMESTAMP": "1608889607455opVimy",
                "X-API-SIGNATURE": "NzA4YTU4MWYxNWZjYzE4ZTJmNDZhZDNiZThjMWI4NGUxNjAxNWM0Nw==",
                "X-API-VERSION": "1.0.1",
                "X-AUTH-TYPE": "sha1",
                "X-API-KEY": "5a4b25aaed25c2ee1b74de72dc03c14e",
                "Host": "mapi.geermurmt.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "Cookie": "m2o_mapi_geermurmt_com=eyJpdiI6ImI4QkVIQ1JOSnh3UHBaV0FuKzdWT0E9PSIsInZhbHVlIjoibHk3aE04N09SWFVmbEFQc3piUEI1ZFpcL3V3QVp5OWVjajRvaGcxV3lwQTZad2orUHV0Y3BJSUYxazZEUXdLdWI2RXB4TXBDcGRYYlBGc2F3bE96bDBRPT0iLCJtYWMiOiJiNTRkMjQwNjA4MDFiZWQ0NmQyY2QyNDI3Mjc3MTgxNWRkODQwYWYwMzZiZWU0Mjk5MGMzN2RmYWQxNGI1NjBlIn0%3D",
            }
            if topic == 1:
                articleid = article.get("topicID")
                url = "http://mapi.geermurmt.com/api/v1/special_content.php"
                data = {
                    "system_version": "6.0.1",
                    "app_version": "1.0.1",
                    "client_id_android": "96f74b7a0458c51f7a6d1adfd0d8bc16",
                    "locating_city": "格尔木",
                    "appkey": "f693b3bffc454cf71ba0a5f3698b9e8d",
                    "version": "1.0.1",
                    "appid": "m2otksygeia48nkoqu",
                    "language": "Chinese",
                    "location_city": "格尔木",
                    "device_token": "eae7a5f81c6a4a155864a3376879ec8b",
                    "phone_models": "MuMu",
                    "package_name": "com.hoge.android.app.wkl",
                    "column_id": articleid,
                    "offset": "0",
                    "new_style": "2"
                }
            else:
                url = "http://mapi.geermurmt.com/api/v1/item.php"
                data = {
                    "system_version": "6.0.1",
                    "app_version": "1.0.1",
                    "client_id_android": "96f74b7a0458c51f7a6d1adfd0d8bc16",
                    "locating_city": "格尔木",
                    "appkey": "f693b3bffc454cf71ba0a5f3698b9e8d",
                    "version": "1.0.1",
                    "appid": "m2otksygeia48nkoqu",
                    "language": "Chinese",
                    "location_city": "格尔木",
                    "device_token": "eae7a5f81c6a4a155864a3376879ec8b",
                    "phone_models": "MuMu",
                    "package_name": "com.hoge.android.app.wkl",
                    "id": articleid,
                }
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                             article_field=article)
            yield [articleparam]

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            topic = fields.get("topic")
            channelid = article.get("channelid")
            channel_type = article.get("channeltype")
            if topic:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                print(content_s)
                articlesparams = []
                for articles in content_s:
                    article_fields = InitClass().article_fields()
                    articleparam = InitClass().article_list_fields()
                    # 获取文章列表内的有用信息
                    article_id = articles["detail_id"]
                    article_title = articles["title"]
                    article_type = articles["type"]
                    share_url = articles['content_url']
                    pubtime = InitClass().date_time_stamp(articles["created_at"])
                    article_covers = list()
                    if 'index_pic' in articles:
                        article_covers.append(articles["index_pic"])
                    # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                    article_fields["articlecovers"] = article_covers
                    article_fields["channelID"] = channelid
                    article_fields["channelname"] = fields.get('channelName')
                    article_fields["channeltype"] = channel_type
                    article_fields["workerid"] = article_id
                    article_fields["title"] = article_title
                    article_fields["contentType"] = article_type
                    article_fields["url"] = share_url
                    article_fields["pubtime"] = pubtime
                    article_fields["specialtopic"] = topic
                    article_fields["topicid"] = fields.get('_id')
                    article_fields["topicTitle"] = fields.get('title')
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
                    worker_id = content_s["id"]
                    article_title = content_s["title"]
                    author = content_s["publish_user_name"]
                    source = content_s["source"]
                    content = ''
                    contentType = 2
                    if 'content' in content_s.keys():
                        content = content_s["content"]
                    try:
                        if 'video' in content_s.keys():
                            videocovers = [content_s["index_pic"]]
                            videoss = [content_s["video"]["host"] + content_s["video"]["dir"] + content_s["video"][
                                "filepath"] + content_s["video"]["filename"]]
                            fields["videos"] = videoss
                            fields["videocover"] = videocovers
                            contentType = 4
                    except Exception as e:
                        logging.info(f"此新闻无视频{e}")
                    try:
                        images = list()
                        images.append(content_s["indexpic"]['host'] + content_s["indexpic"]['filename'])
                        fields["images"] = images
                    except Exception as e:
                        self.logger.info(f"获取文章内图片失败{e}")
                    readnum = content_s["column_click_num"]
                    likenum = content_s["column_praise_num"]
                    sharenum = content_s["column_share_num"]
                    commentnum = content_s["column_comment_num"]
                    url = content_s["content_url"]
                    fields["url"] = url
                    fields["contentType"] = contentType
                    fields["readnum"] = readnum
                    fields["likenum"] = likenum
                    fields["sharenum"] = sharenum
                    fields["commentnum"] = commentnum
                    fields["appname"] = self.newsname
                    fields["platformID"] = self.platform_id
                    fields["title"] = article_title
                    fields["workerid"] = worker_id
                    fields["content"] = content
                    fields["source"] = source
                    fields["author"] = author
                    fields = InitClass().wash_article_data(fields)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
                except Exception as e:
                    num += 1
                    logging.info(f"错误数量{num},{e}")

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = WangKunLunNews(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
