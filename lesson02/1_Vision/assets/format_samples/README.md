# 同一张图的六种存法

这些文件都由 `512×512` 的同一张 RGB 图（`assets/chelsea.png`）生成，用来比较格式与体积。生成脚本见 [../../scripts/make_assets.py](../../scripts/make_assets.py)。

| 文件 | 格式 | 大小 | 说明 |
| --- | --- | ---: | --- |
| `chelsea.png` | PNG | 361,601 B | 无损，DEFLATE |
| `chelsea.bmp` | BMP | 786,486 B | 通常不压缩；786,432 像素 + 54 字节头 |
| `chelsea_deflate.tif` | TIFF + Deflate | 679,844 B | 无损；TIFF 是容器 |
| `chelsea_q95.jpg` | JPEG q95 | 81,858 B | 有损，质量高 |
| `chelsea_q75.jpg` | JPEG q75 | 34,669 B | 有损，常用质量 |
| `chelsea_q30.jpg` | JPEG q30 | 17,539 B | 有损，明显失真 |

可以这样观察：

1. 用图片查看器打开 `chelsea.png` 和 `chelsea_q30.jpg`，放大猫眼睛和胡须，比较边缘。
2. 用十六进制编辑器打开 `chelsea.bmp` 和 `chelsea_q95.jpg`，看文件头：BMP 以 `42 4D`（`BM`）开头，JPEG 以 `FF D8 FF` 开头。
3. 用 `file` 命令或 Python 的 `PIL.Image.open` 检查格式，不要只看后缀。

注意：文件大小会随图片内容变化。这组数字只用于课堂对比，不是格式的固定比率。
