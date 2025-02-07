#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  使用pyqt完成展示图片.py
:time  2025/1/24 11:14
:desc  
"""
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap

class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('PyQt5 Image Viewer')
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height

        # 创建一个 QWidget 作为中心组件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建一个 QVBoxLayout 实例
        self.layout = QVBoxLayout()

        # 创建一个 QLabel 用于显示图片
        self.image_label = QLabel()

        # 使用 QPixmap 加载图片
        self.pixmap = QPixmap('狗头.jpg')  # 替换为你的图片路径
        self.image_label.setPixmap(self.pixmap)

        # 将 QLabel 添加到布局中
        self.layout.addWidget(self.image_label)

        # 设置中心组件的布局
        self.central_widget.setLayout(self.layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageWindow()
    window.show()
    sys.exit(app.exec_())