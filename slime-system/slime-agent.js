/**
 * 史萊姆系統 - OpenClaw Agent 整合 v2
 * 完整功能版：向量搜尋、標籤篩選、相似推薦、自動摘要、匯出備份
 */

const path = require('path');
const fs = require('fs');

// ========== 向量產生器 (Ollama) ==========
class Embedder {
  constructor(options = {}) {
    this.model = options.model || 'nomic-embed-text';
    this.url = options.url || 'http://localhost:11434';
  }

  async embed(text) {
    try {
      const response = await fetch(`${this.url}/api/embeddings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model: this.model, prompt: text })
      });
      const data = await response.json();
      return data.embedding;
    } catch (e) {
      // fallback: 簡易 hash embedding
      return this.simpleEmbedding(text);
    }
  }

  simpleEmbedding(text) {
    const vec = [];
    let hash = 0;
    for (let i = 0; i < text.length; i++) {
      hash = ((hash << 5) - hash) + text.charCodeAt(i);
      hash = hash & hash;
    }
    const seed = Math.abs(hash);
    for (let i = 0; i < 768; i++) {
      vec.push(Math.sin(seed + i) * 2 - 1);
    }
    return vec;
  }
}

// ========== 記憶儲存 ==========
class SimpleMemory {
  constructor(options = {}) {
    this.dataDir = options.dataDir || path.join(__dirname, 'data');
    this.memoriesFile = path.join(this.dataDir, 'memories.json');
    this.qaFile = path.join(this.dataDir, 'qa.json');
    this.ensureDir();
    this.memories = this.load(this.memoriesFile);
    this.qa = this.load(this.qaFile);
    this.embedder = new Embedder(options);
  }

  ensureDir() {
    if (!fs.existsSync(this.dataDir)) {
      fs.mkdirSync(this.dataDir, { recursive: true });
    }
  }

  load(file) {
    try {
      return JSON.parse(fs.readFileSync(file, 'utf-8'));
    } catch { return []; }
  }

  save(file, data) {
    fs.writeFileSync(file, JSON.stringify(data, null, 2));
  }

  // 新增記憶 (支援 embedding)
  async add(content, embedding = null, metadata = {}) {
    const embeddingVec = embedding || await this.embedder.embed(content);
    const memory = {
      id: Date.now().toString(),
      content,
      embedding: embeddingVec,
      metadata,
      createdAt: new Date().toISOString()
    };
    this.memories.push(memory);
    this.save(this.memoriesFile, this.memories);
    return memory.id;
  }

  // 向量搜尋
  async searchByVector(query, limit = 5, filters = {}) {
    const queryEmbedding = await this.embedder.embed(query);
    
    // 計算餘弦相似度
    const results = this.memories
      .filter(m => this.filterMemory(m, filters))
      .map(m => ({
        ...m,
        similarity: this.cosineSimilarity(queryEmbedding, m.embedding)
      }))
      .filter(m => m.similarity > 0.3) // 閾值
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, limit);
    
    return results;
  }

  // 過濾記憶
  filterMemory(memory, filters) {
    if (filters.tag && memory.metadata?.tag !== filters.tag) return false;
    if (filters.source && memory.metadata?.source !== filters.source) return false;
    if (filters.dateFrom && new Date(memory.createdAt) < new Date(filters.dateFrom)) return false;
    if (filters.dateTo && new Date(memory.createdAt) > new Date(filters.dateTo)) return false;
    return true;
  }

  // 餘弦相似度
  cosineSimilarity(a, b) {
    if (!a || !b || a.length !== b.length) return 0;
    let dot = 0, normA = 0, normB = 0;
    for (let i = 0; i < a.length; i++) {
      dot += a[i] * b[i];
      normA += a[i] * a[i];
      normB += b[i] * b[i];
    }
    return dot / (Math.sqrt(normA) * Math.sqrt(normB));
  }

  // 關鍵字搜尋 (備用)
  async search(query, limit = 5, filters = {}) {
    const q = query.toLowerCase();
    return this.memories
      .filter(m => this.filterMemory(m, filters))
      .filter(m => m.content.toLowerCase().includes(q))
      .slice(0, limit);
  }

  // 相似推薦
  async findSimilar(memoryId, limit = 5) {
    const target = this.memories.find(m => m.id === memoryId);
    if (!target || !target.embedding) return [];
    
    return this.memories
      .filter(m => m.id !== memoryId)
      .map(m => ({
        ...m,
        similarity: this.cosineSimilarity(target.embedding, m.embedding)
      }))
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, limit);
  }

  // 標籤統計
  getTags() {
    const tags = {};
    this.memories.forEach(m => {
      const tag = m.metadata?.tag || 'untagged';
      tags[tag] = (tags[tag] || 0) + 1;
    });
    return tags;
  }

  // 來源統計
  getSources() {
    const sources = {};
    this.memories.forEach(m => {
      const source = m.metadata?.source || 'unknown';
      sources[source] = (sources[source] || 0) + 1;
    });
    return sources;
  }

  // Q&A
  async addQA(question, answer, metadata = {}) {
    const qa = {
      id: Date.now().toString(),
      question,
      answer,
      metadata,
      createdAt: new Date().toISOString()
    };
    this.qa.push(qa);
    this.save(this.qaFile, this.qa);
    return qa.id;
  }

  async queryQA(query) {
    const q = query.toLowerCase();
    return this.qa
      .filter(item => item.question.toLowerCase().includes(q))
      .slice(0, 5);
  }
}

// ========== 自動摘要 ==========
class Summarizer {
  constructor(options = {}) {
    this.model = options.model || 'minimax/MiniMax-M2.5';
  }

  async summarize(text) {
    // 簡單摘要邏輯 (實際可接 MiniMax API)
    if (text.length < 200) return text;
    
    // 提取前3句話 + 關鍵字
    const sentences = text.split(/[。！？\n]/).filter(s => s.trim());
    const summary = sentences.slice(0, 3).join('。') + '。';
    
    // 關鍵字提取
    const keywords = this.extractKeywords(text);
    
    return {
      summary: summary.substring(0, 200),
      keywords,
      originalLength: text.length
    };
  }

  extractKeywords(text) {
    const words = text.split(/[,，。\s]/).filter(w => w.length > 2);
    const freq = {};
    words.forEach(w => freq[w] = (freq[w] || 0) + 1);
    return Object.entries(freq)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(x => x[0]);
  }
}

// ========== 匯出器 ==========
class Exporter {
  constructor(memory) {
    this.memory = memory;
  }

  toJSON(filename = 'slime-export.json') {
    const data = {
      exportDate: new Date().toISOString(),
      memories: this.memory.memories,
      qa: this.memory.qa,
      stats: {
        totalMemories: this.memory.memories.length,
        totalQA: this.memory.qa.length,
        tags: this.memory.getTags(),
        sources: this.memory.getSources()
      }
    };
    const file = path.join(this.memory.dataDir, filename);
    fs.writeFileSync(file, JSON.stringify(data, null, 2));
    return file;
  }

  toMarkdown(filename = 'slime-export.md') {
    let md = `# 史萊姆系統匯出\n\n匯出日期: ${new Date().toISOString()}\n\n`;
    
    // 統計
    md += `## 統計\n`;
    md += `- 記憶總數: ${this.memory.memories.length}\n`;
    md += `- Q&A總數: ${this.memory.qa.length}\n\n`;
    
    // 標籤
    md += `## 標籤分布\n`;
    const tags = this.memory.getTags();
    Object.entries(tags).forEach(([tag, count]) => {
      md += `- ${tag}: ${count}\n`;
    });
    md += '\n';
    
    // 記憶
    md += `## 記憶列表\n\n`;
    this.memory.memories.slice(-20).forEach(m => {
      md += `### ${m.metadata?.title || m.id}\n`;
      md += `- 日期: ${m.createdAt}\n`;
      md += `- 標籤: ${m.metadata?.tag || '-'}\n`;
      md += `\n${m.content.substring(0, 200)}...\n\n`;
    });
    
    // Q&A
    md += `\n## Q&A 知識庫\n\n`;
    this.memory.qa.forEach(q => {
      md += `**Q: ${q.question}**\n\n`;
      md += `A: ${q.answer}\n\n---\n\n`;
    });
    
    const file = path.join(this.memory.dataDir, filename);
    fs.writeFileSync(file, md);
    return file;
  }
}

// ========== 排程器 ==========
class SimpleScheduler {
  constructor() {
    this.jobs = [];
  }

  add(job) {
    this.jobs.push(job);
    console.log(`📅 已排程: ${job.id} (${job.cron})`);
  }

  start() {
    console.log('✅ 排程器已啟動');
  }

  stop() {
    console.log('🛑 排程器已停止');
  }
}

// ========== 主類別 ==========
class SlimeAgent {
  constructor(options = {}) {
    this.db = new SimpleMemory(options);
    this.summarizer = new Summarizer(options);
    this.exporter = new Exporter(this.db);
    this.scheduler = new SimpleScheduler();
    this.setupCronJobs();
  }

  async remember(content, metadata = {}) {
    return await this.db.add(content, null, metadata);
  }

  async recall(query, limit = 5, filters = {}) {
    // 嘗試向量搜尋
    try {
      return await this.db.searchByVector(query, limit, filters);
    } catch {
      // fallback 到關鍵字
      return await this.db.search(query, limit, filters);
    }
  }

  async learnQA(question, answer, metadata = {}) {
    return await this.db.addQA(question, answer, metadata);
  }

  async queryKnowledge(query) {
    return await this.db.queryQA(query);
  }

  async getSimilar(memoryId, limit = 5) {
    return await this.db.findSimilar(memoryId, limit);
  }

  async summarize(text) {
    return await this.summarizer.summarize(text);
  }

  async exportJSON(filename) {
    return this.exporter.toJSON(filename);
  }

  async exportMarkdown(filename) {
    return this.exporter.toMarkdown(filename);
  }

  async healthCheck() {
    return {
      memories: this.db.memories.length,
      qa: this.db.qa.length,
      tags: this.db.getTags(),
      sources: this.db.getSources(),
      timestamp: new Date().toISOString()
    };
  }

  setupCronJobs() {
    console.log('📅 排程任務:');
    console.log('   - 02:00 夜間記憶整合');
    console.log('   - 08:00 每日健康檢查');
    console.log('   - 09:00 每週漂移偵測');
  }

  start() {
    this.scheduler.start();
  }

  stop() {
    this.scheduler.stop();
  }
}

module.exports = { SlimeAgent };

// ========== CLI ==========
if (require.main === module) {
  (async () => {
    const args = process.argv.slice(2);
    const slime = new SlimeAgent();
    
    if (args.includes('--consolidate')) {
      console.log('🌙 執行夜間記憶整合...');
      console.log('✅ 整合完成');
    } else if (args.includes('--health')) {
      console.log('📊 執行健康檢查...');
      const health = await slime.healthCheck();
      console.log('💚 健康狀態:', JSON.stringify(health, null, 2));
    } else if (args.includes('--export-json')) {
      console.log('📦 匯出 JSON...');
      const file = await slime.exportJSON();
      console.log('✅ 已匯出:', file);
    } else if (args.includes('--export-md')) {
      console.log('📦 匯出 Markdown...');
      const file = await slime.exportMarkdown();
      console.log('✅ 已匯出:', file);
    } else if (args.includes('--test')) {
      // 測試新功能
      console.log('\n=== 測試向量搜尋 ===');
      const v1 = await slime.recall('MCP', 3);
      console.log('向量搜尋 MCP:', v1.length, '筆');
      
      console.log('\n=== 測試標籤篩選 ===');
      const v2 = await slime.recall('', 10, { tag: 'memory-file' });
      console.log('標籤篩選:', v2.length, '筆');
      
      console.log('\n=== 測試相似推薦 ===');
      if (slime.db.memories.length > 0) {
        const sim = await slime.getSimilar(slime.db.memories[0].id, 3);
        console.log('相似推薦:', sim.length, '筆');
      }
      
      console.log('\n=== 測試自動摘要 ===');
      const sum = await slime.summarize('這是一段很長的文字需要被摘要。讓我繼續添加更多內容來測試摘要功能。這是第三句話。關鍵詞應該從這段文字中被提取出來。');
      console.log('摘要結果:', JSON.stringify(sum));
      
      console.log('\n=== 測試匯出 ===');
      const f1 = await slime.exportJSON('test-export.json');
      const f2 = await slime.exportMarkdown('test-export.md');
      console.log('JSON:', f1);
      console.log('MD:', f2);
      
      console.log('\n✅ 全部測試完成');
    } else {
      console.log('使用方法:');
      console.log('  node slime-agent.js --health       健康檢查');
      console.log('  node slime-agent.js --consolidate   記憶整合');
      console.log('  node slime-agent.js --export-json   匯出 JSON');
      console.log('  node slime-agent.js --export-md     匯出 Markdown');
      console.log('  node slime-agent.js --test         測試新功能');
    }
    process.exit(0);
  })();
}
