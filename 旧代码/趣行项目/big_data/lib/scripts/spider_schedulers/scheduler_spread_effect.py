# -*- coding: utf-8 -*-#
"""
# 准备传播路径调度器
# author: Chris
# date: 2021/1/25
# update: 2021/1/25
"""

import time
import requests
import json
import traceback
import elasticsearch
from lib_conf.config import es_config
from lib_conf.config import api_host
from common_utils.es.scroll_search_es import scroll_search_es


class SchedulerSpreadEffect:

    def __init__(self, logger):
        self._target_works = "dc_works"
        self._es_conn = elasticsearch.Elasticsearch(**es_config)
        self._api_url = f"{api_host}/dc/batch_compute/distance_similar_works/"
        # 超时时间。
        self.timeout = 1 * 60 * 60
        self._logger = logger

    def search_work_id(self):
        must_list = list()
        should_list = list()
        end_time = int(time.time() * 1000)  # 当前时间戳
        start_time = end_time - (3 * 24 * 60 * 60 * 1000)  # 以当前时间戳为基础向前三天
        must_list.append({"term": {"status": 1}})
        # 目前产品要求是河北日报相关产品计算传播路径
        # must_list.append({"term": {"accountName": "河北日报"}})
        should_list.append({"match": {"accountName": "河北日报"}})
        should_list.append({"match": {"platformName": "河北日报"}})
        must_list.append({"bool": {"should": should_list}})
        must_list.append({"range": {"pubTime": {"gte": start_time, "lte": end_time}}})
        query_body = {
            "query": {"bool": {"must": must_list,
                               "must_not": {"term": {"simhash": ""}}
                               }
                      },
            "sort": [{"pubTime": {"order": "desc"}}]
        }
        for i, hits in enumerate(
                scroll_search_es(self._es_conn, self._target_works, query_body, limit=1 * 10 ** 7), start=1):
            try:
                post_body = dict()
                post_body["source_detail"] = hits
                post_body["end_time"] = int(time.time() * 1000)
                post_body["start_time"] = post_body["end_time"] - (7 * 24 * 60 * 60 * 1000)
                self._logger.info(f"{post_body}")
                # self._api_url = "http://127.0.0.1:16301/dc/batch_compute/distance_similar_works/"
                resp = requests.post(self._api_url, json=post_body, timeout=self.timeout)
                if resp.status_code == requests.codes.ok:
                    resp_data = json.loads(resp.content)
                    self._logger.info(f"{resp.status_code}，{json.dumps(resp_data, ensure_ascii=False)}")
                else:
                    raise requests.HTTPError(f"{resp.status_code}")
                time.sleep(10)
            except Exception as e:
                self._logger.warning(f"{e}\n{traceback.format_exc()}")


if __name__ == '__main__':
    from common_utils.llog import LLog
    log_ger = LLog("run_scheduler_spread", only_console=True).logger
    SchedulerSpreadEffect(log_ger).search_work_id()



