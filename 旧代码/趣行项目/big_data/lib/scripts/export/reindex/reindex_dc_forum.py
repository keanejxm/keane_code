#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
重新导一次dc_forum索引的数据。
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
        "query": {"bool": {"must": []}}
    }
    src_index_name = "dc_forum_v1"
    dst_index_name = "dc_forum_v2"

    thread_print(f"开始导数据：{src_index_name} 到 {dst_index_name}.")
    total = 0
    # 执行更新。
    for i, hits in enumerate(scroll_search_es(es_conn, src_index_name, query_body, limit=1 * 10 ** 7), 1):
        # noinspection PyBroadException
        try:
            # 清洗历史数据。
            field_id = hits.pop("_id")
            hits["sourceTypesName"] = hits.pop("sourceTypesNmae")

            # 执行更新。
            res = es_conn.index(
                index=dst_index_name,
                doc_type="_doc",
                id=field_id,
                body=hits
            )

            total += 1
            thread_print(f'{i:>6} {total:>6} {res}')
        except Exception as e:
            thread_print(f"{i:>6} {total:>6} '{e}'\n{traceback.format_exc()}")


if __name__ == '__main__':
    run()
