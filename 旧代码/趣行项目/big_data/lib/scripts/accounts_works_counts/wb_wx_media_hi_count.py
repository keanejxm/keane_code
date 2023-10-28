# -*- coding: utf-8 -*-#
"""
# 微博微信自媒体单个账户的HI数据统计
# author: Chris
# date: 2021/1/23
# update: 2021/1/23
"""

import sys
import time
import datetime
import elasticsearch

from dateutil import tz
from common_utils.utils import md5
from lib_conf.config import es_config
from common_utils.es.scroll_search_es import scroll_search_es


class WbWxMediaHiCount:

    def __init__(self):
        # 连接es
        self._es_conn = elasticsearch.Elasticsearch(**es_config)
        # 查询目标索引
        self._target_works = "dc_works"
        # 存储索引
        self._target_samples = "dc_works_samples"

    @staticmethod
    def get_point_timestamp(millisecond_timestamp, period):
        """
        获取整点时间戳，整天、整小时或整分钟。
        :param millisecond_timestamp: 毫秒时间戳。
        :param period: 归整周期，1每天，2每小时，3每分钟。
        :return:
        """

        # 参数验证。
        assert isinstance(millisecond_timestamp, int) and millisecond_timestamp > 0, \
            f"Error param, millisecond_timestamp: {millisecond_timestamp}."
        assert isinstance(period, int), f"Error param, period: {period}."

        # 根据不同的周期分别计算。
        local_tz = tz.gettz("Asia/Shanghai")
        date_obj = datetime.datetime.fromtimestamp(millisecond_timestamp / 1000, tz=local_tz)
        if period == 1:
            # 当天零点时间戳。
            timestamp = date_obj.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
        elif period == 2:
            # 当天整小时时间戳。
            timestamp = date_obj.replace(minute=0, second=0, microsecond=0).timestamp()
        elif period == 3:
            # 当前整小时整分钟时间戳。
            timestamp = date_obj.replace(second=0, microsecond=0).timestamp()
        else:
            raise AssertionError(f"Error param, period: {period}.")
        return timestamp

    def search_work_id(self):
        source_list = ["_id"]
        end_time = int(time.time() * 1000)  # 当前时间戳
        start_time = end_time - (3 * 24 * 60 * 60 * 1000)  # 以当前时间戳为基础向前三天
        must_list = list()
        must_list.append({"term": {"status": 1}})
        # must_list.append({"range": {"updateTime": {"gte": 1609430400000}}})
        must_list.append({"range": {"pubTime": {"gte": start_time, "lte": end_time}}})
        query_body = {
            "_source": source_list,
            "query": {"bool": {"must": must_list}},
        }
        for i, hits in enumerate(
                scroll_search_es(self._es_conn, self._target_works, query_body, limit=1 * 10 ** 7), start=1):
            work_id = hits["_id"]
            yield work_id

    def save_item_sample(self, work_id, period):
        must_list = list()
        must_list.append({"term": {"_id": work_id}})
        works_query_body = {
            "_source": ["spreadHI", "interactiveHI"],
            "query": {"bool": {"must": must_list}},
        }
        res = self._es_conn.search(
            index=self._target_works, doc_type="_doc", body=works_query_body, request_timeout=3600)
        spread_hi = res["hits"]["hits"][0]["_source"]["spreadHI"]
        interactive_hi = res["hits"]["hits"][0]["_source"]["interactiveHI"]
        now = int(time.time() * 1000)  # 当前时间戳
        # 以当前时间戳转换时间，传参是当前时间戳和搜索模式：1每天，2每小时，3每分钟
        point_time = self.get_point_timestamp(now, period)
        point_time = int(point_time * 1000)
        # 存储时的默认数据
        sample_dict = dict(
            status=1,
            worksID=work_id,
            spreadHI=spread_hi,
            interactiveHI=interactive_hi,
            period=period,
            pointTime=point_time,
            createTime=now,
            updateTime=now,
        )
        field_id = md5(f"{work_id}{period}{point_time}")
        fields = sample_dict
        res = self._es_conn.index(index=self._target_samples, doc_type="_doc", id=field_id, body=fields)
        print(res["_id"] + "----" + res["result"])

    def sample(self, period=1):
        for i, work_id in enumerate(self.search_work_id(), start=1):
            self.save_item_sample(work_id, period)

    def run(self):
        # 执行入口。

        # 获取命令行参数。
        args = sys.argv
        if len(args) <= 1:
            # 执行默认采样，测试一条。
            self.sample()
        else:
            choice = str(args[1]).strip()
            if choice == "perDay":
                self.sample(period=1)
            elif choice == "perHour":
                self.sample(period=2)
            elif choice == "perMinute":
                self.sample(period=3)
            else:
                raise ValueError(f"Unknown args: {choice}, it should be: ['perDay', 'perHour', 'perMinute'].")


if __name__ == '__main__':
    WbWxMediaHiCount().run()
