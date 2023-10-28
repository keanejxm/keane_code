#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  async_test.py
:time  2023/9/18 17:01
:desc  
"""
import asyncio


async def asy_1():
    print("协程1")


async def asy_2():
    print("协程2")


# asyncio.run(asy_2())
tasks = [asy_1(),asy_2()]
# 创建时间循环
loop = asyncio.get_event_loop()
# 添加任务
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
# asyncio.run(asyncio.wait(tasks))