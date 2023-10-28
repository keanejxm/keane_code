"""

# author: albert
# date: 2021/1/21 14:55
# update: 2021/1/21 14:55
"""
import hashlib
import time
import traceback
from urllib.parse import urljoin
import base64
import re
import bs4
import requests
import json
import random
from zlib import crc32
from api_common_utils.proxy import get_abuyun_proxies


def md5(strsea, charset="UTF-8"):
    # 字符串转md5格式
    md5 = hashlib.md5()
    md5.update(strsea.encode(charset))
    return md5.hexdigest()


def get_user_info(user_id, account_type):
    """
    获取用户信息
    :param user_id:  用户ID
    :param account_type:  用户类型
    :return: 用户数据
    """
    try:
        # url = "https://api5-normal-c-lf.snssdk.com/user/profile/homepage/v7/?user_id={}&iid=3614839634402445&device_id=71626273339&ac=wifi&mac_address=90%3A61%3AAE%3A42%3A7B%3A88&channel=tengxun3&aid=13&app_name=news_article&version_code=775&version_name=7.7.5&device_platform=android&ab_version=660830%2C662176%2C1922063%2C1859936%2C1922091%2C1417598%2C662099%2C1938809%2C668774%2C1895192%2C668775%2C1922340%2C1593455%2C1419597%2C1909220%2C1938830%2C1157750%2C1529247%2C668779%2C1851965%2C1873582%2C1941328&ab_feature=102749%2C94563&ssmix=a&device_type=HUAWEI+MLA-AL10&device_brand=Android&language=zh&os_api=22&os_version=5.1.1&uuid=863064924221239&openudid=49061ae427b88909&manifest_version_code=7750&resolution=900*1600&dpi=320&update_version_code=77510&_rticket=1597228432984&tma_jssdk_version=1.66.0.6&pos=5r_-9Onkv6e_eAw1eBI-eCUfv7G_8fLz-vTp6Pn4v6esrKizqKukra6qraykrqiksb_x_On06ej5-L-nrq6zpKSkqq2trK6tqK6kqKyrsb_88Pzt3vTp5L-nv3gMNXgSPnglH7-xv_zw_O3R8vP69Ono-fi_p6ysqLOoq6StrqqtrKSuqKSxv_zw_O3R_On06ej5-L-nrq6zpKSkqq2trK6tqK6kqKyr4A%3D%3D&rom_version=22&plugin=0&host_abi=armeabi-v7a&cdid=fe7047cd-a9ff-4ec1-8fb6-24c8fd5c6d22".format(
        #     user_id)
        url = f"https://api3-normal-c-lf.snssdk.com/user/profile/homepage/v7/?user_id={user_id}&iid=110941835596&device_id=66270096982&ac=wifi&mac_address=44%3A04%3A44%3A4b%3A22%3A20&channel=oppo-cpa&aid=13&app_name=news_article&version_code=767&version_name=7.6.7&device_platform=android&ab_version=1587772%2C668774%2C857804%2C660830%2C662176%2C1555751%2C1612014%2C1419036%2C668775%2C1529249%2C1556060%2C1190522%2C1157750%2C1413879%2C1419597%2C1439625%2C1612104%2C1469498%2C1592803%2C1484965%2C1576655%2C1593455%2C668779%2C662099%2C1419818%2C1553981&ab_group=100169&ab_feature=102749%2C94563&ssmix=a&device_type=OPPO+A37m&device_brand=OPPO&language=zh&os_api=22&os_version=5.1&uuid=862215034992652&openudid=89b1dba591e39c8d&manifest_version_code=7670&resolution=720*1280&dpi=320&update_version_code=76711&_rticket=1586414663301&plugin=18762&tma_jssdk_version=1.58.0.3&pos=5r_-9Onkv6e_egIueDMreCcZeCUfv7G_8fLz-vTp6Pn4v6esrKmzqKylrKyxv_H86fTp6Pn4v6eupbOtrqmlqauxv_zw_O3e9Onkv6e_egIueDMreCcZeCUfv7G__PD87dHy8_r06ej5-L-nrKyps6ispayssb_88Pzt0fzp9Ono-fi_p66ls62uqaWpq-A%3D&rom_version=coloros_v3.0.0_a37m_11_a.08_160616&cdid=0f2d6b28-2373-4629-8c0b-e59d9d3f9fb0"
        headers = {
            "User-Agent": "com.ss.android.article.news/7670 (Linux; U; Android 5.1; zh_CN; OPPO A37m; Build/LMY47I; Cronet/TTNetVersion:3154e555 2020-03-04 QuicVersion:8fc8a2f3 2020-03-02)",
        }
        r = requests.get(url, headers=headers)
        returndict = json.loads(r.text)["data"]
        user_name = returndict["name"]
        user_avatar_url = returndict.get("big_avatar_url")
        user_url = returndict.get("name_card")["card_share_url"]
        gender = 0
        if returndict.get("gender"):
            gender = returndict.get("gender")
        province = ''
        city = ''
        if returndict.get("area"):
            city_str = returndict.get("area")
            if '省' in city_str:
                province = city_str[:city_str.index('省') + 1]
                city = city_str[city_str.index('省') + 1:]
            elif '区' in city_str:
                province = city_str[:city_str.index('区') + 1]
                city = city_str[city_str.index('区') + 1:]
            elif '市' in city_str:
                province = ''
                city = city_str
        words_num = int(returndict.get("publish_count"))
        follo_num = int(returndict.get("followings_count"))
        fans_num = int(returndict.get("followers_count"))
        zan_num = int(returndict.get("digg_count"))

        user_info = {
            "mediaType": 3,
            "mediaName": "头条号",
            "accountType": account_type,
            "_id": md5('3' + str(user_id) + str(account_type)),
            "mediaUid": str(user_id),
            "nickName": user_name,
            "avatar": urljoin(url, str(user_avatar_url).strip()),
            "url": user_url,
            "gender": int(gender),
            "province": province,
            "city": city,
            "fanNum": int(fans_num),
            "followNum": int(follo_num),
            "mediaWorkNum": int(words_num),
            "mediaReadNum": 0,
            "mediaCommentNum": 0,
            "mediaForwardNum": 0,
            "AII": 0,
            "AFCI": 0,
            "mediaLikeNum": int(zan_num),
            "createTime": int(time.time()),
            "createDateTime": int(time.time() * 1000),
            "updateTime": int(time.time()),
            "updateDateTime": int(time.time() * 1000),
        }
        return user_info
    except Exception as e:
        print(f"{e}\n{traceback.format_exc()}")
        return False


