#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_01.py
:time  2025/1/26 13:54
:desc  
"""
import math
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
import sklearn.svm as svm

# 分类算法 逻辑回归、决策树、svm（支持向量机）、朴素贝叶斯
# 读取数据
files_dir = r"E:\keane_data\01_机器学习数据"
df_data = pd.read_csv(os.path.join(files_dir, "multiple2.txt"), header=None)
x = df_data.iloc[:, 0:-1]
y = df_data.iloc[:, -1]

# x_train, x_test, y_train, y_test = ms.train_test_split(x, y, test_size=0.2)

model = svm.SVC(kernel='linear', C=1, gamma=1)

model.fit(x, y)

# y_pred = model.predict(x_train)

c1, c2 = (y == 0), (y == 1)
x_array = np.array(x)
l, r, h = x_array[:, 0].min() - 1, x_array[:, 0].max() + 1, 0.005
b, t, v = x_array[:, 1].min() - 1, x_array[:, 1].max() + 1, 0.005
grid_x = np.meshgrid(np.arange(l, r, h), np.arange(b, t, v))
a_d = grid_x[0].ravel()
flat_x = np.c_[grid_x[0].ravel(), grid_x[1].ravel()]
flat_y = model.predict(flat_x)
grid_y = flat_y.reshape(grid_x[0].shape)
plt.pcolormesh(grid_x[0],grid_x[1],grid_y,cmap="gray")

# plt.figure("svm png")
# plt.xlabel("x")
# plt.ylabel("y")
# plt.scatter(x_array[(y==0)][:,0], x_array[(y==0)][:,1],c="orangered")
# plt.scatter(x_array[(y==1)][:,0], x_array[(y==1)][:,1],c="green")


plt.show()
