# Markdown 公式速查

这份材料由本课程编写。配合[预习课二导读](../README.zh.md)及你复制的 `my-note.md` 使用。你只需尝试**一个行内公式和一个独占一行的公式**；其他写法留作以后查阅。

## 对照源文字和显示结果

在 VS Code 中打开一个 `.md` 文件及其 Markdown 预览。写在**句子中间**的公式前后各用一个美元符号：源文字 `$d=2r$` 显示为 $d=2r$。

让公式**单独占一行**时，把双美元符号分别放在上下两行。把下面三行复制到 `my-note.md`：

```text
$$
A=\pi r^2
$$
```

上面的代码块展示要输入的原始字符；**代码块里**的公式只显示为文字。复制到笔记后，预览会显示为

$$
A=\pi r^2
$$

VS Code 的 Markdown 预览和 GitHub 的 Markdown 页面都支持显示公式。其他 Markdown 阅读工具可能直接显示美元符号。若预览不同，可看 [VS Code 说明](https://code.visualstudio.com/docs/languages/markdown)和 [GitHub 公式说明](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions)。

## 少量常用符号

| 想写什么 | 在 Markdown 中输入 | 在科研笔记中的含义 |
|---|---|---|
| 上标 | `$r^2$` 或 `$r^{10}$` | `^` 让后面的符号或花括号中的整体成为上标。 |
| 下标 | `$m_0$` 或 `$m_{initial}$` | `_` 让后面的符号或花括号中的整体成为下标。 |
| 希腊字母 | `$\theta$`、`$\pi$`、`$\Delta m$` | 分别可表示角度、圆周率和质量变化量。 |
| 分数 | `$\frac{\Delta m}{m_0}$` | 第一组花括号写分子，第二组写分母。 |
| 根号 | `$\sqrt{x}$` | 平方根。 |
| 乘号 | `$a\times b$` | 乘法符号。 |
| 单位 | `$r=5\,\mu\mathrm{m}$` | `\,` 加一点空隙；`\mu` 表示微；`\mathrm{m}` 让单位 m 正体显示。 |

需要更多写法时，直接查原始资料：[Overleaf 的上下标说明](https://www.overleaf.com/learn/latex/Subscripts_and_superscripts)、[希腊字母与符号表](https://www.overleaf.com/learn/latex/List_of_Greek_letters_and_math_symbols)、[分数说明](https://www.overleaf.com/learn/latex/Fractions_and_Binomials)和[数学公式间距说明](https://www.overleaf.com/learn/latex/Spacing_in_math_mode)。这些是按需查询的页面，本次不需要全部读完。

例如，可以把一个简单的质量变化表达式单独写成：

```text
$$
\frac{\Delta m}{m_0}\times 100\%
$$
```

其中 `\%` 在公式里显示百分号。这是**写法示例**，不要求分析实验数据。无需背诵命令：复制一个例子，改动一处，再检查预览即可。

## 动手并检查

1. 在复制的 `my-note.md` 中保留导读里的行内公式 `$d=2r$`。
2. 加入上面的三行面积公式，把 `r^2` 改为 `r_0^2`，对照源文字与预览。
3. 如果只看见美元符号原文，先确认打开的是 Markdown **预览**，再检查阅读工具是否支持公式。保留源文件；不需要安装 LaTeX。

想查更多符号，可参考 [Overleaf 的数学公式说明](https://www.overleaf.com/learn/latex/Mathematical_expressions)。Markdown 公式标记及预览行为可查阅 [VS Code](https://code.visualstudio.com/docs/languages/markdown)和 [GitHub](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions)的说明。本页示例与解释由本课程编写，并未复制这些文档的正文。
