# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging

import requests

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass

bannerCountDir = {}


def setArticleListParam(channelname, channelid, articleparam, article):
    articleparam["channelid"] = channelid
    # articleparam["channelid"] = article['colID']
    articleparam["channelname"] = channelname
    articleparam["articleid"] = article['fileId']
    articleparam["articletype"] = article['articleType']
    articleparam["articletitle"] = article['title']
    if article['colID'] in bannerCountDir.keys():
        bannerCount = bannerCountDir[article['colID']]
        if bannerCount > 0:
            articleparam["banner"] = 1
            bannerCountDir[article['colID']] = bannerCount - 1
            print(bannerCountDir)
        else:
            articleparam["banner"] = 0
    else:
        articleparam["banner"] = 0

    # if len(article['imgUrls']):
    #     articleparam["imageurl"] = article['imgUrls']
    # articleparam["articleurl"] = article['shareUrl']
    # articleparam["videos"] = article['videoUrl']
    # if article['newsType'] == 2:
    #     articleparam["videocover"] = article['imgUrls'][0]
    # articleparam["pubtime"] = article['time']
    # if 'duration' in article.keys():
    #     articleparam["createtime"] = article['duration']  # 暂存视频时长
    # if 'videoSize' in article.keys():
    #     articleparam["updatetime"] = article['videoSize']  # 暂存视频大小
    # articleparam["source"] = article['infoSource']
    # articleparam["author"] = article['author']
    # articleparam["likenum"] = article['digg']
    # articleparam["commentnum"] = article['pl']
    # articleparam["readnum"] = article['title']
    # articleparam["sharenum"] = article['title']
    return articleparam


