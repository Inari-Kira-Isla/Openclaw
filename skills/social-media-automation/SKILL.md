---
name: social-media-automation
description: 全自動社群媒體經營機器人 - OpenClaw + OpenAI + Postiz
metadata:
  openclaw:
    emoji: "🤖"
    version: "1.0"
    date: "2026-02-19"
---

# 全自動社群媒體經營機器人

## 概述

使用 OpenClaw + OpenAI Image Generation + Postiz 实现零人力、自动化的社群媒体经营。

## 技術堆疊

| 元件 | 功能 | 成本 |
|------|------|------|
| OpenClaw | Agent 核心決策 | $0 |
| OpenAI API | AI 圖片生成 | 按量計費 |
| Postiz | 社群排程發布 | $0-29/月 |
| n8n | 工作流自動化 | $0 |

## 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│                    全自動社群經營流程                           │
├─────────────────────────────────────────────────────────────┤
│  1. 內容靈感 (OpenClaw)                                     │
│     ↓                                                        │
│  2. 圖片生成 (OpenAI DALL-E)                               │
│     ↓                                                        │
│  3. 文案撰寫 (OpenClaw + Ollama)                          │
│     ↓                                                        │
│  4. 排程發布 (Postiz)                                      │
│     ↓                                                        │
│  5. 數據追蹤 (n8n)                                         │
└─────────────────────────────────────────────────────────────┘
```

## 實現步驟

### 1. OpenAI 圖片生成

```python
import openai

response = openai.Image.create(
  prompt="時尚品牌形象照片，簡約風格",
  n=4,
  size="1024x1024"
)
```

### 2. Postiz API 整合

```python
import requests

def post_to_social(platform, image_url, caption):
    response = requests.post(
        "https://api.postiz.com/v1/posts",
        headers={"Authorization": f"Bearer {POSTIZ_API_KEY}"},
        json={
            "platform": platform,
            "media": [{"url": image_url}],
            "content": caption,
            "scheduled_at": "2026-02-20T10:00:00Z"
        }
    )
    return response.json()
```

### 3. n8n Workflow

- 觸發：每日定時
- 動作：生成內容 → 製圖 → 發布

## 支援平台

- Instagram
- Facebook
- Twitter/X
- LinkedIn
- TikTok

## 自動化程度

| レベル | 內容 |
|--------|------|
| 🌱 初級 | 圖片 + 文案生成，手動發布 |
| 🚀 中級 | 自動生成 + 排程發布 |
| 🤖 高級 | 完全自動化 + 數據優化 |

## 應用案例

### Lazy Uni Shop

- 產品圖片自動生成
- 社群貼文排程
- 客戶訊息自動回覆

## 相關技能

- `facebook-messenger-handler` - FB 訊息處理
- `whatsapp-handler` - WhatsApp 處理
- `n8n-workflow` - 自動化排程

---
