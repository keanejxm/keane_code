# -*- coding:utf-8 -*-
"""

# author: albert
# date: 2020/11/30
# update: 2020/11/30
"""
import hashlib
import json
import time
import traceback

import elasticsearch
import requests

from api.config import es_config
from api_common_utils.base_data import DEFAULT_WORKS_FIELDS, DEFAULT_USER_INFO_FIELDS
from api_common_utils.text_processing_tools import text_remover_html_tag
from spiders.libs.spiders.we_media.we_media_utils import DEFAULT_WE_MEDIA_USER_INFO_FIELDS, \
    DEFAULT_WE_MEDIA_USER_WORKS_FIELDS


class RMRBAPPAuthorWorkSpider:

    def __init__(self, logger):
        self.logger = logger
        self.headers = {
            "Cookie": "acw_tc=\"2760829216063541661914421e44add46bc8978604212b0ff20cdeafab879f\";"
                      "$Path=\"/\";$Domain=\"app.peopleapp.com\"; "
                      "SERVERID=f0c2519d15ca3b0cae13b80f9d03fb94|1606355193|1606354984",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G977N Build/LMY48Z);DailyNewspaper/7.0.2",
            "Host": "app.peopleapp.com", "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Content-Type": "application/x-www-form-urlencoded", "Content-Length": "0"
        }
        self.conn = elasticsearch.Elasticsearch(**es_config)

    @staticmethod
    def parser_num(str_num):
        if '万' in str_num:
            if '.' in str_num:
                str_num = str_num.replace('万', "000").replace('.', '')
            else:
                str_num = str_num.replace('万', "0000")
        return int(str_num)

    @staticmethod
    def md5(unicode_str, charset="UTF-8"):
        """
        字符串转md5格式。
        :return:
        """
        _md5 = hashlib.md5()
        _md5.update(unicode_str.encode(charset))
        return _md5.hexdigest()

    def parse_author_info_data(self, response_text_dict, task):
        data = response_text_dict["data"]
        now = int(time.time() * 1000)
        platformID = task["platformID"]
        platformName = task["platformName"]
        user_info = dict(dict(), **DEFAULT_WE_MEDIA_USER_INFO_FIELDS)
        user_info["_id"] = self.md5(platformID + data["id"])
        user_info["platformAccountID"] = data["id"]
        user_info["name"] = data["name"]
        user_info["avatar"] = data["avatar"]
        user_info["url"] = data["shareUrl"]
        user_info["region"] = data["location"].split('-')
        user_info["platformID"] = platformID
        user_info["platformName"] = platformName
        user_info["platformFansNum"] = self.parser_num(data["subscribe_num"])
        user_info["platformWorksNum"] = self.parser_num(data["article_count"])
        user_info["weMediaName"] = "人民号"
        user_info["createTime"] = now
        user_info["updateTime"] = now
        return user_info

    def get_author_info(self, task):
        url = 'https://app.peopleapp.com/Api/700/GovApi/govInfo'
        data = {
            "city": "武威市",
            "citycode": "1935",
            "device": "79fb30a6-96bf-3785-9cab-b45732bd5b6d",
            "device_model": "SM-G977N",
            "device_os": "Android 5.1.1",
            "device_product": "samsung",
            "device_size": "900*1600",
            "device_type": "1",
            "district": "民勤县",
            "fake_id": "60053152",
            "gov_id": task["platformAccountID"],
            "interface_code": "702",
            "latitude": "39.001706557182644",
            "longitude": "103.56598582515005",
            "province": "甘肃省",
            "province_code": "3234776",
            "user_gov_id": "0",
            "user_id": "0",
            "version": "7.0.2",
        }
        security_key_str = ''
        for key in data.keys():
            security_key_str += data[key] + '|'
        security_key_str = security_key_str[0:-1] + 'rmrbsecurity$#%sut49fbb427a508bcc'
        security_key_str = self.md5(security_key_str)
        data['securitykey'] = security_key_str
        response = requests.post(url=url, data=data, headers=self.headers, verify=False)
        response_text_dict = response.json()
        user_info = self.parse_author_info_data(response_text_dict, task)
        return user_info

    def parse_author_article_list_data(self, response_text_dict, task):
        article_data_list = []
        platformID = task["platformID"]
        platformName = task["platformName"]
        for article in response_text_dict["data"]:
            url = 'https://app.peopleapp.com/Api/700/ArtInfoApi/getArticleData'
            data = {
                "article_id": str(article["id"]),
                "city": "武威市",
                "citycode": "1935",
                "components_id": "0",
                "device": "79fb30a6-96bf-3785-9cab-b45732bd5b6d",
                "device_model": "SM-G977N",
                "device_os": "Android 5.1.1",
                "device_product": "samsung",
                "device_size": "900*1600",
                "device_type": "1",
                "district": "民勤县",
                "fake_id": "60053152",
                "interface_code": "702",
                "latitude": "39.001706557182644",
                "longitude": "103.56598582515005",
                "province": "甘肃省",
                "province_code": "16815966",
                "type": "2",
                "user_gov_id": "0",
                "user_id": "0",
                "version": "7.0.2",
            }
            security_key_str = ''
            for key in data.keys():
                security_key_str += data[key] + '|'
            security_key_str = security_key_str[0:-1] + 'rmrbsecurity$#%sut49fbb427a508bcc'
            security_key_str = self.md5(security_key_str)
            data['securitykey'] = security_key_str

            detail_content = requests.post(url=url, headers=self.headers, data=data, verify=False)
            detail_content_data = detail_content.json()
            cover = ["http://rmrbcmsonline.peopleapp.com" + url for url in article["cover_img"]]
            now = int(time.time() * 1000)
            article_data = dict(dict(), **DEFAULT_WE_MEDIA_USER_WORKS_FIELDS)
            article_data["_id"] = self.md5(platformID + article["id"])
            article_data["platformWorksID"] = article["gov_id"]
            article_data["platformID"] = platformID
            article_data["platformName"] = platformName
            article_data["accountID"] = self.md5(platformID + str(article["gov_id"]))
            article_data["accountName"] = article["copyfrom"]
            article_data["url"] = article["share_url"]
            article_data["authors"] = [article["copyfrom"]]
            article_data["title"] = article["title"]
            article_data["titleWordsNum"] = len(article["title"])
            article_data["html"] = detail_content.text
            content = text_remover_html_tag(detail_content_data["frontend"]["contents"])
            article_data["content"] = content
            article_data["contentWordsNum"] = len(content)
            article_data["digest"] = content[:200]
            article_data["images"] = detail_content_data["frontend"]['image']
            article_data["covers"] = cover
            article_data["videos"] = []
            article_data["readNum"] = self.parser_num(article["read_count"])
            article_data["likeNum"] = self.parser_num(article["likes_count"])
            article_data["commentNum"] = self.parser_num(article["comment_count"])
            article_data["forwardNum"] = self.parser_num(article["share_count"])
            article_data["updateParams"] = json.dumps({"article_id": str(article["id"]), "type": str(article["type"])})
            article_data["contentType"] = 1
            if article_data["images"]:
                article_data["contentType"] = 2
            if article_data["videos"]:
                article_data["contentType"] = 3
            article_data["pubTime"] = int(article["created_time"]) * 1000
            article_data["createTime"] = now
            article_data["updateTime"] = now
            article_data_list.append(article_data)
        return article_data_list

    def get_author_article_list(self, task):
        # 文章2  视频3  小视频4
        url = 'https://app.peopleapp.com/Api/700/GovApi/govArticleList'
        data = {
            "city": "武威市",
            "citycode": "1935",
            "device": "79fb30a6-96bf-3785-9cab-b45732bd5b6d",
            "device_model": "SM-G977N",
            "device_os": "Android 5.1.1",
            "device_product": "samsung",
            "device_size": "900*1600",
            "device_type": "1",
            "district": "民勤县",
            "fake_id": "60053152",
            "gov_id": task["platformAccountID"],
            "interface_code": "702",
            "latitude": "39.001706557182644",
            "longitude": "103.56598582515005",
            "page": "1",
            "province": "甘肃省",
            "province_code": "3351853",
            "refresh_time": "1606357258",
            "show_num": "20",
            "type": "2",
            "user_gov_id": "0",
            "user_id": "0",
            "version": "7.0.2",
        }
        security_key_str = ''
        for key in data.keys():
            security_key_str += data[key] + '|'
        security_key_str = security_key_str[0:-1] + 'rmrbsecurity$#%sut49fbb427a508bcc'
        security_key_str = self.md5(security_key_str)
        data['securitykey'] = security_key_str
        response = requests.post(url=url, headers=self.headers, data=data, verify=False)
        response_text_dict = response.json()
        article_data = self.parse_author_article_list_data(response_text_dict, task)
        return article_data

    def save_account(self, account):
        index_name = 'dc_accounts'
        field_id = account.pop("_id")
        fields = account
        if self.conn.exists(index=index_name, doc_type="_doc", id=field_id):
            # 更新
            res = "存在 "
        else:
            res = self.conn.index(index=index_name, doc_type="_doc", body=fields, id=field_id)
        return res

    def save_works(self, works):
        for work in works:
            index_name = 'dc_works'
            field_id = work.pop("_id")
            if self.conn.exists(index=index_name, doc_type="_doc", id=field_id):
                # 更新
                continue
            fields = work
            res = self.conn.index(index=index_name, doc_type="_doc", body=fields, id=field_id)
            print(f'《{work["platformName"]}-{work["accountName"]}》 存储结果 为 {res}')
        return 'ok'

    def fetch(self, task):
        try:
            account_res = self.get_author_info(task)
            works = self.get_author_article_list(task)
            # save_res = self.save_account(account_res)
            # save_works_res = self.save_works(works)
            return dict(code=1, msg='ok', data={"account": account_res, "worksList": works})
        except Exception as e:
            self.logger.warning(f"{e}\n{traceback.format_exc()}")
            return dict(code=0, msg=str(e))


if __name__ == '__main__':
    # task = {"platformAccountID": "3237", "platformID": "4b11b30ae0ff9ad36ccf4a9e5c055f97", "platformName": "人民日报APP"}
    # RMRBAPPAuthorWorkSpider(logger).run(task)
    pass

