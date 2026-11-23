"""生成课堂图片与几何参考标签：python prepare_examples.py。"""
from pathlib import Path
import numpy as np
from scipy.ndimage import gaussian_filter
from skimage import data, io
from skimage.draw import disk, ellipse
import tifffile

root = Path(__file__).resolve().parent / '素材'
root.mkdir(exist_ok=True)
coins = data.coins()
io.imsave(root / '01_coins.png', coins, check_contrast=False)
# 裁剪穿过外圈硬币，供模型预测后演示边缘剔除。
io.imsave(root / '02_coins_crop.png', coins[30:275, 25:360], check_contrast=False)
mask = np.zeros((256, 320), dtype=np.uint16)
# 5 个内部颗粒 + 分别接触四边的 4 个颗粒；保留非连续编号。
for label, row, col, radius in [(1,55,60,20),(3,60,135,27),(7,125,70,24),
                                (12,190,110,29),(21,3,230,24),(25,253,220,25),
                                (30,185,2,22),(42,135,318,27)]:
    rr, cc = disk((row, col), radius, shape=mask.shape)
    mask[rr, cc] = label
rr, cc = ellipse(135, 210, 22, 38, rotation=0.4, shape=mask.shape)
mask[rr, cc] = 16
rng = np.random.default_rng(20261121)
image = 30 + 145 * gaussian_filter((mask > 0).astype(float), 1.2)
image += rng.normal(0, 5, mask.shape)
io.imsave(root / '03_particles.png', np.clip(image, 0, 255).astype('uint8'), check_contrast=False)
tifffile.imwrite(root / '03_particles_reference_mask.tif', mask)
print('已生成 3 张案例图片和 1 张几何参考标签。')
