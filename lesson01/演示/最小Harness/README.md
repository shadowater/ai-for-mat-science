# 最小 Harness：让本地模型请求真实工具

配合[第 7 小节](../../内容/04_AI与Agent的工作方式/07_文本命令与Agent_Harness.md)。使用 Python 标准库和已经运行的 Qwen3-0.6B 本地服务，由课程自编程序实现工具循环。

## 现场运行

先按[本地模型说明](../本地语言模型/README.md)启动 WSL GPU 服务，保持系统提示词关闭。然后在本目录运行：

```bash
python3 harness.py --pause
```

每按一次 Enter，模型真实生成下一步请求，程序解析并执行，打印结果。默认任务是“读取教学样品记录、计算圆面积、保存报告、结束”。每次运行创建一个新的 `outputs/时间戳/` 目录存放记录和报告。

连续运行：

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

默认 `data/sample.json` 的半径为 2，面积约 12.57 mm²；替代记录的半径为 3，面积约 28.27 mm²。两组数据用于演示圆面积计算；接触角识别另需图像测量流程。

## 代码分工

[harness.py](harness.py)包含三部分：

1. `choose_action`：把任务、工具说明和历史发送给真实模型，用 JSON Schema 约束输出格式。
2. `Tools`：注册并执行四个固定动作。文件路径由教师启动时指定，半径来自读取的记录；模型在这个简化协议中只生成动作名称。
3. `run`：循环请求、解析、执行、反馈、检查完成并记录全过程。

每轮发送四个候选动作，模型选择其中一个；下一步动作由模型根据任务提示和已给出的消息选择。任务提示明确建议了顺序，因此这是**受指导的工具循环**；自由规划能力需要另设开放任务评估。

JSON 格式约束限制输出形状和动作名称；选择顺序由模型在运行时决定，请结合执行记录核对。请求形如 `{"action":"circle_area"}`，采用课程自定义协议。服务原生 `tool_calls` 和完整 function calling 协议另有各自的消息结构。

`write_report` 使用固定模板，把工具已核对的记录与面积写成 Markdown。模型负责提出调用请求，Python 负责实际读写、计算和核对；报告正文由模板填充。

## 上下文、程序状态与记忆

本框架管理模型输入、工具执行和停止条件，涵盖完整的课堂工具循环。

- `messages` 保存本次对话历史，提交给模型后成为上下文；当前历史按原始消息顺序提供。
- `Tools.record`、`Tools.area`、`Tools.report` 保存执行状态，供 Python 工具使用；模型只有在结果明确加入消息后才看到相应内容。
- `trace.json` 是供人核查的执行记录；模型看到的内容由 `messages` 明确提供。
- 每次启动都新建消息与状态，模型权重保持原样；跨运行复用记录需要另行设计载入流程。

本例使用课程自编的 Python 程序；命令行、日志和暂停功能帮助课堂观察。完整解释见[第七节中的职责与记忆说明](../../内容/04_AI与Agent的工作方式/07_文本命令与Agent_Harness.md)。

## 实际验证与保留记录

当前 WSL / Qwen3-0.6B Q8_0 的真实运行记录位于 [examples](examples/成功执行.json)：

| 案例 | 观察结果 |
| --- | --- |
| [默认完整任务](examples/成功执行.json) | 真实请求 read_record → circle_area → write_report → finish |
| [实际生成报告](examples/实际生成报告.md) | DROP-07，半径 2 mm，面积 12.57 mm² |
| [半径改为 3](examples/半径改为3.json) | 读取 DROP-08，实际算出 28.27 mm² |
| [只读任务](examples/只读任务.json) | 读取后结束，输出为读取记录 |
| [初次较长提示失败](examples/初次失败.json) | 跳过计算并反复请求结束，程序拒绝，到上限停止 |
| [文件缺失](examples/文件缺失.json) | 报读取失败，完成条件保持待满足，输出记录保存了错误 |
| [省略工具结果反馈](examples/未反馈结果.json) | 仍按固定任务顺序完成，见下方解释 |

省略反馈的对照可用 `python3 harness.py --drop-feedback --max-steps 5` 重跑。工具真实执行，日志完整记录；模型上下文中省略工具结果。

**本任务的步骤提示很明确，省略反馈时模型也可能走完。**该记录说明模型可以沿提示中的固定顺序完成此任务；评估模型怎样利用工具反馈，需要另外设计含有内容分支、错误分支或参数选择的任务。课堂把这条记录作为对照案例展示。

运行依赖真实模型，输出可能随提示与配置变化；失败也按实际结果记录。默认最多 8 步，可用 `--max-steps` 在 1—20 范围调整；停止、错误和成功都写入 trace.json。示例历史中的失败如实保留。

## 验证

运行 `python3 -m unittest discover -s . -p 'test_*.py'` 可离线检查执行边界：程序要求前置步骤、识别未知请求、检查半径有效性、限制只读任务写入，并验证报告使用文件内容。真实模型的表现见上述运行记录；离线测试检查 Python 程序的规则。

## 来源

工具、框架、数据、报告模板与讲解均为课程编写。[Hugging Face 工具使用说明](https://huggingface.co/docs/transformers/chat_extras)用于对照模型请求与程序执行的边界；[Anthropic 的简单工作流与 Agent 讨论](https://www.anthropic.com/research/building-effective-agents)供教师选读。第三方材料通过链接供读者查看。

## 第 8 小节：让模型生成数值参数

[tools_with_args.py](tools_with_args.py)沿用本地服务，演示一次带参数调用及反馈；上一节的循环框架继续用于完整任务。

```bash
python3 tools_with_args.py --radius-mm 2 --pause
python3 tools_with_args.py --radius-mm 3
python3 tools_with_args.py --radius-mm 2 --skip-execution
python3 tools_with_args.py --radius-mm -2
```

第一条在模型真实生成请求后暂停，按 Enter 后执行计算。第三条展示模型生成的调用 JSON，执行状态保持在请求阶段。负半径触发工具校验错误，退出码为 1。

本例将 `name` 与 `arguments.radius_mm` 放入 JSON，以 Schema 约束格式，同时检查半径是否保留任务给定值，以及数值是否为大于等于零的有限数。调用成功后回传真实工具结果，再由模型生成说明；完成标志表示工具计算成功，模型措辞还需对照真实结果核查。

它采用课程自定义协议，消息均为 user/assistant。原生 `tool_calls`、模型模板中的工具定义和额外工具系统消息各有独立的实现方式，课堂在讲义中作格式对照。

实际记录：[半径 2](examples/带参数_半径2.json)、[半径 3](examples/带参数_半径3.json)、[未执行](examples/带参数_未执行.json)、[负半径](examples/带参数_负半径.json)。这些均为本机真实请求和输出，原生调用报文仅在讲义中作格式对照。
