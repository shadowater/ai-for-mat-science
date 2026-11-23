"""生成 README 使用的示意图，输出到 素材/figures/。

用法（课程目录下）：
    python scripts/make_figures.py

依赖 numpy、matplotlib、scikit-image、tifffile，均在 requirements.txt 中。
图中数字来自 scripts/fixtures/03_particles_reference_mask.tif。
"""
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.colors import ListedColormap
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
import tifffile
from skimage import color, io, measure, segmentation

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / '素材'
FIXTURES = ROOT / 'scripts' / 'fixtures'
FIG = ASSETS / 'figures'
FIG.mkdir(parents=True, exist_ok=True)

# 中文字体：Windows 用雅黑，Linux/macOS 回退到常见开源字体。
for name in ['Microsoft YaHei', 'Noto Sans CJK SC', 'Source Han Sans SC',
             'PingFang SC', 'WenQuanYi Micro Hei']:
    if any(f.name == name for f in fm.fontManager.ttflist):
        plt.rcParams['font.family'] = name
        break
plt.rcParams.update({
    'axes.unicode_minus': False,
    'figure.facecolor': 'white',
    'savefig.facecolor': 'white',
    'font.size': 11,
})

INK = '#1f2933'
MUTED = '#64748b'
BLUE = '#2563eb'
ORANGE = '#ea580c'
GREEN = '#16a34a'
RED = '#dc2626'
GRID = '#dbe3ec'
LIGHT = '#eff6ff'


def save(fig, name):
    path = FIG / name
    fig.savefig(path, dpi=200, bbox_inches='tight', pad_inches=0.12)
    plt.close(fig)
    print('写入', path.relative_to(ROOT))


def show(ax, img, title, subtitle=None, cmap=None, vmin=None, vmax=None):
    if cmap is None and np.ndim(img) == 2:
        cmap = 'gray'
    ax.imshow(img, cmap=cmap, vmin=vmin, vmax=vmax, interpolation='nearest')
    ax.set_title(title, color=INK, fontsize=12, pad=9)
    ax.axis('off')
    if subtitle:
        ax.text(0.5, -0.04, subtitle, transform=ax.transAxes, ha='center',
                va='top', fontsize=9.5, color=MUTED)


def boundaries_overlay(image, mask, colors):
    """在灰度/RGB 图上画出指定区域的轮廓。colors: {label: rgb}。"""
    base = image.astype(float) / max(float(image.max()), 1.0)
    rgb = color.gray2rgb(base) if image.ndim == 2 else base.copy()
    for label_id, rgb_color in colors.items():
        region = mask == label_id
        edge = segmentation.find_boundaries(region, mode='inner')
        rgb[edge] = rgb_color
    return rgb


