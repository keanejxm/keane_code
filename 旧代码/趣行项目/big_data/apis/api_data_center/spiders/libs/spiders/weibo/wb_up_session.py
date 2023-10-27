# -*- coding:utf-8 -*-
"""
获取微博访客会话。
微博头条文章会话。
整体逻辑由Chris实现。
# author: Trico、Chris
# date: 2020.8.10
# update: 2020.8.10
"""

import requests
import re
import json
from urllib.parse import unquote
from lxml import etree
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()


class TouTiaoSession:

    def __init__(self, cookie, target_url, referer_url, logger):
        self._timeout = 10
        self._webdriver_timeout = 10
        self.target_url = target_url
        self.referer_url = referer_url
        self._logger = logger
        self._request_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;"
                      "q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cookie": cookie,
            # "referer": self.referer_url,
            "Upgrade-Insecure-Requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/84.0.4147.105 Safari/537.36"
            }

    def get_tt_content(self):
        mid_fields = {
            "author": "",
            "title": "",
            "digest": "",
            "content": "",
            "covers": list(),
            "videos": list(),
            "readNum": 0,
        }
        session = requests.Session()
        session.headers.update(self._request_headers)
        target_url = unquote(self.target_url)
        self._logger.info(target_url)
        tt_urls = target_url.split("&")
        target_url = re.findall(r"t\.cn(.*)", tt_urls[1])
        target_url = " http://t.cn" + target_url[0]
        session.headers.update({"Host": "t.cn"})
        resp = session.get(target_url, timeout=self._timeout, allow_redirects=False)
        refer_url = resp.headers["location"]
        new_host = re.findall(r"http[s]?://(.*[om|n])/", refer_url)
        if new_host[0] != "weibo.com":
            self._logger.warning(f"可能出现跨域:{new_host[0]}，原网站并非头条文章，原始地址是：{target_url}")
            return None
        session.headers.update({"Host": "weibo.com"})
        try:
            resp = session.get(refer_url, timeout=self._timeout, allow_redirects=False, verify=False)
            refer_url = resp.headers["location"]
            session.headers.update({"Host": "passport.weibo.com"})
            resp = session.get(refer_url, timeout=self._timeout, allow_redirects=False, verify=False)
            url = re.findall(r"<meta.*(https:.*);\"/>", resp.text, re.S)
            session.headers.update({"Host": "weibo.cn"})
            resp = session.get(url[0], timeout=self._timeout, allow_redirects=False, verify=False)
            """包含视频时会有一个跳转"""
            if resp.status_code != 200:
                refer_url = resp.headers["location"]
                session.headers.update({"Host": "media.weibo.cn"})
                resp = session.get(refer_url, timeout=self._timeout, allow_redirects=False, verify=False)
                refer_url = resp.headers["location"]
                session.headers.update({"Host": "card.weibo.com"})
                resp = session.get(refer_url, timeout=self._timeout, allow_redirects=False, verify=False)
                ref_id = re.findall(r"id/(\d+)", refer_url)
                session.headers.update({"Referer": refer_url})
                refer_url = "https://card.weibo.com/article/m/aj/extend?id={}".format(ref_id[0])
                print(refer_url)
                resp = session.get(refer_url, timeout=self._timeout, allow_redirects=False, verify=False)
                res = json.loads(resp.text)
                print(res)
                mid_fields["title"] = res["data"]["title"]
                mid_fields["author"] = res["data"]["userinfo"]["screen_name"]
                mid_fields["content"] = res["data"]["content"]
                try:
                    card_id = res["data"]["card_list"]
                    card_id = {v: k for k, v in card_id.items()}
                    mid_fields["videos"] = [res["data"]["object_info"][card_id["video"]]["object"]["stream"]["url"]]
                    mid_fields["covers"] = [res["data"]["cover_img"]["full_image"]["url"]]
                    mid_fields["readNum"] = int(res["data"]["read_count"])    # readNum
                    mid_fields["digest"] = res["data"]["summary"]
                except Exception as e:
                    self._logger.warning(str(e))
            else:
                    content_tree = etree.HTML(resp.content)
                    if content_tree is not None and len(content_tree) > 0:
                        con = content_tree.xpath("//div[@class='WB_artical']/div[2]")[0]
                        mid_fields["title"] = con.xpath("//div[@class='title']/text()")[0]  # 标题
                        mid_fields["author"] = con.xpath("//span[@class='author1 W_autocut']/a/em/text()")[0]  # 作者
                        try:
                            mid_fields["digest"] = con.xpath("//div[@class='preface']/text()")  # 摘要
                        except Exception as e:
                            mid_fields["digest"] = ""
                        contents = con.xpath("//div[@class='WB_editor_iframe_new']")
                        content = etree.tostring(contents[0]).decode("utf-8")
                        soup = BeautifulSoup(content, "html.parser")
                        mid_fields["content"] = str(soup).strip()
                    else:
                        self._logger.warning(f"当前页面为空：{url[0]}")
        except Exception as e:
            self._logger.warning(str(e))
        return mid_fields

    def get_toutiao_content(self):
        try:
            mid_fields = {
                "author": "",
                "title": "",
                "digest": "",
                "content": "",
                "url": "",
                "images": list(),
                "covers": list(),
                "videos": list(),
                "readNum": 0,
            }
            session = requests.Session()
            session.headers.update(self._request_headers)
            target_url = unquote(self.target_url)
            self._logger.info(target_url)
            tt_urls = target_url.split("&")
            tar_url = tt_urls[1].replace("u=", "")
            session.headers.update({"Host": "t.cn"})
            resp = session.get(tar_url, timeout=self._timeout, allow_redirects=False)
            refer_url = resp.headers["location"]        # 这里就是目标url，可以获取整个content
            new_host = re.findall(r"http[s]?://(.*[om|n])/", refer_url)
            if len(new_host):
                if new_host[0] != "weibo.com":
                    self._logger.warning(f"可能出现跨域:{new_host[0]}，原网站并非头条文章，原始地址是：{target_url}")
                    return None
                ref_id = re.findall(r"id=(\d+)", refer_url)
                if len(ref_id) == 0:
                    self._logger.warning(f"可能原网站并非头条文章现地址是：{refer_url}，原始地址是：{target_url}")
                    return None
                session.headers.update({"Host": "card.weibo.com"})
                session.headers.update({"Referer": self.referer_url})
                refer_url = "https://card.weibo.com/article/m/aj/extend?id={}".format(ref_id[0])
                resp = session.get(refer_url, timeout=self._timeout, allow_redirects=False, verify=False)
                res = json.loads(resp.text)
                # self._logger.info(f"头条文章的response结果时：{res}")
                mid_fields["title"] = res["data"]["title"]
                mid_fields["author"] = res["data"]["userinfo"]["screen_name"]
                mid_fields["content"] = res["data"]["content"]
                mid_fields["url"] = res["data"]["url"]
                tree = etree.HTML(mid_fields["content"])
                if len(tree):
                    mid_fields["images"] = tree.xpath("//img/@src")
                if res["data"]["cover_img"]:
                    mid_fields["covers"] = [res["data"]["cover_img"]["image"]["url"]]
                read_num = res["data"]["read_count"]  # readNum     mid_fields["readNum"]
                if "万" not in read_num:
                    mid_fields["readNum"] = int(read_num)
                else:
                    mid_fields["readNum"] = int(read_num.replace("万+", ""))*10000
                mid_fields["digest"] = res["data"]["summary"]

                if res["data"]["object_info"] and res["data"]["card_list"]:
                    card_id = res["data"]["card_list"]
                    card_id = {v: k for k, v in card_id.items()}
                    mid_fields["videos"] = [res["data"]["object_info"][card_id["video"]]["object"]["stream"]["url"]]
                else:
                    tree = etree.HTML(mid_fields["content"])
                    if len(tree):
                        mid_fields["videos"] = tree.xpath("//video/@src")
                return mid_fields
            else:
                self._logger.warning(f"可能出现跨域,原始地址是：{target_url},跳转后地址是：{refer_url}")
                return None
        except Exception as e:
            self._logger.warning(str(e))


