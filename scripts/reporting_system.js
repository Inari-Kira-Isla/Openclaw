/**
 * 報告系統 - Reporting System
 * 自動生成報告 (日/週/月)
 */

const fs = require('fs');
const path = require('path');

class ReportingSystem {
  constructor() {
    this.reportPath = path.join(process.env.HOME, '.openclaw/workspace/memory/reports/');
    if (!fs.existsSync(this.reportPath)) {
      fs.mkdirSync(this.reportPath, { recursive: true });
    }
  }
  
  generateDaily(stats) {
    const report = {
      type: 'daily',
      date: new Date().toISOString().split('T')[0],
      stats,
      generatedAt: new Date().toISOString()
    };
    
    return this.saveReport(report);
  }
  
  generateWeekly(stats) {
    const report = {
      type: 'weekly',
      week: this.getWeekNumber(),
      stats,
      generatedAt: new Date().toISOString()
    };
    
    return this.saveReport(report);
  }
  
  saveReport(report) {
    const filename = `${report.type}-${report.date || report.week}.json`;
    fs.writeFileSync(path.join(this.reportPath, filename), JSON.stringify(report, null, 2));
    return filename;
  }
  
  getWeekNumber() {
    const now = new Date();
    const start = new Date(now.getFullYear(), 0, 1);
    const diff = now - start;
    const week = Math.ceil(diff / (7 * 24 * 60 * 60 * 1000));
    return `${now.getFullYear()}-W${week}`;
  }
}

module.exports = new ReportingSystem();
