# -*- coding:utf-8 -*-
"""
计算图片的hash值。
# author: Trico
# date: 2021/1/25
# update: 2021/1/25
"""

import os
import io
import imagehash
from PIL import Image


def img_hash(img_bytes):
    """
    图片哈希（类似：4f999cc90979704c）。
    :param img_bytes: 图片内容流（Bytes类型）。
    :return: <class 'imagehash.ImageHash'>
    """

    assert img_bytes and isinstance(img_bytes, bytes), f"参数错误，img_bytes：{img_bytes}"
    img_fp = io.BytesIO(img_bytes)
    img = Image.open(img_fp)
    return str(imagehash.dhash(img))


def hamming_distance(res1, res2):
    """
    汉明距离，越小说明越相似，等0说明是同一张图片，大于10越上，说明完全不相似。
    :param res1:
    :param res2:
    :return:
    """
    str1 = str(res1)  # <class 'imagehash.ImageHash'> 转成 str
    str2 = str(res2)
    num = 0  # 用来计算汉明距离
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            num += 1
    return num


def test():
    # 测试。

    resources_path = "./resources"
    pics = os.listdir(resources_path)
    for pic in pics:
        if pic.endswith(".png") or pic.endswith(".jpg"):
            img_file = f"{resources_path}/{pic}"
            with open(img_file, "rb") as fr:
                img_bytes = fr.read()
                if img_bytes:
                    h = img_hash(img_bytes)
                    print(f"{pic}，{h}")
                else:
                    print(f"{pic}")


if __name__ == '__main__':
    test()
