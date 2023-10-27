# -*- coding:utf-8 -*-
"""

# author: albert
# date: 2020/12/2
# update: 2020/12/2
"""
import datetime
import hashlib
import json
# import logging as logger
import random
import re
import sys
import time
import traceback

import elasticsearch
import pymysql
import requests
from bs4 import BeautifulSoup
from lxml import etree, html
from api_common_utils.base_data import *

from api_common_utils.proxy import get_abuyun_proxies
from api_common_utils.text_processing_tools import text_remover_html_tag

from api.config import es_config, wechat_random_great_keys_api_url


def get_wx_great_key():
    """
    获取微信万能key，采集用。
    :return:
    """
    resp = requests.get(wechat_random_great_keys_api_url, timeout=10)
    resp_data = json.loads(resp.content)
    return resp_data["data"]["wxKeyPair"]


class WeChatAccountSpider(object):
    """
    采集微信公众号账号信息及作品。
    """

    def __init__(self, logger):
        # 日志对象。
        self._logger = logger
        self._uin, self._key = get_wx_great_key()
        # 会话对象，采集用。
        self._session = requests.Session()
        # 请求头。
        request_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 '
                          'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat',
            'Host': 'mp.weixin.qq.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4'
        }
        self._session.headers = request_headers
        # 配置代理。
        self._session.proxies = get_abuyun_proxies()
        # 超时时间。
        self._timeout = 30
        self.platformType = 1
        self.es_conn = elasticsearch.Elasticsearch(**es_config)


    @staticmethod
    def md5(unicode_str, charset="UTF-8"):
        """
        字符串转md5格式。
        :return:
        """
        _md5 = hashlib.md5()
        _md5.update(unicode_str.encode(charset))
        return _md5.hexdigest()

    def works_statistics_spider(self, biz, mid, sn, idx):
        """
        获取微信作品的阅读数、点赞数、在看数等信息。
        :return:
        """

        # 参数验证。
        assert biz and isinstance(biz, str), "Error param, biz."
        assert mid and isinstance(mid, str), "Error param, mid."
        assert sn and isinstance(sn, str), "Error param, sn."
        assert isinstance(idx, (str, int)), "Error param, idx."

        url = f"https://mp.weixin.qq.com/mp/getappmsgext?uin={self._uin}&key={self._key}"
        datas = {
            "__biz": biz,
            "appmsg_type": "9",
            "mid": str(mid),
            "sn": str(sn),
            "idx": str(idx),
            "is_only_read": 1,
        }
        resp = json.loads(self._session.post(
            url, data=datas, timeout=self._timeout
        ).text)
        if "appmsgstat" in resp and resp["appmsgstat"]:
            work = dict()
            work["readNum"] = resp["appmsgstat"]["read_num"]  # 阅读量
            work["wxLookNum"] = resp["appmsgstat"]["like_num"]  # 在看量
            work["likeNum"] = resp["appmsgstat"]["old_like_num"]  # 点赞
            return work
        else:
            raise ValueError(f"Failed to fetch WeChat readNum, '{resp}'")

    def account_spider(self, acoount_data):
        """
        采集微信账号信息。
        :param biz: 微信biz。
        :param account_type: 账户类型：1运营，2关注，3热门作品。
        :return:
        """
        biz = acoount_data["platformAccountID"]
        # 链接。
        url = f'https://mp.weixin.qq.com/mp/profile_ext?' \
              f'action=home&__biz={biz}&scene=124&uin={self._uin}&key={self._key}&devicetype=Windows+10+x64' \
              f'&version=62090529&lang=zh_CN&a8scene=7' \
              f'&pass_ticket=LzHRlFa10pD7fnwX8qvHRrxq0LSV4FP3v4aPSlM108%2FErCDjiq7utvkYLNQZ0beQ&winzoom=1'
        # 获取结果。
        res = self._session.get(url, timeout=self._timeout).text
        introduction = re.findall(r'<p class="profile_desc">(.*?)</p>', res.replace('\n', ''))[0].replace(' ', '')
        avatar = re.findall('var headimg = "(.*?)"', res)[0]
        acoount_data["introduction"] = introduction
        acoount_data["avatar"] = avatar
        acoount_data["url"] = url
        return acoount_data

    def _video_parser(self, title, resp_text):
        """
        解析视频信息。
        :param title: 标题。
        :param resp_text: 响应体。
        :return:
        """

        # 检查详情页中是否有视频，有的话就整合成video标签。
        video_url = video_poster = video_height = video_width = video_size = video_duration = None
        if '<div class="js_video_channel_container">' in resp_text:
            # 先定位到js代码块。
            """
            请求地址：
            http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&amp;mid=2656998908&amp;idx=1&amp;sn=08a0961e727d25a6fef3830a84b2e31e&amp;chksm=7a64681a4d13e10c5edcd6506995bae2dabd8e8d5bbda7ddd0f2cfdeccdcdfcaee1a13e4b99d&amp;scene=27#wechat_redirect
            ...
            {
                  duration_ms: "77376" * 1 || 0,
                  filesize: "15832513" * 1 || 0,
                  format_id: "10002" * 1 || 0,
                  height: "1080" * 1 || 0,
                  url: "http://mpvideo.qpic.cn/0bf2jmbaqaactmaowovfsfpves6dbbfqecaa.f10002.mp4?dis_k=5ad14717121563db6b782b6422d32300\x26amp;dis_t=1604914654",
                  video_quality_level: "3" * 1 || 0,
                  video_quality_wording: "超清",
                  width: "1920" * 1 || 0
            }
            ...
            window.__mpVideoCoverUrl = "http://mmbiz.qpic.cn/mmbiz_jpg/oq1PymRl9D4WhSxsEiahUJRicHIvMgH5RjtfcPGubMxVrdbDn31rz7u6c08xpaN2YstgPcV73TZRCnHuJia63Jic0w/0?wx_fmt=jpeg";
            """
            # 视频信息。
            video_blocks = re.findall(
                r'{[^}]+?url:\s*"https?://mpvideo\.qpic\.cn/[^"]+",[^}]+?video_quality_level[^}]+?}',
                resp_text
            )
            if video_blocks:
                # 遍历视频js代码块，一般按清晰度高到低。
                for video_block in video_blocks:
                    video_urls = re.findall(r'url: "(https?://mpvideo\.qpic\.cn/[^"]+)",', video_block)
                    if video_urls:
                        # 视频链接。
                        video_url = str(video_urls[0]).strip()
                        video_url = video_url.replace("\\x26amp;", "&")
                        try:
                            # 视频其它信息。
                            video_height = re.findall(r'height: "(\d+)"', video_block)[0]
                            video_width = re.findall(r'width: "(\d+)"', video_block)[0]
                            video_size = re.findall(r'filesize: "(\d+)"', video_block)[0]
                            video_duration = re.findall(r'duration_ms: "(\d+)"', video_block)[0]
                            video_duration = int(int(video_duration) / 1000)
                        except Exception as e:
                            self._logger.debug(f"视频详细信息获取失败：{video_block}，{e}\n{traceback.format_exc()}")
                        break
            # 视频封面图。
            video_posters = re.findall(
                r'window.__mpVideoCoverUrl = "(https?://mmbiz.qpic.cn/mmbiz_jpg/[^"]+)";',
                resp_text
            )
            if video_posters:
                video_poster = str(video_posters[0]).strip()
        if video_url:
            video_string = f'<video ' \
                f'src="{video_url}" ' \
                f'poster="{video_poster}" ' \
                f'title="{title}" ' \
                f'height="{video_height if video_height is not None else ""}" ' \
                f'width="{video_width if video_width is not None else ""}" ' \
                f'size="{video_size if video_size is not None else ""}" ' \
                f'duration="{video_duration}" ' \
                f'controls="controls" />'
            return video_string
        else:
            return None

    def works_parser(self, biz, news_item, default_works, comm_msg_info, is_top):
        """
        解析作品字段。
        :param biz: 微信唯一ID。
        :param news_item: 作品内容。
        :param default_works: 作品的默认字段数据体。
        :param comm_msg_info: 通用数据体，一般包含datetime，代表微信消息的发出时间。
        :return:
        """

        works = dict(dict(), **default_works)
        works["title"] = news_item["title"].strip()  # 标题
        works["pubTime"] = int(comm_msg_info["datetime"]) * 1000 # 发布时间秒
        if news_item["cover"] != "":
            works["covers"] = [news_item["cover"], ]  # 文章封面图
            works["contentType"] = 2
        else:
            works["covers"] = []
            works["contentType"] = -1

        # 文章详情页链接。
        works["url"] = news_item["content_url"]  # 文章链接
        if works["url"] == "":
            raise ValueError("作品链接为空")

        # 获取文章详情页。
        resp = self._session.get(works["url"], timeout=self._timeout)
        resp.encoding = "utf-8"
        content_tree = etree.HTML(resp.text)
        works["content"] = html.tostring(
            content_tree.xpath("//div[@id='js_content']")[0],
            encoding='utf-8').decode("utf-8")
        works["content"] = str(works["content"]).strip()
        # works["html"] = resp.text

        # 来源：央视新闻</span>
        source = re.compile('来源：(.*?)<').findall(works["content"])
        if source:
            works["source"] = source[0]
            works["isOriginal"] = 0
            if source[0] == works["accountName"]:
                works["isOriginal"] = 1

        # 添加content处理。
        bs = BeautifulSoup(works["content"], "html.parser")
        # 处理图片。
        for img_tag in bs.find_all("img"):
            if "data-src" in img_tag.attrs and "src" not in img_tag.attrs:
                img_tag.attrs["src"] = img_tag.attrs["data-src"]
                works["content"] = str(bs)
        parse_html = etree.HTML(works["content"])
        works["images"] = parse_html.xpath('//img//@src')
        if not works["covers"]:
            if works["images"]:
                works["covers"] = works["images"][0]
        works["contentWordsNum"] = len(works["content"])
        # 清洗不可见的标签。
        target_element = bs.find(id="js_content")
        if target_element is not None:
            if "style" in target_element.attrs:
                target_element = bs.find(id="js_content")
                if "visibility: hidden" in target_element["style"]:
                    target_element["style"] = target_element["style"].replace("visibility: hidden", "")
                    works["content"] = str(bs)  # 正文
                    works['digest'] = works["content"][:200]

        # 检查详情页中是否有视频，有的话就整合成video标签。
        video_string = self._video_parser(works["title"], resp.text)
        if video_string:
            works["content"] = f"{video_string}\n{works['content']}"
        works['digest'] = text_remover_html_tag(works["content"])[:200] if text_remover_html_tag(works["content"])[:200] else ''
        # 文章定位信息。
        mid = re.findall(r'mid=(.*?)&', works["url"])[0]
        idx = re.findall(r'idx=(.*?)&', works["url"])[0]
        sn = re.findall(r'sn=(.*?)&', works["url"])[0]
        works['platformWorksID'] = 'mid:' + str(mid) + '_' + 'sn:' + str(sn) + '_' + 'idx:' + str(idx)
        # md5生成唯一id，平台类型+mid+sn+idx+账户类型。
        works['_id'] = self.md5(str(works['platformID']) + works['platformWorksID'])

        # 获取阅读数，点赞数等。
        try:
            return_dict = self.works_statistics_spider(biz, mid, sn, idx)
            works["readNum"] = return_dict["readNum"]  # 阅读量
            works["wxLookNum"] = return_dict["wxLookNum"]  # 在看量
            works["likeNum"] = return_dict["likeNum"]  # 点赞
        except Exception as e:
            self._logger.debug(f"{e}.")
            works["readNum"] = works["wxLookNum"] = works["likeNum"] = 0
        finally:
            time.sleep(0.5)

        # 更新参数。
        works['updateParams'] = json.dumps({
            'biz': biz, 'mid': str(mid), 'sn': str(sn), 'idx': str(idx)
        })
        # is_top
        works["isTop"] = is_top
        # works["spreadHI"] = round(random.uniform(1.1, 20.0), 1)
        # works["interactiveHI"] = round(random.uniform(1.1, 20.0), 1)
        # works["spreadHIIncreasement"] = round(random.uniform(1.1, 20.0), 1)
        return works

    def works_spider(self, account_dict):
        """
        微信作品采集。
        :param account_dict: 账号信息。
        :return:
        """
        biz = account_dict["platformAccountID"]
        # 列表页链接。
        count = 10
        url = f'https://mp.weixin.qq.com/mp/profile_ext?' \
              f'action=getmsg&__biz={biz}&f=json&offset=0&count={count}&uin={self._uin}&key={self._key}'
        retry_times = 2
        news_list = list()
        works_list = list()
        for retry in range(retry_times):
            # noinspection PyBroadException
            try:
                res = self._session.get(url, timeout=self._timeout)
                res_json = json.loads(res.text)
                news_list = json.loads(res_json['general_msg_list'])['list']
                time.sleep(1)
                if news_list:
                    break
            except Exception as e:
                if retry + 1 < retry_times:
                    self._logger.warning(f"Failed to fetch works, try again, '{e}'.")
                else:
                    self._logger.warning(f"Failed to fetch works, '{e}'.")
        if news_list:
            # 设定默认值。
            now = int(time.time() * 1000)
            default_work = dict(**DEFAULT_WORKS_FIELDS)
            default_work['platformID'] = account_dict["platformID"]
            default_work['platformName'] = account_dict["platformName"]
            default_work['platformType'] = self.platformType
            default_work['accountID'] = account_dict["_id"]
            default_work['accountName'] = account_dict["name"]
            default_work['authors'] = [account_dict['name']]
            default_work['createTime'] = now
            default_work['updateTime'] = now
            # 遍历每一条消息。
            for news in news_list:
                try:
                    time.sleep(1)
                    # 通用信息。
                    comm_msg_info = news["comm_msg_info"]
                    # 消息体。
                    news_item = news["app_msg_ext_info"]
                    # 首先解析消息主体。
                    is_top = -1
                    if '1_2_2' in account_dict["types"] or '1_2_3_3' in account_dict["types"] or '1_2_3_5' in account_dict:
                        if news_list.index(news) == 0:
                            default_work['classifications'] = ['rcmd_5']
                            is_top = 1
                    works = self.works_parser(biz, news_item, default_work, comm_msg_info, is_top)
                    works_list.append(works)

                    # 再解析多消息的拓展体。
                    if len(news_item["multi_app_msg_item_list"]) > 0:
                        for news_item in news_item["multi_app_msg_item_list"]:
                            try:
                                works = self.works_parser(biz, news_item, default_work, comm_msg_info, is_top)
                                works_list.append(works)
                            except Exception as e:
                                self._logger.warning(f"{account_dict['name']}, {e}\n{traceback.format_exc()}")
                except Exception as e:
                    self._logger.warning(f"{account_dict['name']}, {e}\n{traceback.format_exc()}")
        return works_list

    def save_author_es(self, account_dict):
        index_name = 'dc_accounts'
        field_id = account_dict.pop("_id")
        fields = account_dict
        res = self.es_conn.index(index=index_name, doc_type="_doc", body=fields, id=field_id)
        return res

    def save_work_es(self, works):
        for work in works:
            index_name = 'dc_works'
            field_id = work.pop("_id")
            if self.es_conn.exists(index=index_name, doc_type="_doc", id=field_id):
                self._logger.debug(f'微信公众号 - 《{work["title"]}》 已存在 ')
                continue
            fields = work
            res = self.es_conn.index(index=index_name, doc_type="_doc", body=fields, id=field_id)
            self._logger.debug(f'微信公众号 - 《{work["accountName"]}》 存储结果 为 {res}')
        return 'ok'

    def spider(self, acoount_data):
        """
        目前biz等参数为写死状态
        :return:
        """

        try:
            # 采集账号信息。
            try:
                account_dict = self.account_spider(acoount_data)
                works = self.works_spider(account_dict)
                # a_res = self.save_author_es(account_dict)
                # w_res = self.save_work_es(works)
                # self._logger.debug(a_res)
                # self._logger.debug(w_res)
            except Exception as e:
                self._logger.warning(f"{acoount_data['platformAccountID']}, {e}\n{traceback.format_exc()}")
                account_dict = works = {}

            # 返回结果。
            if account_dict and works:
                return {'code': 1, 'msg': 'ok', 'data': {'account': account_dict, 'works': works}}
            else:
                return {'code': 0, 'msg': 'failed'}
        except Exception as e:
            self._logger.warning(f"{e}\n{traceback.format_exc()}")
            return {'code': 0, 'msg': 'failed'}

    def update(self, json_data):
        """
        更新阅读量等内容
        :return:
        """

        # 根据平台作品id分离出mid，sn，idx
        params_dict = json.loads(json_data)

        # 获取统计数据。
        works = self.works_statistics_spider(**params_dict)
        works['updateTime'] = int(time.time())
        works['updateDateTime'] = works['updateTime'] * 1000
        return {'code': 1, 'msg': 'ok', 'data': {'works': [works]}}

    def run_from_platforms(self, task):
        query_body = {
          "size": 999999,
          "query": {
            "term": {
              "platformID": task["_id"]
            }
          }
        }
        account_res_list = []
        account_res = self.es_conn.search(index='dc_accounts', body=query_body)
        for res_data in account_res["hits"]["hits"]:
            res_data_dict = res_data["_source"]
            res_data_dict["_id"] = res_data["_id"]
            account_res_list.append(res_data_dict)
        for account_dict in account_res_list:
            res = self.spider(account_dict)

    def run_from_source_type(self, task):
        query_body = {
          "size": 999999,
          "query": {
            "term": {
              "parentID": {
                "value": task["parentID"]
              }
            }
          }
        }
        account_res_list = []
        account_res = self.es_conn.search(index='dc_source_types', body=query_body)
        for res_data in account_res["hits"]["hits"]:
            res_data_dict = res_data["_source"]
            res_data_dict["_id"] = res_data["_id"]
            account_res_list.append(res_data_dict)
        for account_dict in account_res_list:
            res = self.spider(account_dict)

    def run(self, task):
        """
        :param task:
        :return:
        """
        res = self.spider(task)
        if res["code"] == 1:
            result = {
                "code": 1,
                "msg": "success",
                "data": {
                    "account": res["data"]["account"],
                    "worksList": res["data"]["works"],
                }
            }
        else:
            result = {
                "code": 0,
                "msg": "failed",
            }
        # self._logger.debug(f'微信爬虫任务{task}的结果{res}')
        return result

    def fetch_batch(self, task):
        """
        :param task: 微信任务 - 从es中查询出来的任务 - 一个字典 需要包含_id
        :return:
        """
        # 1传递进来的任务可能是 整个平台的微信账号任务
        # 2可能是某个分类下的任务
        # 3可能是一个账号的任务
        # 对平台任务进行判断
        # if task["name"] == "微信公众号":
        #     self.run_from_platforms(task)
        # elif task.get("platformAccountID"):
        #     self.run(task)
        # else:
        #     self.run_from_source_type(task)
        self._logger.debug(f'微信爬虫任务{task}')
        return self.run(task)

    def fetch_yield(self, task):
        """
        :param task: 微信任务 - 从es中查询出来的任务 - 一个字典 需要包含_id
        :return:
        """
        self._logger.debug(f'微信爬虫任务{task}')
        res = self.run(task)
        if res["code"] == 1:
            yield dict(code=1, msg="success", data={"account": res["data"]["account"]})
            for r in res["data"]["worksList"]:
                yield dict(code=1, msg="success", data={"works": r})
        else:
            yield res


if __name__ == '__main__':
    # WeChatAccountSpider(logger).fetch_batch(tasks)
    pass

