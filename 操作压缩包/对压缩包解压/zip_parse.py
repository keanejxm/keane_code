#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  zip_parse.py
:time  2022/10/10 16:49
:desc  
"""
import io
import zipfile
import rarfile
import os


def unzip():
    file_path = f"{os.path.dirname(__file__)}/确认书.zip"
    dst_dir = f"{os.path.dirname(__file__)}/"
    is_zip = zipfile.is_zipfile(file_path)
    zip_content = b""
    with open(file_path,"rb") as r:
        for content in r.readlines():
            zip_content+=content
    zip_content = io.BytesIO(zip_content)
    if is_zip:
        zip_info = zipfile.ZipFile(zip_content, "r")
        for file_name,file_info in zip_info.NameToInfo.items():
        # for file_name in zip_info.namelist():
        #     zip_info.extract(file_name)
            aa = zip_info.open(file_info)
            bb = aa.read()
            print(len(bb))
            with open("aaaa.pdf","wb") as w:
                w.write(bb)
            # print(file_name.encode('cp437').decode('gbk'))
            # res = zip_info.extract(file_name,dst_dir)
            # print(res)
    else:
        print("不是压缩文件")

def unrar():
    with open("1111.rar","rb") as r:
        content  = b"".join(r.readlines())
    rar = rarfile.RarFile(io.BytesIO(content))
    rar.extractall("E:\keane_python\github\keane_code\操作压缩包\对压缩包解压")
    print(rar)

unrar()
