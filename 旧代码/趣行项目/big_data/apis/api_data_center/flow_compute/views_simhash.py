from django.shortcuts import render

# Create your views here.
import json
import jieba
import traceback
import numpy as np
import jieba.analyse
from django.views import View
from django.http import JsonResponse
from api_common_utils.llog import LLog
from api.config import es_config, api_log_path

from api_common_utils.text_processing_tools import text_remover_html_tag

logger = LLog(logger_name="flow_compute", log_path=api_log_path, logger_level="INFO").logger

# # 手动初始化
# jieba.initialize()
# # 加停用词
# pa = "/home/debugger/chris/big_data/big_data_platform/lib/models/sources_weibo_json/stop_words.txt"
# jieba.analyse.set_stop_words(pa)


class GetSimhash(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            logger.debug(f'对外情感分析接口接到的请求参数：{data}')
            content = data["content"]
            clean_method = data.get("clean_method", "re")
            need_cleaning = data.get("need_cleaning")
            if need_cleaning:
                # 需要清洗
                content = text_remover_html_tag(html=content)
                if not content:
                    return JsonResponse({"code": 1, "msg": "大哥，没有文字无法计算simhash的值", "data": ""})
            # 得到输入字符串的hash值
            # 结巴分词
            seg = jieba.cut(content)
            # 取前20个关键词
            keyword = jieba.analyse.extract_tags('|'.join(seg), topK=20, withWeight=True, allowPOS=())
            keyList = []
            # 获取每个词的权重
            for feature, weight in keyword:
                # 每个关键词的权重*总单词数
                weight = int(weight * 20)
                # 获取每个关键词的特征
                if feature == "":
                    feature = 0
                else:
                    # 将字符转为二进制，并向左移动7位
                    x = ord(feature[0]) << 7
                    m = 1000003
                    mask = 2 ** 128 - 1
                    # 拼接每个关键词中字符的特征
                    for c in feature:
                        x = ((x * m) ^ ord(c)) & mask
                    x ^= len(feature)
                    if x == -1:
                        x = -2
                    # 获取关键词的64位表示
                    x = bin(x).replace('0b', '').zfill(64)[-64:]
                    feature = str(x)
                temp = []
                # 获取每个关键词的权重
                for i in feature:
                    if i == '1':
                        temp.append(weight)
                    else:
                        temp.append(-weight)
                    keyList.append(temp)
            # 将每个关键词的权重变成一维矩阵
            list1 = np.sum(np.array(keyList), axis=0)
            # 获取simhash值
            simhash = ''
            for i in list1:
                # 对特征标准化表示
                if i > 0:
                    simhash = simhash + '1'
                else:
                    simhash = simhash + '0'
            return JsonResponse({"code": 1, "msg": "ok", "data": simhash})
        except Exception as e:
            logger.warning(f'{e}\n{traceback.format_exc(e)}')
            return JsonResponse({"code": 0, "msg": "未知错误"})


class CompareSimhash(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            logger.debug(f'对外情感分析接口接到的请求参数：{data}')
            sim1 = data["sim1"]
            sim2 = data["sim2"]
            # 转为二进制结构
            t1 = '0b' + sim1
            t2 = '0b' + sim2
            n = int(t1, 2) ^ int(t2, 2)
            # 相当于对每一位进行异或操作
            i = 0
            while n:
                n &= (n - 1)
                i += 1
            return JsonResponse({"code": 1, "msg": "ok", "data": i})
        except Exception as e:
            logger.warning(f'{e}\n{traceback.format_exc(e)}')
            return JsonResponse({"code": 0, "msg": "未知错误"})
