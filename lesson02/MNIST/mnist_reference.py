# -*- coding: utf-8 -*-
"""
MNIST 手写数字识别：课堂参考实现

用法：
    python mnist_reference.py --model mlp --epochs 1
    python mnist_reference.py --model cnn --epochs 3

这是教师备用脚本。课堂上让学生用 Agent 分步生成并运行，
每一步的提示词见 课堂提示词.md。

只依赖 torch 和 torchvision；matplotlib 可选，用于保存样张和错例图。
"""

import argparse
import json
import random
import time
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

HERE = Path(__file__).resolve().parent


class MLP(nn.Module):
    """784 -> 128 -> 10 的全连接网络。"""

    def __init__(self, hidden=128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Flatten(),
            nn.Linear(28 * 28, hidden),
            nn.ReLU(),
            nn.Linear(hidden, 10),
        )

    def forward(self, x):
        return self.net(x)


class CNN(nn.Module):
    """两个卷积块 + 一个全连接输出层。"""

    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 7 * 7, 10),
        )

    def forward(self, x):
        return self.classifier(self.features(x))


def set_seed(seed):
    random.seed(seed)
    torch.manual_seed(seed)


def build_loaders(data_dir, batch_size):
    # MNIST 的全局均值和标准差，用训练集统计得到
    tf = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,)),
    ])
    train_set = datasets.MNIST(data_dir, train=True, download=True, transform=tf)
    test_set = datasets.MNIST(data_dir, train=False, download=True, transform=tf)
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_set, batch_size=256, shuffle=False)
    return train_set, test_set, train_loader, test_loader


def run_epoch(model, loader, criterion, optimizer=None):
    """训练或评估一轮。optimizer 为 None 时只评估。"""
    training = optimizer is not None
    model.train(training)
    total_loss = 0.0
    correct = 0
    total = 0

    with torch.set_grad_enabled(training):
        for images, labels in loader:
            logits = model(images)
            loss = criterion(logits, labels)
            if training:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            total_loss += loss.item() * labels.size(0)
            correct += (logits.argmax(dim=1) == labels).sum().item()
            total += labels.size(0)

    return total_loss / total, correct / total


def confusion_matrix(model, loader):
    model.eval()
    cm = torch.zeros(10, 10, dtype=torch.int64)
    with torch.no_grad():
        for images, labels in loader:
            preds = model(images).argmax(dim=1)
            for t, p in zip(labels.tolist(), preds.tolist()):
                cm[t, p] += 1
    return cm


def save_examples(model, loader, out_dir, max_items=12):
    """保存样张和错例图；没有 matplotlib 时跳过。"""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        print("（未安装 matplotlib，跳过图片保存）")
        return None

    # 扫描整个测试集，收集错例；第一批可能全对
    all_images, all_labels, all_preds = [], [], []
    model.eval()
    with torch.no_grad():
        for images, labels in loader:
            all_images.append(images)
            all_labels.append(labels)
            all_preds.append(model(images).argmax(dim=1))
    images = torch.cat(all_images)
    labels = torch.cat(all_labels)
    preds = torch.cat(all_preds)

    # 样张：前 8 张
    fig, axes = plt.subplots(2, 4, figsize=(8, 4))
    for ax, image, label in zip(axes.flat, images[:8], labels[:8]):
        ax.imshow(image.squeeze(), cmap="gray")
        ax.set_title(f"label={label.item()}")
        ax.axis("off")
    fig.tight_layout()
    samples_path = out_dir / "samples.png"
    fig.savefig(samples_path, dpi=120)
    plt.close(fig)

    # 错例：最多 12 张
    wrong = (preds != labels).nonzero(as_tuple=True)[0][:max_items]
    if len(wrong) == 0:
        return samples_path
    fig, axes = plt.subplots(3, 4, figsize=(8, 6))
    for ax in axes.flat:
        ax.axis("off")
    for ax, idx in zip(axes.flat, wrong):
        ax.imshow(images[idx].squeeze(), cmap="gray")
        ax.set_title(f"true={labels[idx].item()} pred={preds[idx].item()}")
        ax.axis("off")
    fig.tight_layout()
    wrong_path = out_dir / "misclassified.png"
    fig.savefig(wrong_path, dpi=120)
    plt.close(fig)
    return samples_path, wrong_path


