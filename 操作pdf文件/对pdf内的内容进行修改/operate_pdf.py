#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  operate_pdf.py
:time  2022/8/2 10:44
:desc  
"""
import os
import pdfrw

file_path = os.path.dirname(__file__)
annot_key = '/Annois'
annot_field_key = '/T'
annot_rect_key = '/Rect'
subtype_key = '/Subtype'
widget_subtype_key = '/Widget'
invoice_template_path = f"{file_path}/pdfs/6.基金交易类业务申请表（部门章1）.pdf"
invoice_output_path = f"{file_path}/aaaaa.pdf"


def write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict):
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    pdf_pages = len(template_pdf.pages)
    print(template_pdf.Root)
    print(template_pdf.Root.AcroForm)
    print(template_pdf.Root.AcroForm.Fields)
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    for pagenum in range(pdf_pages):
        aa = template_pdf.pages[pagenum]
        annotaions = template_pdf.pages[pagenum][annot_rect_key]
        if not annotaions:
            continue
        for annotaion in annotaions:
            if annotaion[subtype_key] == widget_subtype_key:
                if annotaion[annot_field_key]:
                    key = annotaion[annot_field_key][1:-1]
                    if key in data_dict.keys():
                        annotaion.update(pdfrw.PdfDict(V=f"{data_dict[key]}"))
        pdfrw.PdfWriter().write(output_pdf_path, template_pdf)


if __name__ == '__main__':
    from PyPDF2 import PdfFileReader,PdfFileWriter

    pdf_reader = PdfFileReader(open(invoice_template_path, "rb"))
    pdf_writer = PdfFileWriter()
    print(pdf_reader.getFormTextFields())
    dictionary = pdf_reader.getFormTextFields()  # returns a python dictionary
    dictionary["fill_6"]="2022年8月3日"
    print(dictionary["fill_6"])
    print(dictionary)
    print(dictionary)
    data_dict = {}
    write_fillable_pdf(invoice_template_path, invoice_output_path, data_dict)
