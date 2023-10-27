# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
# from App.appspider_m import Appspider
# from App.initclass import InitClass

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass

# pip install requests-toolbelt
from requests_toolbelt import MultipartEncoder


class Wenyiyun(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "http://wenyizhiku.artnchina.com/microinformation/app/homepage/info"
        # 频道请求头
        headers = {
            "Host": "wenyizhiku.artnchina.com",
            "Content-Length": "44",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Origin": "http://wenyiyun.artnchina.com",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
            "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary46BMpTcX4pjteJTS",
            "Accept": "*/*",
            "Referer": "http://wenyiyun.artnchina.com/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,en-US;q=0.8",
            "Cookie": "groupId=zgwl.microinfo; JSESSIONID=FD65F52EF342E9CB664124DA764D775B",
            "X-Requested-With": "com.artnchina.wenyiyun",
            "Connection": "keep-alive",
        }
        data = {}
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
        for channel in channelslists['data']['topicList']:
            channelcount = channel['blogCount']
            if channelcount < 10:
                continue
            channelid = channel['topicId']
            channelname = channel['title']
            channeltype = channel['hasCarousel']
            channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channeltype)
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
            has_banner = channel.get("channeltype")
            method = 'post'
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            url = "http://wenyizhiku.artnchina.com/microinformation/app/blogtopic/bloglist"
            data = MultipartEncoder(
                fields={
                    'authorId': '',
                    'typeId': channelid,
                    'topicId': channelid,
                    'history': '',
                    'pageSize': '10',
                    'pageNum': '1',
                    'type': 'micro_information'}
            )
            headers = {
                "Host": "wenyizhiku.artnchina.com",
                "Content-Length": "792",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "Origin": "http://wenyiyun.artnchina.com",
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
                "Accept": "*/*",
                "Referer": "http://wenyiyun.artnchina.com/",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,en-US;q=0.8",
                "Cookie": "groupId=zgwl.microinfo; JSESSIONID=FD65F52EF342E9CB664124DA764D775B",
                "X-Requested-With": "com.artnchina.wenyiyun",
                "Connection": "keep-alive",
                "Content-Type": data.content_type
            }
            channel_json = {
                "groupId": "zgwl.microinfo",
                "JSESSIONID": "FD65F52EF342E9CB664124DA764D775B"
            }

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channel_index_id=channel_index_id, data=data,
                                                                       channeljson=channel_json)
            # 若有两个请求接口则如下： 例如：banner列表和文章列表时两个请求接口
            if has_banner:
                url_banner = "http://wenyizhiku.artnchina.com/microinformation/app/blogtopic/carousel"
                data_banner = MultipartEncoder(
                    fields={
                        'topicId': channelid,
                    }
                )
                json_banner = {
                    "groupId": "zgwl.microinfo"
                }
                headers_banner = {
                    "Host": "wenyizhiku.artnchina.com",
                    "Content-Length": "792",
                    "Pragma": "no-cache",
                    "Cache-Control": "no-cache",
                    "Origin": "http://wenyiyun.artnchina.com",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
                    "Accept": "*/*",
                    "Referer": "http://wenyiyun.artnchina.com/",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,en-US;q=0.8",
                    "Cookie": "groupId=zgwl.microinfo; JSESSIONID=FD65F52EF342E9CB664124DA764D775B",
                    "X-Requested-With": "com.artnchina.wenyiyun",
                    "Connection": "keep-alive",
                    "Content-Type": data_banner.content_type
                }
                # banner请求接口
                articlelist_param_banner = InitClass().articlelists_params_fields(url_banner, headers_banner, method,
                                                                                  channelname,
                                                                                  channel_index_id=channel_index_id
                                                                                  ,
                                                                                  data=data_banner,
                                                                                  channeljson=json_banner,
                                                                                  banners=1)
                yield channel_field, [articlelist_param_banner, articlelist_param]
            else:
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
                if banners == 1:
                    try:
                        articlelists = articlelist_json['data']
                        for article in articlelists:
                            articleparam = InitClass().article_list_fields()
                            articletitle = article['title']
                            blogurl = article['blogUrl']
                            start = blogurl.rindex('/')
                            articleid = blogurl[start + 1:]
                            imageurl = article['imgUrl']
                            articleparam["articleid"] = articleid
                            articleparam["articletitle"] = articletitle
                            articleparam["imageurl"] = imageurl
                            articleparam["channelname"] = channelname
                            articleparam["channelID"] = channelid
                            articleparam["articleurl"] = blogurl
                            articleparam["banner"] = banners
                            yield articleparam
                    except Exception as e:
                        print("eee==", e)
                else:
                    try:
                        articlelists = articlelist_json['data']['blogList']
                        for article in articlelists:
                            articleparam = InitClass().article_list_fields()
                            articletitle = article['title']
                            articleid = article['blogId']
                            videos = article["videoUrl"]  # 在此处获取到文章视频url，避免在文章详情获取不到视频链接，数据类型list
                            source = article["source"]  # 在此处获取到文章的来源，避免在文章详情获取不到来源
                            author = article["author"]  # 在此处获取到文章的作者，避免在文章详情获取不到作者
                            commentnum = article["commentCount"]  # 在此处获取到文章的评论数，避免在文章详情获取不到评论数
                            articleparam["video"] = videos  # 此步骤为存储视频url
                            articleparam["source"] = source  # 此步骤为存储文章来源
                            articleparam["author"] = author  # 此步骤为存储作者
                            try:
                                articleparam["imageurl"] = article['imgUrl'][0]
                            except Exception as e:
                                logging.info(f"在文章列表出无法获得封面图{e}")
                            articleparam["articleid"] = articleid
                            articleparam["articletitle"] = articletitle
                            articleparam["channelname"] = channelname
                            articleparam["channelID"] = channelid
                            articleparam["banner"] = banners
                            yield articleparam
                    except Exception as e:
                        print(e, articlelist_json)
            except Exception as e:
                print(e, articlelist_json)

    def getarticleparams(self, articles):
        """
        组建请求文章详情所需要的数据体
        :param articles:
        :return:
        """
        url = 'http://wenyizhiku.artnchina.com/microinformation/app/blog/detail'
        method = 'post'
        detail_josn = {
            "groupId": "zgwl.microinfo"
        }

        for articleparam in articles:
            banner = articleparam.get("banner")
            articleid = articleparam.get("articleid")
            data = MultipartEncoder(
                fields={
                    'blogId': articleid,
                }
            )

            headers = {
                "Host": "wenyizhiku.artnchina.com",
                "Content-Length": "146",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "Origin": "http://wenyiyun.artnchina.com",
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
                "Accept": "*/*",
                "Referer": "http://wenyiyun.artnchina.com/",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,en-US;q=0.8",
                "Cookie": "groupId=zgwl.microinfo",
                "X-Requested-With": "com.artnchina.wenyiyun",
                "Connection": "keep-alive",
                "Content-Type": data.content_type
            }
            videos = url
            channelname = articleparam.get("channelname")
            channel_index_id = articleparam.get("channelindexid")
            channelid = articleparam.get("channelID")
            imgurl = articleparam.get("imageurl")
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
                                                        imageurl=imgurl, data=data, articlejson=detail_josn,
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
            fields["banner"] = banners
            if articleurl:
                fields["url"] = articleurl
            else:
                fields["url"] = url  # 文章的html网址，提取shareurl
            if imgurl:
                fields["articlecovers"] = [imgurl]  # 文章的封面，一般为上面get到的字段
            else:
                fields["articlecovers"] = []
            fields["videocover"] = []  # videocover #文章的视频封面地址
            fields["pubtime"] = 0  # pubtime #文章的发布时间
            fields["updatetime"] = 0  # updatetime #文章的更新时间
            articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
            try:
                articledetail = articlejson['data']['blog']
                title = articledetail['blogTitle']  # 标题
                source = articledetail['source']  # 来源
                content = articledetail['blogContent']  # 文章内容
                workerid = articledetail['blogId']
                author = articledetail["author"]
                commentnum = articledetail["commentCount"]
                createtime = articledetail["createDate"]
                videos = articledetail["videoUrl"]
                # contentType，作品类型，-1未知，1文字，2图文，3视频文，4纯长视频，5纯短视频，6画廊，7纯音频，8短消息（动态、微头条、微博消息等）
                fields["contentType"] = 1
                fields["appname"] = self.newsname
                fields["platformID"] = self.platform_id
                fields["channelindexid"] = channel_index_id
                fields["title"] = title
                fields["workerid"] = workerid
                fields["source"] = source
                fields["content"] = content
                fields["author"] = author
                fields["commentnum"] = commentnum
                fields["createtime"] = createtime

                try:
                    contentvideos = InitClass().get_video(content)
                    if not videos in contentvideos and videos:
                        contentvideos.append(videos)
                    fields["videos"] = contentvideos
                except Exception as e:
                    print("正文无视频")
                try:
                    images = InitClass().get_images(content)
                    fields["images"] = images
                except Exception as e:
                    print("正文无图片")
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print("eeeee=", e)

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Wenyiyun(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
