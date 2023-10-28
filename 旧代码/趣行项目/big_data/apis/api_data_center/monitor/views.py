import datetime
import json
import time
import elasticsearch
import requests
from django.http import JsonResponse
from django.views import View
from api.config import es_config


class TopicMonitor(View):

    def post(self, request):
        # 取主题的id  主题的查询语句 主题的是否需要提醒
        request_data = json.loads(request.body)
        _id = request_data["id"]
        es_body = json.loads(request_data["es_body"])
        remind = request_data["remind"]

        # 2. 执行查询语句 可能是单个任务， 可能是多个任务 暂定为单个任务（考虑分布 因为是django 接口）
        es_conn = elasticsearch.Elasticsearch(**es_config)
        es_body["aggs"] = {
            "sum_hi": {
              "sum": {
                "field": "HI"
              }
            }
          }
        # 2.1 执行查询获取结果
        index_name = "dc_works"
        res = es_conn.search(index=index_name, body=es_body, doc_type="_doc")
        # 最新的所有稿件的数量
        total = res["hits"]["total"]
        # 最新的热度值的总和
        sum_hi = res["aggregations"]["sum_hi"]["value"]

        # 3. 将结果进行处理 然后存入es中供php查询
        index_monitor_name = "dc_topic_monitor"
        query_body = {
          "query": {
            "term": {
              "_id": "_id"
            }
          }
        }
        mon_res = es_conn.search(index=index_monitor_name, doc_type="_doc", body=query_body)

        # now 为当前程序运行时间的整点时间戳 统一到当前时间的小时
        date = datetime.datetime.now()
        time_str = str(date.year) + '-' + str(date.month) + '-' + str(date.day) + ' ' + str(date.hour)
        now = int(time.mktime(time.strptime(time_str, "%Y-%m-%d %H")) * 1000)
        # 当天的凌晨时间 为了统计 今日新增
        ling_chen_time = str(date.year) + '-' + str(date.month) + '-' + str(date.day)
        data_sj = time.strptime(ling_chen_time, "%Y-%m-%d")
        ling_chen_time = int(time.mktime(data_sj) * 1000)

        # 如果不存在就添加
        if mon_res["hits"]["hits"]:
            data = mon_res["hits"]["hits"][0]["_source"]
            todayNum = 0
            # 获取今日新增的数量
            for i in data[:-13]:
                if i["updateTime"] == ling_chen_time:
                    todayNum = total - i["data"]["topicTotal"]
                    break
            data_list = []
            data_list.extend(data["data"])
            topicAddCount = total - data["data"][-1]["topicTotal"]
            data_list.append({
                "topicTotal": total,
                "topicHI": sum_hi,
                "topicAddCount": topicAddCount,
                "createTime": now
            })
            update_body = {
                "doc": {
                    "todayNum": todayNum,
                    "updateTime": now,
                    "data": data_list,
                }}
            res = es_conn.update(
                index=index_monitor_name,
                doc_type="_doc",
                id=_id,
                body=update_body
            )
        else:
            data = {}
            # 当日新增为最新的主题的总数
            data["todayNum"] = total
            data["updateTime"] = now
            data_list = []
            data_list.append({
                "topicTotal": total,
                "topicHI": sum_hi,
                "topicAddCount": 0,
                "createTime": now
            })
            data["data"] = data_list
            res = es_conn.index(index=index_monitor_name, doc_type="_doc", body=data, id=_id)
        if remind == 1:
            # 回调php
            url = 'http://test.bigdata.hbrbdata.cn/admin/Callback/theme'
            data = {
                "id": _id,
                "pushTime": now
            }
            requests.post(url=url, data=data)
            pass
        res = dict(code=1, msg="success", data=res)
        return JsonResponse(res)

