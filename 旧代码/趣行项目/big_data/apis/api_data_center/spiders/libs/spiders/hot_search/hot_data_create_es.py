# -*- encoding:utf-8 -*-
"""
@功能:将热搜数据存入es
@AUTHOR：Keane
@文件名：hot_data_create_es.py
@时间：2020/12/25  10:29
"""
import hashlib
import json
import time
# import elasticsearch

from api_common_utils.text_processing_tools import get_text_byte_length


class WashData(object):

    @staticmethod
    def md5_encode(data_res):
        has = hashlib.md5()
        has.update(str(data_res).encode("utf8"))
        md_res = has.hexdigest()
        return md_res

    def wash_hot_search_data(self, hot_search_fields, platform):
        top_query = []
        if platform != "4":
            for hot_search_field in hot_search_fields:
                serial_num = hot_search_field.get("serial_num")
                news_name = hot_search_field.get("news_name")
                news_url = hot_search_field.get("news_url")
                update_time = hot_search_field.get("updatetime")
                search_exponent = hot_search_field.get("search_exponent")
                if not search_exponent:
                    search_exponent = ""
                top_q = {"name": news_name, "hotMarks": search_exponent, "url": news_url, "serialNum": serial_num,
                         "updateTime": update_time}
                top_query.append(top_q)
        else:
            top_query = hot_search_fields
        # top_query = json.dumps(top_query, indent=4, ensure_ascii=False)
        top_query = json.dumps(top_query, separators=(",", ":"))
        field = {
            "_id": "",
            "status": 1,
            "queryPlatform": platform,  # 搜索平台，1百度热搜，2微博热搜，3抖音热搜, 4站内热搜
            # 热搜数据，json体（列表顺序决定排序），[{“name”: “热词1”，”hotMarks”：”12345”，…}, {“name”: “热词2”…}]，由于是keyword类型，注意不要太长
            "topQueries": top_query,
            "createTime": int(time.time() * 1000),
            "updateTime": int(time.time() * 1000),
        }
        plat = {"1": "百度热搜", "2": "微博热搜", "3": "抖音热搜", "4": "站内热搜"}
        p = field.get("queryPlatform")
        pla = plat.get(str(p))
        md5_str = field.get("topQueries") + pla
        s = get_text_byte_length(str(md5_str))
        print(s)
        _id = self.md5_encode(md5_str)
        field["_id"] = _id
        return field

    # def _es_create_new_works(self, index_name, field_id, fields):
    #     res = self._es_conn.index(index=index_name, doc_type="_doc", body=fields, id=field_id)
    #     return res["result"]

    # def api_create_articel(self, fields, platform):
    #     fields = self.wash_hot_search_data(fields, platform)
    #     _id = fields.pop("_id")
    #     res = self._es_create_new_works("dc_top_queries_v1", fields=fields, field_id=_id)
    #     return {"code": 1, "msg": "success", "result": res, }

# def test():
#     fields = {
#         "topicID": "4_53685",
#         "platformName": "解放军报",
#         "platformID": "",
#         "channelName": "",
#         "channelID": "",
#         "topicUrl": "http://appapi.81.cn/v4/public/jfjbshare/?topicid=4_53685&type=1",
#         "title": "纪念玉树灾后重建十周年",
#         "digest": "震后十年，灾难的元素渐渐淡去，带着祈愿与美好生活的向往，玉树人在前行……",
#         "topicCover": [
#             "https://appimg.81.cn/thumbs2/680/179/data/mediafile/pic/img/2020/04/09/6557eb0d3d5c49d7b9d"
#             "030601059e093.jpg"
#         ],
#         "pubTime": 1586133933000,
#         "articleNum": 22,
#         "newestArticle": "",
#         "articleIDs": [
#             "4_53829",
#             "4_53825",
#             "4_53831",
#             "4_53827",
#             "4_53817",
#             "4_53731",
#             "4_53729",
#             "4_53707",
#             "4_53705",
#             "4_53703",
#             "4_53701",
#             "4_53699",
#             "4_53697",
#             "4_53695",
#             "4_53693",
#             "4_53691",
#             "4_53689",
#             "4_53717",
#             "4_53733",
#             "4_53723",
#             "4_53721",
#             "4_53725"
#         ],
#         "articlesNumPerHour": "",
#         "original": "",
#         "firstMedia": "",
#         "transPower": "",
#         "hotDegree": "",
#         "wordsFreq": "",
#         "hotDegreeTrend": "",
#         "emotionTrend": "",
#         "region": "",
#         "spreadPath": "",
#         "createTime": "",
#         "updateTime": ""
#     }
#     # es_utils = EsUtils()
#     fields = es_utils.wash_hot_search_data(fields, "aa")
#     _id = fields.pop("_id")
#     res = es_utils._es_create_new_works("dc_topics_v1", fields=fields, field_id=_id)
#     # fields = es_utils.wash_article_data(fields)
#     # _id = fields.pop("_id")
#     # res = es_utils._es_create_new_works("dc_works",fields = fields,field_id = _id)
#     print(res)


# if __name__ == '__main__':
#     test()
