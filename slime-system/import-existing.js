#!/usr/bin/env node
/**
 * 史萊姆系統 - 匯入現有記憶
 * 從 memory/ 目錄匯入資料
 */

const fs = require('fs');
const path = require('path');
const { SlimeAgent } = require('./slime-agent');

const memoryDir = path.join(process.env.HOME, '.openclaw', 'workspace', 'memory');
const slime = new SlimeAgent();

async function importMemories() {
  console.log('📥 開始匯入現有記憶...\n');

  // 讀取所有 markdown 檔案
  const files = fs.readdirSync(memoryDir).filter(f => f.endsWith('.md'));
  
  let imported = 0;
  let skipped = 0;

  for (const file of files) {
    const filePath = path.join(memoryDir, file);
    const content = fs.readFileSync(filePath, 'utf-8');
    
    // 提取標題和日期
    const dateMatch = file.match(/(\d{4}-\d{2}-\d{2})/);
    const date = dateMatch ? dateMatch[1] : file.replace('.md', '');
    
    // 提取標題 (第一行 # 開頭)
    const titleMatch = content.match(/^#\s+(.+)$/m);
    const title = titleMatch ? titleMatch[1] : file.replace('.md', '');
    
    // 跳過 INDEX.md 和太短的文件
    if (file === 'INDEX.md' || content.length < 100) {
      skipped++;
      continue;
    }

    // 匯入為記憶
    try {
      const id = await slime.remember(content.substring(0, 500), {
        source: file,
        date: date,
        title: title,
        type: 'memory-file'
      });
      console.log(`   ✓ ${file}: ${title.substring(0, 30)}...`);
      imported++;
    } catch (e) {
      console.log(`   ✗ ${file}: ${e.message}`);
      skipped++;
    }
  }

  console.log(`\n📊 匯入統計:`);
  console.log(`   成功: ${imported}`);
  console.log(`   跳過: ${skipped}`);

  // 匯入重要 QA
  console.log('\n📚 匯入重要知識 Q&A...');
  
  const qaPairs = [
    ['什麼是 MCP?', 'Model Context Protocol，是代理間溝通的標準協議'],
    ['Kira 是誰?', 'AI OS 的中央治理核心，負責任務分流與 Agent 管理'],
    ['史萊姆系統是做什麼的?', '學習記憶優化系統，包含記憶層、學習機制、進化引擎'],
    ['OpenClaw 是什麼?', '自架 AI 助理平台，類似 Claude Desktop'],
    ['Joe 的技術栈?', 'Node.js, Docker, TypeScript, OpenClaw, ComfyUI, n8n']
  ];

  for (const [q, a] of qaPairs) {
    await slime.learnQA(q, a, { source: 'import', date: '2026-02-27' });
  }
  console.log(`   ✓ ${qaPairs.length} 條 Q&A`);

  // 顯示最終統計
  const health = await slime.healthCheck();
  console.log(`\n💚 系統狀態:`);
  console.log(`   記憶總數: ${health.memories}`);
  console.log(`   Q&A總數: ${health.qa}`);
}

importMemories().then(() => process.exit(0));
