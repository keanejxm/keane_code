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

channelListDir = {
    # 头条-POST-clientversion=129&page=0&operation=up&uuid=ffffffff-f112-77c8-0000-000000000000&platform=2&channelCode=hua_wei_kai_fa_zhe_lian_meng
    588: {"url": "http://appservices.3xmt.com/v2/news/index",
          "header": {"Content-Type": "application/x-www-form-urlencoded",
                     "Content-Length": "131",
                     "Host": "appservices.3xmt.com",
                     "Connection": "Keep-Alive",
                     "Accept-Encoding": "gzip",
                     "User-Agent": "okhttp/3.10.0",
                     },
          "method": "post",
          "data": {"clientversion": "129",
                   "page": "0",
                   "operation": "up",
                   "uuid": "ffffffff-f112-77c8-0000-000000000000",
                   "platform": "2",
                   "channelCode": "hua_wei_kai_fa_zhe_lian_meng",
                   },
          },
    # 权威发布-POST-clientversion=129&uuid=ffffffff-f112-77c8-0000-000000000000&platform=2&channelCode=hua_wei_kai_fa_zhe_lian_meng
    585: {"url": "http://appservices.3xmt.com/v2/authorityRelease/getSectionNews",
          "header": {"Content-Type": "application/x-www-form-urlencoded",
                     "Content-Length": "111",
                     "Host": "appservices.3xmt.com",
                     "Connection": "Keep-Alive",
                     "Accept-Encoding": "gzip",
                     "User-Agent": "okhttp/3.10.0",
                     },
          "method": "post",
          "data": {"clientversion": "129",
                   "uuid": "ffffffff-f112-77c8-0000-000000000000",
                   "platform": "2",
                   "channelCode": "hua_wei_kai_fa_zhe_lian_meng",
                   },
          },
    # 政务政策-POST-clientversion=129&pageSize=20&page=0&uuid=ffffffff-f112-77c8-0000-000000000000&platform=2&channelCode=hua_wei_kai_fa_zhe_lian_meng
    392: {"url": "http://appservices.3xmt.com/v2/policy/list/index",
          "header": {"Content-Type": "application/x-www-form-urlencoded",
                     "Content-Length": "130",
                     "Host": "appservices.3xmt.com",
                     "Connection": "Keep-Alive",
                     "Accept-Encoding": "gzip",
                     "User-Agent": "okhttp/3.10.0",
                     },
          "method": "post",
          "data": {"clientversion": "129",
                   "pageSize": "20",
                   "page": "0",
                   "uuid": "ffffffff-f112-77c8-0000-000000000000",
                   "platform": "2",
                   "channelCode": "hua_wei_kai_fa_zhe_lian_meng",
                   },
          },
    # 成都-POST-clientversion=129&locationid=12&page=0&uuid=ffffffff-f112-77c8-0000-000000000000&platform=2&channelCode=hua_wei_kai_fa_zhe_lian_meng
    2: {"url": "http://appservices.3xmt.com/v2/citynews/list",
        "header": {"Content-Type": "application/x-www-form-urlencoded",
                   "Content-Length": "132",
                   "Host": "appservices.3xmt.com",
                   "Connection": "Keep-Alive",
                   "Accept-Encoding": "gzip",
                   "User-Agent": "okhttp/3.10.0",
                   },
        "method": "post",
        "data": {"clientversion": "129",
                 "locationid": "0",
                 "page": "0",
                 "uuid": "ffffffff-f112-77c8-0000-000000000000",
                 "platform": "2",
                 "channelCode": "hua_wei_kai_fa_zhe_lian_meng",
                 },
        },
    # 民生-POST-clientversion=129&sectioncode=Livelihood&page=0&sectionid=106&uuid=ffffffff-f112-77c8-0000-000000000000&platform=2&channelCode=hua_wei_kai_fa_zhe_lian_meng
    106: {"url": "http://appservices.3xmt.com/v2/news/section",
          "header": {"Content-Type": "application/x-www-form-urlencoded",
                     "Content-Length": "155",
                     "Host": "appservices.3xmt.com",
                     "Connection": "Keep-Alive",
                     "Accept-Encoding": "gzip",
                     "User-Agent": "okhttp/3.10.0",
                     },
          "method": "post",
          "data": {"clientversion": "129",
                   "sectioncode": "Livelihood",
                   "page": "0",
                   "sectionid": "106",
                   "uuid": "ffffffff-f112-77c8-0000-000000000000",
                   "platform": "2",
                   "channelCode": "hua_wei_kai_fa_zhe_lian_meng",
                   },
          },
    # 教育-POST-clientversion=129&page=0&sectionid=645&uuid=ffffffff-f112-77c8-0000-000000000000&platform=2&channelCode=hua_wei_kai_fa_zhe_lian_meng
    645: {"url": "http://appservices.3xmt.com/v2/news/section",
          "header": {"Content-Type": "application/x-www-form-urlencoded",
                     "Content-Length": "132",
                     "Host": "appservices.3xmt.com",
                     "Connection": "Keep-Alive",
                     "Accept-Encoding": "gzip",
                     "User-Agent": "okhttp/3.10.0",
                     },
          "method": "post",
          "data": {"clientversion": "129",
                   "page": "0",
                   "sectionid": "645",
                   "uuid": "ffffffff-f112-77c8-0000-000000000000",
                   "platform": "2",
                   "channelCode": "hua_wei_kai_fa_zhe_lian_meng",
                   },
          },
    # 数据报告，这个是网址
    # 589: "",
    # 公益-POST-clientversion=129&page=0&uuid=ffffffff-f112-77c8-0000-000000000000&platform=2&channelCode=hua_wei_kai_fa_zhe_lian_meng
    108: {"url": "http://appservices.3xmt.com/v2/commonweal/getCommonweal",
          "header": {"Content-Type": "application/x-www-form-urlencoded",
                     "Content-Length": "118",
                     "Host": "appservices.3xmt.com",
                     "Connection": "Keep-Alive",
                     "Accept-Encoding": "gzip",
                     "User-Agent": "okhttp/3.10.0",
                     },
          "method": "post",
          "data": {"clientversion": "129",
                   "page": "0",
                   "uuid": "ffffffff-f112-77c8-0000-000000000000",
                   "platform": "2",
                   "channelCode": "hua_wei_kai_fa_zhe_lian_meng",
                   },
          },
    # 问政-GET-uuid=ffffffff-f112-77c8-0000-000000000000&platform=2&clientversion=129&page=0
    390: {"url": "http://appservices.3xmt.com/v2/question/list",
          "header": {"Host": "appservices.3xmt.com",
                     "Connection": "Keep-Alive",
                     "Accept-Encoding": "gzip",
                     "User-Agent": "okhttp/3.10.0",
                     },
          "method": "get",
          "data": {"uuid": "ffffffff-f112-77c8-0000-000000000000",
                   "platform": "2",
                   "clientversion": "129",
                   "page": "0",
                   },
          },
    # 融媒产品-GET-uuid=ffffffff-f112-77c8-0000-000000000000&uid=0&platform=2&clientversion=129
    586: {"url": "http://appservices.3xmt.com/v2/mediumProduct/getMediumProductNews",
          "header": {"Host": "appservices.3xmt.com",
                     "Connection": "Keep-Alive",
                     "Accept-Encoding": "gzip",
                     "User-Agent": "okhttp/3.10.0",
                     },
          "method": "get",
          "data": {"uuid": "ffffffff-f112-77c8-0000-000000000000",
                   "uid": "0",
                   "platform": "2",
                   "clientversion": "129",
                   },
          },
    # 发布系-GET-nid=0&page=0&uuid=ffffffff-f112-77c8-0000-000000000000&uid=0&platform=2&clientversion=129
    -1: {"url": "http://appservices.3xmt.com/v2/news-subscribe/personalize",
         "header": {"Host": "appservices.3xmt.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.10.0",
                    },
         "method": "get",
         "data": {"nid": "0",
                  "page": "0",
                  "uuid": "ffffffff-f112-77c8-0000-000000000000",
                  "uid": "0",
                  "platform": "2",
                  "clientversion": "129",
                  },
         },
    # 直播-POST-clientversion=129&pagesize=20&page=0&uuid=ffffffff-f112-77c8-0000-000000000000&platform=2&channelCode=hua_wei_kai_fa_zhe_lian_meng
    -2: {"url": "http://appservices.3xmt.com/v2/living/center",
         "header": {"Content-Type": "application/x-www-form-urlencoded",
                    "Content-Length": "130",
                    "Host": "appservices.3xmt.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.10.0",
                    },
         "method": "post",
         "data": {"clientversion": "129",
                  "pagesize": "20",
                  "page": "0",
                  "uuid": "ffffffff-f112-77c8-0000-000000000000",
                  "platform": "2",
                  "channelCode": "hua_wei_kai_fa_zhe_lian_meng",
                  },
         },
}


