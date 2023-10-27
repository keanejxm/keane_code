# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
"""
"articlecovers": "",   默认应为 []
"images": "",       默认应为 []
"videos": "",       默认应为 []
"videocover": "",       默认应为 []
"pubtime": "2018-12-10T13:31:57+0800",   时间类型不对 应为  160*************
"author": null, 默认为  ’‘
"source": null, 默认为  ’‘

"content": "http://zxh5.peopletech.cn/#/detail/normal/7906",  应该为正文
"""
import json

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class Lingdaoliuyanban(Appspider):

    @staticmethod
    # 从首页获取
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "http://zxapi.peopletech.cn/api/v2/menus"
        # 频道请求头
        headers = {
            "Content-Type": "application/json",
            "Host": "zxapi.peopletech.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
        }
        # 频道数据体
        data = {
            "platform": "android",
            "clientVersionCode": "318",
            "deviceOs": "6.0.1",
            "pjCode": "dfldly_10_201707",
            "device_size": "810.0x1440.0",
            "clientVersion": "3.2.8",
            "deviceModel": "Netease-MuMu",
            "udid": "010000000308435",
            "channel": "xiaomi",
        }
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
        # 将返回的数据转为json数据
        channelslists = json.loads(channelsres)
        for channel in channelslists['items']:
            channelid = channel['categoryId']
            channelname = channel['name']
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam

    def getarticlelistparams(self, channelsres):
        """
        此方法目的是组建请求文章列页面数据参数，url，headers，data，若以json形式发送数据，则channeljson = channeljson
        :param channelsparams:
        :return:
        """
        headers = {
            "Content-Type": "application/json",
            "Host": "zxapi.peopletech.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
        }
        method = 'get'
        channel_num = 0
        for channel in self.analyzechannels(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            # 若有两个请求接口则如下： 例如：banner列表和文章列表时两个请求接口
            url = f"http://zxapi.peopletech.cn/api/v2/articles/{channelid}"
            data = {
                "platform": "android",
                "size": "20",
                "clientVersionCode": "318",
                "deviceOs": "6.0.1",
                "pjCode": "dfldly_10_201707",
                "device_size": "810.0x1440.0",
                "clientVersion": "3.2.8",
                "deviceModel": "Netease-MuMu",
                "udid": "010000000308435",
                "channel": "xiaomi",
            }
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
            channelname = articleslist_res.get("channelname")
            channel_index_id = articleslist_res.get("channelindexid")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                try:
                    articlelists = articlelist_json['item']['list']
                    if "head" in articlelist_json['item']:
                        bannerslists = articlelist_json['item']['head']
                        for bannerarticle in bannerslists:
                            articleparam = InitClass().article_list_fields()
                            articletitle = bannerarticle['title']
                            articleid = bannerarticle['articleId']
                            banner = 1
                            if 'medias' in bannerarticle.keys():
                                articleparam["videos"] = bannerarticle['medias'][0]['resources'][0]['url']
                            else:
                                articleparam["videos"] = []
                            try:
                                if 'imageUrl' in bannerarticle:
                                    articleparam["images"] = bannerarticle['imageUrl']
                                else:
                                    articleparam["images"] = None
                            except Exception as e:
                                print(f"在文章列表出无法获得封面图{e}")
                            articleparam["articleid"] = articleid
                            articleparam["articletitle"] = articletitle
                            articleparam["channelname"] = channelname
                            articleparam["channelindexid"] = channel_index_id
                            articleparam["banner"] = banner
                            yield articleparam
                    for article in articlelists:
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        articleparam = InitClass().article_list_fields()
                        articletitle = article['title']
                        articleid = article['id']
                        if 'medias' in bannerarticle:
                            articleparam["videos"] = bannerarticle['medias'][0]['resources'][0]['url']
                        else:
                            articleparam["videos"] = []
                        try:
                            if 'imageUrl' in article:
                                articleparam["images"] = article['imageUrl']
                            else:
                                articleparam["images"] = []
                        except Exception as e:
                            print(f"在文章列表出无法获得封面图{e}")
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["channelname"] = channelname
                        articleparam["channelindexid"] = channel_index_id
                        articleparam["banner"] = banners
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
        headers = {
            "Content-Type": "application/json",
            "Host": "zxapi.peopletech.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
        }
        data = {
            "platform": "android",
            "clientVersionCode": "318",
            "deviceOs": "6.0.1",
            "pjCode": "dfldly_10_201707",
            "device_size": "810.0x1440.0",
            "clientVersion": "3.2.8",
            "deviceModel": "Netease-MuMu",
            "udid": "010000000308435",
            "channel": "xiaomi",
        }
        method = 'get'
        for articleparam in self.analyze_articlelists(articleslist_ress):
            url = f'http://zxapi.peopletech.cn/api/v2/articles/detail/{articleparam.get("articleid")}'
            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
            channel_index_id = articleparam.get("channelindexid")
            banner = articleparam.get("banner")
            imgurl = articleparam.get("images")
            videos = []
            videocover = []
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
                                                        articleurl=articleurl, banners=banner,channel_index_id=channel_index_id)
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
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["channelindexid"] = channel_index_id
            fields["images"] = imgurl
            fields["banner"] = banners
            fields["articlecovers"] = imgurl  # 文章的封面，一般为上面get到的字段
            fields["images"] = imgurl  # 文章详情内的图片url，一般为列表需遍历获取
            fields["videocover"] = imgurl  # 文章的视频封面地址
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                print(articlejson)
                if "item" in articlejson:
                    title = articlejson['item']['title']  # 标题
                    if "source" in articlejson['item']:
                        source = articlejson['item']['source']
                    else:
                        source = ''
                    if "content" in articlejson['item']:
                        content = articlejson['item']['content']
                        if len(videos) < 1:
                            fields["videos"] = InitClass.get_video(content)
                    else:
                        content = ''
                    pubtime = articlejson['item']['date']  # 发布时间
                    workerid = articlejson['item']['id']
                    url = articlejson['item']["shareUrl"]
                    if "author" in articlejson['item']:
                        author = articlejson['item']['author']
                    else:
                        author = ''
                    commentnum = articlejson['item']["comments"]
                    fields["appname"] = self.newsname
                    fields["platformID"] = self.platform_id
                    fields["title"] = title
                    fields["url"] = url
                    fields["workerid"] = workerid
                    fields["source"] = source
                    fields["content"] = content
                    fields["author"] = author
                    fields["commentnum"] = commentnum
                    fields["pubtime"] = InitClass().date_time_stamp(InitClass().format_date(pubtime))
                    fields = InitClass().wash_article_data(fields)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Lingdaoliuyanban(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
