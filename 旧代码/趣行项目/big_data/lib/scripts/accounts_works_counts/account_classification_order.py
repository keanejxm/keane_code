# -*- coding: utf-8 -*-#

"""
# 微博账户以及一级分类部分二级分类排序
# author: Chris
# date: 2021/1/21
# update: 2021/1/21
"""

import elasticsearch

from lib_conf.config import es_config


def account_order():
    es_conn = elasticsearch.Elasticsearch(**es_config)
    # must_list = list()
    # must_list.append({"term": {"parentID": "2_1_5"}})
    # must_list.append(({"term": {"name": "门户"}}))
    # must_list.append({"term": {"_id": "2_1_5_1"}})
    # query_body = {"query": {"bool": {"must": must_list}}}
    # res = es_conn.search(index=index_name, doc_type="_doc", body=query_body, request_timeout=3600)
    # print(res)
    """对dc_source_types中一级分类和部分二级分类添加order值"""
    # index_name = "dc_source_types"
    # fid = "2_1_3"
    # fields = {"doc": {"order": 5}}
    """dc_accounts中账户添加order值"""
    index_name = "dc_accounts"
    fid = "316364fb5c08650dfa3df8fb0d3021bc"
    # 在指定顺序中若没有该账号则顺延，不留其位置
    # 中央：无光明日报、解放军报、
    fields = {"doc": {"order": 103}}
    res = es_conn.update(index=index_name, doc_type="_doc", id=fid, body=fields)
    print(res["_id"] + "---" + res["result"])


account_order()
