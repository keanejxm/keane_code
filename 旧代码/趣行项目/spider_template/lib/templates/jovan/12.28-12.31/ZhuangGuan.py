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
        article_fields["url"] = item['sharelink']  # 分享的网址，字符串
        article_fields["workerid"] = item['itemId']  # 文章id，字符串
        article_fields["title"] = item['title']  # 文章标题，字符串
        # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
        imgList = []
        if 'newPicsList' in item.keys() and item['newPicsList'] is not None:
            for img in item['newPicsList']:
                if 'imgurl' in img.keys() and img['imgurl']:
                    imgList.append(img['imgurl'])
        article_fields["articlecovers"] = imgList  # 列表封面，数组
        # article_fields["images"] = ''  # 正文图片，数组
        if 'videoUrl' in item.keys() and item['videoUrl']:
            article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
        # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
        # article_fields["width"] = ''  # 视频宽，字符串
        # article_fields["height"] = ''  # 视频高，字符串
        # article_fields["source"] = ''  # 文章来源，字符串
        article_fields["pubtime"] = item['timeStamp']  # 发布时间，时间戳（毫秒级，13位）
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
        article_fields["newsType"] = item['type']  # 自己添加新闻类型
    except Exception as e:
        print(e)
    return article_fields


class ZhuangGuan(Appspider):

    @staticmethod
    def get_app_params():
        url1 = "https://zgapp.gxnews.com.cn/cate/list"
        headers = {
            "Accept": "application/json",
            "appVer": "230",
            "User-Agent": "Android Client",
            "deviceVer": "29",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "zgapp.gxnews.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        method = "get"

        app_params1 = InitClass().app_params(url1, headers, method)

        yield [app_params1]

    def analyze_channel(self, channelsres):
        print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            if "https://zgapp.gxnews.com.cn/cate/list" == k:
                channelList = json.loads(v)
                temp = channelList['cates'] + channelList['videoCates']
                for channel in temp:
                    channelid = channel['id']
                    channelname = channel['cateName']
                    if 'webUrl' in channel and channel['webUrl']:
                        continue
                    channelparam = InitClass().channel_fields(channelid, channelname)
                    channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        headers = {
            "Accept": "application/json",
            "appVer": "230",
            "User-Agent": "Android Client",
            "deviceVer": "29",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "zgapp.gxnews.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        method = "get"
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            if 1 == channelid:  # 推荐
                url = f"https://zgapp.gxnews.com.cn/news/initList?limit=1&page=1&cateId={channelid}"
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           channelid=channelid, channeltype="qxtuijian")
                articlelistsparams.append(articlelist_param)
            if 36 == channelid:  # 热点
                url = f"https://zgapp.gxnews.com.cn/news/videoIndex/init"
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           channelid=channelid, channeltype="qxredian")
                articlelistsparams.append(articlelist_param)

                channelRes = requests.get(url, headers=headers).content.decode()
                channelList = json.loads(channelRes)
                for item_opt in channelList['data']['options']:
                    channelid = item_opt['cateId']
                    channelname = item_opt['cateName']
                    url = f"https://zgapp.gxnews.com.cn/news/newsList?limit=15&cateId={channelid}&page=1"
                    articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                               channelid=channelid, channeltype="")
                    articlelistsparams.append(articlelist_param)

            else:
                url = f"https://zgapp.gxnews.com.cn/news/newsList?limit=15&cateId={channelid}&page=1"
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           channelid=channelid, channeltype="")
                articlelistsparams.append(articlelist_param)
        yield articlelistsparams

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            channeltype = articleslistres.get("channelType")
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    print(articleslists)
                    if "qxtuijian" == channeltype:
                        for item_hongdou in articleslists['data']['hongdouList']:
                            article_fields = setListNewsParam(channelname, channelid, 0, item_hongdou)
                            articleparam = InitClass().article_list_fields()
                            articleparam["articelField"] = article_fields
                            articlesparams.append(articleparam)
                        for item_jc in articleslists['data']['jcList']:
                            article_fields = setListNewsParam(channelname, channelid, 0, item_jc)
                            articleparam = InitClass().article_list_fields()
                            articleparam["articelField"] = article_fields
                            articlesparams.append(articleparam)
                        for item_top in articleslists['data']['topList']:
                            article_fields = setListNewsParam(channelname, channelid, 0, item_top)
                            articleparam = InitClass().article_list_fields()
                            articleparam["articelField"] = article_fields
                            articlesparams.append(articleparam)
                        for item_video in articleslists['data']['videoList']:
                            article_fields = setListNewsParam(channelname, channelid, 0, item_video)
                            articleparam = InitClass().article_list_fields()
                            articleparam["articelField"] = article_fields
                            articlesparams.append(articleparam)
                        for item_view in articleslists['data']['viewList']:
                            article_fields = setListNewsParam(channelname, channelid, 0, item_view)
                            articleparam = InitClass().article_list_fields()
                            articleparam["articelField"] = article_fields
                            articlesparams.append(articleparam)
                        for item_yw in articleslists['data']['ywList']:
                            article_fields = setListNewsParam(channelname, channelid, 0, item_yw)
                            articleparam = InitClass().article_list_fields()
                            articleparam["articelField"] = article_fields
                            articlesparams.append(articleparam)
                    elif "qxredian" == channeltype:
                        for item_run in articleslists['data']['runNews']:
                            article_fields = setListNewsParam(channelname, channelid, 1, item_run)
                            articleparam = InitClass().article_list_fields()
                            articleparam["articelField"] = article_fields
                            articlesparams.append(articleparam)
                        for item_vtop in articleslists['data']['videoTops']:
                            article_fields = setListNewsParam(channelname, channelid, 0, item_vtop)
                            articleparam = InitClass().article_list_fields()
                            articleparam["articelField"] = article_fields
                            articlesparams.append(articleparam)
                    else:
                        for item_def in articleslists['data']:
                            article_fields = setListNewsParam(channelname, channelid, 0, item_def)
                            articleparam = InitClass().article_list_fields()
                            articleparam["articelField"] = article_fields
                            articlesparams.append(articleparam)
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        headers = {}
        method = "get"
        for article in articles:
            article_field = article.get('articelField')
            newsType = article_field.get('newsType')
            if "thread" == newsType:
                url = f"https://hd3g.gxnews.com.cn/api/index.php?model=viewthread&filter=yes&limit=15&ac=index&page=1&t={article_field.get('workerid')}"
                articleparam = InitClass().article_params_fields(url, headers, method, article_field=article_field)
                articleparams.append(articleparam)
            elif "tv" == newsType:
                url = f"https://v.gxnews.com.cn/?c=json&a=articlecontent&articleid={article_field.get('workerid')}"
                articleparam = InitClass().article_params_fields(url, headers, method, article_field=article_field)
                articleparams.append(articleparam)
            elif "web" == newsType:
                pass  # 详情是网址
            elif "webtopic" == newsType:
                pass  # 详情是网址
            elif "video" == newsType:
                pass  # 没有详情的地址
            elif "news" == newsType:
                url = f"https://v.gxnews.com.cn/?c=json&a=articlecontent&articleid={article_field.get('workerid')}"
                articleparam = InitClass().article_params_fields(url, headers, method, article_field=article_field)
                articleparams.append(articleparam)
            elif "tblive" == newsType:
                pass  # 详情是网址
            else:
                print(article_field)
        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            appname = article.get("appname")
            fields = article.get("articleField")
            newsType = fields.get("newsType")
            try:
                if article.get("articleres"):
                    if article.get("articleres").startswith(u'\ufeff'):
                        contentJson = json.loads(json.dumps(
                            json.loads(article.get("articleres").encode('utf8')[3:].decode('utf8'), strict=False),
                            indent=4, ensure_ascii=False))
                    else:
                        contentJson = json.loads(
                            json.dumps(json.loads(article.get("articleres"), strict=False), indent=4,
                                       ensure_ascii=False))
                    print(contentJson)
                    if "thread" == newsType:
                        fields["appname"] = appname  # 应用名称，字符串
                        # fields["channelname"] = channelname  # 频道名称，字符串
                        # fields["channelID"] = channelid  # 频道id，字符串
                        # fields["channelType"] = channel_type  # 频道type，字符串
                        # fields["url"] = contentJson['source_url']  # 分享的网址，字符串
                        # fields["workerid"] = item['ctId']  # 文章id，字符串
                        # fields["title"] = item['title']  # 文章标题，字符串
                        content = ""
                        if len(contentJson['results']['posts']):
                            content = contentJson['results']['posts'][0]['pagetext']
                            for img in contentJson['results']['posts'][0]['image_array']:
                                content = content.replace(img['replace_str'], img['picurl'])
                        fields["content"] = content  # 文章内容，字符串
                        # fields["articlecovers"] = imgList  # 列表封面，数组
                        fields["images"] = InitClass.get_images(fields["content"])  # 正文图片，数组
                        # fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                        # fields["videocover"] = [item['videoImg']]  # 视频封面，数组
                        # fields["width"] = ''  # 视频宽，字符串
                        # fields["height"] = ''  # 视频高，字符串
                        # fields["source"] = contentJson['source']  # 文章来源，字符串
                        # fields["pubtime"] = contentJson['ptime']  # 发布时间，时间戳（毫秒级，13位）
                        # fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                        # fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                        # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                        # fields["playnum"] = ''  # 播放数，数值
                        # fields["commentnum"] = item['commentNum']  # 评论数，数值
                        # fields["readnum"] = contentJson['views']  # 阅读数，数值
                        # fields["trannum"] = ''  # 转发数，数值
                        # fields["sharenum"] = ''  # 分享数，数值
                        # fields["author"] = contentJson['username']  # 作者，字符串
                        # fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                        # fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                        # fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                        # fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
                    elif "tv" == newsType:
                        fields["appname"] = appname  # 应用名称，字符串
                        # fields["channelname"] = channelname  # 频道名称，字符串
                        # fields["channelID"] = channelid  # 频道id，字符串
                        # fields["channelType"] = channel_type  # 频道type，字符串
                        # fields["url"] = contentJson['source_url']  # 分享的网址，字符串
                        # fields["workerid"] = item['ctId']  # 文章id，字符串
                        # fields["title"] = item['title']  # 文章标题，字符串
                        fields["content"] = contentJson['articleinfo']['content']  # 文章内容，字符串
                        # fields["articlecovers"] = imgList  # 列表封面，数组
                        fields["images"] = InitClass.get_images(fields["content"])  # 正文图片，数组
                        # fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                        # fields["videocover"] = [item['videoImg']]  # 视频封面，数组
                        # fields["width"] = ''  # 视频宽，字符串
                        # fields["height"] = ''  # 视频高，字符串
                        fields["source"] = contentJson['articleinfo']['source']  # 文章来源，字符串
                        # fields["pubtime"] = contentJson['ptime']  # 发布时间，时间戳（毫秒级，13位）
                        # fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                        # fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                        # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                        # fields["playnum"] = ''  # 播放数，数值
                        # fields["commentnum"] = item['commentNum']  # 评论数，数值
                        # fields["readnum"] = contentJson['views']  # 阅读数，数值
                        # fields["trannum"] = ''  # 转发数，数值
                        # fields["sharenum"] = ''  # 分享数，数值
                        # fields["author"] = contentJson['username']  # 作者，字符串
                        # fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                        # fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                        # fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                        # fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
                        if len(contentJson['articleinfo']['pics_info']):
                            print(contentJson['articleinfo']['pics_info'])
                    elif "web" == newsType:
                        pass  # 详情是网址
                    elif "webtopic" == newsType:
                        pass  # 详情是网址
                    elif "video" == newsType:
                        pass  # 没有详情的地址
                    elif "news" == newsType:
                        fields["appname"] = appname  # 应用名称，字符串
                        # fields["channelname"] = channelname  # 频道名称，字符串
                        # fields["channelID"] = channelid  # 频道id，字符串
                        # fields["channelType"] = channel_type  # 频道type，字符串
                        # fields["url"] = contentJson['source_url']  # 分享的网址，字符串
                        # fields["workerid"] = item['ctId']  # 文章id，字符串
                        # fields["title"] = item['title']  # 文章标题，字符串
                        fields["content"] = contentJson['articleinfo']['content']  # 文章内容，字符串
                        # fields["articlecovers"] = imgList  # 列表封面，数组
                        fields["images"] = InitClass.get_images(fields["content"])  # 正文图片，数组
                        # fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                        # fields["videocover"] = [item['videoImg']]  # 视频封面，数组
                        # fields["width"] = ''  # 视频宽，字符串
                        # fields["height"] = ''  # 视频高，字符串
                        fields["source"] = contentJson['articleinfo']['source']  # 文章来源，字符串
                        # fields["pubtime"] = contentJson['ptime']  # 发布时间，时间戳（毫秒级，13位）
                        # fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                        # fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                        # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                        # fields["playnum"] = ''  # 播放数，数值
                        # fields["commentnum"] = item['commentNum']  # 评论数，数值
                        # fields["readnum"] = contentJson['views']  # 阅读数，数值
                        # fields["trannum"] = ''  # 转发数，数值
                        # fields["sharenum"] = ''  # 分享数，数值
                        # fields["author"] = contentJson['username']  # 作者，字符串
                        # fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                        # fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                        # fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                        # fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
                        if len(contentJson['articleinfo']['pics_info']):
                            print(contentJson['articleinfo']['pics_info'])
                    elif "tblive" == newsType:
                        pass  # 详情是网址
                    else:
                        print(contentJson)
                    print(json.dumps(fields, indent=4, ensure_ascii=False))
                else:
                    print("未获取到详情", fields)
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
    appspider = ZhuangGuan("壮观")
    appspider.run()
