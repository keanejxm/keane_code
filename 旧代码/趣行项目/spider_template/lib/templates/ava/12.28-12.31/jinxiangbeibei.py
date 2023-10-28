# -*- encoding:utf-8 -*-
"""
@功能:缙享北碚解析模板
@AUTHOR：Keane
@文件名：jinxiangbeibei.py
@时间：2020/12/17  17:33
"""

import json
import logging

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


class jinxiangbeibei(Appspider):

    # @staticmethod
    # def get_app_params():
    #     url = "http://newsapp-api.cztv.com/portal/api/navigation"
    #     headers = {
    #         "Accept-Language": "zh-CN,zh;q=0.8",
    #         "User-Agent": "blue_news",
    #         "token": "Txnz0J2w2R7umjUY7y8c0FQisdbgKMFqbBTlJfvJi-KHwHdbDAo1sSuUzhEfxeY9vBmOvvcaB1ij9hOD86Gh6r8sQ9cljkGL8dn4eNyaZI5k15pJR98yWutos-V0NiNx5PH7bQdSoDeIva3dF3CWVA0YU_EH7LVnZ6zKSpRScOk",
    #         "appKey": "af729a3805e711eabf1f005056aaca50",
    #         "timestamp": "1608518756285",
    #         "nonce": "a0f6b20fa69f72959d9a97d568cb9c4b",
    #         "sign": "YWM1OGMyZTBkYTdlMTFkMzlkOGQzNGFjMmMzNDExYmMzMmU2YmQ3YQ==",
    #         "terminal": "1",
    #         "clientVersion": "921",
    #         "Host": "newsapp-api.cztv.com",
    #         "Connection": "Keep-Alive",
    #         "Accept-Encoding": "gzip",
    #     }
    #     data = {
    #         "clientVersion": "921",
    #     }
    #     method = "get"
    #     app_params = InitClass().app_params(url, headers, method, data=data)
    #     yield app_params

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
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
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
        for channel in channelsparams:
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
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid=channelid, data=data,
                                                                       channeltype=channeltype)
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
                print(articleslists)
                try:
                    for key,articles_arr in articleslists["data"].items():
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
                        articleparam["articleField"] = article_fields  # 携带文章采集的数据
                        articleparam["articleid"] = article_id
                        articlesparams.append(articleparam)
                if len(articlesparams):
                    aaaa = self.getarticleparams(articlesparams)
                    bbbb = self.getarticlehtml(aaaa.__next__())
                    self.analyzearticle(bbbb.__next__())
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
                    images = InitClass().get_images(content,type=1)
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
                    fields["contentType"] = content_type
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
        # appparams = self.get_app_params()
        # channelsres = self.getchannels(appparams.__next__())
        channelsparams = self.analyze_channel()
        articlelistparames = self.getarticlelistparams(channelsparams.__next__())
        articleslistsres = self.getarticlelists(articlelistparames.__next__())
        articles = self.analyze_articlelists(articleslistsres.__next__())
        articleparams = self.getarticleparams(articles.__next__())
        articlesres = self.getarticlehtml(articleparams.__next__())
        self.analyzearticle(articlesres.__next__())


if __name__ == '__main__':
    appspider = jinxiangbeibei("缙享北碚")
    appspider.run()
