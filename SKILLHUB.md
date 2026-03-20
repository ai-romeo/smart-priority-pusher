# Smart Priority Pusher

> 📊 每日 X (Twitter) 精选推送 - 25 个账号智能打分 Top 30

## 技能简介

从 25 个精选 X 账号（AI/创业/个人成长/prompt）自动抓取每日推文，按质量分数排序，推送 Top 30 精选内容。

**核心优势：**
- 📊 数据集中管理 - 所有数据存储在 GitHub 仓库
- 🚀 开箱即用 - 无需配置，直接从 GitHub 获取数据
- 🔄 每日自动更新 - 保留最近 7 天数据
- 🎯 智能排序 - 按质量分数优先级推送

## 安装

```bash
skillhub install smart-priority-pusher
```

或手动安装：

```bash
# 克隆到 skills 目录
git clone https://github.com/ai-romeo/smart-priority-pusher.git /path/to/openclaw/workspace/skills/smart-priority-pusher
```

## 使用

### 方式 1：命令行

```bash
# 获取今日精选
python skills/smart-priority-pusher/scripts/fetch_data.py

# 获取指定日期
python skills/smart-priority-pusher/scripts/fetch_data.py --date 2026-03-20

# 只看前 10 条
python skills/smart-priority-pusher/scripts/fetch_data.py --top 10

# 输出 JSON
python skills/smart-priority-pusher/scripts/fetch_data.py --json
```

### 方式 2：OpenClaw 调用

```
用 $smart-priority-pusher 获取今天的 AI 精选
```

### 方式 3：直接读取

```bash
cat skills/smart-priority-pusher/data/daily/2026-03-20.json
```

## 数据源

**25 个精选 X 账号：**

- **AI (3)**: Andrej Karpathy, Josh Woodward, John Rush
- **创业 (2)**: Garry Tan, Paul Graham
- **个人成长 (8)**: Naval, Alex Hormozi, Huberman, DAN KOE, Ray Dalio 等
- **AI 自媒体 (5)**: 李继刚，向阳乔木，宝玉，Orange AI, 凡人小北
- **prompt (3)**: Oogie, TechieSA, Amira Zairi
- **AI builder (1)**: Zara Zhang
- **storyteller (2)**: Ish Verduzco, Lulu Cheng Meservey

**数据来源：** https://github.com/ai-romeo/smart-priority-pusher/tree/main/data/daily

## 数据格式

```json
{
  "date": "2026-03-20",
  "total_items": 25,
  "items": [
    {
      "rank": 1,
      "score": 9.5,
      "title": "标题",
      "source": "账号名称",
      "username": "@username",
      "url": "推文链接",
      "summary": "内容摘要",
      "reason": "推荐理由",
      "likes": 1234,
      "retweets": 567
    }
  ]
}
```

## 配置

### 添加新账号

编辑 `skills/smart-priority-pusher/config/x_sources.json`：

```json
{
  "type": "AI",
  "name": "账号名称",
  "url": "https://x.com/username",
  "username": "username",
  "enabled": true
}
```

### 调整推送数量

编辑 `scripts/fetch_data.py`，修改 `--top` 参数。

## 定时更新（服务端）

**有网络环境的服务器：**

```bash
# 每天执行（cron）
0 8 * * * cd /path/to/smart-priority-pusher && \
  python scripts/x_fetch_daily.py --output data/daily/$(date +\%Y-\%m-\%d).json && \
  git add . && \
  git commit -m "daily: $(date +\%Y-\%m-\%d)" && \
  git push
```

## 依赖

```bash
pip install requests feedparser beautifulsoup4
```

## 注意事项

1. **数据更新** - 每天自动更新，用户拉取最新数据
2. **网络要求** - 用户只需能访问 GitHub，无需梯子
3. **数据保留** - 滚动保留 7 天数据
4. **推送时间** - 建议每天早上 8 点推送

## 反馈

- GitHub Issues: https://github.com/ai-romeo/smart-priority-pusher/issues
- 项目主页：https://github.com/ai-romeo/smart-priority-pusher

---

*Created with ❤️ by [ai-romeo](https://github.com/ai-romeo)*
