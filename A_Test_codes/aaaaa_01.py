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
from paddle.io import Dataset

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
#                 f.write(f"{test_path}\t{fruit_map[fruit_file_name]}\n")
#         else:
#             train_path = os.path.join(path_py, "train_fruit_label.txt")
#             with open(train_path, 'a+') as f:
#                 f.write(f"{train_path}\t{fruit_map[fruit_file_name]}\n")
#         i += 1


class MyDataset(Dataset):
    def __init__(self, mode="train"):
        super(MyDataset, self).__init__()
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
                data.append([image_path, label.strip()])
        return data

    def __getitem__(self, index):
        data = self.data[index][0]

        label = self.data[index][1]

        return data, label

    def __len__(self):
        return len(self.data)


my_dataset = MyDataset("train")
print(my_dataset)