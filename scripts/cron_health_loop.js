#!/usr/bin/env node
'use strict';

/**
 * cron_health_loop.js — Daily positive feedback loop for OpenClaw cron system
 *
 * Analyses run logs from the past 24h, scores each job on health / value / frequency,
 * auto-disables chronically failing jobs, detects duplicates, and sends a Telegram report.
 *
 * Zero npm dependencies — uses only Node built-ins (fs, path, child_process, fetch).
 */

const fs   = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ── Config ──────────────────────────────────────────────────────────────────
const OPENCLAW_HOME   = path.join(process.env.HOME || '/Users/ki', '.openclaw');
const JOBS_PATH       = path.join(OPENCLAW_HOME, 'cron', 'jobs.json');
const RUNS_DIR        = path.join(OPENCLAW_HOME, 'cron', 'runs');
const HISTORY_PATH    = path.join(OPENCLAW_HOME, 'cron', 'health-history.jsonl');

const TG_TOKEN   = process.env.TELEGRAM_BOT_TOKEN || '***REMOVED***';
const ADMIN_CHAT = '8399476482';

const CONSECUTIVE_ERROR_THRESHOLD = 3;
const LOOKBACK_MS = 24 * 60 * 60 * 1000; // 24 hours

// ── 1. loadJobs ─────────────────────────────────────────────────────────────
function loadJobs() {
  console.log('[loadJobs] Reading', JOBS_PATH);
  try {
    const raw = fs.readFileSync(JOBS_PATH, 'utf8');
    const data = JSON.parse(raw);
    console.log(`[loadJobs] Loaded ${data.jobs.length} jobs (version ${data.version})`);
    return data.jobs;
  } catch (err) {
    console.error('[loadJobs] Failed:', err.message);
    return [];
  }
}

// ── 2. loadRunLogs ──────────────────────────────────────────────────────────
function loadRunLogs(jobId, sinceMs) {
  const logPath = path.join(RUNS_DIR, `${jobId}.jsonl`);
  const runs = [];

  if (!fs.existsSync(logPath)) {
    return runs;
  }

  try {
    const lines = fs.readFileSync(logPath, 'utf8').split('\n');
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed) continue;
      try {
        const entry = JSON.parse(trimmed);
        if (entry.ts >= sinceMs) {
          runs.push(entry);
        }
      } catch (_) {
        // Corrupt line — skip silently
      }
    }
  } catch (err) {
    console.warn(`[loadRunLogs] Error reading ${logPath}: ${err.message}`);
  }

  return runs;
}

// ── 3. scoreJob ─────────────────────────────────────────────────────────────
function scoreJob(job, runs) {
  const total = runs.length;

  if (total === 0) {
    // No runs in 24h — use state to infer health
    const lastStatus = job.state?.lastStatus;
    const ce = job.state?.consecutiveErrors || 0;
    if (ce >= 3) return { health: 10, value: 0, frequency: 50, composite: 15 };
    if (lastStatus === 'ok' || lastStatus === 'skipped') return { health: 70, value: 50, frequency: 50, composite: 60 };
    return { health: 50, value: 50, frequency: 50, composite: 50 };
  }

  const okCount = runs.filter(r => r.status === 'ok').length;
  const skippedCount = runs.filter(r => r.status === 'skipped').length;
  const errorCount = runs.filter(r => r.status === 'error').length;

  // If ALL runs are "skipped" — job is working as designed (heartbeat/conditional)
  if (skippedCount === total) {
    return { health: 80, value: 30, frequency: 0, composite: 46 };
  }

  // health — success rate: ok / (ok + error), ignoring skipped
  const nonSkip = okCount + errorCount;
  const health = nonSkip > 0 ? Math.round((okCount / nonSkip) * 100) : 80;

  // value — runs with non-empty summary
  const valuableCount = runs.filter(r => {
    if (!r.summary) return false;
    const s = r.summary.trim();
    return s.length > 0 && s !== 'cron-efficiency';
  }).length;
  const value = Math.round((valuableCount / total) * 100);

  // frequency — how often it actually does work vs skipping
  const skipRate = skippedCount / total;
  const frequency = Math.round((1 - skipRate) * 100);

  // composite score
  const composite = Math.round(health * 0.5 + value * 0.3 + frequency * 0.2);

  return { health, value, frequency, composite };
}

// ── 4. autoDegrade ──────────────────────────────────────────────────────────
function autoDegrade(jobs) {
  const degraded = [];

  for (const job of jobs) {
    if (!job.enabled) continue;
    const ce = job.state?.consecutiveErrors || 0;
    if (ce < CONSECUTIVE_ERROR_THRESHOLD) continue;

    console.log(`[autoDegrade] Disabling "${job.name}" (id=${job.id}, consecutiveErrors=${ce})`);

    try {
      execSync(`openclaw cron edit ${job.id} --disable`, {
        timeout: 15000,
        stdio: 'pipe',
      });
      degraded.push({
        id:    job.id,
        name:  job.name,
        ce:    ce,
        error: job.state?.lastError || '(unknown)',
      });
      console.log(`[autoDegrade] Disabled "${job.name}" successfully`);
    } catch (err) {
      console.error(`[autoDegrade] Failed to disable "${job.name}": ${err.message}`);
    }
  }

  return degraded;
}

