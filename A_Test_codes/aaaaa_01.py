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


class LeNet(nn.Layer):
    def __init__(self, num_classes=10):
        super(LeNet, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2D(1, 6, 3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2D(2, 2),
            nn.Conv2D(6, 16, 5, stride=1, padding=0),
            nn.ReLU(),
            nn.MaxPool2D(2, 2)
        )
        if num_classes > 10:
            self.classifier = nn.Sequential(
                nn.Linear(16 * 5 * 5, 120),
                nn.Linear(120, 84),
                nn.Linear(84, num_classes)
            )
    def forward(self, x):
        x = self.features(x)
        if self.num_classes > 0:
            x = paddle.flatten(x, 1)
            x = self.classifier(x)
        return x
