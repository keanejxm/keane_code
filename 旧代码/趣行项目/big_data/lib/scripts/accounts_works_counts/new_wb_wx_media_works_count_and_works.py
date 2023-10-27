# -*- coding: utf-8 -*-#
"""
# 微博微信自媒体单个账户的作品数统计
# author: Chris
# date: 2021/1/13
# update: 2021/1/13
"""
import json
import asyncio
import elasticsearch

from lib_conf.config import es_config
from common_utils.es.scroll_search_es import scroll_search_es


es_conn = elasticsearch.Elasticsearch(**es_config)


def get_and_save_count():
    body = {
      "size": 0,
      "query": {
        "bool": {
          "must": [
            {
              "terms": {
                "platformType": [
                  1,
                ]
              }
            }
          ]
        }
      },
      "aggs": {
        "group_by_accountID": {
          "terms": {
            "field": "accountID",
            "size": 2147483647
          }
        }
      }
    }
    res = es_conn.search(index="dc_works", doc_type="_doc", body=body)
    for r in res["aggregations"]["group_by_accountID"]["buckets"]:
        account_id = r["key"]
        works_num = r["doc_count"]
        fields = dict(doc={"worksNum": works_num})
        res = es_conn.update(index="dc_accounts", doc_type="_doc", id=account_id, body=fields)
        print(res)


def get_and_save_data():
    body = {
      "size": 0,
      "query": {
        "bool": {
          "must": [
            {
              "terms": {
                "platformType": [
                  1,
                ]
              }
            },
            {
              "range": {
                "pubTime": {
                  "gte": "now-3d/d"
                }
              }
            }
          ]
        }
      },
      "aggs": {
        "group_by_accountID": {
          "terms": {
            "field": "accountID",
            "size": 2147483647
          },
          "aggs": {
            "latest_works": {
              "top_hits": {
                "size": 1,
                "_source": [
                  "title", "pubTime"
                ],
                "sort": [
                  {
                    "pubTime": {
                      "order": "desc"
                    }
                  }
                ]
              }
            }
          }
        }
      }
    }
    res = es_conn.search(index="dc_works", doc_type="_doc", body=body)
    for r in res["aggregations"]["group_by_accountID"]["buckets"]:
        account_id = r["key"]
        _id = r["latest_works"]["hits"]["hits"][0]["_id"]
        title = r["latest_works"]["hits"]["hits"][0]["_source"]["title"]
        pubTime = r["latest_works"]["hits"]["hits"][0]["_source"]["pubTime"]
        data = {"latestWorksTitle": title, "latestWorksPubTime": pubTime, "latestWorksID": _id}
        data = json.dumps(data, ensure_ascii=False, separators=(", ", ":"))
        fields = dict(doc={"extendData": data})
        res = es_conn.update(index="dc_accounts", doc_type="_doc", id=account_id, body=fields)
        print(res)


def run():
    # get_and_save_count()
    get_and_save_data()


if __name__ == '__main__':
    run()