def fig_pipeline():
    img = io.imread(FIXTURES / '03_particles.png')
    mask = tifffile.imread(FIXTURES / '03_particles_reference_mask.tif')
    fig = plt.figure(figsize=(13.5, 3.5))
    ax1 = fig.add_axes([0.01, 0.10, 0.16, 0.76])
    ax2 = fig.add_axes([0.235, 0.10, 0.15, 0.76])
    ax3 = fig.add_axes([0.445, 0.10, 0.16, 0.76])
    ax4 = fig.add_axes([0.66, 0.10, 0.32, 0.76])

    show(ax1, img, '① 原始图像', '每个像素一个灰度值')
    ax2.axis('off')
    box = FancyBboxPatch((0.04, 0.16), 0.92, 0.66,
                         boxstyle='round,pad=0.02,rounding_size=0.10',
                         transform=ax2.transAxes, fc=LIGHT, ec=BLUE, lw=1.6)
    ax2.add_patch(box)
    ax2.text(0.5, 0.64, 'Cellpose-SAM', transform=ax2.transAxes, ha='center',
             va='center', fontsize=14, weight='bold', color=INK)
    ax2.text(0.5, 0.47, '预训练权重 cpsam', transform=ax2.transAxes,
             ha='center', fontsize=10, color=MUTED)
    ax2.text(0.5, 0.30, '像素 → 实例区域', transform=ax2.transAxes,
             ha='center', fontsize=10, color=BLUE)
    ax2.set_title('② 分割模型', color=INK, fontsize=12, pad=9)

    labels = color.label2rgb(mask, bg_label=0, bg_color=(1, 1, 1))
    show(ax3, labels, '③ 实例标签图', '0 是背景，正整数是编号')

    props = [p for p in measure.regionprops(mask) if p.label in (1, 3, 7, 12, 16)]
    rows = []
    for p in props:
        perimeter = measure.perimeter_crofton(np.pad(p.image, 1), directions=4)
        rows.append([str(p.label), str(int(p.area)), f'{perimeter:.0f}'])
    table = ax4.table(cellText=rows, colLabels=['编号', '面积 / px²', '周长 / px'],
                      loc='center', cellLoc='center', colWidths=[0.22, 0.39, 0.39])
    table.auto_set_font_size(False)
    table.set_fontsize(10.5)
    table.scale(1, 1.45)
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor(GRID)
        cell.set_linewidth(0.8)
        if row == 0:
            cell.set_facecolor('#1e293b')
            cell.get_text().set_color('white')
            cell.get_text().set_weight('bold')
        elif row % 2 == 0:
            cell.set_facecolor('#f8fafc')
    ax4.axis('off')
    ax4.set_title('④ 测量表', color=INK, fontsize=12, pad=9)

    for x in (0.183, 0.395, 0.615):
        fig.text(x, 0.47, '→', ha='center', va='center', fontsize=24, color=MUTED)
    save(fig, 'fig_pipeline.png')


def fig_semantic_instance():
    img = io.imread(FIXTURES / '03_particles.png')
    mask = tifffile.imread(FIXTURES / '03_particles_reference_mask.tif')
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.2))
    show(axes[0], img, '原始图像', '灰度图：颗粒亮、背景暗')
    show(axes[1], (mask > 0).astype(float), '语义分割', '只回答：这个像素是不是颗粒',
         cmap=ListedColormap(['white', '#93c5fd']), vmin=0, vmax=1)
    show(axes[2], color.label2rgb(mask, bg_label=0, bg_color=(1, 1, 1)),
         '实例分割', '每个颗粒一个独立编号')
    fig.subplots_adjust(wspace=0.06)
    save(fig, 'fig_semantic_instance.png')


def fig_label_map():
    small = np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 2, 0],
        [0, 1, 1, 1, 0, 2, 0],
        [0, 0, 1, 0, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ])
    mask = tifffile.imread(FIXTURES / '03_particles_reference_mask.tif')
    area_one = int((mask == 1).sum())

    fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.9),
                             gridspec_kw={'width_ratios': [1, 1, 1.25]})
    ax = axes[0]
    palette = ListedColormap(['#ffffff', '#bfdbfe', '#fdba74'])
    ax.imshow(small, cmap=palette, vmin=0, vmax=2)
    for (row, col), value in np.ndenumerate(small):
        ax.text(col, row, str(value), ha='center', va='center',
                fontsize=13, color=INK)
    ax.set_xticks(np.arange(-0.5, small.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, small.shape[0], 1), minor=True)
    ax.grid(which='minor', color='#94a3b8', lw=0.8)
    ax.tick_params(which='both', length=0, bottom=False, left=False,
                   labelbottom=False, labelleft=False)
    ax.set_title('① 局部像素的编号', color=INK, fontsize=12, pad=9)
    ax.text(0.5, -0.04, '同一个编号 = 同一个颗粒', transform=ax.transAxes,
            ha='center', va='top', fontsize=9.5, color=MUTED)

    ys, xs = np.where(mask == 1)
    pad = 14
    crop = (mask[max(ys.min() - pad, 0):ys.max() + pad,
                 max(xs.min() - pad, 0):xs.max() + pad] == 1)
    show(axes[1], crop, '② 编号 1 的掩膜（局部放大）',
         f'数一数 True：面积 = {area_one} px²',
         cmap=ListedColormap(['white', '#1d4ed8']), vmin=0, vmax=1)

    ax = axes[2]
    ax.imshow(color.label2rgb(mask, bg_label=0, bg_color=(1, 1, 1)))
    cy, cx = np.argwhere(mask == 1).mean(axis=0)
    ax.add_patch(plt.Circle((cx, cy), 28, fill=False, ec=ORANGE, lw=2.2))
    ax.set_title('③ 整张图叠加显示', color=INK, fontsize=12, pad=9)
    ax.axis('off')
    ax.text(0.5, -0.04, '橙圈 = 编号 1；编号用于追踪，大小由像素数计算',
            transform=ax.transAxes, ha='center', va='top', fontsize=9.5, color=MUTED)
    fig.subplots_adjust(wspace=0.18)
    save(fig, 'fig_label_map.png')


