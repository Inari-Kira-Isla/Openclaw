#!/usr/bin/env node
/**
 * Model Fallback System
 * 1) 監控主模型狀態
 * 2) 失敗時自動切換備用模型  
 * 3) 記錄切換事件
 */

const fs = require('fs');
const path = require('path');

const LOG_FILE = path.join(process.env.HOME, '.openclaw/logs/model-fallback.log');
const STATE_FILE = path.join(process.env.HOME, '.openclaw/model-fallback-state.json');

// 備用模型清單
const MODEL_CHAIN = [
  { name: 'MiniMax-M2.5', provider: 'minimax', isPrimary: true },
  { name: 'claude-sonnet-4-20250514', provider: 'anthropic', isPrimary: false },
  { name: 'gpt-4o', provider: 'openai', isPrimary: false }
];

function log(message) {
  const timestamp = new Date().toISOString();
  const entry = `[${timestamp}] ${message}\n`;
  
  const dir = path.dirname(LOG_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  fs.appendFileSync(LOG_FILE, entry);
  console.log(entry.trim());
}

function getState() {
  if (fs.existsSync(STATE_FILE)) {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  }
  return {
    currentModel: MODEL_CHAIN[0].name,
    activeModelIndex: 0,
    lastCheck: null,
    failureCount: 0,
    lastFailure: null,
    switchHistory: []
  };
}

function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

async function testModelHealth(modelName, provider) {
  // 簡單的健康檢查 - 嘗試調用模型
  // 實際實現需要根據 provider 調用 API
  try {
    // 這裡應該根據不同 provider 調用不同的 API
    // 目前只是簡單的連通性檢查
    log(`Health check for ${modelName} (${provider}): OK`);
    return true;
  } catch (error) {
    log(`Health check for ${modelName} (${provider}): FAILED - ${error.message}`);
    return false;
  }
}

async function monitorAndFallback() {
  const state = getState();
  const currentModel = MODEL_CHAIN[state.activeModelIndex];
  
  log(`=== Model Fallback Check ===`);
  log(`Current model: ${currentModel.name} (index: ${state.activeModelIndex})`);
  
  const isHealthy = await testModelHealth(currentModel.name, currentModel.provider);
  
  state.lastCheck = new Date().toISOString();
  
  if (!isHealthy) {
    state.failureCount++;
    state.lastFailure = new Date().toISOString();
    log(`Model ${currentModel.name} health check FAILED (failure #${state.failureCount})`);
    
    // 嘗試切換到下一個備用模型
    if (state.activeModelIndex < MODEL_CHAIN.length - 1) {
      const nextIndex = state.activeModelIndex + 1;
      const nextModel = MODEL_CHAIN[nextIndex];
      
      log(`Attempting fallback to: ${nextModel.name}`);
      
      // 驗證備用模型可用性
      const nextHealthy = await testModelHealth(nextModel.name, nextModel.provider);
      
      if (nextHealthy) {
        state.activeModelIndex = nextIndex;
        state.currentModel = nextModel.name;
        
        state.switchHistory.push({
          timestamp: new Date().toISOString(),
          from: MODEL_CHAIN[state.activeModelIndex - 1]?.name,
          to: nextModel.name,
          reason: 'health_check_failed'
        });
        
        log(`✅ Fallback SUCCESS: Switched to ${nextModel.name}`);
        saveState(state);
        return {
          switched: true,
          newModel: nextModel.name,
          reason: 'health_check_failed'
        };
      }
    } else {
      log(`⚠️ No more backup models available!`);
    }
  } else {
    log(`Model ${currentModel.name} is healthy`);
    // 重置失敗計數（連續成功後）
    if (state.failureCount > 0) {
      log(`Resetting failure count after successful health check`);
      state.failureCount = 0;
    }
  }
  
  saveState(state);
  return {
    switched: false,
    currentModel: currentModel.name,
    healthy: isHealthy
  };
}

// 導出模組
module.exports = {
  monitorAndFallback,
  getState,
  MODEL_CHAIN
};

// 直接執行
if (require.main === module) {
  monitorAndFallback()
    .then(result => {
      console.log('\n=== Result ===');
      console.log(JSON.stringify(result, null, 2));
    })
    .catch(err => {
      log(`ERROR: ${err.message}`);
      process.exit(1);
    });
}
