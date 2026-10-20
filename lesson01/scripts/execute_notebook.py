"""Execute trusted teaching cells sequentially, without a Jupyter dependency.
This validates Python calculations; it does not test a Jupyter kernel or RISE.
"""
import base64
import contextlib
import io
import json
import os
from pathlib import Path
import platform

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
os.environ['MPLBACKEND'] = 'Agg'
path = ROOT / 'notebook/lesson01.ipynb'
nb = json.loads(path.read_text())
nb['metadata']['language_info']['version'] = platform.python_version()
namespace = {'__name__': '__main__'}
count = 0
for cell in nb['cells']:
    if cell['cell_type'] != 'code':
        continue
    count += 1
    source = ''.join(cell['source'])
    output = io.StringIO()
    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
        exec(compile(source, f'notebook-cell-{count}', 'exec'), namespace)
    cell['execution_count'] = count
    cell['outputs'] = [{'output_type': 'stream', 'name': 'stdout', 'text': output.getvalue().splitlines(True)}]
    if 'fig.savefig' in source:
        cell['outputs'].append({'output_type': 'display_data', 'metadata': {}, 'data': {
            'image/png': base64.b64encode((ROOT/'outputs/stress.png').read_bytes()).decode(),
            'text/plain': ['Synthetic tensile teaching data']}})
assert namespace['stress'](100, 2) == 50
assert namespace['stress'](100, 4) == 25
for area in [0, -1]:
    try:
        namespace['stress'](100, area)
    except ValueError:
        pass
    else:
        raise AssertionError('Expected invalid area rejection')
path.write_text(json.dumps(nb, ensure_ascii=False, indent=2))
print(f'Executed {count} Python cells; numeric and invalid-area checks passed.')
