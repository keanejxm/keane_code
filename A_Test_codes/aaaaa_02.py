#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_02.py
:time  2025/3/13 9:53
:desc  #
"""
# import pandas as pd
#
# df = pd.DataFrame([[1,2,3,4],[5,6,7,8],[9,10,11,12]],columns=['A','B','C','D'])
# df.sort_values('A',ascending=True,inplace=True)
# print(df)

import cv2

img = cv2.imread('a_a.png')
new_img = cv2.resize(img, (800, 600))
cv2.imwrite('new_a.png', new_img)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()