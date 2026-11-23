"""从 outputs 中的真实预测结果生成讲义用案例图。

先运行：
    uv run python run_examples.py 09_TiO2_SEM_1908248.tif 07_cellpose_039_img.png 08_cellpose_033_img.png

再运行：
    uv run python scripts/make_case_figures.py
"""
from pathlib import Path
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import binary_dilation
from skimage import color, io, segmentation

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'outputs'
FIGS = ROOT / '素材' / 'figures'
CASES = ['09_TiO2_SEM_1908248', '07_cellpose_039_img', '08_cellpose_033_img']


def image_path(name):
    for ext in ('.tif', '.png'):
        path = ROOT / '素材' / f'{name}{ext}'
        if path.exists():
            return path
    raise FileNotFoundError(name)


def load_mask(json_path):
    record = json.loads(Path(json_path).read_text(encoding='utf-8'))
    mask = np.zeros(record['shape'], dtype=np.uint16)
    for obj in record['objects']:
        for x, y in obj['points_xy']:
            mask[y, x] = obj['label']
    return mask


def to_rgb(image):
    image = image.astype(float)
    image = (image - image.min()) / max(float(image.max() - image.min()), 1e-9)
    return color.gray2rgb(image) if image.ndim == 2 else image


def overlay(image, kept, edge):
    rgb = to_rgb(image)
    kept_line = binary_dilation(segmentation.find_boundaries(kept, mode='inner'))
    edge_line = binary_dilation(segmentation.find_boundaries(edge, mode='inner'),
                                iterations=2)
    rgb[kept_line] = [0.1, 1.0, 0.1]
    rgb[edge_line] = [1.0, 0.1, 0.1]
    return rgb


for name in CASES:
    stem = f'{name}_cellpose'
    image = io.imread(image_path(name))
    if 'TiO2_' in name:
        image = image[:712]
    all_mask = load_mask(OUT / f'{stem}_mask.json')
    kept = load_mask(OUT / f'{stem}_filtered_mask.json')
    edge = np.where(kept > 0, 0, all_mask)

    if name.startswith('09'):
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        axes[0].imshow(image, cmap='gray')
        axes[0].set_title('Original')
        axes[1].imshow(color.label2rgb(all_mask, bg_label=0, bg_color=(0, 0, 0)))
        axes[1].set_title(f'Instance labels ({len(np.unique(all_mask)) - 1})')
        axes[2].imshow(overlay(image, kept, edge))
        axes[2].set_title('Green: kept / Red: edge')
        for ax in axes:
            ax.axis('off')
        fig.tight_layout()
        fig.savefig(FIGS / 'fig_case09_result.png', dpi=150, bbox_inches='tight')
        plt.close(fig)

        plt.imsave(FIGS / 'fig_case09_labels.png', color.label2rgb(
            all_mask, bg_label=0, bg_color=(0, 0, 0)))
    else:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.imshow(overlay(image, kept, edge))
        ax.axis('off')
        fig.tight_layout(pad=0)
        fig.savefig(FIGS / f'fig_case{name[:2]}_overlay.png', dpi=150,
                    bbox_inches='tight', pad_inches=0)
        plt.close(fig)

print('案例图已写入', FIGS)
