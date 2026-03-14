#!/usr/bin/env python3
"""
qwen_file.py - Qwen3.5 路径修复文件操作工具

用法:
    python qwen_file.py read <文件路径>
    python qwen_file.py write <文件路径> <内容>
    python qwen_file.py exists <文件路径>
    python qwen_file.py list <目录路径>
    python qwen_file.py mkdir <目录路径>
    python qwen_file.py delete <文件路径>
    python qwen_file.py fix <文件路径>  # 仅返回修复后的路径

功能:
    自动检测并修复路径中中文与 ASCII 字符之间的异常空格
    即使模型输出的路径有误，也能找到正确的文件
"""

import os
import sys
import re
from pathlib import Path


def fix_path(path: str) -> str:
    """
    修复路径中的异常空格
    
    问题模式:
        中文 + 空格 + ASCII → 中文 + ASCII
        ASCII + 空格 + 中文 → ASCII + 中文
    
    示例:
        "中文测试 l.md" → "中文测试l.md"
        "项目 v2.md" → "项目v2.md"
    """
    # 模式1: 中文后接空格再接 ASCII（数字或字母）
    fixed = re.sub(r'([\u4e00-\u9fff])\s+([a-zA-Z0-9])', r'\1\2', path)
    # 模式2: ASCII 后接空格再接中文
    fixed = re.sub(r'([a-zA-Z0-9])\s+([\u4e00-\u9fff])', r'\1\2', fixed)
    # 模式3: 中文后接空格再接特殊字符（如 - _ . 等，再接 ASCII）
    fixed = re.sub(r'([\u4e00-\u9fff])\s+([\-_\.])\s*([a-zA-Z0-9])', r'\1\2\3', fixed)
    
    return fixed


def find_actual_path(path: str):
    """
    查找实际存在的文件路径
    
    策略:
    1. 尝试原始路径
    2. 尝试修复后的路径
    3. 尝试在目录中模糊匹配
    """
    path = os.path.expanduser(path)
    
    # 策略1: 原始路径直接存在
    if os.path.exists(path):
        return path
    
    # 策略2: 修复后的路径存在
    fixed = fix_path(path)
    if fixed != path and os.path.exists(fixed):
        return fixed
    
    # 策略3: 在父目录中查找相似文件
    parent = os.path.dirname(path)
    filename = os.path.basename(path)
    
    if os.path.isdir(parent):
        # 移除空格进行模糊匹配
        filename_no_space = filename.replace(' ', '')
        for f in os.listdir(parent):
            # 如果文件名去掉空格后匹配
            if f.replace(' ', '') == filename_no_space:
                return os.path.join(parent, f)
            
            # 如果修复后的文件名匹配
            if fix_path(f) == fix_path(filename):
                return os.path.join(parent, f)
    
    return None


def safe_read(path: str) -> str:
    """安全读取文件内容"""
    actual = find_actual_path(path)
    if actual is None:
        # 返回所有可能的候选路径
        parent = os.path.dirname(path)
        if os.path.isdir(parent):
            files = os.listdir(parent)
            return f"ERROR: 文件不存在: {path}\n修复尝试: {fix_path(path)}\n目录中的文件:\n" + "\n".join(files)
        return f"ERROR: 文件不存在: {path}\n修复尝试: {fix_path(path)}"
    
    try:
        with open(actual, 'r', encoding='utf-8') as f:
            content = f.read()
        if actual != path:
            return f"[实际路径: {actual}]\n\n{content}"
        return content
    except Exception as e:
        return f"ERROR: 读取失败: {e}"


def safe_write(path: str, content: str) -> str:
    """安全写入文件，确保路径正确"""
    # 总是使用修复后的路径进行写入
    fixed_path = fix_path(path)
    fixed_path = os.path.expanduser(fixed_path)
    
    # 确保目录存在
    parent = os.path.dirname(fixed_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    
    try:
        with open(fixed_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 验证写入
        if path != fixed_path:
            return f"SUCCESS: 写入完成\n请求路径: {path}\n实际路径: {fixed_path}"
        return f"SUCCESS: 写入完成\n路径: {fixed_path}"
    except Exception as e:
        return f"ERROR: 写入失败: {e}"


def safe_exists(path: str) -> str:
    """检查文件是否存在，返回所有可能的路径"""
    original_exists = os.path.exists(path)
    fixed = fix_path(path)
    fixed_exists = os.path.exists(fixed)
    actual = find_actual_path(path)
    
    return f"""路径检查结果:
  原始路径: {path}
    存在: {original_exists}
  
  修复路径: {fixed}
    存在: {fixed_exists}
  
  实际找到: {actual if actual else '未找到'}
"""


def safe_list(path: str) -> str:
    """列出目录内容"""
    actual = find_actual_path(path)
    if actual is None:
        return f"ERROR: 目录不存在: {path}"
    
    if not os.path.isdir(actual):
        return f"ERROR: 不是目录: {actual}"
    
    try:
        files = os.listdir(actual)
        result = f"[目录: {actual}]\n共 {len(files)} 项:\n"
        for f in sorted(files):
            full = os.path.join(actual, f)
            if os.path.isdir(full):
                result += f"  📁 {f}/\n"
            else:
                result += f"  📄 {f}\n"
        return result
    except Exception as e:
        return f"ERROR: 列出目录失败: {e}"


def safe_mkdir(path: str) -> str:
    """创建目录"""
    fixed = fix_path(path)
    fixed = os.path.expanduser(fixed)
    
    try:
        os.makedirs(fixed, exist_ok=True)
        if path != fixed:
            return f"SUCCESS: 目录已创建\n请求路径: {path}\n实际路径: {fixed}"
        return f"SUCCESS: 目录已创建: {fixed}"
    except Exception as e:
        return f"ERROR: 创建目录失败: {e}"


def safe_delete(path: str) -> str:
    """删除文件"""
    actual = find_actual_path(path)
    if actual is None:
        return f"ERROR: 文件不存在: {path}"
    
    try:
        os.remove(actual)
        return f"SUCCESS: 已删除: {actual}"
    except Exception as e:
        return f"ERROR: 删除失败: {e}"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "read":
        if len(sys.argv) < 3:
            print("ERROR: 需要文件路径")
            sys.exit(1)
        print(safe_read(sys.argv[2]))
    
    elif command == "write":
        if len(sys.argv) < 4:
            print("ERROR: 用法: write <路径> <内容>")
            sys.exit(1)
        print(safe_write(sys.argv[2], sys.argv[3]))
    
    elif command == "exists":
        if len(sys.argv) < 3:
            print("ERROR: 需要路径")
            sys.exit(1)
        print(safe_exists(sys.argv[2]))
    
    elif command == "list":
        if len(sys.argv) < 3:
            print(safe_list("."))
        else:
            print(safe_list(sys.argv[2]))
    
    elif command == "mkdir":
        if len(sys.argv) < 3:
            print("ERROR: 需要目录路径")
            sys.exit(1)
        print(safe_mkdir(sys.argv[2]))
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("ERROR: 需要文件路径")
            sys.exit(1)
        print(safe_delete(sys.argv[2]))
    
    elif command == "fix":
        if len(sys.argv) < 3:
            print("ERROR: 需要路径")
            sys.exit(1)
        print(fix_path(sys.argv[2]))
    
    else:
        print(f"ERROR: 未知命令: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