class XinHanDan(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        parentColumns = [188, 11886, 195]  # 188新闻；11886视听；195区县频道
        # 频道url
        url = "http://app.hdxw.cn:8081/app_if/getColumns"
        # 频道请求头
        headers = {
            "Host": "app.hdxw.cn:8081",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.0.1",
        }
        # 频道数据体

        # 如果携带的是json数据体,用appjson发送
        # app_json = {}
        # 频道请求方式
        method = "get"
        appParams = list()
        for temp in parentColumns:
            data = {
                "siteId": "1",
                "parentColumnId": temp,
                "version": "0",
                "columnType": "-1",
            }
            appParam = InitClass().app_params(url, headers, method, data=data)
            appParams.append(appParam)

        # app_params = InitClass().app_params(url, headers, method)
        # 如果携带json数据，用下列方式存储发送数据
        # app_params = InitClass().app_params(url, headers, method, data = data ,appjson=app_json)
        yield appParams

    @staticmethod
    def analyzechannels(channelsres):
        """
        此方法主要获取channelid,channelname即可
        若请求文章列表页需要channeltype，categoryname，categoryid,则以categoryname= categoryname形式传递参数
        :param channelsres:
        :return:
        """
        print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            channelList = json.loads(v)
            for channel in channelList['columns']:
                if 195 == channel['columnId']:  # 195区县频道
                    continue
                channelid = channel['columnId']
                channelname = channel['columnName']
                channelType = channel['columnStyle']
                topCount = channel['topCount']
                bannerCountDir[channelid] = topCount
                channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channelType)
                channelparams.append(channelparam)
        print(bannerCountDir)
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
            channeltype = channel.get("channeltype")
            topCount = channel.get("categoryid")
            url = "http://app.hdxw.cn:8081/app_if/getArticles"
            headers = {
                "Host": "app.hdxw.cn:8081",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.0.1",
            }
            method = 'get'
            # 频道数据体
            data = {
                "columnId": channelid,
                "version": "0",
                "lastFileId": "0",
                "page": "0",
                "adv": "1",
                "columnStyle": channeltype,
            }
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
                if 'list' in articlelist_json.keys() and isinstance(articlelist_json['list'], list):
                    for article in articlelist_json['list']:
                        articleparam = InitClass().article_list_fields()
                        articleparam = setArticleListParam(channelname, channelid, articleparam, article)
                        articlesparams.append(articleparam)
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

        headers = {
            "Host": "app.hdxw.cn:8081",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.0.1",
        }
        method = 'get'
        url = "http://app.hdxw.cn:8081/app_if/getArticleContent"
        data = {}
        for articleparam in articles:
            data = {
                "articleId": articleparam.get("articleid"),
                "colID": articleparam.get("articleid"),
            }
            articletitle = articleparam.get("articletitle")
            articletype = articleparam.get("articletype")
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
            # 这里url_show传的获取详情网页地址，但是会乱码，所以在下个方法再次请求详情
            article_show = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                             videourl=videos, videocover=videocover, pubtime=pubtime,
                                                             createtime=createtime, updatetime=updatetime,
                                                             source=source, author=author, likenum=articletitle,
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
            articletype = articleResponse.get("readnum")  # 没有articletype属性，使用readnum属性代替。
            articletitle = articleResponse.get("sharenum")  # articletitle，使用sharenum属性代替。
            channelid = articleResponse.get("commentnum")
            banner = articleResponse.get("banner")
            articleres = articleResponse.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname  # 应用名称，字符串
            fields["channelID"] = channelid  # 应用名称，字符串
            fields["imageurl"] = imageurl
            fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                print(articlejson)

                fields["appname"] = appname
                if 0 == articletype:  # 普通
                    print(articlejson)
                    fields["appname"] = appname  # 应用名称，字符串
                    fields["url"] = articlejson['shareUrl']  # 分享的网址，字符串
                    fields["workerid"] = articlejson['fileId']  # 文章id，字符串
                    fields["title"] = articlejson['title']  # 文章标题，字符串
                    content = articlejson['content']
                    if 'images' in articlejson.keys():
                        images = articlejson['images']
                        for item in images:
                            if 'imagearray' in item.keys():
                                for item1 in item['imagearray']:
                                    # temp = f"<img {item1['imageStyle']} src=\"{item1['imageUrl']}\" />"
                                    temp = f"<img src=\"{item1['imageUrl']}\" />"
                                    content = content.replace(item1['ref'], temp)
                            else:
                                print(item.keys())
                    fields["content"] = content  # 文章内容，字符串
                    fields["articlecovers"] = [articlejson['imageUrl']]  # # 列表封面，数组
                    # fields["images"] = articlejson['data']['pics']  # 正文图片，数组
                    # fields["videos"] = articlejson['data']['link']  # 视频地址，数组
                    # fields["videocover"] = articlejson['data']['link']  # 视频封面，数组
                    # fields["width"] = articlejson['data']['link']  # 视频宽，字符串
                    # fields["height"] = articlejson['data']['link']  # 视频高，字符串
                    fields["source"] = articlejson['source']  # 文章来源，字符串
                    fields["pubtime"] = InitClass().date_time_stamp(articlejson['publishtime'])  # 发布时间，时间戳（毫秒级，13位）
                    # fields["createtime"] = articlejson['data']['pubDate']  # 创建时间，时间戳（毫秒级，13位）
                    # fields["updatetime"] = articlejson['data']['pubDate']  # 更新时间，时间戳（毫秒级，13位）
                    # fields["likenum"] = articlejson['data']['goodpost']  # 点赞数（喜欢数），数值
                    # fields["playnum"] = articlejson['data']['link']  # 播放数，数值
                    # fields["commentnum"] = len(articlejson['data']['comments'])  # 评论数，数值
                    fields["readnum"] = articlejson['countClick']  # 阅读数，数值
                    # fields["trannum"] = articlejson['data']['link']  # 转发数，数值
                    # fields["sharenum"] = articlejson['data']['link']   # 分享数，数值
                    # fields["author"] = articlejson['data']['author']   # 作者，字符串
                elif 1 == articletype:  # 画廊
                    print(articlejson)
                    fields["appname"] = appname  # 应用名称，字符串
                    fields["url"] = articlejson['shareUrl']  # 分享的网址，字符串
                    fields["workerid"] = articlejson['fileId']  # 文章id，字符串
                    fields["title"] = articlejson['title']  # 文章标题，字符串
                    imgList = []
                    if 'images' in articlejson.keys():
                        images = articlejson['images']
                        for item in images:
                            if 'imagearray' in item.keys():
                                for item1 in item['imagearray']:
                                    imgList.append(item1['imageUrl'])
                            else:
                                print(item.keys())
                    # fields["content"] = content  # 文章内容，字符串
                    fields["articlecovers"] = [articlejson['imageUrl']]  # # 列表封面，数组
                    fields["images"] = imgList  # 正文图片，数组
                    # fields["videos"] = articlejson['data']['link']  # 视频地址，数组
                    # fields["videocover"] = articlejson['data']['link']  # 视频封面，数组
                    # fields["width"] = articlejson['data']['link']  # 视频宽，字符串
                    # fields["height"] = articlejson['data']['link']  # 视频高，字符串
                    fields["source"] = articlejson['source']  # 文章来源，字符串
                    fields["pubtime"] = InitClass().date_time_stamp(articlejson['publishtime'])  # 发布时间，时间戳（毫秒级，13位）
                    # fields["createtime"] = articlejson['data']['pubDate']  # 创建时间，时间戳（毫秒级，13位）
                    # fields["updatetime"] = articlejson['data']['pubDate']  # 更新时间，时间戳（毫秒级，13位）
                    fields["likenum"] = articlejson['countPraise']  # 点赞数（喜欢数），数值
                    # fields["playnum"] = articlejson['data']['link']  # 播放数，数值
                    # fields["commentnum"] = len(articlejson['data']['comments'])  # 评论数，数值
                    fields["readnum"] = articlejson['countClick']  # 阅读数，数值
                    # fields["trannum"] = articlejson['data']['link']  # 转发数，数值
                    fields["sharenum"] = articlejson['countShare']  # 分享数，数值
                    # fields["author"] = articlejson['data']['author']   # 作者，字符串
                elif 2 == articletype:  # 视频
                    print(articlejson)
                    fields["appname"] = appname  # 应用名称，字符串
                    fields["url"] = articlejson['shareUrl']  # 分享的网址，字符串
                    fields["workerid"] = articlejson['fileId']  # 文章id，字符串
                    fields["title"] = articlejson['title']  # 文章标题，字符串
                    # fields["content"] = articlejson['url']  # 文章内容，字符串
                    fields["articlecovers"] = [articlejson['imageUrl']]  # # 列表封面，数组
                    # fields["images"] = articlejson['data']['pics']  # 正文图片，数组
                    videoList = []
                    videoPicList = []
                    if 'videos' in articlejson.keys():
                        videos = articlejson['videos']
                        for item in videos:
                            if 'videoarray' in item.keys():
                                for item1 in item['videoarray']:
                                    # temp = f"<img {item1['imageStyle']} src=\"{item1['imageUrl']}\" />"
                                    videoList.append(item1['videoUrl'])
                                    videoPicList.append(item1['imageUrl'])
                            else:
                                print(item.keys())
                    fields["videos"] = videoList  # 视频地址，数组
                    fields["videocover"] = videoPicList  # 视频封面，数组
                    # fields["width"] = articlejson['data']['link']  # 视频宽，字符串
                    # fields["height"] = articlejson['data']['link']  # 视频高，字符串
                    fields["source"] = articlejson['source']  # 文章来源，字符串
                    fields["pubtime"] = InitClass().date_time_stamp(articlejson['publishtime'])  # 发布时间，时间戳（毫秒级，13位）
                    # fields["createtime"] = articlejson['data']['pubDate']  # 创建时间，时间戳（毫秒级，13位）
                    # fields["updatetime"] = articlejson['data']['pubDate']  # 更新时间，时间戳（毫秒级，13位）
                    fields["likenum"] = articlejson['countPraise']  # 点赞数（喜欢数），数值
                    # fields["playnum"] = articlejson['data']['link']  # 播放数，数值
                    # fields["commentnum"] = len(articlejson['data']['comments'])  # 评论数，数值
                    fields["readnum"] = articlejson['countClick']  # 阅读数，数值
                    # fields["trannum"] = articlejson['data']['link']  # 转发数，数值
                    fields["sharenum"] = articlejson['countShare']  # 分享数，数值
                    # fields["author"] = articlejson['data']['author']   # 作者，字符串
                elif 3 == articletype:  # 专题
                    print(articlejson)
                    fields["appname"] = appname  # 应用名称，字符串
                    fields["url"] = articlejson['shareUrl']  # 分享的网址，字符串
                    fields["workerid"] = articlejson['fileId']  # 文章id，字符串
                    fields["title"] = articlejson['title']  # 文章标题，字符串
                    # fields["content"] = articlejson['url']  # 文章内容，字符串
                    fields["articlecovers"] = [articlejson['picBig']]  # # 列表封面，数组
                    # fields["images"] = articlejson['data']['pics']  # 正文图片，数组
                    # fields["videos"] = articlejson['data']['link']  # 视频地址，数组
                    # fields["videocover"] = articlejson['data']['link']  # 视频封面，数组
                    # fields["width"] = articlejson['data']['link']  # 视频宽，字符串
                    # fields["height"] = articlejson['data']['link']  # 视频高，字符串
                    fields["source"] = articlejson['source']  # 文章来源，字符串
                    fields["pubtime"] = InitClass().date_time_stamp(articlejson['publishtime'])  # 发布时间，时间戳（毫秒级，13位）
                    # fields["createtime"] = articlejson['data']['pubDate']  # 创建时间，时间戳（毫秒级，13位）
                    # fields["updatetime"] = articlejson['data']['pubDate']  # 更新时间，时间戳（毫秒级，13位）
                    fields["likenum"] = articlejson['countPraise']  # 点赞数（喜欢数），数值
                    # fields["playnum"] = articlejson['data']['link']  # 播放数，数值
                    # fields["commentnum"] = len(articlejson['data']['comments'])  # 评论数，数值
                    fields["readnum"] = articlejson['countClick']  # 阅读数，数值
                    # fields["trannum"] = articlejson['data']['link']  # 转发数，数值
                    fields["sharenum"] = articlejson['countShare']  # 分享数，数值
                    # fields["author"] = articlejson['data']['author']   # 作者，字符串
                elif 4 == articletype:  # 网址
                    print(articlejson)
                    fields["appname"] = appname  # 应用名称，字符串
                    fields["url"] = articlejson['shareUrl']  # 分享的网址，字符串
                    fields["workerid"] = articlejson['fileId']  # 文章id，字符串
                    fields["title"] = articlejson['title']  # 文章标题，字符串
                    fields["content"] = articlejson['url']  # 文章内容，字符串
                    fields["articlecovers"] = [articlejson['picBig']]  # # 列表封面，数组
                    # fields["images"] = articlejson['data']['pics']  # 正文图片，数组
                    # fields["videos"] = articlejson['data']['link']  # 视频地址，数组
                    # fields["videocover"] = articlejson['data']['link']  # 视频封面，数组
                    # fields["width"] = articlejson['data']['link']  # 视频宽，字符串
                    # fields["height"] = articlejson['data']['link']  # 视频高，字符串
                    fields["source"] = articlejson['source']  # 文章来源，字符串
                    fields["pubtime"] = InitClass().date_time_stamp(articlejson['publishtime'])  # 发布时间，时间戳（毫秒级，13位）
                    # fields["createtime"] = articlejson['data']['pubDate']  # 创建时间，时间戳（毫秒级，13位）
                    # fields["updatetime"] = articlejson['data']['pubDate']  # 更新时间，时间戳（毫秒级，13位）
                    fields["likenum"] = articlejson['countPraise']  # 点赞数（喜欢数），数值
                    # fields["playnum"] = articlejson['data']['link']  # 播放数，数值
                    # fields["commentnum"] = len(articlejson['data']['comments'])  # 评论数，数值
                    fields["readnum"] = articlejson['countClick']  # 阅读数，数值
                    # fields["trannum"] = articlejson['data']['link']  # 转发数，数值
                    fields["sharenum"] = articlejson['countShare']  # 分享数，数值
                    # fields["author"] = articlejson['data']['author']   # 作者，字符串
                else:
                    print(articlejson)

                print(json.dumps(fields, indent=4, ensure_ascii=False))
            except Exception as e:
                print(e)

    def run(self):
        appParamsList = self.get_app_params().__next__()
        channelsres = {}
        for appParams in appParamsList:
            name = appParams['appdata']['parentColumnId']
            value = self.getchannels(appParams).__next__()
            channelsres[name] = value
        channelsparams = self.analyzechannels(channelsres)
        articleparams = self.getarticlelistsparams(channelsparams.__next__())
        articles_ress = self.getarticlelists(articleparams.__next__())
        articles = self.analyze_articlelists(articles_ress.__next__())
        articlesparam = self.getarticleparams(articles.__next__())
        articles_html = self.getarticlehtml(articlesparam.__next__())
        self.analyzearticles(articles_html.__next__())


if __name__ == '__main__':
    spider = XinHanDan('新邯郸')
    spider.run()
