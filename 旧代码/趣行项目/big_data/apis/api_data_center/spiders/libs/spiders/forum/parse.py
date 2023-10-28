# -*- coding:utf-8 -*-
"""

# author: albert
# date: 2020/12/28
# update: 2020/12/28
"""
import json
import re
import time
import hashlib
import elasticsearch
from lxml import etree
import traceback
from api.config import es_config
from api_common_utils.base_data import *
from api_common_utils.text_processing_tools import text_remover_html_tag
from .download import downloader
from loguru import logger


def md5(unicode_str, charset="UTF-8"):
    """
    字符串转md5格式。
    :return:
    """
    _md5 = hashlib.md5()
    _md5.update(unicode_str.encode(charset))
    return _md5.hexdigest()


def dc_forum_from_es(task, result):
    es_conn = elasticsearch.Elasticsearch(**es_config)
    query_data = {
        "size": 100,
        "query": {
            "term": {
                "parentID": task["_id"]
            }
        }
    }
    res = es_conn.search(index="dc_forum", body=query_data)
    forum_list = []
    forum_result = {"dc_forum": forum_list}
    for scroll_hit in res['hits']['hits']:
        scroll_hit['_source']['_id'] = scroll_hit['_id']
        forum_list.append(scroll_hit['_source'])
    return forum_result


def dc_forum(task, result):
    html = etree.HTML(result)
    class_items_list = html.xpath('//div[@class="ba_list clearfix"]/div')
    platform_id = task["platformID"]
    platform_name = task["platformName"]
    source_types_name = task["sourceTypesName"]
    parentID = task["_id"]
    parentName = task["name"]
    forum_list = []
    forum_result = {"dc_forum": forum_list}
    for item in class_items_list:
        now = int(time.time() * 1000)
        class_dict = dict(dict(), **DEFAULT_FORUM_FIELDS)
        s_class_name = item.xpath('.//p[@class="ba_name"]/text()')[0]
        logo = item.xpath('.//img/@src')[0]
        s_class_url = 'http://tieba.baidu.com' + item.xpath('./a/@href')[0]
        introduction =item.xpath('.//p[@class="ba_desc"]/text()')[0] if item.xpath('.//p[@class="ba_desc"]/text()') else ''
        follows_num = int(item.xpath('.//span[@class="ba_m_num"]/text()')[0])
        works_num = int(item.xpath('.//span[@class="ba_m_num"]/text()')[0])
        forum_id = s_class_name
        s_class_id = md5(platform_id + forum_id)
        class_dict["_id"] = s_class_id
        class_dict["platformID"] = platform_id
        class_dict["platformName"] = platform_name
        class_dict["sourceTypesName"] = source_types_name
        class_dict["name"] = s_class_name
        class_dict["forumId"] = forum_id
        class_dict["introduction"] = introduction
        class_dict["logo"] = logo
        class_dict["url"] = s_class_url
        class_dict["region"] = ""
        class_dict["type"] = 6
        class_dict["parentID"] = parentID
        class_dict["parentName"] = parentName
        class_dict["levelNumber"] = 3
        class_dict["followsNum"] = follows_num
        class_dict["worksNum"] = works_num
        class_dict["createTime"] = now
        class_dict["updateTime"] = now
        logger.debug(class_dict)
        forum_list.append(class_dict)
    return forum_result


