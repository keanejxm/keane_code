# -*- encoding:utf-8 -*-
"""
@功能:将数据上传es
@AUTHOR：Keane
@文件名：es_untils.py
@时间：2020/12/21  15:52
"""
import time

import elasticsearch
import hashlib


class EsUtils(object):
    def __init__(self):
        self.es_hosts = [{"host": "192.168.16.21", "port": 9200}]
        # 链接es
        self._es_conn = elasticsearch.Elasticsearch(self.es_hosts)

    @staticmethod
    def md5_encode(data_res):
        has = hashlib.md5()
        has.update(data_res.encode("utf8"))
        md_res = has.hexdigest()
        return md_res

    @staticmethod
    def wash_topic_data(topic_fields):
        """
        清洗专题的数据
        """
        fields = {
            "_id": "",  # 专题id，app内唯一标识
            "status": 1,
            "topicID": "",  # 专题在平台的id
            "platformName": "",  # 平台名字
            "platformID": "",  # 平台id
            "channelName": "",  # 专题的频道名字
            "channelID": "",  # 专题的频道id
            "url": "",  # 专题url
            "title": "",  # 专题标题
            "digest": "",  # 摘要
            "topicCover": list(),  # 专题封面
            "pubTime": "",  # 专题发布时间
            "worksNum": "",  # 专题文章数量
            "newestArticleID": "",  # 专题最新文章id
            "articlesNumPerHour": "",  # 每小时更新数据
            "original": "",  # 是否原创
            "firstMedia": "",  # 是否首发媒体
            "transPower": "",  # 传播力
            "hotDegree": "",  # 专题热度
            "wordsFreq": "",  # 专题词频
            "hotDegreeTrend": "",  # 热度趋势
            "emotionTrend": "",  # 情感趋势
            "region": "",  # 地区
            "spreadPath": "",  # 传播途径
            "platformReadsNum": 0,
            "platformLikesNum": 0,
            "platformCommentsNum": 0,
            "platformForwardsNum": 0,
            "createTime": int(time.time() * 1000),
            "updateTime": int(time.time() * 1000)
        }
        for key, value in topic_fields.items():
            if key == "createTime":
                value = int(time.time() * 1000)
            if key == "updateTime":
                value = int(time.time() * 1000)
            if key == "articleNum":
                key = "worksNum"
            if key == "topicUrl":
                key = "url"
            if key == "newestArticle":
                key = "newestArticleID"
            fields[key] = value
        return fields

    def wash_article_data(self, article_fields):
        field = {
            "status": 1,
            "platformWorksID": "",
            "platformID": "ddb39873eb64c94140b83bf57becea34",
            "platformName": "",
            "channelID": "",
            "channelName": "",
            "accountID": "",
            "accountName": "",
            "topicID": "",
            "topicTitle":"",
            "epaperLayoutID": "",
            "url": "",
            "authors": [],
            "editors": list(),
            "hbrbAuthors": list(),
            "preTitle": "",
            "subTitle": "",
            "title": "",
            "titleWordsNum": 0,
            "content": "",
            "contentWordsNum": 0,
            "html": "",
            "simhash": "",
            "contentType": -1,
            "digest": "",
            "digestOriginal": "",
            "digestCompute": "",
            "source": "",
            "isOriginal": -1,
            "isOriginalCompute": -1,
            "isTop": -1,
            "images": list(),
            "covers": list(),
            "topics": list(),
            "videos": list(),
            "audios": list(),
            "updateParams": "{}",
            "readNum": 0,
            "commentNum": 0,
            "likeNum": 0,
            "collectNum": 0,
            "forwardNum": 0,
            "wxLookNum": 0,
            "sentiment": -1,
            "sentimentPositiveProb": -1,
            "wangYiJoinNum": 0,
            "personNames": list(),
            "regionNames": list(),
            "organizationNames": list(),
            "keywords": list(),
            "segmentWordsRawInfo": "",
            "hasSpread": -1,
            "hasSimilarWorks": -1,
            "hasSimilarOriginalWorks": -1,
            "reprintNum": 0,
            "reprintMediaNum": 0,
            "spreadHI": 0,
            "interactiveHI": 0,
            "pubTime": 0,
            "createTime": int(time.time() * 1000),
            "updateTime": int(time.time() * 1000),
        }
        article_id = article_fields.get("workerid")
        app_name = article_fields.get("appname")
        title = article_fields.get("title")
        pubtime = article_fields.get("pubtime")
        md5_str = str(article_id) + app_name + title + str(pubtime)
        _id = self.md5_encode(md5_str)
        field["_id"] = _id
        field["topicID"] = article_fields.get("topicid")
        field["topicTitle"] = article_fields.get("topicTitle")
        field["platformName"] = article_fields.get("appname")
        field["platformType"] = 4
        field["platformWorksID"] = article_fields.get("workerid")
        field["channelID"] = article_fields.get("channelindexid")
        field["channelName"] = article_fields.get("channelname")
        field["url"] = article_fields.get("url")
        field["authors"] = article_fields.get("author")
        field["editors"] = article_fields.get("editors")
        field["title"] = article_fields.get("title")
        field["titleWordsNum"] = len(article_fields.get("title"))
        field["content"] = article_fields.get("content")
        field["contentWordsNum"] = len(article_fields.get("content"))
        field["digest"] = ""
        field["source"] = article_fields.get("source")
        field["images"] = article_fields.get("images")
        field["covers"] = article_fields.get("articlecovers")
        field["videos"] = article_fields.get("videos")
        field["audios"] = article_fields.get("audios")
        field["readNum"] = article_fields.get("readnum")
        field["commentNum"] = article_fields.get("commentnum")
        field["likeNum"] = article_fields.get("likenum")
        field["forwardNum"] = article_fields.get("trannum")
        field["pubTime"] = article_fields.get("pubtime")
        field["contentType"] = article_fields.get("contentType")
        if field["platformName"] in field["source"]:
            field["isOriginal"] = 1
        else:
            field["isOriginal"] = 0
        return field

    def _es_create_new_works(self, index_name, field_id, fields):
        res = self._es_conn.index(index = index_name, doc_type = "_doc", body = fields, id = field_id)
        return res["result"]

    def api_create_topic(self, fields):
        """
        储存topic数据
        """
        # fields = self.wash_topic_data(fields)
        try:
            _id = fields.pop("_id")
            print(fields)
            res = self._es_create_new_works("dc_topics_v1", fields = fields, field_id = _id)
            return {"code": 1, "msg": "成功", "result": res, }
        except Exception as e:
            print(e)

    def api_create_articel(self, fields):
        # fields = self.wash_article_data(fields)
        try:
            _id = fields.pop("_id")
            res = self._es_create_new_works("dc_works", fields = fields, field_id = _id)
            return {"code": 1, "msg": "成功", "result": res, }
        except Exception as e:
            print(e)
    def api_create_channel(self,field):
        """
        添加频道信息
        """
        #向es数据库添加频道信息
        field_id = field.pop("_id")
        es_conn = elasticsearch.Elasticsearch([{"host": "180.76.161.67", "port": 9200}])
        # if not es_conn.exists(index = "dc_channels", doc_type = "_doc", id = field_id):
        if not field["types"]:
            field["types"] = []
        field["region"] = []
        res = es_conn.index(index = "dc_channels", id = field_id, body = field, doc_type = "_doc")
        # else:
        #     exist_fields = es_conn.get(index = "dc_channels", id = field_id, doc_type = "_doc")["_source"]
        #     res = es_conn.index(index = "dc_channels", id = field_id, body = exist_fields,
        #                         doc_type = "_doc")
        # #更新app频道es数据库
        # else:
        #     exist_fields = es_conn.get(index = "dc_channels", id = field_id, doc_type = "_doc")["_source"]
        #         exist_fields["types"] = list(set(a))
        #     b = exist_fields["selfTypesIDs"]
        #     b.append(item["id"])
        #     exist_fields["selfTypesIDs"] = list(set(b))
        #     res = es_conn.index(index = "dc_channels", id = field_id, body = exist_fields,
        #                         doc_type = "_doc")
        return res["result"], field_id

