#!/usr/bin/env python3
"""
clean_spaces.py - 清理空格（简化版）

用法:
    python clean_spaces.py <目录>          # 执行清理
    python clean_spaces.py <目录> --report # 仅报告

策略: 只要名字有空格就去掉
"""

import os
import sys


def clean_name(name: str) -> str:
    """直接移除所有空格"""
    return name.replace(' ', '')


def scan(path: str):
    """扫描含空格的文件/目录"""
    items = []
    for root, dirs, files in os.walk(path):
        for d in dirs:
            if ' ' in d:
                items.append(os.path.join(root, d))
        for f in files:
            if ' ' in f:
                items.append(os.path.join(root, f))
    
    # 按深度排序（深层先处理）
    return sorted(items, key=lambda x: x.count('/'), reverse=True)


def clean(path: str, dry_run: bool = False):
    items = scan(path)
    
    if dry_run:
        print(f"扫描: {path}")
        print(f"含空格: {len(items)}个")
        for i in items:
            print(f"  {i} → {clean_name(os.path.basename(i))}")
        return
    
    for original in items:
        cleaned = os.path.join(os.path.dirname(original), clean_name(os.path.basename(original)))
        try:
            os.rename(original, cleaned)
            print(f"OK: {original} → {cleaned}")
        except Exception as e:
            print(f"ERROR: {original}: {e}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    path = sys.argv[1]
    dry_run = "--report" in sys.argv or "--dry-run" in sys.argv
    
    clean(path, dry_run)


if __name__ == "__main__":
    main()
