# -*- coding:utf-8 -*-
"""
测试。
# author: Trico
# date: 2021/1/25
# update: 2021/1/25
"""


def compute_hi(works=None):
    # 测试。

    works = dict(
        platformType=4,
        readNum=12312,
        likeNum=12312,
        commentNum=12312,
        forwardNum=12312,
        collectNum=12312,
        wxLookNum=12312,
    )
    platform_type = works["platformType"]

    if platform_type in (1, 2, 3, 4, 7):
        read_num = works.get("readNum", 0)
        read_num = works.get("readNum", 0)
        like_num = works.get("likeNum", 0)
        comment_num = works.get("commentNum", 0)
        forward_num = works.get("forwardNum", 0)
        collect_num = works.get("collectNum", 0)
        wx_look_num = works.get("wxLookNum", 0)
        if platform_type == 4:
            read_a = (read_num * forward_num) + comment_num

    else:
        raise ValueError(f"未知参数，platformType：{platform_type}")


if __name__ == "__main__":
    compute_hi()
