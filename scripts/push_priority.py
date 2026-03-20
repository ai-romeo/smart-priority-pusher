#!/usr/bin/env python3
"""
Smart Priority Pusher - 智能优先级推送

多源信息聚合 → 智能分类打分 → 优先级推送 Top 10
"""

import json
import hashlib
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import feedparser
import requests
from bs4 import BeautifulSoup


# ============== 配置 ==============

SKILL_DIR = Path(__file__).parent.parent
CONFIG_DIR = SKILL_DIR / "config"
CACHE_DIR = SKILL_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)

# ============== 数据模型 ==============

@dataclass
class Item:
    """信息项"""
    title: str
    url: str
    source: str
    category: str
    summary: str
    published_at: Optional[str]
    fetched_at: str
    
    # 评分相关
    base_score: float = 5.0
    final_score: float = 0.0
    reason: str = ""
    
    def content_hash(self) -> str:
        """生成内容哈希用于去重"""
        content = f"{self.title}{self.summary}"
        return hashlib.md5(content.encode()).hexdigest()


# ============== 信息源抓取 ==============

class SourceFetcher:
    """信息源抓取器"""
    
    def __init__(self, sources_config: Dict):
        self.sources = sources_config
    
    def fetch_all(self, hours: int = 24) -> List[Item]:
        """抓取所有启用的信息源"""
        all_items = []
        
        # RSS 源
        for source in self.sources.get("rss", []):
            if source.get("enabled", True):
                items = self._fetch_rss(source, hours)
                all_items.extend(items)
        
        # API 源
        for source in self.sources.get("api", []):
            if source.get("enabled", True):
                items = self._fetch_api(source, hours)
                all_items.extend(items)
        
        # 网页源
        for source in self.sources.get("web", []):
            if source.get("enabled", False):
                items = self._fetch_web(source, hours)
                all_items.extend(items)
        
        return all_items
    
    def _fetch_rss(self, source: Dict, hours: int) -> List[Item]:
        """抓取 RSS 源"""
        items = []
        try:
            feed = feedparser.parse(source["url"])
            cutoff = datetime.utcnow() - timedelta(hours=hours)
            
            for entry in feed.entries[:50]:  # 限制每个源最多 50 条
                published = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])
                
                if published and published < cutoff:
                    continue
                
                item = Item(
                    title=entry.get("title", "无标题"),
                    url=entry.get("link", ""),
                    source=source["name"],
                    category=source.get("category", "general"),
                    summary=entry.get("summary", entry.get("description", ""))[:500],
                    published_at=published.isoformat() if published else None,
                    fetched_at=datetime.utcnow().isoformat()
                )
                items.append(item)
        except Exception as e:
            print(f"[WARN] RSS 抓取失败 {source['name']}: {e}", file=sys.stderr)
        
        return items
    
    def _fetch_api(self, source: Dict, hours: int) -> List[Item]:
        """抓取 API 源"""
        items = []
        try:
            params = source.get("params", {})
            response = requests.get(source["endpoint"], params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # GitHub API 示例
            if "github" in source["endpoint"].lower():
                for repo in data.get("items", [])[:20]:
                    item = Item(
                        title=repo.get("full_name", "Unknown"),
                        url=repo.get("html_url", ""),
                        source=source["name"],
                        category=source.get("category", "dev"),
                        summary=repo.get("description", "") or "",
                        published_at=None,
                        fetched_at=datetime.utcnow().isoformat()
                    )
                    items.append(item)
        except Exception as e:
            print(f"[WARN] API 抓取失败 {source['name']}: {e}", file=sys.stderr)
        
        return items
    
    def _fetch_web(self, source: Dict, hours: int) -> List[Item]:
        """抓取网页"""
        items = []
        try:
            response = requests.get(source["url"], timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 根据选择器提取内容
            selector = source.get("selector", "article")
            elements = soup.select(selector)
            
            for elem in elements[:20]:
                title_elem = elem.find(["h1", "h2", "h3", "a"])
                if title_elem:
                    item = Item(
                        title=title_elem.get_text(strip=True),
                        url=source["url"],
                        source=source["name"],
                        category=source.get("category", "general"),
                        summary=elem.get_text(strip=True)[:300],
                        published_at=None,
                        fetched_at=datetime.utcnow().isoformat()
                    )
                    items.append(item)
        except Exception as e:
            print(f"[WARN] 网页抓取失败 {source['name']}: {e}", file=sys.stderr)
        
        return items


# ============== 去重 ==============

class Deduplicator:
    """去重器"""
    
    def __init__(self):
        self.seen_urls = set()
        self.seen_hashes = set()
        self._load_cache()
    
    def _load_cache(self):
        """加载缓存"""
        cache_file = CACHE_DIR / "pushed_items.json"
        if cache_file.exists():
            try:
                with open(cache_file) as f:
                    data = json.load(f)
                    # 7 天内已推送的不重复
                    cutoff = (datetime.utcnow() - timedelta(days=7)).isoformat()
                    for item in data:
                        if item.get("fetched_at", "") > cutoff:
                            self.seen_urls.add(item.get("url", ""))
                            self.seen_hashes.add(item.get("hash", ""))
            except:
                pass
    
    def deduplicate(self, items: List[Item]) -> List[Item]:
        """去重"""
        unique = []
        for item in items:
            url_hash = item.url
            content_hash = item.content_hash()
            
            if url_hash in self.seen_urls:
                continue
            if content_hash in self.seen_hashes:
                continue
            
            self.seen_urls.add(url_hash)
            self.seen_hashes.add(content_hash)
            unique.append(item)
        
        return unique
    
    def save_cache(self, items: List[Item]):
        """保存缓存"""
        cache_file = CACHE_DIR / "pushed_items.json"
        data = [
            {"url": item.url, "hash": item.content_hash(), "fetched_at": item.fetched_at}
            for item in items
        ]
        with open(cache_file, "w") as f:
            json.dump(data, f, indent=2)


# ============== 评分 ==============

class Scorer:
    """评分器"""
    
    def __init__(self, preferences: Dict):
        self.prefs = preferences
    
    def score_items(self, items: List[Item]) -> List[Item]:
        """对所有项目评分"""
        for item in items:
            item.final_score = self._calculate_score(item)
        return items
    
    def _calculate_score(self, item: Item) -> float:
        """计算综合评分"""
        # 基础分 (5.0 为基准)
        base = self._assess_quality(item)
        
        # 源权重
        source_weight = self._get_source_weight(item.source)
        
        # 类别优先级
        category_priority = self._get_category_priority(item.category)
        
        # 时效加分
        time_bonus = self._time_bonus(item.published_at)
        
        # 相关性加分
        relevance_bonus = self._relevance_bonus(item)
        
        # 综合计算
        score = base * source_weight * category_priority + time_bonus + relevance_bonus
        return min(10.0, max(0.0, score))  # 限制在 0-10
    
    def _assess_quality(self, item: Item) -> float:
        """评估内容质量 (0-10)"""
        score = 5.0
        
        # 标题长度适中
        if 20 < len(item.title) < 80:
            score += 1.0
        
        # 有摘要
        if item.summary and len(item.summary) > 50:
            score += 1.5
        
        # 避免营销词汇
        ignore_keywords = self.prefs.get("ignoreKeywords", [])
        for keyword in ignore_keywords:
            if keyword in item.title or keyword in item.summary:
                score -= 2.0
        
        return score
    
    def _get_source_weight(self, source: str) -> float:
        """获取源权重"""
        # 简化：根据源名称返回权重
        if "hacker" in source.lower():
            return 1.2
        if "hugging" in source.lower():
            return 1.3
        if "github" in source.lower():
            return 1.1
        return 1.0
    
    def _get_category_priority(self, category: str) -> float:
        """获取类别优先级"""
        categories = self.prefs.get("categories", {})
        if category in categories:
            return categories[category].get("priority", 1.0)
        return 1.0
    
    def _time_bonus(self, published_at: Optional[str]) -> float:
        """时效加分 (0-2)"""
        if not published_at:
            return 0.5
        
        try:
            published = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
            hours_ago = (datetime.utcnow() - published.replace(tzinfo=None)).total_seconds() / 3600
            
            if hours_ago < 2:
                return 2.0
            elif hours_ago < 6:
                return 1.5
            elif hours_ago < 12:
                return 1.0
            elif hours_ago < 24:
                return 0.5
            else:
                return 0.0
        except:
            return 0.5
    
    def _relevance_bonus(self, item: Item) -> float:
        """相关性加分 (0-3)"""
        bonus = 0.0
        interests = self.prefs.get("interests", [])
        
        text = f"{item.title} {item.summary}".lower()
        for interest in interests:
            if interest.lower() in text:
                bonus += 1.0
        
        return min(3.0, bonus)
    
    def generate_reason(self, item: Item) -> str:
        """生成推荐理由"""
        reasons = []
        
        if item.final_score >= 9.0:
            reasons.append("高质量内容")
        
        interests = self.prefs.get("interests", [])
        text = f"{item.title} {item.summary}".lower()
        for interest in interests:
            if interest.lower() in text:
                reasons.append(f"匹配兴趣：{interest}")
                break
        
        if item.category in self.prefs.get("categories", {}):
            cat_name = self.prefs["categories"][item.category].get("displayName", item.category)
            reasons.append(f"分类：{cat_name}")
        
        return " | ".join(reasons) if reasons else "值得关注的内容"


# ============== 推送 ==============

class Pusher:
    """推送器"""
    
    def __init__(self, preferences: Dict):
        self.prefs = preferences.get("pushSettings", {})
    
    def push(self, items: List[Item]) -> str:
        """生成推送消息"""
        format_type = self.prefs.get("format", "markdown")
        
        if format_type == "json":
            return self._format_json(items)
        else:
            return self._format_markdown(items)
    
    def _format_markdown(self, items: List[Item]) -> str:
        """Markdown 格式"""
        lines = [
            f"📊 今日精选 Top {len(items)} ({datetime.now().strftime('%Y-%m-%d')})",
            ""
        ]
        
        medals = ["🥇", "🥈", "🥉"]
        
        for i, item in enumerate(items):
            medal = medals[i] if i < 3 else f"{i+1}."
            
            lines.append(f"{medal} [{item.final_score:.1f}] {item.title}")
            lines.append(f"   来源：{item.source} | 分类：{item.category}")
            
            if self.prefs.get("includeReason", True) and item.reason:
                lines.append(f"   推荐语：{item.reason}")
            
            lines.append(f"   🔗 {item.url}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _format_json(self, items: List[Item]) -> str:
        """JSON 格式"""
        data = {
            "timestamp": datetime.utcnow().isoformat(),
            "totalFetched": len(items),
            "topItems": [
                {
                    "rank": i + 1,
                    "score": round(item.final_score, 1),
                    "title": item.title,
                    "source": item.source,
                    "category": item.category,
                    "url": item.url,
                    "summary": item.summary,
                    "reason": item.reason,
                    "publishedAt": item.published_at
                }
                for i, item in enumerate(items)
            ]
        }
        return json.dumps(data, ensure_ascii=False, indent=2)


# ============== 主流程 ==============

def load_config():
    """加载配置"""
    sources_file = CONFIG_DIR / "sources.json"
    prefs_file = CONFIG_DIR / "user_preferences.json"
    
    with open(sources_file) as f:
        sources = json.load(f)
    
    with open(prefs_file) as f:
        prefs = json.load(f)
    
    return sources, prefs


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="智能优先级推送")
    parser.add_argument("--hours", type=int, default=24, help="时间范围 (小时)")
    parser.add_argument("--top", type=int, default=10, help="推送数量")
    parser.add_argument("--category", type=str, help="指定类别 (逗号分隔)")
    parser.add_argument("--min-score", type=float, default=0, help="最低分数")
    parser.add_argument("--format", type=str, choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", type=str, help="输出到文件")
    
    args = parser.parse_args()
    
    # 加载配置
    sources, prefs = load_config()
    prefs["pushSettings"]["format"] = args.format
    
    # 执行流程
    print(f"[INFO] 开始抓取过去 {args.hours} 小时的内容...", file=sys.stderr)
    
    fetcher = SourceFetcher(sources)
    items = fetcher.fetch_all(hours=args.hours)
    print(f"[INFO] 抓取完成，共 {len(items)} 条", file=sys.stderr)
    
    dedup = Deduplicator()
    items = dedup.deduplicate(items)
    print(f"[INFO] 去重后剩余 {len(items)} 条", file=sys.stderr)
    
    scorer = Scorer(prefs)
    items = scorer.score_items(items)
    
    # 生成推荐理由
    for item in items:
        item.reason = scorer.generate_reason(item)
    
    # 过滤和排序
    min_score = max(args.min_score, prefs.get("minScore", 6.0))
    items = [i for i in items if i.final_score >= min_score]
    
    if args.category:
        categories = [c.strip() for c in args.category.split(",")]
        items = [i for i in items if i.category in categories]
    
    items = sorted(items, key=lambda x: x.final_score, reverse=True)
    items = items[:args.top]
    
    print(f"[INFO] 最终筛选 {len(items)} 条", file=sys.stderr)
    
    # 推送
    pusher = Pusher(prefs)
    output = pusher.push(items)
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"[INFO] 已保存到 {args.output}", file=sys.stderr)
    else:
        print(output)
    
    # 保存缓存
    dedup.save_cache(items)


if __name__ == "__main__":
    main()
