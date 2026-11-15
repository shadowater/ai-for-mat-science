#!/usr/bin/env bash
set -euo pipefail
# Model weights and downloaded runtimes stay outside the course repository.
llm_home="${AIMAT_LLM_HOME:-$HOME/aimat/.local-llm}"
llm_binary="$llm_home/runtime/llama-b12202/llama-server"
llm_model="$llm_home/models/Qwen3-0.6B-Q8_0.gguf"
if [[ ! -x "$llm_binary" || ! -f "$llm_model" ]]; then
  echo '未找到本地运行程序或模型。请按 README 配置，或设置 AIMAT_LLM_HOME。' >&2
  exit 1
fi
llm_paths="$(python3 - "$llm_home/rocm-python" <<'PY'
from pathlib import Path
import sys
root=Path(sys.argv[1])
print(':'.join(str(p) for p in sorted(root.glob('_rocm_sdk_*/lib')) if p.is_dir()))
PY
)"
export LD_LIBRARY_PATH="$llm_paths:/opt/rocm/lib:/usr/lib/wsl/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
# Applicable to older ROCm/ROCDXG stacks as well; scoped to this process.
export HSA_ENABLE_DXG_DETECTION=1
llm_script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
llm_options=(--jinja -m "$llm_model" -c 2048 --parallel 1 --host 127.0.0.1 --port 8088 -lv 4)
case "${1:---gpu}" in
  --cpu) llm_options+=(--device none -ngl 0) ;;
  --gpu)
    llm_devices="$("$llm_binary" --list-devices 2>&1)"
    if ! printf '%s\n' "$llm_devices" | rg -qi 'ROCm[0-9]|AMD Radeon|gfx1200'; then
      printf '%s\n' "$llm_devices" >&2
      echo '没有确认 AMD GPU 后端；请先完成依赖与设备检查，或显式用 --cpu。' >&2
      exit 1
    fi
    llm_options+=(-ngl 99)
    ;;
  --devices) exec "$llm_binary" --list-devices ;;
  *) echo '用法：bash start_wsl.sh [--gpu|--cpu|--devices]' >&2; exit 2 ;;
esac
exec python3 "$llm_script_dir/without_system.py" "$llm_binary" "${llm_options[@]}"
