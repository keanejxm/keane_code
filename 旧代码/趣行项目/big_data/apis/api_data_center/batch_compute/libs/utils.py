# -*- coding:utf-8 -*-

"""
# author: Chris
# date: 2020/12/12
# update: 2020/12/12
"""

import elasticsearch
from api.config import es_config

import re
from bs4 import BeautifulSoup

from api_common_utils.llog import LLog

logger = LLog("test", only_console=True).logger


def check_necessary_words(text, necessary_words):
    pass


def check_source_article(source_detail, logger):
    html_text = source_detail["content"]
    soup = BeautifulSoup(html_text, "html.parser")
    # 来源--微信、看点快报、网易、百家，微博视频--微博，转自--百家
    source_lis = soup.find_all(text=re.compile(r"来源|转发|转自|转发了(.*)"))
    logger.info(f"初次检查content内容结果是：{source_lis}")
    source_str = "".join(source_lis)
    if len(source_lis) > 0 and "转发收藏" in source_str:  # 普通微博
        source_lis = re.findall(r"（(.*)）", soup.get_text())
        source_str = "".join(source_lis)
        logger.info(f"第二次检查`转发收藏`结果是：{source_lis}")
    elif len(source_lis) > 0 and "转发了" in source_str:
        source_lis = re.findall(r"转发了\s+(.*)\s+的微博", soup.get_text())
        source_str = "".join(source_lis)
    # elif len(source_lis) == 0 and "据@" in soup.get_text():        # 普通微博
    #     source_lis = soup.find_all(text=re.compile(r"@(.*)"))
    #     source_str = "".join(source_lis)
    #     logger.info(f"第三次检查`据@`结果是：{source_lis}")
    source_str = re.sub(r".*[来源|转发|转自][:|：]", "", source_str)
    logger.info(f"确定是否原创的最终结果是：{source_str}")
    return source_str


def result_to_tree(source_detail, result, logger):
    parentId = ""
    # 先判定有没有上级，就是根级目录
    root_dict = [{"name": i["accountName"], "value": i["_id"], "parentId": parentId} for i in result["list"]
                 if source_detail["source"] == i["accountName"]]
    if root_dict:
        parentId = root_dict[0]["value"]
    # print(root_dict)
    logger.info(f"根级目录为：{root_dict}")
    # 同级目录
    sibling_dict = []
    if root_dict:
        sibling_dict = [{"name": i["accountName"], "value": i["_id"], "parentId": parentId} for i in result["list"]
                        if i["accountName"] == root_dict[0]["value"]]
    # 待验证作品同为同级目录
    sibling_dict.append({"name": source_detail["accountName"], "value": source_detail["_id"], "parentId": parentId})
    # print(sibling_dict)
    logger.info(f"同级目录是：{sibling_dict}")
    # 子级目录
    children_dict = [{"name": i["accountName"], "value": i["_id"], "parentId": source_detail["_id"]} for i in
                     result["list"] if source_detail["accountName"] == i["source"]]
    # print(children_dict)
    # 判断子级下目录有没有下家
    grandson_dict = []
    if children_dict:
        for children in children_dict:
            grandson = [{"name": i["accountName"], "value": i["_id"], "parentId": children["value"]} for i in
                        result["list"] if children["name"] == i["source"]]
            grandson_dict += grandson
    # print(grandson_dict)
    logger.info(f"孙子级目录为：{grandson_dict}")
    # 判断孙子级目录下有没有下家
    great_grandson_dict = []
    if grandson_dict:
        for grandson in grandson_dict:
            great_grandson = [{"name": i["accountName"], "value": i["_id"], "parentId": grandson["value"]} for i in
                              result["list"] if grandson["name"] == i["source"]]
            great_grandson_dict += great_grandson
    # print(great_grandson_dict)
    logger.info(f"曾孙子目录为：{great_grandson_dict}")
    tree_result = root_dict + sibling_dict + children_dict + grandson_dict
    # print(json.dumps(tree_result, indent=4, ensure_ascii=False))
    if len(tree_result) == 1 and tree_result[0]["name"] == source_detail["accountName"]:
        tree_result = []
    return tree_result


