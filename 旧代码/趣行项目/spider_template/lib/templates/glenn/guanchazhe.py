# -*- encoding:utf-8 -*-
import json
import logging
import datetime
from glenn.appspider_m import Appspider
from glenn.initclass import InitClass


def getInterval2Timestamp(timeStr=""):
    timeFormat = {
        "year": ["年前", "年"],
        "month": ["月前", "月"],
        "day": ["天前", "天"],
        "hour": ["小时前", "小时", "时"],
        "minute": ["分前", '分钟前', "分钟", "分"],
        "second": ["秒前", "秒"],
        # "microsecond": [],
        "timenow": ["刚刚", "一会"],
    }
    timeNow = datetime.datetime.now()  # 获取当前时间
    timeNow.strftime("%Y/%m/%d/ %H:%M:%S")  # 格式化当前时间
    timeStr = "".join(timeStr.split())  # 去除全部空格
    for k, v in timeFormat.items():
        for item in v:
            if item in timeStr:
                index = timeStr.rfind(item)
                timeStr = timeStr[0:index]
                if timeStr.isdecimal():
                    if "year" == k:
                        timeNow = timeNow.replace(year=timeNow.year - int(timeStr))
                    elif "month" == k:
                        timeNow = timeNow.replace(month=timeNow.month - int(timeStr))
                    elif "day" == k:
                        timeNow = timeNow.replace(day=timeNow.day - int(timeStr))
                    elif "hour" == k:
                        timeNow = timeNow.replace(hour=timeNow.hour - int(timeStr))
                    elif "minute" == k:
                        timeNow = timeNow.replace(minute=timeNow.minute - int(timeStr))
                    elif "second" == k:
                        timeNow = timeNow.replace(second=timeNow.second - int(timeStr))
                    elif "timenow" == k:
                        timeNow = timeNow
                    # timeNow = timeNow.replace(k=timeNow.k - int(timeStr))
                    print(timeNow)
                    print(int(timeNow.timestamp()))
    print(int(timeNow.timestamp()))
    return int(timeNow.timestamp())


