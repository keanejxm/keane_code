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
        if 'article' in item.keys():
            if 'live' in item.keys():
                if item['live']:
                    # article_fields["channelType"] = channel_type  # 频道type，字符串
                    article_fields["url"] = item['article']['share_url']  # 分享的网址，字符串
                    article_fields["workerid"] = item['article']['id']  # 文章id，字符串
                    article_fields["title"] = item['article']['title']  # 文章标题，字符串
                    article_fields["content"] = item['live']['web_url']  # 文章内容，字符串
                    imgList = []
                    for img in item['article']['thumb_images']:
                        imgList.append(f"{item['article']['thumb_path']}{img}")
                    article_fields["articlecovers"] = imgList  # 列表封面，数组
                    # article_fields["images"] = ''  # 正文图片，数组
                    # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                    # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
                    # article_fields["width"] = ''  # 视频宽，字符串
                    # article_fields["height"] = ''  # 视频高，字符串
                    # article_fields["source"] = item['SourceUrl']  # 文章来源，字符串
                    article_fields["pubtime"] = item['article']['publish_time']  # 发布时间，时间戳（毫秒级，13位）
                    # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                    article_fields["updatetime"] = item['article']['updated_time']  # 更新时间，时间戳（毫秒级，13位）
                    # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                    # article_fields["playnum"] = ''  # 播放数，数值
                    # article_fields["commentnum"] = item['CommentCount']  # 评论数，数值
                    article_fields["readnum"] = item['article']['click_count']  # 阅读数，数值
                    # article_fields["trannum"] = ''  # 转发数，数值
                    # article_fields["sharenum"] = item['ShareCount']  # 分享数，数值
                    # article_fields["author"] = ''  # 作者，字符串
                    article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                    # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                    # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                    # article_fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
                    article_fields["newsType"] = "qxlive"  # 自己添加新闻类型
                else:
                    # article_fields["channelType"] = channel_type  # 频道type，字符串
                    article_fields["url"] = item['article']['share_url']  # 分享的网址，字符串
                    article_fields["workerid"] = item['article']['id']  # 文章id，字符串
                    article_fields["title"] = item['article']['title']  # 文章标题，字符串
                    # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
                    imgList = []
                    for img in item['article']['thumb_images']:
                        imgList.append(f"{item['article']['thumb_path']}{img}")
                    article_fields["articlecovers"] = imgList  # 列表封面，数组
                    # article_fields["images"] = ''  # 正文图片，数组
                    # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                    # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
                    # article_fields["width"] = ''  # 视频宽，字符串
                    # article_fields["height"] = ''  # 视频高，字符串
                    # article_fields["source"] = item['SourceUrl']  # 文章来源，字符串
                    article_fields["pubtime"] = item['article']['publish_time']  # 发布时间，时间戳（毫秒级，13位）
                    # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                    article_fields["updatetime"] = item['article']['updated_time']  # 更新时间，时间戳（毫秒级，13位）
                    # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                    # article_fields["playnum"] = ''  # 播放数，数值
                    # article_fields["commentnum"] = item['CommentCount']  # 评论数，数值
                    article_fields["readnum"] = item['article']['click_count']  # 阅读数，数值
                    # article_fields["trannum"] = ''  # 转发数，数值
                    # article_fields["sharenum"] = item['ShareCount']  # 分享数，数值
                    # article_fields["author"] = ''  # 作者，字符串
                    article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                    # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                    # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                    # article_fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
                    article_fields["newsType"] = "qxvideo"  # 自己添加新闻类型
            else:
                # article_fields["channelType"] = channel_type  # 频道type，字符串
                article_fields["url"] = item['article']['share_url']  # 分享的网址，字符串
                article_fields["workerid"] = item['article']['id']  # 文章id，字符串
                article_fields["title"] = item['article']['title']  # 文章标题，字符串
                # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
                imgList = []
                for img in item['article']['thumb_images']:
                    imgList.append(f"{item['article']['thumb_path']}{img}")
                article_fields["articlecovers"] = imgList  # 列表封面，数组
                # article_fields["images"] = ''  # 正文图片，数组
                # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
                # article_fields["width"] = ''  # 视频宽，字符串
                # article_fields["height"] = ''  # 视频高，字符串
                # article_fields["source"] = item['SourceUrl']  # 文章来源，字符串
                article_fields["pubtime"] = item['article']['publish_time']  # 发布时间，时间戳（毫秒级，13位）
                # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                article_fields["updatetime"] = item['article']['updated_time']  # 更新时间，时间戳（毫秒级，13位）
                # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                # article_fields["playnum"] = ''  # 播放数，数值
                # article_fields["commentnum"] = item['CommentCount']  # 评论数，数值
                article_fields["readnum"] = item['article']['click_count']  # 阅读数，数值
                # article_fields["trannum"] = ''  # 转发数，数值
                # article_fields["sharenum"] = item['ShareCount']  # 分享数，数值
                # article_fields["author"] = ''  # 作者，字符串
                article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                # article_fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
                article_fields["newsType"] = "qxdef"  # 自己添加新闻类型
        elif 'special' in item.keys():
            # article_fields["channelType"] = channel_type  # 频道type，字符串
            # article_fields["url"] = item['special']['share_url']  # 分享的网址，字符串
            article_fields["workerid"] = item['special']['id']  # 文章id，字符串
            article_fields["title"] = item['special']['title']  # 文章标题，字符串
            article_fields["content"] = item['special']['description']  # 文章内容，字符串
            imgList = []
            for img in item['special']['thumbnails']:
                imgList.append(img)
            article_fields["articlecovers"] = imgList  # 列表封面，数组
            # article_fields["images"] = ''  # 正文图片，数组
            # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
            # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
            # article_fields["width"] = ''  # 视频宽，字符串
            # article_fields["height"] = ''  # 视频高，字符串
            # article_fields["source"] = item['SourceUrl']  # 文章来源，字符串
            # article_fields["pubtime"] = item['special']['publish_time']  # 发布时间，时间戳（毫秒级，13位）
            # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
            article_fields["updatetime"] = item['special']['icon_update_time']  # 更新时间，时间戳（毫秒级，13位）
            # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
            # article_fields["playnum"] = ''  # 播放数，数值
            article_fields["commentnum"] = item['special']['article_count']  # 评论数，数值
            # article_fields["readnum"] = item['special']['click_count']  # 阅读数，数值
            # article_fields["trannum"] = ''  # 转发数，数值
            # article_fields["sharenum"] = item['ShareCount']  # 分享数，数值
            # article_fields["author"] = ''  # 作者，字符串
            article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
            # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
            # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
            # article_fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
            article_fields["newsType"] = "qxtopic"  # 自己添加新闻类型
        else:
            if 'live_status' in item.keys():
                # article_fields["channelType"] = channel_type  # 频道type，字符串
                # article_fields["url"] = item['share_url']  # 分享的网址，字符串
                article_fields["workerid"] = item['id']  # 文章id，字符串
                article_fields["title"] = item['title']  # 文章标题，字符串
                article_fields["content"] = item['web_url']  # 文章内容，字符串
                imgList = []
                if 'cover_path' in item.keys() and item['cover_path']:
                    imgList.append(item['cover_path'])
                article_fields["articlecovers"] = imgList  # 列表封面，数组
                # article_fields["images"] = ''  # 正文图片，数组
                # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
                # article_fields["width"] = ''  # 视频宽，字符串
                # article_fields["height"] = ''  # 视频高，字符串
                # article_fields["source"] = item['SourceUrl']  # 文章来源，字符串
                # article_fields["pubtime"] = item['ctime']  # 发布时间，时间戳（毫秒级，13位）
                # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                # article_fields["updatetime"] = item['article']['updated_time']  # 更新时间，时间戳（毫秒级，13位）
                # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                # article_fields["playnum"] = ''  # 播放数，数值
                # article_fields["commentnum"] = item['CommentCount']  # 评论数，数值
                # article_fields["readnum"] = item['article']['click_count']  # 阅读数，数值
                # article_fields["trannum"] = ''  # 转发数，数值
                # article_fields["sharenum"] = item['ShareCount']  # 分享数，数值
                # article_fields["author"] = ''  # 作者，字符串
                article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                # article_fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
                article_fields["newsType"] = "qxlivenotice"  # 自己添加新闻类型
            else:
                # article_fields["channelType"] = channel_type  # 频道type，字符串
                article_fields["url"] = item['share_url']  # 分享的网址，字符串
                article_fields["workerid"] = item['id']  # 文章id，字符串
                # article_fields["title"] = item['title']  # 文章标题，字符串
                article_fields["content"] = item['content']  # 文章内容，字符串
                # article_fields["articlecovers"] = imgList  # 列表封面，数组
                # article_fields["images"] = ''  # 正文图片，数组
                # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
                # article_fields["width"] = ''  # 视频宽，字符串
                # article_fields["height"] = ''  # 视频高，字符串
                # article_fields["source"] = item['SourceUrl']  # 文章来源，字符串
                article_fields["pubtime"] = item['ctime']  # 发布时间，时间戳（毫秒级，13位）
                # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                # article_fields["updatetime"] = item['article']['updated_time']  # 更新时间，时间戳（毫秒级，13位）
                # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                # article_fields["playnum"] = ''  # 播放数，数值
                # article_fields["commentnum"] = item['CommentCount']  # 评论数，数值
                # article_fields["readnum"] = item['article']['click_count']  # 阅读数，数值
                # article_fields["trannum"] = ''  # 转发数，数值
                # article_fields["sharenum"] = item['ShareCount']  # 分享数，数值
                # article_fields["author"] = ''  # 作者，字符串
                article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                # article_fields["specialtopic"] = ''  # 是否是专题，数值（0标识不是，1标识是）
                # article_fields["topicid"] = bannerItem['contentId']  # 专题id，字符串
                # article_fields["topicTitle"] = bannerItem['contentId']  # 专题标题，字符串
                article_fields["newsType"] = "qxfast"  # 自己添加新闻类型
    except Exception as e:
        print(e)
    return article_fields


