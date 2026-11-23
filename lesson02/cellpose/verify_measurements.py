"""执行 Notebook 的参考路径并检查测量边界情况，无需 Cellpose 权重。"""
import ast
import json
import os
from pathlib import Path
import tempfile

os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'cellpose-lesson02-mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from skimage.draw import disk

root = Path(__file__).resolve().parent
notebook = json.loads((root / '颗粒分割与测量.ipynb').read_text(encoding='utf-8'))
namespace = {}
os.chdir(root)
# 与学生运行相同代码；关闭已显示的图，保持无界面执行。
plt.show = lambda: plt.close('all')
for i, cell in enumerate(notebook['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        ast.parse(source)
        exec(compile(source, f'notebook-cell-{i}', 'exec'), namespace)
measure_particles = namespace['measure_particles']

# 空预测保持有效表结构，并可继续导出。
empty, cleaned = measure_particles(np.zeros((10, 12), dtype=np.uint16))
assert empty.empty and empty['kept'].dtype == bool and not cleaned.any()
# 四边对象和不连续标签；角落对象只计一次。
a = np.zeros((30, 30), dtype=np.uint16)
a[0:3, 0:3] = 2
a[-3:, 10:13] = 8
a[10:13, :3] = 15
a[10:13, -3:] = 40
a[10:13, 10:13] = 99
result, filtered = measure_particles(a)
assert set(result.loc[result.touches_edge, 'label']) == {2, 8, 15, 40}
assert set(np.unique(filtered)) == {0, 99}
assert result.set_index('label').loc[99, 'area_px2'] == 9
# 近边对象在扩展边缘区域内被整体剔除。
a = np.zeros((30, 30), dtype=np.uint16)
a[2:5, 12:15] = 7
assert measure_particles(a, edge_margin_px=0)[0].kept.all()
assert not measure_particles(a, edge_margin_px=2)[1].any()
# 全图对象、孔洞及圆形周长近似。
assert not measure_particles(np.ones((8, 9), dtype=int))[1].any()
a = np.zeros((100, 100), dtype=int)
rr, cc = disk((50, 50), 25, shape=a.shape)
a[rr, cc] = 1
circle, _ = measure_particles(a)
assert abs(circle.iloc[0].perimeter_px / (2*np.pi*25) - 1) < 0.05
solid_perimeter = circle.iloc[0].perimeter_px
a[45:55, 45:55] = 0
ring, _ = measure_particles(a)
assert ring.iloc[0].area_px2 == circle.iloc[0].area_px2 - 100
assert ring.iloc[0].perimeter_px > solid_perimeter
for bad in [np.zeros((2, 2, 2), dtype=int), np.ones((2, 2), dtype=float), -np.ones((2, 2), dtype=int)]:
    try:
        measure_particles(bad)
    except ValueError:
        pass
    else:
        raise AssertionError('非法标签应给出错误提示')
for scale in [0, -1, float('nan'), float('inf')]:
    try:
        measure_particles(np.zeros((3, 3), dtype=int), pixel_size_um=scale)
    except ValueError:
        pass
    else:
        raise AssertionError('非法标定应给出错误提示')
print('通过：Notebook 参考流程、空结果、四边与角落、边缘宽度、孔洞、周长近似、单位换算和输入检查。')
