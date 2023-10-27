# -*- encoding:utf-8 -*-
"""
@功能:湖北日报解析模板
@AUTHOR：jovan
@文件名：HuBeiRiBao.py
@时间：2020年12月22日 15:58:24
有的新闻正文被删除了会报错
"""

import json
import logging
import time

import requests

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass

channelTypeDir = {}


def setListNewsParam(articlesparams, channelname, channelid, banner, item):
    try:
        article_fields = InitClass().article_fields()
        # if 'channelName' in item.keys():
        #     article_fields["channelname"] = item['channelName']  # 频道名称，字符串
        # else:
        article_fields["channelname"] = channelname  # 频道名称，字符串
        # if 'channelId' in item.keys():
        #     article_fields["channelID"] = item['channelId']  # 频道id，字符串
        # else:
        article_fields["channelID"] = channelid  # 频道id，字符串
        # article_fields["channelType"] = channel_type  # 频道type，字符串
        if 'linkUrl' in item.keys():
            article_fields["url"] = item['linkUrl']  # 分享的网址，字符串
        article_fields["title"] = item['title']  # 文章标题，字符串
        # article_fields["content"] = item['webLink']  # 文章内容，字符串
        imgList = []
        if 'guideImage' in item.keys() and len(item['guideImage']):
            imgList.append(item['guideImage'])
        if 'guideImage2' in item.keys() and len(item['guideImage2']):
            imgList.append(item['guideImage2'])
        if 'guideImage3' in item.keys() and len(item['guideImage3']):
            imgList.append(item['guideImage3'])
        if 'guideImage4' in item.keys() and len(item['guideImage4']):
            imgList.append(item['guideImage4'])
        if 'guideImage5' in item.keys() and len(item['guideImage5']):
            imgList.append(item['guideImage5'])
        if 'guideImage6' in item.keys() and len(item['guideImage6']):
            imgList.append(item['guideImage6'])
        if 'guideimagetop' in item.keys() and len(item['guideimagetop']):
            imgList.append(item['guideimagetop'])
        article_fields["articlecovers"] = imgList  # 列表封面，数组
        # article_fields["images"] = ''  # 正文图片，数组
        # article_fields["videocover"] = [item['videoImg']]  # 视频封面，数组
        videoList = []
        if 'videoOrAudio' in item.keys() and len(item['videoOrAudio']):
            videoList.append(item['videoOrAudio'])
        if 'video' in item.keys() and len(item['video']):
            if isinstance(item['video'], str):
                videoList.append(item['video'])
            elif isinstance(item['video'], dict):
                # http://vfile.zhyantai.com/2020/1606/5515/0672/160655150672.ssm/160655150672.m3u8
                if 'host' in item['video'].keys() and 'filepath' in item['video'].keys() and 'filename' in item[
                    'video'].keys():
                    videoUrl = item['video']['host'] + "/" + item['video']['filepath'] + item['video']['filename']
                    videoList.append(videoUrl)
                else:
                    print(item['video'])
            else:
                print(item)
        article_fields["videos"] = videoList  # 视频地址，数组
        # article_fields["width"] = ''  # 视频宽，字符串
        # article_fields["height"] = ''  # 视频高，字符串
        if 'source' in item.keys():
            article_fields["source"] = item['source']  # 文章来源，字符串
        if 'pubDate' in item.keys():
            article_fields["pubtime"] = InitClass().date_time_stamp(item['pubDate'])  # 发布时间，时间戳（毫秒级，13位）
        # article_fields["createtime"] = item['createdate']  # 创建时间，时间戳（毫秒级，13位）
        # article_fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
        # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
        # article_fields["playnum"] = ''  # 播放数，数值
        # article_fields["commentnum"] = item['commentNum']  # 评论数，数值
        # article_fields["readnum"] = ''  # 阅读数，数值
        # article_fields["trannum"] = ''  # 转发数，数值
        # article_fields["sharenum"] = ''  # 分享数，数值
        # article_fields["author"] = ''  # 作者，字符串
        article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
        if 'newsId' in item.keys():
            article_fields["workerid"] = item['newsId']  # 文章id，字符串
        elif 'id' in item.keys():
            article_fields["workerid"] = item['id']  # 文章id，字符串
        else:
            print(item)
        # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
        # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
        if 'newsType' in item.keys():
            article_fields["newstype"] = item['newsType']  # 自己添加新闻类型
        articleparam = InitClass().article_list_fields()
        articleparam["articelField"] = article_fields
        articlesparams.append(articleparam)
    except Exception as e:
        logging.info(e)
    return articlesparams


