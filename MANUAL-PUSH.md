# 手动推送指南

## ✅ SSH Key 已配置好

SSH 认证测试通过：
```
Hi ai-romeo! You've successfully authenticated
```

## 🚀 推送步骤

### 方式 1：在当前目录直接推送

```bash
cd /root/.openclaw/workspace-feishu-writer/github-upload/smart-priority-pusher

# 设置 Git 使用 SSH
git config --global url."git@github.com:".insteadOf "https://github.com/"

# 推送
git push origin main
```

### 方式 2：使用推送脚本

```bash
cd /root/.openclaw/workspace-feishu-writer/github-upload/smart-priority-pusher
./force-push.sh
```

### 方式 3：重新克隆（最可靠）

```bash
# 1. 用 SSH 方式克隆
cd /root/.openclaw/workspace-feishu-writer/github-upload
git clone git@github.com:ai-romeo/smart-priority-pusher.git fresh-push

# 2. 复制文件
cp -r smart-priority-pusher/* fresh-push/
cd fresh-push

# 3. 推送
git add .
git commit -m "Update from workspace"
git push
```

---

## 📋 当前状态

- ✅ SSH Key 已生成并添加到 GitHub
- ✅ 本地代码已提交（最新 commit: 848154a）
- ⏳ 等待推送到 GitHub

---

## ❓ 如果还有问题

检查 GitHub 上的 SSH Key：
1. 访问 https://github.com/settings/keys
2. 确认公钥已添加
3. 标题不限，内容必须是：
   ```
   ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIF/AXclfvDiVsD/kZxOxIT80xw8IndJa/LbI2kEr20NE
   ```
