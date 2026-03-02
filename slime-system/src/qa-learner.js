/**
 * 史萊姆系統 - QA 學習器
 */

const fs = require('fs');
const path = require('path');

class QALearner {
  constructor(options = {}) {
    this.qaStore = options.qaStore || path.join(__dirname, '..', 'data', 'qa-store.json');
    this.questions = this.loadQA();
  }

  loadQA() {
    try {
      return JSON.parse(fs.readFileSync(this.qaStore, 'utf-8'));
    } catch {
      return [];
    }
  }

  saveQA() {
    fs.mkdirSync(path.dirname(this.qaStore), { recursive: true });
    fs.writeFileSync(this.qaStore, JSON.stringify(this.questions, null, 2));
  }

  /**
   * 學習新問題
   */
  async learn(question, answer, metadata = {}) {
    const existing = this.findSimilar(question);
    
    if (existing) {
      // 更新現有答案
      existing.count = (existing.count || 0) + 1;
      existing.lastAnswer = answer;
      existing.lastSeen = new Date().toISOString();
    } else {
      // 新增問題
      this.questions.push({
        id: Date.now().toString(),
        question,
        answer,
        metadata,
        count: 1,
        createdAt: new Date().toISOString(),
        lastSeen: new Date().toISOString(),
        status: 'pending_review'
      });
    }

    this.saveQA();
    return { success: true };
  }

  findSimilar(question) {
    return this.questions.find(q => 
      q.question.toLowerCase().includes(question.toLowerCase().substring(0, 20))
    );
  }

  /**
   * 檢索問題答案
   */
  async retrieve(query) {
    const results = this.questions
      .filter(q => q.question.toLowerCase().includes(query.toLowerCase()))
      .sort((a, b) => (b.count || 0) - (a.count || 0))
      .slice(0, 5);
    
    return results;
  }

  /**
   * 標記為待審核
   */
  markForReview(id) {
    const q = this.questions.find(q => q.id === id);
    if (q) q.status = 'pending_review';
    this.saveQA();
  }

  /**
   * 審核通過
   */
  approve(id) {
    const q = this.questions.find(q => q.id === id);
    if (q) q.status = 'approved';
    this.saveQA();
  }

  getStats() {
    return {
      total: this.questions.length,
      pending: this.questions.filter(q => q.status === 'pending_review').length,
      approved: this.questions.filter(q => q.status === 'approved').length
    };
  }
}

module.exports = { QALearner };
