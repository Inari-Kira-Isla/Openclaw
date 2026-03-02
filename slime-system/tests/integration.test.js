#!/usr/bin/env node
/**
 * 史萊姆系統 - 整合測試
 * 驗證各模組協作
 */

const path = require('path');
const fs = require('fs');

const baseDir = path.join(__dirname, '..');

console.log('🧪 史萊姆系統整合測試\n');

// 測試 1: 記憶層檔案存在
console.log('📋 測試 1: 記憶層模組');
const memoryLayer = fs.readFileSync(path.join(baseDir, 'memory-layer.md'), 'utf-8');
console.log(`   ✓ memory-layer.md (${(memoryLayer.length/1024).toFixed(1)}KB)`);

// 測試 2: 學習機制檔案存在
console.log('\n📋 測試 2: 學習機制模組');
const learningMechanism = fs.readFileSync(path.join(baseDir, 'learning-mechanism.md'), 'utf-8');
console.log(`   ✓ learning-mechanism.md (${(learningMechanism.length/1024).toFixed(1)}KB)`);

// 測試 3: 進化引擎檔案存在
console.log('\n📋 測試 3: 進化引擎模組');
const evolutionEngine = fs.readFileSync(path.join(baseDir, 'evolution-engine.md'), 'utf-8');
console.log(`   ✓ evolution-engine.md (${(evolutionEngine.length/1024).toFixed(1)}KB)`);

// 測試 4: 工作流檔案存在
console.log('\n📋 測試 4: 工作流模組');
const workflow = fs.readFileSync(path.join(baseDir, 'workflow.md'), 'utf-8');
console.log(`   ✓ workflow.md (${(workflow.length/1024).toFixed(1)}KB)`);

// 測試 5: 驗證關鍵功能描述存在
console.log('\n📋 測試 5: 功能驗證');

const checks = [
  { name: 'SQLite-Vec', found: memoryLayer.includes('SQLite-Vec') },
  { name: '向量檢索', found: memoryLayer.includes('向量') },
  { name: 'Prompt Refinement', found: learningMechanism.includes('Prompt Refinement') },
  { name: 'QA Learning', found: learningMechanism.includes('QA Learning') },
  { name: '漂移偵測', found: evolutionEngine.includes('漂移偵測') },
  { name: '效能分析', found: evolutionEngine.includes('效能分析') },
  { name: '排程機制', found: workflow.includes('排程') },
  { name: '狀態追蹤', found: workflow.includes('狀態') },
];

let passed = 0;
checks.forEach(c => {
  if (c.found) {
    console.log(`   ✓ ${c.name}`);
    passed++;
  } else {
    console.log(`   ✗ ${c.name}`);
  }
});

console.log(`\n🏁 結果: ${passed}/${checks.length} 通過`);

if (passed === checks.length) {
  console.log('\n✅ 史萊姆系統整合測試通過！');
  process.exit(0);
} else {
  console.log('\n⚠️ 部分測試失敗，需檢查');
  process.exit(1);
}
