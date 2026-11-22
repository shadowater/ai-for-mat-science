"""按来源清单下载七张显微图，并检查文件 SHA-256。"""
from pathlib import Path
import hashlib
import json
import urllib.request

root = Path(__file__).resolve().parent / '素材'
for item in json.loads((root / '案例来源.json').read_text(encoding='utf-8')):
    target = root / item['file']
    if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() == item['sha256']:
        print('已校验：', target.name)
        continue
    temporary = target.with_suffix(target.suffix + '.part')
    urllib.request.urlretrieve(item['url'], temporary)
    if hashlib.sha256(temporary.read_bytes()).hexdigest() != item['sha256']:
        temporary.unlink()
        raise RuntimeError(f'{target.name} 的源文件内容发生变化，请核对来源记录。')
    temporary.replace(target)
    print('已下载并校验：', target.name)
