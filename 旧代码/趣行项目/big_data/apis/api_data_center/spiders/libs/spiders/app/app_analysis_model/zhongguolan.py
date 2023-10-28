# -*- encoding:utf-8 -*-
"""
@功能:中国蓝解析模板
@AUTHOR：Keane
@文件名：ZhongGuoLan.py
@时间：2020/12/17  17:33
"""

import json
import logging

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class ZhongGuoLan(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://newsapp-api.cztv.com/portal/api/navigation"
        headers = {
            "Accept-Language": "zh-CN,zh;q=0.8",
            "User-Agent": "blue_news",
            "token": "Txnz0J2w2R7umjUY7y8c0FQisdbgKMFqbBTlJfvJi-KHwHdbDAo1sSuUzhEfxeY9vBmOvvcaB1ij9hOD86Gh6r8sQ9cljkGL8dn4eNyaZI5k15pJR98yWutos-V0NiNx5PH7bQdSoDeIva3dF3CWVA0YU_EH7LVnZ6zKSpRScOk",
            "appKey": "af729a3805e711eabf1f005056aaca50",
            "timestamp": "1608518756285",
            "nonce": "a0f6b20fa69f72959d9a97d568cb9c4b",
            "sign": "YWM1OGMyZTBkYTdlMTFkMzlkOGQzNGFjMmMzNDExYmMzMmU2YmQ3YQ==",
            "terminal": "1",
            "clientVersion": "921",
            "Host": "newsapp-api.cztv.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        data = {
            "clientVersion": "921",
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(channelsres)
        for channel in channelslists['data']['newsNodes']:
            channelid = channel['id']
            channelname = channel['title']
            categoryname = channel['url']
            if channelname == '蓝媒号':
                channelid = '4b8408b015d70ec4'
                categoryname = '/api/bmHot?uuid=4b8408b015d70ec4'
            channelparam = InitClass().channel_fields(channelid, channelname, categoryname=categoryname)
            yield channelparam

    def getarticlelistparams(self, channelsres):
        headers = {
            "Accept-Language": "zh-CN,zh;q=0.8",
            "User-Agent": "blue_news",
            "token": "Txnz0J2w2R7umjUY7y8c0FQisdbgKMFqbBTlJfvJi-KHwHdbDAo1sSuUzhEfxeY9vBmOvvcaB1ij9hOD86Gh6r8sQ9cljkGL8dn4eNyaZI5k15pJR98yWutos-V0NiNx5PH7bQdSoDeIva3dF3CWVA0YU_EH7LVnZ6zKSpRScOk",
            "appKey": "af729a3805e711eabf1f005056aaca50",
            "timestamp": "1608521841424",
            "nonce": "7afe3347c5fee2fbc37dee58a85214bd",
            "sign": "NTgxY2IyNTAyYzM0ZDg2YjYzOGY5NmNiYTIwMjgyNDZiZDIzYjBhOA==",
            "terminal": "1",
            "clientVersion": "921",
            "Host": "newsapp-api.cztv.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        channel_num = 0
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")
            categoryname = channel.get("categoryname")
            url = f"http://newsapp-api.cztv.com/portal/{categoryname}"
            if channelname == '头条':
                data = {
                    "id": channelid,
                    "pageSize": "10",
                    "clientVersion": "921",
                    "pubId": "",
                    "pageNum": "1"
                }
            elif channelname == '推荐':
                data = {
                    "id": channelid,
                    "clientVersion": "921",
                    "pubId": "",
                    "pageNum": "1"
                }
            elif channelname == '直播':
                data = {
                    "pageNum": "1",
                    "clientVersion": "921",
                    "pageSize": "10"
                }
            elif channelname == '热评':
                data = {
                    "id": channelid,
                    "pageSize": "10",
                    "clientVersion": "921",
                    "pubId": "",
                    "pageNum": "1"
                }
            elif channelname == '在看':
                data = {
                    "id": channelid,
                    "clientVersion": "921",
                    "pageNum": "1"
                }
            elif channelname == '蓝媒号':
                data = {
                    "clientVersion": "921",
                    "uuid": channelid
                }
            elif channelname == '政务号':
                data = {
                    "clientVersion": "921",
                    "uuid": channelid,
                    "pageNum": "1"
                }
            else:
                continue
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
                if channelname == '直播':
                    try:
                        for articles in articleslists["data"]["moduleList"][3]['nodeList']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            # 获取文章列表内的有用信息
                            article_id = articles["pubId"]
                            article_title = articles["newsTitle"]
                            article_type = articles["newsType"]
                            share_url = f'http://wap.cztv.com/live/+{articles["broadcastId"]}/{articles["pubId"]}.html'
                            article_covers = list()
                            for img in articles["newsImage"]:
                                article_covers.append(img['url'])
                            article_fields["articlecovers"] = article_covers
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channelindexid"] = channel_index_id
                            article_fields["channeltype"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["contentType"] = article_type
                            article_fields["url"] = share_url
                            yield article_fields
                            # 将请求文章必需信息存入
                    except Exception as e:
                        logging.info(f"提取文章列表信息失败{e}")
                else:
                    try:
                        for articles_arr in articleslists["data"]["nodeList"]:
                            for articles in articles_arr['contents']:
                                article_type = articles["newsType"]
                                if article_type == '4':
                                    # 这种类型为专题
                                    print(articles)
                                    topic_fields = InitClass().topic_fields()
                                    articleparam = InitClass().article_list_fields()
                                    # 获取文章列表内的有用信息
                                    article_id = articles["newsDetailUrl"]
                                    article_title = articles["title"]
                                    article_type = articles["newsType"]
                                    share_url = articles['shareInfo']["shareUrl"]
                                    pubtime = InitClass().date_time_stamp(articles["publishTime"])
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
                                    article_id = articles["newsDetailUrl"]
                                    article_title = articles["title"]
                                    article_type = articles["newsType"]
                                    share_url = articles['shareInfo']["shareUrl"]
                                    pubtime = InitClass().date_time_stamp(articles["publishTime"])
                                    article_covers = list()
                                    for img in articles["images"]:
                                        article_covers.append(img['url'])
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
            articleid = article.get("articleid")
            topic = article.get("topic")
            channelname = article.get("channelname")
            if channelname == '直播':
                url = f"http://newsapp-api.cztv.com/portal/api/broadcastDetail?userId=&pubId={articleid}&clientVersion=921&uuid=4b8408b015d70ec4"
                headers = {
                    "Accept-Language": "zh-CN,zh;q=0.8",
                    "User-Agent": "blue_news",
                    "token": "Txnz0J2w2R7umjUY7y8c0FQisdbgKMFqbBTlJfvJi-KHwHdbDAo1sSuUzhEfxeY9vBmOvvcaB1ij9hOD86Gh6r8sQ9cljkGL8dn4eNyaZI5k15pJR98yWutos-V0NiNx5PH7bQdSoDeIva3dF3CWVA0YU_EH7LVnZ6zKSpRScOk",
                    "appKey": "af729a3805e711eabf1f005056aaca50",
                    "timestamp": "1608530198285",
                    "nonce": "f43382242e8bcfb4ce0a7f502ab10418",
                    "sign": "NDhlNGRiZDI2NmU5NTNlODQxZmMzNjBkODRkODZlZjE5MmIzZGYwZQ==",
                    "terminal": "1",
                    "clientVersion": "921",
                    "Host": "newsapp-api.cztv.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                data = {}
            elif topic == 1:
                articleid = article.get("topicID")
                url = f"http://newsapp-api.cztv.com/portal{articleid}&clientVersion=921"
                headers = {
                    "Accept-Language": "zh-CN,zh;q=0.8",
                    "User-Agent": "blue_news",
                    "token": "Txnz0J2w2R7umjUY7y8c0FQisdbgKMFqbBTlJfvJi-KHwHdbDAo1sSuUzhEfxeY9vBmOvvcaB1ij9hOD86Gh6r8sQ9cljkGL8dn4eNyaZI5k15pJR98yWutos-V0NiNx5PH7bQdSoDeIva3dF3CWVA0YU_EH7LVnZ6zKSpRScOk",
                    "appKey": "af729a3805e711eabf1f005056aaca50",
                    "timestamp": "1608530198285",
                    "nonce": "f43382242e8bcfb4ce0a7f502ab10418",
                    "sign": "NDhlNGRiZDI2NmU5NTNlODQxZmMzNjBkODRkODZlZjE5MmIzZGYwZQ==terminal:1",
                    "clientVersion": "921",
                    "Host": "newsapp-api.cztv.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                data = {}
            else:
                url = f"http://newsapp-api.cztv.com/portal{articleid}?clientVersion=921"
                headers = {
                    "Accept-Language": "zh-CN,zh;q=0.8",
                    "User-Agent": "blue_news",
                    "token": "Txnz0J2w2R7umjUY7y8c0FQisdbgKMFqbBTlJfvJi-KHwHdbDAo1sSuUzhEfxeY9vBmOvvcaB1ij9hOD86Gh6r8sQ9cljkGL8dn4eNyaZI5k15pJR98yWutos-V0NiNx5PH7bQdSoDeIva3dF3CWVA0YU_EH7LVnZ6zKSpRScOk",
                    "appKey": "af729a3805e711eabf1f005056aaca50",
                    "timestamp": "1608532301014",
                    "nonce": "35818fa5c1a55b2153f57362c7b827f1",
                    "sign": "YWZlOTJiYTdiYTAzZmRjNzE0MDlmZGFiMDFjYjlhMTBhMGNlNDI4OQ==",
                    "terminal": "1",
                    "clientVersion": "921",
                    "Host": "newsapp-api.cztv.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",

                }
                data = {}
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                             article_field=article)
            yield [articleparam]

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            topic = fields.get("topic")
            channelname = article.get("channelname")
            channelid = article.get("channelid")
            channel_type = article.get("channeltype")
            print(article.get("articleres"))
            if topic:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                print(content_s)
                articlesparams = []
                for articles_arr in content_s["data"]["nodeList"]:
                    for articles in articles_arr['contents']:
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        # 获取文章列表内的有用信息
                        article_id = articles["newsDetailUrl"]
                        article_title = articles["title"]
                        article_type = articles["newsType"]
                        share_url = articles['shareInfo']["shareUrl"]
                        pubtime = InitClass().date_time_stamp(articles["publishTime"])
                        article_covers = list()
                        for img in articles["images"]:
                            article_covers.append(img)
                        article_fields["articlecovers"] = article_covers
                        article_fields["channelID"] = channelid
                        article_fields["channelname"] = fields.get("channelName")
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
            elif channelname == '直播':
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                    print(content_s)
                    worker_id = content_s["data"]['liveNewsDetail']["pubId"]
                    article_title = content_s["data"]['liveNewsDetail']["title"]
                    author = content_s["data"]['liveNewsDetail']["author"]
                    source = content_s["data"]['liveNewsDetail']["sharePretext"]
                    content = ''
                    url = content_s["data"]['liveNewsDetail']['shareUrl']
                    try:
                        videocovers = list()
                        videos = list()
                        videoss = content_s["data"]['moreLinesList']
                        for video in videoss:
                            videocover = video["images"][0]['url']
                            videocovers.append(videocover)
                            videos.append(video['playbackUrl'][1]["url"])
                        fields["videos"] = videos
                        fields["videocover"] = videocovers
                    except Exception as e:
                        logging.info(f"此新闻无视频{e}")
                    try:
                        imagess = content_s["data"]["images"]
                        images = list()
                        for image in imagess:
                            images.append(image["url"])
                        fields["images"] = images
                    except Exception as e:
                        self.logger.info(f"获取文章内图片失败{e}")
                    fields["appname"] = self.newsname
                    fields["platformID"] = self.platform_id
                    fields["url"] = url
                    fields["title"] = article_title
                    fields["workerid"] = worker_id
                    fields["content"] = content
                    fields["source"] = source
                    fields["author"] = author
                    fields = InitClass().wash_article_data(fields)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
                except Exception as e:
                    num += 1
                    logging.info(f"直播类错误数量{num},{e}")
            else:
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                    print(content_s)
                    worker_id = content_s["data"]["id"]
                    article_title = content_s["data"]["title"]
                    author = content_s["data"]["author"]
                    source = content_s["data"]["source"]
                    content = content_s["data"]["htmlText"]
                    try:
                        videocovers = list()
                        videos = list()
                        videoss = content_s["data"]["videos"]
                        for video in videoss:
                            videocover = video["videoThumbnail"]
                            videocovers.append(videocover)
                            videos.append(video['videoPath'][1]["url"])
                        if len(videos) > 0:
                            fields["videos"] = videos
                            fields["videocover"] = videocovers
                        else:
                            print(content)
                            videoss = InitClass().get_video(content)
                            fields["videos"] = videoss
                            fields["videocover"] = videocovers
                    except Exception as e:
                        logging.info(f"此新闻无视频{e}")
                    try:
                        imagess = InitClass().get_images(content)
                        fields["images"] = imagess
                    except Exception as e:
                        self.logger.info(f"获取文章内图片失败{e}")
                    fields["appname"] = self.newsname
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
    appspider = ZhongGuoLan(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
