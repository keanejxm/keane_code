# Author fred
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json

from spiders.libs.spiders.app.appspider_m import Appspider

# import time　　
from spiders.libs.spiders.app.initclass import InitClass


class Haikexinwen(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 获取所有频道url
        url = "https://apinews.haiwainet.cn/column/channels/subscribes/every/list"
        # 频道请求头
        headers = {
            "access_token": "",
            "clientCode": "100002",
            "secret": "ViEL1JR+FvKr8Vbo/Dq8v69VoigfFGZ5XgREL5ymi6TnWgGOT7Aw9P4my1vEcPWo6a0Vrgt97oif0QBVRMrSlGKQGQA6C"
                      "WfcPoYARP8nNYjqrLtae/3qNKNRZP4Oam282VDcB5sCZbsPOJgYSCz9xAZLihERBCnel/mE7sE6ciQ=",
            "autograph": "12345678",
            "X-Tingyun-Id": "kcoKoJaDT54;c=2;r=1596789487;u=7f1cceb0b0316ff51c48b294bc860492::1CE42AC505BE1FB2",
            "Content-Type": "application/json;charset=utf-8",
            "Content-Length": "50",
            "Host": "apinews.haiwainet.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.11.0"
        }
        # 频道数据体
        data = {}
        # 如果携带的是json数据体,用appjson发送
        app_json = {"productVersion": "6.2.20",
                    "productCode": "PRD001"}
        # 频道请求方式
        method = "post"
        app_params = InitClass().app_params(url, headers, method, data=data, appjson=app_json)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        """
        此方法获取channelid,channelname即可
        :param channelsres:
        :return:
        """
        # 将返回的数据转为json数据
        channelslists = json.loads(channelsres)
        channelparams = []
        for channel in channelslists['data']['showList']:
            channelid = channel['channelCode']
            channelname = channel['channelName']
            categoryid = channel['productCode']
            channelparam = InitClass().channel_fields(channelid, channelname, categoryid)
            channelparams.append(channelparam)
        yield channelparams

    def getarticlelistparams(self, channelsparams):
        articleparams = []
        channel_data = list()
        channel_num = 0
        for channel in channelsparams:
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            categoryid = channel.get("categoryid")
            # 获取频道列表
            if channelname == "推荐":
                # 推荐频道列表
                url = "https://apinews.haiwainet.cn/recommend/every/res"
                url_banner = "https://apinews.haiwainet.cn/column/adverts/positions/every/materials"  # banner请求接口
                headers_banner = {
                    "access_token": "",
                    "clientCode": "100002",
                    "secret": "ViEL1JR+FvKr8Vbo/Dq8v69VoigfFGZ5XgREL5ymi6TnWgGOT7Aw9P4my1vEcPWo6a0Vrgt97oif0QBVRMrSl"
                              "GKQGQA6CWfcPoYARP8nNYjqrLtae/3qNKNRZP4Oam282VDcB5sCZbsPOJgYSCz9xAZLihERBCnel/mE7sE6ciQ=",
                    "autograph": "12345678",
                    "X-Tingyun-Id": "kcoKoJaDT54;c=2;r=1827817616;u=7d8899b36fbae21bf19a2b99e96477fe::479CE70CA8C78408",
                    "Content-Type": "application/json;charset=utf-8",
                    "Content-Length": "46",
                    "Host": "apinews.haiwainet.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.11.0",
                }
                headers = {
                    "access_token": "",
                    "clientCode": "100002",
                    "secret": "ViEL1JR+FvKr8Vbo/Dq8v69VoigfFGZ5XgREL5ymi6TnWgGOT7Aw9P4my1vEcPWo6a0Vrgt97oif0QBVRMrS"
                              "lGKQGQA6CWfcPoYARP8nNYjqrLtae/3qNKNRZP4Oam282VDcB5sCZbsPOJgYSCz9xAZLihERBCnel/mE7sE"
                              "6ciQ=",
                    "autograph": "12345678",
                    "X-Tingyun-Id": "kcoKoJaDT54;c=2;r=779520492;u=e82fc801b03bad83cf964d032e709b93::199AD9E4FB7F6418",
                    "Content-Type": "application/json;charset=utf-8",
                    "Content-Length": "124",
                    "Host": "apinews.haiwainet.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.11.0",
                }
                channeljson_header = {
                    "advertCode": 1,
                    "size": 5,
                    "sourceType": "SUT02"
                }
                channeljson = {"latitude": 23.128668333333334,
                               "recommendCode": 1,
                               "deviceId": "008796760196586",
                               "action": 0,
                               "longitude": 113.36772,
                               "mediaId": ""}
                data = {}
                method = 'post'
                self_typeid = self.self_typeid
                platform_id = self.platform_id
                platform_name = self.newsname
                channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                                   self_typeid, channelname,
                                                                                   channel_num)
                channel_data.append(channel_field)
                articlelist_param_banner = InitClass().articlelists_params_fields(url_banner,
                                                                                  headers_banner,
                                                                                  method,
                                                                                  channelname,
                                                                                  data=data,
                                                                                  channeljson=channeljson_header,
                                                                                  banners=1)
                # 添加banner请求数据体，或其他接口请求数据
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           data=data,
                                                                           channeljson=channeljson)

                articleparams.append(articlelist_param_banner)
                articleparams.append(articlelist_param)
            else:
                # 其余频道请求列表url
                url = "https://apinews.haiwainet.cn/search/every/contentSearch"
                headers = {
                    "access_token": "",
                    "clientCode": "100002",
                    "secret": "ViEL1JR+FvKr8Vbo/Dq8v69VoigfFGZ5XgREL5ymi6TnWgGOT7Aw9P4my1vEcPWo6a0Vrgt97oif0QBVRMrSl"
                              "GKQGQA6CWfcPoYARP8nNYjqrLtae/3qNKNRZP4Oam282VDcB5sCZbsPOJgYSCz9xAZLihERBCnel/mE7sE6ciQ=",
                    "autograph": "12345678",
                    "X-Tingyun-Id": "kcoKoJaDT54;c=2;r=1817191217;u=6c79ee1c0d4e8359a005b5c861eb82df::E7E953FDAB3E25E3",
                    "Content-Type": "application/json;charset=utf-8",
                    "Content-Length": "372",
                    "Host": "apinews.haiwainet.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.11.0",

                }
                data = {}
                channeljson = {
                    "size": "10",
                    "contentCollectReturnSwitch": "true",
                    "contentType": "CT001,CT002,CT003,CT004,CT007,CT008",
                    "replyReturnSwitch": "true",
                    "channelId": channelid,
                    "filterBlackSwitch": "true",
                    "contentCountReturnSwitch": "true",
                    "productCode": categoryid,
                    "current": "1",
                    "mediaIsFollowReturnSwitch": "true",
                    "contentUpReturnSwitch": "true",
                    "mediaIsBlackReturnSwitch": "true",
                    "commentReturnSwitch": "true",
                    "sort": "createTime"
                }
                method = 'post'
                self_typeid = self.self_typeid
                platform_id = self.platform_id
                platform_name = self.newsname
                channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                                   self_typeid, channelname,
                                                                                   channel_num)
                channel_data.append(channel_field)
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                           channeljson=channeljson)
                articleparams.append(articlelist_param)
        yield [channel_data, articleparams]

    def analyze_articlelists(self, articleslist_ress):
        articlesparams = []
        for articleslist_res in articleslist_ress:
            banners = articleslist_res.get("banner")
            channelname = articleslist_res.get("channelname")
            articlelist_res = articleslist_res.get("channelres")
            try:
                articlelist_json = json.loads(articlelist_res)
                try:
                    articlelists = articlelist_json['data']
                    if banners == 1:
                        articlelists = articlelists["contentMaterialList"]
                    for article in articlelists:
                        print(article)
                        articleparam = InitClass().article_list_fields()
                        if banners == 1:
                            articleparam["banner"] = banners
                            try:
                                # banner 用fileCode
                                articleid = article['fileCode']
                                articleparam["articleid"] = articleid
                            except Exception as e:
                                self.logger.info(f"{self.newsname}获取banner数据失败{e}")
                        else:
                            try:
                                # 普通新闻 用id
                                articleid = article['id']
                                articleparam["articleid"] = articleid
                            except Exception as e:
                                self.logger.info(f"{self.newsname}没有获取到新闻id{e}")
                        try:
                            articletitle = article['title']
                            articleparam["articletitle"] = articletitle
                        except Exception as e:
                            self.logger.info(f"{self.newsname}没有获取到新闻标题{e}")

                        try:
                            imageurl = article['cover']
                            articleparam["imageurl"] = imageurl
                        except Exception as e:
                            self.logger.info(f"{self.newsname}进入下一步获取新闻封面{e}")
                            try:
                                imageurl = article['horizontal']
                                articleparam["imageurl"] = imageurl
                            except Exception as e:
                                self.logger.info(f"{self.newsname}没有获取到新闻封面{e}")
                        articleparam["channelname"] = channelname
                        articlesparams.append(articleparam)
                except Exception as e:
                    self.logger.info(f"{self.newsname}提取文章内容失败{e}")
            except Exception as e:
                self.logger.info(f"{self.newsname}json解析失败{e}")
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articlesparam = []
        # 请求详情url
        url = 'https://apinews.haiwainet.cn/search/every/contentSearch'
        headers = {
            "access_token": "",
            "clientCode": "100002",
            "secret": "ViEL1JR+FvKr8Vbo/Dq8v69VoigfFGZ5XgREL5ymi6TnWgGOT7Aw9P4my1vEcPWo6a0Vrgt97oif0QBVRMrSlGKQGQA6CW"
                      "fcPoYARP8nNYjqrLtae/3qNKNRZP4Oam282VDcB5sCZbsPOJgYSCz9xAZLihERBCnel/mE7sE6ciQ=",
            "autograph": "12345678",
            "X-Tingyun-Id": "kcoKoJaDT54;c=2;r=1950649457;u=7d8899b36fbae21bf19a2b99e96477fe::479CE70CA8C78408",
            "Content-Type": "application/json;charset=utf-8",
            "Content-Length": "349",
            "Host": "apinews.haiwainet.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.11.0",
        }
        method = 'post'
        for articleparam in articles:
            data = {}
            detailjson = {
                "word": "",
                "size": "10",
                "ids": articleparam.get("articleid"),
                "contentCollectReturnSwitch": "true",
                "contentType": "CT001,CT002,CT003,CT004,CT007,CT008",
                "replyReturnSwitch": "true",
                "breakingReturnSwitch": "true",
                "contentCountReturnSwitch": "true",
                "productCode": "PRD001",
                "current": "1",
                "mediaIsFollowReturnSwitch": "true",
                "contentUpReturnSwitch": "true",
                "mediaIsBlackReturnSwitch": "false",
                "commentReturnSwitch": "true"
            }
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
            # 若APP有关于时间的反爬加sleeptime = 1，若发送为json数据体，则添加articlejson = detailJson
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                        articlejson=detailjson,sleeptime=1,
                                                        videourl=videos, videocover=videocover, pubtime=pubtime,
                                                        createtime=createtime, updatetime=updatetime,
                                                        source=source, author=author, likenum=likenum,
                                                        commentnum=commentnum, sharenum=sharenum, readnum=readnum,
                                                        articleurl=articleurl, banners=banner)
            articlesparam.append(article)
        yield articlesparam

    def analyzearticle(self, articles_res):
        for articleres in articles_res:
            channel_name = articleres.get("channelname")
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            banners = articleres.get("banner")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channel_name
            fields["articlecovers"] = imgurl
            fields["appname"] = appname
            fields["banner"] = banners
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                data = articlejson['data'][0]
                print(data)
                title = data['title']  # 标题
                try:
                    source = data['origin']['mediaName']  # 来源
                    fields["source"] = source
                except Exception as e:
                    self.logger.info(f"{self.newsname}没有获取到文章来源{e}")
                content = data['content']  # 文章内容
                pubtime = data['releaseTimeStamp']  # 发布时间
                createtime = data['createTimeStamp']  # 创建时间
                updatetime = data['updateTimeStamp']  # 更新时间
                viewnum = data['viewCount']  # 阅读数
                author = data['author']  # 作者
                workerid = data['id']  # 新闻id
                url = data['shareUrl']  # 分享url
                cover = data['cover']  # 封面图
                fields["title"] = title
                fields["url"] = url
                fields["workerid"] = workerid
                fields["content"] = content
                fields["pubtime"] = pubtime
                fields["createtime"] = createtime
                fields["updatetime"] = updatetime
                fields["readnum"] = viewnum
                fields["author"] = author
                fields["images"] = cover

                try:
                    video = data['video'][0]
                    fields["videos"] = video['url']  # 视频
                    fields["width"] = video['width']  # 视频宽
                    fields["height"] = video['height']  # 视频高
                except Exception as e:
                    self.logger.info(f"{self.newsname}此文章没有视频{e}")
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print("e data=", e)


