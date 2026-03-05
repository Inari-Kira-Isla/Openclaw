#!/usr/bin/env python3
"""
site_article_generator.py
每小時自動為 AI 學習寶庫生成 1 篇 AEO/SEO 優化文章並 push 到 GitHub。
"""

import os, sys, re, json, sqlite3, random, subprocess, textwrap, time
from datetime import datetime, date
import requests

# ── 設定 ──────────────────────────────────────────────────────────────────────
REPO_DIR    = os.path.expanduser("~/Documents/Openclaw")
DB_PATH     = os.path.expanduser("~/.openclaw/memory/site_articles.db")
BASE_URL    = "https://inari-kira-isla.github.io/Openclaw"
OC_GATEWAY  = "http://127.0.0.1:18789"
OC_TOKEN    = "4267bd714b23adeba00e1e99ad60c066f29006cc5e84a15e"
TG_CHAT_ID  = "8399476482"
MINIMAX_KEY = "sk-cp-1-wFmWnKLx_fRluWBNMioYVWka11Qcl1ZFF7bQxLMt-ODc6iTJ8iwU2ZWRknR8UuSQxUHSV82fqP6iyedFUCEvzEIJDHcY89B5sPhgebIvOA-po0hkxdcTg"
MINIMAX_URL = "https://api.minimax.io/anthropic/v1/messages"

# ── 分類設定 ───────────────────────────────────────────────────────────────────
CATEGORIES = {
    "prompts": {
        "name": "提示詞", "icon": "💡", "label": "提示詞",
        "dir": "prompts",
    },
    "configs": {
        "name": "系統配置", "icon": "⚙️", "label": "系統配置",
        "dir": "configs",
    },
    "tutorials": {
        "name": "教學課程", "icon": "📚", "label": "教學課程",
        "dir": "tutorials",
    },
    "workflows": {
        "name": "工作流", "icon": "🔄", "label": "工作流",
        "dir": "workflows",
    },
    "articles": {
        "name": "科技趨勢", "icon": "📰", "label": "科技趨勢",
        "dir": "articles",
    },
}

