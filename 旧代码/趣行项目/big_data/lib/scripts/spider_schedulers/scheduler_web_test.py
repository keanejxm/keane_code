# -*- coding:utf-8 -*-
"""
爬虫调度器。
# author: Trico
# date: 2021/1/13
# update: 2021/1/13
"""

import json
import datetime
import requests
import traceback

from common_utils.es.scroll_search_es import scroll_search_es
from scripts.spider_schedulers.scheduler import SpiderScheduler


class SpiderSchedulerEPaper(SpiderScheduler):
    """
    调度器。
    """

    def __init__(self, logger):
        super(SpiderSchedulerEPaper, self).__init__(logger=logger)
        self._api_params["spider_type"] = "website"
        self._api_url =  "http://127.0.0.1:18888/dc/spiders/run/"

    def perform(self):
        """
        执行。
        :return:
        """
        # 索引名。
        index_name = "dc_source_spider_templates"
        query_body = {
            "query": {"bool": {"must": [
                {"term": {"platformName": "中国新闻网"}},
            ]}}
        }

        self._logger.info(f"开始执行爬虫，{index_name}，{query_body}")
        # 执行更新。
        try:
            for i, hits in enumerate(
                    scroll_search_es(self._es_conn, index_name, query_body, limit=1 * 10 ** 7, scroll="1h"),
                    start=1
            ):
                # noinspection PyBroadException
                try:
                    post_body = dict(
                        template=hits,
                    )
                    self._logger.info(f"{self._api_params}，{post_body}")
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
    SpiderSchedulerEPaper(logger).perform()


if __name__ == "__main__":
    run_scheduler()
