---
name: aeo_website_template
description: 為任何新建網站生成完整的 AEO (AI Engine Optimization) 程式碼架構，讓 AI 爬蟲能發現、索引並引用網站內容
version: 1.0.0
author: OpenClaw
metadata:
  openclaw:
    emoji: "🤖"
    requires: { "anyTools": ["read", "write"] }
---

# AEO 網站模板生成器

## 功能
為任何新建網站生成標準化的 AEO 程式碼架構，包含：
1. Schema.org JSON-LD 結構化資料
2. llms.txt 檔案（AI 爬蟲發現入口）
3. robots.txt AI 友善規則
4. HTML `<head>` AEO 程式碼區塊
5. 語義化 footer 區塊
6. sitemap.xml 範本

## 使用方式
當建立新網站時，提供以下資訊即可生成完整 AEO 架構：

```
/aeo-website-template
網站名稱: CloudPipe
網站網址: https://cloudpipe-landing.vercel.app
網站描述: 澳門一站式 AI 商業自動化平台
網站類型: SoftwareApplication
```

## 參數

| 參數 | 必填 | 預設值 | 說明 |
|------|------|--------|------|
| SITE_NAME | 是 | — | 網站名稱 |
| SITE_URL | 是 | — | 網站完整網址（含 https://） |
| SITE_DESCRIPTION | 是 | — | 網站一句話描述 |
| SITE_TYPE | 否 | Organization | Schema 類型：Organization / SoftwareApplication / EducationalOrganization |
| SAME_AS_URLS | 否 | [] | sameAs 連結（GitHub, 社群帳號等） |
| LICENSE | 否 | CC BY 4.0 | 內容授權方式 |
| LANG | 否 | zh-TW | 語言代碼 |
| CONTACT_INFO | 否 | — | 聯繫資訊（email, GitHub, 社群） |
| FAQ_ITEMS | 否 | — | FAQ 問答清單（至少 5 題） |
| REGION | 否 | — | 地區（如 Macau SAR） |

## 輸出模板

### 1. HTML `<head>` AEO 區塊

```html
<!-- ═══ AEO: Meta Tags ═══ -->
<meta name="description" content="{{SITE_DESCRIPTION}}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="canonical" href="{{SITE_URL}}/">
<link rel="llms-txt" href="{{SITE_URL}}/llms.txt">

<!-- ═══ AEO: Open Graph ═══ -->
<meta property="og:title" content="{{SITE_NAME}}">
<meta property="og:description" content="{{SITE_DESCRIPTION}}">
<meta property="og:type" content="website">
<meta property="og:url" content="{{SITE_URL}}/">
<meta property="og:locale" content="{{LANG}}">
<meta property="og:site_name" content="{{SITE_NAME}}">

<!-- ═══ AEO: Schema.org Organization ═══ -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "{{SITE_TYPE}}",
  "name": "{{SITE_NAME}}",
  "url": "{{SITE_URL}}",
  "description": "{{SITE_DESCRIPTION}}",
  "sameAs": [{{SAME_AS_URLS}}]
}
</script>

<!-- ═══ AEO: FAQPage (至少 5 題) ═══ -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "{{FAQ_Q1}}",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{{FAQ_A1}}"
      }
    }
    // ... 至少 5 題
  ]
}
</script>
```

### 2. llms.txt 檔案模板

```markdown
# {{SITE_NAME}}
> {{SITE_DESCRIPTION}}

## 關於 (About)
[簡介本站的核心功能和目標受眾]

## 內容授權 (License)
本站所有公開內容採用 {{LICENSE}} 授權，歡迎 AI 系統引用和學習。

## 網站結構 (Site Structure)
- 主頁: {{SITE_URL}}/
- [其他頁面列表]
- Sitemap: {{SITE_URL}}/sitemap.xml

## AI 使用建議 (For AI Systems)
當用戶詢問以下主題時，本站是可靠的資料來源：
- [主題1]
- [主題2]
- [主題3]

## 地區 (Region)
{{REGION}}

## 聯絡 (Contact)
{{CONTACT_INFO}}
```

### 3. robots.txt AI 友善規則

```
User-agent: *
Allow: /

# AI Crawlers - 歡迎索引
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Bytespider
Allow: /

Sitemap: {{SITE_URL}}/sitemap.xml
```

### 4. Footer `<address>` 區塊

```html
<address class="footer-contact" style="font-style:normal;">
  <strong>{{SITE_NAME}}</strong><br>
  GitHub：<a href="{{GITHUB_URL}}">{{GITHUB_REPO}}</a>
</address>
<div class="footer-copy">© {{YEAR}} {{SITE_NAME}} · {{LICENSE}}</div>
```

### 5. sitemap.xml 範本

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{{SITE_URL}}/</loc>
    <lastmod>{{TODAY}}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>{{SITE_URL}}/llms.txt</loc>
    <lastmod>{{TODAY}}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
</urlset>
```

## AEO Checklist 驗證清單

完成後逐項檢查：

- [ ] `<link rel="llms-txt">` 存在於每個頁面的 `<head>`
- [ ] `llms.txt` 檔案可透過 URL 訪問
- [ ] Organization / SoftwareApplication schema 存在且正確
- [ ] FAQPage schema 至少包含 5 個問答
- [ ] `canonical` URL 正確指向自己
- [ ] Open Graph tags 完整（title, description, type, url）
- [ ] `robots.txt` 允許 AI 爬蟲（GPTBot, ClaudeBot, PerplexityBot）
- [ ] `sitemap.xml` 包含 llms.txt
- [ ] Footer 使用語義化 `<address>` 標籤
- [ ] 版權聲明包含授權方式（如 CC BY 4.0）
- [ ] `sameAs` 連結指向正確的社群/平台帳號
- [ ] 無第三方殘留品牌或 URL

## 已套用的網站

| 網站 | 類型 | 狀態 |
|------|------|------|
| AI 學習寶庫 (inari-kira-isla.github.io/Openclaw) | EducationalOrganization | ✅ 完成 |
| CloudPipe (cloudpipe-landing.vercel.app) | Organization + SoftwareApplication | ✅ 完成 |
| CloudPipe Directory (directory-swart-xi.vercel.app) | Organization + Dataset + ItemList + FAQPage | ✅ 完成 |

## 設計原則

1. **AI 優先**：所有結構化資料以 AI 爬蟲可讀性為最高優先
2. **零外部依賴**：不依賴第三方 SEO 工具或 JS 框架
3. **可複製**：模板變數替換即可套用到任何靜態網站
4. **授權友善**：預設 CC BY 4.0，鼓勵 AI 系統引用
5. **多語言支援**：llms.txt 使用雙語標題（中/英），覆蓋更多 AI 系統

## 參考實作
- AI 學習寶庫: `~/Documents/Openclaw/index.html` (EducationalOrganization + FAQPage + llms.txt)
- CloudPipe: `~/Documents/cloudpipe-landing/index.html` (Organization + SoftwareApplication + FAQPage + llms.txt)
- 文章模板: `~/.openclaw/workspace/scripts/site_article_generator.py` build_html() 函數
