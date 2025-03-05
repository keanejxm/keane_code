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


# AlexNet 共8层 前五层为卷积池化，后三层为全连接
# 第一层卷积层 输入：3*224*224       卷积核：48个11*11  步长4  填充0   ((227+2*0-11)/4)+1=55
# 第一层池化层 输入：48*2个3*55*55     最大池化3*3 步长2     ((55-3)/2)+1=27
# 第二层卷积成 输入：48*2个3*27*27     卷积核：128个5*5  步长1   填充2    ((27+2*2-5)/1)+1=27
# 第二层池化层 输入：128*2个3*27*27    最大池化3*3  步长2     ((27-3)/2)+1 = 13
# 第三层卷积层 输入：128*2个3*13*13    卷积核：192个3*3  步长1   填充1 ((13+1*2-3)/1)+1 = 13
# 第四层卷积层 输入：192*2个3*13*13    卷积核：192个3*3  步长1   填充1 ((13+2*1-3)/1)+1 =13
# 第五层卷积层 输入：192*2个3*13*13    卷积核：128个3*3  步长1   填充1 ((13+2*1-3)/1)+1 =13
# 第五层池化层 输入：128*2个3*13*13    最大池化3*3 步长2  ((13-3)/2)+1 = 6


class AlexNetPaddle(nn.Layer):
    def __init__(self, num_classes=1000):
        super(AlexNetPaddle, self).__init__()
        self.num_classes = num_classes
        self.features = nn.Sequential(
            # 第一层
            nn.Conv2D(in_channels=3, out_channels=96, kernel_size=11, stride=4, padding=0),
            nn.ReLU(),
            nn.MaxPool2D(kernel_size=3, stride=2),
            # 第二层
            nn.Conv2D(in_channels=96, out_channels=256, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.MaxPool2D(kernel_size=3, stride=2),
            # 第三层
            nn.Conv2D(in_channels=256, out_channels=384, kernel_size=3, padding=1),
            nn.ReLU(),
            # 第四层
            nn.Conv2D(in_channels=384, out_channels=384, kernel_size=3, padding=1),
            nn.ReLU(),
            # 第五层
            nn.Conv2D(in_channels=384, out_channels=256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2D(kernel_size=3, stride=2),
        )
        if num_classes > 0:
            self.classifier = nn.Sequential(
                nn.Linear(in_features=256 * 6 * 6, out_features=4096),
                nn.Dropout(),
                nn.Linear(in_features=4096, out_features=4096),
                nn.Dropout(),
                nn.Linear(in_features=4096, out_features=num_classes),
            )

    def forward(self, x):
        x = self.features(x)
        if self.num_classes > 0:
            x = paddle.flatten(x, 1)
            x = self.classifier(x)
        return x


alex_net = AlexNetPaddle()
paddle.summary(alex_net, (1, 3, 227, 227))
