# 预习课二：文件、Markdown 与文献来源

这次预习接续第一课，围绕一个虚构的表面实验小例子展开。你不需要写程序或分析曲线。可以预留约 2–3 小时，分几段完成。已经熟悉的步骤，快速核对后继续即可。

## 这次尝试什么

1. 找到文件，说出它的名称、后缀、位置和可能保存的内容。
2. 复制这个文件夹，修改一份简短的 Markdown 笔记，加入本地链接、图片和公式。
3. 比较文字可选择的 PDF 与只有图片的 PDF；记录一篇真实论文的来源。

[`materials/`](materials/) 里有一份现有计算机课程的本地选读正文及配图，也有为本课制作的小样例。请阅读本导读链接的材料，在**自己复制的文件夹**里尝试操作。原始来源页面和可选参考资料需要联网。本课不要求账号、编程环境或提交作业。

## 一、找到你要用的文件

如果收到的是 ZIP 文件，先完整解压，再打开课程文件夹。ZIP 是把多个文件和文件夹打包在一起的一个文件。需要时参考[微软的解压说明](https://support.microsoft.com/en-us/windows/experience/storage-filemanagement/zip-and-unzip-files)或[苹果的解压说明](https://support.apple.com/guide/mac-help/zip-and-unzip-files-and-folders-on-mac-mchlp2528/mac)。在解压出来的文件夹中找到 `README.md`、`README.zh.md` 和 `materials`。

**文件**是保存下来的一个内容单元，比如笔记、图片或 PDF。**文件名**帮助你辨认它。**后缀**是文件名最后一个点号后的部分：`.md` 通常表示 Markdown 文本，`.pdf` 表示 PDF 文档，`.svg` 表示用文字描述的图片。后缀是线索，不是转换工具：把 `picture.svg` 改名为 `picture.pdf`，不会因此得到真正的 PDF。

让文件浏览器显示完整文件名：参考[微软的后缀名说明](https://support.microsoft.com/en-us/windows/experience/storage-filemanagement/common-file-name-extensions-in-windows)或[苹果的后缀名说明](https://support.apple.com/en-hk/guide/mac-help/mchlp2304/mac)。下面的本地读物使用 Windows 截图；Mac 用户可以按苹果的步骤完成这个动作。

**文件夹**可以放文件和其他文件夹。**路径**说明文件在哪里。`materials/figure.svg` 从本导读所在的文件夹出发，因此是**相对路径**。从电脑根目录或磁盘开始的路径，例如 `C:\Users\...` 或 `/Users/...`，是**绝对路径**。相对路径方便我们整体移动文件夹。

阅读本地带配图的[《文件、文件名和文件类型》与《文件夹、路径和目录》选段](materials/missing-web/file-and-file-management.md)，原作是 Hans Wan 和 Windy Deng 的《你缺失的那门计算机课》。作者网站上的[完整章节](https://www.criwits.top/missing/file-and-file-management.html)还有其他内容。预习课一读过的 [SI100+ 2024 计算机基础讲义](https://github.com/teafrogsf/SI100Plus/blob/58ee452e61b462cc70127e8bcc851bb2e022a0b3/Lecture_i_Basic_Knowledge/Lecture_i_Basic_Knowledge.md)也简要回顾了后缀名。在本地选段中找到目录树图片，再到 `file-and-file-management` 子文件夹里找到对应的 `Tree.png` 文件。若不阅读中文，可使用英文导读前面的定义和目录树图片。结合正文，在自己的电脑上辨认一个文件名和一条路径即可，不要求背诵章节内容。

像预习课一那样，在 VS Code 中打开整个 `预习课二` 文件夹（文件 → 打开文件夹）。在左侧文件列表中找到 [`figure.svg`](materials/figure.svg)、[`sample.csv`](materials/sample.csv) 和 [`sample.json`](materials/sample.json)。

**动手试试：**把整个 `预习课二` 文件夹复制到一个新位置，打开复制出来的文件夹。在这个副本的导读中点击 [`figure.svg` 链接](materials/figure.svg)，仍应能找到图片。如果链接失效，检查 `materials` 是否与 `README.md`、`README.zh.md` 一起移动。原文件夹保留作对照。

### 文本文件：把字符保存在文件里

**纯文本文件**保存的是字母、汉字、数字、标点和换行等字符。VS Code 这样的文本编辑器可以让你直接阅读和修改这些字符。纯文本文件不保存 Word 那样的字体选择、页面排版或嵌入的图片。Word 文档和 PDF 即使包含文字，也不等于纯文本文件。

在 VS Code 中打开 [`sample.zh.txt`](materials/sample.zh.txt)，它用普通句子描述本课的虚构样品。`.txt` 是纯文本常见的后缀，但不是唯一的后缀：这里的 `.csv`、`.json` 和 `.md` 文件也都是文本文件。不同格式规定了怎样组织或解释其中的字符。

### CSV：用文本保存一张表

**CSV** 是 **comma-separated values（逗号分隔的值）**的缩写，用文本保存表中的内容，通常用逗号分隔各列。在 VS Code 中打开 [`sample.csv`](materials/sample.csv)：

```csv
sample_id,file_name
M-02,figure.svg
```

这份文件第一行给出了两列的名称：样品编号和文件名。第二行是一条样品记录，逗号把 `M-02` 与 `figure.svg` 分开。电子表格软件可以把同一份文件显示成单元格；VS Code 显示的是它的文本。CSV 不保存 Excel 工作簿中的多个工作表、图表或单元格样式。它常用于交换样品清单、仪器读数这样的简单表格。

需要进一步了解时，选读[微软 CSV 说明](https://support.microsoft.com/en-us/excel/get-started/import-or-export-text-txt-or-csv-files)开头关于文本格式的介绍。实际文件可能使用其他分隔符；内容本身含逗号时还需要引号规则。本次不要求编辑这些情况。

### JSON：用文本保存有名称的信息

**JSON** 是 **JavaScript Object Notation** 的缩写，是一种保存和交换有组织的信息的文本格式。读懂它不需要先学习 JavaScript。打开 [`sample.json`](materials/sample.json)：

```json
{
  "sample_id": "M-02",
  "figure": "figure.svg",
  "fictional": true
}
```

这里的花括号 `{}` 包住一组**名称与值的配对**。冒号前的名称说明后面的值是什么：`"sample_id": "M-02"` 给出样品编号。各对信息用逗号隔开，名称和文字值用普通双引号包住。`true` 表示“是／真”，所以 `"fictional": true` 表示这个样品是虚构的。值还可以是数字、列表或另一组有名称的信息，这些情况以后再学。程序经常用 JSON 保存设置或返回信息，例如论文的题名与作者。

可复用的讲解见 [MDN 的 JSON 入门](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/JSON#no_really_what_is_json)，本次只选读“No, really, what is JSON?”一节。后面的 JavaScript 编程练习不属于本次预习。

**动手对照：**在复制的文件夹里，用 VS Code 打开 TXT、CSV 和 JSON 三份样例，在每份文件里找到 `M-02` 和 `figure.svg`。把 TXT 副本里的 `M-02` 改为 `M-03`，保存后重新打开。在 CSV 中指出列名和一条记录，在 JSON 中指出一个名称及其值。三者可以描述同一个样品，但组织文字的规则不同。修改后缀不会把文件内容自动改写成另一种格式。

## 二、写一份可阅读的科研笔记

**Markdown** 是一种纯文本写法，用少量符号表示标题、列表、链接和图片，阅读工具可以把它们显示成排好版的内容。预习课一已经看过标题和链接。**源文件**是你编辑的文字；**预览**是阅读工具显示出来的样子，两者对应同一份保存的笔记。

在源文件和预览中对照打开本地 [Markdown Guide 语法速查中文版](materials/markdown-guide/markdown-cheat-sheet.zh.md)，原作由 Matt Cone 与 Markdown Guide 贡献者提供。选读**标题、有序/无序列表、链接、图片、行内代码、围栏代码块**；需要详细解释时看[原站语法说明](https://www.markdownguide.org/basic-syntax/)。其余内容可选读，部分扩展写法不一定在所有阅读器中显示。公式请使用本课公式速查中的写法，而不是该文中的 `H~2~O` 或 `X^2^`。下面的本地示例笔记还链接回原阅读材料，可以看看怎样在 Markdown 文件中记录来源。

在复制的文件夹里打开 [`materials/note.zh.md`](materials/note.zh.md)，再复制一份，命名为 `my-note.md`，放在 **`materials` 文件夹里**。修改 `#` 后面的标题和样品名，增加一条列表内容，检查它指向 `figure.svg` 的链接能否打开。要在笔记中直接显示图片，写 `![简短描述](figure.svg)`；描述能在图片无法显示时告诉读者图片内容。只想链接文件而不直接显示图片，写 `[图片](figure.svg)`。

**代码块**会把几行文字按原样显示，适合保留报错或写法示例。在语法速查中找到“围栏代码块”，给笔记加一个内容为 `sample: M-02` 的代码块。它前后的标记各是三个反引号，不是引号。按 **Ctrl+S**（Windows/Linux）或 **Command+S**（macOS）保存，关闭笔记再重新打开，检查改动是否已保存。输入示例中的普通键盘符号；全角字符 `＃`、`＄` 与 `#`、`$` 是不同的字符。

LaTeX 用文字命令描述文档结构和公式。有些 Markdown 阅读工具也能显示用 LaTeX 风格符号写的公式。把笔记中的行内公式 `$A=\pi r^2$` 改成 `$d=2r$`。这里美元符号标记公式；`\pi` 表示 π，`^2` 表示平方。改公式时保留两边的 `$`。较长的公式可以单独一行，前后使用 `$$` 标记。在 VS Code 中打开 Markdown 预览（Windows/Linux：**Ctrl+Shift+V**；macOS：**Shift+Command+V**），对照源文件和显示效果。如果换用其他阅读工具后只看见美元符号原文，可检查那个工具是否支持公式；你的源文件仍然是有效的 Markdown 文本。[VS Code 官方 Markdown 说明](https://code.visualstudio.com/docs/languages/markdown)介绍了预览和公式显示。

本地[公式速查](materials/math-in-markdown.zh.md)展示行内与独占一行的公式、上下标、希腊字母、分数、根号和单位。请在复制的笔记中完成其中两个简短动作；表格可留作以后查阅。[GitHub 官方公式说明](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions)介绍了这些写法在本仓库页面上的显示方式。

在 LaTeX 论文源文件里，`\section{Methods}`、`\includegraphics{figure.png}` 和 `\cite{paper-key}` 分别表示标题、插图和引用。反斜杠引出命令，花括号包住命令使用的内容。这里看懂这个模式就够了，这些文档命令用于 `.tex` 论文源文件；放在 Markdown 中不会自动变成排好版的标题、图片或引用。本次不要求创建或编译一篇 LaTeX 论文。

**可选了解：**[Overleaf](https://www.overleaf.com/) 是在浏览器里编辑 LaTeX 项目的工具。期刊可能提供自己的[论文模板](https://www.overleaf.com/latex/templates/tagged/academic-journal)，也就是现成的排版起点。你可以找一份自己领域期刊的模板，并对照期刊的投稿说明确认它接受哪一版。想看源文件怎样变成 PDF，可选读 [Overleaf 入门教程](https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes)中的“What is LaTeX?”和“Writing your first piece of LaTeX”两节，对照短源文件与展示的结果。本次不要求注册账号或写出论文。

## 三、看看 PDF 里有什么，论文来自哪里

**PDF** 描述文档页面。有些 PDF 保存了可选择、可复制的文字；另一些只有每页的图片，例如扫描纸张后得到的文件。**OCR（光学字符识别）**是让软件尝试把图片里的字变成文字。OCR 能让扫描件可搜索，但识别结果可能有错。有些 PDF 阅读器会自动运行 OCR，因此能选中扫描件里的字，并不一定说明原文件本来就有文字层。[Adobe 的说明](https://helpx.adobe.com/ae_en/acrobat/desktop/create-documents/scan-documents-to-pdfs/recognize-text.html)解释了这一区别。

用 PDF 阅读器打开两份**虚构的课程样例**：[`text-example.pdf`](materials/text-example.pdf) 和 [`image-only-example.pdf`](materials/image-only-example.pdf)。尝试在两份文件中选中“SAMPLE M-02”。文字版存有可选择的字；图片版只存有像素。如果你的阅读器在两份文件中都能选中文字，它可能自动使用了 OCR。本次不用自己运行 OCR。试着向同学解释：如果要让软件准确引用其中一句话，你会先尝试哪份文件？为什么仍要回到原页核对？

论文的 **DOI** 是标识这项成果的长期标识符；**元数据**是题名、作者、发表年份等描述信息。DOI 或搜索结果可以帮你找到原始出处，但它们不是论文全文，也不保证你能下载 PDF。[DOI 基金会](https://www.doi.org/the-identifier/what-is-a-doi/)介绍了这个标识；[Crossref Metadata Search](https://search.crossref.org/)可以在浏览器中按题名查找论文，其[检索帮助](https://search.crossref.org/help/works)说明了可用的检索方式。需要时，将示例论文题名粘贴进去，对照出版方页面查看结果。用程序获取文献记录留到后面的文献实践。

阅读本地[文献记录](materials/paper-record.zh.md)；有网络时打开里面的出版方页面链接。在 `my-note.md` 中加入论文题名、第一作者、年份，以及可点击的 DOI 链接。联网时，对照出版方页面核对其中一项信息。这篇论文与接触角测量有关，后面的课程还会用到这个例子。本次不用下载或总结论文全文。

## 自己检查一下

- 你能解释为什么 TXT、CSV 和 JSON 都是文本文件，并指出 CSV 的一列和 JSON 的一对名称与值吗？
- **整个文件夹**移动以后，你还能打开示意图链接吗？
- 修改后的笔记在 VS Code 预览里是否显示修改后的标题、列表、本地图片、代码块、`$d=2r$` 和独占一行的公式？
- 你能解释两份 PDF 的区别，并找到论文的 DOI 和出版方页面吗？

某一步失败时，记下文件名以及报错原文或实际现象。可以继续使用预习课一学到的搜索、求助方法。这些检查只用于帮助你学习，不要求提交。

## 来源与致谢

本地选段和八张配图来自 [Hans Wan 与 Windy Deng 的《你缺失的那门计算机课》](materials/missing-web/SOURCE.md)，来源、版本、许可和改动均记录在选段旁。本地 [Markdown Guide 语法速查](materials/markdown-guide/SOURCE.md)按 CC BY-SA 4.0 复用，增加了中文翻译并调整了图片链接。示例笔记、公式速查、示意图、小数据文件及两份 PDF 是为本课制作的；PDF 页面里的样品文字是虚构的。其他说明链接到原始页面：[SI100+ 2024 讲义](https://github.com/teafrogsf/SI100Plus/blob/58ee452e61b462cc70127e8bcc851bb2e022a0b3/Lecture_i_Basic_Knowledge/Lecture_i_Basic_Knowledge.md)、[Markdown Guide](https://www.markdownguide.org/basic-syntax/)、[VS Code 的 Markdown 说明](https://code.visualstudio.com/docs/languages/markdown)、[GitHub 的公式说明](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions)、[Adobe 的 OCR 说明](https://helpx.adobe.com/ae_en/acrobat/desktop/create-documents/scan-documents-to-pdfs/recognize-text.html)、[DOI 基金会](https://www.doi.org/the-identifier/what-is-a-doi/)、[Crossref](https://search.crossref.org/)；论文的出版方链接见[文献记录](materials/paper-record.zh.md)。本文件夹没有收录第三方科研论文的正文或图片。
