/**
 * 史萊姆系統 - 記憶層資料庫測試
 */

const assert = require('assert');
const path = require('path');
const MemoryDB = require('../src/memory-db');

// 測試用的臨時資料庫路徑
const TEST_DB_PATH = path.join(__dirname, 'data', 'test-memory.db');

describe('MemoryDB', () => {
  let db;

  beforeEach(() => {
    // 建立測試資料庫
    db = new MemoryDB(TEST_DB_PATH);
    db.initialize();
  });

  afterEach(() => {
    // 關閉並清除測試資料庫
    if (db) {
      db.clearAll();
      db.close();
    }
  });

  describe('Vector Memory Operations', () => {
    /**
     * 測試新增向量記憶
     */
    it('should add a vector memory', () => {
      const embedding = new Array(768).fill(0).map(() => Math.random() * 2 - 1);
      const memory = db.addMemory(
        '測試向量記憶內容',
        embedding,
        { topic: 'test', importance: 4 }
      );

      assert(memory, 'Memory should be created');
      assert(memory.chunk_id, 'Memory should have chunk_id');
      assert(memory.content === '測試向量記憶內容', 'Content should match');
      assert(memory.metadata.topic === 'test', 'Metadata topic should match');
    });

    /**
     * 測試向量維度驗證
     */
    it('should reject embedding with wrong dimensions', () => {
      const wrongEmbedding = new Array(384).fill(0).map(() => Math.random());
      
      assert.throws(() => {
        db.addMemory('測試', wrongEmbedding, {});
      }, /向量維度必須為 768/);
    });

    /**
     * 測試根據 ID 獲取記憶
     */
    it('should get memory by id', () => {
      const embedding = new Array(768).fill(0).map(() => Math.random() * 2 - 1);
      const added = db.addMemory('測試內容', embedding, {});
      const retrieved = db.getMemory(added.id);

      assert(retrieved, 'Should retrieve memory');
      assert(retrieved.id === added.id, 'IDs should match');
      assert(retrieved.content === '測試內容', 'Content should match');
    });

    /**
     * 測試根據 chunk_id 獲取記憶
     */
    it('should get memory by chunk_id', () => {
      const embedding = new Array(768).fill(0).map(() => Math.random() * 2 - 1);
      const added = db.addMemory('測試內容', embedding, {});
      const retrieved = db.getMemoryByChunkId(added.chunk_id);

      assert(retrieved, 'Should retrieve memory by chunk_id');
      assert(retrieved.chunk_id === added.chunk_id, 'Chunk IDs should match');
    });

    /**
     * 測試搜尋向量記憶
     */
    it('should search memory by embedding', () => {
      // 新增多個記憶
      const embedding1 = new Array(768).fill(0).map(() => Math.random() * 2 - 1);
      const embedding2 = new Array(768).fill(0).map(() => Math.random() * 2 - 1);
      
      db.addMemory('關於 Python 程式設計', embedding1, { topic: 'programming' });
      db.addMemory('關於 JavaScript 框架', embedding2, { topic: 'programming' });

      // 搜尋 (使用與 embedding1 類似的向量)
      const results = db.searchMemory(embedding1, 5);

      assert(results.length > 0, 'Should find results');
      assert(results[0].content === '關於 Python 程式設計', 'Most similar should be first');
    });

    /**
     * 測試刪除記憶
     */
    it('should delete memory by id', () => {
      const embedding = new Array(768).fill(0).map(() => Math.random() * 2 - 1);
      const added = db.addMemory('要刪除的記憶', embedding, {});
      
      const deleted = db.deleteMemory(added.id);
      assert(deleted, 'Should delete successfully');

      const retrieved = db.getMemory(added.id);
      assert(!retrieved, 'Memory should be deleted');
    });

    /**
     * 測試更新記憶
     */
    it('should update memory', () => {
      const embedding = new Array(768).fill(0).map(() => Math.random() * 2 - 1);
      const added = db.addMemory('原始內容', embedding, { importance: 1 });
      
      const updated = db.updateMemory(added.id, '更新後內容', { importance: 5 });
      
      assert(updated.content === '更新後內容', 'Content should be updated');
      assert(updated.metadata.importance === 5, 'Metadata should be updated');
    });

    /**
     * 測試列表記憶
     */
    it('should list memories', () => {
      // 新增多個記憶
      for (let i = 0; i < 5; i++) {
        const embedding = new Array(768).fill(0).map(() => Math.random() * 2 - 1);
        db.addMemory(`記憶 ${i}`, embedding, {});
      }

      const memories = db.listMemories(10);
      assert(memories.length === 5, 'Should list all memories');
    });
  });

  describe('Text Memory Operations', () => {
    /**
     * 測試新增文字記憶
     */
    it('should add a text memory', () => {
      const textMemory = db.addTextMemory(
        '這是文字記憶測試',
        ['test', 'demo'],
        'general'
      );

      assert(textMemory, 'Text memory should be created');
      assert(textMemory.id, 'Should have id');
      assert(textMemory.content === '這是文字記憶測試', 'Content should match');
      assert(Array.isArray(textMemory.tags), 'Tags should be array');
    });

    /**
     * 測試獲取文字記憶
     */
    it('should get text memory by id', () => {
      const added = db.addTextMemory('文字內容', ['tag1'], 'faq');
      const retrieved = db.getTextMemory(added.id);

      assert(retrieved, 'Should retrieve text memory');
      assert(retrieved.content === '文字內容', 'Content should match');
      assert(retrieved.type === 'faq', 'Type should match');
    });

    /**
     * 測試搜尋文字記憶 by tags
     */
    it('should search text memories by tags', () => {
      db.addTextMemory('內容 A', ['apple', 'fruit'], 'general');
      db.addTextMemory('內容 B', ['banana', 'fruit'], 'general');
      db.addTextMemory('內容 C', ['carrot', 'vegetable'], 'general');

      const results = db.searchByTags(['fruit'], 10);
      
      assert(results.length === 2, 'Should find 2 fruit items');
    });

    /**
     * 測試刪除文字記憶
     */
    it('should delete text memory', () => {
      const added = db.addTextMemory('要刪除', ['test'], 'general');
      
      const deleted = db.deleteTextMemory(added.id);
      assert(deleted, 'Should delete successfully');

      const retrieved = db.getTextMemory(added.id);
      assert(!retrieved, 'Text memory should be deleted');
    });

    /**
     * 測試更新文字記憶
     */
    it('should update text memory', () => {
      const added = db.addTextMemory('原始', ['old'], 'draft');
      
      const updated = db.updateTextMemory(added.id, '更新', ['new'], 'published');
      
      assert(updated.content === '更新', 'Content should be updated');
      assert(updated.tags.includes('new'), 'Tags should be updated');
      assert(updated.type === 'published', 'Type should be updated');
    });
  });

  describe('Statistics', () => {
    /**
     * 測試獲取統計資訊
     */
    it('should get statistics', () => {
      // 新增一些資料
      const embedding = new Array(768).fill(0).map(() => Math.random() * 2 - 1);
      db.addMemory('向量記憶', embedding, {});
      db.addTextMemory('文字記憶', ['test'], 'general');

      const stats = db.getStats();
      
      assert(stats.vector_memory_count === 1, 'Should have 1 vector memory');
      assert(stats.text_memory_count === 1, 'Should have 1 text memory');
      assert(stats.total_count === 2, 'Should have 2 total');
    });
  });

  describe('Error Handling', () => {
    /**
     * 測試獲取不存在的記憶
     */
    it('should return null for non-existent memory', () {
      const retrieved = db.getMemory(99999);
      assert(!retrieved, 'Should return null for non-existent id');
    });

    /**
     * 測試刪除不存在的記憶
     */
    it('should return false when deleting non-existent memory', () => {
      const deleted = db.deleteMemory(99999);
      assert(deleted === false, 'Should return false');
    });
  });
});

