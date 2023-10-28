# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
import re

import requests

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


def getRealNum(param):
    returnNum = 0
    try:
        if 'k' in param:
            index = param.rfind("k")
            temp = param[0:index]
            pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
            if pattern.match(temp):
                returnNum = int(float(temp) * 1000)
        elif 'w' in param:
            index = param.rfind("w")
            temp = param[0:index]
            pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
            if pattern.match(temp):
                returnNum = int(float(temp) * 10000)
        else:
            returnNum = int(param)
    except Exception as e:
        print(e, returnNum)

    return returnNum


def setArticleListParam(channelname, channelid, banner, articleparam, article):
    # if 'channel_id' in article.keys():
    #     articleparam["channelid"] = article['channel_id']
    articleparam["channelid"] = channelid
    articleparam["channelname"] = channelname
    articleparam["articleid"] = article['news_id']
    articleparam["articletype"] = article['in_type']
    if 'news_title' in article.keys():
        articleparam["articletitle"] = article['news_title']
    if 'title' in article.keys():
        articleparam["articletitle"] = article['title']
    articleparam["banner"] = banner
    if 'pic_path' in article.keys():
        articleparam["imageurl"] = article['pic_path']
    if 'url' in article.keys():
        articleparam["articleurl"] = article['url']
    if 'news_url' in article.keys():
        articleparam["articleurl"] = article['news_url']
    # articleparam["videos"] = article['videourl']
    # articleparam["videocover"] = article['title']
    if 'create_time' in article.keys():
        articleparam["pubtime"] = article['create_time']
    # articleparam["createtime"] = article['title']
    # articleparam["updatetime"] = article['title']
    # articleparam["source"] = article['source']
    # articleparam["author"] = article['author']
    # articleparam["likenum"] = article['digg']
    # articleparam["commentnum"] = article['pl']
    # articleparam["readnum"] = article['title']
    if 'id' in article.keys():
        articleparam["sharenum"] = article['id']
    return articleparam


