#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
测试mysql。
# author: Trico
# date: 2021.1.12
# update: 2021.1.12
"""

import pymysql
from api.config import mysql_config


def test_mysql():
    conn = pymysql.Connect(**mysql_config)
    conn.close()


if __name__ == "__main__":
    test_mysql()
