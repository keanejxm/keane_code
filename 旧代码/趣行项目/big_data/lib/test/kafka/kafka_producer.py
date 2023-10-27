#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Kafka生产者。
# author: Trico
# date: 2019.9.18
"""

import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    compression_type="gzip",
)
print(datetime.datetime.now())

for i in range(3):
    response = producer.send("test", key=b"foo1", value=bytes("python test {}.".format(i), encoding="utf-8"))
    result = response.get(timeout=60)
    print("{:>3} {} '{}'.".format(i, datetime.datetime.now(), result))

# response = producer.send('test', value=b'c29tZSB2YWx1ZQ==', headers=[('content-encoding', b'base64')])
# result = response.get(timeout=60)
# print("{} '{}'.".format(datetime.datetime.now(), result))

# metrics = producer.metrics()

producer.flush()
