#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  排序.py
:time  2025/3/13 16:07
:desc  
"""
import pandas as pd

df = pd.DataFrame([[1,2,3,4],[1,3,3,4],[5,6,7,8],[9,10,11,12]],columns=['A','B','C','D'])
df.sort_values(['A',"B"],ascending=[True,False],inplace=True)
print(df)