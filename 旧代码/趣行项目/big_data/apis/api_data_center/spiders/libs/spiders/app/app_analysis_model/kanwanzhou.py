# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class Kanwanzhounews(Appspider):

    @staticmethod
    def analyzechannels():
        """
        此方法主要获取channelid,channelname即可
        若请求文章列表页需要channeltype，categoryname，categoryid,则以categoryname= categoryname形式传递参数
        :param channelsres:
        :return:
        """
        navList = [
            {
                "id": 1664,
                "name": "快讯",
            },
            {
                'id': 1581,
                'name': '推荐'
            },
            {
                'id': 1602,
                'name': '时政'
            },
            {
                'id': 2223,
                'name': '城际'
            },
            {
                'id': 1676,
                'name': '橘视频'
            }
        ]
        for channel in navList:
            channelid = channel['id']
            channelname = channel['name']
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam

    def getarticlelistparams(self):
        """
        此方法目的是组建请求文章列页面数据参数，url，headers，data，若以json形式发送数据，则channeljson = channeljson
        :param channelsparams:
        :return:
        """
        channel_num = 0
        for channel in self.analyzechannels():
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            url = "https://api.cqliving.com/newsV2.html"
            headers = {
                "Cookie": "PORSESSIONID=69FE704B9873F179DF0A22659ABA1F8A",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                "Content-Length": "155",
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
                "Host": "api.cqliving.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip"

            }
            if channelname == '快讯':
                data = {
                    'lastSortNo': '',
                    'v': '4',
                    'appId': '28',
                    'columnId': channelid,
                    'lastId': '',
                    'isCarousel': 'false',
                    'sessionId': '6bb900da9e6848fdbc579bd8b9e7c6b6',
                    'token': ''
                }
            else:
                data = {
                    "appId": "28",
                    "isCarousel": "true",
                    "columnId": channelid,
                    "v": "4",
                    "businessValue": "",
                    "unionValue": "",
                    "lastId": "",
                    "lastSortNo": "",
                    "lastOnlineTime": "",
                    "sessionId": "6bb900da9e6848fdbc579bd8b9e7c6b6",
                    "token": ""
                }
            method = 'post'
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                       channel_index_id=channel_index_id)
            yield channel_field, [articlelist_param]

    @staticmethod
    def analyze_articlelists(articleslist_ress):
        """
        解析文章列表页，目的是为了获取文章具体信息，组建请求文章详情数据体
        :param articleslist_ress:
        :return:
        """
        for articleslist_res in articleslist_ress:
            banners = articleslist_res.get("banner")
            channelid = articleslist_res.get("channelID")
            channelname = articleslist_res.get("channelname")
            channel_index_id = articleslist_res.get("channelindexid")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                try:
                    articlelists = articlelist_json['data']['news']
                    for article in articlelists:
                        if 'type' in article.keys() and article['type'] == 0:
                            if 'infoLabel' in article.keys() and article['infoLabel'] == ',活动,':
                                articleid = article['id']
                            else:
                                find2 = '.mp4'
                                if channelname == '橘视频':
                                    if find2 in article['contentUrl'] or article['contentUrl'] == '':
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
                                            find1 = '.mp4'
                                            if find1 in article['contentUrl']:
                                                videos = list()
                                                videos.append(article['contentUrl'])
                                                articleparam["videos"] = videos
                                        try:
                                            articleparam["imageurl"] = []
                                            if article['images'] != '':
                                                img = article['images'].split(',')
                                                articleparam["imageurl"] = img
                                                find1 = '.mp4'
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
                                        find1 = '.mp4'
                                        if find1 in article['contentUrl']:
                                            videos = list()
                                            videos.append(article['contentUrl'])
                                            articleparam["videos"] = videos
                                    try:
                                        articleparam["imageurl"] = []
                                        if article['images'] != '':
                                            img = article['images'].split(',')
                                            articleparam["imageurl"] = img
                                            find1 = '.mp4'
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
                                    find2 = '.mp4'
                                    if channelname == '橘视频':
                                        if find2 in article['contentUrl'] or article['contentUrl'] == '':
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
                                                find1 = '.mp4'
                                                if find1 in article['contentUrl']:
                                                    videos = list()
                                                    videos.append(article['contentUrl'])
                                                    articleparam["videos"] = videos
                                            try:
                                                articleparam["imageurl"] = []
                                                if article['images'] != '':
                                                    img = article['images'].split(',')
                                                    articleparam["imageurl"] = img
                                                    find1 = '.mp4'
                                                    if 'contentUrl' in article.keys() and (
                                                            find1 in article['contentUrl']):
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
                                        else:
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
                                            find1 = '.mp4'
                                            if find1 in article['contentUrl']:
                                                videos = list()
                                                videos.append(article['contentUrl'])
                                                articleparam["videos"] = videos
                                        try:
                                            articleparam["imageurl"] = []
                                            if article['images'] != '':
                                                img = article['images'].split(',')
                                                articleparam["imageurl"] = img
                                                find1 = '.mp4'
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
        url = 'https://exapi.cqliving.com/infoDetailNew.html'
        headers = {
            "Host": "exapi.cqliving.com",
            "Connection": "keep-alive",
            "Content-Length": "22",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://share.cqliving.com",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 CQ_XHL(5042;Android;28;6bb900da9e6848fdbc579bd8b9e7c6b6;;0)",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://share.cqliving.com/news-detail-pages/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,en-US;q=0.8",
            "X-Requested-With": "com.yaoyu.wanzhou",
        }
        method = 'post'
        for articleparam in self.analyze_articlelists(articleslist_ress):
            data = {
                'infoClassifyId': articleparam.get("articleid"),
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
            # 若APP有关于时间的反爬加sleeptime = 1，若发送为json数据体，则添加articlejson = articlejson
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                        videourl=videos, videocover=videocover, pubtime=pubtime,
                                                        createtime=createtime, updatetime=updatetime,
                                                        source=source, author=author, likenum=likenum,
                                                        commentnum=commentnum, sharenum=sharenum, readnum=readnum,
                                                        articleurl=articleurl, banners=banner,
                                                        channel_index_id=channel_index_id)
            yield [article]

    def analyzearticle(self,articles_res):
        for articleres in articles_res:
            channelname = articleres.get("channelname")
            channel_index_id = articleres.get("channelindexid")
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
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["channelindexid"] = channel_index_id
            fields["images"] = imgurl
            fields["articlecovers"] = [imgurl]
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
                content = articlejson['data']['content']
                videos = InitClass().get_video(content)
                if videos:
                    fields["videos"] = videos
                    fields["videocover"] = imgurl  # 文章的视频封面地址
                likenum = articlejson['data']['praiseCount']
                commentnum = articlejson['data']['replyCount']
                title = articlejson['data']['title']
                workerid = articlejson['data']['id']
                contentType = 2
                if channelname == '橘视频':
                    contentType = 4
                fields["contentType"] = contentType
                fields["commentnum"] = commentnum  # 文章评论数
                fields["appname"] = appname
                fields["platformID"] = self.platform_id
                fields["workerid"] = workerid
                fields["content"] = content
                fields["likenum"] = likenum
                fields["title"] = title
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Kanwanzhounews(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for channel_field, channel_param in appspider.getarticlelistparams():
        for article_list_res in appspider.getarticlelists(channel_param):
            for article_param in appspider.getarticleparams(article_list_res):
                for article_res in appspider.getarticlehtml(article_param):
                    for data in appspider.analyzearticle(article_res):
                        yield data
        yield {"code": 1, "msg": "OK", "data": {"channel": channel_field}}
