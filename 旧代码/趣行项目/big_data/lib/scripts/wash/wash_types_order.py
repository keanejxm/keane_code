#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
清洗信源类别的排序，根据地域信息编排。
# author: Trico
# date: 2020/12/22
# date: 2020/12/22
"""

import json
import traceback
import elasticsearch

from common_utils.utils import thread_print
from common_utils.es.scroll_search_es import scroll_search_es


def run_convert():
    # 入口。

    with open("/home/debugger/trico/big_data/big_data_platform/resources/region/regions.json", "rb") as fr:
        regions = json.loads(fr.read())
    region_dict = dict()
    for i, region in enumerate(regions, start=1):
        region_dict[region["name"]] = i

    es_hosts = [dict(
        host="192.168.16.21",
        port=9200,
    )]
    es_conn = elasticsearch.Elasticsearch(hosts=es_hosts)
    query_body = {
        "_source": ["name"],
        "query": {"bool": {"must": [
            {"term": {"parentID": "5_1"}}
        ]}},
        # "query": {"bool": {"must": [{"term": {"_id": "3a48d666cf08ac7f13538f848bf135d4"}}]}},
        # "sort": {"createDateTime": {"order": "desc"}},
    }
    index_names = [
        "dc_source_types",
    ]

    for index_name in index_names:
        thread_print(f"{index_name} start.")
        total = 0
        # 执行更新。
        try:
            for i, hit in enumerate(scroll_search_es(es_conn, index_name, query_body, limit=1 * 10 ** 7), 1):
                # noinspection PyBroadException
                try:
                    # 清洗历史数据。
                    field_id = hit["_id"]
                    name = hit["name"]
                    if name in region_dict:
                        order = region_dict[name]
                    else:
                        if name == "海外":
                            order = 35
                        else:
                            thread_print(f"未知名称：{name}")
                            continue
                    fields = dict(doc=dict(order=order))
                    # thread_print(f'{i:>6} {total:>6}: {field_id}, {name}, {fields}.')

                    # 执行更新。
                    res = es_conn.update(
                        index=index_name,
                        doc_type="_doc",
                        id=field_id,
                        body=fields
                    )

                    total += 1
                    thread_print(f'{i:>6} {total:>6} {res["result"]}: {field_id}, {name}, {fields}.')
                except Exception as e:
                    thread_print(f"{i:>6} {total:>6} '{e}'\n{traceback.format_exc()}")
        except Exception as e:
            thread_print(f"{index_name} '{e}'\n{traceback.format_exc()}")


if __name__ == '__main__':
    run_convert()
