#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  oprate_pdf.py
:time  2023/8/10 10:49
:desc  对pdf的操作，pdfrw
"""
import pdfrw
from pdfrw.objects.pdfstring import PdfString
import os
import PyPDF2
from win32com.client import Dispatch, constants, gencache, DispatchEx

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_TU_KEY = "/TU"
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'


class PDFOperate:
    def __init__(self):
        pass

    # 获取表单域的键值对
    @staticmethod
    def fetch_form_filed(pdf_path):
        """"""
        template_pdf = pdfrw.PdfReader(pdf_path)
        pdf_pages = len(template_pdf.pages)
        template_pdf.Root.AcroForm.update(pdfrw.PdfDict(
            NeedAppearances=pdfrw.PdfObject('true')))
        for pagenum in range(pdf_pages):
            annotations = template_pdf.pages[pagenum][ANNOT_KEY]
            if annotations is None:
                continue
            for annotation in annotations:
                if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                    if annotation[ANNOT_FIELD_KEY]:
                        key = annotation[ANNOT_FIELD_KEY][1:-1]
                        key_tu = annotation[ANNOT_TU_KEY].to_unicode() if annotation[ANNOT_TU_KEY] and isinstance(
                            annotation[ANNOT_TU_KEY], PdfString) else None
                        value = annotation[ANNOT_VAL_KEY].to_unicode() if annotation[ANNOT_VAL_KEY] and isinstance(
                            annotation[ANNOT_VAL_KEY], PdfString) else None
                        print(dict(key=key, keyTu=key_tu, value=value))

    # 添加表单域数据
    @staticmethod
    def append_form_key(input_pdf_path, output_pdf_path, data_dict):
        """

        :param input_pdf_path: 文件的路径
        :param output_pdf_path: 输出的路径
        :param data_dict:[fill_6:""] 需要添加的数据，键值对
        :return:
        """
        template_pdf = pdfrw.PdfReader(input_pdf_path)
        pdf_pages = len(template_pdf.pages)
        template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        for pagenum in range(pdf_pages):
            aa = template_pdf.pages[pagenum]
            annotations = template_pdf.pages[pagenum][ANNOT_KEY]
            if not annotations:
                continue
            for annotation in annotations:
                if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                    if annotation[ANNOT_FIELD_KEY]:
                        key = annotation[ANNOT_FIELD_KEY][1:-1]
                        if key in data_dict.keys():
                            annotation.update(pdfrw.PdfDict(V=f"{data_dict[key]}"))
            pdfrw.PdfWriter().write(output_pdf_path, template_pdf)

    @staticmethod
    def append_form_tu(input_pdf_path, output_pdf_path, data_dict):
        """

        :param input_pdf_path: 文件的路径
        :param output_pdf_path: 输出的路径
        :param data_dict:[fill_6:""] 需要添加的数据，键值对
        :return:
        """
        template_pdf = pdfrw.PdfReader(input_pdf_path)
        pdf_pages = len(template_pdf.pages)
        template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        for pagenum in range(pdf_pages):
            annotations = template_pdf.pages[pagenum][ANNOT_KEY]
            if not annotations:
                continue
            for annotation in annotations:
                if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                    if annotation[ANNOT_FIELD_KEY]:
                        key = annotation[ANNOT_FIELD_KEY][1:-1]
                        tu_key = annotation[ANNOT_TU_KEY]
                        if tu_key and isinstance(tu_key, PdfString):
                            tu_key = tu_key.to_unicode()
                            if tu_key in data_dict.keys():
                                annotation.update(pdfrw.PdfDict(V=f"{data_dict[tu_key]}"))
            pdfrw.PdfWriter().write(output_pdf_path, template_pdf)

    @staticmethod
    def append_form_value(input_pdf_path, output_pdf_path, data_dict):
        """

        :param input_pdf_path: 文件的路径
        :param output_pdf_path: 输出的路径
        :param data_dict:[fill_6:""] 需要添加的数据，键值对
        :return:
        """
        template_pdf = pdfrw.PdfReader(input_pdf_path)
        pdf_pages = len(template_pdf.pages)
        template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        for pagenum in range(pdf_pages):
            annotations = template_pdf.pages[pagenum][ANNOT_KEY]
            if not annotations:
                continue
            for annotation in annotations:
                if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                    if annotation[ANNOT_FIELD_KEY]:
                        key = annotation[ANNOT_FIELD_KEY][1:-1]
                        value = annotation[ANNOT_VAL_KEY]
                        if value and isinstance(value, PdfString):
                            value = value.to_unicode()
                            if value in data_dict.keys():
                                annotation.update(pdfrw.PdfDict(V=f"{data_dict[value]}"))
                        if key in data_dict.keys():
                            annotation.update(pdfrw.PdfDict(V=f"{data_dict[key]}"))
            pdfrw.PdfWriter().write(output_pdf_path, template_pdf)

    # 合并pdf
    @staticmethod
    def combine_pdf(outpath, pdf_files: list):
        output = pdfrw.PdfWriter()
        num = 0
        output_acroform = None
        for pdf in pdf_files:
            input = pdfrw.PdfReader(pdf, verbose=False)
            output.addpages(input.pages)
            if pdfrw.PdfName['AcroForm'] in input[pdfrw.PdfName['Root']].keys():  # Not all PDFs have an AcroForm node
                source_acroform = input[pdfrw.PdfName['Root']][pdfrw.PdfName['AcroForm']]
                if pdfrw.PdfName['Fields'] in source_acroform:
                    output_formfields = source_acroform[pdfrw.PdfName['Fields']]
                else:
                    output_formfields = []
                num2 = 0
                for form_field in output_formfields:
                    key = pdfrw.PdfName['T']
                    old_name = form_field[key].replace('(', '').replace(')',
                                                                        '')  # Field names are in the "(name)" format
                    form_field[key] = 'FILE_{n}_FIELD_{m}_{on}'.format(n=num, m=num2, on=old_name)
                    num2 += 1
                if output_acroform == None:
                    # copy the first AcroForm node
                    output_acroform = source_acroform
                else:
                    for key in source_acroform.keys():
                        # Add new AcroForms keys if output_acroform already existing
                        if key not in output_acroform:
                            output_acroform[key] = source_acroform[key]
                    # Add missing font entries in /DR node of source file
                    if (pdfrw.PdfName['DR'] in source_acroform.keys()) and (
                            pdfrw.PdfName['Font'] in source_acroform[pdfrw.PdfName['DR']].keys()):
                        if pdfrw.PdfName['Font'] not in output_acroform[pdfrw.PdfName['DR']].keys():
                            # if output_acroform is missing entirely the /Font node under an existing /DR, simply add it
                            output_acroform[pdfrw.PdfName['DR']][pdfrw.PdfName['Font']] = \
                                source_acroform[pdfrw.PdfName['DR']][
                                    pdfrw.PdfName['Font']]
                        else:
                            # else add new fonts only
                            for font_key in source_acroform[pdfrw.PdfName['DR']][pdfrw.PdfName['Font']].keys():
                                if font_key not in output_acroform[pdfrw.PdfName['DR']][pdfrw.PdfName['Font']]:
                                    output_acroform[pdfrw.PdfName['DR']][pdfrw.PdfName['Font']][font_key] = \
                                        source_acroform[pdfrw.PdfName['DR']][pdfrw.PdfName['Font']][font_key]
                if pdfrw.PdfName['Fields'] not in output_acroform:
                    output_acroform[pdfrw.PdfName['Fields']] = output_formfields
                else:
                    # Add new fields
                    output_acroform[pdfrw.PdfName['Fields']] += output_formfields
            num += 1
        output.trailer[pdfrw.PdfName['Root']][pdfrw.PdfName['AcroForm']] = output_acroform
        output.write(outpath)


class TranslatePdf:
    def __init__(self, pathname, export_folder):
        self._handle_postfix = ['doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx']
        self._filename_list = list()
        # self._export_folder = os.path.join(os.path.abspath('.'), 'pdfconver')
        self._export_folder = export_folder
        if not os.path.exists(self._export_folder):
            os.mkdir(self._export_folder)
        # self._export_folder = export_folder
        self._enumerate_filename(pathname)

    def _enumerate_filename(self, pathname):
        '''
        读取所有文件名
        '''
        full_pathname = os.path.abspath(pathname)
        if os.path.isfile(full_pathname):
            if self._is_legal_postfix(full_pathname):
                self._filename_list.append(full_pathname)
            else:
                raise TypeError('文件 {} 后缀名不合法！仅支持如下文件类型：{}。'.format(pathname, '、'.join(self._handle_postfix)))
        elif os.path.isdir(full_pathname):
            for relpath, _, files in os.walk(full_pathname):
                for name in files:
                    filename = os.path.join(full_pathname, relpath, name)
                    if self._is_legal_postfix(filename):
                        self._filename_list.append(os.path.join(filename))
        else:
            raise TypeError('文件/文件夹 {} 不存在或不合法！'.format(pathname))

    def _is_legal_postfix(self, filename):
        return filename.split('.')[-1].lower() in self._handle_postfix and not os.path.basename(
            filename).startswith(
            '~')

    def run_conver(self):
        '''
        进行批量处理，根据后缀名调用函数执行转换
        '''
        print('需要转换的文件数：', len(self._filename_list))
        for filename in self._filename_list:
            postfix = filename.split('.')[-1].lower()
            funcCall = getattr(self, postfix)
            print('原文件：', filename)
            funcCall(filename)
        print('转换完成！')

    # def doc(self, filename):
    #     '''
    #     doc 和 docx 文件转换
    #     '''
    #     name = os.path.basename(filename).split('.')[0] + '.pdf'
    #     exportfile = os.path.join(self._export_folder, name)
    #     print('保存 PDF 文件：', exportfile)
    #     gencache.EnsureModule('{00020905-0000-0000-C000-000000000046}', 0, 8, 4)
    #     w = Dispatch("Word.Application")
    #     # w = Dispatch("kwps.Application")
    #     try:
    #         doc = w.Documents.Open(filename)
    #         doc.ExportAsFixedFormat(exportfile, constants.wdExportFormatPDF,
    #                                 Item=constants.wdExportDocumentWithMarkup,
    #                                 CreateBookmarks=constants.wdExportCreateHeadingBookmarks)
    #
    #         w.Quit(constants.wdDoNotSaveChanges)
    #     finally:
    #         w.Quit(constants.wdDoNotSaveChanges)
    def doc(self, filename):
        '''
        doc 和 docx 文件转换
        '''
        name = os.path.basename(filename).split('.')[0] + '.pdf'
        exportfile = os.path.join(self._export_folder, name)
        print('保存 PDF 文件：', exportfile)
        convert(filename, exportfile)

    def docx(self, filename):
        self.doc(filename)

    def xls(self, filename):
        '''
        xls 和 xlsx 文件转换
        '''
        name = os.path.basename(filename).split('.')[0] + '.pdf'
        exportfile = os.path.join(self._export_folder, name)
        xlApp = DispatchEx("Excel.Application")
        try:
            xlApp.Visible = False
            xlApp.DisplayAlerts = 0
            books = xlApp.Workbooks.Open(filename, False)
            books.ExportAsFixedFormat(0, exportfile)
            books.Close(False)
            print('保存 PDF 文件：', exportfile)
            xlApp.Quit()
        finally:
            xlApp.Quit()

    def xlsx(self, filename):
        self.xls(filename)

    def ppt(self, filename):
        '''
        ppt 和 pptx 文件转换
        '''
        name = os.path.basename(filename).split('.')[0] + '.pdf'
        exportfile = os.path.join(self._export_folder, name)
        gencache.EnsureModule('{00020905-0000-0000-C000-000000000046}', 0, 8, 4)
        p = Dispatch("PowerPoint.Application")
        try:
            ppt = p.Presentations.Open(filename, False, False, False)
            ppt.ExportAsFixedFormat(exportfile, 2, PrintRange=None)
            print('保存 PDF 文件：', exportfile)
            p.Quit()
        finally:
            p.Quit()

    def pptx(self, filename):
        self.ppt(filename)


if __name__ == '__main__':

    pdf_reader = PyPDF2.PdfFileReader("pdfs/8账户业务申请表-产品投资者（申请免盖骑缝章，双面打印，每份落款处1个公章，一个法人人名章).pdf")
    for page in pdf_reader.pages:
        print(page.extractText())
    # obj = PDFOperate()
    # form_filed = obj.fetch_form_filed("pdfs/8账户业务申请表-产品投资者（申请免盖骑缝章，双面打印，每份落款处1个公章，一个法人人名章).pdf")
    # print(form_filed)
    # data_dict = {
    #     "十亿": "",
    #     "亿": "",
    #     "千万": "1",
    #     "百万": "2",
    #     "十万": "3",
    #     "万": "4",
    #     "千": "",
    #     "百": "",
    #     "拾": "",
    #     "元": "",
    #     "角": "",
    #     "分": "",
    # }
    # obj.append_form_value("pdfs/基金交易类业务申请表.pdf", "aaa.pdf", data_dict)

    # os.rename(f"pdfs/{file_name}",f"pdfs/ceshi")

# class PDFconverterLinux:
#     # -*- coding: utf-8 -*-
#     """
#     linux platform word to pdf
#     """
#     import subprocess
#     import os
#     try:
#         from comtypes import client
#     except ImportError:
#         client = None
#     try:
#         from win32com.client import constants, gencache
#     except ImportError:
#         constants = None
#         gencache = None
#
#     def doc2pdf_linux(docPath, pdfPath):
#         """
#         convert a doc/docx document to pdf format (linux only, requires libreoffice)
#         :param doc: path to document
#         """
#         cmd = 'libreoffice6.3 --headless --convert-to pdf'.split() + [docPath] + ['--outdir'] + [pdfPath]
#         p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
#         p.wait(timeout=30)
#         stdout, stderr = p.communicate()
#         if stderr:
#             raise subprocess.SubprocessError(stderr)
#
#     def doc2pdf(docPath, pdfPath):
#         """
#             convert a doc/docx document to pdf format
#             :param doc: path to document
#             """
#         docPathTrue = os.path.abspath(docPath)  # bugfix - searching files in windows/system32
#         if client is None:  # 判断环境，linux环境这里肯定为None
#             return doc2pdf_linux(docPathTrue, pdfPath)
#         word = gencache.EnsureDispatch('Word.Application')
#         doc = word.Documents.Open(docPathTrue, ReadOnly=1)
#         doc.ExportAsFixedFormat(pdfPath,
#                                 constants.wdExportFormatPDF,
#                                 Item=constants.wdExportDocumentWithMarkup,
#                                 CreateBookmarks=constants.wdExportCreateHeadingBookmarks)
#         word.Quit(constants.wdDoNotSaveChanges)
#
#     if __name__ == '__main__':
#         wordpath = '/var/db/Report_20191206105753.docx'
#         pdfpath = '/var/db'
#         doc2pdf(wordpath, pdfpath)


