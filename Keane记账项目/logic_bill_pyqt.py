#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  logic_bill_pyqt.py
:time  2025/4/21 12:30
:desc  
"""
import pandas as pd
from pathlib import Path
from typing import Tuple, List, Dict, Any
from dataclasses import dataclass


@dataclass
class BillInfo:
    pass


class LogicBill:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.bill_info = self._read_bill()
        self.income_rek = self.income_remark()
        self.expense_rek = self.expense_remark()

    def _read_bill(self):
        bill_path = self.base_path / '个人记账单.xlsx'
        df_dict = pd.read_excel(bill_path, sheet_name=None, header=0)
        return df_dict

    def income_remark(self) -> List:
        """收入备注"""
        df = self.bill_info["收入支出类型"]
        remark = df["incomeType"].to_list()
        return remark

    def expense_remark(self) -> List:
        """支出备注"""
        df = self.bill_info["收入支出类型"]
        remark = df["expenseType"].to_list()
        return remark

    def bank_card(self) -> List[Dict]:
        """银行卡信息"""
        df = self.bill_info["银行卡"]
        return df.to_dict('records')

    def summary_bill(self):
        """账单汇总"""

    def add_record(self, record: Dict[str, Any]):
        """新增一条记录
        record = {
        "date":"1",
        "income":1,
        "incomeType":"1",
        "expense":1,
        "expenseType":"1",
        }"""
        df = self.bill_info["账单流水"]
        df.loc[len(df.index)] = record
        bill_path = self.base_path / '个人记账单.xlsx'
        with pd.ExcelWriter(str(bill_path), engine="openpyxl") as writer:
            for sheet_name,df in self.bill_info.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    def show_intraday_bill(self):
        """展示当天账单"""
        df = self.bill_info["账单流水"]
        return df


if __name__ == '__main__':
    bill = LogicBill()
    record = {
        "date": "1",
        "income": 1,
        "incomeType": "1",
        "expense": 1,
        "expenseType": "1",
    }
    bill.add_record(record)