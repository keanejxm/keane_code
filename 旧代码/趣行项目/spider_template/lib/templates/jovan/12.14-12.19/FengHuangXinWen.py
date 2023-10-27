# Author Keane
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
# 注意：
# 采集了新闻和视频选卡的数据，web类型的新闻没详情接口。
# "vote"、"advert"、"newh5zip"、"survey"、"theme"这几种类型的没有遇到，查看源码获知。
# "normal"、"shortvideo"、"videoshortimg"在视频选卡使用。
# 其他的都是共用的类型
import json

from lib.templates.appspider_m import Appspider

# import time
from lib.templates.initclass import InitClass


def fnArticleparam(article, articleparam):
    articleparam["articletype"] = article['type']
    articleparam["articletitle"] = article['title']
    articleparam["articleid"] = article['id']
    articleparam["imageurl"] = article['thumbnail']
    try:
        articleparam["updatetime"] = InitClass().date_time_stamp(article['updateTime'])
    except Exception as e:
        print(e)
    if "link" in article.keys():
        articleparam["articleid"] = article['link']['url']
        articleparam["articleurl"] = article['link']['weburl']
    if "phvideo" in article.keys():
        articleparam["videos"] = article['phvideo']["videoPlayUrl"]
        articleparam["videocover"] = article['thumbnail']

    articletype = article['type']
    if articletype == "doc":
        print(article, articleparam)
    elif articletype == "topic2" or articletype == "topic":
        print(article, articleparam)
    elif articletype == "slide":
        print(article, articleparam)
    elif articletype == "phvideo":
        print(article, articleparam)
    elif articletype == "short":
        print(article, articleparam)
    elif articletype == "web":
        print(article, articleparam)
    elif articletype == "vote":
        print(article, articleparam)
    elif articletype == "advert":
        print(article, articleparam)
    elif articletype == "newh5zip":
        print(article, articleparam)
    elif articletype == "survey":
        print(article, articleparam)
    elif articletype == "theme":
        print(article, articleparam)
    else:
        print(article, articleparam)

    return articleparam


