#!/usr/bin/env python3
"""
每日数据推送 - 生成当天数据并推送到 GitHub

数据保留 7 天，每天 10 条精选
"""

import json
import hashlib
import sys
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.push_priority import Item, Scorer, Deduplicator

# ============== 配置 ==============

SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data" / "daily"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ============== 数据生成 ==============

def generate_daily_items(date: str = None) -> list:
    """生成每日精选数据"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # 模拟真实数据（实际使用时替换为真实抓取）
    items = [
        {
            "rank": 1,
            "score": 9.5,
            "title": "OpenAI 发布 GPT-4.5：多模态理解能力突破",
            "source": "OpenAI Blog",
            "category": "ai",
            "url": "https://openai.com/index/gpt-4-5/",
            "summary": "GPT-4.5 在多模态理解、代码生成和推理能力上有显著提升，支持更长的上下文窗口。",
            "reason": "高质量内容 | 匹配兴趣：AI",
            "published_at": f"{date}T08:00:00Z"
        },
        {
            "rank": 2,
            "score": 9.2,
            "title": "HuggingFace Transformers 5.0 正式发布",
            "source": "HuggingFace",
            "category": "ai",
            "url": "https://huggingface.co/blog/transformers-5",
            "summary": "Transformers 5.0 带来全新架构，性能提升 40%，支持更多模型格式。",
            "reason": "高质量内容",
            "published_at": f"{date}T09:00:00Z"
        },
        {
            "rank": 3,
            "score": 9.0,
            "title": "Claude 3.5 Sonnet：推理能力新基准",
            "source": "Anthropic",
            "category": "ai",
            "url": "https://www.anthropic.com/news/claude-3-5-sonnet",
            "summary": "Claude 3.5 Sonnet 在数学推理、代码生成和多语言理解上创下新纪录。",
            "reason": "高质量内容 | 匹配兴趣：AI",
            "published_at": f"{date}T10:00:00Z"
        },
        {
            "rank": 4,
            "score": 8.8,
            "title": "LangChain 推出 Agent 框架 2.0",
            "source": "LangChain",
            "category": "ai",
            "url": "https://python.langchain.com/docs/agents/",
            "summary": "新一代 Agent 框架，支持更复杂的任务规划和工具调用。",
            "reason": "匹配兴趣：AI",
            "published_at": f"{date}T11:00:00Z"
        },
        {
            "rank": 5,
            "score": 8.6,
            "title": "Llama 3 70B 开源：性能媲美 GPT-4",
            "source": "Meta AI",
            "category": "ai",
            "url": "https://ai.meta.com/blog/meta-llama-3/",
            "summary": "Meta 发布 Llama 3 70B 开源模型，在多个基准测试中接近 GPT-4 水平。",
            "reason": "匹配兴趣：开源 + AI",
            "published_at": f"{date}T12:00:00Z"
        },
        {
            "rank": 6,
            "score": 8.4,
            "title": "GitHub Copilot X：AI 编程新体验",
            "source": "GitHub",
            "category": "dev",
            "url": "https://github.blog/copilot-x/",
            "summary": "Copilot X 集成 GPT-4，支持对话式代码生成和项目级理解。",
            "reason": "匹配兴趣：开发者工具",
            "published_at": f"{date}T13:00:00Z"
        },
        {
            "rank": 7,
            "score": 8.2,
            "title": "Midjourney V6：图像生成质量飞跃",
            "source": "Midjourney",
            "category": "ai",
            "url": "https://midjourney.com/v6",
            "summary": "V6 版本在细节处理、文字渲染和风格一致性上大幅提升。",
            "reason": "高质量内容",
            "published_at": f"{date}T14:00:00Z"
        },
        {
            "rank": 8,
            "score": 8.0,
            "title": "Stable Diffusion 3 技术报告发布",
            "source": "Stability AI",
            "category": "ai",
            "url": "https://stability.ai/sd3",
            "summary": "SD3 采用新架构，支持更高分辨率和更精准的提示词理解。",
            "reason": "匹配兴趣：AI",
            "published_at": f"{date}T15:00:00Z"
        },
        {
            "rank": 9,
            "score": 7.8,
            "title": "Google Gemini 1.5 Pro：百万级上下文",
            "source": "Google DeepMind",
            "category": "ai",
            "url": "https://deepmind.google/technologies/gemini/",
            "summary": "Gemini 1.5 Pro 支持百万 token 上下文，处理长文档和视频成为可能。",
            "reason": "高质量内容",
            "published_at": f"{date}T16:00:00Z"
        },
        {
            "rank": 10,
            "score": 7.6,
            "title": "AI Agent 开发框架对比：LangChain vs AutoGen",
            "source": "GitHub Trending",
            "category": "dev",
            "url": "https://github.com/topics/ai-agent",
            "summary": "主流 AI Agent 框架功能对比，帮助开发者选择合适的工具。",
            "reason": "匹配兴趣：AI + 开源",
            "published_at": f"{date}T17:00:00Z"
        }
    ]
    
    return items


def save_daily_data(items: list, date: str = None):
    """保存每日数据"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    output_file = DATA_DIR / f"{date}.json"
    
    data = {
        "date": date,
        "generated_at": datetime.now().isoformat(),
        "total_items": len(items),
        "items": items
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[INFO] 已保存：{output_file}", file=sys.stderr)
    return output_file


def cleanup_old_days(keep_days: int = 7):
    """清理旧数据，只保留最近 N 天"""
    cutoff = datetime.now() - timedelta(days=keep_days)
    
    deleted = 0
    for file in DATA_DIR.glob("*.json"):
        # 从文件名解析日期
        try:
            file_date = datetime.strptime(file.stem, "%Y-%m-%d")
            if file_date < cutoff:
                file.unlink()
                deleted += 1
                print(f"[INFO] 删除旧数据：{file.name}", file=sys.stderr)
        except:
            pass
    
    return deleted


def generate_readme():
    """生成数据说明 README"""
    readme_file = DATA_DIR.parent / "README.md"
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 获取最近 7 天的数据文件
    files = sorted(DATA_DIR.glob("*.json"), reverse=True)[:7]
    
    lines = [
        "# Smart Priority Pusher - Daily Data",
        "",
        "## 📊 数据说明",
        "",
        "本目录存放每日精选的 AI 和技术资讯，每天 10 条，保留最近 7 天。",
        "",
        "### 数据格式",
        "",
        "```json",
        "{",
        '  "date": "2026-03-20",',
        '  "generated_at": "2026-03-20T12:00:00",',
        '  "total_items": 10,',
        '  "items": [',
        "    {",
        '      "rank": 1,',
        '      "score": 9.5,',
        '      "title": "标题",',
        '      "source": "来源",',
        '      "category": "分类",',
        '      "url": "链接",',
        '      "summary": "摘要",',
        '      "reason": "推荐理由"',
        "    }",
        "  ]",
        "}",
        "```",
        "",
        "### 可用数据",
        ""
    ]
    
    for file in files:
        try:
            with open(file, encoding='utf-8') as f:
                data = json.load(f)
            lines.append(f"- **{data['date']}**: {data['total_items']} 条")
        except:
            lines.append(f"- **{file.stem}**: 数据加载中...")
    
    lines.extend([
        "",
        "### 使用方式",
        "",
        "```bash",
        "# 克隆仓库",
        "git clone https://github.com/ai-romeo/smart-priority-pusher.git",
        "cd smart-priority-pusher/data/daily",
        "",
        "# 查看最新数据",
        "cat $(ls -t *.json | head -1)",
        "",
        "# 或使用 Python 读取",
        "python ../../scripts/fetch_data.py",
        "```",
        "",
        "### 更新频率",
        "",
        "每天自动更新，保留最近 7 天数据。",
        "",
        "---",
        "",
        f"*最后更新：{today}*"
    ])
    
    with open(readme_file, "w", encoding='utf-8') as f:
        json.dump("\n".join(lines), f, ensure_ascii=False)
    
    print(f"[INFO] 已更新 README", file=sys.stderr)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="每日数据推送")
    parser.add_argument("--date", type=str, help="指定日期 (YYYY-MM-DD)")
    parser.add_argument("--keep-days", type=int, default=7, help="保留天数")
    parser.add_argument("--no-cleanup", action="store_true", help="不清理旧数据")
    
    args = parser.parse_args()
    
    date = args.date or datetime.now().strftime("%Y-%m-%d")
    
    print(f"[INFO] 生成 {date} 的每日数据...", file=sys.stderr)
    
    # 生成数据
    items = generate_daily_items(date)
    
    # 保存
    save_daily_data(items, date)
    
    # 清理旧数据
    if not args.no_cleanup:
        deleted = cleanup_old_days(args.keep_days)
        print(f"[INFO] 清理了 {deleted} 个旧文件", file=sys.stderr)
    
    # 生成 README
    generate_readme()
    
    print(f"[INFO] ✅ {date} 数据生成完成", file=sys.stderr)


if __name__ == "__main__":
    main()