# ── 主題池 ────────────────────────────────────────────────────────────────────
TOPIC_POOL = {
    "prompts": [
        ("Claude 系統提示詞設計：打造高效 AI 助理的完整指南", "claude-system-prompt-guide", "claude 系統提示詞, system prompt 設計, AI助理配置"),
        ("ChatGPT 角色扮演提示詞：讓 AI 成為你的專業顧問", "chatgpt-role-play-prompts", "ChatGPT角色扮演, 提示詞設計, AI顧問"),
        ("Prompt 工程師必學：零樣本與少樣本提示詞技巧", "zero-shot-few-shot-prompting", "zero-shot learning, few-shot prompting, 提示詞工程"),
        ("思維鏈提示詞進階：讓 AI 一步一步解決複雜問題", "chain-of-thought-advanced", "思維鏈, chain of thought, AI推理"),
        ("多步驟工作提示詞框架：TASK-CONTEXT-OUTPUT 方法", "task-context-output-framework", "提示詞框架, AI工作流, 多步驟任務"),
        ("AI 程式碼審查提示詞集：提升程式碼品質的 10 個範本", "code-review-prompts", "程式碼審查, code review, AI提示詞"),
        ("商業文案生成提示詞：從品牌故事到廣告文字的完整套組", "business-copywriting-prompts", "商業文案, AI寫作, 品牌故事"),
        ("資料分析提示詞設計：讓 AI 成為你的數據科學家", "data-analysis-prompts", "資料分析, AI數據, 提示詞設計"),
        ("教學設計提示詞：用 AI 快速製作課程大綱與教材", "teaching-design-prompts", "教學設計, AI教育, 課程大綱"),
        ("多語言翻譯提示詞：超越 Google 翻譯的 AI 本地化技巧", "multilingual-translation-prompts", "多語言翻譯, AI本地化, 翻譯提示詞"),
        ("AI 提示詞安全設計：防止越獄與不當輸出的策略", "prompt-safety-design", "提示詞安全, AI越獄防護, jailbreak防護"),
        ("創意寫作提示詞大全：小說、劇本、詩詞的 AI 創作指南", "creative-writing-prompts", "創意寫作, AI小說, 劇本寫作"),
        ("SEO 文章寫作提示詞：讓 AI 幫你寫出排名第一的內容", "seo-article-writing-prompts", "SEO文章, AI寫作, 搜索引擎優化"),
        ("客服回覆提示詞範本：處理投訴、退款、諮詢的標準話術", "customer-service-prompts", "客服提示詞, AI客服, 客戶服務"),
        ("法律文件提示詞：合約摘要、條款解析的 AI 輔助工具", "legal-document-prompts", "法律文件, AI合約, 條款分析"),
        ("AI 面試準備提示詞：模擬面試官與最佳回答策略", "interview-preparation-prompts", "面試準備, AI面試, 求職技巧"),
        ("電商產品描述提示詞：讓商品文案自動轉化率提升 30%", "ecommerce-product-description-prompts", "電商文案, 產品描述, AI寫作轉化率"),
        ("醫療健康提示詞：症狀分析與健康建議的安全使用指南", "medical-health-prompts", "醫療AI, 健康提示詞, 症狀分析"),
        ("財務報告摘要提示詞：讓 AI 幫你讀懂年報與財報", "financial-report-prompts", "財務報告, AI金融分析, 年報摘要"),
        ("社群媒體提示詞：LinkedIn、Twitter、Instagram 爆款內容生成", "social-media-prompts", "社群媒體, AI內容, LinkedIn提示詞"),
    ],
    "configs": [
        ("Claude Desktop 完整配置指南：MCP Server 一鍵安裝教學", "claude-desktop-mcp-setup", "Claude Desktop, MCP Server, AI配置"),
        ("Cursor AI 程式碼編輯器最佳設定：提升 10 倍開發效率", "cursor-ai-editor-config", "Cursor AI, 程式碼編輯器, AI開發工具"),
        ("本地 AI 環境搭建：Ollama + Open WebUI 完整安裝指南", "ollama-open-webui-setup", "Ollama安裝, Open WebUI, 本地AI環境"),
        ("GitHub Copilot 進階設定：讓 AI 配對程式設計更高效", "github-copilot-advanced-config", "GitHub Copilot, AI程式設計, 配對開發"),
        ("LangChain 環境配置：從零開始搭建 AI Agent 開發環境", "langchain-dev-environment", "LangChain配置, AI Agent開發, Python環境"),
        ("VS Code AI 外掛完整配置：Copilot、Codeium、Tabby 比較", "vscode-ai-extensions-config", "VS Code AI, Copilot, Codeium配置"),
        ("Docker 容器化 AI 應用：最佳實踐與生產環境部署", "docker-ai-deployment", "Docker AI部署, 容器化, 生產環境"),
        ("Vercel + Cloudflare 靜態網站最佳化配置", "vercel-cloudflare-optimization", "Vercel配置, Cloudflare, 靜態網站優化"),
        ("n8n 工作流自動化：AI API 整合完整設定教學", "n8n-ai-api-integration", "n8n配置, 工作流自動化, API整合"),
        ("Notion API 配置指南：連接 AI 打造個人知識管理系統", "notion-api-ai-integration", "Notion API, AI知識管理, 個人系統"),
        ("Supabase + pgvector：向量資料庫配置與 RAG 系統搭建", "supabase-pgvector-rag", "Supabase, pgvector, RAG系統配置"),
        ("Python 虛擬環境最佳實踐：pyenv + venv + pip 完整指南", "python-venv-best-practices", "Python虛擬環境, pyenv, venv"),
        ("Mac M 晶片 AI 開發環境優化：充分利用神經網路引擎", "mac-apple-silicon-ai-dev", "Mac M晶片, Apple Silicon, AI開發優化"),
        ("Redis 快取配置：AI 應用效能提升的關鍵設定", "redis-cache-ai-performance", "Redis配置, 快取, AI效能"),
        ("FastAPI 生產環境配置：AI API 服務的最佳實踐", "fastapi-production-config", "FastAPI配置, AI API, 生產環境"),
    ],
    "tutorials": [
        ("AI Agent 設計模式：ReAct、Plan-and-Execute、Reflection 詳解", "ai-agent-design-patterns", "AI Agent設計, ReAct, Plan-Execute"),
        ("向量資料庫入門：從概念到實作的完整學習路徑", "vector-database-tutorial", "向量資料庫, embedding, 語義搜索"),
        ("用 Python 打造你的第一個 AI 聊天機器人：完整教學", "python-chatbot-tutorial", "Python聊天機器人, AI開發, 入門教學"),
        ("Transformer 架構詳解：不用數學也能理解注意力機制", "transformer-architecture-explained", "Transformer架構, 注意力機制, AI理論"),
        ("RAG 系統進階實作：提升知識庫問答準確率的 5 個技巧", "rag-advanced-techniques", "RAG系統, 知識庫問答, AI準確率"),
        ("Fine-tuning 小型 LLM：用 LoRA 訓練你的業務專屬模型", "lora-fine-tuning-tutorial", "Fine-tuning, LoRA, 模型微調"),
        ("多模態 AI 入門：圖文混合處理的實際應用案例", "multimodal-ai-tutorial", "多模態AI, 圖文處理, Vision AI"),
        ("AI 評估指標完全指南：BLEU、ROUGE、BERTScore 怎麼用", "ai-evaluation-metrics-guide", "AI評估, BLEU, ROUGE, BERTScore"),
        ("Prompt 注入攻擊防護：保護你的 AI 應用不被越獄", "prompt-injection-defense", "Prompt注入, AI安全, 越獄防護"),
        ("串流輸出實作：讓 AI 回覆像打字一樣即時顯示", "streaming-output-tutorial", "串流輸出, Streaming AI, 即時顯示"),
        ("AI 工作流 101：n8n 自動化你的日常任務", "n8n-automation-101", "n8n教學, 工作流自動化, AI任務"),
        ("OpenAI Assistants API 完整教學：打造有記憶的 AI 助理", "openai-assistants-api-tutorial", "OpenAI Assistants, AI記憶, 持久對話"),
        ("Hugging Face 模型部署：從下載到推論 API 的完整流程", "huggingface-model-deployment", "Hugging Face部署, 模型推論, AI API"),
        ("AI 成本控制策略：如何降低 90% 的 API 費用", "ai-cost-optimization-strategies", "AI成本控制, API費用, Token優化"),
        ("Knowledge Graph + LLM：讓 AI 理解複雜關係的新範式", "knowledge-graph-llm-tutorial", "Knowledge Graph, LLM, AI關係理解"),
    ],
    "workflows": [
        ("全自動內容行銷流水線：AI 從選題到發布的完整自動化", "content-marketing-automation", "內容行銷自動化, AI發布, 選題"),
        ("每日 AI 簡報自動化：聚合全球科技新聞推送到 Telegram", "daily-ai-briefing-automation", "每日簡報, AI新聞聚合, Telegram自動化"),
        ("電商訂單自動化：AI 處理退款、投訴、庫存管理", "ecommerce-order-automation", "電商自動化, 訂單處理, AI客服"),
        ("會議記錄 AI 工作流：語音轉文字到摘要到 Notion 一鍵搞定", "meeting-notes-ai-workflow", "會議記錄, 語音轉文字, Notion自動化"),
        ("社群媒體排程工作流：一鍵發布多平台的 AI 輔助系統", "social-media-scheduling-workflow", "社群媒體排程, 多平台發布, AI輔助"),
        ("潛在客戶自動培育：AI 郵件序列 + CRM 整合工作流", "lead-nurturing-ai-workflow", "潛在客戶培育, 郵件自動化, CRM整合"),
        ("財務對帳自動化：AI 讀取銀行對帳單並分類記帳", "financial-reconciliation-workflow", "財務自動化, 銀行對帳, AI記帳"),
        ("程式碼審查自動化：PR 提交自動觸發 AI 代碼分析", "code-review-automation-workflow", "程式碼審查, PR自動化, AI分析"),
        ("客戶意見分析工作流：自動收集評論並生成洞察報告", "customer-feedback-analysis-workflow", "客戶意見分析, 評論分析, AI洞察"),
        ("知識庫更新工作流：讓 AI 自動整理並歸檔每日學習內容", "knowledge-base-update-workflow", "知識庫管理, AI整理, 學習自動化"),
        ("電話銷售 AI 輔助：即時轉錄 + 話術建議 + 跟進自動化", "sales-call-ai-workflow", "電話銷售, AI輔助, 話術建議"),
        ("供應鏈監控工作流：AI 自動追蹤貨物並預警延誤風險", "supply-chain-monitoring-workflow", "供應鏈監控, AI預警, 物流追蹤"),
        ("HR 招募自動化：AI 篩選履歷到安排面試的完整流程", "hr-recruitment-automation", "HR招募, 履歷篩選, 面試安排"),
        ("數據報告自動生成：每週 KPI 儀表板自動更新發送", "kpi-report-automation-workflow", "KPI報告, 數據自動化, 週報"),
        ("多語言客服自動化：AI 即時翻譯 + 多平台統一收件匣", "multilingual-support-workflow", "多語言客服, AI翻譯, 統一收件匣"),
    ],
    "articles": [
        ("DeepSeek R2 技術深度解析：開源模型即將超越 GPT-4o？", "deepseek-r2-analysis", "DeepSeek R2, 開源LLM, GPT-4o比較"),
        ("Apple Intelligence 2026 更新：Siri 終於學會真正的 AI 推理", "apple-intelligence-2026-update", "Apple Intelligence, Siri AI, 推理能力"),
        ("Google Gemini 2.0 Ultra 實測：多模態 AI 的新標竿", "gemini-2-ultra-review", "Gemini 2.0, 多模態AI, Google AI"),
        ("Perplexity AI 商業化之路：搜尋引擎的 AI 顛覆者", "perplexity-ai-business-model", "Perplexity AI, AI搜索引擎, 商業模式"),
        ("2026 AI 晶片戰爭：NVIDIA H200 vs AMD MI300X vs Apple M4 Ultra", "ai-chip-war-2026", "AI晶片, NVIDIA H200, AMD MI300X"),
        ("量子計算遇上 AI：IBM Quantum 最新進展對 ML 的意義", "quantum-computing-ai-2026", "量子計算, IBM Quantum, 機器學習"),
        ("Meta Llama 4 發布：開源 AI 生態系的新里程碑", "meta-llama-4-release", "Meta Llama 4, 開源AI, LLM發布"),
        ("AI Agent 創業浪潮：2026 年最值得關注的 10 家新創", "ai-agent-startups-2026", "AI Agent創業, AI新創, 2026趨勢"),
        ("OpenAI o3 推理模型：數學和程式競賽的人類水平突破", "openai-o3-reasoning-model", "OpenAI o3, 推理模型, AI競賽"),
        ("自動駕駛 AI 2026：Tesla FSD vs Waymo vs 比亞迪 DM-i", "autonomous-driving-2026", "自動駕駛, Tesla FSD, Waymo"),
        ("AI 在醫療診斷的突破：比醫生更準確的影像識別系統", "ai-medical-diagnosis-2026", "AI醫療診斷, 影像識別, 醫療AI"),
        ("大模型 Token 定價戰：誰能把 AI 費用降到零？", "llm-pricing-competition-2026", "LLM定價, AI費用, Token成本"),
        ("Mistral AI 歐洲崛起：挑戰 OpenAI 的法國 AI 獨角獸", "mistral-ai-european-rise", "Mistral AI, 歐洲AI, 法國獨角獸"),
        ("AI 版權爭議 2026：紐約時報 vs OpenAI 判決後的影響", "ai-copyright-lawsuit-2026", "AI版權, 訓練數據, 版權法"),
        ("邊緣 AI 崛起：智慧手機本地推論的效能革命", "edge-ai-smartphone-2026", "邊緣AI, 本地推論, 手機AI"),
        ("Anthropic Claude 4 系列評測：最擅長安全推理的 AI", "anthropic-claude-4-review", "Claude 4, Anthropic, AI安全推理"),
        ("中國 AI 追趕戰：文心一言 4.0、通義千問、混元的最新進展", "china-ai-competition-2026", "中國AI, 文心一言, 通義千問"),
        ("AI 輔助科學發現：AlphaFold 3 在藥物設計的實際應用", "alphafold3-drug-discovery", "AlphaFold 3, 藥物設計, 蛋白質結構"),
        ("Robotics AI 2026：人形機器人走進工廠的關鍵一年", "humanoid-robot-2026", "人形機器人, Robotics AI, 工廠自動化"),
        ("AI 監管全球圖譜：歐盟 AI Act 實施後各國的跟進策略", "global-ai-regulation-2026", "AI監管, 歐盟AI Act, 全球AI政策"),
    ],
}

