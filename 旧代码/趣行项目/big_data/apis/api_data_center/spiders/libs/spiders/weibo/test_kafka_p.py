# -*- coding:utf-8 -*-

"""
# author: Chris
# date: 2020.10.28
# update: 2020.10.28
"""

import json
# import pandas
from threading import Thread

from kafka import KafkaProducer
from xinyuan_weibo import XinYuanAccount, XinYuanWb


# myhosts = "192.168.16.16:9092"
# topic = "1234"
# producer = KafkaProducer(bootstrap_servers="192.168.16.16:9092")
# producer.send(topic, "1256986210".encode())
# producer.close()


# def part_read_excel():
#     exe_path = r"D:\W75-Python\wbSpider\test1000.xlsx"
#     df = pd.read_excel(exe_path)
#     for i in range(10):
#         df1 = df.iloc[i*100:(i+1)*100, :]
#         name = df1["wb_name"].values.tolist()
#         print(name)
#         break


# Kafka发送消息
def kaf_send_message(top, msg):
    my_hosts = "192.168.16.16:9092"
    producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode("utf-8"), bootstrap_servers=my_hosts)
    # msg = json.dumps(msg)
    producer.send(top, msg)
    producer.close()


def official_send(topic, co, uid):
    from lib.common_utils.llog import LLog
    logger = LLog("test", only_console=True).logger
    field = XinYuanWb(co, uid, logger).fetch()
    print(json.dumps(field, indent=4, ensure_ascii=False))
    # field = {"key": 120189, "val": "str3", "exe": 882}
    kaf_send_message(topic, field)


def test_send():
    nick_name = input("请输入微博昵称：")
    ret = XinYuanAccount(nick_name).fetch()
    print(json.dumps(ret, indent=4, ensure_ascii=False))
    try:
        uid = ret["uid"]
    except:
        uid = None
        print("按昵称未找到关联用户")
    if uid:
        co = "SUB=_2A25yZFqUDeRhGeFK41oV9i3EzTmIHXVRp2bcrDV6PUJbktANLXPtkW1NQsFx9ieONTcE2CMlORmjih9LSXdKtxXM; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWcY65F3oGIcM7FDWEY0XlU5NHD95QNShnRShq01hqfWs4DqcjGU0MfUc8V97tt; SUHB=0u5RnPXyvb_Hls; SSOLoginState=1600137924; _T_WM=56915526903"
        from lib.common_utils.llog import LLog
        logger = LLog("test", only_console=True).logger
        field = XinYuanWb(co, uid, logger).fetch()
        print(json.dumps(field, indent=4, ensure_ascii=False))
        # field = {"key": 120189, "val": "str3", "exe": 882}
        # kaf_send_message("test_weibo", field)


if __name__ == '__main__':
    test_send()



