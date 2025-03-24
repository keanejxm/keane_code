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
from PIL import Image
from paddle.io import Dataset
from paddle import nn
from paddle.vision.transforms import Compose, Resize, ToTensor
from paddle.vision.transforms import functional as F

fruit_map = {
    "apple": 1,
    "banana": 2,
    "grape": 3,
    "orange": 4,
    "pear": 5,
}
path_py = os.path.dirname(__file__)
dir_fruits_classify = os.path.join(path_py, "fruits_classify")
dir_fruits = os.path.join(dir_fruits_classify, "fruits")


# for fruit_file_name in os.listdir(dir_fruits):
#     file_name_path = os.path.join(dir_fruits, fruit_file_name)
#     i = 0
#     for image_name in os.listdir(file_name_path):
#         image_path = os.path.join(file_name_path, image_name)
#         if i % 10 == 0:
#             test_path = os.path.join(path_py, "test_fruit_label.txt")
#             with open(test_path, 'a+') as f:
#                 f.write(f"{image_path}\t{fruit_map[fruit_file_name]}\n")
#         else:
#             train_path = os.path.join(path_py, "train_fruit_label.txt")
#             with open(train_path, 'a+') as f:
#                 f.write(f"{image_path}\t{fruit_map[fruit_file_name]}\n")
#         i += 1


class MyDataset(Dataset):
    def __init__(self, mode="train", transform=None):
        super(MyDataset, self).__init__()
        self.transform = transform
        if mode == "train":
            self.data = self._fetch_data("train_fruit_label.txt")
        else:
            self.data = self._fetch_data("test_fruit_label.txt")

    @staticmethod
    def _fetch_data(file_path):
        data = list()
        with open(file_path, "r") as f:
            for line in f.readlines():
                image_path, label = line.split("\t")
                data.append([image_path, int(label.strip())])
        return data

    def __getitem__(self, index):
        image_path, label = self.data[index]
        image = cv2.imread(image_path)  # 转换为 RGB 格式
        if self.transform:
            image = self.transform(image)

        return image, label

    def __len__(self):
        return len(self.data)


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


def train(model, transform):
    model.train()
    # 批次
    epoch_num = 100
    train_num = 0
    # 优化器
    optimizer = paddle.optimizer.Adam(learning_rate=0.001, parameters=model.parameters())
    # 数据加载器
    train_loader = paddle.io.DataLoader(
        dataset=MyDataset(mode="train", transform=transform),
        batch_size=10,
        shuffle=True,
    )
    test_loader = paddle.io.DataLoader(
        dataset=MyDataset(mode="test", transform=transform),
        batch_size=2,
        shuffle=False,
    )
    for epoch_id in range(epoch_num):
        for batch_id, data in enumerate(train_loader):
            images = data[0]
            labels = paddle.to_tensor(data[1])
            labels = paddle.unsqueeze(labels, 1)
            logits = model(images)
            loss = paddle.nn.functional.cross_entropy(logits, labels)
            loss.backward()
            optimizer.step()
            optimizer.clear_grad()
            if batch_id % 10 ==0:
                print(f"epoch_id:{epoch_id}, batch_id:{batch_id}, loss:{loss.numpy()}")
        #测试集评估
        model.eval()
        accuracies = []
        losses = []
        for batch_id, data in enumerate(test_loader):
            images = data[0]
            labels = paddle.unsqueeze(data[1], 1)
            logits = model(images)
            loss = paddle.nn.functional.cross_entropy(logits, labels)
            acc = paddle.metric.accuracy(logits, labels)
            accuracies.append(acc.numpy())
            losses.append(loss.numpy())
            preds = paddle.argmax(logits, axis=1)
            # correct = (preds==labels).astype("float32").mean()
            # accuracies.append(correct.numpy())
        avg_accuracy = sum(accuracies) / len(accuracies)
        print(f"epoch_id:{epoch_id}, avg_accuracy:{avg_accuracy}")

    # 保存模型
    paddle.jit.save(model, path_py)
    print("model saved")
    # 加载模型
    loaded_model = paddle.jit.load(path_py)


transformer = Compose([Resize((227, 227)), ToTensor()])
train(AlexNetPaddle(), transformer)