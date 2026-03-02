/**
 * 史萊姆系統 - 記憶層資料庫實作
 * SQLite-Vec 向量資料庫
 * 
 * 支援:
 * - 768維向量儲存與檢索
 * - Cosine 相似度搜尋
 * - 文字記憶管理
 */

const Database = require('better-sqlite3');
const vec = require('sqlite-vec');
const path = require('path');
const fs = require('fs');

class MemoryDB {
  constructor(dbPath = null) {
    this.dbPath = dbPath || path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'workspace', 'slime-system', 'data', 'memory.db');
    this.db = null;
    this.embeddingDim = 768;
  }

  /**
   * 初始化資料庫連接與表結構
   */
  initialize() {
    // 確保目錄存在
    const dir = path.dirname(this.dbPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    // 建立資料庫連接
    this.db = new Database(this.dbPath);
    this.db.pragma('journal_mode = WAL');
    
    // 加載 sqlite-vec 擴展
    const vecExt = require('sqlite-vec');
    const vecPath = vecExt.getLoadablePath();
    this.db.loadExtension(vecPath);

    // 建立表結構
    this._createTables();
    
    console.log(`[MemoryDB] Initialized at ${this.dbPath}`);
    return this;
  }

  /**
   * 建立資料表
   */
  _createTables() {
    // 向量記憶表
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS memory_vectors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chunk_id TEXT UNIQUE NOT NULL,
        content TEXT NOT NULL,
        embedding BLOB NOT NULL,
        metadata TEXT DEFAULT '{}',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);

    // 文字記憶表
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS memory_text (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        tags TEXT DEFAULT '[]',
        type TEXT DEFAULT 'general',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);

    // 向量索引表 (使用 sqlite-vec)
    this.db.exec(`
      CREATE VIRTUAL TABLE IF NOT EXISTS memory_vec_idx USING vec0(
        embedding FLOAT[768],
        chunk_id TEXT UNIQUE
      )
    `);

    // 建立索引
    this.db.exec(`
      CREATE INDEX IF NOT EXISTS idx_vectors_chunk_id ON memory_vectors(chunk_id);
      CREATE INDEX IF NOT EXISTS idx_vectors_created ON memory_vectors(created_at);
      CREATE INDEX IF NOT EXISTS idx_text_tags ON memory_text(tags);
      CREATE INDEX IF NOT EXISTS idx_text_type ON memory_text(type);
    `);
  }

  /**
   * 新增記憶 (向量)
   * @param {string} content - 記憶內容
   * @param {number[]} embedding - 768維向量
   * @param {object} metadata - 元數據
   * @returns {object} 新增的記錄
   */
  addMemory(content, embedding, metadata = {}) {
    const chunkId = metadata.chunk_id || `mem_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    // 驗證向量維度
    if (embedding.length !== this.embeddingDim) {
      throw new Error(`向量維度必須為 ${this.embeddingDim}，當前為 ${embedding.length}`);
    }

    // 將向量轉換為 Float32Array 並轉為 Buffer
    const embeddingBuffer = Buffer.from(new Float32Array(embedding).buffer);

    const insertVector = this.db.prepare(`
      INSERT INTO memory_vectors (chunk_id, content, embedding, metadata)
      VALUES (?, ?, ?, ?)
    `);

    const insertVecIdx = this.db.prepare(`
      INSERT INTO memory_vec_idx (embedding, chunk_id)
      VALUES (?, ?)
    `);

    const transaction = this.db.transaction(() => {
      insertVector.run(chunkId, content, embeddingBuffer, JSON.stringify(metadata));
      insertVecIdx.run(embeddingBuffer, chunkId);
    });

    transaction();

    return this.getMemoryByChunkId(chunkId);
  }

  /**
   * 新增文字記憶
   * @param {string} content - 記憶內容
   * @param {string[]} tags - 標籤陣列
   * @param {string} type - 類型
   * @returns {object} 新增的記錄
   */
  addTextMemory(content, tags = [], type = 'general') {
    const insert = this.db.prepare(`
      INSERT INTO memory_text (content, tags, type)
      VALUES (?, ?, ?)
    `);

    const result = insert.run(content, JSON.stringify(tags), type);
    
    return this.getTextMemory(result.lastInsertRowid);
  }

  /**
   * 搜尋向量記憶
   * @param {number[]} queryEmbedding - 查詢向量
   * @param {number} limit - 返回數量上限
   * @param {object} filters - 過濾條件 (可選)
   * @returns {array} 搜尋結果
   */
  searchMemory(queryEmbedding, limit = 5, filters = {}) {
    // 驗證向量維度
    if (queryEmbedding.length !== this.embeddingDim) {
      throw new Error(`向量維度必須為 ${this.embeddingDim}，當前為 ${queryEmbedding.length}`);
    }

    const queryBuffer = Buffer.from(new Float32Array(queryEmbedding).buffer);

    // 使用 sqlite-vec 進行向量搜尋 (cosine 相似度)
    const results = this.db.prepare(`
      SELECT 
        mv.chunk_id,
        mv.content,
        mv.metadata,
        mv.created_at,
        mv.updated_at,
        distance
      FROM memory_vec_idx
      JOIN memory_vectors mv ON memory_vec_idx.chunk_id = mv.chunk_id
      WHERE embedding MATCH ?
      ORDER BY distance ASC
      LIMIT ?
    `).all(queryBuffer, limit);

    // 轉換結果格式
    return results.map(row => ({
      chunk_id: row.chunk_id,
      content: row.content,
      metadata: JSON.parse(row.metadata || '{}'),
      created_at: row.created_at,
      updated_at: row.updated_at,
      similarity: 1 - row.distance // 轉換距離為相似度
    }));
  }

  /**
   * 根據 ID 獲取向量記憶
   * @param {number} id - 記錄 ID
   * @returns {object|null} 記錄或 null
   */
  getMemory(id) {
    const row = this.db.prepare(`
      SELECT * FROM memory_vectors WHERE id = ?
    `).get(id);

    if (!row) return null;

    return {
      id: row.id,
      chunk_id: row.chunk_id,
      content: row.content,
      embedding: Array.from(new Float32Array(row.embedding.buffer)),
      metadata: JSON.parse(row.metadata || '{}'),
      created_at: row.created_at,
      updated_at: row.updated_at
    };
  }

  /**
   * 根據 chunk_id 獲取記憶
   * @param {string} chunkId - 區塊 ID
   * @returns {object|null} 記錄或 null
   */
  getMemoryByChunkId(chunkId) {
    const row = this.db.prepare(`
      SELECT * FROM memory_vectors WHERE chunk_id = ?
    `).get(chunkId);

    if (!row) return null;

    return {
      id: row.id,
      chunk_id: row.chunk_id,
      content: row.content,
      embedding: Array.from(new Float32Array(row.embedding.buffer)),
      metadata: JSON.parse(row.metadata || '{}'),
      created_at: row.created_at,
      updated_at: row.updated_at
    };
  }

  /**
   * 根據 ID 獲取文字記憶
   * @param {number} id - 記錄 ID
   * @returns {object|null} 記錄或 null
   */
  getTextMemory(id) {
    const row = this.db.prepare(`
      SELECT * FROM memory_text WHERE id = ?
    `).get(id);

    if (!row) return null;

    return {
      id: row.id,
      content: row.content,
      tags: JSON.parse(row.tags || '[]'),
      type: row.type,
      created_at: row.created_at,
      updated_at: row.updated_at
    };
  }

  /**
   * 刪除向量記憶
   * @param {number} id - 記錄 ID
   * @returns {boolean} 是否成功刪除
   */
  deleteMemory(id) {
    const memory = this.getMemory(id);
    if (!memory) return false;

    // 從向量索引表刪除
    this.db.prepare(`
      DELETE FROM memory_vec_idx WHERE chunk_id = ?
    `).run(memory.chunk_id);

    // 從向量表刪除
    this.db.prepare(`
      DELETE FROM memory_vectors WHERE id = ?
    `).run(id);

    return true;
  }

  /**
   * 根據 chunk_id 刪除記憶
   * @param {string} chunkId - 區塊 ID
   * @returns {boolean} 是否成功刪除
   */
  deleteMemoryByChunkId(chunkId) {
    // 從向量索引表刪除
    this.db.prepare(`
      DELETE FROM memory_vec_idx WHERE chunk_id = ?
    `).run(chunkId);

    // 從向量表刪除
    const result = this.db.prepare(`
      DELETE FROM memory_vectors WHERE chunk_id = ?
    `).run(chunkId);

    return result.changes > 0;
  }

  /**
   * 刪除文字記憶
   * @param {number} id - 記錄 ID
   * @returns {boolean} 是否成功刪除
   */
  deleteTextMemory(id) {
    const result = this.db.prepare(`
      DELETE FROM memory_text WHERE id = ?
    `).run(id);

    return result.changes > 0;
  }

  /**
   * 更新記憶內容
   * @param {number} id - 記錄 ID
   * @param {string} content - 新內容
   * @param {object} metadata - 新元數據
   * @returns {object|null} 更新後的記錄
   */
  updateMemory(id, content, metadata = {}) {
    const existing = this.getMemory(id);
    if (!existing) return null;

    this.db.prepare(`
      UPDATE memory_vectors 
      SET content = ?, metadata = ?, updated_at = CURRENT_TIMESTAMP
      WHERE id = ?
    `).run(content, JSON.stringify(metadata), id);

    return this.getMemory(id);
  }

  /**
   * 更新文字記憶
   * @param {number} id - 記錄 ID
   * @param {string} content - 新內容
   * @param {string[]} tags - 新標籤
   * @param {string} type - 新類型
   * @returns {object|null} 更新後的記錄
   */
  updateTextMemory(id, content, tags = null, type = null) {
    const existing = this.getTextMemory(id);
    if (!existing) return null;

    const newTags = tags !== null ? JSON.stringify(tags) : existing.tags;
    const newType = type !== null ? type : existing.type;

    this.db.prepare(`
      UPDATE memory_text 
      SET content = ?, tags = ?, type = ?, updated_at = CURRENT_TIMESTAMP
      WHERE id = ?
    `).run(content, newTags, newType, id);

    return this.getTextMemory(id);
  }

  /**
   * 列出所有向量記憶
   * @param {number} limit - 返回數量
   * @param {number} offset - 偏移量
   * @returns {array} 記錄列表
   */
  listMemories(limit = 50, offset = 0) {
    const rows = this.db.prepare(`
      SELECT id, chunk_id, content, metadata, created_at, updated_at
      FROM memory_vectors
      ORDER BY created_at DESC
      LIMIT ? OFFSET ?
    `).all(limit, offset);

    return rows.map(row => ({
      id: row.id,
      chunk_id: row.chunk_id,
      content: row.content,
      metadata: JSON.parse(row.metadata || '{}'),
      created_at: row.created_at,
      updated_at: row.updated_at
    }));
  }

  /**
   * 列出所有文字記憶
   * @param {number} limit - 返回數量
   * @param {number} offset - 偏移量
   * @returns {array} 記錄列表
   */
  listTextMemories(limit = 50, offset = 0) {
    const rows = this.db.prepare(`
      SELECT id, content, tags, type, created_at, updated_at
      FROM memory_text
      ORDER BY created_at DESC
      LIMIT ? OFFSET ?
    `).all(limit, offset);

    return rows.map(row => ({
      id: row.id,
      content: row.content,
      tags: JSON.parse(row.tags || '[]'),
      type: row.type,
      created_at: row.created_at,
      updated_at: row.updated_at
    }));
  }

  /**
   * 搜尋文字記憶 by tags
   * @param {string[]} tags - 標籤陣列
   * @param {number} limit - 返回數量
   * @returns {array} 匹配的記錄
   */
  searchByTags(tags, limit = 10) {
    const tagJson = JSON.stringify(tags);
    
    const rows = this.db.prepare(`
      SELECT * FROM memory_text
      WHERE tags LIKE ?
      ORDER BY created_at DESC
      LIMIT ?
    `).all(`%${tags[0]}%`, limit);

    return rows.map(row => ({
      id: row.id,
      content: row.content,
      tags: JSON.parse(row.tags || '[]'),
      type: row.type,
      created_at: row.created_at,
      updated_at: row.updated_at
    }));
  }

  /**
   * 獲取統計資訊
   * @returns {object} 統計數據
   */
  getStats() {
    const vectorCount = this.db.prepare(`
      SELECT COUNT(*) as count FROM memory_vectors
    `).get();

    const textCount = this.db.prepare(`
      SELECT COUNT(*) as count FROM memory_text
    `).get();

    return {
      vector_memory_count: vectorCount.count,
      text_memory_count: textCount.count,
      total_count: vectorCount.count + textCount.count
    };
  }

  /**
   * 關閉資料庫連接
   */
  close() {
    if (this.db) {
      this.db.close();
      console.log('[MemoryDB] Database connection closed');
    }
  }

  /**
   * 清除所有資料 (測試用)
   */
  clearAll() {
    this.db.exec(`
      DELETE FROM memory_vec_idx;
      DELETE FROM memory_vectors;
      DELETE FROM memory_text;
    `);
    console.log('[MemoryDB] All data cleared');
  }
}

// 匯出模組
module.exports = MemoryDB;

// 如果直接執行，進行測試
if (require.main === module) {
  const memDb = new MemoryDB();
  memDb.initialize();
  
  console.log('\n=== MemoryDB Test ===\n');
  
  // 測試新增向量記憶
  console.log('1. Testing addMemory...');
  const testEmbedding = new Array(768).fill(0).map(() => Math.random() * 2 - 1);
  const memory = memDb.addMemory(
    '這是一個測試記憶的內容',
    testEmbedding,
    { topic: 'test', importance: 5 }
  );
  console.log('   Added memory:', memory.chunk_id);
  
  // 測試搜尋
  console.log('2. Testing searchMemory...');
  const searchResults = memDb.searchMemory(testEmbedding, 5);
  console.log('   Found results:', searchResults.length);
  
  // 測試新增文字記憶
  console.log('3. Testing addTextMemory...');
  const textMemory = memDb.addTextMemory('這是文字記憶測試', ['test', 'demo'], 'general');
  console.log('   Added text memory:', textMemory.id);
  
  // 測試列表
  console.log('4. Testing listMemories...');
  const allMemories = memDb.listMemories(10);
  console.log('   Total memories:', allMemories.length);
  
  // 測試統計
  console.log('5. Testing getStats...');
  const stats = memDb.getStats();
  console.log('   Stats:', stats);
  
  // 測試刪除
  console.log('6. Testing deleteMemory...');
  const deleted = memDb.deleteMemory(memory.id);
  console.log('   Deleted:', deleted);
  
  memDb.close();
  console.log('\n=== Test Complete ===\n');
}
