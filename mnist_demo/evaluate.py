import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch

from data import get_loaders
from model import MLP

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MODEL_PATH = Path(__file__).resolve().parent / "outputs" / "model.pt"
FIGURE_PATH = Path(__file__).resolve().parent / "misclassified.png"


def main():
    _, test_loader = get_loaders(batch_size=64)

    model = MLP()
    model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu", weights_only=True))
    model.eval()

    confusion = torch.zeros(10, 10, dtype=torch.int64)
    mis_images, mis_true, mis_pred = [], [], []

    with torch.no_grad():
        for images, labels in test_loader:
            preds = model(images).argmax(dim=1)
            for true, pred in zip(labels.tolist(), preds.tolist()):
                confusion[true, pred] += 1

            wrong = preds != labels
            for image, true, pred in zip(images[wrong], labels[wrong], preds[wrong]):
                if len(mis_images) >= 12:
                    break
                mis_images.append(image)
                mis_true.append(true.item())
                mis_pred.append(pred.item())

    total = confusion.sum().item()
    correct = confusion.diag().sum().item()
    print(f"总准确率: {correct / total:.4f} ({correct}/{total})")

    print("\n混淆矩阵（行=真实，列=预测）:")
    print("true\\pred" + "".join(f"{col:>6}" for col in range(10)))
    for row in range(10):
        counts = "".join(f"{confusion[row, col].item():>6}" for col in range(10))
        print(f"{row:>9}" + counts)

    print("\n每个数字的准确率:")
    for digit in range(10):
        row_total = confusion[digit].sum().item()
        row_correct = confusion[digit, digit].item()
        print(f"数字 {digit}: {row_correct / row_total:.4f} ({row_correct}/{row_total})")

    fig, axes = plt.subplots(3, 4, figsize=(10, 8))
    for ax, image, true, pred in zip(axes.flat, mis_images, mis_true, mis_pred):
        display = (image.squeeze(0) * 0.3081 + 0.1307).clamp(0, 1)
        ax.imshow(display, cmap="gray")
        ax.set_title(f"true: {true}, pred: {pred}")
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(FIGURE_PATH, dpi=150)
    plt.close(fig)

    print(f"\n错分样本图已保存: {FIGURE_PATH}")


if __name__ == "__main__":
    main()
