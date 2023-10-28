# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
import bs4
import requests
from appspider_m import Appspider
from initclass import InitClass


class Jinrinanchuannews(Appspider):

    # @staticmethod
    # def get_app_params():
    #     """
    #     组合请求频道的数据体
    #     :return:
    #     """
    #     # 频道url
    #     url = "https://api.cqliving.com/initStart.html"
    #     # 频道请求头
    #     headers = {
    #         "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    #         "Content-Length": "122",
    #         "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
    #         "Host": "api.cqliving.com",
    #         "Connection": "Keep-Alive",
    #         "Accept-Encoding": "gzip"
    #     }
    #     # 频道数据体
    #     data = {
    #         "appId":"28",
    #         "appVersion":"5042",
    #         "loadingImgVersion":"239",
    #         "columnsVersion": "106",
    #         "type":"1",
    #         "sessionId":"5e994da03ad9411fb8cdb8f7983e4e81",
    #         "token":""
    #     }
    #     # 如果携带的是json数据体,用appjson发送
    #     # app_json = {}
    #     # 频道请求方式
    #     method = "post"
    #     app_params = InitClass().app_params(url, headers, method, data = data)
    #     # 如果携带json数据，用下列方式存储发送数据
    #     # app_params = InitClass().app_params(url, headers, method, data = data ,appjson=app_json)
    #     yield app_params

    @staticmethod
    def analyzechannels():
        """
        此方法主要获取channelid,channelname即可
        若请求文章列表页需要channeltype，categoryname，categoryid,则以categoryname= categoryname形式传递参数
        :param channelsres:
        :return:
        """
        navList = [
            # {
            #     "id": 831,
            #     "name": "头条"
            # },
            {
                "id":2160,
                "name":"时政"
            },
            {
                "id":834,
                "name":"综合"
            },
            {
                "id":2144,
                "name":"民生热线"
            },
            # {
            #     "id":2233,
            #     "name":"直播"
            # },
            # {
            #     "id":2143,
            #     "name":"专题"
            # },
            {
                 "id":10007,
                "name":"看区县"
            },
            {
                "id":10041,
                "name": "部门·镇街"
            }
        ]
        channelparams = []
        for channel in navList:
            channelid = channel['id']
            channelname = channel['name']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)
        yield channelparams
    @staticmethod
    def getarticlelistsparams(channelsparams):
        """
        此方法目的是组建请求文章列页面数据参数，url，headers，data，若以json形式发送数据，则channeljson = channeljson
        :param channelsparams:
        :return:
        """
        print(channelsparams)
        articleparams = []
        for channel in channelsparams:
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
                    'token':''
                }
            else:
                data = {
                    "appId": "32",
                    "isCarousel":"true",
                    "columnId":channelid,
                    "businessValue":"",
                    "unionValue":"",
                    "lastId":"",
                    "lastSortNo":"",
                    "lastOnlineTime":"",
                    "sessionId":"26436776ad77489fa889c8c697038ca4",
                    "token":""
                }
            method = 'post'
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data, channel_id = channelid)
            articleparams.append(articlelist_param)
        yield articleparams

    @staticmethod
    def analyze_articlelists(articleslist_ress):
        """
        解析文章列表页，目的是为了获取文章具体信息，组建请求文章详情数据体
        :param articleslist_ress:
        :return:
        """
        articlesparams = []
        for articleslist_res in articleslist_ress:
            banners = articleslist_res.get("banner")
            channelid = articleslist_res.get("channelID")
            channelname = articleslist_res.get("channelname")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                print(articlelist_json)
                # 可在下面打印处打断点，查看请求到的数据
                #若banner图在articlelist_json中则分来开取并给其复制banner = 1
                try:
                    articlelists = articlelist_json['data']['news']
                    for article in articlelists:
                        if 'type'in article.keys() and article['type'] == 0:
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
                                if 'contentUrl' in article.keys() and article['contentUrl'] != '':
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
                                articleparam["banner"] = banners
                                articleparam["articleurl"] = articleurl
                                articlesparams.append(articleparam)
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
                                    if 'contentUrl' in article.keys() and article['contentUrl'] != '':
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
                                    articleparam["banner"] = banners
                                    articleparam["articleurl"] = articleurl
                                    articlesparams.append(articleparam)
                except Exception as e:
                    print(e, articlelist_json)
            except Exception as e:
                print(e, articlelist_json)
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        """
        组建请求文章详情所需要的数据体
        :param articles:
        :return:
        """
        print(articles)
        articlesparam = []
        url = 'https://exapi.cqliving.com/infoDetailNew.html'
        headers = {
            "Host":"exapi.cqliving.com",
            "Connection":"keep-alive",
            "Content-Length":"22",
            "Accept":"application/json, text/plain, */*",
            "Origin":"https://share.cqliving.com",
            "User-Agent":"Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 CQ_XHL(5042;Android;28;6bb900da9e6848fdbc579bd8b9e7c6b6;;0)",
            "Content-Type":"application/x-www-form-urlencoded",
            "Referer":"https://share.cqliving.com/news-detail-pages/",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,en-US;q=0.8",
            "X-Requested-With":"com.yaoyu.wanzhou",
        }
        method = 'post'
        for articleparam in articles:
            data = {
                'infoClassifyId':articleparam.get("articleid"),
            }
            # 此处代码不需要改动
            articleid = articleparam.get("articleid")
            channelid = articleparam.get("channelID")
            channelname = articleparam.get("channelname")
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
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data = data, articleid = articleid,
                                                        videourl = videos, videocover = videocover, pubtime = pubtime,
                                                        createtime = createtime, updatetime = updatetime,
                                                        source = source, author = author, likenum = likenum,
                                                        commentnum = commentnum, sharenum = sharenum, readnum = readnum,
                                                        articleurl = articleurl,banners = banner,channel_id=channelid)
            articlesparam.append(article)
        yield articlesparam

    @staticmethod
    def analyzearticles(articles_res):
        for articleres in articles_res:
            channelid = articleres.get("channelID")
            channelname = articleres.get("channelname")
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
            fields["channelID"] = channelid
            fields["workerid"] = workerid
            fields["channelname"] = channelname
            fields["images"] = imgurl
            fields["articlecovers"] = imgurl
            fields["banner"] = banners
            # 如果有下列字段需添加
            fields["url"] = articleurl #文章的html网址，提取shareurl
            fields["videos"] = videos #文章的视频链接地址
            fields["videocover"] = videocover #文章的视频封面地址
            fields["source"] = source #文章的来源
            fields["pubtime"] = InitClass().date_time_stamp(pubtime)
            fields["author"] = author #文章作者
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent = 4, ensure_ascii = False))
                res = requests.get(articleurl)
                res.encoding = res.apparent_encoding
                html = res.text
                bf = bs4.BeautifulSoup(html, 'html.parser')
                content = bf.find('div', class_='detail_content')
                contentType = 2
                if content:
                    fields["content"] = content
                    content = str(content)
                    videos = InitClass().get_video(content)
                    if videos:
                        fields["videos"] = videos
                        fields["videocover"] = imgurl  # 文章的视频封面地址
                        contentType = 3
                else:
                    fields["content"] = ''

                likenum = articlejson['data']['praiseCount']
                commentnum = articlejson['data']['replyCount']
                title = articlejson['data']['title']
                fields["contentType"] = contentType
                fields["commentnum"] = commentnum  # 文章评论数
                fields["appname"] = appname
                fields["content"] = content
                fields["likenum"] = likenum
                fields["title"] = title
                print(json.dumps(fields, indent = 4, ensure_ascii = False))
            except Exception as e:
                print(e)

    def run(self):
        # appparams = self.get_app_params()
        # channelsres = self.getchannels(appparams.__next__())
        channelsparams = self.analyzechannels()
        articleparams = self.getarticlelistsparams(channelsparams.__next__())
        articles_ress = self.getarticlelists(articleparams.__next__())
        articles = self.analyze_articlelists(articles_ress.__next__())
        articlesparam = self.getarticleparams(articles.__next__())
        articles_html = self.getarticlehtml(articlesparam.__next__())
        self.analyzearticles(articles_html.__next__())


if __name__ == '__main__':
    spider = Jinrinanchuannews('今日南川')
    spider.run()
