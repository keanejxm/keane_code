# coding:utf-8
import hashlib
import json
import pymysql
import redis
import requests
import time


def md5(strsea, charset="UTF-8"):
    # 字符串转md5格式
    _md5 = hashlib.md5()
    _md5.update(strsea.encode(charset))
    return _md5.hexdigest()


def test_wx_key():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 "
                      "MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat "
                      "QBCore/3.43.901.400 QQBrowser/9.0.2524.400",
    }
    target_name = "河北日报公众号"
    sql = f"select * from wx_sourcelist where platformName in ('{target_name}');"
    with pymysql.connect(
            host="192.168.16.7", user="root", password="quxing",
            database="big_data", cursorclass=pymysql.cursors.DictCursor
    ) as cur:
        cur.execute(sql)
        source_list = cur.fetchall()
        for oneTask in source_list[:1]:
            gzh_id = oneTask["fakeid"]
            for page in range(1):
                offset = page * 10
                con_redis = redis.Redis(
                    host="192.168.16.14", port=6379, password='0075b890aed311eab4330800270d4d0e')
                key_dict = json.loads(con_redis.get("keydict").decode("utf-8"))
                for uin in key_dict.keys():
                    key = key_dict[uin]
                    print(key, uin)
                    list_url = f"https://mp.weixin.qq.com/mp/profile_ext?" \
                               f"action=getmsg" \
                               f"&__biz={gzh_id}&f=json&offset={offset}&count=10&uin={uin}&key={key}"
                    resp = requests.get(list_url, headers=headers, timeout=5).text
                    print(resp)
                    time.sleep(3)


if __name__ == "__main__":
    test_wx_key()
