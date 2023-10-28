# -*- coding:utf-8 -*-
"""
百度接口，自然语言分析。
# author: albert
# date: 2020/12/16
# update: 2020/12/16
"""
import decimal
import traceback
from functools import reduce

from django.shortcuts import render

# Create your views here.
import re
import json
import jieba
import operator
import collections
from aip import AipNlp
from decimal import Decimal
from decimal import localcontext
from api.config import APP_ID, API_KEY, SECRET_KEY
from api_common_utils.text_processing_tools import get_text_byte_length, \
    text_remover_html_tag, text_segmentation, text_remover_symbol

from api_common_utils.llog import LLog

from api.config import api_log_path

nlp_logger = LLog(logger_name="nlp", log_path=api_log_path, logger_level="DEBUG").logger


class Nlp(object):

    def __init__(self, logger=nlp_logger):
        self.client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
        self._logger = logger

    # 判断正负面
    def judge_article_positive_negative(self, data):
        self._logger.debug(f'情感分析接口接到的请求参数：{data}')
        text = data["content"]
        text = text_remover_html_tag(text)
        if not text:
            return dict(code=1001, msg='文本中没有文字', data=[])
        res = []
        client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
        if get_text_byte_length(text) > 2048:
            text_list = text_segmentation(text=text, method='complete', length=770)
            for text in text_list:
                r = client.sentimentClassify(text)
                res.append(r)
            all_result = {"log_id": 0, "text": "",
                          "items": [{"sentiment": 0, "confidence": 0, "positive_prob": 0, "negative_prob": 0}]}
            sentiment = 0
            confidence = 0
            positive_prob = 0
            negative_prob = 0
            for i in res:
                sentiment += i["items"][0]["sentiment"]
                confidence += i["items"][0]["confidence"]
                positive_prob += i["items"][0]["positive_prob"]
                negative_prob += i["items"][0]["negative_prob"]
            sentiment = Decimal(str(sentiment))
            confidence = Decimal(str(confidence))
            positive_prob = Decimal(str(positive_prob))
            negative_prob = Decimal(str(negative_prob))
            with localcontext() as ctx:
                ctx.prec = 3
                sentiment = sentiment / len(res)
                confidence = confidence / len(res)
                positive_prob = positive_prob / len(res)
                negative_prob = negative_prob / len(res)
            sentiment = decimal.Context(prec=1, rounding=decimal.ROUND_HALF_UP).create_decimal(str(sentiment))
            all_result["items"][0]["sentiment"] = sentiment
            all_result["items"][0]["confidence"] = confidence
            all_result["items"][0]["positive_prob"] = positive_prob
            all_result["items"][0]["negative_prob"] = negative_prob
            res.append(all_result)
        else:
            r = client.sentimentClassify(text)
            res.append(r)
        return dict(code=1, msg='ok', data=res)

    # 判断文章标签
    def judge_article_classify(self,data, method='re'):
        self._logger.debug(f'文章标签（关键字）接到的请求参数：{data}')
        title = data["title"]
        content = data["content"]
        res = []
        client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
        content = text_remover_html_tag(content, method=method)
        if not content:
            return dict(code=1001, msg='文本中没有文字', data=[])
        title_byte_length = get_text_byte_length(title)
        content_byte_length = get_text_byte_length(content)
        if title_byte_length == content_byte_length:
            title = title[:20]
        if title_byte_length > 80:
            remover_title = text_remover_symbol(title)
            if get_text_byte_length(remover_title) > 80:
                title = title[:20]
            else:
                title = remover_title
        if get_text_byte_length(content) > 65535:
            remover_symbol_content = text_remover_symbol(content)
            if get_text_byte_length(remover_symbol_content) > 65535:
                text_list = text_segmentation(text=content, method='complete', length=35000)
                for content in text_list:
                    r = client.keyword(title, content)
                    res.extend(r["items"])
                lv_list = sorted(res, key=operator.itemgetter('score'), reverse=True)
                res_list = []
                l_list = []
                res_list.append(res[0])
                l_list.append(res[0]["tag"])
                for r in lv_list:
                    if r["tag"] not in l_list:
                        l_list.append(r["tag"])
                        res_list.append(r)
                res = res_list
                for i in res:
                    i["word_count"] = content.count(i["tag"])
                return dict(code=1, msg='ok', data=res)
        r = client.keyword(title, content)
        res.extend(r["items"])
        for i in res:
            i["word_count"] = content.count(i["tag"])
        return dict(code=1, msg='ok', data=res)

    # 全文分词
    def full_text_participle(self, data):
        self._logger.debug(f'全文分词接口接到的请求参数：{data}')
        text = data["content"]
        text = text_remover_html_tag(text)
        if not text:
            return dict(code=1001, msg='文本中没有文字', data=[])
        res_list = []
        client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
        if get_text_byte_length(text) > 20000:
            remover_text = text_remover_symbol(text)
            if get_text_byte_length(remover_text) > 20000:
                text_list = text_segmentation(text=text, method='complete', length=10000)
                for text in text_list:
                    r = client.lexer(text)
                    res_list.extend(r["items"])
        else:
            r = client.lexer(text)
            res_list.extend(r["items"])
        res = {}
        per = []
        loc = []
        org = []
        measure_word = []
        key_word = []
        for res_dict in res_list:
            if res_dict.get('ne'):
                if res_dict.get('ne') == 'PER':
                    per.append(res_dict.get('item'))
                elif res_dict.get('ne') == 'LOC':
                    loc.append(res_dict.get('item'))
                elif res_dict.get('ne') == 'ORG':
                    org.append(res_dict.get('item'))
            elif res_dict.get('pos'):
                if res_dict.get('pos') in ['v', 'vd', 'vn', 'ad', 'd', 'q', 'r', 'p', 'c', 'u', 'xc', 'w']:
                    continue
                if len(res_dict.get('item')) == 1:
                    continue
                if res_dict.get('pos') == 'm':
                    measure_word.append(res_dict.get('item'))
                key_word.append(dict(word=res_dict.get('item'), word_count=text.count(res_dict.get('item'))))
        key_word = sorted(key_word, key=lambda r: r['word_count'], reverse=True)
        run_function = lambda x, y: x if y in x else x + [y]
        key_word = reduce(run_function, [[], ] + key_word)
        res["人名"] = list(set(per))
        res["地名"] = list(set(loc))
        res["组织"] = list(set(org))
        res["数量词"] = list(set(measure_word))
        res["关键词"] = key_word[:20]
        res["raw_data"] = res_list
        return dict(code=1, msg='ok', data=res)

    # 生成文章摘要、提取文章主题
    def create_article_abstract_theme(self, data):
        self._logger.debug(f'生成文章摘要接口接到的请求参数：{data}')
        title = data["title"]
        content = data["content"]
        max_summary_len = data.get("max_summary_len", 200)
        res = []
        client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
        title = text_remover_html_tag(title)
        content = text_remover_html_tag(content)
        if not content:
            return dict(code=1001, msg='文本中没有文字', data=[])
        title_byte_length = get_text_byte_length(title)
        content_byte_length = get_text_byte_length(content)
        if title_byte_length == content_byte_length:
            title = title[:20]
        if title_byte_length > 400:
            remover_title = text_remover_symbol(title)
            if get_text_byte_length(remover_title) > 400:
                title = title[:20]
        if content_byte_length > 6000:
            text_list = text_segmentation(text=content, method='complete', length=3000)
            for content in text_list:
                data = {
                    "title": title,
                }
                r = client.newsSummary(content, max_summary_len, data)
                res.append(r)
                return dict(code=1, msg='ok', data=res)
        data = {
            "title": title,
        }

        r = client.newsSummary(content, max_summary_len, data)
        res.append(r)
        return dict(code=1, msg='ok', data=res)

    # 对文章聚类、归类
    def article_clustering_classified(self, data):
        self._logger.debug(f'文章聚类归类接口接到的请求参数：{data}')
        title = data["title"]
        content = data["content"]
        client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
        title_byte_length = get_text_byte_length(title)
        content_byte_length = get_text_byte_length(content)
        if title_byte_length == content_byte_length:
            title = title[:20]
        if title_byte_length > 80:
            remover_title = text_remover_symbol(title)
            if get_text_byte_length(remover_title) > 80:
                title = title[:20]
            else:
                title = remover_title
        content = text_remover_html_tag(content)
        if not content:
            return dict(code=1001, msg='文本中没有文字', data=[])
        if get_text_byte_length(content) > 65535:
            remover_symbol_content = text_remover_symbol(content)
            if get_text_byte_length(remover_symbol_content) > 65535:
                text_list = text_segmentation(text=content, method='complete', length=35000)
                lv1 = []
                lv2 = []
                res = {}
                for content in text_list:
                    r = client.topic(title, content)
                    lv1.extend((r["item"]["lv1_tag_list"]))
                    lv2.extend((r["item"]["lv2_tag_list"]))
                # for r in res:
                lv1_list = sorted(lv1, key=operator.itemgetter('score'), reverse=True)
                lv2_list = sorted(lv1, key=operator.itemgetter('score'), reverse=True)
                res_lv2_list = []
                pa_res_lv2_list = []
                res_lv2_list.append(lv2_list[0])
                pa_res_lv2_list.append(lv2_list[0]["tag"])
                for i in lv2_list:
                    if i["tag"] not in pa_res_lv2_list:
                        pa_res_lv2_list.append(i["tag"])
                        res_lv2_list.append(i)
                res["lv1_tag_list"] = lv1_list[0]
                res["lv2_tag_list"] = res_lv2_list
                return dict(code=1, msg='ok', data=[res])
        else:
            r = client.topic(title, content)
            res = r["item"]
            return dict(code=1, msg='ok', data=[res])

    # 计算词频
    def word_frequency(self, data):
        self._logger.debug(f'计算词频接口接到的请求参数：{data}')
        text = data["content"]
        text = text_remover_html_tag(text)
        if not text:
            return dict(code=1001, msg='文本中没有文字', data=[])
        pattern = re.compile(u'\t|/|\n|\.|-|:|;|\)|\(|\?|"|“|”')
        string_data = re.sub(pattern, '', text)
        seg_list_exact = jieba.cut(string_data, cut_all=False)
        object_list = []
        remove_words = [u'的', u'，', u'和', u'是', u'随着', u'对于', u'对', u'等', u'能', u'都', u'及',
                        u'。', u' ', u'、', u'中', u'在', u'了', u'通常', u'如果', u'我们', u'需要']
        for word in seg_list_exact:
            if len(word) == 1:
                continue
            if word not in remove_words:
                object_list.append(word)
        word_counts = collections.Counter(object_list)
        word_counts_top10 = word_counts.most_common(10)
        return dict(code=1, msg='ok', data=word_counts_top10)

    def run(self, request=None, spider_data=None):
        result = dict(code=1, msg='ok', data={})
        if request:
            data = json.loads(request.body)
        else:
            data = spider_data
        nlp_function = data.get("nlp_function")
        if not nlp_function:
                nlp_function = ['emotion', 'label', 'participles', 'abstract', 'classified', 'frequency']
        if 'emotion' in nlp_function:
            try:
                result['data']["情感分析"] = self.judge_article_positive_negative(data)["data"]
            except Exception as e:
                result['data']["情感分析"] = []
                self._logger.debug(f'情感分析：{e}\n{traceback.format_exc(e)}')
        if 'label' in nlp_function:
            for i in range(3):
                method = ["re", "xpath", "bs4"]
                try:
                    result['data']["文章标签"] = self.judge_article_classify(data, method=method[i])["data"]
                    break
                except Exception as e:
                    self._logger.debug(f'文章标签：{e}\n{traceback.format_exc(e)}')
                    if i == 2:
                        result['data']["文章标签"] = []
        if 'participles' in nlp_function:
            try:
                result['data']["全文分词"] = self.full_text_participle(data)["data"]
            except Exception as e:
                result['data']["全文分词"] = []
                self._logger.debug(f'全文分词：{e}\n{traceback.format_exc(e)}')
        if 'abstract' in nlp_function:
            try:
                result['data']["文章摘要"] = self.create_article_abstract_theme(data)["data"]
            except Exception as e:
                result['data']["文章摘要"] = []
                self._logger.debug(f'文章摘要：{e}\n{traceback.format_exc(e)}')
        if 'classified' in nlp_function:
            try:
                result['data']["文章归类"] = self.article_clustering_classified(data)["data"]
            except Exception as e:
                result['data']["文章归类"] = []
                self._logger.debug(f'文章归类：{e}\n{traceback.format_exc(e)}')
        if 'frequency' in nlp_function:
            try:
                result['data']["计算词频"] = self.word_frequency(data)["data"]
            except Exception as e:
                result['data']["计算词频"] = []
                self._logger.debug(f'计算词频：{e}\n{traceback.format_exc(e)}')
        return result