def measure_labels(labels):
    edge_ids = np.unique(np.concatenate([
        labels[0, :], labels[-1, :], labels[:, 0], labels[:, -1]]))
    edge_ids = edge_ids[edge_ids > 0]
    rows = {}
    for p in measure.regionprops(labels):
        perimeter = measure.perimeter_crofton(np.pad(p.image, 1), directions=4)
        rows[int(p.label)] = dict(area=int(p.area), perimeter=perimeter,
                                  cy=p.centroid[0], cx=p.centroid[1],
                                  edge=bool(p.label in edge_ids))
    return rows, set(int(i) for i in edge_ids)


def fig_edge_removal():
    img = io.imread(FIXTURES / '03_particles.png')
    mask = tifffile.imread(FIXTURES / '03_particles_reference_mask.tif')
    rows, edge_ids = measure_labels(mask)
    colors = {label: (1.0, 0.15, 0.15) for label in edge_ids}
    colors.update({label: (0.1, 0.85, 0.35) for label in rows if label not in edge_ids})
    filtered = np.where(np.isin(mask, list(edge_ids)), 0, mask)

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.3))
    ax = axes[0]
    ax.imshow(boundaries_overlay(img, mask, colors))
    for label, info in rows.items():
        ax.text(info['cx'], info['cy'], str(label), ha='center', va='center',
                fontsize=9, color='white',
                bbox=dict(boxstyle='circle,pad=0.12', fc='#1f2933', ec='none', alpha=0.75))
    ax.set_title(f'① 全部 {len(rows)} 个：红 = 接触边缘', color=INK, fontsize=12, pad=9)
    ax.axis('off')
    ax.text(0.5, -0.03, f'边缘编号：{sorted(edge_ids)}', transform=ax.transAxes,
            ha='center', va='top', fontsize=9.5, color=MUTED)

    ax = axes[1]
    ax.imshow(color.label2rgb(filtered, image=img, bg_label=0, alpha=0.55))
    ax.set_title(f'② 保留 {len(rows) - len(edge_ids)} 个完整颗粒',
                 color=INK, fontsize=12, pad=9)
    ax.axis('off')
    ax.text(0.5, -0.03, '面积统计只使用保留颗粒', transform=ax.transAxes,
            ha='center', va='top', fontsize=9.5, color=MUTED)
    fig.subplots_adjust(wspace=0.06)
    save(fig, 'fig_edge_removal.png')


