# -*- encoding:utf-8 -*-
"""
@功能:新湖南解析模板
@AUTHOR：Keane
@文件名：xinhunan.py
@时间：2020/12/17  17:33
"""

import json
import logging

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


class Zhilianxiangyang(Appspider):

    @staticmethod
    def get_app_params():
        url = "https://app.api.btime.com/channel/getChannel"
        # 频道请求头
        headers = {
            'Host': 'app.api.btime.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.9.0',

        }
        # 频道数据体
        data = {
            'protocol': '4',
            'push_switch': '1',
            'token': 'e0fb5784410cc184345a22632a803240',
            'carrier': '',
            'push_id': '5766a4b37307c04998dea233dcf9251f',
            'os_type': 'Android',
            'net': 'WIFI',
            'os': 'V417IR release-keys',
            'browse_mode': '1',
            'os_ver': '23',
            'sid': '',
            'location_citycode': 'local_110000',
            'src': 'lx_android',
            'channel': 'xiaomi',
            'ver': '60301',
            'sign': "619a157",
        }
        # 如果携带的是json数据体,用appjson发送
        # app_json = {}
        # 频道请求方式
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        # 如果携带json数据，用下列方式存储发送数据
        # app_params = InitClass().app_params(url, headers, method, data = data ,appjson=app_json)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        channelslists = [
            {'name': '廉政要闻', 'id': '768'},
            {'name': '高层声音', 'id': '730'},
            {'name': '纪律审查', 'id': '732'},
            {'name': '监督曝光', 'id': '733'},
            {'name': '党纪法规', 'id': '737'},
            {'name': '说案明纪', 'id': '740'},
        ]
        for channel in channelslists:
            channelname = channel["name"]
            channelid = channel["id"]
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "http://sjw.vcs88.com/index.php?g=api&m=news&a=get_news_list"
        bannerurl = 'http://sjw.vcs88.com/index.php?g=api&m=ad&a=index'
        bannerheader = {
            'Content-Length': '0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'sjw.vcs88.com',
            'Connection': 'Keep-Alive',
        }
        method = 'post'
        channelname = '廉政要闻'
        articlelist_param_banner = InitClass().articlelists_params_fields(bannerurl, bannerheader, method, channelname,
                                                                   channelid='768', banners=1)
        articlelistsparams.append(articlelist_param_banner)
        headers = {
            'Content-Length': '46',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'sjw.vcs88.com',
            'Connection': 'Keep-Alive',
            'Cookie': 'PHPSESSID=vnt7flv8906ji19s7eju7gmlm4',
            'Cookie2': '$Version=1',
        }
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            data = {
                'page_size':'10',
                'news_classify_id':channelid,
                'page_index':'1'
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
                    for article in articleslists["List"]:
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        article_id = article["id"]
                        if 'title' in article.keys():
                            article_title = article["title"]
                        else:
                            article_title = article["name"]
                        if 'video' in article.keys():
                            video = [article["video"]]
                            article_fields["videos"] = video
                        if 'video_img' in article.keys():
                            videocover = [article["video_img"]]
                            article_fields["videocover"] = videocover
                        article_covers = list()
                        article_cover = article["img"]
                        article_covers.append(article_cover)
                        article_fields["workerid"] = article_id
                        article_fields["channelID"] = channelid
                        article_fields["channelname"] = channelname
                        article_fields["title"] = article_title
                        article_fields["contentType"] = article_cover
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
            url = 'http://sjw.vcs88.com/index.php?g=api&m=news&a=get_news_deatil'
            headers = {
                'Content-Length': '13',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'sjw.vcs88.com',
                'Connection': 'Keep-Alive',
                'Cookie': 'PHPSESSID=gpms5st9od91busev4i12o5dh6',
                'Cookie2': '$Version=1'
            }
            data = {
                'news_id': articleid
            }
            method = 'post'
            articleparam = InitClass().article_params_fields(url, headers, method, data = data,
                                                             article_field = article_field)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            try:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                print(content_s)
                worker_id = content_s["List"][0]["id"]
                article_title = content_s["List"][0]["title"]
                author = content_s["List"][0]['member_name']
                source = content_s["List"][0]["source"]
                content = content_s["List"][0]["content"]
                videos = [content_s["List"][0]['video']]
                videocovers = [content_s["List"][0]['video_img']]
                images = [content_s["List"][0]['img']]
                url = content_s["List"][0]['share_url']
                fields["videos"] = videos
                fields["images"] = images
                fields["videocover"] = videocovers
                fields["appname"] = self.newsname
                fields["title"] = article_title
                fields["workerid"] = worker_id
                fields["content"] = content
                fields["source"] = source
                fields["author"] = author
                fields["url"] = url
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
    appspider = Zhilianxiangyang("智廉襄阳")
    appspider.run()
