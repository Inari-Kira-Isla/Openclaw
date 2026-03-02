/**
 * 安全系統 - Security System
 * 權限審計 + 異常檢測
 */

const fs = require('fs');
const path = require('path');

class SecuritySystem {
  constructor() {
    this.logPath = path.join(process.env.HOME, '.openclaw/logs/security.json');
    this.events = this.loadEvents();
  }
  
  loadEvents() {
    try {
      if (fs.existsSync(this.logPath)) {
        return JSON.parse(fs.readFileSync(this.logPath, 'utf-8'));
      }
    } catch (e) {}
    return [];
  }
  
  log(event) {
    const record = {
      ...event,
      timestamp: new Date().toISOString()
    };
    
    this.events.push(record);
    fs.writeFileSync(this.logPath, JSON.stringify(this.events.slice(-1000), null, 2));
    
    return record;
  }
  
  detectAnomalies() {
    const anomalies = [];
    const recent = this.events.slice(-100);
    
    // Check for failed logins
    const failedLogins = recent.filter(e => e.type === 'auth' && e.status === 'failed');
    if (failedLogins.length > 5) {
      anomalies.push({ type: 'failed_logins', count: failedLogins.length, severity: 'high' });
    }
    
    return anomalies;
  }
  
  audit() {
    return {
      totalEvents: this.events.length,
      recentEvents: this.events.slice(-10).map(e => ({ type: e.type, timestamp: e.timestamp })),
      anomalies: this.detectAnomalies()
    };
  }
}

module.exports = new SecuritySystem();
