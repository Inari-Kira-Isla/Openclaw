// ============================================
// OpenClaw AI Footprint Tracker
// Cloudflare Worker — Aggregated KV storage
// ============================================

const GITHUB_PAGES_URL = "https://inari-kira-isla.github.io/Openclaw";

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
  // Chinese AI Bots
  "Baiduspider": "Baidu/Ernie AI",
  "Sogou": "Sogou AI",
  "ChatGLM": "ChatGLM/Zhipu AI",
  "360Spider": "360 AI",
  "HunyuanBot": "Tencent Hunyuan",
  "SenseChat": "SenseChat AI",
  "SparkBot": "Spark/iFlytek AI",
  "Kimi": "Kimi/Moonshot AI",
  "Doubao": "Doubao AI",
  "XiaoIce": "XiaoIce AI",
};

async function detectAIBot(userAgent) {
  if (!userAgent) return null;
  const ua = userAgent.toLowerCase();
  for (const [pattern, name] of Object.entries(AI_BOTS)) {
    if (ua.includes(pattern.toLowerCase())) {
      return { pattern, name };
    }
  }
  return null;
}

// Aggregated stats: 1 KV key instead of 59 individual keys
const AGG_KEY = "agg-stats";

async function getAgg(env) {
  try {
    const raw = await env.AI_FOOTPRINT.get(AGG_KEY);
    return raw ? JSON.parse(raw) : { _date: "", today: {}, totals: {} };
  } catch (e) { return { _date: "", today: {}, totals: {} }; }
}

async function putAgg(env, agg) {
  await env.AI_FOOTPRINT.put(AGG_KEY, JSON.stringify(agg));
}

async function logAIVisit(env, botInfo, request, overridePath) {
  const today = new Date().toISOString().split("T")[0];
  const url = new URL(request.url);
  const pagePath = overridePath || url.pathname;

  // Update aggregated blob (1 read + 1 write)
  const agg = await getAgg(env);
  if (agg._date !== today) { agg.today = {}; agg._date = today; }
  agg.today[botInfo.pattern] = (agg.today[botInfo.pattern] || 0) + 1;
  agg.totals[botInfo.pattern] = (agg.totals[botInfo.pattern] || 0) + 1;
  await putAgg(env, agg);

  // Store visit log
  const logKey = `log:${today}`;
  const existing = JSON.parse((await env.AI_FOOTPRINT.get(logKey)) || "[]");
  existing.push({
    ts: Date.now(),
    bot: botInfo.name,
    ua: (request.headers.get("user-agent") || "").substring(0, 100),
    path: pagePath,
    ref: request.headers.get("referer") || "",
    src: overridePath ? "pixel" : "proxy",
  });
  if (existing.length > 500) existing.shift();
  await env.AI_FOOTPRINT.put(logKey, JSON.stringify(existing), { expirationTtl: 30 * 86400 });
}

async function logGeneralVisit(env, request) {
  const today = new Date().toISOString().split("T")[0];
  const agg = await getAgg(env);
  if (agg._date !== today) { agg.today = {}; agg._date = today; }
  agg.today["_human"] = (agg.today["_human"] || 0) + 1;
  agg.totals["_human"] = (agg.totals["_human"] || 0) + 1;
  await putAgg(env, agg);
}

