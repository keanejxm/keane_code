# -*- coding:utf-8 -*-

"""
# author: Chris
# date: 2020/11/24
# update: 2020/11/24
# 凤凰网-大凤号-任意账号搜索与采集
"""
import hashlib
import json
import time
import traceback

import requests

from api_common_utils.base_data import DEFAULT_USER_INFO_FIELDS, DEFAULT_WORKS_FIELDS
from spiders.libs.spiders.we_media.we_media_utils import DEFAULT_WE_MEDIA_USER_WORKS_FIELDS, \
    DEFAULT_WE_MEDIA_USER_INFO_FIELDS


class FengHuangSearchAccounts:

    def __init__(self):
        self._session = requests.Session()
        self._headers = {
            # "User-Agent": "NewsApp/66.1 Android/5.1 (OPPO/OPPO A37m)",
            # "User-Agent": "NewsApp/74.1 Android/5.1.1 (HUAWEI/VOG-AL10)",
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; VOG-AL10 Build/HUAWEIVOG-AL10; wv) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36",
            # "Host": "nine.ifeng.com",
        }

    def app_search(self, keyword):
        data = {
            "client_search_subscribe": "",
            "k": keyword,
            "page": "1",
            "n": "20",
            "gv": "7.17.0",
            "av": "7.17.0",
            "uid": "863064578382402",
            "deviceid": "863064578382402",
            "proid": "ifengnews",
            "os": "android_22",
            "df": "androidphone",
            "vt": "5",
            "screen": "900x1600",
            "publishid": "6102",
            "nw": "wifi",
            "loginid": "",
            "adAid": "",
            "hw": "huawei_vog-al10",
            "st": "16062193173169",
            "sn": "e916c96b59d3dade195f92f604919351",
            "ltoken": "$2kJyeiQHbzIiOw4CO5ADNiMjMkJCLi4GbxIiOuQTM1ITNiQDMkJCLik3YnLiOlP7nlbrrlTouiIIukJCLi"
                      "IHcmLiOlPrsnfJjiEInwJCL29mcj5Wa6ISZyauI100sWgfa00lMgfa1SgcemIsIHdpNiOik7nnLrrlPoulbIul"
                      "TCLiIXakJmc0NCdjluI6IeljiujNWiuMW9J"
        }
        search_url = "https://nine.ifeng.com/searchsubscribe"
        resp = self._session.get(search_url, headers=self._headers, params=data)
        res = json.loads(resp.text)
        ret = []
        if res["data"]:
            ret = [i["followid"] for i in res["data"] if i["name"] == keyword]
        return ret


