# -*- encoding:utf-8 -*-
"""
@功能:百度、微博、抖音热搜
@AUTHOR：Keane
@文件名：hot_search.py
@时间：2020/12/10  8:58
"""
import json
import time
import random
import requests
from lxml import etree
from spiders.libs.spiders.hot_search.hot_data_create_es import WashData
import logging
from api.config import es_config
import elasticsearch


class HotSearch(object):
    def __init__(self, logger):
        self.logger = logger
        self._session = requests
        self.wash_data = WashData()
        self._es_conn = elasticsearch.Elasticsearch(**es_config)

    def bai_du_hot(self, hot_type):
        """
        百度热点
        :return:
        """
        headers = {
            "Cookie": "BIDUPSID=4D6141D8DB81FFFD3C1582DD03787DF1; PSTM=1607505964; BAIDUID=4D6141D8DB81FFFD57090A5602"
                      "FEF9B9:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; PSINO=1; bdshare_firstime=16075"
                      "61654232; H_PS_PSSID=1450_33102_33117_33058_31254_33098_33101_33211_26350_33199_33144_33147_22"
                      "158; BA_HECTOR=alal8l8g018k0124k41ft2sgg0q; Hm_lvt_79a0e9c520104773e13ccd072bc956aa=1607561654,"
                      "1607561751,1607561794; Hm_lpvt_79a0e9c520104773e13ccd072bc956aa=1607561813",
            "Host": "top.baidu.com",
            "Referer": "http://top.baidu.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87"
                          ".0.4280.88 Safari/537.36"
        }
        self._session.headers = headers
        if hot_type == "realtime":
            self.logger.info("开始获取实时热点排名")
            url = "http://top.baidu.com/buzz?b=1&fr=topindex"
        elif hot_type == "today":
            self.logger.info("开始获取今日热点排名")
            url = "http://top.baidu.com/buzz?b=341&fr=topindex"
        elif hot_type == "qiri":
            self.logger.info("开始获取七日热点排名")
            url = "http://top.baidu.com/buzz?b=42&fr=topindex"  # 七日热点
        else:
            url = ""
            self.logger.info("没有此类型热点")
        res = self._session.get(url).text.encode('iso-8859-1').decode('gbk')
        html = etree.HTML(res)
        pai_mings = html.xpath('//table[@class = "list-table"]/tr/td[1]/span/text()')
        key_word_urls = html.xpath('//table[@class = "list-table"]/tr/td[2]/a[1]/@href')
        key_word_titles = html.xpath('//table[@class = "list-table"]/tr/td[2]/a[1]/text()')
        zhi_shus = html.xpath('//table[@class = "list-table"]/tr/td[4]/span/text()')
        hot_news_total = []
        for index in range(len(pai_mings)):
            pai_ming = pai_mings[index]
            key_word_url = key_word_urls[index]
            key_word_title = key_word_titles[index]
            zhi_shu = zhi_shus[index]
            hot_news = {
                "serial_num": pai_ming,
                "news_name": key_word_title,
                "news_url": key_word_url,
                "updatetime": int(time.time() * 1000),
                "search_exponent": zhi_shu,
                "total": len(key_word_titles)
            }
            hot_news_total.append(hot_news)
        print(hot_news_total)
        platform = 1
        fields = self.wash_data.wash_hot_search_data(hot_news_total, platform)
        yield fields
        # res = self.create_es.api_create_articel(hot_news_total,platform)
        # print(res)

    def weibo_hot(self, hot_type):
        headers = {
            "Cookie": "SUB=_2AkMojXXPf8NxqwJRmP4RxWzja4R0ywnEieKe0YQUJRMxHRl-yT9kqhAttRB6Aw1bIEMzoCBt5KmeQdtExZOm855C"
                      "5vVY; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWp_.dnZRG9.Vy5hIKpF.MN; login_sid_t=960efedb5b613"
                      "f9d6d4a3a64f218375e; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; Apache=563869493296"
                      "1.25.1607596796079; SINAGLOBAL=5638694932961.25.1607596796079; ULV=1607596796084:1:1:1:56386949"
                      "32961.25.1607596796079:; UOR=,,www.baidu.com; WBStorage=8daec78e6a891122|undefined",
            "Host": "s.weibo.com",
            "Referer": "https://s.weibo.com/top/summary?cate=socialevent",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87."
                          "0.4280.88 Safari/537.36"
        }
        self._session.headers = headers
        if hot_type == "hot_search":
            self.logger.info(f"开始采集微博热搜榜")
            url = "https://s.weibo.com/top/summary?cate=realtimehot"
        elif hot_type == "emport_news":
            self.logger.info("开始采集微博要闻榜")
            url = "https://s.weibo.com/top/summary?cate=socialevent"
        else:
            url = ""
            self.logger.info("没有此类型")

        res = self._session.get(url).text
        html = etree.HTML(res)
        if hot_type == "hot_search":
            serial_nums = html.xpath("//div[@id='pl_top_realtimehot']/table/tbody/tr/td[1]/text()")
            search_exponents = html.xpath("//div[@id='pl_top_realtimehot']/table/tbody/tr/td[2]/span/text()")
            news_urls = html.xpath("//div[@id='pl_top_realtimehot']/table/tbody/tr/td[2]/a/@href")
            news_names = html.xpath("//div[@id='pl_top_realtimehot']/table/tbody/tr/td[2]/a/text()")
            for index in range(len(news_urls)):
                if index == 0:
                    serial_num = "置顶"
                    search_exponent = ""
                else:
                    serial_num = serial_nums[index - 1]
                    search_exponent = search_exponents[index - 1]
                news_url = "https://s.weibo.com/" + news_urls[index]
                news_name = news_names[index]
                hot_news = {
                    "serial_num": serial_num,
                    "news_name": news_name,
                    "news_url": news_url,
                    "updatetime": int(time.time() * 1000),
                    "search_exponent": search_exponent,
                    "total": len(news_names)
                }
                print(json.dumps(hot_news, indent=4, ensure_ascii=False))
        elif hot_type == "emport_news":
            news_urls = html.xpath("//div[@id='pl_top_realtimehot']/table/tbody/tr/td[2]/a/@href")
            news_names = html.xpath("//div[@id='pl_top_realtimehot']/table/tbody/tr/td[2]/a/text()")
            hot_news_total = list()
            for index in range(len(news_urls)):
                news_url = "https://s.weibo.com/" + news_urls[index]
                news_name = news_names[index]
                hot_news = {
                    "serial_num": index + 1,
                    "news_name": news_name,
                    "news_url": news_url,
                    "updatetime": int(time.time() * 1000),
                    "total": len(news_names)
                }
                hot_news_total.append(hot_news)
                # print(json.dumps(hot_news, indent = 4, ensure_ascii = False))
            platform = 2
            fields = self.wash_data.wash_hot_search_data(hot_news_total, platform)
            yield fields

    @staticmethod
    def _random_mac_address():
        """
        产生随机mac地址
        :return:
        """
        mac_list = []
        for i in range(1, 7):
            mac_str = "".join(random.sample("0123456789abcdef", 2))
            mac_list.append(mac_str)
        rand_mac = ":".join(mac_list)
        return rand_mac

    def douyin_hot(self):
        self.logger.info("开始采集抖音热搜榜")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
        }
        mac_address = self._random_mac_address()
        header_data = {
            "detail_list": 1,
            "mac_address": mac_address,
            "source": 0,
            "current_word": "",
            "words_in_panel": "",
            "trend_entry_word": "",
            "board_type": "2",
            "board_sub_type": "4",
            "need_board_tab": "false",
            "hotlist_param": "",
            "os_api": 23,
            "device_type": "MI 5s",
            "ssmix": "a",
            "manifest_version_code": 14000,
            "dpi": 270,
            "uuid": 300000000122678,
            "app_name": "aweme",
            "version_name": "14.0.0",
            "ts": int(time.time()),
            "cpu_support64": "false",
            "app_type": "normal",
            "appTheme": "dark",
            "ac": "wifi",
            "host_abi": "armeabi-v7a",
            "update_version_code": 14000200,
            "channel": "douyin-huidu-gw-test-1014",
            "_rticket": int(time.time() * 1000),
            "device_platform": "android",
            "iid": 298711487880061,
            "version_code": 14000,
            "cdid": "b4f177e8-f627-49d9-bba5-b46af19e0b27",
            "openudid": "f3455278353c2b73",
            "device_id": 2251444136982392,
            "resolution": "810*1440",
            "os_version": "6.0.1",
            "language": "zh",
            "device_brand": "Xiaomi",
            "aid": 1128,
            "mcc_mnc": 46007,
        }
        url = "https://aweme.snssdk.com/aweme/v1/hot/search/list/?"
        resp = self._session.get(url, params=header_data, headers=headers).text
        resp = json.loads(resp)
        hot_news_total = list()
        for word in resp["data"]["word_list"]:
            serial_nums = word["position"]
            search_exponents = word["hot_value"]
            news_names = word["word"]
            if "position" in word.keys():
                dd = {
                    "offset": 0,
                    "is_from_live": 0,
                    "is_trending": 0,
                    "source": "trending_page",
                    "room_id": "",
                    "count": 5,  # 调整为5个
                    "is_ad": 0,
                    "hotword": word["word"],
                    "action_type": "click"
                }
                header_data.update(dd)
                work_url = "https://api3-normal-c-lq.amemv.com/aweme/v1/hot/search/video/list/"
                videoresp = self._session.get(work_url, params=header_data, headers=headers).text
                videoresp = json.loads(videoresp)
                aweme_lists = videoresp["aweme_list"]
                videos = list()
                for aweme_list in aweme_lists:
                    try:
                        video = aweme_list["share_url"]
                        videos.append(video)
                    except Exception as e:
                        self.logger.info(f"{e},{aweme_list}")
                if not videos:
                    print(aweme_lists)
                if videos:
                    hot_news = {
                        "serial_num": serial_nums,
                        "news_name": news_names,
                        "news_url": videos[0],
                        "updatetime": int(time.time() * 1000),
                        "search_exponent": search_exponents,
                        "total": len(resp["data"]["word_list"])
                    }
                    hot_news_total.append(hot_news)
        platform = 3
        fields = self.wash_data.wash_hot_search_data(hot_news_total, platform)
        yield fields

    def search_keywords(self):
        """
        从dc_works获取关键词数据
        """
        now_ms = int(time.time() * 1000)
        must_list = [
            {"range": {"pubTime": {
                "gte": now_ms - 24 * 60 * 60 * 1000,
                # "gte": int(time.time()*1000),
                "lte": now_ms
            }}}]
        body = {
            "_source": ["keywords"],
            "query": {
                "bool": {"must": must_list},
                # "match_all":{}
            },
        }
        res1 = self._es_conn.search(index="dc_works", request_timeout=3600, body=body)
        return res1

    def word_fre(self):
        keywords_list = self.search_keywords()
        keywords_list = keywords_list["hits"]["hits"]
        words_list = list()
        for keywords in keywords_list:
            words_list.extend(keywords["_source"]["keywords"])
        words_dict = {x: words_list.count(x) for x in set(words_list)}
        words_list = sorted(words_dict.items(), key=lambda item: item[1], reverse=True)
        words_list = words_list[0:30]
        words = list()
        for word in words_list:
            a = dict()
            a[word[0]] = word[1]
            words.append(a)
        if words:
            res = WashData().wash_hot_search_data(words, "4")
            yield res
        else:
            self.logger.debug("数据为空")

    def run(self):
        # hot_types = ["realtime", "today", "qiri"]
        hot_types = ["realtime"]
        for hot_type in hot_types:
            self.bai_du_hot(hot_type)
        # hot_types = ["hot_search", "emport_news"]
        hot_types = ["emport_news"]
        for hot_type in hot_types:
            self.weibo_hot(hot_type)
        self.douyin_hot()

    def hot_batch(self):
        top_queries = list()
        for bai_du_data in self.bai_du_hot("realtime"):
            top_queries.append(bai_du_data)
        for wei_bo_data in self.weibo_hot("emport_news"):
            top_queries.append(wei_bo_data)
        for dou_yin_data in self.douyin_hot():
            top_queries.append(dou_yin_data)
        res = {"code": 1, "msg": "OK", "data": {"topQueries": top_queries}}
        yield res

    def hot_yield(self):
        top_queries = list()
        for bai_du_data in self.bai_du_hot("realtime"):
            top_queries.append(bai_du_data)
        for wei_bo_data in self.weibo_hot("emport_news"):
            top_queries.append(wei_bo_data)
        for dou_yin_data in self.douyin_hot():
            top_queries.append(dou_yin_data)
        for hot_word in self.word_fre():
            top_queries.append(hot_word)
        for top_query in top_queries:
            yield {"code": 1, "msg": "OK", "data": {"topQuery": top_query}}


if __name__ == '__main__':
    logger = logging
    hot_search = HotSearch(logger)
    for s in hot_search.hot_yield():
        print(s)
