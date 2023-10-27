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


def setListNewsParam(articlesparams, channelname, channelid, item):
    try:
        article_fields = InitClass().article_fields()
        article_fields["channelname"] = channelname  # 频道名称，字符串
        article_fields["channelID"] = channelid  # 频道id，字符串
        # article_fields["channelType"] = channel_type  # 频道type，字符串
        article_fields["url"] = item['url']  # 分享的网址，字符串
        article_fields["title"] = item['title']  # 文章标题，字符串
        # article_fields["content"] = item['webLink']  # 文章内容，字符串
        if len(item['imgsrc']):
            article_fields["articlecovers"] = [item['imgsrc']]  # 列表封面，数组
        # article_fields["images"] = ''  # 正文图片，数组
        # article_fields["videocover"] = [item['videoImg']]  # 视频封面，数组
        # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
        # article_fields["width"] = ''  # 视频宽，字符串
        # article_fields["height"] = ''  # 视频高，字符串
        if 'sourcename' in item.keys():
            article_fields["source"] = item['sourcename']  # 文章来源，字符串
        article_fields["pubtime"] = InitClass().date_time_stamp(item['ptime'])  # 发布时间，时间戳（毫秒级，13位）
        # article_fields["createtime"] = item['createdate']  # 创建时间，时间戳（毫秒级，13位）
        # article_fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
        # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
        # article_fields["playnum"] = ''  # 播放数，数值
        # article_fields["commentnum"] = item['commentNum']  # 评论数，数值
        # article_fields["readnum"] = ''  # 阅读数，数值
        # article_fields["trannum"] = ''  # 转发数，数值
        # article_fields["sharenum"] = ''  # 分享数，数值
        article_fields["author"] = item['author']  # 作者，字符串
        if -1 == channelid:
            article_fields["banner"] = 1  # banner标记，数值（0标识不是，1标识是）
        else:
            article_fields["banner"] = 0  # banner标记，数值（0标识不是，1标识是）
        article_fields["workerid"] = item['docid']  # 文章id，字符串
        # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
        # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
        # article_fields["newstype"] = "QxDataDef"  # 自己添加新闻类型
        articleparam = InitClass().article_list_fields()
        articleparam["articelField"] = article_fields
        articlesparams.append(articleparam)
    except Exception as e:
        logging.info(e)
    return articlesparams


videoList = ["1884", "1885", "1065", "1061", "2171", "2451"]


