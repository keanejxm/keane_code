#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025-11-15 18:54
# @Author  : keane
# @Site    : 
# @File    : thsauto_.py
# @Software: PyCharm
import win32gui
import win32con
import win32api
import time
from pywinauto import Desktop,Application
from ctypes import Structure, windll, c_uint, sizeof, byref

KEY_MAP = {
    'ENTER': win32con.VK_RETURN,
    'ESC': win32con.VK_ESCAPE,
    'F1': win32con.VK_F1,
    'F2': win32con.VK_F2,
    'F3': win32con.VK_F3,
    'F4': win32con.VK_F4,
    'F5': win32con.VK_F5,
    'F6': win32con.VK_F6,
    'F7': win32con.VK_F7,
    'F8': win32con.VK_F8,
    'F9': win32con.VK_F9,
    'F10': win32con.VK_F10,
    'F11': win32con.VK_F11,
    'F12': win32con.VK_F12,
    'CTRL': win32con.VK_CONTROL,
    'ALT': win32con.VK_MENU,
    'SHIFT': win32con.VK_SHIFT,
    'TAB': win32con.VK_TAB,
    'CAPSLOCK': win32con.VK_CAPITAL,
    'DEL': win32con.VK_DELETE,
    'INSERT': win32con.VK_INSERT,
    'HOME': win32con.VK_HOME,
    'END': win32con.VK_END,
    'PAGEUP': win32con.VK_PRIOR,
    'PAGEDOWN': win32con.VK_NEXT,
    'WIN': win32con.VK_LWIN,
    'UP': win32con.VK_UP,
    'DOWN': win32con.VK_DOWN,
    'LEFT': win32con.VK_LEFT,
    'RIGHT': win32con.VK_RIGHT,
    '+': win32con.VK_ADD,
    '-': win32con.VK_SUBTRACT,
    '*': win32con.VK_MULTIPLY,
    '/': win32con.VK_DIVIDE
}


class KEYBDINPUT(Structure):
    _fields_ = [
        ("wVk", c_uint),
        ("wScan", c_uint),
        ("dwFlags", c_uint),
        ("time", c_uint),
        ("dwExtraInfo", c_uint)
    ]


class INPUT(Structure):
    _fields_ = [
        ("type", c_uint),
        ("ki", KEYBDINPUT)
    ]


