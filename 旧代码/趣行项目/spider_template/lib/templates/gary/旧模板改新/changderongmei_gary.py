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
from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


class XinHuNan(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://manager.hncdrm.com/api/Article/GetAPPArticleCateList"
        headers = {
            'Content-Type': 'application/json',
            'X-token': 'Mytoken',
            'AppName': 'cdrm',
            'AppType': '0#2.0.7',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': 'manager.hncdrm.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'Cookie': 'acw_tc=2f6a1fd416088788145361527e4cac4615c224afb19253ea8fe53fdccee66b',
            'Content-Length': '89',
        }
        data = {"pageIndex":1,"pageSize":100,"ShowAddressType":1,"IsHidden":0,"IsPart":-1,"CateName":""}
        method = "post"
        app_params = InitClass().app_params(url, headers, method, appjson = data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))
        for channel in channelslists['ResultValue']['rows']:
            channelname = channel['CateName']
            channelid = channel["Id"]
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "http://manager.hncdrm.com/api/Article/GetArticleAPPList"
        headers = {
            'Content-Type': 'application/json',
            'X-token': 'Mytoken',
            'AppName': 'cdrm',
            'AppType': '0#2.0.7',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': 'manager.hncdrm.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'Cookie': 'acw_tc=2f6a1fd416088788145361527e4cac4615c224afb19253ea8fe53fdccee66b',
            'Content-Length': '89',
        }
        method = 'post'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            data = {"IsSlideShow":0,"CateLinkId":channelid,"BusinessType":1,"IsGangGao":1,"PlatType":0,"IsHidden":-1,"AppVersion":"11","PageIndex":1,"PageSize":20}

            banner_data = {"CateLinkId": channelid, "BusinessType": 1, "IsGangGao": 0, "IsSlideShow": 1, "IsHidden": -1,
                           "PageIndex": 1, "PageSize": 5}
            articlelist_param_banner = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                              channelid=channelid,
                                                                              channeljson=banner_data,
                                                                              channeltype='', banners=1)
            articlelistsparams.append(articlelist_param_banner)
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid = channelid, channeljson = data,
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
                    if 'ResultValue' in articleslists.keys():
                        for article in articleslists['ResultValue']['rows']:
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()
                            topic_fields = InitClass().topic_fields()
                            article_id = article["Id"]
                            article_title = article['NewsTitle']
                            article_type = article['ListShowType']
                            share_url = article['LinkUrl']
                            pubtime = InitClass().date_time_stamp(article['CreateDate'])
                            article_covers = list()
                            article_cover = article['LitPic']
                            article_covers.append(article_cover)
                            if article['ListShowType']==10 or (article['ListShowType']==1 and article['LinkUrl']!=''):
                                topic_fields["channelName"] = channelname
                                topic_fields["channelID"] = channelid
                                topic_fields["channeltype"] = channel_type
                                topic_fields["topicID"] = article_id
                                topic_fields["_id"] = article_id
                                topic_fields["contentType"] = article_type
                                topic_fields["topicUrl"] = share_url
                                topic_fields["pubtime"] = pubtime
                                topic_fields["topic"] = 1
                                # 将请求文章必需信息存入
                                articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)
                            else:
                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["channeltype"] = channel_type
                                article_fields["workerid"] = article_id
                                article_fields["title"] = article_title
                                article_fields["contentType"] = article_type
                                article_fields["url"] = share_url
                                article_fields["pubtime"] = pubtime
                                article_fields["banner"] = 1
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
                url = "http://manager.hncdrm.com/api/Article/GetAPPArticleById"
                headers = {
                    'Content-Type': 'application/json',
                    'X-token': 'Mytoken',
                    'AppName': 'cdrm',
                    'AppType': '0#2.0.7',
                    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
                    'Host': 'manager.hncdrm.com',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                    'Cookie': 'UM_distinctid=17698d460741f5-0911b53f17029d-6617061e-64140-17698d460752e8; CNZZDATA1278588593=2016685-1608881824-%7C1608881824; acw_tc=2f6a1fe516088843784853701e1252302047ad3fe1668ba85618afed59496c',
                }
                data = {
                    "id": articleid
                }
            else:
                url = "http://manager.hncdrm.com/api/Article/GetAPPArticleById"
                headers = {
                    'Content-Type': 'application/json',
                    'X-token': 'Mytoken',
                    'AppName': 'cdrm',
                    'AppType': '0#2.0.7',
                    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
                    'Host': 'manager.hncdrm.com',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                    'Cookie': 'acw_tc=2f6a1fa416088813902323336e75e543cbdb50fbc461d44260e7642eab5280; UM_distinctid=17698d460741f5-0911b53f17029d-6617061e-64140-17698d460752e8; CNZZDATA1278588593=2016685-1608881824-%7C1608881824'
                }
                data = {
                    "id": articleid
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
            topic = fields.get("topic")
            if topic:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                articlesparams =[]
                if 'ResultValue' in content_s.keys():
                    try:
                        if content_s["ResultValue"]['NewsList']:
                            for articles_arr in content_s["ResultValue"]['NewsList']:
                                for articles in articles_arr['NewsList']:
                                    article_fields = InitClass().article_fields()
                                    articleparam = InitClass().article_list_fields()
                                    # 获取文章列表内的有用信息
                                    article_id = articles["Id"]
                                    article_title = articles['NewsTitle']
                                    article_type = articles["ListShowType"]
                                    share_url = articles['LinkUrl']
                                    article_covers = [articles['LitPic']]
                                    if "videoUrl" in articles.keys():
                                        videos = [articles ['videoUrl']]
                                    else:
                                        videos = []
                                    article_fields["videos"] = videos
                                    article_fields["channelID"] = articles['Id']
                                    article_fields["videocovers"] = article_covers
                                    article_fields["channelname"] = fields.get("channelName")
                                    article_fields["channeltype"] = article_type
                                    article_fields["workerid"] = article_id
                                    article_fields["title"] = article_title
                                    article_fields["contentType"] = article_type
                                    article_fields["url"] = share_url
                                    article_fields["specialtopic"] = topic
                                    article_fields["topicid"] = fields.get('_id')
                                    articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                    articleparam["articleid"] = article_id
                                    articlesparams.append(articleparam)
                    except Exception as e:
                        print(e)
                    aaaa = self.getarticleparams(articlesparams)
                    bbbb = self.getarticlehtml(aaaa.__next__())
                    self.analyzearticle(bbbb.__next__())
            else:
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict = False), indent = 4, ensure_ascii = False))
                    if content_s['ResultValue']:
                        worker_id = content_s['ResultValue']["Id"]
                        article_title = content_s["ResultValue"]['NewsTitle']
                        author = content_s["ResultValue"]['Writer']
                        source = content_s["ResultValue"]["Source"]
                        pubtime = InitClass().date_time_stamp(content_s["ResultValue"]['PubDate'])
                        if 'ArtContent' in content_s["ResultValue"].keys() and content_s["ResultValue"]['ArtContent']!='':
                            content = content_s["ResultValue"]['ArtContent']
                        else:
                            res = requests.get(content_s["ResultValue"]['LinkUrl'])
                            res.encoding = res.apparent_encoding
                            html = res.text
                            bf = bs4.BeautifulSoup(html, 'html.parser')
                            content = str(bf.find('div', class_='text_con_left'))
                        comment_num = content_s["ResultValue"]['Comment']
                        hit_num = content_s["ResultValue"]["Click"]  # 点击数
                        like_num = content_s["ResultValue"]["Zan"]
                        videos = [content_s["ResultValue"]["Video"]]
                        videocovers = [content_s["ResultValue"]["VideoPic"]]
                        fields["videos"] = videos
                        fields["videocovers"] = videocovers
                        images = [content_s['ResultValue']['LitPic']]
                        fields["images"] = images
                        fields["appname"] = self.newsname
                        fields["title"] = article_title
                        fields["workerid"] = worker_id
                        fields["content"] = content
                        fields["source"] = source
                        fields["pubtime"] = pubtime
                        fields["commentnum"] = comment_num
                        fields["readnum"] = hit_num
                        fields["author"] = author
                        fields["likenum"] = like_num
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
    appspider = XinHuNan("常德融媒")
    appspider.run()
