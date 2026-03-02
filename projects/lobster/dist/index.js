"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Lobster = void 0;
// Lobster System - Main Entry Point
const notion_1 = require("./notion");
const detector_1 = require("./detector");
const recorder_1 = require("./recorder");
const review_1 = require("./review");
// 載入環境變數
const dotenv = __importStar(require("dotenv"));
const path_1 = __importDefault(require("path"));
// Load .env from lobster project directory
dotenv.config({ path: path_1.default.join(__dirname, '..', '.env') });
class Lobster {
    constructor(config) {
        this.notion = new notion_1.NotionClient(config);
        this.detector = new detector_1.Detector();
        this.recorder = new recorder_1.Recorder(this.notion);
        this.review = new review_1.ReviewEngine(this.notion);
    }
    // 自動偵測並記錄錯誤
    async autoDetectAndRecord() {
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
    async addError(error) {
        return this.recorder.recordError(error);
    }
    // 手動記錄成功
    async addSuccess(success) {
        return this.recorder.recordSuccess(success);
    }
    // 行動前檢查
    async checkBeforeAction(action, context) {
        console.log(`🔍 Checking before action: ${action}`);
        const preventions = await this.review.checkBeforeAction(action, context);
        if (preventions.length > 0) {
            console.log(`⚠️ Found ${preventions.length} related errors:`);
            for (const p of preventions) {
                console.log(`   [${p.severity.toUpperCase()}] ${p.title}`);
                console.log(`   → Prevention: ${p.prevention}`);
            }
        }
        else {
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
exports.Lobster = Lobster;
// CLI 入口
async function main() {
    const config = {
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
exports.default = Lobster;
