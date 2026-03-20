#!/usr/bin/env python3
"""
数据获取脚本 - 从 GitHub 仓库获取最新数据

用户无需梯子，直接从 GitHub 读取
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import urllib.request

# GitHub 仓库数据 URL
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-romeo/smart-priority-pusher/main/data/daily"

def get_latest_data_from_github():
    """从 GitHub 获取最新数据"""
    try:
        # 获取今日数据
        today = datetime.now().strftime("%Y-%m-%d")
        url = f"{GITHUB_DATA_URL}/{today}.json"
        
        print(f"[INFO] 从 GitHub 获取数据：{url}", file=sys.stderr)
        
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        return data
    except Exception as e:
        print(f"[ERROR] 获取失败：{e}", file=sys.stderr)
        return None


def get_local_data():
    """从本地仓库获取（备用方案）"""
    data_dir = Path(__file__).parent.parent / "data" / "daily"
    
    if not data_dir.exists():
        return None
    
    files = sorted(data_dir.glob("*.json"), reverse=True)
    if not files:
        return None
    
    with open(files[0], encoding='utf-8') as f:
        return json.load(f)


def display_data(data: dict, top_n: int = None):
    """格式化显示数据"""
    lines = [
        f"📊 X 精选 Top {data['total_items']} ({data['date']})",
        ""
    ]
    
    if data.get('source'):
        lines.append(f"_数据来源：{data['source']}_")
        lines.append("")
    
    medals = ["🥇", "🥈", "🥉"]
    
    items = data.get("items", [])
    if top_n:
        items = items[:top_n]
    
    for item in items:
        rank = item.get("rank", 0)
        medal = medals[rank-1] if rank <= 3 else f"{rank}."
        
        score = item.get("score", 0)
        title = item.get("title", "无标题")
        source = item.get("source", "未知")
        source_type = item.get("source_type", "")
        username = item.get("username", "")
        url = item.get("url", "")
        reason = item.get("reason", "")
        likes = item.get("likes", 0)
        retweets = item.get("retweets", 0)
        
        lines.append(f"{medal} **[{score:.1f}] {title}**")
        lines.append(f"   来源：{source} {username} | 分类：{source_type}")
        
        if reason:
            lines.append(f"   💡 {reason}")
        
        if likes or retweets:
            lines.append(f"   👍 {likes} | 🔁 {retweets}")
        
        if url:
            lines.append(f"   🔗 {url}")
        
        lines.append("")
    
    return "\n".join(lines)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="获取每日 X 精选数据")
    parser.add_argument("--date", type=str, help="指定日期 (YYYY-MM-DD)")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--top", type=int, help="只显示前 N 条")
    parser.add_argument("--local", action="store_true", help="强制使用本地数据")
    
    args = parser.parse_args()
    
    # 获取数据
    data = None
    
    if not args.local:
        # 优先从 GitHub 获取
        if args.date:
            url = f"{GITHUB_DATA_URL}/{args.date}.json"
            try:
                with urllib.request.urlopen(url, timeout=10) as response:
                    data = json.loads(response.read().decode('utf-8'))
            except:
                print(f"[WARN] GitHub 获取失败，尝试本地数据", file=sys.stderr)
        
        if not data:
            data = get_latest_data_from_github()
    
    # 备用：本地数据
    if not data:
        print(f"[INFO] 使用本地数据", file=sys.stderr)
        data = get_local_data()
    
    if not data:
        print("❌ 无法获取数据，请检查网络连接或克隆仓库", file=sys.stderr)
        sys.exit(1)
    
    # 限制数量
    if args.top:
        data["items"] = data["items"][:args.top]
        data["total_items"] = len(data["items"])
    
    # 输出
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(display_data(data, args.top))


if __name__ == "__main__":
    main()
