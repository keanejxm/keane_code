"""
央视新闻模板
author:keane
data:2020/10/27
updata:
"""
import json

from spiders.libs.spiders.app.appspider_m import Appspider

# import time
from spiders.libs.spiders.app.initclass import InitClass


class Yangshinews(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://m.news.cntv.cn/special/json/fl808/index.json?"
        headers = {
            'Host': 'm.news.cntv.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko'
                          ') Chrome/84.0.4147.125 Safari/537.36'
        }
        data = {
            'app_version': '808'
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(channelsres)
        channelparams = []
        for channel in channelslists['data']:
            channelid = channel['url']
            channelname = channel['title']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)
        yield channelparams

    def getarticlelistparams(self, channelsparams):
        articleparams = []
        channel_data = list()
        channel_num = 0
        for channel in channelsparams:
            channel_num += 1
            url = channel.get("channelid")
            channelname = channel.get("channelname")
            headers = {
                'Cookie': 'cna=wCQYGEBkj1ECAd7f1SJ6XlKY',
                'Host': 'api.cportal.cctv.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                              '/84.0.4147.125 Safari/537.36'
            }
            data = {
                'app_version': '808',
                'app_version': '808',
            }
            method = 'get'
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            channel_data.append(channel_field)
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                       channel_index_id=channel_index_id)
            articleparams.append(articlelist_param)
        yield [channel_data, articleparams]

    @staticmethod
    def analyze_articlelists(articleslist_ress):
        articlesparams = []
        for articleslist_res in articleslist_ress:
            channelname = articleslist_res.get("channelname")
            channel_index_id = articleslist_res.get("channelindexid")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            # articlelistsurl = ''
            try:
                articlelist_json = json.loads(articlelist_res)
                try:
                    if "bigImg" in articlelist_json['data'].keys():
                        articlelists = articlelist_json['data']['bigImg'] + articlelist_json['data']['itemList']
                        # articlelistsurl = articlelist_json['data']['listUrl']
                    else:
                        articlelists = articlelist_json['data']['posterPicList']
                    for article in articlelists:
                        print(article)
                        articleparam = InitClass().article_list_fields()
                        try:
                            articletitle = article['itemTitle']
                        except Exception as e:
                            print(e)
                            articletitle = article['itemInfo']['itemTitle']
                        try:
                            articleid = article['itemID']
                        except Exception as e:
                            print(e)
                            articleid = article['itemInfo']['itemID']
                        try:
                            try:
                                imageurl = article['scrollImage']['imgUrl1']
                                articleparam["imageurl"] = imageurl
                            except Exception as e:
                                print(e)
                                imageurl = article['itemImage']
                                articleparam["imageurl"] = imageurl
                        except Exception as e:
                            print(e)
                            imageurl = article['itemInfo']['itemImage']['imgUrl1']
                            articleparam["imageurl"] = imageurl
                        # print(title,imgurl,articleurl)
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["channelname"] = channelname
                        articleparam["channelindexid"] = channel_index_id
                        articlesparams.append(articleparam)
                except Exception as e:
                    print(e, articlelist_json)
            except Exception as e:
                print(e, articlelist_json)
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articlesparam = []
        url = 'http://api.cportal.cctv.com/api/rest/articleInfo?'
        headers = {
            'Cookie': 'cna=wCQYGEBkj1ECAd7f1SJ6XlKY; sca=191345e6',
            'Host': 'api.cportal.cctv.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.'
                          '0.4147.125 Safari/537.36'
        }
        method = 'get'
        for articleparam in articles:
            data = {
                'id': articleparam.get("articleid"),
                'cb': 'test.setMyArticalContent',
            }
            channelname = articleparam.get("channelname")
            channel_index_id = articleparam.get("channelindexid")
            imgurl = articleparam.get("imageurl")
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                        channel_index_id=channel_index_id)
            articlesparam.append(article)
        yield articlesparam

    def analyzearticle(self,articles_res):
        for articleres in articles_res:
            channelname = articleres.get("channelname")
            channel_index_id = articleres.get("channelindexid")
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["channelindexid"] = channel_index_id
            fields["imageurl"] = imgurl
            fields["appname"] = appname
            fields["platformID"] = self.platform_id
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres[25:-1]), indent=4, ensure_ascii=False))
                title = articlejson['title']  # 标题
                source = articlejson['source']  # 来源
                content = articlejson['content']  # 文章内容
                pubtime = articlejson['pubtime']  # 发布时间
                workerid = articlejson['id']
                url = articlejson["url"]
                fields["title"] = title
                fields["url"] = url
                fields["workerid"] = workerid
                fields["source"] = source
                fields["content"] = content
                fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                fields = InitClass().wash_article_data(fields)
                print(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)


def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = Yangshinews(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
    appspider = Yangshinews(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
