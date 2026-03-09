# Claude OAuth 使用規範 - 官方澄清

**日期**: 2026-02-19
**來源**: Joe 分享

---

## 事件背景

### 誤會產生
- Andrew Warner 發文稱「Claude OAuth 官方禁止用於 OpenClaw」
- 開發者社群一片恐慌
- 部分人考慮轉向 ChatGPT

### 官方澄清
Anthropic 的 Thariq (Claude Agent SDK 團隊) 親自說明：

> 「抱歉，這次文件清理造成了誤解。其實：
> - 本地開發、實驗 → 可以用訂閱 ✅
> - 商業用途（build a business on top of Agent SDK） → 請用 API Key ❌」

---

## 規範解讀

| 使用場景 | OAuth 訂閱 | API Key |
|----------|------------|---------|
| 本地開發/實驗 | ✅ 允許 | ✅ |
| 個人專案 | ✅ 允許 | ✅ |
| 商業產品 | ❌ 禁止 | ✅ 必須 |
| OpenClaw 整合 | ⚠️ 灰色地帶 | ✅ 建議 |

---

## 風險評估

| 場景 | 風險 |
|------|------|
| 個人使用 OpenClaw | 低 |
| 免費版 OAuth | 低 |
| Pro/Max 訂閱 OAuth | 中 |
| 年繳訂閱 OAuth | 高 (被Ban風險) |
| 商業用途 | 高 |

---

## 建議做法

### 短期
- 個人使用：維持現狀
- 避免年繳訂閱用於 OpenClaw

### 中期
- 準備 OpenAI OAuth 作為備援
- 評估 MiniMax 本地方案

### 長期
- 建立多元模型策略
- 減少單一 provider 依賴

---

## 我們的立場

- 已有 **MiniMax** 雲端備援
- **Ollama** 本地模型 80% 任務
- **model-dispatcher** 自動調度
- 維持多元供應商策略

---

## 相關討論

- OpenClaw vs Antigravity：帳號 Ban 風險
- OpenAI OAuth：Peter Steinberger 確認可用

---
