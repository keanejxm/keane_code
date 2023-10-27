# Author Keane
# coding=utf-8
# @Time    : 2021/1/11 10:24
# @File    : 测试石家庄加密.py
# @Software: PyCharm
import hashlib
import json
import time

import requests
def md5(strsea, charset="UTF-8"):
    """
    字符串转md5格式。
    :param strsea:
    :param charset:
    :return:
    """

    md5 = hashlib.md5()
    md5.update(strsea.encode(charset))
    return md5.hexdigest()
url = "http://static.sjzrbapp.com:89/type/getTypeListCache"
headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "145",
            "Host": "static.sjzrbapp.com:89",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.1",
        }
data = "sign=cf2fb873a01ac29835e56f1f818a3116&siteId=1&siteid=1&device=00000000-15c7-18b7-8e6b-6f8e0033c587&nonce=1622475814&version=1.1.3&tid=1067&timestamp=1610174467940"
res = requests.post(url,headers = headers,data = data).text
res = json.loads(res)
print(res)
for channel in res["data"]:
    channel_id = channel.get("tid")
    print(channel_id)
    url = "http://static.sjzrbapp.com:89/news/getNewsListCache"
    headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "175",
            "Host": "static.sjzrbapp.com:89",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.1",
        }
    body = {
    "version":"1.1.3",
    "timestamp":str(int(time.time()*1000)),
    "tid":str(974),
    "siteId":"1",
    "siteid":"1",
    # "sign":"5230b1507ac352396a00bda13268f9bc",
    "reqPagenum":"1",
    "nonce":"1622475814",
    "device":"00000000-15c7-18b7-8e6b-6f8e0033c587",
}
    sb = "b11ebd23bb617a75"
    a = sorted(body, reverse=False)
    for i in a:
        sb += (i + "=" + body.get(i))
    sign = md5(sb)
    data = f"reqPagenum=1&sign={sign}&siteId=1&siteid=1&device=00000000-15c7-18b7-8e6b-6f8e0033c587&nonce=1622475814&version=1.1.3&tid=974&timestamp={body.get('timestamp')}"
    res = requests.post(url,headers = headers,data = data).text
    print(res)