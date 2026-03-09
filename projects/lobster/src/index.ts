// Lobster System - Main Entry Point
import { NotionClient } from './notion';
import { Detector } from './detector';
import { Recorder } from './recorder';
import { ReviewEngine } from './review';
import { LobsterConfig, LobsterError, SuccessRecord, DetectionResult } from './types';

// 載入環境變數
import * as dotenv from 'dotenv';
import path from 'path';

// Load .env from lobster project directory
dotenv.config({ path: path.join(__dirname, '..', '.env') });

export class Lobster {
  private notion: NotionClient;
  private detector: Detector;
  private recorder: Recorder;
  private review: ReviewEngine;

  constructor(config: LobsterConfig) {
    this.notion = new NotionClient(config);
    this.detector = new Detector();
    this.recorder = new Recorder(this.notion);
    this.review = new ReviewEngine(this.notion);
  }

  // 自動偵測並記錄錯誤
  async autoDetectAndRecord(): Promise<number> {
    console.log('🔍 Running auto-detection...');
    
    const detections = await this.detector.detectAll();
    console.log(`   Found ${detections.length} potential issues`);
    
    let recorded = 0;
    for (const detection of detections) {
      await this.recorder.recordFromDetection(detection);
      recorded++;
    }

    console.log(`✅ Recorded ${recorded} new errors`);
    return recorded;
  }

  // 手動記錄錯誤
  async addError(error: Omit<LobsterError, 'id' | 'createdAt' | 'updatedAt'>): Promise<string> {
    return this.recorder.recordError(error);
  }

  // 手動記錄成功
  async addSuccess(success: Omit<SuccessRecord, 'id' | 'createdAt'>): Promise<string> {
    return this.recorder.recordSuccess(success);
  }

  // 行動前檢查
  async checkBeforeAction(action: string, context?: string) {
    console.log(`🔍 Checking before action: ${action}`);
    const preventions = await this.review.checkBeforeAction(action, context);
    
    if (preventions.length > 0) {
      console.log(`⚠️ Found ${preventions.length} related errors:`);
      for (const p of preventions) {
        console.log(`   [${p.severity.toUpperCase()}] ${p.title}`);
        console.log(`   → Prevention: ${p.prevention}`);
      }
    } else {
      console.log('✅ No related errors found');
    }
    
    return preventions;
  }

  // 獲取每日回顧
  async getDailyReview() {
    return this.review.getDailyReview();
  }

  // 獲取每週總結
  async getWeeklySummary() {
    return this.review.getWeeklySummary();
  }

  // 獲取統計
  async getStats() {
    return this.recorder.getStats();
  }
}

// CLI 入口
async function main() {
  const config: LobsterConfig = {
    notionApiKey: process.env.NOTION_API_KEY || '',
    databaseId: process.env.NOTION_ERROR_DB_ID || '',
    successDatabaseId: process.env.NOTION_SUCCESS_DB_ID || ''
  };

  if (!config.notionApiKey || !config.databaseId) {
    console.error('❌ Missing Notion configuration. Check .env file.');
    process.exit(1);
  }

  const lobster = new Lobster(config);
  const command = process.argv[2];

  switch (command) {
    case 'detect':
      await lobster.autoDetectAndRecord();
      break;
    
    case 'review':
      const daily = await lobster.getDailyReview();
      console.log('📋 Daily Review:', daily);
      break;
    
    case 'weekly':
      const weekly = await lobster.getWeeklySummary();
      console.log(weekly);
      break;
    
    case 'stats':
      await lobster.getStats();
      break;
    
    case 'check':
      const action = process.argv[3] || 'unknown';
      await lobster.checkBeforeAction(action, process.argv[4]);
      break;

    default:
      console.log(`
🦞 Lobster System - CLI

Usage:
  lobster detect           - Auto-detect and record errors
  lobster review          - Get daily review
  lobster weekly          - Get weekly summary
  lobster stats           - Get error statistics
  lobster check <action>  - Check before action
      `.trim());
  }
}

// 如果直接運行此文件
if (require.main === module) {
  main().catch(console.error);
}

export default Lobster;
