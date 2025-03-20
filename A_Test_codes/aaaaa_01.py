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
with open("fruits_label","r") as f:
    for file_info in  f.readlines():
        filepath,label = file_info.split("\t")
        img = cv2.imread(filepath)
        print(img.shape)
class MyDataset(Dataset):
    def __init__(self,mode="train"):
        super(MyDataset, self).__init__()
        if mode == "train":
            self.data =[

            ]
        else:
            self.data = [

            ]
    def __getitem__(self, index):
        data= self.data[index][0]

        label = self.data[index][1]

        return data, label

    def __len__(self):
        return len(self.data)