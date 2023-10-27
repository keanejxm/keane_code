#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
图片工具库。
# author: Trico
# date: 2019.11.18
# update: 2019.11.18
"""

import io
import cv2
import numpy as np
from PIL import Image


def tif_to_jpg_cv2(input_bytes):
    """
    TIF格式图片转为JPG格式。
    :return:
    """

    image = np.asarray(bytearray(input_bytes))
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = cv2.imencode(".jpg", image)[1]
    image = np.array(image)
    output_bytes = image.tostring()

    return output_bytes


def tif_to_jpg_pil(input_bytes):
    """
    TIF格式图片转为JPG格式。
    :return:
    """

    byte_stream = io.BytesIO(input_bytes)
    image = Image.open(byte_stream)
    # 去掉了透明度。
    image = image.convert('RGB')
    temp_byte_stream = io.BytesIO()
    image.save(temp_byte_stream, format='JPEG')
    output_bytes = temp_byte_stream.getvalue()

    return output_bytes


def compress_image(input_bytes, limit_size=100 * 1024, limit_x_y=(500, 500)):
    """
    压缩图片。
    :return:
    """

    # 参数验证。
    assert input_bytes and isinstance(input_bytes, bytes), "Param error, input_bytes."
    assert isinstance(limit_size, int) and limit_size > 0, "Param error, limit_size: {}.".format(limit_size)
    assert isinstance(limit_x_y, (tuple, list)) and len(limit_x_y) == 2, "Param error, limit_x_y: {}.".format(limit_x_y)
    for pixel in limit_x_y:
        assert pixel > 0, "Param error, limit_x_y: {}.".format(limit_x_y)

    # 大小满足条件时即刻返回。
    current_size = len(input_bytes)
    if current_size <= limit_size:
        return input_bytes

    # 转换成图片对象。
    output_bytes = input_bytes
    input_stream = io.BytesIO(input_bytes)
    image = Image.open(input_stream)
    # 小于指定分辨率时即刻返回。
    x, y = image.size
    if x < limit_x_y[0] or y < limit_x_y[1]:
        return input_bytes

    # 降低图片分辨率。
    if current_size > limit_size:
        for zoom in range(90, 10, -10):
            # 换为百分比。
            zoom = zoom / 100
            _x = int(x * zoom)
            _y = int(y * zoom)
            # 变更分辨率。
            temp_image = image.resize((_x, _y), Image.ANTIALIAS)
            _x, _y = temp_image.size
            # 产出。
            out_stream = io.BytesIO()
            temp_image.save(out_stream, format='JPEG')
            output_bytes = out_stream.getvalue()
            current_size = len(output_bytes)
            # 达到条件时返回。
            if current_size <= limit_size:
                return output_bytes
            # 检查分辨率是否已达到下限。
            if _x < limit_x_y[0] or _y < limit_x_y[1]:
                # 以缩小后的图片对象替代原始图片对象，供后续压缩。
                image = temp_image
                break

    # 降低图片质量。
    if current_size > limit_size:
        for quality in range(90, 10, -10):
            # 产出。
            out_stream = io.BytesIO()
            # 逐渐降低图片质量。
            image.save(out_stream, format='JPEG', quality=quality)
            output_bytes = out_stream.getvalue()
            current_size = len(output_bytes)
            # 达到条件时返回。
            if current_size <= limit_size:
                return output_bytes

    return output_bytes


def tif_to_jpg(*args, **kwargs):
    # TIF格式图片转为JPG格式。

    return tif_to_jpg_pil(*args, **kwargs)
