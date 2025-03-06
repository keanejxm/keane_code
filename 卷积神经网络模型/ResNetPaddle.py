#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_01.py
:time  2025/1/26 13:54
:desc  只搭建了ResNet50
"""
import paddle
from paddle import nn


# 残差结构
class BaseBlock(nn.Layer):
    def __init__(self, in_channel, out_channel, stride=1, downsample=None):
        super(BaseBlock, self).__init__()
        self.conv1 = nn.Conv2D(in_channel, out_channel, kernel_size=3, stride=stride, padding=1)
        self.bn1 = nn.BatchNorm2D(out_channel)
        self.conv2 = nn.Conv2D(out_channel, out_channel, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2D(out_channel)
        self.rule = nn.ReLU()
        self.downsample = downsample

    def forward(self, x):
        identity = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.rule(out)

        out = self.conv2(out)
        out = self.bn2(out)
        if self.downsample is not None:
            identity = self.downsample(x)
        return self.rule(identity + out)


class BottleneckBlock(nn.Layer):
    expansion = 4

    def __init__(self, in_channel, out_channel, stride=1, downsample=None):
        super(BottleneckBlock, self).__init__()
        self.conv1 = nn.Conv2D(in_channel, out_channel, kernel_size=1, stride=1)
        self.bn1 = nn.BatchNorm2D(out_channel)
        self.conv2 = nn.Conv2D(out_channel, out_channel, kernel_size=3, stride=stride, padding=1)
        self.bn2 = nn.BatchNorm2D(out_channel)
        self.conv3 = nn.Conv2D(out_channel, out_channel * self.expansion, kernel_size=1, stride=1)
        self.bn3 = nn.BatchNorm2D(out_channel * self.expansion)
        self.rule = nn.ReLU()
        self.downsample = downsample

    def forward(self, x):
        identity = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.rule(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.rule(out)

        out = self.conv3(out)
        out = self.bn3(out)
        if self.downsample is not None:
            identity = self.downsample(x)
        return self.rule(identity + out)


class ResNetPaddle(nn.Layer):
    def __init__(self, block, num_blocks, num_classes=1000):
        super(ResNetPaddle, self).__init__()
        self.in_channel = 64
        self.conv1 = nn.Conv2D(3, 64, kernel_size=7, stride=2, padding=3)
        self.bn1 = nn.BatchNorm2D(64)
        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool2D(kernel_size=3, stride=2, padding=1)
        self.layer1 = self._make_layer(block, 64, num_blocks[0])
        self.layer2 = self._make_layer(block, 128, num_blocks[1], stride=2)
        self.layer3 = self._make_layer(block, 256, num_blocks[2], stride=2)
        self.layer4 = self._make_layer(block, 512, num_blocks[3], stride=2)
        self.avgpool = nn.AdaptiveAvgPool2D(1)
        self.fc = nn.Linear(512 * block.expansion, num_classes)
        self.relu = nn.ReLU()

    def _make_layer(self, block, out_channel, num_blocks, stride=1):
        downsample = None
        if stride != 1 or self.in_channel != out_channel * block.expansion:
            downsample = nn.Sequential(
                nn.Conv2D(self.in_channel, out_channel * block.expansion, kernel_size=1, stride=stride),
                nn.BatchNorm2D(out_channel * block.expansion),
            )

        layers = []
        layers.append(block(self.in_channel, out_channel, stride, downsample))
        self.in_channel = out_channel * block.expansion
        for i in range(1, num_blocks):
            layers.append(block(self.in_channel, out_channel, stride=1))
        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = paddle.flatten(x, 1)
        x = self.fc(x)
        return x


res_net = ResNetPaddle(BottleneckBlock, [3, 4, 6, 3], num_classes=1000)

paddle.summary(res_net, (1, 3, 224, 224))
