#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  bill_pyqt.py
:time  2025/4/21 10:23
:desc  
"""
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget,
                             QHeaderView, QPushButton, QHBoxLayout,
                             QLabel, QLineEdit, QDateEdit, QComboBox)
from PyQt5.QtCore import Qt, QDate


class FinanceTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("收支记录表格")
        self.setGeometry(100, 100, 1000, 600)

        self.initUI()

    def initUI(self):
        # 主部件和布局
        main_widget = QWidget()
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
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_edit.setDate(QDate.currentDate())

        # 收入类型选择
        income_label = QLabel("收入类型:")
        self.income_combo = QComboBox()
        self.income_combo.addItems(["工资收入", "其他收入"])

        # 收入金额
        income_amount_label = QLabel("金额:")
        self.income_amount_edit = QLineEdit()
        self.income_amount_edit.setPlaceholderText("收入金额")

        # 支出类型选择
        expense_label = QLabel("支出类型:")
        self.expense_combo = QComboBox()
        self.expense_combo.addItems(["房贷支出", "京东白条", "京东金条", "租房支出"])

        # 支出金额
        expense_amount_label = QLabel("金额:")
        self.expense_amount_edit = QLineEdit()
        self.expense_amount_edit.setPlaceholderText("支出金额")

        # 备注
        note_label = QLabel("备注:")
        self.note_edit = QLineEdit()
        self.note_edit.setPlaceholderText("可选备注")

        # 添加按钮
        add_button = QPushButton("添加记录")
        add_button.clicked.connect(self.add_record)

        # 将输入控件添加到布局
        input_layout.addWidget(date_label)
        input_layout.addWidget(self.date_edit)
        input_layout.addWidget(income_label)
        input_layout.addWidget(self.income_combo)
        input_layout.addWidget(income_amount_label)
        input_layout.addWidget(self.income_amount_edit)
        input_layout.addWidget(expense_label)
        input_layout.addWidget(self.expense_combo)
        input_layout.addWidget(expense_amount_label)
        input_layout.addWidget(self.expense_amount_edit)
        input_layout.addWidget(note_label)
        input_layout.addWidget(self.note_edit)
        input_layout.addWidget(add_button)

        main_layout.addLayout(input_layout)

        # 创建表格
        self.table = QTableWidget()
        self.table.setColumnCount(8)  # 日期 + 收入(3列) + 支出(4列) + 余额

        # 设置表头 - 先设置基本列名
        self.table.setHorizontalHeaderLabels([
            "日期",
            "工资收入(元)",
            "其他收入(元)",
            "收入备注",
            "房贷支出(元)",
            "京东白条",
            "京东金条",
            "租房支出",
            "余额(元)"
        ])

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
        clear_button.clicked.connect(self.clear_table)
        export_button = QPushButton("导出数据")
        export_button.clicked.connect(self.export_data)

        button_layout.addWidget(clear_button)
        button_layout.addWidget(export_button)
        main_layout.addLayout(button_layout)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

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
        self.table.setHorizontalHeaderItem(1, income_header)

        expense_header = QTableWidgetItem("支出")
        expense_header.setTextAlignment(Qt.AlignCenter)
        self.table.setHorizontalHeaderItem(4, expense_header)

        # 设置子表头文本
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem("工资收入(元)"))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem("其他收入(元)"))
        self.table.setHorizontalHeaderItem(3, QTableWidgetItem("收入备注"))
        self.table.setHorizontalHeaderItem(4, QTableWidgetItem("房贷支出(元)"))
        self.table.setHorizontalHeaderItem(5, QTableWidgetItem("京东白条"))
        self.table.setHorizontalHeaderItem(6, QTableWidgetItem("京东金条"))
        self.table.setHorizontalHeaderItem(7, QTableWidgetItem("租房支出"))

    def add_record(self):
        # 获取输入值
        date = self.date_edit.date().toString("yyyy-MM-dd")
        income_type = self.income_combo.currentText()
        income_amount = self.income_amount_edit.text()
        expense_type = self.expense_combo.currentText()
        expense_amount = self.expense_amount_edit.text()
        note = self.note_edit.text()

        # 验证金额
        try:
            income = float(income_amount) if income_amount else 0.0
            expense = float(expense_amount) if expense_amount else 0.0
        except ValueError:
            return

        # 计算余额
        self.balance += income - expense

        # 添加新行
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        # 设置单元格数据
        self.table.setItem(row_position, 0, QTableWidgetItem(date))

        # 收入列
        if income_type == "工资收入":
            self.table.setItem(row_position, 1, QTableWidgetItem(str(income)))
            self.table.setItem(row_position, 2, QTableWidgetItem("0"))
        else:
            self.table.setItem(row_position, 1, QTableWidgetItem("0"))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(income)))

        # 收入备注
        self.table.setItem(row_position, 3, QTableWidgetItem(note if note else ""))

        # 支出列
        expense_col = {
            "房贷支出": 4,
            "京东白条": 5,
            "京东金条": 6,
            "租房支出": 7
        }

        # 先清空所有支出列
        for col in range(4, 8):
            self.table.setItem(row_position, col, QTableWidgetItem("0"))

        # 设置当前支出
        col = expense_col[expense_type]
        self.table.setItem(row_position, col, QTableWidgetItem(str(expense)))

        # 设置余额
        self.table.setItem(row_position, 8, QTableWidgetItem(f"{self.balance:.2f}"))

        # 清空输入
        self.income_amount_edit.clear()
        self.expense_amount_edit.clear()
        self.note_edit.clear()

    def clear_table(self):
        self.table.setRowCount(0)
        self.balance = 0.0

    def export_data(self):
        # 这里可以添加导出到Excel或CSV的功能
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceTracker()
    window.show()
    sys.exit(app.exec_())