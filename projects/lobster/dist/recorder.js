"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Recorder = void 0;
class Recorder {
    constructor(notion) {
        this.notion = notion;
    }
    // 記錄錯誤
    async recordError(error) {
        // 先檢查是否已經存在類似的錯誤
        const existing = await this.notion.searchErrors(error.title);
        if (existing.length > 0) {
            // 已經存在，增加發生次數
            const page = existing[0];
            const occurrenceProp = page.properties['發生次數'];
            const newCount = (occurrenceProp?.number || 1) + 1;
            console.log(`Error already exists (${newCount} occurrences): ${error.title}`);
            return page.id;
        }
        // 建立新記錄
        const id = await this.notion.createErrorRecord(error);
        console.log(`Error recorded: ${error.title}`);
        return id;
    }
    // 從偵測結果記錄錯誤
    async recordFromDetection(detection) {
        const error = {
            source: detection.source,
            severity: detection.severity,
            title: detection.title,
            description: detection.description,
            tags: detection.tags,
            status: 'open',
            occurrenceCount: 1
        };
        return this.recordError(error);
    }
    // 記錄成功
    async recordSuccess(success) {
        const id = await this.notion.createSuccessRecord(success);
        console.log(`Success recorded: ${success.title}`);
        return id;
    }
    // 解決錯誤
    async resolveError(errorId, solution, prevention) {
        await this.notion.updateErrorStatus(errorId, 'Resolved');
        console.log(`Error resolved: ${errorId}`);
    }
    // 獲取開放的錯誤
    async getOpenErrors() {
        const errors = await this.notion.getOpenErrors();
        console.log(`Open errors: ${errors.length}`);
    }
    // 獲取錯誤統計
    async getStats() {
        const stats = await this.notion.getErrorStats();
        console.log('Error Statistics:');
        console.log(`  Total: ${stats.total}`);
        console.log(`  Open: ${stats.open}`);
        console.log(`  Resolved: ${stats.resolved}`);
        console.log(`  By Severity:`, stats.bySeverity);
    }
}
exports.Recorder = Recorder;
exports.default = Recorder;