class FengHuangXinWen(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "https://config.nine.ifeng.com/news/channel?"
        # 频道请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36',
            'Host': 'config.nine.ifeng.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        # 频道数据体
        data = {
            'totalProfile': '',
            'gv': '7.17.0',
            'av': '7.17.0',
            'uid': '500000000049572',
            'deviceid': '500000000049572',
            'proid': 'ifengnews',
            'os': 'android_23',
            'df': 'androidphone',
            'vt': '	5',
            'screen': '810x1440',
            'publishid': '6001',
            'nw	wifi': '',
            'loginid': '',
            'adAid': '',
            'hw': 'android_mumu',
            'st': '16073964802667',
            'sn': 'fe9390c571c2faaf0b889906ff4f7075',
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
        channelparams = []
        temp = channelslists['defaultChannel'] + channelslists['more'] + channelslists['videoTag']
        temp = channelslists['videoTag']
        for channel in temp:
            channelid = channel['api']
            channelname = channel['name']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)
        # channelid = temp[3]['api']
        # channelname = temp[3]['name']
        # channelparam = InitClass().channel_fields(channelid, channelname)
        # channelparams.append(channelparam)
        # channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistsparams(channelsparams):
        articleparams = []
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            url = channelid
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Content-Length': '230',
                'Host': 'nine.ifeng.com',
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip',
            }
            data = {
                'action': 'default',
                'pullNum': '1',
                'dailyOpenNum': '2',
                'autoPlay': '1',
                'gv': '7.17.0',
                'av': '7.17.0',
                'uid': '500000000049572',
                'deviceid': '500000000049572',
                'proid': 'ifengnews',
                'os': 'android_23',
                'df': 'androidphone',
                'vt': '5',
                'screen': '810x1440',
                'publishid': '6001',
                'nw': 'wifi',
                'loginid': '',
                'adAid': '',
                'hw': 'android_mumu',
                'st': '16073984336164',
                'sn': '54e9bd41410f2ac5291bc9d4cb8ff403',
            }
            # 如果携带的是json数据体,用appjson发送
            app_json = 'openNum=1&pushStatus=1&lastDoc=%2C%2C%2C&installTime=1607396472&closeWinType=&ltoken=%242kJyeiQHbwIiOiwiIuxGZiojIsICMjRmI6ISesIiIwRmI6IicsIiIyBnIpZ3blNmbiojIiwiI0l2Y6ISesIiIpRmIyR3c0NWaiojI00nIfr34g&closeWinCount=0&closeWinTime=0&'
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
                if len(articlelist_json) > 0:
                    temp = articlelist_json[0]["item"]
                if len(articlelist_json) > 1:
                    if len(temp) > 0:
                        temp += articlelist_json[1]["item"]
                    else:
                        temp = articlelist_json[1]["item"]
                print(temp)
                try:
                    articlelists = temp
                    # articlelistsurl = articlelist_json['data']['listUrl']
                    for article in articlelists:
                        print(article)
                        if article['type'] == "advert":
                            continue
                        articleparam = InitClass().article_list_fields()

                        if article['type'] == "videoshortlist" or article['type'] == "soleMarqueeList":
                            for temp in article['marqueeList']:
                                articleparam = fnArticleparam(temp, articleparam)
                        elif article['type'] == "hotspot":
                            for temp in article['relation']:
                                articleparam = fnArticleparam(temp, articleparam)
                        elif article['type'] == "doc" or article['type'] == "phvideo" or article['type'] == "short" or \
                                article['type'] == "web" or article['type'] == "text_live" or article[
                            'type'] == "slide" or article['type'] == "topic2":
                            articleparam = fnArticleparam(article, articleparam)
                        elif article['type'] == "vote":
                            print(article)
                        elif article['type'] == "newh5zip":
                            print(article)
                        elif article['type'] == "survey":
                            print(article)
                        elif article['type'] == "theme":
                            print(article)
                        elif article['type'] == "normal":
                            articleparam = fnArticleparam(article, articleparam)
                        elif article['type'] == "shortvideo":
                            articleparam = fnArticleparam(article, articleparam)
                        elif article['type'] == 'videoshortimg':
                            articleparam = fnArticleparam(article, articleparam)
                        else:
                            print(article)
                        articleparam["channelname"] = channelname
                        articlesparams.append(articleparam)
                except Exception as e:
                    print(e, articlelist_json)
            except Exception as e:
                print(e, articlelist_json)
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articlesparam = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Content-Length': '414',
            'Host': 'nine.ifeng.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        data = {
            'gv': '7.17.0',
            'av': '7.17.0',
            'uid': '500000000049572',
            'deviceid': '500000000049572',
            'proid': 'ifengnews',
            'os': 'android_23',
            'df': 'androidphone',
            'vt': '5',
            'screen': '810x1440',
            'publishid': '6001',
            'nw': 'wifi',
            'loginid': '',
            'adAid': '',
            'hw': 'android_mumu',
            'st': '16074211772269',
            'sn': '7db9264936b59cabee9e7157622ad6bd',
        }
        # 如果携带的是json数据体,用appjson发送
        article_json = 'ltoken=%242kJyeiQHbwIiOiwiIuxGZiojIsICMjRmI6ISesIiIwRmI6IicsIiIyBnIpZ3blNmbiojIiwiI0l2Y6ISesIiIpRmIyR3c0NWaiojI00nIfr34g&lastDoc=%3CclusterId_yUtAn0CJYc%2Cf5cdcb42-ef77-4f9c-b137-d6dc41775913%2C3%2Cclick%2Cvideo_f5cdcb42-ef77-4f9c-b137-d6dc41775913%2C%3E%7C%3CclusterId_yUtAn0CJYc%2Cf5cdcb42-ef77-4f9c-b137-d6dc41775913%2C13%2Cclick%2Csy%2C%3E%7C%3Cusim_820w8LMqS1A%2Cucms_8210LiuroI1%2C58%2C%2Csy%2C1607418630%3E&'
        method = 'post'
        for articleparam in articles:
            url = ""
            articletype = articleparam.get("articletype")
            if articletype == "doc":
                url = articleparam.get("articleid")
            elif articletype == "topic2" or articletype == "topic":
                url = articleparam.get("articleid")
            elif articletype == "slide":
                url = articleparam.get("articleid")
            elif articletype == "phvideo":
                url = 'https://nine.ifeng.com/apiPhoenixtvDetails?guid=' + articleparam.get("articleid")
            elif articletype == "short":
                url = articleparam.get("articleid")
            elif articletype == "web":
                pass
            elif articletype == "vote":
                pass
            elif articletype == "advert":
                pass
            elif articletype == "newh5zip":
                pass
            elif articletype == "survey":
                pass
            elif articletype == "theme":
                pass
            elif articletype == "normal":
                url = articleparam.get("articleid")
            elif articletype == "shortvideo":
                url = articleparam.get("articleid")
            elif articletype == "videoshortimg":
                url = 'https://nine.ifeng.com/apiPhoenixtvDetails?guid=' + articleparam.get("articleid")
            else:
                print('未识别类型' + articletype)
            if url:
                channelname = articleparam.get("channelname")
                imgurl = articleparam.get("imageurl")
                article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                            articlejson=article_json)
                articlesparam.append(article)
            else:
                print('未请求类型：', articleparam)
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
                if 'meta' in articlejson.keys() and 'body' in articlejson.keys():  # doc类型
                    fields["title"] = articlejson['body']['title']  # 标题
                    fields["url"] = articlejson['body']['shareurl']  # 网站的url
                    fields["workerid"] = articlejson['body']['documentId']  # 文章id
                    fields["source"] = articlejson['body']['source']  # 来源
                    fields["content"] = articlejson['body']['text']  # 文章内容
                    fields["pubtime"] = articlejson['body']['timestamp']  # 发布时间
                    if len(articlejson['body']['img']) > 0:
                        fields["images"] = articlejson['body']['img']  # 图片地址
                        fields["articlecovers"] = articlejson['body']['realimg']
                    if 'hasVideo' in articlejson['body'].keys() and 'Y' == articlejson['body']['hasVideo']:
                        fields["videos"] = articlejson['body']['videos']['Normal']['src']  # 视频的url
                        fields["videocover"] = articlejson['body']['videos']['thumbnail']  # 视频封面
                    fields["author"] = articlejson['body']['title']
                elif 'singleVideoInfo' in articlejson.keys() and 'adData' in articlejson.keys():  # phvideo
                    fields["title"] = articlejson['singleVideoInfo'][0]['title']  # 标题
                    fields["url"] = articlejson['singleVideoInfo'][0]['shareURL']  # 网站的url
                    fields["workerid"] = articlejson['singleVideoInfo'][0]['id']  # 文章id
                    fields["source"] = articlejson['singleVideoInfo'][0]['columnName']  # 来源
                    # fields["content"] = articlejson['singleVideoInfo'][0]['title'] # 文章内容
                    fields["pubtime"] = InitClass().date_time_stamp(
                        articlejson['singleVideoInfo'][0]['videoPublishTime'])  # 发布时间
                    fields["images"] = articlejson['singleVideoInfo'][0]['imgURL']  # 图片地址
                    fields["articlecovers"] = articlejson['singleVideoInfo'][0]['imgURL']
                    fields["videos"] = articlejson['singleVideoInfo'][0]['videoURL']  # 视频的url
                    fields["videocover"] = articlejson['singleVideoInfo'][0]['trimImgURL']  # 视频封面
                    fields["author"] = articlejson['singleVideoInfo'][0]['columnName']
                elif 'code' in articlejson.keys() and 'msg' in articlejson.keys() and 'data' in articlejson.keys():  # topic
                    if 'meta' in articlejson["data"] and 'body' in articlejson["data"]:
                        fields["title"] = articlejson["data"]['meta']['title']  # 标题
                        fields["url"] = articlejson["data"]['meta']['shareUrl']  # 网站的url
                        fields["workerid"] = articlejson["data"]['meta']['id']  # 文章id
                        # fields["source"] = articlejson["data"]['meta']['columnName']  # 来源
                        fields["content"] = articlejson["data"]['body']  # 文章内容
                        fields["pubtime"] = InitClass().date_time_stamp(
                            articlejson["data"]['meta']['publishedTime'])  # 发布时间
                        fields["images"] = articlejson["data"]['meta']['newBannerImg']  # 图片地址
                        fields["articlecovers"] = articlejson["data"]['meta']['thumbnail']
                        # fields["videos"] = articlejson['singleVideoInfo'][0]['videoURL']  # 视频的url
                        # fields["videocover"] = articlejson['singleVideoInfo'][0]['trimImgURL']  # 视频封面
                        # fields["author"] = articlejson['singleVideoInfo'][0]['columnName']
                else:
                    print('未识别详情', articlejson)
                    continue
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
    spider = FengHuangXinWen('凤凰新闻')
    spider.run()
