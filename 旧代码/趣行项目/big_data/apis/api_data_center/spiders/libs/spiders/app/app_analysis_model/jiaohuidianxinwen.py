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
"commentnum": null,   默认为 ''
"content": null,  正文提取失败
"""
import json

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class JiaoHuiDian(Appspider):

    @staticmethod
    # 从首页获取
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "https://jarticle.xhby.net/v3/api/columns"
        # 频道请求头
        headers = {
            "accept": "application/json",
            "cache-control": "no-cache",
            "authorization": "Bearer null",
            "Host": "jarticle.xhby.net",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Cookie": "acw_tc=76b20f7016081070463235460e7242ba8bbfeee598dc2fdaaa7c8ffd0899dd; SERVERID=594b3f5153c1147b39af6db84ed83aab|1608107116|1608104806",
            "User-Agent": "okhttp/3.12.1"
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
        for channel in channelslists['data']['column']:
            channelid = channel['id']
            channelname = channel['title']
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam

    def getarticlelistparams(self, channelsres):
        """
        此方法目的是组建请求文章列页面数据参数，url，headers，data，若以json形式发送数据，则channeljson = channeljson
        :param channelsparams:
        :return:
        """
        channel_num = 0
        self_typeid = self.self_typeid
        platform_id = self.platform_id
        platform_name = self.newsname
        for index in range(0, 3):
            liveurl = f"https://jarticle.xhby.net/v3/api/new_live_articles/{index + 1}"
            liveheaders = {
                "accept": 'application/json',
                'cache-control': 'no-cache',
                'authorization': 'Bearer null',
                'Host': 'jarticle.xhby.net',
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip',
                'Cookie': 'acw_tc=76b20f6016081669830524795e22ceb328b2ae66683266aeb4a369d5601bb7; SERVERID=594b3f5153c1147b39af6db84ed83aab|1608166986|1608166983',
                "User-Agent": "okhttp/3.12.1"
            }
            livedata = {
                'page': '1',
                'limt': "10"
            }
            method = 'get'
            channelname = "直播"
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            articlelist_param = InitClass().articlelists_params_fields(liveurl, liveheaders, method, channelname,
                                                                       channelid=channelname,
                                                                       data=livedata, channel_index_id=channel_index_id)
            yield channel_field, [articlelist_param]
        for channel in self.analyzechannels(channelsres):
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            url = "https://jarticle.xhby.net/v3/api/getColumnArticle"
            headers = {
                "accept": 'application/json',
                'cache-control': 'no-cache',
                'authorization': 'Bearer null',
                'Host': 'jarticle.xhby.net',
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip',
                'Cookie': 'acw_tc=76b20f7016081070463235460e7242ba8bbfeee598dc2fdaaa7c8ffd0899dd; SERVERID=594b3f5153c1147b39af6db84ed83aab|1608107759|1608104806',
                "User-Agent": "okhttp/3.12.1"
            }
            data = {
                'column_id': channelid,
                'page': '10',
                'updateCID': '635c485bc510fde',
                'hide_top': '0',
            }
            method = 'get'
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
            channelid = articleslist_res.get("channelid")
            channel_index_id = articleslist_res.get("channelindexid")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                # 若banner图在articlelist_json中则分来开取并给其复制banner = 1
                try:
                    if "article_top" in articlelist_json['data'].keys() or 'article' in articlelist_json[
                        'data'].keys() or 'data' in articlelist_json['data'].keys():
                        if "article_top" in articlelist_json['data'].keys():
                            articlelists = articlelist_json['data']['article_top']
                            if 'report_articles' in articlelists:
                                articlelists = articlelists['report_articles']
                            for article in articlelists:
                                articleparam = InitClass().article_list_fields()
                                articletitle = article['title']
                                articleid = article['id']
                                try:
                                    if 'pic3' in article:
                                        articleparam["images"] = [article['pic3']]
                                    elif 'pic2' in article:
                                        articleparam["images"] = [article['pic2']]
                                    else:
                                        articleparam["images"] = []
                                except Exception as e:
                                    print(f"在文章列表出无法获得封面图{e}")
                                articleparam["articleid"] = articleid
                                articleparam["articletitle"] = articletitle
                                articleparam["channelname"] = channelname
                                articleparam["banner"] = banners
                                yield articleparam
                        elif "data" in articlelist_json['data']:
                            articlelists = articlelist_json['data']['data']
                            if 'report_articles' in articlelists:
                                articlelists = articlelists['report_articles']
                            for article in articlelists:
                                articleparam = InitClass().article_list_fields()
                                articletitle = article['title']
                                articleid = article['id']
                                channelid = article['column_id']
                                if 'start_time' in article:
                                    start_time = article['start_time']
                                else:
                                    start_time = ''
                                try:
                                    if 'pic3' in article:
                                        articleparam["images"] = [article['pic3']]
                                    elif 'pic2' in article:
                                        articleparam["images"] = [article['pic2']]
                                    else:
                                        articleparam["images"] = None
                                except Exception as e:
                                    print(f"在文章列表出无法获得封面图{e}")
                                articleparam["articleid"] = articleid
                                articleparam["articletitle"] = articletitle
                                articleparam["channelname"] = channelname
                                articleparam["banner"] = banners
                                articleparam['channelid'] = channelid
                                articleparam['start_time'] = start_time
                                yield articleparam
                        else:
                            articlelists = articlelist_json['data']['article']
                            for article in articlelists['data']:
                                # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                                articleparam = InitClass().article_list_fields()
                                articletitle = article['title']
                                articleid = article['id']
                                videos = [article['video_url']]  # 在此处获取到文章视频url，避免在文章详情获取不到视频链接，数据类型list
                                try:
                                    if 'pic3' in article:
                                        articleparam["images"] = [article['pic3']]
                                    elif 'pic2' in article:
                                        articleparam["images"] = [article['pic2']]
                                    else:
                                        articleparam["images"] = None
                                except Exception as e:
                                    print(f"在文章列表出无法获得封面图{e}")
                                articleparam["articleid"] = articleid
                                articleparam["articletitle"] = articletitle
                                articleparam["channelname"] = channelname
                                articleparam["banner"] = banners
                                articleparam["videos"] = videos
                                articleparam["channelid"] = channelid
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
        articlesparam = []
        headers = {
            'accept': 'application/json',
            'cache-control': 'no-cache',
            'authorization': 'Bearer null',
            'Host': 'japi.xhby.net',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'Cookie': 'SERVERID=594b3f5153c1147b39af6db84ed83aab|1608110012|1608104796',
            'User-Agent': 'okhttp/3.12.1',
        }
        method = 'get'
        for articleparam in self.analyze_articlelists(articleslist_ress):
            if articleparam.get('channelid') != '' and articleparam.get('start_time') != '':
                url = f'https://japi.xhby.net/v3/api/getArticleInfo/{articleparam.get("articleid")}?columnId={articleparam.get("channelid")}'
            elif articleparam.get('channelid') != '' and articleparam.get('start_time') == '':
                url = f'https://japi.xhby.net/v3/api/live_info/{articleparam.get("articleid")}?type=1'
            else:
                url = f'https://japi.xhby.net/v3/api/getArticleInfo/{articleparam.get("articleid")} '
            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
            channel_index_id = articleparam.get("channelindexid")
            banner = articleparam.get("banner")
            imgurl = articleparam.get("images")
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
            banners = articleres.get("banner")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["channelindexid"] = channel_index_id
            fields["images"] = imgurl
            fields["banner"] = banners
            fields["articlecovers"] = imgurl  # 文章的封面，一般为上面get到的字段
            fields["images"] = imgurl  # 文章详情内的图片url，一般为列表需遍历获取
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                if 'article' in articlejson['data']:
                    title = articlejson['data']['article']['title']  # 标题
                    if 'source' in articlejson['data']['article'].keys():
                        source = articlejson['data']['article']['source']  # 来源
                    else:
                        source = ''
                    content = articlejson['data']['article']['content']  # 文章内容
                    pubtime = articlejson['data']['article']['created_at']  # 发布时间
                    workerid = articlejson['data']['article']['id']
                    url = articlejson['data']['article']["shareUrl"]
                    author = articlejson['data']['article']['aEditor']
                    if "comments" in articlejson['data']['article']:
                        commentnum = articlejson['data']['article']["comments"]
                    else:
                        commentnum = ''
                else:
                    if len(articlejson['data']['discusses']) > 0:
                        title = articlejson['data']['discusses'][0]['title']  # 标题
                        if 'source' in articlejson['data']['discusses'][0].keys():
                            source = articlejson['data']['discusses'][0]['source']  # 来源
                        else:
                            source = ''
                        content = articlejson['data']['discusses'][0]['content']  # 文章内容
                        pubtime = articlejson['data']['discusses'][0]['updateTime']  # 发布时间
                        workerid = articlejson['data']['discusses'][0]['id']
                        url = ''
                        author = articlejson['data']['discusses'][0]['audit']
                        if "comments" in articlejson['data']['discusses'][0]:
                            commentnum = articlejson['data']['discusses'][0]["comments"]
                        else:
                            commentnum = ''
                fields["appname"] = self.newsname
                fields["platformID"] = self.platform_id
                fields["title"] = title
                fields["url"] = url
                fields["workerid"] = workerid
                fields["source"] = source
                fields["content"] = content
                fields["author"] = author
                fields['channelID'] = channelname
                fields["commentnum"] = commentnum
                fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = JiaoHuiDian(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