// ── 5. detectDuplicates ─────────────────────────────────────────────────────
function charOverlap(a, b) {
  // Simple character-level similarity: |intersection| / |union|
  const setA = new Set(a.toLowerCase());
  const setB = new Set(b.toLowerCase());
  let intersection = 0;
  for (const ch of setA) {
    if (setB.has(ch)) intersection++;
  }
  const union = new Set([...setA, ...setB]).size;
  return union === 0 ? 0 : intersection / union;
}

function detectDuplicates(jobs) {
  const enabled = jobs.filter(j => j.enabled);
  const dupes = [];

  for (let i = 0; i < enabled.length; i++) {
    for (let j = i + 1; j < enabled.length; j++) {
      const a = enabled[i];
      const b = enabled[j];

      // Must share the same cron schedule expression (skip jobs without one)
      if (!a.schedule?.expr || !b.schedule?.expr) continue;
      if (a.schedule.expr !== b.schedule.expr) continue;

      const sim = charOverlap(a.name, b.name);
      if (sim > 0.7) {
        dupes.push({
          job1:       { id: a.id, name: a.name },
          job2:       { id: b.id, name: b.name },
          schedule:   a.schedule.expr,
          similarity: Math.round(sim * 100) / 100,
        });
      }
    }
  }

  return dupes;
}

// ── 6. sendTelegram ─────────────────────────────────────────────────────────
async function sendTelegram(text) {
  const url = `https://api.telegram.org/bot${TG_TOKEN}/sendMessage`;
  console.log('[sendTelegram] Sending report...');

  try {
    const resp = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id:    ADMIN_CHAT,
        text:       text,
      }),
    });

    const body = await resp.json();
    if (!body.ok) {
      console.error('[sendTelegram] Telegram API error:', body.description);
      // Retry without Markdown if parse fails
      if (body.description && body.description.includes('parse')) {
        console.log('[sendTelegram] Retrying without Markdown...');
        const retry = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            chat_id: ADMIN_CHAT,
            text:    text,
          }),
        });
        const retryBody = await retry.json();
        if (retryBody.ok) {
          console.log('[sendTelegram] Sent (plain text fallback)');
        } else {
          console.error('[sendTelegram] Retry also failed:', retryBody.description);
        }
      }
    } else {
      console.log('[sendTelegram] Sent successfully');
    }
  } catch (err) {
    console.error('[sendTelegram] Network error:', err.message);
  }
}

// ── 7. writeHistory ─────────────────────────────────────────────────────────
function writeHistory(report) {
  console.log('[writeHistory] Appending to', HISTORY_PATH);
  try {
    const line = JSON.stringify(report) + '\n';
    fs.appendFileSync(HISTORY_PATH, line, 'utf8');
    console.log('[writeHistory] Done');
  } catch (err) {
    console.error('[writeHistory] Failed:', err.message);
  }
}

