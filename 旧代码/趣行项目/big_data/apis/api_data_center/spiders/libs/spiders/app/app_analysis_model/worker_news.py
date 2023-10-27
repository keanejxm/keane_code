#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
功能描述。
# author: Nile
# create date: 2020/11/26
# update date: 2020/11/26
# appversion: 
"""

import requests
import traceback
import time, random
from lib.common_utils.llog import LLog

class WorkerSpider():

    def __init__(self, logger):
        self._logger = logger
        self._timeout = 20
        self.start_url = "http://47.110.139.194/api/getColumns?cid=2 HTTP/1.1"
        self._session = requests.session()
        self._headers = {
            "Host": "47.110.139.194",
            "User-Agent": "okhttp/3.12.0",
            "Connection": "Keep-Alive"

        }
        self._session.headers.update(self._headers)

    @staticmethod
    def detail_headers(wid):
        """
        详情页专用
        :return:
        """
        now = int(time.time())*1000
        headers = {
            "Host": "api.app.workercn.cn",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Origin": "http://web.app.workercn.cn",
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; LIO-AN00 Build/LIO-AN00; wv) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 agentweb/4.0.2  "
                          "UCBrowser/11.6.4.950",
            "Referer": f"http://web.app.workercn.cn/app/html/new-article.html?id={wid}&t={now}",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "X-Requested-With": "com.grrb.news"
        }
        return headers

    def get_columns_list(self):
        """
        获取频道页列表
        :return:
        """
        try:
            res = self._session.get(url=self.start_url, timeout=self._timeout, verify=False)
            res_columns_list = res.json()["columns"]
            self._logger.info(f"采集到的频道信息为{res_columns_list}")
            for column in res_columns_list:
                if "columnName" in column and column["columnName"] :
                    column_name = column["columnName"]
                    column_id = column["columnID"]
                    column_url = f"http://47.110.139.194/api/getArticles?cid={column_id}&rowNumber=0&lastFileID=0" \
                        f"&pageSize=20&orderby= HTTP/1.1"
                else:
                    continue
                yield column_name, column_url
        except Exception as e:
            self._logger.warning(f"{e}\n{traceback.format_exc()}")

    def get_column_news_list(self):
        """
        获取每个频道的新闻列表
        :return:
        """
        for name, url in self.get_columns_list():
            try:
                res = self._session.get(url=url, timeout=self._timeout, verify=False)
                # 每个频道的新闻暂时取前10条
                news_list = res.json()["list"][:10]
                for article in news_list:
                    yield article, name
            except Exception as e:
                self._logger.warning(f"{e}\n{traceback.format_exc()}")
                continue

    def get_news_detail(self):
        """
        获取每条新闻详细信息
        :return:
        """
        # 定义一个列表，存储新闻详情
        news_list = list()
        now = int(time.time())*1000
        for article, name in self.get_column_news_list():
            try:

                if "fileID" in article and article["fileID"]:
                    wid = article["fileID"]
                    column_name = name
                    # 详情页url
                    detail_url = f"http://api.app.workercn.cn/api/getArticle?aid={wid}&t={now} HTTP/1.1"
                else:
                    continue
                title = article.get("title", "")
                covers = list()
                if "pic1" in article and article["pic1"]:
                    covers.append(article["pic1"])
                else:
                    covers = []
                videos = list()
                if "articleUrl" in article and article["articleUrl"]:
                    videos.append(article["articleUrl"])
                else:
                    videos = []
                now = int(time.time())
                pub_time = article.get("publishTime", 0)
                pub_time = int(time.mktime(time.strptime(pub_time, "%Y-%m-%d %H:%M:%S")))
                # 访问详情页获取详情页信息
                # 获取请求头信息
                headers = self.detail_headers(wid)
                time.sleep(random.random() + 1.7)
                res = requests.get(url=detail_url, headers=headers, timeout=self._timeout)
                res_dict = res.json()
                source = res_dict.get("source", "")
                author = res_dict.get("author", "")
                like_num = res_dict.get("countPraise", 0)
                share_num = res_dict.get("countShare", 0)
                news_info = {
                    "mediatype": "app数据",
                    "appname": "",
                    "channelname": column_name,
                    "url": detail_url,
                    "title": title,
                    "content": res.json()["content"],
                    "articlecovers": covers,
                    "images": "",
                    "videos": videos,
                    "videocover": "",
                    "width": "",
                    "height": "",
                    "source": source,
                    "pubtime": pub_time,
                    "createtime": now,
                    "updatetime": now,
                    "likenum": like_num,
                    "playnum": 0,
                    "commentnum": 0,
                    "readnum": 0,
                    "trannum": 0,
                    "sharenum": share_num,
                    "author": author,
                }
                self._logger.info(f"采集'{column_name}'频道下题目为:{title}新闻详情信息为:{news_info}")
                news_list.append(news_info)
            except Exception as e:
                self._logger.warning(f"{e}\n{traceback.format_exc()}")
                continue
        return {'code': 1, 'msg': 'ok', 'data': {'works': news_list}}

    def run(self):
        """
        执行入口
        :return:
        """
        self.get_news_detail()

if __name__ == '__main__':
    logger = LLog("worker_news", only_console=True, logger_level="DEBUG").logger
    WorkerSpider(logger=logger).run()

