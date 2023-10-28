# -*- encoding:utf-8 -*-
"""
@功能:湖北日报解析模板
@AUTHOR：jovan
@文件名：HuBeiRiBao.py
@时间：2020年12月22日 15:58:24
"""

import json
import logging
import time

import requests

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


class HuBeiRiBao(Appspider):

    @staticmethod
    def get_app_params():
        # 这个是关注的频道列表
        url1 = "http://hbrbapi.hubeidaily.net/amc/client/listMemberSubscribe"
        headers1 = {
            "Host": "hbrbapi.hubeidaily.net",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.0",
            "If-Modified-Since": time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.localtime()),
        }
        data1 = {
            "versionName": "5.0.2",
            "deviceId": "c4cfcdc96ac1eb31",
            "memberId": "",
        }
        method1 = "get"
        app_params1 = InitClass().app_params(url1, headers1, method1, data=data1)
        # 这个是未关注的频道列表
        url2 = "http://hbrbapi.hubeidaily.net/amc/client/listFreeMemberSubscribe"
        headers2 = {
            "If-Modified-Since": time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.localtime()),
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; ALP-AL00 Build/HUAWEIALP-AL00)",
            "Host": "hbrbapi.hubeidaily.net",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        data2 = {
            "deviceId": "c4cfcdc96ac1eb31",
        }
        method2 = "get"
        app_params2 = InitClass().app_params(url2, headers2, method2, data=data2)
        # 这个是底部地方的选卡，但是在上个接口都有返回相同的，故不在请求。
        url3 = "http://hbrbapi.hubeidaily.net/amc/client/listLocalColumn"
        headers3 = {
            "If-Modified-Since": time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.localtime()),
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; ALP-AL00 Build/HUAWEIALP-AL00)",
            "Host": "hbrbapi.hubeidaily.net",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        data3 = {
            "nodeCode": "ecdc5307-888e-4322-8817-f04bd81a7e82",
            "parentId": "0",
        }
        method3 = "get"
        app_params3 = InitClass().app_params(url3, headers3, method3, data=data3)
        yield [app_params1, app_params2]

    def analyze_channel(self, channelsres):
        print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            channelList = json.loads(v)
            for k1, v2 in channelList["data"].items():
                for channel in v2:
                    channelid = channel['columnId']
                    channelname = channel['columnName']
                    channelType = channel['contentType']
                    channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channelType)
                    channelparams.append(channelparam)
                    # break
                    if 'existSubcolumn' in channel.keys() and channel['existSubcolumn']:
                        urlChild = 'http://hbrbapi.hubeidaily.net/amc/client/listLocalColumn'
                        headersChild = {
                            "If-Modified-Since": time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.localtime()),
                            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; ALP-AL00 Build/HUAWEIALP-AL00)",
                            "Host": "hbrbapi.hubeidaily.net",
                            "Connection": "Keep-Alive",
                            "Accept-Encoding": "gzip",
                        }
                        dataChild = {
                            "nodeCode": "ecdc5307-888e-4322-8817-f04bd81a7e82",
                            "parentId": channelid,
                        }
                        channelResChild = requests.get(urlChild, headers=headersChild,
                                                       params=dataChild).content.decode()
                        print(channelResChild)
                        channelDataChild = {
                            str(channelid): channelResChild,
                        }
                        channelsParamsChild = self.analyze_channel_child(channelDataChild)
                        channelparams.extend(channelsParamsChild.__next__())
        channelparam3 = InitClass().channel_fields(22, "直播", channeltype=0)
        channelparams.append(channelparam3)
        yield channelparams

    def analyze_channel_child(self, channelsres):
        print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            channelList = json.loads(v)
            for channel in channelList["data"]["list"]:
                channelid = channel['id']
                channelname = channel['name']
                channelType = channel['contentType']
                channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channelType)
                channelparams.append(channelparam)
                if 'existSubcolumn' in channel.keys() and channel['existSubcolumn']:
                    urlChild = 'http://hbrbapi.hubeidaily.net/amc/client/listLocalColumn'
                    headersChild = {
                        "If-Modified-Since": time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.localtime()),
                        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; ALP-AL00 Build/HUAWEIALP-AL00)",
                        "Host": "hbrbapi.hubeidaily.net",
                        "Connection": "Keep-Alive",
                        "Accept-Encoding": "gzip",
                    }
                    dataChild = {
                        "nodeCode": "ecdc5307-888e-4322-8817-f04bd81a7e82",
                        "parentId": channelid,
                    }
                    channelResChild = requests.get(urlChild, headers=headersChild,
                                                   params=dataChild).content.decode()
                    print(channelResChild)
                    channelDataChild = {
                        str(channelid): channelResChild,
                    }
                    channelsParamsChild = self.analyze_channel_child(channelDataChild)
                    channelparams.extend(channelsParamsChild.__next__())
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "http://hbrbapi.hubeidaily.net/amc/client/listContentByColumn"
        headers = {
            "oauth-token": "",
            "udid": "abeaaf99-9a55-4232-96c7-79ddba532c77",
            "Host": "cgi.voc.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.2.2",
        }
        method = 'get'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            data = {
                "column": channelid,
                "publishFlag": "1",
                "focusNo": "5",
                "pageNo": "0",
                "pageSize": "20",
            }
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid=channelid, data=data,
                                                                       channeltype=channeltype)
            articlelistsparams.append(articlelist_param)

        yield articlelistsparams

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            channel_type = articleslistres.get("channeltype")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    print(articleslists)
                    if 'data' in articleslists.keys():
                        if 'focusList' in articleslists['data']:  # banner
                            for bannerItem in articleslists['data']['focusList']:
                                article_fields = InitClass().article_fields()
                                article_fields["channelname"] = channelname  # 频道名称，字符串
                                article_fields["channelID"] = channelid  # 频道id，字符串
                                article_fields["channelType"] = channel_type  # 频道type，字符串
                                # article_fields["url"] = ''  # 分享的网址，字符串
                                article_fields["title"] = bannerItem['title']  # 文章标题，字符串
                                # article_fields["content"] = ''  # 文章内容，字符串
                                article_fields["articlecovers"] = [bannerItem['imgUrl']]  # 列表封面，数组
                                # article_fields["images"] = ''  # 正文图片，数组
                                # article_fields["videos"] = ''  # 视频地址，数组
                                # article_fields["videocover"] = ''  # 视频封面，数组
                                # article_fields["width"] = ''  # 视频宽，字符串
                                # article_fields["height"] = ''  # 视频高，字符串
                                # article_fields["source"] = ''  # 文章来源，字符串
                                # article_fields["pubtime"] = ''  # 发布时间，时间戳（毫秒级，13位）
                                # article_fields["createtime"] = ''  # 创建时间，时间戳（毫秒级，13位）
                                # article_fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
                                # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                                # article_fields["playnum"] = ''  # 播放数，数值
                                # article_fields["commentnum"] = ''  # 评论数，数值
                                # article_fields["readnum"] = ''  # 阅读数，数值
                                # article_fields["trannum"] = ''  # 转发数，数值
                                # article_fields["sharenum"] = ''  # 分享数，数值
                                # article_fields["author"] = ''  # 作者，字符串
                                article_fields["banner"] = 1  # banner标记，数值（0标识不是，1标识是）
                                # if 7 == bannerItem['contentType']:  # 专题
                                #     article_fields["specialtopic"] = 1
                                #     article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                                # else:
                                #     article_fields["specialtopic"] = 0
                                #     article_fields["workerid"] = bannerItem['contentId']  # 文章id，字符串
                                article_fields["workerid"] = bannerItem['contentId']  # 文章id，字符串
                                article_fields["specialtopic"] = 0  # 是否是专题，数值（0标识不是，1标识是）
                                # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                                # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                                article_fields["articleType"] = bannerItem['contentType']  # 文章类型，自己添加
                                if 'id' in bannerItem.keys():
                                    article_fields["liveRoomId"] = bannerItem['id']  # 直播详情需要，自己添加
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        if 'contentList' in articleslists['data']:
                            for newsItem in articleslists['data']['contentList']:
                                article_fields = InitClass().article_fields()
                                if 'isSpecialContent' in newsItem.keys() and 0 != newsItem['isSpecialContent']:
                                    print(newsItem)
                                article_fields["channelname"] = channelname  # 频道名称，字符串
                                article_fields["channelID"] = channelid  # 频道id，字符串
                                article_fields["channelType"] = channel_type  # 频道type，字符串
                                if 'shareUrl' in newsItem.keys():
                                    article_fields["url"] = newsItem['shareUrl']  # 分享的网址，字符串
                                if 'shareUlr' in newsItem.keys():
                                    article_fields["url"] = newsItem['shareUlr']  # 分享的网址，字符串
                                article_fields["title"] = newsItem['title']  # 文章标题，字符串
                                # article_fields["content"] = ''  # 文章内容，字符串
                                imgList = []
                                if 'imgUrl' in newsItem.keys():
                                    imgList.append(newsItem['imgUrl'])
                                if 'imgList' in newsItem.keys():
                                    for imgItem in newsItem['imgList']:
                                        for k, v in imgItem.items():
                                            if len(v):
                                                imgList.append(v)
                                article_fields["articlecovers"] = imgList  # 列表封面，数组
                                # article_fields["images"] = ''  # 正文图片，数组
                                # article_fields["videos"] = ''  # 视频地址，数组
                                # article_fields["videocover"] = ''  # 视频封面，数组
                                # article_fields["width"] = ''  # 视频宽，字符串
                                # article_fields["height"] = ''  # 视频高，字符串
                                if 'source' in newsItem.keys():
                                    article_fields["source"] = newsItem['source']  # 文章来源，字符串
                                # article_fields["pubtime"] = ''  # 发布时间，时间戳（毫秒级，13位）
                                # article_fields["createtime"] = ''  # 创建时间，时间戳（毫秒级，13位）
                                # article_fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
                                # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                                # article_fields["playnum"] = ''  # 播放数，数值
                                # article_fields["commentnum"] = ''  # 评论数，数值
                                # article_fields["readnum"] = ''  # 阅读数，数值
                                # article_fields["trannum"] = ''  # 转发数，数值
                                # article_fields["sharenum"] = ''  # 分享数，数值
                                # article_fields["author"] = ''  # 作者，字符串
                                article_fields["banner"] = 1  # banner标记，数值（0标识不是，1标识是）
                                # if 7 == bannerItem['contentType']:  # 专题
                                #     article_fields["specialtopic"] = 1
                                #     article_fields["topicid"] = newsItem['contentId']  # 专题id，字符串
                                # else:
                                #     article_fields["specialtopic"] = 0
                                #     article_fields["workerid"] = newsItem['contentId']  # 文章id，字符串
                                article_fields["workerid"] = newsItem['contentId']  # 文章id，字符串
                                article_fields["specialtopic"] = 0  # 是否是专题，数值（0标识不是，1标识是）
                                # article_fields["topicid"] = newsItem['contentId']  # 专题id，字符串
                                article_fields["articleType"] = newsItem['contentType']  # 文章类型，自己添加
                                if 'id' in newsItem.keys():
                                    article_fields["liveRoomId"] = newsItem['id']  # 直播详情需要，自己添加
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                    else:
                        print(articleslists)
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        for article in articles:
            article_field = article.get('articelField')
            articleType = article_field.get("articleType")
            if 1 == articleType:  # 活动
                print(article)
            elif 2 == articleType:  # 抽奖
                print(article)
            elif 3 == articleType:  # 投票
                print(article)
            elif 4 == articleType:  # 直播
                url = "http://hbrbapi.hubeidaily.net/amc/client/getLiveroomInfo"
                headers = {
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; ALP-AL00 Build/HUAWEIALP-AL00)",
                    "Host": "hbrbapi.hubeidaily.net",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                data = {
                    "cId": article_field.get('workerid'),
                    "liveroomId": article_field.get('liveRoomId'),
                }
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, data=data, sleeptime=1,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            elif 5 == articleType:  # 新闻111
                url = "http://hbrbapi.hubeidaily.net/amc/client/getImageTextContentById"
                headers = {
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; ALP-AL00 Build/HUAWEIALP-AL00)",
                    "Host": "hbrbapi.hubeidaily.net",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                if article_field.get("specialtopic") == 1:
                    data = {
                        "cId": article_field.get('topicid'),
                        "contentId": article_field.get('workerid'),
                        "fromFlag": "0",
                        "deviceId": "c4cfcdc96ac1eb31",
                    }
                else:
                    data = {
                        "contentId": article_field.get('workerid'),
                        "fromFlag": "0",
                        "deviceId": "c4cfcdc96ac1eb31",
                    }
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, data=data, sleeptime=1,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            elif 6 == articleType:  # 图集111
                url = "http://hbrbapi.hubeidaily.net/amc/client/getAtlasContentById"
                headers = {
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; ALP-AL00 Build/HUAWEIALP-AL00)",
                    "Host": "hbrbapi.hubeidaily.net",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                if article_field.get("specialtopic") == 1:
                    data = {
                        "cId": article_field.get('topicid'),
                        "contentId": article_field.get('workerid'),
                        "fromFlag": "0",
                        "deviceId": "c4cfcdc96ac1eb31",
                    }
                else:
                    data = {
                        "contentId": article_field.get('workerid'),
                        "fromFlag": "0",
                        "deviceId": "c4cfcdc96ac1eb31",
                    }
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, data=data, sleeptime=1,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            elif 7 == articleType:  # 专题111
                url = "http://hbrbapi.hubeidaily.net/amc/client/getSpecialContentById"
                headers = {
                    "If-Modified-Since": time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.localtime()),
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; ALP-AL00 Build/HUAWEIALP-AL00)",
                    "Host": "hbrbapi.hubeidaily.net",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                data = {
                    "contentId": article_field.get('workerid'),
                    "pageSize": "5",
                }
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, data=data, sleeptime=1,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            elif 8 == articleType:  # 广告
                print(article)
            elif 9 == articleType:  # 视频111
                url = "http://hbrbapi.hubeidaily.net/amc/client/getVideoContentById"
                headers = {
                    "If-Modified-Since": time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.localtime()),
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; ALP-AL00 Build/HUAWEIALP-AL00)",
                    "Host": "hbrbapi.hubeidaily.net",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                if article_field.get("specialtopic") == 1:
                    data = {
                        "cId": article_field.get('topicid'),
                        "contentId": article_field.get('workerid'),
                        "fromFlag": "0",
                        "deviceId": "c4cfcdc96ac1eb31",
                    }
                else:
                    data = {
                        "contentId": article_field.get('workerid'),
                        "fromFlag": "0",
                        "deviceId": "c4cfcdc96ac1eb31",
                    }
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, data=data, sleeptime=1,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            elif 10 == articleType:  # 问卷
                print(article)
            elif 11 == articleType:  # 音频，测试是政情111
                url = "http://hbrbapi.hubeidaily.net/amc/client/getSpecialContentsForColumn"
                headers = {
                    "If-Modified-Since": time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.localtime()),
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; ALP-AL00 Build/HUAWEIALP-AL00)",
                    "Host": "hbrbapi.hubeidaily.net",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                data = {
                    "contentId": article_field.get('workerid'),
                    "pageNo": "0",
                    "pageSize": "10",
                }
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, data=data, sleeptime=1,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            elif 12 == articleType:  # 外链111
                url = "http://hbrbapi.hubeidaily.net/amc/client/getOuterLinkById"
                headers = {
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; ALP-AL00 Build/HUAWEIALP-AL00)",
                    "Host": "hbrbapi.hubeidaily.net",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                if article_field.get("specialtopic") == 1:
                    data = {
                        "cId": article_field.get('topicid'),
                        "contentId": article_field.get('workerid'),
                        "fromFlag": "0",
                        "deviceId": "c4cfcdc96ac1eb31",
                    }
                else:
                    data = {
                        "contentId": article_field.get('workerid'),
                        "fromFlag": "0",
                        "site": "app",
                    }
                method = 'get'
                articleparam = InitClass().article_params_fields(url, headers, method, data=data, sleeptime=1,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            elif 13 == articleType:  # 专栏
                print(article)
            elif 14 == articleType:  #
                print(article)
            elif 15 == articleType:  #
                print(article)
            elif 16 == articleType:  # 报料
                print(article)
            else:
                print(article)
        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            appname = article.get("appname")
            fields = article.get("articleField")
            articleType = fields.get("articleType")
            try:
                contentJson = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                if 1 == contentJson['suc']:
                    newsDetail = contentJson['data']
                    if 1 == articleType:  # 活动
                        print(newsDetail)
                    elif 2 == articleType:  # 抽奖
                        print(newsDetail)
                    elif 3 == articleType:  # 投票
                        print(newsDetail)
                    elif 4 == articleType:  # 直播
                        fields["appname"] = article['appname']  # 应用名称，字符串
                        # fields["channelname"] = ''  # 频道名称，字符串
                        # fields["channelID"] = ''  # 频道id，字符串
                        # fields["channelType"] = ''  # 频道type，字符串
                        fields["url"] = newsDetail['shareUrl']  # 分享的网址，字符串
                        # fields["workerid"] = ''  # 文章id，字符串
                        # fields["title"] = ''  # 文章标题，字符串
                        # fields["content"] = newsDetail['text']  # 文章内容，字符串
                        # fields["articlecovers"] = ''  # 列表封面，数组
                        # fields["images"] = ''  # 正文图片，数组
                        fields["videos"] = [newsDetail['playUrl']]  # 视频地址，数组
                        # fields["videocover"] = ''  # 视频封面，数组
                        # fields["width"] = ''  # 视频宽，字符串
                        # fields["height"] = ''  # 视频高，字符串
                        # fields["source"] = newsDetail['source']  # 文章来源，字符串
                        fields["pubtime"] = InitClass().date_time_stamp(newsDetail['startTime'])  # 发布时间，时间戳（毫秒级，13位）
                        # fields["createtime"] = ''  # 创建时间，时间戳（毫秒级，13位）
                        # fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
                        # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                        # fields["playnum"] = ''  # 播放数，数值
                        # fields["commentnum"] = newsDetail['commentCount']  # 评论数，数值
                        # fields["readnum"] = ''  # 阅读数，数值
                        # fields["trannum"] = ''  # 转发数，数值
                        # fields["sharenum"] = ''  # 分享数，数值
                        # fields["author"] = ''  # 作者，字符串
                        # fields["banner"] = ''  # banner标记，数值（0标识不是，1标识是）
                        # fields["specialtopic"] = 0  # 是否是专题，数值（0标识不是，1标识是）
                        # fields["topicid"] = ''  # 专题id，字符串
                    elif 5 == articleType:  # 新闻111
                        fields["appname"] = article['appname']  # 应用名称，字符串
                        # fields["channelname"] = ''  # 频道名称，字符串
                        # fields["channelID"] = ''  # 频道id，字符串
                        # fields["channelType"] = ''  # 频道type，字符串
                        fields["url"] = newsDetail['shareUlr']  # 分享的网址，字符串
                        # fields["workerid"] = ''  # 文章id，字符串
                        # fields["title"] = ''  # 文章标题，字符串
                        fields["content"] = newsDetail['text']  # 文章内容，字符串
                        # fields["articlecovers"] = ''  # 列表封面，数组
                        # fields["images"] = ''  # 正文图片，数组
                        # fields["videos"] = ''  # 视频地址，数组
                        # fields["videocover"] = ''  # 视频封面，数组
                        # fields["width"] = ''  # 视频宽，字符串
                        # fields["height"] = ''  # 视频高，字符串
                        fields["source"] = newsDetail['source']  # 文章来源，字符串
                        fields["pubtime"] = InitClass().date_time_stamp(newsDetail['publishTime'])  # 发布时间，时间戳（毫秒级，13位）
                        # fields["createtime"] = ''  # 创建时间，时间戳（毫秒级，13位）
                        # fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
                        # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                        # fields["playnum"] = ''  # 播放数，数值
                        fields["commentnum"] = newsDetail['commentCount']  # 评论数，数值
                        # fields["readnum"] = ''  # 阅读数，数值
                        # fields["trannum"] = ''  # 转发数，数值
                        # fields["sharenum"] = ''  # 分享数，数值
                        # fields["author"] = ''  # 作者，字符串
                        # fields["banner"] = ''  # banner标记，数值（0标识不是，1标识是）
                        # fields["specialtopic"] = 0  # 是否是专题，数值（0标识不是，1标识是）
                        # fields["topicid"] = ''  # 专题id，字符串
                    elif 6 == articleType:  # 图集111
                        fields["appname"] = article['appname']  # 应用名称，字符串
                        # fields["channelname"] = ''  # 频道名称，字符串
                        # fields["channelID"] = ''  # 频道id，字符串
                        # fields["channelType"] = ''  # 频道type，字符串
                        fields["url"] = newsDetail['shareUlr']  # 分享的网址，字符串
                        # fields["workerid"] = ''  # 文章id，字符串
                        # fields["title"] = ''  # 文章标题，字符串
                        # fields["content"] = newsDetail['text']  # 文章内容，字符串
                        # fields["articlecovers"] = ''  # 列表封面，数组
                        ingList = []
                        for pic in newsDetail['pictureList']:
                            ingList.append(pic['imagePath'])
                        fields["images"] = ingList  # 正文图片，数组
                        # fields["videos"] = ''  # 视频地址，数组
                        # fields["videocover"] = ''  # 视频封面，数组
                        # fields["width"] = ''  # 视频宽，字符串
                        # fields["height"] = ''  # 视频高，字符串
                        # fields["source"] = newsDetail['source']  # 文章来源，字符串
                        fields["pubtime"] = InitClass().date_time_stamp(newsDetail['publishTime'])  # 发布时间，时间戳（毫秒级，13位）
                        # fields["createtime"] = ''  # 创建时间，时间戳（毫秒级，13位）
                        # fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
                        # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                        # fields["playnum"] = ''  # 播放数，数值
                        fields["commentnum"] = newsDetail['commentCount']  # 评论数，数值
                        # fields["readnum"] = ''  # 阅读数，数值
                        # fields["trannum"] = ''  # 转发数，数值
                        # fields["sharenum"] = ''  # 分享数，数值
                        # fields["author"] = ''  # 作者，字符串
                        # fields["banner"] = ''  # banner标记，数值（0标识不是，1标识是）
                        # fields["specialtopic"] = 0  # 是否是专题，数值（0标识不是，1标识是）
                        # fields["topicid"] = ''  # 专题id，字符串
                    elif 7 == articleType:  # 专题111
                        topicFields = InitClass().topic_fields()
                        topicFields["_id"] = newsDetail['contentId']  # 专题id，app内唯一标识
                        topicFields["platformName"] = article['appname']  # 平台名字（app名字）
                        topicFields["platformID"] = ''  #
                        topicFields["channelName"] = fields['channelname']  # 频道名字
                        topicFields["channelID"] = fields['channelID']  # 频道id
                        topicFields["topicUrl"] = newsDetail['shareUlr']  # topicUrl
                        topicFields["title"] = newsDetail['specialTitle']  #
                        topicFields["digest"] = newsDetail['introduction']  # 简介，摘要
                        topicFields["topicCover"] = [newsDetail['imgUrl']]  # list(),
                        # topicFields["pubTime"] = ''  # 时间戳
                        # topicFields["articleNum"] = ''  # 专题内的文章数量
                        # topicFields["newestArticleID"] = ''  # 最新发布的文章id
                        # topicFields["newestPubtime"] = ''  #
                        # topicFields["articleIDs"] = ''  # 专题内的文章ID
                        # topicFields["articlesNumPerHour"] = ''
                        # topicFields["original"] = ''
                        # topicFields["firstMedia"] = ''
                        # topicFields["transPower"] = ''
                        # topicFields["hotDegree"] = ''
                        # topicFields["wordsFreq"] = ''
                        # topicFields["hotDegreeTrend"] = ''
                        # topicFields["emotionTrend"] = ''
                        # topicFields["region"] = ''
                        # topicFields["spreadPath"] = ''
                        topicFields["createTime"] = newsDetail['createTime']
                        # topicFields["updateTime"] = ''
                        topicArticles = self.getTopicArticles(newsDetail['contentId'], newsDetail['contentClassifys'])
                        articleparams = self.getarticleparams(topicArticles.__next__())
                        articlesres = self.getarticlehtml(articleparams.__next__())
                        self.analyzearticle(articlesres.__next__())
                    elif 8 == articleType:  # 广告
                        print(newsDetail)
                    elif 9 == articleType:  # 视频111
                        fields["appname"] = article['appname']  # 应用名称，字符串
                        # fields["channelname"] = ''  # 频道名称，字符串
                        # fields["channelID"] = ''  # 频道id，字符串
                        # fields["channelType"] = ''  # 频道type，字符串
                        fields["url"] = newsDetail['shareUlr']  # 分享的网址，字符串
                        # fields["workerid"] = ''  # 文章id，字符串
                        # fields["title"] = ''  # 文章标题，字符串
                        # fields["content"] = newsDetail['text']  # 文章内容，字符串
                        # fields["articlecovers"] = ''  # 列表封面，数组
                        # fields["images"] = ''  # 正文图片，数组
                        videoList = []
                        for videoItem in newsDetail['videoList']:
                            for video in videoItem['playUrls']:
                                videoList.append(video['playUrl'])
                        fields["videos"] = videoList  # 视频地址，数组
                        # fields["videocover"] = ''  # 视频封面，数组
                        fields["width"] = ''  # 视频宽，字符串
                        fields["height"] = ''  # 视频高，字符串
                        # fields["source"] = newsDetail['source']  # 文章来源，字符串
                        fields["pubtime"] = InitClass().date_time_stamp(newsDetail['publishTime'])  # 发布时间，时间戳（毫秒级，13位）
                        # fields["createtime"] = ''  # 创建时间，时间戳（毫秒级，13位）
                        # fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
                        # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                        # fields["playnum"] = ''  # 播放数，数值
                        fields["commentnum"] = newsDetail['commentCount']  # 评论数，数值
                        # fields["readnum"] = ''  # 阅读数，数值
                        # fields["trannum"] = ''  # 转发数，数值
                        # fields["sharenum"] = ''  # 分享数，数值
                        # fields["author"] = ''  # 作者，字符串
                        # fields["banner"] = ''  # banner标记，数值（0标识不是，1标识是）
                        # fields["specialtopic"] = 0  # 是否是专题，数值（0标识不是，1标识是）
                        # fields["topicid"] = ''  # 专题id，字符串
                    elif 10 == articleType:  # 问卷
                        print(newsDetail)
                    elif 11 == articleType:  # 音频，测试是政情111
                        print(newsDetail)
                        topicFields = InitClass().topic_fields()
                        topicFields["_id"] = newsDetail['contentId']  # 专题id，app内唯一标识
                        topicFields["platformName"] = article['appname']  # 平台名字（app名字）
                        topicFields["platformID"] = ''  #
                        topicFields["channelName"] = fields['channelname']  # 频道名字
                        topicFields["channelID"] = fields['channelID']  # 频道id
                        topicFields["topicUrl"] = newsDetail['shareUlr']  # topicUrl
                        topicFields["title"] = newsDetail['specialTitle']  #
                        topicFields["digest"] = newsDetail['introduction'] + newsDetail['detailed']  # 简介，摘要
                        topicFields["topicCover"] = [newsDetail['imgUrl']]  # list(),
                        # topicFields["pubTime"] = ''  # 时间戳
                        # topicFields["articleNum"] = ''  # 专题内的文章数量
                        # topicFields["newestArticleID"] = ''  # 最新发布的文章id
                        # topicFields["newestPubtime"] = ''  #
                        # topicFields["articleIDs"] = ''  # 专题内的文章ID
                        # topicFields["articlesNumPerHour"] = ''
                        # topicFields["original"] = ''
                        # topicFields["firstMedia"] = ''
                        # topicFields["transPower"] = ''
                        # topicFields["hotDegree"] = ''
                        # topicFields["wordsFreq"] = ''
                        # topicFields["hotDegreeTrend"] = ''
                        # topicFields["emotionTrend"] = ''
                        # topicFields["region"] = ''
                        # topicFields["spreadPath"] = ''
                        topicFields["createTime"] = newsDetail['createTime']
                        # topicFields["updateTime"] = ''
                        zqArticles = self.getZQArticles(newsDetail['contentId'], newsDetail['specialTitle'],
                                                        newsDetail['contents'])
                        articleparams = self.getarticleparams(zqArticles.__next__())
                        articlesres = self.getarticlehtml(articleparams.__next__())
                        self.analyzearticle(articlesres.__next__())
                    elif 12 == articleType:  # 外链111
                        fields["appname"] = article['appname']  # 应用名称，字符串
                        # fields["channelname"] = ''  # 频道名称，字符串
                        # fields["channelID"] = ''  # 频道id，字符串
                        # fields["channelType"] = ''  # 频道type，字符串
                        fields["url"] = newsDetail['shareUlr']  # 分享的网址，字符串
                        # fields["workerid"] = ''  # 文章id，字符串
                        # fields["title"] = ''  # 文章标题，字符串
                        fields["content"] = newsDetail['linkUrl']  # 文章内容，字符串
                        # fields["articlecovers"] = ''  # 列表封面，数组
                        # fields["images"] = ''  # 正文图片，数组
                        # fields["videos"] = ''  # 视频地址，数组
                        # fields["videocover"] = ''  # 视频封面，数组
                        # fields["width"] = ''  # 视频宽，字符串
                        # fields["height"] = ''  # 视频高，字符串
                        # fields["source"] = newsDetail['source']  # 文章来源，字符串
                        # fields["pubtime"] = InitClass().date_time_stamp(newsDetail['publishTime'])  # 发布时间，时间戳（毫秒级，13位）
                        # fields["createtime"] = ''  # 创建时间，时间戳（毫秒级，13位）
                        # fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
                        # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                        # fields["playnum"] = ''  # 播放数，数值
                        # fields["commentnum"] = newsDetail['commentCount']  # 评论数，数值
                        # fields["readnum"] = ''  # 阅读数，数值
                        # fields["trannum"] = ''  # 转发数，数值
                        # fields["sharenum"] = ''  # 分享数，数值
                        # fields["author"] = ''  # 作者，字符串
                        # fields["banner"] = ''  # banner标记，数值（0标识不是，1标识是）
                        # fields["specialtopic"] = 0  # 是否是专题，数值（0标识不是，1标识是）
                        # fields["topicid"] = ''  # 专题id，字符串
                    elif 13 == articleType:  # 专栏
                        print(newsDetail)
                    elif 14 == articleType:  #
                        print(newsDetail)
                    elif 15 == articleType:  #
                        print(newsDetail)
                    elif 16 == articleType:  # 报料
                        print(newsDetail)
                    else:
                        print(newsDetail)
                else:
                    print("请求失败的新闻", '===', fields['channelname'], '===', fields['title'], )
                print(json.dumps(fields, indent=4, ensure_ascii=False))
            except Exception as e:
                num += 1
                logging.info(f"错误数量{num},{e}")

    def getTopicArticles(self, topicId, topicNewsList):
        articlesparams = []
        for topicNewsItem in topicNewsList:
            for topicNews in topicNewsItem['contents']:
                article_fields = InitClass().article_fields()
                if 'isSpecialContent' in topicNews.keys() and 0 != topicNews['isSpecialContent']:
                    print(topicNews)
                # article_fields["channelname"] = channelname  # 频道名称，字符串
                # article_fields["channelID"] = channelid  # 频道id，字符串
                # article_fields["channelType"] = channel_type  # 频道type，字符串
                # if 'shareUrl' in newsItem.keys():
                #     article_fields["url"] = newsItem['shareUrl']  # 分享的网址，字符串
                # if 'shareUlr' in newsItem.keys():
                #     article_fields["url"] = newsItem['shareUlr']  # 分享的网址，字符串
                article_fields["workerid"] = topicNews['contentId']  # 文章id，字符串
                article_fields["title"] = topicNews['contentTitle']  # 文章标题，字符串
                # article_fields["content"] = ''  # 文章内容，字符串
                imgList = []
                # if 'imgUrl' in topicNews.keys():
                #     imgList.append(topicNews['imgUrl'])
                if 'imgList' in topicNews.keys():
                    for imgItem in topicNews['imgList']:
                        for k, v in imgItem.items():
                            if len(v):
                                imgList.append(v)
                article_fields["articlecovers"] = imgList  # 列表封面，数组
                # article_fields["images"] = ''  # 正文图片，数组
                # article_fields["videos"] = ''  # 视频地址，数组
                # article_fields["videocover"] = ''  # 视频封面，数组
                # article_fields["width"] = ''  # 视频宽，字符串
                # article_fields["height"] = ''  # 视频高，字符串
                if 'source' in topicNews.keys():
                    article_fields["source"] = topicNews['source']  # 文章来源，字符串
                # article_fields["pubtime"] = ''  # 发布时间，时间戳（毫秒级，13位）
                # article_fields["createtime"] = ''  # 创建时间，时间戳（毫秒级，13位）
                # article_fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
                # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                # article_fields["playnum"] = ''  # 播放数，数值
                # article_fields["commentnum"] = ''  # 评论数，数值
                # article_fields["readnum"] = ''  # 阅读数，数值
                # article_fields["trannum"] = ''  # 转发数，数值
                # article_fields["sharenum"] = ''  # 分享数，数值
                # article_fields["author"] = ''  # 作者，字符串
                article_fields["banner"] = 0  # banner标记，数值（0标识不是，1标识是）
                article_fields["specialtopic"] = 1  # 是否是专题，数值（0标识不是，1标识是）
                article_fields["topicid"] = topicId  # 专题id，字符串
                article_fields["articleType"] = topicNews['contentType']  # 文章类型，自己添加
                articleparam = InitClass().article_list_fields()
                articleparam["articelField"] = article_fields
                articlesparams.append(articleparam)

        yield articlesparams

    def getZQArticles(self, topicId, topicName, topicNewsList):
        articlesparams = []
        for topicNews in topicNewsList:
            article_fields = InitClass().article_fields()
            if 'isSpecialContent' in topicNews.keys() and 0 != topicNews['isSpecialContent']:
                print(topicNews)
            # article_fields["channelname"] = channelname  # 频道名称，字符串
            # article_fields["channelID"] = channelid  # 频道id，字符串
            # article_fields["channelType"] = channel_type  # 频道type，字符串
            # if 'shareUrl' in newsItem.keys():
            #     article_fields["url"] = newsItem['shareUrl']  # 分享的网址，字符串
            # if 'shareUlr' in newsItem.keys():
            #     article_fields["url"] = newsItem['shareUlr']  # 分享的网址，字符串
            article_fields["workerid"] = topicNews['contentId']  # 文章id，字符串
            article_fields["title"] = topicNews['contentTitle']  # 文章标题，字符串
            # article_fields["content"] = ''  # 文章内容，字符串
            imgList = []
            # if 'imgUrl' in topicNews.keys():
            #     imgList.append(topicNews['imgUrl'])
            if 'imgList' in topicNews.keys():
                for imgItem in topicNews['imgList']:
                    for k, v in imgItem.items():
                        if len(v):
                            imgList.append(v)
            article_fields["articlecovers"] = imgList  # 列表封面，数组
            # article_fields["images"] = ''  # 正文图片，数组
            # article_fields["videos"] = ''  # 视频地址，数组
            # article_fields["videocover"] = ''  # 视频封面，数组
            # article_fields["width"] = ''  # 视频宽，字符串
            # article_fields["height"] = ''  # 视频高，字符串
            if 'source' in topicNews.keys():
                article_fields["source"] = topicNews['source']  # 文章来源，字符串
            # article_fields["pubtime"] = ''  # 发布时间，时间戳（毫秒级，13位）
            # article_fields["createtime"] = ''  # 创建时间，时间戳（毫秒级，13位）
            # article_fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
            # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
            # article_fields["playnum"] = ''  # 播放数，数值
            # article_fields["commentnum"] = ''  # 评论数，数值
            # article_fields["readnum"] = ''  # 阅读数，数值
            # article_fields["trannum"] = ''  # 转发数，数值
            # article_fields["sharenum"] = ''  # 分享数，数值
            # article_fields["author"] = ''  # 作者，字符串
            article_fields["banner"] = 0  # banner标记，数值（0标识不是，1标识是）
            article_fields["specialtopic"] = 2  # 是否是专题，数值（0标识不是，1标识是）
            article_fields["topicid"] = topicId  # 专题id，字符串
            article_fields["articleType"] = topicNews['contentType']  # 文章类型，自己添加
            articleparam = InitClass().article_list_fields()
            articleparam["articelField"] = article_fields
            articlesparams.append(articleparam)

        yield articlesparams

    def run(self):
        appParamsList = self.get_app_params().__next__()
        channelsres = {}
        for appParams in appParamsList:
            name = appParams['appurl']
            value = self.getchannels(appParams).__next__()
            channelsres[name] = value
        channelsparams = self.analyze_channel(channelsres)
        articlelistparames = self.getarticlelistparams(channelsparams.__next__())
        articleslistsres = self.getarticlelists(articlelistparames.__next__())
        articles = self.analyze_articlelists(articleslistsres.__next__())
        articleparams = self.getarticleparams(articles.__next__())
        articlesres = self.getarticlehtml(articleparams.__next__())
        self.analyzearticle(articlesres.__next__())


if __name__ == '__main__':
    appspider = HuBeiRiBao("湖北日报")
    appspider.run()
