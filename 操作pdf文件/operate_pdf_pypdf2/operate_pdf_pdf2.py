#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  operate_pdf.py
:time  2023/8/22 11:19
:desc  使用pypdf2操作pdf
"""

import PyPDF2
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject, NumberObject, TextStringObject


class OperatePdf:
    def __init__(self):
        pass


    def get_pdf_form(self,model_path):
        pdf_stream = open(model_path, "rb")
        pdf_reader = PyPDF2.PdfReader(pdf_stream, strict=True)
        print(pdf_reader.get_form_text_fields())

    @staticmethod
    def append_pdf_form(model_path, output_path, data_dict):
        """"""
        pdf_stream = open(model_path, "rb")
        pdf_reader = PyPDF2.PdfReader(pdf_stream, strict=False)
        if "/AcroForm" in pdf_reader.trailer["/Root"]:
            pdf_reader.trailer["/Root"]["/AcroForm"].update({NameObject("/NeedAppearances"): BooleanObject(True)})

        pdf_writer = PyPDF2.PdfWriter()
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
            pdf_writer.add_page(pdf_reader.pages[page_index])
            page = pdf_writer.pages[page_index]
            pdf_writer.update_page_form_field_values(page, data_dict)
            for j in range(0, len(page['/Annots'])):
                writer_annot = page['/Annots'][j].get_object()

                if writer_annot.get('/T') in data_dict:
                    writer_annot.update({
                        NameObject("/V"): TextStringObject(data_dict[writer_annot.get('/T')])  # make ReadOnly
                    })
            output_stream = open(output_path, "wb")
            pdf_writer.write(output_stream)

    def combine_pdf(self, pdfs, outpath):
        """合并pdf"""
        pdf_merger = PyPDF2.PdfMerger()
        for pdf in pdfs:
            pdf_merger.append(pdf)
        with open(outpath, 'wb') as output_file:
            pdf_merger.write(output_file)

    def get_content(self,model_path):
        pdf_stream = open(model_path, "rb")
        pdf_reader = PyPDF2.PdfReader(pdf_stream, strict=True)
        for page_num,page in enumerate(pdf_reader.pages):
            print(page.extractText())


    def add_page_num(self,file_path):
        pdf_file = open(file_path,"rb")
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        # 获取总页数
        total_pages = pdf_reader.numPages

        pdf_writer = PyPDF2.PdfFileWriter()
        for page_num in range(total_pages):
            page = pdf_reader.getPage(page_num)
            page.merge_page(page.createBlankPage(width=page.mediaBox.getWidth(),height=page.mediaBox.getHeight()))
            page.merge_page(page)
            page.merge_page(page)
            page.merge_page(page)
            page.merge_page(page)
            page.merge_page(page)
            pdf_writer.addPage(page)
        output_pdf = open("output.pdf","wb")
        pdf_writer.write(output_pdf)
        output_pdf.close()
        pdf_file.close()




if __name__ == '__main__':
    obj = OperatePdf()
    # pdfs =["基金交易类业务申请表_g11.pdf","基金交易类业务申请表_g12.pdf","基金交易类业务申请表_g13.pdf"]
    # pdfs =["基金交易类业务申请表3569-1电子章，手动录入.pdf","基金交易类业务申请表6705-1电子章，手动录入.pdf","基金交易类业务申请表10796-1电子章，手动录入.pdf"]
    # output_path = "aaaa.pdf"
    # obj.combine_pdf(pdfs,output_path)
    # model_file_path = "基金交易类业务申请表_old1.pdf"
    # model_file_path = "源文件.pdf"
    # # obj.get_pdf_form(model_file_path)
    # output_file_path = "基金交易类业务申请表_g11.pdf"
    # data_dict = {
    #     'fill_28': "1111111111",
    #     'fill_1': "建信尊享偏债两年定开家族专享7号",
    #     'fill_3': "10,000,000.00",
    #     '元': '1',
    #     '拾': '2',
    #     '佰': '3',
    #     '仟': '4',
    #     '万': '5',
    #     '拾万': '6',
    #     '佰万': '7',
    #     '仟万': '8',
    #     '亿': '9',
    #     '拾亿': '1',
    #     '佰亿': '2',
    #     '仟亿': '3'
    # }
    # obj.append_pdf_form(model_file_path, output_file_path, data_dict)
    # mod_path = "靳晓明车上人员.pdf"
    mod_path = "document.pdf"
    obj.get_content(mod_path)
