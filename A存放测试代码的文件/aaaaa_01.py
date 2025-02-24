#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_01.py
:time  2025/1/26 13:54
:desc  
"""
import cv2
import os
import matplotlib.pyplot as plt

data_dir = r"E:\keane_data\img_data"

img = cv2.imread(os.path.join(data_dir, r"1.png"), flags=1)
img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)

img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])

bgr_img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

cv2.imshow("bgr", bgr_img)
cv2.imshow("img",img)

plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()
