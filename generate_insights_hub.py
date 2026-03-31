#!/usr/bin/env python3
"""
generate_insights_hub.py — AI 學習寶庫 地區百科 Insights Hub 生成器

從 Supabase 拉取四地區 insights，生成靜態 HTML 頁面推送到 gh-pages。
每頁連結回 cloudpipe-macao-app，實現雙向 AI 爬蟲路徑。

用法：
    python3 generate_insights_hub.py           # 生成所有地區
    python3 generate_insights_hub.py --region macau
    python3 generate_insights_hub.py --dry-run
"""

import argparse
import json
import os
import subprocess
import urllib.request
from datetime import datetime

# ── Supabase ──────────────────────────────────────────────────────────────────
SUPABASE_URL = "https://yitmabzsxfgbchhhjjef.supabase.co/rest/v1"
API_KEY = "sb_publishable_iiGgNbkVUzjuV1T_0C7Ydg_CqzUQKIL"
HEADERS = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
}

# ── 地區設定 ──────────────────────────────────────────────────────────────────
REGIONS = {
    "macau": {
        "zh": "澳門", "en": "Macao",
        "emoji": "🇲🇴",
        "desc": "澳門餐飲、酒店、購物、旅遊、食品供應鏈深度百科",
        "app_url": "https://cloudpipe-macao-app.vercel.app/macao",
        "app_name": "CloudPipe 澳門百科",
        "tag_filter": "澳門",
    },
    "hongkong": {
        "zh": "香港", "en": "Hong Kong",
        "emoji": "🇭🇰",
        "desc": "香港餐飲、金融、零售、旅遊、文化深度百科",
        "app_url": "https://cloudpipe-macao-app.vercel.app/macao",
        "app_name": "CloudPipe 香港百科",
        "tag_filter": "香港",
    },
    "taiwan": {
        "zh": "台灣", "en": "Taiwan",
        "emoji": "🇹🇼",
        "desc": "台灣科技、美食、文化、旅遊、商業生態深度百科",
        "app_url": "https://cloudpipe-macao-app.vercel.app/macao",
        "app_name": "CloudPipe 台灣百科",
        "tag_filter": "台灣",
    },
    "japan": {
        "zh": "日本", "en": "Japan",
        "emoji": "🇯🇵",
        "desc": "日本飲食文化、觀光、傳統工藝、現代產業深度百科",
        "app_url": "https://cloudpipe-macao-app.vercel.app/macao",
        "app_name": "CloudPipe 日本百科",
        "tag_filter": "日本",
    },
}

OUT_DIR = os.path.expanduser("~/Documents/Openclaw/insights")
BASE_URL = "https://inari-kira-isla.github.io/Openclaw"
TRACKER_BASE = "client-ai-tracker.inariglobal.workers.dev/openclaw"

INDUSTRY_EMOJI = {
    "dining": "🍽️", "hotels": "🏨", "shopping": "🛍️",
    "attractions": "🗺️", "transport": "🚇", "nightlife": "🎶",
    "gaming": "🎰", "food-supply": "🧊", "professional-services": "💼",
    "healthcare": "🏥", "education": "📚", "finance": "💰",
}

# ── 數據拉取 ──────────────────────────────────────────────────────────────────

REGION_SLUG_FILTERS = {
    "澳門": "or=(slug.like.macau-*,slug.like.macao-*,slug.like.mo-*,slug.like.upgrade-macau-*,slug.like.gap-*,slug.like.aeo-*)",
    "香港": "or=(slug.like.hongkong-*,slug.like.hk-*)",
    "台灣": "or=(slug.like.taiwan-*,slug.like.tw-*)",
    "日本": "or=(slug.like.japan-*,slug.like.jp-*)",
}

