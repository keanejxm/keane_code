"""
解析模板，对app爬虫爬出的页面解析
人民日报app模板
author:keane
data:2020/11/3
"""
import json
# import re 
# import hashlib
# import time
import hashlib
import logging

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


# from lib.crawler.spiders.app.akafkaproduert import Kafkaproducer
class Renminribao(Appspider):

    @staticmethod
    def md5(data):
        ha = hashlib.md5()
        ha.update(data.encode("utf-8"))
        res = ha.hexdigest()
        return res

    @staticmethod
    def get_app_params():
        url = "https://app.peopleapp.com/Api/700/HomeApi/showCategory?"
        headers = {
            'Cookie': 'acw_tc="276082a816043885967987403ed20069be76016a6d4b0270c25278022e1f31";$Path="/";'
                      '$Domain="app.peopleapp.com"; SERVERID=f0c2519d15ca3b0cae13b80f9d03fb94|1604388603|'
                      '1604388596',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR);DailyNewspaper/7.0.2',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'app.peopleapp.com'
        }
        data = {
            'city': '',
            'citycode': '',
            'device': '1b753f6b-8745-3486-a0c0-5c77dedd56d3',
            'device_model': 'MuMu',
            'device_os': 'Android 6.0.1',
            'device_product': 'Netease',
            'device_size': '810*1440',
            'device_type': '1',
            'district': '',
            'fake_id': '56034407',
            'from': '',
            'ids': '234,1,2,114,102,115,229,7,4,5,6,235,9,10,12,13',
            'interface_code': '702',
            'latitude': '',
            'longitude': '',
            'province': '',
            'province_code': '23502043',
            'to': '',
            'version': '7.0.2',
            'securitykey': 'd48822196478d0a6dc5cbbdcfef400e1',
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))
        for channels in channelslists['data']['show_data'] + channelslists['data']['data']:
            channelid = channels['id']
            channelname = channels['name']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelsparams.append(channelparam)
        yield channelsparams

    def getarticlelistparams(self, channelsparams):
        articlelistsparams = []
        channel_data = list()
        channel_num = 0
        url = 'https://app.peopleapp.com/Api/700/HomeApi/getContentList'
        headers = {
            'Cookie': 'acw_tc="2760828c16043651526641766ed1f8d1f586530774309aecff537229bf4755";$Path="/";$Domain="app.p'
                      'eopleapp.com"; SERVERID=0ada8651e904573396f35517addf582c|1604365174|1604365152',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR);DailyNewspaper/7.1.9.1',
            'Host': 'app.peopleapp.com'
        }
        method = 'get'
        for channel in channelsparams:
            channel_num += 1
            data = {
                'category_id': channel.get("channelid"),
                'city': '北京市',
                'citycode': '010',
                'device': '1b753f6b-8745-3486-a0c0-5c77dedd56d3',
                'device_model': 'MuMu',
                'device_os': 'Android 6.0.1',
                'device_product': 'Netease',
                'device_size': '810*1440',
                'device_type': '1',
                'district': '东城区',
                'fake_id': '56034407',
                'id': '0',
                'image_height': '1440',
                'image_wide': '810',
                'interface_code': '702',
                'latitude': '39.908581634349815',
                'longitude': '116.39732329636996',
                'page': '1',
                'province': '北京市',
                'province_code': '24664114',
                'refresh_ids': '6024071,6023465,827,0,6024058,6023937,6023942,6021434,0,6023944,6023935,6023897,6023'
                               '888,6023877,6023878,6023851,6023837,6023577,6023804,rmh14005238,6023768,6023770',
                'refresh_time': '0',
                'show_num': '20',
                'userId': '',
                'user_gov_id': '0',
                'version': '7.0.2'
            }
            n = ''
            for key in data.keys():
                n += data[key] + '|'
            n = n[0:-1] + 'rmrbsecurity$#%sut49fbb427a508bcc'
            securitykey = self.md5(n)
            data['securitykey'] = securitykey
            channelname = channel.get("channelname")
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            channel_data.append(channel_field)
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                       channel_index_id=channel_index_id)
            articlelistsparams.append(articlelist_param)
        yield [channel_data, articlelistsparams]

    def article_lists_data(self, article, channelname, channel_index_id):
        try:
            articleparam = InitClass().article_list_fields()
            if "id" in article and article["id"]:
                articleid = article['id']
                articleparam["articleid"] = articleid
            if "article_title" in article and article["article_title"]:
                articletitle = article['article_title']
                articleparam["articletitle"] = articletitle
            if "share_image" in article and article["share_image"]:
                imageurl = article['share_image']
                articleparam["imageurl"] = imageurl
            if "share_url" in article and article["share_url"]:
                articleurl = article["share_url"]
                articleparam["articleurl"] = articleurl
            if "read_count" in article and article["read_count"]:
                articleparam["readnum"] = article["read_count"]
            if "likes_count" in article and article["likes_count"]:
                articleparam["likenum"] = article["likes_count"]
            if "share_count" in article and article["share_count"]:
                articleparam["sharenum"] = article["share_count"]
            if "comment_count" in article and article["comment_count"]:
                articleparam["commentnum"] = article["comment_count"]
            if "news_type" in article and article["news_type"]:
                article_type1 = article["news_type"]
                article_types = {"cms": "0", "gov": "2"}
                article_type = article_types.get(article_type1)
                if article_type == "null":
                    print(article_type1)
                articleparam["articletype"] = article_type
            if "is_top" in article and article["is_top"]:
                articleparam["banner"] = article["is_top"]
            articleparam["channelname"] = channelname
            articleparam["channelindexid"] = channel_index_id
            return articleparam
        except Exception as e:
            self.logger.info(f"{e}")

    def analyze_articlelists(self, articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channel_index_id = articleslistres.get("channelindexid")
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
            except Exception as e:
                logging.info(f"解析文章列表失败{e}")
            article_list = articleslists['data']
            if "top" in articleslists and articleslists["top"]:
                article_banner = articleslists['top']
                article_list = article_banner + article_list
            for article in article_list:
                if "data" in article and article["data"]:
                    for article in article["data"]:
                        article["is_top"] = 1
                        article_param = self.article_lists_data(article, channelname, channel_index_id)
                        articlesparams.append(article_param)
                else:
                    article_param = self.article_lists_data(article, channelname, channel_index_id)
                    articlesparams.append(article_param)
        yield articlesparams

    def getarticleparams(self, articles):
        articleparams = []
        url = 'https://app.peopleapp.com/Api/700/ArtInfoApi/getArticleData?'
        headers = {
            'Cookie': 'acw_tc="2760828c16043651526641766ed1f8d1f586530774309aecff537229bf4755";$Path="/";$Domain="app.p'
                      'eopleapp.com"; SERVERID=0ada8651e904573396f35517addf582c|1604365174|1604365152',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR);DailyNewspaper/7.1.9.1',
            'Host': 'app.peopleapp.com'
        }
        for article in articles:
            imgurl = article.get("imageurl")
            banners = article.get("banner")
            channelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            articleurl = article.get("articleurl")
            articleid = article.get("articleid")
            articletype = article.get("articletype")
            videourl = article.get("videourl")
            videocover = article.get("videocover")
            readnum = article.get("readnum")
            likenum = article.get("likenum")
            sharenum = article.get("sharenum")
            commentnum = article.get("commentnum")
            try:
                data = {
                    'article_id': article.get("articleid"),
                    'city': '北京市',
                    'citycode': '010',
                    'device': '1b753f6b-8745-3486-a0c0-5c77dedd56d3',
                    'device_model': 'MuMu',
                    'device_os': 'Android 6.0.1',
                    'device_product': 'Netease',
                    'device_size': '810*1440',
                    'device_type': '1',
                    'district': '东城区',
                    'fake_id': '56034407',
                    'interface_code': '702',
                    'latitude': '39.908581634349815',
                    'longitude': '116.39732329636996',
                    'province': '北京市',
                    'province_code': '26090498',
                    'type': articletype,
                    'user_gov_id': '0',
                    'user_id': '0',
                    'version': '7.0.2',
                }
                n = ''
                for key in data.keys():
                    n += data[key] + '|'
                n = n[0:-1] + 'rmrbsecurity$#%sut49fbb427a508bcc'
                securitykey = self.md5(n)
                data['securitykey'] = securitykey
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, channelname, imgurl,
                                                                 articleurl=articleurl, sleeptime=1, data=data,
                                                                 articleid=articleid, videourl=videourl,
                                                                 videocover=videocover, readnum=readnum,
                                                                 likenum=likenum, sharenum=sharenum, banners=banners,
                                                                 commentnum=commentnum,
                                                                 channel_index_id=channel_index_id)
                articleparams.append(articleparam)
            except Exception as e:
                logging.info(f"{e}")
        yield articleparams

    def analyzearticle(self, articleres):
        for article in articleres:
            appname = article.get("appname")
            channelname = article.get("channelname")
            channel_index_id = article.get("channelindexid")
            imgurl = article.get("imageurl")
            articleurl = article.get("articleurl")
            articleid = article.get("articleid")
            videourl = article.get("videourl")
            videocover = article.get("videocover")
            likenum = article.get("likenum")
            readnum = article.get("readnum")
            sharenum = article.get("sharenum")
            banners = article.get("banner")
            fields = InitClass().article_fields()
            fields["appname"] = appname
            fields["banner"] = banners
            fields["platformID"] = self.platform_id
            fields["url"] = articleurl
            fields["workerid"] = articleid
            fields["likenum"] = likenum
            fields["readnum"] = readnum
            fields["sharenum"] = sharenum
            if not videourl:
                videourl = []
            fields["videos"] = videourl
            fields["videocover"] = videocover
            try:
                articlejson = json.loads(article.get("articleres"))
                articlejson = articlejson['frontend']
                if "title_inner" in articlejson and articlejson["title_inner"]:
                    title = articlejson['title_inner']
                    fields["title"] = title
                if "news_datetime" in articlejson and articlejson["news_datetime"]:
                    pubtime = articlejson['news_datetime']
                    fields["pubtime"] = int(pubtime) * 1000
                if "authors" in articlejson and articlejson["authors"]:
                    author = articlejson["authors"]
                    fields["author"] = author
                if "copyfrom" in articlejson and articlejson["copyfrom"]:
                    source = articlejson['copyfrom']
                    fields["source"] = source
                if "contents" in articlejson and articlejson["contents"]:
                    content = articlejson['contents']
                    fields["content"] = content
                if "comment_count" in articlejson and articlejson['comment_count']:
                    commentnum = articlejson['comment_count']
                    fields["commentnum"] = commentnum
                if "read_count" in articlejson and articlejson["read_count"]:
                    readnum = articlejson["read_count"]
                    fields["readnum"] = readnum
                if "love_num" in articlejson and articlejson["love_num"]:
                    likenum = articlejson["love_num"]
                    fields["likenum"] = likenum
                if "content_imgs" in articlejson and articlejson["content_imgs"]:
                    images = list()
                    imagess = articlejson["content_imgs"]
                    for image in imagess:
                        image = image["pic"]
                        images.append(image)
                    fields["images"] = images
                fields["channelname"] = channelname
                fields["channelindexid"] = channel_index_id
                fields["articlecovers"] = [imgurl]
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                self.logger.info(f"{e}")


def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Renminribao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
