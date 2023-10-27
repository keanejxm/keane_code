# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
import bs4
import requests
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class Xinchongqingnews(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        url = "https://api.cqliving.com/getRecommedAppsAll.html"
        headers = {
            "Cookie": "PORSESSIONID = 9379BEB63D23B9AC37050502EC975CCA",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Content-Length": "61",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1;MuMu Build / V417IR)",
            "Host": "api.cqliving.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        data = {
            "v": "1",
            "appId": "1",
            "sessionId": "23154ab474cc44869b3d8cc49d325abb",
            "token": "",
        }
        method = "post"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyzechannels(channelsres):
        """
        此方法主要获取channelid,channelname即可
        若请求文章列表页需要channeltype，categoryname，categoryid,则以categoryname= categoryname形式传递参数
        :param channelsres:
        :return:
        """
        navList = [
            {
                'id': 851,
                'name': '头条'
            },
            {
                'id': 7104,
                'name': '推荐'
            },
            {
                'id': 852,
                'name': '区县'
            },
            {
                'id': 2190,
                'name': '鸣家'
            },
            # {
            #     'id': 4010,
            #     'name': '渝中'
            # },
            {
                'id': 889,
                'name': '图库'
            },
            {
                'id': 10008,
                'name': '战疫'
            },
            {
                'id': 849,
                'name': '云端'
            },
            {
                'id': 4062,
                'name': '智汇八方'
            },
            {
                'id': 878,
                'name': '教育'
            },
            {
                'id': 879,
                'name': '文艺'
            },
            {
                'id': 876,
                'name': '房产'
            },
            {
                'id': 873,
                'name': '财经'
            },
            {
                'id': 854,
                'name': '生活'
            },
            {
                'id': 7115,
                'name': '健康'
            },
            {
                'id': 7114,
                'name': '旅游'
            },
            {
                'id': 7117,
                'name': '汽车'
            },
            {
                'id': 10057,
                'name': '政法'
            },
            {
                'id': 856,
                'name': '时政'
            },
            # {
            #     'id': 2115,
            #     'name': '专题'
            # },
            {
                'id': 2046,
                'name': '原创'
            },
            {
                'id': 10123,
                'name': '应急'
            },
            {
                'id': 6100,
                'name': '视听'
            }
        ]
        channelslists = json.loads(channelsres)
        for channel in navList+channelslists['data']['dataList']:
            channelid = channel['id'] if "id" in channel else channel['columnsId']
            channelname = channel['name'] if "name" in channel else channel['location']
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam

    def getarticlelistparams(self,channelsres):
        """
        此方法目的是组建请求文章列页面数据参数，url，headers，data，若以json形式发送数据，则channeljson = channeljson
        :param channelsparams:
        :return:
        """
        channel_num = 0
        for channel in self.analyzechannels(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            if channelname == '推荐':
                url = "https://api.cqliving.com/information/recommend/getIndexList.html"
                headers = {
                    "Cookie": "PORSESSIONID = 9379BEB63D23B9AC37050502EC975CCA",
                    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                    "Content-Length": "42",
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1;MuMu Build / V417IR)",
                    "Host": "api.cqliving.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                data = {
                    "v": "3.1",
                    "appId": "1",
                    "columnId": channelid,
                    "token": "",
                    "lastId": "",
                }
            elif channelname == '鸣家':
                url = "https://api.cqliving.com/mj/columnInfos.html"
                headers = {
                    "Cookie": "PORSESSIONID=9379BEB63D23B9AC37050502EC975CCA",
                    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                    "Content-Length": "106",
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1;MuMu Build / V417IR)",
                    "Host": "api.cqliving.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                data = {
                    "lastSortNo": "",
                    "v": "1",
                    "token": "",
                    "appId": "1",
                    "sessionId": "23154ab474cc44869b3d8cc49d325abb",
                    "lastOnlineTime": "",
                    "place": "mc",
                    "lastId": "",
                }
            else:
                url = "https://api.cqliving.com/newsV2.html"
                headers = {
                    "Cookie": "PORSESSIONID=9379BEB63D23B9AC37050502EC975CCA",
                    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                    "Content-Length": "153",
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1;MuMu Build / V417IR)",
                    "Host": "api.cqliving.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                data = {
                    "appId": "1",
                    "v": "5",
                    "isCarousel": "true",
                    "columnId": channelid,
                    "businessValue": "",
                    "unionValue": "",
                    "lastId": "",
                    "lastSortNo": "",
                    "lastOnlineTime": "",
                    "sessionId": "23154ab474cc44869b3d8cc49d325abb",
                    "token": "",
                }
            method = 'post'
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                        data=data,channel_index_id=channel_index_id,
                                                                       channeltype=channeltype)
            yield channel_field,[articlelist_param]

    @staticmethod
    def analyze_articlelists(articleslist_ress):
        """
        解析文章列表页，目的是为了获取文章具体信息，组建请求文章详情数据体
        :param articleslist_ress:
        :return:
        """
        for articleslist_res in articleslist_ress:
            banners = articleslist_res.get("banner")
            channelname = articleslist_res.get("channelname")
            channel_index_id = articleslist_res.get("channelindexid")
            channelid = articleslist_res.get("channelID")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                try:
                    if channelname == '推荐':
                        articlelists = articlelist_json['data']
                        for articleArr in articlelists:
                            for article in articleArr['object']:
                                if 'type' in article.keys() and article['type'] == 0:
                                    if 'infoLabel' in article.keys() and article['infoLabel'] == ',活动,':
                                        articleid = article['id']
                                    else:
                                        articleparam = InitClass().article_list_fields()
                                        articletitle = article['title']
                                        articleid = article['id']
                                        articleurl = article["url"]
                                        if 'infoSource' in article:
                                            source = article["infoSource"]
                                            articleparam["source"] = source  # 此步骤为存储文章来源
                                        if 'nickname' in article:
                                            author = article["nickname"]
                                            articleparam["author"] = author  # 此步骤为存储作者
                                        pubtime = article["onlineTime"]
                                        articleparam["pubtime"] = pubtime
                                        if 'contentUrl' in article.keys():
                                            find1 = '.m3u8'
                                            if find1 in article['contentUrl']:
                                                videos = list()
                                                videos.append(article['contentUrl'])
                                                articleparam["videos"] = videos
                                        try:
                                            articleparam["imageurl"] = []
                                            if article['images'] != '':
                                                img = article['images'].split(',')
                                                articleparam["imageurl"] = img
                                                find1 = '.m3u8'
                                                if 'contentUrl' in article.keys() and (find1 in article['contentUrl']):
                                                    videocover = img
                                                    articleparam["videocover"] = videocover
                                        except Exception as e:
                                            print(e)
                                        articleparam["channelID"] = channelid
                                        articleparam["articleid"] = articleid
                                        articleparam["articletitle"] = articletitle
                                        articleparam["channelname"] = channelname
                                        articleparam["channelindexid"] = channel_index_id
                                        articleparam["banner"] = banners
                                        articleparam["articleurl"] = articleurl
                                        yield articleparam
                    elif channelname == '鸣家':
                        articlelists = articlelist_json['data']['dataList']
                        for article in articlelists:
                            # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                            if 'type' in article.keys() and article['type'] == 0:
                                if 'infoLabel' in article.keys() and article['infoLabel'] == ',活动,':
                                    articleid = article['id']
                                else:
                                    articleparam = InitClass().article_list_fields()
                                    articletitle = article['title']
                                    articleid = article['id']
                                    articleurl = article["url"]
                                    if 'infoSource' in article:
                                        source = article["infoSource"]
                                        articleparam["source"] = source  # 此步骤为存储文章来源
                                    if 'nickname' in article:
                                        author = article["nickname"]
                                        articleparam["author"] = author  # 此步骤为存储作者
                                    pubtime = article["onlineTime"]
                                    articleparam["pubtime"] = pubtime
                                    if 'contentUrl' in article.keys():
                                        find1 = '.m3u8'
                                        if find1 in article['contentUrl']:
                                            videos = list()
                                            videos.append(article['contentUrl'])
                                            articleparam["videos"] = videos
                                    try:
                                        articleparam["imageurl"] = []
                                        if article['images'] != '':
                                            img = article['images'].split(',')
                                            articleparam["imageurl"] = img
                                            find1 = '.m3u8'
                                            if 'contentUrl' in article.keys() and (find1 in article['contentUrl']):
                                                videocover = img
                                                articleparam["videocover"] = videocover
                                    except Exception as e:
                                        print(e)
                                    articleparam["channelID"] = channelid
                                    articleparam["articleid"] = articleid
                                    articleparam["articletitle"] = articletitle
                                    articleparam["channelname"] = channelname
                                    articleparam["channelindexid"] = channel_index_id
                                    articleparam["banner"] = banners
                                    articleparam["articleurl"] = articleurl
                                    yield articleparam
                    else:
                        articlelists = articlelist_json['data']['news']
                        for article in articlelists:
                            if 'type' in article.keys() and article['type'] == 0:
                                if 'infoLabel' in article.keys() and article['infoLabel'] == ',活动,':
                                    articleid = article['id']
                                else:
                                    articleparam = InitClass().article_list_fields()
                                    articletitle = article['title']
                                    articleid = article['id']
                                    articleurl = article["url"]
                                    if 'infoSource' in article:
                                        source = article["infoSource"]
                                        articleparam["source"] = source  # 此步骤为存储文章来源
                                    if 'nickname' in article:
                                        author = article["nickname"]
                                        articleparam["author"] = author  # 此步骤为存储作者
                                    pubtime = article["onlineTime"]
                                    articleparam["pubtime"] = pubtime
                                    if 'contentUrl' in article.keys():
                                        find1 = '.m3u8'
                                        if find1 in article['contentUrl']:
                                            videos = list()
                                            videos.append(article['contentUrl'])
                                            articleparam["videos"] = videos
                                    try:
                                        articleparam["imageurl"] = []
                                        if article['images'] != '':
                                            img = article['images'].split(',')
                                            articleparam["imageurl"] = img
                                            find1 = '.m3u8'
                                            if 'contentUrl' in article.keys() and (find1 in article['contentUrl']):
                                                videocover = img
                                                articleparam["videocover"] = videocover
                                    except Exception as e:
                                        print(e)
                                    articleparam["channelID"] = channelid
                                    articleparam["articleid"] = articleid
                                    articleparam["articletitle"] = articletitle
                                    articleparam["channelname"] = channelname
                                    articleparam["channelindexid"] = channel_index_id
                                    articleparam["banner"] = banners
                                    articleparam["articleurl"] = articleurl
                                    yield articleparam
                        if 'carousels' in articlelist_json['data'].keys():
                            articlelists = articlelist_json['data']['carousels']
                            for article in articlelists:
                                if 'type' in article.keys() and article['type'] == 0:
                                    if 'infoLabel' in article.keys() and article['infoLabel'] == ',活动,':
                                        articleid = article['id']
                                    else:
                                        articleparam = InitClass().article_list_fields()
                                        articletitle = article['title']
                                        articleid = article['id']
                                        articleurl = article["url"]
                                        if 'infoSource' in article:
                                            source = article["infoSource"]
                                            articleparam["source"] = source  # 此步骤为存储文章来源
                                        if 'nickname' in article:
                                            author = article["nickname"]
                                            articleparam["author"] = author  # 此步骤为存储作者
                                        pubtime = article["onlineTime"]
                                        articleparam["pubtime"] = pubtime
                                        if 'contentUrl' in article.keys():
                                            find1 = '.m3u8'
                                            if find1 in article['contentUrl']:
                                                videos = list()
                                                videos.append(article['contentUrl'])
                                                articleparam["videos"] = videos
                                        try:
                                            articleparam["imageurl"] = []
                                            if article['images'] != '':
                                                img = article['images'].split(',')
                                                articleparam["imageurl"] = img
                                                find1 = '.m3u8'
                                                if 'contentUrl' in article.keys() and (find1 in article['contentUrl']):
                                                    videocover = img
                                                    articleparam["videocover"] = videocover
                                        except Exception as e:
                                            print(e)
                                        banners = 0
                                        articleparam["channelID"] = channelid
                                        articleparam["articleid"] = articleid
                                        articleparam["articletitle"] = articletitle
                                        articleparam["channelname"] = channelname
                                        articleparam["channelindexid"] = channel_index_id
                                        articleparam["banner"] = banners
                                        articleparam["articleurl"] = articleurl
                                        yield articleparam
                except Exception as e:
                    print(e, articlelist_json)
            except Exception as e:
                print(e, articlelist_json)

    def getarticleparams(self,articleslist_ress):
        """
        组建请求文章详情所需要的数据体
        :param articles:
        :return:
        """
        articlesparam = []
        url = 'https://api.cqliving.com/getBusinessDetail.html'
        headers = {
            "Cookie": "PORSESSIONID=9379BEB63D23B9AC37050502EC975CCA",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Content-Length": "87",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1;MuMu Build / V417IR)",
            "Host": "api.cqliving.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        method = 'post'
        for articleparam in self.analyze_articlelists(articleslist_ress):
            data = {
                'appId': '1',
                'sourceId': articleparam.get("articleid"),
                'sourceType': '1',
                'sessionId': '23154ab474cc44869b3d8cc49d325abb',
                'token': ''
            }
            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
            channel_index_id = articleparam.get("channelindexid")
            banner = articleparam.get("banner")
            imgurl = articleparam.get("imageurl")
            videos = articleparam.get("videos")
            videocover = articleparam.get("videocover")
            pubtime = articleparam.get("pubtime")
            createtime = articleparam.get("createtime")
            updatetime = articleparam.get("updatetime")
            source = articleparam.get("source")
            author = articleparam.get("author")
            likenum = articleparam.get("likenum")
            commentnum = articleparam.get("commentnum")
            sharenum = articleparam.get("sharenum")
            readnum = articleparam.get("readnum")
            articleurl = articleparam.get("articleurl")
            articleid = articleparam.get("articleid")
            # 若APP有关于时间的反爬加sleeptime = 1，若发送为json数据体，则添加articlejson = articlejson
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                        articleid=articleid, videourl=videos, videocover=videocover,
                                                        pubtime=pubtime,
                                                        createtime=createtime, updatetime=updatetime,
                                                        source=source, author=author, likenum=likenum,
                                                        commentnum=commentnum, sharenum=sharenum, readnum=readnum,
                                                        articleurl=articleurl, banners=banner, sleeptime=1,
                                                        channel_index_id=channel_index_id)
            yield [article]

    def analyzearticle(self,articles_res):
        for articleres in articles_res:
            channelname = articleres.get("channelname")
            channel_index_id = articleres.get("channelindexid")
            channelid = articleres.get("channelID")
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            banners = articleres.get("banner")
            # 若上面存储了此字段需用下列方式获取
            videos = articleres.get("videourl")
            videocover = articleres.get("videocover")
            pubtime = articleres.get("pubtime")
            source = articleres.get("source")
            author = articleres.get("author")
            articleurl = articleres.get("articleurl")
            workerid = articleres.get("articleid")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["workerid"] = workerid
            fields["channelname"] = channelname
            fields["platformID"] = self.platform_id
            fields["channelindexid"] = channel_index_id
            fields["images"] = imgurl
            fields["articlecovers"] = imgurl
            fields["banner"] = banners
            # 如果有下列字段需添加
            fields["url"] = articleurl  # 文章的html网址，提取shareurl
            fields["videos"] = videos  # 文章的视频链接地址
            fields["videocover"] = videocover  # 文章的视频封面地址
            fields["source"] = source  # 文章的来源
            fields["pubtime"] = InitClass().date_time_stamp(pubtime)
            fields["author"] = author  # 文章作者
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                res = requests.get(articleurl)
                res.encoding = res.apparent_encoding
                html = res.text
                bf = bs4.BeautifulSoup(html, 'html.parser')
                content = bf.find('div', class_='detail_content')
                content = str(content)
                videoContent = bf.find('div', class_='topVideo')
                videoContent = str(videoContent)
                videos = InitClass().get_video(videoContent)
                images = InitClass().get_images(content)
                fields["images"] = images  # 文章评论数
                if len(videos):
                    fields["videos"] = videos  # 文章的视频链接地址
                    fields["videocover"] = imgurl  # 文章的视频封面地址
                likenum = articlejson['data']['praiseCount']
                commentnum = articlejson['data']['replyCount']
                title = articlejson['data']['detailTitle']
                fields["commentnum"] = commentnum  # 文章评论数
                fields["appname"] = appname
                fields["content"] = content
                fields["likenum"] = likenum
                fields["title"] = title
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Xinchongqingnews(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