// ── 8. main ─────────────────────────────────────────────────────────────────
async function main() {
  const startMs = Date.now();
  const sinceMs = startMs - LOOKBACK_MS;
  const todayStr = new Date().toISOString().slice(0, 10);

  console.log('='.repeat(60));
  console.log(`[main] Cron Health Loop — ${todayStr}`);
  console.log(`[main] Lookback window: ${new Date(sinceMs).toISOString()} → now`);
  console.log('='.repeat(60));

  // ── Load jobs ──
  const jobs = loadJobs();
  if (jobs.length === 0) {
    console.error('[main] No jobs found. Aborting.');
    process.exit(1);
  }

  const enabledJobs  = jobs.filter(j => j.enabled);
  const disabledJobs = jobs.filter(j => !j.enabled);

  console.log(`[main] Enabled: ${enabledJobs.length}, Disabled: ${disabledJobs.length}`);

  // ── Load run logs & score each enabled job ──
  console.log('[main] Loading run logs and scoring...');
  const scoredJobs   = [];
  let totalRuns      = 0;
  let totalTokens    = 0;
  let totalOkRuns    = 0;
  let totalErrorRuns = 0;
  let totalSkipped   = 0;

  for (const job of enabledJobs) {
    const runs = loadRunLogs(job.id, sinceMs);
    const score = scoreJob(job, runs);

    totalRuns += runs.length;
    totalOkRuns    += runs.filter(r => r.status === 'ok').length;
    totalErrorRuns += runs.filter(r => r.status === 'error').length;
    totalSkipped   += runs.filter(r => r.status === 'skipped').length;

    // Sum token usage
    for (const run of runs) {
      if (run.usage && run.usage.total_tokens) {
        totalTokens += run.usage.total_tokens;
      } else if (run.status === 'ok') {
        // Estimate 1000 tokens per ok run without usage data
        totalTokens += 1000;
      }
    }

    scoredJobs.push({ job, runs, score });
  }

  console.log(`[main] Scored ${scoredJobs.length} jobs, ${totalRuns} total runs`);

  // ── Categorize ──
  const healthy  = scoredJobs.filter(s => s.score.composite >= 80);
  const degraded = scoredJobs.filter(s => s.score.composite >= 30 && s.score.composite < 80);
  const failed   = scoredJobs.filter(s => s.score.composite < 30);

  console.log(`[main] Healthy: ${healthy.length}, Degraded: ${degraded.length}, Failed: ${failed.length}`);

  // ── Auto-degrade high-error jobs ──
  console.log('[main] Checking for auto-degrade candidates...');
  const autoDegraded = autoDegrade(jobs);
  console.log(`[main] Auto-disabled ${autoDegraded.length} jobs`);

  // ── Detect duplicates ──
  console.log('[main] Scanning for duplicates...');
  const duplicates = detectDuplicates(jobs);
  console.log(`[main] Found ${duplicates.length} potential duplicate pairs`);

  // ── Top issues (lowest composite, up to 5) ──
  const topIssues = [...scoredJobs]
    .filter(s => s.score.composite < 80)
    .sort((a, b) => a.score.composite - b.score.composite)
    .slice(0, 5);

  // ── Format token count ──
  const formatTokens = (n) => {
    if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'M';
    if (n >= 1_000)     return (n / 1_000).toFixed(1) + 'K';
    return String(n);
  };

  const formatNum = (n) => n.toLocaleString('en-US');

  // ── Build Telegram report (plain text, no Markdown to avoid parse errors) ──
  const lines = [];
  lines.push(`📊 Cron Health Report (${todayStr})`);
  lines.push('');
  lines.push(`✅ Healthy: ${healthy.length}/${scoredJobs.length}`);
  lines.push(`⚠️ Degraded: ${degraded.length}${autoDegraded.length > 0 ? ` (auto-disabled ${autoDegraded.length})` : ''}`);
  lines.push(`❌ Failed: ${failed.length}`);
  lines.push(`💰 Tokens (24h): ${formatTokens(totalTokens)}`);
  lines.push(`📈 Runs (24h): ${formatNum(totalRuns)} (✓${formatNum(totalOkRuns)} ✗${formatNum(totalErrorRuns)} ⏭${formatNum(totalSkipped)})`);
  lines.push(`📋 Jobs: ${enabledJobs.length} enabled / ${disabledJobs.length} disabled`);

  if (duplicates.length > 0) {
    lines.push('');
    lines.push(`🔍 Duplicates: ${duplicates.length}`);
    for (const d of duplicates.slice(0, 3)) {
      lines.push(`  • "${d.job1.name}" ↔ "${d.job2.name}" (${d.schedule}, sim=${d.similarity})`);
    }
    if (duplicates.length > 3) {
      lines.push(`  …and ${duplicates.length - 3} more`);
    }
  }

  if (topIssues.length > 0) {
    lines.push('');
    lines.push('📋 Top issues:');
    for (const s of topIssues) {
      const ce = s.job.state?.consecutiveErrors || 0;
      lines.push(`  • ${s.job.name} (score: ${s.score.composite}${ce > 0 ? `, ce=${ce}` : ''})`);
    }
  }

  if (autoDegraded.length > 0) {
    lines.push('');
    lines.push('🛑 Auto-disabled:');
    for (const d of autoDegraded) {
      lines.push(`  • ${d.name} (ce=${d.ce})`);
    }
  }

  const reportText = lines.join('\n');
  console.log('\n' + reportText + '\n');

  // ── Send Telegram ──
  await sendTelegram(reportText);

  // ── Write history ──
  const report = {
    ts:          startMs,
    date:        todayStr,
    totalJobs:   jobs.length,
    enabled:     enabledJobs.length,
    disabled:    disabledJobs.length,
    totalRuns,
    okRuns:      totalOkRuns,
    errorRuns:   totalErrorRuns,
    skippedRuns: totalSkipped,
    totalTokens,
    healthy:     healthy.length,
    degraded:    degraded.length,
    failed:      failed.length,
    autoDegraded: autoDegraded.map(d => ({ id: d.id, name: d.name, ce: d.ce })),
    duplicates:   duplicates.length,
    topIssues:    topIssues.map(s => ({ name: s.job.name, composite: s.score.composite })),
    durationMs:   Date.now() - startMs,
  };

  writeHistory(report);

  console.log('='.repeat(60));
  console.log(`[main] Done in ${Date.now() - startMs}ms`);
  console.log('='.repeat(60));
}

// ── Run ─────────────────────────────────────────────────────────────────────
main().catch(err => {
  console.error('[FATAL]', err);
  process.exit(1);
});
