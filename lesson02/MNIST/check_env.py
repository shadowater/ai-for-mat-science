# -*- coding: utf-8 -*-
"""检查 MNIST 课堂环境。运行：python check_env.py"""

import platform
import sys

print("Python", sys.version.split()[0])
print("系统", platform.platform())
print("解释器", sys.executable)

missing = []
for name in ("torch", "torchvision", "matplotlib"):
    try:
        module = __import__(name)
        print(f"{name} {getattr(module, '__version__', '?')}")
    except Exception as exc:
        missing.append(name)
        print(f"{name} 未安装：{exc}")

try:
    import torch
    print("CUDA", torch.cuda.is_available(), "| CPU 线程", torch.get_num_threads())
    if torch.cuda.is_available():
        print("GPU", torch.cuda.get_device_name(0))
except Exception:
    pass

print()
if missing:
    print("缺少：", ", ".join(missing))
    print("安装 CPU 版：")
    print("  python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu")
    print("  python -m pip install matplotlib")
else:
    print("环境就绪。下一步：python mnist_reference.py --model mlp --epochs 1")
    print("如果数据还没下载，第一次运行会自动下载到 data/。")
