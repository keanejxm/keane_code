#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_01.py
:time  2025/1/26 13:54
:desc  
"""
import os.path

import numpy as np
import pandas as pd
import pickle as pkl
import matplotlib.pyplot as plt

import sklearn
import sklearn.linear_model as lr
import sklearn.metrics as sm
import sklearn.model_selection as ms
import sklearn.pipeline as pp
import sklearn.preprocessing as sp
import sklearn.tree as st
import sklearn.ensemble as se
import sklearn.datasets as ds

x = np.array([[3, 1], [2, 5], [1, 8], [6, 4], [5, 2], [3, 5], [4, 7], [4, -1]])
y = np.array([0, 1, 1, 0, 0, 1, 1, 0])

# 构建模型
model = lr.LogisticRegression()
# 训练模型
model.fit(x, y)

# 预测
pred_y = model.predict(np.array([[3, 9], [6, 1]]))
print(pred_y)

a = x[:, 0]
b = x[:, 1]

plt.scatter(x[:, 0], x[:, 1])
plt.show()
