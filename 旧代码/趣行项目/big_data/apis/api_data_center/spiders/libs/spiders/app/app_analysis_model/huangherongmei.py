# -*- encoding:utf-8 -*-
"""
@功能:黄河融媒解析模板
@AUTHOR：Keane
@文件名：huangherongmei.py
@时间：2020/12/23  19:58
"""
import json
import logging
import re

from lxml import etree
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class HuangHeRongMei(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://hwcb.jnetdata.com//jnetcms/sy/index"
        headers = {
            "Connection": "close",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Content-Length": "34",
            "Host": "hwcb.jnetdata.com",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.10.0",
        }
        app_json = "machineid=ZjM0NTUyNzgzNTNjMmI3Mw=="
        method = "get"
        app_params = InitClass().app_params(url, headers, method, appjson = app_json)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        for channellists in channelslists["result"]:
            channel_name = channellists["name"]
            channel_id = channellists["chnlId"]
            channel_url = channellists["url"]
            channel_child = channellists["child"]
            if channel_child:
                for channel in channel_child:
                    child_id = channel_id + "-" + channel["chnlId"]
                    child_name = channel_name + "-" + channel["name"]
                    child_url = channel["url"]
                    channelparam = InitClass().channel_fields(child_id, child_name, channel_url = child_url)
                    channelsparams.append(channelparam)
            else:
                channelparam = InitClass().channel_fields(channel_id, channel_name, channel_url = channel_url)
                channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        bannel_url = "http://hwcb.jnetdata.com/jnetcms/sy/yw/tpxw/index"
        headers = {
            "Host": "hwcb.jnetdata.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.10.0",
            "If-Modified-Since": "Wed, 23 Dec 2020 12:46:39 GMT"
        }
        method = "get"
        articlelist_param = InitClass().articlelists_params_fields(bannel_url, headers, method, "独家", channelid = 78,
                                                                   banners = 1)
        articlelistsparams.append(articlelist_param)
        for channel in channelsparams:
            channel_url = channel.get("channelUrl")
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            channel_json = "pageSize=MTA=&pageNo=MQ==&machineid=ZjM0NTUyNzgzNTNjMmI3Mw=="
            method = "post"
            articlelist_param = InitClass().articlelists_params_fields(channel_url, headers, method, channelname,
                                                                       channelid = channelid, data = channel_json,
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
            banners = articleslistres.get("banner")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent = 4, ensure_ascii = False))
                print(articleslists)
                try:
                    for articles in articleslists["result"]:
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        # 获取文章列表内的有用信息
                        article_id = articles["id"]
                        article_title = articles["doctitle"]
                        share_url = articles["linkUrl"]
                        pubtime = articles["doctime"]
                        if pubtime:
                            pubtime = InitClass().date_time_stamp(pubtime)
                        article_cover = [articles["imgUrl"]]
                        article_fields["articlecovers"] = article_cover
                        # 采集视频
                        try:
                            videos = [articles["videoUrl"]]
                            article_fields["videos"] = videos
                        except Exception as e:
                            logging.info(f"此新闻无视频{e}")
                        # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                        article_fields["channelID"] = channelid
                        article_fields["channelname"] = channelname
                        article_fields["channeltype"] = channel_type
                        article_fields["workerid"] = article_id
                        article_fields["title"] = article_title
                        article_fields["url"] = share_url
                        article_fields["pubtime"] = pubtime
                        article_fields["banner"] = banners
                        # 将请求文章必需信息存入
                        articleparam["articleField"] = article_fields  # 携带文章采集的数据
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
            article_field = article.get("articleField")
            article_id = article_field.get("workerid")
            article_url = article_field.get("url")
            headers = {
                "Host": "hwcb.jnetdata.com",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,en-US;q=0.8",
                "Cookie": "__FT10000028=2020-12-24-9-4-30; __NRU10000028=1608771870982; __RT10000028=2020-12-24-9-4-30",
                "X-Requested-With": "com.future.huangwei",
            }
            method = 'get'
            articleparam = InitClass().article_params_fields(article_url, headers, method,
                                                             article_field = article_field)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            article_res = article.get("articleres")
            fields["appname"] = self.newsname
            # print(article_res.encode("ISO-8859-1").decode("utf8"))
            article_res = article_res.encode("ISO-8859-1").decode("utf8")
            html = etree.HTML(article_res)
            content = html.xpath("//div[@class= 'content-txt']")
            imagess = html.xpath("//img/@src")
            if imagess:
                images = list()
                for image in imagess:
                    image = "http://hwcb.jnetdata.com/sy/hy/gqotblt"+re.findall(r"\.(.*?)",image)[0]
                    images.append(image)
                fields["images"] = images

            try:
                content = list(map(lambda x: etree.tostring(x, encoding="unicode").strip(), content))[0]
                fields["content"] = str(content)
            except Exception as e:
                self.logger.info(f"正则抓取标题为空或title获取规则改变{e}")
            try:
                title = re.findall("var __\$title=(.*?);", article_res)[0]
                fields["title"] = title
            except Exception as e:
                self.logger.info(f"正则抓取标题为空或title获取规则改变{e}")
            try:
                author = re.findall("var __\$AuthorPh=(.*?);", article_res)[0]
                fields["author"] = author
            except Exception as e:
                self.logger.info(f"正则抓取作者为空或author获取规则改变{e}")
            try:
                editor = re.findall("var __\$Editor=(.*?);", article_res)[0]
                fields["editor"] = editor
            except Exception as e:
                self.logger.info(f"正则抓取编辑为空或editor获取规则改变{e}")
            try:
                pub_time = re.findall("var __\$pubtime=(.*?);", article_res)[0]
                fields["pubtime"] = InitClass().date_time_stamp(pub_time)
            except Exception as e:
                self.logger.info(f"正则抓取发布时间为空或pubtime获取规则改变{e}")
            try:
                source = re.findall("var __\$source=(.*?);", article_res)[0]
                fields["source"] = source
            except Exception as e:
                self.logger.info(f"正则抓取文章来源为空或source获取规则改变{e}")
            print(json.dumps(fields, indent = 4, ensure_ascii = False))

