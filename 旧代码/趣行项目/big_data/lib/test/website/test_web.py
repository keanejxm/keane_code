# -*- coding:utf-8 -*-
"""
# project:
# author: Neil
# date: 2021/1/5
# update: 2021/1/5
"""
import json

from test.website.new_web_spider import WebSpider
from api_common_utils.llog import LLog
from test.website.check_epaper_template_from_es import DealWithTemplates

# 遍历结果集。
log = LLog("Test", only_console=False, logger_level="INFO").logger

paper_templates = DealWithTemplates(log).get_data_from_es()

nw = WebSpider(paper_template=paper_templates, logger=log).fetch_yield()