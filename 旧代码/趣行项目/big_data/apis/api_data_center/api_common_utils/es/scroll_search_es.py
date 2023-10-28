#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
分页查询ES数据。
# author: Trico
# date: 2019.8.7
"""


def scroll_search_es(es_conn, index_name, query_body=None, per_hits=100, limit=1):
    """
    从ES中查询数据。
    :return:
    """

    # 参数验证。
    assert int(per_hits) > 0

    # 初始化请求体。
    if not query_body:
        query_body = {"sort": {"createTime": {"order": "desc"}}}

    # 每次查询的返回数目。
    per_hits = per_hits

    # 发起检索请求。
    scroll_response = es_conn.search(
        index=index_name,
        body=query_body,
        scroll='5m',
        size=per_hits,
    )
    scroll_id = scroll_response['_scroll_id']
    total = scroll_response['hits']['total']

    try:
        length = 0
        for scroll_hit in scroll_response['hits']['hits']:
            scroll_hit['_source']['_id'] = scroll_hit['_id']
            yield scroll_hit['_source']

            length += 1
            if length >= limit:
                break

        # 返回数目不够时，继续获取数据。
        if length < limit:
            for i in range(0, int(total / per_hits) + 1):
                try:
                    scroll_response = es_conn.scroll(scroll_id=scroll_id, scroll='5m')
                    for scroll_hit in scroll_response['hits']['hits']:
                        scroll_hit['_source']['_id'] = scroll_hit['_id']
                        yield scroll_hit['_source']

                        length += 1
                        if length >= limit:
                            raise StopIteration
                except StopIteration:
                    break
    except StopIteration:
        # noinspection PyBroadException
        try:
            # 如果不再使用，调用关闭，不然多次查询会维护很多个scroll，损耗性能。
            es_conn.clear_scroll(scroll_id)
        except Exception:
            pass
        raise StopIteration
