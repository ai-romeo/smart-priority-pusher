#!/usr/bin/env python3
"""
飞书推送脚本 - 从 GitHub 获取数据并推送到飞书群

使用方式：
1. 定时任务自动推送
2. 手动触发推送
"""

import json
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

# GitHub 数据源
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-romeo/smart-priority-pusher/main/data/daily"

def fetch_from_github(date: str = None):
    """从 GitHub 获取数据"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    url = f"{GITHUB_DATA_URL}/{date}.json"
    
    try:
        print(f"[INFO] 从 GitHub 获取数据：{url}", file=sys.stderr)
        
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        print(f"[INFO] 获取成功：{data.get('total_items', 0)} 条", file=sys.stderr)
        return data
    except Exception as e:
        print(f"[ERROR] 获取失败：{e}", file=sys.stderr)
        return None


def format_feishu_message(data: dict, top_n: int = 10):
    """格式化为飞书消息"""
    date = data.get('date', '未知')
    items = data.get('items', [])[:top_n]
    
    # 飞书卡片消息
    medals = ["🥇", "🥈", "🥉"]
    
    lines = [
        f"**📊 X 精选 Top {len(items)} ({date})**",
        "",
        f"_数据来源：25 个精选 X 账号 · 智能打分排序_"
    ]
    
    for item in items:
        rank = item.get('rank', 0)
        medal = medals[rank-1] if rank <= 3 else f"{rank}."
        
        score = item.get('score', 0)
        title = item.get('title', '无标题')
        source = item.get('source', '未知')
        username = item.get('username', '')
        reason = item.get('reason', '')
        url = item.get('url', '')
        
        # 清理标题（移除重复的账号名）
        if source in title:
            title = title.replace(source + ':', '').strip()
        
        lines.append("")
        lines.append(f"{medal} **[{score:.1f}] {title}**")
        lines.append(f"   来源：{source} {username}")
        
        if reason:
            lines.append(f"   💡 {reason}")
        
        if url:
            lines.append(f"   🔗 {url}")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"_📦 完整数据：https://github.com/ai-romeo/smart-priority-pusher_")
    lines.append(f"_🔧 复制 Skill 即可用：`git clone https://github.com/ai-romeo/smart-priority-pusher.git`_")
    
    return "\n".join(lines)


def send_to_feishu(message: str):
    """发送到飞书（通过 OpenClaw message 工具）"""
    # 这里使用 OpenClaw 的 message 工具发送
    # 实际使用时会被 OpenClaw 自动路由到飞书
    print(message)
    return True


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="飞书推送")
    parser.add_argument("--date", type=str, help="指定日期 (YYYY-MM-DD)")
    parser.add_argument("--top", type=int, default=10, help="推送数量")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不发送")
    
    args = parser.parse_args()
    
    # 获取数据
    data = fetch_from_github(args.date)
    
    if not data:
        # 尝试获取昨天的数据
        print("[WARN] 今日数据不存在，尝试获取昨天的数据", file=sys.stderr)
        from datetime import timedelta
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        data = fetch_from_github(yesterday)
    
    if not data:
        print("[ERROR] 无法获取数据", file=sys.stderr)
        sys.exit(1)
    
    # 格式化消息
    message = format_feishu_message(data, args.top)
    
    # 发送
    if args.dry_run:
        print("\n[DRY RUN] 预览消息：")
        print(message)
    else:
        print("\n[INFO] 发送到飞书...", file=sys.stderr)
        send_to_feishu(message)
        print("[INFO] ✅ 推送完成", file=sys.stderr)


if __name__ == "__main__":
    main()
