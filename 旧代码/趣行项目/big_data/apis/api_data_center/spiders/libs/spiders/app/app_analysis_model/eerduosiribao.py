# -*- encoding:utf-8 -*-
"""
@功能:新湖南解析模板
@AUTHOR：Keane
@文件名：xinhunan.py
@时间：2020/12/17  17:33
"""

import json
import logging
import bs4
import requests

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class Eerduosi(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://ordosdaily.cn/ordos_jhxt/api.php?s=/Type/getTypeListCache"
        headers = {
            "Host": "ordosdaily.cn",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "User-Agent": "e er duo si ri bao/1.6.7 (iPhone; iOS 14.1; Scale/3.00)",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Length": "15",
            "Connection": "keep-alive",
        }
        data = {
            "siteid": "1",
            "flag": "0"
        }
        method = "post"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelslists = eval(channelsres)
        channellist = channelslists["data"]
        for channel in channellist:
            channelname = channel["cnname"]
            channelid = channel["tid"]
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam
        channelname = "政情"
        channelid = "211"
        channelparam = InitClass().channel_fields(channelid, channelname)
        yield channelparam

    def getarticlelistparams(self, channelsres):
        url = "http://ordosdaily.cn/ordos_jhxt/api.php?s=//News/getNewsListCache"
        headers = {
            "Host": "ordosdaily.cn",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "Cookie": "PHPSESSID=0l83it4r6r5ft0fj9qgfa2odv3",
            "User-Agent": "e er duo si ri bao/1.6.7 (iPhone; iOS 14.1; Scale/3.00)",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Length": "23",
            "Connection": "keep-alive",
        }
        method = 'post'
        channel_num = 0
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            data = {
                "Page": 1,
                "PageSize": 20,
                "device": "0E6E0B84-1D6A-4A58-B720-E716939AC646",
                "flag": 0,
                "siteid": 1,
                "tid": channelid,
                "uid": ""
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
            bannerurl = "http://ordosdaily.cn/ordos_jhxt/api.php?s=/Flash/getFlashCache"
            bannerdata = {
                "flag": 0,
                "siteid": 1,
                "tid": channelid
            }
            banner_param = InitClass().articlelists_params_fields(bannerurl, headers, method, channelname,
                                                                  channelid=channelid, data=bannerdata,
                                                                  channeltype=channeltype, banners=1,
                                                                  channel_index_id=channel_index_id)

            yield channel_field,[articlelist_param,banner_param]

    @staticmethod
    def analyze_articlelists(articleslistsres):
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channel_index_id = articleslistres.get("channelindexid")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            banner = articleslistres.get("banner")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    if banner == 1:
                        try:
                            bannerlist = articleslists["data"]["flash"]
                            for banneritem in bannerlist:
                                articleid = banneritem["nid"]
                                cover = banneritem["imgurl"]
                                covers = list()
                                if cover:
                                    covers.append(cover)
                                article_fields = InitClass().article_fields()
                                articleparam = InitClass().article_list_fields()
                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["channelindexid"] = channel_index_id
                                article_fields["workerid"] = articleid
                                article_fields["banner"] = 1
                                article_fields["articlecovers"] = covers
                                yield article_fields
                        except Exception as e:
                            print("无banner")
                    else:
                        try:
                            # 列表
                            contentlist = articleslists["data"]
                            for article in contentlist:
                                articleid = article["nid"]
                                covers = article["imgs"]
                                rtype = article["rtype"]
                                if rtype == "4":
                                    topic_fields = InitClass().topic_fields()
                                    articleparam = InitClass().article_list_fields()
                                    topic_fields["topicID"] = articleid
                                    topic_fields["channelName"] = channelname
                                    topic_fields["channelindexid"] = channel_index_id
                                    topic_fields["channelID"] = channelid
                                    topic_fields["topicCover"] = covers
                                    topic_fields["topic"] = 1
                                    topic_fields["banner"] = 0
                                    uptime = article["sort_order"]
                                    uptimes = uptime.split(".")
                                    uptime = uptimes[0]
                                    uptime = int(uptime) * 1000
                                    topic_fields["updateTime"] = uptime
                                    topic_fields["createTime"] = 0
                                    topic_fields["pubTime"] = 0
                                    yield topic_fields
                                else:
                                    article_fields = InitClass().article_fields()
                                    articleparam = InitClass().article_list_fields()
                                    article_fields["channelID"] = channelid
                                    article_fields["channelname"] = channelname
                                    article_fields["channelindexid"] = channel_index_id
                                    article_fields["workerid"] = articleid
                                    article_fields["banner"] = 0
                                    article_fields["articlecovers"] = covers
                                    yield article_fields
                        except Exception as e:
                            print("无列表")
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")

    def getarticleparams(self,articleslistsres):
        for article in self.analyze_articlelists(articleslistsres):
            articleid = article.get("workerid")
            topic = article.get("topic")
            if topic == 1:
                url = "http://ordosdaily.cn/ordos_jhxt/api.php?s=//Subject/getSubjectTypes"
                headers = {
                    "Host": "ordosdaily.cn",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "*/*",
                    "Cookie": "PHPSESSID=0l83it4r6r5ft0fj9qgfa2odv3",
                    "User-Agent": "e er duo si ri bao/1.6.7 (iPhone; iOS 14.1; Scale/3.00)",
                    "Accept-Language": "zh-Hans-CN;q=1",
                    "Accept-Encoding": "gzip, deflate",
                    "Content-Length": "14",
                    "Connection": "keep-alive",
                }
                data = {
                    "flag": 0,
                    "sid": articleid
                }
                article["topicUrl"] = url
            else:
                url = "http://ordosdaily.cn/ordos_jhxt/api.php?s=/News/newsinfo"
                headers = {
                    "Host": "ordosdaily.cn",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "*/*",
                    "Cookie": "PHPSESSID=0l83it4r6r5ft0fj9qgfa2odv3",
                    "User-Agent": "e er duo si ri bao/1.6.7 (iPhone; iOS 14.1; Scale/3.00)",
                    "Accept-Language": "zh-Hans-CN;q=1",
                    "Accept-Encoding": "gzip, deflate",
                    "Content-Length": "14",
                    "Connection": "keep-alive",
                }
                data = {
                    "nid": articleid,
                    "uid": ""
                }
            method = 'post'
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
                try:
                    channelid = fields["channelID"]
                    channelname = fields["channelName"]
                    topicid = fields["topicID"]
                    topicdetail = content_s["data"]
                    topictitle = topicdetail["title"]
                    fields["title"] = topictitle
                    topiccolumns = topicdetail["columns"]
                    topicnum = 0
                    newestarticleid = ""
                    newestarticleuptime = 0
                    for section in topiccolumns:
                        cid = section["cid"]
                        surl = "http://ordosdaily.cn/ordos_jhxt/api.php?s=/Subject/getColumnNews"
                        sdata = {
                            "Page": 0,
                            "PageSize": 20,
                            "cid": cid,
                            "flag": 0
                        }
                        sheader = {
                            "Host": "ordosdaily.cn",
                            "Content-Type": "application/x-www-form-urlencoded",
                            "Accept": "*/*",
                            "Cookie": "PHPSESSID=0l83it4r6r5ft0fj9qgfa2odv3",
                            "User-Agent": "e er duo si ri bao/1.6.7 (iPhone; iOS 14.1; Scale/3.00)",
                            "Accept-Language": "zh-Hans-CN;q=1",
                            "Accept-Encoding": "gzip, deflate",
                            "Content-Length": "14",
                            "Connection": "keep-alive",
                        }

                        sres = requests.post(surl, headers=sheader, data=sdata).text
                        sectionlist = json.loads(
                            json.dumps(json.loads(sres, strict=False), indent=4, ensure_ascii=False))
                        # print("sectionlist==",sectionlist)
                        for item in sectionlist["data"]:
                            topicnum += 1
                            articleid = item["nid"]
                            articletitle = item["title"]
                            source = item["copyfrom"]
                            uptime = item["sort_order"]
                            uptimes = uptime.split(".")
                            uptime = uptimes[0]
                            uptime = int(uptime) * 1000
                            if uptime > newestarticleuptime:
                                newestarticleuptime = uptime
                                newestarticleid = articleid
                            comnum = item["comcount"]
                            covers = item["imgs"]
                            articleurl = item["newsurl"]
                            article_fields = InitClass().article_fields()
                            article_fields["appname"] = self.newsname
                            article_fields["platformID"] = self.platform_id
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["url"] = articleurl
                            article_fields["workerid"] = articleid
                            article_fields["title"] = articletitle
                            article_fields["banner"] = 0
                            article_fields["articlecovers"] = covers
                            article_fields["updatetime"] = uptime
                            article_fields["pubtime"] = 0
                            article_fields["createtime"] = 0
                            article_fields["source"] = source
                            article_fields["commentnum"] = comnum
                            article_fields["specialtopic"] = 1
                            article_fields["topicid"] = topicid
                            article_fields["topicTitle"] = topictitle
                            try:
                                res = requests.get(articleurl)
                                res.encoding = 'utf8'
                                bf = bs4.BeautifulSoup(res.text, 'html.parser')
                                content = bf.find('div', id='aritcleContent').decode()
                                article_fields["content"] = content
                                try:
                                    videos = InitClass().get_video(content)
                                    article_fields["videos"] = videos
                                except Exception as e:
                                    print("无视频")
                                try:
                                    images = InitClass().get_images(content)
                                    article_fields["images"] = images
                                except Exception as e:
                                    print("无图片")
                            except Exception as e:
                                print("无html格式正文")
                            article_fields["videocover"] = []
                            yield {"code": 1, "msg": "OK", "data": {"works": article_fields}}
                    fields["articleNum"] = topicnum
                    fields["newestArticleID"] = newestarticleid
                    fields["platformName"] = self.newsname
                except Exception as e:
                    num += 1
                    logging.info(f"错误数量{num},{e}")

            else:
                # 普通
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                    detail = content_s["data"]
                    articletitle = detail["title"]
                    source = detail["copyfrom"]
                    uptime = detail["sort_order"]
                    uptimes = uptime.split(".")
                    uptime = uptimes[0]
                    uptime = int(uptime) * 1000
                    url = detail["newsurl"]
                    comnum = detail["comcount"]
                    readnum = detail["viewnum"]
                    likenum = detail["praisenum"]
                    fields["title"] = articletitle
                    fields["source"] = source
                    fields["commentnum"] = comnum
                    fields["readnum"] = readnum
                    fields["likenum"] = likenum
                    fields["url"] = url
                    fields["appname"] = self.newsname
                    fields["paltformID"] = self.platform_id
                    fields["pubtime"] = 0
                    fields["createtime"] = 0
                    fields["updatetime"] = uptime

                    try:
                        # 请求newsurl 获取正文
                        res = requests.get(url)
                        res.encoding = 'utf8'
                        bf = bs4.BeautifulSoup(res.text, 'html.parser')
                        content = bf.find('div', id='aritcleContent').decode()
                        fields["content"] = content

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

                    except Exception as e:
                        print("无html格式正文")

                    fields["videocover"] = []
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
                except Exception as e:
                    num += 1
                    logging.info(f"错误数量{num},{e}")

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Eerduosi(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
