# -*- coding:utf-8 -*-
"""
# project:大鱼号账号作品采集
# author: Neil
# update: 2020/11/11
# 更新内容：账号文章采集重做，主要包括以下逻辑，增加纯文字文章，图文，纯视频文，视频图文逻辑判断。
"""
import re
import time
import json
import hashlib
import requests
import traceback
import unicodedata
from lxml import etree
from loguru import logger
from api_common_utils.proxy import get_abuyun_proxies


def make_md5(str):
    """
    产生md5加密
    :param str: 加密字符串
    :return: 加密后的字符串
    """
    str_i = str.encode('utf-8')
    md5 = hashlib.md5(str_i).hexdigest()
    return md5

class DaYuSpider:

    def __init__(self, log):
        self._logger = log
        self._timeout = 20
        self._session = requests.session()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/84.0.4147.125 Safari/537.36'
        }
        self.media_type = 7
        self.media_name = '大鱼号'

    def account_spider(self, uid, account_type):
        """
        采用的是抓包技术
        对账号数据进行采集，主要包含头像，昵称
        :param uid: 作者id
        :param account_type: 账号类型
        :return: 账号信息
        """
        try:
            # 对账号详情页发起访问 拿到粉丝数作品数
            url = f'https://upbigsubs-api.uc.cn/api/bigsubs/{uid}/frontpage?' \
                f'uc_param_str=frdnpfvecpntgibiniprdswiutmt' \
                f'&app=ucweb&sub_type=wm&b_version=0.4&errCode=2' \
                f'&errMsg=ucapi.invoke%20not%20exsit%2C%20should%20load' \
                f'%20in%20UCBrowser%20%21&ut=AAQuLl0WSFNXJwCIgccPZnizKN9OiLo2pkPjd5oIoq2jnA%3D%3D'
            author_info = self._session.get(url=url, timeout=self._timeout)
            author_info_json = json.loads(author_info.text)['data']
            name = author_info_json.get('sub_name', "")
            avatar = author_info_json.get("avatar_url","")
            user_url = author_info_json.get('homepage_url', "")
            fans_num = author_info_json.get('follower_counts', 0)
            works_num = author_info_json.get("total_article_cnt", 0)
            now = int(time.time())
            time_10 = now
            time_13 = now * 1000
            account_dict = {
                "_id": make_md5(f'{self.media_type}{uid}{str(account_type)}'),
                "mediaType": self.media_type,
                "mediaName": self.media_name,
                "accountType": int(account_type),
                "mediaUid": str(uid),
                "nickName": name,
                "avatar": avatar,
                "url": user_url,
                "gender": 0,
                "province": "",
                "city": "",
                "fanNum": fans_num,
                "followNum": 0,
                "mediaWorkNum": works_num,
                "mediaReadNum": 0,
                "mediaCommentNum": 0,
                "mediaForwardNum": 0,
                "AII": 0,
                "AFCI": 0,
                "mediaLikeNum": 0,
                "createTime": time_10,
                "createDateTime": time_13,
                "updateTime": time_10,
                "updateDateTime": time_13,
            }
            self._logger.debug(f'采集{account_dict["nickName"]}的用户信息{account_dict}')
            return account_dict
        except Exception as e:
            self._logger.warning(f"{e}\n{traceback.format_exc()}")

    def article_spider(self, account_dict):
        """
        对指定账号下面的新闻数据进行访问并采集
        对新闻列表数据的采集用的是抓包
        :return: 文章列表
        """
        articles_list = list()
        # 首先对账号的数据列表页发起访问
        url = f'https://ff.dayu.com/contents/author/{account_dict["mediaUid"]}?biz_id=1002&_size=8&_page=1' \
            f'&_order_type=published_at&status=1' \
            f'&_fetch=1&uc_param_str=frdnsnpfvecpntnwprdssskt'
        # 列表页数据
        res = self._session.get(url=url, timeout=self._timeout).text
        res_json_list = json.loads(res)['data']
        for article in res_json_list:
            try:
                if 'content_id' in article and article['content_id']:
                    wid = article['content_id']
                    update_params = str(wid)
                else:
                    continue
                _id = make_md5(f'{self.media_type}{wid}{account_dict["accountType"]}')
                # 文章详情url
                author_id = article["author_id"]
                article_url = f"https://mparticle.uc.cn/article_org.html?uc_param_str=frdnsnpfvecpntnwprdssskt" \
                    f"&wm_cid={wid}&wm_id={author_id}"
                # 封面图
                covers = list()
                if 'cover_url' in article and article['cover_url']:
                    covers.append(article['cover_url'])
                else:
                    covers = []

                # 提交时间
                if article['published_at']:
                    pub_time = article['published_at']
                    date = pub_time[:10]
                    hours = pub_time[11:19]
                    pub_time = date + " " + hours
                    pub_time_ = int(time.mktime(time.strptime(pub_time, "%Y-%m-%d %H:%M:%S")))
                    pub_time_13 = int(time.mktime(time.strptime(pub_time, "%Y-%m-%d %H:%M:%S"))) * 1000
                else:
                    now = int(time.time())
                    pub_time_ = now
                    pub_time_13 = now * 1000

                # 对详情页发起访问
                url = f'https://ff.dayu.com/contents/{wid}?biz_id=1002&_fetch_author=1' \
                    f'&_incr_fields=click1,click2,click3,click_total,play,like'
                response = self._session.get(url=url)
                res_json = json.loads(response.text)['data']
                status = res_json.get("status", 0)
                title = res_json.get("title", "").replace(" ", "").replace("\n", "")
                # 正文内容
                videos = list()
                content_type = -1
                content = ""
                if 'text' in res_json['body'] and res_json['body']['text']:
                    content_type = 1
                    content = res_json['body']['text'].replace("\n", "").replace("   ", "")
                    # unicodedata模块提供了normalize方法将Unicode字符转换为正常字符
                    content = unicodedata.normalize('NFKC', content)
                    # 将图片链接加入到正文文本中
                    if 'inner_imgs' in res_json['body'] and res_json['body']['inner_imgs']:
                        content_type = 2
                        for img in res_json['body']['inner_imgs']:
                            i = img['url']
                            content = content.replace(
                                "<!--{img:%d}-->" % res_json['body']['inner_imgs'].index(img),
                                f"<img src='{i}'>")
                    if 'inner_videos' in res_json['body'] and res_json['body']['inner_videos']:
                        content_type = 3
                        for info in res_json['body']['inner_videos']:
                            try:
                                # 视频参数
                                ums_id = info['ums_id']
                                wm_cid = wid
                                wm_id = account_dict["mediaUid"]
                                # 视频封面图
                                poster = info["thumbnail"]
                                # 对详情发起访问获取token
                                res = requests.get(url=article_url)
                                token = requests.utils.dict_from_cookiejar(res.cookies)["vpstoken"]
                                url = f'https://mparticle.uc.cn/api/vps?token={token}&ums_id={ums_id}&' \
                                    f'wm_cid={wm_cid}&wm_id={wm_id}&resolution=high'
                                video = requests.get(url=url).text
                                video_json = json.loads(video)['data']
                                video_url = video_json["url"]
                                videos.append(video_url)
                                content = content.replace(
                                    "<!--{video:%d}-->" % res_json['body']['inner_videos'].index(info),
                                    f"<video src='https://dayu.com/wid={wid}uid={wm_id}/' poster='{poster}'></video>'>")
                                # 判断covers是否为空
                                if covers:
                                    covers = covers
                                else:
                                    covers.append(poster)
                            except Exception as e:
                                self._logger.warning(f"{e}\n{traceback.format_exc()}")

                # 纯视频文章
                elif "videos" in res_json["body"] and res_json["body"]["videos"]:
                    content_type = 3
                    for info in res_json['body']["videos"]:
                        try:
                            ums_id = info['ums_id']
                            wm_cid = wid
                            wm_id = account_dict["mediaUid"]
                            # 视频封面图
                            poster = info["thumbnail"]
                            # 对详情发起访问获取token
                            res = requests.get(url=article_url)
                            token = requests.utils.dict_from_cookiejar(res.cookies)["vpstoken"]
                            url = f'https://mparticle.uc.cn/api/vps?token={token}&ums_id={ums_id}&wm_cid={wm_cid}' \
                                f'&wm_id={wm_id}&resolution=high'
                            video = requests.get(url=url).text
                            video_json = json.loads(video)['data']
                            video_url = video_json["url"]
                            videos.append(video_url)
                            content = f"<div><p><video src='https://dayu.com/wid={wid}uid={wm_id}/' title='{title}' \
                                f'poster='{poster}' controls='controls'>{title}</video></p></div>"
                            # 判断covers是否为空
                            if covers:
                                covers = covers
                            else:
                                covers.append(poster)
                        except Exception as e:
                            self._logger.warning(f"{e}\n{traceback.format_exc()}")

                # 对评论页面发起访问 获取点赞和评论
                if res_json['_extra'] and res_json['_extra']['xss_item_id']:
                    com_item_id = res_json['_extra']['xss_item_id']
                    headers = {
                        'Referer': f'http://sp-iflow.uc.cn/webapp/webview/xissAllComments?app=uc-iflow'
                        f'&aid={com_item_id}&cid=51830095&zzd_from=uc-iflow&uc_param_str=dndsvebichfrntcpgipf'
                        f'&uc_biz_str=S:custom|C:comment|N:true'
                    }
                    url = f'http://sp-iflow.uc.cn/iflow/api/v2/cmt/article/{com_item_id}/comments/byhot'
                    # 对评论页面发起访问
                    com = requests.get(url=url, headers=headers)
                    com_json = json.loads(com.text)['data']
                    # 点赞数
                    like_num = com_json.get('like_cnt', 0)
                    # 评论数
                    comm = com_json.get('comment_cnt', 0)
                else:
                    raise Exception
                now = int(time.time())
                time_10 = now
                time_13 = now * 1000
                work = {
                    "_id": _id,
                    "status": status,
                    "mediaType": self.media_type,
                    "mediaName": self.media_name,
                    "accountType": account_dict["accountType"],
                    "mediaUid": account_dict["mediaUid"],
                    "accountId": account_dict["_id"],
                    "accountUrl": account_dict["url"],
                    "avatar": account_dict['avatar'],
                    "mediaWorkId": wid,
                    "updateParams": update_params,
                    "nickName": account_dict['nickName'],
                    "author": account_dict['nickName'],
                    "source": account_dict['nickName'],
                    "url": article_url,
                    "title": title,
                    "digest": "",
                    "content": content,
                    "contentType": content_type,
                    "isOriginal": -1,
                    "topics": [],
                    "audios": [],
                    "covers": covers,
                    "videos": videos,
                    "readNum": 0,
                    "playNum": 0,
                    "likeNum": like_num,
                    "commentNum": comm,
                    "forwardNum": 0,
                    "createTime": pub_time_,
                    "createDateTime": pub_time_13,
                    "pubTime": pub_time_,
                    "pubDateTime": pub_time_13,
                    "updateTime": time_10,
                    "updateDateTime": time_13,
                }
                self._logger.debug(f'采集{account_dict["nickName"]}的作品信息{work}')
                articles_list.append(work)
            except Exception as e:
                self._logger.warning(f"{e}\n{traceback.format_exc()}")
                continue
        return articles_list

    def account_article(self, uid, account_type):
        """
        用来展示账号和对应文章
        :param uid: uid
        :param account_type: 账号类型
        :return: 数据结果
        """
        account = self.account_spider(uid, account_type)
        articles_list = self.article_spider(account)
        return {'code': 1, 'msg': 'ok', 'data': {'account': account, 'works': articles_list}}

    def update_article(self, params):
        """
        通过文章id 查询文章，发现文章的更新数据，比如播放数，点赞数
        :param params:wid
        :return: 返会文章更新数据
        """
        works = dict()
        try:
            # 对文章发起访问
            url = f'https://ff.dayu.com/contents/{params}?biz_id=1002&_fetch_author=1' \
                f'&_incr_fields=click1,click2,click3,click_total,play,like'
            # 对详情页发起访问
            res = requests.get(url=url)
            res_json = json.loads(res.text)['data']
            # 需要再次对评论页面发起访问 点赞和评论
            if '_extra'in res_json and res_json['_extra']:
                com_item_id = res_json['_extra']['xss_item_id']
                headers = {
                    'Referer': f'http://sp-iflow.uc.cn/webapp/webview/xissAllComments?app=uc-iflow'
                    f'&aid={com_item_id}&cid=51830095&zzd_from=uc-iflow&uc_param_str=dndsvebichfrntcpgipf'
                    f'&uc_biz_str=S:custom|C:comment|N:true'
                }
                url = f'http://sp-iflow.uc.cn/iflow/api/v2/cmt/article/{com_item_id}/comments/byhot'
                # 对评论有页面发起访问
                com = requests.get(url=url, headers=headers).text
                com_json = json.loads(com)['data']
                # 点赞数
                if com_json['like_cnt']:
                    works['likeNum'] = com_json['like_cnt']
                else:
                    works['likeNum'] = 0

                if com_json['comment_cnt']:
                    works['commentNum'] = com_json['comment_cnt']
                else:
                    works['commentNum'] = 0
            works['updateTime'] = int(time.time())
            works['updateDateTime'] = int(time.time()) * 1000
            self._logger.info(f'作品更新信息{works}')
            return {'code': 1, 'msg': 'ok', 'data': {'works_update': works}}
        except Exception as e:
            self._logger.warning(f"{e}\n{traceback.format_exc()}")