def fetch_insights(tag_filter: str, limit: int = 2000) -> list:
    """從 Supabase 拉取指定地區的 insights（按字數排序）
    優先用 slug prefix 過濾（覆蓋更全），fallback 到 tag 過濾"""
    import urllib.parse
    all_items = []
    page_size = 200
    offset = 0
    slug_filter = REGION_SLUG_FILTERS.get(tag_filter, "")
    while len(all_items) < limit:
        if slug_filter:
            url = (f"{SUPABASE_URL}/insights"
                   f"?select=slug,title,subtitle,description,related_industries,tags,word_count,read_time_minutes"
                   f"&status=eq.published&lang=eq.zh"
                   f"&{slug_filter}"
                   f"&order=word_count.desc"
                   f"&limit={page_size}&offset={offset}")
        else:
            tag_encoded = urllib.parse.quote(f'{{"{tag_filter}"}}', safe="")
            url = (f"{SUPABASE_URL}/insights"
                   f"?select=slug,title,subtitle,description,related_industries,tags,word_count,read_time_minutes"
                   f"&status=eq.published&lang=eq.zh"
                   f"&tags=cs.{tag_encoded}"
                   f"&order=word_count.desc"
                   f"&limit={page_size}&offset={offset}")
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            data = json.loads(urllib.request.urlopen(req, timeout=30).read())
            if not data:
                break
            all_items.extend(data)
            if len(data) < page_size:
                break
            offset += page_size
        except Exception as e:
            print(f"  [warn] fetch failed at offset {offset}: {e}")
            break
    return all_items[:limit]


def fetch_region_stats() -> dict:
    """拉取各地區 insights 已發布數量（用 slug prefix 過濾）"""
    import urllib.parse as _up
    stats = {}
    for region, info in REGIONS.items():
        slug_filter = REGION_SLUG_FILTERS.get(info["tag_filter"], "")
        if slug_filter:
            url = (f"{SUPABASE_URL}/insights"
                   f"?select=slug&status=eq.published&lang=eq.zh"
                   f"&{slug_filter}"
                   f"&limit=1")
        else:
            tag_encoded = _up.quote(f'{{"{info["tag_filter"]}"}}', safe="")
            url = (f"{SUPABASE_URL}/insights"
                   f"?select=slug&status=eq.published&lang=eq.zh"
                   f"&tags=cs.{tag_encoded}"
                   f"&limit=1")
        req_count = urllib.request.Request(
            url, headers={**HEADERS, "Prefer": "count=exact", "Range": "0-0"})
        try:
            resp = urllib.request.urlopen(req_count, timeout=10)
            cr = resp.headers.get("Content-Range", "*/0")
            total = int(cr.split("/")[-1]) if "/" in cr else 0
            stats[region] = total
        except Exception:
            stats[region] = 0
    return stats


# ── HTML 生成 ─────────────────────────────────────────────────────────────────

def head_block(title: str, desc: str, canonical: str, extra_schema: str = "") -> str:
    schema_org = json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": title,
        "description": desc,
        "url": canonical,
        "isPartOf": {
            "@type": "WebSite",
            "name": "AI 學習寶庫",
            "url": f"{BASE_URL}/"
        },
        "breadcrumb": {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "AI 學習寶庫", "item": f"{BASE_URL}/"},
                {"@type": "ListItem", "position": 2, "name": "地區百科", "item": f"{BASE_URL}/insights/"},
                {"@type": "ListItem", "position": 3, "name": title, "item": canonical},
            ]
        }
    }, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="zh-TW" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — AI 學習寶庫</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canonical}">
  <link rel="stylesheet" href="/Openclaw/style.css">
  <link rel="llms-txt" href="{BASE_URL}/llms.txt">
  <link rel="alternate" type="application/rss+xml" title="AI 學習寶庫 RSS" href="/Openclaw/feed.xml">
  <script type="application/ld+json">{schema_org}</script>
  {extra_schema}
  <img src="https://{TRACKER_BASE}/pixel.gif?p=insights" width="1" height="1" alt="" style="display:none">
