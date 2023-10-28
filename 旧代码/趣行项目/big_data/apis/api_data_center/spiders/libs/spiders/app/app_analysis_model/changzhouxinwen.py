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
"source": null,    默认为 ''
"pubtime": "2年前",   时间类型不对 应为  160*************


"imageurl": {
        "url": "https://cznews.cz001.com.cn/attachment/pic/201712/25/5a40c18c9d2a3.jpg",
        "width": 400,
        "height": 266,
        "size": 12487
    }  应该放入 images  并且只收录 url

"""
import json
import re
import time

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class ChangZhouNews(Appspider):

    @staticmethod
    # 从首页获取
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "https://cznews.cz001.com.cn/api/category/list.php"
        headers = {
            "User-Agent": "CZNews/3.8.4 (Android; MuMu; 6.0.1)",
            "cznews-uuid": "3A810301-9176-4EFF-BDA8-B06D1C7309541",
            "Host": "cznews.cz001.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method)
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
        for channel in channelslists['cate_list']:
            channelid = channel['fid']
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
            # 若有两个请求接口则如下： 例如：banner列表和文章列表时两个请求接口
            url_banner = "https://cznews.cz001.com.cn/api/thread/recommend.php"  # banner请求接口
            url = "https://cznews.cz001.com.cn/api/thread/list.php"
            headers = {
                "User-Agent": 'CZNews/3.8.4 (Android; MuMu; 6.0.1)',
                "cznews-uuid": "3A810301-9176-4EFF-BDA8-B06D1C7309541",
                "Host": "cznews.cz001.com.cn",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
            }
            data = {
                "fid": channelid
            }
            method = 'get'
            data_banner = {
                "fid": channelid
            }
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)

            articlelist_param_banner = InitClass().articlelists_params_fields(url_banner, headers, method, channelname,
                                                                              data=data_banner,
                                                                              banners=1)  # 添加banner请求数据体，或其他接口请求数据
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data)
            yield channel_field, [articlelist_param_banner, articlelist_param]

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
                # 若banner图在articlelist_json中则分来开取并给其复制banner = 1
                try:
                    if 'recommend_list' in articlelist_json or 'thread_list' in articlelist_json:
                        if 'recommend_list' in articlelist_json:
                            articlelists = articlelist_json['recommend_list']
                        else:
                            articlelists = articlelist_json['thread_list']
                        for article in articlelists:
                            # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                            articleparam = InitClass().article_list_fields()
                            articletitle = article['subject']
                            articleid = article['pid']
                            try:
                                articleparam["imageurl"] = [article['thumb_pic']['url']]
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

    def getarticleparams(self, articleslist_ress):
        """
        组建请求文章详情所需要的数据体
        :param articles:
        :return:
        """
        url = 'https://cznews.cz001.com.cn/api/thread/detail.php'
        headers = {
            "User-Agent": "CZNews/3.8.4 (Android; MuMu; 6.0.1)",
            "cznews-uuid": "3A810301-9176-4EFF-BDA8-B06D1C7309541",
            "Host": "cznews.cz001.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Cookie": "PHPSESSID=6805f35bfmablv1ijg33jqfiol",

        }
        method = 'get'
        for articleparam in self.analyze_articlelists(articleslist_ress):
            data = {
                'pid': articleparam.get("articleid"),
                'source': 'android'
            }
            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
            channel_index_id = articleparam.get("channelindexid")
            banner = articleparam.get("banner")
            imgurl = articleparam.get("imageurl")
            videos = [articleparam.get("videos")]
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
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["channelindexid"] = channel_index_id
            fields["imageurl"] = imgurl
            fields["banner"] = banners
            fields["articlecovers"] = imgurl  # 文章的封面，一般为上面get到的字段
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                title = articlejson['subject']  # 标题
                if "origin" in articlejson:
                    source = articlejson['origin']  # 来源
                else:
                    source = ''
                content = articlejson['message']  # 文章内容
                pubtime1 = articlejson['time_past']  # 发布时间
                pubtime =re.findall(r"(\d)天",pubtime1)
                if not pubtime:
                    pubtime = re.findall(r"(\d)小时",pubtime1)
                    if not pubtime:
                        pubtime = re.findall(r"(\d)分",pubtime1)
                        fields["pubtime"] = int(time.time()-int(pubtime[0])*60)*1000
                    else:
                        fields["pubtime"] = int(time.time()-int(pubtime[0])*60*60)*1000
                else:
                    fields["pubtime"] = int(time.time()-int(pubtime[0])*60*60*24)*1000
                workerid = articlejson['pid']
                url = articlejson['share_url']
                author = articlejson["author"]
                commentnum = len(articlejson['comment_list'])
                fields["appname"] = self.newsname
                fields["platformID"] = self.platform_id
                fields["title"] = title
                fields["url"] = url
                fields["workerid"] = workerid
                fields["source"] = source
                fields["content"] = content
                fields["author"] = author
                fields["commentnum"] = commentnum
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = ChangZhouNews(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
