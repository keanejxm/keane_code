"""
解析模板，对app爬虫爬出的页面解析
河北纪委监察网app模板
author:keane
data:2020/10/29
"""
import json
# import time
# import hashlib
import logging

from spiders.libs.spiders.app.initclass import InitClass
from spiders.libs.spiders.app.appspider_m import Appspider


class Heibeijiwei(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://dev.hebnews.cn/jwcms/index.php?"
        headers = {
            'Host': 'dev.hebnews.cn',
            'Connection': 'keep-alive',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 Html'
                          '5Plus/1.0',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': 'acw_tc=7ceef32116039579513747484e2c28db6bf64ab33579b5becbc32b531e',
        }
        data = {
            'm': 'getindata',
            'c': 'index',
            'a': 'get_menus',
            'pcatid': '0',
            'type': '1',
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))
        for channels in channelslists['items']:
            channelid = channels['catid']
            channelname = channels['catname']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    def getarticlelistparams(self, channelsparams):
        articlelistsparams = list()
        channel_data = list()
        url = 'http://dev.hebnews.cn/jwcms/index.php?'
        headers = {
            'Host': 'dev.hebnews.cn',
            'Connection': 'keep-alive',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like G'
                          'ecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 Html5Plus/1.0',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': 'acw_tc=7ceef32116039579513747484e2c28db6bf64ab33579b5becbc32b531e',
        }
        channel_num = 0
        for channelparam in channelsparams:
            channel_num += 1
            data = {
                'm': 'getindata',
                'c': 'index',
                'a': 'lists',
                'size': '10',
                'catid': channelparam.get("channelid"),
                'page': '1',
            }
            method = 'get'
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channelname = channelparam.get("channelname")

            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                       channel_index_id=channel_index_id)
            channel_data.append(channel_field)
            articlelistsparams.append(articlelist_param)
        yield [channel_data, articlelistsparams]

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            articleslists = articleslistres.get("channelres")
            channel_index_id = articleslistres.get("channelindexid")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
            except Exception as e:
                logging.info(f"解析文章列表失败{e}")
            for article in articleslists['items']:
                articleparam = InitClass().article_list_fields()
                articleid = article['id']
                articletitle = article['title']
                imageurl = article['thumbnail']
                articleparam["articleid"] = articleid
                articleparam["articletitle"] = articletitle
                articleparam["imageurl"] = imageurl
                articleparam["channelname"] = channelname
                articleparam["channelindexid"] = channel_index_id
                articlesparams.append(articleparam)
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        for article in articles:
            d = {'学苑': '44', '教育': '33', '视频': '18', '图片': '17', '专题': '16', '纪检人': '15', '警示': '14',
                 '观点': '13',
                 '法规': '12', '党风': '11', '曝光': '10', '巡视': '9', '审查': '8', '新闻': '7'}
            imgurl = article.get("imageurl")
            channelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            channelid = d.get(channelname)
            url = 'http://dev.hebnews.cn/jwcms/index.php?'
            headers = {
                'Host': 'dev.hebnews.cn',
                'Connection': 'keep-alive',
                'Accept': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, li'
                              'ke Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 Html5Plus/1.0',
                'X-Requested-With': 'XMLHttpRequest',
                'Cookie': 'acw_tc=7ceef32116039579513747484e2c28db6bf64ab33579b5becbc32b531e',
            }
            data = {
                'm': 'getindata',
                'c': 'index',
                'a': 'show',
                'catid': channelid,
                'id': article.get("articleid"),
            }
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                             channel_index_id=channel_index_id)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        for article in articleres:
            channnelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            imgurl = article.get("imageurl")
            appname = article.get("appname")
            articlejson = json.loads(
                json.dumps(json.loads(article.get("articleres")), indent=4, ensure_ascii=False))
            fields = InitClass().article_fields()
            url = articlejson["shareHref"]
            workerid = articlejson["id"]
            videos = list()
            video = articlejson["mvideo"]
            videos.append(video)
            fields["appname"] = appname
            fields["url"] = url
            if videos:
                fields["videos"] = videos
            fields["workerid"] = workerid
            try:
                title = articlejson['title']
                fields["title"] = title
            except Exception as e:
                logging.info(f"没有获取到文章标题{e}")
            try:
                pubtime = articlejson['timestamp']
                fields["pubtime"] = InitClass().date_time_stamp(pubtime)
            except Exception as e:
                logging.info(f"没有获取到文章发布时间{e}")
            try:
                source = articlejson['source']
                fields["source"] = source
            except Exception as e:
                logging.info(f"没有获取到文章来源{e}")
            try:
                content = articlejson['content']
                fields["content"] = content
            except Exception as e:
                logging.info(f"没有获取到文章内容{e}")
            try:
                commentnum = articlejson['comments']
                fields["commentnum"] = commentnum
            except Exception as e:
                logging.info(f"没有获取到文章评论数{e}")
            fields["channelname"] = channnelname
            fields["channelindexid"] = channel_index_id
            fields["platformID"] = self.platform_id
            fields["articlecovers"] = [imgurl]
            fields = InitClass().wash_article_data(fields)
            yield {"code": 1, "msg": "OK", "data": {"works": fields}}


def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = Heibeijiwei(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
    appspider = Heibeijiwei(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    appparams = appspider.get_app_params()
    channelsres = appspider.getchannels(appparams.__next__())
    channelsparams = appspider.analyze_channel(channelsres.__next__())
    articlelistparameses = appspider.getarticlelistparams(channelsparams.__next__())
    articlelistparamess = list()
    for articlelistparamesss in articlelistparameses:
        articlelistparamess = articlelistparamesss
    channel_data = articlelistparamess[0]
    channel_flag = 1
    articlelistparames = articlelistparamess[1]
    articleslistsres = appspider.getarticlelists(articlelistparames)
    articles = appspider.analyze_articlelists(articleslistsres.__next__())
    articleparams = appspider.getarticleparams(articles.__next__())
    articlesres = appspider.getarticlehtml(articleparams.__next__())
    app_data = appspider.analyzearticle(articlesres.__next__())
    for data in app_data:
        datas = data["data"]
        if channel_flag:
            datas["channels"] = channel_data
            channel_flag = 0
        yield data

# if __name__ == '__main__':
#     appspider = Heibeijiwei('河北纪检监察网移动端')
#     appspider.run()
