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


# 2层卷积3层全连接，共5层
# ------------------卷积--------------------
# 第一层卷积 输入：1*32*32（1维）      6*5*5(5*5卷积核 6维)     输出((32-5)/1)+1=28
# 第一层池化 输入：6*28*28（6维）      输出：（28/2）=14
# 第二层卷积 输入：6*14*14（6维）      16*5*5(5*5卷积核 16维)   输出((14-5)/1)+1 = 10
# 第二层池化 输入：6*12*12（16维）     输出：10/2 = 5
# -----------------全连接------------------
# 第一层全连接层 输入：16*5*5=400  输出120
# 第二层全连接层 输入：1*120   输出84
# 第三层全连接层 输入：1*84    输出类别

class LeNetPaddle(nn.Layer):
    def __init__(self, num_classes=10):
        super(LeNetPaddle, self).__init__()
        self.num_classes = num_classes
        self.features = nn.Sequential(
            nn.Conv2D(1, 6, 5, stride=1, padding=0),
            nn.ReLU(),
            nn.MaxPool2D(2, 2),
            nn.Conv2D(6, 16, 5, stride=1, padding=0),
            nn.ReLU(),
            nn.MaxPool2D(2, 2)
        )
        if num_classes > 0:
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


le_net = LeNetPaddle()
paddle.summary(le_net, (1, 1, 32, 32))
