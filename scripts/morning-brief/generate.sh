#!/bin/bash
# Morning Brief 生成腳本
# 目標：11個區塊整合

DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M)

echo "=== Morning Brief $DATE $TIME ==="

# 區塊 1: 系統狀態
echo "1. 系統狀態..."
SYSTEM_STATUS=$(openclaw status 2>/dev/null | head -3)

# 區塊 2: Cron 運作
echo "2. Cron 狀態..."
CRON_COUNT=$(openclaw cron list 2>&1 | grep -c "running")

# 區塊 3: 向量數
echo "3. 向量數..."
VECTOR_COUNT=$(cd ~/.openclaw/workspace-evolution/lobster && python3 -c "from rag_system import RAGSystem; print(RAGSystem().get_stats().get('total_vectors',0))" 2>/dev/null)

# 區塊 4: 記憶變更
echo "4. 記憶變更..."
MEMORY_CHANGES=$(openclaw cron list 2>&1 | grep -c "記憶")

# 區塊 5: 錯誤監控
echo "5. 錯誤監控..."
ERROR_COUNT=$(openclaw cron list 2>&1 | grep -c "error")

# 區塊 6: 閉環系統
echo "6. 閉環..."
LOOP_COUNT=$(openclaw cron list 2>&1 | grep -c "閉環")

# 區塊 7: Hook 狀態
echo "7. Hook..."
HOOK_COUNT=$(openclaw cron list 2>&1 | grep -c "hook")

# 區塊 8: Agents 狀態
echo "8. Agents..."
AGENT_COUNT=$(openclaw cron list 2>&1 | grep -c "agent")

# 區塊 9: 學習系統
echo "9. 學習..."
LEARN_COUNT=$(openclaw cron list 2>&1 | grep -cE "learn|學習")

# 區塊 10: 備份狀態
echo "10. 備份..."
BACKUP_STATUS=$(ls -t ~/.openclaw/backup/202* 2>/dev/null | head -1)

# 區塊 11: 待辦事項
echo "11. 待辦..."
TODO="系統優化中"

# 輸出 Markdown
cat > ~/.openclaw/workspace-evolution/memory/morning-brief-$DATE.md << MD
# Morning Brief - $DATE

## 1. 系統狀態
\`\`\`
$SYSTEM_STATUS
\`\`\`

## 2. Cron 運作
- 運行中: $CRON_COUNT 個

## 3. 向量數
- 總數: $VECTOR_COUNT

## 4. 記憶變更
- 變更數: $MEMORY_CHANGES

## 5. 錯誤監控
- Error數: $ERROR_COUNT

## 6. 閉環系統
- 閉環數: $LOOP_COUNT

## 7. Hook 狀態
- Hook數: $HOOK_COUNT

## 8. Agents
- Agent數: $AGENT_COUNT

## 9. 學習系統
- 學習Cron: $LEARN_COUNT

## 10. 備份
- 最新: $BACKUP_STATUS

## 11. 待辦
- $TODO

---
生成時間: $TIME
MD

echo "=== 完成 ==="
echo "報告: ~/.openclaw/workspace-evolution/memory/morning-brief-$DATE.md"
