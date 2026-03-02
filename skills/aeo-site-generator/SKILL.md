---
name: aeo-site-generator
description: |
  AEO 網站內容生成器。當需要生成 AI 教學內容並發布到網站時使用。
  功能：(1) 根據主題生成各類 AI 教學文檔 (2) 系統提示詞生成 (3) 提示詞模板建立 (4) 
  工具設定教學 (5) 工作流說明 (6) 發布到本地網站。適用場景：(1) 每日 AI 知識分享 (2) 
  建立 AI 教學庫 (3) 生成 prompt 教程 (4) 記錄工具設定
metadata:
  {
    "openclaw": { "emoji": "🌐", "requires": { "anyTools": ["exec", "write", "read"] } },
  }
---

# AEO Site Generator

自動生成 AI 教學內容並發布

## 快速開始

```bash
# 生成內容
python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_content.py generate --type system_prompt --topic "程式設計師"

# 列出內容
python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_content.py list

# 啟動網站
python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_content.py serve
```

## 內容類型

| 類型 | 說明 | 範例 |
|------|------|------|
| system_prompt | 系統提示詞 | 專業程式設計師、數據分析師 |
| prompt_template | 提示詞模板 | 文章摘要、郵件回覆 |
| tool_setup | 工具設定 | OpenClaw 安裝、Ollama 部署 |
| workflow | 工作流 | 每日自動化、資料同步 |
| case_study | 案例分析 | 實際應用解析 |

## OpenClaw 整合

### 生成內容

```javascript
// 1. 生成系統提示詞
exec({
  command: "python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_content.py generate --type system_prompt --topic '產品經理'"
})

// 2. 生成提示詞模板
exec({
  command: "python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_content.py generate --type prompt_template --topic '會議記錄'"
})

// 3. 生成工具教學
exec({
  command: "python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_content.py generate --type tool_setup --topic 'n8n 工作流'"
})
```

### 發布流程

```javascript
// 1. 生成內容
const result = exec("python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_content.py generate --type system_prompt --topic '新主題'")

// 2. 啟動網站
exec("python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_content.py serve &")

// 3. 回報
message({
  action: "send",
  message: `✅ 內容已生成並發布\n\n${result.stdout}`
})
```

## AEO 優化

### Frontmatter 結構

```yaml
---
title: "標題"
type: system_prompt
date: 2026-03-02
tags: ["AI", "提示詞", "學習"]
---
```

### AI 友善標記

```markdown
## 角色描述
你是專業的...

## 核心能力
- 能力 1
- 能力 2

## 輸出格式
請以 Markdown 格式回覆

## 使用範例
輸入：...
輸出：...
```

## 每日自動化

### Cron 排程

```bash
# 每天早上 7 點生成內容
0 7 * * * python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_content.py generate --type random
```

### Telegram 回報

```javascript
// 每日內容生成完成後通知
message({
  action: "send",
  target: "group",
  message: "📚 今日 AI 教學內容已發布"
})
```

## 網站結構

```
aeo-site/
├── content/           # Markdown 內容
│   ├── 2026-03-02_系統提示詞.md
│   └── ...
├── scripts/
│   └── aeo_content.py  # 生成腳本
├── config.json         # 網站配置
└── public/            # 靜態資源
```

## 使用範例

### 用戶請求：生成一個程式設計師提示詞

```javascript
// 分析
const type = "system_prompt"
const topic = "專業程式設計師"

// 生成
exec({
  command: `python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_content.py generate --type ${type} --topic "${topic}"`
})

// 回報
message({
  action: "send",
  message: "✅ 已生成：專業程式設計師系統提示詞"
})
```

### 用戶請求：教我如何設定 Ollama

```javascript
exec({
  command: "python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_content.py generate --type tool_setup --topic 'Ollama 本地部署'"
})
```
