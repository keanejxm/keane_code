# -*- coding: utf-8 -*-#

"""
# 计算传播效果分析--海明距离
# author: Chris
# date: 2021/1/13
# update: 2021/1/13
"""

import json
import traceback
import elasticsearch
from api.config import es_config
from api_common_utils.utils import md5
from batch_compute.libs.cirle_tree_data import CircleAndTreeData
from batch_compute.libs.utils import check_source_article, result_to_tree, result_to_tree_new, ArticleSaveAndDeleteEs
from batch_compute.libs.spread_hi_number import ComputeSpreadHi


class DistanceWorksSpreadEffect:

    def __init__(self, logger):
        # 设定海明距离参数
        self._limit_distance = 6
        # 日志
        self._logger = logger
        # 连接ES。
        self._es_conn = elasticsearch.Elasticsearch(**es_config)
        # 索引联合查询
        self._target_index_list = ["dc_works", "dc_temporary_works_test"]
        # 新索引存放相似作品列表，因为这是simhash算法获取，所以换一个索引
        self._similar_index = "dc_spread_route"
        # 目标索引
        self._target_index = "dc_works"
        # 账户索引，获取region
        self._target_account1 = "dc_accounts"
        # 账户索引，获取region
        self._target_account2 = "dc_platforms"
        # 进入新索引的默认字段
        self._similar_default = {
            "status": 1,
            # 2021/1/22暂时去掉
            # "platformName": "",             # 某一作品的发表平台的名字
            # "platformType": -1,
            # "accountName": "",
            # "title": "",                    # 某一作品的标题
            # "simhash": "",
            # "source": "",
            # "pubTime": 0,                   # 某一作品的发布时间
            # "isOriginal": -1,               # 某一作品是否原创
            # "isOriginalCompute": -1,
            # "matchScore": 0,               # 某一作品的匹配分数
            # "simhash_count": 0,
            "sourceId": "",                 # 某一作品的id
            "similarId": "",                # 某一作品相似作品列表下的其中一个的id
            "similarPlatformID": "",        # 相似作品的平台id
            "similarPlatformType": -1,
            "similarPlatformName": "",      # 相似作品的发布平台名称
            "similarChannelID": "",
            "similarChannelName": "",
            "similarAccountID": "",
            "similarAccountName": "",
            "similarTitle": "",             # 相似作品的标题
            "similarDigest": "",          # 相似作品的摘要
            "similarUrl": "",               # 相似作品的url
            "similarPubTime": 0,            # 相似作品的发布时间
            "similarIsOriginal": -1,        # 某一作品是否原创
            "similarIsOriginalCompute": -1,
            "similarCovers": list(),
            "similarVideos": list(),
            "similarAudios": list(),
            # "sourceSpreadRoute": [],        # 相似作品各个之间的关系
            "sourceParentId": "",            # 相似作品之间关系以parentId形式展现
            "similarRegion": list(),
            "similarSource": ""
        }

    def analyze_spread_route(self, source_detail, result):
        tree_result = []
        end_res = []
        if int(result["total"]) != 0:
            # tree_result = result_to_tree(source_detail, result, self._logger)
            tree_result = result_to_tree_new(source_detail, result, self._logger)
            """处理新数据"""
            new_dict = dict(dict(), **self._similar_default)
            # 原作品信息暂时去掉--2021/1/22
            # new_dict["platformName"] = source_detail["platformName"]
            # new_dict["platformType"] = source_detail["platformType"]
            # new_dict["accountName"] = source_detail["accountName"]
            # new_dict["title"] = source_detail["title"]
            # new_dict["source"] = source_detail["source"]
            # new_dict["pubTime"] = source_detail["pubTime"]
            # new_dict["isOriginal"] = source_detail["isOriginal"]
            # new_dict["isOriginalCompute"] = source_detail["isOriginalCompute"]
            new_dict["sourceId"] = source_detail["_id"]
            for info in result["list"]:
                parse_fields = dict(dict(), **new_dict)
                parse_fields["similarId"] = info["_id"]
                parse_fields["similarPlatformID"] = info["platformID"]
                parse_fields["similarPlatformType"] = info["platformType"]
                parse_fields["similarPlatformName"] = info["platformName"]
                parse_fields["similarChannelID"] = info["channelID"]
                parse_fields["similarChannelName"] = info["channelName"]
                parse_fields["similarAccountID"] = info["accountID"]
                parse_fields["similarAccountName"] = info["accountName"]
                parse_fields["similarTitle"] = info["title"]
                parse_fields["similarDigest"] = info["digest"]
                parse_fields["similarUrl"] = info["url"]
                parse_fields["similarPubTime"] = info["pubTime"]
                parse_fields["similarIsOriginal"] = info["isOriginal"]
                try:
                    parse_fields["similarIsOriginalCompute"] = info["isOriginalCompute"]
                except:
                    parse_fields["similarIsOriginalCompute"] = -1
                parse_fields["similarCovers"] = info["covers"]
                parse_fields["similarVideos"] = info["videos"]
                parse_fields["similarAudios"] = info["audios"]
                parse_fields["similarSource"] = info["source"]
                # parse_fields["similarSource"] = info["source"]
                mid_str1 = [i["parentId"] for i in tree_result if i["_id"] == info["_id"]]
                # mid_str2 = [i["value"] for i in tree_result if i["parentId"] == info["_id"]]
                # parse_fields["sourceSpreadRoute"] = [mid_str1, mid_str2]
                if len(mid_str1) != 0:
                    parse_fields["sourceParentId"] = mid_str1[0]
                """查对应的信源名字，补充region字段信息"""
                must_list = list()
                if info["platformType"] in (1, 2, 7):
                    must_list.append({"term": {"name": info["accountName"]}})
                    must_list.append({"term": {"platformType": info["platformType"]}})
                    query_body = {"_source": ["region"], "query": {"bool": {"must": must_list}}}
                    res = self._es_conn.search(index=self._target_account1, doc_type="_doc", body=query_body, request_timeout=3600)
                else:
                    must_list.append({"term": {"name": info["platformName"]}})
                    must_list.append({"term": {"type": info["platformType"]}})
                    query_body = {"_source": ["region"], "query": {"bool": {"must": must_list}}}
                    res = self._es_conn.search(index=self._target_account2, doc_type="_doc", body=query_body, request_timeout=3600)
                try:
                    region = res["hits"]["hits"][0]["_source"]["region"]
                except:
                    region = []
                    self._logger.warning(f'查询地域信息报错：原始：信息是{res["hits"]["hits"]}')
                parse_fields["similarRegion"] = region
                end_res.append(parse_fields)
        hasSimilarWorks = hasSimilarOriginalWorks = 0
        # 是否有相似作品判断
        if len(end_res) > 0:
            hasSimilarWorks = 1
        # 是否在相似中有原创作品存在
        for item in end_res:
            if item["similarPlatformName"] == "微博" and item["similarIsOriginal"] == 1:
                hasSimilarOriginalWorks = 1
                break
            else:
                if item["similarIsOriginalCompute"] == 1 or item["similarIsOriginal"] == 1:
                    hasSimilarOriginalWorks = 1
                    break
        # 对该文章更新这三个字段
        field = {
            "hasSimilarWorks": hasSimilarWorks,
            "hasSimilarOriginalWorks": hasSimilarOriginalWorks
        }
        field_id = source_detail["_id"]
        fields = dict(doc=field)
        return fields, field_id, end_res

    def search_es_by_title(self, source_detail, target_index_list, start_time, end_time):
        # 初始化结果集。
        result = list()
        # 组合检索体。
        must_list = [
            {"range": {"pubTime": {
                # "gte": source_detail["pubTime"],
                # "lte": source_detail["pubTime"] + 86400 * 30
                "gte": start_time,
                "lte": end_time
            }}},
            {"match": {"title": source_detail["title"]}}]
        body = {
            "size": 9999,
            "_source": [],
            "query": {"bool": {"must": must_list}},
            "sort": {"_score": "desc"}
        }
        res1 = self._es_conn.search(index=target_index_list, request_timeout=3600, body=body)
        if res1["hits"]["total"] > 0:
            max_score = int(res1["hits"]["max_score"])
            min_score = max_score * 0.8     # 计算最低分值，按0.8计算
            body["min_score"] = min_score
            res = self._es_conn.search(index=target_index_list, request_timeout=3600, body=body)
            # 去重集合，用于对匹配结果进行去重。
            unique_match_set = set()
            hits = res["hits"]["hits"]
            for hit in hits:
                try:
                    # 如果查询结果分数大于待匹配文章分数，跳过
                    if int(hit["_score"]) > max_score:
                        continue
                    # 如果查询ID为本身则跳过
                    if hit["_id"] == source_detail["_id"]:
                        continue
                    item = hit["_source"]
                    item["_id"] = hit["_id"]
                    title = item["title"]
                    if not title:  # 标题为空的不添加
                        continue
                    # 匹配分值。
                    item["matchScore"] = int(hit["_score"]) / max_score
                    # 去重。
                    unique_match_id = md5(item["platformName"] + item["url"].strip())
                    if unique_match_id in unique_match_set:
                        continue
                    else:
                        unique_match_set.add(unique_match_id)
                    """去重完成之后整理content字段，除去微博以外都让正则以\转发\等字样洗一遍content字段"""
                    if int(item["platformType"]) != 2:
                        if not item["source"]:
                            source = check_source_article(item, self._logger)
                            item["source"] = source
                        else:
                            source = item["source"]
                        if source not in item["platformName"]:
                            item["isOriginalCompute"] = 0
                    result.append(item)
                except Exception as e:
                    print(f"{e}\n{traceback.format_exc()}")
                    continue
        total_end = len(result)
        # 按时间降序排序
        result_pub = sorted(result, key=lambda x: x["pubTime"])
        if int(source_detail["platformType"]) != 2:
            if result_pub[0]["_id"] != source_detail["_id"]:
                source_detail["isOriginalCompute"] = 0
        return {"total": total_end, "list": result}

    def search_es_by_distance(self, source_detail, start_time, end_time, target_index):
        must_list = list()
        must_list.append({"term": {"status": 1}})
        must_list.append({"range": {"pubTime": {"gte": start_time, "lte": end_time}}})
        # 实现搜索中计算海明距离的脚本
        script_params = {
            "script": {
                "script": {
                    "source": """
                   int total = 0;
                   for (int i = 0; i < doc['simhash'].value.length(); ++i) {
                     if(params.input_sim.charAt(i)!=doc['simhash'].value.charAt(i)) {total++;}}
                   if (total <= params.limit){
                     return true
                   } else {
                     return false
                   }
                 """,
                    "lang": "painless",
                    "params": {
                        "input_sim": source_detail["simhash"],
                        "limit": self._limit_distance
                    }
                }
            }
        }
        must_list.append(script_params)
        query_body = {
            "size": 9999,
            # "_source": source_list,
            "query": {"bool": {"must": must_list,
                               # 查询结果去点simhash为空的
                               "must_not": {"term": {"simhash": ""}}}},
            # 发布时间升序
            "sort": [{"pubTime": {"order": "asc"}}]
        }
        res1 = self._es_conn.search(index=target_index, doc_type="_doc", body=query_body, request_timeout=3600 * 5)
        self._logger.info(f"查询的相似作品数是：{res1['hits']['total']}")
        works = []
        if res1["hits"]["total"] > 0:
            item_res = res1["hits"]["hits"]
            # 对作品本身的原创与否有个计算值
            if int(source_detail["platformType"]) != 2:
                if item_res[0]["_id"] != source_detail["_id"]:
                    source_detail["isOriginalCompute"] = 0
            for item in item_res:
                # 作品本身跳过
                try:
                    if item["_id"] == source_detail["_id"]:
                        continue
                    work = item["_source"]
                    work["_id"] = item["_id"]
                    if not work["simhash"]:
                        continue
                    # 对平台类型不是2（微博）的作品判断其source来源
                    if int(work["platformType"]) != 2:
                        if not work["source"]:
                            source = check_source_article(work, self._logger)
                            work["source"] = source
                        else:
                            source = work["source"]
                        if source not in work["platformName"]:
                            work["isOriginalCompute"] = 0
                    works.append(work)
                except Exception as e:
                    self._logger.warning(f"处理作品id为{item['_id']}报错：, {e}\n{traceback.format_exc()}")
                    continue
        else:
            works = []
            self._logger.warning(f"作品_id是{source_detail['_id']}经海明距离计算没有{self._limit_distance}以内的作品，故该作品无相似作品")

        return {"total": len(works), "list": works}

    def api_search_es_by_distance(self, request):
        end_res = []
        self._logger.info("----Path: {}".format(request.get_full_path()))
        self._logger.info(f"请求体是：{str(request.body, encoding='utf8')}")
        try:
            body = json.loads(request.body)
            source_detail = body["source_detail"]
            start_time = body["start_time"]
            end_time = body["end_time"]
            if int(source_detail["contentType"]) not in (4, 5, 6, 7):
                result = self.search_es_by_distance(source_detail, start_time, end_time, self._target_index)
            else:
                """对文章进入临时es索引"""
                ArticleSaveAndDeleteEs().article_save_es(source_detail)
                result = self.search_es_by_title(source_detail,  self._target_index_list, start_time, end_time)
                """当查询完成之后删除临时索引内的文章"""
                ArticleSaveAndDeleteEs().article_delete_es(source_detail)
            # 进行传播图分析
            if result["total"] > 0:
                detail = "待查作品有相似作品"
                # 产生相似作品
                fields, field_id, end_res = self.analyze_spread_route(source_detail, result)
                # 对spreadHi热度值分析
                fields_hi, field_id = ComputeSpreadHi().run(source_detail, end_res)
                # 对两个要更新的字段合并
                fields["doc"] = {**fields["doc"], **fields_hi["doc"]}
                """存入传播路劲索引"""
                if len(end_res) != 0:
                    for res in end_res:
                        self._es_conn.index(index=self._similar_index, id=res["similarId"], body=res, doc_type="_doc")
                    """在有相似作品的情况下去找传播路径，并生产泡状图与树状图"""
                    fields_spread, field_id = CircleAndTreeData().circle_data_res(source_detail)
                    # 对两个要更新的字段合并
                    fields["doc"] = {**fields["doc"], **fields_spread["doc"]}
                self._es_conn.update(index="dc_works", doc_type="_doc", id=field_id, body=fields)
                data = dict(code=1, msg="success", detail=detail, data=end_res)
            else:
                detail = "待查作品没有相似作品"
                data = dict(code=1, msg="success", detail=detail, data=end_res)
            return data
        except Exception as e:
            self._logger.warning(f"{e}.\n{traceback.format_exc()}")
            return dict(code=0, msg="failed")
