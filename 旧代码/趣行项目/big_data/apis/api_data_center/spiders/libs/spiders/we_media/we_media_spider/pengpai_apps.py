# -*- coding:utf-8 -*-

"""
# author: Chris
# date: 2020/11/26
# update: 2020/11/26
"""
import hashlib
import re
import json
import time
import requests
import traceback

from api_common_utils.base_data import DEFAULT_USER_INFO_FIELDS, DEFAULT_WORKS_FIELDS
from api_common_utils.extract_digest import GetExtractDigest
from spiders.libs.spiders.we_media.we_media_utils import DEFAULT_WE_MEDIA_USER_INFO_FIELDS, \
    DEFAULT_WE_MEDIA_USER_WORKS_FIELDS


def handle_str_number(str_num):
    if str_num:
        if "万" in str_num:
            nums = int(float(str_num.strip("万")) * 10000)
        else:
            nums = int(str_num)
    else:
        nums = 0
    return nums


class PengPaiSearch:

    def __init__(self):
        self._session = requests.Session()
        self._headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; VOG-AL10 Build/HUAWEIVOG-AL10)"
        }
        self._search_data = {
            "WD-VERSION": "8.1.2",
            "WD-UUID": "863064578382402",
            # Dalvik/2.1.0 (Linux; U; Android 5.1.1; VOG-AL10 Build/HUAWEIVOG-AL10) 澎湃新闻/8.1.2
            "WD-UA": "Dalvik%2F2.1.0%20%28Linux%3B%20U%3B%20Android%205.1.1%3B%20VOG-AL10%20Build%2"
                     "FHUAWEIVOG-AL10%29%20%E6%BE%8E%E6%B9%83%E6%96%B0%E9%97%BB%2F8.1.2",
            "WD-CHANNEL": "TX04",
            "PAPER-CLIENT-TYPE": "04",
            "WD-CLIENT-TYPE": "04",
        }

    def app_search(self, kw):
        url = f"https://app.thepaper.cn/clt/jsp/v6/newsearch.jsp?k={kw}&type=7&userType=1"
        resp = self._session.get(url, headers=self._headers, params=self._search_data)
        res = json.loads(resp.text)
        res_name = []
        if res["searchList"]:
            for item in res["searchList"]:
                name = re.findall(r".*>(.*)<.*", item["sname"])[0]
                if name == kw:
                    res_name.append(item["userId"])
                    # 为甚么没用break 因为搜索`新周刊`会有两个结果，一个是媒体一个应该是个人账户
            if len(res_name) == 0:
                print(f"未匹配到与{kw}相同的澎湃号,所以返回搜索结果中第一个")
                res_name = [res["searchList"][0]["userId"]]
        else:
            print("搜索列表为空。【可能是参数需要调整】")
        return res_name


