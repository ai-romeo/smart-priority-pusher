#!/bin/bash
# 一键上传到 GitHub 脚本

set -e

echo "🚀 Smart Priority Pusher - 上传到 GitHub"
echo "=========================================="
echo ""

# 检查是否已安装 git
if ! command -v git &> /dev/null; then
    echo "❌ 错误：未找到 git，请先安装 git"
    exit 1
fi

# 获取 GitHub 用户名
read -p "请输入你的 GitHub 用户名：" GITHUB_USER
if [ -z "$GITHUB_USER" ]; then
    echo "❌ 错误：用户名不能为空"
    exit 1
fi

REPO_NAME="smart-priority-pusher"
REMOTE_URL="https://github.com/${GITHUB_USER}/${REPO_NAME}.git"

echo ""
echo "📦 准备上传到：${REMOTE_URL}"
echo ""

# 初始化 Git
if [ ! -d ".git" ]; then
    echo "📝 初始化 Git 仓库..."
    git init
    git branch -M main
fi

# 添加文件
echo "📋 添加文件..."
git add .

# 提交
echo "💾 提交更改..."
git commit -m "Initial commit: Smart Priority Pusher

- 多源信息聚合 (RSS/API/网页)
- 智能分类和 10 分制打分
- 基于用户偏好的优先级排序
- Top 10 推送，支持 Markdown/JSON 格式
- 去重和缓存机制
- 可配置的信息源和用户偏好

基于 erduo-skills 优化设计" || echo "⚠️  没有需要提交的更改"

# 检查是否已存在 remote
if git remote | grep -q "^origin$"; then
    echo "⚠️  已存在 origin remote，是否覆盖？(y/N)"
    read -p "> " confirm
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        git remote remove origin
    else
        echo "❌ 取消操作"
        exit 1
    fi
fi

# 添加 remote
echo "🔗 关联远程仓库..."
git remote add origin "$REMOTE_URL"

echo ""
echo "✅ 准备完成！接下来请执行："
echo ""
echo "1️⃣  在 GitHub 创建空仓库：${REMOTE_URL}"
echo "   访问：https://github.com/new"
echo "   仓库名：${REPO_NAME}"
echo ""
echo "2️⃣  然后运行："
echo "   git push -u origin main"
echo ""
echo "或者使用 SSH（如果你配置了 SSH key）："
echo "   git remote set-url origin git@github.com:${GITHUB_USER}/${REPO_NAME}.git"
echo "   git push -u origin main"
echo ""
