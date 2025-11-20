#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025-11-15 8:46
# @Author  : keane
# @Site    : 
# @File    : test.py
# @Software: PyCharm

import win32gui
title = "网上股票交易系统"
import win32gui
import win32process
import psutil
import win32con
import json
# def enum_windows_callback(hwnd, lParam):
#     title = win32gui.GetWindowText(hwnd)
#     class_name = win32gui.GetClassName(hwnd)
#     print(f"窗口标题: {title}, 窗口类名: {class_name}")
#     return True  # 继续枚举
#
# win32gui.EnumWindows(enum_windows_callback, None)
# 激活指定应用程序窗口
def activate_window( app_path):
    """
    激活指定应用程序窗口
    :param app_path: 应用程序完整路径
    :return: 成功返回窗口句柄，失败抛出异常
    """
    hwnd_found = None

    def callback(hwnd, extra):
        nonlocal hwnd_found
        if win32gui.IsWindowVisible(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            try:
                proc = psutil.Process(pid)
                print(proc.exe().lower())
                if proc.exe().lower() == app_path.lower():
                    hwnd_found = hwnd
                    if win32gui.IsIconic(hwnd):
                        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    if not win32gui.IsWindow(hwnd):
                        raise Exception("无效的窗口句柄")
                    if not win32gui.IsWindowVisible(hwnd):
                        raise Exception("窗口不可见或已关闭")
                    try:
                        win32gui.SetForegroundWindow(hwnd)
                    except Exception as e:
                        print(
                            f"win32gui.SetForegroundWindow 失败，尝试使用 pywinauto.set_focus()，句柄：{hwnd}，错误：{str(e)}")
                        try:
                            from pywinauto import Application
                            app = Application(backend='uia').connect(handle=hwnd)
                            app.window(handle=hwnd).set_focus()
                        except Exception as e2:
                            raise Exception(f"设置前台窗口失败，句柄：{hwnd}，错误1：{str(e)}，错误2：{str(e2)}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return True

    win32gui.EnumWindows(callback, None)

    if hwnd_found:
        return hwnd_found
    raise Exception("未找到匹配窗口")
# activate_window(r"F:\同花顺远航版\transaction\xiadan.exe")
from pywinauto import Desktop
from pywinauto import Desktop

# 使用uia后端获取桌面对象
# desktop = Desktop(backend='win32')
#
# # 获取所有顶级窗口
# windows = desktop.windows()
#
# for window in windows:
#     try:
#         print(f"窗口标题: {window.window_text()}")
#         print(f"窗口类名: {window.class_name()}")
#     except Exception as e:
#         print(f"获取窗口信息时出错: {e}")
window_params = {'title': '网上股票交易系统5.0'}
dialogs = Desktop(backend='win32').windows(**window_params)
dialog = dialogs[0]
print(dialog.window_text())
