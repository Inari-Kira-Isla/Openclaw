# OpenClaw Docker 開發環境

## 沒有公開 Docker 映像

OpenClaw 是 Node.js 應用，沒有公開的 Docker Hub 映像。

---

## 替代方案：使用 --dev 模式

```bash
# 啟動開發版（自動隔離端口）
openclaw --dev
```

這會使用：
- 配置: `~/.openclaw-dev/config.yml`
- Gateway 端口: 19001
- API 端口: 19080

---

## 或者手動 Docker

如果你想自己 build Docker：

```dockerfile
FROM node:20-alpine

WORKDIR /app

# 全局安裝 OpenClaw
RUN npm install -g openclaw@latest

# 啟動
CMD ["openclaw"]
```

---

## 建議

直接使用 `openclaw --dev` 最簡單！
