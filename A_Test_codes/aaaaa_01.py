#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa_01.py
:time  2025/1/26 13:54
:desc  
"""
import os
from pathlib import Path
import cv2
import numpy as np
import paddle
from PIL import Image
from paddle.io import Dataset, DataLoader
from paddle import nn
from paddle.vision.transforms import Compose, Resize, ToTensor
import yaml
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
import matplotlib.pyplot as plt


@dataclass
class ModelConfig:
    """模型配置类"""
    image_size: Tuple[int, int] = (227, 227)
    # 类别映射
    CLASS_MAPPING = {
        "apple": 0,
        "banana": 1,
        "grape": 2,
        "orange": 3,
        "pear": 4,
    }

    # 路径配置
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "fruits_classify" / "fruits"
    MODEL_DIR = BASE_DIR / "saved_models"
    TRAIN_DIR = BASE_DIR / "train_fruit_label.txt"
    TEST_DIR = BASE_DIR / "test_fruit_label.txt"

    # 训练参数
    IMG_SIZE: Tuple[int, int] = (227, 227)
    BATCH_SIZE: int = 32
    TEST_BATCH_SIZE: int = 32
    EPOCHS: int = 10
    LEARNING_RATE: float = 0.001
    VALID_FREQ: int = 1
    EVAL_STEPS: int = 10
    SAVE_STEPS: int = 50



class FruitClassifier:
    """水果分类器主类"""

    def __init__(self):
        self.setup_paths()

    @staticmethod
    def setup_paths() -> None:
        """设置必要的路径"""

        # 创建必要的目录
        for path in [ModelConfig.MODEL_DIR, ModelConfig.DATA_DIR]:
            path.mkdir(exist_ok=True)

    @staticmethod
    def prepare_dataset(self) -> None:
        """准备训练和测试数据集"""
        train_file = ModelConfig.BASE_DIR / "train_fruit_label.txt"
        test_file = ModelConfig.BASE_DIR / "test_fruit_label.txt"

        if train_file.exists() and test_file.exists():
            return

        for fruit_path in ModelConfig.DATA_DIR.glob("*"):
            if not fruit_path.is_dir():
                continue

            fruit_name = fruit_path.name
            for i, image_path in enumerate(fruit_path.glob("*")):
                label = ModelConfig.CLASS_MAPPING[fruit_name]
                target_file = test_file if i % 10 == 0 else train_file

                with open(target_file, 'a') as f:
                    f.write(f"{image_path}\t{label}\n")


class FruitDataset(Dataset):
    """水果数据集类"""

    def __init__(self, mode: str = "train", transform: Optional[Compose] = None):
        super(FruitDataset, self).__init__()
        self.transform = transform
        self.data = self._load_data(f"{mode}_fruit_label.txt")

    def _load_data(self, file_path: str) -> List[Tuple[str, int]]:
        """加载数据集"""
        data = []
        with open(file_path, "r") as f:
            for line in f.readlines():
                image_path, label = line.strip().split("\t")
                data.append((image_path, int(label)))
        return data

    def __getitem__(self, index: int) -> Tuple[paddle.Tensor, int]:
        """获取单个样本"""
        image_path, label = self.data[index]
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if self.transform:
            image = self.transform(image)

        return image, label

    def __len__(self) -> int:
        return len(self.data)


class AlexNet(nn.Layer):
    """改进的AlexNet模型"""

    def __init__(self, num_classes: int = 1000):
        super(AlexNet, self).__init__()
        self.features = self._make_features()
        self.classifier = self._make_classifier(num_classes)

    @staticmethod
    def _make_features() -> nn.Sequential:
        """构建特征提取层"""
        return nn.Sequential(
            nn.Conv2D(3, 96, 11, 4), nn.ReLU(),
            nn.MaxPool2D(3, 2),
            nn.Conv2D(96, 256, 5, padding=2), nn.ReLU(),
            nn.MaxPool2D(3, 2),
            nn.Conv2D(256, 384, 3, padding=1), nn.ReLU(),
            nn.Conv2D(384, 384, 3, padding=1), nn.ReLU(),
            nn.Conv2D(384, 256, 3, padding=1), nn.ReLU(),
            nn.MaxPool2D(3, 2)
        )

    @staticmethod
    def _make_classifier(num_classes: int) -> nn.Sequential:
        """构建分类器层"""
        return nn.Sequential(
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(4096, 4096),
            nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(4096, num_classes)
        )

    def forward(self, x: paddle.Tensor) -> paddle.Tensor:
        x = self.features(x)
        x = paddle.flatten(x, 1)
        x = self.classifier(x)
        return x


class Trainer:
    """训练器类"""

    def __init__(self, model: nn.Layer):
        self.model = model
        self.setup_training()

    def setup_training(self) -> None:
        """设置训练相关组件"""
        self.optimizer = paddle.optimizer.Adam(
            learning_rate=ModelConfig.LEARNING_RATE,
            parameters=self.model.parameters()
        )
        self.transform = Compose([
            Resize(ModelConfig.IMG_SIZE),
            ToTensor()
        ])

    def create_data_loaders(self):
        """创建训练和测试数据加载器"""
        train_dataset = FruitDataset(mode="train", transform=self.transform)
        test_dataset = FruitDataset(mode="test", transform=self.transform)

        train_loader = DataLoader(
            train_dataset,
            batch_size=ModelConfig.BATCH_SIZE,
            shuffle=True
        )

        test_loader = DataLoader(
            test_dataset,
            batch_size=ModelConfig.TEST_BATCH_SIZE,
            shuffle=True
        )

        return train_loader, test_loader

    def train(self) -> None:
        """训练模型"""
        train_loader, test_loader = self.create_data_loaders()

        # 初始化模型
        criterion = paddle.nn.CrossEntropyLoss()
        metric = paddle.metric.Accuracy()

        best_accuracy = 0.0
        for epoch in range(ModelConfig.EPOCHS):
            # 训练阶段
            self.model.train()
            train_loss = 0.0



            for batch_idx, (data, labels) in enumerate(train_loader):
                labels = paddle.unsqueeze(labels, 1)
                output = self.model(data)
                loss = criterion(output, labels)

                loss.backward()
                self.optimizer.step()
                self.optimizer.clear_grad()

                train_loss += loss.numpy()[0]

                if batch_idx % ModelConfig.EVAL_STEPS == 0:
                    print(f"Epoch: {epoch}, Batch: {batch_idx}, Loss: {loss.numpy()}")

                if batch_idx % ModelConfig.SAVE_STEPS == 0:
                    self.evaluate(test_loader,criterion, metric,best_accuracy)
                    self.save_model(f"model_epoch_{epoch}_batch_{batch_idx}")

    def evaluate(self,test_loader,criterion,metric,best_accuracy) -> float:
        """评估模型"""
        self.model.eval()
        val_loss = 0.0
        metric.reset()

        accuracies = []
        with paddle.no_grad():
            for data, target in test_loader:
                target = paddle.unsqueeze(target, 1)
                output = self.model(data)
                val_loss += criterion(output, target).numpy()[0]
                correct = metric.accuracy(output, target)
                metric.update(correct)
                # accuracies.append(acc.numpy())

        val_accuracy = metric.accumulate()
        avg_val_loss = val_loss / len(test_loader.dataset)
        print(f"\nValidation - Loss: {avg_val_loss:.4f}, Accuracy: {val_accuracy:.4f}")

        # 保存最佳模型
        if val_accuracy > best_accuracy:
            best_accuracy = val_accuracy
            paddle.jit.save(
                self.model,
                path = ModelConfig.MODEL_DIR,
                input_spec=[paddle.static.InputSpec(shape=[None, 3, 224, 224], dtype='float32')],
            )
        avg_accuracy = np.mean(accuracies)
        print(f"Validation Accuracy: {avg_accuracy:.4f}")
        return avg_accuracy

    def save_model(self, name: str) -> None:
        """保存模型"""
        save_path = Path("models") / name
        paddle.jit.save(self.model, str(save_path))
        print(f"Model saved to {save_path}")


class Predictor:
    """图片预测器类"""

    def __init__(self, model_path: Union[str, Path], config: ModelConfig):
        self.config = config
        self.model = self._load_model(model_path)
        self.transform = Compose([
            Resize(config.image_size),
            ToTensor()
        ])
        # 反转类别映射字典，用于获取类别名称
        self.label_map = {v: k for k, v in FruitClassifier.fruit_map.items()}

    def _load_model(self, model_path: Union[str, Path]) -> paddle.jit.TranslatedLayer:
        """加载训练好的模型"""
        try:
            model = paddle.jit.load(str(model_path))
            model.eval()
            return model
        except Exception as e:
            raise RuntimeError(f"模型加载失败: {str(e)}")

    def preprocess_image(self, image_path: Union[str, Path, np.ndarray]) -> paddle.Tensor:
        """预处理图片"""
        if isinstance(image_path, (str, Path)):
            image = cv2.imread(str(image_path))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image = image_path

        if image is None:
            raise ValueError("无法读取图片")

        return self.transform(image)

    def predict_single(self, image_path: Union[str, Path, np.ndarray]) -> Tuple[str, float]:
        """预测单张图片"""
        # 预处理图片
        image = self.preprocess_image(image_path)
        image = paddle.unsqueeze(image, axis=0)  # 添加批次维度

        # 执行预测
        with paddle.no_grad():
            logits = self.model(image)
            probs = paddle.nn.functional.softmax(logits, axis=1)

        # 获取预测结果
        pred_label = paddle.argmax(probs, axis=1).numpy()[0]
        confidence = float(probs.numpy()[0][pred_label])

        # 获取类别名称
        class_name = self.label_map.get(pred_label, "unknown")

        return class_name, confidence

    def predict_batch(self, image_paths: List[Union[str, Path]]) -> List[Tuple[str, float]]:
        """批量预测图片"""
        results = []
        for image_path in image_paths:
            try:
                result = self.predict_single(image_path)
                results.append(result)
            except Exception as e:
                print(f"处理图片 {image_path} 时出错: {str(e)}")
                results.append(("error", 0.0))
        return results

    def visualize_prediction(self, image_path: Union[str, Path],
                             save_path: Optional[Union[str, Path]] = None) -> None:
        """可视化预测结果"""
        # 读取原始图片
        image = cv2.imread(str(image_path))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 获取预测结果
        class_name, confidence = self.predict_single(image_path)

        # 创建图形
        plt.figure(figsize=(10, 6))
        plt.imshow(image)
        plt.title(f'预测类别: {class_name}\n置信度: {confidence:.2%}')
        plt.axis('off')

        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()


def main():
    """主函数"""
    # 训练部分
    config = ModelConfig()
    classifier = FruitClassifier(config)
    classifier.prepare_dataset()

    model = AlexNet(num_classes=config.num_classes)
    trainer = Trainer(model, config)
    trainer.train()

    # 预测部分
    predictor = Predictor("models/best_model", config)

    # 单张图片预测示例
    image_path = "test_image.jpg"
    class_name, confidence = predictor.predict_single(image_path)
    print(f"预测类别: {class_name}, 置信度: {confidence:.2%}")

    # 可视化预测结果
    predictor.visualize_prediction(image_path, save_path="prediction_result.png")

    # 批量预测示例
    test_images = ["test1.jpg", "test2.jpg", "test3.jpg"]
    results = predictor.predict_batch(test_images)
    for image_path, (class_name, confidence) in zip(test_images, results):
        print(f"{image_path}: 类别 - {class_name}, 置信度 - {confidence:.2%}")


# 使用示例
if __name__ == '__main__':
    # 创建预测器实例
    config = ModelConfig()
    predictor = Predictor("path/to/your/model", config)

    # 预测单张图片
    image_path = "test_image.jpg"
    class_name, confidence = predictor.predict_single(image_path)
    print(f"预测结果: {class_name} (置信度: {confidence:.2%})")

    # 可视化预测结果
    predictor.visualize_prediction(image_path)

    # 批量预测
    test_images = ["test1.jpg", "test2.jpg", "test3.jpg"]
    results = predictor.predict_batch(test_images)
    for image_path, (class_name, confidence) in zip(test_images, results):
        print(f"{image_path}: {class_name} ({confidence:.2%})")