def main():
    parser = argparse.ArgumentParser(description="MNIST 手写数字识别课堂演示")
    parser.add_argument("--model", choices=["mlp", "cnn"], default="mlp")
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--hidden", type=int, default=128, help="MLP 隐藏单元数")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--data-dir", default=str(HERE / "data"))
    parser.add_argument("--out-dir", default=str(HERE / "outputs"))
    args = parser.parse_args()

    set_seed(args.seed)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("MNIST 手写数字识别")
    print(f"torch {torch.__version__} | CUDA {torch.cuda.is_available()} | 设备 CPU")
    print("=" * 60)

    train_set, test_set, train_loader, test_loader = build_loaders(
        args.data_dir, args.batch_size
    )
    print(f"训练集 {len(train_set)} 张，测试集 {len(test_set)} 张")
    print(f"每轮 {len(train_loader)} 个 batch（batch_size={args.batch_size}）")

    images, labels = next(iter(train_loader))
    print(f"一个 batch：images {tuple(images.shape)} {images.dtype}，"
          f"labels {tuple(labels.shape)} {labels.dtype}")
    print(f"像素范围（标准化后）：{images.min():.3f} 到 {images.max():.3f}")

    if args.model == "mlp":
        model = MLP(hidden=args.hidden)
    else:
        model = CNN()

    n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print()
    print(model)
    print(f"可训练参数：{n_params:,}")

    with torch.no_grad():
        dummy = torch.randn(2, 1, 28, 28)
        print(f"随机输入 {tuple(dummy.shape)} -> 输出 {tuple(model(dummy).shape)}")

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    history = []
    print()
    print("epoch | train_loss | train_acc | test_loss | test_acc | 秒")
    print("-" * 62)
    for epoch in range(1, args.epochs + 1):
        t0 = time.time()
        train_loss, train_acc = run_epoch(model, train_loader, criterion, optimizer)
        test_loss, test_acc = run_epoch(model, test_loader, criterion)
        seconds = time.time() - t0
        history.append({
            "epoch": epoch,
            "train_loss": train_loss,
            "train_acc": train_acc,
            "test_loss": test_loss,
            "test_acc": test_acc,
            "seconds": seconds,
        })
        print(f"{epoch:>5} | {train_loss:>10.4f} | {train_acc:>9.4f} | "
              f"{test_loss:>9.4f} | {test_acc:>8.4f} | {seconds:>5.1f}")

    cm = confusion_matrix(model, test_loader)
    print()
    print("测试集混淆矩阵（行=真实，列=预测）：")
    print("     " + "".join(f"{j:>6}" for j in range(10)))
    for i in range(10):
        print(f"{i:>3}  " + "".join(f"{int(v):>6}" for v in cm[i]))
    per_class = cm.diagonal() / cm.sum(dim=1).clamp(min=1)
    print()
    print("各类准确率：" + "  ".join(f"{i}:{v:.3f}" for i, v in enumerate(per_class)))

    paths = save_examples(model, test_loader, out_dir)
    torch.save(model.state_dict(), out_dir / "model.pt")
    with open(out_dir / "history.json", "w", encoding="utf-8") as f:
        json.dump({
            "model": args.model,
            "epochs": args.epochs,
            "batch_size": args.batch_size,
            "lr": args.lr,
            "hidden": args.hidden,
            "n_params": n_params,
            "history": history,
        }, f, ensure_ascii=False, indent=2)

    print()
    print(f"模型已保存：{out_dir / 'model.pt'}")
    if paths:
        for p in (paths if isinstance(paths, tuple) else (paths,)):
            print(f"图片已保存：{p}")
    print(f"训练记录：{out_dir / 'history.json'}")


if __name__ == "__main__":
    main()
