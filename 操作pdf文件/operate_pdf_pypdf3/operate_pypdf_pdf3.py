#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  operate_pypdf_pdf3.py
:time  2023/8/25 17:10
:desc  
"""
import PyPDF3
from PyPDF3.generic import BooleanObject, NameObject, IndirectObject, NumberObject, TextStringObject


class OperatePdf:
    def __init__(self):
        pass

    def get_pdf_form(self, model_path):
        pdf_stream = open(model_path, "rb")
        pdf_reader = PyPDF3.PdfFileReader(pdf_stream, strict=True)
        print(pdf_reader.getFormTextFields())

    @staticmethod
    def append_pdf_form(model_path, output_path, data_dict):
        """"""
        pdf_stream = open(model_path, "rb")
        pdf_reader = PyPDF3.PdfFileReader(pdf_stream, strict=False)
        if "/AcroForm" in pdf_reader.trailer["/Root"]:
            pdf_reader.trailer["/Root"]["/AcroForm"].update({NameObject("/NeedAppearances"): BooleanObject(True)})

        pdf_writer = PyPDF3.PdfFileWriter()
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
            pdf_writer.addPage(pdf_reader.pages[page_index])
            page = pdf_writer.getPage(page_index)
            pdf_writer.updatePageFormFieldValues(page, data_dict)
            # for j in range(0, len(page['/Annots'])):
            #     writer_annot = page['/Annots'][j].get_object()
            #
            #     if writer_annot.get('/T') in data_dict:
            #         writer_annot.update({
            #             NameObject("/V"): TextStringObject(data_dict[writer_annot.get('/T')])  # make ReadOnly
            #         })
        output_stream = open(output_path, "wb")
        pdf_writer.write(output_stream)

    def combine_pdf(self, pdfs, outpath):
        """合并pdf"""
        pdf_merger = PyPDF3.PdfFileMerger()
        for pdf in pdfs:
            pdf_merger.append(pdf)
        with open(outpath, 'wb') as output_file:
            pdf_merger.write(output_file)


if __name__ == '__main__':
    obj = OperatePdf()
    model_file_path = "源文件.pdf"
    # obj.get_pdf_form(model_file_path)
    output_file_path = "基金交易类业务申请表_g12.pdf"
    data_dict = {
        'fill_28': "2222222",
        'fill_1': "建信尊享偏债两年定开家族专享7号",
        'fill_3': "10,000,000.00",
        '元': '1',
        '拾': '2',
        '佰': '3',
        '仟': '4',
        '万': '5',
        '拾万': '6',
        '佰万': '7',
        '仟万': '8',
        '亿': '9',
        '拾亿': '1',
        '佰亿': '2',
        '仟亿': '3'
    }
    # obj.append_pdf_form(model_file_path, output_file_path, data_dict)
    pdfs = ["基金交易类业务申请表_g11.pdf", "基金交易类业务申请表_g12.pdf"]
    output_path = "aaaa.pdf"
    obj.combine_pdf(pdfs,output_path)