def result_to_tree_new(source_detail, result, logger):
    end_res_dict = list()  # 最终结果
    up_parent = []  # 祖父级作品
    parent_dict = []
    sibling_dict = []  # 同级作品
    children_dict = []  # 子级作品
    down_children = []
    if len(result["list"]) == 0:
        pass
    elif len(result["list"]) == 1:
        for i in result["list"]:
            item = dict()
            if source_detail["source"]:
                if i["accountName"]:
                    if source_detail["source"] in i["accountName"] \
                            or i["accountName"] in source_detail["source"]:
                        item = {"name": i["accountName"],
                                "type": [i["platformName"], i["platformType"]],
                                "source": i["source"], "parentId": "", "_id": i["_id"]}
                else:
                    if source_detail["source"] in i["platformName"] \
                            or i["platformName"] in source_detail["source"]:
                        item = {"name": i["accountName"],
                                "type": [i["platformName"], i["platformType"]],
                                "source": i["source"], "parentId": "", "_id": i["_id"]}
            if item:
                parent_dict.append(item)
        children_dict = []
        if len(parent_dict) == 0:
            for i in result["list"]:
                item = dict()
                if i["source"]:
                    if source_detail["accountName"]:
                        if i["source"] in source_detail["accountName"] \
                                or source_detail["accountName"] in i["source"]:
                            item = {"name": i["accountName"],
                                    "type": [i["platformName"], i["platformType"]],
                                    "source": i["source"], "parentId": source_detail["_id"],
                                    "_id": i["_id"]}
                    else:
                        if i["source"] in source_detail["platformName"] \
                                or source_detail["platformName"] in i["source"]:
                            item = {"name": i["accountName"],
                                    "type": [i["platformName"], i["platformType"]],
                                    "source": i["source"], "parentId": source_detail["_id"],
                                    "_id": i["_id"]}
                if item:
                    children_dict.append(item)
    else:
        if source_detail["source"]:
            for i in result["list"]:
                item = dict()
                if i["accountName"]:
                    if source_detail["source"] in i["accountName"] \
                            or i["accountName"] in source_detail["source"]:
                        item = {"name": i["accountName"],
                                "type": [i["platformName"], i["platformType"]],
                                "source": i["source"], "parentId": "", "_id": i["_id"]}
                else:
                    if source_detail["source"] in i["platformName"] \
                            or i["platformName"] in source_detail["source"]:
                        item = {"name": i["accountName"],
                                "type": [i["platformName"], i["platformType"]],
                                "source": i["source"], "parentId": "", "_id": i["_id"]}
                if item:
                    parent_dict.append(item)
        logger.info(f"第一次获取父级：{parent_dict}")
        source_detail_lis = []
        if len(parent_dict) != 0:
            # 如果确定待查作品的上级，那么为待查作品加parentID
            for p in range(len(parent_dict)):
                source_detail["parentId"] = parent_dict[p]["_id"]
                source_detail_lis.append(source_detail)
            # 如果确定待查作品的上级，那么再向上追溯该作品的祖父级
            up_parent = []
            for p in range(len(parent_dict)):
                if parent_dict[p]["source"]:
                    for i in result:
                        item = dict()
                        if i["accountName"]:
                            if parent_dict[p]["source"] in i["accountName"] or i["accountName"] in parent_dict[p]["source"]:
                                item = {"name": i["accountName"],
                                        "type": [i["platformName"], i["platformType"]],
                                        "source": i["source"], "_id": i["_id"], "parentId": ""}
                        else:
                            if parent_dict[p]["source"] in i["platformName"] \
                                    or i["platformName"] in parent_dict[p]["source"]:
                                item = {"name": i["accountName"],
                                        "type": [i["platformName"], i["platformType"]],
                                        "source": i["source"], "_id": i["_id"], "parentId": ""}
                        if item:
                            up_parent.append(item)
            logger.info(f"祖父级：{up_parent}")
            # 若有祖父级则在其下查询，看是否有父级同级作品
            if len(up_parent) != 0:
                parent_dict = []
                for u in range(len(up_parent)):
                    for i in result:
                        item = dict()
                        if i["source"]:
                            if up_parent[u]["name"]:
                                if i["source"] in up_parent[u]["name"] or up_parent[u]["name"] in i["source"]:
                                    item = {"name": i["accountName"],
                                            "type": [i["platformName"], i["platformType"]],
                                            "source": i["source"], "_id": i["_id"],
                                            "parentId": up_parent[u]["_id"]}
                            else:
                                if i["source"] in up_parent[u]["type"][0] or up_parent[u]["type"][0] in i["source"]:
                                    item = {"name": i["accountName"],
                                            "type": [i["platformName"], i["platformType"]],
                                            "source": i["source"], "_id": i["_id"],
                                            "parentId": up_parent[u]["_id"]}
                        if item:
                            parent_dict.append(item)
                logger.info(f"祖父级下与已确定父级的同级：{parent_dict}")
        # 确定同级作品
        if len(parent_dict) != 0:
            sibling_dict = []
            for p in range(len(parent_dict)):
                for i in result["list"]:
                    item = dict()
                    if i["similarSource"]:
                        if parent_dict[p]["name"]:
                            if i["similarSource"] in parent_dict[p]["name"] \
                                    or parent_dict[p]["name"] in i["similarSource"]:
                                item = {"name": i["similarAccountName"],
                                        "type": [i["similarPlatformName"], i["similarPlatformType"]],
                                        "source": i["similarSource"], "_id": i["similarId"],
                                        "parentId": parent_dict[p]["_id"]}
                        else:
                            if i["similarSource"] in parent_dict[p]["type"][0] or parent_dict[p]["type"][0] in i[
                                "similarSource"]:
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
        logger.info(f"同级：{sibling_dict}")
        # 子级目录
        children_dict = []
        if len(sibling_dict) != 0:
            for s in range(len(sibling_dict)):
                for i in result["list"]:
                    item = dict()
                    if i["source"]:
                        if sibling_dict[s]["name"]:
                            if i["source"] in sibling_dict[s]["name"] or sibling_dict[s]["name"] in i["source"]:
                                item = {"name": i["accountName"],
                                        "type": [i["platformName"], i["platformType"]],
                                        "source": i["source"], "_id": i["_id"],
                                        "parentId": sibling_dict[s]["_id"]}
                        else:
                            if i["source"] in sibling_dict[s]["type"][0] or sibling_dict[s]["type"][0] in i["source"]:
                                item = {"name": i["accountName"],
                                        "type": [i["platformName"], i["platformType"]],
                                        "source": i["source"], "_id": i["_id"],
                                        "parentId": sibling_dict[s]["_id"]}
                    if item:
                        children_dict.append(item)
        logger.info(f"子级：{children_dict}")
        # 子孙级目录
        down_children = []
        if len(children_dict) != 0:
            for c in range(len(children_dict)):
                for i in result["list"]:
                    item = dict()
                    if i["source"]:
                        if children_dict[c]["name"]:
                            if i["source"] in children_dict[c]["name"] or children_dict[c]["name"] in i["source"]:
                                item = {"name": i["accountName"],
                                        "type": [i["platformName"], i["platformType"]],
                                        "source": i["source"], "_id": i["_id"],
                                        "parentId": children_dict[c]["_id"]}
                        else:
                            if i["source"] in children_dict[c]["type"][0] or children_dict[c]["type"][0] in i["source"]:
                                item = {"name": i["accountName"],
                                        "type": [i["platformName"], i["platformType"]],
                                        "source": i["source"], "_id": i["_id"],
                                        "parentId": children_dict[c]["_id"]}
                    if item:
                        down_children.append(item)
    end_res_dict = up_parent + parent_dict + sibling_dict + children_dict + down_children
    if len(end_res_dict) == 1 and end_res_dict[0]["name"] == source_detail["accountName"]:
        logger.info(f"初步判断该作品{source_detail['_id']}无传播路径")
        end_res_dict = []
    return end_res_dict


