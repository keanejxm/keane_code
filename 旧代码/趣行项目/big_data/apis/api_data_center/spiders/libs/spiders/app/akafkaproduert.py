#!-*- coding:utf-8 -*-
"""
Kafaka生产者
# author: Keane
# create date:
# update date: 2020/11/11
"""
import json

from kafka import KafkaProducer


class KafkaProducers(object):
    @staticmethod
    def senddatas(datas):
        producer = KafkaProducer(bootstrap_servers = ['192.168.16.16:9092'])
        data = json.dumps(datas).encode('utf-8')
        producer.send('appdatas', data)
        producer.close()
