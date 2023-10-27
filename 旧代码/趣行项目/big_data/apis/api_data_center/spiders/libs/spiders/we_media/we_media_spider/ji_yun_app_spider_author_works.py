# -*- coding:utf-8 -*-
"""

# author: albert
# date: 2020/11/30
# update: 2020/11/30
"""

import json
import re
import time
import hashlib
import traceback

import requests

from api_common_utils.text_processing_tools import text_remover_html_tag
from spiders.libs.spiders.we_media.we_media_utils import DEFAULT_WE_MEDIA_USER_WORKS_FIELDS, \
    DEFAULT_WE_MEDIA_USER_INFO_FIELDS


class JIYUNAuthorAndWork:

    def __init__(self, logger):
        self.logger = logger

    @staticmethod
    def md5(unicode_str, charset="UTF-8"):
        """
        字符串转md5格式。
        :return:
        """
        _md5 = hashlib.md5()
        _md5.update(unicode_str.encode(charset))
        return _md5.hexdigest()

    def parse_author_info_data(self, response_text_dict):
        """

        {'answerNum': 0, 'backgroundPic': '', 'city': '石家庄市', 'cityCode': '130100', 'code': 'sjzqxjc', 'contentCount': 141, 'county': '', 'countyCode': '', 'createWay': 0, 'createtime': '2020-10-29 12:33:31', 'description': '<p class="MsoNormal" align="center" style="text-align: left;"><span>开展检察宣传，树立检察形象，获取社情民意，</span>推动政民互动，建设服务社会大众的新平台<font face="微软雅黑">。</font></p>', 'email': 'zzcxjp@163.com', 'followCount': 1, 'groupCodes': '', 'groupId': '', 'groups': [{'PSort': 0, 'code': 'jianchayuanhao', 'createtime': None, 'id': 'a517dd3022ca4f5493090120a601a0f1', 'isShow': 0, 'logo': '', 'longcode': '', 'name': '检察院号', 'pid': '', 'siteId': '', 'sort': 0}, {'PSort': 0, 'code': 'jvzhenhao', 'createtime': None, 'id': '480d08791ef543c9a251f83c359fd9d7', 'isShow': 0, 'logo': '', 'longcode': '', 'name': '矩阵号', 'pid': '', 'siteId': '', 'sort': 0}], 'id': 'c2a6730b03b941ad8df06610d27344aa', 'idNumber': '', 'identityFile1': '', 'identityFile2': '', 'isCheck': 1, 'isComment': 1, 'isContentPayment': 0, 'isEnable': 1, 'isPublishable': 1, 'isRecommended': 0, 'isShare': 0, 'isShield': 0, 'isSubscribe': 0, 'isVipAuthentication': 0, 'level': 2, 'logo': 'https://jiyun.hebyun.com.cn/ugc/mp/media/icon/2020/10/29/0f0c0eb5468a4e24a6b8f9f543c02663.png', 'mediaSeq': 148545, 'mediaType': 3, 'name': '石家庄桥西检察', 'orgId': 'c4c73e61045343afa4cb8dcc15279ceb', 'orgName': '', 'personnalSign': '', 'phone': '15175177089', 'praiseCount': 0, 'province': '河北省', 'provinceCode': '130000', 'rank': '', 'rdSort': 0, 'realName': '', 'sendImmsg': 0, 'serviceList': [{'code': 'picTxt', 'flag': '1', 'name': '图文', 'id': '11', 'rule': []}, {'code': 'media', 'flag': '1', 'name': '音视频', 'id': '14,15', 'rule': []}, {'code': 'verticalVideo', 'flag': '1', 'name': '随手拍', 'id': '13', 'rule': []}, {'code': 'MESSAGE', 'id': '43', 'name': '留言', 'rule': [], 'type': 0}], 'shareCount': 0, 'siteId': 'd78cdde3a4b0442eb8e4298ca4bc6473', 'sort': 8523, 'sortLevel': 0, 'sourceType': '1', 'subscribeCount': 3, 'telephone': '', 'visitCount': 9, 'visitUrl': 'https://jiyun.hebyun.com.cn/html/mediaDetail.html?mediaId=c2a6730b03b941ad8df06610d27344aa&siteId=d78cdde3a4b0442eb8e4298ca4bc6473', 'status': '200', 'msg': '操作成功'}
        """
        data = response_text_dict
        user_info = dict(dict(), **DEFAULT_WE_MEDIA_USER_INFO_FIELDS)
        platformID = "a57898f079a79fd82acbc8652a4b4777"
        platformName = "冀云APP"
        now = int(time.time() * 1000)
        user_info["_id"] = self.md5(platformID + data["id"])
        user_info["platformAccountID"] = data["id"]
        user_info["name"] = data["name"]
        user_info["avatar"] = data["logo"]
        user_info["url"] = data["visitUrl"]
        user_info["region"] = [data["city"]]
        user_info["types"] = [7]
        user_info["platformID"] = platformID
        user_info["platformName"] = platformName
        user_info["platformFansNum"] = int(data["visitCount"])
        user_info["platformWorksNum"] = int(data["contentCount"])
        user_info["platformLikesNum"] = int(data["praiseCount"])
        user_info["platformType"] = 7
        user_info["weMediaName"] = "冀云号"
        user_info["createTime"] = now
        user_info["updateTime"] = now
        return user_info

    def get_author_info(self, media_id):
        url = 'https://jiyun.hebyun.com.cn/mpapi/api/mp/media/getMediaInfoV2'
        data = {
            "mediaId": media_id,
            "appId": "449dcad9ce8a3618a03979e536cc292f",
            "currentTimeMillis": str(int(time.time() * 1000)),
            "platform": "android",
            "siteId": "d78cdde3a4b0442eb8e4298ca4bc6473",
        }
        md5_str = f'{data["currentTimeMillis"]}27f1d25a32714282abd077212c6d824e{data["appId"]}android{data["mediaId"]}{data["siteId"]}'
        sign = self.md5(md5_str)
        data["signature"] = sign
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "jiyun.hebyun.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.11.0",
        }
        response = requests.post(url=url, data=data, headers=headers, verify=False)
        response_text_dict = response.json()
        user_info = self.parse_author_info_data(response_text_dict)
        return user_info

    def parse_author_article_list_data(self, response_text_dict):
        article_data_list = []
        for article in response_text_dict["list"]:

            article_data = article["data"]
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
            }
            detail_content = requests.get(url=article_data["url"], headers=headers, verify=False)
            detail_content_data = detail_content.text
            content_type = 1
            if '.jpg' in detail_content.text:
                content_type = 2
            if '.mp4' in detail_content.text:
                content_type = 3
            now = int(time.time() * 1000)
            article_data = dict(dict(), **DEFAULT_WE_MEDIA_USER_WORKS_FIELDS)
            platformID = "a57898f079a79fd82acbc8652a4b4777"
            platformName = "冀云APP"
            article_data["_id"] = self.md5(platformID + article["id"])
            article_data["platformWorksID"] = article["id"]
            article_data["platformID"] = platformID
            article_data["platformName"] = platformName
            article_data["platformType"] = 7
            article_data["accountID"] = self.md5(platformID + str(article["gov_id"]))
            article_data["accountName"] = article_data['mediaName']
            article_data["url"] = article_data['url']
            article_data["authors"] = [article["copyfrom"]]
            article_data["title"] =  article_data["title"]
            article_data["titleWordsNum"] = len(article["title"])
            article_data["html"] = detail_content.text
            content = text_remover_html_tag(detail_content_data)
            article_data["content"] = content
            article_data["contentWordsNum"] = len(content)
            article_data["digest"] = content[:200]
            article_data["images"] = []
            article_data["covers"] = [article_data['mCoverImg']]
            article_data["videos"] = []
            # article_data["readNum"] = article_data['contentType']
            article_data["likeNum"] = article_data['praiseCount']
            article_data["commentNum"] = article_data['commentCount']
            article_data["forwardNum"] = article_data['shareCount']
            article_data["updateParams"] = json.dumps({"article_id": str(article_data["id"])}),
            article_data["contentType"] = content_type
            article_data["pubTime"] = int(time.mktime(time.strptime(article_data['createtime'], "%Y-%m-%d %H:%M:%S"))) * 1000,
            article_data["createTime"] = now
            article_data["updateTime"] = now
            article_data_list.append(article_data)
        return article_data_list

    def get_author_article_list(self, media_id):
        url = 'https://jiyun.hebyun.com.cn/mpapi/api/mp/content/getContentListByType'
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "jiyun.hebyun.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.11.0",
        }
        data = {
            "contentTypes": "11,15",
            "isOwner": "0",
            "mediaId": media_id,
            "pageNum": "1",
            "pageSize": "10",
            "appId": "2e3045ac416432dab1ed6e0c81f0d8ab",
            "currentTimeMillis": "1606441039062",
            "platform": "android",
            "siteId": "d78cdde3a4b0442eb8e4298ca4bc6473",
        }
        md5_str = f'{data["isOwner"]}{data["pageNum"]}{data["pageSize"]}{data["contentTypes"]}{data["currentTimeMillis"]}27f1d25a32714282abd077212c6d824e{data["appId"]}android{data["mediaId"]}{data["siteId"]}'
        sign = self.md5(md5_str)
        data["signature"] = sign
        response = requests.post(url=url, data=data, headers=headers, verify=False)
        response_text_dict = response.json()
        article_list = self.parse_author_article_list_data(response_text_dict)
        return article_list

    def run(self, media_id):
        account_res = self.get_author_info(media_id)
        works = self.get_author_article_list(media_id)
        return dict(code=0, msg='ok', data={"account": account_res, "worksList": works})

    def fetch(self, task):
        try:
            return self.run(task["platformAccountID"])
        except Exception as e:
            self.logger.warning(f"{e}\n{traceback.format_exc()}")
            return dict(code=0, msg=str(e))


if __name__ == '__main__':
    from loguru import logger
    media_id = "c2a6730b03b941ad8df06610d27344aa"
    JIYUNAuthorAndWork(logger).fetch(media_id)

