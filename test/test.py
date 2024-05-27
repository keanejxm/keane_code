#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  test.py
:time  2023/8/10 15:46
:desc  
"""
# 数字转换
num_map = {
    "0": "零",
    "1": "壹",
    "2": "贰",
    "3": "叁",
    "4": "肆",
    "5": "伍",
    "6": "陆",
    "7": "柒",
    "8": "捌",
    "9": "玖",
}
length_map = {
    "1": "元",
    "2": "拾",
    "3": "佰",
    "4": "仟",
    "5": "万",
    "6": "拾万",
    "7": "佰万",
    "8": "仟万",
    "9": "亿",
    "10": "拾亿",
    "11": "佰亿",
    "12": "仟亿",
}
a = dict()
for key, value in length_map.items():
    a[value] = ""
print(a)


# def translate_number(num, result:str):
#     if not isinstance(num, list):
#         num = list(str(num))
#     num_length = len(num)
#     num_head = num[0]
#     if num_head == "0":
#         if result[-1] != "零":
#             result += "零"
#     else:
#         result += (num_map[num_head] + length_map[str(num_length)])
#     num.remove(num_head)
#     if num:
#         result = translate_number(num, result)
#     if result.endswith("零"):
#         result = result.rstrip("零") + "元整"
#     return result


def translate_num(num: str, result):
    if not isinstance(num, list):
        num = list(str(num))
    num_length = len(num)
    num_head = num[0]
    result[length_map[str(num_length)]] = num_map[num_head]
    if num_head == "0":
        result[length_map[str(num_length)]] = "/"
    num.remove(num_head)
    if num:
        result = translate_num(num, result)


# a = round(23.453, 2)
# b = 345
# print(a + b)
#
# from decimal import Decimal
#
# a = Decimal(5.45) / Decimal(5)
# b = float(a)
# c = round(a, 4)
# print(a)

import win32com.client
import datetime

def create_task_schedule(task_name, program_path, start_time, daily=True, trigger_type='DAILY'):

    # 创建任务执行器对象
    task_scheduler = win32com.client.Dispatch('Schedule.Service')
    task_scheduler.Connect()

    # 创建任务对象
    task = task_scheduler.CreateTask(0)

    # 定义任务的设置
    settings = task.Settings
    settings.Enabled = True
    settings.AllowDemandStart = True
    settings.StartWhenAvailable = True
    settings.Hidden = False

    # 定义触发器 - 在指定的时间运行
    trigger = task.Triggers.Create(win32com.client.constants.TRIGGER_TYPE_ONESTIME)
    trigger.Repetition.Interval = 'PT0S'
    trigger.ExecutionTime = datetime.datetime(2023, 4, 15, 12, 0, 0)  # 设置执行时间

    # 定义操作 - 执行某个程序
    action = task.Actions.Create(win32com.client.constants.TASK_ACTION_EXEC)
    action.Path = 'python.exe'  # 指定Python解释器路径
    action.Arguments = r'E:\keane_python\github\keane_code\test\test1.py'  # 指定要执行的Python脚本

    # 保存任务
    task_folder = task_scheduler.GetFolder('\\')
    task_folder.RegisterTaskDefinition('My Python Task', task, win32com.client.constants.TASK_CREATE_OR_UPDATE, '', '',
                                       0)


# 使用示例
if __name__ == '__main__':
    task_name = 'My Python Script Task'
    program_path = r'E:\keane_python\github\keane_code\test\test1.py'
    start_time = '2024-05-09 14:47:00'  # 日期时间格式
    create_task_schedule(task_name, program_path, start_time)