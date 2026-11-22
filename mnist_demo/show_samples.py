import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # 只保存图片，不弹窗
import matplotlib.pyplot as plt
import numpy as np
from torchvision import datasets, transforms

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DATA_DIR = Path(__file__).resolve().parent / "data"
OUT_PATH = Path(__file__).resolve().parent / "samples.png"

to_tensor = transforms.ToTensor()
normalize = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,)),
])

raw_dataset = datasets.MNIST(root=DATA_DIR, train=True, download=True, transform=None)
tensor_dataset = datasets.MNIST(root=DATA_DIR, train=True, download=True, transform=to_tensor)
norm_dataset = datasets.MNIST(root=DATA_DIR, train=True, download=True, transform=normalize)

n = 8
fig, axes = plt.subplots(2, 4, figsize=(10, 5))
for i, ax in enumerate(axes.flat):
    image, label = tensor_dataset[i]
    ax.imshow(image.squeeze(0), cmap="gray")
    ax.set_title(f"label: {label}")
    ax.axis("off")

fig.tight_layout()
fig.savefig(OUT_PATH, dpi=150)
plt.close(fig)

pil_image, _ = raw_dataset[0]
tensor_image, _ = tensor_dataset[0]
norm_image, _ = norm_dataset[0]
pil_pixels = np.array(pil_image, dtype=np.uint8)

print(f"已保存: {OUT_PATH}")
print(f"单张图 tensor shape: {tuple(tensor_image.shape)}")
print(f"ToTensor 前 (PIL) shape: {pil_pixels.shape}, dtype: {pil_pixels.dtype}, "
      f"范围: [{pil_pixels.min()}, {pil_pixels.max()}]")
print(f"ToTensor 后 dtype: {tensor_image.dtype}, "
      f"范围: [{tensor_image.min().item():.4f}, {tensor_image.max().item():.4f}]")
print(f"Normalize 后 dtype: {norm_image.dtype}, "
      f"范围: [{norm_image.min().item():.4f}, {norm_image.max().item():.4f}]")
