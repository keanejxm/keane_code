#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_02.py
:time  2025/3/13 9:53
:desc  #多分类
"""
from sklearn import datasets
from sklearn import svm
import sklearn.metrics as sm

# 加载数据
digits = datasets.load_digits()
X,y = digits.data, digits.target

# 训练svm模型
clf = svm.SVC(gamma=0.001,C=100.)
clf.fit(X[:-100],y[:-100])

# 预测最后100个样本
predicted = clf.predict(X[-100:])
print(sm.accuracy_score(y[-100:],predicted))