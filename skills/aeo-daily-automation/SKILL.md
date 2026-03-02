---
name: aeo-daily-automation
description: |
  AEO 網站每日自動化。當需要定時生成 AI 教學內容、發布網站、更新內容時使用。
  適用場景：(1) 每日自動生成 AI 提示詞教學 (2) 定時發布新內容到網站 (3) 豐富 AI 知識庫
metadata:
  {
    "openclaw": { "emoji": "📅", "requires": { "anyTools": ["exec", "message"] } },
  }
---

# AEO Daily Automation

每日自動生成 AI 教學內容並發布

## 快速開始

```bash
# 完整流程：生成 + 部署
python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_daily.py full

# 單獨生成
python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_daily.py generate

# 單獨部署
python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_daily.py deploy

# 查看內容列表
python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_content.py list
```

## OpenClaw 整合

### 每日自動執行

```javascript
// 每日早上執行的腳本
const { exec } = require('child_process');

// 生成 + 部署
exec('python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_daily.py full', 
  (error, stdout, stderr) => {
    if (error) {
      // 
      message({
失敗通知        action: "send",
        target: "group",
        message: `❌ AEO 每日生成失敗\n\n${stderr}`
      });
      return;
    }
    
    // 成功通知
    message({
      action: "send",
      target: "group",
      message: `✅ AEO 每日更新完成\n\n${stdout}`
    });
  }
);
```

### 生成特定類型

```javascript
// 生成系統提示詞
exec('python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_content.py generate --type system_prompt --topic "新主題"');

// 生成工具教學
exec('python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_content.py generate --type tool_setup --topic "新工具"');

// 生成工作流
exec('python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_content.py generate --type workflow --topic "新工作流"');
```

### 排程設定

使用 OpenClaw heartbeat：

```javascript
// config
heartbeat: {
  "aeo-daily": {
    "schedule": "0 7 * * *",  // 每天早上 7 點
    "task": "python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_daily.py full",
    "notify": true
  }
}
```

## 內容類型

| 類型 | 說明 | 範例 |
|------|------|------|
| system_prompt | 系統提示詞 | 專業程式設計師、數據分析師 |
| prompt_template | 提示詞模板 | 文章摘要、郵件回覆 |
| tool_setup | 工具設定 | OpenClaw 安裝、Ollama 部署 |
| workflow | 工作流 | 每日自動化、資料同步 |

## 統計

```
📚 目前內容: 24 篇
📅 每日生成: 2-3 篇
🌐 網站更新: 每日自動
```

## 監控

```bash
# 查看日誌
tail -f /tmp/aeo-daily.log

# 測試生成
python3 ~/.openclaw/workspace/aeo-site/scripts/aeo_daily.py generate
```
