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


doc = Document("京北方-006财富工作台三期新尊享APP配合爱予二期项目-开发.docx")
for table in doc.tables:
    deal_doc = DealDocxTable(table)
