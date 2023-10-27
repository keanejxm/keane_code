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
        article_fields["workerid"] = item['NewsID']  # 文章id，字符串
        article_fields["title"] = item['NewsTitle']  # 文章标题，字符串
        # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
        if item['NewsDefImagePath']:
            article_fields["articlecovers"] = [item['NewsDefImagePath']]  # 列表封面，数组
        # article_fields["images"] = ''  # 正文图片，数组
        # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
        # article_fields["videocover"] = [item['coverUrl']]  # 视频封面，数组
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
    except Exception as e:
        print(e)
    return article_fields


class JiuPaiXinWen(Appspider):

    @staticmethod
    def get_app_params():
        url1 = "http://bbcm.bhxww.com/Data/News/NewsCates.ashx?pagesize=1000&open=1&notin=1&mid=0"
        headers = {
            "Host": "bbcm.bhxww.com",
            "Connection": "keep-alive",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 Html5Plus/1.0",
            "X-Requested-With": "com.bhxww.app",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        method = "get"

        app_params1 = InitClass().app_params(url1, headers, method)

        yield [app_params1]

    def analyze_channel(self, channelsres):
        print(channelsres)
        channelparams = []
        channelidAll = 0
        channelnameAll = "全部"
        channelparamAll = InitClass().channel_fields(channelidAll, channelnameAll)
        channelparams.append(channelparamAll)
        for k, v in channelsres.items():
            if "http://bbcm.bhxww.com/Data/News/NewsCates.ashx?pagesize=1000&open=1&notin=1&mid=0" == k:
                channelList = json.loads(v)
                for channel in channelList['Models']:
                    channelid = channel['NewsCateID']
                    channelname = channel['NewsCateName']
                    channelparam = InitClass().channel_fields(channelid, channelname)
                    channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "http://bbcm.bhxww.com/Data/News/NewsList.ashx"
        headers = {
            "Host": "bbcm.bhxww.com",
            "Connection": "keep-alive",
            "Content-Length": "37",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 Html5Plus/1.0",
            "Content-Type": "application/x-www-form-urlencoded;",
            "Accept": "*/*",
            "X-Requested-With": "com.bhxww.app",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        method = "post"

        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            data = f'dppf=2&cid={channelid}&page=1&pagesize=10&key='
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                       channelid=channelid)
            articlelistsparams.append(articlelist_param)

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
                    # print(articleslists)
                    if 'Models' in articleslists.keys():
                        if isinstance(articleslists['Models'], list):
                            for item in articleslists['Models']:
                                article_fields = setListNewsParam(channelname, channelid, banners, item)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        else:
                            print(articleslists['Models'])
                    else:
                        print("列表没数据", articleslists)
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        url = "http://bbcm.bhxww.com/Data/News/NewsInfo.ashx"
        headers = {
            "Host": "bbcm.bhxww.com",
            "Connection": "keep-alive",
            "Content-Length": "37",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 Html5Plus/1.0",
            "Content-Type": "application/x-www-form-urlencoded;",
            "Accept": "*/*",
            "X-Requested-With": "com.bhxww.app",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        method = "post"
        for article in articles:
            article_field = article.get('articelField')
            data = f"id={article_field['workerid']}"
            articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                             article_field=article_field)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            appname = article.get("appname")
            fields = article.get("articleField")
            try:
                contentJson = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                # print(contentJson)
                fields["appname"] = appname  # 应用名称，字符串
                # fields["channelname"] = channelname  # 频道名称，字符串
                # fields["channelID"] = channelid  # 频道id，字符串
                # fields["channelType"] = channel_type  # 频道type，字符串
                # fields["url"] = contentJson['infoCont']  # 分享的网址，字符串
                # fields["workerid"] = item['ctId']  # 文章id，字符串
                # fields["title"] = item['title']  # 文章标题，字符串
                content = InitClass.decode_base64(contentJson['NewsContent'])
                fields["content"] = content  # 文章内容，字符串
                # fields["articlecovers"] = imgList  # 列表封面，数组
                fields["images"] = InitClass.get_images(fields["content"])  # 正文图片，数组
                fields["videos"] = InitClass.get_video(fields["content"])  # 视频地址，数组
                # fields["videocover"] = [item['videoImg']]  # 视频封面，数组
                # fields["width"] = ''  # 视频宽，字符串
                # fields["height"] = ''  # 视频高，字符串
                # fields["source"] = ''  # 文章来源，字符串
                # fields["pubtime"] =  ''  # 发布时间，时间戳（毫秒级，13位）
                fields["createtime"] = InitClass().date_time_stamp(contentJson['CDate'])  # 创建时间，时间戳（毫秒级，13位）
                # fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                # fields["playnum"] = ''  # 播放数，数值
                # fields["commentnum"] = item['commentNum']  # 评论数，数值
                # fields["readnum"] = item['realRead']  # 阅读数，数值
                # fields["trannum"] = ''  # 转发数，数值
                # fields["sharenum"] = ''  # 分享数，数值
                # fields["author"] = contentJson['NewsSrc']  # 作者，字符串
                # fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                # fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                # fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                # fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串

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
    appspider = JiuPaiXinWen("北海第一眼")
    appspider.run()
