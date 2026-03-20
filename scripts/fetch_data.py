#!/usr/bin/env python3
"""
用户数据获取脚本 - 从 GitHub 获取最新数据

无需梯子，直接从 GitHub 仓库读取
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data" / "daily"

def get_latest_data():
    """获取最新一天的数据"""
    if not DATA_DIR.exists():
        print("❌ 数据目录不存在，请先克隆仓库", file=sys.stderr)
        return None
    
    files = sorted(DATA_DIR.glob("*.json"), reverse=True)
    
    if not files:
        print("❌ 暂无数据", file=sys.stderr)
        return None
    
    latest_file = files[0]
    
    with open(latest_file, encoding='utf-8') as f:
        data = json.load(f)
    
    return data

def display_data(data: dict):
    """格式化显示数据"""
    lines = [
        f"📊 AI 精选 Top {data['total_items']} ({data['date']})",
        ""
    ]
    
    medals = ["🥇", "🥈", "🥉"]
    
    for item in data["items"]:
        medal = medals[item["rank"]-1] if item["rank"] <= 3 else f"{item['rank']}."
        
        lines.append(f"{medal} **[{item['score']:.1f}] {item['title']}**")
        lines.append(f"   来源：{item['source']} | 分类：{item['category'].upper()}")
        
        if item.get("reason"):
            lines.append(f"   💡 {item['reason']}")
        
        lines.append(f"   🔗 {item['url']}")
        lines.append("")
    
    return "\n".join(lines)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="获取每日数据")
    parser.add_argument("--date", type=str, help="指定日期 (YYYY-MM-DD)")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--top", type=int, help="只显示前 N 条")
    
    args = parser.parse_args()
    
    if args.date:
        # 读取指定日期
        file = DATA_DIR / f"{args.date}.json"
        if not file.exists():
            print(f"❌ 找不到 {args.date} 的数据", file=sys.stderr)
            sys.exit(1)
        
        with open(file, encoding='utf-8') as f:
            data = json.load(f)
    else:
        # 获取最新
        data = get_latest_data()
        if not data:
            sys.exit(1)
    
    # 限制数量
    if args.top:
        data["items"] = data["items"][:args.top]
        data["total_items"] = len(data["items"])
    
    # 输出
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(display_data(data))

if __name__ == "__main__":
    main()
