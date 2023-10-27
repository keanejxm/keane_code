# -*- coding: utf-8 -*-#
# Date:         2021/1/20

import elasticsearch


def run_convert():
    # 入口。

    es_hosts = [dict(
        host="192.168.16.21",
        port=9200,
    )]
    es_conn = elasticsearch.Elasticsearch(hosts=es_hosts)
    query_body = {
        "size": 9999,
        "_source": ["types"],
        "query": {"bool": {"must": [
            {"term": {"platformType": "2"}},
            {"terms": {"types": ["2_1_5_5"]}}
        ]}},
    }
    index_names = "dc_accounts"
    res = es_conn.search(index=index_names, doc_type="_doc", body=query_body, request_timeout=3600)
    total = 0
    for item in res["hits"]["hits"]:
        fid = item["_id"]
        fields = {"doc": {"types": ["2_1_5_5", "region_level_0_4"]}}
        res = es_conn.update(index=index_names,  doc_type="_doc",  id=fid,  body=fields)
        print(res["_id"] + "----" + res["result"])
        total += 1
    print(total)


run_convert()
