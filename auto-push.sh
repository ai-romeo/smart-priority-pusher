#!/bin/bash
# 自动推送到 GitHub 脚本

set -e

echo "🚀 推送到 GitHub..."
echo "=================="
echo ""

# 配置 Git 用户信息
git config user.email "ai-romeo@users.noreply.github.com"
git config user.name "ai-romeo"

# 配置凭证管理器（记住密码）
git config credential.helper store

# 推送
echo "正在推送到：https://github.com/ai-romeo/smart-priority-pusher"
echo ""
echo "请输入 GitHub Token（粘贴后回车）："
read -s TOKEN

export GIT_ASKPASS=/bin/echo
git push -u origin main

echo ""
echo "✅ 推送完成！"
echo ""
echo "访问仓库：https://github.com/ai-romeo/smart-priority-pusher"
