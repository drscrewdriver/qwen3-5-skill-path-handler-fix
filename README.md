# qwen3-5-skill-path-fixer

🛠️ A lightweight utility to fix automatic space insertion in Qwen3.5 model paths (e.g., Qwen3.5-122B-A10B → Qwen3.5 - 122B - A10B).

📌 问题背景

Qwen3.5 系列模型（如 Qwen3.5-35B-A3B, Qwen3.5-122B-A10B）在某些推理框架或 CLI 工具中加载时，路径中的连字符 - 会被错误地解析为分隔符，导致路径被自动插入空格。例如：

Input:  Qwen3.5-122B-A10B
Output: Qwen3.5 - 122B - A10B  ❌

这会导致文件处理失败，尤其在以下场景中高频出现：

英文用户使用标准 Hugging Face 风格路径（含 - 和数字）
此问题不仅影响中文用户，任何使用 Qwen3.5 家族模型且路径含 - 的用户均可能遭遇。

✨ 解决方案

本工具利用 Skill Method（技能注入法），在模型路径传入前进行预处理，确保原始路径字符串不被篡改。

功能特点
接管 Qwen3.5 模型路径的文件操作
零依赖，纯 Python 实现
支持集成到现有推理/部署流程中

🚀 快速使用
以Claudecode opencode为例子 
请把python脚本放在~/.claude/tools
放置skills/qwenSkillPathHandlerFixer文件夹到你的skills文件夹
想办法在使用qwen3.5系的初始化中加载skill 比如hook机制



📦 安装



🤝 贡献与反馈

欢迎提交 Issue 或 PR！如果你在 OpenClaw、LM Studio、SGLang 或其他框架中遇到此问题，请附上具体环境信息。

💡 提示：此问题源于部分 NLP 预处理模块对路径格式格式的误判（markdown整形）。本工具提供一种通用规避策略，而非修改底层模型代码。
其他问题
长上下文规避替换可能被遗忘这种情况暂未测试出来 但忘记这个规则的话说明使用场景可能就不匹配当前注意力规格
非直接对文件操作的情况 比如编程了以后马上运行 一般来说脚本里按规则不会带数字和连字符才对 暂时未想到好办法 就不绕过了 如果出现和文件写入类似的执行问题欢迎分享

这个 README 强调了：
问题的普遍性（中英文用户都会遇到）
技术本质（路径解析错误，非模型本身 bug）
实用性（可直接集成到现有工作流）
明确的使用示例
