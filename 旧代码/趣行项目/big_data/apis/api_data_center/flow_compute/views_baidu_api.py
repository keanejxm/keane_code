import json

# from django.shortcuts import render

# Create your views here.
import traceback
from django.http import JsonResponse
from django.views import View
from api.config import api_log_path
from api_common_utils.llog import LLog
from flow_compute.lib.baidu_api.nlp import Nlp

logger = LLog(logger_name="baidu_api", log_path=api_log_path, logger_level="INFO").logger


# 判断正负面
class JudgeArticlePositiveNegative(View):

    def post(self, request):
        # 接收正文
        try:
            obj = Nlp(logger=logger)
            data = json.loads(request.body)
            return JsonResponse(obj.judge_article_positive_negative(data))
        except Exception as e:
            logger.warning("{}\n{}".format(e, traceback.format_exc()))
            return JsonResponse(dict(code=0, msg="failed"))


# 判断文章标签
class JudgeArticleClassify(View):

    def post(self, request):
        try:
            obj = Nlp(logger=logger)
            data = json.loads(request.body)
            return JsonResponse(obj.judge_article_classify(data))
        except Exception as e:
            logger.warning("{}\n{}".format(e, traceback.format_exc()))
            return JsonResponse(dict(code=0, msg="failed"))


# 全文分词
class FullTextParticiple(View):

    def post(self, request):
        try:
            obj = Nlp(logger=logger)
            data = json.loads(request.body)
            return JsonResponse(obj.full_text_participle(data))
        except Exception as e:
            logger.warning("{}\n{}".format(e, traceback.format_exc()))
            return JsonResponse(dict(code=0, msg="failed"))


# 生成文章摘要、提取文章主题
class CreateArticleAbstractTheme(View):

    def post(self, request):
        try:
            obj = Nlp(logger=logger)
            data = json.loads(request.body)
            return JsonResponse(obj.create_article_abstract_theme(data))
        except Exception as e:
            logger.warning("{}\n{}".format(e, traceback.format_exc()))
            return JsonResponse(dict(code=0, msg="failed"))


# 对文章聚类、归类
class ArticleClusteringClassified(View):

    def post(self, request):
        try:
            obj = Nlp(logger=logger)
            data = json.loads(request.body)
            return JsonResponse(obj.article_clustering_classified(data))
        except Exception as e:
            logger.warning("{}\n{}".format(e, traceback.format_exc()))
            return JsonResponse(dict(code=0, msg="failed"))


class WordFrequency(View):

    def post(self, request):
        try:
            obj = Nlp(logger=logger)
            data = json.loads(request.body)
            return JsonResponse(obj.word_frequency(data))
        except Exception as e:
            logger.warning("{}\n{}".format(e, traceback.format_exc()))
            return JsonResponse(dict(code=0, msg="failed"))


class NLP(View):

    def post(self, request):
        try:
            obj = Nlp(logger=logger)
            return JsonResponse(obj.run(request))
        except Exception as e:
            logger.warning("{}\n{}".format(e, traceback.format_exc()))
            return JsonResponse(dict(code=0, msg="failed"))
