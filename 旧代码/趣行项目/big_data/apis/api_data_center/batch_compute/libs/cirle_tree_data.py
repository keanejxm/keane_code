# -*- coding: utf-8 -*-#
# Date:         2021/1/15

import time
import json
import elasticsearch

from api.config import es_config
from api_common_utils.utils import md5


def update_es_data():
    """test1"""
    es_conn = elasticsearch.Elasticsearch(**es_config)
    filed = {
        "status": 1,
        "sourceId": "a5eaaa0111001bb06ef0596dbe97d4bb",
        "similarId": "32aec4b40224a73a210d31513c73e51d",
        "similarPlatformID": "7866e297ebeb3d8d600497cac5a46dd8",
        "similarPlatformType": 2,
        "similarPlatformName": "微博",
        "similarChannelID": "",
        "similarChannelName": "",
        "similarAccountID": "01bf9358b01fb2c98d53798990daf2f9",
        "similarAccountName": "河北日报",
        "similarTitle": " 河北日报 :【#石家庄藁城区公布2例确诊病例行程轨迹#】2021年1月3日0—24时，石家庄市藁城区新增2例新冠肺炎确诊病例，对追踪到的密切接触者已全部采取集中隔离医学观察措施。现将该确诊病例的行程轨迹公布如下：患者2，男，52岁，现住石家庄市藁城区刘家佐村。2020年12月26日出现发热症状并居家，27日到藁城区小果庄村某诊所就诊，27—28日居家无外出，29—30日再次到同一诊所就诊，31日—2021年1月2日居家无外出，1月2日下午由家人驾车送到新乐市人民医院就诊，当日核酸检测结果呈阳性，后经鼻、咽拭子采样检测确诊为新冠肺炎病例。1月3日凌晨4点由负压救护车转运至石家庄市定点医院接受隔离治疗。患者3，女，58岁，藁城区增村镇小果庄村村民。2020年12月30日身体出现不适，31日由家人驾车送到邻村某诊所就诊。除此之外，从2020年12月30日至2021年1月3日居家治疗，未接触过其他外来人员，未去过本村以外的地区，未参加集会聚餐等活动。1月3日，经疾控部门集中筛查，其新冠病毒核酸检测结果为阳性，于当日由负压救护车转运至石家庄市定点医院接受隔离治疗，确诊为新冠肺炎病例。（藁城融媒）[编辑|王伟]                 ",
        "similarDigest": "河北日报:2021年1月3日0—24时，石家庄市藁城区新增2例新冠肺炎确诊病例，对追踪到的密切接触者已全部采取集中隔离医学观察措施。现将该确诊病例的行程轨迹公布如下：患者2，男，52岁，现住石家庄市藁城区刘家佐村。患者3，女，58岁，藁城区增村镇小果庄村村民。1月3日，经疾控部门集中筛查，其新冠病毒核酸检测结果为阳性，于当日由负压救护车转运至石家庄市定点医院接受隔离治疗，确诊为新冠肺炎病例。",
        "similarUrl": "https://weibo.com/1623340585/JBCQHBu92",
        "similarPubTime": 1609747198000,
        "similarIsOriginal": 1,
        "similarIsOriginalCompute": -1,
        "similarCovers": [
            "http://wx3.sinaimg.cn/large/001LRn2Fly1gmbpynxlkfj60j60da76v02.jpg"
        ],
        "similarVideos": [],
        "similarAudios": [],
        "sourceParentId": "",
        "similarRegion": ["河北"],
        "similarSource": ""
    }
    # filed_id = "48902b833aef3f1c985a8fa4db9aeb4f"
    filed_id = filed["similarId"]
    res = es_conn.index(index="dc_spread_route", doc_type="_doc", id=filed_id, body=filed)
    print(res["_id"] + "-----" + res["result"])


