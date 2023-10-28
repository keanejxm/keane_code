# -*- coding:utf-8 -*-

"""
# author: Chris
# date: 2020.10.28
# update: 2020.10.28
"""

import pymysql
import time
import requests
import json
import random
from lib.common_utils.mysql_utils import MySQLUtils
from test_kafka_p import official_send
from threading import Thread


def uid_from_sql():
    mysql_config = {
        "host": "192.168.32.18",
        "port": 3306,
        "user": "root",
        # "passwd": "quxing",
        "passwd": "moR7tzWCv$ZYBe*$",
        "db": "big_data_platform",
        "charset": "utf8mb4",
        "cursorclass": pymysql.cursors.DictCursor
    }
    db = MySQLUtils(**mysql_config)
    sql = "select uid from weibo_sourcelist where id <=1000;"
    ret = db.search(sql)
    task_lis = [i["uid"] for i in ret]
    return task_lis


def get_wb_cookie():
    weibo_random_cookie_url = "http://192.168.16.7:16100/crawler_resources/get_random_wb_cookie"
    resp = requests.get(weibo_random_cookie_url, timeout=10)
    resp_data = json.loads(resp.content)
    return resp_data["data"]["wbCookie"]


def test_thread_1(task_l):
    for uid in task_l:
        wb_cookie_info = get_wb_cookie()
        wb_cookie = wb_cookie_info["cookie"]
        print("正在执行的uid是：{}".format(uid))
        official_send("weibo_official_test", wb_cookie, uid)
        time.sleep(random.random())


if __name__ == '__main__':
    task = uid_from_sql()
    ret = []
    for i in range(10):
        t = Thread(target=test_thread_1, args=(task[i*100:(i+1)*100],))
        t.setDaemon(True)
        ret.append(t)
    for r in ret:
        r.start()

    for r in ret:
        r.join()
