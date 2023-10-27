#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
测试采集微博阅读数。
# author: Trico
# date: 2020.4.27
# update: 2020.4.27
"""

import json
import time
import random
import requests

from api_common_utils.proxy import get_abuyun_proxies


def get_wb_counts(wb_name, wb_mid):
    """
    获取某一条微博的统计数目。
    :param wb_name: 微博名称，例如：燕赵都市报冀东版官微。
    :param wb_mid: 10进制微博MID，例如：4498363854215590。
    :return:
    """

    # 参数验证。
    assert wb_name and isinstance(wb_name, str), "Error param, wb_name"
    assert wb_mid and isinstance(wb_mid, str), "Error param, wb_mid"

    request_headers = {
        "Host": "api.weibo.cn",
        "Connection": "Keep-Alive",
        "X-Sessionid": "f093ca26-156e-4433-8479-375428836411",
        "User-Agent": "vivo X7_5.1.1_weibo_10.4.2_android",
        "X-Validator": "Cz+zvAWM8h+mqxLrW9R8DPG3YnPL1h2aZRKA9ffuDSo=",
        "X-Log-Uid": "1030273000938",
        "Accept-Encoding": "gzip, deflate",
    }
    url_template = "https://api.weibo.cn/2/guest/statuses_extend?networktype=wifi&launchid=10000365--x" \
                   "&sensors_device_id=none&orifid=231619$$100303type=1&t=3$$100103type=1&q={wb_name}" \
                   "&t=1$$2302831623340585&uicode=10000002&status_height_scale=1.0&moduleID=705" \
                   "&checktoken=9e8c210c9bd8fb0e3e1bbadd96c81560&featurecode=10000085&wb_version=4402" \
                   "&lcardid=2310020003_hotweibo_wbcard&c=android&s=2ab5de05&ft=0&id={wb_mid}" \
                   "&ua=vivo-vivo X7__weibo__10.4.2__android__android5.1.1&wm=9856_0004" \
                   "&aid=01A-5tfkMJs_4lVp7yP7WS4BNa64BCvoBM8M9yuSNeap6wjdk." \
                   "&did=0634b1c284cb90befc6f8734a17492cdab7138a9&ext=rid:3_0_0_1413090909532629269_0_0_0" \
                   "&uid=1030273000938&v_f=2&v_p=82&from=10A4295010" \
                   "&gsid=_2AkMp-v-zf8NhqwJRm_gXy2jibI1-yQDEieKfpg5oJRM3HRl-" \
                   "wT9kqnMEtRV6AbbHYpaG-nhPTCl5hxW1T_IreIueGG5T" \
                   "&lang=zh_CN&lfid=2302831623340585&skin=default&oldwm=9856_0004&sflag=1&is_recom=-1" \
                   "&oriuicode=10000512_10000003_10000003_10000198&luicode=10000198&has_product=0&sensors_mark=0" \
                   "&android_id=4e653a56ed2bb5df&sensors_is_first_day=none"
    url = url_template.format(wb_name=wb_name, wb_mid=wb_mid)
    resp = requests.get(url, headers=request_headers, timeout=8, proxies=get_abuyun_proxies(), allow_redirects=False)
    # 强制暂停一段时间。
    time.sleep(random.random() + 1)
    assert resp.status_code == requests.codes.ok, "Failed to fetch response, code: {}, text: '{}'.".format(
        resp.status_code, resp.text
    )
    data = json.loads(resp.content)

    # 结果集。
    result = dict(
        wbName=wb_name,
        wbMid=wb_mid,
    )

    # 微博账号粉丝数。
    # noinspection PyBroadException
    try:
        fans_num = int(data["followers_count"])
        assert fans_num >= 0, "Error fans_num."
        result["fanNum"] = fans_num
    except Exception:
        pass

    # 微博账号关注数。
    # noinspection PyBroadException
    try:
        friends_num = int(data["friends_count"])
        assert friends_num >= 0, "Error friends_num."
        result["followNum"] = friends_num
    except Exception:
        pass

    # 微博视频观看数。
    # noinspection PyBroadException
    try:
        play_num = int(data["online_users_number"])
        assert play_num >= 0, "Error play_num."
        result["playNum"] = play_num
    except Exception:
        play_num = 0

    # 微博阅读数。
    # noinspection PyBroadException
    try:
        read_num = int(data["reads_count"])
        assert read_num >= 0, "Error read_num."
        result["readNum"] = read_num
    except Exception:
        if play_num > 0:
            result["readNum"] = play_num

    # 微博视频点赞数。
    # noinspection PyBroadException
    try:
        like_num = int(data["attitudes_count"])
        assert like_num >= 0, "Error like_num."
        result["likeNum"] = like_num
    except Exception:
        pass

    # 微博视频评论数。
    # noinspection PyBroadException
    try:
        comment_num = int(data["comments_count"])
        assert comment_num >= 0, "Error comment_num."
        result["commentNum"] = comment_num
    except Exception:
        pass

    # 微博视频转发数。
    # noinspection PyBroadException
    try:
        forward_num = int(data["reposts_count"])
        assert forward_num >= 0, "Error forward_num."
        result["forwardNum"] = forward_num
    except Exception:
        pass

    # 返回结果。
    return result


def test():
    # 测试入口。
    # res = get_wb_counts("文明冲浪指南", "4535984416889110")
    res = get_wb_counts("测试", "4550075315651515")
    print(res)


if __name__ == "__main__":
    test()
