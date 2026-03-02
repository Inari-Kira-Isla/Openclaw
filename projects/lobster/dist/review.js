"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ReviewEngine = void 0;
class ReviewEngine {
    constructor(notion) {
        this.notion = notion;
    }
    // 行動前檢查 - 檢索相關歷史錯誤
    async checkBeforeAction(action, context) {
        // 搜尋關鍵字
        const keywords = this.extractKeywords(action + ' ' + (context || ''));
        const results = [];
        for (const keyword of keywords) {
            const errors = await this.notion.searchErrors(keyword);
            for (const page of errors) {
                const titleProp = page.properties['標題'];
                const preventionProp = page.properties['預防措施'];
                const severityProp = page.properties['嚴重程度'];
                results.push({
                    errorId: page.id,
                    title: titleProp?.title?.[0]?.text?.content || 'Unknown',
                    prevention: preventionProp?.rich_text?.[0]?.text?.content || 'No prevention recorded',
                    severity: severityProp?.select?.name?.toLowerCase() || 'medium'
                });
            }
        }
        // 去重
        const unique = results.filter((v, i, a) => a.findIndex(t => t.errorId === v.errorId) === i);
        // 按嚴重程度排序
        return unique.sort((a, b) => {
            const severityOrder = { high: 0, medium: 1, low: 2 };
            return severityOrder[a.severity] - severityOrder[b.severity];
        });
    }
    // 每日回顧 - 獲取今日提醒
    async getDailyReview() {
        const stats = await this.notion.getErrorStats();
        const openErrors = await this.notion.getOpenErrors();
        // 簡單趨勢判斷（基於本週 vs 上週）
        // 實際應該從歷史數據計算，這裡暫時返回 stable
        const trend = stats.open > stats.resolved ? 'worsening' :
            stats.open < stats.resolved ? 'improving' : 'stable';
        return {
            openErrors: stats.open,
            highSeverity: stats.bySeverity.high || 0,
            recentErrors: openErrors.slice(0, 5),
            trend
        };
    }
    // 每週總結
    async getWeeklySummary() {
        const stats = await this.notion.getErrorStats();
        return `
📊 Lobster 每週總結

錯誤統計:
- 總錯誤數: ${stats.total}
- 開放中: ${stats.open}
- 已解決: ${stats.resolved}

嚴重程度分布:
- 🔴 高: ${stats.bySeverity.high || 0}
- 🟡 中: ${stats.bySeverity.medium || 0}
- 🟢 低: ${stats.bySeverity.low || 0}

趨勢: ${stats.open > stats.resolved ? '⚠️ 需要關注' : '✅ 持續改善'}
    `.trim();
    }
    // 從文字提取關鍵字
    extractKeywords(text) {
        // 簡單的分詞
        const words = text.toLowerCase()
            .replace(/[^\w\s]/g, ' ')
            .split(/\s+/)
            .filter(w => w.length > 2);
        // 去除常見詞
        const stopWords = ['error', 'failed', 'problem', 'issue', 'the', 'this', 'that'];
        return words.filter(w => !stopWords.includes(w));
    }
}
exports.ReviewEngine = ReviewEngine;
exports.default = ReviewEngine;