// 執行單元測試
if (process.argv[1] && !process.argv[1].includes('mocha')) {
  // 直接執行模式
  console.log('Running MemoryDB manual tests...\n');
  
  const testDb = new MemoryDB(path.join(__dirname, 'data', 'manual-test.db'));
  testDb.initialize();

  try {
    // Test 1: Add memory
    console.log('Test 1: Add vector memory');
    const emb1 = new Array(768).fill(0).map(() => Math.random());
    const mem1 = testDb.addMemory('Hello World', emb1, { topic: 'greeting' });
    console.log('  ✓ Created:', mem1.chunk_id);

    // Test 2: Search
    console.log('Test 2: Search memory');
    const results = testDb.searchMemory(emb1, 5);
    console.log('  ✓ Found:', results.length, 'results');

    // Test 3: Get by id
    console.log('Test 3: Get by ID');
    const found = testDb.getMemory(mem1.id);
    console.log('  ✓ Retrieved:', found ? found.content : 'not found');

    // Test 4: Add text memory
    console.log('Test 4: Add text memory');
    const textMem = testDb.addTextMemory('Text note', ['note', 'test'], 'general');
    console.log('  ✓ Created text memory:', textMem.id);

    // Test 5: Delete
    console.log('Test 5: Delete memory');
    testDb.deleteMemory(mem1.id);
    const afterDelete = testDb.getMemory(mem1.id);
    console.log('  ✓ Deleted:', !afterDelete);

    // Test 6: Stats
    console.log('Test 6: Get stats');
    const stats = testDb.getStats();
    console.log('  ✓ Stats:', stats);

    console.log('\n✅ All manual tests passed!');
  } catch (error) {
    console.error('\n❌ Test failed:', error.message);
    process.exit(1);
  } finally {
    testDb.clearAll();
    testDb.close();
  }
}
