# -*- coding: utf-8 -*-
"""
生成《计算机视觉先导》所需图片。

运行：python lesson02/Vision/scripts/make_assets.py
依赖：Pillow、numpy、matplotlib；MNIST 图片读取用标准库。
"""

import gzip
import io
import json
import struct
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle
from PIL import Image

HERE = Path(__file__).resolve().parent      # lesson02/Vision/scripts
VISION = HERE.parent                        # lesson02/Vision
LESSON02 = VISION.parent                    # lesson02
ROOT = LESSON02.parent                      # 课程根目录
ASSETS = VISION / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def save(fig, name, dpi=150):
    path = ASSETS / name
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", path)


def center_square(im):
    w, h = im.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    return im.crop((left, top, left + side, top + side))


# ---------------------------------------------------------------- 1. 矢量 vs 位图
def make_vector_vs_raster():
    def render(size):
        dpi = 100
        scale = size / 600.0
        fig = plt.figure(figsize=(size / dpi, size / dpi), dpi=dpi)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.add_patch(Circle((0.5, 0.5), 0.36, fill=False,
                            edgecolor="#1e5ac8", linewidth=12 * scale))
        t = np.linspace(0, 1, 400)
        x = 0.2 + 0.6 * t
        y = 0.5 + 0.25 * np.sin(2 * np.pi * t)
        ax.plot(x, y, color="#c82828", linewidth=8 * scale,
                solid_capstyle="round")
        ax.text(0.5, 0.5, "CV", ha="center", va="center",
                fontsize=max(5, 80 * scale), fontweight="bold", color="#141414")
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=dpi, facecolor="white")
        plt.close(fig)
        buf.seek(0)
        return Image.open(buf).convert("RGB")

    hi = render(600)
    lo = render(45).resize((600, 600), Image.Resampling.NEAREST)

    fig, axes = plt.subplots(1, 2, figsize=(9, 4.6))
    for ax, im, title in zip(
        axes, [hi, lo],
        ["矢量：按指令重新计算，放大仍清晰", "位图：记录每个像素，放大看到方块"],
    ):
        ax.imshow(im)
        ax.set_title(title, fontsize=12)
        ax.axis("off")
    fig.suptitle("同一个图形的两种存法", fontsize=14)
    save(fig, "vector_vs_raster.png")


def make_vector_svg():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 600 600">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#1e5ac8"/>
      <stop offset="1" stop-color="#7bb0ff"/>
    </linearGradient>
  </defs>
  <rect width="600" height="600" fill="white"/>
  <circle cx="300" cy="300" r="220" fill="none" stroke="url(#g)" stroke-width="16"/>
  <path d="M120 300 C 210 120, 390 480, 480 300" fill="none" stroke="#c82828" stroke-width="10"/>
  <text x="300" y="315" font-family="Arial, sans-serif" font-size="120" font-weight="bold"
        text-anchor="middle" fill="#141414">CV</text>
