---
name: qwen3.5-path-handler
description: 'Qwen3.5 路径处理器 - 检测到 Qwen3.5 模型时，强制替代所有文件操作（read/write/exists/list/mkdir/delete）为 qwen_file.py 工具，自动修复路径中的中文与 ASCII 混合导致的空格插入 bug。也适用于任何模型的中文路径操作。'
---

# Qwen3.5 路径处理器

## 🔴 强制替换规则

**Qwen3.5 模型或中文路径时，禁止使用默认 read/write，必须用 qwen_file.py。**

| 条件 | 操作 |
|------|------|
| Qwen3.5 模型 | 所有文件操作强制用 qwen_file.py |
| 中文路径（任何模型）| 强制用 qwen_file.py |
| 其他模型 + 非中文路径 | 使用默认工具 |

## 工具替换命令

```
read → python3 ~/.claude/tools/qwen_file.py read '<路径>'
write → python3 ~/.claude/tools/qwen_file.py write '<路径>' '<内容>'
exists → python3 ~/.claude/tools/qwen_file.py exists '<路径>'
list → python3 ~/.claude/tools/qwen_file.py list '<路径>'
mkdir → python3 ~/.claude/tools/qwen_file.py mkdir '<路径>'
delete → python3 ~/.claude/tools/qwen_file.py delete '<路径>'
```

## 核心问题

Qwen3.5 在中文+ASCII混合路径会错误插入空格：
- 模型输出：`中文测试 l.md`（错误）
- 实际应为：`中文测试l.md`（正确）

工具自动修复此问题。

