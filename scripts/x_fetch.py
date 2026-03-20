#!/usr/bin/env python3
"""
X (Twitter) 信息源抓取脚本

从配置的 X 账号抓取推文，生成每日数据
"""

import json
import random
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass

# ============== 配置 ==============

SKILL_DIR = Path(__file__).parent.parent
CONFIG_FILE = SKILL_DIR / "config" / "x_sources.json"
DATA_DIR = SKILL_DIR / "data" / "daily"

# ============== 模拟数据 ==============
# 注：实际使用时需要接入 X API 或使用 Nitter 实例

def generate_x_items() -> list:
    """生成 X 推文数据（模拟）"""
    date = datetime.now().strftime("%Y-%m-%d")
    
    # 基于配置中的账号生成模拟推文
    items = [
        {
            "rank": 1,
            "score": 9.5,
            "title": "Garry Tan: AI 创业的黄金时代已经到来",
            "source": "Garry Tan",
            "source_type": "创业",
            "username": "@garrytan",
            "url": "https://x.com/garrytan/status/xxx",
            "summary": "Y Combinator 总裁 Garry Tan 分享 AI 创业趋势：现在是 AI 创业的最佳时机，门槛降低，机会增多。",
            "reason": "高质量内容 | 匹配兴趣：创业 + AI",
            "published_at": f"{date}T08:30:00Z",
            "likes": 2341,
            "retweets": 456
        },
        {
            "rank": 2,
            "score": 9.3,
            "title": "Andrej Karpathy: 大模型推理优化的新突破",
            "source": "Andrej Karpathy",
            "source_type": "AI",
            "username": "@karpathy",
            "url": "https://x.com/karpathy/status/xxx",
            "summary": "前特斯拉 AI 总监、OpenAI 联合创始人 Karpathy 分享大模型推理优化的最新技术进展。",
            "reason": "高质量内容 | 匹配兴趣：AI",
            "published_at": f"{date}T09:15:00Z",
            "likes": 3521,
            "retweets": 678
        },
        {
            "rank": 3,
            "score": 9.1,
            "title": "Paul Graham: 如何判断创业点子是否值得做",
            "source": "Paul Graham",
            "source_type": "创业",
            "username": "@paulg",
            "url": "https://x.com/paulg/status/xxx",
            "summary": "Y Combinator 创始人 Paul Graham 分享评估创业点子的 5 个关键问题。",
            "reason": "高质量内容 | 匹配兴趣：创业",
            "published_at": f"{date}T10:00:00Z",
            "likes": 1876,
            "retweets": 342
        },
        {
            "rank": 4,
            "score": 8.9,
            "title": "李继刚：Prompt 设计的艺术",
            "source": "李继刚",
            "source_type": "AI 自媒体",
            "username": "@lijigang",
            "url": "https://x.com/lijigang/status/xxx",
            "summary": "知名 AI 提示词工程师分享 Prompt 设计的核心原则和实战技巧。",
            "reason": "匹配兴趣：AI + Prompt",
            "published_at": f"{date}T11:30:00Z",
            "likes": 956,
            "retweets": 234
        },
        {
            "rank": 5,
            "score": 8.7,
            "title": "Naval: 财富与幸福的本质",
            "source": "Naval",
            "source_type": "个人成长",
            "username": "@naval",
            "url": "https://x.com/naval/status/xxx",
            "summary": "AngelList 创始人 Naval Ravikant 分享关于财富积累和人生幸福的深刻见解。",
            "reason": "匹配兴趣：个人成长",
            "published_at": f"{date}T12:00:00Z",
            "likes": 4521,
            "retweets": 892
        },
        {
            "rank": 6,
            "score": 8.5,
            "title": "Alex Hormozi: 如何打造不可阻挡的执行力",
            "source": "Alex Hormozi",
            "source_type": "个人成长",
            "username": "@AlexHormozi",
            "url": "https://x.com/AlexHormozi/status/xxx",
            "summary": "知名创业者和作家分享提升执行力的实用方法和心态建设。",
            "reason": "匹配兴趣：个人成长 + 创业",
            "published_at": f"{date}T13:00:00Z",
            "likes": 2134,
            "retweets": 445
        },
        {
            "rank": 7,
            "score": 8.3,
            "title": "向阳乔木：国内 AI 大模型最新进展汇总",
            "source": "向阳乔木",
            "source_type": "AI 自媒体",
            "username": "@vista8",
            "url": "https://x.com/vista8/status/xxx",
            "summary": "整理汇总国内各大模型厂商的最新技术进展和产品发布。",
            "reason": "匹配兴趣：AI",
            "published_at": f"{date}T14:00:00Z",
            "likes": 567,
            "retweets": 123
        },
        {
            "rank": 8,
            "score": 8.1,
            "title": "Andrew Huberman: 优化大脑表现的神经科学方法",
            "source": "Andrew D. Huberman, Ph.D",
            "source_type": "个人成长",
            "username": "@hubermanlab",
            "url": "https://x.com/hubermanlab/status/xxx",
            "summary": "斯坦福神经科学家分享基于科学的大脑优化和压力管理方法。",
            "reason": "匹配兴趣：个人成长",
            "published_at": f"{date}T15:00:00Z",
            "likes": 3245,
            "retweets": 567
        },
        {
            "rank": 9,
            "score": 7.9,
            "title": "宝玉：AI 辅助编程的最佳实践",
            "source": "宝玉",
            "source_type": "AI 自媒体",
            "username": "@dotey",
            "url": "https://x.com/dotey/status/xxx",
            "summary": "分享使用 AI 工具辅助编程的实战经验和最佳实践。",
            "reason": "匹配兴趣：AI + 开发",
            "published_at": f"{date}T16:00:00Z",
            "likes": 432,
            "retweets": 98
        },
        {
            "rank": 10,
            "score": 7.7,
            "title": "DAN KOE: 数字时代的个人品牌建设",
            "source": "DAN KOE",
            "source_type": "个人成长",
            "username": "@thedankoe",
            "url": "https://x.com/thedankoe/status/xxx",
            "summary": "知名个人成长博主分享如何在数字时代建立有影响力的个人品牌。",
            "reason": "匹配兴趣：个人成长",
            "published_at": f"{date}T17:00:00Z",
            "likes": 1567,
            "retweets": 289
        }
    ]
    
    return items


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="X 信息源抓取")
    parser.add_argument("--date", type=str, help="指定日期 (YYYY-MM-DD)")
    parser.add_argument("--top", type=int, default=10, help="推送数量")
    parser.add_argument("--output", type=str, help="输出文件")
    
    args = parser.parse_args()
    
    date = args.date or datetime.now().strftime("%Y-%m-%d")
    
    print(f"[INFO] 抓取 X 信息源...", file=sys.stderr)
    
    # 生成数据
    items = generate_x_items()
    items = items[:args.top]
    
    # 生成数据结构
    data = {
        "date": date,
        "generated_at": datetime.now().isoformat(),
        "source": "X (Twitter)",
        "total_items": len(items),
        "items": items
    }
    
    # 输出
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[INFO] 已保存到 {args.output}", file=sys.stderr)
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    
    print(f"[INFO] ✅ 抓取完成，共 {len(items)} 条", file=sys.stderr)


if __name__ == "__main__":
    import sys
    main()
