# 最小 Harness：让本地模型请求真实工具

配合[第 7 小节](../../内容/04_AI与Agent的工作方式/07_文本命令与Agent_Harness.md)。只用 Python 标准库和已经运行的 Qwen3-0.6B 本地服务，不依赖 Agent 框架，不安装新模型。

## 现场运行

先按[本地模型说明](../本地语言模型/README.md)启动 WSL GPU 服务，保持系统提示词关闭。然后在本目录运行：

```bash
python3 harness.py --pause
```

每按一次 Enter，模型真实生成下一步请求，程序解析并执行，打印结果。默认任务是“读取教学样品记录、计算圆面积、保存报告、结束”。运行记录和报告放入新建的 `outputs/时间戳/`；重复运行不覆盖既有目录。

不暂停运行：

```bash
python3 harness.py
```

对照只读任务：

```bash
python3 harness.py --task read --pause
```

改用半径为 3 的文件：

```bash
python3 harness.py --record data/sample_radius3.json
```

默认 `data/sample.json` 的半径为 2，面积约 12.57 mm²；替代记录的半径为 3，面积约 28.27 mm²。都是虚构教学数据，不演示接触角识别。

## 代码分工

[harness.py](harness.py)包含三部分：

1. `choose_action`：把任务、工具说明和历史发送给真实模型，用 JSON Schema 约束输出格式。
2. `Tools`：注册并执行四个固定动作。文件路径由教师启动时指定，半径来自读取的记录；模型在这个简化协议中不生成路径或数值参数。
3. `run`：循环请求、解析、执行、反馈、检查完成并记录全过程。

每轮发送四个候选动作，模型选择其中一个；没有按轮次把下一步答案塞给模型。任务提示明确建议了顺序，因此这是**受指导的工具循环**，不是自由规划能力测试。

JSON 格式约束只限制可输出的形状和动作名称，不保证选择顺序正确。请求形如 `{"action":"circle_area"}`，这是课程自定义协议，不是服务原生 `tool_calls` 或完整 function calling 协议。

`write_report` 使用固定模板，把工具已核对的记录与面积写成 Markdown；不是模型自由撰写报告。模型负责提出调用请求，Python 负责实际读写、计算和核对。

## 上下文、程序状态与记忆

本框架既管理模型输入，也管理工具执行和停止条件，不只是转发提示词。

- `messages` 保存本次对话历史，提交给模型后成为上下文；当前没有历史压缩或检索。
- `Tools.record`、`Tools.area`、`Tools.report` 保存执行状态，供 Python 工具使用；模型只有在结果明确加入消息后才看到相应内容。
- `trace.json` 是供人核查的执行记录，不会自动作为长期记忆读回模型。
- 每次启动都新建消息与状态，不跨运行自动恢复记忆，也不修改模型权重。

没有使用第三方 Agent 框架；命令行、日志和暂停功能是为课堂观察增加的辅助部分。完整解释见[第七节中的职责与记忆说明](../../内容/04_AI与Agent的工作方式/07_文本命令与Agent_Harness.md)。

## 实际验证与保留记录

当前 WSL / Qwen3-0.6B Q8_0 的真实运行记录位于 [examples](examples/成功执行.json)：

| 案例 | 观察结果 |
| --- | --- |
| [默认完整任务](examples/成功执行.json) | 真实请求 read_record → circle_area → write_report → finish |
| [实际生成报告](examples/实际生成报告.md) | DROP-07，半径 2 mm，面积 12.57 mm² |
| [半径改为 3](examples/半径改为3.json) | 读取 DROP-08，实际算出 28.27 mm² |
| [只读任务](examples/只读任务.json) | 读取后结束，没有写报告 |
| [初次较长提示失败](examples/初次失败.json) | 跳过计算并反复请求结束，程序拒绝，到上限停止 |
| [文件缺失](examples/文件缺失.json) | 报读取失败，拒绝宣布完成，没有生成报告 |
| [不回传工具结果](examples/未反馈结果.json) | 仍按固定任务顺序完成，见下方解释 |

不反馈结果的对照可用 `python3 harness.py --drop-feedback --max-steps 5` 重跑。它只省略模型上下文中的工具结果，不关闭工具真实执行；日志仍完整记录。

**本任务的步骤提示很明确，因此没有反馈时也可能走完。**这不证明工具反馈不重要，而是说明该案例无法单独证明模型依赖返回结果作决策。对于根据内容、错误分支或参数选择下一步的复杂任务，需要另设计对照。课堂不将这条记录描述为失败。

运行依赖真实模型，输出可能随提示与配置变化；失败不会由预写调用替代。默认最多 8 步，可用 `--max-steps` 在 1—20 范围调整；停止、错误和成功都写入 trace.json。示例历史中的失败如实保留。

## 验证

运行 `python3 -m unittest discover -s . -p 'test_*.py'` 可离线检查执行边界：禁止跳过前置步骤、未知请求、不合适半径、只读任务写入，以及报告是否真正使用文件内容。真实模型验证另见上述记录；离线测试不模拟或证明模型能力。

## 来源

工具、框架、数据、报告模板与讲解均为课程编写。[Hugging Face 工具使用说明](https://huggingface.co/docs/transformers/chat_extras)用于对照模型请求与程序执行的边界；[Anthropic 的简单工作流与 Agent 讨论](https://www.anthropic.com/research/building-effective-agents)供教师选读。未复制第三方框架或代码。

## 第 8 小节：让模型生成数值参数

[tools_with_args.py](tools_with_args.py)沿用本地服务，仅演示一次带参数调用及反馈，不替换上一节的循环框架。

```bash
python3 tools_with_args.py --radius-mm 2 --pause
python3 tools_with_args.py --radius-mm 3
python3 tools_with_args.py --radius-mm 2 --skip-execution
python3 tools_with_args.py --radius-mm -2
```

第一条在模型真实生成请求后暂停，此时尚未计算；按 Enter 才执行。第三条只请求模型生成调用 JSON，不执行、不生成最终回答。负半径按预期被拒绝，退出码为 1。

本例将 `name` 与 `arguments.radius_mm` 放入 JSON，以 Schema 约束格式，但仍检查半径是否保留任务给定值、是否非负有限。调用成功后回传真实工具结果，再由模型生成说明；完成标志只表示工具计算成功，不自动证明模型措辞准确。

它是自定义协议，不是原生 `tool_calls`；消息均为 user/assistant，没有开启 system 提示词。没有提供真实工具定义给模型模板，也没有为本演示启用额外的工具系统消息。

实际记录：[半径 2](examples/带参数_半径2.json)、[半径 3](examples/带参数_半径3.json)、[未执行](examples/带参数_未执行.json)、[负半径](examples/带参数_负半径.json)。这些均为本机真实请求和输出，原生调用报文仅在讲义中作格式对照。
