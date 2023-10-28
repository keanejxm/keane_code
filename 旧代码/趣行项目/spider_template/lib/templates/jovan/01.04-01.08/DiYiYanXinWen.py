# -*- encoding:utf-8 -*-
"""
@功能:湖北日报解析模板
@AUTHOR：jovan
@文件名：HuBeiRiBao.py
@时间：2020年12月22日 15:58:24
"""
from datetime import datetime
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
        if 'docid' in item.keys():
            # article_fields["url"] = url  # 分享的网址，字符串
            article_fields["workerid"] = item['docid']  # 文章id，字符串
            article_fields["title"] = item['title']  # 文章标题，字符串
            # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
            imgs = []
            if item['thumbnail']:
                imgs.append(item['thumbnail'])
            article_fields["articlecovers"] = imgs  # 列表封面，数组
            # article_fields["images"] = ''  # 正文图片，数组
            videos = []
            if 'videos' in item.keys() and item['videos']:
                videos.append(item['videos'])
            article_fields["videos"] = videos  # 视频地址，数组
            # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
            # article_fields["width"] = ''  # 视频宽，字符串
            # article_fields["height"] = ''  # 视频高，字符串
            article_fields["source"] = item['source']  # 文章来源，字符串
            article_fields["pubtime"] = InitClass().date_time_stamp(item['pushtime'])  # 发布时间，时间戳（毫秒级，13位）
            if 'ctime' in item.keys():
                article_fields["createtime"] = item['ctime']  # 创建时间，时间戳（毫秒级，13位）
            if 'utime' in item.keys():
                article_fields["updatetime"] = item['utime']  # 更新时间，时间戳（毫秒级，13位）
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
            article_fields["newsType"] = "qxdef"  # 自己添加新闻类型

        elif '_id' in item.keys():
            if 'roomName' in item.keys():
                # article_fields["url"] = url  # 分享的网址，字符串
                article_fields["workerid"] = item['_id']  # 文章id，字符串
                article_fields["title"] = item['roomName']  # 文章标题，字符串
                # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
                imgs = []
                if item['listImg']:
                    imgs.append(item['listImg'])
                article_fields["articlecovers"] = imgs  # 列表封面，数组
                # article_fields["images"] = ''  # 正文图片，数组
                # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
                # article_fields["width"] = ''  # 视频宽，字符串
                # article_fields["height"] = ''  # 视频高，字符串
                # article_fields["source"] = ''  # 文章来源，字符串
                # article_fields["pubtime"] = ''  # 发布时间，时间戳（毫秒级，13位）
                article_fields["createtime"] = InitClass().date_time_stamp(item['ctime'])  # 创建时间，时间戳（毫秒级，13位）
                # article_fields["updatetime"] = item['utimeStamp']  # 更新时间，时间戳（毫秒级，13位）
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
                article_fields["newsType"] = "qxlive"  # 自己添加新闻类型
            elif 'name' in item.keys():
                # article_fields["url"] = url  # 分享的网址，字符串
                article_fields["workerid"] = item['_id']  # 文章id，字符串
                article_fields["title"] = item['name']  # 文章标题，字符串
                # article_fields["content"] = item['ctImgUrl']  # 文章内容，字符串
                imgs = []
                if item['thumbnailUrl']:
                    imgs.append(item['thumbnailUrl'])
                article_fields["articlecovers"] = imgs  # 列表封面，数组
                # article_fields["images"] = ''  # 正文图片，数组
                # article_fields["videos"] = [item['videoUrl']]  # 视频地址，数组
                # article_fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
                # article_fields["width"] = ''  # 视频宽，字符串
                # article_fields["height"] = ''  # 视频高，字符串
                # article_fields["source"] = ''  # 文章来源，字符串
                # article_fields["pubtime"] = ''  # 发布时间，时间戳（毫秒级，13位）
                article_fields["createtime"] = item['ctimeStamp']  # 创建时间，时间戳（毫秒级，13位）
                # article_fields["updatetime"] = item['utimeStamp']  # 更新时间，时间戳（毫秒级，13位）
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
                article_fields["newsType"] = "qxtopic"  # 自己添加新闻类型
            else:
                print(item)
        else:
            print(item)

    except Exception as e:
        print(e)
    return article_fields


