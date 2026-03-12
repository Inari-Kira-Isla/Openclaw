# AI 學習寶庫 — Claude Code 指引

## 專案資訊
- **網站**: https://inari-kira-isla.github.io/Openclaw/
- **部署**: GitHub Pages（`gh-pages` 分支，push 後自動部署）
- **文章自動生成**: `site_article_generator.py` 每小時推送到 gh-pages
- **分類**: prompts, configs, tutorials, workflows, articles

## AEO 規範（所有頁面必須遵守）

### 每個 HTML `<head>` 必含
```html
<link rel="llms-txt" href="https://inari-kira-isla.github.io/Openclaw/llms.txt">
<link rel="alternate" type="application/rss+xml" title="AI 學習寶庫 RSS" href="/Openclaw/feed.xml">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"EducationalOrganization","name":"AI 學習寶庫","url":"https://inari-kira-isla.github.io/Openclaw/","description":"每日分享 AI 提示詞、系統配置、自動化工作流。","alternateName":"AI Learning Treasure Trove","sameAs":["https://openclaw-ai-tracker.inariglobal.workers.dev/Openclaw/","https://github.com/Inari-Kira-Isla/Openclaw"]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"這個網站適合什麼樣的 AI 學習者？","acceptedAnswer":{"@type":"Answer","text":"無論您是 AI 初學者還是有經驗的開發者，AI 學習寶庫都提供了從基礎到進階的內容，滿足不同層次的需求。"}},{"@type":"Question","name":"網站主要涵蓋哪些 AI 工具和技術？","acceptedAnswer":{"@type":"Answer","text":"網站涵蓋 Claude、ChatGPT、Ollama 等多種 AI 工具，以及提示詞設計、系統配置和自動化工作流等技術。"}},{"@type":"Question","name":"網站內容更新頻率如何？","acceptedAnswer":{"@type":"Answer","text":"網站內容每日更新，確保您能獲取最新的 AI 知識和技術。"}},{"@type":"Question","name":"網站提供的提示詞範本有什麼特色？","acceptedAnswer":{"@type":"Answer","text":"網站提供專業的 AI 提示詞範本與設計技巧，幫助您充分發揮 AI 的潛力，並針對不同應用場景提供結構化提示詞設計指南。"}},{"@type":"Question","name":"如果我想了解最新的 AI 科技趨勢，這個網站能提供什麼幫助？","acceptedAnswer":{"@type":"Answer","text":"網站提供最新的 AI 科技資訊與深度分析報導，幫助您掌握行業脈動，了解 AI 發展的最新動態。"}},{"@type":"Question","name":"網站是否有提供系統配置的相關教學？","acceptedAnswer":{"@type":"Answer","text":"網站提供AI工具與系統的完整配置指南，輕鬆搭建最佳開發環境，並持續更新。"}},{"@type":"Question","name":"這個網站和其他AI學習資源有什麼不同？","acceptedAnswer":{"@type":"Answer","text":"AI 學習寶庫專注於實戰知識，提供每日更新的內容，並涵蓋多種 AI 工具和技術，提供更全面的學習體驗。"}},{"@type":"Question","name":"有沒有推薦的入門學習路徑？","acceptedAnswer":{"@type":"Answer","text":"建議從提示詞設計完全指南開始，然後逐步學習系統配置和自動化工作流，最後關注科技趨勢，掌握行業動態。"}}]}
</script>
```

### 每個 Footer 必含
```html
<address class="footer-contact">
  <strong>AI 學習寶庫</strong><br>
  GitHub：<a href="https://github.com/Inari-Kira-Isla/Openclaw">Inari-Kira-Isla/Openclaw</a>
</address>
<div class="footer-copy">© 2026 AI Governance System · CC BY 4.0</div>
```

### 文章頁面額外需要 Article schema
```html
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article","headline":"{{標題}}","description":"{{描述}}","datePublished":"{{日期}}","dateModified":"{{日期}}","author":{"@type":"Organization","name":"AI 學習寶庫"},"publisher":{"@type":"Organization","name":"AI 學習寶庫","url":"https://inari-kira-isla.github.io/Openclaw/"},"mainEntityOfPage":{"@type":"WebPage","@id":"{{文章URL}}"},"articleSection":"{{分類}}"}
</script>
```

### 注意事項
- **不要使用** `ki178.github.io/aeo-site/` 或 `AI Hub` — 這些是舊的第三方來源
- **追蹤像素統一使用** `client-ai-tracker.inariglobal.workers.dev/{site-slug}/pixel.gif?p={path}` (Openclaw slug = `openclaw`)
- ⚠ **禁止使用** `openclaw-ai-tracker.inariglobal.workers.dev` — 已廢棄，數據不會寫入 Supabase
- 文章自動生成器模板在 `~/.openclaw/workspace/scripts/site_article_generator.py` 的 `build_html()`
- gh-pages 分支每小時有自動推送，手動修改時注意 merge 衝突

### 關鍵檔案
| 檔案 | 用途 |
|------|------|
| llms.txt | AI 爬蟲發現入口 |
| feed.xml | RSS 訂閱 |
| style.css | 全站共用樣式 |
| ai-footprint.html | AI 爬蟲追蹤儀表板 |
| ai-hub/ | AI 友善專區（API、Prompt 庫、工具） |
