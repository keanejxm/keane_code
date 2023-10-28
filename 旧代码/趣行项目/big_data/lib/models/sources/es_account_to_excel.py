# -*- coding: utf-8 -*-#

"""
# 统计近三天微博账户下数据情况
# author: Chris
# date: 2021/1/26
# update: 2021/1/26
"""

import elasticsearch
from api.config import es_config
import pandas as pd


def es_account_to_excel():
    es_conn = elasticsearch.Elasticsearch(**es_config)
    query_body = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "platformType": 2
                        }
                    },
                    {
                        "range": {
                            "pubTime": {
                                "gte": "2021-01-24"
                            }
                        }
                    }
                ]
            }
        },
        "aggs": {
            "group_by_platform": {
                "terms": {
                    "field": "platformName",
                    "size": 2147483647
                },
                "aggs": {
                    "group_by_account": {
                        "terms": {
                            "field": "accountName",
                            "size": 2147483647
                        },
                        "aggs": {
                            "group_by_pubTime": {
                                "date_histogram": {
                                    "field": "pubTime",
                                    "interval": "day",
                                    "format": "yyyy-MM-dd",
                                    "time_zone": "+08:00",
                                    "order": {
                                        "_key": "desc"
                                    },
                                    "missing": "1970-01-01"
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    res = es_conn.search(index="dc_works", request_timeout=3600, body=query_body)
    res_item = res["aggregations"]["group_by_platform"]["buckets"][0]["group_by_account"]["buckets"]
    rest = {
        "name": [],
        "counts": [],
        "2021-01-24": [],
        "2021-01-25": [],
        "2021-01-26": [],
        "2021-01-27": [],
    }
    for item in res_item:
        rest_item = item["group_by_pubTime"]["buckets"]
        rest["name"].append(item["key"])
        rest["counts"].append(item["doc_count"])
        for i in rest_item:
            if i["key_as_string"] == "2021-01-24":
                rest["2021-01-24"].append(i["doc_count"])
            elif i["key_as_string"] == "2021-01-25":
                rest["2021-01-25"].append(i["doc_count"])
            elif i["key_as_string"] == "2021-01-26":
                rest["2021-01-26"].append(i["doc_count"])
            else:
                rest["2021-01-27"].append(i["doc_count"])
        if len(rest["name"]) != len(rest["2021-01-24"]):
            rest["2021-01-24"].append(0)
        if len(rest["name"]) != len(rest["2021-01-25"]):
            rest["2021-01-25"].append(0)
        if len(rest["name"]) != len(rest["2021-01-26"]):
            rest["2021-01-26"].append(0)
        if len(rest["name"]) != len(rest["2021-01-27"]):
            rest["2021-01-27"].append(0)
    df = pd.DataFrame(rest)
    df.to_excel('1.xlsx', index=False)


es_account_to_excel()
