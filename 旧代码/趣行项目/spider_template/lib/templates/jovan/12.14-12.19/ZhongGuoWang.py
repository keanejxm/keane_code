# Author Keane
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json

from app_templates.lib.templates.appspider_m import Appspider

# import time
from app_templates.lib.templates.initclass import InitClass


class ZhongGuoWang(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "https://k1.m.china.com.cn/app/reco?"
        # 频道请求头
        headers = {
            'cookie': '',
            'UPVOTE-VERSION': '0.1',
            'mac': '02:00:00:00:00:00',
            'channelName': '%E8%85%BE%E8%AE%AF%E5%BA%94%E7%94%A8%E5%AE%9D',
            'phoneSystemVersion': '6.0.1',
            'devicelanuage': 'zh',
            'imei': '500000000049572',
            'adId': '',
            'localVersion': '1.11.9',
            'custom': '{"adId":"","ak":"0102670109","appId":"chinaApp","appLanguage":"zh","appType":"android","appVersionCode":"1679","appVersionStr":"1.11.9","buildType":"dev","bundleId":"com.witmob.newsdigest","channel":"%E8%85%BE%E8%AE%AF%E5%BA%94%E7%94%A8%E5%AE%9D","deviceId":"500000000049572","deviceString":"x86","globalApiVersion":"1","idfa":"","idfv":"","imei":"500000000049572","mac":"02:00:00:00:00:00","os":"Android","osLanguage":"zh","osType":"Android","osVersion":"6.0.1","phoneName":"Android","platform":"chinaAPP","telephonyManager":"","userId":"","wifi":"1"}',
            'ostype': 'Android',
            'deviceString': 'x86',
            'Authorization': '',
            'Accept-Encoding': '',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': 'k1.m.china.com.cn',
            'Connection': 'Keep-Alive',
        }
        # 频道数据体
        data = {
            "language": "zh",
            "interfaceVersion": "3",
            "appId": "chinaApp",
            "appId": "chinaApp"
        }
        # 如果携带的是json数据体,用appjson发送
        # app_json = {}
        # 频道请求方式
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        # app_params = InitClass().app_params(url, headers, method, data = data ,appjson=app_json)
        yield app_params

    @staticmethod
    def analyzechannels(channelsres):
        """
        此方法获取channelid,channelname即可
        :param channelsres:
        :return:
        """
        print(channelsres)
        # 将返回的数据转为json数据
        channelslists = json.loads(channelsres)
        # channelslists = json.loads(json.dumps(channelsres,indent=4,ensure_ascii=False))
        print(channelslists)
        temp = channelslists['strong'] + channelslists['subscribed'] + channelslists['noSubscribed']
        channelparams = []
        for channel in temp:
            channelid = channel['menuId']
            channelname = channel['title']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistsparams(channelsparams):
        articleparams = []
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            url = "https://k1.m.china.com.cn/scene/query/list"
            headers = {
                'cookie': '',
                'UPVOTE-VERSION': '0.1',
                'mac': '02:00:00:00:00:00',
                'channelName': '%E8%85%BE%E8%AE%AF%E5%BA%94%E7%94%A8%E5%AE%9D',
                'phoneSystemVersion': '6.0.1',
                'devicelanuage': 'zh',
                'imei': '500000000049572',
                'adId': '',
                'localVersion': '1.11.9',
                'custom': '{"adId":"","ak":"0102670109","appId":"chinaApp","appLanguage":"zh","appType":"android","appVersionCode":"1679","appVersionStr":"1.11.9","buildType":"dev","bundleId":"com.witmob.newsdigest","channel":"%E8%85%BE%E8%AE%AF%E5%BA%94%E7%94%A8%E5%AE%9D","deviceId":"500000000049572","deviceString":"x86","globalApiVersion":"1","idfa":"","idfv":"","imei":"500000000049572","mac":"02:00:00:00:00:00","os":"Android","osLanguage":"zh","osType":"Android","osVersion":"6.0.1","phoneName":"Android","platform":"chinaAPP","telephonyManager":"","userId":"","wifi":"1"}',
                'ostype': 'Android',
                'deviceString': 'x86',
                'Authorization': '',
                'Accept-Encoding': '',
                'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
                'Host': 'k1.m.china.com.cn',
                'Connection': 'Keep-Alive',
            }
            data = {
                'columnId': channelid,
                'page': '1',
                'size': '20'
            }
            # 如果携带的是json数据体,用appjson发送
            app_json = 'appId=chinaApp&'
            method = 'post'
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                       channeljson=app_json)
            articleparams.append(articlelist_param)
        yield articleparams

    @staticmethod
    def analyze_articlelists(articleslist_ress):
        articlesparams = []
        for articleslist_res in articleslist_ress:
            channelname = articleslist_res.get("channelname")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                print(articlelist_json)
                try:
                    articlelists = articlelist_json['list']
                    # articlelistsurl = articlelist_json['data']['listUrl']
                    for article in articlelists:
                        print(article)
                        articleparam = InitClass().article_list_fields()
                        try:
                            articletitle = article['title']
                            articleparam["articletitle"] = articletitle
                        except Exception as e:
                            print(e)
                        try:
                            articleid = article['articleId']
                            articleparam["articleid"] = articleid
                        except Exception as e:
                            print(e)
                        try:
                            if len(article['images']) > 0:
                                imageurl = article['images'][0]
                                articleparam["imageurl"] = imageurl
                        except Exception as e:
                            print(e)
                            # print(title,imgurl,articleurl)
                        try:
                            videoUrl = article['videoUrl']
                            articleparam["videos"] = videoUrl
                        except Exception as e:
                            print(e)
                        try:
                            videoImage = article['videoImage']
                            articleparam["videocover"] = videoImage
                        except Exception as e:
                            print(e)
                        articlesparams.append(articleparam)
                except Exception as e:
                    print(e, articlelist_json)
            except Exception as e:
                print(e, articlelist_json)
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articlesparam = []
        url = 'https://m.china.com.cn/app/article.do?'
        headers = {
            'Host': 'm.china.com.cn',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'Sec-Fetch-User': '?1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': '__guid=144678377.918721679172048600.1607316952173.0317; UM_distinctid=1763b8e58da6b8-0d080743792d13-376b4502-1fa400-1763b8e58db6df; CNZZDATA1262131232=1728708589-1607316188-http%253A%252F%252Fapp.china.com.cn%252F%7C1607316188; cn_1262131232_dplus=%7B%22distinct_id%22%3A%20%221763b8e58da6b8-0d080743792d13-376b4502-1fa400-1763b8e58db6df%22%2C%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201607316957%2C%22initial_view_time%22%3A%20%221607316188%22%2C%22initial_referrer%22%3A%20%22http%3A%2F%2Fapp.china.com.cn%2F%22%2C%22initial_referrer_domain%22%3A%20%22app.china.com.cn%22%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201607316957%7D; monitor_count=2',
        }
        method = 'get'
        for articleparam in articles:
            data = {
                'articleId': articleparam.get("articleid"),
                'menuId': articleparam.get("channelid"),
                'appId': 'chinaApp',
            }
            channelname = articleparam.get("channelname")
            imgurl = articleparam.get("imageurl")
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data)
            articlesparam.append(article)
        yield articlesparam

    @staticmethod
    def analyzearticles(articles_res):
        for articleres in articles_res:
            channelname = articleres.get("channelname")
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["imageurl"] = imgurl
            fields["appname"] = appname
            try:
                print(articleres)
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                print(articlejson)
                title = articlejson['info']['title']  # 标题
                source = articlejson['info']['sourceName']  # 来源
                content = articlejson['info']['content']  # 文章内容
                pubtime = articlejson['info']['pubTime']  # 发布时间
                workerid = articlejson['info']['articleId']  # 文章id
                url = articlejson['info']['artUrl']  # 网站的url
                images = articlejson['info']['images']  # 图片地址
                video = articlejson['info']['videoUrl']  # 视频的url
                videos = list()
                videos.append(video)  # 视频的url
                videocover = articlejson['info']['videoImage']  # 视频封面
                author = articlejson['info']['editor']  # 视频封面
                fields["title"] = title
                fields["url"] = url
                fields["workerid"] = workerid
                fields["source"] = source
                fields["content"] = content
                fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                fields["articlecovers"] = imgurl
                fields["images"] = images
                fields["articlecovers"] = imgurl
                fields["videos"] = videos
                fields["videocover"] = videocover
                fields["author"] = author
                print(json.dumps(fields, indent=4, ensure_ascii=False))
            except Exception as e:
                print(e)

    def run(self):
        appparams = self.get_app_params()
        channelsres = self.getchannels(appparams.__next__())
        channelsparams = self.analyzechannels(channelsres.__next__())
        articleparams = self.getarticlelistsparams(channelsparams.__next__())
        articles_ress = self.getarticlelists(articleparams.__next__())
        articles = self.analyze_articlelists(articles_ress.__next__())
        articlesparam = self.getarticleparams(articles.__next__())
        articles_html = self.getarticlehtml(articlesparam.__next__())
        self.analyzearticles(articles_html.__next__())


if __name__ == '__main__':
    spider = ZhongGuoWang('中国网')
    spider.run()
