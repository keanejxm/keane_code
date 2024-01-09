#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  在excel中筛选自己需要的数据.py
:time  2024/1/9 14:52
:desc  根据表头字段筛选需要的数据
"""
import pandas as pd

df = pd.read_excel("aaa.xlsx")

# 获取的字段
keys = {
    "客户名称": {"num": 1, "map": "productName","columnName":"客户名称"},
    "基金名称": {"num": 2, "map": "fundName","columnName":"基金名称"},
}
filter_list = list()
for df_index, df_value in df.iterrows():
    rows_list = list()
    column_list = df_value.to_list()
    new_df = pd.DataFrame(df.iloc[df_index+1:, :].values, columns=column_list)
    print(df_index, column_list)
    for d_key, d_value in keys.items():
        if d_key in column_list:
            rows_dict = dict()
            for new_df_index, new_df_value in new_df.iterrows():
                map_name = d_value["map"]
                rows_dict[map_name] = new_df_value[d_key]
                rows_list.append(rows_dict)
                if new_df_index + 1 == d_value["num"]:
                    break
    if rows_list:
        filter_list.append(rows_list)
    print("-------------------")