class CircleAndTreeData:

    def __init__(self):
        self.target_index = "dc_spread_route"
        self.spread_index = "dc_spread_route_final"
        self.es_conn = elasticsearch.Elasticsearch(**es_config)

    def search_data_es(self, source_id):
        must_list = list()
        # must_list.append({"term": {"sourceId": "a5eaaa0111001bb06ef0596dbe97d4bb"}})
        must_list.append({"term": {"sourceId": source_id}})
        body = {
            "size": 9999,
            # "_source": ["similarPlatformName", "similarAccountName", "similarSource", "similarPlatformName"],
            "query": {"bool": {"must": must_list}},
        }
        res1 = self.es_conn.search(index="dc_spread_route", request_timeout=3600, body=body)
        result = []
        if res1["hits"]["total"] > 0:
            for work in res1["hits"]["hits"]:
                item = work["_source"]
                item["_id"] = work["_id"]
                result.append(item)
        return result

    def update_data_es(self, rest, fid):
        rest["updateTime"] = int(time.time() * 1000)
        res = self.es_conn.index(index=self.spread_index, doc_type="_doc", body=rest, id=fid)
        print(res["_id"] + "---" + res["result"])

    def tree_data_res(self, source_detail):
        result = self.search_data_es(source_detail["_id"])
        end_res_dict = dict()  # 最终结果
        up_parent = []  # 祖父级作品
        sibling_dict = []  # 同级作品
        children_dict = []  # 子级作品
        if len(result) == 0:
            return end_res_dict
        if len(result) == 1:
            # parent_dict = [
            #     {"name": i["similarAccountName"], "type": [i["similarPlatformName"], i["similarPlatformType"]],
            #      "source": i["similarSource"], "parentId": "", "_id": i["similarId"]} for i in result if
            #     i["similarAccountName"] == source_detail["source"]]
            parent_dict = []
            for i in result:
                item = dict()
                if source_detail["source"]:
                    if i["similarAccountName"]:
                        if source_detail["source"] in i["similarAccountName"] or i["similarAccountName"] in source_detail["source"]:
                            item = {"name": i["similarAccountName"],
                                    "type": [i["similarPlatformName"], i["similarPlatformType"]],
                                    "source": i["similarSource"], "parentId": "", "_id": i["similarId"]}
                    else:
                        if source_detail["source"] in i["similarPlatformName"] or i["similarPlatformName"] in source_detail["source"]:
                            item = {"name": i["similarAccountName"],
                                    "type": [i["similarPlatformName"], i["similarPlatformType"]],
                                    "source": i["similarSource"], "parentId": "", "_id": i["similarId"]}
                if item:
                    parent_dict.append(item)
            children_dict = []
            if len(parent_dict) == 0:
                # children_dict = [
                #     {"name": i["similarAccountName"], "type": [i["similarPlatformName"], i["similarPlatformType"]],
                #      "source": i["similarSource"], "parentId": source_detail["_id"], "_id": i["similarId"]}
                #      for i in result if i["similarSource"] == source_detail["accountName"]]
                for i in result:
                    item = dict()
                    if i["similarSource"]:
                        if source_detail["accountName"]:
                            if i["similarSource"] in source_detail["accountName"] or source_detail["accountName"] in i["similarSource"]:
                                item = {"name": i["similarAccountName"],
                                        "type": [i["similarPlatformName"], i["similarPlatformType"]],
                                        "source": i["similarSource"], "parentId": source_detail["_id"], "_id": i["similarId"]}
                        else:
                            if i["similarSource"] in source_detail["platformName"] or source_detail["platformName"] in i["similarSource"]:
                                item = {"name": i["similarAccountName"],
                                        "type": [i["similarPlatformName"], i["similarPlatformType"]],
                                        "source": i["similarSource"], "parentId": source_detail["_id"], "_id": i["similarId"]}
                    if item:
                        children_dict.append(item)
            if len(parent_dict) != 0:
                end_res_dict = {"name": parent_dict[0]["name"], "type": parent_dict[0]["type"],
                                "children": [{"name": source_detail["accountName"], "parentId": parent_dict[0]["_id"],
                                             "type": [source_detail["platformName"], source_detail["platformType"]],
                                              "_id": source_detail["_id"]}]}
            if len(children_dict) != 0:
                end_res_dict = {"name": source_detail["accountName"],
                                "type": [source_detail["platformName"], source_detail["platformType"]], "parentId": "",
                                "children": children_dict}
            return end_res_dict

        else:
            # 第一次查询获取其上级信息
            # parent_dict = [
            #     {"name": i["similarAccountName"], "type": [i["similarPlatformName"], i["similarPlatformType"]],
            #      "source": i["similarSource"], "parentId": "", "_id": i["similarId"]} for i in result
            #     if i["similarAccountName"] == source_detail["source"]]
            parent_dict = []
            if source_detail["source"]:
                for i in result:
                    item = dict()
                    if i["similarAccountName"]:
                        if source_detail["source"] in i["similarAccountName"] or i["similarAccountName"] in source_detail["source"]:
                            item = {"name": i["similarAccountName"],
                                    "type": [i["similarPlatformName"], i["similarPlatformType"]],
                                    "source": i["similarSource"], "parentId": "", "_id": i["similarId"]}
                    else:
                        if source_detail["source"] in i["similarPlatformName"] or i["similarPlatformName"] in source_detail["source"]:
                            item = {"name": i["similarAccountName"],
                                    "type": [i["similarPlatformName"], i["similarPlatformType"]],
                                    "source": i["similarSource"], "parentId": "", "_id": i["similarId"]}
                    if item:
                        parent_dict.append(item)
            # print(f"第一次获取父级：{parent_dict}")
            source_detail_lis = []
            if len(parent_dict) != 0:
                # 如果确定待查作品的上级，那么为待查作品加parentID
                for p in range(len(parent_dict)):
                    source_detail["parentId"] = parent_dict[p]["_id"]
                    source_detail_lis.append(source_detail)
                # 如果确定待查作品的上级，那么再向上追溯该作品的祖父级
                up_parent = []
                for p in range(len(parent_dict)):
                    # up_parent = [
                    #     {"name": i["similarAccountName"], "type": [i["similarPlatformName"], i["similarPlatformType"]],
                    #      "source": i["similarSource"], "_id": i["similarId"], "parentId": "", } for i in result
                    #     if i["similarAccountName"] == parent_dict[p]["source"]]
                    if parent_dict[p]["source"]:
                        for i in result:
                            item = dict()
                            if i["similarAccountName"]:
                                if parent_dict[p]["source"] in i["similarAccountName"] or i["similarAccountName"] in parent_dict[p]["source"]:
                                    item = {"name": i["similarAccountName"],
                                            "type": [i["similarPlatformName"], i["similarPlatformType"]],
                                            "source": i["similarSource"], "_id": i["similarId"], "parentId": ""}
                            else:
                                if parent_dict[p]["source"] in i["similarPlatformName"] or i["similarPlatformName"] in parent_dict[p]["source"]:
                                    item = {"name": i["similarAccountName"],
                                            "type": [i["similarPlatformName"], i["similarPlatformType"]],
                                            "source": i["similarSource"], "_id": i["similarId"], "parentId": ""}
                            if item:
                                up_parent.append(item)
                print(f"祖父级：{up_parent}")
                # 若有祖父级则在其下查询，看是否有父级同级作品
                if len(up_parent) != 0:
                    parent_dict = []
                    for u in range(len(up_parent)):
                        # parent_dict = [
                        #     {"name": i["similarAccountName"],
                        #      "type": [i["similarPlatformName"], i["similarPlatformType"]],
                        #      "source": i["similarSource"], "_id": i["similarId"], "parentId": up_parent[u]["_id"]} for i
                        #     in result if i["similarSource"] == up_parent[u]["name"]]
                        for i in result:
                            item = dict()
                            if i["similarSource"]:
                                if up_parent[u]["name"]:
                                    if i["similarSource"] in up_parent[u]["name"] or up_parent[u]["name"] in i["similarSource"]:
                                        item = {"name": i["similarAccountName"],
                                                "type": [i["similarPlatformName"], i["similarPlatformType"]],
                                                "source": i["similarSource"], "_id": i["similarId"],
                                                "parentId": up_parent[u]["_id"]}
                                else:
                                    if i["similarSource"] in up_parent[u]["type"][0] or up_parent[u]["type"][0] in i["similarSource"]:
                                        item = {"name": i["similarAccountName"],
                                                "type": [i["similarPlatformName"], i["similarPlatformType"]],
                                                "source": i["similarSource"], "_id": i["similarId"],
                                                "parentId": up_parent[u]["_id"]}
                            if item:
                                parent_dict.append(item)
                    print(f"祖父级下与已确定父级的同级：{parent_dict}")
            # 确定同级作品
            if len(parent_dict) != 0:
                sibling_dict = []
                for p in range(len(parent_dict)):
                    # sibling_dict = [
                    #     {"name": i["similarAccountName"], "type": [i["similarPlatformName"], i["similarPlatformType"]],
                    #      "source": i["similarSource"], "_id": i["similarId"], "parentId": parent_dict[p]["_id"]} for i
                    #     in result if i["similarSource"] == parent_dict[p]["name"]]
                    for i in result:
                        item = dict()
                        if i["similarSource"]:
                            if parent_dict[p]["name"]:
                                if i["similarSource"] in parent_dict[p]["name"] or parent_dict[p]["name"] in i["similarSource"]:
                                    item = {"name": i["similarAccountName"],
                                            "type": [i["similarPlatformName"], i["similarPlatformType"]],
                                            "source": i["similarSource"], "_id": i["similarId"],
                                            "parentId": parent_dict[p]["_id"]}
                            else:
                                if i["similarSource"] in parent_dict[p]["type"][0] or parent_dict[p]["type"][0] in i["similarSource"]:
                                    item = {"name": i["similarAccountName"],
                                            "type": [i["similarPlatformName"], i["similarPlatformType"]],
                                            "source": i["similarSource"], "_id": i["similarId"],
                                            "parentId": parent_dict[p]["_id"]}
                        if item:
                            sibling_dict.append(item)
            # 待查作品本身是同级作品
            if len(source_detail_lis) != 0:
                for sol in source_detail_lis:
                    sibling_dict.append({"name": sol["accountName"], "type": [sol["platformName"], sol["platformType"]],
                                         "source": sol["source"], "_id": sol["_id"], "parentId": sol["parentId"]})
            else:
                sibling_dict.append({"name": source_detail["accountName"],
                                     "type": [source_detail["platformName"], source_detail["platformType"]],
                                     "source": source_detail["source"], "_id": source_detail["_id"], "parentId": ""})
            # print(f"同级：{sibling_dict}")
            # 子级目录
            children_dict = []
            if len(sibling_dict) != 0:
                for s in range(len(sibling_dict)):
                    # children_dict = [
                    #     {"name": i["similarAccountName"], "type": [i["similarPlatformName"], i["similarPlatformType"]],
                    #      "source": i["similarSource"], "_id": i["similarId"], "parentId": sibling_dict[s]["_id"]} for i
                    #     in result if sibling_dict[s]["name"] == i["similarSource"]]
                    for i in result:
                        item = dict()
                        if i["similarSource"]:
                            if sibling_dict[s]["name"]:
                                if i["similarSource"] in sibling_dict[s]["name"] or sibling_dict[s]["name"] in i["similarSource"]:
                                    item = {"name": i["similarAccountName"],
                                            "type": [i["similarPlatformName"], i["similarPlatformType"]],
                                            "source": i["similarSource"], "_id": i["similarId"],
                                            "parentId": sibling_dict[s]["_id"]}
                            else:
                                if i["similarSource"] in sibling_dict[s]["type"][0] or sibling_dict[s]["type"][0] in i["similarSource"]:
                                    item = {"name": i["similarAccountName"],
                                            "type": [i["similarPlatformName"], i["similarPlatformType"]],
                                            "source": i["similarSource"], "_id": i["similarId"],
                                            "parentId": sibling_dict[s]["_id"]}
                        if item:
                            children_dict.append(item)
            # print(f"子级：{children_dict}")
            # 子孙级目录
            down_children = []
            if len(children_dict) != 0:
                for c in range(len(children_dict)):
                    for i in result:
                        item = dict()
                        if i["similarSource"]:
                            if children_dict[c]["name"]:
                                if i["similarSource"] in children_dict[c]["name"] or children_dict[c]["name"] in i["similarSource"]:
                                    item = {"name": i["similarAccountName"],
                                            "type": [i["similarPlatformName"], i["similarPlatformType"]],
                                            "source": i["similarSource"], "_id": i["similarId"],
                                            "parentId": children_dict[c]["_id"]}
                            else:
                                if i["similarSource"] in children_dict[c]["type"][0] or children_dict[c]["type"][0] in i["similarSource"]:
                                    item = {"name": i["similarAccountName"],
                                            "type": [i["similarPlatformName"], i["similarPlatformType"]],
                                            "source": i["similarSource"], "_id": i["similarId"],
                                            "parentId": children_dict[c]["_id"]}
                        if item:
                            down_children.append(item)
        if len(up_parent) > 0:
            end_res_dict = {"name": up_parent[0]["name"], "type": up_parent[0]["type"], "children": parent_dict}
            if len(sibling_dict) != 0:
                for s in end_res_dict["children"]:
                    # s["children"] = [{"name": i["name"], "type": i["type"], "source": i["source"], "_id": i["_id"],
                    #                   "parentId": i["parentId"]} for i in sibling_dict if i["source"] == s["name"]]
                    if s["name"]:
                        s["children"] = [{"name": i["name"], "type": i["type"], "source": i["source"], "_id": i["_id"],
                                          "parentId": i["parentId"]} for i in sibling_dict if i["source"] in s["name"]]
                    else:
                        s["children"] = [{"name": i["name"], "type": i["type"], "source": i["source"], "_id": i["_id"],
                                          "parentId": i["parentId"]} for i in sibling_dict if i["source"] in s["type"][0]]
            if len(children_dict) != 0:
                for c in end_res_dict["children"]:
                    for tem in c["children"]:
                        # tem["children"] = [
                        #     {"name": i["name"], "type": i["type"], "source": i["source"], "_id": i["_id"],
                        #      "parentId": i["parentId"]} for i in children_dict if i["source"] == tem["name"]]
                        if tem["name"]:
                            tem["children"] = [
                                {"name": i["name"], "type": i["type"], "source": i["source"], "_id": i["_id"],
                                 "parentId": i["parentId"]} for i in children_dict if i["source"] in tem["name"]]
                        else:
                            tem["children"] = [
                                {"name": i["name"], "type": i["type"], "source": i["source"], "_id": i["_id"],
                                 "parentId": i["parentId"]} for i in children_dict if i["source"] in tem["type"][0]]
            if len(down_children) != 0:
                for d in end_res_dict["children"]:
                    for temp1 in d["children"]:
                        for temp2 in temp1["children"]:
                            if temp2["name"]:
                                temp2["children"] = [
                                    {"name": i["name"], "type": i["type"], "source": i["source"], "_id": i["_id"],
                                     "parentId": i["parentId"]} for i in down_children if i["source"] in temp2["name"]
                                ]
                            else:
                                temp2["children"] = [
                                    {"name": i["name"], "type": i["type"], "source": i["source"], "_id": i["_id"],
                                     "parentId": i["parentId"]} for i in children_dict if i["source"] in temp2["type"][0]]
        if len(up_parent) == 0 and len(parent_dict) != 0:
            end_res_dict = {"name": parent_dict[0]["name"], "type": parent_dict[0]["type"], "children": sibling_dict}
            if len(sibling_dict) != 0:
                if len(children_dict) != 0:
                    for s in end_res_dict["children"]:
                        # s["children"] = [{"name": i["name"], "type": i["type"], "source": i["source"], "_id": i["_id"],
                        #                   "parentId": i["parentId"]} for i in children_dict if i["source"] == s["name"]]
                        if s["name"]:
                            s["children"] = [{"name": i["name"], "type": i["type"], "source": i["source"], "_id": i["_id"],
                                              "parentId": i["parentId"]} for i in children_dict if i["source"] in s["name"]]
                        else:
                            s["children"] = [{"name": i["name"], "type": i["type"], "source": i["source"], "_id": i["_id"],
                                              "parentId": i["parentId"]} for i in children_dict if i["source"] in s["type"][0]]
                if len(down_children) != 0:
                    for d in end_res_dict["children"]:
                        for tem in d["children"]:
                            if tem["name"]:
                                tem["children"] = [
                                    {"name": i["name"], "type": i["type"], "source": i["source"], "_id": i["_id"],
                                     "parentId": i["parentId"]} for i in down_children if i["source"] in tem["name"]]
                            else:
                                tem["children"] = [
                                    {"name": i["name"], "type": i["type"], "source": i["source"], "_id": i["_id"],
                                     "parentId": i["parentId"]} for i in down_children if i["source"] in tem["type"][0]]
        if len(parent_dict) == 0 and len(sibling_dict) != 0:
            if len(children_dict) != 0:
                end_res_dict = {"name": sibling_dict[0]["name"], "type": sibling_dict[0]["type"], "children": children_dict}
                if len(down_children) != 0:
                    for d in end_res_dict["children"]:
                        if d["name"]:
                            d["children"] = [{"name": i["name"], "type": i["type"], "source": i["source"], "_id": i["_id"],
                                              "parentId": i["parentId"]} for i in sibling_dict if i["source"] in d["name"]]
                        else:
                            d["children"] = [{"name": i["name"], "type": i["type"], "source": i["source"], "_id": i["_id"],
                                              "parentId": i["parentId"]} for i in sibling_dict if i["source"] in d["type"][0]]
        # print(end_res_dict)
        return end_res_dict

    def circle_data_res(self, source_detail):
        # 传播路径
        hasSpread = 0
        rest = self.tree_data_res(source_detail)
        if len(rest) == 0:
            hasSpread = 0
            return {"doc": {"hasSpread": hasSpread}}, source_detail["_id"]
        if len(rest["children"]) == 0:
            hasSpread = 0
            return {"doc": {"hasSpread": hasSpread}}, source_detail["_id"]
        item = {"nodes": [{"id": 101, "name": rest["name"], "type": rest["type"]}], "links": []}
        for first in range(len(rest["children"])):
            mid_dict = {"id": int("101" + str(first)), "name": rest["children"][first]["name"],
                        "type": rest["children"][first]["type"], "_id": rest["children"][first]["_id"],
                        "parentId": rest["children"][first]["parentId"]}
            item["nodes"].append(mid_dict)
            item["links"] += [{"source": 101, "target": mid_dict["id"]}]
            if "children" in rest["children"][first]:
                for second in range(len(rest["children"][first]["children"])):
                    mid_second_dict = {"id": int(str(mid_dict["id"]) + str(second)),
                                       "name": rest["children"][first]["children"][second]["name"],
                                       "type": rest["children"][first]["children"][second]["type"],
                                       "_id": rest["children"][first]["children"][second]["_id"],
                                       "parentId": rest["children"][first]["children"][second]["parentId"]}
                    item["nodes"].append(mid_second_dict)
                    item["links"] += [{"source": mid_dict["id"], "target": mid_second_dict["id"]}]
                    if "children" in rest["children"][first]["children"][second]:
                        for third in range(len(rest["children"][first]["children"][second]["children"])):
                            if rest["children"][first]["children"][second]["children"]:
                                mid_third_dict = {"id": int(str(mid_second_dict["id"]) + str(second)),
                                                  "name": rest["children"][first]["children"][second]["children"][third][
                                                      "name"],
                                                  "type": rest["children"][first]["children"][second]["children"][third][
                                                      "type"],
                                                  "_id": rest["children"][first]["children"][second]["children"][third]["_id"],
                                                  "parentId": rest["children"][first]["children"][second]["children"][third][
                                                      "parentId"]}
                                item["nodes"].append(mid_third_dict)
                                item["links"] += [{"source": mid_second_dict["id"], "target": mid_third_dict["id"]}]
        print(item)
        res_tree = {"application": 1, "worksID": source_detail["_id"],
                    "value": json.dumps(rest, separators=(",", ":"), ensure_ascii=False),
                    "createTime": int(time.time() * 1000)}
        res_circle = {"application": 2, "worksID": source_detail["_id"],
                      "value": json.dumps(item, separators=(",", ":"), ensure_ascii=False),
                      "createTime": int(time.time() * 1000)}
        tree_id = md5(str(res_tree["application"]) + res_tree["worksID"])
        self.update_data_es(res_tree, tree_id)
        circle_id = md5(str(res_circle["application"]) + res_circle["worksID"])
        self.update_data_es(res_circle, circle_id)
        hasSpread = 1
        return {"doc": {"hasSpread": hasSpread}}, source_detail["_id"]


if __name__ == '__main__':
    sod = {"_id": "7cd44e042621a3fa2fdfefa1bf282778", "platformName": "微博", "platformType": 2,
           "accountName": "河北日报", "source": ""}
    # CircleAndTreeData().tree_data_res(sod)
    CircleAndTreeData().circle_data_res(sod)
    # update_es_data()