class QinFengWang(Appspider):

    def analyze_channel(self):
        channelparams = []
        channelDir = {
            # home_title
            "1003": "要闻",
            "1070": "审查",
            "1924": "曝光",
            "1023": "巡视",
            "1024": "巡察",
            "1005": "地市",
            "1865": "警示",
            "1871": "文化",
            "2092": "论坛",
            "1011": "派驻",
            "2201": "国企高校",
            # home_unseletced_title
            "1025": "西安",
            "1026": "咸阳",
            "1027": "商洛",
            "1028": "宝鸡",
            "1029": "安康",
            "1030": "汉中",
            "1031": "延安",
            "1032": "渭南",
            "1033": "榆林",
            "1034": "铜川",
            "1035": "杨凌",
            "1036": "西咸新区",
            # video_title
            "1884": "图解",
            "1885": "镜头",
            "1065": "微视频",
            "1061": "公益广告",
            "2171": "动漫",
            "2451": "视频新闻",
        }
        for k, v in channelDir.items():
            channelid = k
            channelname = v
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)

        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            if videoList.count(channelid):
                url = "http://124.115.170.39:8082/system/rest/UserInfoService/getlistVadio"
                headers = {
                    "Content-Type": "application/json;charset=UTF-8",
                    "Content-Length": "65",
                    "Host": "124.115.170.39:8082",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.3.0",
                }
                method = "post"
                channelJson = {"count": "10", "owner": "1394186967", "start": "0", "wbtreeid": channelid}
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           channelid=channelid, channeljson=channelJson)
                articlelistsparams.append(articlelist_param)
            else:
                url = "http://124.115.170.39:8082/system/rest/UserInfoService/getlistByTreeidAll"
                headers = {
                    "Content-Type": "application/json;charset=UTF-8",
                    "Content-Length": "65",
                    "Host": "124.115.170.39:8082",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.3.0",
                }
                method = "post"
                channelJson = {}
                if '1003' == channelid:
                    channelJson = {"count": "10", "owner": "1394186967", "start": "10", "wbtreeid": channelid}
                else:
                    channelJson = {"count": "10", "owner": "1394186967", "start": "0", "wbtreeid": channelid}
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           channelid=channelid, channeljson=channelJson)
                articlelistsparams.append(articlelist_param)
        urlBanner = "http://124.115.170.39:8082/system/rest/Sowing_Map/Sowing_MapNews"
        headersBanner = {
            "Content-Type": "application/json;charset=UTF-8",
            "Content-Length": "65",
            "Host": "124.115.170.39:8082",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.3.0",
        }
        methodBanner = "post"
        channelJsonBanner = {}
        articlelistParamBanner = InitClass().articlelists_params_fields(urlBanner, headersBanner, methodBanner,
                                                                        "banner",
                                                                        channelid=-1, channeljson=channelJsonBanner)
        articlelistsparams.append(articlelistParamBanner)
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
                    for item in articleslists:
                        if 'info' in item.keys():
                            for item1 in item['info']:
                                if "list" in item1.keys():
                                    for newsItem in item1['list']:
                                        articlesparams = setListNewsParam(articlesparams, channelname, channelid,
                                                                          newsItem)
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
            url = "http://124.115.170.39:8082/system/rest/UserInfoService/getWbnewsById"
            headers = {
                "Content-Type": "application/json;charset=UTF-8",
                "Content-Length": "65",
                "Host": "124.115.170.39:8082",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.3.0",
            }
            method = "post"
            articleJson = {"owner": "1394186967", "wbnewsid": article_field.get("workerid")}
            articleparam = InitClass().article_params_fields(url, headers, method, articlejson=articleJson,
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
                print(contentJson)
                fields["appname"] = appname  # 应用名称，字符串
                content = contentJson[0]['info'][0]['body']
                img = contentJson[0]['info'][0]['img']
                imgList = img[1:len(img) - 1].replace(" ", "").split(',')
                for item in imgList:
                    print(item)
                    str1 = item[0:12]
                    str2 = item[13:len(item)]
                    if str2.find("http://www.qinfeng.gov.cnhttp") != -1:
                        str2 = str2[25:len(str2)]
                    content = content.replace(str1, str2)
                fields["content"] = content  # 文章内容，字符串
                # article_fields["channelname"] = channelname  # 频道名称，字符串
                # article_fields["channelID"] = channelid  # 频道id，字符串
                # article_fields["channelType"] = channel_type  # 频道type，字符串
                # article_fields["url"] = item['url']  # 分享的网址，字符串
                # article_fields["title"] = item['title']  # 文章标题，字符串
                # article_fields["articlecovers"] = [item['imgsrc']]  # 列表封面，数组
                fields["images"] = InitClass().get_images(content)  # 正文图片，数组
                # fields["videocover"] = [item['videoImg']]  # 视频封面，数组
                if ".mp4" in fields['url']:
                    fields["videos"] = [fields['url']]  # 视频地址，数组
                # article_fields["width"] = ''  # 视频宽，字符串
                # article_fields["height"] = ''  # 视频高，字符串
                # article_fields["source"] = item['sourcename']  # 文章来源，字符串
                # article_fields["pubtime"] = InitClass().date_time_stamp(item['ptime'])  # 发布时间，时间戳（毫秒级，13位）
                # article_fields["createtime"] = item['createdate']  # 创建时间，时间戳（毫秒级，13位）
                # article_fields["updatetime"] = ''  # 更新时间，时间戳（毫秒级，13位）
                # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                # article_fields["playnum"] = ''  # 播放数，数值
                # article_fields["commentnum"] = item['commentNum']  # 评论数，数值
                # article_fields["readnum"] = ''  # 阅读数，数值
                # article_fields["trannum"] = ''  # 转发数，数值
                # article_fields["sharenum"] = ''  # 分享数，数值
                # article_fields["author"] = item['author']  # 作者，字符串
                # article_fields["banner"] = 1  # banner标记，数值（0标识不是，1标识是）
                # article_fields["workerid"] = item['docid']  # 文章id，字符串
                # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                print(json.dumps(fields, indent=4, ensure_ascii=False))
            except Exception as e:
                num += 1
                logging.info(f"错误数量{num},{e}")

    def run(self):
        channelsparams = self.analyze_channel()
        articlelistparames = self.getarticlelistparams(channelsparams.__next__())
        articleslistsres = self.getarticlelists(articlelistparames.__next__())
        articles = self.analyze_articlelists(articleslistsres.__next__())
        articleparams = self.getarticleparams(articles.__next__())
        articlesres = self.getarticlehtml(articleparams.__next__())
        self.analyzearticle(articlesres.__next__())


if __name__ == '__main__':
    appspider = QinFengWang("秦风网")
    appspider.run()