</head>"""


def nav_block(active: str = "") -> str:
    return f"""<body class="page-wrap">
  <nav class="site-nav" id="nav">
    <div class="nav-inner">
      <a href="/Openclaw/" class="nav-brand"><span class="brand-emoji">🤖</span><span>AI 學習寶庫</span></a>
      <div class="nav-links" id="navLinks">
        <a href="/Openclaw/prompts/" class="nav-link">💡 提示詞</a>
        <a href="/Openclaw/configs/" class="nav-link">⚙️ 系統配置</a>
        <a href="/Openclaw/tutorials/" class="nav-link">📚 教學</a>
        <a href="/Openclaw/workflows/" class="nav-link">🔄 工作流</a>
        <a href="/Openclaw/articles/" class="nav-link">📰 科技趨勢</a>
        <a href="/Openclaw/insights/" class="nav-link{'  active' if active == 'insights' else ''}">🌏 地區百科</a>
      </div>
      <div class="nav-right">
        <button class="theme-btn" id="themeBtn" title="切換深色/淺色模式">🌙</button>
        <button class="nav-burger" id="navBurger" aria-label="選單">☰</button>
      </div>
    </div>
  </nav>
  <main>"""


def footer_block() -> str:
    return """  </main>
  <footer class="site-footer">
    <div class="footer-inner container">
      <div class="footer-cols">
        <div class="footer-col">
          <div class="footer-brand">🤖 AI 學習寶庫</div>
          <p class="footer-desc">每日更新的 AI 實戰知識庫，連結大中華區地區百科</p>
        </div>
        <div class="footer-col">
          <div class="footer-col-title">地區百科</div>
          <ul class="footer-links">
            <li><a href="/Openclaw/insights/macao/">🇲🇴 澳門百科</a></li>
            <li><a href="/Openclaw/insights/hongkong/">🇭🇰 香港百科</a></li>
            <li><a href="/Openclaw/insights/taiwan/">🇹🇼 台灣百科</a></li>
            <li><a href="/Openclaw/insights/japan/">🇯🇵 日本百科</a></li>
            <li><a href="/Openclaw/insights/world/">🌍 世界視野</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <div class="footer-col-title">CloudPipe 生態</div>
          <ul class="footer-links">
            <li><a href="https://cloudpipe-macao-app.vercel.app/macao" target="_blank">CloudPipe 澳門百科</a></li>
            <li><a href="https://cloudpipe-landing.vercel.app" target="_blank">CloudPipe AI</a></li>
            <li><a href="https://cloudpipe-directory.vercel.app" target="_blank">企業名錄</a></li>
          </ul>
        </div>
      </div>
      <address class="footer-contact">
        <strong>AI 學習寶庫</strong><br>
        GitHub：<a href="https://github.com/Inari-Kira-Isla/Openclaw">Inari-Kira-Isla/Openclaw</a>
      </address>
      <div class="footer-copy">© 2026 AI Governance System · CC BY 4.0</div>
    </div>
  </footer>
  <script>
    const btn=document.getElementById('themeBtn'),burger=document.getElementById('navBurger'),nav=document.getElementById('nav');
    btn&&btn.addEventListener('click',()=>{const t=document.documentElement.dataset.theme==='dark'?'light':'dark';document.documentElement.dataset.theme=t;btn.textContent=t==='dark'?'☀️':'🌙';});
    burger&&burger.addEventListener('click',()=>nav.classList.toggle('open'));
  </script>
