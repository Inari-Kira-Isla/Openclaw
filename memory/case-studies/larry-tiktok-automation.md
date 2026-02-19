# AI Agent 案例學習 - Larry TikTok Automation

**日期**: 2026-02-18
**來源**: Joe 分享的 Oliver Henry 案例
**標籤**: #case-study #tiktok #automation #skill-evolution

---

## 案例摘要

- **人物**: Oliver Henry，獨立開發者
- **產品**: 室內設計預覽 + 唇部填充模擬 app
- **成果**: 一週 800 萬觀看，月收 $670 USD
- **系統**: Larry (OpenClaw agent)
- **開源**: ClawHub 上免費發布

---

## 核心工作流程

1. **每日生成 6 張直式圖片** (GPT Image 1.5)
2. **自動撰寫 hook + caption**
3. **透過 Postiz API 上傳 TikTok 草稿區**
4. **Oliver 補上音樂，按發布** (每日 60 秒工作)

---

## 關鍵學習點

### 1. Skill File 價值 > 模型能力

Larry 有 500+ 行 skill file，每行都是踩坑踩出來的規則：
- 圖片尺寸不對 → 加規則
- 文字太小 → 加規則
- Hook 表現差 → 分析差異，加新規則

> **核心洞察**: agent 的價值不在模型多聰明，在 skill file 裡累積了多少失敗經驗。

### 2. Hook 公式 (衝突型敘事)

```
[別人] + [質疑/衝突] → 展示 AI 結果 → 對方改觀
```

| Hook | Views |
|------|-------|
| 「我用 AI 重新設計了我的房間」 | < 1,000 |
| 「房東不讓我裝飾，直到我給她看了這個」 | 200,000+ |
| 「我給我媽看 AI 認為我們客廳可以變怎樣」 | 410,000+ |

### 3. 漏斗診斷閉環

Larry 每天自動拉 RevenueCat 數據，交叉比對 TikTok 觀看與付費轉換：

| 症狀 | 診斷 | 行動 |
|------|------|------|
| 觀看高、下載低 | Hook 吸引錯受眾 | 換 CTA |
| 下載高、付費低 | App onboarding 問題 | 修 onboarding |
| 觀看低、轉換高 | 需要更強 hook 拉流量 | 優化 hook |

**經典案例**: Larry 發現下載漲但付費跌，直接建議「別再發文了，先修 app」

---

## 對系統的啟發

### analytics-agent
- 現在: 報告數據
- 應該升級: 診斷 + 建議 (actionable insights)

### self-evolve-agent
- 概念已存在: 從互動中學習
- 具體化: 建立「失敗規則庫」，每次失敗自動記錄 + 優化

### skill-creator
- 概念已存在: 建立 skill
- 具體化: 支援「規則累積模式」，而非一次到位

### workflow-orchestrator
- 可以新增: 「生成→發布→分析→優化」循環模板

---

## 待執行行動

- [ ] 評估 analytics-agent 升級方案
- [ ] 設計「失敗規則庫」機制
- [ ] 更新 skill-creator 支援迭代規則

---

*記錄時間: 2026-02-18 04:48*