class DYSpider:

    def __init__(self, logger):
        self.logger = logger

    def run(self, uid):
        return DaYuSpider(log=self.logger).account_article(uid, account_type=2)

    def fetch(self, task):
        try:
            res = self.run(task["platformAccountID"])
            return res
        except Exception as e:
            self.logger.warning(f"{e}\n{traceback.format_exc()}")
            return dict(code=0, msg=str(e))





def get_data(query):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
    }
    url = f'https://m.sm.cn/api/rest?method=Subscribe.feed&q={query}&format=json&page=1'
    try:
        res = requests.get(url=url, headers=headers, proxies=get_abuyun_proxies())
        res_json = json.loads(res.text)
        if res_json['data']:
            res_doc = etree.HTML(res_json['data']['feed_html'])
            accout_tags = res_doc.xpath('//div[@class="cell-wrapper"]')
            result = []
            for accout_tag in accout_tags[:3]:
                try:
                    account_dit = dict()
                    # 昵称
                    usernames = accout_tag.xpath('.//div[@class="info"]//p[@class="title"]/text() '
                                                 '| .//div[@class="info"]//p[@class="title"]/em/text()')
                    if usernames:
                        account_dit["username"] = "".join(usernames)
                    else:
                        continue

                    # 头像
                    avatars = accout_tag.xpath('.//div[@class="img"]/@data-image')
                    if avatars:
                        account_dit["userpicurl"] = avatars[0]
                    else:
                        continue

                    # 首页地址
                    urls = accout_tag.xpath('./a/@href')
                    if urls:
                        account_dit["url"] = urls[0]
                    else:
                        continue

                    # 账号id
                    account_dit["uid"] = account_dit["url"]
                    if "wmId" in account_dit["url"]:
                        wm_ids = re.findall(r'%22wmId%22:%22(.*?)%22', account_dit["url"])
                        if wm_ids:
                            account_dit["uid"] = wm_ids[0]
                        else:
                            continue
                    else:
                        continue

                    # 整合结果。
                    result.append(account_dit)
                    break
                except Exception as e:
                    logger.debug(f"大鱼号搜索，某个逻辑处理失败，{e}")
            return result
        else:
            raise ValueError("未找大鱼号到相关搜索结果")
    except Exception as e:
        logger.warning("{}\n{}".format(e, traceback.format_exc()))


