# -*- coding:utf-8 -*-
"""
# project: 记录模板结果
# author: Neil
# date: 2021/1/5
# update: 2021/1/5
"""
import datetime

from test.epaper_test.newspaper_spider import NewspaperSpider
from test.epaper_test.check_epaper_template_from_es import DealWithTemplates

from lib.common_utils.llog import LLog


log = LLog("correct_epaper", log_path="./epaper_log", only_console=False, logger_level="DEBUG").logger

paper_templates = [DealWithTemplates(log).get_data_from_es()]

# target_dates = [datetime.datetime.now().strftime("%Y-%m-%d")]

for paper_template in paper_templates:
    target_dates = [datetime.datetime.now().strftime("%Y-%m-%d")]
    # target_dates = ["2021-01-20"]
    try:
        NewspaperSpider(paper_template=paper_template, target_dates=target_dates, logger=log).fetch_yield()
    except Exception as e:
        log.warning(f"该{paper_template['platformName']}---{e}")
        continue


