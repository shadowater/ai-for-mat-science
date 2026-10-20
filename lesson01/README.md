# 正课第一课：从数据到科研工作流

这是教师审阅与试讲用的教学包。课堂以[模拟拉伸数据](data/tensile_demo.csv)练习找到输入文件、计算工程应力、核对单位和数值、保存结果，并说明工作流程。完整安排见[教学大纲](01_第一次课教学大纲.md)。

## 材料

- [课堂任务模板](task_template.md)与[数据说明](data/README.md)
- [Notebook](notebook/lesson01.ipynb)及[演示版](notebook/lesson01.slides.html)
- [Slidev 课件源稿](slidev/slides.md)及[已构建课件](slidev/dist/index.html)
- [课件使用说明](03_课件使用与方案比较.md)

## 本地试讲

在 `lesson01` 目录运行 `python scripts/demo_server.py`，然后打开 `http://127.0.0.1:8765/`。Windows 如没有 `python` 命令，可以试 `py -3 scripts/demo_server.py`。首页提供 Slidev 和 Notebook 两种演示方式。短代码演示使用本机 Python；完整 Notebook 需要另装依赖，见[课件使用说明](03_课件使用与方案比较.md)。

模拟数据仅供教学，不代表真实材料性能。现有课件已经构建；`slidev/node_modules` 是可重新安装的依赖，不包含在仓库中。
