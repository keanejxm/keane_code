# -*- encoding:utf-8 -*-
"""
@功能:新湖南解析模板
@AUTHOR：Keane
@文件名：xinhunan.py
@时间：2020/12/17  17:33
"""

import json
import logging
import re
from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


class jixiangChangShun(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://apiparty.xinhuaapp.com/Service/IndexSvr.svc/GetNavigation"
        headers = {
            'Cookie': 'token=11750aa4c10f47353803a60d688639bfe1b4c583e03c530fa02d33955546f858aeaf735f6de78516ca6f9e64a7a0a930491dbbbfa82c77ea0cea2ac0fc9a92431609220566459',
            'token': '11750aa4c10f47353803a60d688639bfe1b4c583e03c530fa02d33955546f858aeaf735f6de78516ca6f9e64a7a0a930491dbbbfa82c77ea0cea2ac0fc9a92431609220566459',
            'Host': 'apiparty.xinhuaapp.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.11.0',
        }
        data = {
            'styleId': '649',
            'appId': '110168',
            'appKey': 'd3031',
            'projectId': '13',
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        for channel in channelslists["Data"]['Fixeds']:
            if channel["Id"] != 119128:
                channelname = channel["Title"]
                channelid = channel["Id"]
                channelparam = InitClass().channel_fields(channelid, channelname)
                channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        headers = {
            'Cookie': 'token=11750aa4c10f47353803a60d688639bfe1b4c583e03c530fa02d33955546f858aeaf735f6de78516ca6f9e64a7a0a930491dbbbfa82c77ea0cea2ac0fc9a92431609220566459',
            'token': '11750aa4c10f47353803a60d688639bfe1b4c583e03c530fa02d33955546f858aeaf735f6de78516ca6f9e64a7a0a930491dbbbfa82c77ea0cea2ac0fc9a92431609220566459',
            'Host': 'apiparty.xinhuaapp.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.11.0',
        }
        method = 'get'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            if channelsparams.index(channel) == 0:
                url = "http://apiparty.xinhuaapp.com/Service/IndexSvr.svc/GetIndexPage"
                data = {
                    'modilarId':channelid,
                    'pageNo':'1',
                    'styleId':'649',
                    'appId':'110168',
                    'appKey':'d3031',
                    'projectId':'13',
                }
            else:
                url = 'http://apiparty.xinhuaapp.com/Service/ContentSvr.svc/GetContentList'
                data = {
                    'modilarId':channelid,
                    'pageNo':'1',
                    'appId':'110168',
                    'appKey':'d3031',
                    'projectId':'13',
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
                    if 'Focus' in articleslists['Data']:
                        #banner
                        for article in articleslists["Data"]['Focus']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article["Id"]
                            article_title = article["Title"]
                            article_type = article['ContentType']
                            share_url = article['ShareUrl']
                            pubtime = article['IssueTime'][6:19]
                            article_covers = list()
                            article_cover = article['ImgUrl']
                            article_covers.append(article_cover)
                            videos = [article['VodUrl']]
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channeltype"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["contentType"] = article_type
                            article_fields["url"] = share_url
                            article_fields["pubtime"] = pubtime
                            article_fields["articlecovers"] = article_covers
                            article_fields["videos"] = videos
                            article_fields["banner"] = 1
                            # 将请求文章必需信息存入
                            articleparam["articleField"] = article_fields  # 携带文章采集的数据
                            articleparam["articleid"] = article_id
                            articlesparams.append(articleparam)
                    if 'IndexContent' in articleslists['Data']:
                        for article in articleslists["Data"]['IndexContent']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article["Id"]
                            article_title = article["Title"]
                            article_type = article['ContentType']
                            share_url = article['ShareUrl']
                            if 'Authors' in article.keys():
                                author = article['Authors']
                            else:
                                author = ''
                            pubtime = article['IssueTime'][6:19]
                            article_covers = list()
                            article_cover = article['ImgUrl']
                            article_covers.append(article_cover)
                            videos = [article['VodUrl']]
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channeltype"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["contentType"] = article_type
                            article_fields["url"] = share_url
                            article_fields["author"] = author
                            article_fields["pubtime"] = pubtime
                            article_fields["articlecovers"] = article_covers
                            article_fields["videos"] = videos
                            # 将请求文章必需信息存入
                            articleparam["articleField"] = article_fields  # 携带文章采集的数据
                            articleparam["articleid"] = article_id
                            articlesparams.append(articleparam)
                    if 'Rolling' in articleslists['Data']:
                        for article in articleslists["Data"]['Rolling']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            article_id = article["Id"]
                            article_title = article["Title"]
                            article_type = article['ContentType']
                            share_url = article['ShareUrl']
                            pubtime = article['IssueTime'][6:19]
                            article_covers = list()
                            article_cover = article['ImgUrl']
                            article_covers.append(article_cover)
                            if 'Authors' in article.keys():
                                author = article['Authors']
                            else:
                                author = ''
                            videos = [article['VodUrl']]
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channeltype"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["contentType"] = article_type
                            article_fields["url"] = share_url
                            article_fields["pubtime"] = pubtime
                            article_fields["articlecovers"] = article_covers
                            article_fields["videos"] = videos
                            article_fields["author"] = author
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
            str = article_field['url'].rsplit('/', 1)[-1]
            id = str.rsplit('.', 1)[0]
            if article_field['banner'] != 1:
                url = "http://api.cportal.cctv.com/api/rest/articleInfo"
                headers = {
                    'Host': 'api.cportal.cctv.com',
                    'Connection': 'keep-alive',
                    'Pragma': 'no-cache',
                    'Cache-Control': 'no-cache',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 xyApp',
                    'Accept': '*/*',
                    'Referer': 'http://app.cctv.com/special/cportal/detail/arti/index.html?id=Arti69Rk8eHdDTcfyGI9BuUb201221&fromapp=cctvnews&version=727',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,en-US;q=0.8',
                    'Cookie': 'cna=8MNxGEM+7mUCAd7f1SLaj7uj; sca=46a6820c; atpsida=0a007a0e8fa091019f27b276_1609226207_5',
                    'X-Requested-With': 'net.xinhuamm.d3031',
                }
                data = {
                    'id':id,
                    'cb':'test.setMyArticalContent'
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
            try:
                str = article.get("articleres").replace('test.setMyArticalContent(', '')
                res = str.replace('})', '}')
                content_s = json.loads(
                    json.dumps(json.loads(res, strict = False), indent = 4, ensure_ascii = False))
                if 'content' in content_s.keys():
                    worker_id = content_s["id"]
                    article_title = content_s["title"]
                    author = fields['author']
                    source = content_s['source']
                    content = content_s["content"]
                    images = InitClass.get_images(content)
                    videos = InitClass.get_video(content)
                    fields["appname"] = self.newsname
                    fields["title"] = article_title
                    fields["images"] = images
                    fields["videos"] = videos
                    fields["workerid"] = worker_id
                    fields["content"] = content
                    fields["source"] = source
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
    appspider = jixiangChangShun("吉祥长顺")
    appspider.run()