class KaiPingXinWen(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道请求头
        headers1 = {
            "Connection": "close",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Content-Length": "343",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
            "Host": "appkp.ccwb.cn",
            "Accept-Encoding": "gzip",
        }
        headers2 = {
            "Connection": "close",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
            "Host": "appkp.ccwb.cn",
            "Accept-Encoding": "gzip",
        }
        # 频道数据体
        data1 = {
            "cw_client": "android",
            "cw_device": "android",
            "cw_os": "android",
            "cw_machine_type": "app",
            "cw_machine_id": "42e7db534a518bc5",
            "cw_country": "中国",
            "cw_province": "云南",
            "cw_city": "昆明",
            "cw_area": "五华区",
            "cw_latitude": "25.034962",
            "cw_longitude": "102.693386",
            "cw_ip": "10.0.2.15",
            "cw_version": "6.014",
            "cw_networktype": "WIFI",
            "cw_devicemodel": "MuMu",
        }
        data2 = {
            "cw_client": "android",
            "cw_device": "android",
            "cw_os": "android",
            "cw_machine_type": "app",
            "cw_machine_id": "42e7db534a518bc5",
            "cw_country": "中国",
            "cw_province": "云南",
            "cw_city": "昆明",
            "cw_area": "五华区",
            "cw_latitude": "25.034962",
            "cw_longitude": "102.693386",
            "cw_ip": "10.0.2.15",
            "cw_version": "6.014",
            "cw_networktype": "WIFI",
            "cw_devicemodel": "MuMu",
            "cw_app_id": "201807231814160AJ9D0",
        }
        # 如果携带的是json数据体,用appjson发送
        # app_json = {}
        # 频道请求方式
        method1 = "post"
        method2 = "get"
        # 频道url
        url1 = "https://appkp.ccwb.cn/api/v1/index/getIndexTopChannelLists"
        url2 = "https://appkp.ccwb.cn/api/v1/channel/getDynamicNewsChannal"

        app_params1 = InitClass().app_params(url1, headers1, method1, data=data1)
        app_params2 = InitClass().app_params(url2, headers2, method2, data=data2)
        # 如果携带json数据，用下列方式存储发送数据
        # app_params = InitClass().app_params(url, headers, method, data = data ,appjson=app_json)
        yield [app_params1, app_params2]

    @staticmethod
    def analyzechannels(channelsres):
        """
        此方法主要获取channelid,channelname即可
        若请求文章列表页需要channeltype，categoryname，categoryid,则以categoryname= categoryname形式传递参数
        :param channelsres:
        :return:
        """
        # # 将返回的数据转为json数据
        # channelslists = json.loads(channelsres)
        # # 返回的数据是编码错误，则用下面代码解析数据
        # # channelslists = json.loads(json.dumps(channelsres,indent=4,ensure_ascii=False))
        print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            if k == "https://appkp.ccwb.cn/api/v1/index/getIndexTopChannelLists":
                channelList = json.loads(v)
                for channel in channelList['data']:
                    channelid = channel['id']
                    channelname = channel['name']
                    channelType = 'QXChannelNews'
                    channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channelType)
                    channelparams.append(channelparam)
            elif k == "https://appkp.ccwb.cn/api/v1/channel/getDynamicNewsChannal":
                channelList = json.loads(v)
                for channel in channelList['data']:
                    channelid = channel['id']
                    channelname = channel['name']
                    channelType = 'QXChannelVideo'
                    channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channelType)
                    channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistsparams(channelsparams):
        """
        此方法目的是组建请求文章列页面数据参数，url，headers，data，若以json形式发送数据，则channeljson = channeljson
        :param channelsparams:
        :return:
        """
        articleparams = []
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channelType = channel.get("channeltype")
            if channelType == "QXChannelNews":
                headers = {
                    "Connection": "close",
                    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                    "Content-Length": "411",
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
                    "Host": "appkp.ccwb.cn",
                    "Accept-Encoding": "gzip",
                }
                # 频道数据体
                data = {
                    "cw_client": "android",
                    "cw_device": "android",
                    "cw_os": "android",
                    "cw_machine_type": "app",
                    "cw_machine_id": "42e7db534a518bc5",
                    "cw_country": "中国",
                    "cw_province": "北京市",
                    "cw_city": "北京市",
                    "cw_area": "东城区",
                    "cw_latitude": "39.908588595920136",
                    "cw_longitude": "116.39731499565973",
                    "cw_ip": "10.0.2.15",
                    "cw_version": "6.014",
                    "cw_networktype": "WIFI",
                    "cw_devicemodel": "MuMu",
                    "cw_page": "1",
                    "cw_channel_id": channelid,
                }
                method = "post"
                url = "https://appkp.ccwb.cn/api/v1/index/getIndexNewsLists"
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           channelid=channelid, data=data)
                articleparams.append(articlelist_param)
            elif channelType == "QXChannelVideo":
                headers = {
                    "Connection": "close",
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
                    "Host": "appkp.ccwb.cn",
                    "Accept-Encoding": "gzip",
                }
                data = {
                    "cw_client": "android",
                    "cw_device": "android",
                    "cw_os": "android",
                    "cw_machine_type": "app",
                    "cw_machine_id": "42e7db534a518bc5",
                    "cw_country": "中国",
                    "cw_province": "北京市",
                    "cw_city": "北京市",
                    "cw_area": "东城区",
                    "cw_latitude": "39.908588595920136",
                    "cw_longitude": "116.39731499565973",
                    "cw_ip": "10.0.2.15",
                    "cw_version": "6.014",
                    "cw_networktype": "WIFI",
                    "cw_devicemodel": "MuMu",
                    "cw_page": "1",
                    "cw_channel_id": channelid,
                }
                method = "get"
                url = "https://appkp.ccwb.cn/api/v1/news/getDynamicNewsLists"

                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           channelid=channelid, data=data)
                articleparams.append(articlelist_param)

        yield articleparams

    @staticmethod
    def analyze_articlelists(articleslist_ress):
        """
        解析文章列表页，目的是为了获取文章具体信息，组建请求文章详情数据体
        :param articleslist_ress:
        :return:
        """
        articlesparams = []
        for articleslist_res in articleslist_ress:
            channelname = articleslist_res.get("channelname")
            channelid = articleslist_res.get("channelid")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                # 可在下面打印处打断点，查看请求到的数据
                print(articlelist_json)
                # 若banner图在articlelist_json中则分来开取并给其复制banner = 1
                for article in articlelist_json['data']:
                    # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                    print(article)
                    if 'focus' in article['in_type']:  # bannner
                        print(article)
                        for item in article['news']:
                            articleparam = InitClass().article_list_fields()
                            articleparam = setArticleListParam(channelname, channelid, 1, articleparam, item);
                            articlesparams.append(articleparam)
                    elif 'DynamicNews' in article['in_type']:
                        print(article)
                        for item in article['news']:
                            articleparam = InitClass().article_list_fields()
                            articleparam = setArticleListParam(channelname, channelid, 0, articleparam, item);
                            articlesparams.append(articleparam)
                    elif 'functions' in article['in_type']:
                        print(article)
                    elif 'RollingNews' in article['in_type']:
                        print(article)
                    elif 'topic' in article['in_type']:
                        print(article)
                        for item in article['news']:
                            articleparam = InitClass().article_list_fields()
                            articleparam = setArticleListParam(channelname, channelid, 0, articleparam, item);
                            articlesparams.append(articleparam)
                    elif 'news' in article['in_type']:
                        print(article)
                        for item in article['news']:
                            articleparam = InitClass().article_list_fields()
                            articleparam = setArticleListParam(channelname, channelid, 0, articleparam, item);
                            articlesparams.append(articleparam)
                    elif 'live' in article['in_type']:
                        print(article)
                        for item in article['news']:
                            articleparam = InitClass().article_list_fields()
                            articleparam = setArticleListParam(channelname, channelid, 0, articleparam, item);
                            articlesparams.append(articleparam)
                    elif 'url' in article['in_type']:
                        print(article)
                        for item in article['news']:
                            articleparam = InitClass().article_list_fields()
                            articleparam = setArticleListParam(channelname, channelid, 0, articleparam, item);
                            articlesparams.append(articleparam)
                    elif 'video' in article['in_type']:
                        print(article)
                        for item in article['news']:
                            articleparam = InitClass().article_list_fields()
                            articleparam = setArticleListParam(channelname, channelid, 0, articleparam, item);
                            articlesparams.append(articleparam)
                    elif 'ChannelGroup' in article['in_type']:
                        print(article)
                    elif 'channel' in article['in_type']:
                        print(article)
                        for item in article['news']:
                            for item1 in item['news']:
                                articleparam = InitClass().article_list_fields()
                                articleparam = setArticleListParam(channelname, channelid, 0, articleparam, item1);
                                articlesparams.append(articleparam)
                    else:
                        print(article)
                    # articleparam = InitClass().article_list_fields()
                    # articleparam = setArticleListParam(channelname, 1, articleparam, article);
                    # articlesparams.append(articleparam)
            except Exception as e:
                print(e, articlelist_json)
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        """
        组建请求文章详情所需要的数据体
        :param articles:
        :return:
        """
        articlesparam = []
        url = ""
        # 频道请求头
        headers = {
            "Connection": "close",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
            "Host": "appkp.ccwb.cn",
            "Accept-Encoding": "gzip",
        }
        # 频道数据体
        data = {}
        # 如果携带的是json数据体,用appjson发送
        # app_json = {}
        # 频道请求方式
        method = "post"
        for articleparam in articles:
            articletype = articleparam.get("articletype")
            if 'topic' in articletype:
                url = "https://appkp.ccwb.cn/api/v1/news/getNewsDetail"
                data = {
                    "cw_client": "android",
                    "cw_device": "android",
                    "cw_os": "android",
                    "cw_machine_type": "app",
                    "cw_machine_id": "42e7db534a518bc5",
                    "cw_country": "中国",
                    "cw_province": "北京市",
                    "cw_city": "北京市",
                    "cw_area": "东城区",
                    "cw_latitude": "39.908588595920136",
                    "cw_longitude": "116.39731499565973",
                    "cw_ip": "10.0.2.15",
                    "cw_version": "6.014",
                    "cw_networktype": "WIFI",
                    "cw_devicemodel": "MuMu",
                    "cw_news_id": articleparam.get("articleid"),
                }
                print(articleparam)
            elif 'news' in articletype:
                url = "https://appkp.ccwb.cn/api/v1/news/getNewsDetail"
                data = {
                    "cw_client": "android",
                    "cw_device": "android",
                    "cw_os": "android",
                    "cw_machine_type": "app",
                    "cw_machine_id": "42e7db534a518bc5",
                    "cw_country": "中国",
                    "cw_province": "北京市",
                    "cw_city": "北京市",
                    "cw_area": "东城区",
                    "cw_latitude": "39.908588595920136",
                    "cw_longitude": "116.39731499565973",
                    "cw_ip": "10.0.2.15",
                    "cw_version": "6.014",
                    "cw_networktype": "WIFI",
                    "cw_devicemodel": "MuMu",
                    "cw_news_id": articleparam.get("articleid"),
                }
                print(articleparam)
            elif 'live' in articletype:
                url = "https://appkp.ccwb.cn/api/v1/live/getNewsLiveDetails"
                data = {
                    "cw_client": "android",
                    "cw_device": "android",
                    "cw_os": "android",
                    "cw_machine_type": "app",
                    "cw_machine_id": "42e7db534a518bc5",
                    "cw_country": "中国",
                    "cw_province": "北京市",
                    "cw_city": "北京市",
                    "cw_area": "东城区",
                    "cw_latitude": "39.908588595920136",
                    "cw_longitude": "116.39731499565973",
                    "cw_ip": "10.0.2.15",
                    "cw_version": "6.014",
                    "cw_networktype": "WIFI",
                    "cw_devicemodel": "MuMu",
                    "cw_news_id": articleparam.get("articleid"),
                }
                print(articleparam)
            elif 'url' in articletype:
                url = "https://appkp.ccwb.cn/api/v1/news/getNewsDetail"
                data = {
                    "cw_client": "android",
                    "cw_device": "android",
                    "cw_os": "android",
                    "cw_machine_type": "app",
                    "cw_machine_id": "42e7db534a518bc5",
                    "cw_country": "中国",
                    "cw_province": "北京市",
                    "cw_city": "北京市",
                    "cw_area": "东城区",
                    "cw_latitude": "39.908588595920136",
                    "cw_longitude": "116.39731499565973",
                    "cw_ip": "10.0.2.15",
                    "cw_version": "6.014",
                    "cw_networktype": "WIFI",
                    "cw_devicemodel": "MuMu",
                    "cw_news_id": articleparam.get("articleid"),
                }
                print(articleparam)
            elif 'video' in articletype:
                url = "https://appkp.ccwb.cn/api/v1/news/getNewsVideoDetail"
                data = {
                    "cw_client": "android",
                    "cw_device": "android",
                    "cw_os": "android",
                    "cw_machine_type": "app",
                    "cw_machine_id": "42e7db534a518bc5",
                    "cw_country": "中国",
                    "cw_province": "北京市",
                    "cw_city": "北京市",
                    "cw_area": "东城区",
                    "cw_latitude": "39.908588595920136",
                    "cw_longitude": "116.39731499565973",
                    "cw_ip": "10.0.2.15",
                    "cw_version": "6.014",
                    "cw_networktype": "WIFI",
                    "cw_devicemodel": "MuMu",
                    "cw_news_id": articleparam.get("articleid"),
                }
                print(articleparam)
            else:
                url = "https://appkp.ccwb.cn/api/v1/news/getNewsDetail"
                data = {
                    "cw_client": "android",
                    "cw_device": "android",
                    "cw_os": "android",
                    "cw_machine_type": "app",
                    "cw_machine_id": "42e7db534a518bc5",
                    "cw_country": "中国",
                    "cw_province": "北京市",
                    "cw_city": "北京市",
                    "cw_area": "东城区",
                    "cw_latitude": "39.908588595920136",
                    "cw_longitude": "116.39731499565973",
                    "cw_ip": "10.0.2.15",
                    "cw_version": "6.014",
                    "cw_networktype": "WIFI",
                    "cw_devicemodel": "MuMu",
                    "cw_news_id": articleparam.get("articleid"),
                }
                print(articleparam)

            articletitle = articleparam.get("articletitle")
            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
            channelid = articleparam.get("channelid")
            articleid = articleparam.get("articleid")
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
            article_show = InitClass().article_params_fields(url, headers, method, channelname, imgurl,
                                                             data=data,
                                                             videourl=videos, videocover=videocover, pubtime=pubtime,
                                                             createtime=createtime, updatetime=updatetime,
                                                             source=source, author=author, likenum=likenum,
                                                             commentnum=channelid, sharenum=articletitle,
                                                             readnum=articletype,
                                                             articleid=articleid, articleurl=articleurl, banners=banner)
            articlesparam.append(article_show)
        yield articlesparam

    @staticmethod
    def analyzearticles(articleResponseData):
        for articleResponse in articleResponseData:
            appname = articleResponse.get("appname")
            channelname = articleResponse.get("channelname")
            imageurl = articleResponse.get("imageurl")
            videourl = articleResponse.get("videourl")
            videocover = articleResponse.get("videocover")
            articleurl = articleResponse.get("articleurl")
            articleid = articleResponse.get("articleid")
            pubtime = articleResponse.get("pubtime")
            createtime = articleResponse.get("createtime")
            updatetime = articleResponse.get("updatetime")
            source = articleResponse.get("source")
            author = articleResponse.get("author")
            likenum = articleResponse.get("likenum")
            articletype = articleResponse.get("readnum")
            articletitle = articleResponse.get("sharenum")
            channelid = articleResponse.get("commentnum")
            banner = articleResponse.get("banner")
            articleres = articleResponse.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["channelID"] = channelid
            fields["imageurl"] = imageurl
            fields["banner"] = banner
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                print(articlejson)

                fields["appname"] = appname
                if 'topic' in articletype:
                    fields["url"] = articlejson['data']['url']  # 文章的html网址，提取shareurl
                    fields["workerid"] = articlejson['data']['news_id']  # 文章的id
                    fields["title"] = articlejson['data']['title']  # 文章的标题
                    # fields["content"] = articlejson['data']['content']  # 文章的内容详情
                    fields["articlecovers"] = articlejson['data']['pic_path']  # 文章的封面，一般为上面get到的字段
                    fields["images"] = articlejson['data']['pic_path']  # 文章详情内的图片url，一般为列表需遍历获取
                    # fields["videos"] = articlejson['data']['videourl']  # 文章的视频链接地址
                    # fields["videocover"] = articlejson['data']['link']  # 文章的视频封面地址
                    # fields["width"] = articlejson['data']['link']  # 文章的视频宽
                    # fields["height"] = articlejson['data']['link']  # 文章的视频高
                    # fields["source"] = articlejson['data']['source']  # 文章的来源
                    # fields["pubtime"] = articlejson['data']['updatedate']  # 文章的发布时间
                    fields["createtime"] = InitClass().date_time_stamp(articlejson['data']['create_time'])  # 文章的发布时间
                    # fields["updatetime"] = articlejson['data']['pubDate']  # 文章的更新时间
                    # fields["likenum"] = articlejson['data']['click_num']  # 文章的点赞数
                    # fields["playnum"] = articlejson['data']['link']  # 视频的播放数
                    # fields["commentnum"] = len(articlejson['data']['comments'])  # 文章评论数
                    fields["readnum"] = getRealNum(articlejson['data']['click_num'])  # 文章的阅读数
                    # fields["trannum"] = articlejson['data']['link']  # 文章的转发数
                    # fields["sharenum"] = articlejson['data']['link']  # 文章分享数
                    # fields["author"] = articlejson['data']['author']  # 文章作者

                    url = 'https://appkp.ccwb.cn/api/v1/news/getTopicLists'
                    headers = {
                        "Connection": "close",
                        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
                        "Host": "appkp.ccwb.cn",
                        "Accept-Encoding": "gzip",
                    }
                    data = {
                        "cw_client": "android",
                        "cw_device": "android",
                        "cw_os": "android",
                        "cw_machine_type": "app",
                        "cw_machine_id": "42e7db534a518bc5",
                        "cw_country": "中国",
                        "cw_province": "北京市",
                        "cw_city": "北京市",
                        "cw_area": "东城区",
                        "cw_latitude": "39.908588595920136",
                        "cw_longitude": "116.39731499565973",
                        "cw_ip": "10.0.2.15",
                        "cw_version": "6.014",
                        "cw_networktype": "WIFI",
                        "cw_devicemodel": "MuMu",
                        "cw_page": "1",
                        "cw_news_id": articleid,
                    }
                    response = requests.post(url=url, headers=headers, data=data).content.decode()
                    articlejson1 = json.loads(json.dumps(json.loads(response), indent=4, ensure_ascii=False))
                    print(articlejson1)
                    fields["content"] = articlejson1['data']  # 文章的内容详情

                elif 'news' in articletype:
                    fields["url"] = articlejson['data']['url']  # 文章的html网址，提取shareurl
                    fields["workerid"] = articlejson['data']['news_id']  # 文章的id
                    fields["title"] = articlejson['data']['title']  # 文章的标题
                    fields["content"] = articlejson['data']['content']  # 文章的内容详情
                    fields["articlecovers"] = articlejson['data']['pic_path']  # 文章的封面，一般为上面get到的字段
                    fields["images"] = articlejson['data']['pic_path']  # 文章详情内的图片url，一般为列表需遍历获取
                    # fields["videos"] = articlejson['data']['videourl']  # 文章的视频链接地址
                    # fields["videocover"] = articlejson['data']['link']  # 文章的视频封面地址
                    # fields["width"] = articlejson['data']['link']  # 文章的视频宽
                    # fields["height"] = articlejson['data']['link']  # 文章的视频高
                    # fields["source"] = articlejson['data']['source']  # 文章的来源
                    # fields["pubtime"] = articlejson['data']['updatedate']  # 文章的发布时间
                    fields["createtime"] = InitClass().date_time_stamp(articlejson['data']['create_time'])  # 文章的发布时间
                    # fields["updatetime"] = articlejson['data']['pubDate']  # 文章的更新时间
                    fields["likenum"] = getRealNum(articlejson['data']['good_num'])  # 文章的点赞数
                    # fields["playnum"] = articlejson['data']['link']  # 视频的播放数
                    fields["commentnum"] = getRealNum(articlejson['data']['comment_num'])  # 文章评论数
                    fields["readnum"] = getRealNum(articlejson['data']['click_num'])  # 文章的阅读数
                    # fields["trannum"] = articlejson['data']['link']  # 文章的转发数
                    # fields["sharenum"] = articlejson['data']['link']  # 文章分享数
                    # fields["author"] = articlejson['data']['author']  # 文章作者
                    if len(articlejson['data']['audio_path']):
                        print(articlejson['data']['audio_path'])
                elif 'live' in articletype:
                    fields["url"] = articlejson['data']['url']  # 文章的html网址，提取shareurl
                    fields["workerid"] = articlejson['data']['id']  # 文章的id
                    fields["title"] = articlejson['data']['title']  # 文章的标题
                    fields["content"] = articlejson['data']['info']  # 文章的内容详情
                    fields["articlecovers"] = articlejson['data']['pic_path']  # 文章的封面，一般为上面get到的字段
                    fields["images"] = articlejson['data']['pic_path']  # 文章详情内的图片url，一般为列表需遍历获取
                    if '3' == articlejson['data']['type']:
                        fields["videos"] = articlejson['data']['video_path']  # 文章的视频链接地址
                    else:
                        print(articlejson['data'])
                    fields["videocover"] = articlejson['data']['pic_path']  # 文章的视频封面地址
                    # fields["width"] = articlejson['data']['link']  # 文章的视频宽
                    # fields["height"] = articlejson['data']['link']  # 文章的视频高
                    # fields["source"] = articlejson['data']['source']  # 文章的来源
                    # fields["pubtime"] = articlejson['data']['updatedate']  # 文章的发布时间
                    fields["createtime"] = InitClass().date_time_stamp(articlejson['data']['create_time'])  # 文章的发布时间
                    # fields["updatetime"] = articlejson['data']['pubDate']  # 文章的更新时间
                    # fields["likenum"] = articlejson['data']['good_num']  # 文章的点赞数
                    # fields["playnum"] = articlejson['data']['link']  # 视频的播放数
                    # fields["commentnum"] = articlejson['data']['comment_num']  # 文章评论数
                    fields["readnum"] = getRealNum(articlejson['data']['click_num'])  # 文章的阅读数
                    # fields["trannum"] = articlejson['data']['link']  # 文章的转发数
                    # fields["sharenum"] = articlejson['data']['link']  # 文章分享数
                    # fields["author"] = articlejson['data']['author']  # 文章作者
                elif 'url' in articletype:
                    fields["url"] = articlejson['data']['url']  # 文章的html网址，提取shareurl
                    fields["workerid"] = articlejson['data']['news_id']  # 文章的id
                    fields["title"] = articlejson['data']['title']  # 文章的标题
                    fields["content"] = articlejson['data']['content']  # 文章的内容详情
                    fields["articlecovers"] = articlejson['data']['pic_path']  # 文章的封面，一般为上面get到的字段
                    fields["images"] = articlejson['data']['pic_path']  # 文章详情内的图片url，一般为列表需遍历获取
                    # fields["videos"] = articlejson['data']['videourl']  # 文章的视频链接地址
                    # fields["videocover"] = articlejson['data']['link']  # 文章的视频封面地址
                    # fields["width"] = articlejson['data']['link']  # 文章的视频宽
                    # fields["height"] = articlejson['data']['link']  # 文章的视频高
                    # fields["source"] = articlejson['data']['source']  # 文章的来源
                    # fields["pubtime"] = articlejson['data']['updatedate']  # 文章的发布时间
                    fields["createtime"] = InitClass().date_time_stamp(articlejson['data']['create_time'])  # 文章的发布时间
                    # fields["updatetime"] = articlejson['data']['pubDate']  # 文章的更新时间
                    fields["likenum"] = getRealNum(articlejson['data']['good_num'])  # 文章的点赞数
                    # fields["playnum"] = articlejson['data']['link']  # 视频的播放数
                    fields["commentnum"] = getRealNum(articlejson['data']['comment_num'])  # 文章评论数
                    fields["readnum"] = getRealNum(articlejson['data']['click_num'])  # 文章的阅读数
                    # fields["trannum"] = articlejson['data']['link']  # 文章的转发数
                    # fields["sharenum"] = articlejson['data']['link']  # 文章分享数
                    # fields["author"] = articlejson['data']['author']  # 文章作者
                elif 'video' in articletype:
                    fields["url"] = articlejson['data']['url']  # 文章的html网址，提取shareurl
                    fields["workerid"] = articlejson['data']['news_id']  # 文章的id
                    fields["title"] = articlejson['data']['title']  # 文章的标题
                    # fields["content"] = articlejson['data']['content']  # 文章的内容详情
                    fields["articlecovers"] = articlejson['data']['pic_path']  # 文章的封面，一般为上面get到的字段
                    fields["images"] = articlejson['data']['pic_path']  # 文章详情内的图片url，一般为列表需遍历获取
                    if 'video_path' in articlejson['data'].keys():
                        fields["videos"] = articlejson['data']['video_path']  # 文章的视频链接地址
                        fields["videocover"] = articlejson['data']['pic_path']  # 文章的视频封面地址
                        fields["width"] = articlejson['data']['width']  # 文章的视频宽
                        fields["height"] = articlejson['data']['height']  # 文章的视频高
                    fields["source"] = articlejson['data']['app_name']  # 文章的来源
                    # fields["pubtime"] = articlejson['data']['updatedate']  # 文章的发布时间
                    fields["createtime"] = InitClass().date_time_stamp(articlejson['data']['create_time'])  # 文章的发布时间
                    # fields["updatetime"] = articlejson['data']['pubDate']  # 文章的更新时间
                    fields["likenum"] = getRealNum(articlejson['data']['good_num'])  # 文章的点赞数
                    # fields["playnum"] = articlejson['data']['link']  # 视频的播放数
                    fields["commentnum"] = getRealNum(articlejson['data']['comment_num'])  # 文章评论数
                    fields["readnum"] = getRealNum(articlejson['data']['click_num'])  # 文章的阅读数
                    # fields["trannum"] = articlejson['data']['link']  # 文章的转发数
                    # fields["sharenum"] = articlejson['data']['link']  # 文章分享数
                    # fields["author"] = articlejson['data']['author']  # 文章作者
                else:
                    print(articlejson)
                    fields["url"] = articlejson['data']['url']  # 文章的html网址，提取shareurl
                    fields["workerid"] = articlejson['data']['news_id']  # 文章的id
                    fields["title"] = articlejson['data']['title']  # 文章的标题
                    fields["content"] = articlejson['data']['content']  # 文章的内容详情
                    fields["articlecovers"] = articlejson['data']['pic_path']  # 文章的封面，一般为上面get到的字段
                    fields["images"] = articlejson['data']['pic_path']  # 文章详情内的图片url，一般为列表需遍历获取
                    # fields["videos"] = articlejson['data']['videourl']  # 文章的视频链接地址
                    # fields["videocover"] = articlejson['data']['link']  # 文章的视频封面地址
                    # fields["width"] = articlejson['data']['link']  # 文章的视频宽
                    # fields["height"] = articlejson['data']['link']  # 文章的视频高
                    # fields["source"] = articlejson['data']['source']  # 文章的来源
                    # fields["pubtime"] = articlejson['data']['updatedate']  # 文章的发布时间
                    fields["createtime"] = InitClass().date_time_stamp(articlejson['data']['create_time'])  # 文章的发布时间
                    # fields["updatetime"] = articlejson['data']['pubDate']  # 文章的更新时间
                    fields["likenum"] = getRealNum(articlejson['data']['good_num'])  # 文章的点赞数
                    # fields["playnum"] = articlejson['data']['link']  # 视频的播放数
                    fields["commentnum"] = getRealNum(articlejson['data']['comment_num'])  # 文章评论数
                    fields["readnum"] = getRealNum(articlejson['data']['click_num'])  # 文章的阅读数
                    # fields["trannum"] = articlejson['data']['link']  # 文章的转发数
                    # fields["sharenum"] = articlejson['data']['link']  # 文章分享数
                    # fields["author"] = articlejson['data']['author']  # 文章作者
                print(json.dumps(fields, indent=4, ensure_ascii=False))
            except Exception as e:
                print(e)

    def run(self):
        appParamsList = self.get_app_params().__next__()
        channelsres = {}
        for appParams in appParamsList:
            name = appParams['appurl']
            value = self.getchannels(appParams).__next__()
            channelsres[name] = value
        print(channelsres)
        channelsparams = self.analyzechannels(channelsres)
        articleparams = self.getarticlelistsparams(channelsparams.__next__())
        articles_ress = self.getarticlelists(articleparams.__next__())
        articles = self.analyze_articlelists(articles_ress.__next__())
        articlesparam = self.getarticleparams(articles.__next__())
        articles_html = self.getarticlehtml(articlesparam.__next__())
        self.analyzearticles(articles_html.__next__())


if __name__ == '__main__':
    spider = KaiPingXinWen('开屏新闻')
    spider.run()
