#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  pdf_reader_1.0.py
:time  2025/4/23 14:38
:desc  
"""
import sys
import fitz  # PyMuPDF
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QFileDialog,
                             QScrollArea, QSpinBox, QSizePolicy)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QSize


class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF阅读器")
        self.setMinimumSize(400, 300)  # 设置最小窗口大小
        self.resize(800, 600)  # 初始窗口大小

        # 主窗口部件
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # 布局
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        self.main_widget.setLayout(self.main_layout)

        # 工具栏
        self.toolbar_layout = QHBoxLayout()
        self.toolbar_layout.setSpacing(10)
        self.main_layout.addLayout(self.toolbar_layout)

        # 打开文件按钮
        self.open_button = QPushButton("打开PDF")
        self.open_button.clicked.connect(self.open_pdf)
        self.toolbar_layout.addWidget(self.open_button)

        # 页面导航
        self.prev_button = QPushButton("上一页")
        self.prev_button.clicked.connect(self.prev_page)
        self.prev_button.setEnabled(False)
        self.toolbar_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("下一页")
        self.next_button.clicked.connect(self.next_page)
        self.next_button.setEnabled(False)
        self.toolbar_layout.addWidget(self.next_button)

        # 页面跳转
        self.page_label = QLabel("页面:")
        self.toolbar_layout.addWidget(self.page_label)

        self.page_spin = QSpinBox()
        self.page_spin.setMinimum(1)
        self.page_spin.valueChanged.connect(self.go_to_page)
        self.toolbar_layout.addWidget(self.page_spin)

        self.page_count_label = QLabel("/ 0")
        self.toolbar_layout.addWidget(self.page_count_label)

        # 缩放控制
        self.zoom_in_button = QPushButton("放大")
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.toolbar_layout.addWidget(self.zoom_in_button)

        self.zoom_out_button = QPushButton("缩小")
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.toolbar_layout.addWidget(self.zoom_out_button)

        # 显示区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_layout.addWidget(self.scroll_area)

        self.pdf_label = QLabel()
        self.pdf_label.setAlignment(Qt.AlignCenter)
        self.pdf_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.scroll_area.setWidget(self.pdf_label)

        # PDF相关变量
        self.doc = None
        self.current_page = 0
        self.zoom_factor = 1.0
        self.base_page_size = QSize(0, 0)  # 存储PDF页面的原始大小

    def open_pdf(self):
        """打开PDF文件"""
        file_path, _ = QFileDialog.getOpenFileName(self, "打开PDF文件", "", "PDF文件 (*.pdf)")

        if file_path:
            try:
                # 关闭当前文档(如果存在)
                if self.doc:
                    self.doc.close()

                # 打开新文档
                self.doc = fitz.open(file_path)
                self.current_page = 0
                self.zoom_factor = 1.0

                # 更新页面导航
                self.page_spin.setMaximum(len(self.doc))
                self.page_count_label.setText(f"/ {len(self.doc)}")

                # 启用按钮
                self.prev_button.setEnabled(len(self.doc) > 1)
                self.next_button.setEnabled(len(self.doc) > 1)

                # 显示第一页
                self.display_page()

                # 自动调整窗口大小
                self.adjust_window_size()

            except Exception as e:
                print(f"打开PDF失败: {e}")

    def display_page(self):
        """显示当前页"""
        if self.doc and 0 <= self.current_page < len(self.doc):
            # 获取页面
            page = self.doc.load_page(self.current_page)

            # 设置缩放
            zoom_matrix = fitz.Matrix(self.zoom_factor, self.zoom_factor)

            # 渲染页面为图像
            pix = page.get_pixmap(matrix=zoom_matrix, alpha=False)

            # 转换为QPixmap
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img)

            # 存储页面原始大小(首次加载时)
            if self.base_page_size.isNull() or self.current_page == 0:
                self.base_page_size = QSize(pix.width, pix.height)

            # 显示图像
            self.pdf_label.setPixmap(pixmap)
            self.pdf_label.resize(pix.width, pix.height)

            # 更新页面计数器
            self.page_spin.setValue(self.current_page + 1)
            # self.adjust_window_size()

    def adjust_window_size(self):
        """根据PDF页面大小调整窗口大小"""
        if not self.base_page_size.isNull():
            # 计算新窗口大小 (页面大小 + 工具栏和边距)
            margin_width = 40  # 左右边距和滚动条宽度
            margin_height = 100  # 工具栏高度和上下边距

            new_width = min(self.base_page_size.width() + margin_width, 1600)  # 限制最大宽度
            new_height = min(self.base_page_size.height() + margin_height, 1200)  # 限制最大高度

            # 确保不小于最小尺寸
            new_width = max(new_width, self.minimumWidth())
            new_height = max(new_height, self.minimumHeight())

            # 调整窗口大小
            self.resize(new_width, new_height)

            # 居中显示
            screen_geometry = QApplication.desktop().screenGeometry()
            x = (screen_geometry.width() - new_width) // 2
            y = (screen_geometry.height() - new_height) // 2
            self.move(x, y)

    def prev_page(self):
        """显示上一页"""
        if self.doc and self.current_page > 0:
            self.current_page -= 1
            self.display_page()

    def next_page(self):
        """显示下一页"""
        if self.doc and self.current_page < len(self.doc) - 1:
            self.current_page += 1
            self.display_page()

    def go_to_page(self, page_num):
        """跳转到指定页"""
        if self.doc and 1 <= page_num <= len(self.doc):
            self.current_page = page_num - 1
            self.display_page()

    def zoom_in(self):
        """放大"""
        self.zoom_factor *= 1.2
        if self.doc:
            self.display_page()

    def zoom_out(self):
        """缩小"""
        self.zoom_factor /= 1.2
        if self.zoom_factor < 0.2:  # 防止缩得过小
            self.zoom_factor = 0.2
        if self.doc:
            self.display_page()

    def resizeEvent(self, event):
        """窗口大小改变事件"""
        super().resizeEvent(event)
        # 可以在这里添加响应窗口大小变化的逻辑
        # 例如自动调整缩放比例等


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec_())