def get_detail_content(toutiao_detail_id, toutiao_logger):
    """
    获取文章详情
    :param toutiao_detail_id:
    :return: 文章内容
    """
    detailurl = "https://a3.pstatp.com/article/content/24/1/{}/{}/1/0/0/".format(
        toutiao_detail_id, toutiao_detail_id)
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1; OPPO A37m Build/LMY47I) NewsArticle/7.0.9 okhttp/3.10.0.2",
    }
    r = requests.get(detailurl, headers = headers)
    # toutiao_logger.debug(f'请求作品-{toutiao_detail_id}-详情的状态码：{r.status_code}')
    # toutiao_logger.debug(f'请求作品-{toutiao_detail_id}-详情的数据：{r.text}')
    setail_content_dict = json.loads(r.text)
    content = setail_content_dict["data"]
    return content


def get_user_works(user_id, toutiao_logger):
    """
    获取用户作品
    :param user_id: 用户id
    :return:  作品列表
    """
    url = "https://api3-normal-c-lf.snssdk.com/api/feed/profile/v1/"
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1; OPPO A37m Build/LMY47I) NewsArticle/7.0.9 okhttp/3.10.0.2",
    }
    datas = {
        "category": "profile_all",
        "visited_uid": int(user_id),
        "stream_api_version": 88,
        "count": 20,
        "offset": 0,
        "iid": 106816989486,
        "device_id": 66270096982,
        "channel": "oppo-cpa",
        "aid": 13,
        "app_name": "news_article",
        "version_code": 763,
        "device_platform": "android",
        "device_type": "OPPO+A37m",
        "os_version": "5.1",
    }
    r = requests.get(url, headers = headers, params = datas, proxies = get_abuyun_proxies())
    toutiao_logger.debug(f'头条号采集获取id={user_id}-用户的作品列表的状态码-{r.status_code}')
    toutiao_logger.debug(f'头条号采集获取id={user_id}-用户的作品列表返回数据-{r.text}')
    return_dict = json.loads(r.text)
    return_dict_list = return_dict["data"]
    return return_dict_list


