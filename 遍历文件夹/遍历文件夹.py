#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  遍历文件夹.py
:time  2024/5/27 9:42
:desc  
"""
import os


def search_dir(
        filepath: str,
        chart_name: str = None,
        suffix_name: str = None,
        dir_list=None
) -> list:
    """
    在路径中查询包含该次的文件夹
    :param filepath:
    :param chart_name:关键字
    :param suffix_name:后缀
    :param dir_list:
    :return:
    """
    if dir_list is None:
        dir_list = []
    if os.path.isdir(filepath):
        for filename in os.listdir(filepath):
            dir_path = os.path.join(filepath, filename)
            if filename:
                if os.path.isdir(dir_path) and chart_name in filename:
                    dir_list.append(dir_path)
            if suffix_name:
                if os.path.isdir(dir_path) and filename.endswith(suffix_name):
                    dir_list.append(dir_path)
            search_dir(dir_path, chart_name, dir_list)
        else:
            return dir_list
