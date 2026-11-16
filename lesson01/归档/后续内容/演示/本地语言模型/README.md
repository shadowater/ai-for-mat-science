# WSL 本地语言模型演示

配合[1.4.5 第 5 小节](../../内容/1.4_AI与Agent的工作方式/1.4.5_从文本向量到语言模型.md)。这是教师演示环境；学生在课堂观察运行过程，模型、运行库和下载缓存放在课程仓库外。

## 本机检查

2026-11-08 检查：Windows 主机为 AMD Radeon RX 9060 XT，注册表专用显存约 15.92 GiB（16GB 规格）；当前 WSL 为 Ubuntu 26.04.1，约 15 GiB 内存，存在 `/dev/dxg` 和 `libdxcore.so`。这张 AMD 卡的识别以 ROCm 后端和卸载日志为准；注册表的专用显存信息比 CIM 的 32 位 AdapterRAM 字段更适合本机容量核对。

容量上适合先用 Qwen3-0.6B：官方 Q8_0 GGUF 文件为 639,446,688 字节，约 610 MiB。运行时还需要缓存和其他缓冲区，总显存用量由模型与运行时缓冲共同组成。确认 GPU 执行时查看后端识别和模型卸载日志。

## 实施进度

- 已停止 Windows 原生运行方案，后续只在 WSL 启动。
- 已下载并核对官方发布 SHA-256，安装 ROCDXG 1.2.2 用户态运行库；Windows 显卡驱动保持原样。
- 已安装隔离的 ROCm Core SDK、数学库及 gfx1200 设备库 10.0.0；安装目录为 `/root/aimat/.local-llm/rocm-python`，系统 Python 保持原有配置。
- 已下载并校验官方模型 LFS SHA-256 和 llama.cpp b12202 发布包 SHA-256，模型与运行程序位于 `/root/aimat/.local-llm/`。
- **GPU 实测通过**：识别到 ROCm0 / RX 9060 XT，报告 16,253 MiB 显存；日志明确记录 `offloaded 29/29 layers to GPU`。上下文 2,048、单并发时，模型缓冲约 604 MiB，KV 缓存约 224 MiB，计算缓冲约 28 MiB。这些分项对应当前配置；其他场景还需按实际日志核对显存需求。
- GPU 上真实分词、单 token 候选返回、聊天流式输出均通过；给出样品记录后返回 `M-02`。CPU 路径也已验证。查看[实测示例](实测示例.json)。

## 在 WSL 启动

在本目录打开终端，运行：

```bash
bash start_wsl.sh --devices
bash start_wsl.sh --gpu
```

保持该终端运行，然后访问 `http://127.0.0.1:8087`，或另开 WSL 终端运行下面的观察脚本。停止服务按 Ctrl+C。服务监听本机回环地址，访问范围限定在本机。

当前服务已启动在上述地址。若再次启动提示端口占用，先使用已有服务，或回到原启动终端停止它。日志位于 `/root/aimat/.local-llm/logs/gpu-server.log`。

[start_wsl.sh](start_wsl.sh)默认查找 `$HOME/aimat/.local-llm`；其他路径可设置 `AIMAT_LLM_HOME`。它对启动进程设置运行库路径，并先检查 GPU 识别；使用 CPU 时明确运行 `bash start_wsl.sh --cpu`。

这是本机验证过的便携式环境。其他 AMD/WSL 组合应按设备和版本逐项验证。重装时需保留 ROCDXG、OpenMP 库，以及完整的推理程序、ROCm core/libraries/gfx1200 包和模型；AMD 官方安装与 WSL 要求见[安装文档](https://rocm.docs.amd.com/en/latest/install/rocm.html)。

## 课堂观察脚本

[inspect_llm.py](inspect_llm.py)使用 Python 标准库调用已经启动的本地 llama-server。模型训练、下载和加载由其他步骤完成。

在本目录运行：

```bash
python3 inspect_llm.py tokens --text '样品编号是 M-02。'
python3 inspect_llm.py next --text '样品编号是 M-'
python3 inspect_llm.py chat --text '记录：样品编号是 M-02。请只回答编号。'
```

默认连接 `http://127.0.0.1:8087`，可用 `--base-url` 修改。服务器启动后，脚本便能连接；连接失败时按报错检查服务状态。脚本的输出来自指定的本地服务。

- `tokens`：显示真实分词片段和编号；有些片段可能是字节列表。
- `next`：原始文本续写，生成一个 token，并保留候选的原始 JSON。请求返回采样前候选分数；`logprob` 是自然对数概率，候选列表覆盖服务端实际返回的部分词表。此模式按续写方式处理输入。
- `chat`：使用服务端聊天模板，按 Qwen3 的非思考模式设置请求，流式显示返回文字；上限为 128 个生成 token，回答可能在句中结束。每次请求独立，历史需要显式提供。界面返回的流式片段可能包含部分 token 或多个 token。

参考：[服务器接口说明](https://github.com/ggml-org/llama.cpp/tree/master/tools/server)、[Qwen 模型卡](https://huggingface.co/Qwen/Qwen3-0.6B)、[官方 GGUF](https://huggingface.co/Qwen/Qwen3-0.6B-GGUF)、[AMD WSL 用户态运行库说明](https://github.com/ROCm/librocdxg)。

代码与课程讲解为自行编写。模型采用其官方 Apache-2.0 许可，运行库和推理程序各遵循其上游许可；本仓库提供代码、说明与原始下载入口，模型和二进制文件从各自来源获取。

## 维护验证

Python 标准库观察脚本的三种模式已通过模拟接口测试与真实 CPU/GPU 服务检查；启动脚本通过 Bash 语法检查，本章流程图可解析，本地文档链接已核对。模型权重与运行包保存在课程仓库外。

## 当前已关闭系统提示词

`start_wsl.sh` 通过本地入口 `127.0.0.1:8087` 启动演示，`without_system.py` 会在转发前移除请求中所有 `role: system` 消息；模型后端位于 `127.0.0.1:8088`。网页与观察脚本统一连接 8087 入口。

采用入口移除，是因为某些服务端处理会把聊天模板中跳过的 system 内容合并进用户消息。入口在转发前直接删除 system 消息。已通过实际 `/apply-template` 验证：模型输入仅保留用户内容，测试系统提示词和 system 消息在入口被移除；流式回答仍正常。聊天角色分隔符与模型自身已训练的行为仍保留。浏览器旧会话中显示的系统提示词文本也由 8087 入口移除。

## 第 6 小节：上下文对照

在本目录执行 `python3 context_demo.py`，对比“空白上下文”“带历史”“移除历史”“只有文件名”“读入正文”这五种请求。使用相邻的虚构 `教学样品记录.txt`，读取范围限定在教学文件。添加 `--output report.json` 可保存完整输入、格式化模板、长度和真实模型结果。

[上下文实测.json](上下文实测.json)记录简化输入后的实际结果；[上下文实测_初次失败.json](上下文实测_初次失败.json)保留较复杂输入下五种场景均作保守答复的第一次尝试与回答原文。两次提示各有差别，适合观察提示变化带来的结果差异；小模型利用资料的效果需通过重复测试评估。

每次脚本请求从新会话开始；带历史场景由脚本显式提供前一轮消息。“收到记录。”是预写的对话示意，最终答案由模型生成；读文件场景由 Python 主动读入并提交正文。课堂说明这些步骤各自由脚本和模型完成。
