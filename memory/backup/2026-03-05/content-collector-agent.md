# content-collector - 趨勢收集 Agent

## 角色
- **功能**: 趨勢收集 + 關鍵字分析 + 熱度統計
- **觸發**: Cron 每小時
- **輸出**: 熱門話題清單 + 關鍵字建議

## 工作流程

### 1. 趨勢收集
```
每小時執行:
□ 抓取 HN/Reddit/Perplexity 熱門
□ 過濾 AI/Tech 相關主題
□ 評估話題潛力 (原創性 + 搜尋量)
```

### 2. 關鍵字分析
```
□ Google Trends API 查詢
□ 搜尋量估算
□ 競爭度評估
□ 長尾關鍵字建議
```

### 3. 輸出格式
```json
{
  "timestamp": "2026-03-02T13:00:00Z",
  "topics": [
    {
      "title": "MCP Protocol 最佳實踐",
      "keywords": ["MCP", "Model Context Protocol", "AI agents"],
      "searchVolume": "high",
      "competition": "medium",
      "priority": "high"
    }
  ],
  "suggested_articles": 5
}
```

## Cron 排程
```
0 * * * * (每小時)
```

## 儲存位置
- 輸出: memory/content-collector/{date}.json
- 熱門話題: memory/hot-topics/{date}.md

---

*Created: 2026-03-02*