def parse_user_article_work(content_dict, user_id, account_type, toutiao_logger):
    """
    解析作品数据
    :param content_dict: 作品数据
    :return: 解析后的数据
    """
    if content_dict.get("group_id"):
        id = content_dict.get("group_id")
    else:
        id = content_dict.get("id")

    content = get_detail_content(id, toutiao_logger)["content"]

    parse_content = content.replace('\n', '')
    img_tag_list = re.compile('<div class="pgc-img">.*?</div>').findall(parse_content)
    new_content = parse_content
    for img_tag in img_tag_list:
        print(img_tag)
        url = re.compile('url=(.*?)"').findall(img_tag)[0].replace('%3A', ':').replace('%2F', '/')
        width = re.compile('width="(.*?)"').findall(img_tag)[0]
        height = re.compile('height="(.*?)"').findall(img_tag)[0]
        new_img_tag = f'<img src="{url}" width="{width}" height="{height}">'
        new_content = new_content.replace(img_tag, new_img_tag)
    content = new_content

    url = content_dict.get("article_url")

    article_type = 1

    is_original = 0
    if content_dict.get("raw_data"):
        is_original = 1

    play_num = 0
    if content_dict.get("video_detail_info"):
        play_num = content_dict.get(
            "video_detail_info").get("video_watch_count")
        if play_num is None:
            play_num = 0

    forward_num = 0
    if content_dict.get("forward_info"):
        forward_num = content_dict.get("forward_info").get("forward_count")

    pub_date_time = 0
    if content_dict.get("publish_time"):
        pub_date_time = int(content_dict.get("publish_time")) * 1000

    covers = []
    if content_dict.get("large_image_list"):
        # covers += [url["url"] for url in content_dict.get("large_image_list")[0]["url_list"]]
        covers.append(content_dict.get("large_image_list")[0]["url"])
        article_type = 2

    read_num = 0
    if content_dict.get("read_count"):
        read_num = content_dict.get("read_count")

    like_count = 0
    if content_dict.get("like_count"):
        like_count = content_dict.get("like_count")

    comment_count = 0
    if content_dict.get("comment_count"):
        comment_count = content_dict.get("comment_count")

    update_params = {
        "mediaWorkId": id
    }

    video = []

    # 增加通过视频id获取视频链接逻辑
    video_id = None
    if content_dict.get("video_id"):
        video_id = content_dict.get("video_id")
        if video_id:
            r = str(random.random())[2:]
            url_part = "/video/urls/v/l/toutiao/mp4/{}?r={}".format(video_id, r)
            s = crc32(url_part.encode())
            url_t = "https://ib.365yg.com{}&s={}".format(url_part, s)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTHL, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
            }
            res = requests.get(url_t, headers = headers).text
            res = json.loads(res)
            res = res["data"]["video_list"]["video_1"]["main_url"]
            video_url = base64.b64decode(res).decode()
            video.append(video_url)

    # 增加将video标签放入content逻辑
    if video:
        video_id_url = "http://toutiao.com/videoid={}".format(video_id)
        soup = bs4.BeautifulSoup(content, "html.parser")
        video_tag = soup.new_tag("video")
        video_tag.attrs.update({"src": video_id_url})
        video_tag.attrs.update({"preload": "true"})
        soup.find("div", {"class": "custom-video"}).insert(1, video_tag)
        content = str(soup).strip()
        article_type=3   #若有视频则文章类型为视频文类型（Keane 2020/11/16）

    user_name = content_dict.get("user_info")["name"]
    user_avatar = content_dict.get("user_info")["avatar_url"]

    work = {
        "mediaType": 3,
        "mediaName": "头条号",
        "accountType": account_type,
        "accountId": md5('3' + str(user_id) + str(account_type)),
        "_id": md5("3" + str(id) + str(account_type)),
        "mediaWorkId": id,
        "author": content_dict.get("source"),
        "title": content_dict.get("title"),
        "digest": content_dict.get("abstract"),
        "url": url,
        "content": content,
        "contentType": article_type,
        "source": content_dict.get("source"),
        "isOriginal": is_original,
        "topics": [],
        "covers": covers,
        "videos": video,
        "readNum": read_num,
        "playNum": play_num,
        "likeNum": like_count,
        "commentNum": comment_count,
        "forwardNum": forward_num,
        "createTime": int(time.time()),
        "createDateTime": int(time.time() * 1000),
        "pubTime": content_dict.get("publish_time"),
        "pubDateTime": pub_date_time,
        "updateTime": int(time.time()),
        "updateDateTime": int(time.time() * 1000),
        "updateParams": json.dumps(update_params),
        "mediaUid": user_id,
        "nickName": user_name,
        "avatar": user_avatar,
        "audios": [],
        "accountUrl": f"http://www.toutiao.com/c/user/{user_id}/",
    }
    return work