class DiYiYanXinWen(Appspider):

    @staticmethod
    def get_app_params():
        url1 = "https://cqxyinterface.cbgcloud.com/api/xy/toc/v1/queryPageAllByMenuId"
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; LIO-AL00 Build/HUAWEILIO-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36",
            "Cache-Control": "max-age=60, max-stale=0",
            "Host": "cqxyinterface.cbgcloud.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "If-Modified-Since": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
        }
        method = "get"
        data = {
            "appCode": "FABU_YUNSHI",
            "companyId": "cqxwzx",
            "userId": "353615334688244cqxwzx",
            "productId": "6B1BEE01515143AFAF290F6044E54A89",
            "serviceCode": "YUNSHI_XSGL",
            "menuId": "FQFOMFT53060O7BRXXGQWF0V1VZXS5ID",
        }

        app_params1 = InitClass().app_params(url1, headers, method, data=data)

        yield [app_params1]

    def analyze_channel(self, channelsres):
        print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            if "https://cqxyinterface.cbgcloud.com/api/xy/toc/v1/queryPageAllByMenuId" == k:
                channelList = json.loads(v)
                # for channel in channelList['data'][0:1]:
                for channel in channelList['data']:
                    channelid = channel['pageId']
                    channelname = channel['name']
                    channeltype = channel['remark']
                    channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channeltype)
                    channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = "https://cqxyinterface.cbgcloud.com/api/xy/toc/v2/queryDatas"
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; LIO-AL00 Build/HUAWEILIO-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36",
            "Cache-Control": "max-age=60, max-stale=0",
            "Host": "cqxyinterface.cbgcloud.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "If-Modified-Since": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
        }
        method = "get"
        data = {}
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")
            companyId = "cqxwzx"
            productId = "6B1BEE01515143AFAF290F6044E54A89"
            pageId = channelid
            if channeltype:
                # 'new_product+cqwspd+91FD5C0F280B4738BF6E8E896DDA46D3+5f03ddef7d40081d987243bc'
                list_temp = channeltype.split("+")
                companyId = list_temp[1]
                productId = list_temp[2]
                pageId = list_temp[3]
                channel["channelid"] = pageId
            url_temp = f"https://cqxyinterface.cbgcloud.com/api/xy/toc/v1/queryModules?" \
                       f"appCode=FABU_YUNSHI&companyId={companyId}&userId=357716466646247cqxwzx&" \
                       f"productId={productId}&serviceCode=YUNSHI_XSGL&pageId={pageId}"
            headers_temp = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; LIO-AL00 Build/HUAWEILIO-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36",
                "Cache-Control": "max-age=60, max-stale=0",
                "Host": "cqxyinterface.cbgcloud.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "If-Modified-Since": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
            }
            modules = ""
            res_temp = requests.get(url_temp, headers=headers_temp).content.decode()
            res_info_temp = json.loads(json.dumps(json.loads(res_temp, strict=False), indent=4, ensure_ascii=False))

            for res_temp in res_info_temp['data']:
                modules += f"{res_temp['_id']}_1_10,"
            if modules:
                modules = modules.strip(",");
            data = {
                "appCode": "FABU_YUNSHI",
                "companyId": companyId,
                "userId": "353615334688244cqxwzx",
                "productId": productId,
                "serviceCode": "YUNSHI_XSGL",
                "modules": modules,
                "pageId": pageId,
            }
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                       channelid=pageId, channeltype=res_info_temp)
            articlelistsparams.append(articlelist_param)
        yield articlelistsparams

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            list_sort_data = articleslistres.get("channelType")
            articleslists = articleslistres.get("channelres")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    print(articleslists)

                    for list_sort in list_sort_data['data']:
                        data_key = list_sort['_id']
                        if 'docids' in list_sort.keys():
                            index = 0
                            data_docs = list_sort['docids']
                            if 'data' in articleslists.keys() and \
                                    isinstance(articleslists['data'], dict) and \
                                    data_key in articleslists['data'].keys():
                                data_item = articleslists['data'][data_key]
                                if 'docs' in data_item.keys() and isinstance(data_item['docs'], dict):
                                    if 'results' in data_item['docs'].keys() and isinstance(
                                            data_item['docs']['results'], list):
                                        for item in data_item['docs']['results']:
                                            if 'docid' in item.keys() and item['docid'] in data_docs:
                                                article_fields = setListNewsParam(channelname, channelid,
                                                                                  1 if index == 0 else 0, item)
                                                articleparam = InitClass().article_list_fields()
                                                articleparam["articelField"] = article_fields
                                                articlesparams.append(articleparam)
                                            elif '_id' in item.keys() and item['_id'] in data_docs:
                                                article_fields = setListNewsParam(channelname, channelid,
                                                                                  1 if index == 0 else 0, item)
                                                articleparam = InitClass().article_list_fields()
                                                articleparam["articelField"] = article_fields
                                                articlesparams.append(articleparam)
                                            else:
                                                print(item)
                                    else:
                                        print(data_item)  # 判断不出啥类型
                                else:
                                    print(data_item)
                            else:
                                print(articleslists)
                            index += 1
                        else:
                            print('自定义图片', list_sort)  # 广告，外链
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
            newsType = article_field.get('newsType')
            if "qxdef" == newsType:
                url = f"https://cqxyinterface.cbgcloud.com/api/xy/content/v1/queryContentByDocId?" \
                      f"appCode=FABU_YUNSHI&companyId=cqxwzx&userId=357716466646247cqxwzx&" \
                      f"productId=6B1BEE01515143AFAF290F6044E54A89&serviceCode=YUNSHI_XSGL"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10; LIO-AL00 Build/HUAWEILIO-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36",
                    "Cache-Control": "max-age=60, max-stale=0",
                    "Content-Type": "application/json; charset=utf-8",
                    "Content-Length": "50",
                    "Host": "cqxyinterface.cbgcloud.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                method = "post"
                articlejson = {
                    "docid": workerid,
                    "isNew": "yes",
                }
                articleparam = InitClass().article_params_fields(url, headers, method, article_field=article_field,
                                                                 articlejson=articlejson)
                articleparams.append(articleparam)
            elif "qxlive" == newsType:
                url = f"https://cqxyinterface.cbgcloud.com/api/xy/live/v1/getLiveById?" \
                      f"appCode=FABU_YUNSHI&companyId=cqxwzx&userId=357716466646247cqxwzx&" \
                      f"productId=6B1BEE01515143AFAF290F6044E54A89&serviceCode=YUNSHI_XSGL"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10; LIO-AL00 Build/HUAWEILIO-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36",
                    "Cache-Control": "max-age=60, max-stale=0",
                    "Content-Type": "application/json; charset=utf-8",
                    "Content-Length": "50",
                    "Host": "cqxyinterface.cbgcloud.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                }
                method = "post"
                articlejson = {
                    "accessToken": "accessToken",
                    "id": workerid,
                    "timeStamp": str(int(time.time())),
                }
                articleparam = InitClass().article_params_fields(url, headers, method, article_field=article_field,
                                                                 articlejson=articlejson)
                articleparams.append(articleparam)
            elif "qxtopic" == newsType:
                url = f"https://cqxyinterface.cbgcloud.com/api/xy/toc/v1/querySpecialById?" \
                      f"appCode=FABU_YUNSHI&companyId=cqxwzx&userId=357716466646247cqxwzx&" \
                      f"productId=6B1BEE01515143AFAF290F6044E54A89&serviceCode=YUNSHI_XSGL&id={workerid}"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10; LIO-AL00 Build/HUAWEILIO-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36",
                    "Cache-Control": "max-age=60, max-stale=0",
                    "Host": "cqxyinterface.cbgcloud.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "If-Modified-Since": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                }
                method = "get"
                articleparam = InitClass().article_params_fields(url, headers, method, article_field=article_field)
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
                    print(contentJson)
                    if "qxdef" == newsType:
                        fields["appname"] = appname  # 应用名称，字符串
                        # fields["channelname"] = channelname  # 频道名称，字符串
                        # fields["channelID"] = channelid  # 频道id，字符串
                        # fields["channelType"] = channel_type  # 频道type，字符串
                        # fields["url"] = contentJson['source_url']  # 分享的网址，字符串
                        # fields["workerid"] = item['ctId']  # 文章id，字符串
                        # fields["title"] = item['title']  # 文章标题，字符串
                        fields["content"] = contentJson['data']['srcontent']  # 文章内容，字符串
                        # fields["articlecovers"] = imgList  # 列表封面，数组
                        fields["images"] = InitClass.get_images(fields["content"])  # 正文图片，数组
                        videos = []
                        if 'videos' in contentJson['data'].keys():
                            for video in contentJson['data']['videos']:
                                if 'vurl' in video.keys() and video['vurl']:
                                    videos.append(video['vurl'])
                        fields["videos"] = videos  # 视频地址，数组
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
                    elif "qxlive" == newsType:
                        fields["appname"] = appname  # 应用名称，字符串
                        # fields["channelname"] = channelname  # 频道名称，字符串
                        # fields["channelID"] = channelid  # 频道id，字符串
                        # fields["channelType"] = channel_type  # 频道type，字符串
                        # fields["url"] = contentJson['source_url']  # 分享的网址，字符串
                        # fields["workerid"] = item['ctId']  # 文章id，字符串
                        # fields["title"] = item['title']  # 文章标题，字符串
                        # fields["content"] = contentJson['data']['srcontent']  # 文章内容，字符串
                        # fields["articlecovers"] = imgList  # 列表封面，数组
                        # fields["images"] = InitClass.get_images(fields["content"])  # 正文图片，数组
                        videos = []
                        for video in contentJson['data']['lives']:
                            if 'stream' in video.keys() and len(video['stream']):
                                videos.append(video['stream'])
                            if 'backUrl' in video.keys() and len(video['backUrl']):
                                videos.append(video['backUrl'])
                        fields["videos"] = videos  # 视频地址，数组
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
                    elif "qxtopic" == newsType:
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
                        url = f"https://cqxyinterface.cbgcloud.com/api/xy/toc/v1/querySpecialDocList?" \
                              f"appCode=FABU_YUNSHI&companyId=cqxwzx&userId=357716466646247cqxwzx&" \
                              f"productId=6B1BEE01515143AFAF290F6044E54A89&serviceCode=YUNSHI_XSGL&" \
                              f"pageNum=10&id={topicFields['topicID']}&currentPage=1"
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Linux; Android 10; LIO-AL00 Build/HUAWEILIO-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36",
                            "Cache-Control": "max-age=60, max-stale=0",
                            "Host": "cqxyinterface.cbgcloud.com",
                            "Connection": "Keep-Alive",
                            "Accept-Encoding": "gzip",
                            "If-Modified-Since": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                        }
                        res_temp = requests.get(url, headers=headers).content.decode()
                        res_info_temp = json.loads(
                            json.dumps(json.loads(res_temp, strict=False), indent=4, ensure_ascii=False))
                        for topicnews in res_info_temp['data']['results']:
                            fields = InitClass().article_fields()
                            fields["channelname"] = topicFields["channelName"]  # 频道名称，字符串
                            fields["channelID"] = topicFields["channelID"]  # 频道id，字符串
                            # fields["channelType"] = channel_type  # 频道type，字符串
                            # fields["url"] = url  # 分享的网址，字符串
                            fields["workerid"] = topicnews['_id']  # 文章id，字符串
                            fields["title"] = topicnews['title']  # 文章标题，字符串
                            fields["content"] = topicnews['srcontent']  # 文章内容，字符串
                            imgs = []
                            if topicnews['thumbnail']:
                                imgs.append(topicnews['thumbnail'])
                            fields["articlecovers"] = imgs  # 列表封面，数组
                            fields["images"] = InitClass.get_images(fields["content"])  # 正文图片，数组
                            videos = []
                            if 'videos' in topicnews.keys():
                                for video in topicnews['videos']:
                                    if 'vurl' in video.keys() and len(video['vurl']):
                                        videos.append(video['vurl'])
                            fields["videos"] = videos  # 视频地址，数组
                            # fields["videocover"] = [item['videoPoster']]  # 视频封面，数组
                            # fields["width"] = ''  # 视频宽，字符串
                            # fields["height"] = ''  # 视频高，字符串
                            fields["source"] = topicnews['source']  # 文章来源，字符串
                            fields["pubtime"] = InitClass().date_time_stamp(
                                topicnews['pushtime'])  # 发布时间，时间戳（毫秒级，13位）
                            if 'ctime' in topicnews.keys():
                                fields["createtime"] = topicnews['ctime']  # 创建时间，时间戳（毫秒级，13位）
                            if 'utime' in topicnews.keys():
                                fields["updatetime"] = topicnews['utime']  # 更新时间，时间戳（毫秒级，13位）
                            # fields["likenum"] = ''  # 点赞数（喜欢数），数值
                            # fields["playnum"] = ''  # 播放数，数值
                            # fields["commentnum"] = item['commentNum']  # 评论数，数值
                            # fields["readnum"] = item['realRead']  # 阅读数，数值
                            # fields["trannum"] = ''  # 转发数，数值
                            # fields["sharenum"] = ''  # 分享数，数值
                            # fields["author"] = ''  # 作者，字符串
                            # fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                            fields["specialtopic"] = 1  # 是否是专题，数值（0标识不是，1标识是）
                            fields["topicid"] = topicFields["topicID"]  # 专题id，字符串
                            fields["topicTitle"] = topicFields["title"]  # 专题标题，字符串
                            print(json.dumps(fields, indent=4, ensure_ascii=False))
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
    appspider = DiYiYanXinWen("第一眼新闻")
    appspider.run()
