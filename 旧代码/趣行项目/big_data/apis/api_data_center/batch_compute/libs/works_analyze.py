# -*- coding:utf-8 -*-

"""
# 作品分析
# author: Chris
# date: 2020/12/9
# update: 2020/12/9
"""

import re
import json
import traceback
import elasticsearch
from api.config import es_config
from bs4 import BeautifulSoup
from api_common_utils.utils import md5

from batch_compute.libs.utils import ArticleSaveAndDeleteEs, check_source_article


class BigDataWorksAnalyze:

    def __init__(self, logger):
        # 连接ES。
        self._es_conn = elasticsearch.Elasticsearch(**es_config)
        # 索引名。
        self._yym_discover_works_index = "yym_discover_works"
        # 索引联合查询
        self._target_index_list = ["yym_discover_works", "dc_temporary_works_test"]
        # 百分数
        self._percent = 0.8
        # 日志
        self._logger = logger
        # 搜索结果展示字段
        self._source_default_dict = {
            "nickName": "",
            "avatar": "",
            "title": "",
            # "content": "",
            "readNum": 0,
            "playNum": 0,
            "likeNum": 0,
            "commentNum": 0,
            "pubTime": 0,
            "isOriginal": -1,
            "isOriginalCompute": -1,
            "isSource": "",
            "mediaName": "",
            "url": ""
        }

    def _query_get_works_by_title(self, source_detail, target_index_list, start_time, end_time, necessary_words=tuple(),
                                  **kwargs):
        """
        根据query查询，根据结果中_score分数判断相似度高的文章，并将结果集按pubTime降序排序
        :param query:
        :param start_time:
        :param end_time:
        :param page:
        :param per:
        :param kwargs:
        :return:
        """
        del kwargs
        # 组合筛选条件
        must_list = list()
        must_list.append({"term": {"status": 1}})
        must_list.append({"match": {"title": source_detail["title"]}})
        if start_time and end_time:
            must_list.append({"range": {"pubTime": {"gte": start_time, "lte": end_time}}})
        else:
            raise AssertionError("Error param, startTime and endTime is needed.")
        sort_clause = {"_score": {"order": "desc"}}    # "_score": "desc"
        query_body = {
            "_source": list(self._source_default_dict.keys()),
            "query": {"bool": {"must": must_list}},
            "sort": sort_clause,
        }
        # 查询结果集，获取query本身的score分数，然后乘以0.8，获取在此之间的文章
        res1 = self._es_conn.search(index=target_index_list, doc_type="_doc", body=query_body, request_timeout=3600)
        # 遍历ES聚合后的结果集。
        result_list = list()
        if res1["hits"]["total"] > 0:
            max_score = int(res1["hits"]["max_score"])
            min_score = max_score * self._percent       # 计算最低分值，按0.8计算
            # 设置最下分值
            query_body["min_score"] = min_score
            # 计算除最低分值后再次查询
            res = self._es_conn.search(index=target_index_list, doc_type="_doc", body=query_body, request_timeout=3600)
            # 去重集合，用于对匹配结果进行去重。
            unique_match_set = set()
            hits = res["hits"]["hits"]
            for hit in hits:
                # 如果查询结果分数大于待匹配文章分数，跳过
                if int(hit["_score"]) > max_score:
                    continue
                # 如果查询ID为本身则跳过
                if hit["_id"] == source_detail["_id"]:
                    continue
                item = dict(self._source_default_dict, **hit["_source"])
                item["_id"] = hit["_id"]
                title = item["title"]
                if not title:       # 标题为空的不添加
                    continue
                # 匹配分值。
                item["matchScore"] = int(hit["_score"]) / max_score
                # 去重。
                unique_match_id = md5(item["platformName"] + item["url"].strip())
                if unique_match_id in unique_match_set:
                    continue
                else:
                    unique_match_set.add(unique_match_id)
                result_list.append(item)
        total_end = len(result_list)
        # 按时间降序排序
        result = sorted(result_list, key=lambda x: x["pubTime"], reverse=True)
        return {"total": total_end, "list": result}

    def _query_get_works_by_content(self, source_detail, target_index_list, start_time, end_time):
        # 组合筛选条件
        must_list = list()
        should_list = []
        filter_list = []
        must_list.append({"term": {"status": 1}})
        # 标签
        # if len(label) > 0:
        #     for word in label:
        #         should_list.append({"match": {"label": word}})
        # must_list.append({"bool": {"should": should_list}})
        if start_time and end_time:
            must_list.append({"range": {"pubTime": {"gte": start_time, "lte": end_time}}})
        else:
            raise AssertionError("Error param, startTime and endTime is needed.")
        """统一用match比对"""
        content = source_detail["content"]
        soup = BeautifulSoup(content, "html.parser")
        query = soup.get_text().strip()
        must_list.append({"match": {"content": query}})
        title = source_detail["title"]
        must_list.append({"match": {"title": title}})
        try:
            keywords = source_detail["keywords"]
        except:
            keywords = ""

        try:
            label = source_detail["keywords"]
        except:
            label = ""
        if keywords:
            must_list.append({"match": {"keywords": keywords}})
        if label:
            must_list.append({"match": {"label": label}})
        # 关键词
        # if keywords:
        #     keywords_query = []
        #     for word in keywords:
        #         keywords_query.append({"term": {"keywords.word": word}})
        #     nested_query = {
        #         "nested": {
        #             "path": "keywords",
        #             "query": {"bool": {"should": keywords_query}},
        #             "score_mode": "none"
        #         }}
        #     filter_list.append(nested_query)
        # # 最终请求体。
        sort_clause = {"_score": {"order": "desc"}}
        body = {
            "_source": list(self._source_default_dict.keys()),
            "query": {"bool": {"must": must_list,
                               "filter": filter_list
                               }},
            "sort": sort_clause
        }
        # 去重集合
        unique_match_set = set()
        res1 = self._es_conn.search(index=target_index_list, doc_type="_doc", body=body, request_timeout=3600)
        # 遍历ES聚合后的结果集。
        result_list = list()
        if res1["hits"]["total"] > 0:
            max_score = res1["hits"]["max_score"]
            if max_score > 600:
                body["min_score"] = max_score * self._percent
            else:
                # 对于分值较小的新闻，也加入最小分值限制，其实分值小也意味着文字内容少。
                body["min_score"] = max_score * 0.5
            # 计算除最低分值后再次查询
            res = self._es_conn.search(index=target_index_list, doc_type="_doc", body=body, request_timeout=3600)
            hits = res["hits"]["hits"]
            for hit in hits:
                # 如果查询结果的分数大于待匹配文章分数，跳过。
                if int(hit["_score"]) > max_score:
                    continue
                # # 如果查询ID为自身，则跳过。如果是同索引内的相似内容也保留。
                # if hit["_id"] == source_detail["_id"]:
                #     continue
                item = dict(self._source_default_dict, **hit["_source"])
                item["_id"] = hit["_id"]
                title = item["title"]
                if not title:  # 标题为空的不添加
                    continue
                item["matchScore"] = int(hit["_score"]) / max_score
                # 去重。
                unique_match_id = md5(item["mediaName"] + item["url"].strip())
                if unique_match_id in unique_match_set:
                    continue
                else:
                    unique_match_set.add(unique_match_id)
                result_list.append(item)
        total_end = len(result_list)
        result = sorted(result_list, key=lambda x: x["pubTime"])
        return {"total": total_end, "list": result}

    def api_query_get_works_list(self, request):
        """
        按request中的query参数在es中检索
        :param request:
        :return:
        """
        source_detail = ""
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
            if article_type == 3 and len(images) == 0:
                result = self._query_get_works_by_title(source_detail, self._target_index_list, start_time, end_time)
            else:
                result = self._query_get_works_by_content(source_detail, self._target_index_list, start_time, end_time)
            return dict(code=1, msg="success", data=result)
        except Exception as e:
            self._logger.warning(f"{e}.\n{traceback.format_exc()}")
            return dict(code=0, msg="failed")
        finally:
            """当查询完成之后删除临时索引内的文章"""
            ArticleSaveAndDeleteEs().article_delete_es(source_detail)

    def api_judge_work_original(self, request):
        # 判断原创现根据内容搜索相似，根据时间排序，有无来源字段，若无在内容中查找有无`来源于燕赵都市报`等类似字样，
        self._logger.info("----Path: {}".format(request.get_full_path()))
        self._logger.info(f"请求体是：{str(request.body, encoding='utf8')}")
        source_detail = ""
        try:
            body = json.loads(request.body)
            source_detail = body["source_detail"]
            source_str = check_source_article(source_detail, self._logger)
            is_source = "".join(re.findall(r"[\w\-]+", source_str))
            self._logger.info(f"对是否有转发的处理结果是{is_source}")
            """从是否有来源、转发、专自等确定转发来源，那么基本可以确定原创或转发"""
            if is_source:
                source_detail["isSource"] = is_source
                if is_source == source_detail["nickName"]:
                    source_detail["isOriginalCompute"] = 1
                    return dict(code=1, msg="success", data=source_detail)
            """将文章存入临时索引"""
            ArticleSaveAndDeleteEs().article_save_es(source_detail)
            work_id = source_detail["_id"]
            # soup = BeautifulSoup(item, "html.parser")
            # content = soup.get_text().strip()
            # query = content
            start_time = body["start_time"]
            end_time = body["end_time"]
            # try:
            #     keywords = json.loads(body["keyword"])
            # except Exception:
            #     keywords = []
            # try:
            #     label = json.loads(body["label"])
            # except Exception:
            #     label = []
            """判断文章类型：纯视频稿与其他，纯视频稿应该走标题搜索，因它没再多的信息了"""
            images = source_detail["images"]
            article_type = source_detail["contentType"]
            if article_type == 3 and len(images) == 0:
                result = self._query_get_works_by_title(source_detail, self._target_index_list, start_time, end_time)
            else:
                result = self._query_get_works_by_content(source_detail, self._target_index_list, start_time, end_time)
            print(result["list"][0]["_id"])
            if result["list"][0]["_id"] != work_id:
                source_detail["isOriginalCompute"] = 0
            else:
                source_detail["isOriginalCompute"] = 1
            return dict(code=1, msg="success", data=source_detail)
        except Exception as e:
            self._logger.warning(f"{e}.\n{traceback.format_exc()}")
            return dict(code=0, msg="failed")
        finally:
            """当查询完成之后删除临时索引内的文章"""
            ArticleSaveAndDeleteEs().article_delete_es(source_detail)


# def batch_article_original():
#     query = ""
#     start_time = 1604972970
#     end_time = 1607564884
#     page = 1
#     per = 50
#     result_list = BigDataWorksAnalyze()._query_get_works_list(query, start_time, end_time, page, per)
#     # if result_list["total"] > 0:
#     #     res = sorted(result_list["list"], key=lambda x: x["pubTime"])           # 按发表时间排序，越早认为是原创
#     #     res[0]["isOriginal"] = 1
#     #     print(res[0])


if __name__ == '__main__':
    qu = "【成都#郫都区郫筒街道太平村升为中风险#地区】经成都市郫都区新冠肺炎疫情防控指挥部研究决定：自2020年12月7日21时起，将成都市郫都区郫筒街道太平村的风险等级由低风险调整为中风险。成都市郫都区其他区域风险等级不变。"
    end = 1607564884
    start = 1604972970
    # BigDataWorksAnalyze().query_get_works_list(qu, start, end, 1, 50)
    # batch_article_original()


