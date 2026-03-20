# 推送命令清单

## 方式 1：使用 Personal Access Token（推荐）

### 1. 创建 Token
访问：https://github.com/settings/tokens
- 选择 "Generate new token (classic)"
- 勾选 `repo` 权限
- 生成后复制 token（只显示一次！）

### 2. 推送代码
```bash
cd /root/.openclaw/workspace-feishu-writer/github-upload/smart-priority-pusher

# 使用 token 推送（替换 YOUR_TOKEN）
git push -u origin main
# 输入用户名：emeo2018
# 输入密码：粘贴你的 token
```

---

## 方式 2：配置 SSH Key

### 1. 生成 SSH Key
```bash
ssh-keygen -t ed25519 -C "emeo2018@users.noreply.github.com"
# 一路回车即可
```

### 2. 添加 SSH Key 到 GitHub
```bash
cat ~/.ssh/id_ed25519.pub
# 复制输出内容
```

访问：https://github.com/settings/keys
- 点击 "New SSH key"
- 粘贴内容并保存

### 3. 切换为 SSH 地址并推送
```bash
cd /root/.openclaw/workspace-feishu-writer/github-upload/smart-priority-pusher
git remote set-url origin git@github.com:emeo2018/smart-priority-pusher.git
git push -u origin main
```

---

## 方式 3：使用 Git Credential Helper

```bash
# 配置凭证管理器
git config --global credential.helper store

# 推送（会提示输入一次，之后记住）
git push -u origin main
```

---

## ✅ 完成后

1. 访问仓库：https://github.com/emeo2018/smart-priority-pusher
2. 编辑 README.md，确认链接正确
3. 添加项目描述和标签
4. 启用 Issues（Settings → Features）

---

## 📌 快速验证

推送成功后，访问：
https://github.com/emeo2018/smart-priority-pusher

应该能看到完整的项目文件！
