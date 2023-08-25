#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  operate_pdf_rw.py
:time  2023/8/22 13:44
:desc  使用pdfrw对pdf进行操作
"""
import pdfrw

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

ANNOT_VAL_KEY = '/V'
ANNOT_TU_KEY = "/TU"
from pdfrw.objects.pdfstring import PdfString
from pdfrw.objects.pdfname import PdfName
from pdfrw.objects.pdfdict import PdfDict
from pdfrw import PdfReader, PdfWriter, PdfName


class OperatePdfRW:
    def __init__(self):
        pass

    @staticmethod
    def find_pdf_form(model_path):
        template_pdf = pdfrw.PdfReader(model_path)
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
                        # key_tu = annotation[ANNOT_TU_KEY] if annotation[ANNOT_TU_KEY] and isinstance(
                        #     annotation[ANNOT_TU_KEY], PdfString) else None
                        # value = annotation[ANNOT_VAL_KEY] if annotation[ANNOT_VAL_KEY] and isinstance(
                        #     annotation[ANNOT_VAL_KEY], PdfString) else None
                        # if key_tu:
                        #     print(value, value.to_unicode())

    @staticmethod
    def append_pdf_value(input_pdf_path, output_pdf_path, data_dict):
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
                print(type(annotation))
                if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                    if annotation[ANNOT_FIELD_KEY]:
                        if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                            if annotation[ANNOT_FIELD_KEY]:
                                key = annotation[ANNOT_FIELD_KEY][1:-1]
                                if key in data_dict.keys():
                                    annotation.update(pdfrw.PdfDict(V=data_dict[key], Ff=1))
                                    # annotation.update({PdfName("V"):data_dict[key],PdfName("Ff"):1})
        pdfrw.PdfWriter().write(output_pdf_path, template_pdf)

    @staticmethod
    def combine_pdf(pdf_files, outpath):
        """"""
        output = PdfWriter()
        num = 0
        output_acroform = None
        for pdf in pdf_files:
            input = PdfReader(pdf, verbose=False)
            output.addpages(input.pages)
            if PdfName('AcroForm') in input[PdfName('Root')].keys():  # Not all PDFs have an AcroForm node
                source_acroform = input[PdfName('Root')][PdfName('AcroForm')]
                if PdfName('Fields') in source_acroform:
                    output_formfields = source_acroform[PdfName('Fields')]
                else:
                    output_formfields = []
                num2 = 0
                for form_field in output_formfields:
                    key = PdfName('T')
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
                    if (PdfName('DR') in source_acroform.keys()) and (
                            PdfName('Font') in source_acroform[PdfName('DR')].keys()):
                        if PdfName('Font') not in output_acroform[PdfName('DR')].keys():
                            # if output_acroform is missing entirely the /Font node under an existing /DR, simply add it
                            output_acroform[PdfName('DR')][PdfName('Font')] = source_acroform[PdfName('DR')][
                                PdfName('Font')]
                        else:
                            # else add new fonts only
                            for font_key in source_acroform[PdfName('DR')][PdfName('Font')].keys():
                                if font_key not in output_acroform[PdfName('DR')][PdfName('Font')]:
                                    output_acroform[PdfName('DR')][PdfName('Font')][font_key] = \
                                        source_acroform[PdfName('DR')][PdfName('Font')][font_key]
                if PdfName('Fields') not in output_acroform:
                    output_acroform[PdfName('Fields')] = output_formfields
                else:
                    # Add new fields
                    output_acroform[PdfName('Fields')] += output_formfields
            num += 1
        output.trailer[PdfName('Root')][PdfName('AcroForm')] = output_acroform
        output.write(outpath)

    @staticmethod
    def pdf_encode(input_str):
        origin_str = b'\xfe\xff'
        return f"({(origin_str + input_str.encode('utf-16-be')).decode('Latin-1')})"


if __name__ == '__main__':
    obj = OperatePdfRW()
    a = "2023年8月23日"
    b = b'\xfe\xff'
    print(f"({(b + a.encode('utf-16-be')).decode('Latin-1')})")
    # model_file_path = "基金交易类业务申请表_old1.pdf"
    model_file_path = "基金账户类业务申请表.pdf"
    # obj.find_pdf_form(model_file_path)
    data_dict = {
        'fill_6': '2023-08-25',
         'fill_9': '建信信托-私人银行家族信托单一信托1858号\xa0',
         'fill_25': '建信信托有限责任公司',
         'fill_26': '34050146860800002176',
         'fill_27': '中国建设银行合肥庐阳支行',
         'fill_8_2': '建信信托-私人银行家族信托单一信托1858号\xa0',
         'fill_4_2': '2018-06-08',
         'fill_9_2': 'ZXD32J20180500007564X',
         'fill_10_2': '2018年09月13日',
         'fill_11_2': '中国建设银行合肥庐阳支行',
         'fill_7_2': '960月',
         'fill_12_2': '伍仟万元整'}
    pdfs = ["基金交易类业务申请表_g11.pdf", "基金交易类业务申请表_g12.pdf"]
    output_path = "aaaa.pdf"
    obj.combine_pdf(pdfs, output_path)
    # model_file_path = "源文件.pdf"
    output_file_path = "基金交易类业务申请表_g13.pdf"
    # product_name = "中文字体编码后的结果"
    # # b =  PdfString(obj.pdf_encode(product_name))
    # # print(b.to_unicode())
    #
    # data_dict = {
    #     'fill_28': PdfString(obj.pdf_encode(product_name)),
    #     'fill_1': "bbbbbb",
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
    # obj.append_pdf_value(model_file_path, output_file_path, data_dict)