def parse_user_article_small_video_work(content_dict, user_id, account_type, toutiao_logger):
    """
    解析作品数据
    :param content_dict: 作品数据
    :return: 解析后的数据
    """
    toutiao_detail_id = content_dict["id"]
    content = get_detail_content(toutiao_detail_id, toutiao_logger)["content"]
    article_type = 5
    url = content_dict.get("display_url")
    id = content_dict.get("id")
    is_original = 0
    if content_dict.get("raw_data"):
        is_original = 1
    play_num = 0
    read_num = 0
    forward_num = 0
    if content_dict.get("raw_data"):
        play_num = content_dict.get("raw_data").get("action").get("play_count")
        read_num = content_dict.get("raw_data").get("action").get("read_count")
        share_count = content_dict.get("raw_data").get(
            "action").get("share_count")
        forward_num = content_dict.get("raw_data").get(
            "action").get("forward_count")
    pub_date_time = 0
    if content_dict.get("raw_data").get("create_time"):
        pub_date_time = int(content_dict.get(
            "raw_data").get("create_time")) * 1000
    covers = []
    if content_dict.get("raw_data"):
        covers = content_dict.get("raw_data")
        if covers.get("first_frame_image_list"):
            covers = covers["first_frame_image_list"][0].get("url")

    like_count = 0
    if content_dict.get("like_count"):
        like_count = content_dict.get("like_count")
    comment_count = 0
    if content_dict.get("comment_count"):
        comment_count = content_dict.get("comment_count")
    update_params = {
        "mediaWorkId": id,
        "article_type": article_type,
    }

    video = []
    videoid = None
    # 修改头条小视频逻辑
    video_small = None
    if content_dict.get("raw_data"):

        # 获取头条小视频videoid
        videoid = content_dict["raw_data"]["video"]["video_id"]

        video_data = content_dict.get("raw_data")
        if video_data:
            video_m = video_data.get("video")
            download_addr = video_m.get("download_addr")
            video_small = download_addr.get("url_list")[0]
            video.append(video_small)
    # 增加将video标签放入content逻辑
    if video:
        video_id_url = "http://toutiao.com/videoid={}".format(videoid)
        soup = bs4.BeautifulSoup(content, "html.parser")
        video_tag = soup.new_tag("video")
        video_tag.attrs.update({"src": video_id_url})
        video_tag.attrs.update({"preload": "true"})
        soup.find("div", {"class": "custom-video"}).insert(1, video_tag)
        content = str(soup).strip()

    user_name = content_dict.get("raw_data")["user"]["info"]["name"]
    user_avatar = content_dict.get("raw_data")["user"]["info"]["avatar_url"]

    work = {
        "mediaType": 3,
        "mediaName": "头条号",
        "accountType": account_type,
        "accountId": md5('3' + str(user_id) + str(account_type)),
        "_id": md5("3" + str(id) + str(account_type)),
        "mediaWorkId": str(id),
        "author": content_dict.get("raw_data").get("user").get("info").get("name"),
        "title": content_dict.get("raw_data").get("title"),
        "digest": content_dict.get("abstract"),
        "url": url,
        "content": content,
        "contentType": article_type,
        "source": content_dict.get("raw_data").get("user").get("info").get("name"),
        "isOriginal": is_original,
        "topics": "",
        "covers": covers,
        "videos": video,
        "readNum": read_num,
        "playNum": play_num,
        "likeNum": like_count,
        "commentNum": comment_count,
        "forwardNum": forward_num,
        "createTime": int(time.time()),
        "createDateTime": int(time.time() * 1000),
        "pubTime": content_dict.get("publish_time"),
        "pubDateTime": pub_date_time,
        "updateTime": int(time.time()),
        "updateDateTime": int(time.time() * 1000),
        "updateParams": json.dumps(update_params),
        "mediaUid": str(user_id),
        "nickName": user_name,
        "avatar": user_avatar,
        "audios": [],
        "accountUrl": f"http://www.toutiao.com/c/user/{user_id}/",
    }
    return work


