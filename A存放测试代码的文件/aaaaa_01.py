#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_01.py
:time  2025/1/26 13:54
:desc  
"""
import os.path

# if not os.path.exists("aaaa"):
#     os.mkdir("aaaa")

# import cv2
#
# img1 = cv2.imread("1df58719a.webp")
# img2 = cv2.imread("d401d55fc.webp")
# add = cv2.add(img1,img2)
# cv2.imshow("image",add)
# cv2.imshow("image2",img2)
# cv2.imshow("iamge1",img1)
# cv2.waitKey()
# cv2.destroyAllWindows()
import time

# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(1738830399)))
# print(time.mktime(time.strptime("20250206", "%Y%m%d")))
# b = time.strftime("%Y%m%d", time.localtime(time.mktime(time.strptime("20250206", "%Y%m%d")) - 1 * 24 * 60 * 60))
# print(b)
import cv2

img1 = cv2.imread(r"E:\keane_python\github\keane_code\A存放测试代码的文件\户型图.jpg")
cv2.imshow("img1", img1)
flip = cv2.flip(img1, 1)
cv2.imshow("img2", flip)
cv2.waitKey()

# cv2.imshow("img1",img1)
# cv2.waitKey()
cv2.destroyAllWindows()


