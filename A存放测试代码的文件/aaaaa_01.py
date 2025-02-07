#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_01.py
:time  2025/1/26 13:54
:desc  
"""
import os.path
import requests

# 数字、字符、表达式
#
# url = "https://jdyboss.zbj.com/api/DemandV3Service/getDemandHallListv3"
# headers = {
#     "cookie": "_uq=83c578b8af7423a23fbab51ac50330bb; uniqid=d01maaw5nv232; _suq=709cf479-4e32-4cec-9514-bf8f4c6e4437; unionJsonOcpc=eyJvdXRyZWZlcmVyIjoiaHR0cHM6Ly93d3cuYmFpZHUuY29tL290aGVyLnBocD9zYy5LZjAwMDBLUXYtcjRGZVEiLCJwbWNvZGUiOiIxMzc1MzU4MDgiLCJ1dG1fc291cmNlIjoiYmRweiJ9; local_city_id=3374; local_city_path=beijing; local_city_name=%E5%8C%97%E4%BA%AC; Hm_lvt_a360b5a82a7c884376730fbdb8f73be2=1738725951; HMACCOUNT=C3AAB8DD0F63050E; vidSended=1; nsid=s%3AAeQeF1BHiDhvplPMky7VacXGcFrRoNMp.SP2QL2GTMLLIB6ZEMvF%2FiDL%2BoN5Z2KxBsH4qk%2Bf%2BXKU; fromurl=75556ffa158ff22c20daf9f4d01536352d510c1a479e2584213771687957e84c; s_s_c=mf9g4pQe2XL9Jx9CXRxQeRNAuuZR46Ff%2B3H4jsDtifRID5w32DRxlUBReG3unP%2BA6E44mIsr48aar1eN2Ggxsg%3D%3D; nickname=%E9%A2%9C%E5%A4%A7%E5%93%A6; brandname=%E9%A2%9C%E5%A4%A7%E5%93%A6; userid=33943900; userkey=7otyUPV%2FWK%2B%2BscM3WN%2FRqYvQG7FC%2BuyyQn%2B3ZMoRn8U%2ByQWiYO6fFv6Rigu9ASyrFElwrTESGaB5I5RdPS%2BuMlzDVGs1d8OzZxl0ojeU%2FEu%2BlFy5f8nyc2nFfUCD%2Fr1bLzH%2BrCH%2F4Lkb62aUHwacR41UYbVAUXkZmE7D4OwUbmUI9Vpk1E0lKIA1byeAmsJAe56Vr5VO6WilpIuNY76l%2BkJPnF1%2BxlgqTQ8dl%2FRTJXNuBBRUI6Ief8WPkXSz8O%2B%2Frode665LTLmFAJPDO8JLeR4VKw%2FEK13LRJYM3OkQaOynzoHhRJaPlXiFBCWEMx2trtMr1NbNyvInow%3D%3D; organizeId=1218984; orgMaster=1; shopName-33943900=%E9%A2%9C%E5%A4%A7%E5%93%A6; jdymenuchannel=1; jdy_manager_qr=1; show-standard-service2025chujiehuodong33943900=1; promotion33943900_ok=true; Hm_lpvt_a360b5a82a7c884376730fbdb8f73be2=1738735187; oldvid=60f73dd1ab59c7db5fa52f68e9c87b6e; vid=97c9186b1feddcda66cc966026c7f247",
#     "origin": "https://jdyboss.zbj.com",
#     "priority": "u=1, i",
#     "referer": "https://jdyboss.zbj.com/osg/open_hall?tab=0&supei=1",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
# }
# data = {"pageNum": 1, "pageSize": 24, "source": 1, "sellerHallType": 4, "category1Id": [18216],
#         "dispatchSearchType": [0]}
# res = requests.post(url, headers=headers, json=data)
# print(res.text)
#
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

img1 = cv2.imread("01.webp")

cv2.imshow("img1",img1)
cv2.waitKey()
cv2.destroyAllWindows()


