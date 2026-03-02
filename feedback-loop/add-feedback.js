#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const STORE_FILE = path.join(__dirname, 'feedback-store.json');

// 初始化存儲文件
function initStore() {
  if (!fs.existsSync(STORE_FILE)) {
    fs.writeFileSync(STORE_FILE, JSON.stringify([], null, 2));
  }
}

// 新增反饋
function addFeedback(type, source, payload, result) {
  initStore();
  const store = JSON.parse(fs.readFileSync(STORE_FILE, 'utf8'));
  
  const entry = {
    id: `fb_${Date.now()}`,
    timestamp: new Date().toISOString(),
    source,
    type,
    payload,
    result,
    version: '1.0.0'
  };
  
  store.push(entry);
  fs.writeFileSync(STORE_FILE, JSON.stringify(store, null, 2));
  console.log('✅ 新增反饋:', entry.id);
  return entry;
}

// 列出反饋
function listFeedback(limit = 10) {
  initStore();
  const store = JSON.parse(fs.readFileSync(STORE_FILE, 'utf8'));
  console.log(`📋 最近 ${limit} 條反饋:`);
  store.slice(-limit).forEach((entry, i) => {
    console.log(`  ${i+1}. [${entry.type}] ${entry.source} - ${entry.timestamp}`);
  });
}

// CLI
const args = process.argv.slice(2);
if (args[0] === 'add' && args[1]) {
  addFeedback(args[1], args[2] || 'cli', {}, 'pending');
} else if (args[0] === 'list') {
  listFeedback(parseInt(args[1]) || 10);
} else {
  console.log('用法:');
  console.log('  node add-feedback.js add <type> [source]  - 新增反饋');
  console.log('  node add-feedback.js list [limit]         - 列出反饋');
}
