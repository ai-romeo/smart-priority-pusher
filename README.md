# Smart Priority Pusher / 智能优先级推送

> 🤖 AI Agent 技能 - 多源信息聚合 → 智能分类打分 → 优先级推送 Top 10

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**智能优先级推送** 是一个 AI Agent 技能，从多个信息源自动抓取内容，通过 AI 智能分析进行自动分类、质量打分、优先级排序，最终只推送最有价值的前 10 条内容。

## ✨ 核心功能

- 📥 **多源聚合** - RSS/Atom、REST API、网页抓取
- 🏷️ **自动分类** - 按主题/领域智能归类
- 📊 **智能打分** - 10 分制综合评分（质量 + 时效 + 相关性 + 来源）
- 🎯 **优先级排序** - 结合用户偏好加权
- 🚀 **Top 10 推送** - 只推送最有价值的内容
- 🔄 **去重缓存** - 7 天内不重复推送相同内容

## 📋 效果演示

```
📊 今日精选 Top 10 (2026-03-20)

🥇 [9.2] GPT-4.5 泄露：多模态能力重大突破
   来源：Hacker News | 分类：AI
   💡 高质量内容 | 匹配兴趣：AI
   🔗 https://news.ycombinator.com/item?id=xxx

🥈 [8.9] OpenClaw 2026.2.26 发布：支持子代理编排
   来源：GitHub Trending | 分类：DEV
   💡 匹配兴趣：开源
   🔗 https://github.com/openclaw/openclaw

🥉 [8.5] HuggingFace Transformers 5.0 正式发布
   来源：Hugging Face Papers | 分类：AI
   💡 高质量内容 | 匹配兴趣：AI
   🔗 https://huggingface.co/blog/transformers-5

4. [8.3] Cursor AI 新功能：全项目上下文理解
   来源：Product Hunt | 分类：PRODUCT
   💡 匹配兴趣：开发者工具
   🔗 https://www.producthunt.com/posts/cursor-ai
...
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/YOUR_USERNAME/smart-priority-pusher.git
cd smart-priority-pusher
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置信息源

编辑 `config/sources.json`：

```json
{
  "rss": [
    {
      "name": "Hacker News",
      "url": "https://news.ycombinator.com/rss",
      "category": "tech",
      "weight": 1.2,
      "enabled": true
    }
  ]
}
```

### 4. 配置个人偏好

编辑 `config/user_preferences.json`：

```json
{
  "interests": ["AI", "开源", "技术新闻"],
  "minScore": 6.0,
  "topN": 10
}
```

### 5. 运行推送

```bash
# 默认推送 Top 10
python scripts/push_priority.py

# 自定义参数
python scripts/push_priority.py --hours 48 --top 5 --min-score 7.0

# 输出 JSON 格式
python scripts/push_priority.py --format json

# 保存到文件
python scripts/push_priority.py --output report.md
```

## 📂 项目结构

```
smart-priority-pusher/
├── README.md                 # 项目说明
├── LICENSE                   # MIT 许可证
├── requirements.txt          # Python 依赖
├── config/
│   ├── sources.json          # 信息源配置
│   └── user_preferences.json # 用户偏好配置
├── scripts/
│   ├── push_priority.py      # 主推送脚本
│   └── demo_push.py          # 演示脚本（模拟数据）
└── cache/                    # 缓存目录（自动生成）
    └── pushed_items.json
```

## ⚙️ 配置说明

### 信息源配置 (sources.json)

支持三种类型的信息源：

**RSS/Atom 订阅**
```json
{
  "name": "Hacker News",
  "url": "https://news.ycombinator.com/rss",
  "category": "tech",
  "weight": 1.2,
  "enabled": true
}
```

**REST API**
```json
{
  "name": "GitHub Trending",
  "endpoint": "https://api.github.com/search/repositories",
  "params": {"q": "stars:>100", "sort": "stars"},
  "category": "dev",
  "weight": 1.1,
  "enabled": true
}
```

**网页抓取**
```json
{
  "name": "特定网页",
  "url": "https://example.com/news",
  "category": "custom",
  "selector": ".article-title",
  "weight": 0.8,
  "enabled": false
}
```

### 用户偏好配置 (user_preferences.json)

```json
{
  "interests": ["AI", "开源", "技术新闻", "产品发布"],
  "ignoreKeywords": ["营销", "广告", "付费课程"],
  "minScore": 6.0,
  "topN": 10,
  "timeRange": "24h",
  "categories": {
    "tech": { "priority": 1.2, "displayName": "技术" },
    "ai": { "priority": 1.5, "displayName": "人工智能" }
  }
}
```

## 📊 打分算法

**综合评分公式：**

```
总分 = 基础分 × 源权重 × 类别优先级 + 时效加分 + 相关性加分
```

| 维度 | 权重 | 说明 |
|------|------|------|
| 内容质量 | 40% | 信息密度、原创性、深度 |
| 时效性 | 20% | 发布时间越新分数越高 |
| 相关性 | 25% | 与用户兴趣匹配程度 |
| 来源可信度 | 15% | 信息源权威性 |

## 🔧 命令行参数

```bash
python scripts/push_priority.py [OPTIONS]

选项:
  --hours INT       时间范围（小时），默认 24
  --top INT         推送数量，默认 10
  --category TEXT   指定类别（逗号分隔）
  --min-score FLOAT 最低分数，默认 6.0
  --format TEXT     输出格式：markdown/json
  --output TEXT     输出到文件
  --help            显示帮助信息
```

## ⏰ 定时任务

配置 cron 定时执行：

```bash
# 每天早上 8 点推送
0 8 * * * cd /path/to/smart-priority-pusher && python scripts/push_priority.py

# 每 4 小时检查高优先级内容
0 */4 * * * cd /path/to/smart-priority-pusher && python scripts/push_priority.py --min-score 8.0
```

## 📝 使用示例

### 示例 1：只看 AI 相关内容

```bash
python scripts/push_priority.py --category ai --top 5
```

### 示例 2：获取过去 48 小时内容

```bash
python scripts/push_priority.py --hours 48 --format json --output report.json
```

### 示例 3：只推送 8 分以上高质量内容

```bash
python scripts/push_priority.py --min-score 8.0 --top 3
```

## 🔌 扩展开发

### 添加新信息源

在 `config/sources.json` 中添加配置即可。

### 自定义打分逻辑

继承 `scripts/push_priority.py` 中的 `Scorer` 类，实现自定义评分算法。

### 集成到 OpenClaw

将项目放入 OpenClaw 的 `skills/` 目录：

```bash
cp -r smart-priority-pusher /path/to/openclaw/workspace/skills/
```

然后在 OpenClaw 中调用：

```
用 $smart-priority-pusher 拉取过去 24 小时的信息，筛选 Top 10 推送给我
```

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📬 联系方式

- GitHub Issues: [提交问题](https://github.com/YOUR_USERNAME/smart-priority-pusher/issues)
- 项目主页：[GitHub](https://github.com/YOUR_USERNAME/smart-priority-pusher)

---

*基于 [erduo-skills](https://github.com/rookie-ricardo/erduo-skills) 的 daily-news-report 和 ak-rss-digest 优化设计*
