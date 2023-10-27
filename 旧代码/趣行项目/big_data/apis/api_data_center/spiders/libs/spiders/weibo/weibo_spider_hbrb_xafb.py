# -*- coding:utf-8 -*-
"""
中央厨房-稿库-微博展示。
微博爬虫。
河北日报微博爬虫；
雄安发布微博爬虫；
# author: Chris
# date: 2020/11/3
# update: 2020/11/3
"""

import re
import os
import requests
import datetime
import time
import json
from lxml import etree, html
import hashlib
import traceback
from urllib.parse import urljoin
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch


class WeiBoFetch(object):

    def __init__(self, cookies, uid):
        self._uid = uid
        self._cookies = cookies
        self._request_header = {
            "authority": "weibo.cn",
            "method": "GET",
            "scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;"
                      "q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cookie": self._cookies,
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/71.0.3578.98 Safari/537.36"
        }
        self._session = requests.Session()
        # 采集网站。
        self._site_url = "https://weibo.cn/"
        # 采集间隔时长。
        self._list_page_interval = 1.5
        # 超时时间
        self._timeout = 5
        # 时间数据。
        self._date_str = str(datetime.date.today())[:10]
        self._year = time.strftime('%Y', time.localtime(time.time()))
        """es索引、链接等"""
        self._es_conn = Elasticsearch("192.168.32.6:9200")
        self._es_index_name = "zycf_gk_wb"
        self._es_doc_type = "wbitem"
        """bos相关"""
        self.bucket_name = "python-spider"
        # 下载路径。
        self._work_path = os.path.dirname(os.path.realpath(__file__))
        self._download_path = f"{self._work_path}/download_files"
        os.makedirs(self._download_path, exist_ok=True)

        # 接口地址（python-spider服务器）。
        self._api = "http://192.168.32.5:8000"

    @staticmethod
    def _md5(_str, charset="UTF-8"):
        """
        计算字符串MD5加密值。
        :param _str: 字符串。
        :return:
        """
        md5 = hashlib.md5()
        md5.update(_str.encode(charset))
        return md5.hexdigest()

    def _get_wb_timestamp(self, time_str):
        """
        计算发布时间时间戳。
        :param time_str: 含有时间信息的字符串。
        :return:
        """

        # 提取时间。
        time_str_type = re.findall(r"来自.+", time_str)
        if time_str_type:
            time_str = time_str.replace(re.findall(r"来自.+", time_str)[0], "")
        else:
            time_str = time_str

        # 时间转换。
        if time_str.strip().startswith("今天"):
            time_str = time_str.replace("今天", "").strip()
            time_str = self._date_str + " " + time_str
            return int(time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M")))
        elif time_str.find("分钟前") != -1:
            minago = (int(re.findall(r'(\d+)分钟前', time_str)[0]))
            nowtime = (datetime.datetime.now() - datetime.timedelta(minutes=minago)).strftime("%Y-%m-%d %H:%M:%S")
            return int(time.mktime(time.strptime(nowtime, "%Y-%m-%d %H:%M:%S")))
        elif time_str.find("月") != -1:
            month = re.findall(r"(\d+)月(\d+)日(.+)", time_str)[0][0]
            day = re.findall(r"(\d+)月(\d+)日(.+)", time_str)[0][1]
            hour_minute = re.findall(r"(\d+)月(\d+)日(.+)", time_str)[0][2].strip()
            time_str = "{}-{}-{} {}".format(self._year, month, day, hour_minute)
            return int(time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M")))
        else:
            return int(time.mktime(time.strptime(time_str.strip(), "%Y-%m-%d %H:%M:%S")))

    @staticmethod
    def _find_sina_time(timestr):
        """
        时间工具函数。
        :param timestr: 时间字符串。
        :return:
        """

        # 如果发现微博中含有今天或分钟前则发布时间为今日
        if timestr.find("今天") != -1 or timestr.find("分钟前") != -1:
            public_time = str(datetime.date.today())[:10]
            return public_time
        if re.findall(r"\d+月\d+日", timestr):
            public_time = str(datetime.datetime.now().year) + \
                          re.findall(r"\d+月\d+日", timestr)[0].replace("月", "-").replace("日", "")
            return public_time
        public_time = timestr[:10]
        return public_time

    @staticmethod
    def _get_info(weibo_content):
        """
        确定作者、编辑等。
        :param weibo_content: 微博全文内容。
        :return:
        """

        tree = etree.HTML(weibo_content)
        realcontent = tree.xpath("//span[@class='ctt']")[0].xpath("string(.)")
        jizhelist = []
        jianjilist = []
        bianjilist = []
        if re.findall(r"\[记者\|(.+?)\]", weibo_content):
            jizhelist = re.findall(r"\[记者\|(.+?)\]", weibo_content)[0].split("、")
        if re.findall(r"\[视频剪辑\|(.+?)\]", weibo_content):
            jianjilist = re.findall(r"\[视频剪辑\|(.+?)\]", weibo_content)[0].split("、")
        if re.findall(r"\[编辑\|(.+?)\]", weibo_content):
            bianjilist = re.findall(r"\[编辑\|(.+?)\]", weibo_content)[0].split("、")
        return "、".join(jizhelist), "、".join(jianjilist), "、".join(bianjilist), realcontent

    def _upload_to_bos(self, pic_url):
        """
        上传文件至BOS。
        :param pic_url: 图片链接。
        :return:
        """

        p_name = "python-spider"
        # 下载图片地址
        img_path = f"{self._download_path}/imgs"
        os.makedirs(img_path, exist_ok=True)
        # 图片名字
        img_name = p_name + self._md5(pic_url) + '.jpg'
        local_img_file_path = f"{img_path}/{img_name}"
        try:
            # 下载图片
            urlretrieve(pic_url, local_img_file_path)
            # 最终图片地址
            url = f"{self._api}/tools_bosftp/"
            files = {
                "fileupload": open(local_img_file_path, "rb")
                # "fileupload": open("imgs/{}".format(localpicname), "rb")
            }
            datas = {
                "bucketname": self.bucket_name,
                "savepath": self.bucket_destination + "/" + img_name,
                "key": "2eef4c1204f7ccef7eb5a1d6bcc6bcfe",
            }
            r = requests.post(url, files=files, data=datas, timeout=8)
            if json.loads(r.text)["message"] == "success":
                print(f"图片上传成功，{pic_url}")
                new_pic_url = "https://bj.bcebos.com/v1/{}/{}".\
                    format(self.bucket_name, self.bucket_destination+"/"+img_name)
            else:
                print(f"图片上传失败，{pic_url}")
                new_pic_url = pic_url
            return new_pic_url
        except Exception as e:
            print(f"{e}\n{traceback.format_exc()}")
        finally:
            if local_img_file_path and os.path.isfile(local_img_file_path):
                os.remove(local_img_file_path)

    def _es_per_exists(self, field_id):
        """
        确定es中是否重复
        :return:
        """

        return self._es_conn.exists(index=self._es_index_name, doc_type=self._es_doc_type, id=field_id)

    def _es_data_to(self, fields):
        """
        数据保存到es中
        :param fields: 数据体。
        :return:
        """

        url = f"{self._api}/tools_mongointoes/"
        test_url = f"{self._api}/tools_mongointoesceshi/"
        datas = {
            "indexname": self._es_index_name,
            "typename": self._es_doc_type,
            "itemid": fields.pop("_id"),
            "saveitem": json.dumps(fields)
        }
        resp = requests.post(url, data=datas)
        print(f"正式存储结果是：{resp.text}")
        resp = requests.post(test_url, data=datas)
        print(f"存放测试存储结果是：{resp.text}")

    # 按业务提取内容
    def _parse(self, element):
        """
        提取微博发布时间
        :param element: 列表页上每一条微博的定位。
        # :param target_url: 每一条微博的url,计划以其md5值作为判重依据，但目前没用。
        :return:
        """

        parse_fields = {
            "_id": "",
            "title": "",
            "contenturl": "",
            "content": "",
            "realcontent": "",
            "createTime": 0,
            "pubTime": 0,
            "authors": "",
            "photographers": "",
            "editors": "",
            "pubSource": "",
            "zanNum": 0,
            "zhuanNum": 0,
            "pingNum": 0,
            "galleryImgs": list(),
            "column": "",
        }
        """根据uid不同，判断微博名称，判断bos转换时的存放路径"""
        if self._uid == "6211141835":
            parse_fields["pubSource"] = "雄安发布微博"
            self.bucket_destination = "zycf_gk/img/xafbwb"
        else:
            parse_fields["pubSource"] = "河北日报微博"
            self.bucket_destination = "zycf_gk/img/hbrbwb"
        """ ------发布时间 爬取时间 插入列名"""
        # 发布时间。
        try:
            parse_fields["pubTime"] = self._get_wb_timestamp(
                element.xpath("div/span[@class='ct']")[0].xpath("string(.)"))
        except Exception as e:
            raise ValueError("Failed to parse pub_time, '{}'.".format(e))
        public_time = self._find_sina_time(element.xpath("div/span[@class='ct']")[0].xpath("string(.)"))
        parse_fields["column"] = "hbrbwb{}".format(public_time.replace("-", ""))

        # ------contenturl,content,title,_id realcontent为纯文本
        # 提取标题和正文，若包含`全文`则进入详情页获取，否则在列表页提取。
        whole_article_href = element.xpath("div[1]//a[text()='全文']/@href")
        if whole_article_href:
            # 请求"全文"的详情页。
            whole_article_url = urljoin(self._site_url, whole_article_href[0])
            parse_fields["contenturl"] = whole_article_url
            resp = self._session.get(whole_article_url, headers=self._request_header, timeout=5)
            content_tree = etree.HTML(resp.content)
            if content_tree is not None and len(content_tree) > 0:
                """real_content改为//div[@id='M_']//text(),避免本来有title但缺少`【`,`】`造成标题缺失"""
                """改回去，因`赞[1] 转发[0] 评论[1] 收藏 28分钟`里数据变化造成加密计算结果变化"""
                if content_tree.xpath("div/a[contains(text(),'组图')]"):    # 不为空
                    real_content = content_tree.xpath("//div[@id='M_']/div[1]/span[@class='ctt']")[0].xpath(
                        "string(.)") + content_tree.xpath("//div[@id='M_']/div[1]/text()[1]") + \
                                  content_tree.xpath("//div[@id='M_']/div[1]/a[2]")[0].xpath(
                                      "string(.)") + content_tree.xpath("//div[@id='M_']/div[1]/text()[2]")
                else:
                    real_content = content_tree.xpath("//div[@id='M_']/div[1]/span[@class='ctt']")[0].xpath("string(.)")
                if re.findall(r"【.+?】", real_content):
                    parse_fields["title"] = re.findall(r"【.+?】", real_content)[0].replace("【", "").replace("】", "")
                else:
                    parse_fields["title"] = ""
                parse_fields["content"] = html.tostring(content_tree.xpath("//div[@id='M_']")[0], encoding='utf-8')\
                    .decode("utf-8")
                parse_fields["_id"] = self._md5(real_content)
            else:
                raise ValueError("·全文·页{} Failed to parse detail content into a tree".format(whole_article_url))
        else:
            # 直接从列表页抽取标题和正文。
            parse_fields["contenturl"] = ""
            # # content_tree = etree.HTML("")
            # if element.xpath("div/a[contains(text(),'组图')]"):
            #     real_content = element.xpath("div[1]/span[@class='ctt']")[0].xpath("string(.)") + \
            #                    element.xpath("div[1]/text()[1]") + element.xpath("div[1]/a[2]")[0].xpath("string(.)") \
            #                    + element.xpath("div[1]/text()[2]")
            # else:
            #     real_content = element.xpath("div[1]/span[@class='ctt']")[0].xpath("string(.)")
            real_content = element.xpath("./div[1]/span[@class='ctt']")[0].xpath("string(.)")
            parse_fields["content"] = html.tostring(element.xpath("div[1]")[0], encoding='utf-8').decode("utf-8")
            if re.findall(r"【.+?】", real_content):
                parse_fields["title"] = re.findall(r"【.+?】", real_content)[0].replace("【", "").replace("】", "")
            else:
                parse_fields["title"] = ""
            parse_fields["_id"] = self._md5(real_content)
            # realcontent = element.xpath("div[1]/span[@class='ctt']")[0].xpath("string(.)")

        """ ---------作去重处理 """
        res = self._es_per_exists(parse_fields["_id"])
        if res:
            print(f"已存在，{parse_fields['_id']}")
            return

        parse_fields["createTime"] = int(
            time.mktime(time.strptime(str(datetime.datetime.today())[:19], "%Y-%m-%d %H:%M:%S")))

        # --------realcontent，记者，视频剪辑，编辑
        parse_fields["authors"], parse_fields["photographers"], parse_fields["editors"], parse_fields["realcontent"] = \
            self._get_info(parse_fields["content"].replace("丨", "|"))

        # 使用beautifulSoup方法提取纯文本
        soup = BeautifulSoup(parse_fields["content"], "html.parser")
        parse_fields["realcontent"] = soup.text
        parse_fields["realcontent"] = parse_fields["realcontent"].strip(":").strip("：")

        # --------点赞 转发 评论数目
        """判断微博是否转发，决定微博的赞、转发的数据来源"""
        # 点赞、转发、评论数。
        long_str = element.xpath("string(.)")
        if "转发理由" in long_str:
            long_str = long_str.split("转发理由")[1]
            parse_fields["zanNum"] = int(re.findall(r"赞\[(\d+)\]", long_str)[0])
            parse_fields["zhuanNum"] = int(re.findall(r"转发\[(\d+)\]", long_str)[0])
            parse_fields["pingNum"] = int(re.findall(r"评论\[(\d+)\]", long_str)[0])
        else:
            parse_fields["zanNum"] = int(re.findall(r"赞\[(\d+)\]", long_str)[0])
            parse_fields["zhuanNum"] = int(re.findall(r"转发\[(\d+)\]", long_str)[0])
            parse_fields["pingNum"] = int(re.findall(r"评论\[(\d+)\]", long_str)[0])

        # 获取图片，存在[组图、原图以及无图]
        pic_group_href = element.xpath("div/a[contains(text(),'组图')]/@href")
        if pic_group_href:
            try:
                pic_group_href = pic_group_href[0]
                resp = self._session.get(pic_group_href, headers=self._request_header, timeout=self._timeout)
                tree = etree.HTML(resp.content)
                if tree is not None and len(tree) > 0:
                    for pic_url in tree.xpath("//img/@src"):
                        try:
                            # 小图中图都换成大图。
                            replacements = re.findall(r"\.cn/(.+)/", pic_url)
                            if replacements:
                                replacement = replacements[0]
                                pic_url = pic_url.replace(replacement, "large")
                            # parse_fields["galleryImgs"].append(pic_url)
                            parse_fields["galleryImgs"].append(self._upload_to_bos(pic_url))
                        except Exception as e:
                            print("·全文·转换大图失败{}.\n{}".format(e, traceback.format_exc()))
                            # self._logger.warning("·全文·转换大图失败{}.\n{}".format(e, traceback.format_exc()))
                            continue
                else:
                    print("·全文·在从tree提取组图时失败{}".format(pic_group_href))
            except Exception as e:
                print("·全文·转换图片报错：{}.\n{}".format(e, traceback.format_exc()))
                # self._logger.warning("{}.\n{}".format(e, traceback.format_exc()))
        else:
            if element.xpath("div/a[text()='原图']"):
                try:
                    pic_url = element.xpath("div/a[text()='原图']/preceding-sibling::a[1]/img/@src")[0]
                    # 小图中图都换成大图。
                    replacements = re.findall(r"\.cn/(.+)/", pic_url)
                    if replacements:
                        replacement = replacements[0]
                        pic_url = pic_url.replace(replacement, "large")
                    # parse_fields["galleryImgs"].append(pic_url)
                    parse_fields["galleryImgs"].append(self._upload_to_bos(pic_url))
                except Exception as e:
                    print("·在列表页获取原图时失败·：{}.\n{}".format(e, traceback.format_exc()))
                    # self._logger.warning("{}.\n{}".format(e, traceback.format_exc()))

        save_item = dict()
        save_item["_id"] = parse_fields["_id"]
        save_item["title"] = parse_fields["title"]
        save_item["url"] = parse_fields["contenturl"]
        save_item["content"] = parse_fields["content"].replace("全文", "")
        save_item["realcontent"] = parse_fields["realcontent"].replace("全文", "")
        save_item["createTime"] = parse_fields["createTime"]
        save_item["pubTime"] = parse_fields["pubTime"]
        save_item["authors"] = parse_fields["authors"].split("、")
        save_item["photographers"] = parse_fields["photographers"]
        save_item["editors"] = parse_fields["editors"].split("、")
        save_item["pubSource"] = parse_fields["pubSource"]
        save_item["zanNum"] = parse_fields["zanNum"]
        save_item["zhuanNum"] = parse_fields["zhuanNum"]
        save_item["pingNum"] = parse_fields["pingNum"]
        save_item["galleryImgs"] = parse_fields["galleryImgs"]
        self._es_data_to(save_item)

        return save_item

    def fetch_pages(self, pages=1):
        """
        从页面开始采集。
        :param pages: 页码。
        :return:
        """

        for page in range(1, pages+1):
            # 列表页起始url改用固定开头/uid
            list_url = f"https://weibo.cn/u/{self._uid}?page={page}"
            print(f"url地址：{list_url}，开始抓取")
            # 若是多页抓取，则会有抓取间隔
            if page > 1:
                time.sleep(self._list_page_interval)
            try:
                resp = self._session.get(list_url, headers=self._request_header)
                # 将响应体解析成树。
                tree = etree.HTML(resp.content)
                if tree is not None and len(tree) > 0:
                    # 定位到每一条微博
                    elements = tree.xpath("//body/div[starts-with(@id, 'M_')]")
                    if elements:
                        for element in elements:
                            # 每一条微博的url
                            # item_id = element.xpath("@id")[0]
                            # doc_id = re.findall("M_(.*)", item_id)[0]
                            # target_url = "https://weibo.com/{}/{}".format(self._uid, doc_id)
                            # url_md5 = self._md5(target_url)
                            # 以此可作为唯一值与数据库比对，判重
                            data = self._parse(element)
                            yield data
                    else:
                        print(f"列表页：{list_url}定位每一条微博报错")
                else:
                    print(f"列表页：{list_url}内容parse to etree 报错")
            except Exception as e:
                print(f"列表页：{list_url}抓取报错： {e}.\n{traceback.format_exc()}")
        # return res

    def fetch(self, pages=1):
        # 入口。
        return self.fetch_pages(pages=pages)


def get_cookies():
    """
    获取微博采集用随机cookie。
    :return:
    """
    resp = requests.get("http://192.168.16.7:16100/crawler_resources/get_random_wb_cookie", timeout=10)
    resp_data = json.loads(resp.content)
    return resp_data["data"]["wbCookie"]["cookie"]


def scheduler():
    # 执行入口。

    cookie = get_cookies()
    # 分别执行河北日报微博采集和雄安发布微博采集。
    uid_lis = ["6211141835", "1623340585"]
    for uid in uid_lis:
        for ret in WeiBoFetch(cookie, uid).fetch_pages(pages=1):
            if ret:
                print(json.dumps(ret, indent=4, ensure_ascii=False))


def test_scheduler():
    # 测试入口。

    cookie = "_T_WM=86948584093; MLOGIN=0; SUB=_2A25yn9t9DeRhGeFL6loR8ijJwz6IHXVuY-U1rDV6PUJbk'tANLXWskW1NQnDNVJnNmnFLL35KvUuNcQjTLmhi_KDq; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFhaDIXcU83cQ8kTIg8-lXC5NHD95QNSK2RehzcSKnEWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNS0-p1h5ESo-Rentt; SUHB=0QS5OroYqiya0F; SSOLoginState=1604037421"
    uid = "1623340585"
    for ret in WeiBoFetch(cookie, uid).fetch_pages(pages=1):
        print(json.dumps(ret, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    scheduler()
