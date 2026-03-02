#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const GRAPH_FILE = path.join(__dirname, 'action-graph.json');

// 模擬器
function simulate(actionId, iterations = 3) {
  const data = JSON.parse(fs.readFileSync(GRAPH_FILE, 'utf8'));
  
  console.log(`\n🎮 模擬執行: ${actionId}`);
  console.log('='.repeat(30));
  
  for (let i = 0; i < iterations; i++) {
    // 隨機 reward (-1 到 1)
    const reward = Math.round((Math.random() * 2 - 1) * 100) / 100;
    
    // 找到相關連接
    const connections = data.connections.filter(c => c.from === actionId);
    
    // 更新權重
    connections.forEach(conn => {
      const adjustment = reward * 0.1;
      conn.weight = Math.max(-1, Math.min(1, conn.weight + adjustment));
    });
    
    // 記錄
    data.learning_log.push({
      iteration: i + 1,
      action: actionId,
      reward,
      timestamp: new Date().toISOString()
    });
    
    console.log(`  迭代 ${i+1}: reward = ${reward}`);
  }
  
  fs.writeFileSync(GRAPH_FILE, JSON.stringify(data, null, 2));
  console.log('\n✅ 學習完成，權重已更新');
}

// CLI
const args = process.argv.slice(2);
const action = args[0] || 'send_message';
const iterations = parseInt(args[1]) || 3;

simulate(action, iterations);
