> 原作：Matt Cone 与 Markdown Guide 贡献者；课程组翻译。[英文原件](markdown-cheat-sheet.md) · [原网页](https://www.markdownguide.org/cheat-sheet/) · [来源、许可与改动](SOURCE.md)。

# Markdown 语法速查

欢迎访问 [Markdown Guide](https://www.markdownguide.org)！

这份速查简要展示 Markdown 的各类语法元素。它无法涵盖所有特殊情况；需要进一步了解某种写法时，请查阅[基础语法](https://www.markdownguide.org/basic-syntax/)和[扩展语法](https://www.markdownguide.org/extended-syntax/)参考资料。

## 基础语法

这些元素出自 John Gruber 的原始设计文档。所有 Markdown 应用都支持这些元素。

### 标题（Heading）

# H1
## H2
### H3

### 粗体（Bold）

**粗体文字**

### 斜体（Italic）

*斜体文字*

### 引用块（Blockquote）

> 引用块

### 有序列表（Ordered List）

1. 第一项
2. 第二项
3. 第三项

### 无序列表（Unordered List）

- 第一项
- 第二项
- 第三项

### 行内代码（Code）

`代码`

### 分隔线（Horizontal Rule）

---

### 链接（Link）

[Markdown Guide](https://www.markdownguide.org)

### 图片（Image）

![替代文字](../figure.svg)

## 扩展语法

这些元素为基础语法添加功能。并非所有 Markdown 应用都支持它们。

### 表格（Table）

| 语法 | 描述 |
| ----------- | ----------- |
| 标题 | 题目 |
| 段落 | 文字 |

### 围栏代码块（Fenced Code Block）

```
{
  "firstName": "John",
  "lastName": "Smith",
  "age": 25
}
```

### 脚注（Footnote）

这是一个带脚注的句子。[^1]

[^1]: 这是脚注。

### 标题标识（Heading ID）

### 我的标题 {#custom-id}

### 定义列表（Definition List）

术语
: 定义

### 删除线（Strikethrough）

~~地球是平的。~~

### 任务列表（Task List）

- [x] 撰写新闻稿
- [ ] 更新网站
- [ ] 联系媒体

### 表情符号（Emoji）

真有趣！ :joy:

（另见[复制粘贴表情符号](https://www.markdownguide.org/extended-syntax/#copying-and-pasting-emoji)）

### 高亮（Highlight）

我需要突出这些==非常重要的文字==。

### 下标（Subscript）

H~2~O

### 上标（Superscript）

X^2^
