# 第二课：计算机视觉与 MNIST

本课先读 **Vision** 的计算机视觉先导，再做 **MNIST** 手写数字识别实战。目录另附 **Cellpose** 颗粒分割与尺寸测量，作为后续的图像分割实践。

## 材料

### Vision：计算机视觉先导

- [Vision 目录说明](1_Vision/README.md)
- [从投稿图到像素：计算机视觉先导](1_Vision/计算机视觉先导.md) —— 主文档
- [素材与来源](1_Vision/assets/来源说明.md)

### MNIST 手写数字识别

- [90 分钟课堂实战](MNIST/README.md)
- [学生 Agent 提示词卡](MNIST/课堂提示词_新.md)

### Cellpose 颗粒分割与测量（后续实践）

- [课堂说明：概念、90 分钟流程与教师准备](4cellpose/README.md)
- [学生 Agent 提示词卡](4cellpose/课堂提示词.md)
- [参考 Notebook 与显微图案例](4cellpose/颗粒分割与测量.ipynb)

## 建议顺序

1. 先读 Vision：理解矢量/位图、RGB/CMYK、图像大小与格式、计算机如何读图。
2. 再做 MNIST：用 Agent 调 PyTorch，完成训练、测试与错例分析。
3. 有余力再讨论猫狗分类的预处理差异。
4. 之后做 Cellpose：先理解语义分割与实例分割，再用 Agent 完成分割、计数、测量和边缘剔除。

Cellpose 部分承接 MNIST 的 Agent 用法，但任务从“分类”换成“分割”：输出不再是一个类别，而是与原图同样大小的编号图。课堂上不展开模型内部结构，重点放在标签图、叠加轮廓和测量结果上。

## 返回

[第一课入口](../lesson01/README.md) · [课程首页](../README.md)