def setListNewsParam(channelname, channelid, banner, item):
    try:
        article_fields = InitClass().article_fields()
        article_fields["channelname"] = channelname  # 频道名称，字符串
        article_fields["channelID"] = channelid  # 频道id，字符串
        # article_fields["channelType"] = channel_type  # 频道type，字符串
        # article_fields["url"] = url  # 分享的网址，字符串
        article_fields["workerid"] = item['id']  # 文章id，字符串
        article_fields["title"] = item['title']  # 文章标题，字符串
        # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
        if 'picurl' in item.keys() and item['picurl']:
            article_fields["articlecovers"] = [item['picurl']]  # 列表封面，数组
        # article_fields["images"] = ''  # 正文图片，数组
        if 'videourl' in item.keys() and item['videourl']:
            article_fields["videos"] = [item['videourl']]  # 视频地址，数组
        if 'videoPoster' in item.keys() and item['videoPoster']:
            article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
        # article_fields["width"] = ''  # 视频宽，字符串
        # article_fields["height"] = ''  # 视频高，字符串
        # article_fields["source"] = ''  # 文章来源，字符串
        # article_fields["pubtime"] = InitClass.date_time_stamp(item['showtime'])  # 发布时间，时间戳（毫秒级，13位）
        # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
        # article_fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
        # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
        # article_fields["playnum"] = ''  # 播放数，数值
        # article_fields["commentnum"] = item['commentNum']  # 评论数，数值
        article_fields["readnum"] = item['viewcount']  # 阅读数，数值
        # article_fields["trannum"] = ''  # 转发数，数值
        # article_fields["sharenum"] = ''  # 分享数，数值
        # article_fields["author"] = ''  # 作者，字符串
        article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
        # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
        # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
        # article_fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
        article_fields["newsType"] = item['newstype']  # 自己添加新闻类型
    except Exception as e:
        print(e)
    return article_fields