def test():
    fields = {
        "topicID": "4_53685",
        "platformName": "解放军报",
        "platformID": "",
        "channelName": "",
        "channelID": "",
        "topicUrl": "http://appapi.81.cn/v4/public/jfjbshare/?topicid=4_53685&type=1",
        "title": "纪念玉树灾后重建十周年",
        "digest": "震后十年，灾难的元素渐渐淡去，带着祈愿与美好生活的向往，玉树人在前行……",
        "topicCover": [
            "https://appimg.81.cn/thumbs2/680/179/data/mediafile/pic/img/2020/04/09/6557eb0d3d5c49d7b9d"
            "030601059e093.jpg"
        ],
        "pubTime": 1586133933000,
        "articleNum": 22,
        "newestArticle": "",
        "articleIDs": [
            "4_53829",
            "4_53825",
            "4_53831",
            "4_53827",
            "4_53817",
            "4_53731",
            "4_53729",
            "4_53707",
            "4_53705",
            "4_53703",
            "4_53701",
            "4_53699",
            "4_53697",
            "4_53695",
            "4_53693",
            "4_53691",
            "4_53689",
            "4_53717",
            "4_53733",
            "4_53723",
            "4_53721",
            "4_53725"
        ],
        "articlesNumPerHour": "",
        "original": "",
        "firstMedia": "",
        "transPower": "",
        "hotDegree": "",
        "wordsFreq": "",
        "hotDegreeTrend": "",
        "emotionTrend": "",
        "region": "",
        "spreadPath": "",
        "createTime": "",
        "updateTime": ""
    }
    es_utils = EsUtils()
    fields = es_utils.wash_topic_data(fields)
    _id = fields.pop("_id")
    res = es_utils._es_create_new_works("dc_topics_v1", fields = fields, field_id = _id)
    # fields = es_utils.wash_article_data(fields)
    # _id = fields.pop("_id")
    # res = es_utils._es_create_new_works("dc_works",fields = fields,field_id = _id)
    print(res)


if __name__ == '__main__':
    test()
