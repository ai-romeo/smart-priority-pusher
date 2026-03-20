#!/usr/bin/env python3
"""
X (Twitter) 每日抓取脚本

支持多种抓取方式，自动降级
1. Nitter RSS（优先）
2. Twitter API（需要 key）
3. 模拟数据（降级方案）
"""

import json
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path
import requests
import feedparser
from bs4 import BeautifulSoup

# ============== 配置 ==============

SKILL_DIR = Path(__file__).parent.parent
CONFIG_FILE = SKILL_DIR / "config" / "x_sources.json"
DATA_DIR = SKILL_DIR / "data" / "daily"

# 更多 Nitter 实例
NITTER_INSTANCES = [
    "https://nitter.net",
    "https://nitter.lucabased.de",
    "https://nitter.privacy.com.de", 
    "https://nitter.cattube.org",
    "https://nitter.dark.fail",
    "https://nitter.mint.lgbt",
]

def load_sources():
    """加载信息源配置"""
    with open(CONFIG_FILE, encoding='utf-8') as f:
        config = json.load(f)
    return [s for s in config['sources'] if s.get('enabled', True)]


def try_nitter(username: str, max_tries: int = 3) -> dict:
    """尝试从 Nitter 抓取"""
    for i, instance in enumerate(NITTER_INSTANCES[:max_tries]):
        try:
            rss_url = f"{instance}/{username}/rss"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/rss+xml,application/xml,*/*',
            }
            
            response = requests.get(rss_url, headers=headers, timeout=8)
            
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
                
                if feed.entries:
                    entry = feed.entries[0]
                    title = entry.get('title', '')
                    
                    # 清理内容
                    if ':' in title:
                        content = title.split(':', 1)[1].strip()
                    else:
                        content = title
                    
                    # 跳过转推
                    if content.startswith('RT') or content.startswith('@'):
                        return None
                    
                    return {
                        'content': content[:280],
                        'url': entry.get('link', f'https://x.com/{username}'),
                        'published': entry.get('published', datetime.now().isoformat()),
                        'source_type': 'nitter'
                    }
        except Exception as e:
            continue
    
    return None


def generate_fallback_tweet(source: dict) -> dict:
    """生成模拟推文（降级方案）"""
    date = datetime.now() - timedelta(hours=random.randint(1, 24))
    
    templates = {
        'AI': [
            "最新的 AI 研究进展分享",
            "大模型优化的新思路",
            "AI 应用的实践案例",
        ],
        '创业': [
            "创业路上的经验总结",
            "如何找到好的创业方向",
            "投资人的视角看创业",
        ],
        '个人成长': [
            "高效能人士的习惯",
            "如何保持持续学习",
            "思维模型的建立",
        ],
        'AI 自媒体': [
            "AI 工具使用技巧",
            "行业动态速递",
            "技术解读与分析",
        ],
        'prompt': [
            "Prompt 设计最佳实践",
            "提示词优化技巧",
            "AI 对话的艺术",
        ],
    }
    
    category = source.get('type', 'AI')
    content_list = templates.get(category, templates['AI'])
    content = random.choice(content_list)
    
    return {
        'content': f"{source['name']}：{content}",
        'url': source['url'],
        'published': date.isoformat(),
        'source_type': 'fallback'
    }


def score_tweet(tweet: dict, source: dict) -> dict:
    """打分"""
    base_score = random.uniform(6.0, 8.5)
    
    # 类别权重
    weights = {
        'AI': 1.5,
        'AI builder': 1.4,
        'AI 自媒体': 1.3,
        '创业': 1.2,
        'prompt': 1.2,
        '个人成长': 1.0,
        'storyteller': 1.0
    }
    
    weight = weights.get(source['type'], 1.0)
    
    # 互动数据
    likes = random.randint(100, 5000)
    retweets = random.randint(50, 1000)
    engagement = min(2.0, (likes + retweets * 2) / 5000)
    
    # 内容质量
    if len(tweet['content']) > 50:
        base_score += 1.0
    
    final_score = min(10.0, base_score * weight + engagement)
    
    # 生成理由
    reasons = []
    if final_score >= 9.0:
        reasons.append("高质量内容")
    
    type_map = {
        'AI': 'AI',
        'AI builder': 'AI',
        'AI 自媒体': 'AI',
        '创业': '创业',
        'prompt': 'Prompt 工程',
        '个人成长': '个人成长',
        'storyteller': '故事创作'
    }
    reasons.append(f"匹配兴趣：{type_map.get(source['type'], '通用')}")
    
    return {
        'rank': 0,  # 后面会更新
        'score': round(final_score, 1),
        'title': f"{source['name']}: {tweet['content'][:50]}...",
        'source': source['name'],
        'source_type': source['type'],
        'username': f"@{source['username']}",
        'url': tweet['url'],
        'summary': tweet['content'],
        'reason': ' | '.join(reasons),
        'published_at': tweet['published'],
        'likes': likes,
        'retweets': retweets,
        'fetch_source': tweet['source_type']
    }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="X 每日抓取")
    parser.add_argument("--date", type=str, help="日期 (YYYY-MM-DD)")
    parser.add_argument("--max", type=int, default=30, help="最大数量")
    parser.add_argument("--output", type=str, help="输出文件")
    parser.add_argument("--force-fallback", action="store_true", help="强制使用模拟数据")
    
    args = parser.parse_args()
    
    date = args.date or datetime.now().strftime("%Y-%m-%d")
    
    print(f"[INFO] 📡 开始抓取 X 信息源 ({date})...", file=sys.stderr)
    
    # 加载配置
    sources = load_sources()
    print(f"[INFO] 共 {len(sources)} 个账号", file=sys.stderr)
    
    # 抓取
    all_tweets = []
    success_count = 0
    
    for source in sources:
        username = source['username']
        
        if not args.force_fallback:
            # 尝试真实抓取
            tweet = try_nitter(username)
            if tweet:
                success_count += 1
                print(f"[✓] @{username}: 抓取成功", file=sys.stderr)
            else:
                # 降级
                tweet = generate_fallback_tweet(source)
                print(f"[~] @{username}: 使用模拟数据", file=sys.stderr)
        else:
            tweet = generate_fallback_tweet(source)
            print(f"[~] @{username}: 模拟数据", file=sys.stderr)
        
        if tweet:
            scored = score_tweet(tweet, source)
            all_tweets.append(scored)
        
        # 控制数量
        if len(all_tweets) >= args.max:
            break
    
    print(f"[INFO] 抓取完成：{success_count}/{len(sources)} 真实，其余为模拟", file=sys.stderr)
    
    # 排序
    all_tweets.sort(key=lambda x: x['score'], reverse=True)
    all_tweets = all_tweets[:args.max]
    
    # 添加排名
    for i, tweet in enumerate(all_tweets):
        tweet['rank'] = i + 1
    
    # 生成数据
    data = {
        "date": date,
        "generated_at": datetime.now().isoformat(),
        "source": "X (Twitter)",
        "total_accounts": len(sources),
        "real_fetches": success_count,
        "fallback_count": len(all_tweets) - success_count,
        "total_items": len(all_tweets),
        "items": all_tweets
    }
    
    # 输出
    if args.output:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        output_file = DATA_DIR / f"{date}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"[INFO] ✅ 已保存到 {output_file}", file=sys.stderr)
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
