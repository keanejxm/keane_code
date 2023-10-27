#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
获取公共参数。
# author: Trico
# date: 2021/1/18
# update: 2021/1/18
"""


def get_data_plural_singular_map(map_direction="p_s"):

    if map_direction == "p_s":
        # 复数与单数映射。
        _map = dict(
            platforms="platform",
            accounts="account",
            channels="channel",
            epaperLayouts="epaperLayout",
            topics="topic",
            worksList="works",
            forums="forum",
            forumDetails="forumDetail",
            topQueries="topQuery",
        )
    elif map_direction == "s_p":
        # 单数与复数映射。
        _map = dict(
            platform="platforms",
            account="accounts",
            channel="channels",
            epaperLayout="epaperLayouts",
            topic="topics",
            works="worksList",
            forums="forums",
            forumDetail="forumDetails",
            topQuery="topQueries",
        )
    else:
        raise ValueError(f"未知参数，map_direction：{map_direction}")

    return _map
