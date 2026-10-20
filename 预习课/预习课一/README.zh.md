# 预习课一：学会如何用搜索解决问题，认识你的计算机

**计算机很棒，但计算机也很笨。**它能完成很多任务，却需要你把每个细节都以它熟悉的语言表达出来。这次预习，我们先学习如何用搜索解决问题，再看看打开一个程序时，计算机内部大致发生了什么。放轻松，你不需要具备任何计算机基础也可以开始。

`materials/` 中的阅读材料存放在这个文件夹内，可以在本地打开。观看视频和下载软件仍需要使用浏览器。

## 这次要做什么

1. 观看 SI100+ 的两节视频：搜索解决问题、计算机基本知识。
2. 阅读相应的本地资料，包括《你缺失的那门计算机课》的两个章节。
3. 安装 Visual Studio Code（简称 VS Code），用它打开**整个文件夹**，并以Markdown的形式查看这份文档（也许会打开一个新世界）。

如果你已经了解某个主题，可以跳过相关章节。

## 一、从一个问题开始，学习搜索

在 [SI100+ B 站视频合集](https://www.bilibili.com/video/BV12L8r6MEn9/)中观看**“如何用搜索解决问题”**。可以打开本地的 [SI100+ 2024 搜索讲义](materials/si100plus-2024/search/Lecture_x_Search.md)对照学习，也可以在浏览器中查看[网页版讲义](https://github.com/teafrogsf/SI100Plus/blob/58ee452e61b462cc70127e8bcc851bb2e022a0b3/Lecture_x_Search/Lecture_x_Search.md)。

然后阅读本地的[《遇到问题怎么办》](materials/missing-web/how-to-find-solutions.md)，这是《你缺计课》[官网同名章节](https://www.criwits.top/missing/how-to-find-solutions.html)的本地阅读版。书中的例子以 Windows 为主，但如何用搜索解决问题的方法也适用于其他系统。

想象一下：一个文件打不开。只说“电脑坏了”，别人很难帮你判断。更有用的描述要说清楚：**你想做什么、做了什么、实际发生了什么**。如果屏幕出现报错，保留它的原文。搜索时可以先用程序名称和报错文字组成简短关键词；结果不符合自己的软件或版本，就调整关键词再试。

遇到问题时，除了使用搜索引擎、请教别人，现在也可以问 AI。AI 对话工具允许你像聊天一样输入问题，再根据回答继续追问。无论问谁，都尽量说清楚**想做什么、做了什么、实际发生了什么**，这有助于问题的解决。下面是一些可以尝试的入口，任选一个即可：

| 地区 | AI 对话工具 | 网页入口 |
|---|---|---|
| 国内 | DeepSeek | [打开 DeepSeek](https://chat.deepseek.com/) |
| 国内 | Kimi | [打开 Kimi](https://www.kimi.com/) |
| 国外 | ChatGPT | [打开 ChatGPT](https://chatgpt.com/) |
| 国外 | Claude | [打开 Claude](https://claude.ai/) |
| 国外 | Gemini | [打开 Gemini](https://gemini.google.com/) |

搜索结果和 AI 的回答都是线索，不是正确性的证明。尽量找到原始出处，核对它是否适用于自己的情况，再验证建议是否有效。你可以用 AI 帮助理解陌生术语，但关键说法仍要用资料或一次小实验核对。

**试着选一个问题练习：**“为什么计算机同时需要内存和存储设备？”“文件打不开时，我该怎样描述问题，才能让搜索引擎、同学或 AI 更好地帮我？”或者“除了搜索引擎和请教别人，我还能使用哪些 AI 对话工具？”先自己尝试寻找答案，再用自己的话说说你是怎样核对的。

## 二、认识屏幕背后的计算机

在同一个 [SI100+ 视频合集](https://www.bilibili.com/video/BV12L8r6MEn9/)中观看**“计算机基本知识”**。需要回顾时，可以打开本地的 [SI100+ 2024 计算机基础讲义](materials/si100plus-2024/basics/Lecture_i_Basic_Knowledge.md)，也可以在浏览器中查看[网页版讲义](https://github.com/teafrogsf/SI100Plus/blob/58ee452e61b462cc70127e8bcc851bb2e022a0b3/Lecture_i_Basic_Knowledge/Lecture_i_Basic_Knowledge.md)。接着阅读本地的[《认识你的电脑》](materials/missing-web/computer-and-its-components.md)，它对应《你缺计课》的[官网章节](https://www.criwits.top/missing/computer-and-its-components.html)。先关注 CPU、内存、存储设备、软件和操作系统；产品名称与型号可以留到以后了解。

先建立这样一幅简单的图景：

| 名词 | 先怎样理解 | 例子 |
|---|---|---|
| **硬件** | 可以触摸到的物理部件 | CPU 芯片、存储设备 |
| **软件** | 让硬件完成任务的指令和数据 | 浏览器、VS Code |
| **CPU** | 执行程序中许多指令的部件 | 进行一次计算 |
| **内存（RAM）** | 程序运行时使用的工作空间 | 暂时保存你正在编辑的文档内容 |
| **存储设备** | 程序关闭或断电后，文件仍能留存的地方 | 已保存的这份预习材料 |
| **操作系统** | 帮助程序使用硬件，并管理文件和运行中程序的软件 | Windows、macOS、Linux |

双击程序图标时，鼠标提供了一个**输入**。操作系统从存储设备找到程序文件并启动它。计算机把所需的指令和数据放进内存，CPU 执行指令，屏幕显示**输出**。这幅图景省略了很多细节，但可以帮助我们理解一个重要区别：**存储设备上保存的文件，与内存中正在运行的程序不是一回事。**

阅读这一节时，如果遇到不懂的地方，可以用刚学到的方法尝试寻找答案，我们也鼓励大家自行学习SI 100+ 和《你缺计课》的其他章节。

## 三、动手任务：用 VS Code 打开这个文件夹

VS Code 是一个**编辑器**，帮助我们打开和修改文件。后续课程会学习怎样把编辑器与 Python 环境配合起来；本次只需学会打开和阅读 Markdown。

1. 从 [VS Code 官方下载页](https://code.visualstudio.com/download)选择适合自己操作系统的版本并安装。已经安装的同学使用现有版本即可。
2. 打开 VS Code，选择**文件 → 打开文件夹**（File → Open Folder），选中整个 `预习课一` 文件夹。左侧文件列表应当能看到 `README.md`、`README.zh.md` 和 `materials`。
3. 在左侧列表中点击 `README.md`。这时看到的是 **Markdown** 文件的原始文字。Markdown 用简单符号给纯文本添加结构：`#` 表示标题，`-` 表示列表项，`[名称](链接)` 表示链接。有兴趣的同学可以在 [Markdown 语法说明](https://www.markdownguide.org/basic-syntax/)中了解更多。
4. 按 **Ctrl+Shift+V**（Windows/Linux）或 **Shift+Command+V**（macOS）打开预览，对照原文和排版后的样子。点击上文的一个**本地阅读链接**，它应当在 VS Code 中打开这个文件夹里的另一份材料；在线链接则会打开浏览器。
5. 分别在原文和预览中找出一个标题、一个列表和一个链接。愿意进一步尝试的话，可以复制这份导读，修改副本并观察预览如何变化。

VS Code 自带 Markdown 预览。如果遇到困难，试着用刚学的方法找答案。[VS Code 官方 Markdown 说明](https://code.visualstudio.com/docs/languages/markdown)列出了预览的操作方法。

## 来源与致谢

视频和 2024 年讲义由 [SI100+ 团队](https://github.com/teafrogsf/SI100Plus)制作。《你缺计课》的两个章节由 Hans Wan 和 Windy Deng 撰写；可查看他们的[网站](https://www.criwits.top/missing/)及[来源与许可说明](materials/missing-web/SOURCE.md)。感谢两个团队分享这些学习资料。
