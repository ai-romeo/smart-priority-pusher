# Smart Priority Pusher / 智能优先级推送

> 🤖 AI Agent Skill - 每日 X (Twitter) 精选推送

## 技能简介

从 25 个精选 X 账号（AI/创业/个人成长/prompt）自动抓取每日推文，智能打分排序，推送 Top 30 精选内容。

**核心优势：**
- 📊 数据集中管理 - 所有数据存储在 GitHub 仓库
- 🚀 开箱即用 - 用户无需配置，直接复制 skill 即可使用
- 🔄 每日自动更新 - 保留最近 7 天数据
- 🎯 智能排序 - 按质量分数优先级推送

## 使用方法

### 方式 1：OpenClaw 调用

```
用 $smart-priority-pusher 获取今天的 AI 精选
```

### 方式 2：命令行

```bash
# 获取最新数据
python scripts/fetch_data.py

# 获取指定日期
python scripts/fetch_data.py --date 2026-03-20

# 输出 JSON
python scripts/fetch_data.py --json --top 10
```

### 方式 3：直接读取

```bash
# 克隆仓库
git clone https://github.com/ai-romeo/smart-priority-pusher.git
cd smart-priority-pusher

# 查看最新数据
cat data/daily/2026-03-20.json
```

## 数据源

**X 账号 (25 个)：**
- AI: Andrej Karpathy, Josh Woodward, John Rush
- 创业：Garry Tan, Paul Graham
- 个人成长：Naval, Alex Hormozi, Huberman, DAN KOE, Ray Dalio
- AI 自媒体：李继刚，向阳乔木，宝玉，Orange AI, 凡人小北
- prompt: Oogie, TechieSA, Amira Zairi
- AI builder: Zara Zhang
- storyteller: Ish Verduzco, Lulu Cheng Meservey

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

## 文件结构

```
smart-priority-pusher/
├── SKILL.md                 # Skill 定义
├── README.md                # 项目说明
├── scripts/
│   ├── fetch_data.py        # 数据获取脚本
│   ├── x_fetch_daily.py     # X 抓取脚本（服务端用）
│   └── daily_push.py        # 每日推送脚本（服务端用）
├── data/
│   └── daily/               # 每日数据（7 天）
│       ├── 2026-03-20.json
│       └── ...
└── config/
    └── x_sources.json       # X 账号配置
```

## 安装方式

### 复制 Skill

```bash
# 克隆到 OpenClaw workspace
cd /path/to/openclaw/workspace
git clone https://github.com/ai-romeo/smart-priority-pusher.git skills/smart-priority-pusher
```

### 使用 Skill

在 OpenClaw 中调用：
```
用 $smart-priority-pusher 获取今天的精选
```

## 定时更新

**服务端（有网络环境）：**

```bash
# 每天早上 8 点执行
0 8 * * * cd /path/to/smart-priority-pusher && \
  python scripts/x_fetch_daily.py --output data/daily/$(date +\%Y-\%m-\%d).json && \
  git add . && \
  git commit -m "daily: $(date +\%Y-\%m-\%d)" && \
  git push
```

**用户端：**
- 无需配置
- 自动从 GitHub 获取最新数据
- 保留 7 天历史记录

## 配置说明

### 添加新账号

编辑 `config/x_sources.json`：

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

编辑 `scripts/fetch_data.py` 中的 `--max` 参数。

## 注意事项

1. **数据更新** - 每天自动更新，用户拉取最新数据
2. **网络要求** - 用户只需能访问 GitHub，无需梯子
3. **数据保留** - 滚动保留 7 天数据
4. **推送时间** - 建议每天早上 8 点推送

## 许可证

MIT License

## 反馈

- GitHub Issues: https://github.com/ai-romeo/smart-priority-pusher/issues
- 项目主页：https://github.com/ai-romeo/smart-priority-pusher

---

*Created with ❤️ by [ai-romeo](https://github.com/ai-romeo)*
