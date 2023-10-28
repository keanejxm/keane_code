# -*- coding:utf-8 -*-
"""

# author: albert
# date: 2020/12/24
# update: 2020/12/24
"""
import jieba
import jieba.analyse
import numpy as np


# 获取字符串对应的hash值
from api_data_center.api_common_utils.text_processing_tools import text_remover_html_tag


class SimhashStr():
    def __init__(self, str):
        self.str = str

    # 得到输入字符串的hash值
    def get_hash(self, need_cleaning=None, clean_method='re'):
        if need_cleaning:
            # 清洗数据
            content = text_remover_html_tag(html=self.str, method=clean_method)
            self.str = content
            # 结巴分词
        seg = jieba.cut(self.str)
        # 取前20个关键词
        keyword = jieba.analyse.extract_tags('|'.join(seg), topK=20, withWeight=True, allowPOS=())
        keyList = []
        # 获取每个词的权重
        for feature, weight in keyword:
            # 每个关键词的权重*总单词数
            weight = int(weight * 20)
            # 获取每个关键词的特征
            feature = self.string_hash(feature)
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
        return simhash

    def string_hash(self, feature):
        if feature == "":
            return 0
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
            return str(x)


if __name__ == '__main__':
    str1 = ""
    sim1 = SimhashStr(str1).get_hash(need_cleaning=True)
    print(sim1)
