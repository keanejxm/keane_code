#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Kafka生产者。
# author: Trico
# date: 2019.9.18
"""

import datetime
from kafka import KafkaAdminClient

client = KafkaAdminClient(
    bootstrap_servers="localhost:9092",
)

print(datetime.datetime.now())

# 删除指定Topic。
# response = client.delete_topics(["foobar", ])
# print("{} '{}'.".format(datetime.datetime.now(), response))
