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

from scripts.spider_schedulers.scheduler import SpiderScheduler


class SpiderSchedulerHotSearch(SpiderScheduler):
    """
    调度器。
    """

    def __init__(self, logger):
        super(SpiderSchedulerHotSearch, self).__init__(logger=logger)
        self._api_params["spider_type"] = "top_query"

    def perform(self):
        """
        执行。
        :return:
        """

        # 索引名。

        self._logger.info(f"开始执行爬虫，'热门'")
        # 执行更新。
        try:
            try:
                self._logger.info(f"{self._api_params}")
                resp = requests.post(self._api_url, params=self._api_params, timeout=self.timeout)
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
    SpiderSchedulerHotSearch(logger).perform()


if __name__ == "__main__":
    run_scheduler()