def dc_hot_forum(task, result):
    res_dict = result["data"]["bang_topic"]["topic_list"]
    platform_id = task["platformID"]
    platform_name = task["platformName"]
    source_types_name = task["sourceTypesName"]
    parentID = task["_id"]
    parentName = task["name"]
    forum_list = []
    forum_result = {"dc_forum": forum_list}
    for topic in res_dict:
        now = int(time.time() * 1000)
        class_dict = dict(dict(), **DEFAULT_FORUM_FIELDS)
        class_name = topic["topic_name"]
        class_url = topic["topic_url"].replace('amp;', '')
        forum_id = str(topic["topic_id"])
        class_id = md5(platform_id + forum_id)
        class_dict["_id"] = class_id
        class_dict["platformID"] = platform_id
        class_dict["platformName"] = platform_name
        class_dict["sourceTypesName"] = source_types_name
        class_dict["name"] = class_name
        class_dict["forumId"] = forum_id
        class_dict["introduction"] = topic["topic_desc"]
        class_dict["logo"] = topic["topic_pic"]
        class_dict["url"] = class_url
        class_dict["region"] = ""
        class_dict["type"] = 6
        class_dict["parentID"] = parentID
        class_dict["parentName"] = parentName
        class_dict["levelNumber"] = 4
        class_dict["followsNum"] = 0
        class_dict["worksNum"] = int(topic["discuss_num"])
        class_dict["createTime"] = now
        class_dict["updateTime"] = now
        logger.debug(class_dict)
        forum_list.append(class_dict)
    return forum_result


