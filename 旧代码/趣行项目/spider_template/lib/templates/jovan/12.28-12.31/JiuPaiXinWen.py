# -*- encoding:utf-8 -*-
"""
@功能:湖北日报解析模板
@AUTHOR：jovan
@文件名：HuBeiRiBao.py
@时间：2020年12月22日 15:58:24
"""

import json
import logging
import random
import time

import requests

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


def setListNewsParam(channelname, channelid, banner, item):
    try:
        article_fields = InitClass().article_fields()
        article_fields["channelname"] = channelname  # 频道名称，字符串
        article_fields["channelID"] = channelid  # 频道id，字符串
        # article_fields["channelType"] = channel_type  # 频道type，字符串
        # article_fields["url"] = item['jsonUrl']  # 分享的网址，字符串
        if 'ctId' in item.keys():
            article_fields["workerid"] = item['ctId']  # 文章id，字符串
        elif 'infoId' in item.keys():
            article_fields["workerid"] = item['infoId']  # 文章id，字符串
        elif 'id' in item.keys():
            article_fields["workerid"] = item['id']  # 文章id，字符串
        else:
            print(item)
        if 'ctTitle' in item.keys():
            article_fields["title"] = item['ctTitle']  # 文章标题，字符串
        elif 'title' in item.keys():
            article_fields["title"] = item['title']  # 文章标题，字符串
        elif 'infoTitle' in item.keys():
            article_fields["title"] = item['infoTitle']  # 文章标题，字符串
        else:
            print(item)

        # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
        imgList = []
        if 'ctImgUrl' in item.keys():
            if "|" in item['ctImgUrl']:
                imgList = item['ctImgUrl'].split('|')
                if len(imgList) and not imgList[1]:
                    imgList.pop()
            else:
                if not item['ctImgUrl']:
                    imgList.append(item['ctImgUrl'])
        elif 'thumb' in item.keys():
            imgList.append(item['thumb'])
        elif 'infoImgUrl' in item.keys():
            imgList = item['infoImgUrl']
        else:
            print(item)

        article_fields["articlecovers"] = imgList  # 列表封面，数组
        # article_fields["images"] = ''  # 正文图片，数组
        if 'videoUrl' in item.keys():
            article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
        if 'coverUrl' in item.keys():
            article_fields["videocover"] = [item['coverUrl']]  # 视频封面，数组
        # article_fields["width"] = ''  # 视频宽，字符串
        # article_fields["height"] = ''  # 视频高，字符串
        # article_fields["source"] = ''  # 文章来源，字符串
        # article_fields["pubtime"] = ''  # 发布时间，时间戳（毫秒级，13位）
        # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
        # article_fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
        # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
        # article_fields["playnum"] = ''  # 播放数，数值
        # article_fields["commentnum"] = item['commentNum']  # 评论数，数值
        # article_fields["readnum"] = item['realRead']  # 阅读数，数值
        # article_fields["trannum"] = ''  # 转发数，数值
        # article_fields["sharenum"] = ''  # 分享数，数值
        # article_fields["author"] = ''  # 作者，字符串
        article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
        # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
        # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
        # article_fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
        if 'ctInfoType' in item.keys():
            article_fields["infoType"] = item['ctInfoType']  # 自己添加新闻类型
        elif 'infoType' in item.keys():
            article_fields["infoType"] = item['infoType']  # 自己添加新闻类型
        else:
            print(item)
            article_fields["infoType"] = ""  # 自己添加新闻类型
        if 'ctType' in item.keys():
            article_fields["newsType"] = item['ctType']  # 自己添加新闻类型
        else:
            print(item)
            article_fields["newsType"] = ""  # 自己添加新闻类型
    except Exception as e:
        print(e)
    return article_fields


