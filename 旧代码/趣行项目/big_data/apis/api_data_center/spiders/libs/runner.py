# -*- coding:utf-8 -*-
"""
爬虫执行器。
# author: Albert, Trico
# date: 2021/1/4
# update: 2021/1/4
"""

from spiders.libs.spiders.weixin.wechat_publish_account import WeChatAccountSpider
from spiders.libs.spiders.weibo.xinyuan_weibo import XinYuanWb
from spiders.libs.spiders.website.new_web_spider import WebSpider
from spiders.libs.spiders.app.app_fetch import AppFetch
from spiders.libs.spiders.epaper.newspaper_spider import NewspaperSpider
from spiders.libs.spiders.forum.forum_run import ForumRun
from spiders.libs.spiders.we_media.we_media_run import WeMediaRun
from spiders.libs.spiders.hot_search.search_hot import HotSearch
from spiders.libs.spiders.app.push_news import PushNews


class SpiderRunner(object):

    def __init__(self, logger, fetch_method="yield"):
        """
        采集微信。
        :param logger: 任务数据。
        :param fetch_method: 提取数据的方式，batch：批采集，yield：流采集。
        :return: dict(code=0/1, msg="...", data=dict(...))
        """

        # 日志对象。
        self._logger = logger

        # 采集方式，批采集或是流采集。
        self._fetch_method = fetch_method

    def fetch_wechat(self, task):
        """
        采集微信。
        :param task: 任务数据。
        :return: dict(code=0/1, msg="...", data=dict(...))
        """

        if self._fetch_method == "batch":
            return WeChatAccountSpider(logger=self._logger).fetch_batch(task)
        elif self._fetch_method == "yield":
            return WeChatAccountSpider(logger=self._logger).fetch_yield(task)
        else:
            raise ValueError(f"未知采集方法：{self._fetch_method}")

    def fetch_weibo(self, task):
        """
        采集微博。
        :param task: 任务数据。
        :return: dict(code=0/1, msg="...", data=dict(...))
        """

        if self._fetch_method == "batch":
            uid = task.get("platformAccountID")
            assert uid and isinstance(uid, str), f"参数错误，platformAccountID：{uid}"
            return XinYuanWb(uid=uid, logger=self._logger).fetch_batch()
        elif self._fetch_method == "yield":
            uid = task.get("platformAccountID")
            assert uid and isinstance(uid, str), f"参数错误，platformAccountID：{uid}"
            return XinYuanWb(uid=uid, logger=self._logger).fetch_yield()
        else:
            raise ValueError(f"未知采集方法：{self._fetch_method}")

    def fetch_website(self, task):
        """
        采集网站。
        :param task: 任务数据。
        :return: dict(code=0/1, msg="...", data=dict(...))
        """

        if self._fetch_method == "batch":
            template = task.get("template")
            return WebSpider(paper_template=template, logger=self._logger).fetch_batch()
        elif self._fetch_method == "yield":
            template = task.get("template")
            return WebSpider(paper_template=template, logger=self._logger).fetch_yield()
        else:
            raise ValueError(f"未知采集方法：{self._fetch_method}")

    def fetch_app(self, task):
        """
        采集客户端。
        :param task: 任务数据。
        :return: dict(code=0/1, msg="...", data=dict(...))
        """

        if self._fetch_method == "batch":
            return AppFetch().fetch_batch(task, logger=self._logger)
        elif self._fetch_method == "yield":
            return AppFetch().fetch_yield(task, logger=self._logger)
        else:
            raise ValueError(f"未知采集方法：{self._fetch_method}")

    def fetch_epaper(self, task):
        """
        采集电子报。
        :param task: 任务数据。
        :return: dict(code=0/1, msg="...", data=dict(...))
        """

        if self._fetch_method == "batch":
            template = task.get("template")
            target_dates = task.get("targetDates")
            return NewspaperSpider(
                paper_template=template, target_dates=target_dates, logger=self._logger
            ).fetch_batch()
        elif self._fetch_method == "yield":
            template = task.get("template")
            target_dates = task.get("targetDates")
            return NewspaperSpider(
                paper_template=template, target_dates=target_dates, logger=self._logger
            ).fetch_yield()
        else:
            raise ValueError(f"未知采集方法：{self._fetch_method}")

    def fetch_forum(self, task):
        """
        采集论坛。
        :param task: 任务数据。
        :return: dict(code=0/1, msg="...", data=dict(...))
        """

        if self._fetch_method == "batch":
            return ForumRun(logger=self._logger).fetch_batch(task)
        elif self._fetch_method == "yield":
            return ForumRun(logger=self._logger).fetch_yield(task)
        else:
            raise ValueError(f"未知采集方法：{self._fetch_method}")

    def fetch_we_media(self, task):
        """
        采集自媒体。
        :param task: 任务数据。
        :return: dict(code=0/1, msg="...", data=dict(...))
        """

        if self._fetch_method == "batch":
            return WeMediaRun(logger=self._logger).fetch_batch(task)
        elif self._fetch_method == "yield":
            return WeMediaRun(logger=self._logger).fetch_yield(task)
        else:
            raise ValueError(f"未知采集方法：{self._fetch_method}")

    def fetch_top_query(self, _):
        """
        采集热搜数据。
        :return: dict(code=0/1, msg="...", data=dict(...))
        """

        if self._fetch_method == "batch":
            return HotSearch(self._logger).hot_batch()
        elif self._fetch_method == "yield":
            return HotSearch(self._logger).hot_yield()
        else:
            raise ValueError(f"未知采集方法：{self._fetch_method}")

    def fetch_push(self, task):
        """
        采集推送数据（客户端）。
        :return: dict(code=0/1, msg="...", data=dict(...))
        """

        if self._fetch_method == "batch":
            raise ValueError(f"采集推送数据，暂无batch分支")
        elif self._fetch_method == "yield":
            platform_name = task.get("platformName")
            platform_id = task.get("platformID")
            return PushNews(appname=platform_name, logger=self._logger, platform_id=platform_id).push_news_yield()
        else:
            raise ValueError(f"未知采集方法：{self._fetch_method}")
