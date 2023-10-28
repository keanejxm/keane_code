# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class XinHuaJinRong(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "http://api.xinhua08.com/mobile/index.php?app=mobile&controller=content&action=category&thumbsize=810" \
              "&type=mobile&phonetype=android&version=6.0.0"
        # 频道请求头
        headers = {
            'If-Modified-Since': 'Wed, 09 Dec 2020 01:20:07 GMT+00:00',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': 'api.xinhua08.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
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
        channelslists = json.loads(channelsres)
        channel_num = 1
        if channel_num == 1:
            channelparam = InitClass().channel_fields(0, "推荐")
            yield channelparam
        for channel in channelslists['data']['news']:
            channelid = channel['catid']
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
            # 若有两个请求接口则如下： 例如：banner列表和文章列表时两个请求接口
            # banner请求接口
            url_banner = f"http://api.xinhua08.com/mobile/index.php?app=mobile&controller=content&action=slide&c" \
                         f"atid={channelid}&time=&version=6.0.0&type=mobile&phonetype=android&thumbsize=810"
            url = f"http://api.xinhua08.com/mobile/index.php?app=mobile&controller=content&action=index&cat" \
                  f"id={channelid}&page=1&time=&keyword=&version=6.0.0&type=mobile&phonetype=android&thumbsize=810"

            headers = {
                'Host': 'api.xinhua08.com',
                'Connection': 'Keep-Alive',
                'User-Agent': 'Mozilla/5.0(Linux;U;Android 2.2.1;en-us;Nexus One Build.FRG83) AppleWebKit/55'
                              '3.1(KHTML,like Gecko) Version/4.0 Mobile Safari/533.1'
            }
            data = {}
            method = 'get'
            data_banner = {}
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)

            articlelist_param_banner = InitClass().articlelists_params_fields(url_banner, headers, method, channelname,
                                                                              data=data_banner,
                                                                              channel_index_id=channel_index_id,
                                                                              banners=1)  # 添加banner请求数据体，或其他接口请求数据
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                       channel_index_id=channel_index_id)
            yield channel_field, [articlelist_param_banner, articlelist_param]

    def analyze_articlelists(self, articleslist_ress):
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
            try:
                articlelist_json = json.loads(articlelist_res)
                try:
                    articlelists = articlelist_json['data']
                    for article in articlelists:
                        articleparam = InitClass().article_list_fields()
                        articletitle = article['title']
                        articleid = article['contentid']
                        try:
                            if article['thumb']:
                                articleparam["imageurl"] = article['thumb']
                        except Exception as e:
                            logging.info(f"在文章列表出无法获得封面图{e}")
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["channelname"] = channelname
                        articleparam["channelindexid"] = channel_index_id
                        articleparam["banner"] = banners
                        yield articleparam
                except Exception as e:
                    self.logger.info(f"{self.newsname},提取新闻列表字段失败{e}")
            except Exception as e:
                self.logger.info(f"{self.newsname}json解析新闻列表失败{e}")

    def getarticleparams(self, articleslist_ress):
        """
        组建请求文章详情所需要的数据体
        :param articleslist_ress:
        :return:
        """

        headers = {
            'Host': 'api.xinhua08.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0(Linux;U;Android 2.2.1;en-us;Nexus One Build.FRG83) AppleWebKit/553.1(K'
                          'HTML,like Gecko) Version/4.0 Mobile Safari/533.1'
        }
        data = {}
        method = 'post'
        for articleparam in self.analyze_articlelists(articleslist_ress):
            channelname = articleparam.get("channelname")
            channel_index_id = articleparam.get("channelindexid")
            url = f'http://api.xinhua08.com/mobile/index.php?app=mobile&controller=article&action=content&conte' \
                  f'ntid={articleparam.get("articleid")}&version=6.0.0&type=mobile&phonetype=android&thumbsize=810'
            if channelname == '专题直播':
                url = f'http://api.xinhua08.com/mobile/index.php?app=mobile&controller=link&action=content&conte' \
                      f'ntid={articleparam.get("articleid")}&version=6.0.0&type=mobile&phonetype=android&thumbsize=810'
            # 此处代码不需要改动
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

    def analyzearticle(self, articles_res):
        for articleres in articles_res:
            channelname = articleres.get("channelname")
            channel_index_id = articleres.get("channelindexid")
            appname = articleres.get("appname")
            banners = articleres.get("banner")
            imgurl = articleres.get("imageurl")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["channelindexid"] = channel_index_id
            fields["platformID"] = self.platform_id
            fields["banner"] = banners
            fields["articlecovers"] = imgurl
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                title = articlejson['data']['title']  # 标题
                pubtime = articlejson['data']['published']  # 发布时间
                workerid = articlejson['data']['contentid']
                url = articlejson['data']["shareurl"]

                if articlejson['data']['thumb']:
                    images = list()
                    images.append(articlejson['data']['thumb'])
                    fields["imageurl"] = images

                if "linkto" in articlejson['data']:
                    videos = articlejson['data']["linkto"]
                    fields["videos"] = videos
                if "content" in articlejson['data']:
                    content = articlejson['data']['content']  # 文章内容
                    fields["content"] = content
                if "source" in articlejson['data']:
                    source = articlejson['data']["source"]
                    fields["source"] = source
                fields["appname"] = appname
                fields["title"] = title
                fields["url"] = url
                fields["workerid"] = workerid
                fields["pubtime"] = pubtime
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)


def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = XinHuaJinRong(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
