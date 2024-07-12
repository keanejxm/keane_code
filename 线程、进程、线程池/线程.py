#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  线程.py
:time  2023/12/28 17:43
:desc  
"""
import concurrent.futures
import queue
import time
import threading

# from multiprocessing import cpu_count


"""
global interpreter lock -- 全局解释器锁
CPython 解释器所采用的一种机制，它确保同一时刻只有一个线程在执行 Python bytecode。
此机制通过设置对象模型（包括 dict 等重要内置类型）针对并发访问的隐式安全简化了 CPython 实现。
给整个解释器加锁使得解释器多线程运行更方便，其代价则是牺牲了在多处理器上的并行性。
不过，某些标准库或第三方库的扩展模块被设计为在执行计算密集型任务如压缩或哈希时释放 GIL。 此外，在执行 I/O 操作时也总是会释放 GIL。
创建一个（以更精细粒度来锁定共享数据的）“自由线程”解释器的努力从未获得成功，因为这会牺牲在普通单处理器情况下的性能。
据信克服这种性能问题的措施将导致实现变得更复杂，从而更难以维护。"""
# 同时运行多个 I/O 密集型任务，

"""
threading.settrace(func)
threading.settrace_all_threads(func)
threading.gettrace()
threading.setprofile(func)
threading.setprofile_all_threads
threading.getprofile()
threading.stack_size([size])
threading.TIMEOUT_MAX
threading.local
"""


class ThreadPoolPractice:
    def task(self, num):
        time.sleep(4)
        print("Task %d is running." % num)
        print(threading.current_thread())
        # 线程标识符
        print(threading.get_ident())
        # 线程的id
        print(threading.get_native_id())
        # 返回主线程Thread对象
        print(threading.main_thread())

    def run_thread(self):
        # 返回当前存活的的Thread对象列表
        print(threading.enumerate())
        print(threading.active_count())
        for i in range(5):
            t = threading.Thread(target=self.task, args=(i,))
            t.start()
        # 返回当前存活的threading.Thread的数量
        print(threading.active_count())
        print(threading.current_thread())

    # 爬虫： 下载数据----解析数据
    def thread_pool(self, func, generator, generator_kwargs=None):
        class BoundedThreadPoolExecutor(concurrent.futures.ThreadPoolExecutor):
            def __init__(self, max_worker=None, thread_name_prefix=""):
                super().__init__(max_worker, thread_name_prefix)
                self._work_queue = queue.Queue(self._max_workers * 2)

        with BoundedThreadPoolExecutor(1) as pool:
            future_tasks = list()
            for i, kwargs in enumerate(generator(**generator_kwargs)):
                future = pool.submit(func, **kwargs)
                future.add_done_callback(fn=self.done_callback)
                future_tasks.append(future)
            concurrent.futures.wait(future_tasks)

    def done_callback(self,future):
        pass

    def test(self, aa, bb):
        print(aa)
        print(bb)

    def run_thread_pool(self):
        def general_task():
            for i in range(4):
                yield dict(
                    aa=i,
                    bb="a" * i
                )

        self.thread_pool(
            func=self.test,
            generator=general_task,
            generator_kwargs=dict()
        )


if __name__ == '__main__':
    obj = ThreadPoolPractice()

    obj.run_thread_pool()
