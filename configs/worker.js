// ============================================
// OpenClaw AI Footprint Tracker
// Cloudflare Worker — D1 (Edge SQLite) storage
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

const BOT_OWNERS = {
  "GPTBot": "OpenAI", "ChatGPT-User": "OpenAI", "OAI-SearchBot": "OpenAI",
  "anthropic-ai": "Anthropic", "ClaudeBot": "Anthropic", "claude-web": "Anthropic",
  "PerplexityBot": "Perplexity", "Google-Extended": "Google", "Googlebot": "Google",
  "Bingbot": "Microsoft", "CCBot": "Common Crawl", "Bytespider": "ByteDance",
  "YouBot": "You.com", "cohere-ai": "Cohere", "Applebot": "Apple",
  "meta-externalagent": "Meta", "FacebookBot": "Meta", "ia_archiver": "Internet Archive",
  "Baiduspider": "Baidu", "Sogou": "Sogou", "ChatGLM": "Zhipu AI",
  "360Spider": "Qihoo 360", "HunyuanBot": "Tencent", "SenseChat": "SenseTime",
  "SparkBot": "iFlytek", "Kimi": "Moonshot AI", "Doubao": "ByteDance", "XiaoIce": "XiaoIce",
};

const BOT_REGIONS = {
  "GPTBot": "International", "ChatGPT-User": "International", "OAI-SearchBot": "International",
  "anthropic-ai": "International", "ClaudeBot": "International", "claude-web": "International",
  "PerplexityBot": "International", "Google-Extended": "International", "Googlebot": "International",
  "Bingbot": "International", "CCBot": "International",
  "YouBot": "International", "cohere-ai": "International", "Applebot": "International",
  "meta-externalagent": "International", "FacebookBot": "International", "ia_archiver": "International",
  "Bytespider": "CN", "Baiduspider": "CN", "Sogou": "CN", "ChatGLM": "CN",
  "360Spider": "CN", "HunyuanBot": "CN", "SenseChat": "CN",
  "SparkBot": "CN", "Kimi": "CN", "Doubao": "CN", "XiaoIce": "CN",
};

function detectAIBot(userAgent) {
  if (!userAgent) return null;
  const ua = userAgent.toLowerCase();
  for (const [pattern, name] of Object.entries(AI_BOTS)) {
    if (ua.includes(pattern.toLowerCase())) {
      return { pattern, name };
    }
  }
  return null;
}

