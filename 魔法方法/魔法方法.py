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
from paddle.io import DataLoader, Dataset
from paddle.vision.transforms import Compose, Normalize


class MyDataset(Dataset):
    def __init__(self, data_dir, label_path, transform=None):
        super(MyDataset, self).__init__()
        self.data_list = []
        with open(label_path, 'r') as f:
            for line in f.readlines():
                image_path, label = line.strip().split("\t")
                image_path = os.path.join(data_dir, image_path)
                self.data_list.append([image_path, label])
        self.transform = transform

    def __getitem__(self, index):
        image_path, label = self.data_list[index]
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        img = img.astype(np.float32)
        if self.transform is not None:
            img = self.transform(img)
        label = int(label)
        return img, label

    def __len__(self):
        return len(self.data_list)

transform = Normalize(mean=[127.5], std=[127.5],data_format='CHW')
train_dataset = MyDataset(r'E:\keane_data\mnist\train',r"E:\keane_data\mnist\train\label.txt", transform=transform)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
for batch_id,data in enumerate(train_loader()):
    images, labels = data
    print("batch_id: {}, 训练数据shape: {}, 标签数据shape: {}".format(batch_id, images.shape, labels.shape))
    break

