# -*- coding:utf-8 -*-

"""
# author: Chris
# date: 2020.10.28
# update: 2020.10.28
"""

import json
from kafka import KafkaConsumer
from common_utils.accounts_crawler_es_utils import AccountsCrawlerESUtils


# consumer = KafkaConsumer("1234", auto_offset_reset="earliest", bootstrap_servers="192.168.16.16:9092")
# for msg in consumer:
#     print(msg.value.decode())


def kaf_rec_message(topic):
    my_hosts = "192.168.16.16:9092"
    consumer = KafkaConsumer(topic, auto_offset_reset="latest", bootstrap_servers=my_hosts, enable_auto_commit=True,)
    for msg in consumer:
        print(json.loads(msg.value.decode(encoding="utf8")))
        msg = json.loads(msg.value.decode(encoding="utf8"))
        from lib.common_utils.llog import LLog
        logger = LLog("test", only_console=True).logger
        AccountsCrawlerESUtils(logger).es_save_accounts_and_works(msg["data"])


kaf_rec_message("weibo_official_test")