class ArticleSaveAndDeleteEs:

    def __init__(self):
        self._es_conn = elasticsearch.Elasticsearch(**es_config)
        # 存放作品索引名。
        self._yym_discover_works_index = "yym_discover_works"
        # 存放待验证作品的临时索引名
        self._temporary_works_index = "dc_temporary_works_test"
        # 临时索引中的字段
        self.default_works_fields = {
            "_id": "",
            "status": 1,
            "platformWorksID": "",  # 平台作品ID，该平台唯一标识此作品的ID，
            "platformID": "",  # 【信源平台】索引里的【_id】
            "platformName": "微博",  # 【信源平台】索引里的【name】
            "platformType": 2,  # 平台类型，1微信、2微博、
            "accountID": "",  # 【信源账号】索引里的_id
            "accountName": "",  # 【信源账号】索引里的name
            # "avatar": avatar,
            "authors": "",
            "url": "",  # 作品链接，可以是分享链接
            "title": "",
            "titleWordsNum": "",  # 标题字数
            "content": "",  # 正文
            "contentWordsNum": "",  # 正文字数
            "html": "",  # 详情页全文，不用于检索
            "simhash": "",  # simhash值，可用于相似作品匹配，应当认为是基于纯文本计算得到的
            "contentType": -1,  # 作品类型，-1未知，1文字，2图文，3视频文，4纯长视频，5纯短视频，等
            "digest": "",  # 摘要，正文前200个中文（含标点符号）
            "source": "",  # 作品转载来源，爬虫直接得到
            "isOriginal": -1,  # 是否原创，-1未知，1是，0否，
            "isOriginalCompute": -1,
            "images": list(),
            "topics": list(),
            "covers": list(),
            "videos": list(),
            "audios": list(),
            "readNum": 0,  # 阅读数
            "likeNum": 0,  # 点赞数
            "commentNum": 0,
            "forwardNum": 0,
            "collectNum": 0,  # 收藏数
            "wxLookNum": 0,
            "wangYiJoinNum": 0,
            "updateParams": "",
            "pubTime": 0,
            "createTime": 0,
            "updateTime": 0,
        }

    def article_save_es(self, source_detail):
        """
        将待验证数据保存进入临时索引
        :param source_detail: 待验证文章详细
        :return:
        """
        assert source_detail and isinstance(source_detail, dict), "Error param, source_detail."
        temp_fields = dict()
        for key, value in source_detail.items():
            # None值不更新。
            if value is not None:
                temp_fields[key] = value
        fields = dict(self.default_works_fields, **temp_fields)
        fields.pop("_id")
        return self._es_conn.index(index=self._temporary_works_index, doc_type="_doc", body=fields,
                                   id=source_detail["_id"])

    def article_delete_es(self, source_detail):
        """
        验证完成之后将数据从临时索引中删除
        :param source_detail:
        :return:
        """
        return self._es_conn.delete(index=self._temporary_works_index, doc_type='_doc', id=source_detail["_id"])