def parse_user_wei_article_work(content_dict, user_id, account_type, toutiao_logger):
    """
    解析作品数据
    :param content_dict: 作品数据
    :return: 解析后的数据
    """
    if content_dict.get("thread_id"):
        id = content_dict.get("thread_id")
    else:
        id = content_dict.get("repost_params")["fw_id"]

    article_type = 1
    url = ''
    if content_dict.get("share_info").get("share_url"):
        url = content_dict.get("share_info").get("share_url")

    is_original = 0
    if content_dict.get("raw_data"):
        is_original = 1

    play_num = 0
    if content_dict.get("video_detail_info"):
        play_num = content_dict.get(
            "video_detail_info").get("video_watch_count")
        if play_num is None:
            play_num = 0

    forward_num = 0
    if content_dict.get("forward_info"):
        forward_num = content_dict.get("forward_info").get("forward_count")

    pub_date_time = 0
    if content_dict.get("publish_time"):
        pub_date_time = int(content_dict.get("publish_time")) * 1000

    covers = []
    if content_dict.get("large_image_list"):
        # covers += [url["url"] for url in content_dict.get("large_image_list")[0]["url_list"]]
        covers.append(content_dict.get("large_image_list")[0]["url"])
        article_type = 2

    read_num = 0
    if content_dict.get("read_count"):
        read_num = content_dict.get("read_count")

    like_count = 0
    if content_dict.get("digg_count"):
        like_count = content_dict.get("digg_count")

    comment_count = 0
    if content_dict.get("comment_count"):
        comment_count = content_dict.get("comment_count")

    update_params = {
        "mediaWorkId": id,
        "article_type": article_type,
    }

    video = []
    # 增加通过视频id获取视频链接逻辑
    video_id = None
    if content_dict.get("video_id"):
        video_id = content_dict.get("video_id")
        if video_id:
            r = str(random.random())[2:]
            url_part = "/video/urls/v/l/toutiao/mp4/{}?r={}".format(video_id, r)
            s = crc32(url_part.encode())
            url_t = "https://ib.365yg.com{}&s={}".format(url_part, s)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTHL, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
            }
            res = requests.get(url_t, headers = headers).text
            res = json.loads(res)
            res = res["data"]["video_list"]["video_1"]["main_url"]
            video_url = base64.b64decode(res).decode()
            video.append(video_url)
            article_type = 3 #若有视频则视频类型为视频文（Keane 2020/11/16）

    # 增加将video标签放入content逻辑
    content = content_dict.get("content")
    if video:
        video_id_url = "http://toutiao.com/videoid={}".format(video_id)
        soup = bs4.BeautifulSoup(content, "html.parser")
        video_tag = soup.new_tag("video")
        video_tag.attrs.update({"src": video_id_url})
        video_tag.attrs.update({"preload": "true"})
        soup.find("div", {"class": "custom-video"}).insert(1, video_tag)
        content = str(soup).strip()

    user_name = content_dict.get("user")["name"]
    user_avatar = content_dict.get("user")["avatar_url"]
    content_size = len(content_dict.get("content"))
    if content_size >= 30:
        title = content_dict.get("content")[0:29]
    else:
        title = content_dict.get("content")
    work = {
        "mediaType": 3,
        "mediaName": "头条号",
        "accountType": account_type,
        "accountId": md5('3' + str(user_id) + str(account_type)),
        "_id": md5("3" + str(id) + str(account_type)),
        "mediaWorkId": str(id),
        "author": user_name,
        "url": url,
        "title": title,
        "digest": content_dict.get("abstract"),
        "content": content,
        "contentType": article_type,
        "source": user_name,
        "isOriginal": is_original,
        "topics": "",
        "covers": covers,
        "videos": video,
        "readNum": read_num,
        "playNum": play_num,
        "likeNum": like_count,
        "commentNum": comment_count,
        "forwardNum": forward_num,
        "createTime": int(time.time()),
        "createDateTime": int(time.time() * 1000),
        "pubTime": content_dict.get("publish_time"),
        "pubDateTime": pub_date_time,
        "updateTime": int(time.time()),
        "updateDateTime": int(time.time() * 1000),
        "updateParams": json.dumps(update_params),
        "mediaUid": str(user_id),
        "nickName": user_name,
        "avatar": user_avatar,
        "audios": [],
        "accountUrl": f"http://www.toutiao.com/c/user/{user_id}/",
    }
    return work


