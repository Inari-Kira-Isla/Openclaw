/**
 * 決策系統 - Decision System
 * AI 輔助決策建議
 */

class DecisionSystem {
  constructor() {
    this.decisions = [];
  }
  
  analyze(options, context) {
    // Simple decision analysis
    const scores = options.map(opt => ({
      option: opt,
      score: this.calculateScore(opt, context),
      reasoning: this.getReasoning(opt, context)
    }));
    
    scores.sort((a, b) => b.score - a.score);
    
    return {
      recommended: scores[0],
      alternatives: scores.slice(1),
      confidence: this.calculateConfidence(scores)
    };
  }
  
  calculateScore(option, context) {
    // Simple scoring algorithm
    let score = 50;
    
    if (option.priority === 'high') score += 20;
    if (option.impact === 'high') score += 20;
    if (option.risk === 'low') score += 10;
    
    return Math.min(100, score);
  }
  
  getReasoning(option, context) {
    return `基於 ${context} 的分析，${option.name} 建議得分 ${option.score}`;
  }
  
  calculateConfidence(scores) {
    if (scores.length < 2) return 'low';
    const gap = scores[0].score - scores[1].score;
    return gap > 20 ? 'high' : 'medium';
  }
  
  recordDecision(decision, outcome) {
    this.decisions.push({
      ...decision,
      outcome,
      timestamp: new Date().toISOString()
    });
  }
}

module.exports = new DecisionSystem();
