# -*- coding:utf-8 -*-

"""
云易媒，账号、作品采集调度程序。
微博。
# author: Chris
# date: 2020.8.27
# update: 2020.8.27
"""
import traceback

import requests
import js2xml
import re
import json
import time
from lxml import etree
from bs4 import BeautifulSoup
from api_common_utils.proxy import get_abuyun_proxies
from spiders.libs.spiders.we_media.we_media_utils import md5


class BjhFetcher:

    def __init__(self, bjh_id, account_type, logger):
        # 平台类型，1微信，2微博，3头条号，4抖音号，5企鹅号，6网易号，7大鱼号，8百家号，9快手号。
        self._media_type = 8
        self._bjh_id = bjh_id
        self._account_type = account_type
        self._headers = {
            "Connection": "Keep-Alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
            "Cookie": "PSTM=1602325038; BIDUPSID=95A5A7855B6298B7C028D37D7E318FF8; "
                      "BAIDUID=66B437B782F6FE66A7B54F2084D4BCD2:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; "
                      "H_PS_PSSID=1455_32875_32952_32970_32705_32962; "
                      "BDUSS=NJbERSeWdOfjYxU1JTa1lKT1BvcWUzV0xieWpHUFFKRnNqLWFkVFBMbUI3Y2xmRVFBQUFBJCQAAAAAAAAAAAEAA"
                      "ABp8j4vwffQ0M6o0rs5MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                      "IFgol-BYKJfRV; BDUSS_BFESS=NJbERSeWdOfjYxU1JTa1lKT1BvcWUzV0xieWpHUFFKRnNqLWFkVFBMbUI3Y2x"
                      "mRVFBQUFBJCQAAAAAAAAAAAEAAABp8j4vwffQ0M6o0rs5MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                      "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIFgol-BYKJfRV",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        self._session = requests.Session()
        self._session.headers.update(self._headers)
        # self._session.proxies = get_abuyun_proxies()
        self._logger = logger

    def _parse_nums_yunying(self, token, wid):
        """
        分析文章的阅读、点赞、转发等数量
        :param token: 账号唯一识别token
        :param uid: 账号id
        :param wid: 文章id
        :return:
        """
        url = 'https://baijiahao.baidu.com/builderinner/open/resource/query/articleStatistics'
        data = {
            "app_token": token,
            "app_id": self._bjh_id,
            "article_id": wid
        }
        resp = self._session.post(url=url, data=data)
        self._logger.info(f"请求作品相关数据的response结果是：{resp.text}")
        res = json.loads(resp.text)
        if "errno" == 0 and "errmsg" == "成功":
            res = res["data"]
            self._logger.info(f"请求作品相关数据的response结果是：{res}")
        else:
            res = res["data"]
        return res

    def _parse_nums_guanzhu(self, comment_url, comment_parm):
        """
        分析文章的阅读、点赞、转发等数量(关注账号)
        :param comment_url:
        :param comment_parm:
        :return:
        """
        resp = self._session.get(comment_url, params=comment_parm, verify=False)
        self._logger.info(f"请求作品相关数据的response结果是：{resp.text}")
        res = re.findall(r".*?({.*}).*", resp.text, re.S)
        res = json.loads(res[0])
        self._logger.debug(f"作品数据的结果是：{res}")
        return res

    def _parse_detail(self, uk, nick_name, avatr, account_id, account_url):
        detail_url = "https://mbd.baidu.com/webpage"
        param = {
            "tab": "main",
            "num": "6",
            "uk": uk,
            "type": "newhome",
            "action": "dynamic",
            "format": "jsonp",
            "otherext": "h5_20200624112743",
            "Tenger-Mhor": "1083193650",
            "callback": "__jsonp01593672621348"
        }
        resp = self._session.get(detail_url, params=param, verify=False)
        self._logger.info(f"请求作品相关信息的response结果是：{resp.text}")
        res = re.findall(r".*?({.*}).*", resp.text, re.S)
        ret = json.loads(res[0])
        self._logger.info(f"作品信息的结果是：{ret}")
        works = []
        comment_url = "https://mbd.baidu.com/webpage"
        comment_parm = {
            "type": "homepage",
            "action": "interact",
            "format": "jsonp",
            "Tenger-Mhor": "2216241224",
            "uk": uk,
            "callback": "__jsonp21598434519127"
        }
        for i in ret["data"]["list"]:
            if i["itemType"] == "zhibo":
                self._logger.warning(f"该条信息是直播相关信息不采集，相关内容是：{i}")
                continue
            try:
                parse_fields = {
                    "_id": "",
                    "status": 1,
                    "mediaType": self._media_type,
                    "mediaName": "百家号",
                    "accountType": self._account_type,
                    "mediaUid": self._bjh_id,     # 平台账号或作者id
                    "accountId": account_id,
                    "nickName": nick_name,
                    "avatar": avatr,
                    "url": "",
                    "accountUrl":account_url,
                    "mediaWorkId": "",      # 平台作品id
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
                params = i["asyncParams"]
                comment_id = i["id"]
                comment_parm.update({"params": "[" + json.dumps(params) + "]"})
                # 文章信息
                parse_fields["title"] = i["itemData"]["title"]
                parse_fields["pubTime"] = i["dynamic_ctime"]
                try:
                    parse_fields["url"] = i["itemData"]["url"]
                except:
                    parse_fields["url"] = i["itemData"]["feed_url"]
                if "article_id" in i["itemData"]:
                    parse_fields["mediaWorkId"] = i["itemData"]["article_id"]
                    if i["itemData"]["imgSrc"]:
                        if type(i["itemData"]["imgSrc"]) == str:
                            parse_fields["covers"] = [i["itemData"]["imgSrc"]]
                        else:
                            parse_fields["covers"] = [pic["src"] for pic in i["itemData"]["imgSrc"]]
                    if i["itemData"]["type"] == "video":
                        video_url = json.loads(i["itemData"]["rmb_videoInfoExt"])["default"][
                            "defaultUrlHttp"]
                        parse_fields["videos"].append(video_url)
                        content = json.loads(i["itemData"]["content"])
                        vid_url = content[0]["src"]
                        vid_title = content[0]["title"]
                        vid_img = content[0]["https"]["cover"]
                        parse_fields["content"] = f"<div><p><video src=\"{vid_url}\" title=\"{vid_title}\" " \
                                                  f"poster=\"{vid_img}\" controls=\"controls\">" \
                                                  f"{vid_title}</video></p></div>"
                        parse_fields["contentType"] = 4  # 认定为纯视频
                    else:
                        resp = self._session.get(parse_fields["url"])
                        content_tree = etree.HTML(resp.content)
                        contents = content_tree.xpath("//div[@class='article-content']")
                        content = etree.tostring(contents[0]).decode("utf-8")
                        soup = BeautifulSoup(content, "html.parser")
                        parse_fields["content"] = str(soup).strip()
                        # if len(parse_fields["covers"]) == 0:
                        #     parse_fields["covers"] = content_tree.xpath("//div[@class='img-container']/img/@src")
                        parse_fields["videos"] = content_tree.xpath("//video/@src")
                        if len(parse_fields["videos"]) != 0:  #  如果文章里面含有视频，判断其长度
                            parse_fields["contentType"] = 3   #  为视频文


                else:
                    parse_fields["mediaWorkId"] = i["itemData"]["nid"]
                    if i["itemData"]["type"] == "3":
                        parse_fields["contentType"] = 4  # 认定为视频
                        parse_fields["covers"] = [i["itemData"]["video_cover"]["http"]]
                        parse_fields["videos"] = [i["itemData"]["video_src"]["http"]]
                        vid_url = parse_fields["videos"][0]
                        vid_title = parse_fields["title"]
                        vid_img = parse_fields["covers"][0]
                        parse_fields["content"] = f"<div><p><video src=\"{vid_url}\" title=\"{vid_title}\" " \
                                                  f"poster=\"{vid_img}\" controls=\"controls\">" \
                                                  f"{vid_title}</video></p></div>"
                    else:
                        parse_fields["covers"] = [pic["img_origin"] for pic in i["itemData"]["imgSrc"]]
                        resp = self._session.get(parse_fields["url"])
                        content_tree = etree.HTML(resp.content)
                        if len(content_tree) != 0:
                            contents = content_tree.xpath("//div[@class='dynamic-item']")
                            content = etree.tostring(contents[0]).decode("utf-8")
                            soup = BeautifulSoup(content, "html.parser")
                            parse_fields["content"] = str(soup).strip()
                            parse_fields["videos"] = content_tree.xpath("//video/@src")
                            if len(parse_fields["videos"]) != 0:  # 如果文章里面含有视频
                                parse_fields["contentType"] = 3  # 为视频文

                            # if len(parse_fields["covers"]) == 0:
                            #     parse_fields["covers"] = content_tree.xpath("//div[@class='img-container']/img/@src")
                        else:
                            print(resp.text)
                # 获取文章的各种数
                # 判断该账号是运营还是关注
                if self._account_type == 2:
                    comment_ret = self._parse_nums_guanzhu(comment_url, comment_parm)
                    parse_fields["commentNum"] = int(
                        comment_ret["data"]["user_list"][comment_id]["comment_num"])  # 评论数
                    parse_fields["readNum"] = comment_ret["data"]["user_list"][comment_id][
                        "read_num"]  # 阅读数

                work_id_str = f'{parse_fields["mediaType"]}{parse_fields["mediaWorkId"]}{parse_fields["accountType"]}'
                parse_fields["_id"] = md5(work_id_str)

                # 如果有视频那么播放数等于阅读数
                if len(parse_fields["videos"]) != 0:
                    parse_fields["playNum"] = parse_fields["readNum"]
                else:
                    pass
                # 判断文章类型
                if parse_fields["contentType"] != 4 and parse_fields["contentType"] != 3:
                    if len(parse_fields["videos"]) == 0 and len(parse_fields["covers"]) != 0:
                        parse_fields["contentType"] = 2
                else:
                    pass

                parse_fields["pubDateTime"] = parse_fields["pubTime"] * 1000
                parse_fields["updateTime"] = int(time.time())
                parse_fields["updateDateTime"] = int(time.time()*1000)
                parse_fields["createTime"] = int(time.time())
                parse_fields["createDateTime"] = int(time.time()*1000)
                parse_fields["updateParams"] = json.dumps({"bjh_id": self._bjh_id, "uk": uk, "params": params,
                                                           "comment_id": comment_id})
                self._logger.info(f'{nick_name}的文章结果为{parse_fields}')
                works.append(parse_fields)
            except Exception as e:
                self._logger.warning(str(e))
                continue
        return works

    def bjh_fetch(self):
        """进入指定账户首页，获取参数uk值、以及相关账户信息"""
        try:
            account = {
                "_id": "",
                "status": 1,
                "mediaType": self._media_type,
                "mediaName": "百家号",
                "accountType": self._account_type,
                "mediaUid": self._bjh_id,
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
            if str(self._bjh_id).startswith("https"):
                url = f'{self._bjh_id}'
                resp = self._session.get(self._bjh_id)
            else:
                url = "https://author.baidu.com/home/{}".format(self._bjh_id)
                resp = self._session.get(url, verify=False)
            resp_1 = etree.HTML(resp.content)
            info = resp_1.xpath("//script[starts-with(text(), 'window.runtime= ')]/text()")
            info = "\n".join(info)
            if len(info):
                src_element = js2xml.parse(info, encoding='utf-8', debug=False)
                account["nickName"] = src_element.xpath("//property[@name='display_name']/string/text()")[0]
                account["avatar"] = src_element.xpath("//property[@name='avatar_big']/string/text()")[0]
                account["url"] = url
                # account["desc"] = src_element.xpath("//property[@name='sign']/string/text()")[0]    # 作者简介
                account["gender"] = int(src_element.xpath("//property[@name='gender']/string/text()")[0])
                try:
                    account["mediaWorkNum"] = src_element.xpath("//property[@name='contentNum']"
                                                           "//property[@name='count']/string/text()")[0]  # 作品数
                except:
                    account["mediaWorkNum"] = src_element.xpath("//property[@name='contentNum']"
                                                           "//property[@name='count']/number/@value")[0]
                if str(account["mediaWorkNum"]).find(".") != -1:
                    account["mediaWorkNum"] = int(float(account["mediaWorkNum"]) * 10000)
                account["mediaWorkNum"] = int(account["mediaWorkNum"])
                account["fanNum"] = int(src_element.xpath("//property[@name='fans_num']/string/text()")[0])  # 粉丝数
                account["followNum"] = int(src_element.xpath("//property[@name='follow_num']/string/text()")[0])   # 关注数
                account["likeNum"] = int(src_element.xpath("//property[@name='likes_num']/number/@value")[0])      # 获赞数
                account["_id"] = md5(f'{self._media_type}{self._bjh_id}{self._account_type}')
                uk = src_element.xpath("//property[@name='uk']/string/text()")[0]
                self._logger.info(f'{account["nickName"]}的账号数据为{account}')
                works = self._parse_detail(uk, account["nickName"], account["avatar"], account["_id"], account["url"])
                return dict(
                    code=1,
                    msg="success",
                    data=dict(
                        account=account,
                        works=works
                    )
                )
            else:
                self._logger.warning(f'{self._bjh_id}的用户信息不存在')
        except Exception as e:
            self._logger.warning(str(e))

    def fetch(self):
        return self.bjh_fetch()


class BjhUpdate:

    def __init__(self, logger):
        self._headers = {
            "Connection": "Keep-Alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": "PSTM=1602325038; BIDUPSID=95A5A7855B6298B7C028D37D7E318FF8; "
                      "BAIDUID=66B437B782F6FE66A7B54F2084D4BCD2:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; "
                      "H_PS_PSSID=1455_32875_32952_32970_32705_32962; "
                      "BDUSS=NJbERSeWdOfjYxU1JTa1lKT1BvcWUzV0xieWpHUFFKRnNqLWFkVFBMbUI3Y2xmRVFBQUFBJCQAAAAAAAAAAAEAA"
                      "ABp8j4vwffQ0M6o0rs5MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                      "IFgol-BYKJfRV; BDUSS_BFESS=NJbERSeWdOfjYxU1JTa1lKT1BvcWUzV0xieWpHUFFKRnNqLWFkVFBMbUI3Y2x"
                      "mRVFBQUFBJCQAAAAAAAAAAAEAAABp8j4vwffQ0M6o0rs5MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                      "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIFgol-BYKJfRV",
        }
        self._session = requests.Session()
        self._session.headers.update(self._headers)
        # self._session.proxies = get_abuyun_proxies()
        self._logger = logger

    def bjh_fetch_update(self, bjh_id, uk, params, comment_id):
        """
        更新文章数据
        :param bjh_id:
        :param uk:
        :param params:
        :param comment_id:
        :return:
        """
        if str(bjh_id).startswith("http"):
            # 该账号为关注账号
            first_url = bjh_id
            self._session.get(first_url, verify=False)
            comment_url = "https://mbd.baidu.com/webpage"
            comment_parm = {
                "type": "homepage",
                "action": "interact",
                "format": "jsonp",
                # "Tenger-Mhor": "2216241224",
                "uk": uk,
                # "callback": "__jsonp21598434519127",
            }
            comment_parm.update({"params": "[" + json.dumps(params) + "]"})
            # 页面请求不报错，但是不是预想的页面
            try:
                resp = self._session.get(comment_url, params=comment_parm, verify=False)
                self._logger.info(f"更新时首次请求的resp结果是：{resp.text}")
                res = re.findall(r".*?({.*}).*", resp.text, re.S)
                comment_ret = json.loads(res[0])
                work = dict()
                work["commentNum"] = int(comment_ret["data"]["user_list"][comment_id]["comment_num"])  # 评论数
                work["readNum"] = comment_ret["data"]["user_list"][comment_id]["read_num"]  # 阅读数
                work["updateTime"] = int(time.time())
                work["updateDateTime"] = int(time.time()) * 1000
                return work
            except Exception as e:
                self._logger.warning(str(e))

    def fetch_update(self, json_data):
        params_dict = json.loads(json_data)
        bjh_id = params_dict["bjh_id"]
        uk = params_dict["uk"]
        params = params_dict["params"]
        comment_id = params_dict["comment_id"]
        work = self.bjh_fetch_update(bjh_id, uk, params, comment_id)
        return {'code': 1, 'msg': 'ok', 'data': {'works': work}}


class BjhHotFetcher:

    def __init__(self, logger):
        # 平台类型，1微信，2微博，3头条号，4抖音号，5企鹅号，6网易号，7大鱼号，8百家号，9快手号。
        self._media_type = 8
        self._headers = {
            "Connection": "Keep-Alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        self._session = requests.Session()
        self._session.headers.update(self._headers)
        self._session.proxies = get_abuyun_proxies()
        self._logger = logger

    def _handle_time(self, time_str1, time_str2):
        ct = str(time.localtime().tm_year)
        str_lis = time_str1.split("-")
        if len(str_lis) > 2:
            time_str1 = ct[:2] + time_str1
            time_str = time_str1 + " " + time_str2
        else:
            time_str = ct + "-" + time_str1 + " " + time_str2
        time_array = time.strptime(time_str, "%Y-%m-%d %H:%M")
        time_stamp = int(time.mktime(time_array))
        if time_stamp > int(time.time()):
            time_str1 = str(int(ct[:2]) - 1) + time_str1[2:]
            time_str = time_str1 + " " + time_str2
            time_array = time.strptime(time_str, "%Y-%m-%d %H:%M")
            time_stamp = int(time.mktime(time_array))
        return time_stamp

    def _ready_url(self):
        all_list = []
        resp = self._session.get("http://news.baidu.com/")
        tree = etree.HTML(resp.text)
        a_list = tree.xpath("//a/@href")
        for a in a_list:
            if a.startswith("http://baijiahao"):
                all_list.append(a)
        types = ["LocalNews", "civilnews", "InternationalNews", "EnterNews", "SportNews", "FinanceNews", "TechNews",
                 "MilitaryNews", "InternetNews", "DiscoveryNews", "DiscoveryNews", "LadyNews", "HealthNews", "PicWall"]
        for kw in types:
            t = int(time.time() * 1000)
            try:
                if kw != "LocalNews":
                    url = "http://news.baidu.com/widget?id={kw}&t={t}".format(kw=kw, t=t)
                    resp = self._session.get(url)
                    tree = etree.HTML(resp.text)
                    a_list = tree.xpath("//a/@href")
                    for a in a_list:
                        if a.startswith("http://baijiahao"):
                            all_list.append(a)
                else:
                    url = "http://news.baidu.com/widget?id={kw}&ajax=json&t={t}".format(kw=kw, t=t)
                    resp = self._session.get(url)
                    resp = json.loads(resp.text)
                    res = resp["data"]["LocalNews"]["data"]["rows"]
                    if res["pic"]["url"].startswith("http://baijiaho"):
                        all_list.append(res["pic"]["url"])
                    for i in res["first"]:
                        if i["url"].startswith("http://baijiahao"):
                            all_list.append(i["url"])
                    for i in res["second"]:
                        if i["url"].startswith("http://baijiahao"):
                            all_list.append(i["url"])
            except Exception as e:
                self._logger.warning(f"关键词{kw}采集失败，原因是：{str(e)}")
                continue
        res_dup = list(set(all_list))
        self._logger.info("目前有%d条任务链接待抓取" % len(res_dup))
        return res_dup

    def fetch_detail(self):
        url_list = self._ready_url()
        ret = []
        for url in url_list:
            parse_fields = {
                "_id": "",
                "status": 1,
                "mediaType": self._media_type,
                "mediaName": "百家号",
                "accountType": 3,
                "mediaUid": "",  # 平台账号或作者id
                "accountId": "",
                "nickName": "",
                "avatar": "",
                "url": "",
                "mediaWorkId": "",  # 平台作品id
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
                "readNum": 0,
                "playNum": 0,
                "likeNum": 0,
                "commentNum": 0,
                "forwardNum": 0,
                "wxLookNum": 0,
                "wangYiJoinNum": 0,
                "HI": 0
            }
            try:
                resp = self._session.get(url, allow_redirects=False)
                """出现跳转情况，跨域之后则不在处理"""
                if resp.status_code != 200:
                    self._logger.info(f"response状态码不为200的请求地址是：{url}")
                    refer_url = resp.headers["location"]
                    host_url = re.findall(r"http[s]?://(.*[om|n])/", refer_url)
                    if host_url[0] != "baijiahao.baidu.com":
                        print("%s出现了跨域,新域名位%s" % (url, host_url[0]))
                        continue
                tree = etree.HTML(resp.content)
                if tree is not None and len(tree) > 0:
                    uid_info = tree.xpath("//div[@id='content-container']/@data-extralog")
                    if len(uid_info) > 0:
                        parse_fields["mediaUid"] = re.findall(r"appId:(.*);", uid_info[0])[0]
                    else:
                        self._logger.info("mediaUid的标签未找到，mediaUid为空")
                    nick_info = tree.xpath("//div[starts-with(@class, 'article-desc')]")[0]
                    try:
                        parse_fields["nickName"] = nick_info.xpath("./div[@class='author-txt']/p/text()")[0]
                        parse_fields["avatar"] = nick_info.xpath("./div[@class='author-icon']/img/@src")[0]
                    except:
                        parse_fields["nickName"] = nick_info.xpath("./div[@class='author-txt']//text()")[0]
                        parse_fields["avatar"] = nick_info.xpath("./div[@class='author-icon']//img/@src")[0]
                    parse_fields["mediaWorkId"] = re.findall(r"id=(\d+)", url)[0]
                    parse_fields["title"] = tree.xpath("//div[@class='article-title']/h2/text()")[0]
                    pub_date = nick_info.xpath(".//span[@class='date']/text()")[0]
                    pub_date = pub_date.replace("发布时间：", "").replace(" ", "")
                    pub_time = nick_info.xpath(".//span[@class='time']/text()")[0]
                    parse_fields["pubTime"] = self._handle_time(pub_date, pub_time)
                    parse_fields["pubDateTime"] = int(parse_fields["pubTime"]) * 1000
                    now = int(time.time())
                    parse_fields["createTime"] = now
                    parse_fields["createDateTime"] = now*1000
                    parse_fields["url"] = url
                    parse_fields["accountUrl"] = f"https://author.baidu.com/home?from=bjh_article&app_id={parse_fields['mediaUid']}"
                    work_id = f'{parse_fields["mediaType"]}{parse_fields["mediaWorkId"]}{parse_fields["accountType"]}'
                    parse_fields["_id"] = md5(work_id)
                    account_id = f'{parse_fields["mediaType"]}{parse_fields["mediaUid"]}{parse_fields["accountType"]}'
                    parse_fields["accountId"] = md5(account_id)

                    # 处理封面图。
                    covers = list()
                    temp_covers = tree.xpath("//div[@class='article-content']/div[@class='img-container']/img/@src")
                    for cover_url in temp_covers:
                        try:
                            resp = requests.head(cover_url, timeout=5)
                            status_code_str = str(resp.status_code)
                            if status_code_str.startswith("2"):
                                covers.append(cover_url)
                            else:
                                self._logger.debug(f"封面图无法访问，{cover_url}，{resp.status_code}")
                        except Exception:
                            self._logger.warning(f"封面图请求失败，{cover_url}")
                    parse_fields["covers"] = covers

                    contents = tree.xpath("//div[@class='article-content']")
                    content = etree.tostring(contents[0]).decode("utf-8")
                    soup = BeautifulSoup(content, "html.parser")
                    if soup.find_all("video"):
                        rets = [s.extract() for s in soup("div", "video-time-length")]
                        self._logger.info(f"删除视频时长标签的结果是：{rets}")
                    parse_fields["content"] = str(soup).strip()
                    if "<video" in parse_fields["content"]:
                        parse_fields["contentType"] = 3
                        parse_fields["videos"] = tree.xpath("//video/@src")
                    else:
                        if "<img" in parse_fields["content"]:
                            parse_fields["contentType"] = 2
                        else:
                            parse_fields["contentType"] = 1
                    ret.append(parse_fields)
            except Exception as e:
                self._logger.warning(str(e))
                continue
        return dict(
            code=1,
            msg="success",
            data=dict(
                works=ret
            )
        )

    def fetch(self):
        return self.fetch_detail()


def search_baijiahao(searchword):
    # 搜索百家号。
    searchurl = "https://m.baidu.com/sf/vsearch?pd=userlist&word={}&tn=vsearch&sa=vs_tab&lid=9835948930178535883&ms=1&from=1001703e&atn=index&mod=1".format(
        searchword)
    returnlist = []
    searchheaders = {
        "Host": "m.baidu.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Mode": "no-cors",
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1; OPPO A37m Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.22 SP-engine/2.18.0 baiduboxapp/11.22.5.10 (Baidu; P1 5.1)",
        "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
        "X-Requested-With": "com.baidu.searchbox",
        "Sec-Fetch-Site": "same-origin",
        # Referer: https://m.baidu.com/sf/vsearch?pd=userlist&word=%E6%B2%B3%E5%8C%97%E6%96%B0%E9%97%BB%E7%BD%91&tn=vsearch&sa=vs_tab&lid=9835948930178535883&ms=1&from=1001703e&atn=index
        "Accept-Encoding": "gzip, deflate",
        # "Accept-Language": zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
        "Cookie": "BAIDUCUID=jaHRi_i42ajSPS8H_a-zag8gv805uSuSYaHwigPj2iKk0qqSB; BAIDUID=9F06C0A9FA34089206F9C41611C89BF5:FG=1; MBD_AT=1588238997; WISE_HIS_PM=1; fontsize=1.0; iadlist=281638185467905; GID=G158YC3ACBTD7QNWFPJVCSQJ5N865LOLLZ; SP_FW_VER=3.180.4; BAIDULOC=12748972_4558638_47_150_1589523570503; SWANJS_VER=3.180.4; delPer=0; PSINO=1; ysm=16081; COOKIE_SESSION=0_0_0_0_0_0_0_0_0_0_0_0_0_1589523637%7C1%230_0_0_0_0_0_0_0_1589523637%7C1; ASUV=1.2.126; wpr=0; BDORZ=AE84CDB3A529C0F8A2B9DCDD1D18B695; MSA_WH=360_534; MSA_PHY_WH=720_1280; MSA_PBT=37.796875; MSA_ZOOM=1056; FC_MODEL=0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_1589523637%7C1%230_0_0_0_0_0_1589523637%7C1%230__0_0_0_0_1333_1589523637; H_WISE_SIDS=142979_146329_144876_145607_140368_146459_146732_145598_146001_145876_139913_146753_146135_139910_146312_146407_146819_145999_110086; cat_ms=q9n1o%2FovOkFuPcD9u1ncq3hlvkTYRsha6skKj%2B2SP2ABq%2B4xwUdF%2FRKjPmYaVSj6; __bsi=10968914762581662877_00_13_N_R_0_0303_c02f_Y",
        "X-Forwarded-For": "222.223.213.34",
    }
    r = requests.get(searchurl, headers=searchheaders)
    r.encoding = "utf8"
    tree = etree.HTML(r.text)
    user_tags = tree.xpath("//div[@class='sfc-userlist-item c-row c-row-align-middle']")
    for user_tag in user_tags:
        url = user_tag.xpath("div[@class='c-span8']/a/@href")[0]
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 5.1; OPPO A37m Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.22 SP-engine/2.18.0 baiduboxapp/11.22.5.10 (Baidu; P1 5.1)",}, allow_redirects=False)
        uid = re.compile('"bjh_id":"(.*?)"').findall(resp.text)[0]
        userdict = {"uid": uid,
                    "username": re.compile('<title>(.*?)</title>').findall(resp.text)[0],
                    # "userpicurl": user_tag.xpath("div[@class='sfc-userlist-logo-wrap c-span2']//img[@class='c-img-img']/@src")[0],
                    "url": url,
                    }
        returnlist.append(userdict)
        break

    return returnlist


class BJSpider:

    def __init__(self, logger):
        self.logger = logger

    def run(self, bjh_id):
        return BjhFetcher(bjh_id=bjh_id, account_type=2, logger=self.logger).fetch()

    def fetch(self, task):
        try:
            res = self.run(task["platformAccountID"])
            return res
        except Exception as e:
            self.logger.warning(f"{e}\n{traceback.format_exc()}")
            return dict(code=0, msg=str(e))