def dc_forum_details(task, result):
    platform_id = task["platformID"]
    platform_name = task["platformName"]
    parent_id = task["_id"]
    parent_name = task["name"]
    html = etree.HTML(result)
    html_str = html.xpath('//code[@id="pagelet_html_frs-list/pagelet/thread_list"]/node()')[0]
    html = etree.HTML(str(html_str).replace("<!--", "").replace("-->", ""))
    class_items_list = html.xpath('//ul[@id="thread_list"]/li[@class=" j_thread_list clearfix"]')
    if not class_items_list:
        class_items_list = html.xpath('//ul[@id="thread_list"]/li')
    top_topic = html.xpath('//li[@class=" j_thread_list thread_top j_thread_list clearfix"]')
    if not top_topic:
        top_topic = html.xpath('//ul[@id="thread_top_list"]/li')
    dc_forum_details_list = []
    forum_result = {"dc_forum_details": dc_forum_details_list}
    # 处理置顶
    for it in top_topic:
        try:
            now = int(time.time() * 1000)
            work = dict(dict(), **DEFAULT_FORUM_DETAILS_FIELDS)
            href = it.xpath('.//div[@class="threadlist_lz clearfix"]//a/@href')[0]
            platformWorksID = href.split('/')[-1]
            _id = md5(platform_id + platformWorksID)
            accountName = it.xpath('.//span[@class="frs-author-name-wrap"]/a/text()')[0]
            accountUrl = "https://tieba.baidu.com" + it.xpath('.//span[@class="frs-author-name-wrap"]/a/@href')[0]
            url = "https://tieba.baidu.com" + href
            authors = it.xpath('.//span[@class="frs-author-name-wrap"]/a/text()')
            title = it.xpath('.//div[@class="threadlist_lz clearfix"]//a/text()')[0]
            titleWordsNum = len(title)
            response = downloader(url)
            xpath_html = etree.HTML(response)
            # question = xpath_html.xpath('//h1/text()')[0]
            question = title
            # html = response
            digest = title
            digestOriginal = title
            isOriginal = 1
            isTop = 1
            items = xpath_html.xpath('//div[@class="p_postlist"]/div')
            oneAnswer = ""
            images = []
            video = []
            contentType = 1
            answer = ""
            commentNum = int(xpath_html.xpath('//li[@class="l_reply_num"]/span[1]/text()')[0])
            updateParams = json.dumps({"url": url})
            for item in items:
                con_str = etree.tostring(item, encoding='utf-8').decode("utf-8")
                con_str = "".join(con_str.split())
                if '广告' in con_str:
                    continue
                content = item.xpath('.//cc/div[2]')[0]
                content_str = etree.tostring(content, encoding='utf-8').decode('utf-8')
                if items.index(item) == 0 or items.index(item) == 1:
                    oneAnswer += '\n<br>' + content_str
                    if 'image' in content_str:
                        contentType = 2
                        images = content.xpath('.//img//@src')
                    if 'video' in content_str:
                        contentType = 3
                        video = content.xpath('.//embed//@data-video')
                answer += "\n<br>" + content_str
            pubTime = re.compile('\d+-\d+-\d+ \d+:\d+').findall(response)[0]
            data_sj = time.strptime(pubTime, "%Y-%m-%d %H:%M")
            pubTime = int(time.mktime(data_sj)) * 1000
            work["_id"] = _id
            work["platformID"] = platform_id
            work["platformName"] = platform_name
            work["parentID"] = parent_id
            work["parentName"] = parent_name
            work["platformWorksID"] = platformWorksID
            work["accountName"] = accountName
            work["accountUrl"] = accountUrl
            work["url"] = url
            work["authors"] = authors
            work["title"] = title
            work["titleWordsNum"] = titleWordsNum
            work["question"] = question
            # work["html"] = html
            work["digest"] = digest
            work["digestOriginal"] = digestOriginal
            work["isOriginal"] = isOriginal
            work["isTop"] = isTop
            work["oneAnswer"] = oneAnswer
            work["answer"] = answer
            work["contentType"] = contentType
            work["images"] = images
            work["videos"] = video
            work["commentNum"] = commentNum
            work["updateParams"] = updateParams
            work["pubTime"] = pubTime
            work["createTime"] = now
            work["updateTime"] = now
            logger.debug(work)
            dc_forum_details_list.append(work)
        except Exception as e:
            logger.warning(f'{e}\n{traceback.format_exc()}')
            continue
    for it in class_items_list:
        try:
            now = int(time.time() * 1000)
            work = dict(dict(), **DEFAULT_FORUM_DETAILS_FIELDS)
            href = it.xpath('.//div[@class="threadlist_lz clearfix"]//a/@href')[0]
            platformWorksID = href.split('/')[-1]
            _id = md5(platform_id + platformWorksID)
            accountName = it.xpath('.//span[@class="frs-author-name-wrap"]/a/text()')[0]
            accountUrl = "https://tieba.baidu.com" + it.xpath('.//span[@class="frs-author-name-wrap"]/a/@href')[0]
            url = "https://tieba.baidu.com" + href
            authors = it.xpath('.//span[@class="frs-author-name-wrap"]/a/text()')
            title = it.xpath('.//div[@class="threadlist_lz clearfix"]//a/text()')[0]
            titleWordsNum = len(title)
            response = downloader(url)
            xpath_html = etree.HTML(response)
            # question = xpath_html.xpath('//h1/text()')[0]
            question = title
            # html = response
            digest = title
            digestOriginal = title
            isOriginal = 1
            isTop = 0
            items = xpath_html.xpath('//div[@class="p_postlist"]/div')
            oneAnswer = ""
            images = []
            video = []
            contentType = -1
            answer = ""
            commentNum = 0
            if xpath_html.xpath('//li[@class="l_reply_num"]/span[1]/text()'):
                commentNum = int(xpath_html.xpath('//li[@class="l_reply_num"]/span[1]/text()')[0])
            updateParams = json.dumps({"url": url})
            for item in items:
                con_str = etree.tostring(item, encoding='utf-8').decode("utf-8")
                con_str = "".join(con_str.split())
                if '广告' in con_str:
                    continue
                content = item.xpath('.//cc/div[2]')[0]
                content_str = etree.tostring(content, encoding='utf-8').decode('utf-8')
                if items.index(item) == 0 or items.index(item) == 1:
                    oneAnswer += '\n<br>' + content_str
                    if 'image' in content_str:
                        contentType = 2
                        images = content.xpath('.//img//@src')
                    if 'video' in content_str:
                        contentType = 3
                        video = content.xpath('.//embed//@data-video')
                answer = answer + "\n<br>" + content_str
            pubTime = re.compile('\d+-\d+-\d+ \d+:\d+').findall(response)[0]
            data_sj = time.strptime(pubTime, "%Y-%m-%d %H:%M")
            pubTime = int(time.mktime(data_sj)) * 1000
            work["_id"] = _id
            work["platformID"] = platform_id
            work["platformName"] = platform_name
            work["parentID"] = parent_id
            work["parentName"] = parent_name
            work["platformWorksID"] = platformWorksID
            work["accountName"] = accountName
            work["accountUrl"] = accountUrl
            work["url"] = url
            work["authors"] = authors
            work["title"] = title
            work["titleWordsNum"] = titleWordsNum
            work["question"] = question
            # work["html"] = html
            work["digest"] = digest
            work["digestOriginal"] = digestOriginal
            work["isOriginal"] = isOriginal
            work["isTop"] = isTop
            work["oneAnswer"] = oneAnswer
            work["answer"] = answer
            work["contentType"] = contentType
            work["images"] = images
            work["videos"] = video
            work["commentNum"] = commentNum
            work["updateParams"] = updateParams
            work["pubTime"] = pubTime
            work["createTime"] = now
            work["updateTime"] = now
            logger.debug(work)
            dc_forum_details_list.append(work)
        except Exception as e:
            logger.warning(f'{e}\n{traceback.format_exc()}')
            continue
    return forum_result


