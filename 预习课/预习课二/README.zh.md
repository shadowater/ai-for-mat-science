# 预习课二：文件、Markdown 与文献来源

这次预习接续第一课，围绕一个虚构的表面实验小例子展开。你不需要写程序或分析曲线。可以预留约 2–3 小时，分几段完成。已经熟悉的步骤，快速核对后继续即可。

## 这次尝试什么

1. 找到文件，说出它的名称、后缀、位置和可能保存的内容。
2. 复制这个文件夹，修改一份简短的 Markdown 笔记，加入本地链接、图片和公式。
3. 比较文字可选择的 PDF 与只有图片的 PDF；记录一篇真实论文的来源。

[`materials/`](materials/) 里的小样例专为本课制作。请阅读本导读链接的材料，在**自己复制的文件夹**里尝试操作。只有补充阅读和原始来源页面需要联网。本课不要求账号、编程环境或提交作业。

## 一、找到你要用的文件

**文件**是保存下来的一个内容单元，比如笔记、图片或 PDF。**文件名**帮助你辨认它。**后缀**是文件名最后一个点号后的部分：`.md` 通常表示 Markdown 文本，`.pdf` 表示 PDF 文档，`.svg` 表示用文字描述的图片。后缀是线索，不是转换工具：把 `picture.svg` 改名为 `picture.pdf`，不会因此得到真正的 PDF。

**文件夹**可以放文件和其他文件夹。**路径**说明文件在哪里。`materials/figure.svg` 从本导读所在的文件夹出发，因此是**相对路径**。从电脑根目录或磁盘开始的路径，例如 `C:\Users\...` 或 `/Users/...`，是**绝对路径**。相对路径方便我们整体移动文件夹。

像预习课一那样，在 VS Code 中打开整个 `预习课二` 文件夹（文件 → 打开文件夹）。在左侧文件列表中找到 [`figure.svg`](materials/figure.svg)、[`sample.csv`](materials/sample.csv) 和 [`sample.json`](materials/sample.json)。**CSV** 是按行和列组织的文本；**JSON** 是用名称和值组织信息的文本。这里仅需辨认文件类型，科研用途留到后续课程。

**动手试试：**把整个 `预习课二` 文件夹复制到一个新位置，打开复制出来的文件夹。在这个副本的导读中点击 [`figure.svg` 链接](materials/figure.svg)，仍应能找到图片。如果链接失效，检查 `materials` 是否与 `README.md`、`README.zh.md` 一起移动。原文件夹保留作对照。

## 二、写一份可阅读的科研笔记

**Markdown** 是一种纯文本写法，用少量符号表示标题、列表、链接和图片，阅读工具可以把它们显示成排好版的内容。预习课一已经看过标题和链接。**源文件**是你编辑的文字；**预览**是阅读工具显示出来的样子，两者对应同一份保存的笔记。

在复制的文件夹里打开 [`materials/note.zh.md`](materials/note.zh.md)，再复制一份，命名为 `my-note.md`，放在 **`materials` 文件夹里**。修改样品名，增加一条列表内容，检查它指向 `figure.svg` 的链接能否打开。要在笔记中直接显示图片，写 `![简短描述](figure.svg)`；描述能在图片无法显示时告诉读者图片内容。只想链接文件而不直接显示图片，写 `[图片](figure.svg)`。

