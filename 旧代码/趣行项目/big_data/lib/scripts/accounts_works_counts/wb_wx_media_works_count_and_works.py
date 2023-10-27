# -*- coding: utf-8 -*-#
"""
# 微博微信自媒体单个账户的作品数统计
# author: Chris
# date: 2021/1/13
# update: 2021/1/13
"""
import json

import elasticsearch

from lib_conf.config import es_config
from common_utils.es.scroll_search_es import scroll_search_es


class WbWxMediaWorksCount:

    def __init__(self):
        # 连接es
        self._es_conn = elasticsearch.Elasticsearch(**es_config)
        # 查询目标索引
        self._target_account = "dc_accounts"
        # 统计索引
        self._target_works = "dc_works"

    def search_accounts_id(self):
        source_list = []
        must_list = list()
        must_list.append({"term": {"status": 1}})
        # 1-微信，2-微博，7-自媒体
        must_list.append({"terms": {"platformType": [1, 2, 7]}})
        query_body = {
            "_source": source_list,
            "query": {"bool": {"must": must_list}},
        }
        for i, hits in enumerate(
                scroll_search_es(self._es_conn, self._target_account, query_body, limit=1 * 10 ** 7), start=1):
            yield hits

    def update_account_works_num(self, account_id, total_count, data):
        fields = dict(doc={"worksNum": total_count, "extendData": data})
        res = self._es_conn.update(index=self._target_account, doc_type="_doc", id=account_id, body=fields)
        # print(res["_id"] + "---" + res["result"])

    def account_count(self, account_id):
        must_list = list()
        must_list.append({"term": {"status": 1}})
        must_list.append({"term": {"accountID": account_id}})
        sort_clause = {"pubTime": {"order": "desc"}}
        query_body = {
            "size": 1,
            "query": {"bool": {"must": must_list}},
            "sort": sort_clause,
        }
        result = self._es_conn.search(index=self._target_works, doc_type="_doc", body=query_body)
        total_count = result["hits"]["total"]
        data = ""
        if result["hits"]["hits"]:
            title = result["hits"]["hits"][0]["_source"]["title"]
            pubTime = result["hits"]["hits"][0]["_source"]["pubTime"]
            data = {"title": title, "pubTime": pubTime}
            data = json.dumps(data, ensure_ascii=False, separators=(", ", ":"))
        return total_count, data

    def run(self):
        rest = self.search_accounts_id()
        for item in rest:
            total_count, data = self.account_count(item["_id"])
            self.update_account_works_num(item["_id"], total_count, data)


if __name__ == '__main__':
    WbWxMediaWorksCount().run()





