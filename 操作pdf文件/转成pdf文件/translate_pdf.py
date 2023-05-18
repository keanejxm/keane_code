#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  translate_pdf.py
:time  2023/5/18 15:27
:desc  将文件转为pdf文件
"""
import os
from win32com.client import Dispatch, constants, gencache, DispatchEx


class PDFConverter:
    def __init__(self, pathname):
        self._handle_postfix = ["doc", "docx", "ppt", "pptx", "xls", "xlsx"]
        self._filename_list = list()
        self._export_folder = os.path.join(os.path.abspath("."), "pdfconver")
        if not self._export_folder:
            os.mkdir(self._export_folder)
        self._enumerate_filename(pathname)

    def _enumerate_filename(self, pathname):
        """
        读取所有文件名
        :param pathname:
        :return:
        """
        full_pathname = os.path.abspath(pathname)
        if os.path.isfile(full_pathname):
            if self._is_legal_postfix(full_pathname):
                self._filename_list.append(full_pathname)
            else:
                raise TypeError(f"文件{pathname}后缀名不合法！仅支持如下文件类型{self._handle_postfix}")
        elif os.path.isdir(full_pathname):
            for relpath, _, files in os.walk(full_pathname):
                for name in files:
                    filename = os.path.join(full_pathname, relpath, name)
                    if self._is_legal_postfix(filename):
                        self._filename_list.append(os.path.join(filename))
        else:
            raise TypeError(f"文件/文件夹{pathname}不存在或不合法")

    def _is_legal_postfix(self, filename):
        return filename.split(".")[-1].lower() in self._handle_postfix and not os.path.basename(filename).startswith(
            "~")

    def run_conver(self):
        """
        进行批量处理，根据后缀名调用函数执行转换
        :return:
        """
        for filename in self._filename_list:
            postfix = filename.split(".")[-1].lower()
            fullCall = getattr(self, postfix)
            print(f"文件：{filename}开始转换")
            fullCall(filename)
        print("转换完成")

    def xls(self, filename):
        """
        xls和xlsx文件转换
        :param filename:
        :return:
        """
        name = os.path.basename(filename).split(".")[0] + ".pdf"
        exportfile = os.path.join(self._export_folder, name)
        xlApp = DispatchEx("Excel.Application")
        xlApp.Visible = False
        xlApp.DisplayAlerts = 0
        books = xlApp.Workbooks.Open(filename, False)
        books.ExportAsFixedFormat(0, exportfile)
        books.Close()
        print(f"保存pdf文件：", exportfile)
        xlApp.Quit()
def xls(filename):
    """
    xls和xlsx文件转换
    :param filename:
    :return:
    """
    name = os.path.basename(filename).split(".")[0] + ".pdf"
    exportfile = f"E:\keane_python\github\keane_code\操作pdf文件\转成pdf文件\{name}"
    xlApp = DispatchEx("Excel.Application")
    xlApp.Visible = False
    xlApp.DisplayAlerts = 0
    books = xlApp.Workbooks.Open(filename, False)
    all_sheets = [sheet.Name for sheet in books.Sheets]
    ws_source = books.Worksheets(all_sheets[0])
    ws_source.PageSetup.Orientation = 2
    ws_source.PageSetup.Zoom = False
    books.ExportAsFixedFormat(0, exportfile)
    books.Close()
    print(f"保存pdf文件：", exportfile)
    xlApp.Quit()

filename = r"E:\keane_python\github\keane_code\操作pdf文件\转成pdf文件\16214-建信信托-货币通宝现金管理集合资金信托计划-赎回明细表.xls"
xls(filename)
from win32com import client as wc

try:
    excel = wc.DispatchEx('Excel.Application')
except:
    try:
        excel = wc.DispatchEx('ket.Application')
    except:
        excel = wc.DispatchEx('et.Application')
newpdf = excel.Workbooks.Open(r'C:\Users\Administrator\Desktop\tt\abc.xls')
excel.DisplayAlerts = 0
# 获取第一个sheet
all_sheets = [sheet.Name for sheet in newpdf.Sheets]
ws_source = newpdf.Worksheets(all_sheets[0])
# 设置页面设置
ws_source.PageSetup.LeftHeader = ""
ws_source.PageSetup.CenterHeader = ""
ws_source.PageSetup.RightHeader = ""
ws_source.PageSetup.LeftFooter = ""
ws_source.PageSetup.CenterFooter = ""
ws_source.PageSetup.RightFooter = ""
# ws_source.PageSetup.FitToPagesTall = 0
ws_source.PageSetup.FirstPageNumber = True
ws_source.PageSetup.LeftMargin = 0
ws_source.PageSetup.RightMargin = 0
ws_source.PageSetup.TopMargin = 0
ws_source.PageSetup.BottomMargin = 0
ws_source.PageSetup.HeaderMargin = 0
ws_source.PageSetup.FooterMargin = 0
# ws_source.PageSetup.PaperSize = 1
ws_source.PageSetup.Orientation = 2  # 横向转换pdf
ws_source.PageSetup.FitToPagesWide = 1  # 所有列压缩在一页纸
ws_source.PageSetup.FitToPagesTall = False
ws_source.PageSetup.Zoom = False  # 所有列压缩在一页纸
ws_source.PageSetup.CenterVertically = True
ws_source.PageSetup.CenterHorizontally = True
ws_source.PageSetup.Draft = False
ws_source.Select()
# 行列自动调整
# ws_source.Columns.AutoFit()
# ws_source.Rows.AutoFit()
# 设置Excel的边框
rows = ws_source.UsedRange.Rows.Count
cols = ws_source.UsedRange.Columns.Count
ws_source.Range(ws_source.Cells(1, 1), ws_source.Cells(rows, cols)).Borders.LineStyle = 1
ws_source.Range(ws_source.Cells(1, 1), ws_source.Cells(rows, cols)).Borders.TintAndShade = 0
ws_source.Range(ws_source.Cells(1, 1), ws_source.Cells(rows, cols)).Borders.Weight = 1
# 转换为PDF文件
newpdf.ExportAsFixedFormat(0, r'C:\Users\Administrator\Desktop\tt\abc.pdf')
newpdf.Close()
excel.Quit()
