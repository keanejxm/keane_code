# -*- coding: utf-8 -*-#
"""
# 微博微信自媒体单个账户的作品数统计
# author: Chris
# date: 2021/1/13
# update: 2021/1/13
"""


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
        # 将来如果所有账户都入户之后可以去掉一下条件
        must_list.append({"range": {"updateTime": {"gte": 1609430400000}}})
        query_body = {
            "_source": source_list,
            "query": {"bool": {"must": must_list}},
        }
        # res = self._es_conn.search(index=self._target_account, doc_type="_doc", body=query_body, request_timeout=3600)
        # for item in res["hits"]["hits"]:
        #     yield item["_id"]
        # # 分页查询
        # res = self._es_conn.search(index=self._target_account, doc_type="_doc", body=query_body,
        #                            scroll='5m', size=self._page_num, request_timeout=3600)
        # # 将查询结果第一页返回
        # yield res["hits"]["hits"]
        # # 游标用于输出查询结果
        # scroll_id = res['_scroll_id']
        # # 按照每页返回数计算有多少页
        # pages = math.floor(res["hits"]["total"]/self._page_num)
        # for page in range(0, pages):
        #     res_scroll = self._es_conn.scroll(scroll_id=scroll_id, scroll='5m')
        #     yield res_scroll["hits"]["hits"]
        for i, hits in enumerate(
                scroll_search_es(self._es_conn, self._target_account, query_body, limit=1 * 10 ** 7), start=1):
            yield hits

    def update_account_works_num(self, account_id, total_count):
        fields = dict(doc={"worksNum": total_count})
        res = self._es_conn.update(index=self._target_account, doc_type="_doc", id=account_id, body=fields)
        # print(res["_id"] + "---" + res["result"])

    def account_count(self, account_id):
        must_list = list()
        must_list.append({"term": {"status": 1}})
        must_list.append({"term": {"accountID": account_id}})
        query_body = {"query": {"bool": {"must": must_list}}}
        result = self._es_conn.search(index=self._target_works, doc_type="_doc", body=query_body)
        total_count = result["hits"]["total"]
        return total_count

    def run(self):
        rest = self.search_accounts_id()
        for item in rest:
            total_count = self.account_count(item["_id"])
            self.update_account_works_num(item["_id"], total_count)


if __name__ == '__main__':
    WbWxMediaWorksCount().run()





