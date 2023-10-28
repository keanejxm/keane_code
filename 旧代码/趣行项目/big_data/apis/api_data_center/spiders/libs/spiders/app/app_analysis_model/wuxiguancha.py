# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class Wuxiguanchanews(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        url = "http://wap.wxgc.wxrb.com/api/mchannel/getChildChannelByCode"
        headers = {
            "signature": "194220e595025fb9d6cf9b036ad27248",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Content-Length": "123",
            "Host": "wap.wxgc.wxrb.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Cookie": "JSESSIONID=5A345A5EDE736CFF2DA3E913A5B3FB98",
            "User-Agent": "okhttp/3.12.1",
        }
        # 频道数据体
        data = {
            "timestamp": "1608100499710",
            "siteId": "BDF761C7DFF141B486E34383312E1708",
            "sign": "b1feeff36eed89c24993e9f070c5fe64",
            "platform": "app",
            "code": "top",
        }
        # 如果携带的是json数据体,用appjson发送
        # app_json = {}
        # 频道请求方式
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
        channelslists = json.loads(channelsres)
        for channel in channelslists['data']['children']:
            channelid = channel['id']
            channelname = channel['name']
            channeltype = channel['alias']
            if channelname == '活动' or channelname == '专题' or channelname == '直播':
                channelname = channel['name']
            else:
                channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channeltype)
                yield channelparam

    def getarticlelistparams(self, channelsres):
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
            if channelname == '视频':
                url = 'http://wap.wxgc.wxrb.com/api/mcontent/getContentList'
                headers = {
                    "signature": "831e7a8cadcf3a3f25419cea1fbcd4d8",
                    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                    "Content-Length": "192",
                    "Host": "wap.wxgc.wxrb.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "Cookie": "JSESSIONID=50E063554B8E6F6AAA8118AF96454E34",
                    "User-Agent": "okhttp/3.12.1",
                }
                data = {
                    "platform": "app",
                    "channelId": "3247F7DAC2234AE39C90C5B5B1C115E2",
                    "sign": "2d6d82e82dec9c8b418a6788c291b378",
                    "pageSize": "10",
                    "contentType": "0",
                    "timestamp": "1608107161924",
                    "siteId": "BDF761C7DFF141B486E34383312E1708",
                    "pageNo": "1",
                }
                method = 'post'
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                           channel_index_id=channel_index_id)
                yield channel_field, [articlelist_param]
            elif channelname == '直播':
                url = 'http://wap.wxgc.wxrb.com/api/mcontent/getContentList'
                headers = {
                    "signature": "6735c8b7ae328ea81ce66a4888673c20",
                    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                    "Content-Length": "192",
                    "Host": "wap.wxgc.wxrb.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "Cookie": "JSESSIONID=CA821593F5EB62925EAB885244BC5900",
                    "User-Agent": "okhttp/3.12.1",
                }
                data = {
                    "platform": "app",
                    "channelId": "B8E0C8C22FC3498280660BB11F6DBF7D",
                    "sign": "290bad192f6facab55a02d114ddaf3a7",
                    "pageSize": "10",
                    "contentType": "0",
                    "timestamp": "1608107183039",
                    "siteId": "BDF761C7DFF141B486E34383312E1708",
                    "pageNo": "1",
                }
                method = 'post'
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                           channel_index_id=channel_index_id)
                yield channel_field, [articlelist_param]
            else:
                url = f"http://wap.wxgc.wxrb.com/pages/json/{channeltype}/list.json"
                headers = {
                    "signature": "4f7d1f459a6aae3f25d05a755b519d98",
                    "random": "999",
                    "Host": "wap.wxgc.wxrb.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "Cookie": "JSESSIONID=963FB27CFA3222E34D2CAD5506D58464",
                    "User-Agent": "okhttp/3.12.1",
                }
                data = {}
                method = 'get'
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
            channelname = articleslist_res.get("channelname")
            channel_index_id = articleslist_res.get("channelindexid")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                print(articlelist_json)
                if channelname == '视频' or channelname == '直播':
                    if "list" in articlelist_json and articlelist_json["list"]:
                        articlelists = articlelist_json['list']
                else:
                    if "contents" in articlelist_json and articlelist_json["contents"]:
                        articlelists = articlelist_json['contents']
                for article in articlelists:
                    articleparam = InitClass().article_list_fields()
                    articletitle = article['title']
                    articleid = article['id']
                    subjectId = article['siteId']
                    try:
                        articleparam["imageurl"] = []
                        if 'mCoverImg' in article.keys():
                            img = list()
                            img.append(article['mCoverImg'])
                            articleparam["imageurl"] = img
                    except Exception as e:
                        print(e)
                    articleparam["subjectId"] = subjectId
                    articleparam["articleid"] = articleid
                    articleparam["articletitle"] = articletitle
                    articleparam["channelname"] = channelname
                    articleparam["channelindexid"] = channel_index_id
                    yield articleparam
            except Exception as e:
                print(e, articlelist_json)

    def getarticleparams(self, articleslist_ress):
        """
        组建请求文章详情所需要的数据体
        :param articles:
        :return:
        """
        url = 'http://wap.wxgc.wxrb.com/api/mcontent/getArticleDetails'
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Content-Length": "147",
            "Host": "wap.wxgc.wxrb.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Cookie": "JSESSIONID=30274E0A7D24C7D73F6C14FC23424ACE",
            "User-Agent": "okhttp/3.12.1",
        }
        method = 'post'
        for articleparam in self.analyze_articlelists(articleslist_ress):
            data = {
                "appid": "490000000245552",
                "platform": "app",
                "timestamp": "1608109467032",
                "contentId": articleparam.get("articleid"),
                "userId": "",
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

    @staticmethod
    def analyzearticle(articles_res):
        for articleres in articles_res:
            channelID = articleres.get("channelID")
            channelname = articleres.get("channelname")
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            banners = articleres.get("banner")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["channelID"] = channelID
            fields["images"] = imgurl
            fields["articlecovers"] = imgurl
            fields["banner"] = banners
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                title = articlejson['title']  # 标题
                content = articlejson['txt']  # 文章内容
                pubtime = articlejson['publishTime']  # 发布时间
                createtime = articlejson['createtime']
                workerid = articlejson['id']
                url = articlejson["url"]
                author = articlejson["userName"]
                likenum = articlejson["praiseCount"]
                commentnum = articlejson["commentCount"]
                if 'moVideoPath' in articlejson.keys() and articlejson['moVideoPath'] != '':
                    videos = list()
                    videocover = list()
                    videos.append(articlejson['moVideoPath'])  # 文章的视频链接地址
                    videocover.append(articlejson['mCoverImg'])  # 文章的视频封面地址
                    fields["videos"] = videos
                    fields["videocover"] = videocover
                    fields["contentType"] = 4
                else:
                    fields["contentType"] = 2
                if 'sourceName' in articlejson.keys():
                    source = articlejson['sourceName']  # 来源
                    fields["source"] = source
                fields["appname"] = appname
                fields["title"] = title
                fields["url"] = url
                fields["workerid"] = workerid
                fields["content"] = content
                fields["author"] = author
                fields["likenum"] = likenum
                fields["commentnum"] = commentnum
                fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                fields["createtime"] = InitClass().date_time_stamp(createtime)
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Wuxiguanchanews(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data