# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class Wuxibobaonews(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "http://wxbb-api.wifiwx.com/mobile/api/bbapp2/lb_news_recomend_column.php?count=10&system_version=6.0.1&app_version=2.2.7&client_id_android=0297b4f3430ca5360c4a326e17d8dde1&locating_city=%E5%8D%97%E4%BA%AC&appkey=qm31EZoorKe0oCu3GfAY3pmxQmw8TZoa&version=2.2.7&appid=36&location_city=%E5%8D%97%E4%BA%AC&device_token=25907d3b0c33083c013735ff99cf14f7&phone_models=MuMu&package_name=com.hoge.android.app.wuxibobao&system_version=6.0.1&app_version=2.2.7&client_id_android=0297b4f3430ca5360c4a326e17d8dde1&locating_city=%E5%8D%97%E4%BA%AC&appkey=qm31EZoorKe0oCu3GfAY3pmxQmw8TZoa&version=2.2.7&appid=36&location_city=%E5%8D%97%E4%BA%AC&device_token=25907d3b0c33083c013735ff99cf14f7&phone_models=MuMu&package_name=com.hoge.android.app.wuxibobao"
        # 频道请求头
        headers = {
            "X-API-TIMESTAMP": "1608088449371kfw93M",
            "X-API-SIGNATURE": "ZmQ0NWE5NDAwOWI1OTMyMWUyMDkzNWVkN2YxNGZiY2JjZTM5YTZhMQ==",
            "X-API-VERSION": "2.2.7",
            "X-AUTH-TYPE": "sha1",
            "X-API-KEY": "70efdf2ec9b086079795c442636b55fb",
            "Host": "wxbb-api.wifiwx.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Cookie": "__jsluid_h=013276033ffaef88f07c6412f9b68e0a",
            "User-Agent": "okhttp/3.9.1",
        }
        # 频道数据体
        data = {}
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
        # 将返回的数据转为json数据
        channelslists = json.loads(channelsres)
        # 返回的数据是编码错误，则用下面代码解析数据
        # channelslists = json.loads(json.dumps(channelsres,indent=4,ensure_ascii=False))
        for channel in channelslists:
            channelid = channel['id']
            channelname = channel['name']
            channelparam = InitClass().channel_fields(channelid, channelname)
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
            url = "http://wxbb-api.wifiwx.com/mobile/api/bbapp2/news.php"
            headers = {
                "Accept-Language": "zh-CN,zh;q=0.8",
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_17 1.0.0",
                "X-API-TIMESTAMP": "1608089479735RqmQNQ",
                "X-API-SIGNATURE": "Y2Q4NzFiMTIwMDFmNzVhODYwYWQ0MTRkMmFjMGE5ZjgxNDU2MDJlYg==",
                "X-API-VERSION": "2.2.7",
                "X-AUTH-TYPE": "sha1",
                "X-API-KEY": "70efdf2ec9b086079795c442636b55fb",
                "Host": "wxbb-api.wifiwx.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "Cookie": "__jsluid_h=013276033ffaef88f07c6412f9b68e0a",
            }
            data = {
                "site_id": "1",
                "client_type": "2",
                "count": "20",
                "except_weight": "90",
                "system_version": "6.0.1",
                "app_version": "2.2.7",
                "client_id_android": "0297b4f3430ca5360c4a326e17d8dde1",
                "locating_city": "南京",
                "appkey": "qm31EZoorKe0oCu3GfAY3pmxQmw8TZoa",
                "version": "2.2.7",
                "appid": "36",
                "location_city": "南京",
                "device_token": "25907d3b0c33083c013735ff99cf14f7",
                "phone_models": "MuMu",
                "package_name": "com.hoge.android.app.wuxibobao",
                "count": "20",
                "offset": "0",
                "column_name": channelname,
                "column_id": channelid,
            }
            method = 'get'
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
            channelname = articleslist_res.get("channelname")
            channel_index_id = articleslist_res.get("channelindexid")
            channelID = articleslist_res.get("channelID")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                try:
                    for b in ["slide", "list"]:
                        if b in articlelist_json and articlelist_json[b]:
                            articlelists = articlelist_json[b]
                            banners = 1 if b == "slide" else 0
                            for article in articlelists:
                                articleparam = InitClass().article_list_fields()
                                articletitle = article['title']
                                articleid = article['id']
                                try:
                                    articleparam["imageurl"] = []
                                except Exception as e:
                                    logging.info(f"在文章列表出无法获得封面图{e}")
                                articleparam["articleid"] = articleid
                                articleparam["articletitle"] = articletitle
                                articleparam["channelname"] = channelname
                                articleparam["channelindexid"] = channel_index_id
                                articleparam["channelID"] = channelID
                                articleparam["banner"] = banners
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
        url = 'http://wxbb-api.wifiwx.com/mobile/api/bbapp2/item.php'
        headers = {
            "Accept-Language": "zh-CN,zh;q=0.8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_17 1.0.0",
            "X-API-TIMESTAMP": "1608090875652gQbZPv",
            "X-API-SIGNATURE": "YWI2ZjJiZTJiMmQ2MzhiN2YxOWU5YjJhNzgxMzgzZDcyM2RiNDBkNQ==",
            "X-API-VERSION": "2.2.7",
            "X-AUTH-TYPE": "sha1",
            "X-API-KEY": "70efdf2ec9b086079795c442636b55fb",
            "Host": "wxbb-api.wifiwx.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Cookie": "__jsluid_h=013276033ffaef88f07c6412f9b68e0a",
        }
        method = 'post'
        for articleparam in self.analyze_articlelists(articleslist_ress):
            data = {
                "system_version": "6.0.1",
                "app_version": "2.2.7",
                "client_id_android": "02b4f3430ca5360c4a326e17d8dde1",
                "locating_city": "南京",
                "appkey": "qm31EZoorKe0oCu3GfAY3pmxQmw8TZoa",
                "version": "2.2.7",
                "appid": "36",
                "location_city": "南京",
                "device_token": "25907d3b0c33083c013735ff99cf14f7",
                "phone_models": "MuMu",
                "package_name": "com.hoge.android.app.wuxibobao",
                'id': articleparam.get("articleid"),
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
            channelID = articleres.get("channelID")
            channelname = articleres.get("channelname")
            channel_index_id = articleres.get("channelindexid")
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            banners = articleres.get("banner")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["platformID"] = self.platform_id
            fields["channelindexid"] = channel_index_id
            fields["channelID"] = channelID
            fields["images"] = [imgurl]
            fields["articlecovers"] = [imgurl]
            fields["banner"] = banners
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                print(articlejson)
                if 'title' in articlejson:
                    title = articlejson['title']  # 标题

                    workerid = articlejson['id']
                    url = articlejson["content_url"]
                    author = articlejson["author"]
                    pubtime = articlejson['publish_time']
                    createtime = articlejson['create_time']
                    if 'content' in articlejson:
                        content = articlejson['content']  # 文章内容
                        fields["content"] = content
                    if 'childs_data' in articlejson:
                        img = list()
                        for imgsrc in articlejson['childs_data']:
                            img.append(imgsrc['host'] + imgsrc['dir'] + imgsrc['filepath'] + imgsrc['filename'])
                        fields["images"] = img
                        fields["articlecovers"] = img
                    if 'video_filename' in articlejson.keys():
                        videos = list()
                        videos.append(
                            articlejson['hostwork'] + '/' + articlejson['video_path'] + articlejson['video_filename'])
                        fields["videos"] = videos
                        fields["width"] = articlejson['width']
                        fields["height"] = articlejson['height']
                    if 'from_appname' in articlejson.keys():
                        source = articlejson['from_appname']  # 来源
                        fields["source"] = source
                    if 'content' in articlejson.keys() and 'video_filename' in articlejson.keys():
                        fields["contentType"] = 3
                    elif 'content' in articlejson.keys():
                        fields["contentType"] = 2
                    elif 'video_filename' in articlejson.keys():
                        if articlejson['width'] >= articlejson['height']:
                            fields["contentType"] = 4
                        else:
                            fields["contentType"] = 5
                    fields["appname"] = appname
                    fields["title"] = title
                    fields["url"] = url
                    fields["workerid"] = workerid
                    fields["author"] = author
                    fields["pubtime"] = int(pubtime) * 1000
                    fields["createtime"] = int(createtime) * 1000
                    fields = InitClass().wash_article_data(fields)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)


def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Wuxibobaonews(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
