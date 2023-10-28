#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
获取公共参数。
# author: Trico
# date: 2021/1/18
# update: 2021/1/18
"""

import json
import elasticsearch

from lib_conf.config import es_config


def get_baidu_tags_to_classifications_map():
    """
    获取百度作品分类和作品归类的映射。
    :return:
    """

    # 连接ES。
    es_conn = elasticsearch.Elasticsearch(**es_config)
    # 索引名。
    index_name = "dc_public_params"
    # 请求体。
    query_body = {
        "size": 1,
        "_source": ["value"],
        "query": {"bool": {"must": [
            {"term": {"name": "baidu_tags_to_classifications_map"}},
            {"term": {"status": 1}}
        ]}},
    }

    res = es_conn.search(index=index_name, doc_type="_doc", body=query_body)
    if res["hits"]["total"] > 0:
        res = res["hits"]["hits"][0]["_source"]["value"]
        res = json.loads(res)
    return res


def get_data_plural_singular_map(map_direction="p_s"):

    if map_direction == "p_s":
        # 复数与单数映射。
        _map = dict(
            platforms="platform",
            accounts="account",
            channels="channel",
            epaperLayouts="epaperLayout",
            topics="topic",
            worksList="works",
            forums="forum",
            forumDetails="forumDetail",
            topQueries="topQuery",
        )
    elif map_direction == "s_p":
        # 单数与复数映射。
        _map = dict(
            platform="platforms",
            account="accounts",
            channel="channels",
            epaperLayout="epaperLayouts",
            topic="topics",
            works="worksList",
            forums="forums",
            forumDetail="forumDetails",
            topQuery="topQueries",
        )
    else:
        raise ValueError(f"未知参数，map_direction：{map_direction}")

    return _map


def test():
    res = get_baidu_tags_to_classifications_map()
    print(res)


if __name__ == "__main__":
    test()
