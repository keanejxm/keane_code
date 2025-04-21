#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  call_bill_pyqt.py
:time  2025/4/21 12:30
:desc  
"""
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget,
                             QHeaderView, QPushButton, QHBoxLayout,
                             QLabel, QLineEdit, QDateEdit, QComboBox)
from ui_bill_pyqt import FinanceTracker
from logic_bill_pyqt import LogicBill
from PyQt5.QtCore import Qt, QDate


class CallBill(QMainWindow, FinanceTracker):
    def __init__(self):
        super().__init__()
        self.logic_bill = LogicBill()
        self.setWindowTitle("收支记录表格")
        self.setGeometry(100, 100, 1000, 600)
        self.setupUI()
        self.setCentralWidget(self.main_widget)
        self.initUI()

    def initUI(self):
        # 日期输入
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_edit.setDate(QDate.currentDate())

        # 收入类型选择
        self.income_combo.addItems(self.logic_bill.income_rek)

        # 支出类型选择
        self.expense_combo.addItems(self.logic_bill.expense_rek)

        # 展示当日账单
        self.show_today_bill()

        # 添加一条记录
        self.add_button.clicked.connect(self.add_record)

    def show_today_bill(self):
        """展示当日账单"""
        bill_df = self.logic_bill.show_intraday_bill()
        for _, record in bill_df.iterrows():
            # 添加新行
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            # 设置单元格数据
            self.table.setItem(row_position, 0, QTableWidgetItem(record["date"]))

            # 收入列
            self.table.setItem(row_position, 1, QTableWidgetItem(str(record["income"])))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(record["incomeType"])))
            self.table.setItem(row_position, 3, QTableWidgetItem(str(record["expense"])))
            self.table.setItem(row_position, 4, QTableWidgetItem(str(record["expenseType"])))

    def add_record(self):
        # 获取输入值
        date = self.date_edit.date().toString("yyyy-MM-dd")
        income_type = self.income_combo.currentText()
        income_amount = self.income_amount_edit.text()
        expense_type = self.expense_combo.currentText()
        expense_amount = self.expense_amount_edit.text()
        # 验证金额
        try:
            income = float(income_amount) if income_amount else 0.0
            expense = float(expense_amount) if expense_amount else 0.0
        except ValueError:
            return
        record = {
            "date": date,
            "income": income,
            "incomeType": income_type,
            "expense": expense,
            "expenseType": expense_type,
        }
        self.logic_bill.add_record(record)
        self.show_today_bill()
        # 清空输入
        self.income_amount_edit.clear()
        self.expense_amount_edit.clear()

    def clear_table(self):
        self.table.setRowCount(0)
        self.balance = 0.0

    def export_data(self):
        # 这里可以添加导出到Excel或CSV的功能
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CallBill()
    window.show()
    sys.exit(app.exec_())
