# GitHub 架構分析報告

## 檔案數量
- 總檔案數: **7,103** 個
- 資料夾數: **606** 個

---

## 發現的問題

### 1. ⚠️ 技能重複 (Skills vs Extensions)
`skills/` 和 `extensions/` 有重複的技能名稱：

| 技能名 | 位置 |
|--------|------|
| discord | skills/, extensions/ |
| telegram | skills/, extensions/ |
| github | skills/, extensions/ |
| slack | skills/, extensions/ |
| weather | skills/, extensions/ |
| notion | skills/, extensions/ |
| line | skills/, extensions/ |
| whatsapp | skills/, extensions/ |
| memory-core | skills/, extensions/ |
| coding-agent | skills/, extensions/ |
| skill-creator | skills/, extensions/ |
| tmux | skills/, extensions/ |

**問題**: 兩個位置都有相同名稱的技能，可能造成混淆和維護困難。

### 2. 📁 主要目錄結構
```
src/
├── agents/      (725 files) - 最多
├── infra/       (336 files)
├── commands/    (332 files)
├── gateway/     (309 files)
├── cli/         (272 files)
├── auto-reply/  (267 files)
├── config/      (203 files)
├── channels/    (160 files)
├── discord/     (139 files)
├── browser/     (128 files)
```

### 3. 🔧 根目錄混乱
- **7 個 Dockerfile** (Dockerfile, Dockerfile.sandbox, 等)
- **6 個 vitest 配置** (vitest.*.config.ts)
- **多個配置文件** 散落根目錄

---

## 建議整理

1. **合併技能目錄**: 決定 `skills/` 或 `extensions/` 為主要位置
2. **移動配置檔**: 將根目錄配置文件移到 `config/` 目錄
3. **清理測試配置**: 整合 vitest 配置

---

_Generated: 2026-03-02_
