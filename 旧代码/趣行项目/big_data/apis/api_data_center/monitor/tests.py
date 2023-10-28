import datetime
import time

import elasticsearch
import pymysql
from django.test import TestCase

# Create your tests here.
from api.config import es_config
from api_common_utils.mysql_utils import MySQLUtils

"""
# 主题监控的索引
PUT /dc_topic_monitor_v1
{
  "aliases": {
    "dc_topic_monitor": {}
  },
  "settings": {
    "index": {
      "number_of_shards": 8,
      "number_of_replicas": 1,
      "max_result_window": "1000000",
      "analysis": {
        "analyzer": {
          "jieba_analyzer": {
            "filter": [
              "unique",
              "lowercase"
            ],
            "char_filter": [
              "html_strip"
            ],
            "type": "custom",
            "tokenizer": "jieba_index"
          }
        }
      }
    }
  },
  "mappings": {
    "_doc": {
      "dynamic": "strict",
      "properties": {
        "topicName": {
          "type": "keyword"
        },
        "todayNum": {
              "type": "long"
            },
        "updateTime": {
          "type": "date"
        },
        "data": {
          "type": "nested",
          "properties": {
            "topicTotal": {
              "type": "long"
            },
            "topicAddCount": {
              "type": "long"
            },
            "topicHI": {
              "type": "float"
            },
            "createTime": {
              "type": "date"
            }
          }
        }
      }
    }
  }
}


需要存储的为主题的  稿件总数  今日新增  热度值  时间 
存储内容 & es 格式：
_id : 主题监控的 id
topicName ： "疫情", # 主题监控的名称
data : [
    {
    "topicTotal" : 1000,  稿件总数
    "topicAddCount"：1000, 稿件较昨日新增的数量
    "topicHI"：10.0, 热度值
    "createTime"：1610000000000, 添加的时间  例如为 1月11日 0点
    },
    
    {
    "topicTotal"：1100,  稿件总数
    "topicAddCount"：100, 稿件较昨日新增的数量
    "topicHI"：10.1, 热度值
    "createTime"：1610000000000, 添加的时间  例如为 1月11日 8点
    },
    {
    "topicTotal"：1200,  稿件总数
    "topicAddCount"：200, 稿件较昨日新增的数量
    "topicHI"：10.2, 热度值
    "createTime"：1610000000000, 添加的时间  例如为 1月11日 12点
    },
    ]


GET dc_works/_search
{
  "query":{
    "bool":{
      "must":[
        {
          "term":{"status":1}},
          {"range":{"pubTime":{"gte":"1597161600000","lte":"1609430399000"}}},
          {"bool":{"should":[{"regexp":{"title":"房子.*?"}},{"regexp":{"preTitle":"房子.*?"}},{"regexp":{"subTitle":"房子.*?"}},{"match":{"content":"房子"}},
          {"regexp":{"question":"房子.*?"}}]}},{"exists":{"field":"videos"}},{"range":{"contentWordsNum":{"gte":1,"lte":100000}}}],"must_not":[{"terms":{"keywords":["121"]}},{"exists":{"field":"images"}},{"bool":{"should":[{"terms":{"platformID":["4c80d36589adff0c8b091b189df9e69d"]}}]}},{"regexp":{"source":"房子.*?"}}]}},"sort":{"pubTime":{"order":"asc"}},"from":0,"size":"10","_source":{"excludes":["content","html","sentimentRawInfo","segmentWordsRawInfo"]}
  , "aggs": {
    "group_by_platformType": {
      "terms": {
        "field": "platformType",
        "size": 2147483647
      },
      "aggs": {
        "group_by_platformName": {
          "terms": {
            "field": "platformName",
            "size": 2147483647
          },
          "aggs": {
            "group_by_account": {
              "terms": {
                "field": "accountName",
                "size": 2147483647
              }
            }
          }
        }
      }
    }
  }
}

"""
mysql_config = {
            "host": "180.76.152.162",
            "port": 3306,
            "user": "kb_admin",
            "passwd": "8^s4!gac",
            "db": "bigdata",
            "charset": "utf8mb4",
            "cursorclass": pymysql.cursors.DictCursor
        }
db = MySQLUtils(**mysql_config)
sql = 'select * from user_theme'
res = db.search(sql)
# 取主题的id  主题的查询语句 主题的是否需要提醒
_id = ''
es_body = {
    "query": {
        "bool": {"must": [{"term":{"status":1}},{"range":{"pubTime":{"gte":"1597161600000","lte":"1609430399000"}}},{"bool":{"should":[{"regexp":{"title":"房子.*?"}},{"regexp":{"preTitle":"房子.*?"}},{"regexp":{"subTitle":"房子.*?"}},{"match":{"content":"房子"}},{"regexp":{"question":"房子.*?"}}]}},{"exists":{"field":"videos"}},{"range":{"contentWordsNum":{"gte":1,"lte":100000}}}],"must_not":[{"terms":{"keywords":["121"]}},{"exists":{"field":"images"}},{"bool":{"should":[{"terms":{"platformID":["4c80d36589adff0c8b091b189df9e69d"]}}]}},{"regexp":{"source":"房子.*?"}}]}},"sort":{"pubTime":{"order":"asc"}},"from":0,"size":"10"}
remind = 1

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
    "terms": {
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
    # 当日新增为最新的主题的总数
    data["todayNum"] = total
    data["updateTime"] = now
    data_list = []
    data["data"] = data_list.append({
        "topicTotal": total,
        "topicHI": sum_hi,
        "topicAddCount": 0,
        "createTime": now
    })
    res = es_conn.index(index=index_monitor_name, doc_type="_doc", body=data, id=_id)
else:
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
if remind == 1:
    # 回调php

    pass
res = dict(code=1, msg="success", data=res)
print()

