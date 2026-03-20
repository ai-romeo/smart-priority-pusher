#!/usr/bin/env python3
"""
演示推送 - 使用模拟数据展示推送效果
"""

from datetime import datetime, timedelta

# 模拟数据
demo_items = [
    {
        "rank": 1,
        "score": 9.2,
        "title": "GPT-4.5 泄露：多模态能力重大突破",
        "source": "Hacker News",
        "category": "ai",
        "url": "https://news.ycombinator.com/item?id=xxx",
        "reason": "高质量内容 | 匹配兴趣：AI | 分类：人工智能"
    },
    {
        "rank": 2,
        "score": 8.9,
        "title": "OpenClaw 2026.2.26 发布：支持子代理编排",
        "source": "GitHub Trending",
        "category": "dev",
        "url": "https://github.com/openclaw/openclaw",
        "reason": "匹配兴趣：开源 | 分类：开发"
    },
    {
        "rank": 3,
        "score": 8.5,
        "title": "HuggingFace Transformers 5.0 正式发布",
        "source": "Hugging Face Papers",
        "category": "ai",
        "url": "https://huggingface.co/blog/transformers-5",
        "reason": "高质量内容 | 匹配兴趣：AI | 分类：人工智能"
    },
    {
        "rank": 4,
        "score": 8.3,
        "title": "Cursor AI 新功能：全项目上下文理解",
        "source": "Product Hunt",
        "category": "product",
        "url": "https://www.producthunt.com/posts/cursor-ai",
        "reason": "匹配兴趣：开发者工具 | 分类：产品"
    },
    {
        "rank": 5,
        "score": 8.1,
        "title": "Rust 1.77 发布：性能提升 30%",
        "source": "Hacker News",
        "category": "dev",
        "url": "https://news.ycombinator.com/item?id=yyy",
        "reason": "匹配兴趣：开源 | 分类：开发"
    },
    {
        "rank": 6,
        "score": 7.8,
        "title": "Claude 3.5 Sonnet：推理能力新基准",
        "source": "Hugging Face Papers",
        "category": "ai",
        "url": "https://huggingface.co/papers/xxx",
        "reason": "匹配兴趣：AI | 分类：人工智能"
    },
    {
        "rank": 7,
        "score": 7.6,
        "title": "VS Code 新功能：AI 结对编程增强",
        "source": "Product Hunt",
        "category": "product",
        "url": "https://www.producthunt.com/posts/vscode",
        "reason": "匹配兴趣：开发者工具 | 分类：产品"
    },
    {
        "rank": 8,
        "score": 7.4,
        "title": "LangChain 推出新一代 Agent 框架",
        "source": "GitHub Trending",
        "category": "ai",
        "url": "https://github.com/langchain-ai",
        "reason": "匹配兴趣：AI | 分类：人工智能"
    },
    {
        "rank": 9,
        "score": 7.2,
        "title": "Next.js 15 RC 发布：React Server Components 优化",
        "source": "Hacker News",
        "category": "dev",
        "url": "https://news.ycombinator.com/item?id=zzz",
        "reason": "匹配兴趣：技术新闻 | 分类：开发"
    },
    {
        "rank": 10,
        "score": 7.0,
        "title": "Llama 3 70B 开源：性能媲美 GPT-4",
        "source": "Hugging Face Papers",
        "category": "ai",
        "url": "https://huggingface.co/meta-llama",
        "reason": "匹配兴趣：开源 | 分类：人工智能"
    }
]

def generate_report():
    """生成推送报告"""
    lines = [
        f"📊 今日精选 Top 10 ({datetime.now().strftime('%Y-%m-%d %H:%M')})",
        "",
        f"_过去 24 小时，从 3 个信息源抓取，去重后筛选出 Top 10_",
        ""
    ]
    
    medals = ["🥇", "🥈", "🥉"]
    
    for item in demo_items:
        medal = medals[item["rank"]-1] if item["rank"] <= 3 else f"{item['rank']}."
        
        lines.append(f"{medal} **[{item['score']:.1f}] {item['title']}**")
        lines.append(f"   来源：{item['source']} | 分类：{item['category'].upper()}")
        lines.append(f"   💡 {item['reason']}")
        lines.append(f"   🔗 {item['url']}")
        lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append("ℹ️ _这是演示数据。配置真实信息源后运行 `push_priority.py` 获取实时内容。_")
    
    return "\n".join(lines)


if __name__ == "__main__":
    print(generate_report())