def dc_forum_hot_details(task, result):
    platform_id = task["platformID"]
    platform_name = task["platformName"]
    parent_id = task["_id"]
    parent_name = task["name"]
    html = etree.HTML(result)
    items = html.xpath('//li[@class="thread-item"]')
    dc_forum_details_list = []
    forum_result = {"dc_forum_details": dc_forum_details_list}
    for it in items:
        try:
            now = int(time.time() * 1000)
            work = dict(dict(), **DEFAULT_FORUM_DETAILS_FIELDS)
            href = it.xpath('.//div[@class="center"]/a/@href')[0]
            platformWorksID = href.split('/')[-1]
            _id = md5(platform_id + platformWorksID)
            accountName = it.xpath('.//p[@class="author-info"]/a/text()')[0].strip()
            accountUrl = "https://tieba.baidu.com" + it.xpath('.//p[@class="author-info"]/a/@href')[0]
            url = "https://tieba.baidu.com" + href
            authors = it.xpath('.//p[@class="author-info"]/a/text()')[0].strip()
            title = it.xpath('.//div[@class="center"]/a/text()')[0]
            titleWordsNum = len(title)
            response = downloader(url)
            xpath_html = etree.HTML(response)
            question = title
            # html = response
            digest = title
            digestOriginal = title
            isOriginal = 1
            isTop = 0
            items = xpath_html.xpath('//div[@class="p_postlist"]/div')
            oneAnswer = ""
            images = []
            video = []
            contentType = -1
            answer = ""
            # commentNum = int(xpath_html.xpath('//li[@class="l_reply_num"]/span[1]/text()')[0])
            commentNum = re.compile('<span class="red" style="margin-right:3px">(\d+)</span>').findall(response)
            commentNum = int(commentNum[0]) if commentNum else 0
            updateParams = json.dumps({"url": url})
            for item in items:
                con_str = etree.tostring(item, encoding='utf-8').decode("utf-8")
                con_str = "".join(con_str.split())
                if '广告' in con_str:
                    continue
                content = item.xpath('.//cc/div[2]')[0]
                content_str = etree.tostring(content, encoding='utf-8').decode('utf-8')
                if items.index(item) == 0 or items.index(item) == 1:
                    oneAnswer += '\n<br>' + content_str
                    if 'image' in content_str:
                        contentType = 2
                        images = content.xpath('.//img//@src')
                    if 'video' in content_str:
                        contentType = 3
                        video = content.xpath('.//embed//@data-video')
                answer = answer + "\n<br>" + content_str
            pubTime = re.compile('\d+-\d+-\d+ \d+:\d+').findall(response)[0]
            data_sj = time.strptime(pubTime, "%Y-%m-%d %H:%M")
            pubTime = int(time.mktime(data_sj)) * 1000
            work["_id"] = _id
            work["platformID"] = platform_id
            work["platformName"] = platform_name
            work["parentID"] = parent_id
            work["parentName"] = parent_name
            work["platformWorksID"] = platformWorksID
            work["accountName"] = accountName
            work["accountUrl"] = accountUrl
            work["url"] = url
            work["authors"] = authors
            work["title"] = title
            work["titleWordsNum"] = titleWordsNum
            work["question"] = question
            # work["html"] = html
            work["digest"] = digest
            work["digestOriginal"] = digestOriginal
            work["isOriginal"] = isOriginal
            work["isTop"] = isTop
            work["oneAnswer"] = oneAnswer
            work["answer"] = answer
            work["contentType"] = contentType
            work["images"] = images
            work["videos"] = video
            work["commentNum"] = commentNum
            work["updateParams"] = updateParams
            work["pubTime"] = pubTime
            work["createTime"] = now
            work["updateTime"] = now
            logger.debug(work)
            dc_forum_details_list.append(work)
        except Exception as e:
            logger.warning(f'{e}\n{traceback.format_exc()}')
            continue
    return forum_result


