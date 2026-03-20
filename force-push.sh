#!/bin/bash
# 手动推送脚本

cd /root/.openclaw/workspace-feishu-writer/github-upload/smart-priority-pusher

# 使用 SSH 直接推送
echo "Testing SSH connection..."
ssh -i /root/.ssh/id_ed25519 -o IdentitiesOnly=yes -T git@github.com

echo ""
echo "Pushing to GitHub..."
git -c url."git@github.com:".insteadOf="https://github.com/" push origin main
