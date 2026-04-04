# qwen3-5-skill-path-handler-fix

> 🛠️ A lightweight utility to fix automatic space insertion in Qwen3.5 model paths (e.g., `Qwen3.5-122B-A10B` → `Qwen3.5 - 122B - A10B`).

## 📌 Problem Statement

When loading Qwen3.5 series models (e.g., `Qwen3.5-35B-A3B`, `Qwen3.5-122B-A10B`) in certain inference frameworks or CLI tools, hyphens (`-`) in the model path are mistakenly interpreted as delimiters. This leads to unwanted spaces being inserted into the path:

```text
Input:  Qwen3.5-122B-A10B
Output: Qwen3.5 - 122B - A10B  ❌
```
This causes file handling or model loading failures, especially in the following scenarios:
English users employing standard Hugging Face–style paths (containing - and alphanumeric characters)
Any user working with Qwen3.5 family models whose paths include hyphens
Note: This issue affects both Chinese and English users—it is not language-specific but stems from how some NLP preprocessing or markdown rendering modules parse identifier strings.
✨ Solution
This tool leverages the Skill Method (a form of runtime patching/hooking) to preprocess model paths before they are consumed by the system, ensuring the original path string remains intact without unintended whitespace.
Key Features
Intercepts and corrects file operations involving Qwen3.5 model paths
Zero dependencies — pure Python implementation
Easily integrable into existing inference or deployment workflows
🚀 Quick Start
Example for ClaudeCode/OpenCode integration:
Place the Python script in ~/.claude/tools/
Copy the skills/qwenSkillPathHandlerFixer/ folder into your skills/ directory
Ensure the skill is loaded during initialization of any Qwen3.5-based workflow (e.g., via a hook mechanism)
💡 Tip: The root cause lies in certain NLP/markdown processors misinterpreting hyphenated identifiers as spaced tokens. This tool provides a practical workaround without modifying the underlying model or framework code.
🤝 Contributions & Feedback
Issues and PRs are welcome! If you encounter this problem in OpenClaw, LM Studio, SGLang, or other environments, please include detailed context about your setup.
⚠️ Known Limitations
Long-context scenarios: Rule replacement might be forgotten in very long contexts — untested, but if the rule is forgotten, the use case may exceed current attention limits.
Non-file I/O cases: For dynamically generated code that executes immediately (e.g., scripts), paths typically shouldn’t contain ambiguous - + digit patterns. No workaround is implemented for such cases yet. If you observe similar issues outside file writing, please share your findings!