async function logAIVisit(env, botInfo, request, overridePath) {
  const today = new Date().toISOString().split("T")[0];
  const path = overridePath || new URL(request.url).pathname;
  await env.DB.batch([
    env.DB.prepare(
      `INSERT INTO ai_visit_counts (site_slug, visit_date, bot_pattern, count_today)
       VALUES ('', ?, ?, 1)
       ON CONFLICT(site_slug, visit_date, bot_pattern)
       DO UPDATE SET count_today=count_today+1, updated_at=CURRENT_TIMESTAMP`
    ).bind(today, botInfo.pattern),
    env.DB.prepare(
      `INSERT INTO ai_visit_logs (site_slug, visit_date, timestamp_ms, bot_pattern, bot_name, ua, page_path, referer, source, bot_owner, bot_region)
       VALUES ('', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
    ).bind(
      today, Date.now(), botInfo.pattern, botInfo.name,
      (request.headers.get("user-agent") || "").substring(0, 200),
      path, request.headers.get("referer") || "",
      overridePath ? "pixel" : "proxy",
      BOT_OWNERS[botInfo.pattern] || "Unknown",
      BOT_REGIONS[botInfo.pattern] || "International"
    ),
  ]);
}

export default {
  async fetch(request, env, ctx) {
    try {
      const url = new URL(request.url);

      // === Tracking pixel endpoint ===
      if (url.pathname === "/track") {
        const userAgent = request.headers.get("user-agent") || "";
        const botInfo = detectAIBot(userAgent);
        if (botInfo && env.DB) {
          const page = url.searchParams.get("p") || "/";
          const trackReq = new Request(request.url, request);
          ctx.waitUntil(logAIVisit(env, botInfo, trackReq, page));
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

      // === Migrate KV data to D1 (one-time) ===
      if (url.pathname === "/migrate-kv-to-d1") {
        if (!env.AI_FOOTPRINT || !env.DB) return new Response("Need both KV and D1 bindings", { status: 500 });
        const today = new Date().toISOString().split("T")[0];
        const migrated = { counts: 0, logs: 0 };

        // Read aggregated KV blob
        const raw = await env.AI_FOOTPRINT.get("agg-stats");
        const agg = raw ? JSON.parse(raw) : { _date: "", today: {}, totals: {} };

        // Insert totals into D1
        const stmts = [];
        for (const [pattern, total] of Object.entries(agg.totals || {})) {
          if (pattern === "_human") continue;
          const todayCount = (agg._date === today && agg.today[pattern]) ? agg.today[pattern] : 0;
          stmts.push(
            env.DB.prepare(
              `INSERT INTO ai_visit_counts (site_slug, visit_date, bot_pattern, count_today)
               VALUES ('', ?, ?, ?)
               ON CONFLICT(site_slug, visit_date, bot_pattern)
               DO UPDATE SET count_today=MAX(count_today, excluded.count_today)`
            ).bind(today, pattern, todayCount)
          );
          // Insert a historical row with the total minus today
          const histCount = total - todayCount;
          if (histCount > 0) {
            stmts.push(
              env.DB.prepare(
                `INSERT INTO ai_visit_counts (site_slug, visit_date, bot_pattern, count_today)
                 VALUES ('', '2026-01-01', ?, ?)
                 ON CONFLICT(site_slug, visit_date, bot_pattern)
                 DO UPDATE SET count_today=MAX(count_today, excluded.count_today)`
              ).bind(pattern, histCount)
            );
          }
          migrated.counts++;
        }

        // Migrate recent logs
        try {
          const logVal = await env.AI_FOOTPRINT.get(`log:${today}`);
          const logs = JSON.parse(logVal || "[]");
          for (const log of logs.slice(-100)) {
            const botPattern = Object.entries(AI_BOTS).find(([, n]) => n === log.bot)?.[0] || log.bot;
            stmts.push(
              env.DB.prepare(
                `INSERT INTO ai_visit_logs (site_slug, visit_date, timestamp_ms, bot_pattern, bot_name, ua, page_path, referer, source)
                 VALUES ('', ?, ?, ?, ?, ?, ?, ?, ?)`
              ).bind(today, log.ts, botPattern, log.bot, (log.ua || "").substring(0, 200), log.path || "/", log.ref || "", log.src || "proxy")
            );
            migrated.logs++;
          }
        } catch (e) { migrated.logError = e.message; }

        // Execute in batches of 50 (D1 batch limit)
        for (let i = 0; i < stmts.length; i += 50) {
          await env.DB.batch(stmts.slice(i, i + 50));
        }

        return new Response(JSON.stringify({ migrated }, null, 2), {
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

        if (!env.DB) {
          return new Response(JSON.stringify(stats, null, 2), {
            headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*", "Cache-Control": "public, max-age=60" },
          });
        }

        try {
          const [todayCounts, totalCounts, logs] = await env.DB.batch([
            env.DB.prepare(
              `SELECT bot_pattern, count_today FROM ai_visit_counts WHERE site_slug='' AND visit_date=?`
            ).bind(today),
            env.DB.prepare(
              `SELECT bot_pattern, SUM(count_today) as total FROM ai_visit_counts WHERE site_slug='' GROUP BY bot_pattern`
            ),
            env.DB.prepare(
              `SELECT timestamp_ms as ts, bot_name as bot, ua, page_path as path, referer as ref, source as src
               FROM ai_visit_logs WHERE site_slug='' AND visit_date=?
               ORDER BY timestamp_ms DESC LIMIT 20`
            ).bind(today),
          ]);

          for (const row of todayCounts.results || []) {
            const name = AI_BOTS[row.bot_pattern];
            if (name && row.count_today > 0) stats.today[name] = row.count_today;
          }
          for (const row of totalCounts.results || []) {
            const name = AI_BOTS[row.bot_pattern];
            if (name && row.total > 0) stats.totals[name] = row.total;
          }
          stats.recentVisits = (logs.results || []).map(r => ({
            ts: r.ts, bot: r.bot, ua: r.ua, path: r.path, ref: r.ref, src: r.src,
          }));
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
      const botInfo = detectAIBot(userAgent);

      if (botInfo && env.DB) {
        ctx.waitUntil(logAIVisit(env, botInfo, request));
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
