# Author Keane
# coding=utf-8
# @Time    : 2021/1/9 10:53
# @File    : shijiazhuangribao1.py
# @Software: PyCharm
import bs4
import json
import time
import hashlib
import traceback
import requests
from datetime import datetime as _datetime
from lxml import etree
from elasticsearch import Elasticsearch


class AppSpideraShiJiaZhuangRiBao(object):
    # 移动端爬虫基类。

    def __init__(self):
        # 获取会话，用于获取各频道XHR数据。
        self._session = None
        self._session = self.get_session()
        self._timeout = 8

        # 详情页链接模板。
        self._detail_link_template = "http://app.peopleapp.com/Api/600/DetailApi/shareArticle?type=0&article_id={}"

        # 编码。
        self._charset = ("utf-8", "utf8", "gb2312", "gbk", "gb18030", "big5")

        # 连接ES。
        self.es_host = "192.168.16.21"
        self.es_port = 9200
        self.index_name = "big_data_mainmedia"
        self.doc_type = "_doc"
        self.hosts = list()
        self.hosts.append(
            dict(
                host=self.es_host,
                port=self.es_port,
            )
        )
        self.es_conn = Elasticsearch(hosts=self.hosts)

    # session
    @staticmethod
    def get_session():
        """
        获取session对象。
        :return:
        """

        # 代理。
        proxy_meta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": "http-dyn.abuyun.com",
            "port": "9020",
            "user": "HR91J1A4881W7H1D",
            "pass": "6A8682072812B30F",
        }
        proxies = {
            "http": proxy_meta,
            "https": proxy_meta,
        }

        # HTTP会话。
        session = requests.Session()
        session.proxies = proxies

        return session

    # 带信息打印
    @staticmethod
    def _print(input_string, *args, **kwargs):
        """
        带信息打印。
        :return:
        """

        print("{} {}".format(_datetime.now(), input_string), flush=True, *args, **kwargs)

    @staticmethod
    def is_hebei(text):
        """
        检查文本是否与河北有关。
        :return:
        """

        if not text:
            return False

        regions = ["河北", "石家庄", "唐山", "秦皇岛", "邯郸", "邢台", "保定", "张家口", "承德", "沧州", "廊坊", "衡水", "雄安"]
        for region in regions:
            try:
                pos = text.index(region)
                if pos >= 0:
                    if region == "河北":
                        pos_temp = text.index("河北区")
                        if pos != pos_temp:
                            return True
                    else:
                        return True
            except ValueError:
                pass

            # 检查关键词内是否存在空格。
            # pattern = r"^.*?[\s]*?{}".format(region[0])
            # for word in region[1:]:
            #     pattern += r"[\s]{1,2}?" + word
            # if re.match(pattern, text, flags=re.S | re.I):
            #     return True

        return False

    # 频道页获取规则
    @staticmethod
    def list_channel_rules():
        """
        列表页获取规则。
        石家庄日报手机客户端，android，1.0.2。
        :return:
        """

        # 爬取规则信息。
        rules = dict(
            name="石家庄日报手机客户端，android，1.1.3",
            rules_list=list(),
            code=1,
            msg="success"
        )

        # 请求头。

        # 频道列表新闻。
        url = "http://static.sjzrbapp.com:89/type/getTypeListCache"
        request_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "145",
            "Host": "static.sjzrbapp.com:89",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.1",
        }
        body = "sign=cf2fb873a01ac29835e56f1f818a3116&siteId=1&siteid=1&device=00000000-1" \
               "5c7-18b7-8e6b-6f8e0033c587&nonce=1622475814&version=1.1.3&tid=1067&timestamp=1610174467940"
        rules['rules_list'].append(dict(
            description="频道信息",
            method='POST',
            url=url,
            request_headers=request_headers,
            body=body,
            extend_fields=dict(
                isDelivery=1,
            )
        ))
        print(rules)
        return json.dumps(rules)

    # 列表页获取规则
    def list_page_rules(self, channel_id):
        """
        列表页获取规则。
        石家庄日报手机客户端，android，1.0.2。
        :return:
        """

        # 爬取规则信息。
        rules = dict(
            name="石家庄日报手机客户端，android，1.1.3",
            rules_list=list(),
            code=1,
            msg="success"
        )
        # banner新闻。
        url = "http://static.sjzrbapp.com:89/flash/getFlashList"
        request_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "145",
            "Host": "static.sjzrbapp.com:89",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.1",
        }
        body = {
            "version": "1.1.3",
            "timestamp": str(int(time.time() * 1000)),
            "tid": str(channel_id),
            "siteId": "1",
            "siteid": "1",
            "nonce": "1622475814",
            "device": "00000000-15c7-18b7-8e6b-6f8e0033c587",
        }
        sb = "b11ebd23bb617a75"
        a = sorted(body, reverse=False)
        for i in a:
            sb += (i + "=" + body.get(i))
        sign = self.md5(sb)
        body = f"sign={sign}&siteId=1&siteid=1&device=00000000-15c7-18b7-8e6b-6f8e0033c587&nonce=1622475814&vers" \
               f"ion=1.1.3&tid={channel_id}&timestamp={body.get('timestamp')}"
        rules['rules_list'].append(dict(
            description="banner列表信息",
            method='POST',
            url=url,
            request_headers=request_headers,
            body=body,
            extend_fields=dict(
                isDelivery=1,
            )
        ))

        # 文章列表新闻。
        url = "http://static.sjzrbapp.com:89/news/getNewsListCache"
        request_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "145",
            "Host": "static.sjzrbapp.com:89",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.1",
        }
        body = {
            "version": "1.1.3",
            "timestamp": str(int(time.time() * 1000)),
            "tid": str(channel_id),
            "siteId": "1",
            "siteid": "1",
            "reqPagenum": "1",
            "nonce": "1622475814",
            "device": "00000000-15c7-18b7-8e6b-6f8e0033c587",
        }
        sb = "b11ebd23bb617a75"
        a = sorted(body, reverse=False)
        for i in a:
            sb += (i + "=" + body.get(i))
        sign = self.md5(sb)
        body = f"reqPagenum=1&sign={sign}&siteId=1&siteid=1&device=00000000-15c7-18b7-8e6b-6f8e0033c587&nonce" \
               f"=1622475814&version=1.1.3&tid={channel_id}&timestamp={body.get('timestamp')}"
        rules['rules_list'].append(dict(
            description="文章列表信息",
            method='POST',
            url=url,
            request_headers=request_headers,
            body=body,
            extend_fields=dict(
                isDelivery=1,
            )
        ))
        print(rules)
        return json.dumps(rules)

    # 生成默认字段
    @staticmethod
    def default_fields():
        """
        生成取默认值的字段，仅对上游新闻（因涉及客户端名称、省、市等字段）。
        :return: 默认字段取值字典。
        """

        return dict(
            # 一级分类。
            categoryFirst="",
            # 二级分类。
            categorySecond="",
            # 三级分类。
            categoryThird="",
            # 关键词。
            keywords=[dict(word="", weight=1.0)],
            # 来源名称。
            platformName="石家庄日报客户端",
            # 来源类型。
            platformType=9,
            # 排名系数。
            rankCoefficient=1.0,
            # 情感分析。
            sentiment=-1,
            # 市名。
            sourceCity="",
            # 省名。
            sourceProvince="",
            # 网站级别。
            sourceLevel=3,
            # 网站类别。
            sourceClassify=1,
            # 重点渠道。
            sourceImportance=1,
            # 主流媒体。
            mainMedia=1,
            # 地域。
            region=[],
            # 关联词。
            relevantWords=[],
            # 状态。
            status=1,
            # 内容提及的城市。
            city="",
            # 媒体类型，0为网PC，1为端app。
            mediaType=1,
            # 是否已完成图片下载和上传云存储。
            loadPicture=0,
        )

    # 检查es中是否存在
    def per_exists(self, _id):
        """
        ES中是否存在。
        :return:
        """

        return self.es_conn.exists(index=self.index_name, doc_type=self.doc_type, id=_id)

    # 发送推送消息
    def send_message(self, field_id, fields):
        """
        发送推送消息。
        :return:
        """

        # 新数据推送至融云线上的用户。
        source_ids = {
            "人民日报客户端": -1,
            "新华社客户端": -2,
            "央视新闻客户端": -3,
        }
        # noinspection PyBroadException
        try:
            platform_name = fields["platformName"]
            title = fields["title"]
            url = "https://backend.tw.hbrbdata.cn/admin/Sendmessage/insertNewAndSend"
            datas = {
                "title": title,
                "sourceId": source_ids[platform_name],
                "newsId": field_id,
            }
            response = requests.post(url, data=datas)
            if response.status_code == requests.codes.ok:
                self._print("Push [{}, {}] successfully.".format(field_id, title))
            else:
                raise ValueError("[{}, {}].".format(field_id, title, response.status_code))
        except Exception as e:
            self._print("Failed to push, '{}'.".format(e))

    # 存入es
    def save_to_es(self, field_id, fields):
        """
        保存至ES集群中。
        :param field_id: _id字段。
        :param fields: 数据体。
        :return:
        """

        # 检查库中是否已存在。
        if not self.per_exists(field_id):
            # 不存在时发送消息，且新增。
            self.send_message(field_id, fields)
            self.es_conn.index(index=self.index_name, doc_type=self.doc_type, id=field_id, body=fields)
            self._print("{} '{}' created.".format(field_id, fields["title"]))
        else:
            # 更新前确认用户是否下载过。
            response = self.es_conn.get(self.index_name, doc_type=self.doc_type, id=field_id, _source=["loadPicture"])
            if "loadPicture" in response["_source"] and response["_source"]["loadPicture"] in (1, "1"):
                self._print("{} '{}' loadPicture is 1 and do nothing.".format(field_id, fields["title"]))
                return
            # 已存在时，只更新content字段。
            update_fields = dict(
                doc=dict(
                    content=fields["content"]
                )
            )
            self.es_conn.update(index=self.index_name, doc_type=self.doc_type, id=field_id, body=update_fields)
            self._print("{} '{}' updated.".format(field_id, fields["title"]))

    # 获取视频url
    @staticmethod
    def get_video_url(raw_content):
        """
        获取本站视频的url。
        :param raw_content:
        :return:
        """

        video_dict = dict(
            hasVideo=0,
            videoUrls=json.dumps(list()),
        )

        soup = bs4.BeautifulSoup(raw_content, 'html.parser')
        tag_list = soup.find_all('video')
        if tag_list:
            video_urls = list()
            for tag in tag_list:
                if tag.has_attr('src'):
                    if tag['src']:
                        video_urls.append(tag['src'])

            if video_urls:
                video_dict['hasVideo'] = 1
                video_dict['videoUrls'] = json.dumps(video_urls)

        return video_dict

    @staticmethod
    def get_img_url(raw_content):
        """
        获取本站视频的url。
        :param raw_content:
        :return:
        """

        img_dict = dict(
            hasImages=0,
            imgUrls=json.dumps(list()),
        )

        soup = bs4.BeautifulSoup(raw_content, 'html.parser')
        tag_list = soup.find_all('img')
        if tag_list:
            img_urls = list()
            for tag in tag_list:
                if tag.has_attr('data-original'):
                    if tag['data-original']:
                        img_urls.append(tag['data-original'])

            if img_urls:
                img_dict['hasImages'] = 1
                img_dict['imgUrls'] = json.dumps(img_urls)

        return img_dict

    # md5加密
    @staticmethod
    def md5(strsea, charset="UTF-8"):
        """
        字符串转md5格式。
        :param strsea:
        :param charset:
        :return:
        """

        md5 = hashlib.md5()
        md5.update(strsea.encode(charset))
        return md5.hexdigest()

    def article(self, site_url):
        """
        过滤详情页内容。
        :param site_url:
        :return:
        """
        html_res = self._session.get(site_url).text
        html_res = html_res.encode("ISO-8859-1").decode("utf8")
        html = etree.HTML(html_res)
        content = html.xpath("//div[@id= 'aritcleContent']")
        content = list(map(lambda x: etree.tostring(x, encoding="unicode").strip(), content))[0]
        images = self.get_img_url(content)
        videos = self.get_video_url(content)
        return content, images, videos

    # 解析数据体，找出关键信息。
    # 解析数据体找出关键信息，列表页及详情页
    def generate_fields(self, site_url, response, extend_fields):
        """
        找出json数据体中的关键信息。
        人民日报手机客户端，android，7.0.2。
        :return:
        """

        # 解析数据体，找出关键信息。
        if isinstance(response, (bytes, str)):
            response = json.loads(response)
        else:
            raise TypeError("Need type of bytes(str).")

        # 验证返回内容。
        if not isinstance(response, dict) or "data" not in response or not isinstance(response["data"], list):
            raise TypeError("The 'data' not found or not a list.")
        if not response["data"]:
            raise ValueError("Empty data_list, {}.".format(site_url))

        # 验证字段参数。
        if not isinstance(extend_fields, dict):
            extend_fields = dict()

        data = response["data"]
        # 再一次验证列表。
        if not data:
            raise ValueError("Empty data_list, {}.".format(site_url))
        for item in data:
            try:
                # articleid是用于排除的字段，正常应该不等于0。
                if "nid" not in item.keys() or item["nid"] in (0, "0"):
                    raise ValueError("'{}' articleid({}) error.".format(item["title"], item["articleid"]))

                # 整合默认字段。
                fields = self.default_fields()
                # 整合参数字段。
                fields = dict(fields, **extend_fields)

                # 检查标题是否存在于列表中。
                if "title" in item.keys() and item["title"]:
                    fields["title"] = item["title"].strip()
                if "publish_time" in item.keys() and item["publish_time"]:
                    fields['pubTime'] = int(item["publish_time"])
                else:
                    pass
                    # 保留字段。
                filler = dict()
                # 转载来源。
                if "copyfrom" in item.keys() and item['copyfrom']:
                    filler['pubSource'] = item['copyfrom']
                else:
                    filler['pubSource'] = ""
                fields['filler'] = json.dumps(filler, indent=4, ensure_ascii=False)
                # 详情页连接。
                url = "http://static.sjzrbapp.com:89/news/newsinfo"
                if "nid" in item.keys() and item["nid"] not in ("0", 0):
                    # 规则一。
                    body = {
                        "nid": str(item["nid"]),
                        # "sign":"62478f9c059e6633ff0e33c21e8a0077",
                        "siteId": "1",
                        "siteid": "1",
                        "device": "00000000-15c7-18b7-8e6b-6f8e0033c587",
                        "nonce": "1622475814",
                        "version": "1.1.3",
                        "timestamp": str(int(time.time() * 1000)),
                    }
                    sb = "b11ebd23bb617a75"
                    a = sorted(body, reverse=False)
                    for i in a:
                        sb += (i + "=" + body.get(i))
                    sign = self.md5(sb)
                    body = f"nid={item['nid']}&sign={sign}&siteId=1&siteid=1&device=00000000-15c7-18b7-8e6b-6f8e0" \
                           f"033c587&nonce=1622475814&version=1.1.3&timestamp={body.get('timestamp')}"
                    try:
                        temp_request_headers = {
                            "Content-Type": "application/x-www-form-urlencoded",
                            "Content-Length": "164",
                            "Host": "static.sjzrbapp.com:89",
                            "Connection": "Keep-Alive",
                            "Accept-Encoding": "gzip",
                            "User-Agent": "okhttp/3.8.1",
                        }
                        detail_response = self._session.post(url,
                                                             headers=temp_request_headers, data=body,
                                                             timeout=self._timeout)
                        # 请求间隔时间。
                        # time.sleep(random.random() + 2)
                        if detail_response.status_code == requests.codes.ok:
                            detaile_article = json.loads(detail_response.text)
                            print(detaile_article)
                            fields["url"] = detaile_article["data"]["shareUrl"]
                            # 赋值正文。
                            if "link" in detaile_article["data"].keys() and detaile_article["data"]["link"]:
                                fields['content'] = detaile_article["data"]["link"]
                            elif "video_path" in detaile_article["data"].keys() and detaile_article["data"][
                                "video_path"]:
                                fields['content'] = detaile_article["data"]["video_path"]
                            else:
                                content, images, videos = self.article(fields["url"])
                                # fields["videoList"] = videos
                                fields['content'] = content
                            if "copyfrom" in detaile_article["data"] and detaile_article["data"]["copyfrom"]:
                                filler = dict()
                                # 转载来源。
                                if "copyfrom" in item.keys() and item['copyfrom']:
                                    filler['pubSource'] = item['copyfrom']
                                else:
                                    filler['pubSource'] = ""
                                fields['filler'] = json.dumps(filler, indent=4, ensure_ascii=False)
                        else:
                            raise ValueError("{}".format(detail_response.status_code))
                    except Exception as e:
                        raise ValueError("Failed to parse content, {} '{}'.".format(fields['url'], e))

                # 爬取时间。
                now = int(time.time())
                fields['createTime'] = now
                fields["imgList"] = "[]"
                # 正文是否有图。
                if "imgs" in item.keys() and item["imgs"]:
                    fields['hasPic'] = 1
                elif "imgurl" in item.keys() and item["imgurl"]:
                    fields['hasPic'] = 1
                else:
                    fields['hasPic'] = 0

                # 封面图。
                fields['coverPic'] = list()
                if "imgs" in item.keys() and item["imgs"]:
                    # 先从列表中取封面图。
                    # noinspection PyBroadException
                    try:
                        fields["coverPic"] = [item["imgs"][0]]
                    except Exception:
                        pass
                else:
                    fields["coverPic"] = [item["imgurl"]]

                # 检查是否与河北有关。
                if self.is_hebei(fields['title']) or self.is_hebei(fields['content']):
                    fields['isHebei'] = 1
                else:
                    fields['isHebei'] = 0

                # 计算出发布日期当天零点的时间戳。
                field_id_str = "{}_{}_{}".format(fields['platformName'], fields['title'], fields["isDelivery"])
                # 计算出本条记录的ID。
                field_id = self.md5(field_id_str)
                yield field_id, fields
            except Exception as e:
                self._print("Error but continue, '{}'.".format(e))
                continue

    # 解析频道页信息获取频道相关信息
    def generate_channel_field(self, site_url, response, extend_fields):
        """
        解析频道页面，获取频道信息
        :param site_url:
        :param response:
        :param extend_fields:
        :return:
        """
        # 解析数据体，找出关键信息。
        if isinstance(response, (bytes, str)):
            response = json.loads(response)
        else:
            raise TypeError("Need type of bytes(str).")

        # 验证返回内容。
        if not isinstance(response, dict) or "data" not in response or not isinstance(response["data"], list):
            raise TypeError("The 'data' not found or not a list.")
        if not response["data"]:
            raise ValueError("Empty data_list, {}.".format(site_url))

        # 验证字段参数。
        if not isinstance(extend_fields, dict):
            extend_fields = dict()

        data = response["data"]
        # 再一次验证列表。
        if not data:
            raise ValueError("Empty data_list, {}.".format(site_url))
        for item in data:
            try:
                # articleid是用于排除的字段，正常应该不等于0。
                if "tid" not in item or item["tid"] in (0, "0"):
                    raise ValueError("'{}' articleid({}) error.".format(item["title"], item["articleid"]))

                # 整合默认字段。
                fields = dict()
                # 整合参数字段。
                fields = dict(fields, **extend_fields)

                # 检查标题是否存在于列表中。
                if "cnname" in item and item["cnname"]:
                    fields["channelName"] = item["cnname"].strip()
                else:
                    continue
                if "tid" in item and item["tid"] and fields["channelName"] != "视频":
                    fields["channelID"] = item["tid"]
                elif "childs" in item and item["childs"]:
                    # for channel in item["childs"]:
                    print(item)
                    channel = item["childs"][0]
                    fields["channelID"] = channel["tid"]
                else:
                    continue
                yield fields
            except Exception as e:
                self._print("Error but continue, '{}'.".format(e))
                continue

    # 按列表页请求规则请求并返回结果
    def deal_with_list_response(self, rule, channel_name):
        """
        按列表页规则请求并返回结果。
        :return:
        """

        if 'method' in rule:
            method = rule['method']
        else:
            return

        if 'url' in rule:
            url = rule['url']
        else:
            return

        if 'request_headers' in rule:
            request_headers = rule['request_headers']
        else:
            return

        if 'body' in rule:
            body = rule['body']
        else:
            body = dict()

        if 'extend_fields' in rule:
            extend_fields = rule['extend_fields']
        else:
            extend_fields = dict()

        if method == 'GET':
            response = self._session.get(url, headers=request_headers, allow_redirects=False, timeout=self._timeout)
        elif method == 'POST':
            response = self._session.post(
                url, headers=request_headers, data=body, allow_redirects=False, timeout=self._timeout
            )
        else:
            self._print("Unknown method: {}.".format(method))
            return

        if response.status_code == requests.codes.ok:
            # 凑齐关键字。

            for field_id, fields in self.generate_fields(url, response.text,
                                                         extend_fields=extend_fields):
                fields["categoryFirst"] = channel_name
                print(field_id)
                print(json.dumps(fields, indent=4, ensure_ascii=False))

            #     # noinspection PyBroadException
            #     try:
            #         # 存入ES集群中。
            #         self.save_to_es(field_id, fields)
            #     except Exception as e:
            #         self._print("Failed to save to ES, '{}'.".format(e))
            #         continue
        else:
            raise ValueError(response.status_code)

    # 按频道页规则请求并返回结果。
    def deal_with_channel_response(self, rule):
        """
        按列表页规则请求并返回结果。
        :return:
        """

        if 'method' in rule:
            method = rule['method']
        else:
            return

        if 'url' in rule:
            url = rule['url']
        else:
            return

        if 'request_headers' in rule:
            request_headers = rule['request_headers']
        else:
            return

        if 'body' in rule:
            body = rule['body']
        else:
            body = dict()

        if 'extend_fields' in rule:
            extend_fields = rule['extend_fields']
        else:
            extend_fields = dict()

        if method == 'GET':
            response = self._session.get(url, headers=request_headers, allow_redirects=False, timeout=self._timeout)
        elif method == 'POST':
            response = self._session.post(
                url, headers=request_headers, data=body, allow_redirects=False, timeout=self._timeout
            )
        else:
            self._print("Unknown method: {}.".format(method))
            return

        if response.status_code == requests.codes.ok:
            print(response.text)
            # 凑齐关键字。
            for fields in self.generate_channel_field(url, response.text,
                                                      extend_fields=extend_fields):
                channel_id = fields.get("channelID")
                channel_name = fields.get("channelName")
                self.deal_with_list_page_rules(self.list_page_rules(channel_id), channel_name)

        else:
            raise ValueError(response.status_code)

    # 处理频道页规则。
    def deal_with_list_channel_rules(self, rules):
        """
        处理列表页规则。
        :return:
        """

        try:
            rules = json.loads(rules)
        except (json.JSONDecodeError, TypeError):
            self._print("{}\n{}".format(rules, traceback.format_exc()))
            return

        if 'rules_list' in rules and isinstance(rules['rules_list'], list) and rules['rules_list']:
            for rule in rules['rules_list']:
                # noinspection PyBroadException
                try:
                    self._print("Start {}.".format(rule["description"]))
                    self.deal_with_channel_response(rule)
                except Exception:
                    if 'url' in rule and rule['url']:
                        self._print("Failed to process this rule, {}.\n{}".format(rule['url'], traceback.format_exc()))
                    else:
                        self._print("Failed to process this rule.\n{}".format(rule['name'], traceback.format_exc()))
                    continue
        else:
            self._print("Empty rule '{}'.")
            return

    # 处理列表页规则。
    def deal_with_list_page_rules(self, rules, channel_name):
        """
        处理列表页规则。
        :return:
        """

        try:
            rules = json.loads(rules)
        except (json.JSONDecodeError, TypeError):
            self._print("{}\n{}".format(rules, traceback.format_exc()))
            return

        if 'rules_list' in rules and isinstance(rules['rules_list'], list) and rules['rules_list']:
            for rule in rules['rules_list']:
                # noinspection PyBroadException
                try:
                    self._print("Start {}.".format(rule["description"]))
                    self.deal_with_list_response(rule, channel_name)
                except Exception:
                    if 'url' in rule and rule['url']:
                        self._print(
                            "Failed to process this rule, {}.\n{}".format(rule['url'], traceback.format_exc()))
                    else:
                        self._print("Failed to process this rule.\n{}".format(rule['name'], traceback.format_exc()))
                    continue
        else:
            self._print("Empty rule '{}'.")
            return

    def run(self):
        # 程序入口。

        self.deal_with_list_channel_rules(self.list_channel_rules())


if __name__ == '__main__':
    aaa = AppSpideraShiJiaZhuangRiBao()
    aaa.run()
