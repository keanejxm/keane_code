#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
创建测试数据。
# author: Trico
# date: 2021/1/28
# date: 2021/1/28
"""

import time
import elasticsearch

from common_utils.utils import md5


def dc_test_image_hash(es_conn):
    """
    测试-图片哈希。
    :return:
    """

    # 时间。
    now = int(time.time() * 1000)
    # 数据。
    image_data = {
        "原图.jpg": "e0bc5e1155565266", "横向拉伸.png": "e0bc5e1155565266", "灰度.png": "e0bc5e1155565266",
        "加水印.png": "e07c4e1259547672", "截取.png": "df6f27585a7a6a5b", "模糊.png": "e0bcde1155565266",
        "任意拉伸.png": "e0bc5e1155565266", "竖向拉伸.png": "e0bc5e1155565266"
    }
    for file_name, hash_value in image_data.items():
        field_id = md5(file_name)
        fields = dict()
        fields["status"] = 1
        fields["url"] = "https://new.qq.com/omn/20210127/20210127A01O2L00.html"
        fields["title"] = "90后驻村干部692篇扶贫日记背后的故事"
        fields["digest"] = "2020年9月29日，骆胤成（右二）在云南宁蒗大兴镇黄板坪村与农户交谈。"
        fields["source"] = "腾讯新闻"
        fields["imageHash"] = [
            dict(
                url=f"https://bj.bcebos.com/v1/quxing-bigdata/test/big_data_platform/image_hash/{file_name}",
                hash=hash_value
            ),
            dict(
                url=f"https://bj.bcebos.com/v1/quxing-bigdata/test/big_data_platform/image_hash/无关.jpg",
                hash="e0c0d0d0d2cae8c8"
            ),
        ]
        fields["imageHashLength"] = len(fields["imageHash"])
        fields["pubTime"] = 1611704940000
        fields["createTime"] = now
        fields["updateTime"] = now
        res = es_conn.index(index="dc_test_image_hash", doc_type="_doc", body=fields, id=field_id)
        print(f"{field_id}，{fields}，{res}")


def run_store():
    # 入口。

    es_hosts = [dict(host="192.168.16.21", port=9200)]
    es_conn = elasticsearch.Elasticsearch(hosts=es_hosts)

    # 测试-图片哈希。
    dc_test_image_hash(es_conn)


if __name__ == '__main__':
    run_store()
