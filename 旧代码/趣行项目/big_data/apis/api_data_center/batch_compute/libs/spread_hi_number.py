# -*- coding: utf-8 -*-#
# Date:         2021/1/21

import math
import time
import datetime

import elasticsearch
from api.config import es_config


class ComputeSpreadHi:

    def __init__(self):
        self._target_index = "dc_spread_route"
        self._es_conn = elasticsearch.Elasticsearch(**es_config)

    def compute_pubtime_score(self, pub_time, target_list):
        """
        基于发布时间计算传播分值。
        :param pub_time: 源数据发布时间。
        :param target_list: 发布时间列表。
        :return:
        """

        if len(target_list) == 0:
            return 0
        time_dict = {}
        pub_date = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(pub_time/1000)), "%Y-%m-%d")
        for one in target_list:
            if int(one) < int(pub_time):
                continue
            one_date = time.localtime(one/1000)
            time_str = time.strftime("%Y-%m-%d", one_date)
            if time_str in time_dict:
                time_dict[time_str] += 1
            else:
                time_dict[time_str] = 1
        if not time_dict:
            return 0

        time_dict_sorted = sorted(time_dict.items(), key=lambda x: x[0], reverse=True)
        long_pub_date = datetime.datetime.strptime(time_dict_sorted[0][0], "%Y-%m-%d")
        sorted_list = sorted(time_dict.items(), key=lambda x: x[1], reverse=True)
        max_num = sorted_list[0][1]
        time_list = []
        for i in sorted_list:
            if i[1] == max_num:
                time_list.append(i)
        time_list = sorted(time_list, key=lambda x: x[0], reverse=False)
        max_publish_date = datetime.datetime.strptime(time_list[0][0], "%Y-%m-%d")
        ferment_days = (max_publish_date - pub_date).days
        all_days = (long_pub_date - pub_date).days
        time_score = math.log((max_num / (ferment_days + 1)) + all_days + 1)
        return time_score

    def search_es_data(self, source_detail):
        must_list = list()
        result = list()
        must_list.append({"term": {"sourceId": source_detail["_id"]}})
        must_list.append({"term": {"parentId": source_detail["_id"]}})
        body = {
            "size": 9999,
            # "_source": ["similarPlatformName", "similarAccountName", "similarSource", "similarPlatformName"],
            "query": {"bool": {"must": must_list}},
        }
        res = self._es_conn.search(index=self._target_index, request_timeout=3600, body=body)
        if res["hits"]["total"] > 0:
            for item in res["hits"]["hits"]:
                work = item["_source"]
                work["_id"] = item["_id"]
                result.append(work)
        return result

    def compute_data_from_es(self, result):
        # 6--论坛不在其中
        # result = self.search_es_data(source_detail)
        count_dict = {"wx_count": 0, "wb_count": 0, "website_count": 0, "app_count": 0, "bz_count": 0,
                      "we_media_count": 0, "count": 0, "timestamp_list": list(), "media_set": set()}
        for spread_detail in result:
            if spread_detail["similarPlatformType"] == 1:
                # 微信，
                count_dict["wx_count"] += 1
                # if spread_detail["rivalImportance"] == 1:
                #     count_dict["important_wx_count"] += 1
                #     count_dict["important_count"] += 1
                # if spread_detail["rivalMainMedia"] == 1:
                #     count_dict["main_media_count"] += 1
            elif spread_detail["similarPlatformType"] == 2:
                # 微博。
                count_dict["wb_count"] += 1
                # if spread_detail["rivalImportance"] == 1:
                #     count_dict["important_wb_count"] += 1
                #     count_dict["important_count"] += 1
                # if spread_detail["rivalMainMedia"] == 1:
                #     count_dict["main_media_count"] += 1
            elif spread_detail["similarPlatformType"] == 3:
                # 网站。
                count_dict["website_count"] += 1
                # if spread_detail["rivalImportance"] == 1:
                #     count_dict["important_wz_count"] += 1
                #     count_dict["important_count"] += 1
                # if spread_detail["rivalMainMedia"] == 1:
                #     count_dict["main_media_count"] += 1
                # # 添加URL去重（覆盖的范围较大，网站、报纸、客户端都会被列入去重范畴，但此集合是用于站外搜索引擎的）。
                # if "rivalUrl" in spread_detail and spread_detail["rivalUrl"]:
                #     count_dict["url_set"].add(spread_detail["rivalUrl"])
            elif spread_detail["similarPlatformType"] == 4:
                # app客户端。
                count_dict["app_count"] += 1
            elif spread_detail["similarPlatformType"] == 5:
                # 报纸。
                count_dict["bz_count"] += 1
                # if spread_detail["rivalImportance"] == 1:
                #     count_dict["important_bz_count"] += 1
                #     count_dict["important_count"] += 1
                # if spread_detail["rivalMainMedia"] == 1:
                #     count_dict["main_media_count"] += 1
            elif spread_detail["similarPlatformType"] == 7:
                # 自媒体。
                count_dict["we_media_count"] += 1
                # if spread_detail["rivalImportance"] == 1:
                #     count_dict["important_we_media_count"] += 1
                #     count_dict["important_count"] += 1
                # if spread_detail["rivalMainMedia"] == 1:
                #     count_dict["main_media_count"] += 1
            # 总数追加1。
            count_dict["count"] += 1   # 被转载次数
            # 整合发布时间列表。
            count_dict["timestamp_list"].append(spread_detail["similarPubTime"])
            # 整合转载媒体信息。
            count_dict["media_set"].add(spread_detail["similarPlatformName"])
        return count_dict

    def compute_spread_hi(self, count_dict, source_detail):
        """
        计算HI相关数值。
        :return:
        """
        # 传播数据统计。
        spread_data = dict()
        # 转载该作品的媒体数。
        spread_data["rePrintNum"] = count_dict["count"]
        spread_data["reprintMediaNum"] = len(count_dict["media_set"])
        # 计算spreadHi。
        spread_score = 0.1 * math.log(count_dict.get("wx_count") + 1) \
                       + 0.1 * math.log(count_dict.get("wb_count") + 1) \
                       + 0.2 * math.log(count_dict.get("website_count") + 1) \
                       + 0.2 * math.log(count_dict.get("app_count") + 1) \
                       + 0.2 * math.log(count_dict.get("bz_count") + 1) \
                       + 0.2 * math.log(count_dict.get("we_media_count") + 1)
        time_score = self.compute_pubtime_score(source_detail["pubTime"], count_dict.get("timestamp_list"))
        mci = 0.9 * spread_score + 0.1 * time_score
        spread_data["hi"] = mci * mci * 10

        # 判断是否为原创 进而选择不同的计算HI方式
        if source_detail["isOriginal"] == 0:  # 非原创
            # 非原创的权重
            spread_data["hi"] = mci * mci * 10 * 0.5
        if source_detail["isOriginal"] == -1 and source_detail["isOriginalCompute"] == 0:  # 非原创
            # 非原创的权重
            spread_data["hi"] = mci * mci * 10 * 0.5

        return spread_data

    def run(self, source_detail, result):
        # result = self.search_es_data(source_detail)
        count_dict = self.compute_data_from_es(result)
        # count_dict = {"count": 100, "wx_count": 10, "wb_count": 10, "website_count": 20, "app_count": 20,
        #               "bz_count": 20, "we_media_count": 20,
        #               "media_set": {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19},
        #               "timestamp_list": [1611342300000, 1611342300000, 1611342300000, 1611342300000, 1611342300000,
        #                                  1611342300000, 1611342300000, 1611342300000, 1611342300000, 1611342300000]}
        spread_data = self.compute_spread_hi(count_dict, source_detail)
        field = {
            "reprintNum": spread_data["rePrintNum"],
            "reprintMediaNum": spread_data["reprintMediaNum"],
            "spreadHI": spread_data["hi"]
        }
        field_id = source_detail["_id"]
        fields = dict(doc=field)
        print(fields)
        return fields, field_id


if __name__ == '__main__':
    sod = {"_id": "a5eaaa0111001bb06ef0596dbe97d4bb", "platformName": "人民日报APP", "platformType": 7,
           "accountName": "河北日报", "source": "南宫发布", "pubTime": 1609729268000, "isOriginal": -1,
           "isOriginalCompute": -1}
    ComputeSpreadHi().run(sod)