class CaiJingZaZhi(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://api.caijingmobile.com//setting/app-start"
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36",
            "Host": "api.caijingmobile.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        method = "get"
        data = {
            'device_info': '{"aaid":"x25193q8-yNs6-2ZHJ-J5c01m48","adid":"8f6bd215614b23b3","carrier":"0","density":"3.0","device_height":"1920","device_width":"1080","imei":"","language":"zh-CN","m_os_v":"10","mac":"58:02:03:04:05:1D","model":"ALP-AL00","vendor":"HUAWEI"}',
            'm_os': '1',
            'appVer': '401',
            'bundleId': 'cn.com.caijing.android',
            'channel': 'tencent',
            'udid': 'androididd722fc4a-fb94-4944-af54-5b62c93490fb',
            'uuid': 'd722fc4a-fb94-4944-af54-5b62c93490fb',
            'platform': '10',
            'network': 'wifi',
        }
        app_params1 = InitClass().app_params(url, headers, method, data=data)

        yield [app_params1]

    def analyze_channel(self, channelsres):
        print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            if "http://api.caijingmobile.com//setting/app-start" == k:
                channelList = json.loads(v)
                for channel in channelList['data']['appColumns']:
                    channelid = channel['columnId']
                    channelname = channel['title']
                    channelType = channel['type']
                    channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channelType)
                    channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []

        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channelType = channel.get("channeltype")
            if 1852 == channelid:  # 投资家接口
                print('付费内容：', channel)
            elif 336 == channelid:  # 专题接口
                url = "http://api.caijingmobile.com/news/special"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36",
                    "Accept": "application/vnd.cj.v1+json",
                    "Host": "api.caijingmobile.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                method = "get"
                data = {
                    'device_info': '{"aaid":"x25193q8-yNs6-2ZHJ-J5c01m48","adid":"8f6bd215614b23b3","carrier":"0","density":"3.0","device_height":"1920","device_width":"1080","imei":"","language":"zh-CN","m_os_v":"10","mac":"58:02:03:04:05:1D","model":"ALP-AL00","vendor":"HUAWEI"}',
                    'm_os': '1',
                    'last_id': '0',
                    'appVer': '401',
                    'bundleId': 'cn.com.caijing.android',
                    'channel': 'tencent',
                    'source_id': '40',
                    'udid': 'androididd722fc4a-fb94-4944-af54-5b62c93490fb',
                    'uuid': 'd722fc4a-fb94-4944-af54-5b62c93490fb',
                    'platform': '10',
                    'network': 'wifi',
                }
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                           channelid=channelid)
                articlelistsparams.append(articlelist_param)
            elif 1524 == channelid:  # 快讯接口
                url = "http://api.caijingmobile.com/flash/lists"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36",
                    "Host": "api.caijingmobile.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                data = {
                    'appVer': '401',
                    'bundleId': 'cn.com.caijing.android',
                    'channel': 'tencent',
                    'action': 'list',
                    'udid': 'androididd722fc4a-fb94-4944-af54-5b62c93490fb',
                    'uuid': 'd722fc4a-fb94-4944-af54-5b62c93490fb',
                    'platform': '10',
                    'network': 'wifi',
                }
                method = "get"
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, "快讯", data=data,
                                                                           channelid=-1)
                articlelistsparams.append(articlelist_param)
            else:
                url = "http://api.caijingmobile.com/news/article"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36",
                    "Accept": "application/vnd.cj.v6+json",
                    "Host": "api.caijingmobile.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                method = "get"
                data = {
                    'column_id': channelid,
                    'device_info': '{"aaid":"x25193q8-yNs6-2ZHJ-J5c01m48","adid":"8f6bd215614b23b3","carrier":"0","density":"3.0","device_height":"1920","device_width":"1080","imei":"","language":"zh-CN","m_os_v":"10","mac":"58:02:03:04:05:1D","model":"ALP-AL00","vendor":"HUAWEI"}',
                    'm_os': '1',
                    'last_id': '0',
                    'appVer': '401',
                    'bundleId': 'cn.com.caijing.android',
                    'channel': 'tencent',
                    'udid': 'androididd722fc4a-fb94-4944-af54-5b62c93490fb',
                    'uuid': 'd722fc4a-fb94-4944-af54-5b62c93490fb',
                    'platform': '10',
                    'network': 'wifi',
                }
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                           channelid=channelid)
                articlelistsparams.append(articlelist_param)

        url = "http://api.caijingmobile.com/caijinghao/video/recommend"
        headers = {
            "Accept": "application/vnd.cj.v1+json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "186",
            "Host": "api.caijingmobile.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.4.1",
        }
        data = {
            "last_id": "0",
            "appVer": "401",
            "bundleId": "cn.com.caijing.android",
            "channel": "tencent",
            "udid": "androididd722fc4a-fb94-4944-af54-5b62c93490fb",
            "uuid": "d722fc4a-fb94-4944-af54-5b62c93490fb",
            "platform": "10",
            "network": "wifi",
        }
        method = "post"
        articlelist_param = InitClass().articlelists_params_fields(url, headers, method, "视频-推荐", data=data,
                                                                   channelid=-2)
        articlelistsparams.append(articlelist_param)

        url = "http://api.caijingmobile.com/caijinghao/video/original"
        headers = {
            "Accept": "application/vnd.cj.v1+json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "186",
            "Host": "api.caijingmobile.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.4.1",
        }
        data = {
            "last_id": "0",
            "appVer": "401",
            "bundleId": "cn.com.caijing.android",
            "channel": "tencent",
            "udid": "androididd722fc4a-fb94-4944-af54-5b62c93490fb",
            "uuid": "d722fc4a-fb94-4944-af54-5b62c93490fb",
            "platform": "10",
            "network": "wifi",
        }
        method = "post"
        articlelist_param = InitClass().articlelists_params_fields(url, headers, method, "视频-视频", data=data,
                                                                   channelid=-3)
        articlelistsparams.append(articlelist_param)

        url = "http://api.caijingmobile.com/caijinghao/video/live"
        headers = {
            "Accept": "application/vnd.cj.v1+json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "186",
            "Host": "api.caijingmobile.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.4.1",
        }
        data = {
            "last_id": "0",
            "appVer": "401",
            "bundleId": "cn.com.caijing.android",
            "channel": "tencent",
            "udid": "androididd722fc4a-fb94-4944-af54-5b62c93490fb",
            "uuid": "d722fc4a-fb94-4944-af54-5b62c93490fb",
            "platform": "10",
            "network": "wifi",
        }
        method = "post"
        articlelist_param = InitClass().articlelists_params_fields(url, headers, method, "视频-直播", data=data,
                                                                   channelid=-4)
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
                    if 'data' in articleslists.keys():
                        if isinstance(articleslists['data'], list):
                            for item in articleslists['data']:
                                article_fields = setListNewsParam(channelname, channelid, 0, item)
                                articleparam = InitClass().article_list_fields()
                                articleparam["articelField"] = article_fields
                                articlesparams.append(articleparam)
                        elif isinstance(articleslists['data'], dict):
                            if 'focus_articles' in articleslists['data'].keys():  # banner
                                for item_top in articleslists['data']['focus_articles']:
                                    article_fields = setListNewsParam(channelname, channelid, 1, item_top)
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                            if 'normal_articles' in articleslists['data'].keys():
                                for item_article in articleslists['data']['normal_articles']:
                                    article_fields = setListNewsParam(channelname, channelid, 0, item_article)
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                            if 'focus' in articleslists['data'].keys():
                                for item_article in articleslists['data']['focus']:
                                    article_fields = setListNewsParam(channelname, channelid, 0, item_article)
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                            if 'origin' in articleslists['data'].keys():
                                for item_article in articleslists['data']['origin']:
                                    article_fields = setListNewsParam(channelname, channelid, 0, item_article)
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                            if 'live' in articleslists['data'].keys():
                                for item_article in articleslists['data']['live']:
                                    article_fields = setListNewsParam(channelname, channelid, 0, item_article)
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                            if 'origin_bottom' in articleslists['data'].keys():
                                for item_article in articleslists['data']['origin_bottom']:
                                    article_fields = setListNewsParam(channelname, channelid, 0, item_article)
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                            if 'notice' in articleslists['data'].keys():
                                for item_article in articleslists['data']['notice']:
                                    article_fields = setListNewsParam(channelname, channelid, 0, item_article)
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                            if 'living' in articleslists['data'].keys():
                                for item_article in articleslists['data']['living']:
                                    article_fields = setListNewsParam(channelname, channelid, 0, item_article)
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                            if 'splendid' in articleslists['data'].keys():
                                for item_article in articleslists['data']['splendid']:
                                    article_fields = setListNewsParam(channelname, channelid, 0, item_article)
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                            if 'review' in articleslists['data'].keys():
                                for item_article in articleslists['data']['review']:
                                    article_fields = setListNewsParam(channelname, channelid, 0, item_article)
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                            if 'focus_special_list' in articleslists['data'].keys():
                                for item_article in articleslists['data']['focus_special_list']:
                                    article_fields = setListNewsParam(channelname, channelid, 0, item_article)
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                            if 'normal_special_list' in articleslists['data'].keys():
                                for item_article in articleslists['data']['normal_special_list']:
                                    article_fields = setListNewsParam(channelname, channelid, 0, item_article)
                                    articleparam = InitClass().article_list_fields()
                                    articleparam["articelField"] = article_fields
                                    articlesparams.append(articleparam)
                        else:
                            print(articleslists)
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
            channelid = article_field.get('channelID')
            workerid = article_field.get('workerid')
            if 'qxdef' == newsType or 'qxvideo' == newsType:
                url = "http://api.caijingmobile.com/news/article/detail"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36",
                    "Accept": "application/vnd.cj.v2+json",
                    "ostype": "0",
                    "Host": "api.caijingmobile.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                method = "get"
                data = {
                    'column_id': channelid,
                    'appVer': '401',
                    'bundleId': 'cn.com.caijing.android',
                    'channel': 'tencent',
                    'id': workerid,
                    'udid': 'androididd722fc4a-fb94-4944-af54-5b62c93490fb',
                    'uuid': 'd722fc4a-fb94-4944-af54-5b62c93490fb',
                    'platform': '10',
                    'network': 'wifi',
                }
                articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                                 article_field=article_field)
                articleparams.append(articleparam)
            elif 'qxtopic' == newsType:
                url = "http://api.caijingmobile.com/news/article"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36",
                    "Accept": "application/vnd.cj.v5+json",
                    "Host": "api.caijingmobile.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                method = "get"
                data = {
                    # {"aaid":"x25193q8-yNs6-2ZHJ-J5c01m48","adid":"8f6bd215614b23b3","carrier":"0","density":"3.0","device_height":"1920","device_width":"1080","imei":"null747167817965698","language":"zh-CN","m_os_v":"10","mac":"58:02:03:04:05:1D","model":"ALP-AL00","vendor":"HUAWEI"}
                    'device_info': '{"aaid":"x25193q8-yNs6-2ZHJ-J5c01m48","adid":"8f6bd215614b23b3","carrier":"0","density":"3.0","device_height":"1920","device_width":"1080","imei":"","language":"zh-CN","m_os_v":"10","mac":"58:02:03:04:05:1D","model":"ALP-AL00","vendor":"HUAWEI"}',
                    'm_os': '1',
                    'special_id': workerid,
                    'last_id': '',
                    'appVer': '401',
                    'bundleId': 'cn.com.caijing.android',
                    'channel': 'tencent',
                    'udid': 'androididd722fc4a-fb94-4944-af54-5b62c93490fb',
                    'uuid': 'd722fc4a-fb94-4944-af54-5b62c93490fb',
                    'platform': '10',
                    'network': 'wifi',
                }
                articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                                 article_field=article_field)
                articleparams.append(articleparam)

            else:
                print("没有详情接口:", article)
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
                    if 'qxtopic' == newsType:
                        topicFields = InitClass().topic_fields()
                        topicFields["topicID"] = fields['workerid']  # 专题id，app内唯一标识
                        topicFields["platformName"] = appname  # 平台名字（app名字）
                        # topicFields["platformID"] = fields['workerid']
                        topicFields["channelName"] = fields['channelname']  # 频道名字
                        topicFields["channelID"] = fields['channelID']  # 频道id
                        # topicFields["topicUrl"] = fields['url']  # topicUrl
                        topicFields["title"] = fields['title']
                        topicFields["digest"] = fields['content']  # 简介，摘要
                        topicFields["topicCover"] = fields['articlecovers']
                        # topicFields["pubTime"] = fields['workerid']  # 时间戳
                        topicFields["articleNum"] = fields['commentnum']  # 专题内的文章数量
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
                        topicFields["updateTime"] = fields['updatetime']
                        topicItem = []
                        if 'focus_articles' in contentJson['data'].keys() and len(
                                contentJson['data']['focus_articles']):
                            topicItem += contentJson['data']['focus_articles']
                        if 'normal_articles' in contentJson['data'].keys() and len(
                                contentJson['data']['normal_articles']):
                            topicItem += contentJson['data']['normal_articles']

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
                        # fields["url"] = contentJson['source_url']  # 分享的网址，字符串
                        # fields["workerid"] = item['ctId']  # 文章id，字符串
                        # fields["title"] = item['title']  # 文章标题，字符串
                        fields["content"] = contentJson['data']['article']['content']  # 文章内容，字符串
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
                if 'article' in item.keys():
                    if 'live' in item.keys():
                        if item['live']:
                            # article_fields["channelType"] = channel_type  # 频道type，字符串
                            article_fields["url"] = item['article']['share_url']  # 分享的网址，字符串
                            article_fields["workerid"] = item['article']['id']  # 文章id，字符串
                            article_fields["title"] = item['article']['title']  # 文章标题，字符串
                            article_fields["content"] = item['live']['web_url']  # 文章内容，字符串
                            imgList = []
                            for img in item['article']['thumb_images']:
                                imgList.append(f"{item['article']['thumb_path']}{img}")
                            article_fields["articlecovers"] = imgList  # 列表封面，数组
                            # article_fields["images"] = ''  # 正文图片，数组
                            # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                            # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
                            # article_fields["width"] = ''  # 视频宽，字符串
                            # article_fields["height"] = ''  # 视频高，字符串
                            # article_fields["source"] = item['SourceUrl']  # 文章来源，字符串
                            article_fields["pubtime"] = item['article']['publish_time']  # 发布时间，时间戳（毫秒级，13位）
                            # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                            article_fields["updatetime"] = item['article']['updated_time']  # 更新时间，时间戳（毫秒级，13位）
                            # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                            # article_fields["playnum"] = ''  # 播放数，数值
                            # article_fields["commentnum"] = item['CommentCount']  # 评论数，数值
                            article_fields["readnum"] = item['article']['click_count']  # 阅读数，数值
                            # article_fields["trannum"] = ''  # 转发数，数值
                            # article_fields["sharenum"] = item['ShareCount']  # 分享数，数值
                            # article_fields["author"] = ''  # 作者，字符串
                            # article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                            article_fields["specialtopic"] = 1  # 是否是专题，数值（0标识不是，1标识是）
                            article_fields["topicid"] = topicId  # 专题id，字符串
                            article_fields["topicTitle"] = topicTitle  # 专题标题，字符串
                            article_fields["newsType"] = "qxlive"  # 自己添加新闻类型
                        else:
                            # article_fields["channelType"] = channel_type  # 频道type，字符串
                            article_fields["url"] = item['article']['share_url']  # 分享的网址，字符串
                            article_fields["workerid"] = item['article']['id']  # 文章id，字符串
                            article_fields["title"] = item['article']['title']  # 文章标题，字符串
                            # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
                            imgList = []
                            for img in item['article']['thumb_images']:
                                imgList.append(f"{item['article']['thumb_path']}{img}")
                            article_fields["articlecovers"] = imgList  # 列表封面，数组
                            # article_fields["images"] = ''  # 正文图片，数组
                            # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                            # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
                            # article_fields["width"] = ''  # 视频宽，字符串
                            # article_fields["height"] = ''  # 视频高，字符串
                            # article_fields["source"] = item['SourceUrl']  # 文章来源，字符串
                            article_fields["pubtime"] = item['article']['publish_time']  # 发布时间，时间戳（毫秒级，13位）
                            # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                            article_fields["updatetime"] = item['article']['updated_time']  # 更新时间，时间戳（毫秒级，13位）
                            # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                            # article_fields["playnum"] = ''  # 播放数，数值
                            # article_fields["commentnum"] = item['CommentCount']  # 评论数，数值
                            article_fields["readnum"] = item['article']['click_count']  # 阅读数，数值
                            # article_fields["trannum"] = ''  # 转发数，数值
                            # article_fields["sharenum"] = item['ShareCount']  # 分享数，数值
                            # article_fields["author"] = ''  # 作者，字符串
                            # article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                            article_fields["specialtopic"] = 1  # 是否是专题，数值（0标识不是，1标识是）
                            article_fields["topicid"] = topicId  # 专题id，字符串
                            article_fields["topicTitle"] = topicTitle  # 专题标题，字符串
                            article_fields["newsType"] = "qxvideo"  # 自己添加新闻类型
                    else:
                        # article_fields["channelType"] = channel_type  # 频道type，字符串
                        article_fields["url"] = item['article']['share_url']  # 分享的网址，字符串
                        article_fields["workerid"] = item['article']['id']  # 文章id，字符串
                        article_fields["title"] = item['article']['title']  # 文章标题，字符串
                        # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
                        imgList = []
                        for img in item['article']['thumb_images']:
                            imgList.append(f"{item['article']['thumb_path']}{img}")
                        article_fields["articlecovers"] = imgList  # 列表封面，数组
                        # article_fields["images"] = ''  # 正文图片，数组
                        # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                        # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
                        # article_fields["width"] = ''  # 视频宽，字符串
                        # article_fields["height"] = ''  # 视频高，字符串
                        # article_fields["source"] = item['SourceUrl']  # 文章来源，字符串
                        article_fields["pubtime"] = item['article']['publish_time']  # 发布时间，时间戳（毫秒级，13位）
                        # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                        article_fields["updatetime"] = item['article']['updated_time']  # 更新时间，时间戳（毫秒级，13位）
                        # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                        # article_fields["playnum"] = ''  # 播放数，数值
                        # article_fields["commentnum"] = item['CommentCount']  # 评论数，数值
                        article_fields["readnum"] = item['article']['click_count']  # 阅读数，数值
                        # article_fields["trannum"] = ''  # 转发数，数值
                        # article_fields["sharenum"] = item['ShareCount']  # 分享数，数值
                        # article_fields["author"] = ''  # 作者，字符串
                        # article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                        article_fields["specialtopic"] = 1  # 是否是专题，数值（0标识不是，1标识是）
                        article_fields["topicid"] = topicId  # 专题id，字符串
                        article_fields["topicTitle"] = topicTitle  # 专题标题，字符串
                        article_fields["newsType"] = "qxdef"  # 自己添加新闻类型
                elif 'special' in item.keys():
                    # article_fields["channelType"] = channel_type  # 频道type，字符串
                    # article_fields["url"] = item['special']['share_url']  # 分享的网址，字符串
                    article_fields["workerid"] = item['special']['id']  # 文章id，字符串
                    article_fields["title"] = item['special']['title']  # 文章标题，字符串
                    article_fields["content"] = item['special']['description']  # 文章内容，字符串
                    imgList = []
                    for img in item['special']['thumbnails']:
                        imgList.append(img)
                    article_fields["articlecovers"] = imgList  # 列表封面，数组
                    # article_fields["images"] = ''  # 正文图片，数组
                    # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                    # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
                    # article_fields["width"] = ''  # 视频宽，字符串
                    # article_fields["height"] = ''  # 视频高，字符串
                    # article_fields["source"] = item['SourceUrl']  # 文章来源，字符串
                    # article_fields["pubtime"] = item['special']['publish_time']  # 发布时间，时间戳（毫秒级，13位）
                    # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                    article_fields["updatetime"] = item['special']['icon_update_time']  # 更新时间，时间戳（毫秒级，13位）
                    # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                    # article_fields["playnum"] = ''  # 播放数，数值
                    article_fields["commentnum"] = item['special']['article_count']  # 评论数，数值
                    # article_fields["readnum"] = item['special']['click_count']  # 阅读数，数值
                    # article_fields["trannum"] = ''  # 转发数，数值
                    # article_fields["sharenum"] = item['ShareCount']  # 分享数，数值
                    # article_fields["author"] = ''  # 作者，字符串
                    # article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                    article_fields["specialtopic"] = 1  # 是否是专题，数值（0标识不是，1标识是）
                    article_fields["topicid"] = topicId  # 专题id，字符串
                    article_fields["topicTitle"] = topicTitle  # 专题标题，字符串
                    article_fields["newsType"] = "qxtopic"  # 自己添加新闻类型
                else:
                    if 'live_status' in item.keys():
                        # article_fields["channelType"] = channel_type  # 频道type，字符串
                        # article_fields["url"] = item['share_url']  # 分享的网址，字符串
                        article_fields["workerid"] = item['id']  # 文章id，字符串
                        article_fields["title"] = item['title']  # 文章标题，字符串
                        article_fields["content"] = item['web_url']  # 文章内容，字符串
                        imgList = []
                        if 'cover_path' in item.keys() and item['cover_path']:
                            imgList.append(item['cover_path'])
                        article_fields["articlecovers"] = imgList  # 列表封面，数组
                        # article_fields["images"] = ''  # 正文图片，数组
                        # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                        # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
                        # article_fields["width"] = ''  # 视频宽，字符串
                        # article_fields["height"] = ''  # 视频高，字符串
                        # article_fields["source"] = item['SourceUrl']  # 文章来源，字符串
                        # article_fields["pubtime"] = item['ctime']  # 发布时间，时间戳（毫秒级，13位）
                        # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                        # article_fields["updatetime"] = item['article']['updated_time']  # 更新时间，时间戳（毫秒级，13位）
                        # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                        # article_fields["playnum"] = ''  # 播放数，数值
                        # article_fields["commentnum"] = item['CommentCount']  # 评论数，数值
                        # article_fields["readnum"] = item['article']['click_count']  # 阅读数，数值
                        # article_fields["trannum"] = ''  # 转发数，数值
                        # article_fields["sharenum"] = item['ShareCount']  # 分享数，数值
                        # article_fields["author"] = ''  # 作者，字符串
                        # article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                        article_fields["specialtopic"] = 1  # 是否是专题，数值（0标识不是，1标识是）
                        article_fields["topicid"] = topicId  # 专题id，字符串
                        article_fields["topicTitle"] = topicTitle  # 专题标题，字符串
                        article_fields["newsType"] = "qxlivenotice"  # 自己添加新闻类型
                    else:
                        # article_fields["channelType"] = channel_type  # 频道type，字符串
                        article_fields["url"] = item['share_url']  # 分享的网址，字符串
                        article_fields["workerid"] = item['id']  # 文章id，字符串
                        # article_fields["title"] = item['title']  # 文章标题，字符串
                        article_fields["content"] = item['content']  # 文章内容，字符串
                        # article_fields["articlecovers"] = imgList  # 列表封面，数组
                        # article_fields["images"] = ''  # 正文图片，数组
                        # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                        # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
                        # article_fields["width"] = ''  # 视频宽，字符串
                        # article_fields["height"] = ''  # 视频高，字符串
                        # article_fields["source"] = item['SourceUrl']  # 文章来源，字符串
                        article_fields["pubtime"] = item['ctime']  # 发布时间，时间戳（毫秒级，13位）
                        # article_fields["createtime"] = item['createDate']  # 创建时间，时间戳（毫秒级，13位）
                        # article_fields["updatetime"] = item['article']['updated_time']  # 更新时间，时间戳（毫秒级，13位）
                        # article_fields["likenum"] = ''  # 点赞数（喜欢数），数值
                        # article_fields["playnum"] = ''  # 播放数，数值
                        # article_fields["commentnum"] = item['CommentCount']  # 评论数，数值
                        # article_fields["readnum"] = item['article']['click_count']  # 阅读数，数值
                        # article_fields["trannum"] = ''  # 转发数，数值
                        # article_fields["sharenum"] = item['ShareCount']  # 分享数，数值
                        # article_fields["author"] = ''  # 作者，字符串
                        # article_fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                        article_fields["specialtopic"] = 1  # 是否是专题，数值（0标识不是，1标识是）
                        article_fields["topicid"] = topicId  # 专题id，字符串
                        article_fields["topicTitle"] = topicTitle  # 专题标题，字符串
                        article_fields["newsType"] = "qxfast"  # 自己添加新闻类型
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
    appspider = CaiJingZaZhi("财经杂志")
    appspider.run()
