import json
import traceback
import elasticsearch
from django.views import View
from django.http import JsonResponse
from flow_compute.lib.baidu_api.nlp import Nlp
from api_common_utils.llog import LLog
from api.config import es_config, api_log_path

logger = LLog(logger_name="outside", log_path=api_log_path, logger_level="DEBUG").logger


class GeteMotionalData(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            logger.debug(f'对外情感分析接口接到的请求参数：{data}')
            es_id = data["_id"]
            es_conn = elasticsearch.Elasticsearch(**es_config)
            index_name = 'dc_works'
            if es_conn.exists(index=index_name, doc_type="_doc", id=es_id):
                query_body = {
                  "_source": ["sentiment", "title", "content", "sentimentPositiveProb"],
                  "query": {
                    "term": {
                      "_id": es_id
                    }
                  }
                }
                response = es_conn.search(
                    index="dc_works",
                    doc_type="_doc",
                    body=query_body,
                )
                works_list = []
                for res_data in response["hits"]["hits"]:
                    res_data_dict = res_data["_source"]
                    res_data_dict["_id"] = res_data["_id"]
                    works_list.append(res_data_dict)
                work_data = works_list[0]
                # 判断有无情感分析的数据
                if work_data["sentiment"] == -1:
                    # 请求ai的接口
                    data = {"content": work_data["content"]}
                    res = Nlp(logger).judge_article_positive_negative(data)
                    if not res["data"]:
                        res = {"code": 1, "msg": "作品无文字 无法进行情感分析"}
                        return JsonResponse(res)
                    if len(res["data"]) > 1:
                        sentiment = res["data"][-1].get("items")[0]["sentiment"]
                        sentimentPositiveProb = res["data"][-1].get("items")[0]["positive_prob"]
                    else:
                        sentiment = res["data"][0].get("items")[0]["sentiment"]
                        sentimentPositiveProb = res["data"][0].get("items")[0]["positive_prob"]
                    # 更新es中的数据
                    update_body = {
                        "doc": {
                            "sentiment": sentiment,
                            "sentimentPositiveProb": sentimentPositiveProb,
                        }}
                    res = es_conn.update(
                        index=index_name,
                        doc_type="_doc",
                        id=es_id,
                        body=update_body
                    )
                    logger.debug(f'更新es的返回值:{res}')
                    res = {
                        "code": 1,
                        "msg": "success",
                        "data": {
                            "sentiment": sentiment,
                            "sentimentPositiveProb": sentimentPositiveProb,
                        }}
                else:
                    res = {
                        "code": 1,
                        "msg": "success",
                        "data": {
                            "sentiment": work_data["sentiment"],
                            "sentimentPositiveProb": work_data["sentimentPositiveProb"],
                        }}
            else:
                res = {"code": 1, "msg": "作品不存在"}
            logger.debug(f'返回的结果为：{res}')
            return JsonResponse(res)
        except Exception as e:
            logger.warning(f'{e}\n{traceback.format_exc()}')
            return JsonResponse({"code": 0, "msg": "未知错误"})