# ── SQLite 初始化 ──────────────────────────────────────────────────────────────
def init_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            date TEXT,
            category TEXT,
            slug TEXT UNIQUE,
            title TEXT,
            file_path TEXT,
            url TEXT,
            published_at TEXT DEFAULT (datetime('now'))
        )
    """)
    con.commit()
    return con

def get_published_slugs(con):
    rows = con.execute("SELECT slug FROM articles").fetchall()
    return {r[0] for r in rows}

def log_article(con, category, slug, title, file_path, url):
    con.execute(
        "INSERT OR IGNORE INTO articles (date, category, slug, title, file_path, url) VALUES (?,?,?,?,?,?)",
        (str(date.today()), category, slug, title, file_path, url)
    )
    con.commit()

# ── MiniMax 呼叫 ───────────────────────────────────────────────────────────────
def call_minimax(prompt: str, system: str = "", max_retries: int = 3) -> str:
    messages = [{"role": "user", "content": prompt}]
    payload = {
        "model": "MiniMax-M2.1",
        "max_tokens": 4096,
        "messages": messages,
    }
    if system:
        payload["system"] = system
    headers = {
        "x-api-key": MINIMAX_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }
    for attempt in range(max_retries):
        try:
            resp = requests.post(MINIMAX_URL, json=payload, headers=headers, timeout=120)
            resp.raise_for_status()
            data = resp.json()
            for block in data.get("content", []):
                if block.get("type") == "text":
                    return block["text"]
            return ""
        except (requests.ConnectionError, requests.Timeout, requests.HTTPError) as e:
            if attempt < max_retries - 1:
                wait = 2 ** (attempt + 1)
                print(f"[minimax] retry {attempt + 1}/{max_retries} after {wait}s: {e}")
                time.sleep(wait)
            else:
                raise
    return ""

# ── 文章生成 ───────────────────────────────────────────────────────────────────
def generate_article_content(title: str, keywords: str, category: str) -> dict:
    cat_name = CATEGORIES[category]["name"]
    system = textwrap.dedent(f"""
        你是一位專業的 AI 科技內容作家，專注於 {cat_name} 領域。
        用繁體中文寫作，語氣專業但易讀。
        內容要對讀者有實際幫助，包含具體步驟、範例和實用建議。
        優化 AEO（Answer Engine Optimization）：在文章開頭直接給出核心答案。
    """).strip()

    prompt = textwrap.dedent(f"""
        請為以下主題撰寫一篇完整的技術文章，輸出嚴格按照指定格式：

        主題：{title}
        關鍵詞：{keywords}
        分類：{cat_name}

        輸出格式（請嚴格遵守，每個標記必須獨佔一行）：
        ---DESCRIPTION---
        [150字以內的 meta description，含核心關鍵詞]
        ---READ_TIME---
        [閱讀時間，如：8]
        ---CONTENT---
        [文章正文，使用 HTML 標籤：<h2>, <h3>, <p>, <ul>, <li>, <ol>, <strong>, <code>, <pre><code>]
        [開頭第一段必須直接回答「{title}」這個問題或主題的核心答案（AEO 優化）]
        [包含 3-5 個 H2 大標題，每節 150-300 字]
        [包含至少一個程式碼範例或具體操作步驟]
        [總字數 800-1500 字]
        ---FAQ---
        Q1: [常見問題1]
        A1: [答案1，100字以內]
        Q2: [常見問題2]
        A2: [答案2，100字以內]
        Q3: [常見問題3]
        A3: [答案3，100字以內]
        ---END---
    """).strip()

    raw = call_minimax(prompt, system)

    def extract(tag, text):
        pattern = rf"---{tag}---\s*(.*?)(?=---\w+---|$)"
        m = re.search(pattern, text, re.DOTALL)
        return m.group(1).strip() if m else ""

    description = extract("DESCRIPTION", raw)
    read_time   = extract("READ_TIME", raw).strip().split()[0] if extract("READ_TIME", raw) else "8"
    content     = extract("CONTENT", raw)
    faq_raw     = extract("FAQ", raw)

    # Parse FAQ
    faqs = []
    q_parts = re.split(r"Q\d+:", faq_raw)
    for part in q_parts[1:]:
        qa = re.split(r"A\d+:", part)
        if len(qa) >= 2:
            faqs.append({
                "q": qa[0].strip(),
                "a": qa[1].strip()
            })

    return {
        "description": description or f"{title} — 完整指南與實用技巧",
        "read_time": read_time,
        "content": content,
        "faqs": faqs[:3],
    }

# ── HTML 模板 ──────────────────────────────────────────────────────────────────
def build_html(title, slug, category, article_date, data: dict) -> str:
    cat = CATEGORIES[category]
    cat_name  = cat["name"]
    cat_icon  = cat["icon"]
    cat_dir   = cat["dir"]
    cat_url   = f"/Openclaw/{cat_dir}/"
    article_url = f"{BASE_URL}/{cat_dir}/{article_date}_{slug}.html"
    canonical   = f"https://inari-kira-isla.github.io/Openclaw/{cat_dir}/{article_date}_{slug}.html"

    faq_schema_items = ""
    faq_html = ""
    for faq in data["faqs"]:
        faq_schema_items += f"""
        {{
          "@type": "Question",
          "name": "{faq['q'].replace('"', '&quot;')}",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "{faq['a'].replace('"', '&quot;')}"
          }}
        }},"""
        faq_html += f"""
          <div class="faq-item">
            <h3 class="faq-q">{faq['q']}</h3>
            <p class="faq-a">{faq['a']}</p>
          </div>"""

    schema_article = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": data["description"],
        "datePublished": article_date,
        "dateModified": article_date,
        "author": {"@type": "Organization", "name": "AI 學習寶庫"},
        "publisher": {"@type": "Organization", "name": "AI 學習寶庫",
                      "url": "https://inari-kira-isla.github.io/Openclaw/"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
        "articleSection": cat_name,
    }, ensure_ascii=False)

    schema_faq = ""
    if data["faqs"]:
        schema_faq = f"""
  <script type="application/ld+json">{{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [{faq_schema_items.rstrip(",")}]
  }}</script>"""

    return f"""<!DOCTYPE html>
