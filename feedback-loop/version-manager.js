/**
 * version-manager.js - 版本控制模組
 * 管理反饋的版本追蹤
 */

const fs = require('fs');
const path = require('path');

const VERSIONS_FILE = path.join(__dirname, 'data', 'versions.json');

function ensureVersions() {
  const dir = path.dirname(VERSIONS_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  if (!fs.existsSync(VERSIONS_FILE)) {
    fs.writeFileSync(VERSIONS_FILE, JSON.stringify({}, null, 2));
  }
}

function readVersions() {
  ensureVersions();
  return JSON.parse(fs.readFileSync(VERSIONS_FILE, 'utf-8'));
}

function writeVersions(versions) {
  ensureVersions();
  fs.writeFileSync(VERSIONS_FILE, JSON.stringify(versions, null, 2));
}

// 獲取所有版本
function getAllVersions() {
  const versions = readVersions();
  return Object.keys(versions).sort();
}

// 創建新版本
function createVersion(version, metadata = {}) {
  const versions = readVersions();
  if (versions[version]) {
    return { created: false, version };
  }
  versions[version] = {
    created: new Date().toISOString(),
    metadata,
    feedbackCount: 0
  };
  writeVersions(versions);
  return { created: true, version };
}

// 獲取版本詳情
function getVersion(version) {
  const versions = readVersions();
  return versions[version] || null;
}

// 更新版本反饋計數
function incrementFeedbackCount(version) {
  const versions = readVersions();
  if (versions[version]) {
    versions[version].feedbackCount = (versions[version].feedbackCount || 0) + 1;
    writeVersions(versions);
  }
}

// 解析版本號 (如 1.2.3 -> { major: 1, minor: 2, patch: 3 })
function parseVersion(version) {
  const parts = version.split('.').map(Number);
  return {
    major: parts[0] || 0,
    minor: parts[1] || 0,
    patch: parts[2] || 0
  };
}

// 比較版本
function compareVersions(v1, v2) {
  const p1 = parseVersion(v1);
  const p2 = parseVersion(v2);
  
  if (p1.major !== p2.major) return p1.major - p2.major;
  if (p1.minor !== p2.minor) return p1.minor - p2.minor;
  return p1.patch - p2.patch;
}

// 獲取最新版本
function getLatestVersion() {
  const versions = getAllVersions();
  if (versions.length === 0) return null;
  return versions.sort(compareVersions).pop();
}

module.exports = {
  getAllVersions,
  createVersion,
  getVersion,
  incrementFeedbackCount,
  parseVersion,
  compareVersions,
  getLatestVersion
};
