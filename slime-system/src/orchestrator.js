/**
 * 史萊姆系統 - 協調器
 * 協調記憶層、學習機制、進化引擎
 */

const path = require('path');

class WorkflowOrchestrator {
  constructor(options = {}) {
    this.memoryLayer = options.memoryLayer;
    this.learningMechanism = options.learningMechanism;
    this.evolutionEngine = options.evolutionEngine;
    this.stateManager = options.stateManager;
    this.scheduler = options.scheduler;
  }

  /**
   * 處理新規學習輸入
   */
  async handleNewLearning(input) {
    const state = await this.stateManager.create('NEW_LEARNING', {
      input,
      step: 'analyzing'
    });

    try {
      // 1. 儲存到記憶層
      await this.stateManager.update(state.id, { step: 'storing' });
      const memoryId = await this.memoryLayer.add(input.content, input.embedding, input.metadata);

      // 2. 觸發學習機制
      await this.stateManager.update(state.id, { step: 'learning' });
      await this.learningMechanism.learn(input);

      // 3. 檢查是否需要進化
      await this.stateManager.update(state.id, { step: 'checking_evolution' });
      const drift = await this.evolutionEngine.detectDrift();
      if (drift.needsImprovement) {
        await this.evolutionEngine.improve(drift);
      }

      await this.stateManager.complete(state.id);
      return { success: true, memoryId };
    } catch (error) {
      await this.stateManager.fail(state.id, error.message);
      throw error;
    }
  }

  /**
   * 處理記憶提取與複習
   */
  async handleRecall(query) {
    const results = await this.memoryLayer.search(query.embedding, query.limit);
    return results;
  }

  /**
   * 夜間記憶整合
   */
  async handleNightlyIntegration() {
    const state = await this.stateManager.create('NIGHTLY_INTEGRATION', { step: 'starting' });

    try {
      // 1. 效能分析
      await this.stateManager.update(state.id, { step: 'analyzing' });
      const performance = await this.evolutionEngine.analyze();

      // 2. 記憶整合
      await this.stateManager.update(state.id, { step: 'integrating' });
      await this.memoryLayer.consolidate();

      // 3. 清理
      await this.stateManager.update(state.id, { step: 'cleaning' });
      await this.memoryLayer.cleanup();

      await this.stateManager.complete(state.id);
      return { success: true, performance };
    } catch (error) {
      await this.stateManager.fail(state.id, error.message);
      throw error;
    }
  }
}

module.exports = { WorkflowOrchestrator };
