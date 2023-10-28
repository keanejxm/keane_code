# -*- coding:utf-8 -*-
"""

# author: albert
# date: 2020/12/28
# update: 2020/12/28
"""
import elasticsearch
from loguru import logger

from spiders.libs.spiders.weixin.wechat_publish_account import WeChatAccountSpider
# 石家庄新闻 0cf2ceec18722ce43b4b86c43479c9bf
# 石家庄日报 fcdc97bd15ed4ac4401cd848d5e3c7d1
# 燕赵晚报 046b1c06cbea4c7dd62e92b4650785cc
# 中央 ： 新华日报 b1306afd16f390e5a6580f88ab9820d6
# 中央 ： 央视新闻 5d7e8b8511a6e708915ee076cd406c44
# 省外的：北京电视台 3d5637064a47b818bb927efbe2dfa899

def run_more():
    tasks = [
      {
        "_id": "3d5637064a47b818bb927efbe2dfa899",
        "status": 1,
        "platformAccountID": "MjM5MDEzNTMyMA==",
        "name": "北京电视台",
        "avatar": "",
        "qrcode": "",
        "gender": -1,
        "mobilePhoneNumber": "",
        "email": "",
        "identityCode": "",
        "certificationType": -1,
        "url": "",
        "region": [
        "北京",
        "北京市"
        ],
        "types": [
        "1_3_1_1",
        "1_2_3_5"
        ],
        "selfTypesIDs": [],
        "platformID": "c874d6f5e772452053b508a6b99dc975",
        "platformName": "微信公众号",
        "platformWorksNum": 0,
        "platformFansNum": 0,
        "platformFollowsNum": 0,
        "platformReadsNum": 0,
        "platformLikesNum": 0,
        "platformCommentsNum": 0,
        "platformForwardsNum": 0,
        "worksNum": 0,
        "readNum": 0,
        "likeNum": 0,
        "commentNum": 0,
        "forwardNum": 0,
        "collectNum": 0,
        "createTime": 0,
        "updateTime": 0,
        "platformType": 0,
        "weMediaName": "公众号"
      },
      {
        "_id": "b1306afd16f390e5a6580f88ab9820d6",
        "status": 1,
        "platformAccountID": "MzA5NzExMzMxMw==",
        "name": "新华日报",
        "avatar": "",
        "qrcode": "",
        "gender": -1,
        "mobilePhoneNumber": "",
        "email": "",
        "identityCode": "",
        "certificationType": -1,
        "url": "",
        "region": [],
        "types": [
        "1_2_3_3"
        ],
        "selfTypesIDs": [],
        "platformID": "c874d6f5e772452053b508a6b99dc975",
        "platformName": "微信公众号",
        "platformWorksNum": 0,
        "platformFansNum": 0,
        "platformFollowsNum": 0,
        "platformReadsNum": 0,
        "platformLikesNum": 0,
        "platformCommentsNum": 0,
        "platformForwardsNum": 0,
        "worksNum": 0,
        "readNum": 0,
        "likeNum": 0,
        "commentNum": 0,
        "forwardNum": 0,
        "collectNum": 0,
        "createTime": 0,
        "updateTime": 0,
        "platformType": 0,
        "weMediaName": "公众号"
      },
      {
            "_id": "0cf2ceec18722ce43b4b86c43479c9bf",
            "status": 1,
            "platformAccountID": "MzI4MjA3NjUwOQ==",
            "name": "石家庄新闻网",
            "avatar": "",
            "qrcode": "",
            "gender": -1,
            "mobilePhoneNumber": "",
            "email": "",
            "identityCode": "",
            "certificationType": -1,
            "url": "",
            "region": [
            "河北",
            "石家庄市"
            ],
            "types": [
            "1_3_3_8",
            "1_2_3_1"
            ],
            "selfTypesIDs": [],
            "platformID": "c874d6f5e772452053b508a6b99dc975",
            "platformName": "微信公众号",
            "platformWorksNum": 0,
            "platformFansNum": 0,
            "platformFollowsNum": 0,
            "platformReadsNum": 0,
            "platformLikesNum": 0,
            "platformCommentsNum": 0,
            "platformForwardsNum": 0,
            "worksNum": 0,
            "readNum": 0,
            "likeNum": 0,
            "commentNum": 0,
            "forwardNum": 0,
            "collectNum": 0,
            "createTime": 0,
            "updateTime": 0,
            "platformType": 0,
            "weMediaName": "公众号"
      },
      {
            "_id": "5d7e8b8511a6e708915ee076cd406c44",
            "status": 1,
            "platformAccountID": "MTI0MDU3NDYwMQ==",
            "name": "央视新闻",
            "avatar": "",
            "qrcode": "",
            "gender": -1,
            "mobilePhoneNumber": "",
            "email": "",
            "identityCode": "",
            "certificationType": -1,
            "url": "",
            "region": [
            "北京",
            "北京市"
            ],
            "types": [
            "1_3_1_1",
            "1_2_3_3"
            ],
            "selfTypesIDs": [],
            "platformID": "c874d6f5e772452053b508a6b99dc975",
            "platformName": "微信公众号",
            "platformWorksNum": 0,
            "platformFansNum": 0,
            "platformFollowsNum": 0,
            "platformReadsNum": 0,
            "platformLikesNum": 0,
            "platformCommentsNum": 0,
            "platformForwardsNum": 0,
            "worksNum": 0,
            "readNum": 0,
            "likeNum": 0,
            "commentNum": 0,
            "forwardNum": 0,
            "collectNum": 0,
            "createTime": 0,
            "updateTime": 0,
            "platformType": 0,
            "weMediaName": "公众号"
      },
      {
            "_id": "fcdc97bd15ed4ac4401cd848d5e3c7d1",
            "status": 1,
            "platformAccountID": "MzA4NTg1MTcwOA==",
            "name": "石家庄日报",
            "avatar": "",
            "qrcode": "",
            "gender": -1,
            "mobilePhoneNumber": "",
            "email": "",
            "identityCode": "",
            "certificationType": -1,
            "url": "",
            "region": [
            "河北",
            "石家庄市"
            ],
            "types": [
            "1_3_3_8",
            "1_2_3_1",
            "1_1_2"
            ],
            "selfTypesIDs": [],
            "platformID": "c874d6f5e772452053b508a6b99dc975",
            "platformName": "微信公众号",
            "platformWorksNum": 0,
            "platformFansNum": 0,
            "platformFollowsNum": 0,
            "platformReadsNum": 0,
            "platformLikesNum": 0,
            "platformCommentsNum": 0,
            "platformForwardsNum": 0,
            "worksNum": 0,
            "readNum": 0,
            "likeNum": 0,
            "commentNum": 0,
            "forwardNum": 0,
            "collectNum": 0,
            "createTime": 0,
            "updateTime": 0,
            "platformType": 0,
            "weMediaName": "公众号"
      },
      {
        "_id": "046b1c06cbea4c7dd62e92b4650785cc",
        "status": 1,
        "platformAccountID": "MjM5MDk1NjM4MA==",
        "name": "燕赵晚报",
        "avatar": "",
        "qrcode": "",
        "gender": -1,
        "mobilePhoneNumber": "",
        "email": "",
        "identityCode": "",
        "certificationType": -1,
        "url": "",
        "region": [
        "河北",
        "石家庄市"
        ],
        "types": [
        "1_3_3_8",
        "1_2_3_1"
        ],
        "selfTypesIDs": [],
        "platformID": "c874d6f5e772452053b508a6b99dc975",
        "platformName": "微信公众号",
        "platformWorksNum": 0,
        "platformFansNum": 0,
        "platformFollowsNum": 0,
        "platformReadsNum": 0,
        "platformLikesNum": 0,
        "platformCommentsNum": 0,
        "platformForwardsNum": 0,
        "worksNum": 0,
        "readNum": 0,
        "likeNum": 0,
        "commentNum": 0,
        "forwardNum": 0,
        "collectNum": 0,
        "createTime": 0,
        "updateTime": 0,
        "platformType": 0,
        "weMediaName": "公众号"
      },
        # {
        #     "_id": "7ac280d502eb92380ecedabe6f8defb4",
        #
        #     "gender": -1,
        #     "platformForwardsNum": 0,
        #     "worksNum": 0,
        #     "qrcode": "",
        #     "platformCommentsNum": 0,
        #     "collectNum": 0,
        #     "platformID": "c874d6f5e772452053b508a6b99dc975",
        #     "platformLikesNum": 0,
        #     "identityCode": "",
        #     "likeNum": 0,
        #     "platformName": "微信公众号",
        #     "introduction": "参与、沟通、记录时代。",
        #     "email": "",
        #     "mobilePhoneNumber": "",
        #     "types": [
        #         "1_3_20"
        #     ],
        #     "certificationType": -1,
        #     "updateTime": 1608724749671,
        #     "avatar": "http://wx.qlogo.cn/mmhead/Q3auHgzwzM5Dlw4H8vWoicXPXccEVkWYgFfn45zFUq38nuViaPF89Pkg/0",
        #     "url": "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5MjAxNDM4MA==&scene=124&uin=MTA1ODU2MDcyNg%3D%3D&key=abbf46418ae1ca63cf72cbdab41c3bf042983d62de13adf26695808cfa7f67b4733572e9c5a7d169ac6498b3106fc7784b4f91f13c256200f8f828f3c204f67ad6f47f84d51f0cabecd5e27b9bef60d024d79aa8095c7a4f287aa8241940a4793f760977c06594b9709cb32b87fdae44104c37cf5ba05af3fa5a2ae2ca7db782&devicetype=Windows+10+x64&version=62090529&lang=zh_CN&a8scene=7&pass_ticket=LzHRlFa10pD7fnwX8qvHRrxq0LSV4FP3v4aPSlM108%2FErCDjiq7utvkYLNQZ0beQ&winzoom=1",
        #     "commentNum": 0,
        #     "platformFansNum": 0,
        #     "platformFollowsNum": 0,
        #     "platformAccountID": "MjM5MjAxNDM4MA==",
        #     "forwardNum": 0,
        #     "readNum": 0,
        #     "createTime": 1608715314545,
        #     "name": "人民日报",
        #     "platformWorksNum": 0,
        #     "platformReadsNum": 0,
        #     "region": [],
        #     "status": 1
        # }
    ]
    for task in tasks:
        WeChatAccountSpider(logger).fetch_batch(task)


