#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  线程.py
:time  2023/12/28 17:43
:desc  
"""
import time
import threading

"""
global interpreter lock -- 全局解释器锁
CPython 解释器所采用的一种机制，它确保同一时刻只有一个线程在执行 Python bytecode。
此机制通过设置对象模型（包括 dict 等重要内置类型）针对并发访问的隐式安全简化了 CPython 实现。
给整个解释器加锁使得解释器多线程运行更方便，其代价则是牺牲了在多处理器上的并行性。
不过，某些标准库或第三方库的扩展模块被设计为在执行计算密集型任务如压缩或哈希时释放 GIL。 此外，在执行 I/O 操作时也总是会释放 GIL。
创建一个（以更精细粒度来锁定共享数据的）“自由线程”解释器的努力从未获得成功，因为这会牺牲在普通单处理器情况下的性能。
据信克服这种性能问题的措施将导致实现变得更复杂，从而更难以维护。"""
# 同时运行多个 I/O 密集型任务，



def task(num):
    time.sleep(4)
    print("Task %d is running." % num)


if __name__ == '__main__':
    for i in range(5):
        t = threading.Thread(target=task, args=(i,))
        t.start()
    print(threading.active_count())
    print(threading.current_thread())
