# -*- coding:utf-8 -*-
"""

# author: albert
# date: 2020/12/24
# update: 2020/12/24
"""


def compare_simhash(sim1, sim2):
    # 转为二进制结构
    t1 = '0b' + sim1
    t2 = '0b' + sim2
    n = int(t1, 2) ^ int(t2, 2)
    # 相当于对每一位进行异或操作
    i = 0
    while n:
        n &= (n - 1)
        i += 1
    return i

