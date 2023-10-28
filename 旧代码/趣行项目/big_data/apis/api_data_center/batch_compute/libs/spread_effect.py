# -*- coding:utf-8 -*-

"""
# 计算传播效果分析
# author: Chris
# date: 2020/12/15
# update: 2020/12/15
"""

import json
import traceback
import elasticsearch
from api.config import es_config
from api_common_utils.utils import md5
from batch_compute.libs.utils import ArticleSaveAndDeleteEs, result_to_tree, check_source_article


def cal_hamming_distance(vector1, vector2):
    vec1_int = int(('0b' + vector1), 2)
    vec2_int = int(('0b' + vector2), 2)
    # 异或操作
    num = vec1_int ^ vec2_int
    # 获取num中1的个数，即为海明距离
    count = 0
    for i in bin(num).replace('0b', ''):
        if i == '1':
            count += 1
    print(count)
    if count < 18:
        return count
    else:
        return None


class WorksSpreadEffect:

    def __init__(self, logger):
        # 设定海明距离参数
        self._limit_distance = 10
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
        # 进入新索引的默认字段
        self._similar_default = {
            "status": 1,
            "sourceId": "",                 # 某一作品的id
            "platformName": "",             # 某一作品的发表平台的名字
            "platformType": -1,
            "accountName": "",
            "title": "",                    # 某一作品的标题
            "simhash": "",
            "source": "",
            "pubTime": 0,                   # 某一作品的发布时间
            "isOriginal": -1,               # 某一作品是否原创
            "isOriginalCompute": -1,
            "matchScore": 0,               # 某一作品的匹配分数
            "simhash_count": 0,
            "similarId": "",                # 某一作品相似作品列表下的其中一个的id
            "similarUrl": "",               # 相似作品的url
            "similarPlatformType": -1,
            "similarPlatformName": "",      # 相似作品的发布平台名称
            "similarAccountName": "",
            "similarTitle": "",             # 相似作品的标题
            "similarSimHash": "",
            "similarPubTime": 0,            # 相似作品的发布时间
            "similarIsOriginal": -1,        # 某一作品是否原创
            "similarIsOriginalCompute": -1,
            "sourceSpreadRoute": []        # 相似作品各个之间的关系
        }

    def analyze_spread_route(self, source_detail, result):
        tree_result = []
        end_res = []
        if int(result["total"]) != 0:
            tree_result = result_to_tree(source_detail, result, self._logger)
            """处理新数据"""
            new_dict = dict(dict(), **self._similar_default)
            new_dict["sourceId"] = source_detail["_id"]
            new_dict["platformName"] = source_detail["platformName"]
            new_dict["platformType"] = source_detail["platformType"]
            new_dict["accountName"] = source_detail["accountName"]
            new_dict["title"] = source_detail["title"]
            new_dict["simhash"] = source_detail["simhash"]
            new_dict["pubTime"] = source_detail["pubTime"]
            new_dict["isOriginal"] = source_detail["isOriginal"]
            new_dict["isOriginalCompute"] = source_detail["isOriginalCompute"]
            for info in result["list"]:
                parse_fields = dict(dict(), **new_dict)
                parse_fields["source"] = info["source"]
                parse_fields["similarId"] = info["_id"]
                parse_fields["similarUrl"] = info["url"]
                parse_fields["similarPlatformName"] = info["platformName"]
                parse_fields["similarPlatformType"] = info["platformType"]
                parse_fields["similarAccountName"] = info["accountName"]
                parse_fields["similarTitle"] = info["title"]
                parse_fields["similarSimHash"] = info["simhash"]
                parse_fields["similarPubTime"] = info["pubTime"]
                parse_fields["similarIsOriginal"] = info["isOriginal"]
                try:
                    parse_fields["similarIsOriginalCompute"] = info["isOriginalCompute"]
                except:
                    parse_fields["similarIsOriginalCompute"] = -1
                mid_str1 = [i["parentId"] for i in tree_result if i["value"] == info["_id"]]
                mid_str2 = [i["value"] for i in tree_result if i["parentId"] == info["_id"]]
                parse_fields["sourceSpreadRoute"] = [mid_str1, mid_str2]
                end_res.append(parse_fields)
        hasSimilarWorks = hasSpread = hasSimilarOriginalWorks = 0
        # 是否有相似作品判断
        if len(end_res) > 0:
            hasSimilarWorks = 1
        # 是否有传播路径判断
        if len(tree_result) > 1:
            hasSpread = 1
        # 是否在相似中有原创作品存在
        for item in end_res:
            if item["similarPlatformName"] == "微博" and item["similarIsOriginal"] == 1:
                hasSimilarOriginalWorks = 1
                break
            else:
                if item["similarIsOriginalCompute"] == 1:
                    hasSimilarOriginalWorks = 1
                    break
        # 对该文章更新这三个字段
        field = {
            "hasSimilarWorks": hasSimilarWorks,
            "hasSpread": hasSpread,
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

    def search_es_by_content(self, source_detail, target_index_list, start_time, end_time):
        # 初始化结果集。
        result = list()

        filter_list = []
        should_list = []
        must_list = []
        """地名"""
        if len(source_detail["regionNames"]) > 0:
            for word in source_detail["regionNames"]:
                should_list.append({"match": {"regionNames": word}})
        """人名"""
        if len(source_detail["personNames"]) > 0:
            for word in source_detail["personNames"]:
                should_list.append({"match": {"personNames": word}})
        """组织名"""
        if len(source_detail["organizationNames"]) > 0:
            for word in source_detail["organizationNames"]:
                should_list.append({"match": {"organizationNames": word}})
        must_list.append({"bool": {"should": should_list}})
        """关键词,使用的词频那作关键词计算"""
        if source_detail["wordFrequency"]:
            keywords_query = []
            for word in source_detail["wordFrequency"]:
                # keywords_query.append({"term": {"keywords.word": word}})
                keywords_query.append({"term": {"wordFrequency.word": word["word"]}})
            nested_query = {
                "nested": {
                    "path": "wordFrequency",
                    "query": {"bool": {"should": keywords_query}},
                    "score_mode": "none"
                }}
            filter_list.append(nested_query)
        # if source_detail["keywords"]:
        #     for word in source_detail["keywords"]:
        #         should_list.append({"match": {"keywords": word}})
        must_list.append({"bool": {"should": should_list}})
        """时间"""
        must_list.append({"range": {"pubTime": {
            # "gte": source_detail["pubTime"],
            # "lte": source_detail["pubTime"] + 86400 * 30
            "gte": start_time,
            "lte": end_time
        }}})
        """内容"""
        must_list.append({"match": {"content": source_detail["content"]}})
        # must_list.append({"terms": {"hasDiscovery": [1]}})
        body = {
            "size": 9999,
            "_source": [],
            "query": {"bool": {
                "must": must_list,
                "filter": filter_list
            }},
            "sort": {"_score": "desc"}
        }
        res1 = self._es_conn.search(index=target_index_list, request_timeout=3600, body=body)
        if res1["hits"]["total"] > 0:
            max_score = int(res1["hits"]["max_score"])
            min_score = max_score * 0.5  # 计算最低分值，按0.8计算
            body["min_score"] = min_score
            res = self._es_conn.search(index=target_index_list, request_timeout=3600, body=body)
            # 去重集合，用于对匹配结果进行去重。
            unique_match_set = set()
            hits = res["hits"]["hits"]
            for hit in hits:
                try:
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
        result_pub = sorted(result, key=lambda x: x["pubTime"])
        if int(source_detail["platformType"]) != 2:
            if result_pub[0]["_id"] != source_detail["_id"]:
                source_detail["isOriginalCompute"] = 0
        return {"total": len(result), "list": result}

    def search_es_by_simhash(self, source_detail, target_index, start_time, end_time):
        source_list = ["title", "platformType", "hasDiscovery", "simhash"]
        must_list = list()
        must_list.append({"term": {"status": 1}})
        must_list.append({"range": {"pubTime": {"gte": start_time, "lte": end_time}}})
        query_body = {
            "size": 9999,
            # "_source": source_list,
            "query": {"bool": {"must": must_list}},
        }
        res1 = self._es_conn.search(index=target_index, doc_type="_doc", body=query_body, request_timeout=3600)
        works = []
        if res1["hits"]["total"] > 0:
            hits = res1["hits"]["hits"]
            for hit in hits:
                if "simhash" in hit["_source"].keys() and hit["_source"]["simhash"]:
                    ret = cal_hamming_distance(source_detail["simhash"], hit["_source"]["simhash"])
                    if ret:
                        sim_res = hit["_source"]
                        sim_res["_id"] = hit["_id"]
                        if sim_res["_id"] == source_detail["_id"]:
                            continue
                        sim_res["simhash_count"] = ret
                        if int(sim_res["platformType"]) != 2:
                            if not sim_res["source"]:
                                source = check_source_article(hit["_source"], self._logger)
                                sim_res["source"] = source
                            else:
                                source = sim_res["source"]
                            if source not in sim_res["platformName"]:
                                sim_res["isOriginalCompute"] = 0
                        works.append(sim_res)
        works = sorted(works, key=lambda x: x["simhash_count"])
        if len(works) > 0:
            if int(source_detail["platformType"]) != 2:
                if works[0]["_id"] != source_detail["_id"]:
                    source_detail["isOriginalCompute"] = 0
        return {"total": len(works), "list": works}

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
            "query": {"bool": {"must": must_list}},
            # 发布时间升序
            "sort": [{"pubTime": {"order": "asc"}}]
        }
        res1 = self._es_conn.search(index=target_index, doc_type="_doc", body=query_body, request_timeout=3600)
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
                    # 对平台类型不是2（微博）的作品判断其source来源
                    if int(work["platformType"]) != 2:
                        if not work["source"]:
                            source = check_source_article(item, self._logger)
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

    def api_search_es_by_query(self, request):
        source_detail = ""
        tree_result = []
        end_res = []
        try:
            self._logger.info("----Path: {}".format(request.get_full_path()))
            self._logger.info(f"请求体是：{str(request.body, encoding='utf8')}")
            body = json.loads(request.body)
            source_detail = body["source_detail"]
            start_time = body["start_time"]
            end_time = body["end_time"]
            """对文章进入临时es索引"""
            ArticleSaveAndDeleteEs().article_save_es(source_detail)
            # result = self._query_get_works_by_title(source_detail, self._target_index_list, start_time, end_time)
            images = source_detail["images"]
            article_type = source_detail["contentType"]
            # 纯视频情况下走标题
            if article_type == 3 and len(images) == 0:
                result = self.search_es_by_title(source_detail, self._target_index_list, start_time, end_time)
            else:
                result = self.search_es_by_content(source_detail, self._target_index_list, start_time, end_time)
            # 进行传播图分析
            if result["total"] > 0:
                fields, field_id, end_res = self.analyze_spread_route(source_detail, result)
                self._es_conn.update(index="dc_works", doc_type="_doc", id=field_id, body=fields)
                """存入传播路劲索引"""
                if end_res:
                    end_res = sorted(end_res, key=lambda x: x["pubTime"])
                    for res in end_res:
                        self._es_conn.index(index=self._similar_index, id=res["similarId"], body=res, doc_type="_doc")
            return dict(code=1, msg="success", data=end_res, tree_data=tree_result)
        except Exception as e:
            self._logger.warning(f"{e}.\n{traceback.format_exc()}")
            return dict(code=0, msg="failed")
        finally:
            """当查询完成之后删除临时索引内的文章"""
            ArticleSaveAndDeleteEs().article_delete_es(source_detail)

    def api_search_es_by_simhash(self, request):
        tree_result = []
        end_res = []
        try:
            self._logger.info("----Path: {}".format(request.get_full_path()))
            self._logger.info(f"请求体是：{str(request.body, encoding='utf8')}")
            body = json.loads(request.body)
            source_detail = body["source_detail"]
            start_time = body["start_time"]
            end_time = body["end_time"]
            result = self.search_es_by_simhash(source_detail, "dc_works", start_time, end_time)
            # 进行传播图分析
            if result["total"] > 0:
                fields, field_id, end_res = self.analyze_spread_route(source_detail, result)
                self._es_conn.update(index="dc_works", doc_type="_doc", id=field_id, body=fields)
                """存入传播路劲索引"""
                if end_res:
                    end_res = sorted(end_res, key=lambda x: x["simhash_count"])
                    for res in end_res:
                        self._es_conn.index(index="dc_custom", id=res["similarId"], body=res, doc_type="_doc")
            return dict(code=1, msg="success", data=end_res, tree_data=tree_result)
        except Exception as e:
            self._logger.warning(f"{e}.\n{traceback.format_exc()}")
            return dict(code=0, msg="failed")

    def api_search_es_by_query_and_simhash(self, request):
        try:
            self._logger.info("----Path: {}".format(request.get_full_path()))
            query_result = self.api_search_es_by_query(request)
            query_res = query_result["data"]
            query_tree = query_result["tree_data"]
            simhash_result = self.api_search_es_by_simhash(request)
            simhash_res = simhash_result["data"]
            simhash_tree = simhash_result["tree_data"]
            return dict(code=1, msg="success", query_data=query_res, query_tree=query_tree,
                        simhash_data=simhash_res, simhash_tree=simhash_tree)
        except Exception as e:
            self._logger.warning(f"{e}.\n{traceback.format_exc()}")
            return dict(code=0, msg="failed")

    def api_search_es_by_distance(self, request):
        """test1"""
        end_res = []
        self._logger.info("----Path: {}".format(request.get_full_path()))
        self._logger.info(f"请求体是：{str(request.body, encoding='utf8')}")
        try:
            body = json.loads(request.body)
            source_detail = body["source_detail"]
            start_time = body["start_time"]
            end_time = body["end_time"]
            result = self.search_es_by_distance(source_detail, self._target_index, start_time, end_time)
            # 进行传播图分析
            if result["total"] > 0:
                fields, field_id, end_res = self.analyze_spread_route(source_detail, result)
                self._es_conn.update(index="dc_works", doc_type="_doc", id=field_id, body=fields)
                """存入传播路劲索引"""
                if end_res:
                    for res in end_res:
                        self._es_conn.index(index=self._similar_index, id=res["similarId"], body=res, doc_type="_doc")
            return dict(code=1, msg="success", data=end_res)
        except Exception as e:
            self._logger.warning(f"{e}.\n{traceback.format_exc()}")
            return dict(code=0, msg="failed")



