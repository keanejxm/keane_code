# -*- coding:utf-8 -*-
"""
# project:大鱼号视频获取
# author: Neil
# date: 2020/11/13

"""

import re
import json
import requests
from api_common_utils.proxy import get_abuyun_proxies
# 代理
a_proxies = get_abuyun_proxies()

class GetDaYuVideo:
    """
    获取大鱼号视频
    """
    @staticmethod
    # 大鱼视频解析
    def get_new_videos_url(url):
        """
        获取大鱼号视频连接
        :param wid: 文章id
        :param uid: 用户id
        :return:
        """

        try:
            wid = re.compile("wid=(.*?)uid").findall(url)[0]
            uid = re.compile("uid=(.*?)/").findall(url)[0]
            headers = {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-CN; LIO-AN00 Build/LIO-AN00)'
                                     ' AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.0.4.846 U3/0.8.0 '
                                     'Mobile Safari/534.30'}
            # 此链接为了获取token
            article_url = f"https://mparticle.uc.cn/article_org.html?uc_param_str=frdnsnpfvecpntnwprdssskt" \
                f"&wm_cid={wid}&wm_id={uid}"
            res = requests.get(url=article_url, proxies=a_proxies, headers=headers)
            token = requests.utils.dict_from_cookiejar(res.cookies)["vpstoken"]
            # 视频详情链接，为了获取视频ums_id
            d_url = f'https://ff.dayu.com/contents/{wid}?biz_id=1002&_fetch_author=1' \
                f'&_incr_fields=click1,click2,click3,click_total,play,like'
            response = requests.get(url=d_url, proxies=a_proxies, headers=headers)
            res_json = json.loads(response.text)['data']
            ums_id = ""
            if 'videos' in res_json['body']:
                for info in res_json['body']['videos']:
                    ums_id = info['ums_id']
            else:
                for info in res_json['body']['inner_videos']:
                    ums_id = info['ums_id']
            url = f'https://mparticle.uc.cn/api/vps?token={token}&ums_id={ums_id}&wm_cid={wid}' \
                f'&wm_id={uid}&resolution=high'
            video = requests.get(url=url, proxies=a_proxies, headers=headers).text
            video_json = json.loads(video)['data']
            video_url = video_json["url"]
            url = video_url
        except Exception as e:
            raise ValueError("请求失败")
        finally:
            return url