def dc_zhifu_forum_details(task, result):
    platform_id = task["platformID"]
    platform_name = task["platformName"]
    parent_id = task["_id"]
    parent_name = task["name"]
    html = etree.HTML(result)
    topic_item_list = html.xpath('//div[@class="List-item TopicFeedItem"]')
    dc_forum_details_list = []
    forum_result = {"dc_forum_details": dc_forum_details_list}
    for topic_item in topic_item_list:
        work = dict(dict(), **DEFAULT_FORUM_DETAILS_FIELDS)

        url = 'http:' + topic_item.xpath('.//h2//a/@href')[0]
        title = topic_item.xpath('.//h2//a/text()')[0]
        user_name = topic_item.xpath('.//div[@class="ContentItem-meta"]/div/meta[1]/@content')[0]
        # user_image = topic_item.xpath('.//div[@class="ContentItem-meta"]/div/meta[2]/@content')[0]
        user_url = topic_item.xpath('.//div[@class="ContentItem-meta"]/div/meta[3]/@content')[0]
        like_num = topic_item.xpath('.//meta[@itemprop="upvoteCount"]/@content')[0] if topic_item.xpath(
            './div[@class="ContentItem AnswerItem"]/meta[@itemprop="upvoteCount"]/@content') else 1
        comment_count = topic_item.xpath('.//meta[@itemprop="commentCount"]/@content')[0]

        response = downloader(url)

        json_dump_data = str(json.loads(
            re.compile('<script id="js-initialData" type="text/json">(.*?)</script>').findall(response)[0]))
        # 两种文章类型 一种是文章 一种是提问
        collectNum = 0
        read_num = 0
        if '/p' in url:
            # 是文章
            content = re.compile("content':.(.*?).'adminClosedComment").findall(json_dump_data)[0]
            excerpt = re.compile("excerpt':.(.*?).'created").findall(json_dump_data)[0]
            platformWorksID = url.split('/')[-1]
            parse_content = text_remover_html_tag(content)
            digest = parse_content[:200]
            work["content"] = content
        elif '/q' in url:
            # 是提问
            content = re.compile("detail':.(.*?).'editableDetail").findall(json_dump_data)[0] + \
                      re.compile("content':.(.*?).'collapsedBy").findall(json_dump_data)[0]
            excerpt = re.compile("detail':.(.*?).'editableDetail").findall(json_dump_data)[0]
            platformWorksID = url.split('/')[-3]
            read_num = int(re.compile("visitCount':(.*?),").findall(json_dump_data)[0])
            collectNum = int(re.compile("followerCount':(.*?),").findall(json_dump_data)[0])
            digest = title
            work["question"] = excerpt
            work["oneAnswer"] = content
            work["answer"] = content

        else:
            content = response
            platformWorksID = int(re.compile("id':(.*?),'title").findall(json_dump_data)[0])
            digest = excerpt = title

        contentType = 1
        images = []
        if 'image' in content:
            contentType = 2
            html = etree.HTML(content)
            images = html.xpath('.//img//@src')
        video = []
        covers = []
        if 'video' in content:
            contentType = 3
            html = etree.HTML(content)
            video = html.xpath('.//a[@class="video-link"]/@href')
            covers = html.xpath('.//a[@class="video-link"]/@data-poster')
        pubTime = int(re.compile("created':(.*?),").findall(json_dump_data)[0]) * 1000
        work["_id"] = md5(str(platform_id) + str(platformWorksID))
        work["platformID"] = platform_id
        work["platformName"] = platform_name
        work["parentID"] = parent_id
        work["parentName"] = parent_name
        work["platformWorksID"] = platformWorksID
        work["accountName"] = user_name
        work["accountUrl"] = user_url
        work["url"] = url
        work["authors"] = [user_name]
        work["title"] = title
        work["titleWordsNum"] = len(title)
        # work["html"] = html
        work["digest"] = digest
        work["digestOriginal"] = excerpt
        work["contentType"] = contentType
        work["images"] = images
        work["videos"] = video
        work["covers"] = covers
        work["readNum"] = read_num
        work["likeNum"] = like_num
        work["commentNum"] = comment_count
        work["collectNum"] = collectNum
        work["updateParams"] = json.dumps({"url": url})
        work["pubTime"] = pubTime
        work["createTime"] = int(time.time() * 1000)
        work["updateTime"] = int(time.time() * 1000)
        logger.debug(work)
        dc_forum_details_list.append(work)

    return forum_result


