# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
import requests
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass
from lxml import html
from html.parser import HTMLParser


# from lxml import etree

class Shanghaichangning(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "http://www.shcnxwxczx.com/Interface/Channel/listChannel.do"
        # 频道请求头
        headers = {
            "Content-Length": "0",
            "Host": "www.shcnxwxczx.com",
            "User-Agent": "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MuMu Build/V417IR) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Accept-Encoding": "gzip",
            "Connection": "keep-alive"
        }
        # 频道数据体
        data = {
            "key": "homepage"
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
    def analyzechannels(channelsres):
        """
        此方法主要获取channelid,channelname即可
        若请求文章列表页需要channeltype，categoryname，categoryid,则以categoryname= categoryname形式传递参数
        :param channelsres:
        :return:
        """
        channelslists = json.loads(channelsres)
        for channel in channelslists['data']:
            channelid = channel['key']
            channelname = channel['title']
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam

    def getarticlelistsparams(self, channelsres):
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
            url = "http://www.shcnxwxczx.com/Interface/Recodrd/listRecod1.do"
            headers = {
                "Content-Length": "0",
                "Host": "www.shcnxwxczx.com",
                "User-Agent": "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MuMu Build/V417IR) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                "Accept-Encoding": "gzip",
                "Connection": "keep-alive"
            }
            data = {
                "pageNum": "1",
                "getSize": "20",
                "key": channelid,
            }
            method = 'post'
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channel_index_id=channel_index_id, data=data)
            if channelname == "头条":
                url_banner = "http://www.shcnxwxczx.com:8020/MIS/visualization/app/column"  # banner请求接口
                headers_banner = {
                    "Content-Length": "0",
                    "Host": "www.shcnxwxczx.com:8020",
                    "User-Agent": "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MuMu Build/V417IR) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                    "Accept-Encoding": "gzip",
                    "Connection": "keep-alive",
                }
                data_banner = {
                    'channelid': 4,
                }
                articlelist_param_banner = InitClass().articlelists_params_fields(url_banner, headers_banner, method,
                                                                                  channelname,
                                                                                  channel_index_id=channel_index_id,
                                                                                  data=data_banner,
                                                                                  banners=1)  # 添加banner请求数据体，或其他接口请求数据
                yield channel_field, [articlelist_param_banner, articlelist_param]
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
            channelname = articleslist_res.get("channelname")
            channelid = articleslist_res.get("channelID")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                try:
                    articlelists = articlelist_json['data']
                    for article in articlelists:
                        articleparam = InitClass().article_list_fields()
                        if "icodata" in article.keys():
                            control_id = article['controlId']
                            if control_id == "slider" or control_id == "hot":
                                icodatas = article["icodata"]
                                for banneritem in icodatas:
                                    banners = 1
                                    if control_id == 'hot':
                                        banners = 0
                                    articletitle = banneritem['TITLE']
                                    updatetime = banneritem['updateTime']
                                    imgs = banneritem['IMG']
                                    jumpurl = banneritem['URL']
                                    if jumpurl:
                                        res = requests.get(jumpurl)
                                        tree = html.fromstring(res.text)
                                        name = tree.xpath('//div[@class="text"]')
                                        name1 = html.tostring(name[0])
                                        content = HTMLParser().unescape(name1.decode())
                                        fields = InitClass().article_fields()
                                        fields["channelID"] = channelid
                                        fields["contentType"] = 1
                                        fields["images"] = []
                                        fields["videos"] = []
                                        fields["videocover"] = []
                                        fields["pubtime"] = 0
                                        fields["createtime"] = 0
                                        fields["channelname"] = channelname

                                        if imgs:
                                            fields["articlecovers"] = [imgs]
                                        else:
                                            fields["articlecovers"] = []

                                        fields["banner"] = banners
                                        fields["appname"] = "上海长宁"
                                        fields["title"] = articletitle
                                        fields["content"] = content
                                        fields["url"] = jumpurl
                                        fields["updatetime"] = InitClass().date_time_stamp(updatetime)
                            else:
                                continue
                        else:
                            articletitle = article['title']
                            articleid = article['id']
                            jump = article['RecordJumpUrl']
                            recordtype = article['RecordType']
                            videos = article["VideoUrl"]
                            pubtime = article["time"]
                            author = article["companyName"]
                            workerid = article["id"]
                            imgurl = ""
                            try:
                                imgurl = article['img']
                                articleparam["imageurl"] = imgurl
                            except Exception as e:
                                logging.info(f"在文章列表出无法获得封面图{e}")
                            if jump:
                                if recordtype == '1' or recordtype == '2':
                                    res = requests.get(jump)
                                    tree = html.fromstring(res.text)
                                    name = tree.xpath('//div[@class="text"]')
                                    try:
                                        name1 = html.tostring(name[0])
                                        content = HTMLParser().unescape(name1.decode())
                                        fields = InitClass().article_fields()
                                        fields["channelID"] = channelid
                                        fields["images"] = []
                                        fields["videos"] = []
                                        fields["videocover"] = []
                                        fields["createtime"] = 0
                                        fields["updatetime"] = 0
                                        if recordtype == '1':
                                            fields["contentType"] = 1
                                        elif recordtype == '2':
                                            fields["contentType"] = 6
                                        else:
                                            fields["contentType"] = -1
                                        fields["channelname"] = channelname
                                        if imgurl:
                                            fields["articlecovers"] = [imgurl]
                                        else:
                                            fields["articlecovers"] = []
                                        fields["banner"] = 0
                                        fields["appname"] = "上海长宁"
                                        fields["title"] = articletitle
                                        fields["url"] = jump
                                        fields["workerid"] = workerid
                                        fields["content"] = content
                                        fields["author"] = author
                                        pubtime = pubtime.rstrip()
                                        fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                                    except Exception as e:
                                        print("e===", e)
                                elif recordtype == '3':
                                    # 专题
                                    articleparam["recordtype"] = '3'
                                    if "http://www.shcnxwxczx.com/news/more" in jump:
                                        paramList = jump.strip().split('?')[1].split('&')
                                        for item in paramList:
                                            key = item.split('=')[0]

                                            if key == "key":
                                                specialkey = item.split('=')[1]

                                                articleparam["specialkey"] = specialkey
                                    else:
                                        # 外部链接
                                        fields = InitClass().article_fields()
                                        fields["channelID"] = channelid

                                        fields["images"] = []
                                        fields["videos"] = []
                                        fields["videocover"] = []
                                        # fields["width"] = 0
                                        # fields["height"] = 0
                                        fields["createtime"] = 0
                                        fields["updatetime"] = 0

                                        fields["contentType"] = -1
                                        fields["channelname"] = channelname

                                        if imgurl:
                                            fields["articlecovers"] = [imgurl]
                                        else:
                                            fields["articlecovers"] = []

                                        fields["banner"] = 0
                                        fields["appname"] = "上海长宁"
                                        fields["title"] = articletitle
                                        fields["url"] = jump
                                        fields["workerid"] = workerid
                                        fields["content"] = jump
                                        fields["author"] = author
                                        pubtime = pubtime.rstrip()
                                        fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                                        print(json.dumps(fields, indent=4, ensure_ascii=False))
                                        continue
                                else:
                                    print("未知类型")
                                    continue
                            articleparam["video"] = videos  # 此步骤为存储视频url
                            articleparam["pubtime"] = pubtime  # 此步骤为存储发布时间
                            articleparam["channelID"] = channelid
                            articleparam["articletitle"] = articletitle
                            articleparam["articleid"] = articleid
                            articleparam["channelname"] = channelname
                            articleparam["banner"] = banners
                            articleparam["articleurl"] = jump
                            yield articleparam
                except Exception as e:
                    print(e, articlelist_json)
            except Exception as e:
                print(e, articlelist_json)

    def getarticleparams(self, articleslist_ress):
        """
        组建请求文章详情所需要的数据体
        :param articles:
        :return:
        """
        for articleparam in self.analyze_articlelists(articleslist_ress):
            recordtype = articleparam.get("recordtype")
            specialkey = articleparam.get("specialkey")
            url = "http://changning.chinashadt.com:8020/Interface/Recodrd/listRecod1.do"
            data = {
                "pageNum": 1,
                "getSize": 20,
                'key': specialkey
            }
            headers = {
                "Host": "changning.chinashadt.com:8020",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "Origin": "http://www.shcnxwxczx.com",
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,en-US;q=0.8",
                "X-Requested-With": "com.msqing.cnnews",
                "Connection": "keep-alive"
            }
            method = 'get'
            # 此处代码不需要改动
            channelid = articleparam.get("channelID")
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
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl,
                                                        channel_index_id=channel_index_id,
                                                        data=data,
                                                        videourl=videos, videocover=videocover, pubtime=pubtime,
                                                        createtime=createtime, updatetime=updatetime,
                                                        source=source, author=author, likenum=likenum,
                                                        commentnum=commentnum, sharenum=sharenum, readnum=readnum,
                                                        articleurl=articleurl, banners=banner)
            yield [article]

    def analyzearticles(self,articles_res):
        for articleres in articles_res:
            channelname = articleres.get("channelname")
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            banners = articleres.get("banner")
            channelid = articleres.get("channelID")
            articleurl = articleres.get("articleurl")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["channelID"] = channelid
            fields["url"] = articleurl
            if imgurl:
                fields["articlecovers"] = [imgurl]
            else:
                fields["articlecovers"] = []
            fields["banner"] = banners
            fields["images"] = []
            fields["videos"] = []
            fields["videocover"] = []
            fields["createtime"] = 0
            fields["updatetime"] = 0
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                # print("articlejson==",articlejson)

                articles = articlejson["data"]
                for article in articles:
                    title = article["title"]
                    try:
                        author = article["companyName"]
                        fields["author"] = author
                    except Exception as e:
                        print("eee")

                    pubtime = article["time"]
                    jumpurl = article["RecordJumpUrl"]
                    workerid = article["id"]
                    # article["img"]
                    recordtype = article["RecordType"]

                    if jumpurl:
                        fields["url"] = jumpurl
                        if recordtype == '1' or recordtype == '2':
                            # 文字，画廊

                            if recordtype == '1':
                                fields["contentType"] = 1
                            elif recordtype == '2':
                                fields["contentType"] = 6
                            else:
                                fields["contentType"] = -1

                            res = requests.get(jumpurl)
                            tree = html.fromstring(res.text)
                            name = tree.xpath('//div[@class="text"]')
                            try:
                                name1 = html.tostring(name[0])
                                content = HTMLParser().unescape(name1.decode())
                                fields["content"] = content

                            except Exception as e:
                                name = tree.xpath('//div[@class="rich_media_content "]')
                                try:
                                    name1 = html.tostring(name[0])
                                    content = HTMLParser().unescape(name1.decode())
                                    fields["content"] = content
                                except Exception as e:
                                    print("e===", e, article)
                    fields["appname"] = appname
                    fields["title"] = title
                    fields["workerid"] = workerid
                    pubtime = pubtime.rstrip()
                    fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Shanghaichangning(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
