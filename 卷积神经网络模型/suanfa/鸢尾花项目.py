#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_02.py
:time  2025/3/13 9:53
:desc  #经典入门案例
"""
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import sklearn.metrics as sm

# 加载数据
iris = load_iris()
x,y = iris.data, iris.target

# 划分训练集与测试集
train_x,test_x,train_y,test_y = train_test_split(x,y,test_size=0.2)

# 训练knn模型
knn = KNeighborsClassifier()
knn.fit(train_x,train_y)
y_pred = knn.predict(test_x)

# 评估
print(sm.classification_report(test_y, y_pred))

# print(sm.accuracy_score(test_y, y_pred))
# print(sm.r2_score(test_y, y_pred))
print(sm.precision_score(test_y, y_pred, average='macro'))
print(sm.recall_score(test_y, y_pred, average='macro'))

# print(knn.score(test_x,test_y))