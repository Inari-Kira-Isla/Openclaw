/**
 * 史萊姆系統 - 範本更新器
 */

const fs = require('fs');
const path = require('path');

class TemplateUpdater {
  constructor(options = {}) {
    this.templateDir = options.templateDir || path.join(__dirname, '..', 'data', 'templates');
    this.templates = this.loadTemplates();
    this.abTests = [];
  }

  loadTemplates() {
    try {
      const file = path.join(this.templateDir, 'templates.json');
      return JSON.parse(fs.readFileSync(file, 'utf-8'));
    } catch {
      return {};
    }
  }

  saveTemplates() {
    fs.mkdirSync(this.templateDir, { recursive: true });
    const file = path.join(this.templateDir, 'templates.json');
    fs.writeFileSync(file, JSON.stringify(this.templates, null, 2));
  }

  /**
   * 更新範本
   */
  async update(templateId, newContent) {
    const oldContent = this.templates[templateId];
    
    // 建立 A/B 測試
    const test = {
      id: Date.now().toString(),
      templateId,
      oldContent,
      newContent,
      startTime: new Date().toISOString(),
      status: 'running'
    };

    this.abTests.push(test);
    
    // 漸進式替換 (先 10% 用戶)
    this.templates[templateId] = {
      content: newContent,
      version: (oldContent?.version || 0) + 1,
      rollout: 0.1,
      testId: test.id
    };

    this.saveTemplates();
    return { success: true, test };
  }

  /**
   * 完成 A/B 測試
   */
  completeTest(testId, winner) {
    const test = this.abTests.find(t => t.id === testId);
    if (!test) return;

    test.status = 'completed';
    test.winner = winner;
    test.endTime = new Date().toISOString();

    // 全面替換
    const template = this.templates[test.templateId];
    if (template) {
      template.content = winner === 'new' ? test.newContent : test.oldContent;
      template.rollout = 1.0;
      template.testId = null;
    }

    this.saveTemplates();
  }

  /**
   * 回滾
   */
  rollback(templateId) {
    const template = this.templates[templateId];
    if (!template?.version) return false;

    const versionFile = path.join(this.templateDir, `v${template.version - 1}.json`);
    try {
      const oldVersion = JSON.parse(fs.readFileSync(versionFile, 'utf-8'));
      this.templates[templateId] = oldVersion;
      this.saveTemplates();
      return true;
    } catch {
      return false;
    }
  }

  getTemplate(id) {
    return this.templates[id];
  }

  listTemplates() {
    return Object.keys(this.templates);
  }
}

module.exports = { TemplateUpdater };