if __name__ == '__main__':
    import json

    source_detail = {
        "nickName": "封面新闻",
        "avatar": "https://sf1-ttcdn-tos.pstatp.com/img/mosaic-legacy/9352/3387322036~120x256.image",
        "title": "成都最新通报",
        "readNum": 122,
        "playNum": 0,
        "likeNum": 3,
        "commentNum": 0,
        "pubTime": 1607353702,
        "isOriginal": 0,
        "isOriginalCompute": 0,
        "source": "新闻联播",
        "mediaName": "头条号",
        "url": "http://mp.weixin.qq.com/s?__biz=MzAwMzMxMDUxNg==&mid=2650203110&idx=1&sn=c663fe956a3e7829120f2ee6e392357a",
        "_id": "96192e1f81d21fd3adc6cd7dee4e6a59",
        "matchScore": 0.6413856891126476,
        "works_spread_route": {"name": "spread_route", "parent": "fcb1d646f7ea78e509ffc599cae431ff"}
    }
    # "works_spread_route": {"name": "spread_route", "parent": "a46edcc54b0e4055e729ae7eef7d0280"}
    es_conn = elasticsearch.Elasticsearch(**es_config)
    ins_id = source_detail.pop("_id")
    es_conn.index(index="dc_spread_works_route_test", doc_type="_doc", id=ins_id,
                  routing="fcb1d646f7ea78e509ffc599cae431ff", body=source_detail)
    # es_conn.delete(index="dc_spread_works_route_test", doc_type="_doc", id="96192e1f81d21fd3adc6cd7dee4e6a59")
