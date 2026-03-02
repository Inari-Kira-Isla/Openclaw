/**
 * analytics.js - 分析反饋趨勢模組
 * 提供反饋數據的統計與趨勢分析
 */

const store = require('./feedback-store');
const versionMgr = require('./version-manager');

// 統計各類型的反饋數量
function countByType() {
  const all = store.readAll();
  const counts = {};
  all.forEach(f => {
    counts[f.type] = (counts[f.type] || 0) + 1;
  });
  return counts;
}

// 統計各來源的數量
function countBySource() {
  const all = store.readAll();
  const counts = {};
  all.forEach(f => {
    counts[f.source] = (counts[f.source] || 0) + 1;
  });
  return counts;
}

// 統計各版本的數量
function countByVersion() {
  const all = store.readAll();
  const counts = {};
  all.forEach(f => {
    counts[f.version] = (counts[f.version] || 0) + 1;
  });
  return counts;
}

// 每日反饋數量趨勢
function dailyTrend(days = 7) {
  const all = store.readAll();
  const now = new Date();
  const trend = {};
  
  for (let i = 0; i < days; i++) {
    const date = new Date(now);
    date.setDate(date.getDate() - i);
    const key = date.toISOString().split('T')[0];
    trend[key] = 0;
  }
  
  all.forEach(f => {
    const date = f.timestamp.split('T')[0];
    if (trend[date] !== undefined) {
      trend[date]++;
    }
  });
  
  return trend;
}

// 計算解決率
function resolutionRate() {
  const all = store.readAll();
  if (all.length === 0) return { resolved: 0, pending: 0, rate: 0 };
  
  const resolved = all.filter(f => f.result && f.result.status === 'resolved').length;
  const pending = all.length - resolved;
  
  return {
    resolved,
    pending,
    rate: Math.round((resolved / all.length) * 100)
  };
}

// 獲取摘要統計
function getSummary() {
  const all = store.readAll();
  return {
    total: all.length,
    byType: countByType(),
    bySource: countBySource(),
    byVersion: countByVersion(),
    dailyTrend: dailyTrend(),
    resolution: resolutionRate(),
    versions: versionMgr.getAllVersions()
  };
}

module.exports = {
  countByType,
  countBySource,
  countByVersion,
  dailyTrend,
  resolutionRate,
  getSummary
};