class FengHuangAccountsAndWorks:

    def __init__(self, logger):
        self.logger = logger
        self._session = requests.Session()
        self._headers = {
            # "User-Agent": "NewsApp/66.1 Android/5.1 (OPPO/OPPO A37m)",
            # "User-Agent": "NewsApp/74.1 Android/5.1.1 (HUAWEI/VOG-AL10)",
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; VOG-AL10 Build/HUAWEIVOG-AL10; wv) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36",
            # "Host": "nine.ifeng.com",
        }
        self._params_data = {
            "gv": "7.17.0",
            "av": "7.17.0",
            "uid": "863064578382402",
            "deviceid": "863064578382402",
            "proid": "ifengnews",
            "os": "android_22",
            "df": "androidphone",
            "vt": "5",
            "screen": "900x1600",
            "publishid": "6102",
            "nw": "wifi",
            "loginid": "",
            "adAid": "",
            "hw": "huawei_vog-al10",
            "st": "16062193173169",
            "sn": "e916c96b59d3dade195f92f604919351",
            # "followid": follow_id,
        }
        self._detail_data = {
            # "subid": "836081",
            # "gv": "7.17.0",
            # "av": "7.17.0",
            # "uid": "863064578382402",
            # "deviceid": "863064578382402",
            # "proid": "ifengnews",
            # "os": "android_22",
            # "df": "androidphone",
            # "vt": "5",
            # "screen": "900x1600",
            # "publishid": "6102",
            # "nw": "wifi",
            # "loginid": "",
            # "adAid": "",
            # "hw": "huawei_vog-al10",
            # "st": "16062193173169",
            # "sn": "e916c96b59d3dade195f92f604919351",
            # # "followid": follow_id,
        }
        # 作品信息默认值。
        self._default_works_fields = dict(dict(), **DEFAULT_WE_MEDIA_USER_WORKS_FIELDS)

    @staticmethod
    def md5(unicode_str, charset="UTF-8"):
        """
        字符串转md5格式。
        :return:
        """
        _md5 = hashlib.md5()
        _md5.update(unicode_str.encode(charset))
        return _md5.hexdigest()

    def _parse_accounts(self, follow_id):
        # follow_id = task["platformAccountID"]
        self._params_data.update({"followid": follow_id})
        url = "https://api.3g.ifeng.com/api_wemedia_index_info"
        resp = self._session.post(url, headers=self._headers, data=self._params_data)
        res = json.loads(resp.text)
        platformID = 'a545ee430b37c5da919ab80e1ec14eed'
        account = dict(dict(), **DEFAULT_WE_MEDIA_USER_INFO_FIELDS)
        account["_id"] = self.md5(platformID + str(res["data"]["userinfo"]["id"]))
        account["platformName"] = "凤凰新闻手机客户端"
        account["weMediaName"] = "大风号"
        account["platformAccountID"] = res["data"]["userinfo"]["id"]
        account["name"] = res["data"]["userinfo"]["name"]
        account["avatar"] = res["data"]["userinfo"]["logo"]
        account["createTime"] = int(time.time() * 1000),
        account["updateTime"] = int(time.time() * 1000),
        account["platformFansNum"] = int(res["data"]["userinfo"]["fans_num"]),
        account["platformFollowsNum"] = int(res["data"]["userinfo"]["follow_num"]),
        if res["data"]["userinfo"]["gender"]:
            account["gender"] = int(res["data"]["userinfo"]["gender"])
        return account

    def _parse_join_num(self, aid):
        url = "https://comment.ifeng.com/v3/get/comments"
        data = {"doc_url": aid}
        resp = self._session.post(url, headers=self._headers, data=data)
        res = json.loads(resp.text)
        num = int(res["join_count"])
        return num

    def _parse_works_video_detail(self, aid, fields):
        self._detail_data.update({"guid": aid})
        detail_url = "https://nine.ifeng.com/apiPhoenixtvDetails"
        resp = self._session.post(detail_url, headers=self._headers, data=self._detail_data)
        num = self._parse_join_num(aid)
        res = json.loads(resp.text)
        fields["platformWorksID"] = res["singleVideoInfo"][0]["id"]
        fields["title"] = res["singleVideoInfo"][0]["title"]
        fields["url"] = res["singleVideoInfo"][0]["shareURL"]
        img_url = res["singleVideoInfo"][0]["largeImgURL"]
        vid_url = res["singleVideoInfo"][0]["videoURL"]
        fields["readNum"] = int(res["singleVideoInfo"][0]["playTime"])
        fields["likeNum"] = res["singleVideoInfo"][0]["praise"]
        fields["readNum"] = fields["readNum"]
        fields["commentNum"] = num
        fields["covers"] = [img_url]
        fields["videos"] = [vid_url]
        fields["platformType"] = 7

        fields["content"] = f"<div><video src=\"{vid_url}\" poster=\"{img_url}\" " \
                            f"controls=\"controls\"></video></div>"
        fields["contentType"] = 3
        fields["createTime"] = int(time.time()*1000)
        fields["updateTime"] = int(time.time() * 1000)
        return fields

    def _parse_works_article_detail(self, aid, fields):
        if "guid" in self._detail_data.keys():
            self._detail_data.pop("guid")
        self._detail_data.update({"aid": aid, "tag": "article"})
        detail_url = "https://nine.ifeng.com/getNewsDocs"
        resp = self._session.post(detail_url, headers=self._headers, data=self._detail_data)
        num = self._parse_join_num(aid)
        res = json.loads(resp.text)
        fields["platformWorksID"] = res["body"]["documentId"]
        fields["title"] = res["body"]["title"]
        fields["url"] = res["body"]["shareurl"]
        fields["likeNum"] = int(res["body"]["praise"])
        fields["commentNum"] = num
        # 调整covers来源，就是单纯从app上看到文章时的情况
        if "realimg" in res["body"].keys():
            fields["covers"] = [res["body"]["realimg"]]
        # 以下covers作为判断文章类型依据
        covers = []
        if res["body"]["img"]:
            covers = [i["url"] for i in res["body"]["img"]]
        if "hasVideo" in res["body"].keys():
            vid_url = res["body"]["videos"][0]["thumbnail"]
            img_url = res["body"]["videos"][0]["video"]["Normal"]["src"]
            # <!-- IFENG_DOC_VIDEO -->
            context = res["body"]["text"]
            vid = f"<div><video src=\"{vid_url}\" poster=\"{img_url}\" " \
                  f"controls=\"controls\"></video></div>"
            context = context.replace("<!-- IFENG_DOC_VIDEO -->", vid)
            fields["contentType"] = 3
        else:
            context = res["body"]["text"]
        if fields["contentType"] != 3:
            if len(covers) != 0:
                fields["contentType"] = 2
        fields["content"] = context
        fields["pubTime"] = fields["pubTime"] * 1000
        fields["createTime"] = int(time.time() * 1000)
        fields["updateTime"] = int(time.time() * 1000)
        return fields

    def _parse_works_video_article(self, tag, follow_id, field):
        self._params_data.update({"tag": tag, "followid": follow_id})
        url = "https://nine.ifeng.com/wemediacontentlist"
        resp = self._session.post(url, headers=self._headers, data=self._params_data)
        res = json.loads(resp.text)
        ret = []
        if res["data"]["feeds"]["list"]:
            for i in res["data"]["feeds"]["list"]:
                fields = dict(dict(), **field)
                try:
                    aid = i["id"]
                    platformID = 'a545ee430b37c5da919ab80e1ec14eed'
                    fields["platformID"] = "a545ee430b37c5da919ab80e1ec14eed"
                    fields["platformName"] = "凤凰新闻手机客户端"
                    fields["_id"] = self.md5(platformID + str(aid))
                    pub_time = i["updateTime"]
                    fields["pubTime"] = int(time.mktime(time.strptime(pub_time, "%Y/%m/%d %H:%M:%S")))
                    if tag == "video":
                        parse_fields = self._parse_works_video_detail(aid, fields)
                        ret.append(parse_fields)
                    elif tag == "article":
                        parse_fields = self._parse_works_article_detail(aid, fields)
                        ret.append(parse_fields)
                    else:
                        fields["platformWorksID"] = aid
                        fields["title"] = i["title"]
                        fields["url"] = i["link"]["weburl"]
                        fields["readNum"] = i["phvideo"]["playTime"]    # 播放数
                        fields["likeNum"] = i["phvideo"]["praise"]    # 点赞数
                        img_url = i["thumbnail"]
                        vid_url = i["phvideo"]["videoPlayUrl"]
                        fields["content"] = f"<div><video src=\"{vid_url}\" poster=\"{img_url}\" " \
                                            f"controls=\"controls\"></video></div>"
                        fields["contentType"] = 3
                        fields["covers"] = [img_url]
                        fields["videos"] = [vid_url]
                        fields["pubTime"] = fields["pubTime"] * 1000
                        fields["createTime"] = int(time.time() * 1000)
                        fields["updateTime"] = int(time.time() * 1000)
                        ret.append(fields)
                except Exception as e:
                    print(e)
                    continue

        return ret

    def app_accounts_works(self, follow_id):
        try:
            accounts = self._parse_accounts(follow_id)
            fields = dict(dict(), **self._default_works_fields)
            fields["accountName"] = accounts["name"]
            fields["accountID"] = accounts["_id"]
            # tag = "video"
            # url = "https://nine.ifeng.com/wemediacontentlist"
            """先视频后文章，因详细那块的参数不同，小视频则不用去详细那块"""
            tag_url = ["video", "article", "miniVideo"]
            result1 = []
            for tag in tag_url:
                try:
                    works = self._parse_works_video_article(tag, follow_id, fields)
                    result1 += works
                except Exception as e:
                    self.logger.warning(f"{e}\n{traceback.format_exc()}")
                    continue
            return dict(
                code=1,
                msg="success",
                total=len(result1),
                data=dict(
                    account=accounts,
                    worksList=result1
                )
            )
            # works_article = self._parse_works_article(follow_id, fields)
        except Exception as e:
            return dict(code=0, msg=str(e))

    def fetch(self, task):
        try:
            res = self.app_accounts_works(task["platformAccountID"])
            return res
        except Exception as e:
            self.logger.warning(f"{e}\n{traceback.format_exc()}")
            return dict(code=0, msg=str(e))


if __name__ == '__main__':
    from loguru import logger
    kw = "河北新闻网"
    uid = FengHuangSearchAccounts().app_search(kw)
    if uid:
        # weMedia_836081
        if uid[0].startswith("weMedia_"):
            result = FengHuangAccountsAndWorks(logger).app_accounts_works(uid[0])
            with open(kw + "res.json", "w", encoding="utf8") as f:
                f.write(json.dumps(result, indent=4, ensure_ascii=False))
        else:
            uuid = "weMedia_" + uid[0]
            FengHuangAccountsAndWorks(logger).app_accounts_works(uid[0])
    else:
        print(f"{kw}搜索无果")
    # logger = ''
    # task = {}
    # result = FengHuangAccountsAndWorks(logger).fetch_batch(task)

