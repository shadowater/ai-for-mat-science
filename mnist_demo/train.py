import argparse
import sys
import time
from pathlib import Path

import torch
from torch import nn

from data import get_loaders
from model import CNN, MLP

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"

seed = 42


def parse_args():
    parser = argparse.ArgumentParser(description="在 MNIST 上训练 MLP 或 CNN")
    parser.add_argument("--model", choices=["mlp", "cnn"], default="mlp")
    parser.add_argument("--hidden", type=int, default=128, help="MLP 隐藏层宽度")
    parser.add_argument("--epochs", type=int, default=1)
    return parser.parse_args()


def build_model(name, hidden):
    return MLP(hidden=hidden) if name == "mlp" else CNN()


def output_path_for(args):
    if args.model == "cnn":
        return OUTPUT_DIR / "model_cnn.pt"
    if args.hidden == 128:
        return OUTPUT_DIR / "model.pt"
    return OUTPUT_DIR / f"model_h{args.hidden}.pt"


def evaluate(model, loader):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in loader:
            preds = model(images).argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
    return correct / total, correct, total


def main():
    args = parse_args()
    torch.manual_seed(seed)

    train_loader, test_loader = get_loaders(batch_size=64)

    model = build_model(args.model, args.hidden)
    total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    print(f"模型: {args.model}" + (f" (hidden={args.hidden})" if args.model == "mlp" else ""))
    print(f"可训练参数总数: {total_params}")

    start = time.perf_counter()
    epoch_times = []
    for epoch in range(1, args.epochs + 1):
        epoch_start = time.perf_counter()
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for batch_idx, (images, labels) in enumerate(train_loader, start=1):
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            preds = outputs.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

            if batch_idx % 100 == 0:
                print(f"epoch {epoch} batch {batch_idx}/{len(train_loader)}  "
                      f"平均 loss: {running_loss / 100:.4f}")
                running_loss = 0.0

        epoch_elapsed = time.perf_counter() - epoch_start
        epoch_times.append(epoch_elapsed)
        print(f"第 {epoch} 轮训练准确率: {correct / total:.4f} ({correct}/{total})  "
              f"本轮耗时: {epoch_elapsed:.2f} 秒")

    test_acc, test_correct, test_total = evaluate(model, test_loader)
    print(f"测试准确率: {test_acc:.4f} ({test_correct}/{test_total})")

    elapsed = time.perf_counter() - start

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = output_path_for(args)
    torch.save(model.state_dict(), output_path)

    print(f"平均每轮耗时: {sum(epoch_times) / len(epoch_times):.2f} 秒")
    print(f"模型已保存: {output_path}")
    print(f"总耗时: {elapsed:.2f} 秒")


if __name__ == "__main__":
    main()
