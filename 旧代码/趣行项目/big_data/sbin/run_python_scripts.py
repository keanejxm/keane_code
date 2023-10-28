# -*- coding:utf-8 -*-
"""
脚本执行器。
# author: Trico
# date: 2021/1/19
# update: 2021/1/19
"""

import os
import sys


def kafka_listener(argv):
    """
    kafka监听器。
    :return:
    """

    # noinspection PyBroadException
    try:
        # 获取监听器数量。
        listener_num = int(argv[3])
    except Exception:
        listener_num = 1

    # 选择执行哪一种监听器。
    if argv[2] == "a1":
        from scripts.kafka_listener.a1_flow_compute import run
        run(listener_num=listener_num)
    elif argv[2] == "a2":
        from scripts.kafka_listener.a2_save_to_es import run
        run(listener_num=listener_num)
    elif argv[2] == "b1":
        from scripts.kafka_listener.b1_save_to_es import run
        run(listener_num=listener_num)
    elif argv[2] == "c1":
        from scripts.kafka_listener.c1_save_to_es import run
        run(listener_num=listener_num)
    else:
        raise ValueError(f"参数错误，{argv}")


def spider_schedulers(argv):
    """
    kafka监听器。
    :return:
    """

    # 获取监听器数量。
    spider_type = argv[2]
    print(spider_type)


def print_usage(argv):
    """
    打印执行方式。
    :return:
    """

    print(f"用法：\n\t{argv[0]} kafka_listener ...", flush=True)


def run(python_path="lib"):
    """
    入口。
    :return:
    """

    argv = sys.argv
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lib_path = f"{project_path}/{python_path}"
    sys.path.insert(0, lib_path)
    if len(argv) >= 2:
        if argv[1] == "kafka_listener":
            if len(argv) >= 3:
                kafka_listener(argv)
            else:
                print_usage(argv)
        elif argv[1] == "scheduler":
            spider_schedulers(argv)
        else:
            print_usage(argv)
    else:
        print_usage(argv)


if __name__ == "__main__":
    run()
