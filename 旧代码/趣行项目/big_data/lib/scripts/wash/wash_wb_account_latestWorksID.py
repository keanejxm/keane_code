# -*- coding: utf-8 -*-#

"""
# 清晰微博账号中的extendData字段下的latestWorksID值
# author: Chris
# date: 2021/1/13
# update: 2021/1/13
"""

import json
import time
import traceback
import elasticsearch
from api.config import es_config
from api_common_utils.utils import md5
from common_utils.es.scroll_search_es import scroll_search_es


def update_es_data():
    es_conn = elasticsearch.Elasticsearch(**es_config)
    index_name = "dc_accounts"
    query_body = {
        "_source": ["extendData", "platformID"],
        "query": {"bool": {"must": [
            # {"terms": {"name": ["北京日报"]}},
            # {"terms": {"name": [
            #     "光明日报", "新华每日电讯", "重庆日报",
            #     "北京日报", "辽宁日报", "昆明日报", "新华日报", "人民网", "中国银行", "财经时报",
            #     "紫光阁", "新华视点", "环球人物杂志", "人民画报", "天津网", "山西广播电视台",
            #     "腾讯视频", "网易汽车", "和讯网", "千龙网中国首都网", "健身专辑",
            #     "新浪汽车", "南宁日报", "廊坊晚报", "舟山网官方微博",
            #     "石家庄广播电视台", "秦皇岛晚报", "邯郸新闻网", "余杭晨报",
            #     "甘肃日报", "海南日报", "河北新闻网", "燕赵都市报",
            #     "宁夏日报", "四川日报", "广西日报", "解放日报", "湖南日报", "吉林日报", "河北日报", "马研网", "福建日报",
            #     "党史网", "中国教育在线", "经济参考报", "人民日报", "中国新闻周刊", "央视新闻", "文旅中国", "中国新闻网",
            #     "看电影", "微博明星", "腾讯自选股", "网路冷眼",
            #     "微博贵州", "中国长安网", "唐山消防", "邢台检察", "石家庄消防", "唐山检察",
            #     "太原户政", "晋中气象", "安徽共青团", "成都机关工委", "梨视频", "简阳总工会", "成化工商联", "成都校园",
            #     "温江工会", "成都科协", "温江妇联", "胡杨文化", "中国妇女出版社", "海尔兄弟", "开心麻花",
            #     "光线传媒", "迪士尼电影", "博纳影业集团"
            # ]}},
            {"term": {"platformType": 2}},
        ]}}
    }
    # res1 = es_conn.search(index=index_name, request_timeout=3600, body=query_body)
    for i, item in enumerate(
            scroll_search_es(es_conn, index_name, query_body, limit=1 * 10 ** 7, scroll="1h"),
            start=1
    ):
        try:
            # extendData不在item内指未采集过
            if "extendData" not in item:
                continue
            old_data = json.loads(item["extendData"])
            # latestWorksID不在old_data指采集过，但是没有这个值
            if "latestWorksID" not in old_data:
                body = {
                    "_source": ["title", "pubTime"],
                    "query": {"bool": {"must": [{"term": {"accountID": item["_id"]}}]}},
                    "sort": [{"pubTime": {"order": "desc"}}]}
                res1 = es_conn.search(index="dc_works", request_timeout=3600, body=body)
                old_title = old_data["title"]
                res1_title = res1["hits"]["hits"][0]["_source"]["title"]
                res1_pub = res1["hits"]["hits"][0]["_source"]["pubTime"]
                old_data["latestWorksID"] = res1["hits"]["hits"][0]["_id"]
                if old_title == res1_title:
                    filed = {"doc": {"extendData": json.dumps(old_data, ensure_ascii=False),
                                     "updateTime": int(time.time() * 1000)}}
                else:
                    old_data["title"] = res1_title
                    old_data["pubTime"] = res1_pub
                    filed = {"doc": {"extendData": json.dumps(old_data, ensure_ascii=False),
                                     "updateTime": int(time.time() * 1000)}}
                res = es_conn.update(index=index_name, doc_type="_doc", id=item["_id"], body=filed)
                continue
            # 下面意思是采集过但是值不对，把纯数字的worksId改为作品id
            if not old_data["latestWorksID"].isdigit():
                continue
            old_id = old_data["latestWorksID"]
            new_id = md5(item["platformID"] + old_id)
            old_data["latestWorksID"] = new_id
            filed = {"doc": {"extendData": json.dumps(old_data, ensure_ascii=False),
                             "updateTime": int(time.time() * 1000)}}
            res = es_conn.update(index=index_name, doc_type="_doc", id=item["_id"], body=filed)
            # print(res["_id"] + "-----" + res["result"])
        except Exception as e:
            print(f"{e}.\n{traceback.format_exc()}")
            print(item)
            print("--" * 10)
            continue


update_es_data()
