"""Plot the measured and original ESOL predictions supplied with Delaney (2004).

Run: python plot_esol.py
Requires numpy and matplotlib. Uses the original prediction column without fitting.
"""
import csv
import hashlib
import json
import os
import tempfile
from pathlib import Path

os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'esol-matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'ci034243x_si_001.txt'
with SOURCE.open(encoding='utf-8-sig', newline='') as stream:
    records = list(csv.DictReader(stream))
measured = np.array([float(r['measured log(solubility:mol/L)']) for r in records])
predicted = np.array([float(r['ESOL predicted log(solubility:mol/L)']) for r in records])
assert len(records) == 1144 and np.isfinite(measured).all() and np.isfinite(predicted).all()
error = predicted - measured
within = np.abs(error) <= 1
metrics = {
    'source_file': SOURCE.name,
    'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'source_doi': '10.1021/ci034243x',
    'evaluation_scope': 'Small training subset; original measured/predicted columns; no refitting',
    'sample_count': len(records),
    'aae_log10': float(np.abs(error).mean()),
    'rmse_log10': float(np.sqrt(np.mean(error ** 2))),
    'r2_definition': '1 - sum((predicted-measured)^2) / sum((measured-mean(measured))^2)',
    'r2': float(1 - np.sum(error ** 2) / np.sum((measured - measured.mean()) ** 2)),
    'within_one_log10_count': int(within.sum()),
    'within_one_log10_fraction': float(within.mean()),
}
(ROOT / 'esol_metrics.json').write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False})
fig, ax = plt.subplots(figsize=(6.4, 6.0), layout='constrained')
limits = (np.floor(min(measured.min(), predicted.min())) - .3, np.ceil(max(measured.max(), predicted.max())) + .3)
x = np.linspace(*limits, 200)
ax.fill_between(x, x - 1, x + 1, color='#e4eff4', label='Within +/-1 log unit')
ax.plot(x, x, color='#334a59', linewidth=1.3, label='Prediction = measurement')
ax.scatter(measured[within], predicted[within], s=17, color='#227b91', alpha=.55, edgecolors='none', label=f'Within band: {within.sum()}')
ax.scatter(measured[~within], predicted[~within], s=19, color='#c56a28', alpha=.70, edgecolors='none', label=f'Outside band: {(~within).sum()}')
ax.set(xlim=limits, ylim=limits, xlabel='Measured log$_{10}$[S / (mol L$^{-1}$)]', ylabel='ESOL predicted log$_{10}$[S / (mol L$^{-1}$)]')
ax.set_aspect('equal')
ax.set_title('ESOL: measured vs predicted solubility\nSmall training subset | 1,144 compounds', fontsize=13, loc='left', pad=16)
ax.grid(alpha=.15)
ax.set_axisbelow(True)
ax.legend(loc='upper left', frameon=True, framealpha=.95, fontsize=9)
ax.text(.97, .035, f"AAE = {metrics['aae_log10']:.3f}\nRMSE = {metrics['rmse_log10']:.3f}\nWithin +/-1: {within.mean():.1%}", transform=ax.transAxes, ha='right', va='bottom', fontsize=10, bbox={'facecolor':'white','edgecolor':'#dce5eb','alpha':.95,'pad':8})
fig.savefig(ROOT / 'esol_measured_vs_predicted.png', dpi=180, metadata={'Description': 'Calculated from Delaney (2004) supporting information, DOI 10.1021/ci034243x. Training subset.'})
plt.close(fig)
print(json.dumps(metrics, ensure_ascii=False, indent=2))
