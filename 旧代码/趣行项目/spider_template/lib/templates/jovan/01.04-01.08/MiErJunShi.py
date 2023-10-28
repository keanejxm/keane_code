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
        # article_fields["url"] = item['Url']  # 分享的网址，字符串
        if 'id' in item.keys():
            article_fields["workerid"] = item['id']  # 文章id，字符串
        elif 'aid' in item.keys():
            article_fields["workerid"] = item['aid']  # 文章id，字符串
        else:
            pass
        article_fields["title"] = item['title']  # 文章标题，字符串
        # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
        imgList = []
        if 'picList' in item.keys() and len(item['picList']):
            imgList = item['picList']
        article_fields["articlecovers"] = imgList  # 列表封面，数组
        # article_fields["images"] = ''  # 正文图片，数组
        # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
        # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
        # article_fields["width"] = ''  # 视频宽，字符串
        # article_fields["height"] = ''  # 视频高，字符串
        # article_fields["source"] = item['SourceUrl']  # 文章来源，字符串
        # article_fields["pubtime"] = InitClass().date_time_stamp(item['PostDateTime'])  # 发布时间，时间戳（毫秒级，13位）
        # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
        # article_fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
        # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
        # article_fields["playnum"] = ''  # 播放数，数值
        # article_fields["commentnum"] = item['CommentCount']  # 评论数，数值
        # article_fields["readnum"] = item['ReadCount']  # 阅读数，数值
        # article_fields["trannum"] = ''  # 转发数，数值
        # article_fields["sharenum"] = item['ShareCount']  # 分享数，数值
        # article_fields["author"] = ''  # 作者，字符串
        article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
        # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
        # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
        # article_fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
        # article_fields["newsType"] = item['Type']  # 自己添加新闻类型
    except Exception as e:
        print(e)
    return article_fields


class MiErJunShi(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://api.wap.junshijia.com/api/apps/index.php?"
        headers = {
            "Content-Length": "274",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "api.wap.junshijia.com",
            "Connection": "Keep-Alive",
            "User-Agent": "Mozilla/5.0 (Linux; U; Android 10; zh-cn; ALP-AL00 Build/HUAWEIALP-AL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Accept-Encoding": "gzip",
        }
        method = "post"
        param_json = 'proct=mierapp&controller=Modules&app_version=2.8.4&apiCode=7&os_version=ALP-AL00%2C10&device_uuid=383951470e3c80700aee41d9967ae991&app_channel=market_xiaomi&os_sdk=29&province=%E9%83%91%E5%B7%9E&user_id=0&action=index&getLoginLog=true&plat=android&versioncode=20201105&vip=0'
        app_params1 = InitClass().app_params(url, headers, method, appjson=param_json)

        yield [app_params1]

    def analyze_channel(self, channelsres):
        # print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            if "http://api.wap.junshijia.com/api/apps/index.php?" == k:
                channelList = json.loads(v)
                for channel in channelList['data']['newsChannels']['channelList']:
                    if 'extend_url' in channel.keys() and channel['extend_url']:
                        print(channel)
                    else:
                        channelid = channel['id']
                        channelname = channel['name']
                        channelparam = InitClass().channel_fields(channelid, channelname)
                        channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "http://api.wap.junshijia.com/api/apps/index.php?"
        headers = {
            "Content-Length": "294",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "api.wap.junshijia.com",
            "Connection": "Keep-Alive",
            "User-Agent": "Mozilla/5.0 (Linux; U; Android 10; zh-cn; ALP-AL00 Build/HUAWEIALP-AL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Accept-Encoding": "gzip",
        }
        method = "post"

        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            param_json = f'proct=mierapp&controller=News&app_version=2.8.4&city=&apiCode=7&os_version=ALP-AL00%2C10&channel={channelid}&device_uuid=383951470e3c80700aee41d9967ae991&app_channel=market_xiaomi&apiVersion=v1&os_sdk=29&province=%E9%83%91%E5%B7%9E&user_id=0&action=newslist&page=1&plat=android&versioncode=20201105&vip=0'

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channeljson=param_json, channelid=channelid)
            articlelistsparams.append(articlelist_param)
        yield articlelistsparams

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    print(articleslists)
                    if 'data' in articleslists.keys() and 'newsLists' in articleslists['data'].keys():
                        for item_news in articleslists['data']['newsLists']:
                            if 15 == item_news['newsShowType']:
                                for item_arc in item_news['arcList']:
                                    article_fields = setListNewsParam(channelname, channelid, 1, item_arc)
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                            else:
                                article_fields = setListNewsParam(channelname, channelid, 0, item_news)
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
        url = "http://api.wap.junshijia.com/api/apps/index.php?"
        headers = {
            "Content-Length": "294",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "api.wap.junshijia.com",
            "Connection": "Keep-Alive",
            "User-Agent": "okhttp/2.5.0",
            "Accept-Encoding": "gzip",
        }
        method = "post"

        for article in articles:
            article_field = article.get('articelField')
            workerid = article_field.get('workerid')
            param_json = f"proct=mierapp&controller=Article&app_version=2.8.4&apiCode=7&os_version=ALP-AL00%2C10&device_uuid=383951470e3c80700aee41d9967ae991&app_channel=market_xiaomi&apiVersion=v1&os_sdk=29&province=%E9%83%91%E5%B7%9E&user_id=0&action=details&plat=android&versioncode=20201105&vip=0&aid={workerid}&"
            articleparam = InitClass().article_params_fields(url, headers, method, article_field=article_field,
                                                             articlejson=param_json)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            appname = article.get("appname")
            fields = article.get("articleField")
            try:
                if article.get("articleres"):
                    contentJson = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                    print(contentJson)
                    fields["appname"] = appname  # 应用名称，字符串
                    # fields["channelname"] = channelname  # 频道名称，字符串
                    # fields["channelID"] = channelid  # 频道id，字符串
                    # fields["channelType"] = channel_type  # 频道type，字符串
                    fields["url"] = contentJson['data']['shareUrl']  # 分享的网址，字符串
                    # fields["workerid"] = item['ctId']  # 文章id，字符串
                    # fields["title"] = item['title']  # 文章标题，字符串
                    fields["content"] = contentJson['data']['webContent']  # 文章内容，字符串
                    # fields["articlecovers"] = imgList  # 列表封面，数组
                    fields["images"] = InitClass.get_images(fields["content"])  # 正文图片，数组
                    if 'videoUrl' in contentJson['data'].keys() and contentJson['data']['videoUrl']:
                        fields["videos"] = [contentJson['data']['videoUrl']]  # 视频地址，数组
                    # fields["videocover"] = [item['videoImg']]  # 视频封面，数组
                    # fields["width"] = ''  # 视频宽，字符串
                    # fields["height"] = ''  # 视频高，字符串
                    # fields["source"] = contentJson['source']  # 文章来源，字符串
                    fields["pubtime"] = contentJson['data']['publishTime']  # 发布时间，时间戳（毫秒级，13位）
                    # fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                    # fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                    # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                    # fields["playnum"] = ''  # 播放数，数值
                    # fields["commentnum"] = item['commentNum']  # 评论数，数值
                    # fields["readnum"] = contentJson['views']  # 阅读数，数值
                    # fields["trannum"] = ''  # 转发数，数值
                    # fields["sharenum"] = ''  # 分享数，数值
                    fields["author"] = contentJson['data']['authorNickName']  # 作者，字符串
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
    appspider = MiErJunShi("米尔军事")
    appspider.run()
