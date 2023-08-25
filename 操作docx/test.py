#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  test.py
:time  2023/7/24 17:02
:desc  
"""
import pandas as pd
import numpy as np
from docx import Document
from 操作docx.operate_docx import DealDocxTable


doc = Document("基金交易类业务申请表.docx")
for table in doc.tables:
    deal_doc = DealDocxTable(table)