class YanTaiShiKe(Appspider):

    @staticmethod
    def get_app_params():
        url1 = "http://api.jiaodong.net/ytnews/V13/News/getChannels"
        headers = {
            "Accept-Language": "zh-CN,zh;q=0.8",
            "User-Agent": "okhttp-okgo/jeasonlzy",
            "Host": "api.jiaodong.net",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Cookie": "security_session_verify=780d375084ae8c629b2c0f2e96b4f219; security_session_verify=780d375084ae8c629b2c0f2e96b4f219; security_session_verify=780d375084ae8c629b2c0f2e96b4f219",
        }
        method = "get"
        app_params1 = InitClass().app_params(url1, headers, method)

        yield [app_params1]

    def analyze_channel(self, channelsres):
        print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            if 'http://api.jiaodong.net/ytnews/V13/News/getChannels' == k:
                channelList = json.loads(v)
                for channel in channelList['data']:
                    channelid = channel['channelid']
                    channelname = channel['channelname']
                    channelType = channel['style']
                    guideid = -1
                    guideid_ext1 = -1
                    if channel['guideid'] is not None:
                        guideid = channel['guideid']
                    if channel['guideid_ext1'] is not None:
                        guideid_ext1 = channel['guideid_ext1']
                    channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channelType,
                                                              categoryid=guideid, categoryname=guideid_ext1)
                    channelparams.append(channelparam)
        channelparam1 = InitClass().channel_fields(143, "微视", channeltype="hjnews",
                                                   categoryid=-1, categoryname=-1)
        channelparams.append(channelparam1)
        channelparam2 = InitClass().channel_fields(2032000000000000, "直播", channeltype="jdnews",
                                                   categoryid=-1, categoryname=-1)
        channelparams.append(channelparam2)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channelType = channel.get("channeltype")
            categoryidId = channel.get("categoryid")
            categoryName = channel.get("categoryname")
            channelTypeDir[channelid] = channelType
            url = ""
            headers = {
                "Accept-Language": "zh-CN,zh;q=0.8",
                "User-Agent": "okhttp-okgo/jeasonlzy",
                "Host": "api.jiaodong.net",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "Cookie": "security_session_verify=780d375084ae8c629b2c0f2e96b4f219; security_session_verify=780d375084ae8c629b2c0f2e96b4f219; security_session_verify=780d375084ae8c629b2c0f2e96b4f219",
            }
            method = "get"
            if "海螺号" == channelname:
                url = f"http://api.jiaodong.net/ytnews/V13/Blog/getLine?page_count=20&news_type=0&uid="
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           channelid=channelid)
                articlelistsparams.append(articlelist_param)
            else:
                if "northnews" == channelType:
                    print(channel)  # 未出现
                elif "hjnews" == channelType:
                    url = f"http://api.jiaodong.net/ytnews/V13/HJNews/getNews?column_id=143&page=1&pagesize=20"
                    articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                               channelid=channelid)
                    articlelistsparams.append(articlelist_param)
                elif "politics" == channelType:  # 问政
                    url = f"http://api.jiaodong.net/ytnews/V13/Politics/getLives?p=1&pageSize=20"
                    articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                               channelid=channelid)
                    articlelistsparams.append(articlelist_param)
                else:  # jdnews
                    if int(categoryidId) != -1:
                        url = f"http://api.jiaodong.net/ytnews/V13/News/getBlockNews?guideid={categoryidId}"
                        articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                                   banners=1,
                                                                                   channelid=channelid)
                        articlelistsparams.append(articlelist_param)
                    if int(categoryName) != -1:
                        url = f"http://api.jiaodong.net/ytnews/V13/News/getBlockNews?guideid={categoryName}"
                        articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                                   channelid=channelid)
                        articlelistsparams.append(articlelist_param)

                    url = f"http://api.jiaodong.net/ytnews/V13/News/getNews?channelid={channelid}&page_count=20&news_type=0&uid= "
                    articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                               channelid=channelid)
                    articlelistsparams.append(articlelist_param)
        yield articlelistsparams

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            banner = articleslistres.get('banner')
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    print(articleslists)
                    if 'data' in articleslists.keys():
                        for item in articleslists['data']:
                            articlesparams = setListNewsParam(articlesparams, channelname, channelid, banner, item)

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
            workerid = article_field.get('workerid')
            channelID = article_field.get('channelID')
            channelname = article_field.get('channelname')
            newsType = article_field.get('newstype')
            url = ""
            headers = {
                "Accept-Language": "zh-CN,zh;q=0.8",
                "User-Agent": "okhttp-okgo/jeasonlzy",
                "Host": "api.jiaodong.net",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "Cookie": "security_session_verify=780d375084ae8c629b2c0f2e96b4f219; security_session_verify=780d375084ae8c629b2c0f2e96b4f219; security_session_verify=780d375084ae8c629b2c0f2e96b4f219",
            }
            method = "get"
            if "海螺号" == channelname:
                url = f"http://api.jiaodong.net/ytnews/V13/Blog/blogNewsDetail?newsid={workerid}"
            else:
                if channelID in channelTypeDir.keys():
                    if "northnews" == channelTypeDir[channelID]:
                        print(article)  # 未出现
                        continue
                    elif "hjnews" == channelTypeDir[channelID]:  # 微视
                        url = f"http://api.jiaodong.net/ytnews/V13/HJNews/getNewsInfo?id={workerid}"
                    elif "politics" == channelTypeDir[channelID]:  # 问政
                        url = f"http://api.jiaodong.net/ytnews/V13/Politics/getLiveDetail?live_id={workerid}"
                    else:  # jdnews
                        url = f"http://api.jiaodong.net/ytnews/V13/News/getNewsInfo?newsid={workerid}"
                else:
                    print(article_field)
                    continue
            articleparam = InitClass().article_params_fields(url, headers, method, article_field=article_field,
                                                             sleeptime=0)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            appname = article.get("appname")
            fields = article.get("articleField")
            channelname = fields.get('channelname')
            channelID = fields.get('channelID')
            try:
                contentJson = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                print(contentJson)
                if "海螺号" == channelname:
                    newsDetail = contentJson['data']
                    fields["appname"] = appname  # 应用名称，字符串
                    # fields["channelname"] = ""  # 频道名称，字符串
                    # fields["channelID"] = ""  # 频道id，字符串
                    # fields["channelType"] = ""  # 频道type，字符串
                    # fields["url"] = ""  # 分享的网址，字符串
                    # fields["workerid"] = ""  # 文章id，字符串
                    # fields["title"] = ""  # 文章标题，字符串
                    content = ""
                    if 'content' in newsDetail.keys() and len(newsDetail['content']):
                        content += newsDetail['content']
                    if 'content2' in newsDetail.keys() and len(newsDetail['content2']):
                        content += newsDetail['content2']
                    if 'content3' in newsDetail.keys() and len(newsDetail['content3']):
                        content += newsDetail['content3']
                    if 'content4' in newsDetail.keys() and len(newsDetail['content4']):
                        content += newsDetail['content4']
                    if 'content5' in newsDetail.keys() and len(newsDetail['content5']):
                        content += newsDetail['content5']
                    if 'content6' in newsDetail.keys() and len(newsDetail['content6']):
                        content += newsDetail['content6']
                    fields["content"] = content  # 文章内容，字符串
                    # fields["articlecovers"] = ""  # 列表封面，数组
                    fields["images"] = InitClass().get_images(fields["content"])  # 正文图片，数组
                    # fields["videos"] = ""  # 视频地址，数组
                    # fields["videocover"] = ""  # 视频封面，数组
                    # fields["width"] = ""  # 视频宽，字符串
                    # fields["height"] = ""  # 视频高，字符串
                    # fields["source"] = ""  # 文章来源，字符串
                    # fields["pubtime"] = ""  # 发布时间，时间戳（毫秒级，13位）
                    # fields["createtime"] = ""  # 创建时间，时间戳（毫秒级，13位）
                    # fields["updatetime"] = ""  # 更新时间，时间戳（毫秒级，13位）
                    # fields["likenum"] = ""  # 点赞数（喜欢数），数值
                    # fields["playnum"] = ""  # 播放数，数值
                    fields["commentnum"] = newsDetail['commentCount']  # 评论数，数值
                    # fields["readnum"] = ""  # 阅读数，数值
                    # fields["trannum"] = ""  # 转发数，数值
                    # fields["sharenum"] = ""  # 分享数，数值
                    # fields["author"] = ""  # 作者，字符串
                    # fields["banner"] = ""  # banner标记，数值（0标识不是，1标识是）
                    # fields["specialtopic"] = ""  # 是否是专题，数值（0标识不是，1标识是）
                    # fields["topicid"] = ""  # 专题id，字符串
                    if 'video' in newsDetail.keys():
                        print(newsDetail['video'])
                else:
                    if channelID in channelTypeDir.keys():
                        if "northnews" == channelTypeDir[channelID]:
                            print(contentJson)  # 未出现
                            continue
                        elif "hjnews" == channelTypeDir[channelID]:  # 微视
                            newsDetail = contentJson['data'][0]
                            fields["appname"] = appname  # 应用名称，字符串
                            # fields["channelname"] = ""  # 频道名称，字符串
                            # fields["channelID"] = ""  # 频道id，字符串
                            # fields["channelType"] = ""  # 频道type，字符串
                            # fields["url"] = ""  # 分享的网址，字符串
                            # fields["workerid"] = ""  # 文章id，字符串
                            # fields["title"] = ""  # 文章标题，字符串
                            # content = ""
                            # if 'content' in newsDetail.keys() and len(newsDetail['content']):
                            #     content += newsDetail['content']
                            # if 'content2' in newsDetail.keys() and len(newsDetail['content2']):
                            #     content += newsDetail['content2']
                            # if 'content3' in newsDetail.keys() and len(newsDetail['content3']):
                            #     content += newsDetail['content3']
                            # if 'content4' in newsDetail.keys() and len(newsDetail['content4']):
                            #     content += newsDetail['content4']
                            # if 'content5' in newsDetail.keys() and len(newsDetail['content5']):
                            #     content += newsDetail['content5']
                            # if 'content6' in newsDetail.keys() and len(newsDetail['content6']):
                            #     content += newsDetail['content6']
                            # fields["content"] = content  # 文章内容，字符串
                            # fields["articlecovers"] = ""  # 列表封面，数组
                            fields["images"] = InitClass().get_images(fields["content"])  # 正文图片，数组
                            # fields["videos"] = ""  # 视频地址，数组
                            # fields["videocover"] = ""  # 视频封面，数组
                            # fields["width"] = ""  # 视频宽，字符串
                            # fields["height"] = ""  # 视频高，字符串
                            # fields["source"] = ""  # 文章来源，字符串
                            # fields["pubtime"] = ""  # 发布时间，时间戳（毫秒级，13位）
                            # fields["createtime"] = ""  # 创建时间，时间戳（毫秒级，13位）
                            # fields["updatetime"] = ""  # 更新时间，时间戳（毫秒级，13位）
                            # fields["likenum"] = ""  # 点赞数（喜欢数），数值
                            # fields["playnum"] = ""  # 播放数，数值
                            fields["commentnum"] = newsDetail['commentCount']  # 评论数，数值
                            # fields["readnum"] = ""  # 阅读数，数值
                            # fields["trannum"] = ""  # 转发数，数值
                            # fields["sharenum"] = ""  # 分享数，数值
                            # fields["author"] = ""  # 作者，字符串
                            # fields["banner"] = ""  # banner标记，数值（0标识不是，1标识是）
                            # fields["specialtopic"] = ""  # 是否是专题，数值（0标识不是，1标识是）
                            # fields["topicid"] = ""  # 专题id，字符串
                            # if 'video' in newsDetail.keys():
                            #     print(newsDetail['video'])
                        elif "politics" == channelTypeDir[channelID]:  # 问政
                            print(contentJson)
                            newsDetail = contentJson['data']
                            fields["appname"] = appname  # 应用名称，字符串
                            # fields["channelname"] = ""  # 频道名称，字符串
                            # fields["channelID"] = ""  # 频道id，字符串
                            # fields["channelType"] = ""  # 频道type，字符串
                            # fields["url"] = ""  # 分享的网址，字符串
                            # fields["workerid"] = ""  # 文章id，字符串
                            # fields["title"] = ""  # 文章标题，字符串
                            # fields["content"] = content  # 文章内容，字符串
                            # fields["articlecovers"] = ""  # 列表封面，数组
                            fields["images"] = InitClass().get_images(fields["content"])  # 正文图片，数组
                            fields["videos"] = [newsDetail['video']]  # 视频地址，数组
                            # fields["videocover"] = ""  # 视频封面，数组
                            # fields["width"] = ""  # 视频宽，字符串
                            # fields["height"] = ""  # 视频高，字符串
                            # fields["source"] = ""  # 文章来源，字符串
                            # fields["pubtime"] = ""  # 发布时间，时间戳（毫秒级，13位）
                            # fields["createtime"] = ""  # 创建时间，时间戳（毫秒级，13位）
                            # fields["updatetime"] = ""  # 更新时间，时间戳（毫秒级，13位）
                            # fields["likenum"] = ""  # 点赞数（喜欢数），数值
                            # fields["playnum"] = ""  # 播放数，数值
                            # fields["commentnum"] = newsDetail['commentCount']  # 评论数，数值
                            # fields["readnum"] = ""  # 阅读数，数值
                            # fields["trannum"] = ""  # 转发数，数值
                            # fields["sharenum"] = ""  # 分享数，数值
                            # fields["author"] = ""  # 作者，字符串
                            # fields["banner"] = ""  # banner标记，数值（0标识不是，1标识是）
                            # fields["specialtopic"] = ""  # 是否是专题，数值（0标识不是，1标识是）
                            # fields["topicid"] = ""  # 专题id，字符串
                            # if 'video' in newsDetail.keys():
                            #     print(newsDetail['video'])
                        else:  # jdnews
                            newsDetail = contentJson['data']
                            fields["appname"] = appname  # 应用名称，字符串
                            # fields["channelname"] = ""  # 频道名称，字符串
                            # fields["channelID"] = ""  # 频道id，字符串
                            # fields["channelType"] = ""  # 频道type，字符串
                            # fields["url"] = ""  # 分享的网址，字符串
                            # fields["workerid"] = ""  # 文章id，字符串
                            # fields["title"] = ""  # 文章标题，字符串
                            content = ""
                            if 'content' in newsDetail.keys() and len(newsDetail['content']):
                                content += newsDetail['content']
                            if 'content2' in newsDetail.keys() and len(newsDetail['content2']):
                                content += newsDetail['content2']
                            if 'content3' in newsDetail.keys() and len(newsDetail['content3']):
                                content += newsDetail['content3']
                            if 'content4' in newsDetail.keys() and len(newsDetail['content4']):
                                content += newsDetail['content4']
                            if 'content5' in newsDetail.keys() and len(newsDetail['content5']):
                                content += newsDetail['content5']
                            if 'content6' in newsDetail.keys() and len(newsDetail['content6']):
                                content += newsDetail['content6']
                            fields["content"] = content  # 文章内容，字符串
                            # fields["articlecovers"] = ""  # 列表封面，数组
                            fields["images"] = InitClass().get_images(fields["content"])  # 正文图片，数组
                            # fields["videos"] = ""  # 视频地址，数组
                            # fields["videocover"] = ""  # 视频封面，数组
                            # fields["width"] = ""  # 视频宽，字符串
                            # fields["height"] = ""  # 视频高，字符串
                            # fields["source"] = ""  # 文章来源，字符串
                            # fields["pubtime"] = ""  # 发布时间，时间戳（毫秒级，13位）
                            # fields["createtime"] = ""  # 创建时间，时间戳（毫秒级，13位）
                            # fields["updatetime"] = ""  # 更新时间，时间戳（毫秒级，13位）
                            # fields["likenum"] = ""  # 点赞数（喜欢数），数值
                            # fields["playnum"] = ""  # 播放数，数值
                            fields["commentnum"] = newsDetail['commentCount']  # 评论数，数值
                            # fields["readnum"] = ""  # 阅读数，数值
                            # fields["trannum"] = ""  # 转发数，数值
                            # fields["sharenum"] = ""  # 分享数，数值
                            # fields["author"] = ""  # 作者，字符串
                            # fields["banner"] = ""  # banner标记，数值（0标识不是，1标识是）
                            # fields["specialtopic"] = ""  # 是否是专题，数值（0标识不是，1标识是）
                            # fields["topicid"] = ""  # 专题id，字符串
                            if 'video' in newsDetail.keys():
                                print(newsDetail['video'])
                            if 10000 == newsDetail['newsType']:  # 普通新闻
                                print(contentJson['data'])
                            elif 20000 == newsDetail['newsType']:  # 专题
                                print(contentJson['data'])
                                fields["content"] = newsDetail['webUrl']
                                fields["title"] = newsDetail['title']
                            elif 30000 == newsDetail['newsType']:  # 未出现
                                print(contentJson['data'])
                            elif 40000 == newsDetail['newsType']:  # 外链
                                print(contentJson['data'])
                                fields["content"] = newsDetail['webUrl']
                            elif 50000 == newsDetail['newsType']:  # 外链
                                print(contentJson['data'])
                                fields["content"] = newsDetail['webUrl']
                            elif 60000 == newsDetail['newsType']:  # 图片
                                print(contentJson['data'])
                                imgList = []
                                for imgItem in newsDetail['imgs']:
                                    imgList.append(imgItem['imgUrl'])
                                fields['images'] = imgList
                            else:  # 未出现
                                print(contentJson['data'])

                    else:
                        print(contentJson)
                        continue
                print(json.dumps(fields, indent=4, ensure_ascii=False))
            except Exception as e:
                num += 1
                logging.info(f"错误数量{num},{e}")

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
    appspider = YanTaiShiKe("烟台时刻")
    appspider.run()