def dc_zhihu_hot_forum(task, result):
    html = etree.HTML(result)
    platform_id = task["platformID"]
    platform_name = task["platformName"]
    source_types_name = task["sourceTypesName"]
    parentID = task["_id"]
    parentName = task["name"]
    forum_list = []
    forum_result = {"dc_forum": forum_list}
    items = html.xpath('//main/div//a')
    for topic in items:
        now = int(time.time() * 1000)
        class_dict = dict(dict(), **DEFAULT_FORUM_FIELDS)
        class_name = topic.xpath('.//h1/text()')[0]
        class_url = topic.xpath('./@href')[0]
        forum_id = str(topic.xpath('./@href')[0].split('/')[-1])
        class_id = md5(platform_id + forum_id)
        class_dict["_id"] = class_id
        class_dict["platformID"] = platform_id
        class_dict["platformName"] = platform_name
        class_dict["sourceTypesName"] = source_types_name
        class_dict["name"] = class_name
        class_dict["forumId"] = forum_id
        class_dict["introduction"] = topic.xpath('.//div[@class="css-1o6sw4j"]/text()')[0] if topic.xpath(
            './/div[@class="css-1o6sw4j"]/text()') else ''
        class_dict["logo"] = topic.xpath('.//img/@src')[0] if topic.xpath('.//img/@src') else ''
        class_dict["url"] = class_url
        class_dict["region"] = ""
        class_dict["type"] = 6
        class_dict["parentID"] = parentID
        class_dict["parentName"] = parentName
        class_dict["levelNumber"] = 4
        class_dict["followsNum"] = 0
        class_dict["worksNum"] = int(topic.xpath('.//div[@class="css-1ixcu37"]/text()')[0].replace(' 万热度', '0000'))
        class_dict["createTime"] = now
        class_dict["updateTime"] = now
        logger.debug(class_dict)
        forum_list.append(class_dict)
    return forum_result


