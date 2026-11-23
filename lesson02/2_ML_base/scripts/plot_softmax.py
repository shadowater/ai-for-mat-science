"""绘制二分类 Softmax 中一个类别的概率曲线。"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# 两个类别的分数为 [z, 0]，展示第一个类别的 Softmax 概率。
z = np.linspace(-6, 6, 401)
p = 1 / (1 + np.exp(-z))
fig, ax = plt.subplots(figsize=(5.5, 3.5), layout='constrained')
ax.plot(z, p, color='#2563eb', linewidth=2.5)
ax.set(xlabel='Score z (other score = 0)', ylabel='Probability',
       title='Softmax: two classes', xlim=(-6, 6), ylim=(0, 1))
ax.set_yticks([0, 0.5, 1])
ax.grid(alpha=0.2)
path = Path(__file__).resolve().parents[1] / '素材/softmax_curve.png'
fig.savefig(path, dpi=180)
print(path)
