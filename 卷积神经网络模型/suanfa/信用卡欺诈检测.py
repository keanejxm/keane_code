#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_02.py
:time  2025/3/13 9:53
:desc  # 不平衡数据
"""
from sklearn.tree import DecisionTreeClassifier
import sklearn.metrics as sm

X_train = []
y_train = []
# 假设X_train,y_train已准备好（0=正常，1=欺诈）
model = DecisionTreeClassifier(
    class_weight={0:1,1:10},
    max_depth=5,
)

model.fit(X_train,y_train)

# 评估（关注召回率）
print(sm.classification_report(y_train,model.predict(X_train)))