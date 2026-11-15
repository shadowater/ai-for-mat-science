# 查看实际模型的词向量关系

优先打开[四组典型案例与向量说明](课堂候选案例.md)。包括国家与首都、亲属称谓、英文比较级和进行式；课堂展示运算后的检索排名。

- [完整 1,024 维向量与运算结果](典型案例完整向量.json)
- [16 个词的完整向量 CSV](典型词向量.csv)
- [扩展探索结果](扩展实测结果.json)
- [最初的中文词对探索](实测结果.json)

直接读取部署模型的初始嵌入表，以权重中的向量和计算结果说明词语相似程度。模型文件保存在课程仓库外。

## 复现

依赖见 `requirements.txt`：NumPy 和 llama.cpp 项目的 GGUF Python 读取工具。本次使用 `/tmp/aimat-lesson01-verify/bin/python3` 的隔离环境完成；已运行的本地服务提供分词与 token 解码。

在本目录执行：

```bash
OPENBLAS_NUM_THREADS=4 python3 export_examples.py
```

脚本提取四组案例的向量、计算差与和、检索最近词，并导出完整 JSON 与 CSV。课堂文档显示前 8 维，计算使用全部 1,024 维。

扩展探索可运行：

```bash
OPENBLAS_NUM_THREADS=4 python3 inspect_embeddings.py
OPENBLAS_NUM_THREADS=4 python3 benchmark_analogies.py
```

默认模型路径为 `$HOME/aimat/.local-llm/models/Qwen3-0.6B-Q8_0.gguf`，本地地址为 `http://127.0.0.1:8087`。参数可用各脚本的 `--help` 查看。重跑会更新指定输出文件，需要保留旧记录时请指定新的输出位置。

输入表为 151,936 × 1,024，Q8_0 反量化后约占 594 MiB；计算还需其他数组。脚本读取模型文件，权重、GPU 服务和系统提示词配置保持原样。

代码与中文课堂候选为课程编写。关系类别参考 [Word2Vec 作者题库](https://github.com/tmikolov/word2vec/blob/master/questions-words.txt)，原题库通过链接供读者查看。结果表示向量近邻关系，语义解释还需结合具体语境。
