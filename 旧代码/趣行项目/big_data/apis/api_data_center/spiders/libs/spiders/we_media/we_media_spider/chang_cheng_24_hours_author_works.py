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
from loguru import logger
from api_common_utils.text_processing_tools import text_remover_html_tag
from spiders.libs.spiders.we_media.we_media_utils import DEFAULT_WE_MEDIA_USER_INFO_FIELDS, \
    DEFAULT_WE_MEDIA_USER_WORKS_FIELDS


class ChangCheng24Hours:

    def __init__(self, logger):
        self.logger = logger
        self.headers = {
            "Accept-Language": "zh-CN,zh;q=0.8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G977N Build/TAS-AN00) m2oSmartCity_267 1.0.0",
            "X-API-TIMESTAMP": "1606381389160kbL97i",
            "X-API-SIGNATURE": "ODFkY2Q1ODFmYmVjZjI4NTU1MzIxMDI2MmI5YTliYmNmNzg0ODg3Mg==",
            "X-API-VERSION": "3.2.0",
            "X-AUTH-TYPE": "sha1",
            "X-API-KEY": "eda80a3d5b344bc40f3bc04f65b7a357",
            "Host": "mapi.hebei.com.cn",
            "Connection": "Keep-Alive", "Accept-Encoding": "gzip",
            "Cookie": "m2o_mapi_hebei_com_cn=eyJpdiI6IlVocjJuXC9VZm1wZ3pXUlYxU2VKRWV3P"
                      "T0iLCJ2YWx1ZSI6IjFzTFwvdmxEZXBod2l6VTk1MG5SS0ZqN2xwOTI0ZXhsUHVQM"
                      "HlBdHZaemloeEZFMVNqSVcyTURnamlsU3oyclc0elpBSHYrK2NtQjZBcFwvVnZYWV"
                      "RpeXc9PSIsIm1hYyI6IjE2ZWU1OGIxMjJkMWRmMDNiYjEwZTBhNTI0YTNmMWViMjMw"
                      "N2IxZmI3NWIxNDhjYTMzOTE5ZTg4MmYwMjc1NmUifQ%3D%3D"}

    @staticmethod
    def md5(unicode_str, charset="UTF-8"):
        """
        字符串转md5格式。
        :return:
        """
        _md5 = hashlib.md5()
        _md5.update(unicode_str.encode(charset))
        return _md5.hexdigest()

    @staticmethod
    def parser_num(str_num):
        if '万' in str_num:
            if '.' in str_num:
                str_num = str_num.replace('万', "000").replace('.', '')
            else:
                str_num = str_num.replace('万', "0000")
        return int(str_num)

    def parse_author_info_data(self, response_text_dict):
        data = response_text_dict["data"]
        user_info = dict(dict(), **DEFAULT_WE_MEDIA_USER_INFO_FIELDS)
        now = int(time.time() * 1000)
        platformID = "221c7a69b782c486c269e62028f2a24f"
        platformName = "长城24小时APP"
        user_info["_id"] = self.md5(platformID + str(data["site_id"]))
        user_info["platformAccountID"] = str(data["site_id"])
        user_info["name"] = data["name"]
        user_info["avatar"] = data["indexpic"]["host"] + data["indexpic"]["filename"]
        user_info["url"] = data["content_url"]
        user_info["region"] = ['河北', data["areas"]["name"]]
        user_info["types"] = [7]
        user_info["platformID"] = platformID
        user_info["platformName"] = platformName
        user_info["platformReadsNum"] = self.parser_num(str(data["article_click_num"]))
        user_info["platformWorksNum"] = self.parser_num(str(data["article_num"]))
        user_info["platformType"] = 7
        user_info["weMediaName"] = "长城号"
        user_info["createTime"] = now
        user_info["updateTime"] = now
        return user_info

    def get_author_info(self, site_id):
        url = f'http://mapi.hebei.com.cn/api/v1/subscribe/{site_id}'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
        }
        response = requests.get(url=url, headers=headers)
        response_text_dict = response.json()
        user_info = self.parse_author_info_data(response_text_dict)
        return user_info

    def parse_author_article_list_data(self, response_text_dict):
        article_data_list = []
        for article in response_text_dict:
            try:
                url = f'http://mapi.hebei.com.cn/api/v1/item.php?id={article["id"]}'
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
                }
                detail_content = requests.get(url=url, headers=headers)
                detail_content_data = detail_content.json()
                content_type = 1
                if '.jpg' in detail_content.text:
                    content_type = 2
                if '.mp4' in detail_content.text:
                    content_type = 3
                now = int(time.time() * 1000)
                platformID = '221c7a69b782c486c269e62028f2a24f'
                platformName = '长城24小时APP'
                article_data = dict(dict(), **DEFAULT_WE_MEDIA_USER_WORKS_FIELDS)
                article_data["_id"] = self.md5(platformID + str(article["id"]))
                article_data["platformWorksID"] = str(article["id"])
                article_data["platformID"] = platformID
                article_data["platformName"] = platformName
                article_data["accountID"] = self.md5(platformID + str(article["origin_site_id"]))
                article_data["accountName"] = article["author"]
                article_data["url"] = f"http://v.hebei.com.cn/ccw/detail/news.php?rid={article['id']}"
                article_data["authors"] = [article["author"]]
                article_data["title"] = article["title"]
                article_data["titleWordsNum"] = len(article["title"])
                # article_data["html"] = detail_content.text
                content = text_remover_html_tag(detail_content_data["content"])
                article_data["content"] = content
                article_data["contentWordsNum"] = len(content)
                article_data["digest"] = content[:200]
                article_data["covers"] = [article["index_pic"]]
                article_data["videos"] = [re.compile('"video_url":"(.*?)"').findall(detail_content.text)[0]] if re.compile('"video_url":"(.*?)"').findall(detail_content.text) else []
                article_data["readNum"] = article["click_num"]
                article_data["likeNum"] = article["column_praise_num"]
                article_data["commentNum"] = article["column_comment_num"]
                article_data["forwardNum"] = article["column_share_num"]
                article_data["updateParams"] = json.dumps({"article_id": str(article["id"])})
                article_data["contentType"] = content_type
                article_data["pubTime"] = int(article["publish_time_stamp"]) * 1000
                article_data["createTime"] = now
                article_data["updateTime"] = now
                article_data_list.append(article_data)
            except Exception as e:
                continue
        return article_data_list

    def get_author_article_list(self, site_id):
        url = f'http://mapi.hebei.com.cn/api/v1/contents.php?site_id={site_id}'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
        }
        response = requests.get(url=url, headers=headers)
        response_text_dict = response.json()
        article_list = self.parse_author_article_list_data(response_text_dict)
        return article_list

    def run(self, site_id):
        account_res = self.get_author_info(site_id)
        works = self.get_author_article_list(site_id)
        return dict(code=1, msg='ok', data={"account": account_res, "worksList": works})

    def fetch(self, task):
        try:
            res = self.run(task["platformAccountID"])
            return res
        except Exception as e:
            self.logger.warning(f"{e}\n{traceback.format_exc()}")
            return dict(code=0, msg=str(e))


if __name__ == '__main__':
    site_id = "790"
    ChangCheng24Hours(logger).run(site_id)

