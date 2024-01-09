#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  进程.py
:time  2023/12/29 10:18
:desc  
"""
import os
import time
from multiprocessing import Pool
from multiprocessing import Process

def f(x):
    time.sleep(2)
    return x*x

def f1(name):
    info("function f1")
    print("hello",name)

def info(title):
    print(title)
    print("module name",__name__)
    print("parent process",os.getppid())
    print("process id",os.getpid())

if __name__ == '__main__':
    # with Pool(5) as p:
    #     print(p.map(f,[1,2,3]))
            # print(p.map(f1,"1"))
    info("main line")
    p = Process(target=f1,args=("Bob",))
    p.start()
    p.join()