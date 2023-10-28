# -*- coding:utf-8 -*-
"""
上传信源模板，源自每个人的统计数据（excel表）。
# author: Trico
# date: 2020/12/16
# update: 2020/12/16
"""

import os
import json
import time
import elasticsearch
from models.sources.parse_sources import SourceData
from models.sources.weibo_name_to_uid import XinYuanAccount

from common_utils.utils import md5
import traceback


def test_name_true(conn, item):
    query_body = {
        "size": 9999,
        "query": {
            "bool": {
                "must": [
                    {"match_phrase": {"name": item["name"]}},
                    {"term": {"platformName": "微博"}}
                ]
            }
        }
    }
    response = conn.search(index="dc_accounts", doc_type="_doc", body=query_body)
    if int(response["hits"]["total"]) == 1:
        if "platformType" not in response["hits"]["hits"][0]["_source"].keys():
            fid = response["hits"]["hits"][0]["_id"]
            conn.update(index="dc_accounts", doc_type="_doc", id=fid,
                        body={"doc": {"platformType": 2, "updateTime": int(time.time()*1000),
                                      "selfTypesIDs": [item["id"]]}})
            print(f'--{response["hits"]["hits"][0]["_source"]["name"]}--已更新了platformType')
    return response


class TempSources(SourceData):
    """
    整理人工提取的信源数据。
    """

    def __init__(self):
        super(TempSources, self).__init__()

    def save_to_es(self, path, data):
        """
        保存信源至ES。
        :return:
        """

        platform_type = str(os.path.basename(path).split(".")[0])
        p_type = self._known_types[platform_type]
        with open(path, "rb") as fr:
            content = json.load(fr)
        es_conn = elasticsearch.Elasticsearch([{"host": "180.76.161.67", "port": 9200}])
        now = int(time.time() * 1000)
        platform_type_dict = dict()
        # platform_type_dict["_id"] = platform_type_id
        platform_type_dict["status"] = 1
        platform_type_dict["name"] = "微博"
        platform_type_dict["introduction"] = ""
        platform_type_dict["logo"] = ""
        platform_type_dict["weMediaName"] = "微博"
        platform_type_dict["url"] = ""
        platform_type_dict["type"] = int(p_type)
        platform_type_dict["types"] = list()
        platform_type_dict["selfTypesIDs"] = [p_type]
        platform_type_dict["region"] = list()
        platform_type_dict["createTime"] = now
        platform_type_dict["updateTime"] = now
        platform_type_id = md5(platform_type_dict["name"] + p_type)
        res = es_conn.index(index="dc_platforms", id=platform_type_id, body=platform_type_dict, doc_type="_doc")
        for item in content.values():
            try:
                fields = dict()
                field_id = item["id"]
                fields["name"] = item["name"]
                fields["createTime"] = int(time.time() * 1000)
                fields["updateTime"] = int(time.time() * 1000)
                if "is_main" in item and item["is_main"] == 1 and item["parent_id"]:
                    # 主体，可能是报纸名、网站名、账号名等。
                    resp = test_name_true(es_conn, item)
                    if int(resp["hits"]["total"]) == 1:
                        print(f"--{resp['hits']['hits'][0]['_source']['name']}--已经存在，到此结束")
                        continue
                    if item["name"] in data:
                        print(f"--{item['name']}--已经存在与寻找为空的txt文本中，到此结束")
                        continue
                    result = XinYuanAccount().fetch(item)
                    # md5(platformID+platformAccountID)
                    if len(result) != 0:
                        account_id = result[0]["uid"]
                        mid_str = md5(platform_type_dict["name"] + p_type)
                        field_id = md5(mid_str + account_id)
                        if not es_conn.exists(index="dc_accounts", id=field_id, doc_type="_doc"):
                            fields["status"] = 1
                            fields["platformAccountID"] = result[0]["uid"]
                            fields["introduction"] = ""
                            fields["avatar"] = result[0]["avatar"]
                            fields["qrcode"] = ""
                            fields["gender"] = int(result[0]["sex"])
                            fields["mobilePhoneNumber"] = ""
                            fields["email"] = ""
                            fields["identityCode"] = ""
                            fields["certificationType"] = -1
                            fields["url"] = result[0]["url"]
                            if result[0]["city"]:
                                fields["region"] = [result[0]["province"], result[0]["city"]]
                            else:
                                fields["region"] = [result[0]["province"]]
                            """这个id和name"""
                            fields["platformID"] = mid_str
                            fields["platformName"] = platform_type_dict["name"]
                            fields["platformType"] = int(p_type)
                            fields["weMediaName"] = "微博"
                            fields["platformWorksNum"] = 0
                            fields["platformFansNum"] = 0
                            fields["platformFollowsNum"] = 0
                            fields["platformReadsNum"] = 0
                            fields["platformLikesNum"] = 0
                            fields["platformCommentsNum"] = 0
                            fields["platformForwardsNum"] = 0
                            fields["worksNum"] = 0
                            fields["readNum"] = 0
                            fields["likeNum"] = 0
                            fields["commentNum"] = 0
                            fields["forwardNum"] = 0
                            fields["collectNum"] = 0
                            if item["parent_id"]:
                                fields["types"] = [item["parent_id"]]
                            else:
                                fields["types"] = []
                            fields["selfTypesIDs"] = [item["id"]]
                            res = es_conn.index(index="dc_accounts", id=field_id, body=fields, doc_type="_doc")
                        else:
                            exist_fields = es_conn.get(index="dc_accounts", id=field_id, doc_type="_doc")["_source"]
                            if item["parent_id"]:
                                exist_fields["types"].append(item["parent_id"])
                                exist_fields["types"] = list(set(exist_fields["types"]))
                            exist_fields["selfTypesIDs"].append(item["id"])
                            exist_fields["selfTypesIDs"] = list(set(exist_fields["selfTypesIDs"]))
                            res = es_conn.index(index="dc_accounts", id=field_id, body=exist_fields, doc_type="_doc")
                    else:
                        print(f"{item['name']}的查询结果是：{result}")
                        continue
                else:
                    fields["parentID"] = item["parent_id"]
                    fields["eName"] = ""
                    fields["describe"] = ""
                    fields["tagInfo"] = ""
                    fields["order"] = 0
                    if not es_conn.exists(index="dc_source_types", id=field_id, doc_type="_doc"):
                        res = es_conn.index(index="dc_source_types", id=field_id, body=fields, doc_type="_doc")
            except Exception as e:
                print(f"{e}.\n{traceback.format_exc()}")
                path = "/home/debugger/chris/big_data/big_data_platform/lib/models/sources_weibo_json/"
                with open(path + "error_res.txt", "a", encoding="utf8") as f:
                    f.write(json.dumps(item, ensure_ascii=False))
                    f.write("\n")
                continue

            print(f"{field_id}，{res['result']}")

    def save(self):
        """
        保存信源模型。
        :return:
        """

        # for path in self.find_target_files(self._path_3, "json"):
        #     if "报纸数据" in path:
        #         res = self.save_to_es(path)
        path = "/home/debugger/chris/big_data/big_data_platform/lib/models/sources_weibo_json/微博数据.json"
        path1 = "/home/debugger/chris/big_data/big_data_platform/lib/models/sources_weibo_json/empty_res.txt"
        print(os.path.exists(path1))
        with open(path1, "r", encoding="utf8") as f1:
            json_data1 = f1.read()
        self.save_to_es(path, json_data1)


if __name__ == '__main__':
    TempSources().save()
