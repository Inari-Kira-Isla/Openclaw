/**
 * feedback-store.js - 儲存反饋記錄模組
 * 提供反饋數據的讀寫操作
 */

const fs = require('fs');
const path = require('path');

const STORE_DIR = path.join(__dirname, 'data');
const STORE_FILE = path.join(STORE_DIR, 'feedback.json');

// 確保數據目錄存在
function ensureStore() {
  if (!fs.existsSync(STORE_DIR)) {
    fs.mkdirSync(STORE_DIR, { recursive: true });
  }
  if (!fs.existsSync(STORE_FILE)) {
    fs.writeFileSync(STORE_FILE, JSON.stringify([], null, 2));
  }
}

// 讀取所有反饋
function readAll() {
  ensureStore();
  const data = fs.readFileSync(STORE_FILE, 'utf-8');
  return JSON.parse(data);
}

// 寫入反饋
function writeAll(feedbackList) {
  ensureStore();
  fs.writeFileSync(STORE_FILE, JSON.stringify(feedbackList, null, 2));
}

// 新增反饋
function add(entry) {
  const list = readAll();
  const newEntry = {
    id: entry.id || `fb_${Date.now()}`,
    timestamp: entry.timestamp || new Date().toISOString(),
    source: entry.source,
    type: entry.type,
    payload: entry.payload,
    version: entry.version || '1.0.0',
    result: entry.result || null
  };
  list.push(newEntry);
  writeAll(list);
  return newEntry;
}

// 根據 ID 查詢
function findById(id) {
  const list = readAll();
  return list.find(f => f.id === id);
}

// 根據版本查詢
function findByVersion(version) {
  const list = readAll();
  return list.filter(f => f.version === version);
}

// 更新反饋結果
function updateResult(id, result) {
  const list = readAll();
  const idx = list.findIndex(f => f.id === id);
  if (idx !== -1) {
    list[idx].result = result;
    writeAll(list);
    return list[idx];
  }
  return null;
}

// 刪除反饋
function remove(id) {
  const list = readAll();
  const newList = list.filter(f => f.id !== id);
  writeAll(newList);
  return newList.length < list.length;
}

module.exports = {
  readAll,
  add,
  findById,
  findByVersion,
  updateResult,
  remove
};
