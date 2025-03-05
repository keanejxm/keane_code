#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_01.py
:time  2025/1/26 13:54
:desc  
"""
import os
import cv2
import numpy as np
import paddle
from matplotlib import pyplot as plt
from paddle.io import DataLoader, Dataset
from paddle.vision import transforms
from paddle.vision.transforms import Compose, Normalize
from paddle import nn


class ResNetPaddle(nn.Layer):
    def __init__(self, num_classes=1000):
        super(ResNetPaddle, self).__init__()
        self.num_classes = num_classes
        self.features = nn.Sequential(
            nn.Conv2D()
        )