def fig_agent_loop():
    fig, ax = plt.subplots(figsize=(12.5, 3.1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    boxes = [
        (0.02, '① 你说清目标', '自然语言，一次一件事'),
        (0.265, '② Agent 执行', '写代码、运行、贴输出'),
        (0.51, '③ 你看结果', '叠图、编号数、面积'),
        (0.755, '④ 核对与追问', '对不上就让它给依据'),
    ]
    width, height, y0 = 0.215, 0.40, 0.38
    for i, (x, title, sub) in enumerate(boxes):
        box = FancyBboxPatch((x, y0), width, height,
                             boxstyle='round,pad=0.008,rounding_size=0.02',
                             fc='white', ec=BLUE if i % 2 == 0 else ORANGE,
                             lw=1.8, transform=ax.transAxes)
        ax.add_patch(box)
        ax.text(x + width / 2, y0 + height * 0.66, title, ha='center',
                va='center', fontsize=12.5, weight='bold', color=INK)
        ax.text(x + width / 2, y0 + height * 0.30, sub, ha='center',
                va='center', fontsize=9.5, color=MUTED)
        if i < 3:
            ax.annotate('', xy=(x + width + 0.030, y0 + height / 2),
                        xytext=(x + width + 0.004, y0 + height / 2),
                        arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=2,
                                        mutation_scale=13))
    arc = FancyArrowPatch((0.86, y0 - 0.01), (0.13, y0 - 0.01),
                          connectionstyle='arc3,rad=-0.28', arrowstyle='-|>',
                          color=BLUE, lw=1.6, ls='--', transform=ax.transAxes,
                          mutation_scale=13)
    ax.add_patch(arc)
    ax.text(0.5, 0.05, '不对就回到上一步：改一句话、重跑、再看',
            ha='center', fontsize=9.5, color=BLUE)
    ax.text(0.5, 0.92, '你定目标和验收标准，Agent 负责实现和执行',
            ha='center', fontsize=11, color=MUTED)
    save(fig, 'fig_agent_loop.png')


def fig_tio2():
    img = io.imread(ASSETS / '09_TiO2_SEM_1908248.tif')
    roi = img[:712]
    fig = plt.figure(figsize=(12.5, 4.0))
    ax1 = fig.add_axes([0.01, 0.08, 0.26, 0.80])
    ax2 = fig.add_axes([0.30, 0.08, 0.26, 0.80])
    ax3 = fig.add_axes([0.60, 0.08, 0.38, 0.80])

    ax1.imshow(img, cmap='gray', vmin=0, vmax=255)
    ax1.axhline(711.5, color=RED, lw=1.4, ls='--')
    ax1.add_patch(Rectangle((0, 712), img.shape[1], img.shape[0] - 712,
                            color=RED, alpha=0.18, lw=0))
    ax1.text(20, 744, '仪器信息栏（不分析）', color='white', fontsize=9,
             bbox=dict(boxstyle='round,pad=0.25', fc=RED, ec='none', alpha=0.85))
    ax1.text(20, 60, '分析区：0–712 行', color='white', fontsize=9.5,
             bbox=dict(boxstyle='round,pad=0.25', fc='#1f2933', ec='none', alpha=0.75))
    ax1.set_title('① 原图与 ROI', color=INK, fontsize=12, pad=9)
    ax1.axis('off')

    ax2.imshow(roi, cmap='gray', vmin=0, vmax=255)
    ax2.plot([840, 940], [660, 660], color='white', lw=4, solid_capstyle='butt')
    ax2.text(890, 645, '100 px ≈ 0.73 μm', color='white', ha='center',
             fontsize=9, bbox=dict(boxstyle='round,pad=0.2', fc='#1f2933', ec='none', alpha=0.75))
    ax2.set_title('② 裁剪后的分析区', color=INK, fontsize=12, pad=9)
    ax2.axis('off')

    ax3.axis('off')
    ax3.text(0.0, 0.86, '像素尺寸标定', fontsize=13, weight='bold', color=INK)
    lines = [
        ('视野宽度', '7.520 μm'),
        ('横向像素', '1024 px'),
        ('像素尺寸 s', '7.520 ÷ 1024'),
        ('', '≈ 0.00734 μm/px'),
        ('面积', 'A × s²  (μm²)'),
        ('周长', 'P × s  (μm)'),
    ]
    for i, (left, right) in enumerate(lines):
        y = 0.70 - i * 0.115
        ax3.text(0.02, y, left, fontsize=10.5, color=MUTED)
        ax3.text(0.52, y, right, fontsize=10.5, color=INK,
                 weight='bold' if i in (2, 3) else 'normal')
    ax3.add_patch(FancyBboxPatch((0.0, 0.0), 0.98, 0.98,
                                 boxstyle='round,pad=0.02,rounding_size=0.03',
                                 transform=ax3.transAxes, fc='#f8fafc',
                                 ec=GRID, lw=1.2, zorder=0))
    ax3.set_title('③ 从像素到微米', color=INK, fontsize=12, pad=9)
    save(fig, 'fig_tio2_roi.png')


if __name__ == '__main__':
    fig_pipeline()
    fig_semantic_instance()
    fig_label_map()
    fig_edge_removal()
    fig_agent_loop()
    fig_tio2()
