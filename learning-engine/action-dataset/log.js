#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const DATASET_FILE = path.join(__dirname, 'dataset.json');

// 初始化
function init() {
  if (!fs.existsSync(DATASET_FILE)) {
    fs.writeFileSync(DATASET_FILE, JSON.stringify({ actions: [], results: [], pairs: [] }, null, 2));
  }
}

// 記錄 Action
function logAction(name, input, output) {
  init();
  const data = JSON.parse(fs.readFileSync(DATASET_FILE, 'utf8'));
  
  const action = {
    id: `action_${Date.now()}`,
    name,
    input,
    output,
    timestamp: new Date().toISOString()
  };
  
  data.actions.push(action);
  fs.writeFileSync(DATASET_FILE, JSON.stringify(data, null, 2));
  console.log('✅ Action 記錄:', action.id, name);
  return action;
}

// 記錄 Result + Reward
function logResult(actionId, success, feedback = {}) {
  init();
  const data = JSON.parse(fs.readFileSync(DATASET_FILE, 'utf8'));
  
  const result = {
    id: `result_${Date.now()}`,
    action_id: actionId,
    success,
    feedback,
    timestamp: new Date().toISOString()
  };
  
  // 計算 reward
  let reward = 0;
  if (success) reward = 1;
  if (feedback.negative) reward = -1;
  result.reward = reward;
  
  data.results.push(result);
  
  // 建立 pair
  data.pairs.push({ action_id: actionId, result_id: result.id, reward });
  
  fs.writeFileSync(DATASET_FILE, JSON.stringify(data, null, 2));
  console.log('✅ Result 記錄:', result.id, 'reward:', reward);
  return result;
}

// CLI
const args = process.argv.slice(2);
if (args[0] === 'action' && args[1]) {
  logAction(args[1], {}, {});
} else if (args[0] === 'result' && args[1]) {
  logResult(args[1], args[2] === 'true');
} else {
  console.log('用法:');
  console.log('  node log-action.js action <name>');
  console.log('  node log-action.js result <action_id> <success>');
}
