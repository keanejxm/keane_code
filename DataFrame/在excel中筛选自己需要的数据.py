#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  在excel中筛选自己需要的数据.py
:time  2024/1/9 14:52
:desc  根据表头字段筛选需要的数据
"""
import pandas as pd

df = pd.read_excel("g_net_v_exl.xlsx")


def filter_column(df):
    """
    pass
    :param column:df中的表头
    :param df:
    :param table_data:
    :return:
    """
    # 产品名称
    product_names = ["产品名称", "客户名称", "客户姓名", "账号名称", "投资者名称", "TA账号名称", "账户名",
                     "交易账户名称"]
    # 基金代码
    fund_code = ["基金代码", "产品代码", "资产代码", "产品编码", "TA代码"]
    # 基金名称
    fund_name = ["账套名称", "基金名称", "资产名称", "产品名称", "产品全称", "客户姓名", "基金中文名称"]
    # 虚拟净值
    net_value = ["单位净值", "基金份额净值", "计提后单位净值", "计算日产品净值", "资产份额净值", "虚拟单位净值",
                 "虚拟净值", "试算单位净值（扣除业绩报酬后）", "虚拟后净值", "单位净值列值"]
    # 日期
    date_time = ["日期", "净值日期", "最新净值日期", "估值基准日", "业务日期", "估值日期", "日期(相等值)",
                 "计算日期(相等值)", "基金净值日期", "截止日期", "份额日期", "份额查询日期"]
    # 余额日期20231109：银叶产品中需要获取的日期为余额日期
    balance_datetime = ["余额日期"]
    column_map = {
        "productName": product_names,
        "fundCode": fund_code,
        "fundName": fund_name,
        "netValue": net_value,
        "dateTime": date_time,
        "balanceDateTime": balance_datetime
    }
    column_info = dict()
    column_names = [column_name for column_name in df.columns if not pd.isna(column_name)]
    for column_name in column_names:
        if "份额" in column_name and "净值" not in column_name and "虚拟" not in column_name and "日期" not in \
                column_name and "占比" not in column_name and "tranche" in column_info:
            column_info["tranche"] = column_name
        for column_key, column_value in column_map.items():
            if column_name in column_value and column_key not in column_info:
                column_info[column_key] = column_name
    return column_info


def fetch_data(column_info, df_value, row_dict):
    for column_key, column_value in column_info.items():
        row_dict[column_key] = df_value[column_value]
        if len(column_info) == 1:
            return row_dict
    return row_dict


def filter_column_data(column_info, df):
    """
    从df中获取数据，针对表格g_net_v_exl表格，此表格在general_net_value中适用，
    TODO:需要后期不断更新
    :param column_info:
    :param df:
    :return:
    """
    row_data = list()
    for df_index, df_value in df.iterrows():
        row_dict = dict()
        for column_key, column_value in column_info.items():
            row_dict[column_key] = df_value[column_value]
            if len(column_info) == 1:
                row_data.append(row_dict)
                return row_data
        row_data.append(row_dict)
    return row_data


new_data = dict()
for df_index, df_value in df.iterrows():
    if df_index == 0:
        new_df = df
    else:
        # print(df.iloc[df_index-1:df_index,:].values)
        new_df = pd.DataFrame(df.iloc[df_index:, :].values,
                              columns=df.iloc[df_index - 1:df_index, :].values.tolist()[0])
        # new_df = pd.DataFrame(df.iloc[df_index-1:, :].values)
    column_info = filter_column(new_df)
    if column_info:
        new_data[len(column_info)] = filter_column_data(column_info, new_df)
print(new_data)

need_word = ["productName", "fundName", "fundCode", "netValue", "DateTime", "balanceDateTime"]

a = {1: [{'productName': '建信信托-鑫享14天1号集合资金信托计划'}],
     4: [
         {'dateTime': '2024-01-05', 'fundCode': 'SVW938', 'fundName': '银叶积汇1号私募证券投资基金',
          'netValue': '1.0243'},
         {'dateTime': '2024-01-05', 'fundCode': 'SVW938', 'fundName': '银叶积汇1号私募证券投资基金',
          'netValue': '1.0243'}]
     }

c = [{'productName': '建信信托-鑫享14天1号集合资金信托计划'}]

b = [
    {'dateTime': '2024-01-05', 'fundCode': 'SVW938', 'fundName': '银叶积汇1号私募证券投资基金',
     'netValue': '1.0243'},
    {'dateTime': '2024-01-05', 'fundCode': 'SVW938', 'fundName': '银叶积汇1号私募证券投资基金',
     'netValue': '1.0243'}]
c_df = pd.DataFrame(c)
b_df = pd.DataFrame(b)

new_df_a = pd.concat([c_df, b_df], axis=1)
new_df_a.fillna(method = 'ffill',inplace=True)
print(new_df)
