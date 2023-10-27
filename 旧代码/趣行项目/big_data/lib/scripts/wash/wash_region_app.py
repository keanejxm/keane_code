#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
添加region字段地域信息。
# author: Keane
# date: 2021/1/12
# date: 2021/1/12
"""
import json
import traceback
import elasticsearch

from common_utils.utils import thread_print
from common_utils.es.scroll_search_es import scroll_search_es



class AppendRegion(object):
    def __init__(self):
        self.es_hosts = [dict(host="192.168.16.21",port=9200,)]
        self.es_conn = elasticsearch.Elasticsearch(hosts=self.es_hosts)
    def get_type(self):
        query_body = {
        "_source": ["_id","name"],
        "query": {"bool": {"must": [
            {"term": {"_id": "4_3"}},
            # {"term": {"isTop": "1"}}
        ]}},
    }
        index_names = [
            "dc_source_types",
        ]
        for index_name in index_names:
            thread_print(f"{index_name}start")
            total = 0
            try:
                for i,hits in enumerate(scroll_search_es(self.es_conn,index_name,query_body,limit=1*10**7),1):
                    try:
                        field_id = hits["_id"]
                        field_name = hits["name"]
                        yield field_id,field_name
                    except Exception as e:
                        pass
            except:
                pass
    def get_platform(self):
        # for id, name in self.get_type():
            # name = name.replace("省","")
            query_body = {
                "_source": ["_id", "region"],
                "query": {"bool": {"must": [
                    {"term": {"types": "4_3"}},
                    # {"term": {"isTop": "1"}}
                ]}},
            }
            index_names = [
                "dc_platforms",
            ]
            for index_name in index_names:
                thread_print(f"{index_name} start.")
                total = 0
                # 执行更新。

                try:
                    for i, hits in enumerate(scroll_search_es(self.es_conn, index_name, query_body, limit=1 * 10 ** 7), 1):
                        # noinspection PyBroadException
                        try:
                            # 清洗历史数据。
                            field_id = hits["_id"]
                            region = hits["region"]
                            # types.append("region_level_0_1")
                            # types = json.loads(types)
                            # if types == 1:
                            #     continue
                            fields = dict(doc=dict(region=["北京"]))

                            # 执行更新。
                            res = self.es_conn.update(
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

def run():
    app_append_region = AppendRegion()
    app_append_region.get_platform()


if __name__ == '__main__':
    run()