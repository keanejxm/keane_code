# -*- coding:utf-8 -*-
"""
从es 中取一条数据 进行nlp接口生成结果， 并将结果保存到当前数据中
# author: albert
# date: 2020/12/23
# update: 2020/12/23
"""
import json

import elasticsearch
import requests


class ESToNLP:

    def __init__(self):
        self.conn = elasticsearch.Elasticsearch([{"host": "180.76.161.67", "port": 9200}])

    def parse_data_and_update(self, need_nlp_works, nlp_res):
        nlp_res_data = nlp_res["data"]

        if len(nlp_res_data["情感分析"]) > 1:
            sentiment = nlp_res_data["情感分析"][-1].get("items")["sentiment"]
            sentimentPositiveProb = nlp_res_data["情感分析"][-1].get("items")["positive_prob"]
        else:
            sentiment = nlp_res_data["情感分析"][0].get("items")["sentiment"]
            sentimentPositiveProb = nlp_res_data["情感分析"][0].get("items")["positive_prob"]

        tags = nlp_res_data["文章标签"]
        hasDiscovery = -1
        if tags:
            hasDiscovery = 1

        personNames = nlp_res_data["全文分词"]["人名"]
        regionNames = nlp_res_data["全文分词"]["地名"]
        organizationNames = nlp_res_data["全文分词"]["组织"]
        keywords = nlp_res_data["全文分词"]["关键词"]
        segmentWordsRawInfo = nlp_res_data["全文分词"]["raw_data"]

        digestCompute = nlp_res_data["文章摘要"]["summary"]

        wordFrequency = nlp_res_data["计算词频"]

        doc = {
            # 情感分析
            "sentiment": sentiment,
            "sentimentPositiveProb": sentimentPositiveProb,
            "sentimentRawInfo": json.dumps(nlp_res_data["情感分析"], ensure_ascii=False),

            # 文章标签
            "tags": tags,
            "tagsLength": len(tags),
            "hasDiscovery": hasDiscovery,

            # 全文分词
            "personNames": personNames,
            "regionNames": regionNames,
            "organizationNames": organizationNames,
            "keywords": keywords,
            "segmentWordsRawInfo": json.dumps(segmentWordsRawInfo, ensure_ascii=False),

            # 摘要
            "digestCompute": digestCompute,

            # 词频
            "wordFrequency": wordFrequency,
            "wordFrequencyLength": len(wordFrequency),

        }
        field_id = need_nlp_works["_id"]
        fields = dict(doc=doc)
        res = self.conn.update(index="dc_works", doc_type="_doc", id=field_id, body=fields)
        return res

    def get_nlp_data(self, need_nlp_works):
        url = 'http://180.76.96.208:16266/dc/nlp_test/nlp/'
        data = {
            "title": need_nlp_works["title"],
            "content": need_nlp_works["content"],
        }
        response = requests.post(url=url, data=data)
        return response.json()

    def get_article_from_es(self, page, per):
        source_list = ["title", "content"]
        # sort子句。
        sort_clause = {"pubTime": {"order": "asc"}}
        query_body = {
            "from": (page - 1) * per,
            "size": per,
            "_source": source_list,
            "query": {
                "match_all": {}
              },
            "sort": sort_clause,
        }
        response = self.conn.search(
            index="dc_works",
            doc_type="_doc",
            body=query_body,
        )
        works = []
        for res_data in response["hits"]["hits"]:
            res_data_dict = res_data["_source"]
            res_data_dict["_id"] = res_data["_id"]
            works.append(res_data_dict)
        return works

    def run(self, works=None):
        per = 10
        if not works:
            res_list = []
            for i in range(1, 10):
                # 获取一条数据 从es 中
                es_works = self.get_article_from_es(page=i, per=per)
                need_nlp_works = es_works[0]
                # 获取nlp的结果
                nlp_res = self.get_nlp_data(need_nlp_works)
                # 将结果合并 更新数据
                res = self.parse_data_and_update(need_nlp_works, nlp_res)
                res_list.append(res)
            return res_list
        need_nlp_works = works
        # 获取nlp的结果
        nlp_res = self.get_nlp_data(need_nlp_works)
        # 将结果合并 更新数据
        res = self.parse_data_and_update(need_nlp_works, nlp_res)
        return [res]


if __name__ == '__main__':
    res = ESToNLP().run()

