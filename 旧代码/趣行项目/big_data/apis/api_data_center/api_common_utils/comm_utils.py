# -*- coding:utf-8 -*-
"""
# project: 公共工具仅供智能检索使用
# author: Neil
# date: 2020/12/9
# update: 2020/12/9
"""
import datetime
import re
import time
import jieba
import difflib
import numpy as np
from collections import Counter


class CommUtils:

    @staticmethod
    def pydiffcount(str1, str2):
        """
        判断str1, str2的相似度结果为浮点型。
        :param str1:
        :param str2:
        :return:
        """
        diff_result = difflib.SequenceMatcher(None, str1, str2).ratio()
        return diff_result

    @staticmethod
    def editcount(str1, str2):
        """
        numpy
        :param str1:
        :param str2:
        :return:
        """
        len_str1 = len(str1)
        len_str2 = len(str2)
        # 二维数组，x行y列
        taglist = np.zeros((len_str1 + 1, len_str2 + 1))
        for a in range(len_str1):
            taglist[a][0] = a
        for a in range(len_str2):
            taglist[0][a] = a
        for i in range(1, len_str1 + 1):
            for j in range(1, len_str2 + 1):
                if str1[i - 1] == str2[j - 1]:
                    temp = 0
                else:
                    temp = 1
                taglist[i][j] = min(taglist[i - 1][j - 1] + temp, taglist[i][j - 1] + 1, taglist[i - 1][j] + 1)
        return 1 - taglist[len_str1][len_str2] / max(len_str1, len_str2)

    @staticmethod
    def coscount(str1, str2):
        """
        numpy进行结果比对
        :param str1:
        :param str2:
        :return:
        """
        co_str1 = (Counter(str1))
        co_str2 = (Counter(str2))
        p_str1 = []
        p_str2 = []
        for temp in set(str1 + str2):
            p_str1.append(co_str1[temp])
            p_str2.append(co_str2[temp])
        p_str1 = np.array(p_str1)
        p_str2 = np.array(p_str2)
        return p_str1.dot(p_str2) / (np.sqrt(p_str1.dot(p_str1)) * np.sqrt(p_str2.dot(p_str2)))

    def getsimilarity(self, strA, strB):
        """
        返回最终结果
        :param strA:
        :param strB:
        :return:
        """
        if strA == strB:
            return 1.0
        listA = jieba.lcut(strA)
        listB = jieba.lcut(strB)
        pydiffValue = self.pydiffcount(strA, strB)
        editValue = self.editcount(listA, listB)
        cosValue = self.coscount(listA, listB)
        score = cosValue * 0.4 + editValue * 0.3 + 0.3 * pydiffValue
        return score

    def getPublicTime(self, string):
        """
        对获取的时间标签进行处理
        :param string:
        :return:
        """
        pattern = r"(?P<year>(20|21)?\d{2})[.年/-](?P<month>\d{1,2})[.月/-](?P<day>\d{1,2})[.日]?([\s]{0,4}(?P<hour>\d{1,2})[:：](?P<minute>\d{1,2})([:：](?P<second>\d{1,2}))?)?"
        match = re.search(pattern, string, flags=0)
        if match:
            groupDict = match.groupdict()
            year = "0000"
            month = "00"
            day = "00"
            hour = "00"
            minute = "00"
            second = "00"
            if 'year' in groupDict:
                year = groupDict['year']
                if len(year) == 2:
                    nowyear = str(datetime.datetime.now().year)[0:2]
                    year = nowyear + year
            if 'month' in groupDict:
                month = groupDict['month']
                if len(month) == 1:
                    month = "0" + month
            if 'day' in groupDict:
                day = groupDict['day']
                if len(day) == 1:
                    day = "0" + day
            if groupDict['hour'] is not None:
                hour = groupDict['hour']
                if len(hour) == 1:
                    hour = "0" + hour
            if groupDict['minute'] is not None:
                minute = groupDict['minute']
                if len(minute) == 1:
                    minute = "0" + minute
            if groupDict['second'] is not None:
                second = groupDict['second']
                if len(second) == 1:
                    second = "0" + second
            publicTime = year + month + day + hour + minute + second
            timeArray = time.strptime(publicTime, "%Y%m%d%H%M%S")
            timeStamp = int(time.mktime(timeArray))
            return timeStamp
