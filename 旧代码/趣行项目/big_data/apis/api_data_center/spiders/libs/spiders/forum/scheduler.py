# -*- coding:utf-8 -*-
"""

# author: albert
# date: 2020/12/28
# update: 2020/12/28
"""
import elasticsearch
from loguru import logger
from spiders.libs.spiders.forum.forum_run import ForumRun, es_config


def save_to_es(res):
    forum_list = res["data"]["forums"]
    forum_detail = res["data"]["forumDetails"]
    es_conn = elasticsearch.Elasticsearch(**es_config)
    if forum_list:
        for forum in forum_list:
            fetch_id = forum.pop("_id")
            fetch_data = forum
            r = es_conn.index(index="dc_forum", id=fetch_id, doc_type="_doc", body=fetch_data)
            logger.debug(r)
    if forum_detail:
        for detail in forum_detail:
            _id = detail.pop("_id")
            detail_fetch_data = detail
            r = es_conn.index(index="dc_forum_details", id=_id, doc_type="_doc", body=detail_fetch_data)
            logger.debug(r)


def save_yeild_es(res):
    es_conn = elasticsearch.Elasticsearch(**es_config)
    if "forum" in res:
        forum = res["forum"]
        fetch_id = forum.pop("_id")
        fetch_data = forum
        r = es_conn.index(index="dc_forum", id=fetch_id, doc_type="_doc", body=fetch_data)
        logger.debug(f'{forum["name"]}: {r}')
    else:
        detail = res["forumDetail"]
        _id = detail.pop("_id")
        detail_fetch_data = detail
        r = es_conn.index(index="dc_forum_details", id=_id, doc_type="_doc", body=detail_fetch_data)
        logger.debug(r)


def run_from_name(name):
    es_hosts = [dict(
        host="192.168.16.21",
        port=9200,
    )]
    es_conn = elasticsearch.Elasticsearch(hosts=es_hosts)
    body = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"name": {"value": name}}}
                    # {"term": {"levelNumber": 3}}
                ]
            }
        }
    }
    res = es_conn.search(index="dc_forum", doc_type="_doc", body=body)
    res = res["hits"]["hits"][0]
    data = res["_source"]
    data["_id"] = res["_id"]
    res = ForumRun(logger).fetch_yield(data)
    for r in res:
        if r["code"] == 1:
            save_yeild_es(r["data"])
        print(r)


if __name__ == '__main__':
    # 河北吧   贴吧热榜  河北  知乎热榜  热点话题
    name = '社会事件及话题'
    run_from_name(name)

