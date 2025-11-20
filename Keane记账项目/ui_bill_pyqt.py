#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  ui_bill_pyqt.py
:time  2025/4/21 12:29
:desc  
"""
import sys
from PyQt5.QtWidgets import (QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
                             QHeaderView, QPushButton, QHBoxLayout,
                             QLabel, QLineEdit, QDateEdit, QComboBox)
from PyQt5.QtCore import Qt, QDate


class FinanceTracker(object):
    def setupUI(self):
        # 主部件和布局
        self.main_widget = QWidget()
        main_layout = QVBoxLayout()

        # 标题
        title_label = QLabel("个人收支记录表")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 输入区域
        input_layout = QHBoxLayout()

        # 日期输入
        date_label = QLabel("日期:")
        self.date_edit = QDateEdit()

        # 收入类型选择
        income_label = QLabel("收入类型:")
        self.income_combo = QComboBox()
        self.income_combo_text = QLineEdit()
        self.income_combo_text.setPlaceholderText("工资收入(元)")
        # 收入金额
        income_amount_label = QLabel("金额:")
        self.income_amount_edit = QLineEdit()
        self.income_amount_edit.setPlaceholderText("收入金额")

        # 支出类型选择
        expense_label = QLabel("支出类型:")
        self.expense_combo = QComboBox()
        self.expense_combo_text = QLineEdit()
        self.expense_combo_text.setPlaceholderText("贷款支出(元)")

        # 支出金额
        expense_amount_label = QLabel("金额:")
        self.expense_amount_edit = QLineEdit()
        self.expense_amount_edit.setPlaceholderText("支出金额")

        # 添加按钮
        self.add_button = QPushButton("添加记录")


        # 将输入控件添加到布局
        input_layout.addWidget(date_label)
        input_layout.addWidget(self.date_edit)
        input_layout.addWidget(income_label)
        input_layout.addWidget(self.income_combo)
        input_layout.addWidget(self.income_combo_text)
        input_layout.addWidget(income_amount_label)
        input_layout.addWidget(self.income_amount_edit)
        input_layout.addWidget(expense_label)
        input_layout.addWidget(self.expense_combo)
        input_layout.addWidget(self.expense_combo_text)
        input_layout.addWidget(expense_amount_label)
        input_layout.addWidget(self.expense_amount_edit)
        input_layout.addWidget(self.add_button)
        main_layout.addLayout(input_layout)

        # 创建表格
        self.table = QTableWidget()
        self.table.setColumnCount(6)  # 日期 + 收入+收入备注 + 支出 + 支出备注 +余额

        # 创建自定义表头
        self.create_custom_header()

        # 设置表格样式
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 5px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)

        main_layout.addWidget(self.table)

        # 底部按钮
        button_layout = QHBoxLayout()
        clear_button = QPushButton("清空表格")
        export_button = QPushButton("导出数据")
        # 账单汇总
        summary_bill = QPushButton("账单汇总")
        # 账单图示
        graph_bill = QPushButton("账单图示")

        button_layout.addWidget(clear_button)
        button_layout.addWidget(export_button)
        button_layout.addWidget(summary_bill)
        button_layout.addWidget(graph_bill)
        main_layout.addLayout(button_layout)

        self.main_widget.setLayout(main_layout)
        # self.setCentralWidget(main_widget)

        # 初始化余额
        self.balance = 0.0

    def create_custom_header(self):
        # 创建主表头"收入"和"支出"
        header = self.table.horizontalHeader()

        # 合并单元格创建主表头
        # 收入主表头 (合并列1-3)
        self.table.setSpan(0, 1, 1, 3)
        # 支出主表头 (合并列4-7)
        self.table.setSpan(0, 4, 1, 4)

        # 设置主表头文本
        income_header = QTableWidgetItem("收入")
        income_header.setTextAlignment(Qt.AlignCenter)
        self.table.setVerticalHeaderItem(0, income_header)
        # self.table.setHorizontalHeaderItem(1, income_header)

        expense_header = QTableWidgetItem("支出")
        expense_header.setTextAlignment(Qt.AlignCenter)
        self.table.setVerticalHeaderItem(4, expense_header)
        # self.table.setHorizontalHeaderItem(4, expense_header)

        # 设置子表头文本
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("日期"))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem("收入(元)"))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem("收入类型"))
        self.table.setHorizontalHeaderItem(3, QTableWidgetItem("支出(元)"))
        self.table.setHorizontalHeaderItem(4, QTableWidgetItem("支出类型"))
        self.table.setHorizontalHeaderItem(5, QTableWidgetItem("余额(元)"))
