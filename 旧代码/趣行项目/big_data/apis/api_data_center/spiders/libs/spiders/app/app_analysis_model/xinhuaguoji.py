# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class XinHuaGuoJi(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "https://xhgjapi.zhongguowangshi.com/v7_0/wsApi.ashx"
        # 频道请求头
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '398',
            'Host': 'xhgjapi.zhongguowangshi.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.4.2'
        }
        # 频道数据体
        data = {
            'userID': '0',
            'clientMarket': '108',
            'clientType': '400002',
            'clientLongitude': '0.0',
            'clientApp': '104',
            'action': '20001',
            'clientHeight': '1440',
            'clientNet': 'wifi',
            'clientBundleID': 'org.xinhua.xnews_international',
            'languageType': '1',
            'clientModel': 'MuMu',
            'latticeid': '0',
            'clientLable': '490000000245552',
            'clientWidth': '810',
            'clientdDev': '0',
            'clientToken': '40ea7af3db8cf58d5dd8dd8339ac9160',
            'currpage': '1',
            'clientOs': '6.0.1',
            'clientDate': '1607394934',
            'clientLatitude': '0.0',
            'clientVer': '7.2.0'
        }
        # 如果携带的是json数据体,用appjson发送
        # app_json = {}
        # 频道请求方式
        method = "post"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyzechannels(channelsres):
        """
        此方法获取channelid,channelname即可
        :param channelsres:
        :return:
        """
        # 将返回的数据转为json数据
        channelslists = json.loads(channelsres)
        for channel in channelslists['data']:
            channelid = channel['id']
            channelname = channel['name']
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam

    def getarticlelistparams(self, channelsres):
        channel_num = 0
        for channel in self.analyzechannels(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            url_banner = "https://xhgjapi.zhongguowangshi.com/v7_0/wsApi.ashx"  # banner请求接口
            url = 'https://xhgjapi.zhongguowangshi.com/v7_0/wsApi.ashx'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': '411',
                'Host': 'xhgjapi.zhongguowangshi.com',
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip',
                'User-Agent': 'okhttp/3.4.2'
            }
            data = {
                'userID': '0',
                'clientMarket': '108',
                'clientType': '400002',
                'clientLongitude': '0.0',
                'clientApp': '104',
                'areatype': '0',
                'action': '20002',
                'clientHeight': '1440',
                'clientNet': 'wifi',
                'clientBundleID': 'org.xinhua.xnews_international',
                'languageType': '1',
                'clientModel': 'MuMu',
                'latticeid': channelid,
                'clientLable': '490000000245552',
                'clientWidth': '810',
                'clientdDev': '0',
                'clientToken': '40ea7af3db8cf58d5dd8dd8339ac9160',
                'currpage': '1',
                'clientOs': '6.0.1',
                'clientDate': '1607410353',
                'clientLatitude': '0.0',
                'clientVer': '7.2.0'
            }
            method = 'post'
            data_banner = {
                'userID': '0',
                'clientMarket': '108',
                'clientType': '400002',
                'clientLongitude': '0.0',
                'clientApp': '104',
                'areatype': '0',
                'action': '20003',
                'clientHeight': '1440',
                'clientNet': 'wifi',
                'clientBundleID': 'org.xinhua.xnews_international',
                'languageType': '1',
                'clientModel': 'MuMu',
                'latticeid': channelid,
                'clientLable': '490000000245552',
                'clientWidth': '810',
                'clientdDev': '0',
                'clientToken': '40ea7af3db8cf58d5dd8dd8339ac9160',
                'currpage': '1',
                'clientOs': '6.0.1',
                'clientDate': '1607410353',
                'clientLatitude': '0.0',
                'clientVer': '7.2.0'
            }
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
                        articletitle = article['topic']
                        articleid = article['id']
                        try:
                            articleparam["imageurl"] = article['imgList'][0]
                        except Exception as e:
                            self.logger.info(f"{self.newsname}没有获取文章封面图{e}")
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["channelname"] = channelname
                        articleparam["channelindexid"] = channel_index_id
                        articleparam["banner"] = banners
                        yield articleparam
                except Exception as e:
                    self.logger.info(f"提取字段失败{e}")
            except Exception as e:
                self.logger.info(f"{self.newsname}json解析失败{e}")

    def getarticleparams(self, articleslist_ress):
        url = 'https://xhgjapi.zhongguowangshi.com/v7_0/wsApi.ashx'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '398',
            'Host': 'xhgjapi.zhongguowangshi.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.4.2'
        }
        method = 'post'
        for articleparam in self.analyze_articlelists(articleslist_ress):
            data = {
                'id': articleparam.get("articleid"),
                'userID': '0',
                'clientMarket': '108',
                'clientType': '400002',
                'clientLongitude': '0.0',
                'clientApp': '104',
                'action': '20006',
                'showpic': '0',
                'clientHeight': '1440',
                'clientNet': 'wifi',
                'clientBundleID': 'org.xinhua.xnews_international',
                'languageType': '1',
                'clientModel': 'MuMu',
                'clientLable': '490000000245552',
                'clientWidth': '810',
                'clientdDev': '0',
                'clientToken': '40ea7af3db8cf58d5dd8dd8339ac9160',
                'clientOs': '6.0.1',
                'clientDate': '1607412069',
                'clientLatitude': '0.0',
                'docid': articleparam.get("articleid"),
                'clientVer': '7.2.0'
            }
            channelname = articleparam.get("channelname")
            channel_index_id = articleparam.get("channelindexid")
            imgurl = articleparam.get("imageurl")
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                        channel_index_id=channel_index_id)
            yield [article]

    def analyzearticle(self,articles_res):
        for articleres in articles_res:
            channelname = articleres.get("channelname")
            channel_index_id = articleres.get("channelindexid")
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["channelindexid"] = channel_index_id
            fields["platformID"] = self.platform_id
            fields["articlecovers"] = imgurl
            fields["appname"] = appname
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                print(articlejson)
                title = articlejson['data']['topic']  # 标题
                content = articlejson['data']['Content']  # 文章内容
                pubtime = articlejson['data']['releaseDate']  # 发布时间
                workerid = articlejson['data']['id']
                videos = articlejson['data']['videoUrl']
                likenum = articlejson['data']['goodNum']
                commentnum = articlejson['data']['commentCount']
                url = articlejson['data']["mobileHtmlUrl"]
                if "contentImgList" in articlejson["data"].keys():
                    images = list()
                    for image in articlejson["data"]["contentImgList"]:
                        images.append(image["src"])
                    fields["images"] = images
                pubtime = pubtime.replace("/", "-")
                fields["title"] = title
                fields["url"] = url
                fields["videos"] = videos
                fields["likenum"] = likenum
                fields["workerid"] = workerid
                fields["content"] = content
                fields["commentnum"] = commentnum
                fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)


def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = XinHuaGuoJi(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
