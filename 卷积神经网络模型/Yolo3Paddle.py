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


# YOLO3

# 定义卷积块
class ConvBlock(nn.Layer):
    def __init__(self, in_channel, out_channel, kernel_size, stride=1, padding=0):
        super(ConvBlock, self).__init__()
        self.conv = nn.Conv2D(in_channel, out_channel, kernel_size, stride=stride, padding=padding)
        self.bn = nn.BatchNorm(out_channel)
        self.LeakyReLU = nn.LeakyReLU()

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.LeakyReLU(x)
        return x


# 定义残差单元

class ResidualBlock(nn.Layer):
    def __init__(self, in_channel):
        super(ResidualBlock, self).__init__()
        self.conv1 = ConvBlock(in_channel, in_channel // 2, kernel_size=1)
        self.conv2 = ConvBlock(in_channel // 2, in_channel, kernel_size=3, padding=1)

    def forward(self, x):
        residual = x
        x = self.conv1(x)
        x = self.conv2(x)
        x = paddle.add(x, residual)
        return x


# darknet-53
class DarknetBlock(nn.Layer):
    def __init__(self):
        super(DarknetBlock, self).__init__()
        self.conv1 = ConvBlock(3, 32, kernel_size=3, padding=1)
        self.conv2 = ConvBlock(32, 64, kernel_size=3, stride=2, padding=1)
        self.residual_block1 = self._make_residual_block(64, 1)
        self.conv3 = ConvBlock(64, 128, kernel_size=3, stride=2, padding=1)
        self.residual_block2 = self._make_residual_block(128, 2)
        self.conv4 = ConvBlock(128, 256, kernel_size=3, stride=2, padding=1)
        self.residual_block3 = self._make_residual_block(256, 8)
        self.conv5 = ConvBlock(256, 512, kernel_size=3, stride=2, padding=1)
        self.residual_block4 = self._make_residual_block(512, 8)
        self.conv6 = ConvBlock(512, 1024, kernel_size=3, stride=2, padding=1)
        self.residual_block5 = self._make_residual_block(1024, 4)

    @staticmethod
    def _make_residual_block(in_channel, num_block):
        layers = []
        for i in range(num_block):
            layers.append(ResidualBlock(in_channel))
        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.residual_block1(x)
        x = self.conv3(x)
        x = self.residual_block2(x)
        x = self.conv4(x)
        out1 = self.residual_block3(x)
        x = self.conv5(out1)
        out2 = self.residual_block4(x)
        x = self.conv6(out2)
        out3 = self.residual_block5(x)
        return out1, out2, out3


class DetectionBlock(nn.Layer):
    def __init__(self, in_channel, out_channel):
        super(DetectionBlock, self).__init__()
        self.conv1 = ConvBlock(in_channel, out_channel, kernel_size=1, stride=1, padding=0)
        self.conv2 = ConvBlock(out_channel, out_channel * 2, kernel_size=3, stride=1, padding=1)
        self.conv3 = ConvBlock(out_channel * 2, out_channel, kernel_size=1, stride=1, padding=0)
        self.conv4 = ConvBlock(out_channel, out_channel * 2, kernel_size=3, stride=1, padding=1)
        self.conv5 = ConvBlock(out_channel * 2, out_channel, kernel_size=1, stride=1, padding=0)

        self.conv6 = ConvBlock(out_channel * 2, out_channel * 2, kernel_size=3, stride=1, padding=1)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        route = self.conv5(x)
        tip = self.conv6(route)
        return route, tip


class UpSample(nn.Layer):
    # "bilinear
    def __init__(self, scale_factor=2, mode='nearest'):
        super(UpSample, self).__init__()
        self.up_sample = nn.Upsample(scale_factor=scale_factor, mode=mode)

    def forward(self, x):
        return self.up_sample(x)


class Yolo3(nn.Layer):
    def __init__(self, in_channel, out_channel):
        super(Yolo3, self).__init__()
        self.darknet = DarknetBlock()
        self.detection = DetectionBlock(in_channel, out_channel)
        self.up_sample = UpSample()


    def forward(self, x):

        out1, out2, out3 = self.darknet(x)

