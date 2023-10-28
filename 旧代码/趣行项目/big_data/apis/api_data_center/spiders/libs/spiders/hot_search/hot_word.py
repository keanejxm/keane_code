#!/usr/bin/env python3
# -*- coding:utf-8
# Author Keane
# coding=utf-8
# @Time    : 2021/1/14 10:53
# @File    : hot_word.py
# @Software: PyCharm
import time
import elasticsearch
from spiders.libs.spiders.hot_search.hot_data_create_es import WashData
from api_common_utils.llog import LLog
from api.config import es_config
class HotWord(object):
    def __init__(self):
        self._es_conn = elasticsearch.Elasticsearch(**es_config)
        self.logger = LLog("hotwords", only_console = True, logger_level = "INFO").logger
    def search_keywords(self):
        """
        从dc_works获取关键词数据
        """
        now_ms = int(time.time() * 1000)
        must_list = [
            {"range": {"pubTime": {
                "gte": now_ms - 24 * 60 * 60 * 1000,
                # "gte": int(time.time()*1000),
                "lte": now_ms
            }}}]
        body = {
            "_source": ["keywords"],
            "query": {
                "bool": {"must": must_list},
                # "match_all":{}
                      },
        }
        res1 = self._es_conn.search(index="dc_works", request_timeout=3600, body=body)
        return res1
    def word_fre(self):
        keywords_list = self.search_keywords()
        keywords_list = keywords_list["hits"]["hits"]
        words_list = list()
        for keywords in keywords_list:
            words_list.extend(keywords["_source"]["keywords"])
        words_dict = {x: words_list.count(x) for x in set(words_list)}
        words_list = sorted(words_dict.items(), key=lambda item: item[1], reverse=True)
        words_list =  words_list[0:30]
        words = list()
        for word in words_list:
            a = dict()
            a[word[0]] = word[1]
            words.append(a)
        if words:
            res = WashData().wash_hot_search_data(words,"4")
            yield res
        else:
            self.logger.debug("数据为空")
if __name__ == '__main__':
    hot_word = HotWord()
    print()
    res = hot_word.word_fre()
    print(res)