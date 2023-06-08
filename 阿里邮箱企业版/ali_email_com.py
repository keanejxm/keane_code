#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  ali_email_com.py
:time  2023/6/7 17:18
:desc  
"""
import os
import time
import re
import traceback
import io
import logging
import requests
import json
import base64
from lxml import etree
from urllib.parse import urlparse
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA

QIYE_HOST = "https://qiye.aliyun.com"


class AliEmailCom:
    def __init__(self, account, password):
        self._logger = self.logger_custom()
        self._file_path = os.path.dirname(__file__)
        self.session = requests.Session()
        self.session.cookies.update(self._read_cookie(f"{self._file_path}/cookie_files/qiye_cookie"))
        self._account = account
        self._password = password
        self.name = None
        self.csrf_token = None
        self.root_token = None
        self.attach_token = None

    # 自定义日志文件
    @staticmethod
    def logger_custom():
        """"""
        logger_name = "logger_files"
        log_path = os.path.dirname(__file__)
        if not logger_name or not isinstance(logger_name, str):
            raise ValueError(f"logger_name是空值或者logger_name类型错误")
        normal_format = '%(asctime)s - %(process)d/%(thread)d [%(module)s:%(lineno)d] %(levelname)s: %(message)s'
        # 即在控制台输出，输出文件
        if log_path:
            logger_path = os.path.join(log_path, logger_name)
            os.makedirs(logger_path, mode=0o755, exist_ok=True)
            log_file_name = os.path.join(logger_path, f"{logger_name}.log")
            formatter = logging.Formatter(normal_format)
            log = logging.getLogger(logger_name)
            log.setLevel(level=logging.INFO)
            handler = logging.FileHandler(log_file_name)
            handler.setLevel(level=logging.INFO)
            handler.setFormatter(formatter)
            console = logging.StreamHandler()
            console.setLevel(level=logging.INFO)
            # console.setFormatter(formatter)
            log.addHandler(handler)
            log.addHandler(console)
            return log

    @staticmethod
    def _read_cookie(file_path):
        with open(file_path, "r", encoding="utf-8") as r:
            try:
                cookie_dict = json.loads(r.readlines()[0])
                return cookie_dict
            finally:
                r.close()

    def _get_cookie(self):
        cookie_dict = requests.utils.dict_from_cookiejar(self.session.cookies)
        return cookie_dict

    @staticmethod
    def _python_encrypt(password, public_key):
        """"""
        public_key = public_key
        public_key = '-----BEGIN PUBLIC KEY-----\n' + public_key + '\n-----END PUBLIC KEY-----'
        rsa_key = RSA.import_key(public_key)
        cipher = Cipher_pksc1_v1_5.new(rsa_key)
        cipher_text = base64.b64encode(cipher.encrypt(password.encode("utf8")))
        return cipher_text.decode("utf8")

    @staticmethod
    def _headers(url):
        headers = {
            "Host": urlparse(url).netloc,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113."
                          "0.0.0 Safari/537.36"
        }
        return headers

    # 进入阿里邮箱页面
    def _host_ali(self):
        """"""
        headers = self._headers(QIYE_HOST)
        res = self.session.get(QIYE_HOST, headers=headers)
        if res.status_code == requests.codes.ok:
            res_html = etree.HTML(res.text)
            iframe_url = res_html.xpath("//iframe[@class='login_panel_iframe']/@src")
            if iframe_url:
                return iframe_url[0].replace("&amp", "")
            else:
                a_url = res_html.xpath("//input[@id='reurl']/@value")
                return a_url[0]
        else:
            raise ValueError(f"进入阿里邮箱企业版页面失败")

    def _get_url_login_index(self, url_oauth):
        """
        通过url得到url,请求302
        :param url_login_oauth:
        :return:
        """
        headers = self._headers(url_oauth)
        headers["Referer"] = QIYE_HOST
        res = self.session.get(url_oauth, headers=headers, allow_redirects=False)
        url_login_index = res.headers["Location"]
        return url_login_index

    def _get_page_info(self, state, refer_url):
        """
        获取网页信息，包含忘记密码的网址，和密码加密的值
        :param state:
        :return:
        """
        url = f"{QIYE_HOST}/rpc/v2/login/options?state={state}"
        headers = self._headers(url)
        headers["Referer"] = refer_url
        res = self.session.get(url, headers=headers)
        if res.status_code == requests.codes.ok:
            res_json = json.loads(res.content)
            return res_json
        else:
            raise ValueError(f"获取网页信息请求错误")

    def get_captcha_url(self, refer_url, state):
        """
        获取图片验证码
        :return:
        """
        url = f"{QIYE_HOST}/rpc/v2/authentication/captcha"
        headers = self._headers(url)
        headers["Referer"] = refer_url
        data = {
            "scenario": "authPassword",
            "state": state
        }
        res = self.session.post(url, headers=headers, json=data)
        if res.status_code == requests.codes.ok:
            res_json = json.loads(res.content)
            # {"captchaKey":"","captchaRequired":false,"captchaURL":"","data":{},"type":""}
            return res_json
        else:
            raise ValueError(f"获取验证码请求失败")

    def _data_challenge_password(self, state, pubkey, device_id):
        """"""
        data = {
            "userEmail": self._account,
            "state": state,
            "type": "PASSWORD",
            "challengeValue": {
                "captcha": {},
                "password": self._python_encrypt(self._password, pubkey)},
            "deviceId": {
                "type": "UMID",
                "value": device_id
            }}
        return data

    @staticmethod
    def _data_challenge_sms(state, device_id, phone_code):
        """"""
        data = {
            "type": "SMS",
            "state": state,
            "deviceId": {
                "type": "UMID",
                "value": device_id},
            "challengeValue": {
                "sms": phone_code
            },
            "trustThisDevice": True
        }
        return data

    def _challenge_login(self, refer_url, data, token=None):
        """
        登录邀请
        :return:
        """
        self._logger.info(f"开始登录邀请")
        url = f"{QIYE_HOST}/rpc/v2/login/challenge"
        headers = self._headers(url)
        headers["Referer"] = refer_url
        headers["Origin"] = QIYE_HOST
        if token:
            headers["Authorization"] = f"Bearer {token}"
        res = self.session.post(url, headers=headers, json=data)
        if res.status_code == requests.codes.ok:
            res_json = json.loads(res.content)
            return res_json
        else:
            raise ValueError(f"登录邀请请求失败")

    def _theme_ui(self, url):
        headers = self._headers(url)
        headers["Referer"] = url
        res = self.session.get(url, headers=headers)
        if res.status_code == requests.codes.ok:
            return True
        else:
            return False

    def _internal_actions(self, refer_url, state):
        """"""
        url = f"{QIYE_HOST}/rpc/v2/login/internal/getAdditionalActions?state={state}"
        headers = self._headers(url)
        headers["Referer"] = refer_url
        res = self.session.get(url, headers=headers)
        if res.status_code == requests.codes.ok:
            res_json = json.loads(res.content)
            return res_json
        else:
            raise ValueError(f"第二次获取token失败")

    def _login_user(self, refer_url, token):
        url = f"{QIYE_HOST}/rpc/v2/login/user"
        headers = self._headers(url)
        headers["Referer"] = refer_url
        headers["Authorization"] = f"Bearer {token}"
        res = self.session.get(url, headers=headers)
        if res.status_code == requests.codes.ok:
            res_json = json.loads(res.content)
            return res_json
        else:
            raise ValueError(f"获取登录url请求错误")

    def _get_phone(self, refer_url, token):
        """
        获取用户手机号
        :param refer_url:
        :param token:
        :return:
        """
        url = f"{QIYE_HOST}/rpc/v2/me/authentication/phoneMethods"
        headers = self._headers(url)
        headers["Referer"] = refer_url
        headers["Authorization"] = f"Bearer {token}"
        res = self.session.get(url, headers=headers)
        if res.status_code == requests.codes.ok:
            res_json = json.loads(res.content)
            return res_json["phoneMethods"]
        else:
            raise ConnectionError("获取手机号请求错误")

    # 发送手机验证码
    def _send_phone_captcha(self, refer_url, token):
        """
        发送手机验证码
        :return:
        """
        url = f"{QIYE_HOST}/rpc/v2/me/authentication/phoneMethods/sendSmsOTP"
        headers = self._headers(url)
        headers["Referer"] = refer_url
        headers["Authorization"] = f"Bearer {token}"
        data = {"scenario": "login"}
        res = self.session.post(url, headers=headers, json=data)
        if res.status_code == requests.codes.ok:
            return True
        else:
            raise ConnectionError("发送手机验证码请求失败")

    def _login_continue(self, token, refer_url, state):
        """
        继续登录流程获取一个重定向的url
        :return:
        """
        url = f"{QIYE_HOST}/rpc/v2/login/continue"
        headers = self._headers(url)
        headers["Authorization"] = f"Bearer {token}"
        headers["Referer"] = refer_url
        headers["Origin"] = QIYE_HOST
        data = {"state": state}
        res = self.session.post(url, headers=headers, json=data)
        if res.status_code == requests.codes.ok:
            res_json = json.loads(res.content)
            return res_json["redirectURL"]
        else:
            raise ConnectionError("继续登录失败")

    def _callback_core(self, url, refer_url):
        """"""
        headers = self._headers(url)
        headers["Referer"] = refer_url
        res = self.session.get(url, headers=headers, allow_redirects=False)
        return res.headers["Location"]

    def _index(self, url, refer_url):
        """
        请求主页面，在主页面中获取root_token
        :return:
        """
        headers = self._headers(url)
        headers["Referer"] = refer_url
        res = self.session.get(url, headers=headers)
        if res.status_code == requests.codes.ok:
            res_html = etree.HTML(res.text)
            root_token = res_html.xpath("//input[@id = 'browser_log_browser']/@value")
            if root_token:
                return str(root_token[0])
            else:
                return None
        else:
            raise ConnectionError("主页请求错误")

    def get_time_refresh_data(self, refer_url, csrf_token, root_token):
        """"""
        url = f"{QIYE_HOST}/alimail/ajax/navigate/getTimerRefreshData.txt?_timestamp_={int(time.time() * 1000)}"
        headers = self._headers(url)
        headers["Referer"] = refer_url
        headers["Origin"] = QIYE_HOST
        data = {
            "reset": "1",
            "sessionMode": "0",
            "_csrf_token_": csrf_token,
            "_root_token_": root_token,
            "_refer_hash_": "",
            "_tpl_": "DEFAULT"
        }
        res = self.session.post(url, headers=headers, data=data)
        if res.status_code == requests.codes.ok:
            res_json = json.loads(res.content)
            return res_json
        else:
            raise ConnectionError("请求刷新数据错误")

    # 2023年5月31日阿里邮箱更新
    def _update_version(self):
        """"""
        url = f"{QIYE_HOST}/alimail/updateVersion?t=&h="
        headers = self._headers(url)
        headers["Referer"] = f"{QIYE_HOST}/alimail/"
        res = self.session.get(url, headers=headers)
        if res.status_code == requests.codes.ok:
            return True

    def login(self):
        """
        登录邮箱
        :return:
        """
        url_oauth = self._host_ali()
        if url_oauth != "/alimail/":
            state = [i.split("=") for i in urlparse(url_oauth).query.split("&") if "state" in i][0][1]
            device_id = [i.split("=") for i in urlparse(url_oauth).query.split("&") if "device_id" in i]
            device_id = device_id[0][1] if device_id else ""
            url_login_index = self._get_url_login_index(url_oauth)
            # 获取页面以及密码加密信息，,用来获取到密码公钥，对密码进行加密
            page_info = self._get_page_info(state, url_login_index)
            pubkey = page_info["authenticationMethods"]["password"]["encryptionPublicKey"]
            captcha_info = self.get_captcha_url(url_login_index, state)
            if "captchaKey" in captcha_info and captcha_info:
                # 需要输入验证码 TODO:此处适用于有图片验证码的情况，暂时没用到，碰到后补全
                pass
            # 发送登录邀请
            account_data = self._data_challenge_password(state, pubkey, device_id)
            challenge_info = self._challenge_login(url_login_index, account_data)
            if "redirectURL" not in challenge_info:
                res = self._theme_ui(url_login_index)
                internal_info = self._internal_actions(url_login_index, state)
                token = internal_info["temporaryAccessToken"]
                user_info = self._login_user(url_login_index, token)
                phone_info = self._get_phone(url_login_index, token)
                if self._send_phone_captcha(url_login_index, token):
                    phone_code = input("请输入手机验证码：")
                else:
                    phone_code = None
                # 使用手机验证码登录
                data_sms = self._data_challenge_sms(state, device_id, phone_code)
                challenge_info = self._challenge_login(url_login_index, data_sms, token)
                token = challenge_info["temporaryAccessToken"]
                redirect_url = self._login_continue(token, url_login_index, state)
            else:
                redirect_url = challenge_info["redirectURL"]
            url_index = self._callback_core(redirect_url, url_login_index)
            # 版本更新
            root_token = self._index(url_index, url_login_index)
            update_version = self._update_version()
        else:
            url_index = f"{QIYE_HOST}{url_oauth}"
            url_login_index = QIYE_HOST
        # 请求url_index获取root_token
        cookie_dict = self._get_cookie()
        print(cookie_dict)
        root_token = self._index(url_index, url_login_index)
        cookie_dict = self._get_cookie()
        print(cookie_dict)
        csrf_token = cookie_dict["_csrf_token_"]
        res = self.get_time_refresh_data(url_index, csrf_token, root_token)
        self.attach_token = res["attachToken"]
        cookie_dict = self._get_cookie()
        self.csrf_token = csrf_token
        browser_log = self.browser_log(url_index, csrf_token)
        self.get_shortcut_list(url_index,csrf_token,root_token)
        ali_file_content = json.dumps(cookie_dict)
        ali_file_path = f"{self._file_path}/cookie_files/qiye_cookie"
        # self._save_cookie(ali_file_path, ali_file_content)

        return True

    def browser_log(self, refer_url, csrf_token):
        """更新tooken"""
        url = f"{QIYE_HOST}/alimail/ajax/error/browserLog.txt?_timestamp_={int(time.time() * 1000)}"
        headers = self._headers(url)
        headers["Origin"] = QIYE_HOST
        headers["Referer"] = refer_url
        data = {
            "_root_token_": "dC00Nzg5NzEtcGxxS05X7739",
            "key": "",
            "text": f"[CSRF_UPDATE] New: [{csrf_token}] Old: [{csrf_token}]",
            "level": "info"
        }
        res = self.session.post(url, headers=headers, data=data)
        if res.status_code == requests.codes.ok:
            res_json = json.loads(res.content)
            return True
        else:
            raise ConnectionError("请求错误")

    def get_shortcut_list(self, refer_url, csrf_token, root_token):
        url = f"{QIYE_HOST}/alimail/ajax/navigate/getShortcutList.txt?_timestamp_={int(time.time() * 1000)}"
        data = {
            "_csrf_token_": csrf_token,
            "_root_token_": root_token,
            "_refer_hash_": "",
            "_tpl_": "DEFAULT"
        }
        headers = self._headers(url)
        headers["Origin"] = QIYE_HOST
        headers["Referer"] = refer_url
        res = self.session.post(url, headers=headers, data=data)
        if res.status_code == requests.codes.ok:
            res_json = json.loads(res.content)

    # 保存cookie信息
    def _save_cookie(self, file_path, file_content):
        """"""
        with open(file_path, "w") as w:
            try:
                w.write(file_content)
            finally:
                w.close()


# 读取邮件
class ReadEmailList:
    def __init__(self, login_user: AliEmailCom, logger):
        self._login_user = login_user
        self._logger = logger

    @staticmethod
    def _headers(url):
        headers = {
            "Host": urlparse(url).netloc,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113."
                          "0.0.0 Safari/537.36"
        }
        return headers

    # 获取邮箱分组
    def get_group_email(self):
        """"""
        url = f"{QIYE_HOST}/alimail/ajax/navigate/getMailNavData.txt?_timestamp_={int(time.time() * 1000)}"
        headers = self._headers(url)
        headers["Origin"] = QIYE_HOST
        headers["Referer"] = f"{QIYE_HOST}/alimail/"
        data = {
            "queryFolder": "1",
            "queryTag": "1",
            "queryStack": "1",
            "_csrf_token_": self._login_user.csrf_token,
            "_root_token_": self._login_user.root_token,
            "_refer_hash_": "",
            "_tpl_": "DEFAULT"
        }
        res = self._login_user.session.post(url, headers=headers, data=data)
        print(res)

    def _update_setting(self):
        """
        更新配置
        :return:
        """
        url = f"{QIYE_HOST}/alimail/ajax/settingsGeneral/updateSettings.txt?_timestamp_={int(time.time() * 1000)}"
        headers = self._headers(url)
        headers["Origin"] = QIYE_HOST
        headers["Referer"] = f"{QIYE_HOST}/alimail/"
        data = {
            "allSettings": json.dumps({"navCollapseStatus": 134217728}),
            "_csrf_token_": self._login_user.csrf_token,
            "_root_token_": self._login_user.root_token,
            "_refer_hash_": "",
            "_tpl_": "DEFAULT"
        }
        res = self._login_user.session.post(url, headers=headers, data=data)
        if res.status_code == requests.codes.ok:
            res_json = json.loads(res.content)
        else:
            raise ConnectionError(f"更新配置请求失败")

    # 读取邮件
    def read_email(self, offset=0, folder_ids=("2", "120")):
        """
        读取邮件列表
        :return:
        """
        for folder_id in folder_ids:
            self._update_setting()
            url = f"{QIYE_HOST}/alimail/ajax/mail/queryMailList.txt?_timestamp_={int(time.time() * 1000)}"
            headers = self._headers(url)
            headers["Origin"] = QIYE_HOST
            headers["Referer"] = f"{QIYE_HOST}/alimail/"
            data = {
                "showFrom": "1",
                "query": json.dumps({"folderIds": [folder_id]}, ensure_ascii=False),
                "fragment": "1",
                "offset": str(offset),
                "length": "25",
                "curIncrementId": "0",
                "forceReturnData": "1",
                "_csrf_token_": self._login_user.csrf_token,
                "_root_token_": self._login_user.root_token,
                "_refer_hash_": "",
                "_tpl_": "DEFAULT",
            }
            res = self._login_user.session.post(url, headers=headers, data=data)
            if res.status_code == requests.codes.ok:
                res_json = json.loads(res.content)
                if "dataList" in res_json:
                    for mail_info in res_json["dataList"]:
                        try:
                            mail_id = mail_info["mailId"]
                            receive_time = time.strftime("%Y-%m-%d %H:%M",
                                                         time.localtime(mail_info["timestamp"] / 1000))
                            mail_title = mail_info.get("encSubject")
                            self._logger.info(f"开始获取名为【{mail_title}】的内容")
                            detail_info = self._read_email_detail(mail_id)
                            detail_info["emailID"] = mail_id
                            detail_info["emailTitle"] = mail_title
                            detail_info["receiveTime"] = receive_time
                            yield detail_info
                        except Exception as e:
                            self._logger.info(f"{e}\n{traceback}")
                else:
                    yield None
            else:
                raise ValueError(f"获取邮件列表失败")

    # 读取邮件详细信息
    def _read_email_detail(self, email_id):
        now = int(time.time() * 1000)
        url = f"{QIYE_HOST}/alimail/ajax/mail/loadMail.txt?_timestamp_={now}"
        headers = {
            "Host": "qiye.aliyun.com",
            "Origin": QIYE_HOST,
            "Referer": f"{QIYE_HOST}/alimail/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "X-CSRF-TOKEN": self._login_user.csrf_token,
        }
        data = {
            "mailId": email_id,
            "charset": "",
            "full": "1",
            "_csrf_token_": self._login_user.csrf_token,
            "_root_token_": self._login_user.csrf_token,
            "_refer_hash_": "",
            "_tpl_": "v5",
        }
        res = self._login_user.session.post(url, headers=headers, data=data)
        if res.status_code == requests.codes.ok:
            res_json = json.loads(res.content)
            sender = res_json["data"]["from"]["displayName"]
            sender_mail = res_json["data"]["from"]["email"]
            sender_info = dict(sender=sender, senderMail=sender_mail)
            content = res_json["data"]["body"]
            receiver_infos = res_json["data"]["to"]
            receive_infos = list()
            for receiver_info in receiver_infos:
                receiver = receiver_info["name"]
                receiver_mail = receiver_info["email"]
                receive_infos.append(dict(receiver=receiver, receiverMail=receiver_mail))
            email_account = res_json["email"]
            # 附件信息id
            if "attachList" in res_json["data"] and res_json["data"]["attachList"]:
                attach_list = res_json["data"]["attachList"]
                attach_infos = list()
                for attach_info in attach_list:
                    # 附件id
                    attach_id = attach_info["attachmentId"]
                    attach_type = attach_info["clientExtraInfo"]["fileType"]
                    attach_size = attach_info["size"]
                    attach_name = attach_info["fileName"]
                    attach_infos.append(dict(emailId=email_id, attachId=attach_id, emailAccount=email_account,
                                             attachType=attach_type, attachName=attach_name, attachSize=attach_size))
            else:
                attach_infos = None
            return dict(senderInfo=sender_info, content=content, receiveInfo=receive_infos, attachInfo=attach_infos)
        else:
            raise ValueError(f"获取邮件详情失败")

    # 下载附件
    def download_attach(self, attach_info):
        mail_id = attach_info["emailId"]
        attach_id = attach_info["attachId"]
        receive_mail = attach_info["emailAccount"]
        file_type = attach_info["attachType"]
        file_name = attach_info["attachName"]
        cookie_dict = requests.utils.dict_from_cookiejar(self._login_user.session.cookies)
        print(cookie_dict)
        e = cookie_dict["at"]
        e = re.findall("\"(.*com.cn)", e)[0]
        url = f"{QIYE_HOST}/attachment/downloadex"
        data = {
            "et": "normal",
            "m": mail_id,
            "f": attach_id,
            "e": e,
            "ext": file_type,
            "n": file_name,
            "ri": "/alimail/internalLinks/refreshToken",
        }
        headers = {
            "Host": "qiye.aliyun.com",
            "Referer": f"{QIYE_HOST}/alimail/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        }
        res = self._login_user.session.get(url, headers=headers, params=data)
        if res.status_code == requests.codes.ok:
            return dict(fileContent=res.content)
        else:
            raise ValueError(f"文件下载失败")

    # 查询开始时间到结束时间内的邮件
    def fetch_mail_list_date(self, offset, start_date, end_date):
        """"""
        start_year = time.strftime("%Y", time.strptime(start_date, "%Y%m%d"))
        start_month = time.strftime("%m", time.strptime(start_date, "%Y%m%d"))
        start_day = time.strftime("%d", time.strptime(start_date, "%Y%m%d"))
        end_year = time.strftime("%Y", time.strptime(end_date, "%Y%m%d"))
        end_month = time.strftime("%m", time.strptime(end_date, "%Y%m%d"))
        end_day = time.strftime("%d", time.strptime(end_date, "%Y%m%d"))
        url = f"{QIYE_HOST}/alimail/ajax/mail/queryMailList.txt?_timestamp_={int(time.time() * 1000)}"
        headers = self._headers(url)
        headers["Origin"] = QIYE_HOST
        headers["Referer"] = f"{QIYE_HOST}/alimail/"
        data = {
            "showFrom": "1",
            "query": json.dumps({"keywordFields": 7,
                                 # "keywords": ["jcc2hao@163.com"],
                                 "start": {"y": start_year, "m": start_month, "d": start_day},
                                 "end": {"y": end_year, "m": end_month, "d": end_day},
                                 "advancedSearch": True}),
            "fragment": "1",
            "offset": str(offset),
            "length": "25",
            "curIncrementId": "0",
            "forceReturnData": "1",
            "_csrf_token_": self._login_user.csrf_token,
            "_root_token_": self._login_user.root_token,
            "_refer_hash_": "",
            "_tpl_": "v5",
        }
        res = self._login_user.session.post(url, headers=headers, data=data)
        if res.status_code == requests.codes.ok:
            res_json = json.loads(res.content)
            if "dataList" in res_json and res_json["dataList"]:
                for mail_info in res_json["dataList"]:
                    try:
                        mail_id = mail_info["mailId"]
                        receive_time = time.strftime("%Y-%m-%d %H:%M",
                                                     time.localtime(mail_info["timestamp"] / 1000))
                        mail_title = mail_info.get("encSubject")
                        self._logger.info(f"开始获取名为【{mail_title}】的内容")
                        detail_info = self._read_email_detail(mail_id)
                        detail_info["emailID"] = mail_id
                        detail_info["emailTitle"] = mail_title
                        detail_info["receiveTime"] = receive_time
                        yield detail_info
                    except Exception as e:
                        self._logger.info(f"{e}\n{traceback}")
            else:
                yield None
        else:
            raise ValueError(f"获取邮件列表失败")


class SendEmail:
    def __init__(self, login_user: AliEmailCom, logger):
        self._login_user = login_user
        self._logger = logger
        self._now = int(time.time() * 1000)

    # 获取邮箱地址
    # 上传附件
    # 发送邮件
    # 判断请求是否未200
    @staticmethod
    def _judge_req(res):
        if res.status_code == requests.codes.ok:
            return True
        else:
            return False

    @staticmethod
    def _headers(url):
        headers = {
            "Host": urlparse(url).netloc,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113."
                          "0.0.0 Safari/537.36"
        }
        return headers

    def _send_email(self, mail_data):
        """"""
        now = int(time.time() * 1000)
        url = f"{QIYE_HOST}/alimail/ajax/mail/sendMail.txt?_timestamp_={now}"
        headers = self._headers(url)
        headers["Origin"] = QIYE_HOST
        headers["Referer"] = f"{QIYE_HOST}/alimail/"
        data = {
            "mailJsonData": json.dumps(mail_data, ensure_ascii=False),
            "_csrf_token_": self._login_user.csrf_token,
            "_root_token_": self._login_user.root_token,
            "_refer_hash_": "h=WyJmbV81YzNGdFh6TXhOMTh4TmpZMU1qRXdPVFl4TVRBeiIsWyI1IiwiIix7InR5cGUiOiJuZXcifSx7fV1d",
            "_tpl_": "v5",
            "_frame_": "5__1",
        }
        res = self._login_user.session.post(url, headers=headers, data=data)
        if self._judge_req(res):
            res_json = json.loads(res.content)
            if "success" in res_json:
                return True
            else:
                return False
        else:
            return False

    def _start_draft(self):
        """"""
        url = f"{QIYE_HOST}/alimail/ajax/mail/startDraft.txt?_timestamp_={self._now}"
        headers = self._headers(url)
        headers["Origin"] = QIYE_HOST
        headers["Referer"] = f"{QIYE_HOST}/alimail/"
        data = {
            "mailIds": "[]",
            "_csrf_token_": self._login_user.csrf_token,
            "_root_token_": self._login_user.root_token,
            "_refer_hash_": "",
            "_tpl_": "v5",
        }
        res = self._login_user.session.post(url, headers=headers, data=data)
        req = self._judge_req(res)
        if self._judge_req(res):
            res_json = json.loads(res.content)
            draft_id = res_json["draftSessionId"]
            return draft_id
        else:
            raise ValueError(f"打开编辑邮件信息失败")

    # 上传附件
    def _upload_attach(self, file_name, file_content=None, file_path=None):
        assert file_path or file_content, "无法获取附件内容"
        file_content = self._read_attach_content(file_path) if not file_content else file_content
        # 获取附件名字
        file_name_info = os.path.splitext(file_name)
        attach_file_name = file_name_info[0]
        url = f"{QIYE_HOST}/attachment/uploadex"
        headers = self._headers(url)
        headers["Origin"] = QIYE_HOST
        headers["Referer"] = f"{QIYE_HOST}/alimail/"
        # session_dict = requests.utils.dict_from_cookiejar(self._login_user.session.cookies)
        """
        s: zhangqianglin_ccbtrust_com_cn_f58a6ef04f%40priv.ccbtrust.com.cnPKCPA1685321279566
        e: zhangqianglin_ccbtrust_com_cn_f58a6ef04f%40priv.ccbtrust.com.cn
        c: json
        et: normal
        """
        e = re.findall("(.*?\.cn)", self._login_user.attach_token)
        params = {
            "s": self._login_user.attach_token,
            "et": "normal",
            "e": e[0],
            "c": "json",
        }
        if isinstance(file_content, bytes):
            files = {file_name: (
                attach_file_name,
                io.BytesIO(file_content)
            )}
        else:
            files = {file_name: (
                attach_file_name,
                file_content
            )}
        res = self._login_user.session.post(url, headers=headers, params=params, files=files)
        if self._judge_req(res):
            upload_res_info = dict()
            for upload_infos in res.text.split("&"):
                upload_info = upload_infos.split("=")
                upload_res_info[upload_info[0]] = upload_info[1]
            upload_res_info["fileName"] = file_name
            return upload_res_info
        else:
            return None

    # 读取附件内容
    @staticmethod
    def _read_attach_content(file_path):
        file_content = b""
        with open(file_path, "rb") as r:
            try:
                for content in r.readlines():
                    file_content += content
            finally:
                r.close()
        return file_content

    # 查询联系人中是否已存在邮箱地址
    def _search_email_address(self, access_email):
        for i in range(len(access_email)):
            key_word = access_email[0:i + 1]
            now = int(time.time() * 1000)
            url = f"{QIYE_HOST}/alimail/ajax/recipient/getRecipientResolveData.txt?_timestamp_={now}"
            headers = self._headers(url)
            headers["Origin"] = QIYE_HOST
            headers["Referer"] = f"{QIYE_HOST}/alimail/"
            data = {
                "accountOnly": "0",
                "keyword": key_word,
                "maxCount": "32",
                "needResolve": "0",
                "_csrf_token_": self._login_user.csrf_token,
                "_root_token_": self._login_user.root_token,
                "_refer_hash_": "",
                "_tpl_": "v5",
            }
            res = self._login_user.session.post(url, headers=headers, data=data)
            if self._judge_req(res):
                res_json = json.loads(res.content)
                if "suggestionList" in res_json and res_json["suggestionList"]:
                    receiver_users = res_json["suggestionList"]
                    if len(receiver_users) <= 3:
                        for receiver_user in receiver_users:
                            receiver_email = receiver_user[0]["email"]
                            if receiver_email == access_email:
                                return receiver_user[0]
            else:
                return None
        else:
            return None

    def _send_ali_email(self, title, access_useres: list, copy_to=None, body=None, upload_file_infos=None):
        assert upload_file_infos, "无法获取附件内容"
        assert access_useres, "请输入发送邮箱地址"
        assert title, "请输入邮件标题"
        data = {
            "to": [],
            "cc": [],
            "bcc": [],
            "separatedSend": False,
            "atFlagId": int(time.time() * 1000),
            "highPriority": False,
            "saveToSendFolder": True,
            "html": True,
            "clientExtraInfo": {},
            "body": "",
            "attachList": [],
            "draftSessionId": "",
            "from": {"email": self._login_user._account, "name": self._login_user.name},
            "guid": ""
        }
        # 创建编辑邮件页面
        draft_id = self._start_draft()
        data["draftSessionId"] = draft_id
        # 查询联系人是否存在
        for access_user in access_useres:
            access_user_info = self._search_email_address(access_user)
            # 如果联系人存在，获取联系人信息
            if access_user_info:
                access_user_info["namePinYin"] = []
                access_user_info["isError"] = False
                data["to"].append(access_user_info)
            else:
                # 如果联系人不存在，创建联系信息
                data["to"].append({"name": access_user.split("@")[0], "email": access_user, "isError": False})

        # 查看是否有抄送
        if copy_to:
            for copyto in copy_to:
                copy_to_info = self._search_email_address(copyto)
                # 如果联系人存在，获取联系人信息
                if copy_to_info:
                    copy_to_info["namePinYin"] = []
                    copy_to_info["isError"] = False
                    data["cc"].append(copy_to_info)
                else:
                    # 如果联系人不存在，创建联系信息
                    data["cc"].append({"name": copyto.split("@")[0], "email": copyto, "isError": False})
        # 查看是否有附件，有上传附件，无不上传
        # 附件地址
        # 编辑文本内容
        # 上传附件
        body = ""
        for upload_file_info in upload_file_infos:
            data["attachList"].append({
                "clientId": f"sqm_{upload_file_info['s']}",
                "fileName": upload_file_info["fileName"],
                "size": upload_file_info['s'],
                "tempUrl": upload_file_info['l']
            })
            body += f"{upload_file_info['fileName']}\n"
        data["body"] = title if not body else body
        data["subject"] = title
        send_res = self._send_email(data)
        if send_res:
            self._logger.info(f"邮件发送成功")
            return True
        else:
            self._logger.info(f"邮件未发送成功")
            return False


if __name__ == '__main__':
    obj = AliEmailCom("wangmin1@priv.ccbtrust.com.cn", "Min@8114167")
    # obj = AliEmailCom("lvyepei@priv.ccbtrust.com.cn", "Lyp12345")
    obj.login()
    email_list = ReadEmailList(obj, AliEmailCom.logger_custom())
    for email_info in email_list.read_email():
        if "attachInfo" in email_info and email_info["attachInfo"]:
            for attach_info in email_info["attachInfo"]:
                print(email_list.download_attach(attach_info))
