# 显微图来源

课堂主案例为以下三张 TiO₂ 电镜图，均来自 [BAM 研究团队公开数据](https://github.com/BAMresearch/automatic-sem-image-segmentation/tree/master/Datasets/Electron%20Microscopy%20Images)。

> **SEM（Scanning Electron Microscopy，扫描电子显微术）**：通过扫描电子束获得样品表面相关信息的成像方法。**TSEM（Transmission Scanning Electron Microscopy，透射扫描电子显微术）**：在扫描过程中利用透射电子形成图像的方法。

| 文件 | 来源 | 课堂用途 |
| --- | --- | --- |
| `09_TiO2_SEM_1908248.tif` | BAM，SEM / `1908248.tif` | 主案例：TiO₂ 颗粒的二维投影面积、周长与团聚现象 |
| `10_TiO2_SEM_1908250.tif` | BAM，SEM / `1908250.tif` | 第二个视野：观察稀疏颗粒与小目标 |
| `11_TiO2_TSEM_1908249.tif` | BAM，TSEM / `1908249.tif` | 透射对比度下的颗粒边界 |

另保留两张 [Cellpose 官方在线演示](https://huggingface.co/spaces/mouseland/cellpose/tree/main/samples) 示例图，作备用观察，不进入主流程：

| 文件 | 来源 | 备用用途 |
| --- | --- | --- |
| `07_cellpose_039_img.png` | Cellpose 官方 `039_img.png` | 杆状与球状目标的形貌差异 |
| `08_cellpose_033_img.png` | Cellpose 官方 `033_img.png` | 多边形颗粒的接触边界与周长 |

BAM 数据集的研究对象为 TiO₂ 颗粒，相关研究为 [Rühle、Krumrey 和 Hodoroaba：Workflow towards automated segmentation of agglomerated, non-spherical particles from electron microscopy images using artificial neural networks](https://doi.org/10.1038/s41598-021-84287-6)。

五个原始文件均按课程顺序重命名，像素与文件内容保持原样。`案例来源.json` 保存下载地址和文件校验值。BAM 原图为 768×1024 像素，Notebook 分析前 712 行，底部 56 行仪器信息保留在原文件中。物理尺寸标定应结合原图标尺、视野宽度或仪器元数据完成；Notebook 默认使用像素单位。

来源项目的许可说明：[Cellpose 项目与数据说明](https://github.com/MouseLand/cellpose)、[官方演示仓库说明](https://huggingface.co/spaces/mouseland/cellpose/blob/main/README.md)、[BAM 数据许可](https://github.com/BAMresearch/automatic-sem-image-segmentation/blob/master/LICENSE)。BAM 图像数据采用 CC BY-NC-ND 4.0；Cellpose 项目对其标注数据集标注为 CC BY-NC。随材料保留原始图和来源信息；分析结果由 Notebook 在本地 `outputs` 中生成。

五张图的原始下载可用 `uv run python download_examples.py` 复现，脚本逐一核对文件校验值。

## 示意图

`figures/` 存放 README 和[课堂讲义](../课堂讲义.md)使用的说明图，全部由本课程脚本基于 `素材/` 中的图和 `scripts/fixtures/` 的几何参考图生成，不引入额外下载的第三方图片：

| 文件 | 内容 | 数据来源 |
| --- | --- | --- |
| `fig_pipeline.png` | 原图 → 模型 → 标签图 → 测量表 | `scripts/fixtures/03_particles.png` 与参考标签 |
| `fig_semantic_instance.png` | 语义分割与实例分割对比 | `scripts/fixtures/03_particles.png` 与参考标签 |
| `fig_label_map.png` | 编号矩阵、编号 1 的二值掩膜、整图叠加 | `scripts/fixtures/03_particles_reference_mask.tif` |
| `fig_edge_removal.png` | 边缘剔除前后：9 个 → 保留 5 个 | `scripts/fixtures/03_particles_reference_mask.tif` |
| `fig_tio2_roi.png` | 分析区、标尺与像素尺寸换算 | `09_TiO2_SEM_1908248.tif` 的信息栏 |
| `fig_agent_loop.png` | 学生与 Agent 的协作循环 | 课程绘制 |
| `fig_case09_original.png` | 09 图分析区原图 | `09_TiO2_SEM_1908248.tif` 前 712 行 |
| `fig_case09_labels.png` | 09 图的彩色实例标签 | `outputs` 中的 cpsam 预测 |
| `fig_case09_result.png` | 原图、214 个实例、保留/边缘轮廓三联图 | `outputs` 中的 cpsam 预测 |
| `fig_case07_overlay.png` | 07 图保留（绿）与边缘（红）轮廓 | `outputs` 中的 cpsam 预测 |
| `fig_case08_overlay.png` | 08 图保留（绿）与边缘（红）轮廓 | `outputs` 中的 cpsam 预测 |

示意图重新生成（依赖 numpy、matplotlib、scikit-image、tifffile）：

```bash
uv run python scripts/make_figures.py
```

案例结果图需要先跑预测，再从 `outputs` 生成：

```bash
uv run python run_examples.py 09_TiO2_SEM_1908248.tif 07_cellpose_039_img.png 08_cellpose_033_img.png
uv run python scripts/make_case_figures.py
```

图中的中文使用系统自带字体（Windows 为微软雅黑），其他系统会回退到常见开源中文字体。TiO₂ 实测计数见 [验证记录](../验证记录.md)。