def test_wb_tou_tiao_session():
    # 测试微博头条文章会话。

    """下雨天"""
    # t_url = "https://weibo.cn/sinaurl?f=w&u=http%3A%2F%2Ft.cn%2FA6yv7rsF&ep=J92F3ieQC%2C2966211953%2CJ92F3ieQC%2C2966211953"
    """我的办公室键盘"""
    t_url = "https://weibo.cn/sinaurl?f=w&u=http%3A%2F%2Ft.cn%2FA6yJ7QHI&ep=Jayee1ioa%2C2966211953%2CJayee1ioa%2C2966211953"
    co = "_T_WM=931c4220c866321fa4e6000511d36367; SUB=_2A25yNXnBDeRhGeFK41oV9i3EzTmIHXVR1geJrDV6PUJbktANLRL-kW1NQsFx9" \
         "pLyawPVGK8NmhWCv9hY6J1sr5PU; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWcY65F3oGIcM7FDWEY0XlU5NHD95QNShnRShq01" \
         "hqfWs4DqcjGU0MfUc8V97tt; SUHB=0QS5MaHSj9-Xnt; SSOLoginState=1597049233"
    # r_url = "https://weibo.cn/u/2966211953"
    # r_url = "https://weibo.cn/u/5288584137"
    # t_url = "https://weibo.cn/sinaurl?f=w&u=http%3A%2F%2Ft.cn%2FA64jRHFL&ep=JkIbv3TXv%2C5288584137%2CJkIbv3TXv%2C5288584137"
    # TouTiaoSession(co, t_url, r_url).get_tt_content()


    co = "_T_WM=1eb8ca81a23b526b869a9dd5eaa24fdd; SUB=_2A25yZFqUDeRhGeFK41oV9i3EzTmIHXVRp2bcrDV6PUJbktANLXPtkW1NQsFx9ieONTcE2CMlORmjih9LSXdKtxXM; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWcY65F3oGIcM7FDWEY0XlU5NHD95QNShnRShq01hqfWs4DqcjGU0MfUc8V97tt; SUHB=0u5RnPXyvb_Hls; SSOLoginState=1600137924"
    from common_utils.llog import LLog
    logger = LLog("test", only_console=True).logger
    r_url = "https://weibo.cn/u/2656274875"
    t_url = "https://weibo.cn/sinaurl?f=w&u=http%3A%2F%2Ft.cn%2FA64jwunG&ep=JkE0d6VAL%2C2656274875%2CJkE0d6VAL%2C2656274875"
    TouTiaoSession(co, t_url, r_url, logger).get_toutiao_content()
