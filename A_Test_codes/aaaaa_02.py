#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_02.py
:time  2025/3/13 9:53
:desc  #
"""
import pandas as pd

df = pd.DataFrame([[1,2,3,4],[5,6,7,8],[9,10,11,12]],columns=['A','B','C','D'])
df.sort_values('A',ascending=True,inplace=True)
print(df)