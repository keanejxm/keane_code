# -*- coding:utf-8 -*-

"""
# author: Chris
# date: 2020.10.28
# update: 2020.10.28
"""

import requests
import time
import re
import hashlib
import traceback
import datetime
import json
from lxml import etree
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .wb_up_session import TouTiaoSession
from .wb_counts import get_wb_counts
from .wb_convert_rid_to_mid import convert_wb_rid_to_mid

from api_common_utils.get_wb_cookie import get_wb_cookie
from api_common_utils.proxy import get_abuyun_proxies


class XinYuanWb:

    def __init__(self, uid, logger):
        cook = get_wb_cookie()
        cookies = cook["cookie"]
        self._cookies = cookies
        self._uid = uid
        self._logger = logger
        # 微博列表页请求头。
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
        self._timeout = 5
        self._site_url = "https://weibo.cn/"
        # 采集间隔时长。
        self._list_page_interval = 1.5
        self.gender = {"未知": 0, "男": 1, "女": 2, "其它": 3}
        proxy = get_abuyun_proxies()
        self._session.proxies = proxy

    def _md5(self, unicode_str, charset="UTF-8"):
        """
        字符串转md5格式。
        :return:
        """
        _md5 = hashlib.md5()
        _md5.update(unicode_str.encode(charset))
        return _md5.hexdigest()

    def _get_wb_timestamp(self, time_str):
        """
        提取微博发布时间。
        :param time_str: 含有时间信息的字符串。
        :return:
        """

        this_date = str(datetime.date.today())[:10]
        this_year = time.strftime('%Y', time.localtime(time.time()))

        # 提取时间。
        time_str_type = re.findall(r"来自.+", time_str)
        if time_str_type:
            time_str = time_str.replace(re.findall(r"来自.+", time_str)[0], "")
        else:
            time_str = time_str

        # 时间转换。
        if time_str.strip().startswith("今天"):
            time_str = time_str.replace("今天", "").strip()
            time_str = this_date + " " + time_str
            return int(time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M")))
        elif time_str.find("分钟前") != -1:
            minago = (int(re.findall(r'(\d+)分钟前', time_str)[0]))
            nowtime = (datetime.datetime.now() - datetime.timedelta(minutes=minago)).strftime("%Y-%m-%d %H:%M:%S")
            return int(time.mktime(time.strptime(nowtime, "%Y-%m-%d %H:%M:%S")))
        elif time_str.find("月") != -1:
            month = re.findall(r"(\d+)月(\d+)日(.+)", time_str)[0][0]
            day = re.findall(r"(\d+)月(\d+)日(.+)", time_str)[0][1]
            hour_minute = re.findall(r"(\d+)月(\d+)日(.+)", time_str)[0][2].strip()
            time_str = "{}-{}-{} {}".format(this_year, month, day, hour_minute)
            return int(time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M")))
        else:
            return int(time.mktime(time.strptime(time_str.strip(), "%Y-%m-%d %H:%M:%S")))

    def _parse_video(self, vid_url):
        """
        返回可打开的视频地址
        :param vid_url:
        :return:
        """
        try:
            # vid_url_li = vid_url.split("object_id")
            vid_url = "https://m.weibo.cn/s/video/object?object_id=" + vid_url
            resp = self._session.get(vid_url)
            res = json.loads(resp.text)
            video_url = res["data"]["object"]["stream"]["url"]       # 视频连接
            video_img = res["data"]["object"]["image"]["url"]           # 视频封面连接
        except:
            video_url = video_img = ""
            self._logger.warning(f"视频链接{vid_url},未能获取到视频地址")
        return video_url, video_img

    def _parse_content(self, content, vid_url, vid_img):
        """
        在content内添加video标签
        :param content:
        :param vid_url:
        :param vid_img:
        :return:
        """
        soup = BeautifulSoup(content, "html.parser")
        video = soup.new_tag("video")
        video.attrs.update({"src": vid_url})
        video.attrs.update({"poster": vid_img})
        soup.find("div").insert(-1, video)
        return str(soup).strip()

    def _parse(self, nick_name, uid, doc_rid, element, url):
        """
        处理详情
        :param nick_name:
        :param uid:
        :param doc_rid:
        :param element:
        :param url:
        :param url_md5:
        :return:
        """
        parse_fields = {
            "_id": "",
            "status": 1,
            "platformWorksID": "",              # 平台作品ID，该平台唯一标识此作品的ID，
            "platformID": "",                   # 【信源平台】索引里的【_id】
            "platformName": "微博",             # 【信源平台】索引里的【name】
            "platformType": 2,                  # 平台类型，1微信、2微博、
            "channelID": "",
            "channelName": "",
            "accountID": "",                     # 【信源账号】索引里的_id
            "accountName": nick_name,                  # 【信源账号】索引里的name
            # "avatar": avatar,
            "topicID": "",
            "topicTitle": "",
            "epaperLayoutID": "",
            "authors": [],
            "editors": [],
            "hbrbAuthors": [],
            "preTitle": "",
            "subTitle": "",
            "url": url,                          # 作品链接，可以是分享链接
            "title": "",
            "titleWordsNum": "",                 # 标题字数
            "content": "",                      # 正文
            "contentWordsNum": "",              # 正文字数
            "html": "",                         # 详情页全文，不用于检索
            "simhash": "",                      # simhash值，可用于相似作品匹配，应当认为是基于纯文本计算得到的
            "contentType": -1,                  # 作品类型，-1未知，1文字，2图文，3视频文，4纯长视频，5纯短视频，等
            "digest": "",                       # 摘要，正文前200个中文（含标点符号）
            "source": "",                       # 作品转载来源，爬虫直接得到
            "isOriginal": -1,                   # 是否原创，-1未知，1是，0否，
            "isOriginalCompute": -1,
            "isTop": -1,
            "isPush": -1,
            "classifications": [],
            "images": list(),
            "topics": list(),
            "covers": list(),
            "videos": list(),
            "audios": list(),
            "readNum": 0,                       # 阅读数
            "likeNum": 0,                       # 点赞数
            "commentNum": 0,
            "forwardNum": 0,
            "collectNum": 0,                    # 收藏数
            "wxLookNum": 0,
            "wangYiJoinNum": 0,
            "updateParams": "",
            "sentiment": -1,
            "sentimentPositiveProb": -1,
            "sentimentRawInfo": "",
            "tags": [],
            "tagsLength": 0,
            "personNames": [],
            "regionNames": [],
            "organizationNames": [],
            "keywords": [],
            "segmentWordsRawInfo": [],
            "wordFrequency": [],
            "wordFrequencyLength": 0,
            "hasDiscovery": -1,
            "hasSpread": -1,
            "hasSimilarWorks": -1,
            "hasSimilarOriginalWorks": -1,
            "reprintNum": 0,
            "reprintMediaNum": 0,
            "spreadHI": 0.0,
            "interactiveHI": 0.0,
            "pubTime": 0,
            "createTime": 0,
            "updateTime": 0,
        }
        """微博的分类只有头条文章（细分：1文字、2图文、3视频文）和微博消息（短消息）"""
        parse_fields["contentType"] = 8
        # 计算出mid。
        wb_mid = convert_wb_rid_to_mid(doc_rid)
        # 发布时间。
        try:
            parse_fields["pubTime"] = self._get_wb_timestamp(
                element.xpath("div/span[@class='ct']")[0].xpath("string(.)"))
        except Exception as e:
            raise ValueError("Failed to parse pub_time, '{}'.".format(e))
        # 判断微博内容是否为原创。
        if element.xpath("div[last()]/span[1][text()='转发理由:']"):
            parse_fields["isOriginal"] = 0
            source = element.xpath("string(div[1]/span[1])")
            try:
                source_str = re.findall(r"转发了\s+(.*)\s+的微博", source)
                parse_fields["source"] = source_str[0].strip()
            except:
                parse_fields["source"] = ""
        else:
            parse_fields["isOriginal"] = 1

        """关于文章扩展类型的讨论"""
        """假如类型为头条文章,那么content,title则为头条文章的详情页不再是那条微博的详情页了"""
        tou_tiao = element.xpath("div[1]//a/@href")
        if len(tou_tiao) > 0:
            tt_article1 = [i for i in tou_tiao if i.startswith("https://weibo.cn/sinaurl?")]
            tt_article = []
            for tt in tt_article1:
                if len(tt.split("&")) > 2:
                    tt_article.append(tt)
        else:
            tt_article = []
        if len(tt_article) > 0:
            # parse_fields["extendContentType"] = 2

            """确定为头条文章那么请求该链接获取content,title"""
            refer_url = "https://weibo.cn/u/{}".format(uid)
            mid_fields = TouTiaoSession(self._cookies, tt_article[0], refer_url, self._logger).get_toutiao_content()
            if mid_fields:
                parse_fields["title"] = mid_fields["title"]
                parse_fields["authors"] = mid_fields["author"]
                parse_fields["content"] = mid_fields["content"]
                parse_fields["images"] = mid_fields["images"]
                parse_fields["videos"] = mid_fields["videos"]
                parse_fields["covers"] = mid_fields["covers"]
                parse_fields["readNum"] = mid_fields["readNum"]
                parse_fields["digest"] = mid_fields["digest"]
                # video_con判断是否存在视频链接，因为头条文章已处理了视频
                video_con = []
                """对头条文章类型进行分类"""
                if len(parse_fields["videos"]) != 0:
                    parse_fields["contentType"] = 3
                elif len(parse_fields["videos"]) == 0 and len(parse_fields["images"]) != 0:
                    parse_fields["contentType"] = 2
                else:
                    parse_fields["contentType"] = 1
            else:
                """当判断为头条文章的出现跨域无返回值时，扩展类型修改，对应值则从列表页中获取"""
                parse_fields["contentType"] = 8
                # video_con判断是否存在视频链接
                video_con = element.xpath("div[1]//a/@href")
                # parse_fields["extendContentType"] = 1
                contents = element.xpath("div[1]")
                if contents:
                    content = etree.tostring(contents[0]).decode("utf-8")
                    soup = BeautifulSoup(content, "html.parser")
                    soup_title = str(soup).strip().split("<br/>")[0]
                    soup_title_str = BeautifulSoup(soup_title, "html.parser")
                    cos = soup_title_str.get_text()
                    parse_fields["title"] = cos
                    parse_fields["content"] = str(soup).strip()
                else:
                    raise ValueError("Failed to fetch content, {}.".format(url))
        else:
            # parse_fields["extendContentType"] = 1
            """获取微博标题与正文(全文的详情页或者列表页)、视频videos是否存在"""
            # 提取标题和正文，有的微博内容无法在列表页里展示全，需要另外获取详情。
            whole_article_hrefs = element.xpath("div[1]//a[text()='全文']/@href")
            if whole_article_hrefs:
                # 请求"全文"的详情页。
                whole_article_url = urljoin(self._site_url, whole_article_hrefs[0])
                resp = self._session.get(whole_article_url, headers=self._request_header, timeout=5)
                # parse_fields["html"] = resp.text
                content_tree = etree.HTML(resp.content)
                # video_con判断是否存在视频链接
                if content_tree is not None and len(content_tree) > 0:
                    video_con = content_tree.xpath("//div[@id='M_']/div[1]/a/@href")
                    contents = content_tree.xpath("//div[@id='M_']/div[1]")
                    if contents:
                        content = etree.tostring(contents[0]).decode("utf-8")
                        soup = BeautifulSoup(content, "html.parser")
                        soup_title = str(soup).strip().split("<span class=\"ct\">")[0]
                        soup_title_str = BeautifulSoup(soup_title, "html.parser")
                        cos = soup_title_str.get_text()
                        parse_fields["title"] = cos
                        parse_fields["content"] = str(soup).strip()
                    else:
                        raise ValueError("Failed to fetch content, {}.".format(whole_article_url))
                else:
                    raise ValueError("Failed to parse detail content into a tree, {}.".format(whole_article_url))
            else:
                # 直接从列表页抽取标题和正文。
                # realcontent = element.xpath("div[1]/span[@class='ctt']")[0].xpath("string(.)")
                # video_con判断是否存在视频链接
                video_con = element.xpath("div[1]//a/@href")
                contents = element.xpath("div[1]")
                if contents:
                    content = etree.tostring(contents[0]).decode("utf-8")
                    soup = BeautifulSoup(content, "html.parser")
                    soup_title = re.split(r"赞.*", str(soup).strip())[0]
                    soup_title_str = BeautifulSoup(soup_title, "html.parser")
                    cos = soup_title_str.get_text()
                    parse_fields["title"] = cos
                    parse_fields["content"] = str(soup).strip()
                else:
                    raise ValueError("Failed to fetch content, {}.".format(url))
        """点赞、转发、评论数下面方法的获取，依靠get_wb_counts()方法更新；来自(微博、360客户端...)"""
        # 点赞、转发、评论数。
        is_owner = element.xpath("./div[1]/span[@class='cmt']//text()")
        is_owner = "".join(is_owner)
        if is_owner.startswith("转发了"):
            is_flag = False
        else:
            is_flag = True
        long_str = element.xpath("string(.)")
        if is_flag:
            parse_fields["likeNum"] = int(re.findall(r"赞\[(\d+)\]", long_str)[0])
            parse_fields["forwardNum"] = int(re.findall(r"转发\[(\d+)\]", long_str)[0])
            parse_fields["commentNum"] = int(re.findall(r"评论\[(\d+)\]", long_str)[0])
        else:
            # self._logger.info(f"这是转发文章各种数计算用转发理由之后的，{long_str}")
            long_str = long_str.split("转发理由")[1]
            parse_fields["likeNum"] = int(re.findall(r"赞\[(\d+)\]", long_str)[0])
            parse_fields["forwardNum"] = int(re.findall(r"转发\[(\d+)\]", long_str)[0])
            parse_fields["commentNum"] = int(re.findall(r"评论\[(\d+)\]", long_str)[0])
        # 图片。12-21修正图片归属于images字段
        pic_group_hrefs = element.xpath("div/a[contains(text(),'组图')]/@href")
        if pic_group_hrefs:
            try:
                pic_group_href = pic_group_hrefs[0]
                resp = self._session.get(pic_group_href, headers=self._request_header, timeout=self._timeout)
                tree = etree.HTML(resp.content)
                time.sleep(5)
                if tree is not None and len(tree) > 0:
                    for pic_url in tree.xpath("//img/@src"):
                        try:
                            # 小图中图都换成大图。
                            replacements = re.findall(r"\.cn/(.+)/", pic_url)
                            if replacements:
                                replacement = replacements[0]
                                pic_url = pic_url.replace(replacement, "large")
                            parse_fields["images"].append(pic_url)
                        except Exception as e:
                            self._logger.warning("{}.\n{}".format(e, traceback.format_exc()))
                            continue
                else:
                    self._logger.warning("Failed to parse image group content into a tree, {}.".format(pic_group_href))
            except Exception as e:
                self._logger.warning("{}.\n{}".format(e, traceback.format_exc()))
        else:
            if element.xpath("div/a[text()='原图']"):
                try:
                    pic_url = element.xpath("div/a[text()='原图']/preceding-sibling::a[1]/img/@src")[0]
                    # 小图中图都换成大图。
                    replacements = re.findall(r"\.cn/(.+)/", pic_url)
                    if replacements:
                        replacement = replacements[0]
                        pic_url = pic_url.replace(replacement, "large")
                    parse_fields["images"].append(pic_url)
                except Exception as e:
                    self._logger.warning("{}.\n{}".format(e, traceback.format_exc()))
        # covers字段为images字段的第一张图片
        if len(parse_fields["images"]) > 0:
            parse_fields["covers"] = [parse_fields["images"][0]]

        """重新确定视频连接,object_id来源于span[@class=ctt]/a[last()]/@href"""
        # video_con = element.xpath("div[1]//a/@href")
        video_tf = [i for i in video_con if "video" in i]
        if video_tf:
            vid_num = re.findall(r"object_id=(.*?)&", video_tf[0])[0]
            video_url, video_img = self._parse_video(vid_num)
            # 当确定又视频链接时才重新调整covers、content内容，否则pass
            # 存在一些因为其他原因造成不能获取视频信息的情况,
            if video_url:
                parse_fields["videos"] = [video_url]
                content_vid = self._parse_content(parse_fields["content"], video_url, video_img)
                parse_fields["content"] = content_vid
            else:
                parse_fields["videos"] = []

        """关于文章类型的讨论"""
        # 文章类型讨论 12-23如果封面图为空、正文内有图，则把首张图赋给封面图
        if len(parse_fields["images"]) > 0 and len(parse_fields["covers"]) == 0:
            parse_fields["covers"] = parse_fields["images"][0]

        wb_read_num = wb_play_num = 0
        try:
            wb_counts = get_wb_counts(nick_name.rstrip("微博"), wb_mid=uid)
            try:
                wb_read_num = wb_counts["readNum"]
            except Exception:
                wb_read_num = 0
            # try:
            #     wb_play_num = wb_counts["playNum"]
            # except:
            #     wb_play_num = 0
        except Exception as e:
            self._logger.warning(f"{doc_rid},{e},{traceback.format_exc()}")
        parse_fields["readNum"] = wb_read_num  # 阅读数
        # if is_flag:
        #     parse_fields["playNum"] = wb_play_num  # 播放数

        """新添加话题"""
        topics = element.xpath("./div[1]/span/a/text()")  # 话题列表
        parse_fields["topics"] = [i for i in topics if i.startswith("#")]
        parse_fields["platformWorksID"] = wb_mid
        # MD5(str(name) + str(type))
        parse_fields["platformID"] = self._md5(parse_fields["platformName"] + str(parse_fields["platformType"]))
        # md5(platformID+platformAccountID)
        parse_fields["accountID"] = self._md5(parse_fields["platformID"] + uid)
        coding_str1 = str(parse_fields["platformID"]) + str(parse_fields["platformWorksID"])
        parse_fields["_id"] = self._md5(coding_str1)
        parse_fields["updateParams"] = json.dumps({"nickName": nick_name, "mediaWorkId": wb_mid, "is_flag": is_flag},
                                                  separators=(",", ":"), ensure_ascii=False)
        parse_fields["titleWordsNum"] = len(parse_fields["title"])
        parse_fields["contentWordsNum"] = len(parse_fields["title"])
        parse_fields["digest"] = parse_fields["title"][:200]
        parse_fields["createTime"] = int(time.time()*1000)
        parse_fields["updateTime"] = int(time.time()*1000)
        parse_fields["pubTime"] = parse_fields["pubTime"] * 1000
        return parse_fields

    def fetch_page(self, page=1):
        account = {
            "_id": "",
            "status": 1,
            "platformAccountID": "",        # 平台账号id如微信的biz
            "introduction": "",             # 简介（之前的认证信息）
            "name": "",
            "avatar": "",
            "qrcode": "",                   # 二维码图片链接
            "gender": -1,
            "mobilePhoneNumber": "",         # 手机号
            "email": "",                    # 邮箱地址
            "identityCode": "",             # 身份证号
            "certificationType": -1,        # -1未知，1政府，2媒体，3企业等
            "url": "",
            "region": [],                   # 地域
            # "province": "",
            # "city": "",
            "types": [],                    # 分类
            "selfTypesIDs": [],
            "platformID": "",               # 信源平台里的索引id
            "platformName": "",             # 信源平台索引里的name
            "platformType": 2,              # 信源平台索引中的【type】，1微信、2微博、
            "weMediaName": "微博",          # 该平台的自媒体账号统称，参考：【公众号】、【微博】
            "extendData": "{}",             # 该账号的最新作品信息
            "platformWorksNum": 0,          # 所在平台总计【作品】数
            "platformFansNum": 0,           # 所在平台总计【粉丝】数
            "platformFollowsNum": 0,        # 所在平台总计【关注者】数
            "platformReadsNum": 0,          # 所在平台总计【阅读】数，亦可代表视频【播放】数
            "platformLikesNum": 0,          # 所在平台总计【点赞】数
            "platformCommentsNum": 0,       # 所在平台总计【评论】数
            "platformForwardsNum": 0,       # 所在平台总计【转发】数
            "worksNum": 0,                  # 库内【作品】数
            "readNum": 0,                  # 库内【阅读】数
            "likeNum": 0,                  # 库内【点赞】数
            "commentNum": 0,               # 库内【评论】数
            "forwardNum": 0,               # 库内【转发】数
            "createTime": 0,                # 创建时间
            "updateTime": 0,                # 更新时间
        }
        for current_page in range(page, page+1):
            list_url = "https://weibo.cn/u/{}?page={}".format(self._uid, current_page)
            # 请求列表页。
            try:
                resp = self._session.get(list_url, headers=self._request_header)
                # 多页采集时，每次请求后需等待一段时间。
                if page > 1:
                    # 间隔休息。
                    time.sleep(self._list_page_interval)
                """保存列表页，加时间戳"""
                tree = etree.HTML(resp.content)
                if tree is not None and len(tree) > 0:
                    """只有第一页有账号信息"""
                    if current_page == 1:
                        account["platformAccountID"] = self._uid
                        account["url"] = "https://weibo.cn/u/{}".format(self._uid)
                        platform_tree = tree.xpath("//div[@class='u']")[0]
                        account["avatar"] = platform_tree.xpath("./table/tr/td[1]/a/img/@src")[0]  # 账号头像地址
                        nick_nfo = platform_tree.xpath("./table/tr/td[2]/div/span[1]//text()")
                        if len(nick_nfo) > 2:
                            account["name"] = nick_nfo[0].replace("\n", "").replace("\t", "").strip()
                            account["gender"] = nick_nfo[1].replace("\n", "").replace("\t", "").strip().split('/')[0]
                            account["region"] = nick_nfo[1].replace("\n", "").replace("\t", "").strip().split('/')[1]
                        else:
                            account["name"] = nick_nfo[0].replace("\n", "").replace("\t", "").strip().split('\xa0')[
                                0]
                            gender_info = nick_nfo[0].replace("\n", "").replace("\t", "").strip().split('\xa0')[1]
                            account["gender"] = gender_info.split('/')[0]
                            account["region"] = gender_info.split('/')[1]
                        account["region"] = [account["region"]]
                        account["gender"] = self.gender[account['gender']]
                        account["introduction"] = platform_tree.xpath("./table/tr/td[2]/div/span[2]//text()")[0]  # 认证信息
                        num_info = platform_tree.xpath("./div//text()")
                        account["platformWorksNum"] = int(re.search(r"微博\[(\d+)\]?", str(num_info)).group(1))  # 总微博数
                        account["platformFollowsNum"] = int(re.search(r"关注\[(\d+)\]?", str(num_info)).group(1))  # 关注数
                        account["platformFansNum"] = int(re.search(r"粉丝\[(\d+)\]?", str(num_info)).group(1))  # 粉丝数
                        account["platformName"] = "微博"
                        account["platformID"] = self._md5(account["platformName"] + str(account["platformType"])) # 顺序很重要
                        coding_str1 = str(account["platformID"] + account["platformAccountID"])    # 顺序很重要
                        account["_id"] = self._md5(coding_str1)
                        now = int(time.time() * 1000)
                        account["updateTime"] = now
                        account["createTime"] = now
                        """获取该账号的最新作品的时间、标题id等"""
                        elements = tree.xpath("//body/div[starts-with(@id, 'M_')]")
                        works_id = title = ""
                        pub_time = 0
                        if elements:
                            contents = elements[0].xpath("div[1]")
                            content = etree.tostring(contents[0]).decode("utf-8")
                            soup = BeautifulSoup(content, "html.parser")
                            soup_text = soup.get_text()
                            if "置顶" not in soup_text:
                                item_id = elements[0].xpath("@id")[0]
                                pub_str = elements[0].xpath("div/span[@class='ct']")[0].xpath("string(.)")
                            else:
                                contents = elements[1].xpath("div[1]")
                                content = etree.tostring(contents[0]).decode("utf-8")
                                soup = BeautifulSoup(content, "html.parser")
                                item_id = elements[1].xpath("@id")[0]
                                pub_str = elements[1].xpath("div/span[@class='ct']")[0].xpath("string(.)")
                            soup_title = re.split(r"赞.*", str(soup).strip())[0]
                            soup_title_str = BeautifulSoup(soup_title, "html.parser")
                            cos = soup_title_str.get_text()
                            title = cos
                            doc_id = re.findall("M_(.*)", item_id)[0]
                            works_id = convert_wb_rid_to_mid(doc_id)
                            try:
                                pub_time = self._get_wb_timestamp(pub_str)
                                pub_time = pub_time * 1000
                            except Exception as e:
                                raise ValueError("获取账号最新作品时间报错：, '{}'.".format(e))
                        coding_str = str(account["platformName"]) + str(account["platformType"])
                        mid_id = self._md5(coding_str)
                        coding_str1 = mid_id + works_id
                        works_id = self._md5(coding_str1)
                        account["extendData"] = json.dumps(
                            {"latestWorksID": works_id, "latestWorksPubTime": pub_time, "latestWorksTitle": title},
                            separators=(",", ":"), ensure_ascii=False)
                    # 定位到每一条微博信息。
                    elements = tree.xpath("//body/div[starts-with(@id, 'M_')]")
                    if elements:
                        for element in elements:
                            try:
                                item_id = element.xpath("@id")[0]
                                doc_id = re.findall("M_(.*)", item_id)[0]
                                assert doc_id, "Error, failed to fetch wb uid."
                                target_url = "https://weibo.com/{}/{}".format(self._uid, doc_id)
                                url_md5 = self._md5(target_url)
                                nick_name = account["name"]
                                avatar = account["avatar"]
                                res_data = self._parse(nick_name, self._uid, doc_id, element, target_url)
                                if elements.index(element) == 0:
                                    data = dict(code=1, msg="OK", data=dict(account=account, works=res_data))
                                else:
                                    data = dict(code=1, msg="OK", data=dict(works=res_data))
                                yield data
                            except Exception as e:
                                self._logger.warning(f"{target_url}, {e}.\n{traceback.format_exc()}")
                                continue
                    else:
                        self._logger.warning("Failed to fetch elements, {}.".format(list_url))
                        data = dict(code=1, msg="OK", data=dict(account=account))
                        yield data
                else:
                    self._logger.warning("Failed to parse list content into a tree, {}.".format(list_url))
            except Exception as e:
                self._logger.warning("{}.\n{}".format(e, traceback.format_exc()))

    def fetch_yield(self):
        rest = self.fetch_page()
        # for i in rest:
        #     print(json.dumps(i, indent=4, ensure_ascii=False))
        return rest

    def fetch_batch(self):
        account_res = []
        works_res = []
        rest = self.fetch_page()
        for i in rest:
            if "account" in i["data"]:
                account_res.append(i["data"]["account"])
                works_res.append(i["data"]["works"])
            else:
                works_res.append(i["data"]["works"])
        result = {"code": 1, "msg": "OK", "data": {"accounts": account_res, "worksList": works_res}}
        return result


def data_test_crawl():
    # 删除：新京报1644114654，中国青年报1726918143，光明日报1402977920，央视财经2258727970，央证公开课2032139271
    # 2-14剔除"5301384788", "1816461852", "2829904260", "2111919165",
    uds = ["1715118170", "3215951873", "1698857957", "2336569730", "1291152165", "5617030362", "2271051770",
           "2207702064", "1893892941", "2656274875", "1738004582", "1642512402", "2803301701", "1623340585",
           "2698146894"]
    # co = "_T_WM=fbc383e7727e6d15824fff3427afac85; SUB=_2A25ynwxcDeRhGeVP7FIW9C3FzTuIHXVuY5QUrDV6PUJbktANLXbnkW1NTReDzWwRkfDDmYghUMJb6fxeeDeHC_xA; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhqWqJYp58eqHrVgypOM4Vp5NHD95Q0eKM7S0B01KqNWs4DqcjVi--ciKn4iKyFi--ciKLhi-iWi--NiK.Xi-2Ri--ciKnRi-zNe02NehMXe0.cS7tt; SUHB=0D-1xZQpKHbE-y; SSOLoginState=1604025357"
    # cook = get_wb_cookie()
    # co = cook["cookie"]
    """河北新闻网、河北日报、人民日报、燕赵都市报"""
    # uds1 = ["2698146894", "1623340585", "2803301701", "1738004582"]
    from lib.common_utils.llog import LLog
    logger = LLog("test", only_console=True).logger
    for ud in uds:
        res = XinYuanWb(ud, logger).fetch_yield()
        for info in res:
            print(json.dumps(info, indent=4, ensure_ascii=False))
        # AccountsCrawlerESUtils(logger).es_save_accounts_and_works(res["data"])
        # with open("result.json", "w", encoding="utf8") as f:
        #     f.write(json.dumps(res, indent=4, ensure_ascii=False))
        import elasticsearch
        es_conn = elasticsearch.Elasticsearch([{"host": "180.76.161.67", "port": 9200}])
        for info in res:
            if "account" in info["data"]:
                fid = info["data"]["account"].pop("_id")
                # es_conn.index(index="dc_accounts", id=fid, body=info["data"]["account"], doc_type="_doc")
                new_fields = dict()
                for key, value in info["data"]["account"].items():
                    if value:
                        if key not in ("region", "createTime"):
                            if key.endswith("Num"):
                                if value != 0:
                                    new_fields[key] = value
                            else:
                                new_fields[key] = value
                now = int(time.time() * 1000)
                new_fields["updateTime"] = now
                new_fields = dict(doc=new_fields)
                res = es_conn.update(index="dc_accounts", doc_type="_doc", body=new_fields, id=fid)
                logger.info(f"{fid}，{res['result']}")
                if info["data"]["works"]:
                    wid = info["data"]["works"].pop("_id")
                    res = es_conn.index(index="dc_works", id=wid, body=info["data"]["works"], doc_type="_doc")
                    logger.info(f"{wid}，{res['result']}")
            else:
                wid = info["data"]["works"].pop("_id")
                res = es_conn.index(index="dc_works", id=wid, body=info["data"]["works"], doc_type="_doc")
                logger.info(f"{wid}，{res['result']}")
        logger.info(f"账号--{ud}--采集完成")


if __name__ == '__main__':
    data_test_crawl()
    # from lib.common_utils.llog import LLog
    # logg = LLog("test", only_console=True).logger
    # XinYuanWb("1623340585", logg).fetch_batch()






