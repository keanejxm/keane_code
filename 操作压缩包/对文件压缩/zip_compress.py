#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  zip_compress.py
:time  2023/5/19 9:31
:desc  对文件进行压缩
"""
import os
import zipfile

def zip_compress(dirpath):
    """
    对文件压缩
    :return:
    """
    print(f"原始文件夹路径：{dirpath}")
    output_name = f"{dirpath}.zip"
    parent_name = os.path.dirname(dirpath)
    print(f"压缩文件夹目录：{parent_name}")
    zip = zipfile.ZipFile(output_name,"w",zipfile.ZIP_DEFLATED)
    for root,dirs,files in os.walk(dirpath):
        for file in files:
            if str(file).startswith("~$"):
                continue
            filepath = os.path.join(root,file)
            print(f"压缩文件路径：{filepath}")
            writepath = os.path.relpath(filepath,parent_name)
            zip.write(filepath,writepath)
    zip.close()

dir_path = r"E:\keane_python\github\keane_code\操作压缩包\对文件压缩\交易数据合并"
zip_compress(dir_path)