LaTeX 用文字命令描述文档结构和公式。有些 Markdown 阅读工具也能显示用 LaTeX 风格符号写的公式。把笔记中的行内公式 `$A=\pi r^2$` 改成 `$d=2r$`。这里美元符号标记公式；`\pi` 表示 π，`^2` 表示平方。改公式时保留两边的 `$`。较长的公式可以单独一行，前后使用 `$$` 标记。在 VS Code 中打开 Markdown 预览（Windows/Linux：**Ctrl+Shift+V**；macOS：**Shift+Command+V**），对照源文件和显示效果。如果换用其他阅读工具后只看见美元符号原文，可检查那个工具是否支持公式；你的源文件仍然是有效的 Markdown 文本。[VS Code 官方 Markdown 说明](https://code.visualstudio.com/docs/languages/markdown)介绍了预览和公式显示。

在 LaTeX 论文源文件里，`\section{Methods}`、`\includegraphics{figure.png}` 和 `\cite{paper-key}` 分别表示标题、插图和引用。反斜杠引出命令，花括号包住命令使用的内容。这里看懂这个模式就够了，本次不要求创建或编译一篇 LaTeX 论文。

**可选了解：**[Overleaf](https://www.overleaf.com/) 是在浏览器里编辑 LaTeX 项目的工具。期刊可能提供自己的[论文模板](https://www.overleaf.com/latex/templates/tagged/academic-journal)，也就是现成的排版起点。你可以找一份自己领域期刊的模板，并对照期刊的投稿说明确认它接受哪一版。本次不要求注册账号或写出论文。

## 三、看看 PDF 里有什么，论文来自哪里

**PDF** 描述文档页面。有些 PDF 保存了可选择、可复制的文字；另一些只有每页的图片，例如扫描纸张后得到的文件。**OCR（光学字符识别）**是让软件尝试把图片里的字变成文字。OCR 能让扫描件可搜索，但识别结果可能有错。有些 PDF 阅读器会自动运行 OCR，因此能选中扫描件里的字，并不一定说明原文件本来就有文字层。[Adobe 的说明](https://helpx.adobe.com/ae_en/acrobat/desktop/create-documents/scan-documents-to-pdfs/recognize-text.html)解释了这一区别。

用 PDF 阅读器打开两份**虚构的课程样例**：[`text-example.pdf`](materials/text-example.pdf) 和 [`image-only-example.pdf`](materials/image-only-example.pdf)。尝试在两份文件中选中“SAMPLE M-02”。文字版存有可选择的字；图片版只存有像素。如果你的阅读器在两份文件中都能选中文字，它可能自动使用了 OCR。本次不用自己运行 OCR。试着向同学解释：如果要让软件准确引用其中一句话，你会先尝试哪份文件？为什么仍要回到原页核对？

论文的 **DOI** 是标识这项成果的长期标识符；**元数据**是题名、作者、发表年份等描述信息。DOI 或搜索结果可以帮你找到原始出处，但它们不是论文全文，也不保证你能下载 PDF。[DOI 基金会](https://www.doi.org/the-identifier/what-is-a-doi/)介绍了这个标识；[Crossref 的元数据说明](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)展示了怎样查找登记过的记录。这里不需要调用 API。

阅读本地[文献记录](materials/paper-record.zh.md)；有网络时打开里面的出版方页面链接。在 `my-note.md` 中加入论文题名、第一作者、年份，以及可点击的 DOI 链接。联网时，对照出版方页面核对其中一项信息。这篇论文与接触角测量有关，后面的课程还会用到这个例子。本次不用下载或总结论文全文。

## 自己检查一下

- **整个文件夹**移动以后，你还能打开示意图链接吗？
- 修改后的笔记在 VS Code 预览里是否显示标题、列表、本地图片和 `$d=2r$`？
- 你能解释两份 PDF 的区别，并找到论文的 DOI 和出版方页面吗？

某一步失败时，记下文件名以及报错原文或实际现象。可以继续使用预习课一学到的搜索、求助方法。这些检查只用于帮助你学习，不要求提交。

## 来源与致谢

`materials/` 中的笔记、示意图、小数据文件及两份 PDF 都是为本课制作的；PDF 页面里的样品文字是虚构的。外部说明及真实论文只链接原始页面：[VS Code 的 Markdown 说明](https://code.visualstudio.com/docs/languages/markdown)、[Adobe 的 OCR 说明](https://helpx.adobe.com/ae_en/acrobat/desktop/create-documents/scan-documents-to-pdfs/recognize-text.html)、[DOI 基金会](https://www.doi.org/the-identifier/what-is-a-doi/)、[Crossref](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)；论文的出版方链接见[文献记录](materials/paper-record.zh.md)。本文件夹没有收录第三方论文的正文或图片。
