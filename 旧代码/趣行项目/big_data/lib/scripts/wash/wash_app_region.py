#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
清洗status字段。
# author: Trico
# date: 2021/1/12
# date: 2021/1/12
"""

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
        "_source": ["name"],
        "query": {"bool": {"must": [
            {"term": {"_id": "1eaeddc307f51c3b2d361fc45d482765"}},
            # {"term": {"isTop": "1"}}
        ]}},
        # "query": {"bool": {"must": [{"term": {"_id": "3a48d666cf08ac7f13538f848bf135d4"}}]}},
        # "sort": {"createDateTime": {"order": "desc"}},
    }
    index_names = [
        "dc_platforms",
    ]

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
                    name = hits["name"]
                    # if region == 1:
                    #     continue
                    fields = dict(doc=dict(order=110))

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
