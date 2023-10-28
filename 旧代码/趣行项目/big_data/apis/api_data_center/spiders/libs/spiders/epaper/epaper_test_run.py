"""
# project: 测试程序
# author: Neil
# date: 2021/1/18 21:50
# update: 
"""



import datetime
from api_common_utils.llog import LLog

from spiders.libs.spiders.epaper.deal_with_epaper_templates import DealWithTemplates
from spiders.libs.spiders.epaper.newspaper_spider import NewspaperSpider

log = LLog("Test", only_console=True, logger_level="DEBUG").logger
paper_templates = [DealWithTemplates(log).get_data_from_es()]

# target_dates = [datetime.datetime.now().strftime("%Y-%m-%d")]
target_dates = ["2021-01-21"]
# 637报纸
for paper_template in paper_templates:
    nw = NewspaperSpider(paper_template=paper_template, target_dates=target_dates, logger=log)
    a = nw.fetch_yield()
    for i in a :
        print(i)

