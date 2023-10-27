# -*- coding:utf-8 -*-
"""
上传信源模板，源自每个人的统计数据（excel表）。
# author: Trico
# date: 2020/12/16
# update: 2020/12/16
"""

import json
import os
import re
import time

import elasticsearch

from common_utils.utils import md5
from models.sources.parse_sources import SourceData


class TempSources(SourceData):
    """
    整理人工提取的信源数据。
    """

    def __init__(self):
        super(TempSources, self).__init__()

    def save_to_es(self, path):
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
        # 添加app平台到es平台数据库
        # 平台的id和平台的name
        platform_id = ""
        platform_name = ""
        num = 0
        for item in content.values():
            fields = dict()
            field_id = item["id"]
            res_other = re.findall("^3_1_(\d+_\d+)$|^3_2_(\d+_\d+)$|^3_3_(\d+_\d+)$",
                                   field_id)  # 取到这个数据是第三方移动端，和地方媒体客户端,的客户端id
            if res_other:
                num += 1
                print(res_other)
                print(item["name"])
            res_central = re.findall("^4_3_(\d+)$|^4_4_(\d+)$", field_id)  # 取到这个数据说明是中央媒体客户端，客户端id
            if res_central:
                num += 1
                print(res_central)
                print(item["name"])
            fields["name"] = item["name"]
            fields["createTime"] = now
            fields["updateTime"] = now
            if "is_main" in item and item["is_main"] == 1:
                # 主体，可能是报纸名、网站名、账号名等。
                field_id = md5(item["name"] + p_type)
                if res_other or res_central:
                    # platform_id = field_id
                    # platform_name = item["name"]
                    if not es_conn.exists(index="dc_platforms", doc_type="_doc", id=field_id):
                        fields["introduction"] = ""
                        fields["logo"] = ""
                        fields["weMediaName"] = ""
                        fields["url"] = item["url"]
                        fields["type"] = int(p_type)
                        if item["parent_id"]:
                            fields["types"] = [item["parent_id"]]
                        else:
                            fields["types"] = []
                        fields["selfTypesIDs"] = [item["id"]]
                        fields["region"] = []
                        fields["worksNum"] = 0
                        fields["region"] = []
                        fields["status"] = 0
                        res = es_conn.index(index="dc_platforms", id=field_id, body=fields, doc_type="_doc")

                    # 更新app平台数据库
                    else:
                        exist_fields = es_conn.get(index="dc_platforms", id=field_id, doc_type="_doc")["_source"]
                        if item["parent_id"]:
                            a = exist_fields["types"]
                            a.append(item["parent_id"])
                            exist_fields["types"] = list(set(a))
                        b = exist_fields["selfTypesIDs"]
                        b.append(item["id"])
                        exist_fields["selfTypesIDs"] = list(set(b))
                        res = es_conn.index(index="dc_platforms", id=field_id, body=exist_fields, doc_type="_doc")
                # else:
                #     #添加频道信息
                #     field_id = md5(platform_id+item["name"])
                #     if not es_conn.exists(index = "dc_channels", doc_type = "_doc", id = field_id):
                #         fields["status"] = 0
                #         fields["platformID"] = platform_id
                #         fields["platformName"] = platform_name
                #         fields["url"] = item["url"]
                #         if item["parent_id"]:
                #             fields["types"] = [item["parent_id"]]
                #         else:
                #             fields["types"] = []
                #         fields["selfTypesIDs"] = [item["id"]]
                #         fields["region"] = []
                #         res = es_conn.index(index = "dc_channels", id = field_id, body = fields, doc_type = "_doc")
                #
                #     # 更新app频道es数据库
                #     else:
                #         exist_fields = es_conn.get(index = "dc_channels", id = field_id, doc_type = "_doc")["_source"]
                #         if item["parent_id"]:
                #             a = exist_fields["types"]
                #             a.append(item["parent_id"])
                #             exist_fields["types"] = list(set(a))
                #         b = exist_fields["selfTypesIDs"]
                #         b.append(item["id"])
                #         exist_fields["selfTypesIDs"] = list(set(b))
                #         res = es_conn.index(index = "dc_channels", id = field_id, body = exist_fields,
                #                             doc_type = "_doc")
                else:
                    res = {"result": "hh"}
            else:
                fields["parentID"] = item["parent_id"]
                fields["tagInfo"] = "type"
                fields["status"] = 1
                fields["eName"] = ""
                fields["describe"] = ""
                res = es_conn.index(index="dc_source_types", id=field_id, body=fields, doc_type="_doc")
            print(f"{field_id}，{res['result']}")

    def save(self):
        """
        保存信源模型。
        :return:
        """
        path = "/home/debugger/keane/big_data/big_data_platform/lib/models/sources/APP数据.json"

        res = self.save_to_es(path)


if __name__ == '__main__':
    TempSources().save()
