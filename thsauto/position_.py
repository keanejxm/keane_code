#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025-11-20 9:40
# @Author  : keane
# @Site    : 存放同花顺相关操作
# @File    : position_.py
# @Software: PyCharm
import time

from src.thsauto_ import WindowService


class PositionThs:
    def __init__(self):
        self.windows_service = WindowService()
        self.win_windows = self._init_windows()

    def _init_windows(self):
        """
        初始化同花顺客户端展示窗口
        :return:
        """
        win_windows = self.windows_service.fetch_window_hwnd()
        # 获取窗口句柄
        for win_window in win_windows:
            window_title = win_window["title"]
            if window_title != "网上股票交易系统5.0":
                continue
            window_hwnd = win_window["hwnd"]
            # 获取窗口
            self.windows_service.show_window(window_hwnd)
            # 获取控件
            window_params = dict(title="网上股票交易系统5.0")
            pywinauto_window = self.windows_service.get_target_window(window_params)
            # 获取控件
            children_list = self.windows_service.find_element_in_window(pywinauto_window)
            win_window["pywinautoChildren"] = children_list
            return win_window
        else:
            raise Exception("未找到同花顺客户端窗口")

    # 获取资金信息
    def get_balance(self):
        # 定义需要获取的字段及其对应的control_id
        balance_fields = {
            '资金余额': 1012,
            '冻结金额': 1013,
            '可用金额': 1016,
            '可取金额': 1017,
            '股票市值': 1014,
            '总资产': 1015,
            '持仓盈亏': 1027,
            '当日盈亏': 1026,
            '当日盈亏比': 1029
        }
        result = dict()
        # 遍历获取数据
        for field, control_id in balance_fields.items():
            element = next(e for e in self.win_windows["pywinautoChildren"] if e["controlId"] == control_id)
            if element:
                result[field] = element["controlText"][0]
            else:
                result[field] = None
        return result

    # 下单
    def send_order(self, stock_code=None, buy_price=None, buy_volume=None):
        # 证券代码
        stock_code = "600200"
        # 买入价格
        buy_price = "1.01"
        # 买入数量
        buy_volume = "9"
        # 进入下单页面
        input_data = {
            "sotckCode": stock_code,
            "buyPrice": buy_price,
            "buyVolume": buy_volume,
        }
        self.windows_service.send_key("F1")
        order_data = {
            "sotckCode": 1032,
            "buyPrice": 1033,
            "buyVolume": 1034,
        }
        # 获取对应句柄
        for filed_name, control_id in order_data.items():
            element = next(e for e in self.win_windows["children"] if e["controlId"] == control_id)
            if element:
                # 输入数据
                self.windows_service.send_char_to_edit(element["hwnd"], input_data[filed_name])
            else:
                raise ValueError(f"未找到{filed_name}对应的控件")

        # 点击下单按钮
        print(self.win_windows)
        button_hwnd = [e for e in self.win_windows["children"] if e["controlId"] == 1006][0]
        self.windows_service.click_control_by_handle(button_hwnd["hwnd"])

        # 获取下单确认窗口
        def confirm_window_params(title=None) -> dict:
            new_windows: list[dict] = self.windows_service.fetch_window_hwnd()
            if not new_windows:
                raise ValueError("未找到确认确认窗口")

            confirm_button = next(
                (
                    child
                    for new_window in new_windows
                    for child in new_window["children"]
                    if child.get("title") == title
            ),
                None
            )
            if not confirm_button:
                raise ValueError(f"未找到包含'{title}'按钮的窗口")

            return confirm_button

        # 点击是
        time.sleep(2)
        confirm_window_data = confirm_window_params(title="是(&Y)")
        self.windows_service.click_control_by_handle(confirm_window_data["hwnd"])
        # 继续委托
        time.sleep(2)
        continue_enturst_data1=confirm_window_params(title="继续委托")
        self.windows_service.click_control_by_handle(continue_enturst_data1["hwnd"])
        # 继续委托
        time.sleep(2)
        continue_enturst_data2=confirm_window_params(title="继续委托")
        self.windows_service.click_control_by_handle(continue_enturst_data2["hwnd"])
        # 获取下单结果
        # result = self.windows_service.get_control_text_by_handle(1007)
        # return result


if __name__ == '__main__':
    obj = PositionThs()
    print(obj.get_balance())

