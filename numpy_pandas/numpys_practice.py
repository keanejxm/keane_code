#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  numpys_practice.py
:time  2023/9/28 16:46
:desc  练习numpy
"""
import numpy as np
import pandas as pd

print(np.__version__)
"""
1、numpy中的数据类型
  理解python中的数据类型：
    动态类型语言-->理解这一特性如何工作
              -->python变量不仅是他们的值还包括了关于值的类型的一些信息
    静态类型语言
    
        python整型不仅仅是一个整型
2、创建数组
3、numpy数组属性——>数组索引、数组切片、数组变形、数组拼接分裂  
"""

print(np.zeros(10, dtype=int))
print(np.ones((3, 5), dtype=float))
print(np.full((3, 5), 3.14, dtype=float))
print(np.arange(0, 20, 2))
print(np.linspace(0, 1, 5))
print(np.random.random((3, 3)))
print(np.random.normal(0, 1, (3, 3)))
print(np.random.randint(0, 10, (3, 3)))
print(np.eye(3))
print(np.empty(3))
# numpy数组属性（ndim、shape、size；dtype，itemsize）
np.random.seed(0)
x1 = np.random.randint(10, size=6)
x2 = np.random.randint(10, size=(3, 4))
x3 = np.random.randint(10, size=(3, 4, 5))
for i in [x1, x2, x3]:
    print(i.ndim, i.shape, i.size)
# 数组属性、数组索引、数组切片（一维子数组、多维子数组、获取数组的行和列、非副本视图子数组、创建数组的副本）、数组的变形reshape,newaxis、数组的拼接和分裂
# 2.2数组属性、数组索引、数组切片（一维子数组，多维子数组、获取数组的行和列、非副本视图子数组、创建数组的副本）、数组的变形、数组的拼接和分裂
# 2.3数组运算:求倒数、绝对值、三角函数（逆三角函数）、指数和对数、指定输出、聚合、外积  
population_dict = {'California': 38332521, 'Texas': 26448193, 'New York': 19651127, 'Florida': 19552860,
                   'Illinois': 12882135}
area_dict = {'California': 423967, 'Texas': 695662, 'New York': 141297, 'Florida': 170312,
             'Illinois': 149995}
pop_dict = {'California': 38332521, 'Texas': 26448193, 'New York': 19651127, 'Florida': 19552860,
            'Illinois': 12882135}
index = [('California', 2000), ('California', 2010), ('New York', 2000), ('New York', 2010), ('Texas', 2000),
         ('Texas', 2010)]
def make_df(cols,ind):
    data = {c:[str(c) +str(i) for i in ind] for c in cols}
    return pd.DataFrame(data,ind)


print(make_df('ABC', range(3)))