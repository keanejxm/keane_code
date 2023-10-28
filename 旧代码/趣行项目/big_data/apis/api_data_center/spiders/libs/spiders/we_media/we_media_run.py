# -*- coding:utf-8 -*-
"""

# author: albert
# date: 2021/1/5
# update: 2021/1/5
"""
from spiders.libs.spiders.we_media.we_media_spider.chang_cheng_24_hours_author_works import ChangCheng24Hours
from spiders.libs.spiders.we_media.we_media_spider.ji_yun_app_spider_author_works import JIYUNAuthorAndWork
from spiders.libs.spiders.we_media.we_media_spider.pengpai_apps import PengPaiAccountsAndWorks
from spiders.libs.spiders.we_media.we_media_spider.fenghuang_apps import FengHuangAccountsAndWorks
from spiders.libs.spiders.we_media.we_media_spider.ren_min_ri_bao_spider_author_works import RMRBAPPAuthorWorkSpider
from spiders.libs.spiders.we_media.we_media_spider.yym_we_media_spider.yym_run import YYMRun
import copy

class WeMediaRun:

    def __init__(self, logger):
        self.logger = logger

    def get_obj(self, task):
        we_media_obj = {
            "长城24小时APP": ChangCheng24Hours,
            "凤凰新闻手机客户端": FengHuangAccountsAndWorks,
            "冀云APP": JIYUNAuthorAndWork,
            "澎湃号手机客户端": PengPaiAccountsAndWorks,
            "人民日报APP": RMRBAPPAuthorWorkSpider,

            "今日头条": YYMRun,
            "UC浏览器": YYMRun,
            "百度新闻": YYMRun,
            "看点快报": YYMRun,
        }
        return we_media_obj[task["platformName"]]

    def _fetch(self, task):
        result = self.get_obj(task)(self.logger).fetch(task)
        return result

    def fetch_batch(self, task):
        return self._fetch(task)

    def fetch_yield(self, task):
        res = self._fetch(task)
        work_res = copy.deepcopy(res)
        if res["code"] == 1:
            yield dict(code=1, msg="success", data={"account": res["data"]["account"]})
            for r in work_res["data"]["worksList"]:
                yield dict(code=1, msg="success", data={"works": r})
        else:
            yield res

