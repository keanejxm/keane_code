# -*- encoding:utf-8 -*-
"""
@功能:内蒙古头条解析模板
@AUTHOR：Keane
@文件名：NeiMengGuTouTiao.py
@时间：2020/12/17  17:33
"""

import json
import logging

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class NeiMengGuTouTiao(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://app.nmgcb.com.cn/chenbao/api/index/indexNav"
        headers = {
            "Content-Type": "application/json",
            "Charset": "UTF-8",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Host": "app.nmgcb.com.cn"
        }
        data = {}
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(channelsres)
        for channel in channelslists['data']:
            channelid = channel['id']
            channelname = channel['title']
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam

    def getarticlelistparams(self, channelsres):
        channel_num = 0
        headers = {
            "Content-Type": "application/json",
            "Charset": "UTF-8",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Host": "app.nmgcb.com.cn"
        }
        url = "http://app.nmgcb.com.cn/chenbao/api/index/newsList"
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")
            data = {
                "navId": channelid,
                "page": "1"
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
                    for articles in articleslists["data"]:
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        # 获取文章列表内的有用信息
                        article_id = articles["id"]
                        article_title = articles["title"]
                        article_type = 2
                        share_url = f'http://app.nmgcb.com.cn/chenbao/index/index/index?navId={channelid}&id={article_id}'
                        pubtime = int(articles["dtTime"])
                        article_covers = list()
                        images = list()
                        if 'indexPic' in articles and articles["indexPic"]:
                            article_covers.append(articles["indexPic"])
                        if 'originalPic' in articles and articles["originalPic"]:
                            images.append(articles["originalPic"])
                        # 采集视频
                        try:
                            if 'videoPath' in articles.keys():
                                videocovers = list()
                                videocover = articles["picture"]
                                videocovers.append(videocover)
                                videoss = articles["videoPath"]
                                videos = list()
                                videos.append(videoss)
                                article_fields["videos"] = videos
                                article_fields["videocovers"] = videocovers
                                article_type = 4
                        except Exception as e:
                            logging.info(f"此新闻无视频{e}")
                        # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                        article_fields["articlecovers"] = article_covers
                        article_fields["images"] = images
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
                        yield article_fields
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")

    def getarticleparams(self,articleslistsres):
        for article in self.analyze_articlelists(articleslistsres):
            articleid = article.get("workerid")
            url = "http://app.nmgcb.com.cn/chenbao/api/detail/detail"
            headers = {
                "Content-Type": "application/json",
                "Charset": "UTF-8",
                "Accept": "*/*",
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "Host": "app.nmgcb.com.cn"
            }
            data = {
                "id": articleid,
                "navId": article.get('channelID')
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
                worker_id = content_s["data1"]["data"]["id"]
                article_title = content_s["data1"]["data"]["title"]
                author = content_s["data1"]["data"]["author"]
                source = content_s["data1"]["data"]["source"]
                content = content_s["data2"]["data"]["content"]
                images = InitClass().get_images(content)
                fields["images"] = images
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
    appspider = NeiMengGuTouTiao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
