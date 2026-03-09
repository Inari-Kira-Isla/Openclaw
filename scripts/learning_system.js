/**
 * 學習系統 - Learning System
 * 持續學習與模型優化
 */

const fs = require('fs');
const path = require('path');

class LearningSystem {
  constructor() {
    this.learningPath = path.join(process.env.HOME, '.openclaw/workspace/memory/learning.json');
    this.learnings = this.loadLearnings();
  }
  
  loadLearnings() {
    try {
      if (fs.existsSync(this.learningPath)) {
        return JSON.parse(fs.readFileSync(this.learningPath, 'utf-8'));
      }
    } catch (e) {}
    return [];
  }
  
  saveLearnings() {
    fs.writeFileSync(this.learningPath, JSON.stringify(this.learnings, null, 2));
  }
  
  learn(topic, content, source) {
    const learning = {
      id: Date.now(),
      topic,
      content,
      source,
      timestamp: new Date().toISOString(),
      status: 'new'
    };
    
    this.learnings.push(learning);
    this.saveLearnings();
    
    return learning;
  }
  
  getRecentLearnings(days = 7) {
    const cutoff = Date.now() - (days * 24 * 60 * 60 * 1000);
    return this.learnings.filter(l => new Date(l.timestamp).getTime() > cutoff);
  }
  
  getTopics() {
    return [...new Set(this.learnings.map(l => l.topic))];
  }
}

module.exports = new LearningSystem();
