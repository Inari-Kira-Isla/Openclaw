// ============================================
// OpenClaw AI Footprint Tracker
// Cloudflare Worker - Deploy at: dash.cloudflare.com
// Proxies GitHub Pages + logs AI bot visits to KV
// ============================================

const GITHUB_PAGES_URL = "https://inari-kira-isla.github.io/Openclaw";
const KV_NAMESPACE = "AI_FOOTPRINT"; // Bind KV namespace in CF dashboard

// Known AI crawlers User-Agent patterns
const AI_BOTS = {
  "GPTBot": "OpenAI GPT",
  "ChatGPT-User": "ChatGPT Browser",
  "OAI-SearchBot": "OpenAI Search",
  "anthropic-ai": "Anthropic Claude",
  "ClaudeBot": "Claude Crawler",
  "claude-web": "Claude Web",
  "PerplexityBot": "Perplexity AI",
  "Google-Extended": "Google Gemini Training",
  "Googlebot": "Google Search",
  "Bingbot": "Microsoft Bing AI",
  "CCBot": "Common Crawl",
  "Bytespider": "ByteDance AI",
  "YouBot": "You.com AI",
  "cohere-ai": "Cohere AI",
  "Applebot": "Apple AI",
  "meta-externalagent": "Meta AI",
  "FacebookBot": "Meta AI Bot",
  "ia_archiver": "Internet Archive",
};

async function detectAIBot(userAgent) {
  if (\!userAgent) return null;
  const ua = userAgent.toLowerCase();
  for (const [pattern, name] of Object.entries(AI_BOTS)) {
    if (ua.includes(pattern.toLowerCase())) {
      return { pattern, name };
    }
  }
  return null;
}

async function logAIVisit(env, botInfo, request) {
  const today = new Date().toISOString().split("T")[0];
  const url = new URL(request.url);
  
  // Increment daily counter for this bot
  const dayKey = `day:${today}:${botInfo.pattern}`;
  const current = parseInt(await env.AI_FOOTPRINT.get(dayKey) || "0");
  await env.AI_FOOTPRINT.put(dayKey, String(current + 1), { expirationTtl: 30 * 86400 });
  
  // Store visit detail (last 1000)
  const logKey = `log:${today}`;
  const existing = JSON.parse(await env.AI_FOOTPRINT.get(logKey) || "[]");
  existing.push({
    ts: Date.now(),
    bot: botInfo.name,
    ua: request.headers.get("user-agent")?.substring(0, 100),
    path: url.pathname,
    ref: request.headers.get("referer") || ""
  });
  // Keep only last 500 entries per day
  if (existing.length > 500) existing.shift();
  await env.AI_FOOTPRINT.put(logKey, JSON.stringify(existing), { expirationTtl: 30 * 86400 });
  
  // Update total counter
  const totalKey = `total:${botInfo.pattern}`;
  const total = parseInt(await env.AI_FOOTPRINT.get(totalKey) || "0");
  await env.AI_FOOTPRINT.put(totalKey, String(total + 1));
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // === AI Stats API endpoint ===
    if (url.pathname === "/ai-stats.json") {
      const today = new Date().toISOString().split("T")[0];
      const stats = { today: {}, totals: {}, recentVisits: [] };
      
      for (const [pattern, name] of Object.entries(AI_BOTS)) {
        const dayCount = parseInt(await env.AI_FOOTPRINT.get(`day:${today}:${pattern}`) || "0");
        const total = parseInt(await env.AI_FOOTPRINT.get(`total:${pattern}`) || "0");
        if (dayCount > 0) stats.today[name] = dayCount;
        if (total > 0) stats.totals[name] = total;
      }
      stats.recentVisits = JSON.parse(await env.AI_FOOTPRINT.get(`log:${today}`) || "[]").slice(-20);
      stats.generatedAt = new Date().toISOString();
      
      return new Response(JSON.stringify(stats, null, 2), {
        headers: { 
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Cache-Control": "no-cache"
        }
      });
    }
    
    // === Proxy to GitHub Pages ===
    const targetUrl = GITHUB_PAGES_URL + url.pathname + url.search;
    
    // Detect and log AI bots (async, non-blocking)
    const userAgent = request.headers.get("user-agent") || "";
    const botInfo = await detectAIBot(userAgent);
    if (botInfo && env.AI_FOOTPRINT) {
      ctx.waitUntil(logAIVisit(env, botInfo, request));
    }
    
    // Proxy the request
    const response = await fetch(targetUrl, {
      method: request.method,
      headers: { "User-Agent": userAgent }
    });
    
    return new Response(response.body, {
      status: response.status,
      headers: response.headers
    });
  }
};