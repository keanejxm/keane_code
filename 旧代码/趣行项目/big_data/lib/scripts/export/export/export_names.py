#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
导出账号名。
# author: Trico
# date: 2021/1/20
# date: 2021/1/20
"""

import traceback
import elasticsearch

from common_utils.utils import thread_print
from common_utils.es.scroll_search_es import scroll_search_es


def run():
    # 入口。

    es_hosts = [dict(
        host="192.168.16.21",
        port=9200,
    )]
    es_conn = elasticsearch.Elasticsearch(hosts=es_hosts)
    query_body = {
        "_source": ["platformName", "name"],
        "query": {"bool": {"must": [
            {"term": {"platformType": 7}}
        ]}},
        "sort": {"name": {"order": "asc"}}
    }
    index_name = "dc_accounts"
    thread_print(f"开始导数据：{index_name} 到 {index_name}.")
    # 执行更新。
    with open(f"./{index_name}.txt", "a") as fw:
        for i, hits in enumerate(scroll_search_es(es_conn, index_name, query_body, limit=1 * 10 ** 7), 1):
            # noinspection PyBroadException
            try:
                # 清洗历史数据。
                msg = f"{hits.get('platformName')}\t{hits.get('name')}\n"
                fw.write(msg)
            except Exception as e:
                thread_print(f"'{e}'\n{traceback.format_exc()}")


def run_forum_names():
    # 入口。

    es_hosts = [dict(
        host="192.168.16.21",
        port=9200,
    )]
    es_conn = elasticsearch.Elasticsearch(hosts=es_hosts)
    query_body = {
        "_source": ["platformName", "name"],
        "query": {"bool": {"must": [
            {"term": {"levelNumber": 3}}
        ]}},
        "sort": {"name": {"order": "asc"}}
    }
    index_name = "dc_forum"
    thread_print(f"开始导数据：{index_name} 到 {index_name}.")
    # 执行更新。
    with open(f"./{index_name}.txt", "a") as fw:
        for i, hits in enumerate(scroll_search_es(es_conn, index_name, query_body, limit=1 * 10 ** 7), 1):
            # noinspection PyBroadException
            try:
                # 清洗历史数据。
                msg = f"{hits.get('platformName')}\t{hits.get('name')}\n"
                fw.write(msg)
            except Exception as e:
                thread_print(f"'{e}'\n{traceback.format_exc()}")


if __name__ == '__main__':
    run_forum_names()
