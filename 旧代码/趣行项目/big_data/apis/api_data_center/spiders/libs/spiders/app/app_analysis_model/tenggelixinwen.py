# -*- encoding:utf-8 -*-
"""
@功能:腾格里新闻解析模板
@AUTHOR：Keane
@文件名：ZhongGuoLan.py
@时间：2020/12/17  17:33
"""

import json
import logging

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class TengGeLiNews(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://mapi.m2oplus.nmtv.cn/api/open/nmtv/news_recomend_column.php"
        headers = {
            "Accept-Language": "zh-CN,zh;q=0.8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_399 1.0.0",
            "X-API-TIMESTAMP": "1608775143727mPCP9A",
            "X-API-SIGNATURE": "OTI0ODE2OThkNmViZWM5ZTU2MTE1NmNmNzI1Zjk2YzJjZjQyMmIzNA==",
            "X-API-VERSION": "3.2.2",
            "X-AUTH-TYPE": "sha1",
            "X-API-KEY": "352fe25daf686bdb4edca223c921acea",
            "Host": "mapi.m2oplus.nmtv.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        data = {
            "count": "10",
            "system_version": "6.0.1",
            "app_version": "3.2.2",
            "client_type": "android",
            "client_id_android": "3b4da3543889c3cfa7c4bde8221ba213",
            "locating_city": "呼和浩特",
            "appkey": "8ac448c9e37116888e64b8fea0fb35ac",
            "version": "3.2.2",
            "appid": "m2offty0m1tvuvibwb",
            "language": "Chinese",
            "location_city": "呼和浩特",
            "device_token": "d119c798abcab29ed55d8b2d9db62388",
            "phone_models": "MuMu",
            "package_name": "com.hoge.android.app.nmwlt"
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
            if channelname != '百灵悦听':
                if channelname == '爱上内蒙古':
                    channelid = 411
                channelparam = InitClass().channel_fields(channelid, channelname)
                yield channelparam
        yield {"channelid": "123", "channelname": "首页"}

    def getarticlelistparams(self, channelsres):
        channel_num = 0
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")
            if channelname == '爱上内蒙古':
                url = "http://mapi.m2oplus.nmtv.cn/api/v1/special_content.php?"
                headers = {
                    "Accept-Language": "zh-CN,zh;q=0.8",
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_399 1.0.0",
                    "X-API-TIMESTAMP": "1608778820715RE1Ykr",
                    "X-API-SIGNATURE": "MjVhNWUyZjIwMjhjYmY5ZWY3MDcxYzM1MzkzNTQ1YjVjZDMwNDEwNg==",
                    "X-API-VERSION": "3.2.2",
                    "X-AUTH-TYPE": "sha1",
                    "X-API-KEY": "352fe25daf686bdb4edca223c921acea",
                    "Host": "mapi.m2oplus.nmtv.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",

                }
                data = {
                    "app_version": "3.2.2",
                    "appid": "m2offty0m1tvuvibwb",
                    "appkey": "8ac448c9e37116888e64b8fea0fb35ac",
                    "client_id_android": "3b4da3543889c3cfa7c4bde8221ba213",
                    "client_type": "android",
                    "column_id": channelid,
                    "device_token": "d119c798abcab29ed55d8b2d9db62388",
                    "language": "Chinese",
                    "locating_city": "呼和浩特",
                    "location_city": "呼和浩特",
                    "new_style": "2",
                    "offset": "0",
                    "package_name": "com.hoge.android.app.nmwlt",
                    "phone_models": "MuMu",
                    "system_version": "6.0.1",
                    "version": "3.2.2"
                }
            elif channelname == '首页':
                headers = {
                    "Accept-Language": "zh-CN,zh;q=0.8",
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_399 1.0.0",
                    "X-API-TIMESTAMP": "16087907767028zz6Mo",
                    "X-API-SIGNATURE": "ZTRmYWM0MzQyNTA4MDYxNTcyZDFkMDE1NDZjODc4YzQxY2NjMjEzNw==",
                    "X-API-VERSION": "3.2.2",
                    "X-AUTH-TYPE": "sha1",
                    "X-API-KEY": "352fe25daf686bdb4edca223c921acea",
                    "Host": "mapi.m2oplus.nmtv.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip"
                }
                url = "http://mapi.m2oplus.nmtv.cn/api/open/nmtv/home_page_new.php"
                data = {
                    "system_version": "6.0.1",
                    "app_version": "3.2.2",
                    "client_type": "android",
                    "client_id_android": "3b4da3543889c3cfa7c4bde8221ba213",
                    "locating_city": "呼和浩特",
                    "appkey": "8ac448c9e37116888e64b8fea0fb35ac",
                    "version": "3.2.2",
                    "appid": "m2offty0m1tvuvibwb",
                    "language": "Chinese",
                    "location_city": "呼和浩特",
                    "device_token": "d119c798abcab29ed55d8b2d9db62388",
                    "phone_models": "MuMu",
                    "package_name": "com.hoge.android.app.nmwlt",
                }
            else:
                headers = {
                    "Accept-Language": "zh-CN,zh;q=0.8",
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_399 1.0.0",
                    "X-API-TIMESTAMP": "1608775539201hXxBWN",
                    "X-API-SIGNATURE": "NTdhOTQ3MzRkZGUxNGJmNDRlNDM5MmVjMTgyMDViNDFlZGEzMGMxNw==",
                    "X-API-VERSION": "3.2.2",
                    "X-AUTH-TYPE": "sha1",
                    "X-API-KEY": "352fe25daf686bdb4edca223c921acea",
                    "Host": "mapi.m2oplus.nmtv.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip"

                }
                url = "http://mapi.m2oplus.nmtv.cn/api/open/nmtv/news.php"
                data = {
                    "site_id": "1",
                    "client_type": "2",
                    "count": "20",
                    "except_weight": "90",
                    "system_version": "6.0.1",
                    "app_version": "3.2.2",
                    "client_type": "android",
                    "client_id_android": "3b4da3543889c3cfa7c4bde8221ba213",
                    "locating_city": "呼和浩特",
                    "appkey": "8ac448c9e37116888e64b8fea0fb35ac",
                    "version": "3.2.2",
                    "appid": "m2offty0m1tvuvibwb",
                    "language": "Chinese",
                    "location_city": "呼和浩特",
                    "device_token": "d119c798abcab29ed55d8b2d9db62388",
                    "phone_models": "MuMu",
                    "package_name": "com.hoge.android.app.nmwlt",
                    "column_id": channelid,
                    "since_id": "592357",
                    "group": "1",
                    "fid_name": channelname
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
                    if channelname == '首页':
                        for article_list in articleslists:
                            if article_list['name'] == '视频' or article_list['name'] == '习近平专题' or article_list[
                                'name'] == '48小时热榜' or article_list['name'] == '轮转图':
                                for lists in article_list['data']:
                                    for articles in lists['data']:
                                        article_type = articles["type"]
                                        if article_type != 'link':
                                            if article_type == 'topic':
                                                # 这种类型为专题
                                                print(articles)
                                                topic_fields = InitClass().topic_fields()
                                                articleparam = InitClass().article_list_fields()
                                                # 获取文章列表内的有用信息
                                                article_id = articles["content_id"]
                                                article_title = articles["title"]
                                                article_type = articles["type"]
                                                share_url = articles['content_url']
                                                pubtime = int(articles["publish_time_stamp"]) * 1000
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
                                                # 将请求文章必需信息存入
                                                yield topic_fields
                                            else:
                                                article_fields = InitClass().article_fields()
                                                articleparam = InitClass().article_list_fields()
                                                # 获取文章列表内的有用信息
                                                article_id = articles["id"]
                                                article_title = articles["title"]
                                                article_type = articles["type"]
                                                share_url = articles['content_url']
                                                pubtime = int(articles["publish_time_stamp"]) * 1000
                                                article_covers = list()
                                                if articles["index_pic"]:
                                                    article_covers.append(articles["index_pic"])
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
                                                # 将请求文章必需信息存入
                    else:
                        if channelname == '爱上内蒙古':
                            lists = articleslists
                        else:
                            lists = articleslists["list"]
                        for articles in lists:
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
                                pubtime = int(articles["publish_time_stamp"]) * 1000
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
                                # 将请求文章必需信息存入
                            else:
                                article_fields = InitClass().article_fields()
                                articleparam = InitClass().article_list_fields()
                                # 获取文章列表内的有用信息
                                article_id = articles["id"]
                                article_title = articles["title"]
                                article_type = articles["type"]
                                share_url = articles['content_url']
                                pubtime = int(articles["publish_time_stamp"]) * 1000
                                article_covers = list()
                                if articles["index_pic"]:
                                    article_covers.append(articles["index_pic"])
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
                url = "http://mapi.m2oplus.nmtv.cn/api/v1/special_content.php?"
                headers = {
                    "Accept-Language": "zh-CN,zh;q=0.8",
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_399 1.0.0",
                    "X-API-TIMESTAMP": "1608778820715RE1Ykr",
                    "X-API-SIGNATURE": "MjVhNWUyZjIwMjhjYmY5ZWY3MDcxYzM1MzkzNTQ1YjVjZDMwNDEwNg==",
                    "X-API-VERSION": "3.2.2",
                    "X-AUTH-TYPE": "sha1",
                    "X-API-KEY": "352fe25daf686bdb4edca223c921acea",
                    "Host": "mapi.m2oplus.nmtv.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",

                }
                data = {
                    "app_version": "3.2.2",
                    "appid": "m2offty0m1tvuvibwb",
                    "appkey": "8ac448c9e37116888e64b8fea0fb35ac",
                    "client_id_android": "3b4da3543889c3cfa7c4bde8221ba213",
                    "client_type": "android",
                    "column_id": articleid,
                    "device_token": "d119c798abcab29ed55d8b2d9db62388",
                    "language": "Chinese",
                    "locating_city": "呼和浩特",
                    "location_city": "呼和浩特",
                    "new_style": "2",
                    "offset": "0",
                    "package_name": "com.hoge.android.app.nmwlt",
                    "phone_models": "MuMu",
                    "system_version": "6.0.1",
                    "version": "3.2.2"
                }
            else:
                url = "http://mapi.m2oplus.nmtv.cn/api/v1/item.php"
                headers = {
                    "Accept-Language": "zh-CN,zh;q=0.8",
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_399 1.0.0",
                    "X-API-TIMESTAMP": "16087791446287fOE8A",
                    "X-API-SIGNATURE": "YWY1MzlkZDJkZWM2MTg4NDdjYmEwMTFlMjYwYTNlYTFhNGYzNTZiNg==",
                    "X-API-VERSION": "3.2.2",
                    "X-AUTH-TYPE": "sha1",
                    "X-API-KEY": "352fe25daf686bdb4edca223c921acea",
                    "Host": "mapi.m2oplus.nmtv.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip"
                }
                data = {
                    "app_version": "3.2.2",
                    "appid": "m2offty0m1tvuvibwb",
                    "appkey": "8ac448c9e37116888e64b8fea0fb35ac",
                    "client_id_android": "3b4da3543889c3cfa7c4bde8221ba213",
                    "client_type": "android",
                    "device_token": "d119c798abcab29ed55d8b2d9db62388",
                    "id": articleid,
                    "language": "Chinese",
                    "locating_city": "呼和浩特",
                    "location_city": "呼和浩特",
                    "package_name": "com.hoge.android.app.nmwlt",
                    "phone_models": "MuMu",
                    "system_version": "6.0.1",
                    "version": "3.2.2"
                }
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                             article_field=article)
            yield [articleparam]

    def analyzearticle(self, articleres):
        print(articleres)
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
                    article_id = articles["id"]
                    article_title = articles["title"]
                    article_type = articles["type"]
                    share_url = articles['content_url']
                    pubtime = int(articles["publish_time_stamp"]) * 1000
                    article_covers = list()
                    if articles["index_pic"]:
                        article_covers.append(articles["index_pic"])
                    article_fields["articlecovers"] = article_covers
                    article_fields["channelID"] = channelid
                    article_fields["channelname"] = fields.get("channelName")
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
    appspider = TengGeLiNews(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
