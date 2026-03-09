---
name: mcp_builder
description: MCP Server 建構與骨架生成。當需要快速建立 MCP Server 專案時觸發。
metadata: { "openclaw": { "emoji": "🏗️" } }
---

# MCP Server 建構

快速建立 MCP Server 專案，包含專案結構、程式碼模板、依賴配置與測試框架。

## 操作 / 工作流程

1. **需求確認** — 確認 Server 名稱、功能描述、需要的 Tool 列表
2. **骨架生成** — 建立專案目錄結構：
   ```
   mcp-server-{name}/
   ├── src/
   │   ├── index.ts          # 入口檔
   │   ├── server.ts         # Server 類別
   │   └── tools/            # Tool 定義
   ├── tests/
   │   └── server.test.ts
   ├── package.json
   ├── tsconfig.json
   └── README.md
   ```
3. **程式碼生成** — 使用 `@modelcontextprotocol/sdk` 產生 Server 類別與 Tool 定義
4. **依賴安裝** — 執行 `npm init -y && npm install @modelcontextprotocol/sdk`
5. **編譯驗證** — 執行 `npx tsc` 確認編譯通過

## 參數

| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| name | string | — | Server 名稱（小寫、連字符） |
| tools | array | [] | Tool 定義列表 |
| description | string | — | Server 功能描述 |
| transport | string | stdio | 傳輸方式：stdio / http |

## 輸出格式

```
🏗️ MCP Server 已建立
名稱：mcp-server-[name]
路徑：[專案路徑]
工具數：[N] 個
狀態：編譯通過 ✅

下一步：
1. cd mcp-server-[name]
2. 編輯 src/tools/ 加入業務邏輯
3. npx tsc && node dist/index.js
```

## 錯誤處理

| 錯誤 | 處理 |
|------|------|
| 目錄已存在 | 詢問是否覆蓋或使用新名稱 |
| npm install 失敗 | 檢查網路連線與 Node.js 版本 |
| TypeScript 編譯失敗 | 列出錯誤訊息，自動修復常見問題 |
| SDK 版本不相容 | 建議升級 Node.js 或降級 SDK |

## 使用範例

- "幫我建立一個 MCP Server"
- "建一個有天氣查詢工具的 MCP Server"
- "用 HTTP 傳輸模式建立 MCP Server"