<html lang="zh-TW" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | AI 學習寶庫</title>
  <meta name="description" content="{data['description']}">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" type="application/rss+xml" title="AI 學習寶庫 RSS" href="/Openclaw/feed.xml">
  <link rel="llms-txt" href="https://inari-kira-isla.github.io/Openclaw/llms.txt">
  <link rel="stylesheet" href="/Openclaw/style.css">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{data['description']}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{article_url}">
  <script type="application/ld+json">{schema_article}</script>{schema_faq}
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"EducationalOrganization","name":"AI 學習寶庫","url":"https://inari-kira-isla.github.io/Openclaw/","description":"每日分享 AI 提示詞、系統配置、自動化工作流。","alternateName":"AI Learning Treasure Trove","sameAs":["https://openclaw-ai-tracker.inariglobal.workers.dev/Openclaw/","https://github.com/Inari-Kira-Isla/Openclaw"]}}</script>
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"這個網站適合什麼樣的 AI 學習者？","acceptedAnswer":{{"@type":"Answer","text":"無論您是 AI 初學者還是有經驗的開發者，AI 學習寶庫都提供了從基礎到進階的內容，滿足不同層次的需求。"}}}},{{"@type":"Question","name":"網站主要涵蓋哪些 AI 工具和技術？","acceptedAnswer":{{"@type":"Answer","text":"網站涵蓋 Claude、ChatGPT、Ollama 等多種 AI 工具，以及提示詞設計、系統配置和自動化工作流等技術。"}}}},{{"@type":"Question","name":"網站內容更新頻率如何？","acceptedAnswer":{{"@type":"Answer","text":"網站內容每日更新，確保您能獲取最新的 AI 知識和技術。"}}}},{{"@type":"Question","name":"網站提供的提示詞範本有什麼特色？","acceptedAnswer":{{"@type":"Answer","text":"網站提供專業的 AI 提示詞範本與設計技巧，幫助您充分發揮 AI 的潛力，並針對不同應用場景提供結構化提示詞設計指南。"}}}},{{"@type":"Question","name":"如果我想了解最新的 AI 科技趨勢，這個網站能提供什麼幫助？","acceptedAnswer":{{"@type":"Answer","text":"網站提供最新的 AI 科技資訊與深度分析報導，幫助您掌握行業脈動，了解 AI 發展的最新動態。"}}}},{{"@type":"Question","name":"網站是否有提供系統配置的相關教學？","acceptedAnswer":{{"@type":"Answer","text":"網站提供AI工具與系統的完整配置指南，輕鬆搭建最佳開發環境，並持續更新。"}}}},{{"@type":"Question","name":"這個網站和其他AI學習資源有什麼不同？","acceptedAnswer":{{"@type":"Answer","text":"AI 學習寶庫專注於實戰知識，提供每日更新的內容，並涵蓋多種 AI 工具和技術，提供更全面的學習體驗。"}}}},{{"@type":"Question","name":"有沒有推薦的入門學習路徑？","acceptedAnswer":{{"@type":"Answer","text":"建議從提示詞設計完全指南開始，然後逐步學習系統配置和自動化工作流，最後關注科技趨勢，掌握行業動態。"}}}}]}}</script>
</head>
<body class="page-wrap">
  <div class="read-progress" id="readProgress"></div>

  <nav class="site-nav" id="nav">
    <div class="nav-inner">
      <a href="/Openclaw/" class="nav-brand"><span class="brand-emoji">🤖</span><span>AI 學習寶庫</span></a>
      <div class="nav-links" id="navLinks">
        <a href="/Openclaw/prompts/" class="nav-link">💡 提示詞</a>
        <a href="/Openclaw/configs/" class="nav-link">⚙️ 系統配置</a>
        <a href="/Openclaw/tutorials/" class="nav-link">📚 教學</a>
        <a href="/Openclaw/workflows/" class="nav-link">🔄 工作流</a>
        <a href="/Openclaw/articles/" class="nav-link">📰 科技趨勢</a>
      </div>
      <div class="nav-right">
        <button class="theme-btn" id="themeBtn" title="切換深色/淺色模式">🌙</button>
        <button class="nav-burger" id="navBurger" aria-label="選單">☰</button>
      </div>
    </div>
  </nav>

  <div class="article-wrap">
    <nav class="breadcrumb">
      <a href="/Openclaw/">首頁</a>
      <span class="bc-sep">›</span>
      <a href="{cat_url}">{cat_icon} {cat_name}</a>
      <span class="bc-sep">›</span>
      <span>{title[:30]}{'...' if len(title) > 30 else ''}</span>
    </nav>

    <header class="article-header">
      <div class="art-item-badge">{cat_icon} {cat_name}</div>
      <h1 class="article-title">{title}</h1>
      <div class="article-info">
        <span>📅 {article_date}</span>
        <span>⏱ {data['read_time']} 分鐘閱讀</span>
        <span>✍️ AI 學習寶庫</span>
      </div>
    </header>

    <div class="article-body">
      {data['content']}
    </div>

    {f'''<section class="faq-section" style="margin-top:3rem;padding-top:2rem;border-top:1px solid var(--border)">
      <h2 style="margin-bottom:1.5rem">常見問題</h2>
      {faq_html}
    </section>''' if data['faqs'] else ''}

    <div style="margin-top:3rem;padding:20px;background:var(--bg-2);border-radius:var(--r);text-align:center">
      <p style="font-size:14px;color:var(--text-2);margin-bottom:12px">繼續探索更多 {cat_name} 內容</p>
      <a href="{cat_url}" style="display:inline-block;padding:10px 24px;background:var(--primary);color:#fff;border-radius:var(--r-sm);text-decoration:none;font-weight:600;font-size:14px">查看更多文章 →</a>
    </div>
  </div>

  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-brand">🤖 AI 學習寶庫</div>
      <nav class="footer-nav">
        <a href="/Openclaw/prompts/">提示詞</a>
        <a href="/Openclaw/configs/">系統配置</a>
        <a href="/Openclaw/tutorials/">教學</a>
        <a href="/Openclaw/workflows/">工作流</a>
        <a href="/Openclaw/articles/">科技趨勢</a>
        <a href="/Openclaw/feed.xml">RSS</a>
      </nav>
      <address class="footer-contact">
        <strong>AI 學習寶庫</strong><br>
        GitHub：<a href="https://github.com/Inari-Kira-Isla/Openclaw">Inari-Kira-Isla/Openclaw</a>
      </address>
      <div class="footer-copy">© 2026 AI Governance System · CC BY 4.0</div>
    </div>
  </footer>

  <script>
    // Theme
    const html = document.documentElement, btn = document.getElementById('themeBtn');
    const saved = localStorage.getItem('oc-theme') || 'light';
    html.dataset.theme = saved; btn.textContent = saved === 'dark' ? '☀️' : '🌙';
    btn.addEventListener('click', () => {{
      const next = html.dataset.theme === 'dark' ? 'light' : 'dark';
      html.dataset.theme = next; localStorage.setItem('oc-theme', next);
      btn.textContent = next === 'dark' ? '☀️' : '🌙';
    }});
    document.getElementById('navBurger').addEventListener('click', () => {{
      document.getElementById('nav').classList.toggle('open');
    }});
    // Reading progress
    const bar = document.getElementById('readProgress');
    window.addEventListener('scroll', () => {{
      const d = document.documentElement;
      const pct = d.scrollTop / (d.scrollHeight - d.clientHeight);
      bar.style.transform = `scaleX(${{Math.min(pct, 1)}})`;
    }});
  </script>