export default {
  async fetch(request, env, ctx) {
    try {
      const url = new URL(request.url);

      // === Tracking pixel endpoint ===
      if (url.pathname === "/track") {
        const userAgent = request.headers.get("user-agent") || "";
        const botInfo = await detectAIBot(userAgent);
        if (botInfo && env.AI_FOOTPRINT) {
          const page = url.searchParams.get("p") || "/";
          const trackReq = new Request(request.url, request);
          ctx.waitUntil(logAIVisit(env, botInfo, trackReq, page));
        } else if (env.AI_FOOTPRINT) {
          ctx.waitUntil(logGeneralVisit(env, request));
        }
        const gif = Uint8Array.from(atob("R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"), c => c.charCodeAt(0));
        return new Response(gif, {
          headers: {
            "Content-Type": "image/gif",
            "Cache-Control": "no-store, no-cache, must-revalidate",
            "Access-Control-Allow-Origin": "*",
          },
        });
      }

      // === Migrate legacy keys to aggregated blob ===
      if (url.pathname === "/migrate-agg") {
        if (!env.AI_FOOTPRINT) return new Response("No KV", { status: 500 });
        const today = new Date().toISOString().split("T")[0];
        const agg = { _date: today, today: {}, totals: {} };
        for (const [pattern] of Object.entries(AI_BOTS)) {
          try {
            const tv = await env.AI_FOOTPRINT.get(`total:${pattern}`);
            if (tv) agg.totals[pattern] = parseInt(tv);
            const dv = await env.AI_FOOTPRINT.get(`day:${today}:${pattern}`);
            if (dv) agg.today[pattern] = parseInt(dv);
          } catch (e) {}
        }
        try {
          const ht = await env.AI_FOOTPRINT.get(`total:_human`);
          if (ht) agg.totals["_human"] = parseInt(ht);
          const hd = await env.AI_FOOTPRINT.get(`day:${today}:_human`);
          if (hd) agg.today["_human"] = parseInt(hd);
        } catch (e) {}
        await env.AI_FOOTPRINT.put(AGG_KEY, JSON.stringify(agg));
        return new Response(JSON.stringify({ migrated: agg }, null, 2), {
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
        });
      }

      // === AI Stats API endpoint (cached 900s) ===
      if (url.pathname === "/ai-stats.json") {
        const cache = caches.default;
        const cacheKey = new Request(request.url, { method: "GET" });
        const cached = await cache.match(cacheKey);
        if (cached) return cached;

        const today = new Date().toISOString().split("T")[0];
        const stats = { today: {}, totals: {}, recentVisits: [], generatedAt: new Date().toISOString() };

        if (!env.AI_FOOTPRINT) {
          return new Response(JSON.stringify(stats, null, 2), {
            headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*", "Cache-Control": "public, max-age=60" },
          });
        }

        try {
          // 1 KV read for all stats
          const agg = await getAgg(env);
          const todayData = (agg._date === today) ? agg.today : {};
          const totalData = agg.totals || {};

          for (const [pattern, name] of Object.entries(AI_BOTS)) {
            const dc = todayData[pattern] || 0;
            const tc = totalData[pattern] || 0;
            if (dc > 0) stats.today[name] = dc;
            if (tc > 0) stats.totals[name] = tc;
          }
          const ht = todayData["_human"] || 0;
          const hT = totalData["_human"] || 0;
          if (ht > 0) stats.today["Human Visitors"] = ht;
          if (hT > 0) stats.totals["Human Visitors"] = hT;

          // 1 more KV read for recent visits
          try {
            const logVal = await env.AI_FOOTPRINT.get(`log:${today}`);
            stats.recentVisits = JSON.parse(logVal || "[]").slice(-20);
          } catch (e) {}
        } catch (e) { stats._error = e.message; }

        const hasData = Object.keys(stats.totals).length > 0;
        const ttl = hasData ? 900 : 60;
        const resp = new Response(JSON.stringify(stats, null, 2), {
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*", "Cache-Control": `public, max-age=${ttl}` },
        });
        ctx.waitUntil(cache.put(cacheKey, resp.clone()));
        return resp;
      }

      // === Proxy to GitHub Pages ===
      let proxyPath = url.pathname;
      if (proxyPath === "/Openclaw" || proxyPath.startsWith("/Openclaw/")) {
        proxyPath = proxyPath.slice(9) || "/";
      }
      const targetUrl = GITHUB_PAGES_URL + proxyPath + url.search;
      const userAgent = request.headers.get("user-agent") || "";
      const botInfo = await detectAIBot(userAgent);

      if (botInfo && env.AI_FOOTPRINT) {
        ctx.waitUntil(logAIVisit(env, botInfo, request));
      } else if (env.AI_FOOTPRINT) {
        ctx.waitUntil(logGeneralVisit(env, request));
      }

      const response = await fetch(targetUrl, {
        method: request.method,
        headers: { "User-Agent": userAgent },
      });

      const newHeaders = new Headers(response.headers);
      newHeaders.set("Access-Control-Allow-Origin", "*");

      return new Response(response.body, {
        status: response.status,
        headers: newHeaders,
      });
    } catch (e) {
      return new Response(JSON.stringify({ error: e.message }), {
        status: 500,
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
      });
    }
  },
};