class WindowService:
    def __init__(self):
        pass

    # 获取窗口句柄
    def fetch_window_hwnd(self):
        window_list = list()

        def enum_windows_callback(hwnd, lparam):
            """窗口枚举的回调函数（顶层窗口）"""
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                window_class = win32gui.GetClassName(hwnd)
                control_info = {
                    "class": window_class,
                    "title": window_title,
                    "hwnd": hwnd,
                    "children": []
                }
                window_list.append(control_info)
                self.fetch_child_controls(hwnd, control_info["children"])
            return True

        win32gui.EnumWindows(enum_windows_callback, None)
        return window_list

    # 根据句柄获取子控件相关数据
    def fetch_child_controls(self, hwnd, children_list: list):
        def child_callback(child_hwnd, lparam):
            if win32gui.IsWindowVisible(child_hwnd):
                child_title = win32gui.GetWindowText(child_hwnd)
                child_class = win32gui.GetClassName(child_hwnd)
                control_id = win32gui.GetDlgCtrlID(child_hwnd)

                child_info = {
                    "class": child_class,
                    "title": child_title,
                    "controlId": control_id,
                    "hwnd": child_hwnd,
                    "children": []
                }
                children_list.append(child_info)
                self.fetch_child_controls(child_hwnd, child_info["children"])
            return True  # 继续枚举下一个子控件

        win32gui.EnumChildWindows(hwnd, child_callback, None)

    # 点击控件
    def click_control_by_handle(self, handle):
        if not win32gui.IsWindow(handle):
            raise ValueError("无效的窗口句柄")

        rect = win32gui.GetWindowRect(handle)
        x = rect[0] + (rect[2] - rect[0]) // 2
        y = rect[1] + (rect[3] - rect[1]) // 2

        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

    # 发送字符到编辑框
    def send_char_to_edit(self, handle, char_):
        if not win32gui.IsWindow(handle):
            raise ValueError("无效的窗口句柄")
        for char in char_:
            char_code = ord(char)
            win32gui.SendMessage(handle, win32con.WM_CHAR, char_code, 0)

    def _get_virtual_key_codes(self, key_sequence: list):
        """
        将按键序列转换为虚拟键码
        :param key_sequence: 按键序列
        :return: 虚拟键码列表
        """
        vk_codes = []
        for key in key_sequence:
            if len(key) == 1:
                vk_codes.append(ord(key.upper()))
            elif key in KEY_MAP:
                vk_codes.append(KEY_MAP[key])
            else:
                raise ValueError(f"无效的按键: {key}")
        return vk_codes

    def _press_modifier_keys(self, vk_codes: list, delay: float) -> None:
        """
        按下所有修饰键
        :param vk_codes: 虚拟键码列表
        :param delay: 按键之间的延迟时间
        """
        for vk in vk_codes[:-1]:
            win32api.keybd_event(vk, 0, 0, 0)
            time.sleep(delay)

    def send_key_combination(self, keys: str, delay: float = 0.1):
        """
        发送组合键（支持格式：'CTRL+SHIFT+A'）
        :param keys: 组合键字符串（用+连接）
        :param delay: 按键之间的延迟时间（秒）
        """
        key_sequence = [k.strip().upper() for k in keys.split('+')]
        key_sequence = [k.replace('\\PLUS', '+') for k in key_sequence]

        vk_codes = self._get_virtual_key_codes(key_sequence)

        self._press_modifier_keys(vk_codes, delay)
        win32api.keybd_event(vk_codes[-1], 0, 0, 0)
        time.sleep(delay)
        win32api.keybd_event(vk_codes[-1], 0, win32con.KEYEVENTF_KEYUP, 0)
        self._release_modifier_keys(vk_codes, delay)

    def _release_modifier_keys(self, vk_codes: list, delay: float) -> None:
        """
        释放所有修饰键
        :param vk_codes: 虚拟键码列表
        :param delay: 按键之间的延迟时间
        """
        for vk in reversed(vk_codes[:-1]):
            win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(delay)

    def _process_single_key(self, key: str):
        """
        处理单个按键
        :param key: 单个按键字符串
        """
        if key == '':  # 处理空字符停顿
            time.sleep(0.5)
            return

        if len(key) == 1:
            vk = ord(key.upper())
        elif key in KEY_MAP:
            vk = KEY_MAP[key]
        else:
            for char in key:
                vk = ord(char.upper())
                win32api.keybd_event(vk, 0, 0, 0)
                win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
                time.sleep(0.05)
            return

        win32api.keybd_event(vk, 0, 0, 0)
        win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.05)

    def send_key(self, keys):
        """
        发送组合键（支持格式：'CTRL C' 或单个键，花括号内为组合键）
        :param keys: 组合键字符串（用空格连接）或单个键
        """
        key_sequence = [k.strip().upper() for k in keys.split(' ')]
        for key in key_sequence:
            if key.startswith('{') and key.endswith('}'):
                combination = key[1:-1]
                self.send_key_combination(combination)
            else:
                self._process_single_key(key)

    def show_window(self, hwnd):
        if not win32gui.IsWindow(hwnd):
            raise ValueError('无效的窗口句柄')
        # 检查窗口是否最小化
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        else:
            win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        win32gui.SetForegroundWindow(hwnd)

    # 通过pywinauto获取窗口参数
    def get_target_window(self, window_params, retries=3, delay=0.5):
        for i in range(retries):
            try:
                # 使用pywinauto
                dialogs = Desktop(backend='win32').windows(**window_params)
                if dialogs:
                    return dialogs[0]
                time.sleep(delay)
            except Exception as e:
                if i == retries - 1:
                    raise Exception(f"查找窗口失败: {str(e)}")
                time.sleep(delay)
        return None

    # 通过id获取句柄
    def find_element_in_window(self, window):
        element_list = list()
        descendants = window.descendants()
        for element in descendants:
            control_id = element.control_id()
            hwnd = element.handle
            if isinstance(control_id, (int, str)):
                element_list.append(dict(controlId=element.control_id(), controlText=element.window_text(), hwnd=hwnd))
            else:
                element_list.append(dict(controlId=element.control_id(), controlText=element.window_text(), hwnd=hwnd))
        return element_list

    def start_app(self, app_path):
        try:
            # win32api.ShellExecute(0, 'open', app_path, '', '', 1)
            app = Application(backend='uia').start(app_path)
            # 等待窗口可见
            time.sleep(3)
            print(app.process)
            app = Application().connect()
        except Exception as e:
            print(f"启动应用失败: {str(e)}")