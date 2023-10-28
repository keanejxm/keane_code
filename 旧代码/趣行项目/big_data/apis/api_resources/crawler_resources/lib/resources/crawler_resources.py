#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
爬虫资源接口。
2020年11月20日，更新，阿布云代理加入经典模式。
# author: Trico
# date: 2020/8/9
# date: 2020/11/20
"""

import gzip
import json
import redis
import base64
import random
import pymysql
import logging
from api_common_utils.mysql_utils import MySQLUtils


class CrawlerResourcesAPI(object):
    # 爬虫资源接口。

    def __init__(self, request, logger):

        # 日志对象。
        assert isinstance(logger, logging.Logger)
        self._logger = logger

        # 记录请求。
        remote_ip = request.META.get('REMOTE_ADDR', 'unknown client ip')
        self._logger.info(f"Client IP: {remote_ip}, Path: {request.get_full_path()}")

        # 请求体。
        self._request = request

    def get_random_wx_great_key(self):
        """
        获取随机微信万能Key。
        :return:
        """

        # 连接微信万能Key的Redis。
        redis_config_for_wechat_great_keys = dict(
            host="192.168.16.14", port=6379, password="0075b890aed311eab4330800270d4d0e"
        )
        # 连接Redis。
        redis_conn = redis.Redis(**redis_config_for_wechat_great_keys)
        key_dict = json.loads(redis_conn.get("keydict").decode("utf-8"))
        key_list = []
        for uin, key in key_dict.items():
            key_list.append((uin, key))
        random_key_pair = random.choice(key_list)
        self._logger.info(f"Return wx great key of \"{random_key_pair}\".")
        return dict(wxKeyPair=random_key_pair)

    def get_random_wb_cookie(self):
        """
        获取随机微博cookie。
        :return:
        """

        # 连接MySQL。
        mysql_config_for_weibo_cookie = {
            "host": "192.168.16.7",
            "port": 3306,
            "user": "root",
            "passwd": "quxing",
            "db": "big_data",
            "charset": "utf8mb4",
            "cursorclass": pymysql.cursors.DictCursor
        }

        # 连接MySQL。
        db = MySQLUtils(**mysql_config_for_weibo_cookie)
        try:
            sql = f"select wb_loginName, cookie from wb_cookies " \
                  f"where status = 1 limit 100;"
            rows = db.search(sql)
            if rows:
                row = random.choice(rows)
                self._logger.info(f"Return wb cookie of \"{row['wb_loginName']}\".")
                return dict(wbCookie=row)
            else:
                raise ValueError("Failed to fetch wb cookie by '{}'.".format(sql))
        except Exception:
            raise
        finally:
            db.conn.close()

    def get_abuyun_proxy(self):
        """
        获取阿布云代理信息。
        :return:
        """

        # mode代表模式，1动态版，2专业版，3经典版。
        mode = self._request.GET.get("mode")
        # 代理。
        if mode in (1, "1"):
            # 动态版。
            abuyun_meta = dict(
                host="http-dyn.abuyun.com",
                port="9020",
                username="HR91J1A4881W7H1D",
                password="6A8682072812B30F"
            )
        elif mode in (3, "3"):
            # 经典版。
            abuyun_meta = dict(
                host="http-cla.abuyun.com",
                port="9030",
                username="HN2S7MX1126ID19C",
                password="804311F2D5F7552F"
            )
        else:
            # 默认用动态版。
            abuyun_meta = dict(
                host="http-dyn.abuyun.com",
                port="9020",
                username="HR91J1A4881W7H1D",
                password="6A8682072812B30F"
            )
        # 代理链接。
        proxy_url = f"http://{abuyun_meta['username']}:{abuyun_meta['password']}" \
                    f"@{abuyun_meta['host']}:{abuyun_meta['port']}"
        abuyun_proxies = {
            "http": proxy_url,
            "https": proxy_url,
        }
        proxy = dict(
            meta=abuyun_meta,
            proxies=abuyun_proxies
        )
        proxy_bytes = gzip.compress(json.dumps(proxy, separators=(",", ":")).encode("utf-8"))
        proxy_bytes = base64.standard_b64encode(proxy_bytes)
        proxy_str = proxy_bytes.decode("utf-8")
        return proxy_str
