/**
 * 共享知識庫 API
 * Shared Knowledge Base API
 * 
 * 提供統一的讀寫介面給 Kira & Isla 兩系統使用
 */

const fs = require('fs');
const path = require('path');

const BASE_DIR = path.dirname(__filename);

/**
 * 讀取知識庫索引
 */
function getIndex() {
  const indexPath = path.join(BASE_DIR, 'index.json');
  return JSON.parse(fs.readFileSync(indexPath, 'utf-8'));
}

/**
 * 更新知識庫索引
 */
function updateIndex(data) {
  const indexPath = path.join(BASE_DIR, 'index.json');
  fs.writeFileSync(indexPath, JSON.stringify(data, null, 2));
}

/**
 * 更新狀態
 */
function updateStatus(data) {
  const statusPath = path.join(BASE_DIR, 'status.json');
  const current = JSON.parse(fs.readFileSync(statusPath, 'utf-8'));
  const updated = { ...current, ...data };
  fs.writeFileSync(statusPath, JSON.stringify(updated, null, 2));
  return updated;
}

/**
 * 讀取狀態
 */
function getStatus() {
  const statusPath = path.join(BASE_DIR, 'status.json');
  return JSON.parse(fs.readFileSync(statusPath, 'utf-8'));
}

/**
 * 列出所有知識
 */
function listKnowledge() {
  const knowledgeDir = path.join(BASE_DIR, 'knowledge');
  const discussionsDir = path.join(BASE_DIR, 'discussions');
  
  const files = {
    knowledge: [],
    discussions: []
  };
  
  // 掃描 knowledge 目錄
  if (fs.existsSync(knowledgeDir)) {
    fs.readdirSync(knowledgeDir).forEach(file => {
      if (file.endsWith('.md')) {
        files.knowledge.push(file);
      }
    });
  }
  
  // 掃描 discussions 目錄
  if (fs.existsSync(discussionsDir)) {
    const dateDirs = fs.readdirSync(discussionsDir);
    dateDirs.forEach(date => {
      const datePath = path.join(discussionsDir, date);
      if (fs.statSync(datePath).isDirectory()) {
        fs.readdirSync(datePath).forEach(file => {
          if (file.endsWith('.md')) {
            files.discussions.push(`${date}/${file}`);
          }
        });
      }
    });
  }
  
  return files;
}

/**
 * 讀取知識
 */
function readKnowledge(type, filePath) {
  let fullPath;
  
  if (type === 'knowledge') {
    fullPath = path.join(BASE_DIR, 'knowledge', filePath);
  } else if (type === 'discussion') {
    fullPath = path.join(BASE_DIR, 'discussions', filePath);
  } else {
    throw new Error('Invalid type: use "knowledge" or "discussion"');
  }
  
  if (!fs.existsSync(fullPath)) {
    throw new Error(`File not found: ${filePath}`);
  }
  
  return fs.readFileSync(fullPath, 'utf-8');
}

/**
 * 寫入知識
 */
function writeKnowledge(type, filePath, content, agent = 'unknown') {
  let fullPath;
  let dirPath;
  
  if (type === 'knowledge') {
    dirPath = path.join(BASE_DIR, 'knowledge');
    fullPath = path.join(dirPath, filePath);
  } else if (type === 'discussion') {
    // 自動建立日期目錄
    const date = new Date().toISOString().slice(0, 10);
    dirPath = path.join(BASE_DIR, 'discussions', date);
    fullPath = path.join(dirPath, filePath);
  } else {
    throw new Error('Invalid type: use "knowledge" or "discussion"');
  }
  
  // 建立目錄
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
  
  // 寫入檔案
  fs.writeFileSync(fullPath, content);
  
  // 更新狀態
  const status = getStatus();
  status.lastSync = new Date().toISOString();
  status.totalKnowledge = listKnowledge().knowledge.length;
  status.totalDiscussions = listKnowledge().discussions.length;
  status.agents[agent] = {
    lastAccess: new Date().toISOString(),
    contributions: (status.agents[agent]?.contributions || 0) + 1
  };
  updateStatus(status);
  
  return { success: true, path: fullPath };
}

/**
 * 搜尋知識
 */
function searchKnowledge(keyword) {
  const files = listKnowledge();
  const results = [];
  
  const searchInFile = (type, filePath) => {
    const content = readKnowledge(type, filePath);
    if (content.toLowerCase().includes(keyword.toLowerCase())) {
      results.push({ type, file: filePath });
    }
  };
  
  files.knowledge.forEach(f => searchInFile('knowledge', f));
  files.discussions.forEach(f => searchInFile('discussion', f));
  
  return results;
}

// 命令列介面
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  
  switch (command) {
    case 'list':
      console.log(JSON.stringify(listKnowledge(), null, 2));
      break;
    case 'read':
      console.log(readKnowledge(args[1], args[2]));
      break;
    case 'write':
      console.log(writeKnowledge(args[1], args[2], args[3], args[4] || 'cli'));
      break;
    case 'search':
      console.log(JSON.stringify(searchKnowledge(args[1]), null, 2));
      break;
    case 'status':
      console.log(JSON.stringify(getStatus(), null, 2));
      break;
    default:
      console.log('Usage:');
      console.log('  node api.js list');
      console.log('  node api.js read <type> <file>');
      console.log('  node api.js write <type> <file> <content> [agent]');
      console.log('  node api.js search <keyword>');
      console.log('  node api.js status');
  }
}

module.exports = {
  getIndex,
  updateIndex,
  getStatus,
  updateStatus,
  listKnowledge,
  readKnowledge,
  writeKnowledge,
  searchKnowledge
};