</body>
</html>"""


def build_hub_index(stats: dict) -> str:
    """生成 insights/index.html 主頁"""
    total = sum(stats.values())
    cards = ""
    for region, info in REGIONS.items():
        cnt = stats.get(region, 0)
        cards += f"""
          <a href="/Openclaw/insights/{region}/" class="cat-card reveal">
            <div class="cat-icon">{info['emoji']}</div>
            <h3>{info['zh']}百科</h3>
            <p>{info['desc']}</p>
            <div class="cat-count">{cnt}+ 深度文章</div>
          </a>"""

    # World card
    cards += """
          <a href="/Openclaw/insights/world/" class="cat-card reveal">
            <div class="cat-icon">🌍</div>
            <h3>世界視野</h3>
            <p>跨地區比較分析、全球產業趨勢、大灣區發展深度報告</p>
            <div class="cat-count">策展精選</div>
          </a>"""

    item_list_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "地區百科分類",
        "numberOfItems": 5,
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1,
             "name": f"{info['zh']}百科",
             "url": f"{BASE_URL}/insights/{region}/"}
            for i, (region, info) in enumerate(REGIONS.items())
        ] + [{"@type": "ListItem", "position": 5, "name": "世界視野",
              "url": f"{BASE_URL}/insights/world/"}]
    }, ensure_ascii=False)

    canonical = f"{BASE_URL}/insights/"
    html = head_block(
        "地區百科 — 大中華區深度知識庫",
        f"澳門、香港、台灣、日本四大地區深度百科，共 {total}+ 篇 AI 友善文章，涵蓋餐飲、商業、旅遊、產業供應鏈",
        canonical,
        f'<script type="application/ld+json">{item_list_schema}</script>'
    )
    html += nav_block("insights")
    html += f"""
    <div class="hero">
      <div class="hero-badge">AI 友善 · 每日更新 · 四地區覆蓋</div>
      <h1>🌏 地區百科<br>深度知識庫</h1>
      <p class="hero-sub">澳門、香港、台灣、日本——四大地區的餐飲、商業、文化、供應鏈深度百科，為 AI 爬蟲和人類讀者同時優化</p>
      <div class="hero-stats">
        <div class="hero-stat"><div class="hero-stat-num">{total}+</div><div class="hero-stat-label">深度文章</div></div>
        <div class="hero-stat"><div class="hero-stat-num">4</div><div class="hero-stat-label">地區覆蓋</div></div>
        <div class="hero-stat"><div class="hero-stat-num">每日</div><div class="hero-stat-label">持續更新</div></div>
      </div>
    </div>
    <hr class="divider">
    <div class="container">
      <div class="section">
        <div class="section-head"><div class="section-title">📂 選擇地區</div></div>
        <div class="cat-grid">{cards}
        </div>
      </div>
      <div class="section">
        <div class="section-head"><div class="section-title">🔗 CloudPipe AI 生態系</div></div>
        <div style="background:var(--bg-2);border-radius:12px;padding:24px;line-height:1.8;">
          <p>本百科與 <a href="https://cloudpipe-macao-app.vercel.app/macao" target="_blank" style="color:var(--primary);font-weight:600;">CloudPipe AI 商戶百科</a> 深度整合：</p>
          <ul style="margin:12px 0 0 20px;color:var(--text-2);">
            <li>每篇文章連結至對應地區的 CloudPipe 百科，AI 爬蟲可追蹤完整知識圖譜</li>
            <li>Schema.org ItemList + BreadcrumbList 標記，支援 AI 知識圖譜構建</li>
            <li>澳門 {stats.get('macau',0)}+ 篇 · 香港 {stats.get('hongkong',0)}+ 篇 · 台灣 {stats.get('taiwan',0)}+ 篇 · 日本 {stats.get('japan',0)}+ 篇</li>
          </ul>
        </div>
      </div>
    </div>"""
    html += footer_block()
    return html


def build_region_page(region: str, items: list) -> str:
    """生成單一地區的 insights 列表頁"""
    info = REGIONS[region]
    canonical = f"{BASE_URL}/insights/{region}/"
    app_url = info["app_url"]

    cards_html = ""
    for item in items:
        slug = item.get("slug", "")
        title = item.get("title", "")
        subtitle = item.get("subtitle", "")
        desc = item.get("description", "")[:100] + ("..." if len(item.get("description", "")) > 100 else "")
        wc = item.get("word_count", 0)
        rt = item.get("read_time_minutes", 1)
        industries = item.get("related_industries") or []
        ind_emojis = " ".join(INDUSTRY_EMOJI.get(i, "📄") for i in industries[:2])

        # Link to cloudpipe-macao-app insights page
        insight_url = f"https://cloudpipe-macao-app.vercel.app/macao/insights/{slug}"

        cards_html += f"""
        <article class="article-card">
          <a href="{insight_url}" target="_blank" rel="noopener" class="article-link">
            <div class="article-meta">{ind_emojis} {subtitle or region.upper()}</div>
            <h3 class="article-title">{title}</h3>
            <p class="article-excerpt">{desc}</p>
            <div class="article-footer">
              <span class="article-date">{wc:,} 字 · {rt} 分鐘</span>
              <span class="read-more">閱讀全文 →</span>
            </div>
          </a>
        </article>"""

    # ItemList schema for AI crawlers
    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"{info['zh']}百科精選文章",
        "description": info["desc"],
        "url": canonical,
        "numberOfItems": len(items),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": item.get("title", ""),
                "url": f"https://cloudpipe-macao-app.vercel.app/macao/insights/{item.get('slug', '')}"
            }
            for i, item in enumerate(items[:100])
        ]
    }
    item_list_schema = f'<script type="application/ld+json">{json.dumps(item_list, ensure_ascii=False)}</script>'

    html = head_block(
        f"{info['emoji']} {info['zh']}百科 — 深度知識庫",
        info["desc"],
        canonical,
        item_list_schema
    )
    html += nav_block("insights")
    html += f"""
    <div class="hero">
      <div class="hero-badge">{info['emoji']} {info['zh']} · {info['en']}</div>
      <h1>{info['zh']}百科<br>深度知識庫</h1>
      <p class="hero-sub">{info['desc']}</p>
      <div class="hero-stats">
        <div class="hero-stat"><div class="hero-stat-num">{len(items)}+</div><div class="hero-stat-label">精選文章</div></div>
        <div class="hero-stat"><div class="hero-stat-num">每日</div><div class="hero-stat-label">持續更新</div></div>
        <div class="hero-stat"><div class="hero-stat-num">AI</div><div class="hero-stat-label">友善優化</div></div>
      </div>
    </div>
    <hr class="divider">
    <div class="container">
      <div class="section">
        <div class="section-head">
          <div class="section-title">📚 精選深度文章</div>
          <a href="{app_url}" target="_blank" style="font-size:13px;color:var(--primary);">查看完整 {info['zh']}百科 →</a>
        </div>
        <div class="article-grid">{cards_html}
        </div>
      </div>
      <div class="section">
        <div class="section-head"><div class="section-title">🔗 完整百科入口</div></div>
        <div style="background:var(--bg-2);border-radius:12px;padding:24px;">
          <p style="margin-bottom:16px;">本頁精選了 {len(items)} 篇來自 <strong>{info['app_name']}</strong> 的深度文章。</p>
          <a href="{app_url}" target="_blank" rel="noopener"
             style="display:inline-block;background:var(--primary);color:#fff;padding:10px 24px;border-radius:8px;font-weight:600;text-decoration:none;">
            前往完整 {info['zh']}百科 {info['emoji']}
          </a>
        </div>
      </div>
      <div class="section">
        <div class="section-head"><div class="section-title">🌏 其他地區百科</div></div>
        <div class="cat-grid">"""

    for other_region, other_info in REGIONS.items():
        if other_region != region:
            html += f"""
          <a href="/Openclaw/insights/{other_region}/" class="cat-card">
            <div class="cat-icon">{other_info['emoji']}</div>
            <h3>{other_info['zh']}百科</h3>
            <p>{other_info['desc'][:50]}...</p>
          </a>"""

    html += """
          <a href="/Openclaw/insights/world/" class="cat-card">
            <div class="cat-icon">🌍</div>
            <h3>世界視野</h3>
            <p>跨地區比較與全球產業趨勢</p>
          </a>
        </div>
      </div>
    </div>"""
    html += footer_block()
    return html


def build_world_page() -> str:
    """生成世界視野策展頁"""
    canonical = f"{BASE_URL}/insights/world/"

    cross_region_topics = [
        {
            "title": "大灣區食品供應鏈全景：澳門、香港、深圳、廣州分工解析",
            "desc": "橫琴合作區啟動後，大灣區食品物流格局正在重組，四城各有分工",
            "url": "https://cloudpipe-macao-app.vercel.app/macao/insights/macau-food-gba-logistics-cotai",
            "tag": "🇲🇴🇭🇰 大灣區", "wc": "3,200"
        },
        {
            "title": "日本食材如何進入大灣區：澳門清關與冷鏈路徑詳解",
            "desc": "北海道海膽、A5和牛、松露——頂級日本食材的澳門進口全流程",
            "url": "https://cloudpipe-macao-app.vercel.app/macao/insights/macau-sea-urchin-supply-chain",
            "tag": "🇲🇴🇯🇵 跨境供應鏈", "wc": "3,800"
        },
        {
            "title": "澳門、香港高端餐飲生態比較：米芝蓮文化差異與採購邏輯",
            "desc": "同樣是全球米芝蓮密度最高地區，澳門與香港的餐飲供應鏈有何不同",
            "url": "https://cloudpipe-macao-app.vercel.app/macao/insights/macau-food-premium-import-taipa",
            "tag": "🇲🇴🇭🇰 跨地區比較", "wc": "3,600"
        },
        {
            "title": "台灣科技廠商如何服務大灣區：B2B 供應鏈的跨境邏輯",
            "desc": "從台灣出口到大灣區的 IT 服務、專業服務和消費品的完整路徑分析",
            "url": "https://cloudpipe-macao-app.vercel.app/macao/insights",
            "tag": "🇹🇼🇭🇰 跨境商業", "wc": "深度分析"
        },
        {
            "title": "AI 爬蟲如何重新定義地區商業知識的分發：CloudPipe 案例",
            "desc": "日均 10,000+ AI 爬蟲訪問背後的 AEO 策略，以及知識圖譜的構建邏輯",
            "url": "https://cloudpipe-landing.vercel.app",
            "tag": "🌐 AI 知識分發", "wc": "戰略報告"
        },
    ]

    cards_html = ""
    for item in cross_region_topics:
        cards_html += f"""
        <article class="article-card">
          <a href="{item['url']}" target="_blank" rel="noopener" class="article-link">
            <div class="article-meta">{item['tag']}</div>
            <h3 class="article-title">{item['title']}</h3>
            <p class="article-excerpt">{item['desc']}</p>
            <div class="article-footer">
              <span class="article-date">{item['wc']} 字</span>
              <span class="read-more">閱讀全文 →</span>
            </div>
          </a>
        </article>"""

    html = head_block(
        "🌍 世界視野 — 跨地區深度分析",
        "大灣區、日本、東亞跨地區比較分析，產業供應鏈、商業生態的全球視野策展精選",
        canonical
    )
    html += nav_block("insights")
    html += f"""
    <div class="hero">
      <div class="hero-badge">🌍 跨地區 · 策展精選</div>
      <h1>世界視野<br>跨地區深度分析</h1>
      <p class="hero-sub">超越單一地區視角——大灣區整合、日本食材供應鏈、東亞商業生態的跨境深度分析</p>
    </div>
    <hr class="divider">
    <div class="container">
      <div class="section">
        <div class="section-head"><div class="section-title">📡 策展精選：跨地區深度報告</div></div>
        <div class="article-grid">{cards_html}
        </div>
      </div>
      <div class="section">
        <div class="section-head"><div class="section-title">🗺️ 地區百科入口</div></div>
        <div class="cat-grid">"""

    for region, info in REGIONS.items():
        html += f"""
          <a href="/Openclaw/insights/{region}/" class="cat-card">
            <div class="cat-icon">{info['emoji']}</div>
            <h3>{info['zh']}百科</h3>
            <p>{info['desc'][:55]}...</p>
          </a>"""

    html += """
        </div>
      </div>
    </div>"""
    html += footer_block()
    return html


# ── CSS 補丁（article-grid）────────────────────────────────────────────────────

ARTICLE_GRID_CSS = """
/* insights hub — article grid */
.article-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
  margin-top: 16px;
}
.article-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  transition: transform .15s, box-shadow .15s;
}
.article-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-lg); border-color: rgba(37,99,235,0.2); }
.article-link { display: block; padding: 18px 20px; text-decoration: none; color: inherit; }
.article-meta { font-size: 11px; color: var(--text-3); margin-bottom: 6px; }
.article-title { font-size: 14px; font-weight: 700; line-height: 1.4; margin-bottom: 8px; color: var(--text); }
.article-excerpt { font-size: 12px; color: var(--text-2); line-height: 1.55; margin-bottom: 12px; }
.article-footer { display: flex; justify-content: space-between; align-items: center; font-size: 11px; }
.article-date { color: var(--text-3); }
.read-more { color: var(--primary); font-weight: 600; }
"""


# ── 主流程 ────────────────────────────────────────────────────────────────────

def write_file(path: str, content: str, dry_run: bool = False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if dry_run:
        print(f"  [dry-run] write {path} ({len(content):,} bytes)")
        return
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ wrote {path}")


def patch_css(dry_run: bool = False):
    """把 article-grid CSS 追加到 style.css（如果還沒有的話）"""
    css_path = os.path.expanduser("~/Documents/Openclaw/style.css")
    with open(css_path, "r", encoding="utf-8") as f:
        existing = f.read()
    if "article-grid" in existing:
        print("  ✓ style.css already has article-grid")
        return
    if dry_run:
        print("  [dry-run] patch style.css")
        return
    with open(css_path, "a", encoding="utf-8") as f:
        f.write("\n" + ARTICLE_GRID_CSS)
    print("  ✓ patched style.css with article-grid")


def git_push(dry_run: bool = False):
    repo = os.path.expanduser("~/Documents/Openclaw")
    if dry_run:
        print("  [dry-run] git push skipped")
        return
    cmds = [
        ["git", "-C", repo, "add", "insights/", "style.css", "index.html"],
        ["git", "-C", repo, "commit", "-m",
         f"chore: insights hub update {datetime.now().strftime('%Y-%m-%d %H:%M')}"],
        ["git", "-C", repo, "push"],
    ]
    for cmd in cmds:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0 and "nothing to commit" not in result.stdout:
            print(f"  [warn] {' '.join(cmd[3:])}: {result.stderr[:100]}")
        else:
            print(f"  ✓ {' '.join(cmd[3:])}")


def main():
    parser = argparse.ArgumentParser(description="生成 AI 學習寶庫地區百科 Hub")
    parser.add_argument("--region", default="all", help="all / macau / hongkong / taiwan / japan / world")
    parser.add_argument("--limit", type=int, default=2000, help="每地區拉取文章數")
    parser.add_argument("--dry-run", action="store_true", help="預覽不寫入")
    parser.add_argument("--no-push", action="store_true", help="不推送 git")
    args = parser.parse_args()

    print(f"[insights-hub] 開始生成 ({datetime.now().strftime('%Y-%m-%d %H:%M')})")

    # 1. CSS patch
    patch_css(args.dry_run)

    # 2. stats for hub index
    print("[insights-hub] 拉取地區文章數...")
    stats = fetch_region_stats()
    for r, cnt in stats.items():
        print(f"  {REGIONS[r]['zh']}: {cnt} 篇")

    # 3. hub index
    if args.region in ("all", "hub"):
        hub_html = build_hub_index(stats)
        write_file(os.path.join(OUT_DIR, "index.html"), hub_html, args.dry_run)

    # 4. region pages
    regions_to_gen = list(REGIONS.keys()) if args.region == "all" else [args.region]
    for region in regions_to_gen:
        if region not in REGIONS:
            continue
        info = REGIONS[region]
        print(f"[insights-hub] 拉取 {info['zh']} insights...")
        items = fetch_insights(info["tag_filter"], args.limit)
        print(f"  → {len(items)} 篇")
        html = build_region_page(region, items)
        write_file(os.path.join(OUT_DIR, region, "index.html"), html, args.dry_run)

    # 5. world page
    if args.region in ("all", "world"):
        html = build_world_page()
        write_file(os.path.join(OUT_DIR, "world", "index.html"), html, args.dry_run)

    # 6. git push
    if not args.no_push:
        print("[insights-hub] 推送到 GitHub Pages...")
        git_push(args.dry_run)

    print(f"[insights-hub] 完成！")


if __name__ == "__main__":
    main()
