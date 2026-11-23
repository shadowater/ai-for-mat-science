"""运行 Notebook 真实推理路径，批量保存案例预测和测量结果。

python run_examples.py [图片文件名 ...]
默认运行素材/案例来源.json 中的七张显微图。
"""
import argparse
import json
import os
from pathlib import Path
import re
import time

os.environ.setdefault('MPLBACKEND', 'Agg')
import matplotlib.pyplot as plt
plt.show = lambda: plt.close('all')
root = Path(__file__).resolve().parent
os.chdir(root)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('images', nargs='*')
args = parser.parse_args()
images = args.images or [item['file'] for item in json.loads((root / '素材/案例来源.json').read_text())]
nb = json.loads((root / '颗粒分割与测量.ipynb').read_text())
namespace = {}
summary = []
for filename in images:
    start = time.monotonic()
    print(f'开始：{filename}', flush=True)
    for cell in nb['cells']:
        if cell['cell_type'] != 'code':
            continue
        source = ''.join(cell['source'])
        source = source.replace("SOURCE = 'reference'", "SOURCE = 'cellpose'")
        source = re.sub(r"^IMAGE_NAME = .*", f'IMAGE_NAME = {filename!r}', source, flags=re.M)
        exec(compile(source, '颗粒分割与测量.ipynb', 'exec'), namespace)
    table = namespace['all_particles']
    row = dict(file=filename, all=len(table), kept=int(table.kept.sum()),
               removed=int(table.touches_edge.sum()), seconds=round(time.monotonic()-start, 2))
    summary.append(row)
    (root / 'outputs/batch_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n')
    print('完成：', row, flush=True)
