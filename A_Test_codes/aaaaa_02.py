#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_02.py
:time  2025/3/13 9:53
:desc  #
"""
import pandas as pd

df = pd.DataFrame([[2,"14000",3,4],[1,"1750",7,8]],columns=['A','B','C','D'])
# df.sort_values(['A','B'],ascending=[True,True],inplace=True)
a = df.loc[:,"B"]
print(a)