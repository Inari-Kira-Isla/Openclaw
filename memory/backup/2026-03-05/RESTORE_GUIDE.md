# 系統崩潰恢復指南

---

## 恢復流程

### 1. 恢復配置

```bash
# 確認崩潰日期
DATE="20260301"  # 改為你既備份日期

# 恢復 openclaw 配置
cp ~/.openclaw/backup/$DATE/openclaw.json ~/.openclaw/
```

---

### 2. 恢復 Crons

由於 Crons 係導出既 text 檔案，需要人手重新建立：

```bash
# 查看既 Crons
cat ~/.openclaw/backup/$DATE/crons.txt
```

或者直接人手重新建立關鍵既 Cron Jobs：

```bash
# 系統健康檢查
openclaw cron add --name "系統健康" --cron "*/15 * * * *" --message "系統健康檢查" --target host

# 自動修復鉤子
openclaw cron add --name "auto-fix-hook" --cron "0 * * * *" --message "每小時自動修復" --target host

# 系統備份
openclaw cron add --name "系統備份" --cron "0 3 * * *" --message "每日03:00自動系統備份" --target host

# 對話摘要
openclaw cron add --name "對話摘要" --cron "0 * * * *" --message "每小時對話摘要" --agent "cynthia" --target main
```

---

### 3. 恢復 Skills

```bash
# 恢復 Skills
cp -r ~/.openclaw/backup/$DATE/skills ~/.openclaw/workspace/
```

---

### 4. 恢復 Memory

```bash
# 恢復 Memory
cp -r ~/.openclaw/backup/$DATE/memory ~/.openclaw/workspace/
```

---

### 5. 恢復 Agents

```bash
# 恢復 Agents
cp -r ~/.openclaw/backup/$DATE/agents ~/.openclaw/
```

---

## 緊急恢復（最基本）

如果淨係想快啲撈番系統：

```bash
# 1. 恢復最新既配置
cp ~/.openclaw/backup/$(ls ~/.openclaw/backup | tail -1)/openclaw.json ~/.openclaw/

# 2. 恢復 Skills
cp -r ~/.openclaw/backup/$(ls ~/.openclaw/backup | tail -1)/skills ~/.openclaw/workspace/

# 3. 重新啟動 OpenClaw
openclaw gateway restart
```

---

## 驗證

```bash
# 檢查狀態
openclaw status

# 檢查 Crons
openclaw cron list | wc -l

# 檢查向量
openclaw memory status

# 檢查Agents
openclaw agents list | wc -l
```

---

## 重要配置

### 必須重建既 Cron Jobs

| Cron | 頻率 | 功能 |
|------|------|------|
| 系統健康 | */15 * * * | 每15分鐘健康檢查 |
| auto-fix-hook | 0 * * * | 每小時自動修復 |
| 系統備份 | 0 3 * * * | 每日03:00備份 |
| 對話摘要 | 0 * * * | 每小時對話摘要 |

---

## 恢復後檢查清單

- [ ] openclaw status 正常
- [ ] Agents 數量正確
- [ ] Crons 運行中
- [ ] Memory 向量正常
- [ ] Skills 可用

---

*建立：2026-03-01*