def dc_zhihu_forum_hot_details(task, result):
    platform_id = task["platformID"]
    platform_name = task["platformName"]
    parent_id = task["_id"]
    parent_name = task["name"]
    dc_forum_details_list = []
    forum_result = {"dc_forum_details": dc_forum_details_list}

    work = dict(dict(), **DEFAULT_FORUM_DETAILS_FIELDS)

    url = task["url"]
    title = task["name"]
    # user_name = topic_item.xpath('.//div[@class="ContentItem-meta"]/div/meta[1]/@content')[0]
    # user_image = topic_item.xpath('.//div[@class="ContentItem-meta"]/div/meta[2]/@content')[0]
    # user_url = topic_item.xpath('.//div[@class="ContentItem-meta"]/div/meta[3]/@content')[0]
    # like_num = topic_item.xpath('.//meta[@itemprop="upvoteCount"]/@content')[0] if topic_item.xpath(
    #     './div[@class="ContentItem AnswerItem"]/meta[@itemprop="upvoteCount"]/@content') else 1
    # comment_count = topic_item.xpath('.//meta[@itemprop="commentCount"]/@content')[0]

    response = result

    json_dump_data = str(json.loads(
        re.compile('<script id="js-initialData" type="text/json">(.*?)</script>').findall(response)[0]))
    # 两种文章类型 一种是文章 一种是提问
    collectNum = 0
    read_num = 0
    if '/p' in url:
        # 是文章
        content = re.compile("content':.(.*?).'adminClosedComment").findall(json_dump_data)[0]
        excerpt = re.compile("excerpt':.(.*?).'created").findall(json_dump_data)[0]
        platformWorksID = url.split('/')[-1]
        parse_content = text_remover_html_tag(content)
        digest = parse_content[:200]
        work["content"] = content
        pubTime = int(re.compile("created':(.*?),").findall(json_dump_data)[0]) * 1000

    elif '/q' in url:
        # 是提问
        content = re.compile("detail':.(.*?).'editableDetail").findall(json_dump_data)[0] + \
                  re.compile("content':.(.*?).'collapsedBy").findall(json_dump_data)[0]
        excerpt = re.compile("detail':.(.*?).'editableDetail").findall(json_dump_data)[0]
        platformWorksID = url.split('/')[-3]
        read_num = int(re.compile("visitCount':(.*?),").findall(json_dump_data)[0])
        collectNum = int(re.compile("followerCount':(.*?),").findall(json_dump_data)[0])
        digest = title
        work["question"] = excerpt
        work["oneAnswer"] = content
        work["answer"] = content
        work["likeNum"] = int(re.compile("voteupCount.:(.*?),").findall(json_dump_data)[0])
        work["commentNum"] = int(re.compile("commentCount.:(.*?),").findall(json_dump_data)[0])
        pubTime = int(re.compile("created':(.*?),").findall(json_dump_data)[0]) * 1000

    else:
        content = response
        platformWorksID = int(re.compile("{'id': '(\d+)', 'title'").findall(json_dump_data)[0])
        digest = excerpt = title
        pubTime = int(re.compile("updatedAt':(.*?),").findall(json_dump_data)[0]) * 1000

    contentType = 1
    images = []
    if 'image' in content:
        contentType = 2
        html = etree.HTML(content)
        images = html.xpath('.//img//@src')
    video = []
    covers = []
    if 'video' in content:
        contentType = 3
        html = etree.HTML(content)
        video = html.xpath('.//a[@class="video-link"]/@href')
        covers = html.xpath('.//a[@class="video-link"]/@data-poster')
    work["_id"] = md5(str(platform_id) + str(platformWorksID))
    work["platformID"] = platform_id
    work["platformName"] = platform_name
    work["parentID"] = parent_id
    work["parentName"] = parent_name
    work["platformWorksID"] = platformWorksID
    # work["accountName"] = user_name
    # work["accountUrl"] = user_url
    work["url"] = url
    # work["authors"] = [user_name]
    work["title"] = title
    work["titleWordsNum"] = len(title)
    # work["html"] = html
    work["digest"] = digest
    work["digestOriginal"] = excerpt
    work["contentType"] = contentType
    work["images"] = images
    work["videos"] = video
    work["covers"] = covers
    work["readNum"] = read_num
    # work["likeNum"] = like_num
    # work["commentNum"] = comment_count
    work["collectNum"] = collectNum
    work["updateParams"] = json.dumps({"url": url})
    work["pubTime"] = pubTime
    work["createTime"] = int(time.time() * 1000)
    work["updateTime"] = int(time.time() * 1000)
    logger.debug(work)
    dc_forum_details_list.append(work)

    return forum_result

