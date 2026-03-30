---
name: qwen3.5-path-handler
description: 'Qwen3.5 路径处理器 - 检测到 Qwen3.5 模型时，强制替代所有文件操作（read/write/exists/list/mkdir/delete）为 qwen_file.py 工具，自动修复路径中的中文与 ASCII 混合导致的空格插入 bug，以及连字符 `-` 前后的空格。初次处理目录前，建议先使用 clean_spaces.py 清理现有空格结构。'
---

# Qwen3.5 路径处理器

## 🔴 强制替换规则

**Qwen3.5 模型或中文路径时，禁止使用默认 read/write，必须用 qwen_file.py。**

| 条件 | 操作 |
|------|------|
| Qwen3.5 模型 | 所有文件操作强制用 qwen_file.py |
| 中文路径（任何模型）| 强制用 qwen_file.py |
| 其他模型 + 非中文路径 | 使用默认工具 |

---

## 🔧 工具说明

### 1. qwen_file.py - 文件操作替代工具

```
read → python3 ~/.claude/tools/qwen_file.py read '<路径>'
write → python3 ~/.claude/tools/qwen_file.py write '<路径>' '<内容>'
exists → python3 ~/.claude/tools/qwen_file.py exists '<路径>'
list → python3 ~/.claude/tools/qwen_file.py list '<路径>'
mkdir → python3 ~/.claude/tools/qwen_file.py mkdir '<路径>'
delete → python3 ~/.claude/tools/qwen_file.py delete '<路径>'
fix → python3 ~/.claude/tools/qwen_file.py fix '<路径>'  # 仅返回修复后的路径
```

**修复内容：**
- 中文与 ASCII 之间的空格
- 连字符 `-` 前后的空格（重点修复）
- 下划线 `_` 前后的空格
- 点号 `.` 前后的空格（保留开头点，如 `.git`）

### 2. clean_spaces.py - 空格清理工具

**初次处理目录前，建议先运行清理脚本：**

```bash
# 仅生成报告（不执行清理）
python3 ~/.claude/tools/clean_spaces.py '<目标目录>' --dry-run

# 执行清理
python3 ~/.claude/tools/clean_spaces.py '<目标目录>'

# Markdown 格式报告
python3 ~/.claude/tools/clean_spaces.py '<目标目录>' --report

# JSON 格式输出
python3 ~/.claude/tools/clean_spaces.py '<目标目录>' --report --json
```

**清理策略：**
- 移除所有文件/目录名中的空格
- 递归处理子目录
- 自动处理文件名冲突（添加序号）

---

## 📋 推荐工作流程

### Step 1: 初次处理目录

```bash
# 先扫描目录，生成报告
python3 ~/.claude/tools/clean_spaces.py '~/my-project' --report

# 确认无误后，执行清理
python3 ~/.claude/tools/clean_spaces.py '~/my-project'
```

### Step 2: 文件操作

```bash
# 使用 qwen_file.py 替代默认工具
python3 ~/.claude/tools/qwen_file.py list '~/my-project'
python3 ~/.claude/tools/qwen_file.py read '~/my-project/文件名.md'
```

---

## 🎯 核心问题

Qwen3.5 在中文+ASCII混合路径会错误插入空格：
- 模型输出：`中文测试 l.md`（错误）
- 实际应为：`中文测试l.md`（正确）

连字符问题：
- 模型输出：`TS - 01 基础.md`（错误）
- 实际应为：`TS-01基础.md`（正确）

工具自动修复以上所有问题。

---

## 📁 工具位置

```
~/.claude/tools/
├── qwen_file.py      # 文件操作替代工具
└── clean_spaces.py   # 空格清理工具
```

---

**版本：** 2.0（改进版）
**更新：** 2026-03-30
**新增：** 连字符完整处理 + 空格清理脚本
