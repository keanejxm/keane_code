# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class Renminribaowenchuang(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        url = "http://rmrbwc.com/rest/themeTypes/client"
        headers = {
            "token": "",
            "Host": "rmrbwc.com",
            "Accept-Encoding": "gzip",
            "Cookie": "JSESSIONID=C8826175D8C13DEB77A2ECF5F7630E00",
            "User-Agent": "okhttp/3.9.1",
            "Connection": "keep-alive",
        }
        data = {}
        method = "get"
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
        for channel in channelslists['payload']:
            channelid = channel['id']
            channelname = channel['name']
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
            url = "http://rmrbwc.com/rest/themes/v1/list"
            headers = {
                "token": "",
                "Host": "rmrbwc.com",
                "Accept-Encoding": "gzip",
                "Cookie": "JSESSIONID=C8826175D8C13DEB77A2ECF5F7630E00",
                "User-Agent": "okhttp/3.9.1",
                "Connection": "keep-alive"
            }
            data = {
                "id": channelid,
                "currentPage": 0,
                "pageSize": 6,
            }
            method = 'get'
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channel_index_id=channel_index_id, data=data)
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
                    articlelists = articlelist_json['payload']
                    list = articlelists['themeList']['list']
                    banner_list = articlelists['bannerList']
                    activitys = []
                    try:
                        activity_list = articlelists['activityList']
                        for activityitem in activity_list:
                            actype = activityitem['type']
                            if actype != 1:
                                activitys += activityitem['objectList']
                    except Exception as e:
                        activitys = []
                    for article in banner_list:
                        banners = 1
                        articleparam = InitClass().article_list_fields()
                        articletitle = article['description']
                        try:
                            articleid = article['targetId']
                        except Exception as e:
                            articleid = article['id']
                        try:
                            articleparam["imageurl"] = article['pictureInfo']['url']
                        except Exception as e:
                            logging.info(f"在文章列表出无法获得封面图{e}")
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["channelname"] = channelname
                        articleparam["channelID"] = channelid
                        articleparam["banner"] = banners
                        yield articleparam
                    for article in list + activitys:
                        banners = 0
                        articleparam = InitClass().article_list_fields()
                        articletitle = article['title']
                        articleid = article['id']
                        pubtime = article["publishTime"]  # 在此处获取到文章的发布时间，避免在文章详情获取不到发布时间
                        createtime = article["creationTime"]  # 在此处获取到文章的创建时间，避免在文章详情获取不创建时间
                        updatetime = article["updateTime"]  # 在此处获取到文章的更新时间，避免在文章详情获取不到更新时间
                        source = article["source"]  # 在此处获取到文章的来源，避免在文章详情获取不到来源
                        author = article["author"]  # 在此处获取到文章的作者，避免在文章详情获取不到作者
                        readnum = article["viewCount"]  # 在此处获取到文章的阅读数，避免在文章详情获取不到阅读数
                        articleurl = article["themeUrl"]  # 在此处获取到文章html地址，避免在文章详情获取不到html地址
                        articleparam["pubtime"] = pubtime  # 此步骤为存储发布时间
                        articleparam["createtime"] = createtime  # 此步骤为存储创建时间
                        articleparam["updatetime"] = updatetime  # 此步骤为存储更新时间
                        articleparam["source"] = source  # 此步骤为存储文章来源
                        articleparam["author"] = author  # 此步骤为存储作者
                        articleparam["readnum"] = readnum
                        articleparam["articleurl"] = articleurl
                        try:
                            coverinfo = article["coverInfo"]
                            articleparam["imageurl"] = coverinfo["url"]
                        except Exception as e:
                            logging.info(f"在文章列表出无法获得封面图{e}")
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["channelname"] = channelname
                        articleparam["channelID"] = channelid
                        articleparam["banner"] = banners
                        yield articleparam
                except Exception as e:
                    print('eeeee==== ', e, articlelist_json)
            except Exception as e:
                print('eee===== ', e, articlelist_json)

    def getarticleparams(self, articleslist_ress):
        """
        组建请求文章详情所需要的数据体
        :param articles:
        :return:
        """
        headers = {
            'token': '',
            'Host': 'rmrbwc.com',
            'Accept-Encoding': 'gzip',
            'Cookie': 'JSESSIONID=C8826175D8C13DEB77A2ECF5F7630E00',
            'User-Agent': 'okhttp/3.9.1',
            'Connection': 'keep-alive'
        }
        data = {}
        method = 'get'
        for articleparam in self.analyze_articlelists(articleslist_ress):
            channelid = articleparam.get("articleid")
            url = 'http://rmrbwc.com/rest/themes/' + str(channelid)
            videos = url
            channelname = articleparam.get("channelname")
            channel_index_id = articleparam.get("channelindexid")
            channelid = articleparam.get("channelID")
            banner = articleparam.get("banner")
            imgurl = articleparam.get("imageurl")
            # videos = articleparam.get("videos")
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
            article = InitClass().article_params_fields(url, headers, method, channelname,
                                                        channel_index_id=channel_index_id,
                                                        imageurl=imgurl, data=data,
                                                        videourl=videos, videocover=videocover, pubtime=pubtime,
                                                        createtime=createtime, updatetime=updatetime,
                                                        source=source, author=author, likenum=likenum,
                                                        commentnum=commentnum, sharenum=sharenum, readnum=readnum,
                                                        articleurl=articleurl, banners=banner)
            yield [article]

    def analyzearticles(self,articles_res):
        for articleres in articles_res:
            channelname = articleres.get("channelname")
            channel_index_id = articleres.get("channelindexid")
            channelid = articleres.get("channelID")
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            banners = articleres.get("banner")
            url = articleres.get("videourl")
            articleurl = articleres.get("articleurl")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["channelID"] = channelid
            if articleurl:
                fields["url"] = articleurl
            else:
                fields["url"] = url

            if imgurl:
                fields["articlecovers"] = [imgurl]
            else:
                fields["articlecovers"] = []

            fields["banner"] = banners
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                code = articlejson['code']
                if code != 0:
                    print("code != 0")
                    continue
                article = articlejson['payload']
                workerid = article['id']
                title = article['title']  # 标题
                content = article['content']  # 文章内容
                createtime = article['creationTime']
                updatetime = article['updateTime']
                pubtime = article['publishTime']
                readnum = article['viewCount']
                author = article["author"]
                source = article['source']  # 来源
                fields["contentType"] = 1
                fields["readnum"] = readnum  # 文章的阅读数
                fields["appname"] = self.newsname
                fields["platformID"] = self.platform_id
                fields["channelindexid"] = channel_index_id
                fields["title"] = title
                fields["workerid"] = workerid
                fields["source"] = source
                fields["content"] = content
                fields["author"] = author
                # fields["commentnum"] = commentnum
                fields["createtime"] = InitClass().date_time_stamp(createtime)
                fields['updatetime'] = InitClass().date_time_stamp(updatetime)
                fields["pubtime"] = InitClass().date_time_stamp(pubtime)

                fields["videocover"] = []

                try:
                    videos = InitClass().get_video(content)
                    fields["videos"] = videos
                except Exception as e:
                    print("正文无视频")
                try:
                    images = InitClass().get_images(content)
                    fields["images"] = images
                except Exception as e:
                    print("正文无图片")
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print('eeeee=', e)

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Renminribaowenchuang(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
