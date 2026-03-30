#!/usr/bin/env python3
"""
qwen_file.py - Qwen3.5 路径修复文件操作工具（简化版）

用法:
    python qwen_file.py read <路径>
    python qwen_file.py write <路径> <内容>
    python qwen_file.py exists <路径>
    python qwen_file.py list <目录路径>
    python qwen_file.py mkdir <目录路径>
    python qwen_file.py delete <路径>
    python qwen_file.py fix <路径>    # 返回无空格路径

核心策略:
    只要见到空格就去掉，不判断类型
"""

import os
import sys


def fix_path(path: str) -> str:
    """直接移除所有空格"""
    return os.path.expanduser(path).replace(' ', '')


def find_path(path: str):
    """查找实际存在的路径"""
    original = os.path.expanduser(path)
    fixed = fix_path(path)
    
    # 尝试原始路径
    if os.path.exists(original):
        return original
    
    # 尝试无空格路径
    if os.path.exists(fixed):
        return fixed
    
    # 在父目录模糊匹配
    parent = os.path.dirname(fixed)
    filename = os.path.basename(fixed)
    
    if os.path.isdir(parent):
        for f in os.listdir(parent):
            if f.replace(' ', '') == filename:
                return os.path.join(parent, f)
    
    return None


def safe_read(path: str) -> str:
    actual = find_path(path)
    if not actual:
        return f"ERROR: 不存在: {path} → {fix_path(path)}"
    
    try:
        with open(actual, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"ERROR: 读取失败: {e}"


def safe_write(path: str, content: str) -> str:
    fixed = fix_path(path)
    parent = os.path.dirname(fixed)
    if parent:
        os.makedirs(parent, exist_ok=True)
    
    try:
        with open(fixed, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"OK: {fixed}"
    except Exception as e:
        return f"ERROR: 写入失败: {e}"


def safe_exists(path: str) -> str:
    actual = find_path(path)
    return f"原始: {path}\n无空格: {fix_path(path)}\n找到: {actual or '不存在'}"


def safe_list(path: str) -> str:
    actual = find_path(path) or fix_path(path)
    if not os.path.isdir(actual):
        return f"ERROR: 不是目录: {actual}"
    
    try:
        items = os.listdir(actual)
        result = f"[{actual}] {len(items)}项:\n"
        for f in sorted(items):
            result += f"  {f}\n"
        return result
    except Exception as e:
        return f"ERROR: {e}"


def safe_mkdir(path: str) -> str:
    fixed = fix_path(path)
    try:
        os.makedirs(fixed, exist_ok=True)
        return f"OK: {fixed}"
    except Exception as e:
        return f"ERROR: {e}"


def safe_delete(path: str) -> str:
    actual = find_path(path)
    if not actual:
        return f"ERROR: 不存在: {path}"
    
    try:
        if os.path.isdir(actual):
            os.rmdir(actual)
        else:
            os.remove(actual)
        return f"OK: {actual}"
    except Exception as e:
        return f"ERROR: {e}"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "read":
        print(safe_read(sys.argv[2]) if len(sys.argv) > 2 else "ERROR: 需路径")
    elif cmd == "write":
        print(safe_write(sys.argv[2], sys.argv[3]) if len(sys.argv) > 3 else "ERROR: 需路径和内容")
    elif cmd == "exists":
        print(safe_exists(sys.argv[2]) if len(sys.argv) > 2 else "ERROR: 需路径")
    elif cmd == "list":
        print(safe_list(sys.argv[2] if len(sys.argv) > 2 else "."))
    elif cmd == "mkdir":
        print(safe_mkdir(sys.argv[2]) if len(sys.argv) > 2 else "ERROR: 需路径")
    elif cmd == "delete":
        print(safe_delete(sys.argv[2]) if len(sys.argv) > 2 else "ERROR: 需路径")
    elif cmd == "fix":
        print(fix_path(sys.argv[2]) if len(sys.argv) > 2 else "ERROR: 需路径")
    else:
        print(f"ERROR: 未知命令: {cmd}")



if __name__ == "__main__":
    main()