</svg>
"""
    path = ASSETS / "vector_demo.svg"
    path.write_text(svg, encoding="utf-8")
    print("saved", path)


# ---------------------------------------------------------------- 2. 像素网格
def make_pixel_grid():
    pattern = np.array([
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]) * 255

    fig, ax = plt.subplots(figsize=(7, 7))
    for r in range(8):
        for c in range(8):
            v = int(pattern[r, c])
            color = "#ffffff" if v == 0 else "#111111"
            ax.add_patch(Rectangle((c, 7 - r), 1, 1, facecolor=color, edgecolor="#999999", linewidth=0.8))
            ax.text(c + 0.5, 7 - r + 0.5, f"0x{v:02X}", ha="center", va="center",
                    color="#777777" if v == 0 else "white", fontsize=9, family="DejaVu Sans")
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    ax.set_aspect("equal")
    ax.set_xticks(np.arange(0.5, 8, 1))
    ax.set_yticks(np.arange(0.5, 8, 1))
    ax.set_xticklabels(range(8))
    ax.set_yticklabels(list(range(7, -1, -1)))
    ax.set_xlabel("列")
    ax.set_ylabel("行")
    ax.set_title("灰度图：一格 = 一个像素 = 一个字节（0x00–0xFF）", fontsize=12)
    save(fig, "pixel_grid.png")


# ---------------------------------------------------------------- 3. RGB / CMYK / 灰度
def make_color_channels():
    im = center_square(Image.open(ASSETS / "chelsea.png").convert("RGB")).resize((300, 300))
    arr = np.asarray(im).astype(np.float32) / 255.0

    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    gray = 0.299 * r + 0.587 * g + 0.114 * b

    k = 1.0 - np.max(arr, axis=2)
    denom = np.clip(1.0 - k, 1e-6, None)
    c = (1.0 - r - k) / denom
    m = (1.0 - g - k) / denom
    y = (1.0 - b - k) / denom

    panels = [
        ("原图 RGB", arr),
        ("R 通道", r),
        ("G 通道", g),
        ("B 通道", b),
        ("灰度（亮度）", gray),
        ("C 通道（青）", c),
        ("M 通道（品红）", m),
        ("Y 通道（黄）", y),
        ("K 通道（黑）", k),
    ]

    fig, axes = plt.subplots(3, 3, figsize=(10, 10))
    for ax, (title, data) in zip(axes.flat, panels):
        if data.ndim == 3:
            ax.imshow(np.clip(data, 0, 1))
        else:
            ax.imshow(np.clip(data, 0, 1), cmap="gray", vmin=0, vmax=1)
        ax.set_title(title, fontsize=11)
        ax.axis("off")
    fig.suptitle("RGB、灰度与 CMYK：同一张图的不同通道", fontsize=14)
    fig.tight_layout()
    save(fig, "rgb_cmyk_gray.png")


# ---------------------------------------------------------------- 4. 格式体积与失真
def make_format_compare():
    im = center_square(Image.open(ASSETS / "chelsea.png").convert("RGB")).resize((512, 512))
    out = ASSETS / "format_samples"
    out.mkdir(exist_ok=True)

    variants = [
        ("PNG", out / "chelsea.png", dict(optimize=True)),
        ("BMP", out / "chelsea.bmp", {}),
        ("TIFF (Deflate)", out / "chelsea_deflate.tif", dict(compression="tiff_adobe_deflate")),
        ("JPEG q95", out / "chelsea_q95.jpg", dict(quality=95)),
        ("JPEG q75", out / "chelsea_q75.jpg", dict(quality=75)),
        ("JPEG q30", out / "chelsea_q30.jpg", dict(quality=30)),
    ]
    sizes = {}
    for label, path, kwargs in variants:
        im.save(path, **kwargs)
        sizes[label] = path.stat().st_size
        print(f"{label:12s} {sizes[label]:>8d} B  {sizes[label]/1024:>8.1f} KB")

    (ASSETS / "format_sizes.json").write_text(
        json.dumps(sizes, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # 同一细节区域，比较压缩痕迹
    box = (150, 120, 330, 300)
    crop_png = im.crop(box)
    crop_q95 = Image.open(out / "chelsea_q95.jpg").crop(box)
    crop_q30 = Image.open(out / "chelsea_q30.jpg").crop(box)

    fig = plt.figure(figsize=(11, 7))
    gs = fig.add_gridspec(2, 3, height_ratios=[1.1, 1])
    for i, (label, crop) in enumerate([
        ("PNG（无损）", crop_png),
        ("JPEG q95（有损，较轻）", crop_q95),
        ("JPEG q30（有损，明显）", crop_q30),
    ]):
        ax = fig.add_subplot(gs[0, i])
        ax.imshow(crop)
        ax.set_title(label, fontsize=11)
        ax.axis("off")

    ax = fig.add_subplot(gs[1, :])
    labels = list(sizes)
    values = [sizes[k] / 1024 for k in labels]
    colors = ["#2a6fdb", "#6c8ebf", "#8e6ccf", "#d9822b", "#e0a23a", "#c94c4c"]
    bars = ax.bar(labels, values, color=colors)
    for bar, v in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, v + max(values) * 0.02,
                f"{v:.0f} KB", ha="center", va="bottom", fontsize=9)
    ax.set_ylabel("文件大小（KB）")
    ax.set_title("同一张 512×512 图片，存成不同格式的体积", fontsize=12)
    ax.set_ylim(0, max(values) * 1.18)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    save(fig, "format_compare.png")


# ---------------------------------------------------------------- 5. MNIST 样张
def read_idx_images(path):
    with gzip.open(path, "rb") as f:
        magic, n, rows, cols = struct.unpack(">IIII", f.read(16))
        assert magic == 2051, magic
        data = np.frombuffer(f.read(), dtype=np.uint8).reshape(n, rows, cols)
    return data


def read_idx_labels(path):
    with gzip.open(path, "rb") as f:
        magic, n = struct.unpack(">II", f.read(8))
        assert magic == 2049, magic
        data = np.frombuffer(f.read(), dtype=np.uint8)
    return data


def load_mnist():
    raw = LESSON02 / "MNIST" / "data" / "MNIST" / "raw"
    img_path = raw / "train-images-idx3-ubyte.gz"
    lbl_path = raw / "train-labels-idx1-ubyte.gz"
    if not img_path.exists() or not lbl_path.exists():
        print("MNIST 未找到，跳过 MNIST 图片。先运行 lesson02/MNIST 的下载。")
        return None, None
    return read_idx_images(img_path), read_idx_labels(lbl_path)


def make_mnist_samples(images, labels):
    picks = []
    for digit in range(10):
        idx = int(np.where(labels == digit)[0][0])
        picks.append(idx)

    fig, axes = plt.subplots(2, 5, figsize=(9, 4))
    for ax, idx in zip(axes.flat, picks):
        ax.imshow(images[idx], cmap="gray", vmin=0, vmax=255)
        ax.set_title(f"标签 {labels[idx]}", fontsize=11)
        ax.axis("off")
    fig.suptitle("MNIST：28×28 灰度图，0 黑 255 白", fontsize=13)
    fig.tight_layout()
    save(fig, "mnist_samples.png")


def make_mnist_pixels(images, labels):
    idx = int(np.where(labels == 5)[0][0])
    img = images[idx]
    r0, c0, size = 8, 8, 12
    patch = img[r0:r0 + size, c0:c0 + size]

    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    axes[0].imshow(img, cmap="gray", vmin=0, vmax=255)
    axes[0].add_patch(Rectangle((c0 - 0.5, r0 - 0.5), size, size,
                                fill=False, edgecolor="#d62728", linewidth=2))
    axes[0].set_title("完整 28×28（红框是右图区域）", fontsize=11)
    axes[0].axis("off")

    axes[1].imshow(patch, cmap="gray", vmin=0, vmax=255)
    for r in range(size):
        for c in range(size):
            v = int(patch[r, c])
            if v == 0:
                continue
            axes[1].text(c, r, str(v), ha="center", va="center", fontsize=7.5,
                         color="white",
                         bbox=dict(boxstyle="round,pad=0.12", facecolor="black",
                                   edgecolor="none", alpha=0.55))
    axes[1].set_title("放大 12×12：格子里是 0–255 的灰度值", fontsize=11)
    axes[1].set_xticks([])
    axes[1].set_yticks([])

    fig.suptitle("MNIST 的一小块：每个格子一个字节", fontsize=13)
    fig.tight_layout()
    save(fig, "mnist_pixels.png")


# ---------------------------------------------------------------- 6. 读取流程
def make_pipeline():
    fig, ax = plt.subplots(figsize=(10.5, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 12)
    ax.axis("off")

    boxes = [
        (9.6, "文件字节：PNG / JPEG / MNIST IDX", "#e8f0fe"),
        (7.6, "解码器：读文件头、解压、还原像素", "#e8f0fe"),
        (5.6, "像素数组  H×W×C，uint8（0–255）", "#e6f4ea"),
        (3.6, "张量  C×H×W，float32（0–1 或标准化）", "#e6f4ea"),
        (1.6, "批张量  [B, C, H, W]  →  模型", "#fce8e6"),
    ]
    for y, text, color in boxes:
        ax.add_patch(FancyBboxPatch((1.0, y - 0.55), 8.0, 1.1,
                                    boxstyle="round,pad=0.08,rounding_size=0.15",
                                    facecolor=color, edgecolor="#5f6b7a", linewidth=1.2))
        ax.text(5.0, y, text, ha="center", va="center", fontsize=11.5)

    for y0, y1 in [(9.05, 8.15), (7.05, 6.15), (5.05, 4.15), (3.05, 2.15)]:
        ax.add_patch(FancyArrowPatch((5.0, y0), (5.0, y1),
                                     arrowstyle="-|>", mutation_scale=18,
                                     linewidth=1.6, color="#5f6b7a"))

    notes = [
        (9.6, "PNG 无损 / JPEG 有损"),
        (7.6, "PIL: Image.open()"),
        (5.6, "np.array(img).shape = (H, W, C)"),
        (3.6, "ToTensor + Normalize"),
        (1.6, "模型只认张量，不认 .png 后缀"),
    ]
    for y, text in notes:
        ax.text(9.25, y, text, ha="left", va="center", fontsize=9, color="#555555")

    ax.set_title("计算机怎样把一张图送进模型", fontsize=15, pad=20, x=5 / 14)
    save(fig, "pipeline.png")


# ---------------------------------------------------------------- 7. 猫狗示例
def make_cat_dog():
    cat = center_square(Image.open(ASSETS / "chelsea.png").convert("RGB")).resize((300, 300))
    dog = center_square(Image.open(ASSETS / "dog.jpg").convert("RGB")).resize((300, 300))

    fig, axes = plt.subplots(1, 2, figsize=(8, 4.4))
    for ax, im, title in zip(axes, [cat, dog], ["猫：标签 0", "狗：标签 1"]):
        ax.imshow(im)
        ax.set_title(title, fontsize=12)
        ax.axis("off")
    fig.suptitle("猫狗分类：每张图是 [3, 224, 224] 的 RGB 张量", fontsize=13, y=1.0)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    save(fig, "cat_dog.png")


def main():
    make_vector_vs_raster()
    make_vector_svg()
    make_pixel_grid()
    make_color_channels()
    make_format_compare()
    images, labels = load_mnist()
    if images is not None:
        make_mnist_samples(images, labels)
        make_mnist_pixels(images, labels)
    make_pipeline()
    make_cat_dog()
    print("done")


if __name__ == "__main__":
    main()
