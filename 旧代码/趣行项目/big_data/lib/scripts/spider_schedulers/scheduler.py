# -*- coding:utf-8 -*-
"""
爬虫调度器。
# author: Trico
# date: 2021/1/13
# update: 2021/1/13
"""

import logging
import elasticsearch

from lib_conf.config import api_host, es_config


class SpiderScheduler(object):
    """
    Kafka生产者类。
    """

    def __init__(self, logger, fetch_method="yield", target="kafka"):
        # 日志对象。
        assert isinstance(logger, logging.Logger), "Error param, logger."
        self._logger = logger
        # 连接ES。
        self._es_conn = elasticsearch.Elasticsearch(**es_config)
        # 接口。
        self._api_url = f"{api_host}/dc/spiders/run/"
        # 接口参数。
        self._api_params = dict(result_target=target, fetch_method=fetch_method)
        # 超时时间。
        self.timeout = 1 * 60 * 60

    def perform(self):
        """执行。"""

        ...
