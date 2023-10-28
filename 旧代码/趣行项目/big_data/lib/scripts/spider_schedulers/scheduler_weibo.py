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
import time
import random

from lib_conf.config import log_path
from common_utils.es.scroll_search_es import scroll_search_es
from scripts.spider_schedulers.scheduler import SpiderScheduler


class SpiderSchedulerWeiBo(SpiderScheduler):
    """
    调度器。
    """

    def __init__(self, logger):
        super(SpiderSchedulerWeiBo, self).__init__(logger=logger)
        self._api_params["spider_type"] = "weibo"

    def perform(self):
        """
        执行。
        :return:
        """

        # 索引名。
        index_name = "dc_accounts"
        query_body = {
            "_source": ["name", "platformAccountID", ],
            "query": {"bool": {"must": [
                # {"terms": {"name": ["河北日报"]}},
                # {"terms": {"name": [
                #     "光明日报", "新华每日电讯", "重庆日报",
                #     "北京日报", "辽宁日报", "昆明日报", "新华日报", "人民网", "中国银行", "财经时报",
                #     "紫光阁", "新华视点", "环球人物杂志", "人民画报", "天津网", "山西广播电视台",
                #     "头条文章", "腾讯视频", "网易汽车", "和讯网", "千龙网中国首都网", "健身专辑",
                #     "新浪汽车", "南宁日报", "廊坊晚报", "舟山网官方微博",
                #     "石家庄广播电视台", "秦皇岛晚报", "邯郸新闻网", "余杭晨报",
                #     "甘肃日报", "海南日报", "河北新闻网", "燕赵都市报",
                #     "宁夏日报", "四川日报", "广西日报", "解放日报", "湖南日报", "吉林日报", "河北日报", "马研网", "福建日报",
                #     "党史网", "中国教育在线", "经济参考报", "人民日报", "中国新闻周刊", "央视新闻", "文旅中国", "中国新闻网",
                #     "看电影", "微博明星", "腾讯自选股", "网路冷眼",
                #     "微博贵州", "中国长安网", "唐山消防", "邢台检察", "石家庄消防", "唐山检察",
                #     "太原户政", "晋中气象", "安徽共青团", "成都机关工委", "梨视频", "简阳总工会", "成化工商联", "成都校园",
                #     "温江工会", "成都科协", "温江妇联", "胡杨文化", "中国妇女出版社", "海尔兄弟", "开心麻花",
                #     "光线传媒", "迪士尼电影", "博纳影业集团"
                # ]}},
                {"term": {"platformType": 2}},
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
                    time.sleep(random.uniform(1, 2))
                    post_body = hits
                    self._logger.info(f"{self._api_params}，{post_body}")
                    # self._api_url = "http://127.0.0.1:16301/dc/spiders/run/"
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
    # logger = LLog("run_scheduler", only_console=True).logger
    logger = LLog("run_scheduler_weibo", log_path=log_path, logger_level="DEBUG").logger
    SpiderSchedulerWeiBo(logger).perform()


if __name__ == "__main__":
    run_scheduler()