def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = HuangHeRongMei(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    appparams = appspider.get_app_params()
    channelsres = appspider.getchannel(appparams.__next__())
    channelsparams = appspider.analyze_channel(channelsres.__next__())
    articlelistparameses = appspider.getarticlelistparams(channelsparams.__next__())
    articlelistparamess = list()
    for articlelistparamesss in articlelistparameses:
        articlelistparamess = articlelistparamesss
    channel_data = articlelistparamess[0]
    articlelistparames = articlelistparamess[1]
    articleslistsres = appspider.getarticlelists(articlelistparames)
    articles = appspider.analyze_articlelists(articleslistsres.__next__())
    articleparams = appspider.getarticleparams(articles.__next__())
    articlesres = appspider.getarticlehtml(articleparams.__next__())
    app_data = appspider.analyzearticle(articlesres.__next__())
    article_retu = {
        "code": "1",
        "msg": "json",
        "data": dict(),
    }
    data_dict = dict()
    data_dict["channels"] = channel_data
    articles_list = list()
    topics_list = list()
    for data in app_data:
        if "works" in data["data"]:
            articles_list.append(data["data"]["works"])
        elif "topic" in data["data"]:
            topics_list.append(data["data"]["topic"])
        else:
            pass
    article_retu["data"]["topics"] = topics_list
    article_retu["data"]["worksList"] = articles_list
    yield article_retu


def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = HuangHeRongMei(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    appparams = appspider.get_app_params()
    channelsres = appspider.getchannels(appparams.__next__())
    channelsparams = appspider.analyze_channel(channelsres.__next__())
    articlelistparameses = appspider.getarticlelistparams(channelsparams.__next__())
    articlelistparamess = list()
    for articlelistparamesss in articlelistparameses:
        articlelistparamess = articlelistparamesss
    channel_data = articlelistparamess[0]
    articlelistparames = articlelistparamess[1]
    articleslistsres = appspider.getarticlelists(articlelistparames)
    articles = appspider.analyze_articlelists(articleslistsres.__next__())
    articleparams = appspider.getarticleparams(articles.__next__())
    articlesres = appspider.getarticlehtml(articleparams.__next__())
    app_data = appspider.analyzearticle(articlesres.__next__())
    for data in app_data:
        channel = {"code": 1, "msg": "OK", "data": {"channel": channel_data}}
        yield {"data": data, "channels": channel}
