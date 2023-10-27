# -*- coding:utf-8 -*-
"""
爬虫调度器。
# author: Trico
# date: 2021/1/13
# update: 2021/1/13
"""

import json
import requests
import traceback

from common_utils.es.scroll_search_es import scroll_search_es
from scripts.spider_schedulers.scheduler import SpiderScheduler


class SpiderSchedulerWeChat(SpiderScheduler):
    """
    微信调度器。
    """

    def __init__(self, logger):
        super(SpiderSchedulerWeChat, self).__init__(logger=logger)
        self._api_params["spider_type"] = "wechat"

    def perform(self):
        """
        执行。
        :return:
        """

        # 索引名。
        index_name = "dc_accounts"
        # query_body = {
        #     "query": {"bool": {"must": [
        #         {"term": {"_id": "7ac280d502eb92380ecedabe6f8defb4"}},
        #     ]}}
        # }
        query_body = {
          "query": {
            "bool": {
              "must": [
                {"terms": {"name": [
                  "河北日报", "北京日报", "人民日报", "新华日报", "新京报", "央视新闻", "参考消息", "中国日报", "新华社", "央视网"
                  ]
                }},
                {"term": {
                  "platformID": {
                    "value": "c874d6f5e772452053b508a6b99dc975"
                  }
                }
                }
              ]
            }
          }
        }

        self._logger.info(f"开始执行爬虫，{index_name}，{query_body}")
        # 执行更新。
        try:
            for i, hits in enumerate(scroll_search_es(self._es_conn, index_name, query_body, limit=1 * 10 ** 7, scroll="1h"), 1):
                # noinspection PyBroadException
                try:
                    post_body = hits
                    resp = requests.post(self._api_url, params=self._api_params, json=post_body, timeout=self.timeout)
                    if resp.status_code == requests.codes.ok:
                        resp_data = json.loads(resp.content)
                        self._logger.info(f"{resp.status_code}，{json.dumps(resp_data, ensure_ascii=False)}")
                    else:
                        raise requests.HTTPError(f"{resp.status_code}，{self._api_params}")
                except Exception as e:
                    self._logger.warning(f"{e}\n{traceback.format_exc()}")
        except Exception as e:
            self._logger.warning(f"{e}\n{traceback.format_exc()}")


def run_scheduler():
    # 执行。

    from common_utils.llog import LLog
    logger = LLog("run_scheduler", only_console=True).logger
    SpiderSchedulerWeChat(logger).perform()


if __name__ == "__main__":
    run_scheduler()
