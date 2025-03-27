#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_02.py
:time  2025/3/13 9:53
:desc  #二分类
"""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

emails = ["免费领取奖品","会议通知查收","限时特惠"]
labels = [1,0,1]

# 文本向量化
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(emails)
# 训练模型
model = MultinomialNB()
model.fit(X, labels)

# 预测新邮件
new_email = ["优惠促销"]
print(model.predict(vectorizer.transform(new_email)))