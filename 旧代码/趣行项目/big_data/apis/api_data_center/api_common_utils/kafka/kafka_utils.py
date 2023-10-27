# -*- coding:utf-8 -*-
"""
Kafka工具。
# author: Trico
# date: 2021/1/14
# update: 2021/1/14
"""

import kafka

from api.config import kafka_producer_config, kafka_consumer_config


def dc_kafka_producer():
    """
    Kafka生产者类。
    """

    # 生产者。
    return kafka.producer.KafkaProducer(**kafka_producer_config)


def dc_kafka_consumer(topic):
    """Kafka消费者。"""

    # 消费者。
    assert topic and isinstance(topic, str), f"参数错误，topic：{topic}"
    group_id = f"api_dc_consumer_{topic}"
    return kafka.consumer.KafkaConsumer(topic, group_id=group_id, **kafka_consumer_config)
