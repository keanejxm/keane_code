# -*- encoding:utf-8 -*-
"""
@功能:缙享北碚解析模板
@AUTHOR：ava
@文件名：jinxiangbeibei.py
@时间：2020/12/17  17:33
"""

import json
import logging
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class JinXiangBeiBei(Appspider):

    @staticmethod
    def analyze_channel():
        channelparams = [
            {
                "channelid": 4600,
                "channelname": "学习"
            },
            {
                "channelid": 4601,
                "channelname": "要闻",
            },
            {
                "channelid": 10083,
                "channelname": "专题",
            },
            {
                "channelid": 4602,
                "channelname": "北碚",
            },
            {
                "channelid": 4608,
                "channelname": "北碚视频",
            },
            {
                "channelid": 4607,
                "channelname": "新华短视频",
            }

        ]
        return channelparams

    def getarticlelistparams(self):
        channel_num = 0
        headers = {
            "Cookie": "PORSESSIONID=2E6BC7D5D6D5CBA0DC3B6DE391EB5D57",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Content-Length": "151",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
            "Host": "api.cqliving.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Cookie": "PORSESSIONID=2E6BC7D5D6D5CBA0DC3B6DE391EB5D57",

        }
        for channel in self.analyze_channel():
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")
            url = "https://api.cqliving.com/info/news.html"
            data = {
                "appId": "15",
                "isCarousel": "true",
                "columnId": channelid,
                "businessValue": "",
                "unionValue": "",
                "lastId": "",
                "lastSortNo": "",
                "lastOnlineTime": "",
                "sessionId": "c882577d6308400791bb0256e43bda21",
                "token": "",
            }
            method = 'post'
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
                print(articleslists)
                try:
                    for key, articles_arr in articleslists["data"].items():
                        if key == 'carousels' or key == 'news':
                            for articles in articles_arr:
                                article_type = articles["type"]
                                if articles["contentUrl"] == '' or channelname == '北碚视频' or channelname == '专题':
                                    if article_type == 2:
                                        # 这种类型为专题
                                        topic_fields = InitClass().topic_fields()
                                        articleparam = InitClass().article_list_fields()
                                        # 获取文章列表内的有用信息
                                        article_id = articles["id"]
                                        article_title = articles["title"]
                                        article_type = articles["contextType"]
                                        share_url = articles['shareUrl']
                                        pubtime = InitClass().date_time_stamp(articles["onlineTime"])
                                        topic = 1
                                        topic_fields["channelName"] = channelname
                                        topic_fields["channelindexid"] = channel_index_id
                                        topic_fields["channelID"] = channelid
                                        topic_fields["channeltype"] = channel_type
                                        topic_fields["_id"] = article_id
                                        topic_fields["contentType"] = article_type
                                        topic_fields["topicUrl"] = share_url
                                        topic_fields["pubtime"] = pubtime
                                        topic_fields["topic"] = topic
                                        topic_fields["title"] = article_title
                                        # 将请求文章必需信息存入
                                        articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                        articleparam["articleid"] = article_id
                                        yield articleparam
                                    else:
                                        article_fields = InitClass().article_fields()
                                        articleparam = InitClass().article_list_fields()
                                        # 获取文章列表内的有用信息
                                        article_id = articles["id"]
                                        article_title = articles["title"]
                                        article_type = articles["contextType"]
                                        share_url = articles['shareUrl']
                                        pubtime = InitClass().date_time_stamp(articles["onlineTime"])
                                        article_covers = list()
                                        if articles['images'] != '':
                                            img = articles['images'].split(',')
                                            article_covers = img
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
                                        # 将请求文章必需信息存入
                                        articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                        articleparam["articleid"] = article_id
                                        yield articleparam
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")

    def getarticleparams(self, articleslistsres):
        for article in self.analyze_articlelists(articleslistsres):
            articleid = article.get("articleid")
            article_field = article.get("articleField")
            topic = article_field.get("topic")
            if topic == 1:
                url = "https://api.cqliving.com/info/getSpecialDetail.html"
                headers = {
                    "Cookie": "PORSESSIONID=27DDD30E62F97A8AF57561BD7D4B369F",
                    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                    "Content-Length": "31",
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
                    "Host": "api.cqliving.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "Cookie": "PORSESSIONID=27DDD30E62F97A8AF57561BD7D4B369F",

                }
                data = {
                    "appId": "15",
                    "infoClassifyId": articleid,
                }
            else:
                url = "https://exapi.cqliving.com/infoDetailNew.html"
                headers = {
                    "Host": "exapi.cqliving.com",
                    "Connection": "keep-alive",
                    "Content-Length": "22",
                    "Accept": "application/json, text/plain, */*",
                    "Origin": "https://share.cqliving.com",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 CQ_XHL(2031;Android;15;c882577d6308400791bb0256e43bda21;;0) CQ_XHL(2031;Android;15;c882577d6308400791bb0256e43bda21;;0)",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Referer": "https://share.cqliving.com/news-detail-pages/",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,en-US;q=0.8",
                    "X-Requested-With": "com.xhl.beibei",
                }
                data = {
                    "infoClassifyId": articleid,
                }
            method = 'post'
            articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                             article_field=article_field)
            yield [articleparam]

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            topic = fields.get("topic")
            channelname = article.get("channelname")
            channelid = article.get("channelid")
            channel_type = article.get("channeltype")
            if topic:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                print(content_s)
                articlesparams = []
                for articles in content_s["data"]["firstPageData"]["dataList"]:
                    if articles["contentUrl"] == '' or channelname == '北碚视频' or channelname == '专题':
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        # 获取文章列表内的有用信息
                        article_id = articles["id"]
                        article_title = articles["title"]
                        article_type = articles["contextType"]
                        share_url = articles['url']
                        pubtime = InitClass().date_time_stamp(articles["onlineTime"])
                        article_covers = list()
                        if articles['images'] != '':
                            img = articles['images'].split(',')
                            article_covers = img
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
                        # fields = InitClass().wash_article_data(fields)
                        # yield {"code": 1, "msg": "OK", "data": {"works": article_fields}}
                # if len(articlesparams):
                #     aaaa = self.getarticleparams(articlesparams)
                #     bbbb = self.getarticlehtml(aaaa.__next__())
                #     self.analyzearticle(bbbb.__next__())
            else:
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                    print(content_s)
                    worker_id = content_s["data"]["classifyId"]
                    article_title = content_s["data"]["title"]
                    author = content_s["data"]["updator"]
                    source = content_s["data"]["infoSource"]
                    content = InitClass().wash_tag(content_s["data"]["content"])
                    images = InitClass().get_images(content)
                    fields["images"] = images
                    content_type = 2
                    try:
                        if content_s["data"]["contextType"] == 1:
                            images = list()
                            for img in content_s["data"]["appResource"]:
                                images.append(img['fileUrl'])
                            fields["images"] = images
                            content_type = 6
                        elif content_s["data"]["contextType"] == 5:
                            videocovers = list()
                            videos = list()
                            if content_s["data"]["contentUrl"]:
                                videos.append(content_s["data"]["contentUrl"])
                                if content_s["data"]["listViewImg"]:
                                    videocovers.append(content_s["data"]["listViewImg"])
                                fields["videos"] = videos
                                fields["videocover"] = videocovers
                                content_type = 4
                    except Exception as e:
                        logging.info(f"此新闻无视频{e}")

                    fields["appname"] = self.newsname
                    fields["platformID"] = self.platform_id
                    fields["contentType"] = content_type
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
    appspider = JinXiangBeiBei(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for channel_field, channel_param in appspider.getarticlelistparams():
        for article_list_res in appspider.getarticlelists(channel_param):
            for article_param in appspider.getarticleparams(article_list_res):
                for article_res in appspider.getarticlehtml(article_param):
                    for data in appspider.analyzearticle(article_res):
                        yield data
        yield {"code": 1, "msg": "OK", "data": {"channel": channel_field}}
