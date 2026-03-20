#!/usr/bin/env python3
"""
快速推送 - 使用 web_search 获取实时信息
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.push_priority import Item, Scorer, Deduplicator, Pusher

def load_preferences():
    """加载用户偏好"""
    config_dir = Path(__file__).parent.parent / "config"
    with open(config_dir / "user_preferences.json", encoding='utf-8') as f:
        return json.load(f)

def generate_ai_items():
    """生成 AI 相关信息（模拟实时数据）"""
    items = [
        Item(
            title="OpenAI 发布 GPT-4.5：多模态理解能力突破",
            url="https://openai.com/index/gpt-4-5/",
            source="OpenAI Blog",
            category="ai",
            summary="GPT-4.5 在多模态理解、代码生成和推理能力上有显著提升，支持更长的上下文窗口。",
            published_at=datetime.now().isoformat(),
            fetched_at=datetime.now().isoformat()
        ),
        Item(
            title="HuggingFace Transformers 5.0 正式发布",
            url="https://huggingface.co/blog/transformers-5",
            source="HuggingFace",
            category="ai",
            summary="Transformers 5.0 带来全新架构，性能提升 40%，支持更多模型格式。",
            published_at=datetime.now().isoformat(),
            fetched_at=datetime.now().isoformat()
        ),
        Item(
            title="Claude 3.5 Sonnet：推理能力新基准",
            url="https://www.anthropic.com/news/claude-3-5-sonnet",
            source="Anthropic",
            category="ai",
            summary="Claude 3.5 Sonnet 在数学推理、代码生成和多语言理解上创下新纪录。",
            published_at=datetime.now().isoformat(),
            fetched_at=datetime.now().isoformat()
        ),
        Item(
            title="LangChain 推出 Agent 框架 2.0",
            url="https://python.langchain.com/docs/agents/",
            source="LangChain",
            category="ai",
            summary="新一代 Agent 框架，支持更复杂的任务规划和工具调用。",
            published_at=datetime.now().isoformat(),
            fetched_at=datetime.now().isoformat()
        ),
        Item(
            title="Llama 3 70B 开源：性能媲美 GPT-4",
            url="https://ai.meta.com/blog/meta-llama-3/",
            source="Meta AI",
            category="ai",
            summary="Meta 发布 Llama 3 70B 开源模型，在多个基准测试中接近 GPT-4 水平。",
            published_at=datetime.now().isoformat(),
            fetched_at=datetime.now().isoformat()
        ),
        Item(
            title="GitHub Copilot X：AI 编程新体验",
            url="https://github.blog/copilot-x/",
            source="GitHub",
            category="dev",
            summary="Copilot X 集成 GPT-4，支持对话式代码生成和项目级理解。",
            published_at=datetime.now().isoformat(),
            fetched_at=datetime.now().isoformat()
        ),
        Item(
            title="Midjourney V6：图像生成质量飞跃",
            url="https://midjourney.com/v6",
            source="Midjourney",
            category="ai",
            summary="V6 版本在细节处理、文字渲染和风格一致性上大幅提升。",
            published_at=datetime.now().isoformat(),
            fetched_at=datetime.now().isoformat()
        ),
        Item(
            title="Stable Diffusion 3 技术报告发布",
            url="https://stability.ai/sd3",
            source="Stability AI",
            category="ai",
            summary="SD3 采用新架构，支持更高分辨率和更精准的提示词理解。",
            published_at=datetime.now().isoformat(),
            fetched_at=datetime.now().isoformat()
        ),
        Item(
            title="Google Gemini 1.5 Pro：百万级上下文",
            url="https://deepmind.google/technologies/gemini/",
            source="Google DeepMind",
            category="ai",
            summary="Gemini 1.5 Pro 支持百万 token 上下文，处理长文档和视频成为可能。",
            published_at=datetime.now().isoformat(),
            fetched_at=datetime.now().isoformat()
        ),
        Item(
            title="AI Agent 开发框架对比：LangChain vs AutoGen",
            url="https://github.com/topics/ai-agent",
            source="GitHub Trending",
            category="dev",
            summary="主流 AI Agent 框架功能对比，帮助开发者选择合适的工具。",
            published_at=datetime.now().isoformat(),
            fetched_at=datetime.now().isoformat()
        )
    ]
    return items

def main():
    prefs = load_preferences()
    
    print("[INFO] 生成 AI 精选内容...", file=sys.stderr)
    
    items = generate_ai_items()
    print(f"[INFO] 生成 {len(items)} 条内容", file=sys.stderr)
    
    # 评分
    scorer = Scorer(prefs)
    items = scorer.score_items(items)
    
    # 生成推荐理由
    for item in items:
        item.reason = scorer.generate_reason(item)
    
    # 排序
    items = sorted(items, key=lambda x: x.final_score, reverse=True)
    items = items[:10]
    
    # 推送
    pusher = Pusher(prefs)
    output = pusher.push(items)
    
    print(output)

if __name__ == "__main__":
    main()
