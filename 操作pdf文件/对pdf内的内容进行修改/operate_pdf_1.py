#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  operate_pdf_1.py
:time  2022/8/3 10:55
:desc  
"""
import os
import PyPDF2
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject, NumberObject, TextStringObject


def set_need_appearances_writer(writer):
    # basically used to ensured there are not
    # overlapping form fields, which makes printing hard
    try:
        catalog = writer._root_object
        # get the AcroForm tree and add "/NeedAppearances attribute
        if "/AcroForm" not in catalog:
            writer._root_object.update({
                NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)})

        need_appearances = NameObject("/NeedAppearances")
        writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)


    except Exception as e:
        print('set_need_appearances_writer() catch : ', repr(e))

    return writer


file_path = os.path.dirname(__file__)
invoice_template_path = f"{file_path}/pdfs/1.基金账户类业务申请表（机构）（部门章1）.pdf"
invoice_output_path = f"{file_path}/pdfs/改基金账户类业务申请表1.pdf"

data_dict = dict(fill_6='2022年12月31日', )  # this is a dict of your DB form values


# output_stream is your flattened PDF
# 添加pdf表单数据
def append_pdf_form(pdf_file_path, general_pdf_path, data_dict):
    """
    添加pdf表单数据
    :return:
    """
    pdf_stream = open(pdf_file_path, "rb")
    pdf_reader = PyPDF2.PdfFileReader(pdf_stream, strict=False)
    if "/AcroForm" in pdf_reader.trailer["/Root"]:
        pdf_reader.trailer["/Root"]["/AcroForm"].update({NameObject("/NeedAppearances"): BooleanObject(True)})

    pdf_writer = PyPDF2.PdfFileWriter()
    try:
        catalog = pdf_writer._root_object
        if "/AcroForm" not in catalog:
            pdf_writer._root_object.update(
                {NameObject("/AcroForm"): IndirectObject(len(pdf_writer._objects), 0, pdf_writer)})
        need_appearances = NameObject("/NeedAppearances")
        pdf_writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
    except Exception as e:
        print('set_need_appearances_writer() catch : ', repr(e))
    if "/AcroForm" in pdf_writer._root_object:
        pdf_writer._root_object["/AcroForm"].update({NameObject("/NeedAppearances"): BooleanObject(True)})
    for page_index in range(len(pdf_reader.pages)):
        pdf_writer.addPage(pdf_reader.getPage(page_index))
        page = pdf_writer.getPage(page_index)
        pdf_writer.updatePageFormFieldValues(page, data_dict)
        for j in range(0, len(page['/Annots'])):
            writer_annot = page['/Annots'][j].getObject()
            if writer_annot.get('/T') == data_dict:
                writer_annot.update({
                    NameObject("/V"): TextStringObject(data_dict[writer_annot.get('/T')])  # make ReadOnly
                })
        output_stream = open(general_pdf_path, "wb")
        pdf_writer.write(output_stream)


if __name__ == '__main__':
    file_path = os.path.dirname(__file__)
    invoice_template_path = f"{file_path}/pdfs/6.基金交易类业务申请表（部门章1）.pdf"
    invoice_output_path = f"{file_path}/pdfs/改基金账户类业务申请表6.pdf"

    data_dict = dict(fill_4='壹', fill_5="贰")  # this is a dict of your DB form values

    append_pdf_form(invoice_template_path, invoice_output_path, data_dict)