class PengPaiAccountsAndWorks:

    def __init__(self, logger):
        self.logger = logger
        self._session = requests.Session()
        self._headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; VOG-AL10 Build/HUAWEIVOG-AL10)"
        }
        self._search_data = {
            # "WD-VERSION": "8.1.2",
            "WD-UUID": "863064578382402",
            # # Dalvik/2.1.0 (Linux; U; Android 5.1.1; VOG-AL10 Build/HUAWEIVOG-AL10) 澎湃新闻/8.1.2
            # "WD-UA": "Dalvik%2F2.1.0%20%28Linux%3B%20U%3B%20Android%205.1.1%3B%20VOG-AL10%20Build%2"
            #          "FHUAWEIVOG-AL10%29%20%E6%BE%8E%E6%B9%83%E6%96%B0%E9%97%BB%2F8.1.2",
            # "WD-CHANNEL": "TX04",
            # "PAPER-CLIENT-TYPE": "04",
            # "WD-CLIENT-TYPE": "04",
        }

    @staticmethod
    def md5(unicode_str, charset="UTF-8"):
        """
        字符串转md5格式。
        :return:
        """
        _md5 = hashlib.md5()
        _md5.update(unicode_str.encode(charset))
        return _md5.hexdigest()

    def _parse_article_detail(self, vid_flag, art_id):
        # url = f"https://app.thepaper.cn/clt/jsp/v6/new_detail_pph.jsp?c={art_id}"     # 图文稿
        # https://app.thepaper.cn/clt/jsp/v6/sparkerVideoContent.jsp?c=10153109         # 视频
        if vid_flag:
            url = f"https://app.thepaper.cn/clt/jsp/v6/sparkerVideoContent.jsp?c={art_id}"
        else:
            url = f"https://app.thepaper.cn/clt/jsp/v6/new_detail_pph.jsp?c={art_id}"
        resp = self._session.get(url, params=self._search_data, headers=self._headers)
        resp = json.loads(resp.content)
        works_fields = dict(dict(),**DEFAULT_WE_MEDIA_USER_WORKS_FIELDS)
        works_fields["_id"] = self.md5("16589a5b863884ae64845f3dd8c96465" + str(art_id))
        works_fields["platformID"] = "16589a5b863884ae64845f3dd8c96465"
        works_fields["platformName"] = "澎湃号手机客户端"
        works_fields["platformWorksID"] = art_id
        works_fields["accountID"] = resp["content"]["userInfo"]["userId"]
        works_fields["accountName"] = resp["content"]["userInfo"]["name"]
        works_fields["title"] = resp["content"]["name"]
        works_fields["digest"] = resp["content"]["summary"]
        works_fields["accountName"] = resp["content"]["userInfo"]["name"]
        works_fields["createTime"] = int(time.time() * 1000)
        works_fields["updateTime"] = int(time.time() * 1000)
        pub_time = resp["content"]["pubTime"]
        works_fields["pubTime"] = int(time.mktime(time.strptime(pub_time, "%Y-%m-%d %H:%M"))) * 1000
        works_fields["url"] = "https://m.thepaper.cn/newsDetail_forward_" + art_id
        # 调整covers来源，就是单纯从app上看到文章时的情况
        if resp["coverPic"]:
            if resp["coverPic"] != "https://file.thepaper.cn/clt/img/media_wwwbig_v6.png":      # 这是一张澎湃号媒体的图片与新闻本身无关
                works_fields["covers"] = [resp["coverPic"]]
        if "html" in resp["content"].keys():
            works_fields["content"] = resp["content"]["html"]
            digest, content_num = GetExtractDigest().extract(resp["content"]["html"])
            works_fields["digest"] = digest
            works_fields["contentWordsNum"] = content_num
        else:
            video_url = resp["content"]["videos"][0]["url"]
            image_url = resp["coverPic"]
            video = f"<div><video src=\"{video_url}\" poster=\"{image_url}\" controls=\"controls\"></video></div>"
            works_fields["videos"] = [video]
            works_fields["content"] = video
        works_fields["likeNum"] = resp["content"]["praiseTimes"]        # 点赞数
        works_fields["commentNum"] = resp["content"]["interactionNum"]        # 评论数
        """由于分视频与图文，所以更新参数设置为url链接"""
        works_fields["updateParams"] = json.dumps({"url": url}, ensure_ascii=False)
        # 以下covers作为判断文章类型依据
        covers = [i["url"] for i in resp["content"]["images"]]
        if len(works_fields["videos"]) != 0:
            works_fields["contentType"] = 3
        elif len(works_fields["videos"]) == 0 and len(covers) != 0:
            works_fields["contentType"] = 2
        return works_fields

    def _parse_accounts(self, uid):
        url = f"https://app.thepaper.cn/clt/jsp/v6/personalHome.jsp?uid={uid}&userType=1"
        resp = self._session.get(url, params=self._search_data, headers=self._headers)
        resp = json.loads(resp.content)
        account = dict(dict(), **DEFAULT_WE_MEDIA_USER_INFO_FIELDS)
        account["_id"] = self.md5("16589a5b863884ae64845f3dd8c96465" + str(uid))
        account["platformID"] = "16589a5b863884ae64845f3dd8c96465"
        account["platformName"] = "澎湃号手机客户端"
        account["weMediaName"] = "澎湃号"

        account["platformAccountID"] = resp["userInfo"]["userId"]
        account["name"] = resp["userInfo"]["sname"]
        account["avatar"] = resp["userInfo"]["pic"]
        account["url"] = "https://m.thepaper.cn/user_" + resp["userInfo"]["userId"]
        account["region"] = [resp["userInfo"]["area"]]
        account["platformLikesNum"] = handle_str_number(resp["userInfo"]["praiseNum"])
        account["platformFollowsNum"] = handle_str_number(resp["userInfo"]["attentionNum"])
        account["platformFansNum"] = handle_str_number(resp["userInfo"]["fansNum"])
        account["createTime"] = int(time.time() * 1000)
        account["updateTime"] = int(time.time() * 1000)

        # if resp["userInfo"]["sex"]:
        #     account["sex"] = int(resp["userInfo"]["sex"])
        # print(json.dumps(account, indent=4, ensure_ascii=False))
        return account

    def _parse_articles(self, uid):
        url = f"https://app.thepaper.cn/clt/jsp/v6/personalHomeDynamics.jsp?uid={uid}&userType=1&objectType=0"
        # https://app.thepaper.cn/clt/jsp/v6/personalHomeDynamics.jsp?uid=4610021&userType=0&objectType=0
        resp = self._session.get(url, params=self._search_data, headers=self._headers)
        resp = json.loads(resp.content)
        ret = []
        for info in resp["contList"]:
            try:
                art_vid = info["contId"]
                vid_flag = False
                if info["waterMark"]:
                    vid_flag = True
                fields = self._parse_article_detail(vid_flag, art_vid)
                ret.append(fields)
            except Exception as e:
                print(f"{e}.\n{traceback.format_exc()}")
                continue
        return ret

    def run(self, uid):
        try:
            account = self._parse_accounts(uid)
            works = self._parse_articles(uid)
            return dict(
                code=1,
                msg="success",
                total=len(works),
                data=dict(
                    account=account,
                    worksList=works
                )
            )
        except Exception as e:
            return dict(code=0, msg=str(e))

    def fetch(self, task):
        try:
            return self.run(task["platformAccountID"])
        except Exception as e:
            self.logger.warning(f"{e}\n{traceback.format_exc()}")
            return dict(code=0, msg=str(e))


if __name__ == '__main__':
    from loguru import logger
    keyword = "河北新闻网"     # uu = ['3880709']
    # keyword = "陈述根本"        # uu = ['4610021']
    uu = PengPaiSearch().app_search(keyword)
    if uu:
        res = PengPaiAccountsAndWorks(logger).run(uu[0])
        with open(keyword + "result.json", "w", encoding="utf8") as f:
            f.write(json.dumps(res, indent=4, ensure_ascii=False))
    else:
        print("未找到目标")
