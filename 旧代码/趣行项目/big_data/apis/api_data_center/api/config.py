#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
项目基础配置信息。
# author: Trico
# date: 2020.12.2
# update: 2020.12.2
"""

import os
import pymysql


# 设定运行环境。
import api.environment as env

# 工程名称
project_name = "big_data_platform"
# 接口名称。
api_name = "data_center"

# 工作路径和日志路径。
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assert BASE_DIR, "BASE_DIR不能为空"
api_path = BASE_DIR
# 其它路径。
api_log_path = f"{api_path}/logs"
api_template_path = f"{api_path}/templates"
api_download_files_path = f"{api_path}/download_files"
api_plugins_path = f"{api_path}/plugins"

# 特殊路径配置。
if env.run_env == env.production_env:
    # 其它路径。
    api_log_path = f"/opt/data/{project_name}/{api_name}/logs"
else:
    pass

# 本接口绑定的主机名，http协议非80、443端口时需注意端口号。
if env.run_env == env.production_env:
    api_host = "http://127.0.0.1:17001"
    external_api_host = "http://xxx.hbrbdata.cn"
else:
    api_host = "http://127.0.0.1:17000"
    external_api_host = "http://xxx.hbrbdata.cn"

# 连接MySQL。
if env.run_env == env.production_env:
    mysql_config = {
        "host": "192.168.32.5",
        "port": 3306,
        "user": "debugger",
        "passwd": "903976",
        "db": "data_center",
        "charset": "utf8mb4",
        "cursorclass": pymysql.cursors.DictCursor
    }
    normal_mysql_config = mysql_config.pop("cursorclass")
else:
    mysql_config = {
        "host": "192.168.32.5",
        "port": 3306,
        "user": "debugger",
        "passwd": "903976",
        "db": "data_center",
        "charset": "utf8mb4",
        "cursorclass": pymysql.cursors.DictCursor
    }
    normal_mysql_config = mysql_config.pop("cursorclass")

# 连接ES。
if env.run_env == env.production_env:
    es_config = {
        "hosts": [
            {
                "host": "192.168.16.21",
                "port": 9200,
            }
        ],
        "timeout": 30
    }
else:
    es_config = {
        "hosts": [
            {
                "host": "192.168.16.21",
                "port": 9200,
            }
        ],
        "timeout": 30
    }

# 连接Kafka。
if env.run_env == env.production_env:
    kafka_servers = ["192.168.16.16:9092", ]
    # 生产者。
    kafka_producer_config = dict(
        bootstrap_servers=kafka_servers,
        acks="all",
        retries=1,
        compression_type="gzip",
        max_request_size=100 * 1024 * 1024,
        # None代表听从系统配置。
        send_buffer_bytes=None,
    )
    # 消费者（group_id将和topic绑定）。
    kafka_consumer_config = dict(
        bootstrap_servers=kafka_servers,
        fetch_max_bytes=100 * 1024 * 1024,
        max_partition_fetch_bytes=100 * 1024 * 1024,
        # None代表听从系统配置。
        receive_buffer_bytes=None,
        # 调试用。
        # auto_offset_reset="earliest",
        # enable_auto_commit=False,
    )
else:
    kafka_servers = ["192.168.16.16:9092", ]
    # 生产者。
    kafka_producer_config = dict(
        bootstrap_servers=kafka_servers,
        acks="all",
        retries=1,
        compression_type="gzip",
        max_request_size=100 * 1024 * 1024,
        # None代表听从系统配置。
        send_buffer_bytes=None,
    )
    # 消费者（group_id将和topic绑定）。
    kafka_consumer_config = dict(
        bootstrap_servers=kafka_servers,
        fetch_max_bytes=100 * 1024 * 1024,
        max_partition_fetch_bytes=100 * 1024 * 1024,
        # None代表听从系统配置。
        receive_buffer_bytes=None,
        # 调试用。
        # auto_offset_reset="earliest",
        # enable_auto_commit=False,
    )

# 百度。
APP_ID = '23109692'
API_KEY = 'R7SNd6NIHqqnVvP9vgWxIdZm'
SECRET_KEY = 'gBd91KpGjmmBY3dBUaSOV0T4cmPZfiUh'

# Kafka主题。
kafka_topics = {
    "origin": "dc-original",
    "push": "dc-push",
    "flowComputed": "dc-flow-computed",
    "forum": "dc-forum",
    "store": "dc-store",
}

# 爬虫资源接口主机地址。
crawler_resources_host = "http://192.168.16.7:16100"
# 获取随机微信万能key。
wechat_random_great_keys_api_url = f"{crawler_resources_host}/crawler_resources/get_random_wx_great_key"
# 获取随机微博cookie。
weibo_random_cookie_api_url = f"{crawler_resources_host}/crawler_resources/get_random_wb_cookie"
