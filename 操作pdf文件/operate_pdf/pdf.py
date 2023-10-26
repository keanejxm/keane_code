#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  pdf.py
:time  2023/8/25 17:47
:desc  
"""


# 读pdf
class PdfReader:
    def __init__(self, stream):
        pass
        self.read(stream)

    def read(self, stream):
        b = stream.seek(-1, 2)
        line = ""
        while not line:
            line = self.readNextEenLine(stream)


if __name__ == '__main__':
    pdf_content = open("基金交易类业务申请表3569-1电子章，手动录入.pdf", "rb")
    obj = PdfReader(pdf_content)
