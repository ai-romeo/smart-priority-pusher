# 安装和使用指南

## 🚀 快速开始

### 方式 1：OpenClaw Skill（推荐）

```bash
# 1. 克隆到 OpenClaw workspace
cd /path/to/openclaw/workspace
git clone https://github.com/ai-romeo/smart-priority-pusher.git skills/smart-priority-pusher

# 2. 在 OpenClaw 中调用
用 $smart-priority-pusher 获取今天的精选
```

### 方式 2：独立使用

```bash
# 1. 克隆仓库
git clone https://github.com/ai-romeo/smart-priority-pusher.git
cd smart-priority-pusher

# 2. 获取最新数据
python scripts/fetch_data.py

# 3. 查看 JSON 格式
python scripts/fetch_data.py --json

# 4. 只看前 10 条
python scripts/fetch_data.py --top 10
```

### 方式 3：直接读取数据

```bash
# 1. 克隆仓库
git clone https://github.com/ai-romeo/smart-priority-pusher.git
cd smart-priority-pusher/data/daily

# 2. 查看最新数据
cat $(ls -t *.json | head -1)

# 3. 查看指定日期
cat 2026-03-20.json
```

---

## 📊 数据说明

**数据来源：** 25 个精选 X (Twitter) 账号

**分类：**
- AI (3): Andrej Karpathy, Josh Woodward, John Rush
- 创业 (2): Garry Tan, Paul Graham
- 个人成长 (8): Naval, Alex Hormozi, Huberman 等
- AI 自媒体 (5): 李继刚，向阳乔木，宝玉等
- prompt (3): Oogie, TechieSA, Amira Zairi
- AI builder (1): Zara Zhang
- storyteller (2): Ish Verduzco, Lulu Cheng Meservey

**更新频率：** 每天早上 8 点自动更新

**数据保留：** 滚动保留最近 7 天

---

## 🔧 配置说明

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

编辑 `scripts/fetch_data.py`，修改 `--top` 参数。

---

## 📦 文件结构

```
smart-priority-pusher/
├── SKILL.md                 # Skill 定义
├── README.md                # 项目说明
├── INSTALL.md               # 安装指南（本文件）
├── scripts/
│   ├── fetch_data.py        # 数据获取脚本（用户使用）
│   └── x_fetch_daily.py     # X 抓取脚本（服务端用）
├── data/
│   └── daily/               # 每日数据（7 天）
└── config/
    └── x_sources.json       # X 账号配置
```

---

## ⏰ 定时更新（服务端）

**有网络环境的服务器：**

```bash
# 安装依赖
pip install requests feedparser beautifulsoup4

# 每天执行（cron）
0 8 * * * cd /path/to/smart-priority-pusher && \
  python scripts/x_fetch_daily.py --output data/daily/$(date +\%Y-\%m-\%d).json && \
  git add . && \
  git commit -m "daily: $(date +\%Y-\%m-\%d)" && \
  git push
```

---

## ❓ 常见问题

### Q: 获取数据失败？
A: 检查是否能访问 GitHub Raw：
```bash
curl https://raw.githubusercontent.com/ai-romeo/smart-priority-pusher/main/data/daily/2026-03-20.json
```

### Q: 如何添加新账号？
A: 编辑 `config/x_sources.json`，添加账号信息。

### Q: 数据多久更新一次？
A: 每天早上 8 点自动更新。

### Q: 可以获取历史数据吗？
A: 可以，保留 7 天数据：
```bash
python scripts/fetch_data.py --date 2026-03-19
```

---

## 📬 反馈

- GitHub Issues: https://github.com/ai-romeo/smart-priority-pusher/issues
- 项目主页：https://github.com/ai-romeo/smart-priority-pusher

---

*Created with ❤️ by [ai-romeo](https://github.com/ai-romeo)*
