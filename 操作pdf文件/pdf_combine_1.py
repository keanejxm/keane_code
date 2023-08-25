#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  pdf_combine_1.py
:time  2023/8/22 10:59
:desc  
"""
import fitz

# 打开PDF文档
doc1 = fitz.open("基金交易类业务申请表3569-1电子章，手动录入.pdf")
doc2 = fitz.open("基金交易类业务申请表6705-1电子章，手动录入.pdf")
# 将doc2文档插入到doc1后面
doc1.insert_pdf(doc2)
# 将插入后的文档保存为“merge.pdf”
doc1.save("merge.pdf")