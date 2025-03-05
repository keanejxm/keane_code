#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_01.py
:time  2025/1/26 13:54
:desc  
"""
import paddle
from paddle import nn


class VGG16Paddle(nn.Layer):
    def __init__(self, num_classes=1000):
        super(VGG16Paddle, self).__init__()
        self.num_classes = num_classes
        self.features = nn.Sequential(
            # 第一组 输入3*224*224  卷积核：64*3*3
            nn.Conv2D(3, 64, 3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2D(64, 64, 3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2D(2, 2),
            # 第二组
            nn.Conv2D(64, 128, 3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2D(128, 128, 3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2D(2, 2),
            # 第三组
            nn.Conv2D(128, 256, 3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2D(256, 256, 3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2D(256, 256, 3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2D(2, 2),
            # 第四组
            nn.Conv2D(256, 512, 3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2D(512, 512, 3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2D(512, 512, 3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2D(2, 2),
            # 第五组
            nn.Conv2D(512, 512, 3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2D(512, 512, 3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2D(512, 512, 3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2D(2, 2),
        )
        if num_classes > 0:
            self.classifier = nn.Sequential(
                nn.Linear(512 * 7 * 7, 4096),
                # nn.ReLU(),
                nn.Linear(4096, 4096),
                # nn.ReLU(),
                nn.Linear(4096, num_classes),
                nn.ReLU(),
            )

    def forward(self, x):
        x = self.features(x)
        if self.num_classes > 0:
            x = paddle.flatten(x, 1)
            x = self.classifier(x)
        return x


vvg_16_paddle = VGG16Paddle()
paddle.summary(vvg_16_paddle, (1, 3, 224, 224))