class SiChuanFaBu(Appspider):
    @staticmethod
    def get_app_params():
        url1 = "http://appservices.3xmt.com/v2/section/index"
        headers = {
            "Host": "appservices.3xmt.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.10.0",
        }
        method = "get"
        data = {
            "uuid": "ffffffff-f112-77c8-0000-000000000000",
            "uid": "0",
            "platform": "2",
            "clientversion": "129",
        }
        app_params1 = InitClass().app_params(url1, headers, method, data=data)

        yield [app_params1]

    def analyze_channel(self, channelsres):
        print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            if "http://appservices.3xmt.com/v2/section/index" == k:
                channelList = json.loads(v)
                for channel in channelList['object']:
                    channelid = channel['id']
                    channelname = channel['name']
                    channelparam = InitClass().channel_fields(channelid, channelname)
                    channelparams.append(channelparam)
        channelparam = InitClass().channel_fields(-1, "发布系")
        channelparams.append(channelparam)
        channelparam = InitClass().channel_fields(-2, "直播")
        channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = ""
        headers = {
            "Host": "www3.ctdsb.net",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/2.5.0",
        }
        method = "get"
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            if channelid in channelListDir.keys():
                url = channelListDir[channelid]["url"]
                header = channelListDir[channelid]["header"]
                method = channelListDir[channelid]["method"]
                data = channelListDir[channelid]["data"]

                articlelist_param = InitClass().articlelists_params_fields(url, header, method, data=data,
                                                                           channel_name=channelname,
                                                                           channelid=channelid)
                articlelistsparams.append(articlelist_param)
        url = 'http://appservices.3xmt.com/v2/location/list/vo'
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "147",
            "Host": "appservices.3xmt.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.10.0",
        }
        data = {
            "clientversion": "129",
            "location": "38.041072,114.524828",
            "type": "0",
            "uuid": "ffffffff-f112-77c8-0000-000000000000",
            "platform": "2",
            "channelCode": "hua_wei_kai_fa_zhe_lian_meng",
        }
        response = requests.post(url=url, headers=headers, data=data).content.decode()
        channelcity = json.loads(response)
        print(channelcity)
        for city in channelcity['object']['areaList']:
            url = "http://appservices.3xmt.com/v2/citynews/list"
            header = {"Content-Type": "application/x-www-form-urlencoded",
                      "Content-Length": "132",
                      "Host": "appservices.3xmt.com",
                      "Connection": "Keep-Alive",
                      "Accept-Encoding": "gzip",
                      "User-Agent": "okhttp/3.10.0",
                      }
            method = "post"
            data = {"clientversion": "129",
                    "locationid": city['id'],
                    "page": "0",
                    "uuid": "ffffffff-f112-77c8-0000-000000000000",
                    "platform": "2",
                    "channelCode": "hua_wei_kai_fa_zhe_lian_meng",
                    }

            articlelist_param = InitClass().articlelists_params_fields(url, header, method, data=data,
                                                                       channel_name=city['name'],
                                                                       channelid=city['id'])
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
                    if 'object' in articleslists.keys():
                        if 'newsList' in articleslists['object'].keys():
                            for itemnews in articleslists['object']['newsList']:
                                article_fields = setListNewsParam(channelname, channelid, 0, itemnews)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        if 'recommendUIList' in articleslists['object'].keys():
                            pass  # 这个是快捷按钮
                        if 'livePreList' in articleslists['object'].keys():
                            for itemlive in articleslists['object']['livePreList']:
                                article_fields = setListNewsParam(channelname, channelid, 0, itemlive)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        if 'recommendNewsList' in articleslists['object'].keys():
                            for itemrecom in articleslists['object']['recommendNewsList']:
                                article_fields = setListNewsParam(channelname, channelid, 1, itemrecom)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        if 'authorityReleaseV2Vo' in articleslists['object'].keys():
                            for itemauthority in articleslists['object']['authorityReleaseV2Vo']:
                                if 'sectionList' in itemauthority:
                                    for itemauthoritysection in itemauthority['sectionList']:
                                        article_fields = setListNewsParam(channelname, channelid, 0,
                                                                          itemauthoritysection)
                                        articleparam = InitClass().article_list_fields()
                                        articleparam["articelField"] = article_fields
                                        articlesparams.append(articleparam)
                        if 'topList' in articleslists['object'].keys():
                            for itemtop in articleslists['object']['topList']:
                                article_fields = setListNewsParam(channelname, channelid, 1, itemtop)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        if 'readList' in articleslists['object'].keys():
                            for itemread in articleslists['object']['readList']:
                                article_fields = setListNewsParam(channelname, channelid, 0, itemread)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        if 'pubList' in articleslists['object'].keys():
                            for itempub in articleslists['object']['pubList']:
                                article_fields = setListNewsParam(channelname, channelid, 0, itempub)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        if 'sectionlist' in articleslists['object'].keys():
                            pass  # 这个是快捷按钮
                        if 'topnewslist' in articleslists['object'].keys():
                            for itemtopnews in articleslists['object']['topnewslist']:
                                article_fields = setListNewsParam(channelname, channelid, 1, itemtopnews)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        if 'secList' in articleslists['object'].keys():
                            for itemsec in articleslists['object']['secList']:
                                article_fields = setListNewsParam(channelname, channelid, 0, itemsec)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        if 'reportList' in articleslists['object'].keys():
                            for itemreport in articleslists['object']['reportList']:
                                article_fields = setListNewsParam(channelname, channelid, 0, itemreport)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        if 'mediumProductV2Vos' in articleslists['object'].keys():
                            for itemmedium in articleslists['object']['mediumProductV2Vos']:
                                if 'sectionList' in itemmedium:
                                    for itemmediumsection in itemmedium['sectionList']:
                                        article_fields = setListNewsParam(channelname, channelid, 0, itemmediumsection)
                                        articleparam = InitClass().article_list_fields()
                                        articleparam["articelField"] = article_fields
                                        articlesparams.append(articleparam)
                        if 'list' in articleslists['object'].keys():
                            for item in articleslists['object']['list']:
                                article_fields = setListNewsParam(channelname, channelid, 0, item)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        if 'livingReservationNews' in articleslists['object'].keys():
                            for itemlivingR in articleslists['object']['livingReservationNews']:
                                article_fields = setListNewsParam(channelname, channelid, 0, itemlivingR)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        if 'livingCenterNewsPage' in articleslists['object'].keys():
                            if 'list' in articleslists['object']['livingCenterNewsPage'].keys():
                                for livingC in articleslists['object']['livingCenterNewsPage']['list']:
                                    article_fields = setListNewsParam(channelname, channelid, 0, livingC)
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

            newsType = article_field.get('newsType')
            if "6" == newsType:
                url = f"http://scfbservices.3xmt.com/v2/news/special?newsid={article_field.get('workerid')}&uid=0&clientversion=129&uuid=ffffffff-f112-77c8-0000-000000000000&platform=2&verification=null&auth=null"
                headers = {
                    "Host": "scfbservices.3xmt.com",
                    "Connection": "keep-alive",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36",
                    "Origin": "http://appweb.scpublic.cn",
                    "X-Requested-With": "com.hisw.sichuan_publish",
                    "Referer": f"http://appweb.scpublic.cn/front-end/news-detail/special.html?newsid={article_field.get('workerid')}&uid=0&uuid=ffffffff-f112-77c8-0000-000000000000&platform=2&clientversion=129",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                }
                method = "get"
                articleparam = InitClass().article_params_fields(url, headers, method, article_field=article_field)
                articleparams.append(articleparam)
            else:
                url = f"http://appservices.3xmt.com/v2/news/detail"
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Content-Length": "125",
                    "Host": "appservices.3xmt.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.10.0",
                }
                method = "post"
                data = {
                    "newsid": article_field.get("workerid"),
                    "clientversion": "129",
                    "uuid": "ffffffff-f112-77c8-0000-000000000000",
                    "platform": "2",
                    "channelCode": "hua_wei_kai_fa_zhe_lian_meng",
                }
                articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            appname = article.get("appname")
            fields = article.get("articleField")
            newsType = fields.get('newsType')
            try:
                if article.get("articleres"):
                    contentJson = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                    # print(contentJson)
                    if "6" == newsType:
                        topicFields = InitClass().topic_fields()
                        topicFields["topicID"] = fields['workerid']  # 专题id，app内唯一标识
                        topicFields["platformName"] = appname  # 平台名字（app名字）
                        # topicFields["platformID"] = fields['workerid']
                        topicFields["channelName"] = fields['channelname']  # 频道名字
                        topicFields["channelID"] = fields['channelID']  # 频道id
                        # topicFields["topicUrl"] = contentJson['data']['sphead'][0]['shareUrl']  # topicUrl
                        topicFields["title"] = fields['title']
                        # topicFields["digest"] = contentJson['description']  # 简介，摘要
                        topicFields["topicCover"] = fields['articlecovers']
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
                        for topicCate in contentJson['object']['list']:
                            topicItem += topicCate['list']
                            topicItem += topicCate['listV2']
                        topicArticles = self.getTopicArticles(fields['channelname'], fields['channelID'],
                                                              topicFields['title'],
                                                              topicFields["topicID"], topicItem)
                        articleparams = self.getarticleparams(topicArticles.__next__())
                        articlesres = self.getarticlehtml(articleparams.__next__())
                        self.analyzearticle(articlesres.__next__())
                    else:
                        fields["appname"] = appname  # 应用名称，字符串
                        # fields["channelname"] = channelname  # 频道名称，字符串
                        # fields["channelID"] = channelid  # 频道id，字符串
                        # fields["channelType"] = channel_type  # 频道type，字符串
                        fields["url"] = contentJson['object']['news']['ext_shareurl']  # 分享的网址，字符串
                        # fields["workerid"] = item['ctId']  # 文章id，字符串
                        # fields["title"] = item['title']  # 文章标题，字符串
                        fields["content"] = contentJson['object']['news']['detail']  # 文章内容，字符串
                        # fields["articlecovers"] = imgList  # 列表封面，数组
                        fields["images"] = InitClass.get_images(fields["content"])  # 正文图片，数组
                        if 'linkurl' in contentJson['object']['news'].keys() and contentJson['object']['news'][
                            'linkurl']:
                            fields["videos"] = [contentJson['object']['news']['linkurl']]  # 视频地址，数组
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
                    print(json.dumps(fields, indent=4, ensure_ascii=False))
                else:
                    print("未获取到详情", fields)
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
                # article_fields["url"] = url  # 分享的网址，字符串
                article_fields["workerid"] = item['id']  # 文章id，字符串
                article_fields["title"] = item['title']  # 文章标题，字符串
                # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
                if 'picurl' in item.keys() and item['picurl']:
                    article_fields["articlecovers"] = [item['picurl']]  # 列表封面，数组
                # article_fields["images"] = ''  # 正文图片，数组
                if 'videourl' in item.keys() and item['videourl']:
                    article_fields["videos"] = [item['videourl']]  # 视频地址，数组
                if 'videoPoster' in item.keys() and item['videoPoster']:
                    article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
                # article_fields["width"] = ''  # 视频宽，字符串
                # article_fields["height"] = ''  # 视频高，字符串
                # article_fields["source"] = ''  # 文章来源，字符串
                # article_fields["pubtime"] = InitClass.date_time_stamp(item['showtime'])  # 发布时间，时间戳（毫秒级，13位）
                # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                # article_fields["updatetime"] = item['updateDate']  # 更新时间，时间戳（毫秒级，13位）
                # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                # article_fields["playnum"] = ''  # 播放数，数值
                # article_fields["commentnum"] = item['commentNum']  # 评论数，数值
                article_fields["readnum"] = item['viewcount']  # 阅读数，数值
                # article_fields["trannum"] = ''  # 转发数，数值
                # article_fields["sharenum"] = ''  # 分享数，数值
                # article_fields["author"] = ''  # 作者，字符串
                # article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                article_fields["specialtopic"] = 1  # 是否是专题，数值（0标识不是，1标识是）
                article_fields["topicid"] = topicId  # 专题id，字符串
                article_fields["topicTitle"] = topicTitle  # 专题标题，字符串
                article_fields["newsType"] = item['newstype']  # 自己添加新闻类型
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
    appspider = SiChuanFaBu("四川发布")
    appspider.run()
