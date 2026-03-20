# 📌 上传到 GitHub 指南

## 快速开始

### 1. 在 GitHub 创建新仓库

访问 https://github.com/new，创建名为 `smart-priority-pusher` 的空仓库

### 2. 初始化 Git 并推送

```bash
# 进入项目目录
cd smart-priority-pusher

# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Smart Priority Pusher"

# 关联远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/smart-priority-pusher.git

# 推送
git push -u origin main
```

### 3. 如果提示分支名问题

```bash
# 修改默认分支名为 main
git branch -M main
git push -u origin main
```

## 项目文件清单

上传到 GitHub 的文件：

```
smart-priority-pusher/
├── README.md                 ← 使用 README_STANDALONE.md 重命名
├── LICENSE                   ✓
├── requirements.txt          ✓
├── config/
│   ├── sources.json          ✓
│   └── user_preferences.json ✓
├── scripts/
│   ├── push_priority.py      ✓
│   └── demo_push.py          ✓
└── .gitignore               ← 创建（排除 cache/）
```

## 创建 .gitignore

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.env

# 缓存
cache/
*.cache

# IDE
.vscode/
.idea/
*.swp
*.swo

# 系统文件
.DS_Store
Thumbs.db

# 日志
*.log
EOF
```

## 完整命令清单

```bash
# 1. 创建 .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
cache/
.vscode/
.idea/
*.log
.DS_Store
EOF

# 2. 重命名 README
mv README_STANDALONE.md README.md

# 3. Git 初始化
git init
git branch -M main
git add .
git commit -m "Initial commit: Smart Priority Pusher

- 多源信息聚合 (RSS/API/网页)
- 智能分类和 10 分制打分
- 基于用户偏好的优先级排序
- Top 10 推送，支持 Markdown/JSON 格式
- 去重和缓存机制
- 可配置的信息源和用户偏好

基于 erduo-skills 优化设计"

# 4. 关联远程（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/smart-priority-pusher.git

# 5. 推送
git push -u origin main
```

## 后续更新

```bash
# 修改后推送更新
git add .
git commit -m "feat: 更新说明"
git push
```

## GitHub Pages（可选）

如果需要展示项目页面，可以启用 GitHub Pages：

1. 仓库 Settings → Pages
2. Source 选择 `main` 分支
3. 保存后访问 `https://YOUR_USERNAME.github.io/smart-priority-pusher/`

## 添加 Badge

在 README.md 顶部添加：

```markdown
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Stars](https://img.shields.io/github/stars/YOUR_USERNAME/smart-priority-pusher.svg)](https://github.com/YOUR_USERNAME/smart-priority-pusher)
```

---

完成！🎉 你的项目已经上传到 GitHub 了！
