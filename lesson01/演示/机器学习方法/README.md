# 真实化学测量数据：三种机器学习方法动画

配合[第 4 章第 3 节](../../内容/04_AI与Agent的工作方式/03_聚类降维与分类.md)。下载本目录后，在浏览器打开 `index.html`，选择 K-Means、PCA 或 SVM，再点击“播放动画”。页面直接读取同目录的 `wine-data.js` 和 `demo.js`，打开时无需联网。

## 数据与处理

数据采用 Aeberhard 与 Forina 的 [UCI Wine 数据集](https://archive.ics.uci.edu/dataset/109/wine)，共 178 个样品、13 项化学测量指标，按 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 许可使用。浏览器数据来自 `sklearn.datasets.load_wine()`；`prepare_wine.py` 记录了提取和计算步骤。

- **K-Means**：取酒精和苹果酸两列，各自减去均值再除以标准差；固定分为三组，初始中心由确定性的最远点方法选取。动画逐步执行最近中心分配和组内均值更新。K-Means 计算中没有使用品种标签。
- **PCA**：对全部 13 项指标逐列标准化，计算前两个主成分。动画先显示酒精与苹果酸的标准化散点图，再切换到主成分散点图；切换过程仅用于展示视图变化。
- **SVM**：用前两个主成分及数据集中的品种标签训练线性分类器。圆点显示数据集标签，淡色背景显示分类器在二维平面上的预测类别。此处展示训练数据上的边界。

所有点对应真实样品；K-Means 和 PCA 的二维坐标是从原始测量值计算得到的。页面中的组数、初始化和 SVM 参数用于课堂演示。

## 重新生成数据

具备 Python、NumPy 与 scikit-learn 的环境中，运行 `python prepare_wine.py` 可生成 `wine-data.js`。生成脚本使用 scikit-learn 内置的 UCI Wine 副本；学生播放动画只需要 HTML 和两个 JS 文件。

数据引用：Aeberhard, S. & Forina, M. (1992). *Wine* [Dataset]. UCI Machine Learning Repository. [doi:10.24432/C5PC7J](https://doi.org/10.24432/C5PC7J)。
