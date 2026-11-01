# 问卷星 API 建卷记录

本记录说明如何将本目录的中文课程调研问卷创建到问卷星，便于后续复用和维护。

## 本次结果

- 源问卷：[questionnaire.zh.md](questionnaire.zh.md)
- API 建卷文件：[questionnaire.wjx.jsonl](questionnaire.wjx.jsonl)
- 已创建问卷 ID：`393325516`
- 填写/预览地址：<https://v.wjx.cn/vm/tLTGJCD.aspx>
- 创建后由官方 CLI 回读校验：题目结构、状态和访问链接均通过。

问卷包含 25 道实际题目与 5 个章节说明，涵盖单选、多选、排序、简答和 3 道矩阵单选题。Q25 被保留为选填。

## 当前发布状态

问卷已创建为草稿，但没有自动发布。问卷星返回的原因是账户手机号验证已超过一年，需要账户持有人重新验证手机号。完成验证后，可在问卷星后台发布该问卷。

## 建卷方法

问卷星官方 `wjx-cli` 的 JSONL 建卷入口为 `survey create`。首行使用 `问卷基础信息`，其后每行一个 JSON 对象，对应一道题或一个章节说明。常用字段：

- `qtype`：题型，例如 `单选`、`多选`、`排序`、`简答题`、`矩阵单选`、`段落说明`。
- `title`：题目或章节标题。
- `select`：选项数组。
- `rowtitle`：矩阵题的行标题数组。
- `prompt`：填写说明。
- `requir`：是否必答；选填题必须在创建命令的 `optional_titles` 中显式声明。

建议先运行不落库预演，再真正创建。以下命令使用环境变量传入密钥，避免把密钥写入文件或 Git 历史：

```powershell
$env:WJX_API_KEY = '<仅在本机临时设置的 API Key>'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$OutputEncoding = [System.Text.UTF8Encoding]::new()

Push-Location '课程调研'
@{
  file = 'questionnaire.wjx.jsonl'
  optional_titles = @('Q25. 你还有哪些希望教师提前考虑的课程安排或学习支持需求？')
} | ConvertTo-Json -Compress |
  wjx --stdin --format json --dry-run --yes --non-interactive survey create
Pop-Location
```

移除 `--dry-run` 后即提交创建。创建完成后，CLI 会回读验证问卷的结构、状态与链接。

## 安全注意事项

- 不要把 API Key 放入 JSONL、Markdown、代码或 Git 提交中。
- API Key 曾出现在聊天记录或其他非机密位置时，应立即在问卷星后台删除并重新生成。
- 使用最小权限、可过期的专用 API Key；完成一次性建卷任务后可直接撤销。
- 对外发布前，应在问卷星编辑器中复核“其他（请填写）”、多选限选及排序题的交互是否符合预期。
