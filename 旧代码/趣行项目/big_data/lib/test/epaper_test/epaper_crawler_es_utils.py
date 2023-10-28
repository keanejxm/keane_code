# -*- coding:utf-8 -*-
"""

# author: Neil
# date: 2020/12/2
# update: 2020/12/2
"""


class NewspaperCrawlerEs:

    def __init__(self):
        # 版面索引。
        self._big_data_epaper_layout_index = "dc_epaper_layout_?"
        self.default_accounts_fields = {
            "url": "",
            "platformName": "",
            "platformType": 6,
            "sourceLevel": -1,
            "sourceClassify": -1,
            "sourceImportance": -1,  # byte
            "mainMedia": -1,  # byte
            "sourceProvince": "",
            "sourceCity": "",
            "sourceCounty": "",
            "categoryFirst": "",
            "categorySecond": "",
            "categoryThird": "",
            "rankCoefficient": 1.0,
            "status": 1,
            "layoutTitle": "",
            "filler": "{}",
            "layoutSeq": 1,
            "layoutNum": 0,
            "wangYiJoinNum": 0,
            "paperID": "",
            "layoutMapAreas": [],
            "layoutMapAreasLength": 0,
            "mapImage": "",
            "mapImageLocal": "",
            "largeImage": "",
            "largeImageLocal": "",
            "pdf": "",
            "pdfLocal": "",
        }
        # 稿件索引。
        self._big_data_epaper_works_index = "dc_epaper_article_?"
        self.default_works_fields = {
            "url": "",
            "platformName": "",
            "platformType": 6,
            "sourceLevel": -1,
            "sourceClassify": -1,
            "sourceImportance": -1,  # byte
            "mainMedia": -1,  # byte
            "sourceProvince": "",
            "sourceCity": "",
            "sourceCounty": "",
            "categoryFirst": "",
            "categorySecond": "",
            "categoryThird": "",
            "rankCoefficient": 1.0,
            "status": 1,
            "title": "",
            "preTitle": "",
            "subTitle": "",
            "content": "",
            "coverPic": [],
            "smallCoverPic": [],
            "hasPic": -1,
            "hasVideo": -1,
            "isHebei": -1,
            "sentiment": -1,
            "filler": "{}",
            "region": [],
            "area": [],
            "relevantWords": [],
            "summary": "",
            "summaryText": "",
            "layoutSeq": 1,
            "layoutNum": 1,
            "paperID": ""
        }