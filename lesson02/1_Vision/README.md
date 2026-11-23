# Vision：计算机视觉先导

[返回第二课入口](../README.md) · [返回课程首页](../../README.md)

本目录放 MNIST 之前的先导材料，以及配套图片和生成脚本。

## 材料

- [从投稿图到像素：计算机视觉先导](计算机视觉先导.md) —— 主文档
- [素材与来源](assets/来源说明.md)
- [图片生成脚本](scripts/make_assets.py) —— 重新生成全部图表
- [格式对比样例](assets/format_samples/) —— 同一张图的 PNG/BMP/TIFF/JPEG 文件
- [MNIST 手写数字识别课堂实战](../MNIST/README.md)

## 主文档讲什么

1. 从 Wiley / ACS 的投稿图要求切入：矢量图、位图、dpi、RGB/CMYK；
2. 计算机怎样识别矢量图与位图；
3. 灰度、RGB、CMYK，以及一个像素到底用几个字节/几位十六进制表示；
4. 未压缩大小怎么算，RAW 例子，PNG 是否无损；
5. JPEG、TIFF、BMP 等格式的压缩与选择；
6. 计算机读图流程；MNIST 的 IDX 格式与张量形状；
7. 猫狗分类要多做什么预处理。

## 建议讲法（约 90 分钟）

| 时间 | 内容 | 重点 |
| --- | --- | --- |
| 0:00–0:10 | 投稿要求 + 矢量/位图 | 为什么 EPS 不受 dpi 限制 |
| 0:10–0:25 | 像素、灰度、RGB、CMYK | 一个像素到底几个字节 |
| 0:25–0:40 | 图像大小、RAW、PNG | 亲手算一遍字节数 |
| 0:40–0:55 | JPEG/TIFF/BMP、有损/无损 | 看格式对比图 |
| 0:55–1:15 | 读图流程 + MNIST IDX | 从文件到 `[64,1,28,28]` |
| 1:15–1:30 | 猫狗示例与讨论 | 真实图像多了什么 |

## 重新生成图片

在课程根目录运行：

```bash
python lesson02/Vision/scripts/make_assets.py
```

依赖 Pillow、numpy、matplotlib。MNIST 样张需要先运行过 `lesson02/MNIST` 的数据下载。

## 相关课程

- [MNIST 手写数字识别课堂实战](../MNIST/README.md)
- [第一课入口](../../lesson01/README.md)
