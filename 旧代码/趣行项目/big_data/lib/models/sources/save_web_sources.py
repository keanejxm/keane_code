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
from common_utils.utils import md5


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
        for item in content.values():
            fields = dict()
            fields["status"] = 1
            field_id = item["id"]
            fields["name"] = item["name"]
            fields["createTime"] = now
            fields["updateTime"] = now
            if "is_main" in item and item["is_main"] == 1:
                # 主体，可能是报纸名、网站名、账号名等。
                field_id = md5(item["name"] + p_type)
                if not es_conn.exists(index="dc_platforms", id=field_id, doc_type="_doc"):
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
                    res = es_conn.index(index="dc_platforms", id=field_id, body=fields, doc_type="_doc")
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
            else:
                fields["parentID"] = item["parent_id"]
                fields["eName"] = ""
                fields["describe"] = ""
                res = es_conn.index(index="dc_source_types", id=field_id, body=fields, doc_type="_doc")
            print(f"{field_id}，{res['result']}")

    def save(self):
        """
        保存信源模型。
        :return:
        """
        paths = rf"/home/debugger/neil/big_data/big_data_platform/lib/models/sources/全部信源_结果/网站数据.json"
        res = self.save_to_es(paths)


if __name__ == '__main__':
    TempSources().save()
