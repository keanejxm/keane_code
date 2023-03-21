#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  operate.py
:time  2023/3/15 14:41
:desc  
"""
import pandas as pd
# 筛选
df = pd.read_excel("")
res_df = df[~df["账套全称"].str.contains("阳光",na=True)]
# 修改某一行某一列的值
for df_index,df_value in df.iterrows():
    df.loc[df_index,"aaaaa"] = "aaaa"