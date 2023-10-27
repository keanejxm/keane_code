"""
# project: 
# author: Neil
# date: 2021/1/19 15:56
# update: 
"""
from spiders.libs.spiders.website.deal_with_epaper_templates import DealWithTemplates
import json
from api_common_utils.llog import LLog
from spiders.libs.spiders.website.new_web_spider import WebSpider

log = LLog("Test", only_console=True, logger_level="DEBUG").logger

result = DealWithTemplates(log).get_data_from_es()

# web_data4 = {
#     "platformName": "中国新闻网",
#     "sourceProvince": "北京市",
#     "sourceCity": "北京市",
#     "sourceCounty": "",
#     # 1：国家级，2：省级，3：市级，4：区县级，0：商业类网站。
#     "sourceLevel": 1,
#     # 1：媒体类，2：政务类，3：商业类。
#     "sourceClassify": 1,
#     # 是否重点渠道。
#     "sourceImportance": 1,
#     # 是否主流媒体。
#     "mainMedia": 1,
#     # 起始地址。
#     "start_url": "http://www.chinanews.com/",
#     "cookie": "cnsuuid=f05695a4-5fc9-b7f4-2ec7-c9334b0fbc0b2267.102397822924_1610177698910",
#     # 首页头条新闻
#     "headline_news": [],
#     # 轮播信息
#     "banner_news": ["//div[@class='banner_info']/ul/li/a"],
#     # 轮播旁边新闻
#     "banner_news_side": ["//div[@class='xwzxdd-dbt']/h1/a | //div[@class='xwzxdd-xbt']/div/a"],
#     # 导航信息
#     "channel_info_xpath": ["//div[@id='nav']/ul/li/a"],
#     # 详情链接。
#     "doc_links": [
#         r"https?://[\w\-\.]+\.chinanews\.com/\w+/\d{4,}/\d{2}-\d{2}/\d+\.shtml$",
#         r"https?://[\w\-\.]+\.chinanews\.com/\w+/\d+.shtml$",
#     ],
#     # 目标采集字段，成功时忽略后续模板。
#     "fields": {
#         "title": [
#             {"xpath": "//div[@class='content']/h1[1]/text()", },
#             {"xpath": "//h1[@id='tit']/text()", },
#             {"xpath": "//div[@class='left']/h1/text()", },
#         ],
#         "content": [
#             {"xpath": "//div[@class='left_zw']", },
#         ],
#         "pubSource": [
#             {
#                 "xpath": "//div[@class='left-time']/div[@class='left-t']/a[@class='source']/text()",
#             },
#             {
#                 "xpath": "//div[@class='left-time']/div[@class='left-t']/"
#                          "span[contains(text(), '来源：')]/text()",
#                 "regex": r"来源[: ：](\w+)$",
#             },
#             {
#                 "xpath": "//div[@class='left-t'][contains(text(), '来源：')]/text()",
#                 "regex": r"来源[: ：](\w+)$",
#             },
#         ],
#         "pubTime": [
#             {"xpath": "//div[@class='left-time']/div[@class='left-t']/text()[1]", },
#             {"xpath": "//div[@class='left-time']/div[@class='left-t']/span[1]/text()", },
#         ],
#         "authors": [
#             {"xpath": "//div[@class='author-info']/"
#                       "a[@data-author and contains(@class, 'author-name')]/text()", },
#         ],
#         "summary": [],
#     },
# }
# paper_templates4 = {
#     "status": 1,
#     "name": "",
#     "describe": "",
#     "value": json.dumps(web_data4, ensure_ascii=False),
#     "platformID": "4cc3f203bd871ee92989ef96ac9e5617",
#     "platformName": "中国新闻网",
#     "platformType": 3,
#     "channelID": "",
#     "channelName": "",
#     "accountID": "",
#     "accountName": "",
#     "topicID": "",
#     "topicTitle": "",
#     "worksID": "",
#     "worksTitle": "",
#     "createTime": "",
#     "updateTime": "",
# }
nw = WebSpider(paper_template=result, logger=log).fetch_yield()
for i in nw:
    print(i)