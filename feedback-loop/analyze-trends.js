#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const STORE_FILE = path.join(__dirname, 'feedback-store.json');

// 分析趨勢
function analyzeTrends() {
  if (!fs.existsSync(STORE_FILE)) {
    console.log('📊 無反饋數據');
    return;
  }
  
  const store = JSON.parse(fs.readFileSync(STORE_FILE, 'utf8'));
  
  console.log('📊 反饋趨勢分析');
  console.log('================');
  console.log(`總反饋數: ${store.length}`);
  
  // 按類型統計
  const typeCount = {};
  store.forEach(e => {
    typeCount[e.type] = (typeCount[e.type] || 0) + 1;
  });
  console.log('\n📈 按類型:');
  Object.entries(typeCount).forEach(([type, count]) => {
    console.log(`  ${type}: ${count}`);
  });
  
  // 按來源統計
  const sourceCount = {};
  store.forEach(e => {
    sourceCount[e.source] = (sourceCount[e.source] || 0) + 1;
  });
  console.log('\n📥 按來源:');
  Object.entries(sourceCount).forEach(([source, count]) => {
    console.log(`  ${source}: ${count}`);
  });
  
  // 成功率
  const success = store.filter(e => e.result === 'success').length;
  console.log(`\n✅ 成功率: ${store.length ? (success / store.length * 100).toFixed(1) : 0}%`);
}

// CLI
const args = process.argv.slice(2);
analyzeTrends();
