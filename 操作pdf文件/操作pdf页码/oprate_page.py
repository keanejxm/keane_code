#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  oprate_page.py
:time  2024/5/16 15:49
:desc  
"""
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io


def CreatePageWithWords(words, x, y):
    packet = io.BytesIO()
    # 使用Reportlab创建一个新的PDF，原理是将两个页面叠加起来
    can = canvas.Canvas(packet, pagesize=A4)
    pdfmetrics.registerFont(TTFont("chs", "C:/Windows/Fonts/simsunb.ttf"))
    can.setFont("chs", 12)
    can.drawString(x, y, str(words))
    can.save()
    packet.seek(0)
    return PdfReader(packet)


def AddNumber():
    # input1 = input("输入原始文件路径：")
    input1 = "3.芜湖宸乾产权变动申请.pdf"
    pdf_file = PdfReader(open(input1, "rb"))
    # dir_path = input("输入输出文件路径(包含文件名)：")
    dir_path = "111.pdf"
    output = PdfWriter()
    for i in range(len(pdf_file.pages)):
        new_pdf = CreatePageWithWords(i + 1, 100, 40)
        page = pdf_file.pages[i]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)
        print("\r progress:{:.0f}%".format((i + 1) / len(pdf_file.pages) * 100), end="")
    with open(dir_path, 'wb') as out:
        output.write(out)
    print("Done!")

if __name__ == '__main__':
    AddNumber()