"""

# author: albert
# date: 2021/1/21 15:13
# update: 2021/1/21 15:13
"""
import hashlib
import time
import traceback

from api_common_utils.text_processing_tools import text_remover_html_tag
from spiders.libs.spiders.we_media.we_media_spider.yym_we_media_spider.bjh_fetcher import BJSpider
from spiders.libs.spiders.we_media.we_media_spider.yym_we_media_spider.dayu_account_work_spider import DYSpider
from spiders.libs.spiders.we_media.we_media_spider.yym_we_media_spider.kandian_fetch import KDSpider
from spiders.libs.spiders.we_media.we_media_spider.yym_we_media_spider.toutiao_account_works import TTSpider
from spiders.libs.spiders.we_media.we_media_utils import DEFAULT_WE_MEDIA_USER_WORKS_FIELDS, \
    DEFAULT_WE_MEDIA_USER_INFO_FIELDS


class YYMRun:

    def __init__(self, logger):
        self.logger = logger

    @staticmethod
    def md5(unicode_str, charset="UTF-8"):
        """
        字符串转md5格式。
        :return:
        """
        _md5 = hashlib.md5()
        _md5.update(unicode_str.encode(charset))
        return _md5.hexdigest()

    def get_result(self, task):
        name_mapping = {
            "今日头条": TTSpider,
            "UC浏览器": DYSpider,
            "看点快报": KDSpider,
            "百度新闻": BJSpider,
        }
        yym_spider = name_mapping[task["platformName"]]
        yym_result = yym_spider(self.logger).fetch(task)
        return yym_result

    def parse_account(self, account, task):
        now = int(time.time() * 1000)
        platformID = task["platformID"]
        platformName = task["platformName"]
        new_account_dict = dict(dict(), **DEFAULT_WE_MEDIA_USER_INFO_FIELDS)
        new_account_dict["_id"] = self.md5(platformID + str(account['mediaUid']))
        new_account_dict["platformAccountID"] = str(account['mediaUid'])
        new_account_dict["name"] = account['nickName']
        new_account_dict["avatar"] = account['avatar']
        new_account_dict["gender"] = account['gender']
        new_account_dict["url"] = account['url']
        region = []
        if account['province']:
            region.append(account['province'])
        if account['city']:
            region.append(account['city'])
        new_account_dict["region"] = region
        new_account_dict["types"] = [7]
        new_account_dict["platformID"] = platformID
        new_account_dict["platformName"] = platformName
        new_account_dict["platformWorksNum"] = int(account['mediaWorkNum'])
        new_account_dict["platformFansNum"] = int(account['fanNum'])
        new_account_dict["platformFollowsNum"] = int(account['followNum'])
        new_account_dict["platformReadsNum"] = int(account['mediaReadNum'])
        new_account_dict["platformLikesNum"] = int(account['mediaLikeNum'])
        new_account_dict["platformCommentsNum"] = int(account['mediaCommentNum'])
        new_account_dict["platformForwardsNum"] = int(account['mediaForwardNum'])
        new_account_dict["weMediaName"] = account['mediaName']
        new_account_dict["createTime"] = now
        new_account_dict["updateTime"] = now
        return new_account_dict

    def parse_works(self, works_list, task):
        new_works_list = []
        for works in works_list:
            now = int(time.time() * 1000)
            platformID = task["platformID"]
            platformName = task["platformName"]
            article_data = dict(dict(), **DEFAULT_WE_MEDIA_USER_WORKS_FIELDS)
            article_data["_id"] = self.md5(platformID + str(works['mediaWorkId']))
            article_data["platformWorksID"] = str(works['mediaWorkId'])
            article_data["platformID"] = platformID
            article_data["platformName"] = platformName
            article_data["accountID"] = self.md5(platformID + str(works['mediaUid']))
            article_data["accountName"] = works['nickName']
            article_data["url"] = works['url']
            article_data["authors"] = [works['nickName']]
            article_data["title"] = works["title"]
            article_data["titleWordsNum"] = len(works["title"])
            # article_data["html"] = detail_content.text
            content = text_remover_html_tag(works["content"])
            article_data["content"] = content
            article_data["contentWordsNum"] = len(content)
            article_data["digest"] = content[:200]
            article_data["images"] = works['covers']
            article_data["covers"] = works['covers']
            article_data["videos"] = works['videos']
            article_data["readNum"] = works['readNum']
            article_data["likeNum"] = works['likeNum']
            article_data["commentNum"] = works['commentNum']
            article_data["forwardNum"] = works['forwardNum']
            article_data["updateParams"] = works['updateParams']
            article_data["contentType"] = works['contentType']
            article_data["pubTime"] = int(works['pubDateTime'])
            article_data["createTime"] = now
            article_data["updateTime"] = now
            new_works_list.append(article_data)
        return new_works_list

    def parse_yym_result(self, yym_result, task):
        account_dict = yym_result["data"]["account"]
        works = yym_result["data"]["works"]
        account = self.parse_account(account_dict, task)
        works_list = self.parse_works(works, task)
        return dict(
                code=1,
                msg="success",
                data=dict(
                    account=account,
                    worksList=works_list
                )
            )

    def fetch(self, task):
        try:
            yym_result = self.get_result(task)
            if yym_result["code"] == 0:
                return yym_result
            res = self.parse_yym_result(yym_result, task)
            return res
        except Exception as e:
            self.logger.warning(f"{e}\n{traceback.format_exc()}")
            return dict(code=0, msg=str(e))


if __name__ == '__main__':
    from loguru import logger
    task = {
        "platformID": "",
        "platformName": "今日头条",
        "platformAccountID": "54804078351",
    }
    res = YYMRun(logger).fetch(task)