def fetch_batch(appname, logger, platform_id, self_typeid):
    appspider = Haikexinwen(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    appparams = appspider.get_app_params()
    channelsres = appspider.getchannels(appparams.__next__())
    channelsparams = appspider.analyze_channel(channelsres.__next__())
    articlelistparameses = appspider.getarticlelistparams(channelsparams.__next__())
    articlelistparamess = list()
    for articlelistparamesss in articlelistparameses:
        articlelistparamess = articlelistparamesss
    channel_data = articlelistparamess[0]
    articlelistparames = articlelistparamess[1]
    articleslistsres = appspider.getarticlelists(articlelistparames)
    articles = appspider.analyze_articlelists(articleslistsres.__next__())
    articleparams = appspider.getarticleparams(articles.__next__())
    articlesres = appspider.getarticlehtml(articleparams.__next__())
    app_data = appspider.analyzearticle(articlesres.__next__())
    article_retu = {
        "code": "1",
        "msg": "json",
        "data": dict(),
    }
    data_dict = dict()
    data_dict["channels"] = channel_data
    articles_list = list()
    topics_list = list()
    for data in app_data:
        if "works" in data["data"]:
            articles_list.append(data["data"]["works"])
        elif "topic" in data["data"]:
            topics_list.append(data["data"]["topic"])
        else:
            pass
    article_retu["data"]["topics"] = topics_list
    article_retu["data"]["worksList"] = articles_list
    yield article_retu


def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Haikexinwen(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
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