def parse_user_xg_video(content_dict, user_id, account_type, toutiao_logger):
    """
    解析视频作品数据
    :param content_dict: 作品数据
    :return: 解析后的数据
    """
    toutiao_detail_id = content_dict["item_id"]

    content = get_detail_content(toutiao_detail_id, toutiao_logger)["content"]
    url = content_dict.get("display_url")

    article_type = 4

    id = content_dict.get("item_id")

    is_original = 0
    if content_dict.get("raw_data"):
        is_original = 1

    play_num = 0
    if content_dict.get("video_detail_info"):
        play_num = content_dict.get(
            "video_detail_info").get("video_watch_count")

    forward_num = 0
    if content_dict.get("forwardNum"):
        forward_num = content_dict.get("forwardNum").get("forward_count")

    pub_date_time = 0
    if content_dict.get("publish_time"):
        pub_date_time = int(content_dict.get("publish_time")) * 1000

    covers = []
    if content_dict.get("large_image_list"):
        # covers += [url["url"] for url in content_dict.get("large_image_list")[0]["url_list"]]
        covers.append(content_dict.get("large_image_list")[0]["url"])

    read_num = 0
    if content_dict.get("read_count"):
        read_num = content_dict.get("read_count")

    like_count = 0
    if content_dict.get("like_count"):
        like_count = content_dict.get("like_count")

    comment_count = 0
    if content_dict.get("comment_count"):
        comment_count = content_dict.get("comment_count")

    update_params = {
        "mediaWorkId": id,
        "article_type": article_type,
    }

    video = []

    # 增加通过视频id获取视频链接逻辑
    video_id = None
    if content_dict.get("video_id"):
        video_id = content_dict.get("video_id")
        if video_id:
            r = str(random.random())[2:]
            url_part = "/video/urls/v/l/toutiao/mp4/{}?r={}".format(video_id, r)
            s = crc32(url_part.encode())
            url_t = "https://ib.365yg.com{}&s={}".format(url_part, s)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTHL, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
            }
            res = requests.get(url_t, headers = headers).text
            res = json.loads(res)
            res = res["data"]["video_list"]["video_1"]["main_url"]
            video_url = base64.b64decode(res).decode()
            video.append(video_url)

    # 增加将video加入content逻辑

    if video:
        video_id_url = "http://toutiao.com/videoid={}".format(video_id)
        soup = bs4.BeautifulSoup(content, "html.parser")
        video_tag = soup.new_tag("video")
        video_tag.attrs.update({"src": video_id_url})
        video_tag.attrs.update({"preload": "true"})
        soup.find("div", {"class": "custom-video"}).insert(1, video_tag)
        content = str(soup).strip()

    user_name = content_dict.get("user_info")["name"]
    user_avatar = content_dict.get("user_info")["avatar_url"]

    work = {
        "mediaType": 3,
        "mediaName": "头条号",
        "accountType": account_type,
        "accountId": md5('3' + str(user_id) + str(account_type)),
        "_id": md5("3" + str(id) + str(account_type)),
        "mediaWorkId": str(id),
        "author": content_dict.get("source"),
        "title": content_dict.get("title"),
        "url": url,
        "digest": content_dict.get("abstract"),
        "content": content,
        "contentType": article_type,
        "source": content_dict.get("source"),
        "isOriginal": is_original,
        "topics": "",
        "covers": covers,
        "videos": video,
        "readNum": read_num,
        "playNum": play_num,
        "likeNum": like_count,
        "commentNum": comment_count,
        "forwardNum": forward_num,
        "createTime": int(time.time()),
        "createDateTime": int(time.time() * 1000),
        "pubTime": content_dict.get("publish_time"),
        "pubDateTime": pub_date_time,
        "updateTime": int(time.time()),
        "updateDateTime": int(time.time() * 1000),
        "updateParams": json.dumps(update_params),
        "mediaUid": str(user_id),
        "nickName": user_name,
        "avatar": user_avatar,
        "audios": [],
        "accountUrl": f"http://www.toutiao.com/c/user/{user_id}/",
    }
    return work


