# -*- coding:utf-8 -*-

"""
企鹅号账户爬虫
# author: Chris
# date: 2020/11/6
# update: 2020/11/6
"""

import requests
import json
import time
import traceback
from lxml import etree
from bs4 import BeautifulSoup

from api_common_utils.proxy import get_abuyun_proxies


class KanDianFetch:

    def __init__(self, logger):
        # 平台类型，1微信，2微博，3头条号，4抖音号，5企鹅号，6网易号，7大鱼号，8百家号，9快手号。
        self._media_type = 5
        
        # 请求头。
        self._headers = {
            'User-Agent': '%E7%9C%8B%E7%82%B9%E5%BF%AB%E6%8A%A56530(android)',
            'Cookie': 'lskey=; luin=; skey=; uin=; kb_qbid=; '
                      'qb_guid=88422b2763c8d28f1c064846377988cb; '
                      'qb_qua=QV=3&PL=ADR&PR=KB&PP=com.tencent.reading'
                      '&PPVN=6.5.30.0&CO=SYS&PB=GE&VE=P&DE=PHONE&CHID=9002096'
                      '&LCID=0&MO= LIO-AN00 &RL=1920*1080&OS=5.1.1&API=22&REF=qb_0&TM=00; logintype=0;',
            'Host': 'r.cnews.qq.com',
            'Referer': 'http://cnews.qq.com/cnews/android/'
        }
        # 会话。
        self._session = requests.Session()
        self._logger = logger
        self._qie_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                              "(KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
            "host": "om.qq.com",
            }
        self._pc_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
            "Host":	"kuaibao.qq.com",
        }
        self._time_out = 10

        # 账号信息默认值。
        self._default_account = {
            "_id": "",
            "status": 1,
            "mediaType": self._media_type,
            "mediaName": "企鹅号",
            "accountType": -1,
            "mediaUid": "",
            "nickName": "",
            "avatar": "",
            "url": "",
            "gender": 0,
            "province": "",
            "city": "",
            "fanNum": 0,
            "followNum": 0,
            "workNum": 0,
            "readNum": 0,
            "playNum": 0,
            "likeNum": 0,
            "commentNum": 0,
            "forwardNum": 0,
            "wxLookNum": 0,
            "wangYiJoinNum": 0,
            "mediaWorkNum": 0,
            "mediaReadNum": 0,
            "mediaPlayNum": 0,
            "mediaLikeNum": 0,
            "mediaCommentNum": 0,
            "mediaForwardNum": 0,
            "mediaWxLookNum": 0,
            "mediaWangYiJoinNum": 0,
            "AII": 0,
            "AFCI": 0,
        }

        # 作品信息默认值。
        self._default_works_fields = {
            "_id": "",
            "status": 1,
            "mediaType": self._media_type,
            "mediaName": "企鹅号",
            "accountType": -1,
            "mediaUid": "",
            "accountId": "",
            "accountUrl": "",
            "nickName": "",
            "avatar": "",
            "url": "",
            "mediaWorkId": "",
            "author": "",
            "title": "",
            "digest": "",
            "content": "",
            "contentType": 1,
            "extendContentType": -1,
            "source": "",
            "isOriginal": "",
            "topics": list(),
            "covers": list(),
            "videos": list(),
            "audios": list(),
            "updateParams": "{}",
            "pubTime": 0,
            "pubDateTime": 0,
            "createTime": 0,
            "createDateTime": 0,
            "updateTime": 0,
            "updateDateTime": 0,
            "readNum": 0,
            "playNum": 0,
            "likeNum": 0,
            "commentNum": 0,
            "forwardNum": 0,
            "wxLookNum": 0,
            "wangYiJoinNum": 0,
            "HI": 0
        }

    def _parse_vid_url(self, vid):
        """
        解析视频。
        :return:
        """

        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        }
        url = f"http://vv.video.qq.com/getinfo?vids={vid}&platform=101001&charge=0&otype=json&defn=shd"
        resp = self._session.get(url, headers=headers)
        ret = resp.text[len('QZOutputJson='):-1]
        ret = json.loads(ret)
        url = ret['vl']['vi'][0]['ul']['ui'][0]['url'] + ret['vl']['vi'][0]['fn'] + "?vkey=" + ret['vl']['vi'][0][
            'fvkey']
        return url

    def _parse_article_or_video_detail(self, url):
        """
        采集详情。
        :return:
        """

        fields = dict()
        detail_resp = self._session.get(url, headers=self._pc_headers, timeout=self._time_out)
        detail_res = detail_resp.content.decode(encoding="utf-8")
        # self._logger.debug(f"url地址是{url}的详情是{detail_res}")
        detail_res = json.loads(detail_res)
        fields["url"] = detail_res["short_url"]  # 文章地址
        # 评论点赞数
        if "count_info" in detail_res and detail_res["count_info"]:
            # 评论 点赞 分享
            fields["commentNum"] = detail_res["count_info"]["comments"]
            fields["likeNum"] = detail_res["count_info"]["like_info"]
            fields["forwardNum"] = detail_res["count_info"]["share_count"]
        else:
            fields["commentNum"] = 0
            fields["likeNum"] = 0
            fields["forwardNum"] = 0
        # 内容
        context = detail_res["content"]["text"]
        img_list = []
        vid_list = []
        if "attribute" in detail_res and detail_res["attribute"]:
            imgs = detail_res["attribute"]
            for im, img in imgs.items():
                video = dict()
                if im.startswith("IMG_"):
                    img_list.append(img["origUrl"])
                else:
                    video["poster"] = img["img"]
                    video["src"] = img["playurl"]
                    video["height"] = img["height"]
                    video["width"] = img["width"]
                    video["vid"] = img["vid"]
                    vid_list.append(video)
        if img_list:
                for img in img_list:
                    context = context.replace("<!--IMG_%d-->" % img_list.index(img), f"<img src='{img}'>")
        if vid_list:
            for vid in vid_list:
                vid["src"] = self._parse_vid_url(vid["vid"])
                context = context.replace(
                    "<!--VIDEO_%d-->" % vid_list.index(vid),
                    f"<video src={vid['src']} poster={vid['poster']} controls='controls'> </video>")
        fields["content"] = context
        fields["covers"] = img_list
        fields["videos"] = [i["src"] for i in vid_list]
        return fields

    def _parse_app_detail(self, account, contents):
        """
        解析客户端响应体。
        :return:
        """

        works_list = []
        if contents["info"]["newsList"] and contents["info"]["videoList"]:
            content_list = contents["info"]["newsList"] + contents["info"]["videoList"]
        elif contents["info"]["newsList"]:
            content_list = contents["info"]["newsList"]
        else:
            self._logger.warning(f"账户---{account['mediaUid']}---下没有作品")
            return

        # 默认字段值。
        with_account_info_fields = dict(dict(), **self._default_works_fields)
        with_account_info_fields["accountType"] = account["accountType"]
        with_account_info_fields["mediaUid"] = account["mediaUid"]
        with_account_info_fields["accountId"] = account["_id"]
        with_account_info_fields["accountUrl"] = account["url"]
        with_account_info_fields["nickName"] = account["nickName"]
        with_account_info_fields["avatar"] = account["avatar"]

        # 遍历作品列表。
        for content in content_list:
            """作品详情"""
            if content["title"] == "红包分享页":
                self._logger.warning(f"此处应该是遇到广告了, 内容是{content}")
                continue
            # 初始化一条数据。
            parse_fields = dict(dict(), **with_account_info_fields)
            parse_fields["title"] = content["title"]        # 文章标题
            parse_fields["mediaWorkId"] = content["id"]     # 文章id
            parse_fields["digest"] = content["abstract"]    # 简介
            parse_fields["pubTime"] = int(content["timestamp"])
            parse_fields["pubDateTime"] = int(content["timestamp"])*1000
            """content详情"""
            """此处表示传参为图文稿类型而非视频稿"""
            # https://kuaibao.qq.com/getSubNewsContent?id=
            if "rowkey" in content.keys():
                detail_url = f"https://kuaibao.qq.com/getSubNewsContent?id={content['rowkey']}"
                parse_fields["updateParams"] = json.dumps({"wid": content["rowkey"]}, separators=(",", ":"))
            else:
                detail_url = f"https://kuaibao.qq.com/getSubNewsContent?id={content['id']}"
                parse_fields["updateParams"] = json.dumps({"wid": content["id"]}, separators=(",", ":"))
            fields = self._parse_article_or_video_detail(detail_url)
            parse_fields["url"] = fields["url"]
            parse_fields["commentNum"] = fields["commentNum"]
            parse_fields["likeNum"] = fields["likeNum"]
            parse_fields["forwardNum"] = fields["forwardNum"]
            parse_fields["content"] = fields["content"]
            parse_fields["covers"] = fields["covers"]
            parse_fields["videos"] = fields["videos"]
            if parse_fields["videos"]:
                parse_fields["contentType"] = 3
            if len(parse_fields["videos"]) == 0 and len(parse_fields["covers"]) != 0:
                parse_fields["contentType"] = 2
            # 计算作品ID。
            work_id_str = f'{parse_fields["mediaType"]}{parse_fields["mediaWorkId"]}{parse_fields["accountType"]}'
            parse_fields["_id"] = (work_id_str)
            works_list.append(parse_fields)
        return works_list

    def _parse_cookie_works(self, contents, account):
        """
        解析作品数据。
        :return:
        """

        # 初始化结果列表。
        works_list = []

        # 默认字段值。
        with_account_info_fields = dict(dict(), **self._default_works_fields)
        with_account_info_fields["accountType"] = account["accountType"]
        with_account_info_fields["mediaUid"] = account["mediaUid"]
        with_account_info_fields["accountId"] = account["_id"]
        with_account_info_fields["accountUrl"] = account["url"]
        with_account_info_fields["nickName"] = account["nickName"]
        with_account_info_fields["avatar"] = account["avatar"]
        uid = account["mediaUid"]

        for content in contents["data"]["articles"]:
            parse_fields = dict(dict(), **with_account_info_fields)
            """作品详情"""
            parse_fields["title"] = content["title"]
            parse_fields["url"] = content["url"]
            parse_fields["mediaWorkId"] = content["article_id"]
            # parse_fields["covers"] = content["cover_pics"]
            pub_time = content["pub_time"]
            parse_fields["pubTime"] = int(time.mktime(time.strptime(pub_time, "%Y-%m-%d %H:%M:%S")))
            parse_fields["pubDateTime"] = parse_fields["pubTime"] * 1000
            parse_fields["readNum"] = content["read"]
            parse_fields["commentNum"] = content["commentnum"]
            """重新确定封面图，就是app或后台看到的"""
            parse_fields["covers"] = content["cover_pics"]
            """提取content内容"""
            self._qie_headers.update({"Host": "page.om.qq.com"})
            self._session.proxies = None
            res = self._session.get(parse_fields["url"], headers=self._qie_headers)
            tree = etree.HTML(res.text)
            soup = tree.xpath("//section[@class='article']")
            """依此判断文章内是否有封面图"""
            covers = tree.xpath("//section[@class='article']//img/@src")
            if soup:
                context = etree.tostring(soup[0], encoding="utf-8").decode("utf-8")
            else:
                context = ""
            """判断是否存在video"""
            if content["video"]:    # 表示存在视频
                if "vid" not in content.keys():     # 图文视频稿
                    vid = [i["vid"] for i in content["v_infos"]]
                    if content["video"][vid[0]]["img"]:
                        imgs = content["video"][vid[0]]["img"]
                        # vid_img = content["video"][vid[0]]["img"]["imgurl1000"]["imgurl"]
                        vid_img = content["video"][vid[0]]["img"][list(imgs.keys())[0]]["imgurl"]
                    else:
                        vid_img = ""
                    for vi in vid:
                        url = self._parse_vid_url(vi)
                        parse_fields["videos"] = [url]

                    soup = BeautifulSoup(context, "html.parser")
                    video = soup.new_tag("video")
                    video.attrs.update({"src": parse_fields["videos"][0]})
                    video.attrs.update({"poster": vid_img})
                    video.attrs.update({"preload": "true"})
                    soup.find("div", "video_play").insert(0, video)
                    parse_fields["content"] = str(soup).strip()

                    parse_fields["updateParams"] = json.dumps(
                        {
                            "wid": content["article_id"],
                            "type": "article",
                            "nid": uid
                        },
                        separators=(",", ":")
                    )
                else:
                    vid = [content["vid"]]
                    if content["video"]["img"]:
                        imgs = content["video"]["img"]
                        # vid_img = content["video"][vid[0]]["img"]["imgurl1000"]["imgurl"]
                        vid_img = content["video"]["img"][list(imgs.keys())[0]]["imgurl"]
                    else:
                        vid_img = ""
                    for vi in vid:
                        url = self._parse_vid_url(vi)
                        parse_fields["videos"] = [url]
                    context = f"<div><video src=\"{parse_fields['videos'][0]}\" poster=\"{vid_img}\" " \
                              f"controls=\"controls\"></video></div>"
                    parse_fields["content"] = context
                    parse_fields["updateParams"] = json.dumps(
                        {"wid": content["article_id"], "type": "video", "nid": uid}, separators=(",", ":"))

            else:
                parse_fields["content"] = context
                parse_fields["updateParams"] = json.dumps(
                    {"wid": content["article_id"], "type": "article", "nid": uid}, separators=(",", ":"))

            if parse_fields["videos"]:
                parse_fields["contentType"] = 3
            if len(parse_fields["videos"]) == 0 and len(covers) != 0:
                parse_fields["contentType"] = 2

            # self.make_md5('5' + uid + article_dic['accountType'])
            work_id_str = f'{parse_fields["mediaType"]}{parse_fields["mediaWorkId"]}{parse_fields["accountType"]}'
            parse_fields["_id"] = (work_id_str)
            works_list.append(parse_fields)
        return works_list

    def fetch_account_type_2(self, account_type, user_params):
        """
        采集关注账号作品。
        :return:
        """

        # 参数验证。
        assert account_type == 2, f"参数错误，account_type：{account_type}"
        assert user_params and isinstance(user_params, (list, dict)), f"参数错误，user_params：{user_params}"

        # 初始化账号信息。
        account = dict(dict(), **self._default_account)
        account["accountType"] = account_type

        # 获取账号信息。
        uid = user_params["uid"]
        uid_type = user_params["uid_type"]
        body = {"chlidType": uid_type, "chlid": uid}
        """账号信息获取"""
        account_url = "https://r.cnews.qq.com/getSubItem?devid=866174162882183"
        try:
            resp = self._session.post(account_url, data=body, headers=self._headers, timeout=self._time_out)
            res = resp.text.encode("utf-8").decode("unicode_escape")
            res = json.loads(res)
            account["mediaUid"] = uid
            account["nickName"] = res["channelInfo"]["chlname"]  # 昵称
            account["avatar"] = res["channelInfo"]["icon"]  # 头像
            account["url"] = f"https://kuaibao.qq.com/s/MEDIANEWSLIST?chlid={uid}&chlidType={uid_type}"
            account["fanNum"] = res["channelInfo"]["subCount"]  # 粉丝数
            account["mediaReadNum"] = res["channelInfo"]["readCount"]  # 阅读数
            account["mediaLikeNum"] = res["channelInfo"]["likeCount"]  # 点赞数
            account["mediaForwardNum"] = res["channelInfo"]["shareCount"]  # 分享数
            account["_id"] = (f"{self._media_type}{uid}{account_type}")
            account['createTime'] = int(time.time())
            account['createDateTime'] = int(time.time() * 1000)
            account['updateTime'] = int(time.time())
            account['updateDateTime'] = int(time.time() * 1000)
        except Exception as e:
            self._logger.warning(f"关注账户{uid}账户信息获取报错：, {e}.\n{traceback.format_exc()}")
        """作品信息获取"""
        """作品信息获取之前依靠看点快报app抓包分图文（包含视频文）、视频两个分类依次请求，"""
        """但是今天**11-7**发现视频的内容无法获取，故决定更换采集方法，app抓包只需获取账户信息即可"""
        # article_url = "https://r.cnews.qq.com/getSubNewsIndex?devid=866174162882183"
        # video_url = "https://r.cnews.qq.com/getVideoNewsIndex?devid=866174162882183"
        # try:
        #     article_resp = self._session.post(article_url, data=body, headers=self._headers, timeout=self._time_out)
        #     article_res = article_resp.text.encode("utf-8").decode("unicode_escape")
        #     article_res = json.loads(article_res)
        #     ret = self._parse_app_detail(uid, article_res)
        #     result += ret
        #     print(len(result))
        #     print(json.dumps(result, indent=4, ensure_ascii=False))
        # except Exception as e:
        #     self._logger.warning(f"关注账户{self._uid}作品文章类获取报错：, {e}.\n{traceback.format_exc()}")
        #
        # try:
        #     video_resp = self._session.post(video_url, data=body, headers=self._headers, timeout=self._time_out)
        #     video_res = video_resp.text.encode("utf-8").decode("unicode_escape")
        #     video_res = json.loads(video_res)
        #     ret1 = self._parse_app_detail(uid, video_res, video="123")
        #     result += ret1
        # except Exception as e:
        #     self._logger.warning(f"关注账户{self._uid}作品视频类获取报错：, {e}.\n{traceback.format_exc()}")
        """以下是更新后的方法，比如账户的首页地址`https://kuaibao.qq.com/media/3406935823?chlid=3406935823&chlidType=1`"""
        # https://kuaibao.qq.com/n/getMediaCardInfo?chlid=3406935823&chlidType=1
        target_url = f"https://kuaibao.qq.com/n/getMediaCardInfo?chlid={uid}&chlidType={uid_type}"
        # referer: https://kuaibao.qq.com/media/3406935823?chlid=3406935823&chlidType=1
        refer_url = f"https://kuaibao.qq.com/media/{uid}?chlid={uid}&chlidType={uid_type}"
        self._pc_headers.update({"Referer": refer_url})
        resp = self._session.get(target_url, headers=self._pc_headers, timeout=30)
        res = json.loads(resp.text)
        if "info" not in res.keys():
            self._logger.warning(f"关注账户{uid}作品采集报错，获取不到其详细作品，此次请求结果是：{res}")
            return
        works_list = self._parse_app_detail(account, res)
        return account, works_list

    def fetch(self, account_type, uid=None, user_params=None):
        """
        分两种抓取方式：
        1、运营账号：因为需要可靠的粉丝数，所以依靠自主cookie获取
        2、关注账号：则是从看点快报app抓包获取
        """
        account, works_list = self.fetch_account_type_2(account_type, user_params)
        # 返回结果集。
        return dict(code=1, msg="success", data=dict(account=account, works=works_list))


class KDSpider:

    def __init__(self, logger):
        self.logger = logger

    def run(self, user_id):
        uuid = {"uid": user_id, "uid_type": "1"}
        return KanDianFetch(logger=self.logger).fetch(account_type=2, user_params=uuid)

    def fetch(self, task):
        try:
            res = self.run(task["platformAccountID"])
            return res
        except Exception as e:
            self.logger.warning(f"{e}\n{traceback.format_exc()}")
            return dict(code=0, msg=str(e))



def test():
    # 测试。
    from common_utils.llog import LLog
    _logger = LLog("test", only_console=True).logger
    uuid = {"uid": "1593992018", "uid_type": "1"}
    rets = KanDianFetch(_logger).fetch(account_type=2, user_params=uuid)
    print(json.dumps(rets, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    test()