class JiuPaiXinWen(Appspider):

    @staticmethod
    def get_app_params():
        url1 = "http://app.jiupaicn.com/indexapp.php?version=335&m=content&c=wap&a=cate_list"
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36",
            "Connection": "Keep-Alive",
            "Charset": "UTF-8",
            "Accept-Encoding": "gzip",
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "appjph.jiupaicn.com",
            "Content-Length": "0",
        }
        method = "get"

        app_params1 = InitClass().app_params(url1, headers, method)

        yield [app_params1]

    def analyze_channel(self, channelsres):
        print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            if "http://app.jiupaicn.com/indexapp.php?version=335&m=content&c=wap&a=cate_list" == k:
                channelList = json.loads(v)
                for channel in channelList['top_menu']:
                    channelid = channel['cateId']
                    channelname = channel['cateName']
                    channelType = channel['type']
                    channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channelType)
                    channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = ""
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36",
            "Connection": "Keep-Alive",
            "Charset": "UTF-8",
            "Accept-Encoding": "gzip",
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "appjph.jiupaicn.com",
            "Content-Length": "0",
        }
        method = "post"

        urlTJ = "http://appjph.jiupaicn.com/v3/rescommend/defaultList"
        dataTJ = f'deviceId=2d4a3a2d194098fa'
        articlelist_paramTJ = InitClass().articlelists_params_fields(urlTJ, headers, method, "推荐", data=dataTJ)
        articlelistsparams.append(articlelist_paramTJ)

        urlTJBanner = "http://appjph.jiupaicn.com/app/content/rescommend/rollList"
        articlelist_paramTJBanner = InitClass().articlelists_params_fields(urlTJBanner, headers, method, "推荐Banner",
                                                                           banners=1)
        articlelistsparams.append(articlelist_paramTJBanner)

        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channelType = channel.get("channeltype")
            if 'both' == channelType:
                url = "http://appjph.jiupaicn.com/jphnews/column/list"
                data = f'lastId=&threePicsLastId=&columnId={channelid}'
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                           channelid=channelid, channeltype=channelType)
                articlelistsparams.append(articlelist_param)
            elif 'jph_concern' == channelType:  # 九派号
                url = "http://appjph.jiupaicn.com/app/member/hot/list"
                data = f'page=1&pageSize=5'
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                           channelid=channelid, channeltype=channelType)
                articlelistsparams.append(articlelist_param)
            elif 'jph' == channelType:  # 旅行
                url = "http://appjph.jiupaicn.com/v3/column/new/list"
                data = f'leftLastId=&pageRowLength=20&columnId={channelid}&smallLastId='
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                           channelid=channelid, channeltype=channelType)
                articlelistsparams.append(articlelist_param)
            else:
                print(channel)
        urlJH = "http://appjph.jiupaicn.com/v3/column/new/list"
        dataJH = f'leftLastId=&pageRowLength=20&columnId=dbe8ab53fa52403f9bca4b920136b7a7&smallLastId='
        articlelist_paramJH = InitClass().articlelists_params_fields(urlJH, headers, method, "江湖绘", data=dataJH,
                                                                     channelid='dbe8ab53fa52403f9bca4b920136b7a7',
                                                                     channeltype='jph')
        articlelistsparams.append(articlelist_paramJH)

        urlSP = "http://appjph.jiupaicn.com/app/content/picOrvideo/list"
        dataSP = f'type=2&page=1&pageSize=10'
        articlelist_paramSP = InitClass().articlelists_params_fields(urlSP, headers, method, '视频', data=dataSP)
        articlelistsparams.append(articlelist_paramSP)

        yield articlelistsparams

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            banners = articleslistres.get("banners")
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    print(articleslists)
                    if 'resultData' in articleslists.keys():
                        if isinstance(articleslists['resultData'], list):
                            for item in articleslists['resultData']:
                                article_fields = setListNewsParam(channelname, channelid, banners, item)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        elif isinstance(articleslists['resultData'], dict):
                            for k, v in articleslists['resultData'].items():
                                if isinstance(v, list):
                                    for item in v:
                                        article_fields = setListNewsParam(channelname, channelid, banners, item)
                                        articleparam = InitClass().article_list_fields()
                                        articleparam["articelField"] = article_fields
                                        articlesparams.append(articleparam)
                                else:
                                    print(k, v)
                        else:
                            print(articleslists['resultData'])
                    elif 'txtCont' in articleslists.keys():
                        if isinstance(articleslists['txtCont'], list):
                            for item in articleslists['txtCont']:
                                article_fields = setListNewsParam(channelname, channelid, banners, item)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        else:
                            print(articleslists['txtCont'])
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
            infoType = article_field.get('infoType')
            newsType = article_field.get('newsType')
            url = ""
            headers = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36",
                "Connection": "Keep-Alive",
                "Charset": "UTF-8",
                "Accept-Encoding": "gzip",
                "Accept": "*/*",
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "appjph.jiupaicn.com",
                "Content-Length": "0",
            }
            method = "post"
            if '1' == infoType:  # 跳转到九派新闻详情
                url = f"http://app.jiupaicn.com/indexapp.php?version=335&m=content&c=wap&a=contents&json[secCode]=&json[channelId]=&json[columnId]={article_field['channelID']}&json[infoId]={article_field['workerid']}&json[deviceId]=2d4a3a2d194098fa&json[userId]=undefined"
                articleparam = InitClass().article_params_fields(url, headers, "get", article_field=article_field)
                articleparams.append(articleparam)
            elif '2' == infoType:  # 跳转到栏目
                print('未识别栏目', article_field.get('channelname'), article_field.get('title'))
            elif '3' == infoType:  # 跳转到专题
                url = f"http://app.jiupaicn.com/indexapp.php?version=335&m=content&c=wap&a=zhuanti&json[specialId]={article_field['workerid']}&rdnum={random.random()}"
                articleparam = InitClass().article_params_fields(url, headers, "get", article_field=article_field)
                articleparams.append(articleparam)
            elif '4' == infoType:  # 跳转广告
                print('未识别广告', article_field.get('channelname'), article_field.get('title'))
            elif "5" == infoType or "" == infoType:  # 跳转到九派号
                if '3' == newsType:
                    print('未识别九派号图集', article_field.get('channelname'), article_field.get('title'))
                else:
                    url = "http://appjph.jiupaicn.com/v3/detail"
                    data = f"id={article_field['workerid']}&deviceId=2d4a3a2d194098fa"
                    articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                                     article_field=article_field)
                    articleparams.append(articleparam)
            elif '10' == infoType:  # H5链接
                print('未识别H5链接', article_field.get('channelname'), article_field.get('title'))
            else:
                print('未识别类型', infoType, article_field.get('channelname'), article_field.get('title'))

        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            appname = article.get("appname")
            fields = article.get("articleField")
            try:
                contentJson = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                print(contentJson)
                infoType = fields.get('infoType')
                newsType = fields.get('newsType')
                if '1' == infoType:  # 跳转到九派新闻详情
                    fields["appname"] = appname  # 应用名称，字符串
                    # fields["channelname"] = channelname  # 频道名称，字符串
                    # fields["channelID"] = channelid  # 频道id，字符串
                    # fields["channelType"] = channel_type  # 频道type，字符串
                    # fields["url"] = contentJson['infoCont']  # 分享的网址，字符串
                    # fields["workerid"] = item['ctId']  # 文章id，字符串
                    # fields["title"] = item['title']  # 文章标题，字符串
                    fields["content"] = contentJson['infoCont']  # 文章内容，字符串
                    imgList = []
                    if 'infoImgUrl' in contentJson.keys():
                        if "|" in contentJson['infoImgUrl']:
                            imgList = contentJson['infoImgUrl'].split('|')
                            if len(imgList) and not imgList[1]:
                                imgList.pop()
                        else:
                            if not contentJson['infoImgUrl']:
                                imgList.append(contentJson['infoImgUrl'])
                    fields["articlecovers"] = imgList  # 列表封面，数组
                    # fields["images"] = ''  # 正文图片，数组
                    # fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                    # fields["videocover"] = [item['videoImg']]  # 视频封面，数组
                    # fields["width"] = ''  # 视频宽，字符串
                    # fields["height"] = ''  # 视频高，字符串
                    # fields["source"] = ''  # 文章来源，字符串
                    fields["pubtime"] = InitClass.date_time_stamp(contentJson['pubDate'])  # 发布时间，时间戳（毫秒级，13位）
                    # fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                    # fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                    # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                    # fields["playnum"] = ''  # 播放数，数值
                    # fields["commentnum"] = item['commentNum']  # 评论数，数值
                    # fields["readnum"] = item['realRead']  # 阅读数，数值
                    # fields["trannum"] = ''  # 转发数，数值
                    # fields["sharenum"] = ''  # 分享数，数值
                    fields["author"] = contentJson['pubAuthor']  # 作者，字符串
                    # fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                    # fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                    # fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                    # fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
                elif '2' == infoType:  # 跳转到栏目
                    print('未识别栏目', contentJson)
                elif '3' == infoType:  # 跳转到专题
                    topicFields = InitClass().topic_fields()
                    topicFields["topicID"] = fields['workerid']  # 专题id，app内唯一标识
                    topicFields["platformName"] = appname  # 平台名字（app名字）
                    # topicFields["platformID"] = fields['workerid']
                    topicFields["channelName"] = fields['channelname']  # 频道名字
                    topicFields["channelID"] = fields['channelID']  # 频道id
                    # topicFields["topicUrl"] = fields['workerid']  # topicUrl
                    # topicFields["title"] = fields['workerid']
                    topicFields["digest"] = contentJson['description']  # 简介，摘要
                    topicFields["topicCover"] = [contentJson['topicImgUrl']]
                    # topicFields["pubTime"] = fields['workerid']  # 时间戳
                    # topicFields["articleNum"] = fields['workerid']  # 专题内的文章数量
                    # topicFields["newestArticleID"] = fields['workerid']  # 最新发布的文章id
                    # topicFields["articlesNumPerHour"] = fields['workerid']
                    # topicFields["original"] = fields['workerid']
                    # topicFields["firstMedia"] = fields['workerid']
                    # topicFields["transPower"] = fields['workerid']
                    # topicFields["hotDegree"] = fields['workerid']
                    # topicFields["wordsFreq"] = fields['workerid']
                    # topicFields["hotDegreeTrend"] = fields['workerid']
                    # topicFields["emotionTrend"] = fields['workerid']
                    # topicFields["region"] = fields['workerid']
                    # topicFields["spreadPath"] = fields['workerid']
                    # topicFields["createTime"] = fields['workerid']
                    # topicFields["updateTime"] = fields['workerid']
                    topicItem = []
                    for topicCate in contentJson['topicCate']:
                        topicItem += topicCate['infoList']
                    topicArticles = self.getTopicArticles(fields['channelname'], fields['channelID'], fields['title'],
                                                          fields['workerid'], topicItem)
                    articleparams = self.getarticleparams(topicArticles.__next__())
                    articlesres = self.getarticlehtml(articleparams.__next__())
                    self.analyzearticle(articlesres.__next__())
                elif '4' == infoType:  # 跳转广告
                    print('未识别广告', contentJson)
                elif "5" == infoType or "" == infoType:  # 跳转到九派号
                    if '3' == newsType:
                        print('未识别九派号图集', contentJson)
                    else:
                        fields["appname"] = appname  # 应用名称，字符串
                        # fields["channelname"] = channelname  # 频道名称，字符串
                        # fields["channelID"] = channelid  # 频道id，字符串
                        # fields["channelType"] = channel_type  # 频道type，字符串
                        # fields["url"] = item['jsonUrl']  # 分享的网址，字符串
                        # fields["workerid"] = item['ctId']  # 文章id，字符串
                        # fields["title"] = item['title']  # 文章标题，字符串
                        fields["content"] = contentJson['resultData']['content']  # 文章内容，字符串
                        # fields["articlecovers"] = imgList  # 列表封面，数组
                        fields["images"] = InitClass.get_images(fields["content"])  # 正文图片，数组
                        # fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                        # fields["videocover"] = [item['videoImg']]  # 视频封面，数组
                        # fields["width"] = ''  # 视频宽，字符串
                        # fields["height"] = ''  # 视频高，字符串
                        # fields["source"] = ''  # 文章来源，字符串
                        # fields["pubtime"] = ''  # 发布时间，时间戳（毫秒级，13位）
                        fields["createtime"] = contentJson['resultData']['createDate']  # 创建时间，时间戳（毫秒级，13位）
                        fields["updatetime"] = contentJson['resultData']['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                        # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                        # fields["playnum"] = ''  # 播放数，数值
                        # fields["commentnum"] = item['commentNum']  # 评论数，数值
                        fields["readnum"] = contentJson['resultData']['read']  # 阅读数，数值
                        # fields["trannum"] = ''  # 转发数，数值
                        # fields["sharenum"] = ''  # 分享数，数值
                        # fields["author"] = ''  # 作者，字符串
                        # fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                        # fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                        # fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                        # fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
                elif '10' == infoType:  # H5链接
                    print('未识别H5链接', contentJson)
                else:
                    print('未识别类型', contentJson)
                print(json.dumps(fields, indent=4, ensure_ascii=False))
            except Exception as e:
                num += 1
                logging.info(f"错误数量{num},{e}")

    def getTopicArticles(self, channelname, channelid, topicTitle, topicId, topicNewsList):
        articlesparams = []
        for item in topicNewsList:
            try:
                article_fields = InitClass().article_fields()
                article_fields["channelname"] = channelname  # 频道名称，字符串
                article_fields["channelID"] = channelid  # 频道id，字符串
                # article_fields["channelType"] = channel_type  # 频道type，字符串
                # article_fields["url"] = item['jsonUrl']  # 分享的网址，字符串
                if 'infoUrl' in item.keys():
                    article_fields["workerid"] = item['infoUrl']  # 文章id，字符串
                else:
                    print(item)
                if 'infoTitle' in item.keys():
                    article_fields["title"] = item['infoTitle']  # 文章标题，字符串
                else:
                    print(item)

                # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
                imgList = []
                if 'ctImgUrl' in item.keys():
                    if "|" in item['ctImgUrl']:
                        imgList = item['ctImgUrl'].split('|')
                        if len(imgList) and not imgList[1]:
                            imgList.pop()
                    else:
                        if not item['ctImgUrl']:
                            imgList.append(item['ctImgUrl'])
                elif 'thumb' in item.keys():
                    imgList.append(item['thumb'])
                elif 'infoImgUrl' in item.keys():
                    imgList = item['infoImgUrl']
                else:
                    print(item)

                article_fields["articlecovers"] = imgList  # 列表封面，数组
                # article_fields["images"] = ''  # 正文图片，数组
                if 'videoUrl' in item.keys():
                    article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                if 'coverUrl' in item.keys():
                    article_fields["videocover"] = [item['coverUrl']]  # 视频封面，数组
                # article_fields["width"] = ''  # 视频宽，字符串
                # article_fields["height"] = ''  # 视频高，字符串
                # article_fields["source"] = ''  # 文章来源，字符串
                # article_fields["pubtime"] = ''  # 发布时间，时间戳（毫秒级，13位）
                # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                # article_fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                # article_fields["playnum"] = ''  # 播放数，数值
                # article_fields["commentnum"] = item['commentNum']  # 评论数，数值
                # article_fields["readnum"] = item['realRead']  # 阅读数，数值
                # article_fields["trannum"] = ''  # 转发数，数值
                # article_fields["sharenum"] = ''  # 分享数，数值
                # article_fields["author"] = ''  # 作者，字符串
                # article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                article_fields["specialtopic"] = 1  # 是否是专题，数值（0标识不是，1标识是）
                article_fields["topicid"] = topicId  # 专题id，字符串
                article_fields["topicTitle"] = topicTitle  # 专题标题，字符串
                if 'infoType' in item.keys():
                    infoType = item['infoType']
                    if 'news' == infoType:
                        article_fields["infoType"] = "1"  # 自己添加新闻类型
                        article_fields["newsType"] = ""
                    elif 'jph' == infoType:
                        article_fields["infoType"] = "5"  # 自己添加新闻类型
                        article_fields["newsType"] = "1"
                    elif 'jphPic' == infoType:
                        article_fields["infoType"] = "5"  # 自己添加新闻类型
                        article_fields["newsType"] = "3"
                    elif 'topic' == infoType:
                        pass
                    elif 'redTopic' == infoType:
                        pass
                    elif 'activity' == infoType:
                        pass
                    elif 'htmlFive' == infoType:
                        pass
                    elif 'redTopic' == infoType:
                        pass
                    elif 'video' == infoType:
                        article_fields["infoType"] = "5"  # 自己添加新闻类型
                        article_fields["newsType"] = "2"
                    else:
                        article_fields["infoType"] = "1"  # 自己添加新闻类型
                        article_fields["newsType"] = ""
                else:
                    article_fields["infoType"] = "1"  # 自己添加新闻类型
                    article_fields["newsType"] = ""
                articleparam = InitClass().article_list_fields()
                articleparam["articelField"] = article_fields
                articlesparams.append(articleparam)
            except Exception as e:
                print(e)

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
    appspider = JiuPaiXinWen("九派新闻")
    appspider.run()
