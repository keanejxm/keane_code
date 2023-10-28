#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
清洗爬虫模板。
# author: Trico
# date: 2021/1/18
# date: 2021/1/18
"""

import json
import time
import traceback
import elasticsearch

from common_utils.utils import thread_print
from common_utils.es.scroll_search_es import scroll_search_es


def run_convert():
    # 入口。

    es_hosts = [dict(
        host="192.168.16.21",
        port=9200,
    )]
    es_conn = elasticsearch.Elasticsearch(hosts=es_hosts)
    query_body = {
        "_source": [],
        "query": {"bool": {"must": [
            {"term": {"platformType": 4}}
        ]}}
    }
    index_names = [
        "dc_source_spider_templates",
    ]

    now = int(time.time() * 1000)
    for index_name in index_names:
        thread_print(f"{index_name} start.")
        total = 0
        # 执行更新。
        try:
            for i, hits in enumerate(scroll_search_es(es_conn, index_name, query_body, limit=1 * 10 ** 7), 1):
                # noinspection PyBroadException
                try:
                    # 清洗历史数据。
                    field_id = hits["_id"]
                    platform_id = hits["platformID"]
                    platform_name = hits["platformName"]
                    value = json.loads(hits["value"])
                    value["platformID"] = platform_id
                    value["platformName"] = platform_name
                    fields = dict(doc=dict(
                        value=json.dumps(value, separators=(",", ":")),
                        createTime=now,
                        updateTime=now,
                    ))

                    # 执行更新。
                    res = es_conn.update(
                        index=index_name,
                        doc_type="_doc",
                        id=field_id,
                        body=fields
                    )

                    total += 1
                    thread_print(f'{i:>6} {total:>6} {res["result"]}: {field_id}, {fields}.')
                except Exception as e:
                    thread_print(f"{i:>6} {total:>6} '{e}'\n{traceback.format_exc()}")
        except Exception as e:
            thread_print(f"{index_name} '{e}'\n{traceback.format_exc()}")


if __name__ == '__main__':
    run_convert()