def run_one(name):
    es_hosts = [dict(
        host="192.168.16.21",
        port=9200,
    )]
    es_conn = elasticsearch.Elasticsearch(hosts=es_hosts)
    body = {
      "query": {
        "bool": {
          "must": [
            {"term": {
              "name": {
                "value": name
              }
            }},
            {"term": {
              "platformID": {
                "value": "c874d6f5e772452053b508a6b99dc975"
              }
            }
            }
          ]
        }
      }
    }
    res = es_conn.search(index="dc_accounts", doc_type="_doc", body=body)
    res = res["hits"]["hits"][0]
    data = res["_source"]
    data["_id"] = res["_id"]
    task = data
    return WeChatAccountSpider(logger).fetch_batch(task)


def run():
    res = run_one("河北日报")
    logger.debug(res)
    # run_more()


if __name__ == '__main__':
    run()

"""
uin=MjExNDkzMDQ5Nw%3D%3D
key=db703f13e9c93d824fdd0fde83a55a27bf637062463c61a6c0dca8ec14a66dc3d37ca5974901079f75f8a78d1b607bbbc1933d69ba96d71f46a0ccddeb9775a0664b4f454732621ff9c475a391e73dedbeddce61c8bbc86054e175b6a846f2701eb1dd2ffa5a9c6f63d4c5f261f32d3bbacea702000d5efc4a0afc780baab11c&devicetype=Windows+10+x64&version=63010029&lang=zh_CN&ascene=1&pass_ticket=hs7o%2FTQb1jxhcK1ZgUhU67fR66QEMqQZl2N%2BLXWWuKy7a24s9QY9cvpycKNT8sxv&fontgear=2

"""
"""



政府类  
94f80a4534f068c47e664662c8471d5e  河北卫生健康
省级
bd59e99f436e33b6bb8e25b719d9a77a  河北广播电视台







"""