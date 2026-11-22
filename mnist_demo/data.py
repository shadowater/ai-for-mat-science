import sys
from pathlib import Path

import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DATA_DIR = Path(__file__).resolve().parent / "data"

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,)),
])


def get_loaders(batch_size=64):
    train_dataset = datasets.MNIST(
        root=DATA_DIR, train=True, download=True, transform=transform
    )
    test_dataset = datasets.MNIST(
        root=DATA_DIR, train=False, download=True, transform=transform
    )

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    return train_loader, test_loader


if __name__ == "__main__":
    train_loader, test_loader = get_loaders()

    print(f"训练集数量: {len(train_loader.dataset)}")
    print(f"测试集数量: {len(test_loader.dataset)}")

    images, labels = next(iter(train_loader))
    print(f"images.shape: {tuple(images.shape)}")
    print(f"images.dtype: {images.dtype}")
    print(f"labels.shape: {tuple(labels.shape)}")
    print(f"labels.dtype: {labels.dtype}")
    print(f"像素最小值: {images.min().item():.4f}")
    print(f"像素最大值: {images.max().item():.4f}")
