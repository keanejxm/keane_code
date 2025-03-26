#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_03.py
:time  2025/3/26 9:05
:desc  
"""
# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_01.py
:time  2025/1/26 13:54
:desc  水果分类模型训练与评估
"""
import os
import cv2
import paddle
import numpy as np
from paddle.io import Dataset
from paddle import nn
from paddle.vision.transforms import Compose, Resize, ToTensor
from paddle.optimizer import Adam
from paddle.metric import Accuracy
from tqdm import tqdm


class FruitConfig:
    """配置参数类"""
    # 类别映射
    CLASS_MAPPING = {
        "apple": 0,
        "banana": 1,
        "grape": 2,
        "orange": 3,
        "pear": 4,
    }

    # 路径配置
    BASE_DIR = os.path.dirname(__file__)
    DATA_DIR = os.path.join(BASE_DIR, "fruits_classify", "fruits")
    MODEL_DIR = os.path.join(BASE_DIR, "saved_models")
    TRAIN_TXT = os.path.join(BASE_DIR, "train_fruit_label.txt")
    TEST_TXT = os.path.join(BASE_DIR, "test_fruit_label.txt")

    # 训练参数
    IMG_SIZE = (227, 227)  # AlexNet输入尺寸
    BATCH_SIZE = 32
    TEST_BATCH_SIZE = 32
    EPOCHS = 10
    LEARNING_RATE = 0.001
    VALID_FREQ = 1  # 验证频率


class FruitDataset(Dataset):
    """改进的水果数据集类"""

    def __init__(self, mode="train", transform=None):
        """
        初始化数据集
        Args:
            mode: 数据集模式 ("train"或"test")
            transform: 数据预处理变换
        """
        super().__init__()
        self.transform = transform
        self.data = self._load_data(mode)

    def _load_data(self, mode):
        """加载数据路径和标签"""
        file_path = FruitConfig.TRAIN_TXT if mode == "train" else FruitConfig.TEST_TXT
        data = []

        with open(file_path, "r") as f:
            for line in f:
                img_path, label = line.strip().split("\t")
                data.append((img_path, int(label)))
        return data

    def __getitem__(self, idx):
        """获取单个样本"""
        img_path, label = self.data[idx]

        # 读取图像并确保RGB格式
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        if self.transform:
            img = self.transform(img)

        return img, np.array(label, dtype="int64")

    def __len__(self):
        return len(self.data)


class ImprovedAlexNet(nn.Layer):
    """改进的AlexNet模型"""

    def __init__(self, num_classes=len(FruitConfig.CLASS_MAPPING)):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2D(3, 96, kernel_size=11, stride=4, padding=2),
            nn.ReLU(),
            nn.MaxPool2D(kernel_size=3, stride=2),
            nn.Conv2D(96, 256, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.MaxPool2D(kernel_size=3, stride=2),
            nn.Conv2D(256, 384, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2D(384, 384, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2D(384, 256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2D(kernel_size=3, stride=2),
        )
        self.classifier = nn.Sequential(
            nn.Dropout(p=0.5),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(),
            nn.Dropout(p=0.5),
            nn.Linear(4096, 4096),
            nn.ReLU(),
            nn.Linear(4096, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = paddle.flatten(x, 1)
        x = self.classifier(x)
        return x


def create_data_loaders():
    """创建训练和测试数据加载器"""
    transform = Compose([
        Resize(FruitConfig.IMG_SIZE),
        ToTensor(),
    ])

    train_dataset = FruitDataset(mode="train", transform=transform)
    test_dataset = FruitDataset(mode="test", transform=transform)

    train_loader = paddle.io.DataLoader(
        train_dataset,
        batch_size=FruitConfig.BATCH_SIZE,
        shuffle=True,
        num_workers=4,
        drop_last=True
    )

    test_loader = paddle.io.DataLoader(
        test_dataset,
        batch_size=FruitConfig.TEST_BATCH_SIZE,
        shuffle=False,
        num_workers=4
    )

    return train_loader, test_loader


def train_and_evaluate():
    """训练和评估模型"""
    # 准备数据
    train_loader, test_loader = create_data_loaders()

    # 初始化模型
    model = ImprovedAlexNet()
    optimizer = Adam(
        learning_rate=FruitConfig.LEARNING_RATE,
        parameters=model.parameters()
    )
    criterion = nn.CrossEntropyLoss()
    metric = Accuracy()

    # 创建模型保存目录
    os.makedirs(FruitConfig.MODEL_DIR, exist_ok=True)

    best_accuracy = 0.0
    for epoch in range(FruitConfig.EPOCHS):
        # 训练阶段
        model.train()
        train_loss = 0.0
        train_bar = tqdm(train_loader, desc=f"Train Epoch {epoch + 1}/{FruitConfig.EPOCHS}")

        for batch_idx, (data, target) in enumerate(train_bar):
            # 前向传播
            output = model(data)
            loss = criterion(output, target)

            # 反向传播
            loss.backward()
            optimizer.step()
            optimizer.clear_grad()

            train_loss += loss.numpy()[0]
            train_bar.set_postfix({"loss": f"{loss.numpy()[0]:.4f}"})

        # 验证阶段
        if (epoch + 1) % FruitConfig.VALID_FREQ == 0:
            model.eval()
            val_loss = 0.0
            metric.reset()

            with paddle.no_grad():
                val_bar = tqdm(test_loader, desc="Validating")
                for data, target in val_bar:
                    output = model(data)
                    val_loss += criterion(output, target).numpy()[0]
                    correct = metric.compute(output, target)
                    metric.update(correct)
                    val_bar.set_postfix({"val_loss": f"{val_loss / (batch_idx + 1):.4f}"})

            val_accuracy = metric.accumulate()
            avg_val_loss = val_loss / len(test_loader)

            print(f"\nValidation - Loss: {avg_val_loss:.4f}, Accuracy: {val_accuracy:.4f}")

            # 保存最佳模型
            if val_accuracy > best_accuracy:
                best_accuracy = val_accuracy
                model_save_path = os.path.join(FruitConfig.MODEL_DIR, "best_model")
                paddle.jit.save(
                    model,
                    path=model_save_path,
                    input_spec=[paddle.static.InputSpec(shape=[None, 3, *FruitConfig.IMG_SIZE], dtype="float32")]
                )
                print(f"Saved best model with accuracy: {val_accuracy:.4f} to {model_save_path}")


if __name__ == "__main__":
    train_and_evaluate()