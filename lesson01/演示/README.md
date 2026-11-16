# 第一课演示与课堂样例：1.1—1.4.4

[返回第一课入口](../README.md)

## 1.2、1.3：计算、绘图与文件编码

打开[计算与文件编码 Notebook](计算与文件编码.ipynb)，在 Jupyter 或支持 Notebook 的编辑器中选择 Python 内核，依次运行三个代码单元格：

1. 计算半径 2 mm 的圆面积，核对约 12.57 mm²。
2. 绘制半径与面积的关系，修改半径观察圆点变化。
3. 读取课堂中文样例的字节，再用 UTF-8 解码，观察字节与字符的对应关系。

环境需要 `ipykernel` 和 `matplotlib`，可在本目录运行 `python -m pip install -r requirements.txt`。原含工具调用部分的完整 Notebook 已移至[归档](../归档/后续内容/演示/计算与工具调用.ipynb)。

- [CMD 演示图](cmd-example.svg)：Windows CMD 中创建并重命名文件夹。
- [0 与 1 文字图](binary-meme.svg)：配合二进制概念。
- [XML 样例](sample.xml)：虚构样品 M-02 的结构化记录。

## 课堂文件样例

以下文件使用虚构样品 M-02，供计算机与文件章节操作。课前检查仍使用 `课前准备/样例/`。

| 文件 | 课堂用途 |
| --- | --- |
| [sample.csv](sample.csv)、[sample.xlsx](sample.xlsx) | 对照纯文本表格与 Excel 工作簿 |
| [sample.json](sample.json)、[sample.xml](sample.xml) | 对照同一条样品信息的不同结构 |
| [sample.zh.txt](sample.zh.txt) | 练习用 UTF-8 与 GBK 读取中文文本 |
| [figure.svg](figure.svg)、[note.zh.md](note.zh.md) | 观察图片链接、Markdown 与公式预览 |
| [paper-record.zh.md](paper-record.zh.md) | 核对真实文献的 DOI 与出版信息 |
| [text-example.pdf](text-example.pdf)、[image-only-example.pdf](image-only-example.pdf) | 对照文字层 PDF 与图像层 PDF |
| [比例尺练习.svg](比例尺练习.svg) | 使用明确标定的教学示意图练习像素换算 |
| [公式速查.md](公式速查.md) | 查阅本课需要的 Markdown 公式写法 |

`M-02`、样品图片和比例尺练习均为教学示意。文献记录只包含题名、作者、年份、DOI 和出版方链接。两份单页 PDF 由课程组编写，其中一份包含页面文字，另一份包含同样内容的图像。

## 1.4.2：拟合与参数

- [Arrhenius 拟合](Arrhenius拟合/README.md)：原始参数、线性化和计算结果。
- [最小二乘动画](最小二乘/index.html)：用独立的教学数据观察参数、梯度下降和误差；[操作说明](最小二乘/README.md)。

## 1.4.3：聚类、降维与分类

[机器学习方法动画](机器学习方法/index.html)使用 178 个葡萄酒样品的化学测量数据，展示 K-Means、PCA 和 SVM。下载后可离线打开，数据来源见[说明](机器学习方法/README.md)。

## 1.4.4：分子描述符与神经网络

- [溶解度模型实验](溶解度模型/README.md)：数据、训练脚本与评估结果。
- [逐层计算附件](溶解度模型/网络逐层计算.md)：完整公式和 49 个参数。
- [训练与手动调参网页](溶解度模型/交互演示/index.html)：回放实际训练记录，修改参数并即时比较预测；[使用说明](溶解度模型/交互演示/README.md)。
- [分子表示演示](分子表示/index.html)：对照乙醇与二甲醚的连接环境；[说明](分子表示/README.md)。

## 后续材料

语言模型、词向量和 Harness 演示统一存放在[后续内容归档](../归档/后续内容/README.md)。
