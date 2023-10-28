#!-*- coding:utf-8 -*-
"""
Kafka 消费者
# author: Keane
# create date:
# update date: 2020/11/11
"""
from kafka import KafkaConsumer


class KafkaConsumers(object):
    @staticmethod
    def recvive_datas():
        consumer = KafkaConsumer('appdatas', bootstrap_servers = ['192.168.16.16:9092'])
        for msg in consumer:
            print(msg)
            print(msg.key)
            print(eval(msg.value.decode(encoding = 'utf-8')))
