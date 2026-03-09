/**
 * API 系統 - API System
 * 外部 API 整合管理
 */

class APISystem {
  constructor() {
    this.apis = {
      notion: { name: 'Notion', status: 'active', calls: 0 },
      telegram: { name: 'Telegram', status: 'active', calls: 0 },
      minimax: { name: 'MiniMax', status: 'active', calls: 0 },
      ollama: { name: 'Ollama', status: 'active', calls: 0 }
    };
  }
  
  trackCall(apiName) {
    if (this.apis[apiName]) {
      this.apis[apiName].calls++;
    }
  }
  
  getStatus() {
    return Object.entries(this.apis).map(([key, api]) => ({
      ...api,
      id: key
    }));
  }
  
  getHealth() {
    const allActive = Object.values(this.apis).every(a => a.status === 'active');
    return {
      healthy: allActive,
      apis: this.getStatus()
    };
  }
}

module.exports = new APISystem();
