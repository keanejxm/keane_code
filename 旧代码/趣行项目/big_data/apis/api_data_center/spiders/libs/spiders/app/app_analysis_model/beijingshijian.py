# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import time
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class BeijingshijianNews(Appspider):

    @staticmethod
    # 从首页获取
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "https://app.api.btime.com/channel/getChannel"
        headers = {
            'Host': 'app.api.btime.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.9.0',

        }
        data = {
            'protocol': '4',
            'push_switch': '1',
            'token': 'e0fb5784410cc184345a22632a803240',
            'carrier': '',
            'push_id': '5766a4b37307c04998dea233dcf9251f',
            'os_type': 'Android',
            'timestamp': int(time.time()),
            'net': 'WIFI',
            'os': 'V417IR release-keys',
            'browse_mode': '1',
            'os_ver': '23',
            'sid': '',
            'location_citycode': 'local_110000',
            'src': 'lx_android',
            'channel': 'xiaomi',
            'ver': '60301',
            'sign': "619a157",
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
        channelslists = json.loads(channelsres)
        for channel in channelslists['data']['like']:
            channelid = channel['cid']
            channelname = channel['cname']
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam

    def getarticlelistparams(self, channelsres):
        """
        此方法目的是组建请求文章列页面数据参数，url，headers，data，若以json形式发送数据，则channeljson = channeljson
        :param channelsparams:
        :return:
        """
        url = "https://app.api.btime.com/news/list"
        method = 'get'
        headers = {
            'Host': 'app.api.btime.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.9.0',
        }
        channel_num = 0
        for channel in self.analyzechannels(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            data = {
                'protocol': '3',
                'cid': channelid,
                'cname': channelname,
                'is_paging': '1',
                'offset': '0',
                'refresh_type': '1',
                'refresh_count': '1',
                'last': '',
                'refresh_total': '1',
                'push_switch': '1',
                'token': 'e0fb5784410cc184345a22632a803240',
                'carrier': '',
                'push_id': '5766a4b37307c04998dea233dcf9251f',
                'os_type': 'Android',
                'timestamp': int(time.time()),
                'net': 'WIFI',
                'os': 'V417IR release-keys',
                'browse_mode': '1',
                'os_ver': '23',
                'sid': '',
                'location_citycode': 'local_110000',
                'src': 'lx_android',
                'channel': 'xiaomi',
                'ver': '60301',
                'sign': 'c778b0c',
            }
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                       channelid=channelid,
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
            channelid = articleslist_res.get("channelid")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                # 若banner图在articlelist_json中则分来开取并给其复制banner = 1
                try:
                    articlelists = articlelist_json['data']['data']
                    for article in articlelists:
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        if articlelists.index(article) == 0 and article['module'] != 44:
                            if 'news' in article['data'].keys():
                                listdata = article['data']['news']
                                for articlecontent in listdata:
                                    articleparam = InitClass().article_list_fields()
                                    articleid = articlecontent['gid']
                                    articletitle = articlecontent['data']['title']
                                    try:
                                        articleparam["images"] = articlecontent['data']['covers']
                                    except Exception as e:
                                        print(f"在文章列表出无法获得封面图{e}")
                                    articleparam["articleid"] = articleid
                                    articleparam["articletitle"] = articletitle
                                    articleparam["channelname"] = channelname
                                    articleparam["channel_index_id"] = channel_index_id
                                    articleparam["channelid"] = channelid
                                    articleparam["banner"] = 1
                                    yield articleparam
                            else:
                                listdata = article['data']
                                articleparam = InitClass().article_list_fields()
                                articletitle = listdata['title']
                                articleid = listdata["gid"]
                                try:
                                    articleparam["images"] = listdata['covers']
                                except Exception as e:
                                    print(f"在文章列表出无法获得封面图{e}")
                                articleparam["articleid"] = articleid
                                articleparam["articletitle"] = articletitle
                                articleparam["channelname"] = channelname
                                articleparam["channel_index_id"] = channel_index_id
                                articleparam["channelid"] = channelid
                                articleparam["banner"] = 1
                                yield articleparam
                        else:
                            if 'news' in article['data']:
                                listdata = article['data']['news']
                                for articlecontent in listdata:
                                    print(article)
                                    articleparam = InitClass().article_list_fields()
                                    articleid = articlecontent['gid']
                                    articletitle = articlecontent['data']['title']
                                    try:
                                        articleparam["images"] = articlecontent['data']['covers']
                                    except Exception as e:
                                        print(f"在文章列表出无法获得封面图{e}")
                                    articleparam["articleid"] = articleid
                                    articleparam["articletitle"] = articletitle
                                    articleparam["channelname"] = channelname
                                    articleparam["channel_index_id"] = channel_index_id
                                    articleparam["channelid"] = channelid
                                    articleparam["banner"] = 1
                                    yield articleparam
                            else:
                                listdata = article['data']
                                articleparam = InitClass().article_list_fields()
                                articleid = article['gid']
                                articletitle = listdata['title']
                                try:
                                    articleparam["images"] = listdata['covers']
                                except Exception as e:
                                    print(f"在文章列表出无法获得封面图{e}")
                                articleparam["articleid"] = articleid
                                articleparam["articletitle"] = articletitle
                                articleparam["channelname"] = channelname
                                articleparam["channel_index_id"] = channel_index_id
                                articleparam["channelid"] = channelid
                                articleparam["banner"] = 0
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
        url = 'https://app.api.btime.com/trans'
        headers = {
            'Content-Length': '0',
            'Host': 'app.api.btime.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.9.0',
        }
        method = 'post'
        for articleparam in self.analyze_articlelists(articleslist_ress):
            data = {
                'ver': '60301',
                'token': 'e0fb5784410cc184345a22632a803240',
                'timestamp': int(time.time()),
                'src': 'lx_android',
                'sign': '9a3a36c',
                'sid': '',
                'push_switch': '1',
                'push_id': '5766a4b37307c04998dea233dcf9251f',
                'protocol': '2',
                'os_ver': '23',
                'os_type': 'Android',
                'os': 'V417IR release-keys',
                'net': 'WIFI',
                'm': 'btime',
                'location_citycode': 'local_110000',
                'gid': articleparam.get('articleid'),
                'fmt': 'json',
                'channel': 'xiaomi',
                'carrier': '',
                'browse_mode': '1',
            }
            if articleparam.get('articletype') == 3:
                url = 'https://app.api.btime.com/btv/relevant'
                method = 'get'
                headers = {
                    'Host': 'app.api.btime.com',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                    'User-Agent': 'okhttp/3.9.0',
                }
            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
            channel_index_id = articleparam.get("channelindexid")
            channelid = articleparam.get("channelid")
            banner = articleparam.get("banner")
            imgurl = articleparam.get("images")
            videos = articleparam.get("videos")
            videocover = articleparam.get("videocover")
            pubtime = articleparam.get("pubtime")
            createtime = articleparam.get("createtime")
            updatetime = articleparam.get("updatetime")
            source = articleparam.get("source")
            author = articleparam.get("author")
            commentnum = articleparam.get("commentnum")
            sharenum = articleparam.get("sharenum")
            readnum = articleparam.get("readnum")
            articleurl = articleparam.get("articleurl")
            # 若APP有关于时间的反爬加sleeptime = 1，若发送为json数据体，则添加articlejson = articlejson
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                        videourl=videos, videocover=videocover, pubtime=pubtime,
                                                        createtime=createtime, updatetime=updatetime,
                                                        source=source, author=author, likenum=channelid,
                                                        commentnum=commentnum, sharenum=sharenum, readnum=readnum,
                                                        articleurl=articleurl, banners=banner,
                                                        channel_index_id=channel_index_id)
            yield [article]

    def analyzearticle(self,articles_res):
        for articleres in articles_res:
            channelname = articleres.get("channelname")
            channel_index_id = articleres.get("channelindexid")
            channelid = articleres.get("likenum")
            imgurl = articleres.get("images")
            appname = articleres.get("appname")
            banners = articleres.get("banner")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["channelindexid"] = channel_index_id
            fields["channelID"] = channelid
            fields["banner"] = banners
            fields["images"] = imgurl  # 文章详情内的图片url，一般为列表需遍历获取
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                htmlcoentent = ''
                if 'video' in articlejson['data']:
                    if 'content' in articlejson['data']:
                        for text in articlejson['data']['content']:
                            if text['type'] == 'txt':
                                htmlcoentent += f"<p>{text['value']}</p>"
                            elif text['type'] == 'img':
                                htmlcoentent += f"<p><img src='{text['value']}' alt=''/><span></span></p>"

                            content = f"<div class='content'>{htmlcoentent}</div>"  # 文章内容
                            fields["content"] = content
                            videos = InitClass.get_video(content)
                            images = InitClass.get_images(content)
                            fields["videos"] = videos
                            fields["images"] = images
                    title = articlejson['data']['title']  # 标题
                    source = articlejson['data']['source']  # 来源
                    imgurl = articlejson['data']['image_urls']
                    pubtime = articlejson['data']['time']  # 发布时间
                    workerid = articlejson['data']['gid']
                    url = articlejson['data']["url"]
                    author = articlejson['data']["news_edit_user"]
                    if "comments" in articlejson['data'].keys():
                        commentnum = articlejson['data']["comments"]
                    else:
                        commentnum = '0'
                    fields["appname"] = self.newsname
                    fields["platformID"] = self.platform_id
                    fields["title"] = title
                    fields["url"] = url
                    fields["images"] = imgurl
                    fields["workerid"] = workerid
                    fields["source"] = source
                    fields["author"] = author
                    fields["commentnum"] = commentnum
                    try:
                        fields["pubtime"] = int(pubtime) * 1000
                    except Exception as e:
                        print(e)
                        fields["pubtime"] = int(pubtime) * 1000
                    fields = InitClass().wash_article_data(fields)
                    yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = BeijingshijianNews(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
