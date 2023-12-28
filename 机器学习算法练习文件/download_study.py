#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  download_study.py
:time  2023/11/20 16:35
:desc  
"""
import os.path
import random
import re
import time
from Crypto.Cipher import AES
import requests
import json
import http.client

# http.client.HTTPConnection._http_vsn = 10
# http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

cookie = "sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22E_bfvf43s%22%2C%22first_id%22%3A%2218acb2235051428-01acc60ebfbc938-26031d51-1327104-18acb223506b4e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfbG9naW5faWQiOiJFX2JmdmY0M3MiLCIkaWRlbnRpdHlfY29va2llX2lkIjoiMThhY2IyMjM1MDUxNDI4LTAxYWNjNjBlYmZiYzkzOC0yNjAzMWQ1MS0xMzI3MTA0LTE4YWNiMjIzNTA2YjRlIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22E_bfvf43s%22%7D%2C%22%24device_id%22%3A%2218acb2235051428-01acc60ebfbc938-26031d51-1327104-18acb223506b4e%22%7D; Hm_lvt_51179c297feac072ee8d3f66a55aa1bd=1700528241,1700700655,1700787621,1701067246; Hm_lpvt_51179c297feac072ee8d3f66a55aa1bd=1701067246; TMOOC-SESSION=b8b5f7e1fe0b40e3ab1d8a26af3df6ac; stuClaIdCookie=1033808; tesSessionId=b8b5f7e1fe0b40e3ab1d8a26af3df6ac; sessionid=b8b5f7e1fe0b40e3ab1d8a26af3df6ac|E_bfvf43s"

session = requests.Session()
session.cookies.update({"Cookie": cookie})


class DownloadVideo:
    def __init__(self):
        pass

    def headers(self):
        headers = {
            "Authorization": "b8b5f7e1fe0b40e3ab1d8a26af3df6ac|E_bfvf43s",
            "Origin": "https://tts10.tmooc.cn",
            "Referer": "https://tts10.tmooc.cn/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }
        return headers

    def get_channel(self):
        url = "https://ttsservice.tmooc.cn/tedu-student/v1/study-center/formal"
        headers = self.headers()
        res = session.get(url, headers=headers)
        res_json = json.loads(res.text)
        # print(res_json)
        # 解析数据
        big_stage_list = res_json["bigStageList"]
        for big_stage in big_stage_list:
            small_stage_list = big_stage["smallStageList"]
            big_stage_name = big_stage["bigStageName"]
            for small_stage in small_stage_list:
                day_stage_list = small_stage["dayStageList"]
                small_stage_name = small_stage["smallStageName"]
                for day_stage in day_stage_list:
                    live_or_video_list = day_stage["liveOrVideoList"]
                    day_stage_name = day_stage["knowledgeName"]
                    for live_or_video in live_or_video_list:
                        if "playbackMenuVideoId" in live_or_video:
                            playback_menu_video_id = live_or_video["playbackMenuVideoId"]
                            menu_video_name = live_or_video["menuVideoName"]
                            yield dict(bigStageName=big_stage_name,
                                       smallStageName=small_stage_name,
                                       dayStageName=day_stage_name,
                                       menuVideoName=menu_video_name,
                                       playbackMenuVideoId=playback_menu_video_id)

    def get_video_url(self, stage_info):
        playback_menu_video_id = stage_info["playbackMenuVideoId"]
        url = f"https://ttsservice.tmooc.cn/tedu-student/v1/video/find-playback-msg/{playback_menu_video_id}"
        headers = self.headers()
        res = session.get(url, headers=headers)
        res_json = json.loads(res.content)
        return res_json

    def get_ts_urls(self, url):
        headers = self.headers()
        res = session.get(url, headers=headers)
        res_text = res.text
        res_text_list = res_text.split("\n")
        ts_url_list = list()
        key_code = None
        for ln in res_text_list:
            if ln.startswith("https://c.it211.com.cn") and ln.endswith(".ts"):
                ts_url_list.append(ln)
            if ln.startswith("#EXT-X-KEY") and ln.endswith("key\""):
                time.sleep(1)
                key_url = re.findall("(https://c.it211.com.cn/.*key)", ln)
                key_url = key_url[0]
                headers = self.headers()
                key_code = session.get(key_url, headers=headers).content
        return ts_url_list, key_code

    # 下载ts文件
    def download_ts_file(self, video_url_info, url_list, key_code):
        # dict(bigStageName=big_stage_name,
        # smallStageName=small_stage_name,
        # dayStageName=day_stage_name,
        # menuVideoName=menu_video_name,
        # playbackMenuVideoId=playback_menu_video_id)
        big_stage_name = video_url_info["bigStageName"]
        # if big_stage_name in ["机器学习", "深度学习"]:
        small_stage_name = video_url_info["smallStageName"]
        day_stage_name = video_url_info["dayStageName"]
        menu_video_name = video_url_info["menuVideoName"]
        file_path = rf"F:\达内视频\{big_stage_name}\{small_stage_name}\{day_stage_name}"
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        for index, url in enumerate(url_list):
            try:
                print(f"共{len(url_list)}个：采集{big_stage_name}_{small_stage_name}_{menu_video_name}_{index}")
                # 判断文件中是否存在，存在跳过
                if os.path.exists(f"{file_path}/{menu_video_name}_{index}.ts"):
                    continue
                time.sleep(random.randint(0, 5))
                headers_1 = self.headers()
                headers_1["Accept-Encoding"] = "gzip, deflate, br"
                headers_1["Host"] = "c.it211.com.cn"
                # http.client.HTTPConnection._http_vsn = 10
                # http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
                res = session.get(url, headers=headers_1, stream=True)

                res_content = res.content
                # 解码
                aes = AES.new(key_code, AES.MODE_CBC, b"0000000000000000")
                with open(f"{file_path}/{menu_video_name}_{index}.ts", "wb") as f:
                    f.write(aes.decrypt(res_content))
                f.close()
            except Exception as e:
                print(e)

    def start(self):
        for stage_info in self.get_channel():
            try:
                video_url_info = self.get_video_url(stage_info)
                video_url = video_url_info["videoUrl"]
                video_urls, key_code = self.get_ts_urls(video_url)
                print(f"key_code:{key_code}")
                self.download_ts_file(stage_info, video_urls, key_code)
            except Exception as e:
                pass


if __name__ == '__main__':
    obj = DownloadVideo()
    obj.start()
