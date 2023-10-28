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
# 筛选出某列不包含关键字的数据
res_df1 = df[~df["账套全称"].str.contains("阳光", na=True)]
# 筛选出某列包含关键字的数据
res_df2 = df[df["账套全称"].str.contains("阳光", na=True)]
# 修改某一行某一列的值
for df_index, df_value in df.iterrows():
    df.loc[df_index, "aaaaa"] = "aaaa"
    # 修改值等于值的值
    df.loc[df['is_dup'] == True, "is_dup"] = "是"

# dataFrame排序
df.sort_values(by = ["column"],ascending=True)
# 使用正则替换
df = df.apply(lambda x: x.str.replace(r"\s+", "", regex=True))