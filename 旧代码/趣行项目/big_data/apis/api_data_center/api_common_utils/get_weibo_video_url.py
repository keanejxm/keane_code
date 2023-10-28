# -*- coding:utf-8 -*-
"""
通过微博的视频id获取微博视频临时链接
author:keane
datatime:2020/11/7
"""

import json
import re
import time
import requests


class GetWeiboVideoUrl(object):
    """
    通过微博的视频id获取微博视频临时链接
    """

    @staticmethod
    def get_weibo_video_url_old(url):
        """
        通过微博的视频id获取微博视频临时链接
        :return:
        """

        try:
            video_ids = re.findall(r'object_id=([\d:]+)', url)  # 在url中获取video_id
            if video_ids:
                video_id = video_ids[0]
                url = "https://weibo.cn/aj/video/getdashinfo?"
                headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                  '(KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
                }
                data = {
                    'ajwvr': '6',
                    'media_ids': video_id,
                    '__rnd': str(int(time.time() * 1000))
                }
                video_url_res = requests.get(url, headers=headers, params=data).text
                try:
                    video_url_json = json.loads(video_url_res)
                    video_url = video_url_json['data']['list'][0]['details'][0]['play_info']['url']
                    url = video_url
                except Exception as a:
                    print(a, '获取视频文件失败')
        finally:
            return url

    @staticmethod
    def get_weibo_video_url(url):
        """
        通过微博的视频id获取微博视频临时链接
        :return:
        """

        try:
            # 参数验证。
            assert "m.weibo.cn/s/video/show" in url, f"url未识别，{url}"
            # 匹配出视频ID。
            video_ids = re.findall(r'object_id=([\d:]+)', url)  # 在url中获取video_id
            if video_ids:
                vid_url = "https://m.weibo.cn/s/video/object?object_id=" + video_ids[0]
                headers = {
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/71.0.3578.98 Safari/537.36",
                }
                resp = requests.get(vid_url, headers=headers)
                resp_json = json.loads(resp.content)
                # 封面图。
                # video_img = resp_json["data"]["object"]["image"]["url"]  # 视频封面连接
                url_part = resp_json["data"]["object"]["stream"]
                if "hd_url" in url_part:
                    video_url = str(url_part["hd_url"]).strip()  # 视频连接
                elif "url" in url_part:
                    video_url = str(url_part["url"]).strip()
                else:
                    return url

                assert video_url, f"video_url未识别，{video_url}"
                url = video_url
        finally:
            return url


def test():
    url = GetWeiboVideoUrl.get_weibo_video_url("https://m.weibo.cn/s/video/show?object_id=1034:4568151715938320")
    print(url)


if __name__ == '__main__':
    test()
