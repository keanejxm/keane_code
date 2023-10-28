#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
信源类别排序。
# author: Trico
# date: 2021/1/4
# date: 2021/1/4
"""

import time
import elasticsearch

from common_utils.es.scroll_search_es import scroll_search_es


def paper_types_order(es_conn):
    """
    保存作品归类信息。
    :return:
    """

    index_name = "dc_source_types"
    now = int(time.time() * 1000)
    target_names = ["中央级别党报", "省市级别党报", "区县级别党报", "都市类", "财经类", "法制类", "科教人文类", "医药健康类", "老年生活类", "其他专业类", "境外报纸"]
    query_body = {
        "_source": ["_id", "name"],
        "query": {"bool": {"must": [{"term": {"parentID": "5_2"}}]}}
    }
    for hit in scroll_search_es(es_conn, index_name, query_body, limit=10 ** 5):
        field_id = hit["_id"]
        name = hit["name"]
        if hit["name"] in target_names:
            order = target_names.index(name) + 1
            fields = dict()
            fields["order"] = order
            fields["updateTime"] = now
            fields = dict(doc=fields)
            # print(hit, fields)
            res = es_conn.update(index=index_name, doc_type="_doc", body=fields, id=field_id)
            print(f"{field_id}，{fields}，{res}")
        else:
            print(f"未知，{hit}")


def region_level(es_conn):
    """
    信源级别。
    :return:
    """

    index_name = "dc_source_types"
    now = int(time.time() * 1000)
    data = [
        {
            "_id": "region_level_0",
            "_source": {
                "eName": "",
                "name": "地域级别",
                "describe": "",
                "parentID": None,
                "status": 1,
                "tagInfo": "",
                "order": 1,
                "createTime": now,
                "updateTime": now
            }
        },
        {
            "_id": "region_level_0_1",
            "_source": {
                "eName": "",
                "name": "中央级",
                "describe": "",
                "parentID": "region_level_0",
                "status": 1,
                "tagInfo": "",
                "order": 1,
                "createTime": now,
                "updateTime": now
            }
        },
        {
            "_id": "region_level_0_2",
            "_source": {
                "eName": "",
                "name": "省级",
                "describe": "",
                "parentID": "region_level_0",
                "status": 1,
                "tagInfo": "",
                "order": 2,
                "createTime": now,
                "updateTime": now
            }
        },
        {
            "_id": "region_level_0_3",
            "_source": {
                "eName": "",
                "name": "市级",
                "describe": "",
                "parentID": "region_level_0",
                "status": 1,
                "tagInfo": "",
                "order": 3,
                "createTime": now,
                "updateTime": now
            }
        },
        {
            "_id": "region_level_0_4",
            "_source": {
                "eName": "",
                "name": "区县级",
                "describe": "",
                "parentID": "region_level_0",
                "status": 1,
                "tagInfo": "",
                "order": 4,
                "createTime": now,
                "updateTime": now
            }
        },
        {
            "_id": "region_level_0_5",
            "_source": {
                "eName": "",
                "name": "乡镇级",
                "describe": "",
                "parentID": "region_level_0",
                "status": 1,
                "tagInfo": "",
                "order": 5,
                "createTime": now,
                "updateTime": now
            }
        }
    ]
    for item in data:
        field_id = item['_id']
        fields = item["_source"]
        res = es_conn.index(index=index_name, doc_type="_doc", body=fields, id=field_id)
        print(f"{field_id}，{fields}，{res}")


def important_media(es_conn):
    """
    重点渠道媒体。
    :return:
    """

    index_name = "dc_source_types"
    now = int(time.time() * 1000)
    data = [
        {
            "_id": "important_media",
            "_source": {
                "eName": "",
                "name": "重点渠道媒体",
                "describe": "信源中出现此_id，即代表为重点渠道媒体",
                "parentID": None,
                "status": 1,
                "tagInfo": "",
                "order": 1,
                "createTime": now,
                "updateTime": now
            }
        }
    ]
    for item in data:
        field_id = item['_id']
        fields = item["_source"]
        res = es_conn.index(index=index_name, doc_type="_doc", body=fields, id=field_id)
        print(f"{field_id}，{fields}，{res}")


def main_media(es_conn):
    """
    主流媒体。
    :return:
    """

    index_name = "dc_source_types"
    now = int(time.time() * 1000)
    data = [
        {
            "_id": "main_media",
            "_source": {
                "eName": "",
                "name": "主流媒体",
                "describe": "信源中出现此_id，即代表为主流媒体",
                "parentID": None,
                "status": 1,
                "tagInfo": "",
                "order": 1,
                "createTime": now,
                "updateTime": now
            }
        }
    ]
    for item in data:
        field_id = item['_id']
        fields = item["_source"]
        res = es_conn.index(index=index_name, doc_type="_doc", body=fields, id=field_id)
        print(f"{field_id}，{fields}，{res}")


def run():
    # 入口。

    es_hosts = [dict(host="192.168.16.21", port=9200)]
    es_conn = elasticsearch.Elasticsearch(hosts=es_hosts)

    # 报纸类别排序。
    # paper_types_order(es_conn)

    # 地域级别信息。
    # region_level(es_conn)

    # 重点渠道媒体。
    important_media(es_conn)

    # 主流媒体。
    main_media(es_conn)


if __name__ == '__main__':
    run()