def parse_user_work(content_dict, user_id, account_type, toutiao_logger):
    """
    对用的作品进行解析
    :param content_dict: 用户的作品数据
    :return: 解析后的作品数据
    """
    # -* 视频文章 *-
    if content_dict.get("article_type") == 2:
        return parse_user_xg_video(content_dict, user_id, account_type, toutiao_logger)

    # -* 文章 *-
    elif content_dict.get("aggr_type") == 1:
        return parse_user_article_work(content_dict, user_id, account_type, toutiao_logger)

    # -* 微头条 *-
    elif content_dict.get("user") and content_dict.get("group_source") == 5:
        return parse_user_wei_article_work(content_dict, user_id, account_type, toutiao_logger)

    # -* 小视频 *-
    elif content_dict.get("raw_data"):
        return parse_user_article_small_video_work(content_dict, user_id, account_type, toutiao_logger)


def get_user_data(user_id, account_type, toutiao_logger):
    """
    获取用户作品列表并解析
    :param user_id: 用户ID
    :return: 解析后的用户作品列表
    """
    works = get_user_works(user_id, toutiao_logger)
    result_list = []
    for work in works:
        try:
            content_dict = json.loads((work.get("content")))
            parse_work = parse_user_work(content_dict, user_id, account_type, toutiao_logger)
            result_list.append(parse_work)
        except Exception as e:
            continue
    return result_list


def get_media_user_work_info(user_id, toutiao_logger):
    """
    获取账户信息
    :param user_id:  用户ID
    :return: 用户的数据
    """
    account_type = 2

    user_info = get_user_info(user_id, account_type)

    result_list = get_user_data(user_id, account_type, toutiao_logger)

    if not user_info:
        result_data = {
            "code": 0,
            "msg": "error",
            "data": {
                "account": "",
                "works": result_list}}
        return result_data
    result_data = {
        "code": 1,
        "msg": "ok",
        "data": {
            "account": user_info,
            "works": result_list}}
    return result_data


class TTSpider:

    def __init__(self, logger):
        self.logger = logger

    def run(self, user_id):
        return get_media_user_work_info(user_id=user_id, toutiao_logger=self.logger)

    def fetch(self, task):
        try:
            res = self.run(task["platformAccountID"])
            return res
        except Exception as e:
            self.logger.warning(f"{e}\n{traceback.format_exc()}")
            return dict(code=0, msg=str(e))


if __name__ == '__main__':
    from loguru import logger
    user_id = "54804078351"
    res = TTSpider(logger).run(user_id)
    print(res)


