#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
保存公共参数。
# author: Trico
# date: 2020/12/24
# date: 2020/12/24
"""

import time
import json
import elasticsearch

from common_utils.utils import md5


def store_regions(es_conn):
    """
    保存地域信息。
    :return:
    """

    with open("/home/debugger/trico/big_data/big_data_platform/resources/region/regions.json", "rb") as fr:
        regions = fr.read().decode("utf-8")

    now = int(time.time() * 1000)
    name = "regions"
    field_id = md5(name)
    fields = dict()
    fields["status"] = 1
    fields["name"] = name
    fields["eName"] = name
    fields["describe"] = "地域信息，省、市等"
    fields["value"] = regions
    fields["createTime"] = now
    fields["updateTime"] = now
    res = es_conn.index(index="dc_public_params", doc_type="_doc", body=fields, id=field_id)
    print(f"{field_id}，{fields}，{res}")


def store_tags(es_conn):
    """
    保存分类信息。
    :return:
    """

    now = int(time.time() * 1000)
    name = "tags"
    field_id = md5(name)
    fields = dict()
    fields["status"] = 1
    fields["name"] = name
    fields["eName"] = name
    fields["describe"] = "标签（分类）信息，【1、国际 2、体育 3、娱乐 4、社会 5、财经 6、时事 7、科技 8、情感 " \
                         "9、汽车 10、教育 11、时尚 12、游戏 13、军事 14、旅游 15、美食 16、文化 " \
                         "17、健康养生 18、搞笑 19、家居 20、动漫 21、宠物 22、母婴育儿 23、星座运势 " \
                         "24、历史 25、音乐 26、综合】等"
    fields["value"] = json.dumps([
        "国际", "体育", "娱乐", "社会", "财经", "时事", "科技", "情感", "汽车",
        "教育", "时尚", "游戏", "军事", "旅游", "美食", "文化", "健康养生", "搞笑",
        "家居", "动漫", "宠物", "母婴育儿", "星座运势", "历史", "音乐", "综合"],
        separators=(",", ":")
    )
    fields["createTime"] = now
    fields["updateTime"] = now
    res = es_conn.index(index="dc_public_params", doc_type="_doc", body=fields, id=field_id)
    print(f"{field_id}，{fields}，{res}")


def store_classifications(es_conn):
    """
    保存作品归类信息。
    :return:
    """

    now = int(time.time() * 1000)
    name = "classifications"
    recommend_id = "rcmd"
    field_id = md5(name)
    fields = dict()
    fields["status"] = 1
    fields["name"] = name
    fields["eName"] = name
    fields["describe"] = "作品归类。新闻推荐，已知子类有：【党报头条——中央和省级党报头条新闻】，" \
                         "【政府头条——央级和省级政府网站的头条新闻】，" \
                         "【网媒头条——央级媒体和省级媒体的网站头条新闻】，" \
                         "【App头条——主流App首页要闻、热点、头条】，【微信头条——政府、官媒类（即微信数据-媒体类-中央和省级数据）微信公众号头条】，" \
                         "【时事要闻——对应百度的“时事”分类】，【法治社会——对应百度的“社会”分类】，" \
                         "【直击财经——对应百度的“财经”分类】，【体育纵横——对应百度的“体育”分类】，" \
                         "【成长路——对应百度的“教育”分类】，【文化聚焦——对应百度的“文化”分类】，" \
                         "【国际视野——对应百度的“国际”分类】，【科学探索——对应百度的“科技”分类】，" \
                         "【军事天地——对应百度的“军事”分类】，【健康养生——对应百度的“健康养生”分类】，" \
                         "【历史纵横——对应百度的“历史”分类】，【情感天地——对应百度的“情感”分类】，" \
                         "【时尚娱乐——对应百度的“娱乐”+“时尚”分类】，【车驰天下——对应百度的“汽车”分类】，" \
                         "【旅游小秘————对应百度的“旅游”分类】，【寻觅美食——对应百度的“美食”分类】，" \
                         "【家居快递————对应百度的“家居”分类】，【趣味搞笑——对应百度的“搞笑”分类】，" \
                         "【宅之动漫——对应百度的“动漫”分类】，【宠物专栏——对应百度的“宠物”分类】，" \
                         "【母婴育儿——对应百度的“母婴育儿”分类】，【星座运势——对应百度的“星座运势”分类】，" \
                         "【音乐新闻——对应百度的“音乐”分类】，【游戏天地——对应百度的“游戏”分类】，" \
                         "【综合资讯——对应百度的“综合”分类】等"
    fields["createTime"] = now
    fields["updateTime"] = now

    children = [
        "党报头条——中央和省级党报头条新闻", "政府头条——央级和省级政府网站的头条新闻",
        "网媒头条——央级媒体和省级媒体的网站头条新闻",
        "App头条——主流App首页要闻、热点、头条", "微信头条——政府、官媒类（即微信数据-媒体类-中央和省级数据）微信公众号头条",
        "时事要闻——对应百度的“时事”分类", "法治社会——对应百度的“社会”分类",
        "直击财经——对应百度的“财经”分类", "体育纵横——对应百度的“体育”分类",
        "成长路——对应百度的“教育”分类", "文化聚焦——对应百度的“文化”分类",
        "国际视野——对应百度的“国际”分类", "科学探索——对应百度的“科技”分类",
        "军事天地——对应百度的“军事”分类", "健康养生——对应百度的“健康养生”分类",
        "历史纵横——对应百度的“历史”分类", "情感天地——对应百度的“情感”分类",
        "时尚娱乐——对应百度的“娱乐”+“时尚”分类", "车驰天下——对应百度的“汽车”分类",
        "旅游小秘————对应百度的“旅游”分类", "寻觅美食——对应百度的“美食”分类",
        "家居快递————对应百度的“家居”分类", "趣味搞笑——对应百度的“搞笑”分类",
        "宅之动漫——对应百度的“动漫”分类", "宠物专栏——对应百度的“宠物”分类",
        "母婴育儿——对应百度的“母婴育儿”分类", "星座运势——对应百度的“星座运势”分类",
        "音乐新闻——对应百度的“音乐”分类", "游戏天地——对应百度的“游戏”分类",
        "综合资讯——对应百度的“综合”分类"
    ]
    values = list()
    for i, child in enumerate(children, start=1):
        sub_field_id = f"{recommend_id}_{i}"
        sub_fields = dict(id=sub_field_id)
        if "—" in child:
            name = child.split("—")[0]
        else:
            name = child
        sub_fields["name"] = name
        sub_fields["order"] = i
        sub_fields["describe"] = child
        values.append(sub_fields)
    fields["value"] = json.dumps(values, separators=(",", ":"))

    res = es_conn.index(index="dc_public_params", doc_type="_doc", body=fields, id=field_id)
    print(f"{field_id}，{fields}，{res}")


def store_baidu_tags_classifications_map(es_conn):
    """
    保存百度作品分类和作品归类的映射。
    :return:
    """

    now = int(time.time() * 1000)
    name = "baidu_tags_to_classifications_map"
    field_id = md5(name)
    fields = dict()
    fields["status"] = 1
    fields["name"] = name
    fields["eName"] = name
    fields["describe"] = "百度作品分类和作品归类的映射"
    fields["createTime"] = now
    fields["updateTime"] = now

    tags_classifications_map = dict(
        实事=dict(id="rcmd_6", name="时事要闻"),
        社会=dict(id="rcmd_7", name="法治社会"),
        财经=dict(id="rcmd_8", name="直击财经"),
        体育=dict(id="rcmd_9", name="体育纵横"),
        教育=dict(id="rcmd_10", name="成长路"),
        文化=dict(id="rcmd_11", name="文化聚焦"),
        国际=dict(id="rcmd_12", name="国际视野"),
        科技=dict(id="rcmd_13", name="科学探索"),
        军事=dict(id="rcmd_14", name="军事天地"),
        健康养生=dict(id="rcmd_15", name="健康养生"),
        历史=dict(id="rcmd_16", name="历史纵横"),
        情感=dict(id="rcmd_17", name="情感天地"),
        娱乐=dict(id="rcmd_18", name="时尚娱乐"),
        时尚=dict(id="rcmd_18", name="时尚娱乐"),
        汽车=dict(id="rcmd_19", name="车驰天下"),
        旅游=dict(id="rcmd_20", name="旅游小秘"),
        美食=dict(id="rcmd_21", name="寻觅美食"),
        家居=dict(id="rcmd_22", name="家居快递"),
        搞笑=dict(id="rcmd_23", name="趣味搞笑"),
        动漫=dict(id="rcmd_24", name="宅之动漫"),
        宠物=dict(id="rcmd_25", name="宠物专栏"),
        母婴育儿=dict(id="rcmd_26", name="母婴育儿"),
        星座运势=dict(id="rcmd_27", name="星座运势"),
        音乐=dict(id="rcmd_28", name="音乐新闻"),
        游戏=dict(id="rcmd_29", name="游戏天地"),
        综合=dict(id="rcmd_30", name="综合资讯"),
    )
    fields["value"] = json.dumps(tags_classifications_map, separators=(",", ":"))

    res = es_conn.index(index="dc_public_params", doc_type="_doc", body=fields, id=field_id)
    print(f"{field_id}，{fields}，{res}")


def run_store():
    # 入口。

    es_hosts = [dict(host="192.168.16.21", port=9200)]
    es_conn = elasticsearch.Elasticsearch(hosts=es_hosts)

    # 保存地域信息。
    # store_regions(es_conn)

    # 保存分类信息。
    # store_tags(es_conn)

    # 保存作品归类信息。
    store_classifications(es_conn)

    # 保存百度作品分类和作品归类的映射。
    # store_baidu_tags_classifications_map(es_conn)


if __name__ == '__main__':
    run_store()
