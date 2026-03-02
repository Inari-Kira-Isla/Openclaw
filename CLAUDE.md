# 待處理反饋

## 2026-03-01

### 對話結束鉤子 - RAG儲存 + Session清理
- **來源**: Joe
- **需求**: 對話結束後儲存到RAG資料庫，然後刪除Session保持系統乾淨
- **狀態**: 規劃中

**可行方案**:
1. 建立 `session-cleanup`鉤子
2. 觸發條件: session idle超時或明確結束
3. 動作: 擷取對話摘要 → 存向量資料庫 → 刪除session
4. 可用工具: `sessions_list` + `sessions_history` + vector DB

---
