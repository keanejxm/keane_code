#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_01.py
:time  2025/1/26 13:54
:desc  
"""
import numpy as np
import sklearn.linear_model as lr
import sklearn.metrics as sm
import sklearn.model_selection as ms
import sklearn.pipeline as pp
import sklearn.preprocessing as sp
import pickle as pkl

# pp.make_pipeline(sp.PolynomialFeatures(2), lr.LinearRegression())
data1 = np.array([[1,2],[3,4]])
data2 = np.array([[5,6]])
mms = sp.MinMaxScaler()
data = mms.fit(data1)
data1_r = mms.transform(data1)
data2_r = mms.transform(data2)
print(data1_r)
print(data2_r)
# mms.transform([1,2,3,4,5])
# lr.LinearRegression()
