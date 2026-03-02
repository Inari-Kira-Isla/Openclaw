/**
 * 數據分析系統 - Analytics System
 * 使用分析 + 趨勢預測
 */

class AnalyticsSystem {
  constructor() {
    this.metrics = {
      requests: 0,
      errors: 0,
      responseTime: [],
      tokens: 0
    };
  }
  
  trackRequest(duration, tokens, hasError = false) {
    this.metrics.requests++;
    if (hasError) this.metrics.errors++;
    this.metrics.responseTime.push(duration);
    this.metrics.tokens += tokens;
    
    // Keep only last 1000
    if (this.metrics.responseTime.length > 1000) {
      this.metrics.responseTime = this.metrics.responseTime.slice(-1000);
    }
  }
  
  getStats() {
    const avgResponseTime = this.metrics.responseTime.reduce((a, b) => a + b, 0) / 
                           (this.metrics.responseTime.length || 1);
    
    return {
      requests: this.metrics.requests,
      errors: this.metrics.errors,
      errorRate: (this.metrics.errors / this.metrics.requests * 100).toFixed(2) + '%',
      avgResponseTime: avgResponseTime.toFixed(0) + 'ms',
      tokens: this.metrics.tokens
    };
  }
  
  predictTrend() {
    // Simple linear prediction based on recent data
    const recent = this.metrics.responseTime.slice(-100);
    if (recent.length < 10) return { trend: 'stable', confidence: 'low' };
    
    const avg = recent.reduce((a, b) => a + b, 0) / recent.length;
    const trend = avg > 500 ? 'degrading' : 'stable';
    
    return { trend, confidence: 'medium', avgResponseTime: avg };
  }
}

module.exports = new AnalyticsSystem();
