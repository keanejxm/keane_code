# -*- encoding:utf-8 -*-
"""
@功能:新湖南解析模板
@AUTHOR：Keane
@文件名：xinhunan.py
@时间：2020/12/17  17:33
"""
# 中国长安网-首页

import json
import logging
import urllib
import urllib.parse
import requests

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class Zhongguochanganwang(Appspider):

    @staticmethod
    def get_app_params():
        url1 = "http://www.chinapeace.gov.cn/app/appchannel3/navs.shtml"
        url2 = "http://www.chinapeace.gov.cn/app/appchannel3/navs.shtml"
        for url in [url1, url2]:
            headers = {
                "content-type": "application/x-www-form-urlencoded",
                "credentials": "include",
                "mode": "cors",
                "Host": "www.chinapeace.gov.cn",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.12.1",
                "Connection": "keep-alive",
            }
            data = {}
            method = "get"
            app_params = InitClass().app_params(url, headers, method, data=data)
            yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        dfchannellist = [{"channelname": "北京", "channelId": "110000"},
                         {"channelname": "天津", "channelId": "120000"},
                         {"channelname": "河北", "channelId": "130000"},
                         {"channelname": "山西", "channelId": "140000"},
                         {"channelname": "内蒙", "channelId": "150000"},
                         {"channelname": "辽宁", "channelId": "210000"},
                         {"channelname": "吉林", "channelId": "220000"},
                         {"channelname": "黑龙江", "channelId": "230000"},
                         {"channelname": "上海", "channelId": "310000"},
                         {"channelname": "江苏", "channelId": "320000"},
                         {"channelname": "浙江", "channelId": "330000"},
                         {"channelname": "安徽", "channelId": "340000"},
                         {"channelname": "福建", "channelId": "350000"},
                         {"channelname": "江西", "channelId": "360000"},
                         {"channelname": "山东", "channelId": "370000"},
                         {"channelname": "河南", "channelId": "410000"},
                         {"channelname": "湖北", "channelId": "420000"},
                         {"channelname": "湖南", "channelId": "430000"},
                         {"channelname": "广东", "channelId": "440000"},
                         {"channelname": "广西", "channelId": "450000"},
                         {"channelname": "海南", "channelId": "410000"},
                         {"channelname": "重庆", "channelId": "500000"},
                         {"channelname": "四川", "channelId": "510000"},
                         {"channelname": "贵州", "channelId": "520000"},
                         {"channelname": "云南", "channelId": "530000"},
                         {"channelname": "西藏", "channelId": "540000"},
                         {"channelname": "陕西", "channelId": "610000"},
                         {"channelname": "甘肃", "channelId": "620000"},
                         {"channelname": "青海", "channelId": "630000"},
                         {"channelname": "宁夏", "channelId": "640000"},
                         {"channelname": "新疆", "channelId": "650000"}]
        channelslists = eval(channelsres)
        channellist = channelslists["result"] + dfchannellist
        for channel in channellist:
            channelname = channel["channelName"]
            channelid = channel["channelId"]
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam

    def getarticlelistparams(self, channelsres):
        url = "http://www.chinapeace.gov.cn/xxbs/manuscriptInfo/getManuscriptListByChannelCode"
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "credentials": "include",
            "mode": "cors",
            "Host": "www.chinapeace.gov.cn",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.1",
            "Connection": "keep-alive",
        }
        method = 'get'
        channel_num = 0
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            data = {
                "channelCode": channelid,
                "currentPage": 1
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
            if channelname == "推荐":
                bannerurl = "http://www.chinapeace.gov.cn/app/tjtpxw/list.shtml"
                bannerdata = {}
                banner_param = InitClass().articlelists_params_fields(bannerurl, headers, method, channelname,
                                                                      channelid=channelid, data=bannerdata,
                                                                      channeltype=channeltype, banners=1,
                                                                      channel_index_id=channel_index_id)
                yield channel_field,[banner_param,articlelist_param]
            else:
                yield channel_field,[articlelist_param]

    @staticmethod
    def analyze_articlelists(articleslistsres):
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channel_index_id = articleslistres.get("channelindexid")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            channel_type = articleslistres.get("channeltype")
            banner = articleslistres.get("banner")
            try:
                if banner:
                    articleslists = eval(articleslists)
                else:
                    articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    if "result" in articleslists.keys():
                        contentlist = articleslists["result"]
                        for article in contentlist:
                            author = article["zrbj"]
                            source = article["source"]
                            articletitle = article["title"]
                            articletitle = urllib.parse.unquote(articletitle)
                            articleid = article["manuscriptId"]
                            pubtime = article["published_time"]
                            pubtime = InitClass().date_time_stamp(pubtime)
                            article_covers = list()
                            contents = article["contentSources"]
                            for item in contents:
                                imgurl = item["path"]
                                article_covers.append(imgurl)
                            iszhuanti = article["isZhuant"]
                            if iszhuanti == "1":
                                topic_fields = InitClass().topic_fields()
                                redirecturl = article["redirectUrl"]
                                topic_fields["topicID"] = articleid
                                topic_fields["channelName"] = channelname
                                topic_fields["channelindexid"] = channel_index_id
                                topic_fields["channelID"] = channelid
                                topic_fields["topicUrl"] = redirecturl
                                topic_fields["title"] = articletitle
                                topic_fields["topicCover"] = article_covers
                                topic_fields["topic"] = 1
                                topic_fields["pubTime"] = pubtime
                                topic_fields["articleNum"] = 0
                                topic_fields["createTime"] = 0
                                topic_fields["updateTime"] = 0
                                yield topic_fields
                            else:

                                article_fields = InitClass().article_fields()
                                articleparam = InitClass().article_list_fields()
                                # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["workerid"] = articleid
                                article_fields["title"] = articletitle
                                article_fields["articlecovers"] = article_covers
                                article_fields["banner"] = banner
                                article_fields["author"] = author
                                article_fields["source"] = source
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
            if topic == 1:
                continue
            else:
                url = "http://www.chinapeace.gov.cn/xxbs/manuscriptInfo/getManuscriptContentById"
                headers = {
                    "content-type": "application/x-www-form-urlencoded",
                    "credentials": "include",
                    "mode": "cors",
                    "Host": "www.chinapeace.gov.cn",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.12.1",
                    "Connection": "keep-alive",
                }
                data = {
                    "manuscriptId": articleid
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
            if topic:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                print("专题content_s=", content_s)
            try:

                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))

                # print("普通content_s=",content_s)

                url = content_s["url"]
                content = content_s["content"]
                content = urllib.parse.unquote(content)

                fields["url"] = url
                fields["appname"] = self.newsname
                fields["platformID"] = self.platform_id
                fields["content"] = content

                fields["createtime"] = 0
                fields["updatetime"] = 0
                fields["videocover"] = []
                try:
                    videos = InitClass().get_video(content)
                    fields["videos"] = videos
                except Exception as e:
                    print("无视频")

                try:
                    images = InitClass().get_images(content)
                    fields["images"] = images

                except Exception as e:
                    print("无图片")
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                num += 1
                logging.info(f"错误数量{num},{e}")

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Zhongguochanganwang(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
