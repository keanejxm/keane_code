#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_02.py
:time  2025/3/13 9:53
:desc  # 二分类
"""
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression

# 加载数据
data = load_breast_cancer()
X,y = data.data,data.target

# 训练模型
model = LogisticRegression(max_iter=1000)
model.fit(X,y)

# 输出特征重要性
print("最重要的特征:", data.feature_names[model.coef_.argmax()])