#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_01.py
:time  2025/1/26 13:54
:desc  
"""

import numpy as np
import pandas as pd
import pickle as pkl

import sklearn
import sklearn.linear_model as lr
import sklearn.metrics as sm
import sklearn.model_selection as ms
import sklearn.pipeline as pp
import sklearn.preprocessing as sp
import sklearn.tree as st
import sklearn.ensemble as se
import sklearn.datasets as ds

# 下载数据
data = pd.read_excel("boston_data.xlsx")
# 划分特征和真实值
x = data.iloc[:, :-1]
y = data.iloc[:, -1]
# 划分训练集，测试集
train_x, test_x, train_y, test_y = sklearn.model_selection.train_test_split(
    x, y,
    test_size=0.2,
    random_state=42
)
# 构建模型
# tree_model = st.DecisionTreeRegressor()
tree_model = se.AdaBoostRegressor(
    st.DecisionTreeRegressor(max_depth=7),
    n_estimators=400,
    random_state=7
)
# tree_model = se.RandomForestRegressor(n_estimators=400,max_depth=15,random_state=42)
# tree_model = se.GradientBoostingRegressor(
#     n_estimators=100,
#     max_depth=10,
#     random_state=42,
# )
# 进行训练
tree_model.fit(train_x, train_y)
# 模型预测
pred_y = tree_model.predict(test_x)
feature = tree_model.feature_importances_
feature_name = tree_model.feature_names_in_
r2_score = sm.r2_score(test_y, pred_y)
print(r2_score)
# 保存模型