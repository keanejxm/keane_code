# Author Keane
# coding=utf-8
# @Time    : 2021/1/13 12:03
# @File    : pandas_untils.py
# @Software: PyCharm
import pandas as pd
class Pandas(object):
    def read_xml(self):
        df = pd.read_excel(r".xls")
        for i in df["appname"]:
            print(i)
if __name__ == '__main__':
    pds = Pandas()
    pds.read_xml()