# from win32com import client as wc
#
# try:
#     excel = wc.DispatchEx('Excel.Application')
# except:
#     try:
#         excel = wc.DispatchEx('ket.Application')
#     except:
#         excel = wc.DispatchEx('et.Application')
# newpdf = excel.Workbooks.Open(r'C:\Users\Administrator\Desktop\tt\abc.xls')
# excel.DisplayAlerts = 0
# # 获取第一个sheet
# all_sheets = [sheet.Name for sheet in newpdf.Sheets]
# ws_source = newpdf.Worksheets(all_sheets[0])
# # 设置页面设置
# ws_source.PageSetup.LeftHeader = ""
# ws_source.PageSetup.CenterHeader = ""
# ws_source.PageSetup.RightHeader = ""
# ws_source.PageSetup.LeftFooter = ""
# ws_source.PageSetup.CenterFooter = ""
# ws_source.PageSetup.RightFooter = ""
# # ws_source.PageSetup.FitToPagesTall = 0
# ws_source.PageSetup.FirstPageNumber = True
# ws_source.PageSetup.LeftMargin = 0
# ws_source.PageSetup.RightMargin = 0
# ws_source.PageSetup.TopMargin = 0
# ws_source.PageSetup.BottomMargin = 0
# ws_source.PageSetup.HeaderMargin = 0
# ws_source.PageSetup.FooterMargin = 0
# # ws_source.PageSetup.PaperSize = 1
# ws_source.PageSetup.Orientation = 2  # 横向转换pdf
# ws_source.PageSetup.FitToPagesWide = 1  # 所有列压缩在一页纸
# ws_source.PageSetup.FitToPagesTall = False
# ws_source.PageSetup.Zoom = False  # 所有列压缩在一页纸
# ws_source.PageSetup.CenterVertically = True
# ws_source.PageSetup.CenterHorizontally = True
# ws_source.PageSetup.Draft = False
# ws_source.Select()
# # 行列自动调整
# # ws_source.Columns.AutoFit()
# # ws_source.Rows.AutoFit()
# # 设置Excel的边框
# rows = ws_source.UsedRange.Rows.Count
# cols = ws_source.UsedRange.Columns.Count
# ws_source.Range(ws_source.Cells(1, 1), ws_source.Cells(rows, cols)).Borders.LineStyle = 1
# ws_source.Range(ws_source.Cells(1, 1), ws_source.Cells(rows, cols)).Borders.TintAndShade = 0
# ws_source.Range(ws_source.Cells(1, 1), ws_source.Cells(rows, cols)).Borders.Weight = 1
# # 转换为PDF文件
# newpdf.ExportAsFixedFormat(0, r'C:\Users\Administrator\Desktop\tt\abc.pdf')
# newpdf.Close()
# excel.Quit()
# def xls(filename):
#     """
#     xls和xlsx文件转换
#     :param filename:
#     :return:
#     """
#     name = os.path.basename(filename).split(".")[0] + ".pdf"
#     exportfile = f"E:\keane_python\github\keane_code\操作pdf文件\转成pdf文件\{name}"
#     xlApp = DispatchEx("Excel.Application")
#     try:
#         xlApp.Visible = False
#         xlApp.DisplayAlerts = 0
#         books = xlApp.Workbooks.Open(filename, False)
#         all_sheets = [sheet.Name for sheet in books.Sheets]
#         ws_source = books.Worksheets(all_sheets[0])
#         ws_source.PageSetup.Orientation = 1
#         ws_source.PageSetup.Zoom = False
#         ws_source.PageSetup.FitToPagesTall = False
#         books.ExportAsFixedFormat(0, exportfile)
#         books.Close()
#         print(f"保存pdf文件：", exportfile)
#     finally:
#         xlApp.Quit()