</body>
</html>"""

# ── 更新 sitemap.xml ───────────────────────────────────────────────────────────
def update_sitemap(new_url: str):
    sitemap_path = os.path.join(REPO_DIR, "sitemap.xml")
    if not os.path.exists(sitemap_path):
        return
    with open(sitemap_path, "r", encoding="utf-8") as f:
        content = f.read()
    if new_url in content:
        return
    today = str(date.today())
    entry = f'  <url><loc>{new_url}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>\n'
    content = content.replace("</urlset>", entry + "</urlset>")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(content)

# ── 更新分類首頁 ───────────────────────────────────────────────────────────────
def update_category_index(category: str, title: str, slug: str, article_date: str, description: str):
    cat = CATEGORIES[category]
    index_path = os.path.join(REPO_DIR, cat["dir"], "index.html")
    if not os.path.exists(index_path):
        return

    article_url = f"/Openclaw/{cat['dir']}/{article_date}_{slug}.html"
    short_desc = description[:120] + "..." if len(description) > 120 else description

    new_item = f"""
          <a href="{article_url}" class="art-item reveal">
            <div class="art-item-badge">最新</div>
            <h3>{title}</h3>
            <p>{short_desc}</p>
            <div class="art-item-meta">
              <span>{article_date}</span>
              <span class="sep">·</span>
              <span>AI 生成</span>
            </div>
          </a>"""

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 插入在 art-list 的最前面
    content = content.replace(
        '<div class="art-list">',
        '<div class="art-list">' + new_item,
        1
    )
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

# ── Git push ───────────────────────────────────────────────────────────────────
def git_push_article(category, slug, article_date, title, html, description, article_url):
    """Checkout gh-pages, write article + update sitemap/index, commit and push."""
    original_branch = None
    try:
        # Remember current branch
        r = subprocess.run(["git", "-C", REPO_DIR, "rev-parse", "--abbrev-ref", "HEAD"],
                          capture_output=True, text=True)
        original_branch = r.stdout.strip()

        # Stash everything on current branch (including untracked files)
        subprocess.run(["git", "-C", REPO_DIR, "stash", "--include-untracked"],
                      capture_output=True)

        # Checkout gh-pages
        subprocess.run(["git", "-C", REPO_DIR, "checkout", "gh-pages"],
                      check=True, capture_output=True)
        subprocess.run(["git", "-C", REPO_DIR, "pull", "--ff-only", "origin", "gh-pages"],
                      capture_output=True)

        # Write article HTML on gh-pages branch
        cat_dir = CATEGORIES[category]["dir"]
        filename = f"{article_date}_{slug}.html"
        file_path = os.path.join(REPO_DIR, cat_dir, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

        # Update sitemap and category index (on gh-pages version of these files)
        update_sitemap(article_url)
        update_category_index(category, title, slug, article_date, description)

        # Stage files
        files_to_add = [
            file_path,
            os.path.join(REPO_DIR, "sitemap.xml"),
            os.path.join(REPO_DIR, cat_dir, "index.html"),
        ]
        for f in files_to_add:
            subprocess.run(["git", "-C", REPO_DIR, "add", f], check=True, capture_output=True)

        # Commit and push
        msg = f"content: {title[:60]}"
        subprocess.run(["git", "-C", REPO_DIR, "commit", "-m", msg],
                      check=True, capture_output=True)
        subprocess.run(["git", "-C", REPO_DIR, "push", "origin", "gh-pages"],
                      check=True, capture_output=True)
        print(f"[git] pushed to gh-pages: {filename}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[git] error: {e}")
        return False
    finally:
        # Always return to original branch and restore stash
        if original_branch:
            subprocess.run(["git", "-C", REPO_DIR, "checkout", original_branch],
                          capture_output=True)
            subprocess.run(["git", "-C", REPO_DIR, "stash", "pop"],
                          capture_output=True)

# ── Telegram 通知 ──────────────────────────────────────────────────────────────
def notify_telegram(msg: str):
    try:
        result = subprocess.run(
            ["/usr/local/bin/openclaw", "message", "send",
             "--channel", "telegram", "--account", "kira",
             "--target", TG_CHAT_ID, "--message", msg],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode == 0:
            print(f"[telegram] ✅ 通知已發送")
        else:
            print(f"[telegram] ❌ 發送失敗 (exit {result.returncode}): {result.stderr.strip()}")
    except Exception as e:
        print(f"[telegram] ❌ 例外: {e}")

# ── 主流程 ────────────────────────────────────────────────────────────────────
def main():
    print(f"[site_article_generator] 啟動 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    con = init_db()
    published = get_published_slugs(con)

    # 按類別輪流：根據今天已發布文章數決定分類
    today_rows = con.execute("SELECT category FROM articles WHERE date=?", (str(date.today()),)).fetchall()
    today_cats = [r[0] for r in today_rows]
    cat_counts = {c: today_cats.count(c) for c in CATEGORIES}
    category = min(cat_counts, key=lambda c: cat_counts[c])

    # 選未發布的主題
    pool = TOPIC_POOL[category]
    available = [(t, s, k) for t, s, k in pool if s not in published]
    if not available:
        print(f"[site_article_generator] {category} 主題已全部發布，隨機選取")
        available = pool

    topic = random.choice(available)
    title, slug, keywords = topic
    article_date = str(date.today())

    print(f"[site_article_generator] 生成: [{category}] {title}")

    # 生成內容 (API 呼叫，不需要檔案系統)
    try:
        data = generate_article_content(title, keywords, category)
    except Exception as e:
        print(f"[site_article_generator] 生成失敗: {e}")
        sys.exit(1)

    # 在記憶體中建立 HTML (不寫入檔案)
    html = build_html(title, slug, category, article_date, data)

    # Git: checkout gh-pages → 寫入檔案 → commit → push → 回到原分支
    cat_dir = CATEGORIES[category]["dir"]
    filename = f"{article_date}_{slug}.html"
    file_path = os.path.join(REPO_DIR, cat_dir, filename)
    article_url = f"{BASE_URL}/{cat_dir}/{filename}"

    pushed = git_push_article(category, slug, article_date, title, html,
                              data["description"], article_url)

    # 記錄到 DB
    log_article(con, category, slug, title, file_path, article_url)
    con.close()

    status = "✅ 已發布" if pushed else "⚠️ 寫入成功但 push 失敗"
    print(f"[site_article_generator] {status}: {title}")

    # Telegram 快報
    notify_telegram(f"📝 新文章發布\n{CATEGORIES[category]['icon']} {title}\n🔗 {article_url}")

if __name__ == "__main__":
    main()
