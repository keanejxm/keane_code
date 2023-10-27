#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Kafka消费者。
# author: Trico
# date: 2019.9.18
"""

import datetime
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "test",
    bootstrap_servers="localhost:9092",
    group_id='test_group',
)
print(datetime.datetime.now())

for i, msg in enumerate(consumer):
    print("{:>3} {} '{}'.".format(i, datetime.datetime.now(), msg))
