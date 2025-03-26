#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_02.py
:time  2025/3/13 9:53
:desc  #
"""
import os
from tkinter import Image

import cv2
import numpy as np
import paddle
from paddle.io import Dataset, DataLoader
from paddle import nn
from PIL import Image
from paddle.vision.transforms import transforms

# image_path = r"E:\keane_python\github\keane_code\A_Test_codes\fruits_classify\fruits\apple\0.jpg"
# image = cv2.imread(image_path)
# transform = transforms.ToTensor()
# image_tensor = transform(image).unsqueeze(0)
# out1 = paddle.nn.Conv2D(3, 3, 3, stride=2, padding=0)
# out1 = out1(image_tensor)
# output_image = out1.squeeze(0).squeeze(0).numpy()
# output_image = (output_image * 255).astype(np.uint8)
# output_image = output_image.reshape(output_image.shape[1], output_image.shape[2], 3)
# cv2.imshow("output", output_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# output_image = Image.fromarray(output_image)
# output_image.show()

# ----------------------------------------------------------------------------------------------------------------------
from pathlib import Path
from dataclasses import dataclass
@dataclass
class Config:
    x:int
    y:int


print(Path(__file__).parent)
base_dir = Path(__file__).parent
new_dir = base_dir / "new_dir"
base_dir.exists()