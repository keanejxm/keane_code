# -*- encoding:utf-8 -*-
"""
@功能:中国蓝解析模板
@AUTHOR：Keane
@文件名：ZhongGuoLan.py
@时间：2020/12/17  17:33
"""

import json
import logging

from appspider_m import Appspider
from initclass import InitClass


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
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        navList = [
            {
                'channelid': '4b8408b015d70ec4',
                'channelname': '政务号',
                'categoryname': '/api/getGovernmentHotspot?uuid=4b8408b015d70ec4',
            },
            {
                'channelid': '139',
                'channelname': '在看',
                'categoryname': '/api/getShortVideo?id=139',
            }
        ]
        channelslists = json.loads(channelsres)
        channelparams = []
        for channel in channelslists['data']['newsNodes']:
            channelid = channel['id']
            channelname = channel['title']
            categoryname = channel['url']
            if channelname == '蓝媒号':
                channelid = '4b8408b015d70ec4'
                categoryname = '/api/bmHot?uuid=4b8408b015d70ec4'
            channelparam = InitClass().channel_fields(channelid, channelname, categoryname = categoryname)
            channelparams.append(channelparam)
        channelparams = channelparams + navList
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        print(channelsparams)
        articlelistsparams = []
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
        for channel in channelsparams:
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
            method = 'get'
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
                            article_fields["channeltype"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["contentType"] = article_type
                            article_fields["url"] = share_url
                            # 将请求文章必需信息存入
                            articleparam["articleField"] = article_fields  # 携带文章采集的数据
                            articleparam["articleid"] = article_id
                            articlesparams.append(articleparam)
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
                                    articlesparams.append(articleparam)
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

                                    # 采集视频
                                    # try:
                                    #     videocovers = list()
                                    #     videocover = articles["video"]["cover"]
                                    #     videocovers.append(videocover)
                                    #     videoss = articles["video"]["data"]
                                    #     videos = list()
                                    #     for video in videoss:
                                    #         videos.append(video["url"])
                                    #     article_fields["videos"] = videos
                                    #     article_fields["videocovers"] = videocovers
                                    # except Exception as e:
                                    #     logging.info(f"此新闻无视频{e}")
                                    # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                                    article_fields["articlecovers"] = article_covers
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
            topic = article_field.get("topic")
            channelname = article_field.get("channelname")

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
            articleparam = InitClass().article_params_fields(url, headers, method, data = data,
                                                             article_field = article_field)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        print(articleres)
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            topic = fields.get("topic")
            channelname = article.get("channelname")
            channelid = article.get("channelid")
            channel_type = article.get("channeltype")
            if topic:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
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
                        # 采集视频
                        # try:
                        #     videocovers = list()
                        #     videocover = articles["video"]["cover"]
                        #     videocovers.append(videocover)
                        #     videoss = articles["video"]["data"]
                        #     videos = list()
                        #     for video in videoss:
                        #         videos.append(video["url"])
                        #     article_fields["videos"] = videos
                        #     article_fields["videocovers"] = videocovers
                        # except Exception as e:
                        #     logging.info(f"此新闻无视频{e}")
                        # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
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
                bbbb= self.getarticlehtml(aaaa.__next__())
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
                    fields["url"] = url
                    fields["title"] = article_title
                    fields["workerid"] = worker_id
                    fields["content"] = content
                    fields["source"] = source
                    fields["author"] = author
                    print(json.dumps(fields, indent=4, ensure_ascii=False))
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
                    print(json.dumps(fields, indent=4, ensure_ascii=False))
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
    appspider = ZhongGuoLan("中国蓝")
    appspider.run()