class GuanChaZhe(Appspider):

    @staticmethod
    def analyze_channel():
        channelsparams = []
        channelslists = [
            {'id': '0', 'type': '', 'name': '要闻'},
            {'id': '1', 'type': '', 'name': '时评'},
            {'id': '2', 'type': '', 'name': '朋友圈'},
            {'id': '3', 'type': '', 'name': '滚动'},
            {'id': '5', 'type': 'CaiJing', 'name': '财经'},
            {'id': '5', 'type': 'ChanJing', 'name': '产经'},
            {'id': '5', 'type': 'GongYe·KeJi', 'name': '科技'},
            {'id': '5', 'type': 'qiche', 'name': '汽车'},
            {'id': '5', 'type': 'GuoJi·ZhanLue', 'name': '国际'},
            {'id': '5', 'type': 'JunShi', 'name': '军事'},
            {'id': '4', 'type': 'XinShiDai', 'name': '新时代'},
            {'id': '10', 'type': '', 'name': '视频'}
        ]
        for channel in channelslists:
            channelname = channel["name"]
            channelid = channel["id"]
            channeltype = channel['type']
            channelparam = InitClass().channel_fields(channelid, channelname, channeltype=channeltype)
            channelsparams.append(channelparam)
        yield channelsparams

    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []
        url = ""
        headers = {
            "Host": "app.guancha.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; VTR-AL00 Build/HUAWEIVTR-AL00)"
        }
        data = {}
        method = 'get'
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            if channelname == '要闻':
                url = "https://app.guancha.cn/news/yaowen-new.json"  # 要闻请求接口
                data = {
                    "v": "202012141",
                    "pageNo": "1",
                    "device": "android"
                }
            elif channelname == '视频':
                url = "https://app.guancha.cn/video/list"  # 视频请求接口
                data = {
                    "v": "202012141",
                    "pageNo": "1",
                    "access-token": '',
                    "device": "android"
                }
            else:
                url = "https://app.guancha.cn/news/common-list.json"  # 其他请求接口
                data = {
                    "v": "202012141",
                    "type": channeltype,
                    "id": channelid,
                    "pageNo": "1",
                    "device": "android"
                }
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid=channelid, data=data,
                                                                       channeltype=channeltype)
            articlelistsparams.append(articlelist_param)
            break
        yield articlelistsparams

    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            channel_type = articleslistres.get("channeltype")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    for article in articleslists["data"]["items"]:
                        article_fields = InitClass().article_fields()
                        articleparam = InitClass().article_list_fields()
                        print(article)
                        # 获取文章列表内的有用信息
                        article_id = article["id"]
                        article_title = article["title"]
                        article_type = ""
                        share_url = ""
                        pubtime = ""
                        if channelname == '视频':
                            article_type = article["video_sign"]
                            share_url = article["share_url"]
                            pubtime = article["published_at"]
                            article_covers = list()
                            article_cover = article["big_pic"]
                            article_covers.append(article_cover)
                            # 采集视频
                            try:
                                videocovers = list()
                                videocover = article["big_pic"]
                                videocovers.append(videocover)
                                videoss = article["video"]["data"]
                                videos = list()
                                for video in videoss:
                                    videos.append(video["url"])
                                article_fields["videos"] = videos
                                article_fields["videocovers"] = videocovers
                            except Exception as e:
                                logging.info(f"此新闻无视频{e}")
                        else:
                            article_type = article["news_type"]
                            share_url = article["url"]
                            pubtime = article["news_time"]
                            article_covers = list()
                            article_cover = article["pic"]
                            article_covers.append(article_cover)

                        # 将采集的有用信息存入文章最终数据字典内,包括列表的channelID，如有channelType也可存入
                        article_fields["channelID"] = channelid
                        article_fields["channelname"] = channelname
                        article_fields["channeltype"] = channel_type
                        article_fields["workerid"] = article_id
                        article_fields["title"] = article_title
                        article_fields["contentType"] = article_type
                        article_fields["url"] = share_url
                        if channelname == '视频':
                            article_fields["pubtime"] = InitClass().date_time_stamp(pubtime)
                        else:
                            article_fields["pubtime"] = pubtime
                        article_fields["banner"] = 0
                        # 将请求文章必需信息存入
                        articleparam["articleField"] = article_fields  # 携带文章采集的数据
                        articleparam["articleid"] = article_id
                        articlesparams.append(articleparam)
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        for article in articles:
            articleid = article.get("articleid")
            article_field = article.get("articleField")
            if isinstance(article.get("videocovers"), list) and len(article.get("videocovers")):
                url = "https://playvideo.qcloud.com/getplayinfo/v4/1251245530/5285890811733089851"
                headers = {
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Connection": "keep-alive",
                    "Host": "playvideo.qcloud.com",
                    "Origin": "https://m.guancha.cn",
                    "Referer": "https://m.guancha.cn/",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "cross-site",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36"
                }
                data = {
                    "psign": article.get("article_type")
                }
            else:
                url = "https://app.guancha.cn/news/content"
                headers = {
                    'Host': 'app.guancha.cn',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; VTR-AL00 Build/HUAWEIVTR-AL00)'
                }
                data = {
                    'id': articleid,
                    'device': 'android',
                    'v': '202012141',
                    'type': article.get("article_type"),
                    'access-token': ''
                }
            method = 'get'
            articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                             article_field=article_field)
            articleparams.append(articleparam)
        yield articleparams

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            try:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                print(content_s)
                if "requestId" in content_s.keys():
                    try:
                        videocovers = list()
                        videocover = content_s["coverInfo"]["coverUrl"]
                        videocovers.append(videocover)
                        video = content_s["videoInfo"]["sourceVideo"]["url"]
                        videos = list()
                        videos.append(video)
                        fields["videos"] = videos
                        fields["videocover"] = videocovers
                    except Exception as e:
                        logging.info(f"此新闻无视频{e}")
                else:
                    worker_id = content_s["data"]["id"]
                    article_title = content_s["data"]["title"]
                    author = content_s["data"]["author"]
                    source = content_s["data"]["source"]
                    content = content_s["data"]["content"]
                    comment_num = content_s["data"]["comment_num"]
                    # hit_num = content_s["data"]["Hits"]  # 点击数
                    try:
                        images = list()
                        images.append(content_s["share_pic"])
                        fields["images"] = images
                    except Exception as e:
                        self.logger.info(f"获取文章内图片失败{e}")
                    # fields["appname"] = self.newsname
                    fields["title"] = article_title
                    fields["workerid"] = worker_id
                    fields["content"] = content
                    fields["source"] = source
                    fields["commentnum"] = comment_num
                    fields["author"] = author
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
    appspider = GuanChaZhe("观察者")
    appspider.run()
