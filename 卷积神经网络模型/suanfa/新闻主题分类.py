#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_02.py
:time  2025/3/13 9:53
:desc  # 多分类
"""
from sklearn.datasets import fetch_20newsgroups
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

# 加载数据
categories = ['sci.space', 'rec.sport.baseball', 'comp.graphics', 'talk.politics']
newsgroups = fetch_20newsgroups(categories=categories, shuffle=True, random_state=42)

# 文本向量化（TF-IDF）
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(newsgroups.data)

# 训练模型
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X, newsgroups.target)

# 预测示例
new_text = ["NASA announced new Mars mission"]
print(newsgroups.target_names[clf.predict(vectorizer.transform(new_text))[0]])