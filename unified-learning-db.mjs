/**
 * Unified Learning Database
 * 統一學習數據庫腳本
 * 
 * 功能：
 * 1. 統一管理所有學習數據（錯誤記錄、效能數據、用戶反饋）
 * 2. 提供 CRUD 操作介面
 * 3. 儲存為 JSON 格式
 * 4. 支援查詢和分析
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 數據庫路徑
const DB_PATH = join(__dirname, 'data', 'learning-db.json');

// 確保數據目錄存在
function ensureDbDir() {
  const dir = dirname(DB_PATH);
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
}

// 讀取數據庫
function readDb() {
  ensureDbDir();
  if (!existsSync(DB_PATH)) {
    return {
      errors: [],
      performance: [],
      feedback: [],
      skills: [],
      prompts: [],
      metadata: {
        created: new Date().toISOString(),
        updated: new Date().toISOString(),
        version: '1.0.0'
      }
    };
  }
  try {
    return JSON.parse(readFileSync(DB_PATH, 'utf-8'));
  } catch (e) {
    console.error('Error reading DB:', e);
    return { errors: [], performance: [], feedback: [], skills: [], prompts: [], metadata: { created: new Date().toISOString(), updated: new Date().toISOString(), version: '1.0.0' } };
  }
}

// 寫入數據庫
function writeDb(data) {
  ensureDbDir();
  data.metadata.updated = new Date().toISOString();
  writeFileSync(DB_PATH, JSON.stringify(data, null, 2), 'utf-8');
}

// ============ CRUD 操作 ============

// 錯誤記錄 CRUD
export const errors = {
  add(error) {
    const db = readDb();
    const record = {
      id: `err_${Date.now()}`,
      timestamp: new Date().toISOString(),
      ...error
    };
    db.errors.unshift(record);
    if (db.errors.length > 1000) db.errors = db.errors.slice(0, 1000);
    writeDb(db);
    return record;
  },
  
  list(limit = 50, filter = {}) {
    const db = readDb();
    let results = db.errors;
    if (filter.type) results = results.filter(e => e.type === filter.type);
    if (filter.severity) results = results.filter(e => e.severity === filter.severity);
    if (filter.skill) results = results.filter(e => e.skill === filter.skill);
    return results.slice(0, limit);
  },
  
  get(id) {
    const db = readDb();
    return db.errors.find(e => e.id === id);
  },
  
  update(id, updates) {
    const db = readDb();
    const idx = db.errors.findIndex(e => e.id === id);
    if (idx === -1) return null;
    db.errors[idx] = { ...db.errors[idx], ...updates, updated: new Date().toISOString() };
    writeDb(db);
    return db.errors[idx];
  },
  
  delete(id) {
    const db = readDb();
    const idx = db.errors.findIndex(e => e.id === id);
    if (idx === -1) return false;
    db.errors.splice(idx, 1);
    writeDb(db);
    return true;
  },
  
  stats() {
    const db = readDb();
    const now = Date.now();
    const day = 86400000;
    return {
      total: db.errors.length,
      last24h: db.errors.filter(e => now - new Date(e.timestamp).getTime() < day).length,
      byType: db.errors.reduce((acc, e) => { acc[e.type] = (acc[e.type] || 0) + 1; return acc; }, {}),
      bySeverity: db.errors.reduce((acc, e) => { acc[e.severity] = (acc[e.severity] || 0) + 1; return acc; }, {})
    };
  }
};

// 效能數據 CRUD
export const performance = {
  add(data) {
    const db = readDb();
    const record = {
      id: `perf_${Date.now()}`,
      timestamp: new Date().toISOString(),
      ...data
    };
    db.performance.unshift(record);
    if (db.performance.length > 1000) db.performance = db.performance.slice(0, 1000);
    writeDb(db);
    return record;
  },
  
  list(limit = 50, filter = {}) {
    const db = readDb();
    let results = db.performance;
    if (filter.metric) results = results.filter(p => p.metric === filter.metric);
    if (filter.agent) results = results.filter(p => p.agent === filter.agent);
    return results.slice(0, limit);
  },
  
  get(id) {
    const db = readDb();
    return db.performance.find(p => p.id === id);
  },
  
  delete(id) {
    const db = readDb();
    const idx = db.performance.findIndex(p => p.id === id);
    if (idx === -1) return false;
    db.performance.splice(idx, 1);
    writeDb(db);
    return true;
  },
  
  stats() {
    const db = readDb();
    if (db.performance.length === 0) return { total: 0, avg: {} };
    const byMetric = {};
    db.performance.forEach(p => {
      if (!byMetric[p.metric]) byMetric[p.metric] = [];
      if (typeof p.value === 'number') byMetric[p.metric].push(p.value);
    });
    const avg = {};
    for (const m in byMetric) {
      avg[m] = byMetric[m].reduce((a, b) => a + b, 0) / byMetric[m].length;
    }
    return { total: db.performance.length, avg, count: Object.keys(byMetric).length };
  }
};

// 用戶反饋 CRUD
export const feedback = {
  add(feedback) {
    const db = readDb();
    const record = {
      id: `fb_${Date.now()}`,
      timestamp: new Date().toISOString(),
      ...feedback
    };
    db.feedback.unshift(record);
    if (db.feedback.length > 1000) db.feedback = db.feedback.slice(0, 1000);
    writeDb(db);
    return record;
  },
  
  list(limit = 50, filter = {}) {
    const db = readDb();
    let results = db.feedback;
    if (filter.type) results = results.filter(f => f.type === filter.type);
    if (filter.sentiment) results = results.filter(f => f.sentiment === filter.sentiment);
    if (filter.source) results = results.filter(f => f.source === filter.source);
    return results.slice(0, limit);
  },
  
  get(id) {
    const db = readDb();
    return db.feedback.find(f => f.id === id);
  },
  
  update(id, updates) {
    const db = readDb();
    const idx = db.feedback.findIndex(f => f.id === id);
    if (idx === -1) return null;
    db.feedback[idx] = { ...db.feedback[idx], ...updates };
    writeDb(db);
    return db.feedback[idx];
  },
  
  delete(id) {
    const db = readDb();
    const idx = db.feedback.findIndex(f => f.id === id);
    if (idx === -1) return false;
    db.feedback.splice(idx, 1);
    writeDb(db);
    return true;
  },
  
  stats() {
    const db = readDb();
    return {
      total: db.feedback.length,
      byType: db.feedback.reduce((acc, f) => { acc[f.type] = (acc[f.type] || 0) + 1; return acc; }, {}),
      bySentiment: db.feedback.reduce((acc, f) => { acc[f.sentiment] = (acc[f.sentiment] || 0) + 1; return acc; }, {})
    };
  }
};

// 技能學習 CRUD
export const skills = {
  add(skill) {
    const db = readDb();
    const record = {
      id: `skill_${Date.now()}`,
      timestamp: new Date().toISOString(),
      ...skill
    };
    db.skills.unshift(record);
    writeDb(db);
    return record;
  },
  
  list(limit = 50) {
    const db = readDb();
    return db.skills.slice(0, limit);
  },
  
  get(id) {
    const db = readDb();
    return db.skills.find(s => s.id === id);
  },
  
  update(id, updates) {
    const db = readDb();
    const idx = db.skills.findIndex(s => s.id === id);
    if (idx === -1) return null;
    db.skills[idx] = { ...db.skills[idx], ...updates };
    writeDb(db);
    return db.skills[idx];
  },
  
  delete(id) {
    const db = readDb();
    const idx = db.skills.findIndex(s => s.id === id);
    if (idx === -1) return false;
    db.skills.splice(idx, 1);
    writeDb(db);
    return true;
  }
};

// Prompt 學習 CRUD
export const prompts = {
  add(prompt) {
    const db = readDb();
    const record = {
      id: `prompt_${Date.now()}`,
      timestamp: new Date().toISOString(),
      ...prompt
    };
    db.prompts.unshift(record);
    writeDb(db);
    return record;
  },
  
  list(limit = 50) {
    const db = readDb();
    return db.prompts.slice(0, limit);
  },
  
  search(query) {
    const db = readDb();
    const q = query.toLowerCase();
    return db.prompts.filter(p => 
      (p.name && p.name.toLowerCase().includes(q)) ||
      (p.content && p.content.toLowerCase().includes(q)) ||
      (p.tags && p.tags.some(t => t.toLowerCase().includes(q)))
    );
  },
  
  delete(id) {
    const db = readDb();
    const idx = db.prompts.findIndex(p => p.id === id);
    if (idx === -1) return false;
    db.prompts.splice(idx, 1);
    writeDb(db);
    return true;
  }
};

// ============ 通用查詢 ============

export const query = {
  // 搜尋所有數據
  search(type, text) {
    const db = readDb();
    const q = text.toLowerCase();
    if (type && type !== 'all') {
      return db[type]?.filter(item => 
        JSON.stringify(item).toLowerCase().includes(q)
      ) || [];
    }
    // 搜尋所有類型
    return {
      errors: db.errors.filter(e => JSON.stringify(e).toLowerCase().includes(q)),
      performance: db.performance.filter(p => JSON.stringify(p).toLowerCase().includes(q)),
      feedback: db.feedback.filter(f => JSON.stringify(f).toLowerCase().includes(q)),
      skills: db.skills.filter(s => JSON.stringify(s).toLowerCase().includes(q)),
      prompts: db.prompts.filter(p => JSON.stringify(p).toLowerCase().includes(q))
    };
  },
  
  // 獲取所有數據
  all() {
    return readDb();
  },
  
  // 獲取摘要
  summary() {
    const db = readDb();
    return {
      errors: db.errors.length,
      performance: db.performance.length,
      feedback: db.feedback.length,
      skills: db.skills.length,
      prompts: db.prompts.length,
      lastUpdated: db.metadata.updated
    };
  },
  
  // 導出數據
  export(format = 'json') {
    const db = readDb();
    if (format === 'json') {
      return JSON.stringify(db, null, 2);
    }
    return db;
  },
  
  // 導入數據
  import(data) {
    const db = readDb();
    const newData = typeof data === 'string' ? JSON.parse(data) : data;
    // 合併數據
    if (newData.errors) db.errors = [...newData.errors, ...db.errors].slice(0, 1000);
    if (newData.performance) db.performance = [...newData.performance, ...db.performance].slice(0, 1000);
    if (newData.feedback) db.feedback = [...newData.feedback, ...db.feedback].slice(0, 1000);
    if (newData.skills) db.skills = [...newData.skills, ...db.skills];
    if (newData.prompts) db.prompts = [...newData.prompts, ...db.prompts];
    writeDb(db);
    return db;
  }
};

// ============ CLI 入口 ============

if (import.meta.url === `file://${process.argv[1]}`) {
  const cmd = process.argv[2];
  const args = process.argv.slice(3);
  
  const usage = `
Usage: node unified-learning-db.mjs <command> [options]

Commands:
  add-error <type> <message> [severity]
  list-errors [limit] [type]
  error-stats
  
  add-perf <metric> <value> [agent]
  list-perf [limit]
  
  add-feedback <type> <message> [sentiment]
  list-feedback [limit]
  feedback-stats
  
  add-skill <name> <description>
  list-skills
  search-prompts <query>
  
  search <text>
  summary
  export
  import <file>
  
Examples:
  node unified-learning-db.mjs add-error "validation" "Invalid input" "high"
  node unified-learning-db.mjs list-errors 20
  node unified-learning-db.mjs error-stats
  node unified-learning-db.mjs add-perf "response_time" 250 "kira"
  node unified-learning-db.mjs add-feedback "bug" "Button not working" "negative"
  node unified-learning-db.mjs summary
  `;
  
  try {
    switch (cmd) {
      case 'add-error': {
        const [type, message, severity = 'medium'] = args;
        const result = errors.add({ type, message, severity });
        console.log('Added error:', result.id);
        break;
      }
      case 'list-errors': {
        const [limit = 50, type] = args;
        const filter = type ? { type } : {};
        console.log(JSON.stringify(errors.list(parseInt(limit), filter), null, 2));
        break;
      }
      case 'error-stats':
        console.log(JSON.stringify(errors.stats(), null, 2));
        break;
        
      case 'add-perf': {
        const [metric, value, agent] = args;
        const result = performance.add({ metric, value: parseFloat(value), agent });
        console.log('Added performance:', result.id);
        break;
      }
      case 'list-perf': {
        const [limit = 50] = args;
        console.log(JSON.stringify(performance.list(parseInt(limit)), null, 2));
        break;
      }
        
      case 'add-feedback': {
        const [type, message, sentiment = 'neutral'] = args;
        const result = feedback.add({ type, message, sentiment });
        console.log('Added feedback:', result.id);
        break;
      }
      case 'list-feedback': {
        const [limit = 50] = args;
        console.log(JSON.stringify(feedback.list(parseInt(limit)), null, 2));
        break;
      }
      case 'feedback-stats':
        console.log(JSON.stringify(feedback.stats(), null, 2));
        break;
        
      case 'add-skill': {
        const [name, description] = args;
        const result = skills.add({ name, description });
        console.log('Added skill:', result.id);
        break;
      }
      case 'list-skills': {
        const [limit = 50] = args;
        console.log(JSON.stringify(skills.list(parseInt(limit)), null, 2));
        break;
      }
      case 'search-prompts': {
        const [queryText] = args;
        console.log(JSON.stringify(prompts.search(queryText), null, 2));
        break;
      }
        
      case 'search': {
        const [text] = args;
        console.log(JSON.stringify(query.search('all', text), null, 2));
        break;
      }
      case 'summary':
        console.log(JSON.stringify(query.summary(), null, 2));
        break;
      case 'export':
        console.log(query.export());
        break;
        
      default:
        console.log(usage);
    }
  } catch (e) {
    console.error('Error:', e.message);
    console.log(usage);
  }
}

export default { errors, performance, feedback, skills, prompts, query };
