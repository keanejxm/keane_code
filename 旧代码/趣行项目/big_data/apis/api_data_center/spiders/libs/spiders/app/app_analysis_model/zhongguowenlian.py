# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : 中国文联
# @Software: PyCharm
""""
此app有专题需对专题特别处理
"""
import json
import logging
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class ZhongGuoWenLian(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        url = "https://prod.ccmapp.cn/api-cms-terminal/open/category?imei=490000000245552&id=a7fcda08806544d696a57" \
              "f698868c5f2"
        headers = {
            "url_name": "find",
            "Host": "prod.ccmapp.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.6.0",
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
        for channel in channelslists['data']:
            channelid = channel['id']
            channelname = channel['name']
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam

    def getarticlelistparams(self, channelsres):
        """
        此方法目的是组建请求文章列页面数据参数，url，headers，data，若以json形式发送数据，则channeljson = channeljson
        :param channelsres:
        :return:
        """
        channel_num = 0
        for channel in self.analyzechannels(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            if channelname == '关注':
                url = "http://md.ccmapp.cn:9998/rec"
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": "d666b359747e24cd1c39e0a74e60481e",
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
                    "Host": "md.ccmapp.cn:9998",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "Content-Length": "201"
                }
                data = {}
                channel_json = {"page": "1", "uid": "", "bid": "602816897101692", "item_type": "NewsBase",
                                "appkey": "36636158d26b7bf147b2059b8443c0c2", "gid": "080027f86771",
                                "sid": "4a70fdb3402732835231c10b9c8a59ec", "method": "602816897101692"}
                method = 'post'
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           data=data, channeljson=channel_json,
                                                                           channelid=channelid,
                                                                           channel_index_id=channel_index_id)
            else:
                url = "https://prod.ccmapp.cn/api-cms-production/app/production/pub/content/listWithAd"
                headers = {
                    "url_name": "find",
                    "Content-Type": "application/json; charset=UTF-8",
                    "Content-Length": "103",
                    "Host": "prod.ccmapp.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.6.0",
                }
                data = {}
                method = 'post'
                channel_json = {"categoryId": channelid, "currentPage": "1", "excludeUnitIds": [], "pageSize": "20"}
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           data=data, channeljson=channel_json,
                                                                           channelid=channelid,
                                                                           channel_index_id=channel_index_id)

            yield channel_field, [articlelist_param]

    def analyze_articlelists(self, articleslist_ress):
        """
        解析文章列表页，目的是为了获取文章具体信息，组建请求文章详情数据体
        :param articleslist_ress:
        :return:
        """
        for articleslist_res in articleslist_ress:
            channelname = articleslist_res.get("channelname")
            channel_index_id = articleslist_res.get("channelindexid")
            channelid = articleslist_res.get("channelid")
            articlelist_res = articleslist_res.get("channelres")
            if channelname == '关注':
                try:
                    articlelist_json = json.loads(articlelist_res)
                    # 可在下面打印处打断点，查看请求到的数据
                    try:
                        for article in articlelist_json:
                            if isinstance(article, list):
                                # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                                articleparam = InitClass().article_list_fields()
                                articletitle = article[0]['title']
                                articleid = article[0]['id']
                                try:
                                    articleparam["imageurl"] = []
                                except Exception as e:
                                    self.logger.info({e})
                                articleparam["articleid"] = articleid
                                articleparam["articletitle"] = articletitle
                                articleparam["channelname"] = channelname
                                articleparam["channelindexid"] = channel_index_id
                                articleparam["channelid"] = channelid
                                yield articleparam
                    except Exception as e:
                        self.logger.info(f"{e}")
                except Exception as e:
                    self.logger.info(f"{e}")
            else:
                try:
                    articlelist_json = json.loads(articlelist_res)
                    # 可在下面打印处打断点，查看请求到的数据
                    print(articlelist_json)
                    # 若banner图在articlelist_json中则分来开取并给其复制banner = 1
                    try:
                        articlelists = articlelist_json['data']
                        for article in articlelists:
                            # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                            articleparam = InitClass().article_list_fields()
                            articletitle = article['title']
                            articleid = article['id']

                            try:
                                articleparam["imageurl"] = list()
                            except Exception as e:
                                logging.info(f"在文章列表出无法获得封面图{e}")
                            articleparam["articleid"] = articleid
                            articleparam["articletitle"] = articletitle
                            articleparam["channelname"] = channelname
                            articleparam["channelindexid"] = channel_index_id
                            articleparam["channelid"] = channelid
                            yield articleparam
                    except Exception as e:
                        self.logger.info(f"{e}")
                except Exception as e:
                    self.logger.info(f"{e}")

    def getarticleparams(self, articleslist_ress):
        """
        组建请求文章详情所需要的数据体
        :param articleslist_ress:
        :return:
        """
        headers = {
            "Host": "prod.ccmapp.cn",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, lik"
                          "e Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 Html5Plus/1.0",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,en-US;q=0.8",
            "X-Requested-With": "com.cflac.art"
        }
        data = {}
        method = 'get'
        for articleparam in self.analyze_articlelists(articleslist_ress):
            url = f'http://prod.ccmapp.cn/api-cms-production/app/production/pub/content/inf' \
                  f'o?id={articleparam.get("articleid")}&categoryId={articleparam.get("channelid")}&termi' \
                  f'nalType=3&token=&imei=test'

            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
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
                                                        articleurl=articleurl)
            yield [article]

    def analyzearticle(self, articles_res):
        for articleres in articles_res:
            channelname = articleres.get("channelname")
            channel_index_id = articleres.get("channelindexid")
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["channelindexid"] = channel_index_id
            fields["articlecovers"] = imgurl
            try:
                if articleres:
                    articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                    if articlejson['data']:
                        title = articlejson['data']['title']  # 标题
                        source = articlejson['data']['source']  # 来源
                        content = articlejson['data']['content']  # 文章内容
                        pubtime = articlejson['data']['publishTime']  # 发布时间
                        workerid = articlejson['data']['id']
                        url = articlejson['data']["h5URL"]
                        author = articlejson['data']["author"]
                        if 'image' in articlejson['data']:
                            img = list()
                            img.append(articlejson['data']["image"])
                            fields["images"] = img
                        if 'multimediaURL' in articlejson['data']:
                            fields["videos"] = articlejson['data']["multimediaURL"]
                        fields["appname"] = appname
                        fields["platformID"] = self.platform_id
                        fields["title"] = title
                        fields["url"] = url
                        fields["workerid"] = workerid
                        fields["source"] = source
                        fields["content"] = content
                        fields["author"] = author
                        fields["pubtime"] = pubtime
                        fields = InitClass().wash_article_data(fields)
                        yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)


def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = ZhongGuoWenLian(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
