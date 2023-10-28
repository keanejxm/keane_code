#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
清洗客户端信源，order字段。
此脚本定制性强，不要用于其它非必须场景中。
# author: Trico
# date: 2021/1/23
# date: 2021/1/23
"""

import json
import traceback
import elasticsearch

from common_utils.utils import thread_print
from common_utils.es.scroll_search_es import scroll_search_es


def run_restore_source_types():
    # 因误删数据，而从快照索引中恢复。

    es_hosts = [dict(
        host="192.168.16.21",
        port=9200,
    )]
    es_conn = elasticsearch.Elasticsearch(hosts=es_hosts)
    query_body = {
        "_source": [],
        "query": {"bool": {"must": [
            {"regexp": {"parentID": {"value": "4_1"}}}
        ]}}
    }
    index_name = "restored_dc_source_types_v1"

    thread_print(f"{index_name} start.")
    total = 0
    # 执行更新。
    for i, hits in enumerate(scroll_search_es(es_conn, index_name, query_body, limit=1 * 10 ** 7), 1):
        # noinspection PyBroadException
        try:
            # 清洗历史数据。
            field_id = hits.pop("_id")
            fields = hits

            # 执行更新。
            if not es_conn.exists(
                index="dc_source_types_v1",
                doc_type="_doc",
                id=field_id,
            ):
                res = es_conn.index(
                    index="dc_source_types_v1",
                    doc_type="_doc",
                    id=field_id,
                    body=fields
                )
            else:
                thread_print(f'{i:>6} {total:>6} 已存在，{field_id}')
                continue

            total += 1
            thread_print(f'{i:>6} {total:>6} {res}, {fields}')
        except Exception as e:
            thread_print(f"{i:>6} {total:>6} '{e}'\n{traceback.format_exc()}")


def run_convert_source_types():
    # 入口。

    es_hosts = [dict(
        host="192.168.16.21",
        port=9200,
    )]
    es_conn = elasticsearch.Elasticsearch(hosts=es_hosts)
    query_body = {
        "_source": [],
        "query": {"bool": {"must": [
            {"regexp": {"parentID": {"value": "4_5.*?"}}}
        ]}}
    }
    index_name = "dc_source_types"

    thread_print(f"{index_name} start.")
    total = 0
    # 执行更新。
    for i, hits in enumerate(scroll_search_es(es_conn, index_name, query_body, limit=1 * 10 ** 7), 1):
        # noinspection PyBroadException
        try:
            # 清洗历史数据。
            field_id = hits.pop("_id")
            if hits["name"] == "北京市":
                field_id = "4_1_41"
            elif hits["name"] == "天津市":
                field_id = "4_1_42"
            elif hits["name"] == "上海市":
                field_id = "4_1_43"
            else:
                thread_print(f"未知类型：{field_id}，{hits}")
            hits["parentID"] = hits["parentID"].replace("4_5", "4_1")
            fields = hits

            # 执行更新。
            res = es_conn.index(
                index=index_name,
                doc_type="_doc",
                id=field_id,
                body=fields
            )

            total += 1
            thread_print(f'{i:>6} {total:>6} {res}, {fields}')
        except Exception as e:
            thread_print(f"{i:>6} {total:>6} '{e}'\n{traceback.format_exc()}")


def run_convert_platforms():
    # 入口。

    es_hosts = [dict(
        host="192.168.16.21",
        port=9200,
    )]
    es_conn = elasticsearch.Elasticsearch(hosts=es_hosts)
    query_body = {
        "_source": ["types"],
        "query": {"bool": {"must": [
            {"regexp": {"types": {"value": "4_5.*?"}}}
        ]}}
    }
    index_name = "dc_platforms"

    thread_print(f"{index_name} start.")
    total = 0
    # 执行更新。
    for i, hits in enumerate(scroll_search_es(es_conn, index_name, query_body, limit=1 * 10 ** 7), 1):
        # noinspection PyBroadException
        try:
            # 清洗历史数据。
            field_id = hits.pop("_id")
            source_types = hits["types"]
            new_source_types = list()
            for source_type in source_types:
                if source_type.startswith("4_5_1"):
                    new_source_types.append(source_type.replace("4_5_1", "4_1_41"))
                elif source_type.startswith("4_5_2"):
                    new_source_types.append(source_type.replace("4_5_2", "4_1_42"))
                elif source_type.startswith("4_5_3"):
                    new_source_types.append(source_type.replace("4_5_3", "4_1_43"))
                else:
                    new_source_types.append(source_type)
            if not new_source_types:
                continue
            fields = dict(doc=dict(types=new_source_types))

            # 执行更新。
            res = es_conn.update(
                index=index_name,
                doc_type="_doc",
                id=field_id,
                body=fields
            )

            total += 1
            thread_print(f'{i:>6} {total:>6} {res["result"]}: {field_id}, {fields}')
        except Exception as e:
            thread_print(f"{i:>6} {total:>6} '{e}'\n{traceback.format_exc()}")


def run_source_types_order():
    # 入口。

    with open("../../../resources/region/regions.json", "rb") as fr:
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
            {"term": {"parentID": "4_1"}}
        ]}}
    }
    index_name = "dc_source_types"

    thread_print(f"{index_name} start.")
    total = 0
    # 执行更新。
    for i, hit in enumerate(scroll_search_es(es_conn, index_name, query_body, limit=1 * 10 ** 7), 1):
        # noinspection PyBroadException
        try:
            # 清洗数据。
            field_id = hit["_id"]
            name = hit["name"]
            for region, _order in region_dict.items():
                if region in name:
                    order = _order
                    break
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


def run_convert_platforms_shanghai():
    # 入口。

    es_hosts = [dict(
        host="192.168.16.21",
        port=9200,
    )]
    es_conn = elasticsearch.Elasticsearch(hosts=es_hosts)
    query_body = {
        "_source": ["types"],
        "query": {"bool": {"must": [
            {"term": {"types": {"value": "4_1_43"}}}
        ]}}
    }
    index_name = "dc_platforms"

    thread_print(f"{index_name} start.")
    total = 0
    # 执行更新。
    for i, hits in enumerate(scroll_search_es(es_conn, index_name, query_body, limit=1 * 10 ** 7), 1):
        # noinspection PyBroadException
        try:
            # 清洗历史数据。
            field_id = hits.pop("_id")
            source_types = hits["types"]
            new_source_types = list()
            for source_type in source_types:
                if source_type.startswith("4_1_43"):
                    new_source_types.append(source_type.replace("4_1_43", "4_1_6"))
                else:
                    new_source_types.append(source_type)
            if not new_source_types:
                continue
            fields = dict(doc=dict(types=new_source_types))

            # 执行更新。
            res = es_conn.update(
                index=index_name,
                doc_type="_doc",
                id=field_id,
                body=fields
            )

            total += 1
            thread_print(f'{i:>6} {total:>6} {res["result"]}: {field_id}, {fields}')
        except Exception as e:
            thread_print(f"{i:>6} {total:>6} '{e}'\n{traceback.format_exc()}")


if __name__ == '__main__':
    # run_restore_source_types()
    # run_convert_source_types()
    # run_convert_platforms()
    run_source_types_order()
    # run_convert_platforms_shanghai()
